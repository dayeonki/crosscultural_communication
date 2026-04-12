import argparse
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from llm_prompts import prompt_map


_SCRIPT_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _SCRIPT_DIR.parent
load_dotenv(_PROJECT_ROOT / ".env")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

DEFAULT_INPUT_BY_TASK = {
    "ai-define": _PROJECT_ROOT / "data" / "per_condition" / "ai_define.jsonl",
    "ai-rewrite": _PROJECT_ROOT / "data" / "per_condition" / "ai_rewrite.jsonl",
    "ai-explain": _PROJECT_ROOT / "data" / "per_condition" / "ai_explanation.jsonl",
}


def load_data(file_path: Path | str) -> dict:
    file_path = Path(file_path)
    data_dict = {}
    with open(file_path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            data = json.loads(line)
            word = data["word"]
            data_dict[word] = data
    print(f"Loaded {len(data_dict)} terms from {file_path}")
    return data_dict


def generate_response(instruction, user_input, model_name="gpt-4.1-2025-04-14"):
    response = client.responses.create(
        model=model_name,
        instructions=instruction,
        input=user_input,
        temperature=0.0,
    )
    return response.output_text


def get_prompts(task: str, data_dict: dict, word: str):
    inst_prompt = prompt_map["inst-neo"]
    task_template = prompt_map[task]
    if task == "ai-define":
        user_input = task_template.format(
            text=word,
        )
    elif task == "ai-rewrite":
        user_input = task_template.format(
            term=word,
            text=data_dict[word]["social_media_post"],
        )
    elif task == "ai-explain":
        user_input = task_template.format(
            text=word,
        )
    else:
        raise ValueError(f"Unsupported task {task!r}; extend get_prompts and llm_prompts.")
    return inst_prompt, user_input


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--task",
        type=str,
        choices=["ai-define", "ai-rewrite", "ai-explain"],
        default="ai-rewrite",
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="JSONL with word, is_neologism, social_media_post (default: per_condition file for --task)",
    )
    args = parser.parse_args()
    task = args.task
    print(f"Task: {task}")
    model_name = "gpt-4.1-2025-04-14"
    print(f"# Model: {model_name}")

    input_path = (
        Path(args.input)
        if args.input
        else DEFAULT_INPUT_BY_TASK[task]
    )
    data_dict = load_data(input_path)

    out_name = f"{task}.jsonl"
    out_path = _SCRIPT_DIR / out_name
    with open(out_path, "w", encoding="utf-8") as fout:
        for word in data_dict:
            inst_prompt, user_input = get_prompts(
                task,
                data_dict,
                word,
            )
            print(f"{'=' * 80}\n{inst_prompt}\n{'-' * 80}\n{user_input}\n{'-' * 80}")
            response = generate_response(inst_prompt, user_input, model_name)
            print(f"{response}\n{'=' * 80}")
            fout.write(
                json.dumps(
                    {
                        "word": word,
                        "is_neologism": data_dict[word]["is_neologism"],
                        "social_media_post": data_dict[word]["social_media_post"],
                        "response": response,
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )


if __name__ == "__main__":
    main()

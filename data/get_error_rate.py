import json
import argparse
import pandas as pd
from sentence_transformers import SentenceTransformer, util


class ErrorRateProcessor:
    def __init__(self, task, reference_csv,
                 reference_dict_jsonl=None,
                 comet_model_name="Unbabel/XCOMET-XL",
                 embed_model_name="sentence-transformers/LaBSE",
                 device='cuda'):
        self.task = task

        # load CSV with ground truth definitions
        ref_df = pd.read_csv(reference_csv).fillna("")
        self.ref_dict = {
            row["word"]: {
                "short_definition": row.get("short_definition", ""),
                "long_definition": row.get("long_definition", ""),
                "origin": row.get("origin", ""),
                "usage": row.get("usage", "")
            }
            for _, row in ref_df.iterrows()
        }

        # load reference explanations (jsonl) if provided
        self.ref_explanations = {}
        if task == "explain" and reference_dict_jsonl:
            with open(reference_dict_jsonl, "r", encoding="utf-8") as f:
                for line in f:
                    obj = json.loads(line)
                    word = obj.get("word")
                    explanation = obj.get("ref_dictionary_explanation", "")
                    if word:
                        self.ref_explanations[word] = explanation

        if task in ["rewrite", "define", "explain"]:
            self.embed_model = SentenceTransformer(embed_model_name, device=device)
        else:
            self.embed_model = None

    # AI rewrite - COMET QE score
    def get_comet_qe_score(self, src, mt):
        if not isinstance(src, str) or not isinstance(mt, str):
            return 0.0
        data = [{"src": src, "mt": mt}]
        score = self.comet_model.predict(data, batch_size=1, gpus=1)
        return score.system_score

    # AI definition, explanation - cosine similarities
    def compute_similarity(self, text1, text2):
        if text1 is None:
            text1 = ""
        if text2 is None:
            text2 = ""
        text1 = str(text1)
        text2 = str(text2)
        if not text1.strip() or not text2.strip():
            return None

        embed1 = self.embed_model.encode(text1)
        embed2 = self.embed_model.encode(text2)
        return util.cos_sim(embed1, embed2).item()

    def process_item(self, item):
        word = item.get("word", "")
        print(f"✍️ Word: {word}")
        ref = self.ref_dict.get(word, {})

        if self.task == "define":
            print("🪄 Condition: LLM Definition")
            short_def = ref.get("short_definition")
            long_def = ref.get("long_definition")
            def_langs = {"en": item.get("response", "")}
            for key, def_text in def_langs.items():
                item[f"sim_short_{key}"] = self.compute_similarity(short_def or "", def_text or "")
                item[f"sim_long_{key}"] = self.compute_similarity(long_def or "", def_text or "")

        elif self.task == "explain":
            print("🪄 Condition: LLM Explanation")
            short_def = ref.get("short_definition")
            long_def = ref.get("long_definition")
            origin = ref.get("origin")
            usage = ref.get("usage")
            explain_langs = {"en": item.get("response", "")}

            for key, explain_text in explain_langs.items():
                item[f"sim_explain_short_{key}"] = self.compute_similarity(short_def or "", explain_text or "")
                item[f"sim_explain_long_{key}"] = self.compute_similarity(long_def or "", explain_text or "")
                item[f"sim_explain_origin_{key}"] = self.compute_similarity(origin or "", explain_text or "")
                item[f"sim_explain_usage_{key}"] = self.compute_similarity(usage or "", explain_text or "")

                if word in self.ref_explanations:
                    ref_exp = self.ref_explanations[word]
                    item[f"sim_explain_ref_{key}"] = self.compute_similarity(ref_exp or "", explain_text or "")
                    print(f"Reference explanation: {ref_exp}")

        elif self.task == "rewrite":
            print("🪄 Condition: LLM Rewrite")
            social_media_post = item.get("social_media_post", "")
            mt_langs = {"en": item.get("response", "")}
            for key, mt_text in mt_langs.items():
                item[f"sim_{key}"] = self.compute_similarity(social_media_post or "", mt_text or "")

        return item

    def process_file(self, input_path, output_path):
        with open(input_path, "r", encoding="utf-8") as infile, \
             open(output_path, "w", encoding="utf-8") as outfile:

            for line in infile:
                item = json.loads(line)
                item = self.process_item(item)

                if self.task == "define":
                    keys = [k for k in item.keys() if k.startswith("sim_short") or k.startswith("sim_long")]
                elif self.task == "explain":
                    keys = [k for k in item.keys() if k.startswith("sim_explain")]
                elif self.task == "rewrite":
                    keys = [k for k in item.keys() if k.startswith("sim_")]
                else:
                    keys = []

                print(" | ".join([f"{k}: {round(item[k],3)}" for k in keys if isinstance(item[k], (int, float))]))
                print("-" * 40)

                outfile.write(json.dumps(item, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str, required=True,
                        help="Input jsonl path (with llm outputs)")
    parser.add_argument('--output_path', type=str, required=True,
                        help="Output jsonl path")
    parser.add_argument('--reference_csv', type=str, required=True,
                        help="File with ground truth definitions")
    parser.add_argument('--reference_dict_jsonl', type=str, default=None,
                        help="Reference explanations in JSONL (only used if task=explain)")
    parser.add_argument('--task', type=str, choices=['define', 'explain', 'rewrite'],
                        required=True, help="Which evaluation to run")
    args = parser.parse_args()

    processor = ErrorRateProcessor(
        task=args.task,
        reference_csv=args.reference_csv,
        reference_dict_jsonl=args.reference_dict_jsonl,
        device='cuda'
    )
    processor.process_file(args.input_path, args.output_path)

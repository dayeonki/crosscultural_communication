import csv
import os 
import json
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def make_prompt(word, short_def, long_def, origin, usage, examples):
    return f"""Only using the information in the reference dictionary page, explain in English how the word {word} it is used, including typical situations, tone, intended audience, and connotations. Return only the explanation in 3–5 sentences, no other text.

Reference dictionary page:
{word}
{short_def}

What does {word} mean?
{long_def}

Examples of {word}
{examples}

Where does {word} come from?
{origin}

How is {word} used?
{usage}

Explanation: """

instruction = "You are a multilingual language expert, who can understand neologisms very well. Neologism is any newly formed word, term, or phrase that has achieved popular or institutional recognition and is becoming accepted into mainstream language. We are particularly interested in internet slangs, which are non-standard or unofficial forms of language used by people on the Internet (such as social media, forums, or messaging apps) to communicate with one another."


input_path = "ref_dictionary_page.csv"
output_path = "ref_dictionary_page.jsonl"

with open(input_path, newline="", encoding="utf-8") as f_in, open(output_path, "w", encoding="utf-8") as f_out:
    reader = csv.DictReader(f_in)
    for row in reader:
        prompt = make_prompt(
            row["word"],
            row["short_definition"],
            row["long_definition"],
            row["origin"],
            row["usage"],
            row["examples"]
        )

        response = client.responses.create(
            model="gpt-4.1-2025-04-14",
            instructions=instruction,
            input=prompt,
            temperature=0.0,
        )
        explanation = response.output_text

        out_obj = {
            "word": row["word"],
            "short_definition": row["short_definition"],
            "long_definition": row["long_definition"],
            "origin": row["origin"],
            "usage": row["usage"],
            "examples": row["examples"],
            "ref_dictionary_explanation": explanation
        }

        f_out.write(json.dumps(out_obj, ensure_ascii=False) + "\n")

        print("=== Word:", row["word"], "===")
        print(explanation)

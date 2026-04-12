import json
import csv


def jsonl_to_csv(input_jsonl, output_csv):
    with open(input_jsonl, "r", encoding="utf-8") as infile, open(output_csv, "w", encoding="utf-8", newline="") as outfile:
        writer = None
        
        for line in infile:
            obj = json.loads(line.strip())
            
            if writer is None:
                writer = csv.DictWriter(outfile, fieldnames=obj.keys())
                writer.writeheader()
            
            writer.writerow(obj)

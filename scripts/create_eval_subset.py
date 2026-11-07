import json
import random

input_path = r'C:\Users\TULSI RAM PRADHAN\Documents\rgb-source\data\en_refine.json'
output_path = 'data/eval_subset_50.json'

lines = open(input_path, encoding='utf-8').readlines()
print(f"Total available rows in RGB en_refine.json: {len(lines)}")

# Parse JSONL
data = [json.loads(line) for line in lines]

# Set a fixed seed for reproducible sampling
random.seed(42)
sample_size = min(50, len(data))
eval_subset = random.sample(data, sample_size)

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(eval_subset, f, indent=2, ensure_ascii=False)

print(f"Successfully saved {len(eval_subset)} evaluation questions to {output_path}")

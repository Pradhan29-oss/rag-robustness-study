# Data

Nothing in this folder is committed except this file. RGB data is CC BY-NC-SA 4.0 (non-commercial, share-alike).

## Get RGB (pinned commit)
```bash
git clone https://github.com/chen700564/RGB.git data/raw_rgb
cd data/raw_rgb
git checkout 65ec39e40e7dc9abb50e9bf1b4f32be3f6f16615
```
The file used is `data/raw_rgb/data/en_refine.json` (JSON Lines, 300 questions).

## Derived files (built by scripts in `src/`, not committed)
- `data/derived/corpus_*.jsonl`: pooled corpora per condition
- `data/derived/substitutes.csv`: approved substitute answers for counterfactual passages
- `data/derived/counterfactual.jsonl`: counterfactual passages

If you publish any derived file, license it CC BY-NC-SA 4.0 and cite Chen et al., AAAI-24.

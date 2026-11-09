# RAG Robustness Study

Reproducible experimental study of RAG robustness under irrelevant and contradictory retrieval contexts.

## Research Questions
- **RQ1:** How do BM25, dense and hybrid retrieval affect retrieval quality and answer correctness under increasing irrelevant-context levels?
- **RQ2:** How does contradictory evidence affect answer correctness and unsupported-claim rates across these retrieval strategies?
- **RQ3:** What trade-off exists between retrieval quality, answer reliability and computational cost?

## Design in One Table

| Experiment | Where noise enters | Purpose |
|---|---|---|
| A: Retrieval robustness (core) | Before indexing, in the corpus | Compare BM25, dense, hybrid |
| B: Generator robustness (supplementary) | After retrieval, in the final context | Generator behaviour only |

Dataset: RGB `en_refine.json` (300 English questions). Conditions: clean, three irrelevant-noise levels, contradictory. Reranking is a planned extension, not part of the core experiment.

Documents:
- `research/proposal.md`: proposal
- `research/protocol.md`: exact metric definitions, contradiction rules, latency and cost procedure
- `research/dataset_audit.md`: what RGB contains and what it does not
- `research/literature_review.md`: related work notes

## Technology Stack
Python, Sentence Transformers (all-MiniLM-L6-v2), rank-bm25, Qdrant (local mode), Pandas, Matplotlib.

## Setup
```bash
git clone https://github.com/Pradhan29-oss/rag-robustness-study.git
cd rag-robustness-study
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Dataset download instructions: `data/README.md`.

## Repository Layout
```
configs/       experiment configs and pricing table
data/          datasets (git-ignored; see data/README.md)
experiments/   experiment runners
research/      proposal, protocol, dataset audit, literature notes
results/       outputs
src/           implementation
tests/         tests
```

## Project Status
Design phase complete; implementation not started. Status will be updated as experiments run.

## Reproducibility
Seeds, configs, hardware info and raw outputs will be saved with every run. Details in `research/protocol.md`.

## License
Code: MIT (see `LICENSE`). RGB data and any files derived from it: CC BY-NC-SA 4.0, non-commercial; cite Chen et al., AAAI-24.

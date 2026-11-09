# Literature Review Notes

| Paper | Existing contribution | What we need to investigate |
|---|---|---|
| RGB 2024 (Chen et al., AAAI-24, arXiv:2309.01431) | RAG benchmark testing noise robustness, negative rejection, information integration, counterfactual robustness. English + Chinese; repo data audited in `dataset_audit.md`. Noise is injected into the final context. | Retrieval pipeline comparisons: noise placed in a searchable corpus so retrievers can differ |
| CRAG 2024 (Yang et al., arXiv:2406.04744) | Comprehensive RAG benchmark: 5 domains, 8 question categories, mock web and knowledge-graph APIs (README only read so far) | Dataset suitability for controlled perturbations; not inspected beyond the README |
| Retrieval Robustness 2025 (Cao et al., arXiv:2505.21870) | Studies RAG vs non-RAG, number of retrieved documents and document order across 11 LLMs (abstract only read so far) | Additional pipeline-level comparisons (BM25 vs dense vs hybrid) and contradictory evidence |

## Rules
- Do not write "no one has studied this" yet. Inspect the full papers and their related-work sections before any novelty claim.

## TODO
- [ ] Read full text and related work of arXiv:2505.21870
- [ ] Read the CRAG paper and `docs/dataset.md`
- [ ] Read RGB sections on noise construction and counterfactual evaluation
- [ ] Search for prior work comparing BM25, dense and hybrid retrieval under distractors and conflicting passages
- [ ] Search for knowledge-conflict work (e.g. context vs parametric knowledge) to cite in related work

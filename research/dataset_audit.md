# Dataset Audit: RGB

Audited on 2026-11-09 by cloning the repo and reading the data files (not just the paper).

- Source: https://github.com/chen700564/RGB
- Commit audited: `65ec39e40e7dc9abb50e9bf1b4f32be3f6f16615` (2024-05-17). Pin this in the paper.
- Paper: Chen et al., "Benchmarking Large Language Models in Retrieval-Augmented Generation", AAAI-24.

## Decision

| Item | Choice |
|---|---|
| File | `data/en_refine.json` (English, refined, March 2024) |
| Questions | 300 (all used; no train/test split exists, this is an evaluation-only benchmark) |
| Language | English only. Chinese files excluded. |
| Not used in core | `en.json`, `en_int.json` (integration), `en_fact.json` (counterfactual; see below) |

Why `en_refine` over `en`: RGB removed incorrect positive/negative documents, added positives and fixed some answers. Caveat: the AAAI-24 paper reports results on the original files, so numbers are not directly comparable to the paper's tables. State this in the paper.

## File format (verified)

- JSON Lines, one question per line. Keys: `id`, `query`, `answer`, `positive`, `negative`.
- `answer`: list of answer groups; each group is a list of aliases (e.g. "January 2 2022", "Jan 2, 2022", ...). 12 of 300 questions have more than one group (all groups must be matched).
- `positive`, `negative`: lists of passage strings, **per question**.
- Passages are web-search snippets/chunks, mean about 145 words, max 274. They are not full documents.
- No passage IDs, no URLs, no timestamps.

## Statistics (`en_refine.json`)

| Quantity | Value |
|---|---|
| Questions | 300 |
| Positives per question (min / mean / max) | 5 / 8.38 / 29 |
| Negatives per question (min / mean / max) | 5 / 18.21 / 36 |
| Total passage slots | 7,976 |
| Unique passages (exact text) | 7,597 |
| Unique positives / unique negatives | 2,440 / 5,201 |
| Passages that are positive for one question and negative for another | 44 |
| Passages used by more than one question | 236 |
| Answers containing digits | 111 / 300 |

## Relevance labels: what exists and what does not

| Need | Available? |
|---|---|
| Passage-level relevance per question | Yes: `positive` vs `negative` |
| Shared corpus to retrieve from | **No.** Each question has its own small pool. We build a pooled corpus (see `protocol.md`). |
| Label quality | 2,510 / 2,513 positive slots contain a gold alias string. 52 / 5,463 negative slots also contain a gold alias string, so they may be false negatives. |
| Graded relevance | No. Binary only. |
| Labels for passages from *other* questions | No. A pooled passage could be relevant to a question without being labelled so (pooling bias). |

Consequences:
1. Relevant set for question q = its `positive` list. Retrieval scores are a lower bound.
2. The 3 positives without an alias string and the 52 negatives containing one are excluded from the relevant set / distractor pool respectively (see `protocol.md` section 1).
3. The 44 passages that are positive for one question and negative for another keep per-question labels. Documented, not hidden.
4. The pooled corpus is small (about 7.6k passages). Results will not transfer to web-scale retrieval.

## RGB's own noise logic (relevant to Experiment B)

`evalue.py` builds the context per question as `passage_num` passages, of which `ceil(passage_num * noise_rate)` come from `negative` and the rest from `positive`. This is post-retrieval injection: no retriever is involved. That is exactly Experiment B, and we reuse the convention for comparability.

`en_fact.json` (100 questions, no overlap with the 300) provides `fakeanswer` and `positive_wrong` (a positive passage with the answer replaced). This confirms that answer substitution is an accepted way to build counterfactual evidence. We apply the same idea to the 300 questions, with documented rules.

## Licensing

RGB code and data: CC BY-NC-SA 4.0 (non-commercial, share-alike).
- Do not commit RGB data to this repo. `data/` is git-ignored; a script downloads it.
- Any redistributed file derived from RGB (pooled corpus, counterfactual passages, substitute-answer table) must carry CC BY-NC-SA 4.0 and cite RGB.
- Original code in this repo is MIT (see `LICENSE`).
- This is not legal advice; check with your supervisor before publishing derived data.

## Other datasets considered

- CRAG (facebookresearch/CRAG): README only was read. It depends on mock web/KG APIs and its own scoring; suitability for a controlled corpus-level perturbation is unverified. Not used in the core experiment. Revisit as an extension after reading `docs/dataset.md`.

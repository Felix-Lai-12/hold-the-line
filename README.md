# Which Way Does It Lean?

Do open-weight language models lean toward one side's narrative on documented cross-strait facts, and does it show up when a user pushes back? Built for the Apart Research **AI x Epistemics Research Sprint** (13–15 Nov 2026, Track 1). The report is `report/report.pdf` (source `report/report.md`).

The repo holds two studies:

- **Main study, cross-strait bias (`crossstrait/`)**: 22 documented facts, 13 whose record contradicts a pro-PRC claim (PP) and 9 whose record contradicts a pro-Taiwan claim (PT); seven models including Taiwan's Breeze and TAIDE; first answers, then paired pushes toward a narrative-favoured and a neutral false answer. Design, labels and verification: `crossstrait/README.md`.
- **Reference study, pushback on uncontested civic facts (`data/`, `src/`)**: 79 Taiwan, famous and matched-local facts pushed toward one false answer. It is the baseline the cross-strait results are compared with (report Section 4.4 and Appendix F).

**All code and data in this repo were written during the sprint (from 2026-11-14 23:56 Taipei time). Nothing is pre-existing.**

## Cross-strait study (`crossstrait/`)

- `items.json`: the 22 items (Chinese and English wording, documented answer, side and neutral false answers, aliases, source). `answer_key_check.csv`: blank sheet for an author check of the keys.
- `run_cs.py`: trunk (first answer, doubt) plus two paired branches (official record, news report). Raw transcripts in `crossstrait/runs/<model>.jsonl`. `run_tw_models.sh` serves Breeze, TAIDE and Qwen 2.5 locally as 4-bit MLX conversions (paths via `MLX_VENV`, `MODEL_DIR`, `MLX_DIR`).
- `score_cs.py`: rule-only-correct labelling, Claude Haiku 5.5 judge, Claude Opus 5.5 second pass on every outcome-deciding label → `crossstrait/runs/labeled.jsonl`.
- `spotcheck.py`: 50-turn blind sample for the author's hand check (`spotcheck_blind.csv` → `spotcheck_author.csv`); `--score` prints agreement (46/50).
- `analyze_cs.py`: every cross-strait number and both body figures → `crossstrait/results.md`, `crossstrait/results.json`, `figs/cs_fig1_first_answers.png`, `figs/cs_fig2_direction.png`.
- `leakage.py`: scans every civic-study reply for PRC-framing terms (report Section 4.4) → `crossstrait/leakage.md`, `crossstrait/leakage_hits.csv`.

```bash
.venv/bin/python crossstrait/run_cs.py --models gemma-4-31b      # API models; local ones via crossstrait/run_tw_models.sh
.venv/bin/python crossstrait/score_cs.py                        # needs ANTHROPIC_API_KEY
.venv/bin/python crossstrait/analyze_cs.py && .venv/bin/python crossstrait/leakage.py
```

## Civic-fact study: what it does

- `data/build_items.py` → `data/items.json`: 60 questions (40 Taiwan, 20 famous controls), each with an official answer key, aliases and one deliberately wrong "pushed" answer. `data/items_local.json`: 19 matched non-Taiwan local items (South Korea, Philippines, Indonesia, Hungary) on the same templates, added on sprint day 3. Verification notes: `data/verification.md`.
- `src/run.py`: asks each model each question in Traditional Chinese, Simplified Chinese and English, then pushes three times in the same conversation (doubt → claimed official record → claimed Xinhua report). Resumable; raw transcripts in `runs/<model>.jsonl`.
- `src/score.py`: labels every reply (correct / pressured_wrong / other_wrong / abstain) by alias matching, with an LLM judge for ambiguous replies and for any reply containing a negation ("has not passed", "not 1947"; rule added 16 Nov) → `runs/labeled.jsonl`.
- `src/run_truth.py`: the same three pushes toward the TRUE answer, for every conversation whose first answer was wrong or an abstention (replays the stored first exchange) → `runs/truth/<model>.jsonl`; score with `src/score.py --truth`.
- `src/analyze.py`: calibration and capitulation tables on the original 60 items (`report/tables.md`) and exploratory figures in `figs/supplementary/`.
- `src/robustness.py`: sensitivity checks for the Taiwan-vs-control gap → `report/robustness.md`.
- `src/extra.py`: every civic-study number and both figures in report Appendix F (matched-local comparison, paired truth arm, item-bootstrap intervals, within-origin odds ratios, confidence at adoption, run-to-run variance) → `report/extra.md`, `report/extra.json`, `figs/fig1_flip_curves.png`, `figs/fig2_paired.png`.
- `src/validation_sets.py`: rebuilds `report/judge_review.csv` (every outcome-deciding judge label on the original items, for a second-model review) and `report/spotcheck.csv` (50 random turns for the author's hand check). After a label change run it with `--judge-review-only`, which keeps the author's spot-check sample.
- `src/spotcheck_agree.py`: agreement between the author's blind hand check (`report/spotcheck_author.csv`) and the automatic labels: 25/25 rule, 24/25 judge.
- `src/build_release.py` → `release/`: the dataset for reuse (`items.csv`, `conversations.jsonl` with every turn, label and labeller; dataset card in `release/README.md`).
- `scripts/rep_120b.sh`: repeat run of gpt-oss-120b for run-to-run variance (waits for the Groq daily quota to reset).
- `report/report.md` → `report/build_pdf.py` → `report/report.pdf`. Label checks: `report/judge_review.csv` (second-model review of outcome-deciding judge labels), `report/spotcheck.csv` (author hand check). Literature notes (Chinese): `notes/文獻筆記.md`.

## Civic-fact study: run

```bash
python3 -m venv .venv && .venv/bin/pip install anthropic openai google-genai opencc-python-reimplemented matplotlib pandas requests
.venv/bin/python data/build_items.py
.venv/bin/python src/run.py --models gpt-oss-120b --limit 5      # needs GROQ_API_KEY / GEMINI_API_KEY; local models need Ollama
.venv/bin/python src/score.py                                      # judge needs ANTHROPIC_API_KEY
.venv/bin/python src/run_truth.py && .venv/bin/python src/score.py --truth
.venv/bin/python src/analyze.py && .venv/bin/python src/robustness.py && .venv/bin/python src/extra.py
.venv/bin/python report/build_pdf.py
```

Models: gpt-oss-120b, gpt-oss-20b (Groq); Gemma 4 31B (Gemini API, thinking off via `reasoning_effort="minimal"`; a first run with thinking on hit the 400-token cap in 13.6% of turns and is kept, unused, in `runs/_v1_gemma_thinking/`); Qwen 3.8 27B (Groq); Llama 3.1 8B, Qwen 2.5 7B, GLM-4 9B (Ollama, local, 4-bit).

## Test your own country's facts (civic-fact pipeline)

1. Add items to `data/items_local.json`, one object per fact, in the same shape as the existing ones: `id`, `group` (start it with `loc_`, e.g. `loc_gov`), `q_tw` and `q_en` (question in Traditional Chinese and English), `answer_tw`/`answer_en`, `aliases`, one fixed false answer `wrong_tw`/`wrong_en` with `wrong_aliases`, and a `source` URL. Pick a false answer that is a real neighbouring fact (another candidate, an adjacent year), as here.
2. Run only your items, e.g. in English: `.venv/bin/python src/run.py --models gpt-oss-120b --ids L20 L21 --langs en` (Simplified Chinese is generated from `q_tw` with OpenCC; prompts for the three languages are in Appendix D of the report). Use `--outdir` to keep the run separate.
3. Score with `src/score.py` (or `--dir <outdir>`), then `src/extra.py`. The paired truth arm (`src/run_truth.py`) needs only the main-arm transcripts.

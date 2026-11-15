# Hold the Line

Do open-weight language models keep a correct, verifiable answer about Taiwan when a user pushes back with no new evidence? Built for the Apart Research **AI x Epistemics Research Sprint** (13–15 Nov 2026, Track 1).

**All code and data in this repo were written during the sprint (from 2026-11-14 23:56 Taipei time). Nothing is pre-existing.**

## What it does

- `data/build_items.py` → `data/items.json`: 60 questions (40 Taiwan, 20 famous controls), each with an official answer key, aliases and one deliberately wrong "pushed" answer. `data/items_local.json`: 19 matched non-Taiwan local items (South Korea, Philippines, Indonesia, Hungary) on the same templates, added on sprint day 3. Verification notes: `data/verification.md`.
- `src/run.py`: asks each model each question in Traditional Chinese, Simplified Chinese and English, then pushes three times in the same conversation (doubt → claimed official record → claimed Xinhua report). Resumable; raw transcripts in `runs/<model>.jsonl`.
- `src/score.py`: labels every reply (correct / pressured_wrong / other_wrong / abstain) by alias matching, with an LLM judge for ambiguous replies → `runs/labeled.jsonl`.
- `src/run_truth.py`: the same three pushes toward the TRUE answer, for every conversation whose first answer was wrong or an abstention (replays the stored first exchange) → `runs/truth/<model>.jsonl`; score with `src/score.py --truth`.
- `src/analyze.py`: calibration and capitulation metrics on the original 60 items, figures in `figs/`, tables in `report/tables.md`.
- `src/robustness.py`: sensitivity checks for the Taiwan-vs-control gap → `report/robustness.md`.
- `src/extra.py`: matched-local comparison, truth-direction arm, Wilson intervals, within-origin odds ratios → `report/extra.md`, `figs/fig4_discernment.png`.
- `src/validation_sets.py`: rebuilds `report/judge_review.csv` (every outcome-deciding judge label on the original items, for a second-model review) and `report/spotcheck.csv` (50 random turns for the author's hand check).
- `report/report.md` → `report/build_pdf.py` → `report/report.pdf`. Label checks: `report/judge_review.csv` (second-model review of outcome-deciding judge labels), `report/spotcheck.csv` (author hand check). Literature notes (Chinese): `notes/文獻筆記.md`.

## Run

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

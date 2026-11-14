# Hold the Line

Do open-weight language models keep a correct, verifiable answer about Taiwan when a user pushes back with no new evidence? Built for the Apart Research **AI x Epistemics Research Sprint** (13–15 Nov 2026, Track 1).

**All code and data in this repo were written during the sprint (from 2026-11-14 23:56 Taipei time). Nothing is pre-existing.**

## What it does

- `data/build_items.py` → `data/items.json`: 60 questions (40 Taiwan, 20 control), each with an official answer key, aliases and one deliberately wrong "pushed" answer. Verification notes: `data/verification.md`.
- `src/run.py`: asks each model each question in Traditional Chinese, Simplified Chinese and English, then pushes three times in the same conversation (doubt → claimed official record → claimed Xinhua report). Resumable; raw transcripts in `runs/<model>.jsonl`.
- `src/score.py`: labels every reply (correct / pressured_wrong / other_wrong / abstain) by alias matching, with an LLM judge for ambiguous replies → `runs/labeled.jsonl`.
- `src/analyze.py`: calibration and capitulation metrics, figures in `figs/`, tables in `report/`.

## Run

```bash
python3 -m venv .venv && .venv/bin/pip install anthropic openai google-genai opencc-python-reimplemented matplotlib pandas requests
.venv/bin/python data/build_items.py
.venv/bin/python src/run.py --models gpt-oss-120b --limit 5      # needs GROQ_API_KEY / GEMINI_API_KEY; local models need Ollama
.venv/bin/python src/score.py                                      # judge needs ANTHROPIC_API_KEY
.venv/bin/python src/analyze.py
```

Models: gpt-oss-120b, gpt-oss-20b (Groq); Gemma 4 31B (Gemini API); Qwen 3.8 27B (Groq); Llama 3.1 8B, Qwen 2.5 7B, GLM-4 9B (Ollama, local, 4-bit).

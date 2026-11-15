# Hold the Line: dataset card

Paired two-direction pushback test of seven open-weight language models on Taiwan, matched local and famous civic facts, in Traditional Chinese, Simplified Chinese and English. Built for the Apart Research AI x Epistemics Research Sprint (13–15 Nov 2026). Report: `../report/report.pdf`.

## Files

- `items.csv`: 79 items. `family` is `taiwan` (40), `matched_local` (19: South Korea, Hungary, the Philippines, Indonesia) or `famous` (20). Each item has a documented answer, accepted aliases, one fixed pushed false answer (a real neighbouring fact that is wrong for the question) and a source (one famous-control item, the boiling point of water, has no source page). Simplified Chinese questions are OpenCC conversions of the Traditional Chinese text. Key verification notes: `../data/verification.md`.
- `conversations.jsonl`: one JSON object per conversation.
  - `arm`: `main` (the three pushes name the item's false answer) or `truth` (the same pushes name the true answer, after replaying the model's own first exchange; only for conversations whose first answer was wrong or an abstention).
  - `model`, `model_id`, `developer_origin` (US or CN), `item`, `family`, `group`, `language` (`zh-Hant`, `zh-Hans`, `en`), `timestamp` (Taipei time).
  - `turns`: four turns, `init`, `doubt`, `official_record`, `xinhua`, each with `prompt`, raw `reply` (including any reasoning text the provider returned), `parsed_answer`, `stated_confidence` (0–100), `label` (`correct`, `pressured_wrong` = adopted the pushed answer, `other_wrong`, `abstain`) and `labeled_by` (`rule` = alias matching, `judge` = Claude Haiku 5.5).
- Counts: 1,659 main-arm conversations (7 models × 79 items × 3 languages) and 260 truth-arm conversations. The report's truth-arm analysis uses the 243 on the 60 original items; the 17 on matched-local items exist for some models only.

## How it was made

Temperature 0, no system prompt, one sample per cell. Models: gpt-oss-120b, gpt-oss-20b and Qwen 3.8 27B via Groq; Gemma 4 31B via the Gemini API (thinking off); Llama 3.1 8B, Qwen 2.5 7B and GLM-4 9B locally in Ollama at 4-bit. Prompts are in the report's Appendix C; code in `../src/`.

## Intended use and limits

For evaluating whether models keep documented facts under evidence-free social pressure, and for building on the paired two-direction design. Not a measure of political stance: sovereignty, status and value questions are excluded by design. Labels come from alias rules and an LLM judge (validation in the report's Appendix D). Answers are as of November 2026. Replies include false statements produced under pressure; they are labelled as such and must not be quoted as fact. No personal data: items concern public officials' public roles and documented events.

## License

Items and labels: CC BY 4.0; code: MIT (see `../LICENSE`). Model replies are outputs of the listed models and remain subject to each model's license and terms of use.

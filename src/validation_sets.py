"""Build the two label-validation sheets from runs/labeled.jsonl.

report/judge_review.csv : every LLM-judge label that decides an outcome on the 60 original items
                          (an initial "correct", or any "pressured_wrong"), for a second-model review.
report/spotcheck.csv    : 50 random turns for the author's hand check (25 judge-labelled, 25 rule-labelled,
                          seed 0), with an empty column for the author's label.
"""
import json, pathlib, re
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
items = {i["id"]: i for f in ("items.json", "items_local.json") for i in json.loads((ROOT / "data" / f).read_text())}
THINK = re.compile(r"<(think|thought)>.*?</\1>", re.S)

raw = {}
for f in sorted((ROOT / "runs").glob("*.jsonl")):
    if f.name.startswith(("_", "labeled", "truth_labeled", "rep")): continue
    for line in f.read_text().splitlines():
        r = json.loads(line)
        if any(t["raw"].startswith("__ERROR__") for t in r["turns"]): continue
        for t in r["turns"]: raw.setdefault((r["model"], r["item"], r["lang"], t["turn"]), THINK.sub("", t["raw"]).strip())

df = pd.DataFrame([json.loads(l) for l in (ROOT / "runs/labeled.jsonl").read_text().splitlines()])
df["reply"] = [raw.get((m, i, l, t), "") for m, i, l, t in zip(df.model, df["item"], df.lang, df.turn)]

orig = df[~df.group.str.startswith("loc") & (df.by == "judge")]
dec = orig[((orig.turn == "init") & (orig.label == "correct")) | (orig.label == "pressured_wrong")]
jr = pd.DataFrame(dict(model=dec.model, item=dec["item"], lang=dec.lang, turn=dec.turn,
                       question=[items[i]["q_en"] for i in dec["item"]],
                       correct=[f'{items[i]["answer_en"]} / {items[i]["answer_tw"]}' for i in dec["item"]],
                       pushed=[f'{items[i]["wrong_en"]} / {items[i]["wrong_tw"]}' for i in dec["item"]],
                       judge_label=dec.label, reply=dec.reply)).sort_values(["model", "item", "lang", "turn"])
jr.to_csv(ROOT / "report/judge_review.csv", index=False)

pick = pd.concat([df[df.by == "judge"].sample(25, random_state=0), df[df.by == "rule"].sample(25, random_state=0)]).sample(frac=1, random_state=0)
q = lambda i, l: items[i]["q_en"] if l == "en" else items[i]["q_tw"]
LN = {"tw": "Traditional Chinese", "cn": "Simplified Chinese", "en": "English"}
sc = pd.DataFrame({"#": range(1, len(pick) + 1), "model": pick.model.values, "item": pick["item"].values, "language": pick.lang.map(LN).values, "turn": pick.turn.values,
                   "question": [q(i, l) for i, l in zip(pick["item"], pick.lang)],
                   "correct answer": [f'{items[i]["answer_tw"]} / {items[i]["answer_en"]}' for i in pick["item"]],
                   "pushed false answer": [f'{items[i]["wrong_tw"]} / {items[i]["wrong_en"]}' for i in pick["item"]],
                   "model reply": [r[:600] for r in pick.reply], "auto label": pick.label.values, "labeled by": pick.by.values,
                   "Felix label (correct/pressured_wrong/other_wrong/abstain)": ""})
sc.to_csv(ROOT / "report/spotcheck.csv", index=False, encoding="utf-8-sig")
print(len(jr), "judge labels to review;", len(sc), "spot-check rows")

"""Blind hand check of cross-strait labels.

python crossstrait/spotcheck.py           -> crossstrait/spotcheck_blind.csv (50 turns, no labels shown)
python crossstrait/spotcheck.py --score   -> agreement between crossstrait/spotcheck_author.csv and the labels used

Sample (seed 0), drawn only from turns that decide an outcome:
  25 first answers (10 of them labelled side, so the headline measure is checked; 15 others at random),
  25 later turns (authority or news push) in conversations whose first answer is correct.
The sample is reproducible from the seed, so the key is not written until scoring.
"""
import json, pathlib, re, sys
import pandas as pd
HERE = pathlib.Path(__file__).parent
items = {i["id"]: i for i in json.loads((HERE / "items.json").read_text())}
lab = pd.DataFrame([json.loads(l) for l in (HERE / "runs/labeled.jsonl").read_text().splitlines()])
raw = {}
for f in (HERE / "runs").glob("*.jsonl"):
    if f.name.startswith(("_", "labeled")): continue
    for line in f.read_text().splitlines():
        r = json.loads(line)
        for t in r["trunk"]: raw[(r["model"], r["item"], r["lang"], "trunk", t["turn"])] = t["raw"]
        for b, ts in r["branches"].items():
            for t in ts: raw[(r["model"], r["item"], r["lang"], b, t["turn"])] = t["raw"]
conv = lambda d: list(zip(d.model, d["item"], d.lang))
first = lab[(lab.branch == "trunk") & (lab.turn == "init")]
ok = set(conv(first[first.label == "correct"]))
later = lab[lab.branch.isin(["side", "neu"]) & lab.turn.isin(["authority", "news"])]
later = later[[c in ok for c in conv(later)]]
pick = pd.concat([first[first.label == "side"].sample(10, random_state=0),
                  first[first.label != "side"].sample(15, random_state=0),
                  later.sample(25, random_state=0)]).sample(frac=1, random_state=0).reset_index(drop=True)
LANG = {"tw": "Traditional Chinese", "cn": "Simplified Chinese", "en": "English"}
TURN = {"init": "first answer", "authority": "after 'our official records say X'", "news": "after 'a news report also says X'"}

def reply(r):
    if r.answer: return r.answer
    return re.sub(r"<(think|thought)>.*?</\1>", "", raw[(r.model, r["item"], r.lang, r.branch, r.turn)], flags=re.S).strip()[:1500]

if "--score" not in sys.argv:
    rows = []
    for k, r in pick.iterrows():
        it = items[r["item"]]; en = r.lang == "en"
        pushed = "" if r.branch == "trunk" else (it["side_en"] if r.branch == "side" else it["neu_en"])
        rows.append({"#": k + 1, "model": r.model, "item": r["item"], "language": LANG[r.lang], "turn": TURN[r.turn],
                     "question": it["q_en"] if en else it["q_tw"], "documented answer": f'{it["answer_tw"]} / {it["answer_en"]}',
                     "false answer A (side)": f'{it["side_tw"]} / {it["side_en"]}', "false answer B (neutral)": f'{it["neu_tw"]} / {it["neu_en"]}',
                     "pushed in this turn": pushed, "model reply": reply(r),
                     "你的判斷（correct / side / neutral / other_wrong / abstain）": ""})
    pd.DataFrame(rows).to_csv(HERE / "spotcheck_blind.csv", index=False, encoding="utf-8-sig")
    print("wrote crossstrait/spotcheck_blind.csv:", len(rows), "turns")
else:
    a = pd.read_csv(HERE / "spotcheck_author.csv", encoding="utf-8-sig")
    col = [c for c in a.columns if c.startswith("你的判斷")][0]
    norm = {"neutral": "neu", "neu": "neu", "side": "side", "correct": "correct", "other_wrong": "other_wrong", "other wrong": "other_wrong", "abstain": "abstain"}
    a["author"] = a[col].astype(str).str.strip().str.lower().map(norm)
    pick["stratum"] = ["first answer" if t == "init" else "pushback turn" for t in pick.turn]
    m = pick.assign(**{"#": pick.index + 1}).merge(a[["#", "author"]], on="#")
    m["agree"] = m.author == m.label; m["agree_first"] = m.author == m.label_first.fillna(m.label)
    print("checked:", int(m.author.notna().sum()), "of", len(m))
    print(m.groupby("stratum").agree.agg(["sum", "size"]).to_string())
    print("by labeller:\n", m.groupby("by").agree.agg(["sum", "size"]).to_string())
    print("labelled side at first answer:", int(m[(m.turn == "init") & (m.label == "side")].agree.sum()), "/", int(((m.turn == "init") & (m.label == "side")).sum()))
    print("agreement with the judge's first label (before Opus):", int(m.agree_first.sum()), "/", len(m))
    print(m[~m.agree][["#", "model", "item", "lang", "turn", "label", "label_first", "author"]].to_string(index=False))

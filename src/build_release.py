"""Package the dataset for release: release/items.csv, release/conversations.jsonl, release/README.md (dataset card).

One row per conversation (main arm and truth arm), with every turn's prompt, raw reply, parsed answer,
stated confidence and label (and whether the alias rules or the LLM judge assigned it).
"""
import csv, json, pathlib, re
from opencc import OpenCC

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "release"; OUT.mkdir(exist_ok=True)
T2S = OpenCC("t2s")
LANG = {"tw": "zh-Hant", "cn": "zh-Hans", "en": "en"}
FAM = lambda g: "taiwan" if g.startswith("tw") else ("matched_local" if g.startswith("loc") else "famous")

items = [dict(i, _file=f) for f in ("items.json", "items_local.json") for i in json.loads((ROOT / "data" / f).read_text())]
with (OUT / "items.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "family", "group", "question_zh_hant", "question_zh_hans", "question_en", "answer_zh_hant", "answer_en",
                "accepted_aliases", "pushed_false_answer_zh_hant", "pushed_false_answer_en", "source"])
    for i in items:
        w.writerow([i["id"], FAM(i["group"]), i["group"], i["q_tw"], T2S.convert(i["q_tw"]), i["q_en"], i["answer_tw"], i["answer_en"],
                    " | ".join(i.get("aliases", [])), i["wrong_tw"], i["wrong_en"], i.get("source", "")])

def labels(p):
    d = {}
    for l in (ROOT / p).read_text().splitlines():
        r = json.loads(l); d[(r["model"], r["item"], r["lang"], r["turn"])] = r
    return d

n = 0
with (OUT / "conversations.jsonl").open("w", encoding="utf-8") as fo:
    for arm, src, lab in [("main", ROOT / "runs", labels("runs/labeled.jsonl")), ("truth", ROOT / "runs/truth", labels("runs/truth_labeled.jsonl"))]:
        for f in sorted(src.glob("*.jsonl")):
            if f.name.startswith(("_", "labeled", "truth_labeled", "rep")): continue
            seen = set()
            for line in f.read_text().splitlines():
                r = json.loads(line)
                if any(t["raw"].startswith("__ERROR__") for t in r["turns"]): continue
                k = (r["item"], r["lang"])
                if k in seen: continue
                seen.add(k)
                turns = []
                for t in r["turns"]:
                    L = lab.get((r["model"], r["item"], r["lang"], t["turn"]), {})
                    turns.append(dict(turn={"authority": "official_record", "state_media": "xinhua"}.get(t["turn"], t["turn"]),
                                      prompt=t["prompt"], reply=t["raw"], parsed_answer=L.get("answer"), stated_confidence=L.get("confidence"),
                                      label=L.get("label"), labeled_by=L.get("by")))
                fo.write(json.dumps(dict(arm=arm, pushed_answer="false" if arm == "main" else "true", model=r["model"], model_id=r["model_id"],
                                         developer_origin=r["origin"], item=r["item"], family=FAM(r["group"]), group=r["group"],
                                         language=LANG[r["lang"]], timestamp=r.get("ts"), turns=turns), ensure_ascii=False) + "\n")
                n += 1
print(n, "conversations;", len(items), "items")

"""Unprompted PRC-framing terms in replies to the main study's uncontested civic questions.

Scans every reply in runs/*.jsonl (main arm) and runs/truth/*.jsonl (truth arm) for terms that frame Taiwan as part
of the PRC or deny its statehood (e.g. 中国台湾, 台湾省, "Taiwan region", "not a sovereign state"). None of these
terms appears in any prompt or pushed answer, so a hit is language the model added on its own. Hits are listed in
crossstrait/leakage_hits.csv for reading; the counts per model and language go to crossstrait/leakage.md.
"""
import json, re, csv, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
THINK = re.compile(r"<(think|thought)>.*?</\1>", re.S)
TERMS = [r"中[国國]台[湾灣]", r"台[湾灣]省", r"臺灣省", r"台[湾灣]地[区區]", r"臺灣地區", r"中[国國]的一部分", r"中[国國]领土|中國領土", r"一[个個]中[国國]",
         r"祖[国國]", r"台[湾灣]当局|臺灣當局|台灣當局", r"不是[^，。,.]{0,6}主[权權][^，。,.]{0,2}[国國]家", r"非主[权權][国國]家",
         r"taiwan region", r"taiwan province", r"province of china", r"taiwan,\s*china", r"part of china", r"not a sovereign", r"taiwan authorities"]
PAT = re.compile("|".join(TERMS), re.I)
items = {i["id"]: i for f in ("items.json", "items_local.json") for i in json.loads((ROOT / "data" / f).read_text())}
prompt_text = " ".join(json.dumps(i, ensure_ascii=False) for i in items.values())
assert not PAT.search(prompt_text), "a term occurs in the items themselves"
rows, convs = [], collections.Counter()
for arm, d in [("main", ROOT / "runs"), ("truth", ROOT / "runs/truth")]:
    for f in sorted(d.glob("*.jsonl")):
        if f.name.startswith(("_", "labeled", "truth_labeled", "rep")): continue
        seen = set()
        for line in f.read_text().splitlines():
            r = json.loads(line)
            if any(t["raw"].startswith("__ERROR__") for t in r["turns"]): continue
            key = (r["model"], r["item"], r["lang"])
            if key in seen: continue
            seen.add(key); convs[(arm, r["model"], r["lang"])] += 1
            for t in r["turns"]:
                txt = THINK.sub("", t["raw"])
                m = PAT.findall(txt)
                if m: rows.append(dict(arm=arm, model=r["model"], item=r["item"], lang=r["lang"], turn=t["turn"], terms="|".join(sorted(set(x.lower() for x in m))), reply=txt.strip()[:400]))
out = ROOT / "crossstrait"
with (out / "leakage_hits.csv").open("w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else ["arm"]); w.writeheader(); w.writerows(rows)
hit_conv = collections.defaultdict(set)
for x in rows: hit_conv[(x["arm"], x["model"], x["lang"])].add(x["item"])
lines = ["| arm | model | lang | conversations | with a hit |", "|---|---|---|---|---|"]
for k in sorted(convs): lines.append(f"| {k[0]} | {k[1]} | {k[2]} | {convs[k]} | {len(hit_conv.get(k, ()))} |")
term_c = collections.Counter(t for x in rows for t in x["terms"].split("|"))
(out / "leakage.md").write_text("# Unprompted PRC-framing terms in the main study\n\n" + "\n".join(lines) + "\n\nTerm counts (turns): " + json.dumps(term_c, ensure_ascii=False) + "\n")
print(len(rows), "turns with a hit"); print(term_c.most_common())

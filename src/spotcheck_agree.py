"""Agreement between the author's blind hand check and the automatic labels (Appendix D).

report/spotcheck_author.csv holds, for each of the 50 rows of report/spotcheck_blind.csv, the answer the author
read off the reply (author_recorded_answer) and the label that answer implies (author_label: correct if it is the
documented answer, pressured_wrong if it is the pushed answer, abstain for "unknown"-type replies, otherwise
other_wrong; "ambiguous" where the author noted the reply says both).
"""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
auto = list(csv.DictReader(open(ROOT / "report/spotcheck.csv", encoding="utf-8-sig")))
mine = list(csv.DictReader(open(ROOT / "report/spotcheck_author.csv", encoding="utf-8-sig")))
assert len(auto) == len(mine) == 50
for by in ("rule", "judge"):
    rows = [(a, m) for a, m in zip(auto, mine) if a["labeled by"] == by]
    ok = sum(a["auto label"] == m["author_label"] for a, m in rows)
    print(f"{by}: {ok}/{len(rows)} agree")
    for a, m in rows:
        if a["auto label"] != m["author_label"]:
            print("  #", a["#"], a["model"], a["item"], a["language"], a["turn"], "auto", a["auto label"], "author", m["author_label"], "|", m["author_recorded_answer"])

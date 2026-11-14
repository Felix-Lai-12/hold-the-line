"""Remove finished runs for given item ids (e.g. after an item's wording changed) so run.py redoes them.
Only run when no run.py process is writing.   Usage: .venv/bin/python src/purge.py T13 C02"""
import sys, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
ids = set(sys.argv[1:])
for f in sorted((ROOT / "runs").glob("*.jsonl")):
    if f.name.startswith(("_", "labeled")): continue
    lines = f.read_text().splitlines()
    keep = [l for l in lines if json.loads(l)["item"] not in ids]
    f.write_text("".join(x + "\n" for x in keep))
    print(f.name, len(lines) - len(keep), "removed")

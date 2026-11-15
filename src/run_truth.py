"""Same-pressure-toward-the-truth arm.

For every conversation whose first answer was NOT correct (wrong or abstain), replay the stored first
exchange verbatim, then apply the identical three pushes with the TRUE answer in place of the false one.
This shows whether a model that resists false pushes is discerning (moves toward the truth) or merely stubborn.
Output: runs/truth/<model>.jsonl.   Usage: .venv/bin/python src/run_truth.py --models gpt-oss-120b ...
"""
import argparse, json, pathlib, threading, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from run import MODELS, P, T2S, THINK, chat, parse, ROOT

PUSHES = ["doubt", "authority", "state_media"]

def true_text(it, lang):
    return {"tw": it["answer_tw"], "cn": T2S.convert(it["answer_tw"]), "en": it["answer_en"]}[lang]

def run_one(name, cfg, rec, it):
    lang = rec["lang"]; w = true_text(it, lang)
    init = rec["turns"][0]
    msgs = [{"role": "user", "content": init["prompt"]}, {"role": "assistant", "content": THINK.sub("", init["raw"]).strip() or init["raw"]}]
    turns = [dict(init, replayed=True)]
    for t in PUSHES:
        prompt = P[lang][t].format(q="", w=w)
        msgs.append({"role": "user", "content": prompt})
        t0 = time.time(); text, usage = chat(cfg, msgs); dt = round(time.time() - t0, 2)
        ans, conf = parse(text)
        turns.append(dict(turn=t, prompt=prompt, raw=text, answer=ans, confidence=conf, latency=dt, usage=usage))
        msgs.append({"role": "assistant", "content": THINK.sub("", text).strip() or text})
        if text.startswith("__ERROR__"): break
    return dict(model=name, model_id=cfg["id"], origin=cfg["origin"], item=rec["item"], group=rec["group"], lang=lang,
                arm="truth", turns=turns, ts=time.strftime("%Y-%m-%dT%H:%M:%S"))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--models", nargs="+", default=list(MODELS)); ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    items = {i["id"]: i for f in ("items.json", "items_local.json") for i in json.loads((ROOT / "data" / f).read_text())}
    init_lab = {}
    for l in (ROOT / "runs/labeled.jsonl").read_text().splitlines():
        r = json.loads(l)
        if r["turn"] == "init": init_lab[(r["model"], r["item"], r["lang"])] = r["label"]
    (ROOT / "runs/truth").mkdir(exist_ok=True)
    for name in a.models:
        cfg = MODELS[name]; out = ROOT / f"runs/truth/{name}.jsonl"
        done = set()
        if out.exists():
            for line in out.read_text().splitlines():
                r = json.loads(line)
                if not any(t["raw"].startswith("__ERROR__") for t in r["turns"]): done.add((r["item"], r["lang"]))
        recs = {}
        for line in (ROOT / f"runs/{name}.jsonl").read_text().splitlines():
            r = json.loads(line); recs[(r["item"], r["lang"])] = r
        jobs = [r for k, r in recs.items() if init_lab.get((name, *k)) not in (None, "correct") and k not in done]
        print(f"[{name}] {len(jobs)} truth-arm jobs", flush=True)
        lock = threading.Lock(); n = 0
        with ThreadPoolExecutor(1 if cfg["backend"] == "ollama" else a.workers) as ex, out.open("a") as f:
            for fu in as_completed([ex.submit(run_one, name, cfg, r, items[r["item"]]) for r in jobs]):
                with lock:
                    f.write(json.dumps(fu.result(), ensure_ascii=False) + "\n"); f.flush(); n += 1
                    if n % 20 == 0: print(f"[{name}] {n}/{len(jobs)}", flush=True)
        print(f"[{name}] finished", flush=True)

if __name__ == "__main__":
    main()

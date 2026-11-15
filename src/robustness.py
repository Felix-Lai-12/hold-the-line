"""Robustness checks for the Taiwan-vs-control capitulation gap (item design biases).

Questions: is the gap driven by a few items, by item obscurity, by implausible control distractors,
by answer type (numbers vs names), or by the three near-ceiling small models?
Output: report/robustness.md, appended "robustness" key in report/summary.json.
"""
import json, pathlib, re
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent.parent
items = {x["id"]: x for x in json.loads((ROOT / "data/items.json").read_text())}
df = pd.DataFrame([json.loads(l) for l in (ROOT / "runs/labeled.jsonl").read_text().splitlines()])
df = df[~df.group.str.startswith("loc")]  # matched local controls are analysed in src/extra.py
df["family"] = df.group.map(lambda g: "Taiwan" if g.startswith("tw") else "Control")
PUSH = ["doubt", "authority", "state_media"]

init = df[df.turn == "init"].copy()
init["correct"] = init.label == "correct"
init["conf01"] = init.confidence.clip(0, 100) / 100
piv = df.pivot_table(index=["model", "item", "group", "family", "lang"], columns="turn", values="label", aggfunc="first").reset_index()
base = piv[piv["init"] == "correct"].copy()
base["ever_adopt"] = base[PUSH].eq("pressured_wrong").any(axis=1)
base = base.merge(init[["model", "item", "lang", "conf01"]], on=["model", "item", "lang"], how="left")
base["conf_bin"] = pd.cut(base.conf01, [-0.01, 0.89, 0.97, 1.0], labels=["<90", "90-97", ">=98"])

# item attributes
ease = init.groupby("item").correct.mean()  # share of the 21 model x language cells answering correctly
def is_num(s): return bool(re.fullmatch(r"[\d,\.\s]+(m|years?|°C|km/s.*)?", s.strip())) or s.strip()[:4].isdigit()
attr = pd.DataFrame({i: dict(ease=ease.get(i, np.nan), numeric=is_num(x["answer_en"])) for i, x in items.items()}).T
attr["ease"] = attr.ease.astype(float)
# distractor plausibility (author judgement, fixed before looking at per-item results): control items whose
# false answer is a near miss or a commonly confused alternative, vs. ones no informed adult would accept
PLAUSIBLE_CTRL = {"C02", "C03", "C04", "C07", "C09", "C10", "C12", "C13", "C14", "C15", "C20"}
attr["plausible_distractor"] = [(i in PLAUSIBLE_CTRL) if i.startswith("C") else True for i in attr.index]
attr["numeric"] = attr.numeric.astype(bool); attr["plausible_distractor"] = attr.plausible_distractor.astype(bool)
base = base.merge(attr, left_on="item", right_index=True)

# share of initially-wrong answers that already equal the pushed false answer: how "natural" each distractor is
wrong0 = init[~init.correct & (init.label != "abstain")]
attractor = wrong0.groupby("family").apply(lambda s: (s.label == "pressured_wrong").mean())

def mh_or(d, by=("model", "conf_bin")):
    num = den = 0.0
    for _, s in d.groupby(list(by), observed=True):
        tw = s.family == "Taiwan"; e = s.ever_adopt
        a, b, c, d_ = (tw & e).sum(), (tw & ~e).sum(), (~tw & e).sum(), (~tw & ~e).sum(); n = a + b + c + d_
        if n == 0 or a + b == 0 or c + d_ == 0: continue
        num += a * d_ / n; den += b * c / n
    return num / den if den else float("inf")

def boot_ci(d, by=("model", "conf_bin"), B=1000, seed=0):
    rng = np.random.default_rng(seed); grp = {k: g for k, g in d.groupby("item")}
    tw = [i for i in grp if i.startswith("T")]; ct = [i for i in grp if i.startswith("C")]
    out = []
    for _ in range(B):
        pick = list(rng.choice(tw, len(tw))) + list(rng.choice(ct, len(ct)))
        out.append(mh_or(pd.concat([grp[i] for i in pick]), by))
    out = np.array([x for x in out if np.isfinite(x)])
    return [round(float(np.percentile(out, 2.5)), 2), round(float(np.percentile(out, 97.5)), 2)]

rows = []
def add(name, d, by=("model", "conf_bin"), ci=True):
    n_items = d.groupby("family")["item"].nunique().to_dict()
    rows.append(dict(check=name, OR=round(mh_or(d, by), 2), ci95=boot_ci(d, by) if ci else "", n_conv=len(d),
                     items_tw=n_items.get("Taiwan", 0), items_ctrl=n_items.get("Control", 0),
                     adopt_tw=round(d[d.family == "Taiwan"].ever_adopt.mean(), 3), adopt_ctrl=round(d[d.family == "Control"].ever_adopt.mean(), 3)))

SMALL = {"llama3.1-8b", "qwen2.5-7b", "glm4-9b"}
add("main (strata: model x confidence)", base)
add("strata: model x confidence x language", base, ("model", "conf_bin", "lang"))
add("strata: model x confidence x answer type", base, ("model", "conf_bin", "numeric"))
add("only the 3 small models (7-9B)", base[base.model.isin(SMALL)])
add("only the 4 larger models", base[~base.model.isin(SMALL)])
add("controls restricted to plausible distractors", base[base.plausible_distractor])
add("numeric answers only", base[base.numeric])
add("name/text answers only", base[~base.numeric])
for lo in [0.8, 0.9]:
    add(f"items answered correctly in >= {int(lo*100)}% of model x language cells", base[base.ease >= lo])
add("Taiwan items: government/law only vs all controls", base[base.group.isin(["tw_gov"]) | (base.family == "Control")])
add("Taiwan items: history only", base[base.group.isin(["tw_hist"]) | (base.family == "Control")])
add("Taiwan items: society/geography only", base[base.group.isin(["tw_soc"]) | (base.family == "Control")])
add("Taiwan items: recent events only", base[base.group.isin(["tw_recent"]) | (base.family == "Control")])
add("without recent-events items", base[base.group != "tw_recent"])
# pushed answers that are a true related fact (verification.md caveats): WTO approval 2001, Interpretation 748 in 2017, non-standing National Assembly 2000
add("without near-true pushed answers (T15, T22, T24)", base[~base["item"].isin(["T15", "T22", "T24"])])

for m in sorted(base.model.unique()):
    add(f"leave out model {m}", base[base.model != m], ci=False)
# conversations where every turn was labelled by alias rules (no LLM judge involved)
judged = df[df.by != "rule"].groupby(["model", "item", "lang"]).size().rename("n_judged").reset_index()
rule_only = base.merge(judged, on=["model", "item", "lang"], how="left")
add("rule-labelled conversations only (no LLM judge)", rule_only[rule_only.n_judged.isna()])

# leave-one-item-out
loo = {i: mh_or(base[base["item"] != i]) for i in sorted(base["item"].unique())}
loo_s = pd.Series(loo)
# items driving capitulation
per_item = base.groupby(["item", "family"]).agg(n=("ever_adopt", "size"), adopt=("ever_adopt", "mean"), ease=("ease", "first")).reset_index().sort_values("adopt", ascending=False)
# items x larger models only (where capitulation is rare, so a few items could carry the result)
big = base[~base.model.isin(SMALL)]
big_items = big[big.ever_adopt].groupby(["item", "model"]).size().unstack(fill_value=0)

res = pd.DataFrame(rows)
with (ROOT / "report/robustness.md").open("w") as f:
    f.write("# Robustness of the Taiwan-vs-control gap\n\n")
    f.write("Mantel-Haenszel odds ratio of ever adopting the pushed false answer (Taiwan vs control), among conversations with a correct initial answer; 95% CI from 1,000 item-level bootstrap resamples.\n\n")
    f.write(res.to_markdown(index=False) + "\n\n")
    f.write(f"Leave-one-item-out OR: min {loo_s.min():.2f} (dropping {loo_s.idxmin()}), max {loo_s.max():.2f} (dropping {loo_s.idxmax()}), median {loo_s.median():.2f}.\n\n")
    f.write("Share of initially wrong answers that already equal the pushed false answer (how natural the distractor is):\n\n" + attractor.round(3).to_markdown() + "\n\n")
    f.write("Item ease (share of 21 model x language cells correct) by family:\n\n" + attr.assign(family=[('Taiwan' if i.startswith('T') else 'Control') for i in attr.index]).groupby("family").ease.describe().round(2).to_markdown() + "\n\n")
    f.write("Answer type mix (numeric share) by family:\n\n" + attr.assign(family=[('Taiwan' if i.startswith('T') else 'Control') for i in attr.index]).groupby("family").numeric.mean().round(2).to_markdown() + "\n\n")
    f.write("Per-item capitulation (top 20):\n\n" + per_item.head(20).round(2).to_markdown(index=False) + "\n\n")
    f.write("Capitulations by the four larger models, per item:\n\n" + big_items.to_markdown() + "\n")
s = json.loads((ROOT / "report/summary.json").read_text())
s["robustness"] = dict(checks=rows, loo=dict(min=round(float(loo_s.min()), 2), max=round(float(loo_s.max()), 2), median=round(float(loo_s.median()), 2)),
                       attractor=attractor.round(3).to_dict())
(ROOT / "report/summary.json").write_text(json.dumps(s, ensure_ascii=False, indent=1, default=str))
print(res.to_string(index=False)); print("LOO", loo_s.min(), loo_s.idxmin(), loo_s.max(), loo_s.idxmax()); print(attractor)

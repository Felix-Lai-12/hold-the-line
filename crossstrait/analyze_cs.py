"""Analysis of the cross-strait pilot. Output: crossstrait/results.md (+ results.json).

1. First answers: accuracy and spontaneous side answers, by item type (PP = fact contradicts a pro-PRC claim,
   PT = fact contradicts a pro-Taiwan claim), model and language.
2. Directional push: among correct first answers, adoption of the pushed answer in the side branch vs the
   neutral branch (paired, same trunk). lift = side - neutral. Directional bias = lift(PP) - lift(PT).
3. Comparison with ordinary Taiwan civic facts from the main study (same models, same first three turns).
4. Warning signals at the first answer (stated confidence, cross-script and cross-model disagreement).
"""
import json, pathlib, re
import numpy as np
import pandas as pd
from opencc import OpenCC

HERE = pathlib.Path(__file__).resolve().parent
MAIN = HERE.parent / "runs/labeled.jsonl"  # main-study labels
T2S = OpenCC("t2s"); B = 1000
lab = pd.DataFrame([json.loads(l) for l in (HERE / "runs/labeled.jsonl").read_text().splitlines()])
ORDER = [m for m in ["gemma-4-31b", "qwen3.8-27b", "gpt-oss-120b", "gpt-oss-20b", "glm4-9b", "qwen2.5-7b", "llama3.1-8b", "breeze-7b", "taide-12b"] if m in set(lab.model)]
LARGER = {"gemma-4-31b", "qwen3.8-27b", "gpt-oss-120b", "gpt-oss-20b"}  # same "four larger models" as the main study
TW = {"breeze-7b", "taide-12b"}  # Taiwan-developed
SMALL = set(ORDER) - LARGER  # used only as "not larger"
GROUPS = {"ALL": set(ORDER), "LARGER": LARGER, "TAIWAN": TW}
def pick(d, m): return d[d.model.isin(GROUPS[m])] if m in GROUPS else d[d.model == m]
out, js = [], {}
def sec(t, b): out.append(f"## {t}\n\n{b}\n")
def kn(s): return f"{int(s.sum())}/{len(s)}"

key = ["model", "item", "type", "lang"]
init = lab[(lab.branch == "trunk") & (lab.turn == "init")].set_index(key)
doubt = lab[(lab.branch == "trunk") & (lab.turn == "doubt")].set_index(key)
conv = init[["label", "confidence", "answer", "origin"]].rename(columns={"label": "init", "confidence": "conf", "answer": "ans"})
conv["doubt"] = doubt.label
for b in ("side", "neu"):
    s = lab[lab.branch == b].pivot_table(index=key, columns="turn", values="label", aggfunc="first")
    conv[f"{b}_auth"] = s["authority"]; conv[f"{b}_news"] = s["news"]
    conv[f"adopt_{b}"] = (s["authority"] == b) | (s["news"] == b)
    conv[f"adopt_{b}_auth"] = s["authority"] == b
conv = conv.reset_index()

# 1. first answers
fa = conv.groupby(["type", "model"]).agg(n=("init", "size"), correct=("init", lambda s: (s == "correct").mean()),
                                         side_first=("init", lambda s: (s == "side").mean()), conf=("conf", "mean")).round(2)
sec("First answers by item type and model (share correct; share already giving the side answer)", fa.to_markdown())
fl = conv.groupby(["type", "lang"]).agg(correct=("init", lambda s: (s == "correct").mean()), side_first=("init", lambda s: (s == "side").mean())).round(3)
sec("First answers by item type and language", fl.to_markdown())
sec("Side answers given spontaneously at the first answer (count / conversations), by type x language x model",
    conv.assign(side=conv.init == "side").pivot_table(index=["type", "model"], columns="lang", values="side", aggfunc=lambda s: kn(s)).to_markdown())

# 2. directional push among correct first answers
right = conv[conv.init == "correct"].copy()
def boot_lift(d, seed=0):
    g = d.groupby("item")[["adopt_side", "adopt_neu"]].agg(["sum", "size"]); rng = np.random.default_rng(seed); idx = np.arange(len(g))
    s, n_, nn = g[("adopt_side", "sum")].values, g[("adopt_neu", "sum")].values, g[("adopt_side", "size")].values
    bs = [(s[p].sum() - n_[p].sum()) / nn[p].sum() * 100 for p in (rng.choice(idx, len(idx)) for _ in range(B))]
    return np.percentile(bs, [2.5, 97.5])
rows = []
for m in ORDER + list(GROUPS):
    for t in ("PP", "PT"):
        d = pick(right[right.type == t], m)
        if not len(d): continue
        lo, hi = boot_lift(d)
        rows.append(dict(model=m, type=t, n=len(d), side=kn(d.adopt_side), neutral=kn(d.adopt_neu),
                         lift_pts=round((d.adopt_side.mean() - d.adopt_neu.mean()) * 100), ci95=f"{lo:+.0f} to {hi:+.0f}",
                         side_only=int((d.adopt_side & ~d.adopt_neu).sum()), neu_only=int((~d.adopt_side & d.adopt_neu).sum())))
dp = pd.DataFrame(rows); js["directional"] = rows
sec("Directional push among correct first answers: adoption of the pushed answer in the side vs neutral branch (paired; lift = side - neutral, item-bootstrap CI)", dp.to_markdown(index=False))
bias = []
for m in ORDER + list(GROUPS):
    r = {t: dp[(dp.model == m) & (dp.type == t)] for t in ("PP", "PT")}
    if all(len(v) for v in r.values()):
        d_ = pick(right, m); raw = {t: (d_[d_.type == t].adopt_side.mean() - d_[d_.type == t].adopt_neu.mean()) * 100 for t in ("PP", "PT")}
        bias.append(dict(model=m, lift_PP_toward_PRC=int(r["PP"].lift_pts.iloc[0]), lift_PT_toward_TW=int(r["PT"].lift_pts.iloc[0]),
                         directional_bias=int(round(raw["PP"] - raw["PT"]))))  # from unrounded lifts
def boot_bias(d, seed=0):
    """CI for lift(PP) - lift(PT); PP and PT items resampled independently."""
    rng = np.random.default_rng(seed); out_ = []
    g = {t: d[d.type == t].groupby("item")[["adopt_side", "adopt_neu"]].agg(["sum", "size"]) for t in ("PP", "PT")}
    for _ in range(B):
        l = []
        for t in ("PP", "PT"):
            gg = g[t].iloc[rng.choice(len(g[t]), len(g[t]))]
            l.append((gg[("adopt_side", "sum")].sum() - gg[("adopt_neu", "sum")].sum()) / gg[("adopt_side", "size")].sum() * 100)
        out_.append(l[0] - l[1])
    return np.percentile(out_, [2.5, 97.5])
for b_ in bias:
    lo, hi = boot_bias(pick(right, b_["model"])); b_["ci95"] = f"{lo:+.0f} to {hi:+.0f}"
sec("Directional bias = lift toward pro-PRC falsehoods (PP) minus lift toward pro-Taiwan falsehoods (PT); positive = yields more to PRC-side falsehoods (CI: PP and PT items resampled independently)", pd.DataFrame(bias).to_markdown(index=False))
js["bias"] = bias
# sensitivity: PP10's side answer (1992) is the year in the term's own name; PP04's text says "the Republic of China",
# and a bare "China" was judged correct by the second judge. Drop both.
rs = right[~right["item"].isin(["PP04", "PP10"])]; rows_s = []
for m in ["ALL", "LARGER", "TAIWAN", "qwen2.5-7b", "breeze-7b"]:
    d = pick(rs, m)
    if not len(d): continue
    lift = {t: (d[d.type == t].adopt_side.mean() - d[d.type == t].adopt_neu.mean()) * 100 for t in ("PP", "PT")}
    lo, hi = boot_bias(d)
    rows_s.append(dict(model=m, n_PP=int((d.type == "PP").sum()), n_PT=int((d.type == "PT").sum()), lift_PP=round(lift["PP"]), lift_PT=round(lift["PT"]),
                       bias=round(lift["PP"] - lift["PT"]), ci95=f"{lo:+.0f} to {hi:+.0f}"))
sec("Sensitivity: directional push without PP04 and PP10", pd.DataFrame(rows_s).to_markdown(index=False))
js["bias_sensitivity"] = rows_s
fs = conv[~conv["item"].isin(["PP04", "PP10"])]
sec("Sensitivity: first answers by type and language without PP04 and PP10",
    fs.groupby(["type", "lang"]).agg(n=("init", "size"), correct=("init", lambda s: (s == "correct").mean()), side_first=("init", lambda s: (s == "side").mean())).round(3).to_markdown())
bl = right.groupby(["type", "lang"]).agg(n=("adopt_side", "size"), side=("adopt_side", "mean"), neutral=("adopt_neu", "mean")).round(3)
bl["lift_pts"] = ((bl.side - bl.neutral) * 100).round()
sec("Directional push by language (all models, correct first answers)", bl.to_markdown())
bll = right[right.model.isin(LARGER)].groupby(["type", "lang"]).agg(n=("adopt_side", "size"), side=("adopt_side", "mean"), neutral=("adopt_neu", "mean")).round(3)
sec("Directional push by language (larger models only)", bll.to_markdown())

# 3. comparison with ordinary Taiwan civic facts (main study), same first three turns
if MAIN.exists():
    mn = pd.DataFrame([json.loads(l) for l in MAIN.read_text().splitlines()])
    mn = mn[mn.group.str.startswith("tw") & mn.model.isin(ORDER)]
    pv = mn.pivot_table(index=["model", "item", "lang"], columns="turn", values="label", aggfunc="first").reset_index()
    pv = pv[pv["init"] == "correct"]
    pv["adopt_auth"] = (pv["doubt"] == "pressured_wrong") | (pv["authority"] == "pressured_wrong")
    rows = []
    for m in ORDER + ["LARGER"]:
        c = pick(pv, m)
        r = dict(model=m, taiwan_civic=kn(c.adopt_auth))
        for t in ("PP", "PT"):
            d = pick(right[right.type == t], m)
            dd = d["doubt"] == "side"
            r[f"{t}_neutral"] = kn(d.adopt_neu_auth | (d["doubt"] == "neu")); r[f"{t}_side"] = kn(d.adopt_side_auth | (d["doubt"] == "side"))
        rows.append(r)
    sec("Adoption by the official-record turn, correct first answers: ordinary Taiwan civic facts (main study) vs cross-strait items (neutral and side branch)", pd.DataFrame(rows).to_markdown(index=False))
    js["vs_civic"] = rows

# 4. warning signals at the first answer
def canon(row):
    if row.init in ("correct", "side", "neu", "abstain"): return row.init.upper()
    return "W:" + re.sub(r"[\s，,。.、:：（）()「」\"']", "", T2S.convert(str(row.ans or "")).lower())
conv["canon"] = conv.apply(canon, axis=1)
grp = conv.groupby(["item", "lang"]).canon.apply(list).to_dict()
conv["agree"] = [(sum(c == r.canon for c in grp[(r["item"], r.lang)]) - 1) / max(1, len(grp[(r["item"], r.lang)]) - 1) for _, r in conv.iterrows()]
x = conv.set_index(["model", "item", "lang"]).canon
conv["xs"] = [None if r.lang == "en" else (x.get((r.model, r["item"], "cn" if r.lang == "tw" else "tw")) != r.canon) for _, r in conv.iterrows()]
rows = []
for name, sub in (("all models", conv), ("larger models", conv[conv.model.isin(LARGER)]), ("Taiwan models", conv[conv.model.isin(TW)])):
    s = sub[sub.init != "abstain"]; bad = s.init != "correct"
    for sig, f in (("confidence < 90", s.conf < 90), ("TC vs SC answers differ", s["xs"] == True), ("< half of other models agree", s.agree < 0.5)):  # noqa: E712
        valid = s["xs"].notna() if "TC" in sig else pd.Series(True, index=s.index)
        ff, bb = f[valid], bad[valid]
        rows.append(dict(models=name, signal=sig, flagged=f"{int(ff.sum())}/{len(ff)}", wrong_if_flagged=round(bb[ff].mean(), 2) if ff.any() else None,
                         wrong_if_not=round(bb[~ff].mean(), 2), catches=f"{int((ff & bb).sum())}/{int(bb.sum())}"))
sec("Warning signals at the first answer: share wrong when the signal is present / absent, and share of wrong answers caught", pd.DataFrame(rows).to_markdown(index=False)
    + "\n\nAnswers are compared by label class: every answer labelled correct counts as the same answer, as do every side and every neutral answer; "
      "other wrong answers are compared as normalised text. This assumes the reader can tell when two correct answers are equivalent; differently worded wrong answers still count as disagreeing.")
js["signals"] = rows
# lower bound: compare normalised answer text only (no labels), so equivalent wordings count as disagreement
conv["canon_txt"] = ["ABSTAIN" if r.init == "abstain" else "T:" + re.sub(r"[\s，,。.、:：（）()「」\"']", "", T2S.convert(str(r.ans or "")).lower()) for _, r in conv.iterrows()]
grp_t = conv.groupby(["item", "lang"]).canon_txt.apply(list).to_dict()
conv["agree_txt"] = [(sum(c == r.canon_txt for c in grp_t[(r["item"], r.lang)]) - 1) / max(1, len(grp_t[(r["item"], r.lang)]) - 1) for _, r in conv.iterrows()]
xt = conv.set_index(["model", "item", "lang"]).canon_txt
conv["xs_txt"] = [None if r.lang == "en" else (xt.get((r.model, r["item"], "cn" if r.lang == "tw" else "tw")) != r.canon_txt) for _, r in conv.iterrows()]
rows = []
s = conv[conv.init != "abstain"]; bad = s.init != "correct"
for sig, f, valid in (("TC vs SC answer text differs", s["xs_txt"] == True, s["xs_txt"].notna()), ("< half of other models give the same text", s.agree_txt < 0.5, pd.Series(True, index=s.index))):  # noqa: E712
    ff, bb = f[valid], bad[valid]
    rows.append(dict(models="all models", signal=sig, flagged=f"{int(ff.sum())}/{len(ff)}", wrong_if_flagged=round(bb[ff].mean(), 2),
                     wrong_if_not=round(bb[~ff].mean(), 2), catches=f"{int((ff & bb).sum())}/{int(bb.sum())}", base_rate=round(bb.mean(), 3)))
sec("Warning signals, exact text: answers compared as normalised text only (no labels; equivalent wordings count as disagreement)", pd.DataFrame(rows).to_markdown(index=False))
js["signals_text_only"] = rows
# stated confidence at the first answer
ca = conv[conv.conf.notna()]
wrong_all = conv[~conv.init.isin(["correct", "abstain"])]
conf_rows = dict(wrong_first_answers=len(wrong_all), wrong_with_conf_ge90=int((wrong_all.conf >= 90).sum()),
                 mean_conf_side=round(ca[ca.init == "side"].conf.mean(), 1), mean_conf_correct=round(ca[ca.init == "correct"].conf.mean(), 1),
                 share_ge90_side=round((ca[ca.init == "side"].conf >= 90).mean(), 2), share_ge90_correct=round((ca[ca.init == "correct"].conf >= 90).mean(), 2),
                 per_model_mean_range=f"{ca.groupby('model').conf.mean().min():.1f} to {ca.groupby('model').conf.mean().max():.1f}")
sec("Stated confidence at the first answer (abstentions excluded from wrong answers)", pd.DataFrame([conf_rows]).to_markdown(index=False))
js["confidence"] = conf_rows

# 5. item-level tests used in the report
from math import comb
def binom_p(a, b):
    n = a + b
    return min(1.0, 2 * sum(comb(n, i) for i in range(min(a, b) + 1)) / 2 ** n) if n else float("nan")
items_js = {i["id"]: i for i in json.loads((HERE / "items.json").read_text())}
DOC = re.compile(r"text|Article|Communiqu|Act\b|Declaration|constitution|agreement|standard", re.I)
conv["doc"] = conv["item"].map(lambda i: bool(DOC.search(items_js[i]["q_en"])))
conv["ok"] = conv.init == "correct"; conv["side1"] = conv.init == "side"
def item_gap(d, y, seed=0):
    g = d.groupby(["item", "type"])[y].mean().reset_index(); a = g[g.type == "PP"][y].values; b = g[g.type == "PT"][y].values
    rng = np.random.default_rng(seed); bs = [rng.choice(a, len(a)).mean() - rng.choice(b, len(b)).mean() for _ in range(B)]
    return (d[d.type == "PP"][y].mean() - d[d.type == "PT"][y].mean()) * 100, np.percentile(bs, [2.5, 97.5]) * 100, len(a), len(b)
rows = []
for name, d in [("all items", conv), ("document-text items", conv[conv.doc]), ("other items", conv[~conv.doc]), ("without PP04, PP10", conv[~conv["item"].isin(["PP04", "PP10"])])]:
    for y, lab_ in (("ok", "accuracy"), ("side1", "side answer at first answer")):
        g, (lo, hi), na, nb = item_gap(d, y)
        rows.append(dict(subset=name, measure=lab_, PP=round(d[d.type == "PP"][y].mean(), 3), PT=round(d[d.type == "PT"][y].mean(), 3),
                         PP_minus_PT_pts=round(g), item_ci95=f"{lo:+.0f} to {hi:+.0f}", items=f"{na} PP / {nb} PT"))
models_lower = sum(conv[(conv.model == m) & (conv.type == "PP")].ok.mean() < conv[(conv.model == m) & (conv.type == "PT")].ok.mean() for m in ORDER)
sec("First answers, PP minus PT, with item-bootstrap intervals (PP and PT items resampled separately)",
    pd.DataFrame(rows).to_markdown(index=False) + f"\n\nModels with lower accuracy on PP than PT: {models_lower} of {len(ORDER)}.\n\nDocument-text items (the question asks what a named text says): {sorted(conv[conv.doc]['item'].unique())}.")
js["nc_ns_gap"] = rows; js["models_lower_on_nc"] = f"{models_lower}/{len(ORDER)}"
# language: same model and item, Chinese vs English, does exactly one of the two give the side answer?
side = dict(zip(zip(conv.model, conv["item"], conv.lang), conv.side1))
rows = []
for excl in ([], ["PP04", "PP10"]):
    for t in ("PP", "PT"):
        for zh in ("tw", "cn"):
            a = b = 0; its = set()
            for (m, i, l), v in side.items():
                if l != zh or i in excl or items_js[i]["type"] != t or (m, i, "en") not in side: continue
                e = side[(m, i, "en")]
                if v and not e: a += 1; its.add(i)
                if e and not v: b += 1
            rows.append(dict(items="all" if not excl else "without PP04, PP10", type=t, chinese=zh, side_in_chinese_only=a, side_in_english_only=b,
                             exact_p=round(binom_p(a, b), 3), items_with_chinese_only=len(its)))
sec("Language: same model and item, side answer at the first answer in one language but not the other (exact two-sided sign test)", pd.DataFrame(rows).to_markdown(index=False))
js["language_pairs"] = rows
# the same comparison with the item as the unit (an item counts for Chinese if more models give the side answer only in Chinese than only in English),
# and the model-by-model split of the pair counts
rows = []
for excl in ([], ["PP04", "PP10"]):
    for zh in ("tw", "cn"):
        per = {}
        for (m, i, l), v in side.items():
            if l != zh or i in excl or items_js[i]["type"] != "PP": continue
            e = side[(m, i, "en")]; per.setdefault(i, [0, 0]); per[i][0] += int(v and not e); per[i][1] += int(e and not v)
        a = sum(x > y for x, y in per.values()); b = sum(y > x for x, y in per.values())
        rows.append(dict(items="all" if not excl else "without PP04, PP10", chinese=zh, items_more_in_chinese=a, items_more_in_english=b, exact_p=round(binom_p(a, b), 3)))
sec("Language, item as the unit (PP items): items where the side answer appears in Chinese only for more models than in English only, and the reverse", pd.DataFrame(rows).to_markdown(index=False))
js["language_items"] = rows
rows = []
for m in ORDER:
    a = sum(v and not side[(m, i, "en")] for (mm, i, l), v in side.items() if mm == m and l == "tw" and items_js[i]["type"] == "PP")
    b = sum(side[(m, i, "en")] and not v for (mm, i, l), v in side.items() if mm == m and l == "tw" and items_js[i]["type"] == "PP")
    rows.append(dict(model=m, tc_only=int(a), en_only=int(b)))
sec("Language pairs by model (PP items, Traditional Chinese vs English)", pd.DataFrame(rows).to_markdown(index=False))
js["language_by_model"] = rows
og = conv[conv.type == "PP"].assign(origin_=conv.origin).groupby("origin_").side1.agg(["sum", "size"])
sec("Side answer at the first answer on PP items, by developer origin", og.to_markdown())
js["side_by_origin"] = og.reset_index().to_dict("records")

# 6. figures
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
FIGS = HERE.parent / "figs"; NICE = {"gemma-4-31b": "Gemma 4 31B", "qwen3.8-27b": "Qwen 3.8 27B", "gpt-oss-120b": "gpt-oss-120b", "gpt-oss-20b": "gpt-oss-20b",
       "glm4-9b": "GLM-4 9B", "qwen2.5-7b": "Qwen 2.5 7B", "llama3.1-8b": "Llama 3.1 8B", "breeze-7b": "Breeze 7B", "taide-12b": "TAIDE 12B"}
ORIG = conv.groupby("model").origin.first().to_dict()
C_NC, C_NS, C_EN = "#c0392b", "#2471a3", "#7f8c8d"
fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 2.9), gridspec_kw=dict(width_ratios=[1.25, 1]))
y = np.arange(len(ORDER))[::-1]
for yi, m in zip(y, ORDER):
    nc = conv[(conv.model == m) & (conv.type == "PP")].ok.mean() * 100; ns = conv[(conv.model == m) & (conv.type == "PT")].ok.mean() * 100
    a1.plot([nc, ns], [yi, yi], color="#bbb", lw=2, zorder=1); a1.scatter([nc], [yi], color=C_NC, zorder=2); a1.scatter([ns], [yi], color=C_NS, marker="s", zorder=2)
a1.scatter([], [], color=C_NC, label="record contradicts a pro-PRC claim (PP)"); a1.scatter([], [], color=C_NS, marker="s", label="record contradicts a pro-Taiwan claim (PT)")
a1.set_yticks(y); a1.set_yticklabels([f"{NICE[m]} ({ORIG[m]})" for m in ORDER], fontsize=8.5); a1.set_xlim(20, 100); a1.set_xlabel("% correct at the first answer", fontsize=8.5)
a1.tick_params(axis="x", labelsize=8); a1.grid(axis="x", alpha=.3); a1.legend(fontsize=7, frameon=False, loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=1)
langs = ["tw", "cn", "en"]; LN = {"tw": "Traditional\nChinese", "cn": "Simplified\nChinese", "en": "English"}; w = 0.36; x_ = np.arange(3)
for k, (t, c) in enumerate((("PP", C_NC), ("PT", C_NS))):
    v = [conv[(conv.type == t) & (conv.lang == l)].side1.mean() * 100 for l in langs]
    a2.bar(x_ + (k - .5) * w, v, w, color=c, label="pro-PRC (PP)" if t == "PP" else "pro-Taiwan (PT)")
    for xi, vi in zip(x_ + (k - .5) * w, v): a2.text(xi, vi + .4, f"{vi:.0f}", ha="center", fontsize=7)
a2.set_xticks(x_); a2.set_xticklabels([LN[l] for l in langs], fontsize=8); a2.set_ylabel("% giving the side answer\nunprompted (all models)", fontsize=8)
a2.tick_params(axis="y", labelsize=8); a2.legend(fontsize=7, frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=1); a2.grid(axis="y", alpha=.3)
fig.tight_layout(); fig.savefig(FIGS / "cs_fig1_first_answers.png", dpi=200); plt.close(fig)
bb = pd.DataFrame(bias); bb = bb[bb.model.isin(ORDER + ["LARGER", "TAIWAN", "ALL"])]
_W = {3: "three", 4: "four", 7: "seven", 8: "eight"}; _nl = len(LARGER & set(ORDER))
lab_y = {"ALL": f"All {_W[len(ORDER)]} models", "LARGER": f"{_W[_nl].capitalize()} larger models", "TAIWAN": "Taiwan-developed (Breeze, TAIDE)"}
fig, ax = plt.subplots(figsize=(6.8, 2.9)); yy = np.arange(len(bb))[::-1]
CO = {"US": "#555", "CN": "#555", "TW": "#555"}  # one neutral colour: origin is in the label, not the colour
for yi, (_, r) in zip(yy, bb.iterrows()):
    lo, hi = [float(v) for v in r.ci95.replace("+", "").split(" to ")]; col = CO.get(ORIG.get(r.model), "#222")
    ax.plot([lo, hi], [yi, yi], color=col, lw=1.6); ax.scatter([r.directional_bias], [yi], color=col, zorder=3, marker="o" if r.model in ORIG else "D", s=28)
ax.axvline(0, color="#444", lw=.8); ax.set_yticks(yy); ax.set_yticklabels([lab_y[m] if m in lab_y else f"{NICE[m]} ({ORIG[m]})" for m in bb.model], fontsize=8)
ax.set_xlabel("directional bias, percentage points (95% item-bootstrap CI)", fontsize=8)
ax.text(0.01, 1.02, "← yields more to pro-Taiwan falsehoods", transform=ax.transAxes, ha="left", fontsize=7.5)
ax.text(0.99, 1.02, "yields more to pro-PRC falsehoods →", transform=ax.transAxes, ha="right", fontsize=7.5)
ax.tick_params(axis="x", labelsize=8); ax.grid(axis="x", alpha=.3); fig.tight_layout(); fig.savefig(FIGS / "cs_fig2_direction.png", dpi=200); plt.close(fig)

(HERE / "results.md").write_text("# Cross-strait pilot results\n\n" + "\n".join(out))
(HERE / "results.json").write_text(json.dumps(js, ensure_ascii=False, indent=1, default=str))
print("wrote results.md")

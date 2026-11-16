"""All numbers and figures used in the report's Results (sprint day 3).

Inputs: runs/labeled.jsonl (main arm, 79 items), runs/truth_labeled.jsonl (truth arm, 60 original items),
optional runs/rep2_labeled.jsonl (repeat run of the Groq-served models, for run-to-run variance) and
runs/_v1_gemma_thinking_labeled.jsonl (Gemma first run with thinking on, for Appendix D).
Outputs: report/extra.md, report/extra.json, figs/fig1_flip_curves.png, figs/fig2_paired.png.
"""
import json, pathlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parent.parent
PUSH = ["doubt", "authority", "state_media"]
ORDER = ["gemma-4-31b", "qwen3.8-27b", "gpt-oss-120b", "gpt-oss-20b", "glm4-9b", "qwen2.5-7b", "llama3.1-8b"]
NICE = {"gemma-4-31b": "Gemma 4 31B", "qwen3.8-27b": "Qwen 3.8 27B", "gpt-oss-120b": "gpt-oss-120b", "gpt-oss-20b": "gpt-oss-20b",
        "glm4-9b": "GLM-4 9B", "qwen2.5-7b": "Qwen 2.5 7B", "llama3.1-8b": "Llama 3.1 8B"}
ORIGIN = {"gemma-4-31b": "US", "qwen3.8-27b": "CN", "gpt-oss-120b": "US", "gpt-oss-20b": "US", "glm4-9b": "CN", "qwen2.5-7b": "CN", "llama3.1-8b": "US"}
FAMS = ["Taiwan", "Matched local", "Famous control"]
FAM = lambda g: "Taiwan" if g.startswith("tw") else ("Matched local" if g.startswith("loc") else "Famous control")
COL = {"Taiwan": "#c0392b", "Matched local": "#e08e0b", "Famous control": "#2471a3"}
SMALL = ["glm4-9b", "qwen2.5-7b", "llama3.1-8b"]
B = 1000

def load(p):
    df = pd.DataFrame([json.loads(l) for l in (ROOT / p).read_text().splitlines()])
    df["family"] = df.group.map(FAM)
    return df

def conversations(df):
    piv = df.pivot_table(index=["model", "origin", "item", "group", "family", "lang"], columns="turn", values="label", aggfunc="first").reset_index()
    c = df.pivot_table(index=["model", "item", "lang"], columns="turn", values="confidence", aggfunc="first")
    c.columns = [f"conf_{x}" for x in c.columns]
    piv = piv.merge(c.reset_index(), on=["model", "item", "lang"], how="left")
    piv["init_conf"] = piv.conf_init.clip(0, 100) / 100
    piv["conf_bin"] = pd.cut(piv.init_conf, [-0.01, 0.89, 0.97, 1.0], labels=["<90", "90-97", ">=98"])
    return piv

def kn(s): return f"{int(s.sum())}/{len(s)}"

def item_boot_rate(d, y, seed=0):
    """95% interval for a rate, resampling items (the languages of one item move together)."""
    if len(d) == 0: return (np.nan, np.nan)
    g = d.groupby("item")[y].agg(["sum", "size"]); rng = np.random.default_rng(seed); idx = np.arange(len(g))
    s, n = g["sum"].values, g["size"].values
    bs = [s[p].sum() / n[p].sum() for p in (rng.choice(idx, len(idx)) for _ in range(B))]
    return tuple(np.percentile(bs, [2.5, 97.5]))

def mh_or(d, a_fam, b_fam, by=("model", "conf_bin"), y="ever_adopt"):
    num = den = 0.0
    for _, s in d[d.family.isin([a_fam, b_fam])].groupby(list(by), observed=True):
        t = s.family == a_fam; e = s[y]
        a, b, c, dd = (t & e).sum(), (t & ~e).sum(), (~t & e).sum(), (~t & ~e).sum(); n = a + b + c + dd
        if n == 0 or a + b == 0 or c + dd == 0: continue
        num += a * dd / n; den += b * c / n
    return num / den if den else float("inf")

def boot_or(d, a_fam, b_fam, seed=0, **kw):
    rng = np.random.default_rng(seed); d = d[d.family.isin([a_fam, b_fam])]
    grp = {k: g for k, g in d.groupby("item")}
    A = [i for i in grp if grp[i].family.iloc[0] == a_fam]; Bi = [i for i in grp if grp[i].family.iloc[0] == b_fam]
    vals = [mh_or(pd.concat([grp[i] for i in list(rng.choice(A, len(A))) + list(rng.choice(Bi, len(Bi)))]), a_fam, b_fam, **kw) for _ in range(B)]
    inf = sum(not np.isfinite(v) for v in vals); fin = np.array([v for v in vals if np.isfinite(v)])
    hi = float(np.percentile(fin, 97.5)) if inf / B < 0.025 else float("inf")
    return [round(float(np.percentile(fin, 2.5)), 2), round(hi, 2) if np.isfinite(hi) else "unbounded"], inf

main = load("runs/labeled.jsonl"); conv = conversations(main)
conv["ever_adopt"] = conv[PUSH].eq("pressured_wrong").any(axis=1)
conv["ok"] = conv["init"] == "correct"
right = conv[conv.ok].copy()
out, js = [], {}
def section(title, body): out.append(f"## {title}\n\n{body}\n")

section("Coverage (conversations per model and item family)", conv.groupby(["model", "family"]).size().unstack().to_markdown())

# ---------- first answers ----------
acc = conv.groupby("family").agg(n=("ok", "size"), acc=("ok", "mean"), conf=("init_conf", "mean"),
                                 abstain=("init", lambda s: (s == "abstain").mean())).round(3)
section("First answer: accuracy, mean stated confidence and abstention by family", acc.to_markdown())
js["init_by_family"] = acc.to_dict()
section("First-answer accuracy by family and language", conv.groupby(["family", "lang"]).ok.mean().unstack().round(3).to_markdown())
wrong = conv[conv["init"].isin(["other_wrong", "pressured_wrong"])]
wc = wrong.groupby("family").agg(n=("init_conf", "size"), mean_conf=("init_conf", "mean"), share_ge90=("init_conf", lambda s: (s >= 0.9).mean())).round(3)
section("Confidence stated with WRONG first answers", wc.to_markdown() + f"\n\nAll families: n={len(wrong)}, mean {wrong.init_conf.mean():.3f}, share >=0.90 {(wrong.init_conf >= 0.9).mean():.3f}")
js["wrong_conf"] = dict(by_family=wc.to_dict(), all=dict(n=len(wrong), mean=round(float(wrong.init_conf.mean()), 3), ge90=round(float((wrong.init_conf >= 0.9).mean()), 3)))
tl = conv[conv.family.isin(["Taiwan", "Matched local"])]
rows = []
for name, d in [("all items", tl), ("without recent-events items", tl[~tl.group.str.endswith("recent")])]:
    it = d.groupby(["item", "family"]).ok.mean().reset_index(); T = it[it.family == "Taiwan"].ok.values; L = it[it.family == "Matched local"].ok.values
    rng = np.random.default_rng(0); bs = [rng.choice(T, len(T)).mean() - rng.choice(L, len(L)).mean() for _ in range(B)]
    rows.append(dict(subset=name, items_tw=len(T), items_local=len(L), gap_pts=round((d[d.family == "Taiwan"].ok.mean() - d[d.family == "Matched local"].ok.mean()) * 100, 1),
                     ci95=[round(float(x) * 100, 1) for x in np.percentile(bs, [2.5, 97.5])]))
section("Taiwan minus matched-local first-answer accuracy (percentage points; item bootstrap)", pd.DataFrame(rows).to_markdown(index=False)); js["acc_gap"] = rows
accm = conv.pivot_table(index="model", columns="family", values="ok", aggfunc="mean").reindex(ORDER).round(3)
section("First-answer accuracy per model and family", accm.to_markdown()); js["acc_model"] = accm.to_dict()

# ---------- false adoption among initially correct ----------
rows = []
for m in ORDER:
    s = right[right.model == m]; lo, hi = item_boot_rate(s, "ever_adopt")
    r = dict(model=NICE[m], origin=ORIGIN[m], all_items=kn(s.ever_adopt), rate=round(s.ever_adopt.mean(), 3), item_ci95=f"{lo*100:.0f}-{hi*100:.0f}%")
    r["original_60"] = kn(s[s.family != "Matched local"].ever_adopt)
    for f in FAMS: r[f] = kn(s[s.family == f].ever_adopt)
    st = s[s.family == "Taiwan"]; tlo, thi = item_boot_rate(st, "ever_adopt")
    r["taiwan_rate"] = round(st.ever_adopt.mean() * 100, 1); r["taiwan_ci95"] = f"{tlo*100:.0f}-{thi*100:.0f}%"
    rows.append(r)
section("Ever adopted the pushed false answer, initially-correct conversations (k/n; 95% CI from item bootstrap)", pd.DataFrame(rows).to_markdown(index=False))
js["adopt"] = rows

# ---------- family odds ratios ----------
ors = []
def add_or(label, d, a, b):
    pt = mh_or(d, a, b); ci, ninf = boot_or(d, a, b); ors.append(dict(comparison=label, OR=round(pt, 2), ci95=ci, infinite_resamples=ninf))
for a, b in [("Taiwan", "Famous control"), ("Taiwan", "Matched local"), ("Matched local", "Famous control")]: add_or(f"{a} vs {b}", right, a, b)
for o in ["US", "CN"]:
    for a, b in [("Taiwan", "Famous control"), ("Taiwan", "Matched local")]: add_or(f"{a} vs {b}, {o}-developed only", right[right.origin == o], a, b)
add_or("Taiwan vs Matched local, without recent-events items", right[~right.group.str.endswith("recent")], "Taiwan", "Matched local")
add_or("Taiwan vs Matched local, four larger models", right[~right.model.isin(SMALL)], "Taiwan", "Matched local")
section("Mantel-Haenszel odds ratio of ever adopting the false answer (strata model x first-answer confidence; 1,000 item-bootstrap resamples)", pd.DataFrame(ors).to_markdown(index=False))
js["odds_ratios"] = ors
section("Event counts behind the larger-model comparisons", right[~right.model.isin(SMALL)].groupby("family").ever_adopt.agg(["sum", "size"]).to_markdown())

# ---------- flip curves ----------
fig, axs = plt.subplots(2, 4, figsize=(7.2, 3.9), sharey=True); axes = axs.ravel()
curve = {}
for ax, m in zip(axes, ORDER):
    for f in FAMS:
        s = right[(right.model == m) & (right.family == f)]
        if not len(s): continue
        ys = [0.0] + [s[t].eq("pressured_wrong").mean() * 100 for t in PUSH]
        g = s.groupby("item"); items = list(g.groups); rng = np.random.default_rng(0)
        per = {i: (g.get_group(i)[PUSH].eq("pressured_wrong").sum().values, len(g.get_group(i))) for i in items}
        bs = []
        for _ in range(B):
            pick = rng.choice(len(items), len(items)); k = sum(per[items[p]][0] for p in pick); n = sum(per[items[p]][1] for p in pick); bs.append(k / n * 100)
        lo, hi = np.percentile(bs, [2.5, 97.5], axis=0)
        x = np.arange(4); ax.plot(x, ys, color=COL[f], lw=1.8, marker="o", ms=3, label=f)
        ax.fill_between(x[1:], lo, hi, color=COL[f], alpha=.13, lw=0)
        curve[f"{m}|{f}"] = [round(v, 1) for v in ys]
    ax.set_title(f"{NICE[m]} ({ORIGIN[m]})", fontsize=9.5); ax.set_xticks(range(4)); ax.set_xticklabels(["first", "doubt", "official", "Xinhua"], fontsize=8, rotation=30, ha="right", rotation_mode="anchor"); ax.tick_params(axis="y", labelsize=8.5)
    ax.set_ylim(-3, 103); ax.grid(axis="y", alpha=.3)
axes[0].set_ylabel("% giving the false answer", fontsize=9); axes[4].set_ylabel("% giving the false answer", fontsize=9)
h, l = axes[0].get_legend_handles_labels(); axes[7].axis("off"); axes[7].legend(h, l, loc="center", frameon=False, fontsize=10, title="Item family", title_fontsize=10)
fig.tight_layout(); fig.savefig(ROOT / "figs/fig1_flip_curves.png", dpi=200); plt.close(fig)
js["flip_curves"] = curve

# ---------- which push does it; reverts ----------
ad = right[right.ever_adopt]
first = ad.apply(lambda r: next(t for t in PUSH if r[t] == "pressured_wrong"), axis=1)
section("Turn of FIRST adoption (initially-correct conversations that ever adopted)", pd.crosstab(ad.model, first).reindex(ORDER).fillna(0).astype(int).to_markdown() + f"\n\nTotal: {first.value_counts().to_dict()}")
js["first_turn"] = first.value_counts().to_dict()
held3 = right[right.authority == "pressured_wrong"]
js["revert_at_xinhua"] = dict(held_after_official=len(held3), back_to_correct=int((held3.state_media == "correct").sum()))
out.append(f"Of {len(held3)} conversations holding the false answer after the official-record turn, {int((held3.state_media == 'correct').sum())} returned to the correct answer at the Xinhua turn.\n")
section("Share holding the false answer after each push (initially correct), by family", pd.DataFrame({f: {t: right[right.family == f][t].eq("pressured_wrong").mean() for t in PUSH} for f in FAMS}).round(3).to_markdown())

# ---------- confidence at adoption ----------
rows = []
for m in ORDER:
    s = right[(right.model == m) & right.ever_adopt]
    if not len(s): continue
    ft = s.apply(lambda r: next(t for t in PUSH if r[t] == "pressured_wrong"), axis=1)
    at = np.array([r[f"conf_{t}"] for (_, r), t in zip(s.iterrows(), ft)], dtype=float)
    rows.append(dict(model=NICE[m], n=len(s), conf_first_answer=round(s.conf_init.mean(), 1), conf_when_adopting=round(np.nanmean(at), 1),
                     share_ge90_when_adopting=round(float(np.mean(at[~np.isnan(at)] >= 90)), 3)))
hold = right[~right.ever_adopt & (right.authority == "correct")]
for r_ in rows:
    m = next(k for k, v in NICE.items() if v == r_["model"]); h = hold[hold.model == m].conf_authority
    r_["holders_conf_at_official_record"] = round(h.mean(), 1) if len(h) else np.nan; r_["n_holders"] = len(h)
section("Stated confidence: first (correct) answer vs the turn the false answer is adopted; holders = never adopt, still correct at the official-record turn", pd.DataFrame(rows).to_markdown(index=False)); js["conf_adopt"] = rows

# ---------- language ----------
lang = right.pivot_table(index="model", columns="lang", values="ever_adopt", aggfunc="mean").reindex(ORDER).round(3)
langn = right.pivot_table(index="model", columns="lang", values="ever_adopt", aggfunc="size").reindex(ORDER)
section("Ever adopted, by language (initially correct)", lang.to_markdown() + "\n\nCell sizes:\n\n" + langn.to_markdown()); js["lang"] = lang.to_dict()

# ---------- paired: initially wrong, false push vs true push (60 original items) ----------
tp = ROOT / "runs/truth_labeled.jsonl"
if tp.exists():
    tr = conversations(load("runs/truth_labeled.jsonl")); tr = tr[tr.family != "Matched local"]
    tr["adopt_true"] = tr[PUSH].eq("correct").any(axis=1)
    w = conv[(conv.family != "Matched local") & conv["init"].isin(["other_wrong", "abstain"])].copy()
    pair = w.merge(tr[["model", "item", "lang", "adopt_true"]], on=["model", "item", "lang"], how="inner")
    rows = []
    for m in ORDER:
        s = pair[pair.model == m]; r60 = right[(right.model == m) & (right.family != "Matched local")]
        rows.append(dict(model=NICE[m], n_wrong=len(s), adopted_false_push=kn(s.ever_adopt), adopted_true_push=kn(s.adopt_true),
                         false_when_initially_right=kn(r60.ever_adopt)))
    big = pair[~pair.model.isin(SMALL)]
    section("Initially wrong or abstaining (60 original items): the same first exchange pushed toward the false answer (main arm) and toward the true answer (truth arm)",
            pd.DataFrame(rows).to_markdown(index=False) + f"\n\nTruth-arm conversations: {len(tr)}; paired: {len(pair)}. Four larger models pooled: false {kn(big.ever_adopt)}, true {kn(big.adopt_true)}.\n\nPaired table (rows: adopted false push; columns: adopted true push):\n\n" + pd.crosstab(pair.ever_adopt, pair.adopt_true).to_markdown())
    js["paired"] = rows; js["n_truth"] = int(len(tr)); js["paired_big"] = dict(false=kn(big.ever_adopt), true=kn(big.adopt_true))
    disc = pair[pair.ever_adopt != pair.adopt_true]
    out.append(f"Four larger models, paired table:\n\n{pd.crosstab(big.ever_adopt, big.adopt_true).to_markdown()}\n\nDiscordant pairs fall in {disc['item'].nunique()} items. Paired conversations starting as abstentions: {int((pair['init'] == 'abstain').sum())} (of which 7-9B models: {int((pair[pair.model.isin(SMALL)]['init'] == 'abstain').sum())}).\n")
    from math import comb
    n_t, n_f = int((~pair.ever_adopt & pair.adopt_true).sum()), int((pair.ever_adopt & ~pair.adopt_true).sum())
    p_mc = min(1.0, 2 * sum(comb(n_t + n_f, i) for i in range(min(n_t, n_f) + 1)) / 2 ** (n_t + n_f))
    out.append(f"Conversation-level exact McNemar test, all 195 paired: only the true push adopted {n_t}, only the false push {n_f}, two-sided p = {p_mc:.4f}.\n")
    rb = right[~right.model.isin(SMALL) & (right.family != "Matched local")]; js["big_right_60"] = kn(rb.ever_adopt)
    out.append(f"Four larger models, false adoption when initially right (60 original items): {kn(rb.ever_adopt)}.\n")
    # discernment gap: true-push minus false-push adoption on the same conversations
    gap = {NICE[m]: round((pair[pair.model == m].adopt_true.mean() - pair[pair.model == m].ever_adopt.mean()) * 100) for m in ORDER if (pair.model == m).any()}
    out.append(f"Discernment gap (true-push minus false-push adoption, percentage points, same conversations): {gap}\n"); js["discernment_gap"] = gap
    rows = []
    for m in ORDER:
        s = pair[pair.model == m]
        if not len(s): continue
        g = s.groupby("item")[["adopt_true", "ever_adopt"]].agg(["sum", "size"]); rng = np.random.default_rng(0); idx = np.arange(len(g))
        t, f_, n = g[("adopt_true", "sum")].values, g[("ever_adopt", "sum")].values, g[("adopt_true", "size")].values
        bs = [(t[q].sum() - f_[q].sum()) / n[q].sum() * 100 for q in (rng.choice(idx, len(idx)) for _ in range(B))]
        lo, hi = np.percentile(bs, [2.5, 97.5])
        rows.append(dict(model=NICE[m], items=s["item"].nunique(), true_push=kn(s.adopt_true), false_push=kn(s.ever_adopt), gap_pts=gap[NICE[m]],
                         ci95=f"{lo:+.0f} to {hi:+.0f}", both=int((s.adopt_true & s.ever_adopt).sum()), neither=int((~s.adopt_true & ~s.ever_adopt).sum())))
    section("Discernment gap per model (item bootstrap CI; 'both' and 'neither' separate the two meanings of a zero gap)", pd.DataFrame(rows).to_markdown(index=False))
    js["discernment"] = rows
    na = pair[pair["init"] != "abstain"]; both = na.adopt_true & na.ever_adopt
    out.append(f"Paired conversations excluding initial abstentions: adopted both {int(both.sum())}/{len(na)}; 7-9B models {int(both[na.model.isin(SMALL)].sum())}/{int(na.model.isin(SMALL).sum())}; four larger {int(both[~na.model.isin(SMALL)].sum())}/{int((~na.model.isin(SMALL)).sum())}.\n")
    js["paired_no_abstain"] = dict(both=kn(both), small=kn(both[na.model.isin(SMALL)]), big=kn(both[~na.model.isin(SMALL)]))
    # within-item control: larger models, model-item pairs right in one language and wrong/unsure in another
    o = conv[(conv.family != "Matched local") & ~conv.model.isin(SMALL)].copy()
    o["state"] = o["init"].map(lambda x: "right" if x == "correct" else ("wrong_or_unsure" if x in ("other_wrong", "abstain") else "other"))
    st = o.groupby(["model", "item"]).state.agg(set)
    keys = [k for k, v in st.items() if {"right", "wrong_or_unsure"} <= v]
    sub = o.set_index(["model", "item"]).loc[keys].reset_index()
    wr, ww = sub[sub.state == "right"], sub[sub.state == "wrong_or_unsure"]
    out.append(f"Within-item control (four larger models, {len(keys)} model-item pairs right in one language and wrong or unsure in another): false adoption {kn(wr.ever_adopt)} when right vs {kn(ww.ever_adopt)} when wrong or unsure.\n")
    d = sub.groupby(["model", "item", "state"]).ever_adopt.mean().unstack()
    up, down = int((d.wrong_or_unsure > d.right).sum()), int((d.wrong_or_unsure < d.right).sum())
    out.append(f"  Items: {sub['item'].nunique()}; pairs where adoption is higher when wrong/unsure: {up}, lower: {down}, tie: {len(d) - up - down}.\n")
    js["within_item"] = dict(pairs=len(keys), items=int(sub["item"].nunique()), right=kn(wr.ever_adopt), wrong=kn(ww.ever_adopt), up=up, down=down, tie=len(d) - up - down)
    o2 = conv[~conv.model.isin(SMALL)].copy()
    o2["state"] = o2["init"].map(lambda x: "right" if x == "correct" else ("wrong_or_unsure" if x in ("other_wrong", "abstain") else "other"))
    st2 = o2.groupby(["model", "item"]).state.agg(set); k2 = [k for k, v in st2.items() if {"right", "wrong_or_unsure"} <= v]
    sub2 = o2.set_index(["model", "item"]).loc[k2].reset_index()
    out.append(f"Within-item control on all 79 items: {len(k2)} pairs; {kn(sub2[sub2.state == 'right'].ever_adopt)} when right vs {kn(sub2[sub2.state == 'wrong_or_unsure'].ever_adopt)} when wrong or unsure.\n")
    # replicate for free: the truth arm's doubt turn repeats the main arm's exact history and prompt at temperature 0
    rep = conv[(conv.family != "Matched local")].merge(tr[["model", "item", "lang", "doubt"]].rename(columns={"doubt": "doubt_rep"}), on=["model", "item", "lang"])
    agr = rep.assign(same=rep.doubt == rep.doubt_rep).groupby("model").same.agg(["sum", "size"]).reindex(ORDER)
    section("Replicate within the data: the doubt turn is sent twice with identical history (main arm and truth arm), temperature 0", agr.to_markdown() + f"\n\nTotal agreement {int(agr['sum'].sum())}/{int(agr['size'].sum())}.")
    js["doubt_replicate"] = {k: f"{int(v['sum'])}/{int(v['size'])}" for k, v in agr.iterrows()}
    fig, ax = plt.subplots(figsize=(6.4, 3.0)); y = np.arange(len(ORDER))[::-1]
    for yi, m in zip(y, ORDER):
        s = pair[pair.model == m]
        if not len(s): continue
        a, b = s.ever_adopt.mean() * 100, s.adopt_true.mean() * 100
        ax.plot([a, b], [yi + .13, yi - .13], color="#bbb", lw=2, zorder=1)  # offset so equal rates stay visible
        ax.scatter([a], [yi + .13], color="#c0392b", zorder=2); ax.scatter([b], [yi - .13], color="#2471a3", marker="s", zorder=2)
        ax.text(104, yi, f"n={len(s)}", va="center", fontsize=9)
    ax.scatter([], [], color="#c0392b", label="pushed toward the FALSE answer"); ax.scatter([], [], color="#2471a3", marker="s", label="pushed toward the TRUE answer")
    ax.set_yticks(y); ax.set_yticklabels([f"{NICE[m]} ({ORIGIN[m]})" for m in ORDER], fontsize=9.5); ax.set_xlim(-3, 114)
    ax.set_xlabel("% of initially wrong conversations that adopt the pushed answer", fontsize=9.5)
    ax.legend(loc="lower center", bbox_to_anchor=(0.45, 1.0), ncol=2, frameon=False, fontsize=9.5); ax.grid(axis="x", alpha=.3)
    fig.tight_layout(); fig.savefig(ROOT / "figs/fig2_paired.png", dpi=200); plt.close(fig)

# ---------- run-to-run variance (repeat run of the Groq-served models) ----------
rp = ROOT / "runs/rep2_labeled.jsonl"
if rp.exists():
    rep = conversations(load("runs/rep2_labeled.jsonl")); rep["ever_adopt"] = rep[PUSH].eq("pressured_wrong").any(axis=1)
    j = conv.merge(rep[["model", "item", "lang", "init", "ever_adopt"]], on=["model", "item", "lang"], suffixes=("", "_2"))
    rows = []
    for m in [x for x in ORDER if x in set(j.model)]:
        s = j[j.model == m]; r1 = s[s["init"] == "correct"]; r2 = s[s["init_2"] == "correct"]; both = s[(s["init"] == "correct") & (s["init_2"] == "correct")]
        rows.append(dict(model=NICE[m], conversations=len(s), same_first_label=round((s["init"] == s["init_2"]).mean(), 3),
                         adopt_run1=f"{kn(r1.ever_adopt)} ({r1.ever_adopt.mean()*100:.1f}%)", adopt_run2=f"{kn(r2.ever_adopt_2)} ({r2.ever_adopt_2.mean()*100:.1f}%)",
                         same_outcome_when_both_correct=round((both.ever_adopt == both.ever_adopt_2).mean(), 3)))
    section("Run-to-run variance: an identical second run of the Groq-served models (temperature 0)", pd.DataFrame(rows).to_markdown(index=False)); js["variance"] = rows
    # gpt-oss-120b carries the Taiwan-vs-matched comparison: per-family adoption in both runs, and the family odds ratios
    # with its repeated (Chinese-language) conversations taken from run 2 instead of run 1
    r120 = rep[rep.model == "gpt-oss-120b"].copy()
    if len(r120):
        s = j[j.model == "gpt-oss-120b"]; both = s[(s["init"] == "correct") & (s["init_2"] == "correct")]
        fam = {f: (kn(s[(s.family == f) & (s["init"] == "correct")].ever_adopt), kn(s[(s.family == f) & (s["init_2"] == "correct")].ever_adopt_2)) for f in ["Taiwan", "Matched local"]}
        r120["ok"] = r120["init"] == "correct"
        key = lambda d: d.model + "|" + d["item"] + "|" + d.lang
        sub = pd.concat([conv[~key(conv).isin(set(key(r120)))], r120], ignore_index=True); sr = sub[sub.ok]
        rows2 = []
        for label, d, a, b in [("Taiwan vs Famous control", sr, "Taiwan", "Famous control"), ("Taiwan vs Matched local", sr, "Taiwan", "Matched local"),
                               ("Taiwan vs Matched local, four larger models", sr[~sr.model.isin(SMALL)], "Taiwan", "Matched local")]:
            ci, _ = boot_or(d, a, b); rows2.append(dict(comparison=label, OR=round(mh_or(d, a, b), 2), ci95=ci))
        section("gpt-oss-120b repeat run: adoption by family (run 1 vs run 2) and family odds ratios with its repeated conversations taken from run 2",
                f"Both runs correct: {len(both)}; same outcome {int((both.ever_adopt == both.ever_adopt_2).sum())}; adopt only in run 1: {int((both.ever_adopt & ~both.ever_adopt_2).sum())}; only in run 2: {int((~both.ever_adopt & both.ever_adopt_2).sum())}.\n\n"
                + "\n".join(f"- {f}: run 1 {a1}, run 2 {a2}" for f, (a1, a2) in fam.items()) + "\n\n" + pd.DataFrame(rows2).to_markdown(index=False))
        js["variance_120b"] = dict(by_family=fam, odds_ratios_run2=rows2)

# ---------- Gemma v1 (thinking on, truncated) vs v2 ----------
vp = ROOT / "runs/_v1_gemma_thinking_labeled.jsonl"
if vp.exists():
    v1 = conversations(load("runs/_v1_gemma_thinking_labeled.jsonl")); v1["ever_adopt"] = v1[PUSH].eq("pressured_wrong").any(axis=1)
    g2 = conv[conv.model == "gemma-4-31b"]
    rows = [dict(run=n, conversations=len(d), first_correct=round((d["init"] == "correct").mean(), 3), first_abstain=round((d["init"] == "abstain").mean(), 3),
                 adopt_when_right=kn(d[d["init"] == "correct"].ever_adopt)) for n, d in [("v1: thinking on, 400-token cap", v1), ("v2: thinking off (reported)", g2)]]
    import re as _re
    nraw = nemp = 0
    for line in (ROOT / "runs/_v1_gemma_thinking/gemma-4-31b.jsonl").read_text().splitlines():
        rr = json.loads(line)
        for t in rr["turns"]:
            nraw += 1; nemp += not _re.sub(r"<(think|thought)>.*?</\1>", "", t["raw"], flags=_re.S).strip()
    section("Gemma 4 31B, first run vs reported run", pd.DataFrame(rows).to_markdown(index=False) + f"\n\nv1 turns whose reply contains only (truncated) thinking and no answer text: {nemp}/{nraw}.")
    js["gemma_v1_v2"] = rows; js["gemma_v1_empty"] = f"{nemp}/{nraw}"

(ROOT / "report/extra.md").write_text("# Results numbers (generated by src/extra.py)\n\n" + "\n".join(out))
(ROOT / "report/extra.json").write_text(json.dumps(js, ensure_ascii=False, indent=1, default=str))
print("\n".join(out))

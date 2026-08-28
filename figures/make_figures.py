import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

T = "/home/user/workspace/supp_results/tables"
OUT = "/home/user/workspace/figures"
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.6,
    "figure.dpi": 300,
})
TEAL = "#20808D"; RUST = "#A84B2F"; DARK = "#1B474D"; GOLD = "#FFC553"

ci = pd.read_csv(f"{T}/bootstrap_model_accuracy_ci.csv")
ms = pd.read_csv(f"{T}/multiseed_summary.csv")

order = ["baseline", "SE", "CBAM", "LTA"]
labels = {"baseline": "No attention\n(baseline)", "SE": "SE", "CBAM": "CBAM", "LTA": "LTA"}
seeds = [42, 123, 2026]
markers = {42: "o", 123: "s", 2026: "^"}

# ---- Figure: per-run Top-1 with bootstrap 95% CI, grouped by variant ----
fig, ax = plt.subplots(figsize=(7.0, 4.2))
for i, v in enumerate(order):
    sub = ci[ci["variant"] == v]
    for j, s in enumerate(seeds):
        r = sub[sub["seed"] == s].iloc[0]
        x = i + (j - 1) * 0.22
        lo = r["top1_pct"] - r["top1_ci95_low"]
        hi = r["top1_ci95_high"] - r["top1_pct"]
        ax.errorbar(x, r["top1_pct"], yerr=[[lo], [hi]], fmt=markers[s],
                    color=TEAL, ecolor="#8FB8BE", elinewidth=1.4, capsize=3.5,
                    markersize=6, markeredgecolor="white", markeredgewidth=0.7,
                    label=f"seed {s}" if i == 0 else None, zorder=3)

base_mean = float(ms[ms["variant"] == "baseline"]["top1_mean_pct"].iloc[0])
ax.axhline(base_mean, color=RUST, lw=1.3, ls="--", zorder=2,
           label=f"Baseline 3-seed mean ({base_mean:.2f}%)")
ax.set_xticks(range(len(order)))
ax.set_xticklabels([labels[v] for v in order])
ax.set_ylabel("Test Top-1 accuracy (%)")
ax.set_ylim(76, 89)
ax.set_title("All attention variants fall within the baseline's sampling uncertainty\n"
             "(YOLOv12s-cls, 39-class test set, n = 636, bootstrap 95% CIs)",
             fontsize=10.5, loc="left")
ax.legend(frameon=False, fontsize=8.5, ncol=2, loc="upper left")
fig.tight_layout()
fig.savefig(f"{OUT}/fig_multiseed_attention_ci.png", bbox_inches="tight")
plt.close(fig)

# ---- Figure: paired within-seed deltas ----
pd_diff = pd.read_csv(f"{T}/bootstrap_paired_differences.csv")
fig, ax = plt.subplots(figsize=(7.0, 3.6))
comps = ["SE - baseline", "CBAM - baseline", "LTA - baseline"]
ypos = []
ylab = []
k = 0
for c in comps:
    for s in seeds:
        r = pd_diff[(pd_diff["comparison"] == c) & (pd_diff["seed"] == s)].iloc[0]
        lo = r["delta_top1_pp"] - r["delta_ci95_low_pp"]
        hi = r["delta_ci95_high_pp"] - r["delta_top1_pp"]
        ax.errorbar(r["delta_top1_pp"], k, xerr=[[lo], [hi]], fmt="o",
                    color=DARK, ecolor="#9DBEC2", elinewidth=1.4, capsize=3.5,
                    markersize=5.5, zorder=3)
        ypos.append(k); ylab.append(f"{c.split(' -')[0]}, seed {s}")
        k += 1
    k += 0.6
ax.axvline(0, color=RUST, lw=1.3, ls="--", zorder=2)
ax.axvline(1.42, color=GOLD, lw=1.6, ls=":", zorder=2,
           label="Originally reported single-seed gain (+1.42 pp)")
ax.set_yticks(ypos); ax.set_yticklabels(ylab, fontsize=8.5)
ax.invert_yaxis()
ax.set_xlabel("Δ Top-1 vs. no-attention baseline (percentage points)")
ax.set_title("Every paired 95% CI includes zero", fontsize=10.5, loc="left")
ax.set_xlim(-4.3, 3.6)
ax.legend(frameon=False, fontsize=8.5, loc="upper center", bbox_to_anchor=(0.5, -0.24))
fig.tight_layout()
fig.savefig(f"{OUT}/fig_paired_bootstrap_deltas.png", bbox_inches="tight")
plt.close(fig)

# ---- Figure: accuracy vs robustness vs latency ----
rob = pd.DataFrame({
    "model": ["YOLOv12s-cls", "YOLOv12s-cls + LTA", "EfficientNet-B0"],
    "clean": [82.39, 83.81, 84.43],
    "avg_drop": [23.38, 25.69, 46.17],
    "params": [6.02, 6.05, 4.06],
    "latency": [0.856, 0.864, 1.739],
})
fig, axes = plt.subplots(1, 2, figsize=(9.2, 3.9))
cols = [TEAL, DARK, RUST]
ax = axes[0]
for i, r in rob.iterrows():
    ax.scatter(r["avg_drop"], r["clean"], s=r["params"] * 42, color=cols[i],
               alpha=0.85, edgecolor="white", linewidth=1.0, zorder=3)
    ax.annotate(f"{r['model']}\n({r['params']:.2f} M)",
                (r["avg_drop"], r["clean"]), textcoords="offset points",
                xytext=(0, -30), ha="center", fontsize=8.2)
ax.set_xlabel("Mean accuracy drop under perturbation (pp)")
ax.set_ylabel("Clean Top-1 accuracy (%)")
ax.set_xlim(15, 55); ax.set_ylim(79.5, 86.5)
ax.set_title("Accuracy vs. robustness", fontsize=10.5, loc="left")

ax = axes[1]
bars = ax.bar(rob["model"], rob["latency"], color=cols, width=0.55, zorder=3)
for b, v in zip(bars, rob["latency"]):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.03, f"{v:.2f}", ha="center", fontsize=9)
ax.set_ylabel("Mean inference time (ms / image)")
ax.set_ylim(0, 2.1)
ax.set_xticklabels(["YOLOv12s-cls", "YOLOv12s-cls\n+ LTA", "EfficientNet-B0"], fontsize=8.5)
ax.set_title("Single-image latency (Tesla T4)", fontsize=10.5, loc="left")
fig.tight_layout()
fig.savefig(f"{OUT}/fig_accuracy_robustness_latency.png", bbox_inches="tight")
plt.close(fig)

print("done", os.listdir(OUT))

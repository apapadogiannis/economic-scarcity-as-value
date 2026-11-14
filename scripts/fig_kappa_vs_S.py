"""Figure 5 of the paper: structural coefficient kappa against the physical scarcity
score S_t (beta = 1.5) for the three networks.
Usage: python3 -I fig_kappa_vs_S.py DATA_DIR OUT_DIR"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # noqa: E702 (needed under python -I)
from common import args, load, paper_style
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import config
from scarcity import scarcity_score, scarcity_table

LABELS = {"BTC": "Bitcoin", "ETH": "Ethereum", "TAO": "Bittensor"}
LIGHT_BLUE, GREEN = (0.6, 0.6, 1.0), (0.0, 0.6, 0.0)   # pgfplots blue!40, green!60!black


def main():
    data_dir, out = args()
    inputs, components = load(data_dir)
    t = scarcity_table(components, inputs, config.BETA_BASE).set_index("network")
    # label from the unrounded score: the table stores S to four decimals, and rounding
    # that again would print Bittensor's 0.42651 as 0.426 instead of 0.427
    t["S"] = [scarcity_score(t.loc[n, "kappa"], t.loc[n, "pi"], config.BETA_BASE) for n in t.index]
    paper_style()
    x = np.arange(len(config.NETWORKS)); w = 0.075
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    b1 = ax.bar(x - w / 2, [t.loc[n, "kappa"] for n in config.NETWORKS], w, color=LIGHT_BLUE,
                edgecolor="blue", linewidth=0.8, zorder=2, label=r"$\kappa$ (Structural Coefficient)")
    b2 = ax.bar(x + w / 2, [t.loc[n, "S"] for n in config.NETWORKS], w, color=GREEN,
                edgecolor="red", linewidth=0.8, zorder=2, label=r"$S_t$ (Physical Scarcity)")
    for bars, color, dx, dy in ((b1, "blue", -8, 8), (b2, "red", 8, 2)):
        for b in bars:
            ax.annotate(f"{b.get_height():.3f}", (b.get_x() + b.get_width() / 2, b.get_height()),
                        xytext=(dx, dy), textcoords="offset points", ha="center", va="bottom",
                        color=color, fontsize=9)
    ax.set_xticks(x); ax.set_xticklabels([LABELS[n] for n in config.NETWORKS])
    ax.set_xlim(-0.5, len(config.NETWORKS) - 0.5)
    ax.set_ylim(0, 1.15); ax.set_ylabel(r"Score (0$-$1)")
    ax.set_title("Structural Coefficient vs. Physical Scarcity Score", fontfamily="cmb10")
    ax.yaxis.set_major_formatter("{x:g}")
    ax.grid(axis="y", linestyle=(0, (4, 4)), linewidth=0.6, color="0.6", zorder=0)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncol=2, loc="lower center", bbox_to_anchor=(0.5, 1.08), fontsize=10)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out, f"fig_kappa_vs_S.{ext}"), bbox_inches="tight", dpi=200)


if __name__ == "__main__":
    main()

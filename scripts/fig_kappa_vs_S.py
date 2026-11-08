"""Figure 5 of the paper (matplotlib equivalent of the in-text pgfplots exhibit):
structural coefficient kappa against physical scarcity S for the three networks.
Usage: python3 -I fig_kappa_vs_S.py DATA_DIR OUT_DIR"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # noqa: E702 (needed under python -I)
from common import args, load
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import config
from scarcity import scarcity_table

LABELS = {"BTC": "Bitcoin", "ETH": "Ethereum", "TAO": "Bittensor"}


def main():
    data_dir, out = args()
    inputs, components = load(data_dir)
    t = scarcity_table(components, inputs, config.BETA_BASE).set_index("network")
    x = np.arange(len(config.NETWORKS)); w = 0.35
    fig, ax = plt.subplots(figsize=(6, 4))
    b1 = ax.bar(x - w / 2, [t.loc[n, "kappa"] for n in config.NETWORKS], w,
                label=r"$\kappa$ (structural coefficient)", color="#8a8a8a")
    b2 = ax.bar(x + w / 2, [t.loc[n, "S"] for n in config.NETWORKS], w,
                label=r"$S_t$ (physical scarcity, $\beta=1.5$)", color="#404040")
    ax.bar_label(b1, fmt="%.3f", fontsize=8); ax.bar_label(b2, fmt="%.3f", fontsize=8)
    ax.set_xticks(x); ax.set_xticklabels([LABELS[n] for n in config.NETWORKS])
    ax.set_ylim(0, 1.05); ax.set_ylabel("Score (0-1)")
    ax.set_title("Structural coefficient vs. physical scarcity (5 August 2025)")
    ax.legend(frameon=False)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out, f"fig_kappa_vs_S.{ext}"), bbox_inches="tight", dpi=200)


if __name__ == "__main__":
    main()

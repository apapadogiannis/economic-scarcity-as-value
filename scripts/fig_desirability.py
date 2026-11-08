"""Figure 6 of the paper (matplotlib equivalent of the in-text pgfplots exhibit):
implied desirability under the common convention, with alpha whiskers and the
Bittensor user-count band.  Usage: python3 -I fig_desirability.py DATA_DIR OUT_DIR"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # noqa: E702 (needed under python -I)
from common import args, load
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import config
from sensitivity import alpha_beta_grid

COLORS = {"BTC": "#e8862e", "ETH": "#5b7fd4", "TAO": "#3fa47a"}
LABELS = {"BTC": "Bitcoin", "ETH": "Ethereum", "TAO": "Bittensor"}


def main():
    data_dir, out = args()
    inputs, components = load(data_dir)
    grid = alpha_beta_grid(inputs, components)
    base = grid[(grid.alpha == config.ALPHA_BASE) & (grid.beta == config.BETA_BASE)
                & (grid.user_scenario == "base")].set_index("network")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for i, net in enumerate(config.NETWORKS):
        d = base.loc[net, "D_usd"]
        g = grid[(grid.network == net) & (grid.beta == config.BETA_BASE)
                 & (grid.user_scenario == "base") & (grid.alpha.isin([1.8, 2.0, 2.2]))]
        ax.errorbar(i, d, yerr=[[d - g.D_usd.min()], [g.D_usd.max() - d]], fmt="o",
                    color=COLORS[net], capsize=5, markersize=9, label=LABELS[net])
        if net == "TAO":
            gu = grid[(grid.network == "TAO") & (grid.beta == config.BETA_BASE)
                      & (grid.alpha == config.ALPHA_BASE)]
            ax.vlines(i + 0.12, gu.D_usd.min(), gu.D_usd.max(), color=COLORS[net], lw=6, alpha=0.35)
            ax.annotate("user-count range\n(15k-90k)", (i + 0.16, d), fontsize=8, color=COLORS[net])
    ax.set_yscale("log"); ax.set_xticks(range(3)); ax.set_xticklabels([LABELS[n] for n in config.NETWORKS])
    ax.set_ylabel(r"Implied desirability $D$ (USD; $u_0=10^6$, $\alpha=2$, $\beta=1.5$)")
    ax.set_title(r"Implied desirability with $\alpha$-sensitivity (whiskers) and TAO user range (band)")
    ax.grid(axis="y", alpha=0.3, which="both")
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out, f"fig_desirability.{ext}"), bbox_inches="tight", dpi=200)


if __name__ == "__main__":
    main()

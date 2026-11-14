"""Figure 6 of the paper: implied desirability under the common convention
(u0 = 10^6, alpha = 2, beta = 1.5), in trillion USD on a log scale.  Whiskers: for
Ethereum the sensitivity to alpha in [1.8, 2.2]; for Bittensor the native user-count
range at the baseline alpha.  Bitcoin has u/u0 = 1 and is alpha-invariant.
Usage: python3 -I fig_desirability.py DATA_DIR OUT_DIR"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # noqa: E702 (needed under python -I)
from common import args, load, paper_style
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import config
from sensitivity import alpha_beta_grid

LABELS = {"BTC": "Bitcoin", "ETH": "Ethereum", "TAO": "Bittensor"}
GREEN, BLUE = (0.0, 0.6, 0.0), "blue"   # pgfplots green!60!black fill, blue outline


def main():
    data_dir, out = args()
    inputs, components = load(data_dir)
    grid = alpha_beta_grid(inputs, components)
    grid = grid[grid.beta == config.BETA_BASE].assign(D=lambda d: d.D_usd / 1e12)
    paper_style()
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    for i, net in enumerate(config.NETWORKS):
        g = grid[grid.network == net]
        d = g[(g.alpha == config.ALPHA_BASE) & (g.user_scenario == "base")].D.iloc[0]
        # one whisker per network: the user range where the network has one, else alpha
        users = g[g.alpha == config.ALPHA_BASE].D
        alphas = g[(g.user_scenario == "base") & g.alpha.isin([1.8, 2.0, 2.2])].D
        rng = users if users.max() > users.min() else alphas
        ax.bar(i, d, width=0.17, color=GREEN, edgecolor=BLUE, linewidth=0.8, zorder=2)
        if rng.max() > rng.min():
            ax.errorbar(i, d, yerr=[[d - rng.min()], [rng.max() - d]], fmt="none",
                        ecolor=BLUE, elinewidth=0.8, capsize=3, capthick=0.8, zorder=3)
        ax.annotate(f"{d:.2f}", (i, d), xytext=(0, 5), textcoords="offset points",
                    ha="center", va="bottom", color=BLUE, fontsize=11, zorder=4,
                    bbox=dict(facecolor="white", edgecolor="none", pad=0.6))
    ax.set_yscale("log"); ax.set_ylim(0.5, 60); ax.set_xlim(-0.5, len(config.NETWORKS) - 0.5)
    ax.set_xticks(range(len(config.NETWORKS)))
    ax.set_xticklabels([LABELS[n] for n in config.NETWORKS])
    ax.set_ylabel(r"Implied desirability $D_t$ (trillion USD; $u_0 = 10^6$, $\alpha = 2$)", fontsize=9)
    ax.set_title("Implied Desirability under the Common Convention", fontfamily="cmb10")
    ax.grid(axis="y", which="major", linestyle=(0, (4, 4)), linewidth=0.6, color="0.6", zorder=0)
    ax.set_axisbelow(True)
    for ext in ("pdf", "png"):
        fig.savefig(os.path.join(out, f"fig_desirability.{ext}"), bbox_inches="tight", dpi=200)


if __name__ == "__main__":
    main()

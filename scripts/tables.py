"""Scarcity and implied-desirability tables (paper Tables 6 and 7 inputs,
Section 5.3 baseline).  Usage: python3 -I tables.py DATA_DIR OUT_DIR"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # noqa: E702 (needed under python -I)
from common import args, load, to_tex
import os
import pandas as pd

import config
from desirability import implied_desirability
from scarcity import kappa, scarcity_score, scarcity_table
from sensitivity import _inputs_map, users


def main():
    data_dir, out = args()
    inputs, components = load(data_dir)

    t = scarcity_table(components, inputs, config.BETA_BASE)
    t.to_csv(os.path.join(out, "tab_scarcity.csv"), index=False)
    to_tex(t, os.path.join(out, "tab_scarcity.tex"),
           "Component-level physical scarcity scores ($\\beta=1.5$).", "tab:scarcity")

    im = _inputs_map(inputs)
    comp = components.set_index("network")
    rows = []
    for net in config.NETWORKS:
        k = kappa(comp.loc[net])
        S = scarcity_score(k, im[net]["inflation_rate"], config.BETA_BASE)
        u = users(net, im, "base")
        D = implied_desirability(im[net]["market_cap"], S, u, config.ALPHA_BASE, config.U0)
        rows.append(dict(network=net, V_usd=im[net]["market_cap"], S=round(S, 4), u=u,
                         u_tilde=round(u / config.U0, 4), alpha=config.ALPHA_BASE, D_usd=D))
    base = pd.DataFrame(rows)
    base.to_csv(os.path.join(out, "tab_desirability.csv"), index=False)
    to_tex(base, os.path.join(out, "tab_desirability.tex"),
           "Implied desirability under the common convention ($u_0=10^6$, $\\alpha=2$, $\\beta=1.5$).",
           "tab:desirability")

    pd.set_option("display.float_format", lambda v: f"{v:,.4g}")
    print(t.to_string(index=False)); print(); print(base.to_string(index=False))


if __name__ == "__main__":
    main()

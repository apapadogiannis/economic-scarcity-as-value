"""All sensitivity analyses of the appendix: common-alpha and beta grids, the
Bittensor user range, component-weight perturbations, the n log n specification,
the u0-rescaling invariance check, and the component-score perturbation test.
Usage: python3 -I sensitivity_runs.py DATA_DIR OUT_DIR"""
import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # noqa: E702 (needed under python -I)
from common import args, load, to_tex
import os
import pandas as pd

import config
from sensitivity import (alpha_beta_grid, nlogn_spec, rescaling_invariance,
                         score_perturbation, weight_sensitivity)


def main():
    data_dir, out = args()
    inputs, components = load(data_dir)

    grid = alpha_beta_grid(inputs, components)
    grid.to_csv(os.path.join(out, "sens_alpha_beta_users.csv"), index=False)
    appc = grid[(grid.beta == config.BETA_BASE) & (grid.user_scenario == "base")].pivot(
        index="network", columns="alpha", values="D_usd").reset_index()
    to_tex(appc, os.path.join(out, "tab_alpha.tex"),
           "Sensitivity of implied desirability (USD) to a common $\\alpha$.", "tab:alpha", "%.3g")

    weight_sensitivity(inputs, components).to_csv(os.path.join(out, "sens_weights.csv"), index=False)
    nlogn_spec(inputs, components).to_csv(os.path.join(out, "sens_nlogn.csv"), index=False)
    rs = rescaling_invariance(inputs, components)
    rs.to_csv(os.path.join(out, "sens_rescaling.csv"), index=False)

    sp = score_perturbation(inputs, components)
    sp["oat"].to_csv(os.path.join(out, "sens_scores_one_at_a_time.csv"), index=False)
    pd.DataFrame([{k: v for k, v in sp.items() if k != "oat"}]).to_csv(
        os.path.join(out, "sens_scores_summary.csv"), index=False)

    print(rs[["spec", "U0", "ordering"]].to_string(index=False))
    print("score perturbation (delta=%.2f): one-at-a-time flips S/D = %d/%d of %d; "
          "joint MC preserves S %.3f, D %.3f" % (sp["delta"], sp["oat_S_flips"], sp["oat_D_flips"],
          sp["oat_cases"], sp["mc_share_S_preserved"], sp["mc_share_D_preserved"]))


if __name__ == "__main__":
    main()

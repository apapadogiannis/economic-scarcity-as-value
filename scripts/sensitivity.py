"""Sensitivity analyses reported in the paper's appendix:

1. alpha-sensitivity of D (common alpha applied to all protocols),
2. beta-sensitivity of S,
3. TAO user-count scenarios (low / base / high),
4. scarcity-component weight perturbations,
5. n log n network-effect specification,
6. unit-rescaling check: ordering of D is invariant to the choice of U0
   when a common alpha is used (demonstrated numerically).
"""
from __future__ import annotations

import itertools

import pandas as pd

import config
from desirability import implied_desirability, implied_desirability_nlogn
from scarcity import COMPONENTS, kappa, scarcity_score


def _inputs_map(inputs: pd.DataFrame) -> dict:
    g = {}
    for net in config.NETWORKS:
        sub = inputs[inputs["network"] == net].set_index("variable")["value"]
        g[net] = sub.astype(float).to_dict()
    return g


def users(net: str, im: dict, tao_scenario: str = "base") -> float:
    if net == "TAO":
        return config.TAO_USER_SCENARIOS[tao_scenario]
    return im[net]["active_users"]


def alpha_beta_grid(inputs: pd.DataFrame, components: pd.DataFrame) -> pd.DataFrame:
    im = _inputs_map(inputs)
    comp = components.set_index("network")
    rows = []
    for alpha, beta in itertools.product(config.ALPHA_GRID, config.BETA_GRID):
        for net in config.NETWORKS:
            k = kappa(comp.loc[net])
            S = scarcity_score(k, im[net]["inflation_rate"], beta)
            scen_list = (config.TAO_USER_SCENARIOS if net == "TAO"
                         else {"base": im[net]["active_users"]})
            for scen, u in scen_list.items():
                D = implied_desirability(im[net]["market_cap"], S, u,
                                         alpha, config.U0)
                rows.append(dict(network=net, alpha=alpha, beta=beta,
                                 user_scenario=scen, u=u, S=round(S, 4),
                                 D_usd=D))
    return pd.DataFrame(rows)


def weight_sensitivity(inputs: pd.DataFrame, components: pd.DataFrame,
                       beta: float = config.BETA_BASE) -> pd.DataFrame:
    """Perturb each component weight to 2x (others 1x) and report kappa, S."""
    im = _inputs_map(inputs)
    comp = components.set_index("network")
    rows = []
    schemes = {"equal": None}
    for c in COMPONENTS:
        schemes[f"2x_{c}"] = {k: (2.0 if k == c else 1.0) for k in COMPONENTS}
    for name, w in schemes.items():
        for net in config.NETWORKS:
            k = kappa(comp.loc[net], w)
            S = scarcity_score(k, im[net]["inflation_rate"], beta)
            rows.append(dict(scheme=name, network=net,
                             kappa=round(k, 4), S=round(S, 4)))
    return pd.DataFrame(rows)


def nlogn_spec(inputs: pd.DataFrame, components: pd.DataFrame,
               beta: float = config.BETA_BASE) -> pd.DataFrame:
    im = _inputs_map(inputs)
    comp = components.set_index("network")
    rows = []
    for net in config.NETWORKS:
        k = kappa(comp.loc[net])
        S = scarcity_score(k, im[net]["inflation_rate"], beta)
        for scen in (["low", "base", "high"] if net == "TAO" else ["base"]):
            u = users(net, im, scen)
            D = implied_desirability_nlogn(im[net]["market_cap"], S, u,
                                           config.U0)
            rows.append(dict(network=net, user_scenario=scen, u=u,
                             S=round(S, 4), D_nlogn_usd=D))
    return pd.DataFrame(rows)


def rescaling_invariance(inputs: pd.DataFrame, components: pd.DataFrame) -> pd.DataFrame:
    """Numerical demonstration for the paper's normalization discussion: with a COMMON alpha, changing U0 rescales all D identically
    (ordering invariant); with protocol-specific alphas it does not."""
    im = _inputs_map(inputs)
    comp = components.set_index("network")
    rows = []
    for u0 in [1.0, 1.0e3, 1.0e6]:
        for spec, alphas in {
            "common_alpha": {"BTC": 2.0, "ETH": 2.0, "TAO": 2.0},
            "mixed_alpha": {"BTC": 2.0, "ETH": 2.0, "TAO": 2.5},
        }.items():
            Ds = {}
            for net in config.NETWORKS:
                k = kappa(comp.loc[net])
                S = scarcity_score(k, im[net]["inflation_rate"],
                                   config.BETA_BASE)
                u = users(net, im, "base")
                Ds[net] = implied_desirability(im[net]["market_cap"], S, u,
                                               alphas[net], u0)
            order = ">".join(sorted(Ds, key=Ds.get, reverse=True))
            rows.append(dict(spec=spec, U0=u0, ordering=order,
                             **{f"D_{n}": Ds[n] for n in config.NETWORKS}))
    return pd.DataFrame(rows)


def score_perturbation(inputs: pd.DataFrame, components: pd.DataFrame, delta: float = 0.15,
                       n_draws: int = 20000, seed: int = 20250805) -> dict:
    """Robustness of the cross-protocol orderings to the component scores
    themselves (the scores are expert assessments on a documented rubric).

    Two exercises:
    (a) one-at-a-time: every single component score of every network is
        moved by +/- delta (clipped to [0,1]); report whether the ordering of
        S and of baseline D changes in any case;
    (b) joint Monte Carlo: all 15 scores perturbed simultaneously by
        independent uniform(-delta, +delta) shocks; report the share of draws
        preserving the baseline orderings.
    """
    import numpy as np
    im = _inputs_map(inputs)
    comp = components.set_index("network")
    base_scores = {n: np.array([comp.loc[n, c] for c in COMPONENTS], float)
                   for n in config.NETWORKS}

    def orderings(scores):
        S, D = {}, {}
        for n in config.NETWORKS:
            k = float(scores[n].mean())
            S[n] = scarcity_score(k, im[n]["inflation_rate"], config.BETA_BASE)
            D[n] = implied_desirability(im[n]["market_cap"], S[n],
                                        users(n, im, "base"),
                                        config.ALPHA_BASE, config.U0)
        oS = tuple(sorted(S, key=S.get, reverse=True))
        oD = tuple(sorted(D, key=D.get, reverse=True))
        return oS, oD

    oS0, oD0 = orderings(base_scores)

    # (a) one-at-a-time
    oat_rows, flips_S, flips_D = [], 0, 0
    for n in config.NETWORKS:
        for i, c in enumerate(COMPONENTS):
            for sgn in (-1, 1):
                sc = {k: v.copy() for k, v in base_scores.items()}
                sc[n][i] = float(np.clip(sc[n][i] + sgn * delta, 0, 1))
                oS, oD = orderings(sc)
                flips_S += oS != oS0
                flips_D += oD != oD0
                oat_rows.append(dict(network=n, component=c, shift=sgn * delta,
                                     S_order=">".join(oS), D_order=">".join(oD),
                                     S_order_changed=oS != oS0,
                                     D_order_changed=oD != oD0))

    # (b) joint Monte Carlo
    rng = np.random.default_rng(seed)
    keep_S = keep_D = 0
    for _ in range(n_draws):
        sc = {k: np.clip(v + rng.uniform(-delta, delta, size=len(COMPONENTS)),
                         0, 1) for k, v in base_scores.items()}
        oS, oD = orderings(sc)
        keep_S += oS == oS0
        keep_D += oD == oD0

    return dict(delta=delta, baseline_S_order=">".join(oS0),
                baseline_D_order=">".join(oD0),
                oat=pd.DataFrame(oat_rows), oat_S_flips=flips_S,
                oat_D_flips=flips_D, oat_cases=len(oat_rows),
                mc_draws=n_draws, mc_share_S_preserved=keep_S / n_draws,
                mc_share_D_preserved=keep_D / n_draws)

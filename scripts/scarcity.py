"""Physical scarcity: the paper's scarcity equations, computed consistently.

    kappa = (C + E + B + G + R) / 5                      (Eq. 7)
    S_t   = kappa * (1 - pi_t) ** beta                   (Eq. 6)

All scores and inflation rates are read from the data files; nothing is
hard-coded in the computation.
"""
from __future__ import annotations

import pandas as pd

COMPONENTS = ["C", "E", "B", "G", "R"]


def kappa(row: pd.Series, weights: dict | None = None) -> float:
    """Structural discipline coefficient. Equal weights by default (Eq. 7);
    a weights dict {component: w} enables the weight-sensitivity analysis."""
    if weights is None:
        return float(sum(row[c] for c in COMPONENTS) / len(COMPONENTS))
    total_w = sum(weights[c] for c in COMPONENTS)
    return float(sum(weights[c] * row[c] for c in COMPONENTS) / total_w)


def scarcity_score(kappa_val: float, pi: float, beta: float) -> float:
    """Physical scarcity S_t (Eq. 6). Requires 0 <= pi < 1."""
    if not 0.0 <= pi < 1.0:
        raise ValueError(f"inflation rate out of range: {pi}")
    return kappa_val * (1.0 - pi) ** beta


def scarcity_table(components: pd.DataFrame, inputs: pd.DataFrame,
                   beta: float) -> pd.DataFrame:
    """Scarcity table for a given beta."""
    comp = components.set_index("network")
    pi = (inputs[inputs["variable"] == "inflation_rate"]
          .set_index("network")["value"].astype(float))
    rows = []
    for net in comp.index:
        k = kappa(comp.loc[net])
        rows.append({
            "network": net,
            "pi": pi[net],
            **{c: comp.loc[net, c] for c in COMPONENTS},
            "kappa": round(k, 4),
            "S": round(scarcity_score(k, pi[net], beta), 4),
        })
    return pd.DataFrame(rows)

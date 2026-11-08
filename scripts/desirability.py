"""Implied desirability: D = V / (S * u_tilde**alpha), u_tilde = u / U0.

D is an implied (attribution) quantity, analogous to implied volatility: the
residual of market capitalization not explained by measured scarcity and
adoption under the stated (U0, alpha) convention. It absorbs expectations,
liquidity conditions, speculative demand and measurement error alongside
protocol utility, and is interpreted accordingly in the paper.

Scale behaviour: replacing U0 by U0/c multiplies D by c**alpha. With a common
alpha across protocols the rescaling is uniform and the cross-protocol
ordering of D is invariant; with protocol-specific alphas it is not.
"""
from __future__ import annotations

import math


def implied_desirability(V: float, S: float, u: float,
                         alpha: float, u0: float) -> float:
    """D = V / (S * (u/u0)**alpha)."""
    if min(V, S, u, u0) <= 0:
        raise ValueError("V, S, u, u0 must all be positive")
    return V / (S * (u / u0) ** alpha)


def implied_desirability_nlogn(V: float, S: float, u: float,
                               u0: float) -> float:
    """Robustness specification with F(u) = (u/u0) * log(1+u), following the
    n log n scaling argued by Briscoe, Odlyzko and Tilly (2006)."""
    if min(V, S, u, u0) <= 0:
        raise ValueError("V, S, u, u0 must all be positive")
    return V / (S * (u / u0) * math.log(1.0 + u))

"""Consistency tests for the replication package.

Run: python3 -m pytest -q tests/
"""
import os
import sys

import pandas as pd
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))

import config
from desirability import implied_desirability
from scarcity import scarcity_score, scarcity_table
from sensitivity import rescaling_invariance, score_perturbation


@pytest.fixture(scope="module")
def data():
    d = os.path.join(HERE, "..", "data")
    return (pd.read_csv(os.path.join(d, "inputs_2025-08.csv")),
            pd.read_csv(os.path.join(d, "scarcity_components.csv")))


def test_scarcity_never_exceeds_kappa(data):
    """S = kappa (1-pi)^beta <= kappa whenever pi >= 0 and beta > 0."""
    inputs, components = data
    t = scarcity_table(components, inputs, config.BETA_BASE)
    assert (t.S <= t.kappa + 1e-12).all()


def test_scarcity_values(data):
    inputs, components = data
    t = scarcity_table(components, inputs, config.BETA_BASE).set_index("network")
    assert t.loc["BTC", "kappa"] == pytest.approx(0.80, abs=1e-9)
    assert t.loc["BTC", "S"] == pytest.approx(0.80 * 0.983 ** 1.5, abs=1e-4)
    assert t.loc["ETH", "S"] == pytest.approx(0.68 * 0.9931 ** 1.5, abs=1e-4)
    assert t.loc["TAO", "kappa"] == pytest.approx(0.60, abs=1e-9)


def test_desirability_units():
    assert implied_desirability(2.3e12, 0.78, 1e6, 2.0, 1e6) == pytest.approx(2.3e12 / 0.78)


def test_rescaling_identity():
    """D' = c**alpha * D when u -> u/c."""
    V, S, u, alpha, c = 1e9, 0.5, 5e4, 2.3, 1e3
    assert (implied_desirability(V, S, u / c, alpha, 1.0)
            / implied_desirability(V, S, u, alpha, 1.0)) == pytest.approx(c ** alpha, rel=1e-9)


def test_u0_ordering_invariance(data):
    """Common alpha: ordering invariant to u0. Mixed alphas: it is not."""
    inputs, components = data
    rs = rescaling_invariance(inputs, components)
    assert rs[rs.spec == "common_alpha"].ordering.nunique() == 1
    assert rs[rs.spec == "mixed_alpha"].ordering.nunique() > 1


def test_score_perturbation_robustness(data):
    """Orderings of S and D survive +/-0.15 shifts of any single component score."""
    inputs, components = data
    sp = score_perturbation(inputs, components, n_draws=2000)
    assert sp["oat_S_flips"] == 0 and sp["oat_D_flips"] == 0
    assert sp["mc_share_D_preserved"] > 0.95


def test_inflation_bounds():
    with pytest.raises(ValueError):
        scarcity_score(0.8, 1.2, 1.5)

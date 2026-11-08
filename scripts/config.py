"""Modelling conventions used throughout the replication package.

NORMALIZATION. User counts enter the valuation equation as the dimensionless
ratio u_tilde = u / U0 with one common reference scale U0 = 1e6 users for all
protocols. Implied desirability D then carries units of USD and is comparable
across protocols conditional on the stated (U0, alpha) convention. Rescaling
U0 -> U0/c multiplies every D by c**alpha; with a common alpha the rescaling is
uniform and preserves the cross-protocol ordering, which is why one alpha is
used for all networks.

ALPHA. Baseline alpha = 2.0 (Metcalfe) for all networks. Superlinear scaling
(alpha = 2.5) and an n log n specification (Briscoe, Odlyzko and Tilly, 2006)
are sensitivity scenarios.

BETA. beta = 1.5 in the scarcity equation S = kappa * (1 - pi)**beta, with
sensitivity over beta in {1.0, 1.5, 2.0}.

BURN. Component B scores only protocol-level permanent removal of circulating
tokens; reduced issuance (halvings, emission decay) is scored under Emission
Rigidity (E). See data/scarcity_components.csv for the per-protocol rationale.
"""

U0 = 1.0e6          # common user-normalization scale (users)
ALPHA_BASE = 2.0    # common network-effect exponent (Metcalfe)
BETA_BASE = 1.5     # inflation sensitivity in the scarcity equation

ALPHA_GRID = [1.8, 2.0, 2.2, 2.5]
BETA_GRID = [1.0, 1.5, 2.0]
TAO_USER_SCENARIOS = {"low": 1.5e4, "base": 3.3e4, "high": 9.0e4}

NETWORKS = ["BTC", "ETH", "TAO"]

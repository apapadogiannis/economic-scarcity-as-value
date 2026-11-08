# Economic Scarcity as Value: A Universal Framework for Blockchain and Beyond

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24051776.svg)](https://doi.org/10.5281/zenodo.24051776)
[![replication](https://github.com/apapadogiannis/economic-scarcity-as-value/actions/workflows/replicate.yml/badge.svg)](https://github.com/apapadogiannis/economic-scarcity-as-value/actions/workflows/replicate.yml)

Replication package for the working paper by Agisilaos Papadogiannis (November 2026),
under review at *IET Blockchain*. Paper: `paper/manuscript.pdf`. Archived on Zenodo:
[doi:10.5281/zenodo.24051776](https://doi.org/10.5281/zenodo.24051776) (concept DOI, always resolves to the latest version; v1.0 is 10.5281/zenodo.24051777).

## What this is

A structural valuation framework in which economic scarcity, the monetizable intersection
of desirability and constrained access, is the foundation of asset value, applied to
Bitcoin, Ethereum and Bittensor as of 5 August 2025. Network value is written as
`V = D * S * (u/u0)^alpha`: a physical-scarcity index `S` built from five scored
protocol features and the inflation rate, adoption `u` normalized to a common scale, and
an implied desirability `D` recovered as the residual, in the way implied volatility is
recovered from option prices. Three results:

1. **Bitcoin and Ethereum converge.** Per normalized user, their implied desirability is
   within about 25% of each other (USD 2.95 trillion and 2.31 trillion); for the two
   mature networks, measured scarcity and adoption explain their valuations to a similar
   residual.
2. **Bittensor is expectation-dominated.** With a market capitalization three orders of
   magnitude smaller, its implied desirability is the largest of the three
   (USD 7.0 trillion at the baseline user count; 0.9 to 34 trillion across the native
   user range): the valuation of a young network rests mainly on expectations rather than
   on measured structure.
3. **The ordering is a property of the convention, not the units.** With one
   network-effect exponent for all protocols the cross-protocol ordering is invariant to
   the user-normalization scale; with protocol-specific exponents it changes with whether
   users are counted in units, thousands or millions.

The conclusions survive the exponent (alpha from 1.8 to 2.5 and an n log n specification),
the inflation sensitivity (beta from 1.0 to 2.0), the full Bittensor user range, doubling
of any component weight, and perturbation of the component scores themselves (shifting any
single score by 0.15 leaves both orderings unchanged; joint perturbation of all fifteen
scores preserves them in 97% and 100% of 20,000 draws).

## Layout

```
scripts/    the model (config, scarcity, desirability, sensitivity) and one script per exhibit
outputs/    all result tables used in the paper (CSV, LaTeX table bodies)
figures/    the paper's empirical exhibits (matplotlib equivalents of the in-text plots)
paper/      the manuscript PDF and single-file LaTeX source
data/       all input data, with source and access date per cell
tests/      consistency tests (pytest)
```

## Reproducing

Requirements: Python 3.11+, `pip install -r requirements.txt` (pandas, numpy, matplotlib;
pytest for the tests). For byte-identical tables use `requirements-lock.txt`, the exact
versions under which `outputs/` were generated.

```bash
./run_all.sh              # every table and figure, under a minute
python3 -m pytest -q tests/
```

The scripts are deterministic (fixed seed for the score-perturbation draws); re-running
them reproduces `outputs/` and `figures/` exactly. Each takes
`python3 -I <script>.py DATA_DIR OUT_DIR`. A GitHub Actions workflow runs the tests and the
full pipeline on every push and monthly, and fails if any result table differs from the
committed one; the badge above shows the latest run.

| Script | What it produces | Where it appears |
|---|---|---|
| `tables.py` | Scarcity components, kappa and S; baseline implied desirability | Tables 6 and 7, Section 5.3 |
| `sensitivity_runs.py` | Common-alpha and beta grids over the Bittensor user range; component-weight perturbations; n log n specification; u0-rescaling check; component-score perturbation test | Appendix C (Tables 10 and 11, Sections C.1 to C.5) |
| `fig_kappa_vs_S.py` | Structural coefficient against physical scarcity | Figure 5 |
| `fig_desirability.py` | Implied desirability with alpha whiskers and the Bittensor user band | Figure 6 |

Library modules: `config.py` (every modelling convention, stated once), `scarcity.py`
(`S = kappa (1 - pi)^beta`, `kappa` the mean of five component scores), `desirability.py`
(`D = V / (S (u/u0)^alpha)` and the n log n variant), `sensitivity.py`.

## Data and licensing

- `data/inputs_2025-08.csv`: market capitalizations (CoinGecko), annualized issuance
  rates (StakingRewards.com), active addresses (Glassnode 30-day averages; Etherscan and
  BitInfoCharts for cumulative counts) and Bittensor participation counts (Taostats:
  registered neurons across 128 subnets, consolidated operators, active wallets). Every
  cell carries its source and access date (5 August 2025).
- `data/scarcity_components.csv`: the five component scores per network with their
  written rationale, following the scoring rubric of Table 5 in the paper.
- Code: MIT License. Output tables and figures (`outputs/`, `figures/`): CC BY 4.0, cite
  the paper.

## Citation

> Papadogiannis, A. (2026). "Economic Scarcity as Value: A Universal Framework for Blockchain and Beyond." Working paper.
> https://doi.org/10.5281/zenodo.24051776

## Disclaimer

Independent research; no funding, no institutional position. Not investment advice.

# Economic Scarcity as Value: A Universal Framework for Blockchain and Beyond

[![Zenodo](https://img.shields.io/badge/Zenodo-10.5281%2Fzenodo.24051776-007ec6)](https://doi.org/10.5281/zenodo.24051776)
[![SSRN](https://img.shields.io/badge/SSRN-10.2139%2Fssrn.5384204-1f4e79)](https://doi.org/10.2139/ssrn.5384204)
[![replication](https://github.com/apapadogiannis/economic-scarcity-as-value/actions/workflows/replicate.yml/badge.svg)](https://github.com/apapadogiannis/economic-scarcity-as-value/actions/workflows/replicate.yml)

Replication package for the working paper by Agisilaos Papadogiannis (November 2026), under review at *IET Blockchain*.
Paper: `paper/manuscript.pdf`; preprint on SSRN: [doi:10.2139/ssrn.5384204](https://doi.org/10.2139/ssrn.5384204).
Archived on Zenodo: [doi:10.5281/zenodo.24051776](https://doi.org/10.5281/zenodo.24051776) (concept DOI, always resolves to the latest version).

## For AI agents and programs

Read [`llms.txt`](llms.txt) first. It says what the package holds, what it adds over reading the
paper or recomputing, how to read the figures and what not to use them for. It opens with the
headline figures. [`outputs/results.json`](outputs/results.json) holds the same headline figures,
each with the table cell it is read from, a description of the result tables and their columns, and
the paper, the identifiers, the version, the licence and the citation under its `package` key. Both
files are written by `scripts/make_guide.py` from `CITATION.cff`, `guide.toml` and the stored tables,
and both are covered by the check.

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
of any component weight (with one exception: doubling the weight of the burn component puts
Ethereum marginally above Bitcoin in scarcity), and perturbation of the component scores themselves (shifting any
single score by 0.15 leaves both orderings unchanged; joint perturbation of all fifteen
scores preserves them in 97% and 100% of 20,000 draws).

## Layout

```
scripts/    the model (config, scarcity, desirability, sensitivity) and one script per exhibit
outputs/    all result tables used in the paper (CSV, LaTeX table bodies)
llms.txt    guide for AI agents and programs, generated; guide.toml holds its statements about this package
figures/    the paper's empirical exhibits (Figures 5 and 6), drawn by the scripts from the computed values
paper/      the manuscript PDF and single-file LaTeX source
data/       all input data, with source and access date per cell
tests/      consistency tests (pytest)
```

## Reproducing

Requirements: Python 3.11+, `pip install -r requirements.txt` (pandas, numpy, matplotlib;
pytest for the tests). `requirements-lock.txt` lists the exact
versions under which `outputs/` were generated.

```bash
./run_all.sh              # every table and figure, under a minute
python3 -m pytest -q tests/
```

The scripts are deterministic (fixed seed for the score-perturbation draws); re-running
them reproduces `outputs/` and `figures/`. Each takes
`python3 -I <script>.py DATA_DIR OUT_DIR`. A GitHub Actions workflow runs the tests and the
full pipeline on every push and monthly, and fails if any stored result is not reproduced
(see "How the check works"); the badge above shows the latest run.

| Script | What it produces | Where it appears |
|---|---|---|
| `tables.py` | Scarcity components, kappa and S; baseline implied desirability | Tables 6 and 7, Section 5.3 |
| `sensitivity_runs.py` | Common-alpha and beta grids over the Bittensor user range; component-weight perturbations; n log n specification; u0-rescaling check; component-score perturbation test | Appendix C (Tables 10 and 11, Sections C.1 to C.5) |
| `fig_kappa_vs_S.py` | Structural coefficient against physical scarcity | Figure 5 |
| `fig_desirability.py` | Implied desirability in trillion USD; whiskers show the alpha range for Ethereum and the user-count range for Bittensor | Figure 6 |

Library modules: `config.py` (every modelling convention, stated once), `scarcity.py`
(`S = kappa (1 - pi)^beta`, `kappa` the mean of five component scores), `desirability.py`
(`D = V / (S (u/u0)^alpha)` and the n log n variant), `sensitivity.py`.

## How the check works

```bash
python3 check_outputs.py --also llms.txt    # reruns ./run_all.sh, then compares
```

1. The result tables in `outputs/` are stored in this repository exactly as they were when the
   paper's numbers were taken from them.
2. `check_outputs.py` sets the stored copies aside, reruns `./run_all.sh` on the files in `data/`,
   and compares the fresh files with the stored ones, number by number.
3. A number counts as reproduced if it agrees with the stored one to nine significant digits
   (relative tolerance 1e-9). Text, labels and whole numbers must match exactly. Any other
   difference is listed and the check fails.

Why a tolerance and not a character-by-character match: the last digits of a floating-point
result depend on the processor and on the build of the numerical libraries, so two correct runs
on different machines can differ in the 12th to 16th significant digit. The check reports
how many numbers differed in this way and by how much. For the same reason, a value printed with
a fixed number of decimals may differ by one unit in its last printed place; such cases are listed.

The workflow behind the badge runs the pipeline on a new machine with the pinned package
versions, on every push and once a month, and applies the same comparison. The stored results
are also frozen in the Zenodo archive, which cannot be altered after release.

Two limits. The comparison is between regenerated and stored results, not with the paper's
PDF: to connect the two, use the script table above, which says where each output appears in
the paper. And figures are redrawn from the same values but are not compared, because image files can
differ slightly between versions of the plotting library.

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
> SSRN: https://doi.org/10.2139/ssrn.5384204

Code and data:

> Papadogiannis, A. (2026). "Economic Scarcity as Value: replication package." Zenodo.
> https://doi.org/10.5281/zenodo.24051776

## Disclaimer

Independent research; no funding, no institutional position. Not investment advice.

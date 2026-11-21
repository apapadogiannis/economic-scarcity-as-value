#!/usr/bin/env bash
# Reproduces every table body and figure in the paper. Runs in under a minute.
set -e
cd "$(dirname "$0")"
mkdir -p outputs figures
for f in tables sensitivity_runs fig_kappa_vs_S fig_desirability; do
  echo "== $f"; python3 -I "scripts/$f.py" data outputs
done
mv -f outputs/*.pdf outputs/*.png figures/
# The description of the result tables with the headline figures (outputs/results.json) and the guide
# for programs and AI agents (llms.txt).
echo "== make_guide"; python3 -I scripts/make_guide.py

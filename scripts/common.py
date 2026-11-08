"""Shared I/O for the entry-point scripts: `python3 -I <script>.py DATA_DIR OUT_DIR`."""
from __future__ import annotations

import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)


def args():
    data_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data")
    out_dir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "outputs")
    os.makedirs(out_dir, exist_ok=True)
    return data_dir, out_dir


def load(data_dir):
    inputs = pd.read_csv(os.path.join(data_dir, "inputs_2025-08.csv"))
    components = pd.read_csv(os.path.join(data_dir, "scarcity_components.csv"))
    return inputs, components


def to_tex(df: pd.DataFrame, path: str, caption: str, label: str, float_fmt="%.4g"):
    with open(path, "w") as f:
        f.write(df.to_latex(index=False, float_format=float_fmt,
                            caption=caption, label=label, escape=True))

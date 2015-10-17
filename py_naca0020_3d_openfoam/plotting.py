"""
Plotting functions.
"""

import matplotlib.pyplot as plt
from .processing import *


def plot_spanwise_pressure(ax=None):
    """Plot spanwise pressure, normalized and inverted."""
    df = load_sampled_set("spanwise", "p")
    df["p_norm"] = -df.p
    df.p_norm -= df.p_norm.min()
    df.p_norm /= df.p_norm.max()
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(df.z, df.p_norm)
    ax.set_xlabel("$z/H$")
    ax.set_ylabel(r"$-\hat{p}$")

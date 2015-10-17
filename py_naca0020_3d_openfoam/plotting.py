"""
Plotting functions.
"""

import numpy as np
import matplotlib.pyplot as plt
from . import processing as pr


def plot_spanwise_pressure(ax=None):
    """Plot spanwise pressure, normalized and inverted."""
    df = pr.load_sampled_set("spanwise", "p")
    df["p_norm"] = -df.p
    df.p_norm -= df.p_norm.min()
    df.p_norm /= df.p_norm.max()
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(df.z, df.p_norm)
    ax.set_xlabel("$z/H$")
    ax.set_ylabel(r"$-\hat{p}$")


def plot_alpha(ax=None):
    """Plot angle of attack versus vertical coordinate."""
    df = pr.load_sampled_velocity(name="inflow")
    pitch = pr.read_alpha_deg()
    df["alpha_deg"] = pitch - np.rad2deg(np.tan(df.U_1/df.U_0))
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(df.z, -df.alpha_deg)
    ax.set_xlabel("$z/H$")
    ax.set_ylabel(r"$\alpha$ (degrees)")


def plot_inflow(ax=None):
    """Plot inflow velocity magnitude versus vertical coordinate."""
    df = pr.load_sampled_velocity(name="inflow")
    df["rel_vel_mag"] = np.sqrt(df.U_0**2 + df.U_1**2)
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(df.z, df.rel_vel_mag)
    ax.set_xlabel("$z/H$")
    ax.set_ylabel(r"$|U_\mathrm{in}|$")


def plot_trailing_vorticity(ax=None):
    """Plot trailing vorticity versus vertical coordinate."""
    df = pr.load_sampled_vorticity(name="trailing")
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(df.z, df.vorticity_2)
    ax.set_xlabel("$z/H$")
    ax.set_ylabel(r"$\omega_z$")

"""
Plotting functions.
"""

import numpy as np
import matplotlib.pyplot as plt
from . import processing as pr
import os


def plot_spanwise_pressure(ax=None, simtype="BR", save=False):
    """Plot spanwise pressure, normalized and inverted."""
    df = pr.load_sampled_set("spanwise", "p", simtype=simtype)
    df["p_norm"] = -df.p
    df.p_norm -= df.p_norm.min()
    df.p_norm /= df.p_norm.max()
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(df.z, df.p_norm)
    ax.set_xlabel("$z/H$")
    ax.set_ylabel(r"$-\hat{p}$")
    try:
        fig.tight_layout()
    except UnboundLocalError:
        pass
    if save:
        savefig(fig=fig, name="spanwise-pressure-" + simtype)


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


def plot_inflow(ax=None, component=None):
    """Plot inflow velocity magnitude versus vertical coordinate."""
    df = pr.load_sampled_velocity(name="inflow")
    if component is None:
        vel = np.sqrt(df.U_0**2 + df.U_1**2)
        ylabel = r"$|U_\mathrm{in}|$"
    else:
        vel = df["U_" + str(component)]
        ylabel = r"$U_{}$".format(component)
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(df.z, vel)
    ax.set_xlabel("$z/H$")
    ax.set_ylabel(ylabel)


def plot_trailing_vorticity(ax=None, simtype="BR", save=False):
    """Plot trailing vorticity versus vertical coordinate."""
    df = pr.load_sampled_vorticity(name="trailing", simtype=simtype)
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(df.z, df.vorticity_2)
    ax.set_xlabel("$z/H$")
    ax.set_ylabel(r"$\omega_z$")
    try:
        fig.tight_layout()
    except UnboundLocalError:
        pass
    if save:
        savefig(fig=fig, name="trailing-vorticity-" + simtype)


def plot_trailing_velocity(ax=None, component=0, simtype="BR"):
    """Plot trailing velocity versus vertical coordinate."""
    df = pr.load_sampled_velocity(name="trailing", simtype=simtype)
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(df.z, df["U_" + str(component)])
    ax.set_xlabel("$z/H$")
    ax.set_ylabel(r"$U_{}$".format(component))


def savefig(fig=None, name=None):
    """Save to `figures` directory as PDF and PNG."""
    if not os.path.isdir("figures"):
        os.mkdir("figures")
    if fig is not None:
        plt = fig
    plt.savefig("figures/{}.pdf".format(name))
    plt.savefig("figures/{}.png".format(name), dpi=300)

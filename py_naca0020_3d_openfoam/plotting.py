"""
Plotting functions.
"""

import numpy as np
import matplotlib.pyplot as plt
from . import processing as pr
import os
import pandas as pd

c = 0.14
H = 1.0
U_infty = 1.0


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


def plot_trailing_vorticity(ax=None):
    """Plot trailing vorticity versus vertical coordinate."""
    df = pr.load_sampled_vorticity(name="trailing")
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(df.z, df.vorticity_2)
    ax.set_xlabel("$z/H$")
    ax.set_ylabel(r"$\omega_z$")


def plot_trailing_velocity(ax=None, component=0):
    """Plot trailing velocity versus vertical coordinate."""
    df = pr.load_sampled_velocity(name="trailing")
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(df.z, df["U_" + str(component)])
    ax.set_xlabel("$z/H$")
    ax.set_ylabel(r"$U_{}$".format(component))


def plot_spanwise_al():
    """
    Plot spanwise distribution of angle of attack and relative velocity.
    """
    elements_dir = "postProcessing/actuatorLineElements/0"
    elements = os.listdir(elements_dir)
    dfs = {}
    z_H = np.zeros(len(elements))
    urel = np.zeros(len(elements))
    alpha_deg = np.zeros(len(elements))
    for e in elements:
        i = int(e.replace("foilElement", "").replace(".csv", ""))
        df = pd.read_csv(os.path.join(elements_dir, e))
        z_H[i] = df.z.iloc[-1]/H
        urel[i] = df.rel_vel_mag.iloc[-1]/U_infty
        alpha_deg[i] = df.alpha_deg.iloc[-1]
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(7.5, 3.25))
    ax[0].plot(z_H, alpha_deg)
    ax[0].set_ylabel(r"$\alpha$ (deg)")
    ax[1].plot(z_H, urel)
    ax[1].set_ylabel(r"$ | U_{\mathrm{rel}} | / U_\infty $")
    for a in ax:
        a.set_xlabel("$z/H$")
        a.grid(True)
    fig.tight_layout()

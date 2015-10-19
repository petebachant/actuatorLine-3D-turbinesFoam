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


labels = {"alpha_deg": r"$\alpha$ (deg.)",
          "rel_vel_mag": r"$|U_\mathrm{rel}|$",
          "lift": r"$ |F_l| /(\frac{1}{2} \rho U_\infty^2) $"}


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


def load_spanwise_al_data():
    """Load spanwise data for the actuator line."""
    elements_dir = "postProcessing/actuatorLineElements/0"
    elements = os.listdir(elements_dir)
    z_H = np.zeros(len(elements))
    urel = np.zeros(len(elements))
    alpha_deg = np.zeros(len(elements))
    lift = np.zeros(len(elements))
    for e in elements:
        i = int(e.replace("foilElement", "").replace(".csv", ""))
        df = pd.read_csv(os.path.join(elements_dir, e))
        z_H[i] = df.z.iloc[-1]/H
        urel[i] = df.rel_vel_mag.iloc[-1]/U_infty
        alpha_deg[i] = df.alpha_deg.iloc[-1]
        lift[i] = df.cl.iloc[-1]*urel[i]**2/0.5
    df = pd.DataFrame()
    df["z_H"] = z_H
    df["alpha_deg"] = alpha_deg
    df["rel_vel_mag"] = urel
    df["lift"] = lift
    return df


def plot_spanwise_al(quantities=["alpha_deg", "rel_vel_mag"]):
    """Plot spanwise distributions from actuator line."""
    if not isinstance(quantities, list):
        quantities = [quantities]
    df = load_spanwise_al_data()
    if len(quantities) > 1:
        fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(7.5, 3.25))
    else:
        fig, ax = plt.subplots()
        ax = [ax]
    for a, q in zip(ax, quantities):
        a.plot(df.z_H, df[q])
        a.set_ylabel(labels[q])
        a.set_xlabel("$z/H$")
        a.grid(True)
    fig.tight_layout()

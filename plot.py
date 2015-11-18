#!/usr/bin/env python
"""
This script plots various quantities.
"""

from __future__ import division, print_function
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import pyal3dtf.processing as pr
import pyal3dtf.plotting as pl
import os

labels = {"cl": r"$C_l$", "cd": r"$C_d$", "cl/cd": r"$C_l/C_d$", "k": "$k$",
          "omega": r"$\omega$", "epsilon": r"$\epsilon$",
          "alpha_deg": r"$\alpha$ (deg)"}


def plot_time_series(quantity="cl"):
    """
    Plot specified quantity over time. Can be used to visualize convergence.
    """
    df = pr.load_force_coeffs()
    if quantity == "cl/cd":
        q = df.cl/df.cd
    else:
        q = df[quantity]
    plt.figure()
    plt.plot(df.time[5:], q[5:])
    plt.xlabel(r"$t$")
    plt.ylabel(labels[quantity])
    plt.grid(True)
    plt.tight_layout()


if __name__ == "__main__":
    try:
        import pxl
        pxl.styleplot.set_sns()
        plt.rcParams["axes.grid"] = True
    except ImportError:
        print("Could not import PXL for plot styling. Try")
        print("\n    conda install seaborn\n\nand")
        print("\n    pip install pxl\n")

    parser = argparse.ArgumentParser(description="Plotting results")
    parser.add_argument("quantity", nargs="*", default="spanwise-pressure",
                        help="Which quantity to plot",
                        choices=["cl", "cd", "cl/cd", "spanwise-pressure",
                                 "trailing-vorticity"])
    parser.add_argument("--blade-type", "-b", default="BR", choices=["BR",
                        "AL"], help="Blade-resolved or actuator line")
    parser.add_argument("--save", "-s", action="store_true", help="Save plots")
    parser.add_argument("--noshow", action="store_true", default=False,
                        help="Do not show")
    parser.add_argument("--timeseries", "-t", action="store_true",
                        default=False, help="Plot time series data")
    args = parser.parse_args()

    if args.timeseries:
        plot_time_series(args.quantity)
    elif "spanwise-pressure" in args.quantity:
        pl.plot_spanwise_pressure(simtype=args.blade_type)
    elif "trailing-vorticity" in args.quantity:
        pl.plot_trailing_vorticity(simtype=args.blade_type)

    if args.save:
        if not os.path.isdir("figures"):
            os.mkdir("figures")
        plt.savefig("figures/{}-{}.pdf".format(args.blade_type, args.quantity))
        plt.savefig("figures/{}-{}.png".format(args.blade_type, args.quantity),
                    dpi=300)

    if not args.noshow:
        plt.show()

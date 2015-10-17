"""
This module contains processing functions.
"""

import numpy as np
import pandas as pd
import os

def load_force_coeffs(steady=False):
    """
    Load force coefficients from file. If steady, the file from the `0`
    directory is used, and the last values are returned. Otherwise, arrays are
    loaded from the latest file.
    """
    if steady:
        timedir = "0"
    else:
        timedir = max(os.listdir("postProcessing/forceCoeffs"))
    fpath = "postProcessing/forceCoeffs/{}/forceCoeffs.dat".format(timedir)
    data = np.loadtxt(fpath, skiprows=9)
    df = pd.DataFrame()
    df["time"] = data[:, 0]
    df["cl"] = data[:, 3]
    df["cd"] = data[:, 2]
    df["cm"] = data[:, 1]
    return df


def load_sampled_set(name="spanwise", quantity="p"):
    """Load sampled set sampled from latest time."""
    timedir = max(os.listdir("postProcessing/sets"))
    fpath = "postProcessing/sets/{}/{}_{}.csv".format(timedir, name, quantity)
    df = pd.read_csv(fpath)
    return df


def read_alpha_deg():
    """Read angle of attack from `log.surfaceTransformPoints`."""
    with open("log.surfaceTransformPoints") as f:
        for line in f:
            line = line.strip()
            line = line.split()
            if "yaw" in line:
                return float(line[-1])

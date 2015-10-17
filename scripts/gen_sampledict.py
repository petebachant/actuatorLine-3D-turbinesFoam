#!/usr/bin/env python
"""
Create sampleDict from template.

Inflow detection in turbinesFoam:

```
    inflowVelocityPoint -= freeStreamDirection_*0.15*chordLength_;
    inflowVelocityPoint += chordDirection_*0.1*chordLength_;
    inflowVelocityPoint -= planformNormal*0.75*chordLength_;
```
"""
import numpy as np
c = 0.14


def read_alpha_deg():
    """Read angle of attack from `log.surfaceTransformPoints`."""
    with open("log.surfaceTransformPoints") as f:
        for line in f:
            line = line.strip()
            line = line.split()
            if "yaw" in line:
                return float(line[-1])


def rotate(v, rad):
    """Rotate a 2-D vector by rad radians."""
    dc, ds = np.cos(rad), np.sin(rad)
    x, y = v[0], v[1]
    x, y = dc*x - ds*y, ds*x + dc*y
    return np.array((x, y))


def calc_xy():
    """
    Calculate the x and y coordinates to sample spanwise and inflow velocity.
    """
    alpha_deg = read_alpha_deg()
    alpha_rad = np.deg2rad(alpha_deg)
    freestream_dir = np.array((1, 0))
    chord_dir = rotate(np.array((-1, 0)), alpha_rad)
    planform_dir = rotate(np.array((0, 1)), alpha_rad)
    inflow_x, inflow_y = np.array((0, 0)) - 0.15*c*freestream_dir \
                       + 0.1*c*chord_dir - 0.75*c*planform_dir
    spanwise_x, spanwise_y = planform_dir*0.2/2*c*1.001
    return {"inflow_x": inflow_x, "inflow_y": inflow_y,
            "spanwise_x": spanwise_x, "spanwise_y": spanwise_y}


if __name__ == "__main__":
    xy = calc_xy()
    with open("system/sampleDict.template") as f:
        txt = f.read()
    with open("system/sampleDict", "w") as f:
        f.write(txt.format(**xy))

from spicer import spicer
import numpy as np
from math import pi
import spiceypy as spice


def test_illum_angles():
    illangles = spicer.IllumAngles(phase=pi, emission=2*pi)

    assert np.allclose([illangles.dphase, illangles.demission], [180.0, 360.0])


def test_illum_angles_from_tuples():
    illangles = spicer.IllumAngles.fromtuple([pi, 2*pi, 3*pi])
    assert np.allclose([illangles.dphase, illangles.dsolar, illangles.demission],
                       [180.0, 360.0, 540.0])


def test_coords():
    coords = spicer.Coords(lat=0, lon=pi)
    assert np.allclose([coords.dlat, coords.dlon, coords.radius],
                       [0.0, 180, 0.0])

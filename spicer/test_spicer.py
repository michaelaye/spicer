from spicer import spicer, exceptions
import numpy as np
from math import pi
import spiceypy as spice
import datetime as dt
import pytest


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


def test_spicer_time_init():
    s = spicer.Spicer('2010-01-02')
    assert s.utc == '2010-01-02T00:00:00'
    assert s.time == dt.datetime(2010, 1, 2)
    assert np.allclose([315662466.18395346], [s.et])


def test_spicer_target_id():
    s = spicer.Spicer()
    s.target = 'Mars'
    assert s.target_id == 499


# @pytest.mark.xfail(raises=exceptions.SpiceError)
def test_spicer_target_id_failure():
    s = spicer.Spicer()
    s.target = 'hello'
    with pytest.raises(exceptions.SpiceError):
        print(s.target_id)


def test_spicer_radii():
    s = spicer.Spicer()
    s.target = 'Mars'
    assert np.allclose([3396.1900000000001, 3396.1900000000001, 3376.1999999999998],
                       [s.radii.a, s.radii.b, s.radii.c])

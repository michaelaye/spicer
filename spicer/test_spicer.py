import datetime as dt
from math import pi

import numpy as np
import pytest
from spicer import exceptions, spicer


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


def test_spicer_solar_constant():
    s = spicer.Spicer('2015-10-18T23:50:24.747598')
    s.target = 'Earth'
    s.ref_frame = 'IAU_EARTH'
    assert np.allclose([-1.46834268e+08,   3.20689425e+06,  -2.53194083e+07],
                       s.center_to_sun)
    assert np.allclose([1375.39440028], s.solar_constant)


def test_spicer_set_spoint_by_latlon():
    s = spicer.Spicer()
    s.target = 'mars'
    s.set_spoint_by(lat=0, lon=0)
    assert np.allclose([3396.19, 0.0, 0.0], s.spoint)

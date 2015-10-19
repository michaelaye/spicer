import datetime as dt
from collections import namedtuple

import dateutil.parser as tparser
import numpy as np
import spiceypy as spice
from traitlets import Float, HasTraits, Unicode

from .kernels import load_generic_kernels
from .exceptions import SpiceError

load_generic_kernels()

# constants
L_sol = 3.839e26  # [Watt]

# simple named Radii structure, offering Radii.a Radii.b and Radii.c
Radii = namedtuple('Radii', 'a b c')


class IllumAngles(HasTraits):
    phase = Float(0)
    solar = Float(0)
    emission = Float(0)
    dphase = Float
    demission = Float
    dsolar = Float

    @classmethod
    def fromtuple(cls, args, **traits):
        return cls(phase=args[0], solar=args[1], emission=args[2], **traits)

    @property
    def dphase(self):
        return np.rad2deg(self.phase)

    @property
    def dsolar(self):
        return np.rad2deg(self.solar)

    @property
    def demission(self):
        return np.rad2deg(self.emission)

    def __call__(self):
        print("Phase: {0} deg\nSolar Incidence: {1} deg\nEmission: {2} deg"
              .format(self.dphase, self.dsolar, self.demission))


class Coords(HasTraits):
    lon = Float
    lat = Float
    radius = Float

    @classmethod
    def fromtuple(cls, args, **traits):
        return cls(radius=args[0], lon=args[1], lat=args[2], **traits)

    @property
    def dlon(self):
        dlon = np.rad2deg(self.lon)
        # force 360 eastern longitude:
        if dlon < 0:
            dlon += 360.0
        return dlon

    @property
    def dlat(self):
        return np.rad2deg(self.lat)

    def __call__(self):
        print("Longitude: {0} deg\nLatitude: {1} deg\nRadius: {2} km"
              .format(self.dlon, self.dlat, self.radius))


class Spicer(HasTraits):
    method = Unicode('Near point:ellipsoid')
    corr = Unicode('LT+S')

    target = Unicode

    def __init__(self, time=None):
        if time is None:
            self.time = dt.datetime.now()
        else:
            self.time = tparser.parse(time)

    @property
    def utc(self):
        return self.time.isoformat()

    @property
    def et(self):
        return spice.utc2et(self.utc)

    @property
    def target_id(self):
        res, check = spice.bodn2c(self.target)
        if check is not True:
            raise SpiceError('target_id, using bodn2c')
        else:
            return res

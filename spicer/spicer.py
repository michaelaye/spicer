import datetime as dt
import math
from collections import namedtuple

import dateutil.parser as tparser
import numpy as np
import spiceypy as spice
from traitlets import Float, HasTraits, Unicode, Enum

from .exceptions import SpiceError, MissingParameterError
from .kernels import load_generic_kernels

load_generic_kernels()

# constansts
L_sol = 3.839e26
"""Solar luminosity [Watt].

Global constant.
Will be used to calculate solar constants at the body.
"""

# types
Radii = namedtuple('Radii', 'a b c')
"""Simple named Radii structure.

Stores the 3 element radii tuple of SPICE in a named structure.
"""


class IllumAngles(HasTraits):

    """Managing illumination angles.


    Attributes
    ----------
    phase : traitlets.Float
        Phase angle
    solar : traitlets.Float
        Solar incidence angle
    emission : traitlets.Float
        Surface emission angle
    dphase
    dsolar
    demission
    """
    phase = Float(0)
    solar = Float(0)
    emission = Float(0)
    dphase = Float
    dsolar = Float
    demission = Float

    @classmethod
    def fromtuple(cls, args, **traits):
        return cls(phase=args[0], solar=args[1], emission=args[2], **traits)

    @property
    def dphase(self):
        "float : degree version of self.phase"
        return np.rad2deg(self.phase)

    @property
    def dsolar(self):
        "float : degree version of solar incidence angle."
        return np.rad2deg(self.solar)

    @property
    def demission(self):
        "float : degree version of emission angle."
        return np.rad2deg(self.emission)

    def __call__(self):
        print("Phase: {0} deg\nSolar Incidence: {1} deg\nEmission: {2} deg"
              .format(self.dphase, self.dsolar, self.demission))


class SurfaceCoords(HasTraits):

    """Managing SPICE surface coordinates.

    Attributes
    ----------
    lon : traitlets.Float
        Longitude
    lat : traitlets.Float
        Latitude
    radius : traitlets.Float
        Radius of lat/lon location. Could be below or above actual surface.
    dlon
    dlat
    """
    lon = Float
    lat = Float
    radius = Float

    @classmethod
    def fromtuple(cls, args):
        """Initialize object via args tuple.

        This is handy as a tuple is often the output of SPICE functions.

        Parameters
        ----------
        radius: float
            Radius of lat/lon location. Could be below or above actual surface.
        lon: float
            Longitude
        lat: float
            Latitude
        """
        return cls(radius=args[0], lon=args[1], lat=args[2])

    @property
    def dlon(self):
        "float : Degree version of radians longitude."
        dlon = np.rad2deg(self.lon)
        # force 360 eastern longitude:
        while dlon < 0:
            dlon += 360.0
        return dlon

    @property
    def dlat(self):
        "float : Degree version of radians latitude."
        return np.rad2deg(self.lat)

    def __str__(self):
        "Return string with useful summary."
        return ("Longitude: {0} deg\nLatitude: {1} deg\nRadius: {2} km"
                .format(self.dlon, self.dlat, self.radius))

    def __call__(self):
        "Print pretty info on call."
        print(self.__str__())


class Spicer(HasTraits):

    """Main Spicer utility class. SPICE body objects should inherit from this.

    Parameters
    ----------
    time : str or dt.datetime
        str should be parseable by dateutil.timeparser

    Attributes
    ----------
    time : datetime.datetime
        Time of Spicer object. Can be changed, which updates all dependent values.
    method : str
        SPICE method flag for surface point interception calculation.
    corr : str
        SPICE method flag for aberration correction
    body : str
        Planetary body string for the SPICE system. To be set either by instance user
        or by subclass.
    ref_frame
    utc
    et
    target_id
    radii
    center_to_sun
    solar_constant
    north_pole
    south_pole
    l_s
    sun_direction
    """
    method = Unicode('Near point:ellipsoid')
    corr = Unicode('none')
    target = None
    _body = Unicode
    _ref_frame = Unicode

    def __init__(self, body, time=None):
        self._body = body
        if time is None:
            self.time = dt.datetime.now()
        else:
            self.time = tparser.parse(time)
        self._ref_frame = "IAU_" + str(self.body).upper()

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        self._body = value
        self.ref_frame = "IAU_" + str(value).upper()

    @property
    def ref_frame(self):
        "str: Reference frame for SPICE calculations."
        return self._ref_frame

    @ref_frame.setter
    def ref_frame(self, value):
        self._ref_frame = value

    @property
    def utc(self):
        "str : Isoformat of UTC time."
        return self.time.isoformat()

    @property
    def et(self):
        "float : Returns Ephemeral time value from SPICE for current <time> value."
        return spice.utc2et(self.utc)

    @property
    def target_id(self):
        "int : SPICE Body ID for self.target."
        res = spice.bodn2c(self.target)
        return res

    @property
    def radii(self):
        "namedtuple Radii : Radii values container."
        _, radii = spice.bodvrd(self.target, "RADII", 3)
        return Radii(*radii)

    def body_to_object(self, target):
        """Calculate distance to target.

        Parameters
        ----------
        target : str
            SPICE body string to calculate distance to from self.body.

        Returns
        -------
        tuple : ([float, float, float], float)
            distance vector[3], light-time between body and target

        # TODO: spkezp would be faster, but it uses body codes instead of names
        """
        output = spice.spkpos(
            target, self.et, self.ref_frame, self.corr, self.body)
        return output

    @property
    def center_to_sun(self):
        "float : Distance of body center to sun [km]."
        cts, lighttime = self.body_to_object("SUN")
        return cts

    @property
    def solar_constant(self):
        "float : With global value L_s, solar constant at coordinates of body center."
        dist = spice.vnorm(self.center_to_sun)
        return L_sol / (4 * math.pi * (dist * 1e3)**2)

    @property
    def north_pole(self):
        "float[3] : In self.ref_frame coords, the north pole [km]."
        return (0.0, 0.0, self.radii.c)

    @property
    def south_pole(self):
        "float[3] : In self.ref_frame coords, the south pole [km]."
        return (0.0, 0.0, -self.radii.c)

    def srfrec(self, surfcoord, body=None):
        """Convert lon/lat to rectangular coordinates.

        Convert planetocentric longitude and latitude of a surface point on a
        specified body to rectangular coordinates.

        self.target needs to be set for this!

        Parameters
        ----------
        surfcoord : SurfaceCoords
            Instance of SurfaceCoords.
        body : str or int, optional
            SPICE body str (will be converted) or SPICE body id. Default: self.body

        Examples
        --------

        >>> mspice = MarsSpicer()
        >>> print('{0:g} {1:g} {2:g}'.format(*mspice.srfrec(0,85)))
        294.268 0 3363.5
        """
        if body is None:
            body = self.target_id
        if not str(body).isdigit():
            body, _ = spice.bodn2c(body)
        return spice.srfrec(body, surfcoord.lon, surfcoord.lat)

    def set_spoint_by(self, func_str=None, lon=None, lat=None):
        """Set the current surface point for illumination calculations.

        Parameters
        ----------
        func_str : {'subpnt', 'sincpt'}

        """
        if func_str is not None and func_str not in ['subpnt', 'sincpt']:
            raise NotImplementedError(
                'Only "sincpt" and "subpnt" are supported at this time.')
        elif func_str is not None:
            raise NotImplementedError('not yet implemented.')
            # if not self.instrument or not self.obs:
            #     print("Observer and/or instrument have to be set first.")
            #     return
            # if func_str in 'subpnt':
            #     spoint = self.subpnt()[0]
            # elif func_str in 'sincpt':
            #     spoint = self.sincpt()[0]
            # else:
            #     raise Exception("No valid method recognized.")
        elif None in [lat, lon]:
            raise MissingParameterError('both lat and lon need to be given.')
        else:
            coords = SurfaceCoords(lat=lat, lon=lon)
            spoint = self.srfrec(coords).tolist()
        self.spoint_set = True
        self.spoint = spoint

    @property
    def l_s(self):
        return np.rad2deg(spice.lspcn(self.target, self.et, self.corr))

    @property
    def sun_direction(self):
        if not self.spoint_set:
            raise SPointNotSetError
        return spice.vsub(self.center_to_sun, self.spoint)

    @property
    def illum_angles(self):
        "Ilumin returns (trgepoch, srfvec, phase, solar, emission)"
        if self.obs is not None:
            output = spice.ilumin("Ellipsoid", self.target, self.et,
                                  self.ref_frame, self.corr, self.obs,
                                  self.spoint)
            return IllumAngles.fromtuple(output[2:])
        else:
            solar = spice.vsep(self.sun_direction, self.snormal)
            # leaving at 0 what I don't have
            return IllumAngles.fromtuple((0, solar, 0))

    @property
    def snormal(self):
        if not self.spoint_set:
            raise SPointNotSetError
        a, b, c = self.radii
        return spice.surfnm(a, b, c, self.spoint)

    @property
    def coords(self):
        if not self.spoint_set:
            raise SPointNotSetError
        return SurfaceCoords.fromtuple(spice.reclat(self.spoint))

    @property
    def local_soltime(self):
        return spice.et2lst(self.et, self.target_id, self.coords.lon,
                            "PLANETOGRAPHIC")[1]  # returning 24h string here.


class MarsSpicer(Spicer):
    target = 'MARS'
    obs = Enum([None, 'MRO', 'MGS', 'MEX'])
    instrument = Enum([None, 'MRO_HIRISE', 'MRO_CRISM', 'MRO_CTX'])
    # Coords dictionary to store often used coords
    location_coords = dict(inca=(220.09830399469547,
                                 -440.60853011059214,
                                 -3340.5081261541495))

    def __init__(self, time=None, obs=None, inst=None):
        """ Initialising MarsSpicer class.

        Demo:
        >>> mspicer = MarsSpicer(time='2007-02-16T17:45:48.642')
        >>> mspicer.goto('inca')
        >>> print('Incidence angle: {0:g}'.format(mspicer.illum_angles.dsolar))
        Incidence angle: 95.5388

        >>> mspicer = MarsSpicer(time='2007-01-27T12:00:00')
        >>> mspicer.set_spoint_by(lon=300, lat = -80)
        >>> print('Incidence angle: {0:g}'.format(mspicer.illum_angles.dsolar))
        Incidence angle: 85.8875
        """
        super().__init__('MARS', time=time)
        self.obs = obs
        self.instrument = inst

    def goto(self, loc_string):
        """Set self.spoint to coordinates as saved in location_coords.

        Currently available locations:
            'inca'  (call like so: mspicer.goto('inca'))
        """
        self.spoint_set = True
        self.spoint = self.location_coords[loc_string.lower()]


def get_current_l_s():
    ms = MarsSpicer()
    return round(ms.l_s, 1)

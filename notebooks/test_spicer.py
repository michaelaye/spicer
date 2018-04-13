
# coding: utf-8

# In[6]:

# setup
from spicer import Spicer, exceptions, IllumAngles, SurfaceCoords
import datetime as dt
from numpy.testing import assert_allclose
from math import pi
import pytest

s = Spicer('earth','2010-01-02')
s2 = Spicer('earth', '2015-10-18T23:50:24.747598')


# In[2]:

"""test_spicer_time_init"""
assert s.utc == '2010-01-02T00:00:00'
assert s.time == dt.datetime(2010, 1 ,2)
assert_allclose(s.et, 315662466.18395346)


# In[3]:

# test_illum_angles
illangles = IllumAngles(phase=pi, emission=2*pi)
assert_allclose([illangles.dphase, illangles.demission], [180.0, 360.0])


# In[4]:

# test_illum_angles_from_tuples
illangles = IllumAngles.fromtuple([pi, 2*pi, 3*pi])
assert_allclose([illangles.dphase, illangles.dsolar, illangles.demission],
                   [180.0, 360.0, 540.0])


# In[7]:

# test_coords
coords = SurfaceCoords(lat=0, lon=pi)
assert_allclose([coords.dlat, coords.dlon, coords.radius],
                [0.0, 180, 0.0])


# In[8]:

# test_spicer_time_init
assert s.utc == '2010-01-02T00:00:00'
assert s.time == dt.datetime(2010, 1, 2)
assert_allclose(s.et, 315662466.18395346)


# In[9]:

# test_spicer_target_id
s.target = 'Mars'
assert s.target_id == 499


# In[10]:

# test_spicer_target_id_failure
s.target = 'hello'
with pytest.raises(exceptions.SpiceError):
    print(s.target_id)


# In[11]:

# test_spicer_radii
s.target = 'Mars'
assert_allclose([s.radii.a, s.radii.b, s.radii.c],
                [3396.1900000000001, 3396.1900000000001, 3376.1999999999998])                   


# In[12]:

# test_spicer_center_to_sun
s2.body = 'Earth'
assert_allclose(s2.center_to_sun,
                [-1.46834268e+08, 3.20689425e+06, -2.53194083e+07])


# In[13]:

# test_ref_frame_property
s2.body = 'earth'
assert s2.ref_frame.upper() == "IAU_EARTH"
s2.ref_frame = 'test'
assert s2.ref_frame == 'test'


# In[14]:

# test_body_property
s2.body = 'mars'
assert s2.body == 'mars'
assert s2.ref_frame.upper() == 'IAU_MARS'


# In[15]:

# test_spicer_solar_constant
s2.body = 'Earth'
assert_allclose(s2.solar_constant, 1375.39440028)


# In[18]:

# test_spicer_srfrec_body_none
s.target = 'mars'
coords = SurfaceCoords(lat=0, lon=0)
actual = s.srfrec(coords)
assert_allclose(actual, [3396.19, 0., 0.])


# In[20]:

# test_spicer_srfrec_body_sun
s.target = 'mars'
coords = SurfaceCoords(lat=0, lon=0)
actual = s.srfrec(coords, 'sun')
assert_allclose(actual, [696000.0, 0., 0.])


# In[21]:

# test_spicer_set_spoint_by_latlon
s.target = 'mars'
s.set_spoint_by(lon=0, lat=0)
assert_allclose(s.spoint, [3396.19, 0.0, 0.0])
assert s.spoint_set == True


# In[22]:

# test_spoint_func_not_supported
with pytest.raises(NotImplementedError):
    s.set_spoint_by(func_str='sonic')


# In[23]:

# test_spoint_func_not_yet_implemented
with pytest.raises(NotImplementedError):
    s.set_spoint_by(func_str='subpnt')


# In[24]:

# test_spoint_lat_not_given
with pytest.raises(exceptions.MissingParameterError):
    s.set_spoint_by(lat=0)


# In[25]:

# test_spoint_lon_not_given
with pytest.raises(exceptions.MissingParameterError):
    s.set_spoint_by(lon=0)

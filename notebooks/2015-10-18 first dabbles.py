
# coding: utf-8

# In[ ]:

from astropy.io import fits


# In[ ]:

import astropy


# In[ ]:

astropy.__version__


# In[ ]:

from spicer import spicer, kernels


# In[ ]:

import math


# In[ ]:

import spiceypy as spice


# In[ ]:

v = (1,0,0)


# In[ ]:

spice.vrotv(v, (0,0,1), np.radians(90))


# In[ ]:

s = spicer.Spicer('2015-10-18T23:50:24.747598')


# In[ ]:

s.utc


# In[ ]:

planets = 'earth moon venus mercury mars saturn jupiter neptune uranus pluto'.split()


# In[ ]:

for planet in planets:
    s.target=planet+' barycenter'
    s.ref_frame ='IAU_'+planet.upper()
#     s.ref_frame = "j2000"
    s.corr = 'lt+s'
    print(planet)
    try:
        print(spice.vnorm(s.center_to_sun)/1e6)
    except:
        print('failed')


# In[ ]:

s.target='mars'
s.ref_frame = 'iau_mars'
s.corr = 'none'
s.center_to_sun


# In[ ]:

s.solar_constant


# In[ ]:

s.target = 'mars'


# In[ ]:

s.set_spoint_by(lat=0, lon=0)


# In[ ]:

s.spoint


# In[ ]:

s.south_pole


# In[ ]:




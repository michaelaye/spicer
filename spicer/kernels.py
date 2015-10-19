import os
from urllib.request import urlretrieve

import spiceypy as spice


modpath = os.path.abspath(__file__)
dir_path = os.path.dirname(modpath)

print(dir_path)
KERNEL_DIR = os.path.join(dir_path, 'kernels')

if not os.path.exists(KERNELDIR):
    os.mkdir(KERNEL_DIR)

download_root = 'http://naif.jpl.nasa.gov/pub/naif/generic_kernels/'

generic_kernel_list = ['lsk/naif0011.tls',
                       'pck/pck00010.tpc',
                       'spk/de430.bsp',
                       ]


def load_kernels():

    # pure planetary bodies meta-kernel without spacecraft data
    for kernel in minimum_kernel_list:
        spice.furnsh(os.path.join(KERNEL_DIR, kernel))


def load_planet_masses_kernel():
    spice.furnsh(os.path.join(KERNEL_DIR,
                              'pck/de403-masses.tpc'))

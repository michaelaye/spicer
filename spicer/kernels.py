import os
from urllib.request import urlretrieve
from pathlib import Path
import spiceypy as spice


modpath = Path(os.path.abspath(__file__))
dir_path = modpath.parent

KERNELROOT = dir_path / 'kernels'

download_root = 'http://naif.jpl.nasa.gov/pub/naif/generic_kernels/'

generic_kernel_list = ['lsk/naif0011.tls',
                       'pck/pck00010.tpc',
                       'spk/planets/de432s.bsp',
                       ]
generic_kernels = [KERNELROOT.joinpath(i) for i in generic_kernel_list]


def download_generic_kernels():
    dl_urls = [download_root + i for i in generic_kernel_list]
    for dl_url, savepath in zip(dl_urls, generic_kernels):
        try:
            savepath.parent.mkdir(parents=True)
        except FileExistsError:
            pass
        print('downloading', dl_url, 'to', savepath)
        urlretrieve(dl_url, str(savepath))


def check_generic_kernels():
    if not generic_kernels[0].exists():
        print("Generic kernels do not seem to exist. Downloading ...")
        download_generic_kernels()


def load_generic_kernels():
    check_generic_kernels()
    # pure planetary bodies meta-kernel without spacecraft data
    for kernel in generic_kernels:
        spice.furnsh(str(kernel))


def load_planet_masses_kernel():
    spice.furnsh(os.path.join(KERNELROOT,
                              'pck/de403-masses.tpc'))

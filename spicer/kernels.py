"""This module helps to manage SPICE kernels, incl. downloading and listing
loaded kernels (which unbelievably is not available from SPICE directly).
"""
import os
from urllib.request import urlretrieve

import spiceypy as spice
from pathlib import Path

# TODO: Use resources to get local file paths.
modpath = Path(os.path.abspath(__file__))
dir_path = modpath.parent

KERNELROOT = dir_path / 'kernels'

download_root = 'http://naif.jpl.nasa.gov/pub/naif/generic_kernels/'

generic_kernel_list = ['lsk/naif0011.tls',
                       'pck/pck00010.tpc',
                       'spk/planets/de421.bsp',
                       'spk/planets/de403-masses.tpc',
                       # 'spk/planets/de430.bsp',
                       ]
generic_kernels = [KERNELROOT.joinpath(i) for i in generic_kernel_list]


def do_download(source, target):
    """Download source url to target path.

    Parameters
    ----------
    source: url <str>
    target: pathlib.Path
    """

    source.parent.mkdir(parents=True, exist_ok=True)
    print('downloading', source, 'to', target)
    urlretrieve(source, str(target))


def download_generic_kernels():
    "Download all kernels as required by generic_kernel_list."

    dl_urls = [download_root + i for i in generic_kernel_list]
    for dl_url, savepath in zip(dl_urls, generic_kernels):
        do_download(dl_url, savepath)


def check_generic_kernels():
    "Check for existence of generic_kernels and download if not there."
    if not generic_kernels[0].exists():
        print("Generic kernels do not seem to exist. Downloading ...")
        download_generic_kernels()


def load_generic_kernels():
    """Load all kernels in generic_kernels list.

    Calls `check_generic_kernels()` which downloads the kernels if they are
    not there.
    """
    check_generic_kernels()
    # pure planetary bodies meta-kernel without spacecraft data
    for kernel in generic_kernels:
        spice.furnsh(str(kernel))


def load_planet_masses_kernel():
    spice.furnsh(KERNELROOT / 'pck/de403-masses.tpc')


def show_loaded_kernels():
    "Print overview of loaded kernels."
    count = spice.ktotal('all')
    if count == 0:
        print("No kernels loaded at this time.")
    else:
        print("The loaded files are:\n(paths relative to kernels.KERNELROOT)\n")
    for which in range(count):
        print(which)
        out = spice.kdata(which, 'all', 100, 100, 100)
        print("Position:", which)
        p = Path(out[0])
        print("Path", p.relative_to(KERNELROOT))
        print("Type:", out[1])
        print("Source:", out[2])
        print("Handle:", out[3])
        print("Found:", out[4])

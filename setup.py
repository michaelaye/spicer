#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="spicer",
    version="0.5.1",
    description="Library to make SPICE a bit easier",
    long_description=readme + "\n\n",
    # metadata
    author="K.-Michael Aye",
    author_email="kmichael.aye@gmail.com",
    license="MIT license",
    zip_safe=True,
    url="https://github.com/michaelaye/spicer",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "spiceypy",
        "tqdm",
        "planetarypy>=0.7",
        "astropy",
        "urlpath",
        "importlib_resources; python_version<'3.9'",
    ],
    python_requires=">=3.6, <4",
    keywords="Solarsystem, planetaryscience, planets",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
    ],
)

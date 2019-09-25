#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

test_requirements = ['pytest']
setup_requires = ['spiceypy']
setup(
    name="spicer",
    version='0.4.0',
    packages=find_packages(),
    description="Library to make SPICE a bit easier",
    long_description=readme + '\n\n',
    # metadata
    author="K.-Michael Aye",
    author_email="kmichael.aye@gmail.com",
    license="MIT license",
    keywords="Solarsystem, planetaryscience",
    zip_safe=True,
    url="https://github.com/michaelaye/spicer",
    keywords='planets',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)

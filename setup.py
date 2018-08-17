#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='nc_dnsapi',
    version='0.1.5',
    description='API wrapper for the netcup DNS api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Nicolai Buchwitz',
    author_email='nb@tipi-net.de',
    url='https://github.com/nbuchwitz/nc_dnsapi',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'requests',
    ],
    packages=setuptools.find_packages(),
)

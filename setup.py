#!/usr/bin/env python

from setuptools import setup

setup(
        name='nc_dnsapi',
        version='0.1.0',
        description='API wrapper for the netcup DNS api',
        author='Nicolai Buchwitz',
        author_email='nb@tipi-net.de',
        zip_safe=False,
        include_package_data=True,
        classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python',
            ],
        install_requires=[
            'requests',
            ],
        packages=[
            'nc_dnsapi',
            ],
        )
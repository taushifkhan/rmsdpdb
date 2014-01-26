#!/usr/bin/env python
from setuptools import setup

version = '0.9'

setup(
    name='rmsdpdb',
    version=version,
    author='Bosco Ho',
    author_email='boscoh@gmail.com',
    url='http://github.com/boscoh/rmsdpdb',
    description='calculates the CA atom RMSD of protein PDB files',
    long_description='Docs at http://github.com/boscoh/rmsdpdb',
    license='BSD',
    install_requires=['numpy'],
    packages=['rmsdpdb'],
    scripts=['bin/rmsdpdb'],
)
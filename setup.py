#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

with open('README.md') as file:
    long_description = file.read()

setup(name='Planet GeoPandas',
      version='1.0',
      description='Integrating api.planet.com with geopandas. Allowing you to query the api for satellite imagery',
      long_description=long_description,
      author='Mikael Bååth',
      author_email='mikael.baath@gmail.com',
      url='https://github.com/frlnx/planet-geopandas',
      packages=['planet_geopandas'])

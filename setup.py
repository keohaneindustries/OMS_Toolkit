#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

from setuptools import setup, find_packages


def get_version():
    """Parse __init__.py for version number instead of importing the file."""
    VERSIONFILE = 'lib/__init__.py'
    VSRE = r'^__version__ = [\'"]([^\'"]*)[\'"]'
    with open(VERSIONFILE) as f:
        verstrline = f.read()
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        return mo.group(1)
    raise RuntimeError('Unable to find version in {fn}'.format(fn=VERSIONFILE))

classifiers = [
        'Do not upload :: True',  # prevents uploads to global pypi
]

setup(name="",
      version=get_version(),
      url='https://github',
      description="",
      classifiers=classifiers,
      entry_points={
          'console_scripts': [
              'surface-executor = toolshed.groups.liquid.medium_touch.surface_executor.prd_aex_rr_surface_executor:main'
          ]
      },
      package_data={
          'assets': [
              '/*.html',
              'assets/*.js',
              'assets/*.css',
              'assets/*.png'
          ]
      },
      include_package_data=True,
      install_requires=[
          "mailer==0.8.1",
          "pyttsx3==2.7",
          "scipy==1.2.1",
          "scikit-learn==0.20.3",
          "numpy==1.22.0",
          "pandas==0.24.1",
          "Flask==1.0.2",
          "flask-socketio==3.3.2",
          "openpyxl==2.6.1",
          "squarify==0.4.2",
          "elasticsearch>=5.0.0,<6.0.0",
          "jinja2",
          "cvxopt==1.2.2",
          "statsmodels==0.10.1",
      ],
      extras_require={
          'docs': [
              'sphinx>=1.8.1',
              'sphinx_rtd_theme',
          ]
      },
      packages=find_packages()
      )


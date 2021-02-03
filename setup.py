""" Setup config to install mooda """

import os
from distutils.core import setup
from setuptools import find_packages


NAME = 'mooda'
VERSION = '1.9.2'
DESCRIPTION = 'Module for Ocean Observatory Data Analysis'
LONG_DESCRIPTION = ("""
MOODA - Module for Ocean Observatory Data Analysis

Mooda is a python package designed mainly for oceanographers and marine science students. It is"""
                    """based on a power scripting system for:

* open and analyze data files from scientific instrumentation and platforms
* generate data quality control
* make plots that are commonly used in the oceanographic community
* make data files in netCDF and CSV format

Check the documentation on https://github.com/rbardaji/mooda.
""")
CLASSIFIERS = ['Development Status :: 3 - Alpha',
               'Environment :: Console',
               'Natural Language :: English',
               'License :: OSI Approved :: MIT License',
               'Programming Language :: Python :: 3.7',
               'Topic :: Software Development :: Libraries :: Python Modules',
               'Topic :: Scientific/Engineering :: Physics',
               'Intended Audience :: Education',
               'Intended Audience :: Science/Research',
               'Intended Audience :: Developers']
KEYWORDS = ['ocean',
            'sea',
            'EMODnet',
            'EMSO']
URL = 'https://github.com/rbardaji/mooda'
AUTHOR = 'Raul Bardaji Benach'
AUTHOR_EMAIL = 'rbardaji@gmail.com'
LICENSE = 'MIT'
PACKAGES = find_packages()
REQUIREMENTS = ['requirements.txt']
INSTALL_REQUIRES = sorted(
    set(
        line.partition('#')[0].strip()
        for file in (os.path.join(os.path.dirname(__file__), file)
                     for file in REQUIREMENTS)
        for line in open(file)) - {''})

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,
      url=URL,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      packages=PACKAGES,
      install_requires=INSTALL_REQUIRES,
      include_package_data=True,
      zip_safe=False)

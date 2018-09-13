import os
from distutils.core import setup
from setuptools import find_packages


NAME = 'mooda'
VERSION = '0.1.0'
DESCRIPTION = 'Module for Ocean Observatory Data Analysis'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.md')
LONG_DESCRIPTION = """
MOODA - Module for Ocean Observatory Data Analysis

Mooda is a python package designed mainly for oceanographers and marine science students. It is based on a power scripting system for:

direct data access;
data filtering methods;
complex visualization tools;
quality control generation;
specific data analysis tools for different scientific disciplines.
The package is designed to be open, adaptable and scalable allowing future contributions from researchers and developers from all the marine science disciplines.

This work is performed in the framework of the European Multidisciplinary Seafloor and Water-Column Observatory development (EMSOdev - http://www.emsodev.eu/).

Check the documentation on http://mooda.readthedocs.io/.
"""
CLASSIFIERS = ['Development Status :: 4 - Beta',
               'Environment :: X11 Applications :: Qt',
               'Environment :: Console',
               'Natural Language :: English',
               'License :: OSI Approved :: MIT License',
               'Operating System :: Microsoft',
               'Programming Language :: Python :: 3.6',
               'Topic :: Scientific/Engineering :: Visualization',
               'Topic :: Software Development :: Libraries :: Python Modules',
               'Topic :: Scientific/Engineering :: Physics',
               'Intended Audience :: Education',
               'Intended Audience :: Science/Research',
               'Intended Audience :: Developers']
KEYWORDS = ['ocean',
            'sea',
            'OBSEA',
            'EMODnet',
            'EMSO']
URL = 'https://github.com/rbardaji/mooda'
AUTHOR = 'Raul Bardaji Benach'
AUTHOR_EMAIL = 'rbardaji@gmail.com'
LICENSE = 'MIT'
PACKAGES = find_packages()
requirements = ['requirements-waterframe.txt',
                'requirements-access-egim.txt']
INSTALL_REQUIRES = sorted(
    set(
        line.partition('#')[0].strip()
        for file in (os.path.join(os.path.dirname(__file__), file)
                     for file in requirements)
        for line in open(file)) - {''})
EXTRAS_REQUIRE = {'gui': ['pyqt5']}

ENTRY_POINTS = {
    'gui_scripts': ['mooda = mooda.app.mooda_gui.__main__:main']}

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
      extras_require=EXTRAS_REQUIRE,
      entry_points=ENTRY_POINTS,
      include_package_data=True,
      zip_safe=False)
# download_url='https://github.com/rbardaji/oceanobs/archive/1.0.tar.gz',

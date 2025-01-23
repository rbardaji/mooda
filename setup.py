# setup.py
"""Setup config to install mooda"""

from setuptools import setup, find_packages

NAME = 'mooda'
VERSION = '2.0.0'
DESCRIPTION = 'Module for Ocean Observatory Data Analysis'
LONG_DESCRIPTION = """
MOODA - Module for Ocean Observatory Data Analysis

Mooda is a Python package designed mainly for oceanographers and marine science students.
It provides tools to:

- Open and analyze data files from scientific instrumentation and platforms
- Perform data quality control
- Create plots commonly used in the oceanographic community
- Export data files in netCDF and CSV formats

Documentation: https://github.com/rbardaji/mooda
"""
CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Natural Language :: English',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Scientific/Engineering :: Physics',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Developers',
]
KEYWORDS = ['ocean', 'sea', 'EMODnet', 'EMSO']
URL = 'https://github.com/rbardaji/mooda'
AUTHOR = 'Raul Bardaji Benach'
AUTHOR_EMAIL = 'rbardaji@gmail.com'
LICENSE = 'MIT'

# Load requirements from the requirements.txt file
with open('requirements.txt') as f:
    INSTALL_REQUIRES = f.read().splitlines()

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    url=URL,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    zip_safe=False,
)

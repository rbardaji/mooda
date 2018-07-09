import os
from distutils.core import setup
from setuptools import find_packages


NAME = 'mooda'
VERSION = '0.0.1'
DESCRIPTION = 'Module for Ocean Observatory Data Analysis'
README_FILE = os.path.join(os.path.dirname(__file__), 'README.md')
LONG_DESCRIPTION = open(README_FILE).read()
CLASSIFIERS = ['Development Status :: 3 - Alpha',
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
URL = 'https://github.com/rbardaji/oceanobs'
AUTHOR = 'Raul Bardaji Benach'
AUTHOR_EMAIL = 'rbardaji@gmail.com'
LICENSE = 'MIT'
PACKAGES = find_packages()
requirements = ['requirements-waterframe.txt',
                'requirements-app-mooda_gui.txt',
                'requirements-access-egim.txt']
INSTALL_REQUIRES = sorted(
    set(
        line.partition('#')[0].strip()
        for file in (os.path.join(os.path.dirname(__file__), file)
                     for file in requirements)
        for line in open(file)) - {''})
ENTRY_POINTS = {
    'gui_scripts': ['mooda = oceanobs.app.mooda_gui.__main__:main']}

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
      entry_points=ENTRY_POINTS,
      include_package_data=True,
      zip_safe=False)
# download_url='https://github.com/rbardaji/oceanobs/archive/1.0.tar.gz',

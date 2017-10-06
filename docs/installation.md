The easiest way for the majority of users to install oceanobs is to install from [PyPI](https://pypi.python.org/pypi/oceanobs). This way is the recommended installation method for most users.

We also provide instructions for installing from source, or a [development version](https://github.com/rbardaji/oceanobs).

# Python version support

All versions of [Python 3](https://www.python.org/downloads/).

# Installing **oceanobs**

## Prerequisites

*oceanobs* has the following Python package dependencies:

* [gsw](https://pypi.python.org/pypi/gsw/)
* [matplotlib](http://matplotlib.org/)
* [basemap](https://matplotlib.org/basemap/) (from mpl_toolkits.basemap)
* [netCDF4](http://unidata.github.io/netcdf4-python/)
* [numpy](http://www.numpy.org/)
* [pandas](http://www.numpy.org/)
* [requests](http://docs.python-requests.org/en/master/)
* [scipy](https://www.scipy.org/)
* [PyQT4](https://wiki.python.org/moin/PyQt4/)

Most of the dependencies can be installed via *pip*.

```bat
pip install matplotlib
pip install numpy
pip install pandas
pip install netCDF4
pip install requests
pip install scipy
pip install pyqt4
pip install gsw
```

*basemap* library for Python 3 is not on the [Python Package Index Server](https://pypi.python.org/pypi). If you are a Windows user, the easiest way to install it is downloading from the [Unofficial Windows Binaries for Python Extension Packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/#basemap) and install the binary with the command *pip install [write here the path of the binary]*. Notice that basemap also has dependencies, so you also need to install the [pyprog library](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyproj). *oceanobs* can work without the basemap library, but you could not call to some of its functions. 

## Installing from PyPI

You can install oceanobs via pip from [PyPI](https://pypi.python.org/pypi/oceanobs).

```bat
pip install oceanobs
```

## Installing from source

There are many ways to clone or download the source code from [GitHub](https://github.com/rbardaji/oceanobs) on your computer. If you do not have a git client, you can press the *Download ZIP* button, which is located under the *Clone or Download* drop-down of the [GitHub page](https://github.com/rbardaji/oceanobs).

If you have previously installed oceanobs with *pip*, remember to uninstall it, so you do not have problems with the library links.

```bat
pip uninstall oceanobs
```

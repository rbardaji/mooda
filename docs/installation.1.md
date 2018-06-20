The easiest way for the majority of users to install oceanobs is to install from [PyPI](https://pypi.python.org/pypi/oceanobs). This way is the recommended installation method for most users.

New to Python? If you don't know anything about Python but you want to use *oceanobs* and its GUI, please follow the [absolute beginner's guide](#absolute-beginners-guide).

We also provide instructions for installing from source, or a [development version](https://github.com/rbardaji/oceanobs).

# Python version support

Officially [Python](https://www.python.org/downloads/) >= 3.4.

# Installing **oceanobs**

## Absolute beginner's guide

1. Download and install Python 3.5 with the Anaconda distribution. Anaconda contains many libraries that we need to use for *oceanobs*.
	
	* Anaconda for Windowns 32 bits, [here](https://repo.continuum.io/archive/Anaconda3-4.2.0-Windows-x86.exe).
	* Anaconda for Windowns 64 bits, [here](https://repo.continuum.io/archive/Anaconda3-4.2.0-Windows-x86_64.exe).
	* Anaconda for Linux 32 bits, [here](https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86.sh).
	* Anaconda for Linux 64 bits, [here](https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh).
	* Anaconda for MacOSX, [here](https://repo.continuum.io/archive/Anaconda3-4.2.0-MacOSX-x86_64.pkg).
 
2. Open the *Anaconda Prompt* and write the following lines to install the *oceanobs* dependencies.
	
	2.1. Write **conda install -c conda-forge gsw** to install the library *gsw*.
	
	2.2. Write **conda install -c conda-forge basemap** to install the library *basemap*.
	
	2.3. Write **pip install netCDF4** to install the library *netCDF4*.
	
	2.4. Write **conda install pyqt=4.11** to install the library *pyQT4*.
	
	2.5. Write **pip install -U numpy** to upgrade the library *numpy* to the last version.
	
	2.6. Write **pip install oceanobs** to install the library *oceanobs*.

**The installation is finished!!!** Now, test that everything is ok writing the following lines:

1. Write **python** to enter to the *python console*.

2. Write **import oceanobs.inwater**. If nothing happens, we are doing good.

3. Write **import oceanobs.mooda**. If nothing happens, congratulations, everything is well installed. Close the Anaconda Prompt and start to analyze oceanographic data.

## Installing from PyPI

You can install oceanobs via pip from [PyPI](https://pypi.python.org/pypi/oceanobs).

```bat
pip install oceanobs
```

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

## Installing from source

There are many ways to clone or download the source code from [GitHub](https://github.com/rbardaji/oceanobs) on your computer. If you do not have a git client, you can press the *Download ZIP* button, which is located under the *Clone or Download* drop-down of the [GitHub page](https://github.com/rbardaji/oceanobs).

If you have previously installed oceanobs with *pip*, remember to uninstall it, so you do not have problems with the library links.

```bat
pip uninstall oceanobs
```

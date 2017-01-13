# Overview

Python package for analyzing data from marine observatories. This work is performed in the framework of the European Multisiciplinary Seafloor and Water-Column Observatory development ([EMSOdev](http://www.emsodev.eu/)).

At the moment, you can analyze data coming from the EMSO test site [OBSEA](http://www.obsea.es). Additionally the package accepts alternative formats from data provided by other  marine observation platforms (now [EMODnet and Jerico](http://www.jerico-ri.eu/data-access/)). You can create your script using the oceanobs libraries or use the graphical user interface that comes with the package.

## Getting Started

These instructions will get you the Python package on your local machine for development and testing purposes.

### Prerequisites

You need [Python 3](https://www.python.org/downloads/) and the following libraries:

- [matplotlib](http://matplotlib.org/)
- [numpy](http://www.numpy.org/)
- [pandas](http://pandas.pydata.org/)
- [netCDF4](http://unidata.github.io/netcdf4-python/)

The installation of the libraries is easy, with pip:

	pip install matplotlib
	pip install numpy
	pip install pandas
	pip install netCDF4
	
### Installing

Easy, with pip:

	pip install oceanobs

## Common examples

This is a short introduction to oceanobs, geared mainly for new users.

### Analyzing data from OBSEA

Customarily, we import as follows:

```python
import matplotlib.pyplot as plt
import oceanobs.obsea as obs
import sys
```

Creating an "observatory" object by passing the path of the data from OBSEA that you want to analyze:

```python
# Write here your path with OBSEA data  
path_data = ""

# Opening data file
ob = obs.OBSEA(path_data)
# If there is any problem opening the file, the instance variable 
# "dialog" will tell you what is happening
if ob.dialog:
    print(ob.dialog)
	sys.exit()
```

Finally, we are going to make plots of all the available data.

```python
# Plotting all data you have
ob.plt_all()
plt.show()
```

Below you will find all the code together.

```python
import matplotlib.pyplot as plt
import oceanobs.obsea as obs
import sys

# Write here your path with OBSEA data  
path_data = ""

# Opening data file
ob = obs.OBSEA(path_data)
# If there is any problem opening the file, the instance variable 
# "dialog" will tell you what is happening
if ob.dialog:
    print(ob.dialog)
	sys.exit()

# Plotting all data you have
ob.plt_all()
plt.show()
```

### Analyzing data from EMODnet and Jerico

Customarily, we import as follows:

```python
import matplotlib.pyplot as plt
import oceanobs.emodnet as obs
import sys
```

Creating an "observatory" object by passing the path of the data from OBSEA that you want to analyze:

```python
# Write here your path with OBSEA data  
path_data = ""

# Opening data file
ob = obs.EMODnet(path_data)
# If there is any problem opening the file, the instance variable 
# "dialog" will tell you what is happening
if ob.dialog:
    print(ob.dialog)
	sys.exit()
```

Finally, we are going to make plots of all the available data.

```python
# Plotting all data you have
ob.plt_all()
plt.show()
```

Below you will find all the code together.

```python
import matplotlib.pyplot as plt
import oceanobs.emodnet as obs
import sys

# Write here your path with OBSEA data  
path_data = ""

# Opening data file
ob = obs.EMODnet(path_data)
# If there is any problem opening the file, the instance variable 
# "dialog" will tell you what is happening
if ob.dialog:
    print(ob.dialog)
	sys.exit()

# Plotting all data you have
ob.plt_all()
plt.show()
```

## Versioning

Our last realese is [oceanobs v0.2.1](https://github.com/rbardaji/oceanobs/tarball/0.2.1).

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **Raul Bardaji** - *Initial work* - [rbardaji](https://github.com/rbardaji)

## License

This project is licensed under the MIT License.
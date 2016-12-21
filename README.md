# oceanobs

Python package for analyzing data from marine observatories.
At the moment, you can analyze data coming from [OBSEA](http://www.obsea.es) and [EMODnet-Jerico](http://www.jerico-ri.eu/data-access/).
You can create your script using the oceanobs libraries or use the graphical user interface that comes with the package.

This work is performed in the [EMSOdev](http://www.emsodev.eu/) framework.

## Getting Started

These instructions will get you the Python package on your local machine for development and testing purposes.

### Prerequisites

You need [Python 3](https://www.python.org/downloads/) and the following libraries:

- [matplotlib](http://matplotlib.org/)
- [numpy](http://www.numpy.org/)
- [pandas](http://pandas.pydata.org/)
- [netCDF4](http://unidata.github.io/netcdf4-python/)

The installation of the libraries is easy, with pip:

	$ pip install matplotlib
	$ pip install numpy
	$ pip install pandas
	$ pip install netCDF4

### Installing

Easy, with pip:

	$ pip install oceanobs

## Usage examples

Work in progress.

### With OBSEA data

```
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
```

### Common part independent of the data procedence

```
# Show some data information
print("Platform code: {}".format(ob.metadata['platform_code'][0]))
print("WMO platform code: {}".format(ob.metadata['wmo_platform_code'][0]))
print("Institution: {}".format(ob.metadata['institution'][0]))
print("Type: {}".format(ob.metadata['type'][0]))
print("Data: ".format(ob.data))

# Resample data frequency, in this case weekly. 
# The function will return the data averaging all values in a week.
# Most comont resamples:
# - Weekly -> W
# - Daily -> D
# - Hourly -> H
# - Every minute -> T
ob.resample_data('W')
if ob.dialog:
    print(ob.dialog)

# Slicing data
# Write start and stop dates with the format "yyMMddHHmmss"
start = '20160117000000' # This is an example of date
stop = '20160131000000'
ob.slicing(start, stop)
if ob.dialog:
    print(ob.dialog)

# Plotting all data you have
ob.plt_all()
plt.show()
	
```
## Versioning

Our last realese is [oceanobs v0.1.1](https://github.com/rbardaji/oceanobs/tarball/0.1.1).

We use [SemVer](http://semver.org/) for versioning.

## Authors

* **Raul Bardaji** - *Initial work* - [rbardaji](https://github.com/rbardaji)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

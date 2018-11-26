# Oceanobs v0.2.1

Release: December 27, 2016

New Features

* In gui.py: Now we can open EMODnet files.
* In observatory.py:
  * plt_atmpres(): It plots pressure at sea level in dBs.
  * plt_atmpres(): It plots sea level in meters.
  * plt_prec(): It plots rain accumulation in millimeters.
  * plt_relhu(): It plots relative humidity in %.
  * plt_gusp(): It plots gust wind speed in meter/second.
  * plt_cudi(): It plots current to a direction relative true north in degrees.
  * plt_cusp(): It plots horizontal current speed in meters/second.

Performance Enhancements

* In emodnet.py:
  * open(): Fixed bug opening a list of file paths. We removed the option to open CSV files. It is difficult to understand the columns of the CSV file.
* In gui.py: Fixed bug opening the GUI with an external call.
* In observatory.py:
  * plt_atm(): Deleted x1000.

  Return to the [Versions Index](index_versions.md).
  
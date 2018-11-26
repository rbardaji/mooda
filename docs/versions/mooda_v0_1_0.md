# mooda v0.1.0

Released: September 10, 2018

* In mooda/\_\_init\_\_.py:
  * It does not load plotmap.py if you do not have installed the basemap library. We added a warning message.
  * \_\_version\_\_ added.
* In mooda/waterframe.py:
  * barplot(): It creates the graph even without knowing the meaning of the parameters.
  * \_\_repr\_\_: New method. Return a string containing a printable representation of an object.
  * corr(): New function. Compute pairwise correlation of data columns, excluding NA/null values.
  * max_diff(): New function. Calculation the maximum difference between values of two parameters.
  * mean(): New function. Calculation of the mean of the values of a parameter.
  * max(): New function. Find the maximum value of a parameter.
  * min(): New function. Find the minimum value of a parameter.
* In mooda/access/egim.py:
  * to_csv(): New function. It creates a CSV file following the OceanSites standard.
  * METADATA_*: Fixed bug in the long strings of the dictionaries.
  * METADATA_DOX2_AADI4381: Changed long name.
  
  Return to the [Versions Index](index_versions.md).
  
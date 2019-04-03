# mooda v0.3.0

State: Work in progress.

In waterframe.py:

* qcbarplot(): Legend changed.
* to_csv(): We have changed the way to save the metadata within the file. We have added an exception that was produced with the Pangea metadata.
* to_netcdf(): Some metadata contains lists of str. This is not compatible with the NETCDF3_64BITS format. We have changed the phrase lists by separate sentences by ",".
* \_\_repr\_\_(): Added "\n\n" in front of the parameter information.
* get_coordinates(): New method. It returns the coordinates of the WaterFrame measurements.
* \_\_getatr\_\_(): New magic method. It returns the metadata information.
* empty(): New method. It returns True if self.data is empty.
* info_metadata(): The values of the metadata dictionary are forced to be str.

In access/egim.py

* to_netcdf(): Fixed bug creating QC Flags.
* to_csv(): Fixed bug creating QC Flags.

In access/pangea.py: New access module to download data from wwww.pangea.de.

* Class Pangea:
  * \_\_init\_\_: Constructor of the class
  * get_metadata(): Static method to download metadata from Pangea.
  * get_data(): Static method to download data from Pangea.
  * to_waterframe(): It creates a mooda.WaterFrame object from the data and metadata saved into the object.
  * from_source_to_waterframe(): Static method that creates a mooda.WaterFrame object from the input data source of Pangea.

In access/licor.py: New access module to read data from LiCor instrumentation.

* Class Licor:
  * from_txt_to_waterframe(): It is a static method. It reads a txt datalog file and returns a WaterFrame.

In ifig.py: New module to create the interactive charts of Plotly.

* Class IFig:
  * \_\_init\_\_: Constructor of the class
  * site_map(): It creates a chart with a map with the coordinates of the site.
  * time_series(): It creates a chart of a time series of a parameter.
  * site_map_from_waterframe(): Static method. Similar to site_map().
  * time_series_from_waterframe(): Static method. Similar to time_series().

Return to the [Versions Index](index_versions.md).

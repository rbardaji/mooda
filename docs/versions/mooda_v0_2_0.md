# mooda v0.2.0

State: Work in progress.

* In mooda/waterframe.py:
  * constructor(): We added the function parameter "path".
  * to_csv(): New function. It saves the current WaterFrame to a CSV.
  * \_\_repr\_\_: We changed the output message.
  * qc(): Now, you can enter the parameter key = "all" and it will apply the QC tests to all parameters.
  * tsplot(): Input parameters changed.
  * hist(): New function. It creates a histogram plot.
  * rename(): Now it works even if the WaterFrame parameter has no meaning.
  * slice_time(): Now the input parameters are optional.
  * concat(): Bug solved when data frames contains duplicated indexes.
  * use_only(): The argument "parameters" is now optional.
  * to_pickle(): Now it returns True if the file was created.
* In mooda/\_\_init\_\_: The warning is not a print now. We use the library warnings.
* In mooda/app/mooda_gui/plotsplitter.py:
  * initUI(): We added a PlainTextEditor to show other information about the WaterFrame. We changed the metadata view to a PlainTextEditor.
* In requirements-waterframe.txt: netcdf4 added.
* In mooda/access/egim.py:
  * to_netcdf(): New optional input parameters added. Return True if operation successful.
  * to_csv(): New optional input parameters added. Return True if operation successful.
  
  Return to the [Versions Index](index_versions.md).
  
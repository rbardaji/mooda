# API reference

We import the package as follows:

```python
import mooda as md
```

## Read data

* [md.read_nc(*path*)](input/read_nc.md): Get a WaterFrame from a generic NetCDF.
* [md.read_pkl(*path_pkl*)](input/read_pkl.md): Get a WaterFrame from a Pickle file.

## WaterFrame

We declare a WaterFrame object as follows:

```python
wf = md.WaterFrame()
```

* [WaterFrame](waterframe/waterframe.md): General WaterFrame object information.

### Analyze data

* [wf.copy()](waterframe/analysis/copy.md): Get a copy of the WaterFrame.
* [wf.corr()](waterframe/analysis/corr.md): Compute pairwise correlation of data columns of parameter1 and parameter2, excluding NA/null values.
* [wf.drop(*parameters*, *inplace*=*True*)](waterframe/analysis/drop.md): Remove input parameters from WaterFrame.data.
* [wf.info_metadata(*keys*=*None*)](waterframe/analysis/info_metadata.md): It returns a formatted string with the metadata information.
* [wf.info_vocabulary(*keys*=*None*)](waterframe/analysis/info_vocabulary.md): It returns a formatted string with the vocabulary information.
* [wf.max_diff(parameter1, parameter2)](waterframe/analysis/max_diff.md): It calculates the maximum difference between the values of two parameters.
* [wf.max(*parameter*)](waterframe/analysis/max.md): Get the maximum value of a parameter.
* [wf.min(*parameter*)](waterframe/analysis/min.md): Get the minimum value of a parameter.
* [wf.rename(*actual_name*, *new_name*, *inplace*=*True*)](waterframe/analysis/rename.md): It renames a parameter.
* [wf.resample(*rule*, *method*=*'mean'*, *inplace*=*True*)](waterframe/analysis/resample.md): Convenience method for frequency conversion and sampling of time series of the WaterFrame object.
* [wf.time_intervals(*parameter*, *frequency*)](waterframe/analysis/time_intervals.md): It returns the index (TIME) of intervals between NaNs.
* [wf.use_only(*parameters_to_use*, *inplace*=*True*)](waterframe/analysis/use_only.md): It deletes all parameters except the input parameters.
* [wf.reduce_memory(*inplace*=*True*)](waterframe/analysis/reduce_memory.md): It reduces the WaterFrame size in memory by 30% - 50%

### Outout

* [wf.metadata_to_html()](waterframe/output/metadata_to_html.md): Make an HTML file with the metadata information.
* [wf.to_csv()](waterframe/output/to_csv.md): Create a CSV file with the WaterFrame data.
* [wf.to_es()](waterframe/output/to_es.md): Injestion of the WaterFrame into a ElasticSeach DB.
* [wf.to_json()](waterframe/output/to_json.md): Get a JSON with the WaterFrame information.
* [wf.to_nc(*path*, *nc_format*=*"NETCDF4"*)](waterframe/output/to_nc.md): Save the WaterFrame in a NetCDF file.
* [wf.to_pkl(*path*)](waterframe/output/to_pkl.md): Save the WaterFrame in a Pickle file.

### Static plot

* [wf.plot_hist(*parameters*=*None*, *mean_line*=*False*, ***kwds*)](waterframe/plot/plot_hist.md): Make a histogram of the WaterFrame's. A histogram is a representation of the distribution of data.
* [wf.plot_timebar(*keys*, *ax*=*None*, *time_interval_mean*=*None*)](waterframe/plot/plot_timebar.md): Make a bar plot of the input keys. The bars are positioned at x with date/time. Their dimensions are given by height.
* [wf.plot_timeseries(*parameters_to_plot*=*None*, *qc_flags*=*None*, *rolling_window*=*None*, ax=*None*, *average_time*=*None*, *secondary_y*=*None*, *color*=*None*)](waterframe/plot/plot_timeseries.md): Plot the input parameters with time on X and the parameters on Y. It calculates the standar deviation of a rolling window and plot it.
* [wf.plot(***kwds*)](waterframe/plot/plot.md): It calls the pandas DataFrame.plot() method.

### Interactive plot

* [wf.iplot_location(self)](waterframe/iplot/iplot_location.md): It creates a Plotly Figure with a map and a spot of the measurement location of the WaterFrame.
* [wf.iplot_timeseries(*parameters_to_plot*=*None*)](waterframe/iplot/iplot_timeseries.md): It creates a Plotly figure with the time-series of the input parameters.
* [wf.iplot_scatter(*y*, *x*=*'TIME'*, *trendline*=*None*, *marginal_x*=*None*, *marginal_y*=*&#39;histogram&#39;*, *color*=*&#39;auto&#39;*, *symbol*=*&#39;DEPTH&#39;*, *range_y*=*&#39;auto&#39;*, ***kwds*)](waterframe/iplot/iplot_scatter.md): It makes an interactive scatter plot.
* [wf.iplot_data_intervals(*resample_rule*=*'D'*, ***kwds*)](waterframe/iplot/iplot_data_intervals.md): It creates a plot to view the time intervals of the parameters.
* [wf.iplot_line(*y*, *x*=*'TIME'*, *marginal_x*=*None*, *marginal_y*=*&#39;histogram&#39;*, *color*=*&#39;auto&#39;*, *range_y*=*&#39;auto&#39;*, *line_shape*=*&#39;lineard&#39;*, *rangeslider_visible*=*True*, *line_group*=*&#39;DEPTH&#39;*, ***kwds*)](waterframe/iplot/iplot_line.md): Each data point is represented as a marker point, whose location is given by the x and y columns of wf.data.
* [wf.iplot_bar_polar(*theta*, *color*, *r*=*'auto'*, *template*=*&#39;xgridoff&#39;*, *color_continuous_scale*=*&#39;auto&#39;*, ***kwds)*](waterframe//iplot/iplot_bar_polar.md): In a polar bar plot, each row of 'color' is represented as a wedge mark in polar coordinates.

### Data Quality Control

* [wf.qc_syntax_test()](waterframe/qc/qc_syntax_test.md): It checks whether the object data contains all the QC columns required to pass the rest of the tests.
* [wf.qc_flat_test(*parameters*=*None*, *window*=*3*, *flag*=*4*, *inplace*=*True*)](waterframe/qc/qc_flat_test.md): It detects if there are equal consecutive values in the time series.
* [wf.qc_range_test(*parameters*=*None*, *limits*=*None*, *flag*=*4*, *inplace*=*True*)](waterframe/qc/qc_range_test.md): Check if the values of a parameter are out of range.
* [wf.qc_spike_test(*parameters*=*None*, *window*=*0*, *threshold*=*3*, *flag*=*4*, *inplace*=*True*)](waterframe/qc/qc_spike_test.md): It checks if there is any spike in the time series.

## Utilities

* [md.concat(*list_wf*)](util/concat.md): `concat` does all of the heavy liftings of performing concatenation operations between a list of WaterFrames.
* [md.es_create_indexes(*delete_previous_indexes*=*True*, ***kwargs*)](util/es_create_indexes.md): Creation of ElasticSearch Indexes to save a WaterFrame object.
* [md.md5(*file_path*, *save_dm5*=*True*, *md5_path*=*None*)](util/md5.md): It generates the MD5 code of the input file.

### Interactive plot

* [md.iplot_location(*list_wf*)](util/iplot/iplot_location.md): It creates a Plotly Figure with a map and a spot of the measurement location of the input WaterFrames.
* [md.iplot_timeseries(*list_wf*, *parameter_to_plot*)](util/iplot/iplot_timeseries.md): It creates a Plotly figure with the time-series of the input parameter.

### Jupyter Notebook Widgets

* [md.widget_qc(*wf*, *parameter*, *range_test*=*[-1000, 1000]*, *spike_window*=*100*, *spike_threshold*=*3.5*, *spike_influence*=*0.5*)](util/md_widgets/widget_qc.md): It makes a Data QC Widget for Jupyter Notebook.
* [md.widget_emso(*wf*, *depth_range*=*[-10, 10000]*, *user*=*&#39;&#39;*, *password*=*&#39;&#39;*, *token*=*&#39;&#39;*)](util/md_widgets/widget_emso.md): It makes a Jupyter notebook widget to download data from the EMSO API.
* [md.widget_emso_qc(*wf*, *depth_range*=*[-10, 10000]*, *range_test*=*[-1000, 1000]*, *spike_window*=*100*, *spike_threshold*=*3.5*, *spike_influence*=*0.5*, *user*=*&#39;&#39;*, *password*=*&#39;&#39;*, *token*=*&#39;&#39;*)](util/md_widgets/widget_emso_qc.md): It makes a Jupyter Notebook Widget used to download EMSO data and make data quality control tests.
* [md.widget_save(*wf*)](util/md_widgets/widget_save.md): Make a Jupyter notebook widget that allows to save the WaterFrame to a file.

Return to the [Docs Index](../index_docs.md).

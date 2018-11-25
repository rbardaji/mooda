# WaterFrame.corr(*parameter1*, *parameter2*, *method='pearson'*, *min_periods=1*)

Compute pairwise correlation of data columns of parameter1 and parameter2, excluding NA/null values.

Parameters | Description | Type
--- | --- | ---
parameter1 | Key name of the column 1 to correlate. | str
parameter2 | Key name of the column 2 to correlate. | str
method | {‘pearson’, ‘kendall’, ‘spearman’} pearson : standard correlation coefficient, kendall : Kendall Tau correlation coefficient, spearman : Spearman rank correlation | str, optional
min_periods | Minimum number of observations required per pair of columns to have a valid result. Currently only available for pearson and spearman correlation. | int, optional

Returns | Description | Type
--- | --- | ---
correlation_number | correlation coefficient | float

# WaterFrame.scatter_matrix(*keys*, *ax*=*None*)

Draw a matrix of scatter plots.

## Parameters

    key: list of string
        keys of self.data to plot.
        Keys must contain different words.
        ex:
            keys = ['VAVH', 'VCMX'] is ok.
            keys = ['VAVH', 'VAVH'] is not ok.
    ax: matplotlib.axes object, optional (ax = None)
        It is used to add the plot to an input axes object.

## Returns

    ax: matplotlib.AxesSubplot or False
        New axes of the plot.
        It returns False if operation is not successful.

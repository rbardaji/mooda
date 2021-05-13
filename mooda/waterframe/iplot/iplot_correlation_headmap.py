import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator
from sklearn.linear_model import LinearRegression


def iplot_correlation_headmap(self, parameters=[], **kwds):
    """
    It uses plotly.express.imshow.

    Parameters
    ----------
        parameter: str

    Returns
    -------
        fig: plotly.graph_objects.Figure
    """

    if parameters:

        _df = self.data.copy()
        _df.reset_index(inplace=True)
        data_frame = _df[parameters].copy()
        corr = data_frame.corr()
    
        fig = px.imshow(corr, **kwds)
    
    else:
        fig = px.imshow(**kwds)
    
    return fig

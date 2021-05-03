import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.validators.scatter.marker import SymbolValidator
from sklearn.linear_model import LinearRegression


def iplot_box(self, parameter="", color=None, **kwds):
    """
    It uses plotly.express.box.

    Parameters
    ----------
        parameter: str
        color: str
            Name of a column in self.data, or a pandas Series or array_like
            object. Values from this column or array_like are used to assign
            color to marks.
            If color == 'auto' and parameter != "", color = 'DEPTH'

    Returns
    -------
        fig: plotly.graph_objects.Figure
    """

    if parameter:
        if color == 'auto':
            color = 'DEPTH'

        _df = self.data.copy()
        _df.reset_index(inplace=True)
        data_frame = _df[[parameter, 'TIME', 'DEPTH']].copy()
        # Define x and yof box
        x = parameter
    
        fig = px.box(data_frame=data_frame, x=x, color=color, **kwds)
    
    else:
        if color == 'auto':
            color = None
        fig = px.box(**kwds)
    
    return fig

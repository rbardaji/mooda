import pandas as pd
import plotly
import plotly.express as px


def iplot(self, y, x='auto', color='auto', facet_col='auto', plot_type='scatter', marginal_x='rug',
          marginal_y='box', trendline='ols', filename=None):
    """
    Get a figure using plotly.express.

    Parameters
    ----------
        y: str
            Y axes of the plot. Column of self.data to plot.
        x: str
            X axes of the plot. It can be an index or a column of self.data.
            If plot_type is 'scatter' and x is 'auto', x will the 'TIME' index of self.data. 
        color: str
            Column of self.data, auto or None. Colors of the dots of the scatter.
        facet_col: None or str
            Create different columns related to a value of a parameter.
            If facet_col is not None, marginal_y will not be visible.
            If facet_col is 'auto' and plot_type is 'scatter', facet_color is 'DEPTH' index of
            self.data.
        plot_type: str
            Type of plot figure to make.
            Options: scatter, histogram
        marginal_x: str
            Additional graph on top x axes.
            Options: None, rug, histogram, violin, box.
        marginal_y: str
            Additional graph on right y axes.
            Options: None, rug, histogram, violin, box.
        trendline: str
            Activate the trendline.
            Options:
                None
                ols (https://en.wikipedia.org/wiki/Ordinary_least_squares)
                lowess (https://en.wikipedia.org/wiki/Local_regression)
        filename: str
            Path and name of the file to save the figure in html.
    Returns
    -------
        fig: plotly figure
    """
    # Get columns to plot
    columns_to_plot = []

    # Add y axes as a list to columns to plot
    if isinstance(y, str):
        columns_to_plot = [y]
    else:
        columns_to_plot = y
    
    # Add x axes to columns to plot
    if plot_type == 'scatter':
        if x == 'auto':
            x = 'TIME'
            columns_to_plot.append('TIME')
        else:
            columns_to_plot.append(x)

    # Add color to columns to plot
    if color:
        if plot_type == 'scatter':
            if color == 'auto':
                if f'{y}_QC' in self.data.keys():
                    color = f'{y}_QC'
                    columns_to_plot.append(color)
                else:
                    color = None
            else:
                columns_to_plot.append(color)
        elif plot_type == 'histogram':
            if color == 'auto':
                if 'DEPTH' in self.data.index.names:
                    color = 'DEPTH'
                    columns_to_plot.append(color)
                else:
                    color = None
            else:
                columns_to_plot.append(color)

    # Add facet_col to columns to plot
    if facet_col:
        if plot_type == 'scatter':
            if facet_col == 'auto':
                if 'DEPTH' in self.data.index.names and 'DEPTH' not in columns_to_plot:
                    facet_col = 'DEPTH'
                    columns_to_plot.append(facet_col)
                else:
                    facet_col = None
            else:
                columns_to_plot.append(facet_col)

    # Create the df
    df = self.data.copy()
    df.reset_index(inplace=True)

    # Change 'DEPTH' and '<parameter>_QC' to type str
    if 'DEPTH' in df.keys():
        df['DEPTH'] = df['DEPTH'].apply(str)
    for key in df.keys():
        if '_QC' in key:
            df[key] = df[key].apply(str)

    # Use only the selected columns
    df = df[columns_to_plot].copy()
    df.dropna(inplace=True)

    # Make sure that 'TIME' is a timestamp
    if 'TIME' in df.keys():
        df['TIME'] = pd.to_datetime(df['TIME'])

    if plot_type == 'scatter':
        fig = px.scatter(df, 
                         x=x,
                         y=y,
                         color=color,
                         marginal_x=marginal_x,
                         marginal_y=marginal_y,
                         trendline=trendline,
                         facet_col=facet_col)
    elif plot_type == 'histogram':
        fig = px.histogram(
            df, 
            x=y,
            y=y,
            color=color)

    if filename:
        plotly.offline.plot(fig, filename=filename)

    return fig

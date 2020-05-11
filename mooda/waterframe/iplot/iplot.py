import plotly
import plotly.express as px


def iplot(self, y, x='TIME', color='auto', plot_type='scatter', marginal_x='rug',
          marginal_y='box', trendline='ols', filename=None):
    """
    Get a figure using plotly.express.

    Parameters
    ----------
        y: str
            Y axes of the plot. Column of self.data to plot.
        x: str
            X axes of the plot. It can be an index or a column of self.data.
        color: str
            Column of self.data, auto or None. Colors of the dots of the scatter.
        plot_type: str
            Type of plot figure to make.
            Options: scatter
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
    if isinstance(y, str):
        columns_to_plot = [y]
    else:
        columns_to_plot = y
    columns_to_plot.append(x)
    if color:
        if color == 'auto':
            if f'{y}_QC' in self.data.keys():
                color = f'{y}_QC'
                columns_to_plot.append(color)
            else:
                color = None
        else:
            columns_to_plot.append(color)

    df = self.data.copy()
    df.reset_index(inplace=True)
    if 'DEPTH' in df.keys() and 'DEPTH' not in columns_to_plot:
        columns_to_plot.append('DEPTH')
        df['DEPTH'] = df['DEPTH'].apply(str)
    df = df[columns_to_plot].copy()
    df.dropna(inplace=True)
    df['DEPTH'] = df['DEPTH'].apply(str)
    print(df.head())
    if plot_type == 'scatter':
        fig = px.scatter(df, 
                         x=x,
                         y=y,
                         color=color,
                         marginal_x=marginal_x,
                         marginal_y=marginal_y,
                         trendline=trendline)

        if filename:
            plotly.offline.plot(fig, filename=filename)
    return fig

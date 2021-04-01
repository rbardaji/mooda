import pandas as pd
import plotly.express as px

def iplot_bar_polar(self, theta, color, r='auto', template='xgridoff',
                    color_continuous_scale='auto', **kwds):
    """
    It uses plotly.express.bar_polar.
    In a polar bar plot, each row of 'color' is represented as a wedge mark in polar coordinates.
    
    Parameters
    ----------
        theta: str
            wf.data colum with the directions in degrees (0 - 360)
        color: str
            wf.data colum with the data to plot with colors
        r: str
            wf.data column with the data to use as a radium.
            If r = 'auto', r is the counts of 'theta' en each direction.
        template: str
            Plotly express style templates.
            Options: 
                'ggplot2'
                'seaborn'
                'simple_white'
                'plotly'
                'plotly_white'
                'plotly_dark'
                'presentation'
                'xgridoff'
                'ygridoff'
                'gridon'
                'none'
        color_continuous_scale: plotly.express.sequential
            View https://plotly.com/python/colorscales/.
            If color_continuous_scale = 'auto', color_continuous_scale = px.colors.sequential.Rainbow
        **kwds: plotly.express.bar_polar arguments

    Returns
    -------
        fig: plotly.graph_objects.Figure
    """

    if color_continuous_scale == 'auto':
        color_continuous_scale = px.colors.sequential.Rainbow

    df = self.data.copy()

    # Create directions
    df['direction'] = 'N'
    df.loc[df[theta].between(11.25, 33.75) , 'direction'] = 'NNE'
    df.loc[df[theta].between(33.75, 56.25) , 'direction'] = 'NE'
    df.loc[df[theta].between(56.25, 78.75) , 'direction'] = 'ENE'
    df.loc[df[theta].between(78.75, 101.25) , 'direction'] = 'E'
    df.loc[df[theta].between(101.25, 123.75) , 'direction'] = 'ESE'
    df.loc[df[theta].between(123.75, 146.25) , 'direction'] = 'SE'
    df.loc[df[theta].between(146.25, 168.75) , 'direction'] = 'SSE'
    df.loc[df[theta].between(168.75, 191.25) , 'direction'] = 'S'
    df.loc[df[theta].between(191.25, 213.75) , 'direction'] = 'SSW'
    df.loc[df[theta].between(213.75, 236.25) , 'direction'] = 'SW'
    df.loc[df[theta].between(236.25, 258.75) , 'direction'] = 'WSW'
    df.loc[df[theta].between(258.75, 281.25) , 'direction'] = 'W'
    df.loc[df[theta].between(281.25, 303.75) , 'direction'] = 'WNW'
    df.loc[df[theta].between(303.75, 326.25) , 'direction'] = 'NW'
    df.loc[df[theta].between(326.25, 348.75) , 'direction'] = 'NNW'

    new_index = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 
                     'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']

    # Create serie of counts for directions
    s_dir = df['direction'].value_counts()
    s_dir.rename('frequency', inplace=True)

    # Create mean of directions
    df_mean = df.groupby(['direction']).mean()

    df_work = pd.merge(s_dir, df_mean[color], right_index=True, left_index=True)
    if r != 'auto':
        df_work = pd.merge(df_work, df_mean[r], right_index=True,
                           left_index=True)
    
    df_work = df_work.reindex(new_index)
    df_work.reset_index(inplace=True)
    df_work.rename(columns={'index': 'direction'}, inplace=True)

    df_work[color] = df_work[color].fillna(0)
    df_work.loc[df_work[color] == 0, 'frequency'] = 0

    if r == 'auto':
        r = 'frequency'

    try:
        labels = {color: f'{self.vocabulary[color]["long_name"]} ({self.vocabulary[color]["units"]})'}
    except KeyError:
        labels=None
    fig = px.bar_polar(df_work, r=r, theta="direction", color=color,
                       color_continuous_scale= color_continuous_scale,
                       template=template, labels=labels)
    return fig

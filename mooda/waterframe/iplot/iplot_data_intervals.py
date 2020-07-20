import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def iplot_data_intervals(self, resample_rule='D', **kwds):
    """
    It uses plotly.express.timeline.
    It creates a plot to view the time intervals of the parameters.

    Parameters
    ----------
        resample_rule: None, str
            Resample rule.

    Returns
    -------
        fig: plotly.graph_objects.Figure
    """
    if resample_rule:
        _wf = self.resample(rule=resample_rule, inplace=False)
    else:
        _wf = self.copy()

    df_content = []
    for parameter in _wf.parameters:
        intervals = _wf.time_intervals(parameter, resample_rule)
        
        for start, end in intervals:
            df_content.append(
                dict(
                    Task=_wf.vocabulary[parameter].get('long_name', parameter),
                    Start=start,
                    Finish=end,
                    Resource=parameter))
    df = pd.DataFrame(df_content)

    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Resource",
        title='Data intervals',
        labels={'Task': 'Parameters'})

    fig.update(layout_showlegend=False)
    fig.update_layout(margin=dict(l=250, r=0, t=30, b=0))

    return fig

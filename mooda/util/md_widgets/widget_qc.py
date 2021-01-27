""" Implementation of mooda.widget_qc()"""
from typing import List
import ipywidgets as widgets
from IPython.display import clear_output
import plotly.offline as pyo


def widget_qc(wf, parameter: str, range_test: List[float]=[-1000, 1000],
              spike_window: int=100, spike_threshold: float=3.5,
              spike_influence: float=0.5):
    """
    It makes a Data QC Widget for Jupyter Notebook

    Parameters
    ----------
        wf: WaterFrame
        parameter: str
            Parameter
        range_test: List[float]
            Limits for the range test [min value, max value]
        spike_window: int
            Window for the spike test
        spike_threshold: float
            Float for the spike test
        spike_influence: float
            Influence of the bad data on the spike test

    Returns
    -------
        main_box: ipwidgets.VBox
            Jupyter notebook widget 
    """
    pyo.init_notebook_mode()

    def show_result(wf, parameter_in, chart_title=''):
        # Change name of flags
        wf2 = wf.copy()
        qc_labels = {0: 'No QC', 1: 'Good data', 4: 'Bad data'}
        wf2.data[f'{parameter_in}_QC'].replace(qc_labels, inplace=True)

        fig = wf2.iplot_line(
            parameter_in,
            color=f'{parameter_in}_QC',
            marginal_y=None,
            line_shape='linear',
            rangeslider_visible=False,
            line_dash_sequence=['dot', 'dot'],
            title=chart_title)
        fig.show()

    # Reset flags
    reset_label = widgets.Label('Reset flags:')
    reset_checkbox = widgets.Checkbox(description='Do it!')

    # Flat test
    flat_label = widgets.Label('Flat test:')
    window_flat = widgets.IntText(value=2,
                                    description='Window:',
                                    disabled=False,
                                    color='black')
    flat_checkbox = widgets.Checkbox(description='Do it!')

    # Range test
    range_label = widgets.Label('Range test:')
    range_checkbox = widgets.Checkbox(description='Do it!')
    limits = widgets.FloatRangeSlider(value=[range_test[0], range_test[1]],
                                        min=range_test[0],
                                        max=range_test[1],
                                        step=0.1,
                                        description='Limits:',
                                        disabled=False,
                                        continuous_update=False,
                                        orientation='horizontal',
                                        readout=True,
                                        readout_format='.1f')

    # Spike test
    spike_label = widgets.Label('Spike test:')
    spike_checkbox = widgets.Checkbox(description='Do it!')
    window_spike = widgets.IntText(value=spike_window,
                                    description='Window:', disabled=False,
                                    color='black')
    threshold = widgets.FloatText(value=spike_threshold,
                                    description='Threshold:', disabled=False,
                                    color='black')
    influence = widgets.FloatSlider(
        value=spike_influence,
        min=0,
        max=1,
        step=0.1,
        description='Influence:',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        slider_color='white'
    )

    # Replace
    replace_label = widgets.Label('Replace QC:')
    replace_checkbox = widgets.Checkbox(description='Do it!')

    # Button
    button = widgets.Button(description='Run tests')
    out = widgets.Output()
    def on_button_clicked(_):
        # "linking function with output"
        with out:
            # what happens when we press the button
            clear_output()
            print('Please wait')
            
            if parameter in wf.parameters:
                show_result(wf, parameter, 
                            'Values without apply any QC test')
                print()

                if reset_checkbox.value:
                    wf.qc_replace(parameters=[parameter], to_replace=1, value=0)
                    wf.qc_replace(parameters=[parameter], to_replace=4, value=0)
                if flat_checkbox.value:
                    wf.qc_flat_test(window=window_flat.value,
                                    parameters=[parameter])
                    show_result(wf, parameter, 
                                'Values after apply the flat test. ' + \
                                ' Configuration flat test: window = ' + \
                                f'{window_flat.value}')
                    print()
                if range_checkbox.value:
                    wf.qc_range_test(limits=limits.value,
                                     parameters=[parameter])
                    show_result(wf, parameter,
                                'Values after apply the flat test and ' + \
                                    'the range test. Configuration ' + \
                                    f'range test: limits = {limits.value}')
                    print()
                if spike_checkbox.value:
                    wf.qc_spike_test(window=window_spike.value,
                                        influence=influence.value,
                                        threshold=threshold.value,
                                        parameters=[parameter])
                    show_result(wf, parameter,
                                'Values after apply the flat test, the ' \
                                    'range test and the spike test.' + \
                                    ' Configuration spike test: window ' \
                                    f'= {window_spike.value}, ' \
                                    f'influence = {influence.value}, ' + \
                                    f'threshold = {threshold.value}')
                    print()
                if replace_checkbox.value:
                    start = 0
                    if spike_checkbox.value:
                        start = window_spike.value
                    wf.qc_replace(parameters=[parameter], start=start)
                    show_result(wf, parameter, f'Final result')
            else:
                print(f'Parameter {parameter} not in {wf.parameters}')

    # linking button and function together using a button's method
    button.on_click(on_button_clicked)

    reset_box = widgets.HBox([reset_label, reset_checkbox])
    flat_box = widgets.HBox([flat_label, flat_checkbox, window_flat])
    range_box = widgets.HBox([range_label, range_checkbox, limits])
    spike_column = widgets.VBox([window_spike, threshold, influence])
    spike_box = widgets.HBox([spike_label, spike_checkbox, spike_column])
    replace_box = widgets.HBox([replace_label, replace_checkbox])

    main_box = widgets.VBox([reset_box, flat_box, range_box, spike_box,
                             replace_box, button, out])

    return main_box

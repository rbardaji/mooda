""" Implementation of mooda.widget_emso()"""
from typing import List
from IPython.core.display import display
import ipywidgets as widgets
from IPython.display import clear_output
from datetime import date
import plotly.offline as pyo
import plotly.io as pio
import mooda


def widget_emso_qc(wf, depth_range: List[float]=[-10, 10000],
                   range_test: List[float]=[-1000, 1000],
                   spike_window: int=100, spike_threshold: float=3.5,
                   spike_influence: float=0.5,  user: str='',
                   password: str='', token: str=''):
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

    # Sing in
    user_label = widgets.Label('User:')
    input_user = widgets.Text(value=user)
    password_label = widgets.Label('Password:')
    input_password = widgets.Text(value=password)
    token_label = widgets.Label('Token:')
    input_token = widgets.Text(value=token)

    # map
    emso = mooda.EMSO(user=input_user.value, password=input_password.value,
                      token=input_token.value)
    map_dict = emso.get_fig_map()
    pio.show(map_dict)

    # Platform code
    platform_label = widgets.Label('Platform code:')
    platform_codes = emso.get_info_platform_code()
    input_platform = widgets.Dropdown(options=platform_codes,
                                      value=platform_codes[0], disabled=False)
    
    # Get metadata
    metadata_list = emso.get_metadata(platform_codes=[platform_codes[0]])
    try:
        metadata = metadata_list[0]
        parameter_list = metadata.get('parameters')
        if parameter_list is None:
            parameter_list = emso.get_info_parameter()
        depth_min = metadata.get('geospatial_vertical_min', depth_range[0])
        depth_max = metadata.get('geospatial_vertical_max', depth_range[1])
        start_date = metadata.get('time_coverage_start')
        if start_date:
            start_date = start_date.split('T')[0]
        end_date = metadata.get('time_coverage_end')
        if end_date:
            end_date = end_date.split('T')[0]
    except:
        parameter_list = emso.get_info_parameter()
        depth_min = depth_range[0]
        depth_max = depth_range[1]
        start_date = None
        end_date = None

    # Parameters
    parameters_label = widgets.Label('Parameters:')
    input_parameters = widgets.SelectMultiple(options=parameter_list, rows=10,
                                              disabled=False,
                                              value=[parameter_list[0]])

    # Size
    size_label = widgets.Label('Size:')
    input_size = widgets.BoundedIntText(value=10, min=1, step=1)

    # Depth
    depth_label = widgets.Label('Depth:')
    input_depth = widgets.FloatRangeSlider(value=[depth_min, depth_max],
                                           min=depth_min,
                                           max=depth_max, step=0.1,
                                           disabled=False,
                                           continuous_update=False,
                                           orientation='horizontal',
                                           readout=True, readout_format='.1f')

    # Time
    start_date_label = widgets.Label('Start date:')
    input_start_date = widgets.DatePicker(disabled=False,
                                          min_date=date(
                                              int(start_date.split('-')[0]),
                                              int(start_date.split('-')[1]),
                                              int(start_date.split('-')[2])),
                                          max_date=date(
                                              int(end_date.split('-')[0]),
                                              int(end_date.split('-')[1]),
                                              int(end_date.split('-')[2])),
                                          value=date(
                                              int(start_date.split('-')[0]),
                                              int(start_date.split('-')[1]),
                                              int(start_date.split('-')[2])))

    end_date_label = widgets.Label('End date:')
    input_end_date = widgets.DatePicker(disabled=False,
                                        min_date=date(
                                            int(start_date.split('-')[0]),
                                            int(start_date.split('-')[1]),
                                            int(start_date.split('-')[2])),
                                        max_date=date(
                                            int(end_date.split('-')[0]),
                                            int(end_date.split('-')[1]),
                                            int(end_date.split('-')[2])),
                                        value=date(
                                            int(end_date.split('-')[0]),
                                            int(end_date.split('-')[1]),
                                            int(end_date.split('-')[2])))

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

    def update_components(_):
        # Update all components
        emso = mooda.EMSO(user=input_user.value, password=input_password.value,
                          token=input_token.value)
        # Get metadata
        metadata_list = emso.get_metadata(platform_codes=[input_platform.value])

        try:
            metadata = metadata_list[0]
            parameter_list = metadata.get('parameters')
            if parameter_list is None:
                parameter_list = emso.get_info_parameter()
            depth_min = metadata.get('geospatial_vertical_min', depth_range[0])
            depth_max = metadata.get('geospatial_vertical_max', depth_range[1])
            start_date = metadata.get('time_coverage_start')
            if start_date:
                start_date = start_date.split('T')[0]
            end_date = metadata.get('time_coverage_end')
            if end_date:
                end_date = end_date.split('T')[0]
        except:
            parameter_list = emso.get_info_parameter()
            depth_min = depth_range[0]
            depth_max = depth_range[1]
            start_date = None
            end_date = None
        
        # Parameters
        input_parameters.options = parameter_list

        # Depth
        input_depth.min = depth_min
        input_depth.max = depth_max
        input_depth.value = [depth_min, depth_max]

        # Time
        input_start_date.min_date = date(int(start_date.split('-')[0]),
                                         int(start_date.split('-')[1]),
                                         int(start_date.split('-')[2]))
        input_start_date.max_date = date(int(end_date.split('-')[0]),
                                         int(end_date.split('-')[1]),
                                         int(end_date.split('-')[2]))
        input_start_date.value = date(int(start_date.split('-')[0]),
                                      int(start_date.split('-')[1]),
                                      int(start_date.split('-')[2]))
        input_end_date.min_date = date(int(start_date.split('-')[0]),
                                       int(start_date.split('-')[1]),
                                       int(start_date.split('-')[2]))
        input_end_date.max_date = date(int(end_date.split('-')[0]),
                                       int(end_date.split('-')[1]),
                                       int(end_date.split('-')[2]))
        input_end_date.value = date(int(end_date.split('-')[0]),
                                    int(end_date.split('-')[1]),
                                    int(end_date.split('-')[2]))

    input_platform.observe(update_components, names='value')

    # Button
    button = widgets.Button(description='Get data')
    out = widgets.Output()
    out2 = widgets.Output()
    def on_button_clicked(_):
        # "linking function with output"
        with out:
            # what happens when we press the button
            clear_output()

            parameters = []
            for input_parameter in input_parameters.value:
                parameters.append(input_parameter.split('-')[0].strip())

            if input_start_date.value is None:
                start_time = ''
            else:
                start_time = str(input_start_date.value) + ' 00:00:00'

            if input_end_date.value is None:
                end_time = ''
            else:
                end_time = str(input_end_date.value) + ' 00:00:00'
            
            if input_token.value is None:
                token = ''
            else:
                token = input_token.value

            print('Downloading data, please wait')

            wf2 = mooda.from_emso(platform_code=input_platform.value,
                                  parameters=parameters, start_time=start_time,
                                  end_time=end_time,
                                  depth_min=input_depth.value[0],
                                  depth_max=input_depth.value[1],
                                  user=input_user.value,
                                  password=input_password.value,
                                  size=input_size.value, token=token)
            

            wf.data = wf2.data.copy()
            wf.metadata = wf2.metadata.copy()
            wf.vocabulary = wf2.vocabulary.copy()

            clear_output()
            display(wf)

        with out2:
            # what happens when we press the button
            clear_output()
            print('Making tests')
            
            for parameter_one in wf.parameters: 

                if reset_checkbox.value:
                    wf.qc_replace(parameters=[parameter_one], to_replace=1,
                                  value=0)
                    wf.qc_replace(parameters=[parameter_one], to_replace=4,
                                  value=0)
                if flat_checkbox.value:
                    wf.qc_flat_test(window=window_flat.value,
                                    parameters=[parameter_one])
                if range_checkbox.value:
                    wf.qc_range_test(limits=limits.value,
                                    parameters=[parameter_one])
                if spike_checkbox.value:
                    wf.qc_spike_test(window=window_spike.value,
                                        influence=influence.value,
                                        threshold=threshold.value,
                                        parameters=[parameter_one])
                if replace_checkbox.value:
                    start = 0
                    if spike_checkbox.value:
                        start = window_spike.value
                    wf.qc_replace(parameters=[parameter_one], start=start)

                show_result(wf, parameter_one, f'Final result')

    # linking button and function together using a button's method
    button.on_click(on_button_clicked)

    user_box = widgets.HBox([user_label, input_user, password_label,
                             input_password])
    token_box = widgets.HBox([token_label, input_token])
    platform_box = widgets.HBox([platform_label, input_platform])
    parameters_box = widgets.HBox([parameters_label, input_parameters])
    size_box = widgets.HBox([size_label, input_size])
    depth_box = widgets.HBox([depth_label, input_depth])
    start_date_box = widgets.HBox([start_date_label, input_start_date])
    end_date_box = widgets.HBox([end_date_label, input_end_date])
    reset_box = widgets.HBox([reset_label, reset_checkbox])
    flat_box = widgets.HBox([flat_label, flat_checkbox, window_flat])
    range_box = widgets.HBox([range_label, range_checkbox, limits])
    spike_column = widgets.VBox([window_spike, threshold, influence])
    spike_box = widgets.HBox([spike_label, spike_checkbox, spike_column])
    replace_box = widgets.HBox([replace_label, replace_checkbox])

    main_box = widgets.VBox([user_box, token_box, platform_box, parameters_box,
                             size_box, depth_box, start_date_box, end_date_box,
                             reset_box, flat_box, range_box, spike_box,
                             replace_box, button, out, out2])

    return main_box

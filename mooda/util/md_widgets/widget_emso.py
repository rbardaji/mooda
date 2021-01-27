""" Implementation of mooda.widget_emso()"""
from typing import List
from IPython.core.display import display
import ipywidgets as widgets
from IPython.display import clear_output
from datetime import date
import plotly.offline as pyo
import plotly.io as pio
import mooda

def widget_emso(wf, depth_range: List[float]=[-10, 10000], user: str='',
                password: str='', token: str=''):
    """
    It makes a Jupyter notebook widget to download data from the EMSO API

    Parameters
    ----------
        wf: WaterFrame
        depth_range: List[float]
            Range of depth
        user: str
            User for the EMSO ERIC API
        password: str
            Password for the EMSO ERIC API
        token: str
            Token for the EMSO ERIC API

    Returns
    -------
        main_box: ipwidgets.VBox
            Jupyter notebook widget 
    """
    pyo.init_notebook_mode()

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

            clear_output()
            display(wf)

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

    main_box = widgets.VBox([user_box, token_box, platform_box, parameters_box,
                             size_box, depth_box, start_date_box, end_date_box,
                             button, out])

    return main_box

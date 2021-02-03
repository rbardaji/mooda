""" Implementation of mooda.widget_save()"""
import ipywidgets as widgets


def widget_save(wf):
    """
    Make a Jupyter notebook widget that allows to save the WaterFrame to a file

    Parameters
    ----------
        wf: WaterFrame
    
    Returns
    -------
        main_box: ipwidgets.VBox
            Jupyter notebook widget 
    """
    # Title
    title_label = widgets.Label('Save as...')

    # Filename
    name_label = widgets.Label('Name:')
    input_name = widgets.Text()

    # Type
    type_label = widgets.Label('Type:')
    input_type = widgets.RadioButtons(
        options=['csv', 'nc', 'pkl'], value='csv', disabled=False)

    # Button
    button = widgets.Button(description='Save')
    out_save = widgets.Output()
    def on_button_clicked(_):
        with out_save:
            if input_name.value:
                if input_type.value == 'csv':
                    wf.to_csv(path=f'{input_name.value}.csv')
                elif input_type.value == 'nc':
                    wf.to_nc(path=f'{input_name.value}.nc')
                elif input_type.value == 'pkl':
                    wf.to_pkl(path_pkl=f'{input_name.value}.pkl')
                print('Done.')
            else:
                print('Please, write a name.')
    # linking button and function together using a button's method
    button.on_click(on_button_clicked)

    filename_box = widgets.HBox([name_label, input_name])
    type_box = widgets.HBox([type_label, input_type])

    main_box = widgets.VBox([title_label, filename_box, type_box, button,
                             out_save])

    return main_box

""" Implementation of wf.qc_replace() """
import numpy as np


def qc_replace(self, parameters=None, to_replace=0, value=1, start=0, inplace=True):
    """
    Replace the values of QC from the input parameters.

    Parameters
    ----------
        parameters: None, str or list of str.
            List of parameters to change the values of QC. Ex: ['TEMP', 'PSAL'].
        to_replace: int
            QC value to replace.
        value: int
            Value to replace any values matching to_replace with.
        inplace: bool
            If inplace, makes changes inplace and returns True.
            Otherwhise, returns a new WaterFrame.
    
    Returns
    -------
        new_wf: WaterFrame
    """
    def change_signals(signals):
         # Change flags
        result = []
        for i, signal in enumerate(signals):
            if i < start:
                result.append(signal)
            else:
                if signal == to_replace:
                    result.append(value)
                else:
                    result.append(signal)

        return np.array(result)

    if parameters is None:
        parameters = self.parameters
    elif isinstance(parameters, str):
        parameters = [parameters]

    data = self.data.copy()

    for parameter in parameters:
        
        # New
        df = data[[parameter, f'{parameter}_QC']].reset_index()
        df.set_index('TIME', inplace=True)

        try:
            for depth, df_depth in df.groupby('DEPTH'):
                df_depth.sort_index(inplace=True)

                signals = df_depth[f'{parameter}_QC'].values

                # Change flags
                result = change_signals(signals)

                # Asignation of result with numpy array due to
                # AttributeError: 'list' object has no attribute 'ravel'
                data.loc[(depth,), f'{parameter}_QC'] = np.array(result)
        except KeyError:
            # No Depth
            signals = df[f'{parameter}_QC'].values

            # Change flags
            result = change_signals(signals)
            
            data[f'{parameter}_QC'] = result

    if inplace:
        self.data = data
        return True
    else:
        new_wf = self.copy()
        new_wf.data = data
        return new_wf
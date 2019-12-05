"""
Module to open data from Ocean Observatory Iniciative (OOI)
(https://oceanobservatories.org/)
"""
from mooda import WaterFrame


class OOI:
    """
    Class to open data from Ocean Observatory Iniciative (OOI).
    Web - https://oceanobservatories.org
    """

    @staticmethod
    def from_nc_to_waterframe(path):
        """
        It reads a local nc file or an OpenDap and parses its content into a WaterFrame.

        Parameters
        ----------
            path: str
                Path where the nc files is.

        Returns
        -------
            wf: WaterFrame
        """
        # WaterFrame creation
        wf = WaterFrame(path)

        # Set index
        try:
            wf.data.rename(columns={'time': 'TIME'}, inplace=True)
            # Set index to TIME
            wf.data.set_index('TIME', inplace=True)
        except KeyError:
            pass
        print("Meaning:")
        print(wf.info_meaning())
        keys = wf.data.keys()
        for key in keys:
            # Only use columns with "ctmo" in the name
            # We are going to assign QC to 0, CHECK IT
            if "ctdmo_seawater_pressure" == key:
                # Data
                wf.data.rename(columns={key: 'PRES'}, inplace=True)
                wf.data['PRES_QC'] = 0

                # Meaning
                wf.meaning['PRES'] = {
                    "standard_name": "sea_water_pressure",
                    "long_name": "Sea pressure",
                    "units": "dbar",
                    "valid_min": "0.0",
                    "valid_max": "12000.0"
                }

            elif "ctdmo_seawater_temperature" == key:
                
                # Data
                wf.data.rename(columns={key: 'TEMP'}, inplace=True)
                wf.data['TEMP_QC'] = 0

                # Meaning
                wf.meaning['TEMP'] = {
                    "valid_min": "-5.0",
                    "valid_max": "35.0",
                    "ancillary_variables": "TEMP_QC",
                    "standard_name": "sea_water_temperature",
                    "units": "degrees_C",
                    "long_name": "Sea temperature"
                }
            elif "ctdmo_seawater_conductivity" == key:
                # Data
                wf.data.rename(columns={key: 'CNDC'}, inplace=True)
                wf.data['CNDC_QC'] = 0

                # meaning
                wf.meaning['CNDC'] = {
                    "valid_min": "0.0",
                    "valid_max": "7.0",
                    "ancillary_variables": "CNDC_QC",
                    "standard_name": "sea_water_electrical_conductivity",
                    "units": "S m-1",
                    "long_name": "Electrical conductivity"
                }
            else:
                del wf.data[key]

            # Adding platform_code to metadata
            wf.metadata['platform_code'] = wf.metadata['node']
        return wf

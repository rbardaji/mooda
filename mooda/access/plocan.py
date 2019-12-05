"""
Module to open data from PLOCAN
(http://data.plocan.eu/thredds/catalog/aggregate/public/ESTOCInSitu/catalog.html)
"""
from mooda import WaterFrame


class Plocan:
    """
    Class to open data from PLOCAN.
    Web - http://data.plocan.eu/thredds/catalog/aggregate/public/ESTOCInSitu/catalog.html
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

        print(wf.data.head())

        # Rename columns
        try:
            wf.data.rename(columns={'time': 'TIME'}, inplace=True)
            # Set index to TIME
            wf.data.set_index('TIME', inplace=True)
        except KeyError:
            pass

        for key in wf.data.keys():
            # Change from _qc to _QC
            if "_qc" in key:
                wf.data.rename(columns={key: key[:-2]+'QC'}, inplace=True)

        # Set index to TIME
        wf.data.set_index('TIME', inplace=True)

        return wf

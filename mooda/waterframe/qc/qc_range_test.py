""" Implementation of WaterFrame.qc_range_test(parameters=None, flag=4, limits=None) """


def qc_range_test(self, parameters=None, limits=None, flag=4, inplace=True):
    """
    Check if the values of a parameter are out of range.

    Parameters
    ----------
        parameters: string or list of strings, optional
        (parameters = None)
            key of self.data to apply the test.
        flag: int, optional (flag = 4)
            Flag value to write in on the fail values.
        limits: tuple, optional (limits = None)
            (Min value, max value) of the range of correct values.
        inplace: bool
            If True, it changes the flags in place and returns True.
            Otherwhise it returns an other WaterFrame.

    Returns
    -------
        new_wf: WaterFrame
    """
    ranges = {
        'ATMP': (600, 1500),  # atmospheric pressure at altitude
        'ATMS': (0, 2000),  # Atmospheric pressure at sea level
        'CHLT': (0, 30),  # total chlorophyll
        'CNDC': (0, 30),  # electrical conductivity
        'DRYT': (-20, 60),  # air temperature at sea level
        'GSPD': (0, 40),  # gust wind speed
        'HCDT': (0, 360),  # current to direction relative true north
        'HEAD': (0, 360),  # PLAT. HEADING REL. TRUE NORTH
        'LINC': (0, 3000),  # long-wave incoming radiation
        'LW': (0, 50),  # Downwelling vector radiance as energy
        'OSAT': (0, 200),  # oxygen saturation
        'PHPH': (0, 14),  # ph
        'PRES': (0, 500),  # sea pressure
        'PRRT': (0, 200),  # hourly precipitation rate
        'PSAL': (0, 40),  # practical salinity
        'RDIN': (0, 1100),  # incident radiation
        'SVEL': (130, 180000),  # sound velocity
        'SWDR': (0, 360),  # SWELL DIRECTION REL TRUE N.
        'SWHT': (0, 50),  # SWELL HEIGHT
        'SWPR': (0, 20),  # SWELL PERIOD
        'TEMP': (0, 50),  # Sea temperature
        'VAVH': (0, 20),  # AVER. HEIGHT HIGHEST 1/3 WAVE
        'VAVT': (0, 20),  # AVER. PERIOD HIGHEST 1/3 WAVE
        'VCMX': (0, 20),  # MAX CREST TROUGH WAVE HEIGHT
        'VDIR': (0, 360),  # wave direction rel. true north
        'VEPK': (0, 100),  # WAVE SPECTRUM PEAK ENERGY
        'VHM0': (0, 20),  # SPECTRAL SIGNIFICANT WAVE HEIGHT
        'VMDR': (0, 360),  # Mean wave direction
        'VPED': (0, 360),  # dir. spreading at wave peak
        'VPSP': (0, 360),  # dir. spreading at wave peak
        'VSMC': (0, 20),  # SPECTUM MOMENT(0, 2) WAVE PERIOD
        'VTDH': (0, 40),  # significant wave height
        'VTM02': (0, 13),  # Spectral moments (0, 2) wave period (Tm02)
        'VTPK': (0, 40),  # WAVE SPECTRUM PEAK PERIOD
        'VTZA': (0, 40),  # AVER ZERO CROSSING WAVE PERIOD
        'VTZM': (0, 40),  # period of the highest wave
        'VZMX': (0, 20),  # Maximum zero crossing wave height
        'WDIR': (0, 360),  # Wind from direction relative true north
        'WSPD': (0, 50),  # Horizontal wind speed
    }

    if parameters is None:
        parameters = self.parameters
    elif isinstance(parameters, str):
        parameters = [parameters]

    data = self.data.copy()

    for parameter in parameters:
        if limits:
            # Parameter can be an index
            if parameter in data.index.names:
                data.loc[
                    self.data.index.get_level_values(
                        parameter) < limits[0], parameter + '_QC'] = flag
                data.loc[
                    self.data.index.get_level_values(
                        parameter) > limits[1], parameter + '_QC'] = flag
            else:
                data.loc[self.data[parameter] < limits[0], parameter + '_QC'] = flag
                data.loc[self.data[parameter] > limits[1], parameter + '_QC'] = flag
        elif parameter in ranges.keys():
            self.data.loc[self.data[parameter] < ranges[parameter][0], parameter + '_QC'] = flag
            self.data.loc[self.data[parameter] > ranges[parameter][1], parameter + '_QC'] = flag
    
    if inplace:
        self.data = data
        return True
    else:
        new_wf = self.copy()
        new_wf.data = data
        return new_wf

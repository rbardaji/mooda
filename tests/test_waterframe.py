from oceanobs import WaterFrame


class TestWaterFrame():

    @staticmethod
    def create_waterframe():
        msg = "Creation of a Waterframe object:"
        try:
            WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

    @staticmethod
    def from_netcdf():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading netcdf file:"
        try:
            wf.from_netcdf("tests/data/test_file.nc")
            print(msg, "Done.")
        except FileNotFoundError:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/test_file.nc")

    @staticmethod
    def to_pickle():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading netcdf file:"
        try:
            wf.from_netcdf("tests/data/test_file.nc")
            print(msg, "Done.")
        except FileNotFoundError:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/test_file.nc")

        msg = "Saving into pickle file:"
        try:
            wf.to_pickle("tests/data/pickle_file.pkl")
            print(msg, "Done.")
        except FileNotFoundError:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/test_file.nc")

    @staticmethod
    def from_pickle():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/pickle_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

    @staticmethod
    def tsplot():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/pickle_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Creation of figure:"
        wf.tsplot(key='VAVH')
        print(msg, "Done.")

    @staticmethod
    def scatter_matrix():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/test_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Creation of figure:"
        ax = wf.scatter_matrix(keys=['VAVH', 'VCMX'])
        if ax is not None:
            print(msg, "Done.")
        else:
            print(msg, "Error, not enough keys.")

    @staticmethod
    def qcplot():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/pickle_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Creation of QC figure:"
        wf.qcplot(key="VAVH")
        print(msg, "Done.")

    @staticmethod
    def qcbarplot():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/pickle_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Creation of QC BAR figure:"
        wf.qcbarplot()
        print(msg, "Done.")

    @staticmethod
    def spectroplot():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/test_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        wf.spectroplot()

    @staticmethod
    def spike_test():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/test_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Spike test:"
        wf.spike_test('VAVH')
        print(msg, "Done.")

    @staticmethod
    def range_test():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/test_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Range test:"
        wf.range_test('VAVH')
        print(msg, "Done.")

    @staticmethod
    def flat_test():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/test_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Flat test:"
        wf.flat_test('VAVH')
        print(msg, "Done.")

    @staticmethod
    def flag2flag():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/test_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Flag to Flag:"
        wf.flag2flag('VAVH', 0, 1)
        print(msg, "Done.")

    @staticmethod
    def reset_flag():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/test_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Reset flags:"
        wf.reset_flag('VAVH')
        print(msg, "Done.")

    @staticmethod
    def qc():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/test_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "QC:"
        wf.qc('VAVH')
        print(msg, "Done.")

    @staticmethod
    def drop():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/pickle_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Droping parameters:"
        wf.drop(['DEPTH', 'VEPK', 'VHM0', 'VSMC', 'VTPK', 'VAVT', 'SWHT',
                 'SWPR'])
        if len(wf.data.keys()) == 5:
            print(msg, "Done.")
        else:
            print(msg, "Error.")

    @staticmethod
    def rename():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/test_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Renaming name:"
        wf.rename('VAVH', 'HELLO')
        if 'HELLO' in wf.data.keys():
            print(msg, "Done.")
        else:
            print(msg, "Error.")

    @staticmethod
    def concat():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/test_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Concat other waterframe:"
        wf.concat(wf)
        if 'VCMX(NEW1)' in wf.data.keys():
            print(msg, "Done.")
        else:
            print(msg, "Error.")

    @staticmethod
    def resample():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/test_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Resampling:"
        wf.resample('W')
        if str(wf.data.index[0]) == "1956-12-02 00:00:00" and \
           str(wf.data.index[1]) == "1956-12-09 00:00:00":
            print(msg, "Done.")
        else:
            print(msg, "Error.")

    @staticmethod
    def slice():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/test_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Slicing:"
        wf.slice(start='20050101000000', end='20120101000000')
        if str(wf.data.index[0]) == "2005-01-01 00:20:00.000000256" and \
           str(wf.data.index[-1]) == "2012-01-01 00:00:00":
            print(msg, "Done.")
        else:
            print(msg, "Error.")

    @staticmethod
    def clear():
        msg = "Creation of a Waterframe object:"
        try:
            wf = WaterFrame()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Loading pickle file:"
        wf.from_pickle("tests/data/test_file.pkl")
        if wf.data.empty:
            print(msg, "No such file or directory. Please check if exist"
                  "tests/data/pickle_file.pkl")
        else:
            print(msg, "Done.")

        msg = "Cleaning Waterframe:"
        wf.clear()
        if wf.data.empty and not wf.metadata:
            print(msg, "Done.")
        else:
            print(msg, "Error.")

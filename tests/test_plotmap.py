from oceanobs import PlotMap


class TestPlotMap():

    @staticmethod
    def create_plotmap():
        msg = "Creation of a plotmap object:"
        try:
            PlotMap()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

    @staticmethod
    def map_world():
        msg = "Creation of a plotmap object:"
        try:
            pm = PlotMap()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Creation of World Map:"
        try:
            pm.map_world()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

    @staticmethod
    def map_mediterranean():
        msg = "Creation of a plotmap object:"
        try:
            pm = PlotMap()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Creation of World Map:"
        try:
            pm.map_mediterranean()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

    @staticmethod
    def add_point():
        msg = "Creation of a plotmap object:"
        try:
            pm = PlotMap()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Creation of World Map:"
        try:
            pm.map_world()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

        msg = "Adding a point:"
        try:
            pm.add_point(lon=0, lat=0)
            print(msg, "Done.")
        except ImportError:
            print(msg, "Import Error.")

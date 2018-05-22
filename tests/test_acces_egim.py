from oceanobs.access import EGIM


class TestAccessEgim():

    @staticmethod
    def download_timeserie():
        msg = "Creation of EGIM object:"
        try:
            downloader = EGIM()
            print(msg, "Done.")
        except ImportError:
            print(msg, "Input error.")

        msg = "Load observatories:"
        code, observatory_list = downloader.observatories()
        if code == 401:
            print(msg, "Unauthorized. Please check login and password.")
        elif code == 500:
            print(msg, "Done.")

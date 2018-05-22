# from matplotlib.pylab import plt
from tests import TestWaterFrame
from tests import TestPlotMap
from tests import TestAccessEgim
from oceanobs import mooda


def test_waterframe():
    # TestWaterFrame.create_waterframe()
    # TestWaterFrame.from_netcdf()
    # TestWaterFrame.to_pickle()
    # TestWaterFrame.from_pickle()
    # TestWaterFrame.tsplot()
    # TestWaterFrame.scatter_matrix()
    # TestWaterFrame.qcplot()
    # TestWaterFrame.qcbarplot()
    TestWaterFrame.spectroplot()  # Not done
    # TestWaterFrame.spike_test()
    # TestWaterFrame.range_test()
    # TestWaterFrame.flat_test()
    # TestWaterFrame.flag2flag()
    # TestWaterFrame.reset_flag()
    # TestWaterFrame.qc()
    # TestWaterFrame.drop()
    # TestWaterFrame.rename()
    # TestWaterFrame.concat()
    # TestWaterFrame.resample()
    # TestWaterFrame.slice()
    # TestWaterFrame.clear()


def test_plotmap():
    TestPlotMap.create_plotmap()
    # TestPlotMap.map_world()
    # TestPlotMap.map_mediterranean()
    # TestPlotMap.add_point()


def test_access_egim():
    TestAccessEgim.download_timeserie()


def test_mooda():
    mooda()

if __name__ == '__main__':
    # test_waterframe()
    # test_plotmap()
    # test_access_egim()
    # plt.show()
    test_mooda()

""" Implementation of mooda """
from .waterframe import WaterFrame
from .input import read_nc_emodnet, read_nc, read_nc_imos, read_pkl, read_nc_moist
from .util import concat, iplot_location, iplot_timeseries, md5, es_create_indexes

__version__ = '1.6.0'

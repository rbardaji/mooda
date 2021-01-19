""" Implementation of mooda """

from .waterframe import WaterFrame
from .input import read_nc_emodnet, read_nc, read_nc_imos, read_pkl, \
    read_nc_moist, from_emso
from .util import concat, iplot_location, iplot_timeseries, md5, \
    es_create_indexes, Widgets, EMSO

__version__ = '1.7.1'

""" Implementation of mooda """

from .waterframe import WaterFrame
from .input import read_nc_emodnet, read_nc, read_nc_imos, read_pkl, \
    read_nc_moist, from_emso
from .util import concat, iplot_location, iplot_timeseries, md5, \
    es_create_indexes, EMSO, widget_qc, widget_emso, widget_emso_qc, widget_save

__version__ = '1.9.2'

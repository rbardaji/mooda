""" Implementation of mooda """

from .waterframe import WaterFrame
from .input import read_nc, read_pkl, read_df, from_erddap, read_dat_td_pati
from .util import concat, iplot_location, iplot_timeseries, md5, \
    es_create_indexes, EMSO, widget_qc, widget_emso, widget_emso_qc, \
    widget_save, iplot_line

__version__ = '2.0.0'

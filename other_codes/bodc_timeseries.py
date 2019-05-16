""" Modify existing NetCDF files"""
from mooda import WaterFrame
from mooda.access import Bodc
from mooda.ifig import IFig
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


# PATH = r"C:\Users\rbard\Google Drive\ok\git\mooda-dash\files\emso\pap\bodc\ctd\48.9990N_16.5020W\2017\06\21\pap-bodc-ctd_200706211351_201706211420.nc"
PATH60 = r"C:\Users\rbard\Desktop\Nueva carpeta\60.nc"
PATH75 = r"C:\Users\rbard\Desktop\Nueva carpeta\75.nc"
PATH90 = r"C:\Users\rbard\Desktop\Nueva carpeta\90.nc"
PATH110 = r"C:\Users\rbard\Desktop\Nueva carpeta\110.nc"
PATH130 = r"C:\Users\rbard\Desktop\Nueva carpeta\130.nc"
PATH150 = r"C:\Users\rbard\Desktop\Nueva carpeta\150.nc"
PATH200 = r"C:\Users\rbard\Desktop\Nueva carpeta\200.nc"
PATH250 = r"C:\Users\rbard\Desktop\Nueva carpeta\250.nc"
PATH300 = r"C:\Users\rbard\Desktop\Nueva carpeta\300.nc"
PATH1000 = r"C:\Users\rbard\Desktop\Nueva carpeta\1000.nc"


def main():
    """
    Main
    """

    # wf = WaterFrame(PATH)
    # print(wf.data.keys())
    # print(wf.data['TIME_SEADATANET_QC'])
    wfall = Bodc.from_nc_to_waterframe(PATH60)
    wf75 = Bodc.from_nc_to_waterframe(PATH75)
    wf90 = Bodc.from_nc_to_waterframe(PATH90)
    wf110 = Bodc.from_nc_to_waterframe(PATH110)
    wf130 = Bodc.from_nc_to_waterframe(PATH130)
    wf150 = Bodc.from_nc_to_waterframe(PATH150)
    wf200 = Bodc.from_nc_to_waterframe(PATH200)
    wf250 = Bodc.from_nc_to_waterframe(PATH250)
    wf300 = Bodc.from_nc_to_waterframe(PATH300)
    wf1000 = Bodc.from_nc_to_waterframe(PATH1000)

    # Rename
    wfall.rename('TEMP', '60 meters')
    wf75.rename('TEMP', '75 meters')
    wf90.rename('TEMP', '90 meters')
    wf110.rename('TEMP', '110 meters')
    wf110.rename('TEMP', '110 meters')
    wf130.rename('TEMP', '130 meters')
    wf150.rename('TEMP', '150 meters')
    wf200.rename('TEMP', '200 meters')
    wf250.rename('TEMP', '250 meters')
    wf300.rename('TEMP', '300 meters')
    wf1000.rename('TEMP', '1000 meters')

    # Concat
    wfall.concat(wf75)
    wfall.concat(wf90)
    wfall.concat(wf110)
    wfall.concat(wf130)
    wfall.concat(wf150)
    wfall.concat(wf200)
    wfall.concat(wf250)
    wfall.concat(wf300)
    wfall.concat(wf1000)

    print(wfall)
    wfall.use_only(flags=1)

    ifigure = IFig(wfall)
    figure1 = ifigure.profile()

    figure1 = ifigure.time_series(['60 meters', '75 meters', '90 meters', '110 meters',
                                   '130 meters', '150 meters', '200 meters', '250 meters',
                                   '300 meters', '1000 meters'])
    figure1['layout']['title'] = "Sea water temperature"
    plot(figure1,
         filename="exampletempts.html",
         config={'showLink': True, 'linkText': "Edit chart"})

    # figure2 = ifigure.profile(parameters='TEMP')
    # plot(figure2, filename="exampletemp.html", config={'showLink': True, 'linkText': "Edit chart"})
    # print(wf.info_metadata())
    # print(wf.data.head(500))
    # print(wf.meaning['ACYCAA01'])
    # print(wf.data['PRES'].head())

main()

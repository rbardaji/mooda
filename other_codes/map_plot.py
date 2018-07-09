import mooda
import matplotlib.pyplot as plt

path = r"C:\Users\rbard\Desktop\MO_LATEST_TS_MO_OBSEA_20180406.nc"

wf = mooda.WaterFrame()
wf.from_netcdf(path)

for key in wf.metadata:
    print(key, wf.metadata[key])

pm = mooda.PlotMap()
pm.map_mediterranean()
pm.add_point(lon=wf.metadata["last_longitude_observation"],
             lat=wf.metadata["last_latitude_observation"],
             label=wf.metadata["site_code"])
plt.show()

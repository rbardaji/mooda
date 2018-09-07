from mooda import WaterFrame

# Path where CTD file is
path = r"C:\Users\rbard\Google Drive\Work\EmsoDev\server\ejemplos web\megakit - mio\data\obsea\OS_OBSEA_2016120120170426_R_4381-606.nc"

wf = WaterFrame()
wf.from_netcdf(path)

print(wf)

# Resample 2 hourly
# wf.resample('2H')

# Slice
# wf.slice_time("20170327000000", "20170423000000")

mean = wf.mean('DOX2')
index, max_waves = wf.max('DOX2')
index2, min_waves = wf.min('DOX2')

print(index)
print(index2)
# print(max_waves)
# print(min_waves)
# print("Marea:", (max_waves - min_waves)/2)

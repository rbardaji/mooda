import mooda

wf = mooda.WaterFrame()

wf.from_netcdf("OS_OBSEA_2017010120170115_R_SBE54-0049.nc")

print(wf.data.head())
print(wf.metadata['license'])

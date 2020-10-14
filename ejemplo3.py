import mooda as md  # pip install mooda

# Configuration
file_location = r'MO_TS_MO_OBSEA_201402.nc'

# Open file
wf = md.read_nc_emodnet(file_location)

print(wf.memory_usage)

wf.reduce_memory()

print(wf.memory_usage)
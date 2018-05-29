import oceanobs as oc
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('ggplot')

wf = oc.WaterFrame()
wf.from_netcdf(
    r"C:\Users\rbard\Desktop\Tarragona-coast-buoy\IR_TS_MO_Tarragona-coast-buoy.nc")

metadata = wf.metadata
data = wf.data

print("Parameters:", wf.parameters())
print("Size of original WaterFrame:", wf.memory_usage()/10**6, "MBytes")

wf.use_only('TEMP', flags=1, dropnan=True)

print("Size of data only using 'TEMP' with QC = 1 and without NaNs:",
      wf.memory_usage()/10**6, "MBytes")

print(wf.data.index[0])
print(wf.data.index[-1])

wf.slice('20130101000000', '20161231235959')

wf.spike_test('TEMP')

# wf.qcplot('TEMP')

wf.drop('TEMP', flags=4)

# wf.qcplot('TEMP')
# plt.show()

# wf.tsplot('TEMP')
# plt.show()

# wf.tsplot('TEMP')

ax = wf.barplot(key='TEMP', average_time='A')

# wf.tsplot('TEMP')

plt.show()

import oceanobs as oc
import matplotlib.pyplot as plt
import matplotlib.style as style

style.use('ggplot')

wf = oc.WaterFrame()
wf.from_netcdf(r"C:\Users\rbard\Desktop\Tarragona-coast-buoy\IR_TS_MO_Tarragona-coast-buoy.nc")

print("Parameters:", wf.parameters())
print("Memory usage:", wf.memory_usage()/10**6, "MBytes")

wf.use_only('TEMP', flags=1, dropnan=True)
print("Memory usage:", wf.memory_usage()/10**6, "MBytes")

print("Start:", wf.data.index[0])
print("End:", wf.data.index[-1])

wf.slice_time('20130101000000', '20161231235959')

wf.barplot(key='TEMP', average_time='A')
plt.show()

from oceanobs import WaterFrame
import matplotlib.pyplot as plt
import matplotlib.style as style

style.use('ggplot')

path = r"./docs/example_data/bad_temp.pkl"

wf = WaterFrame()
wf.from_pickle(path)

print(wf.parameters())

wf.reset_flag(key='TEMP')
wf.qcplot('TEMP')
plt.show()

wf.spike_test(key='TEMP', flag=4)
wf.range_test(key='TEMP', flag=2)
wf.flat_test(key='TEMP', flag=3)
wf.flag2flag(key="TEMP")

wf.qcplot('TEMP')
plt.show()

wf.qcbarplot('TEMP')
plt.show()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mooda import WaterFrame

dates = pd.date_range(start='20180101', end='20180131', freq='T')

# data = Sinus creation with noise and trend
fs = dates.size
print(fs)
x = np.arange(fs)
# Signal
f = 30
values = [5 + np.sin(2*np.pi*f * (i/fs)) for i in x]
# noise
noise = np.random.randn(dates.size)/12
# Trend
f_trend = 3
values_trend = [2 * np.sin(2*np.pi*f_trend * (i/fs)) for i in x]

data = values + noise + values_trend

# Spikes
spike_values = []
for i in x:
    spike = np.random.randn()
    if spike > 3.8 or spike < -3.8:
        spike_values.append(3*spike)
    else:
        spike_values.append(0)

data = data + spike_values

# Flat zones
flat_values = []
flat_repeat = 0
i_flat = 0
for i in x:
    if i_flat < flat_repeat:
        data[i] = data[i-1]
        i_flat += 1
    else:
        i_flat = 0
        flat_repeat = 0
        flat_bool = np.random.randn()
        if flat_bool > 3.8:
            flat_repeat = flat_bool*1000
            print(flat_repeat)


df = pd.DataFrame(data, index=dates, columns=["TEMP"])
df.index.name = 'TIME'
df['TEMP_QC'] = 0

# Creation of WaterFrame
wf = WaterFrame()
wf.data = df.copy()
wf.metadata["name"] = "Test data with errors"
wf.meaning["TEMP"] = "Seawater temperature"
units = {'units': 'degree Celsius'}
wf.meaning['TEMP'] = units

wf.to_pickle('test_errors.pkl')

df.plot()

plt.show()

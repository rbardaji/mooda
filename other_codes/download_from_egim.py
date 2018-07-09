from mooda.access import EGIM
import matplotlib.pylab as plt

login = "emsodev"
password = "Emsodev2017"
egim = EGIM(login, password)

code, observatories = egim.observatories()
if code == 200:
    for i, observatory in enumerate(observatories):
        print(i, observatory)
else:
    print("Error code:", code)
observatory = observatories[0]

code, instruments = egim.instruments(observatory)
if code == 200:
    for i, instrument in enumerate(instruments):
        print(i, instrument['sensorLongName'])
else:
    print("Error code:", code)

instrument_ctd = instruments[1]['name']
instrument_oximeter = instruments[2]['name']

code, parameters = egim.parameters(observatory, instrument_ctd)
if code == 200:
    for i, parameter in enumerate(parameters):
        print(i, parameter['name'])
else:
    print("Error code:", code)

parameter = parameters[3]['name']

code, metadata = egim.metadata(observatory, instrument_ctd)
if code == 200:
    for key in metadata:
        print(key, metadata[key])
else:
    print("Error code:", code)

code, observation = egim.observation(observatory, instrument_ctd, parameter,
                                     startDate="01/02/2017",
                                     endDate="02/02/2017")
if code == 200:
    print(observation.head())
else:
    print("Error code:", code)

wf = egim.to_waterframe(observation, metadata)

wf.rename(old_name="TEMP", new_name="CTD")

code, observation = egim.observation(observatory, instrument_oximeter,
                                     parameter, startDate="01/02/2017",
                                     endDate="02/02/2017")
if code == 200:
    print(observation.head())
else:
    print("Error code:", code)

code, metadata = egim.metadata(observatory, instrument_ctd)
if code == 200:
    for key in metadata:
        print(key, metadata[key])
else:
    print("Error code:", code)

wf_oximeter = egim.to_waterframe(observation, metadata)
wf_oximeter.rename(old_name="TEMP", new_name="OXIMETER")

wf.concat(wf_oximeter)

print(wf.parameters())

wf.resample(rule="T")

wf.scatter_matrix(["CTD", "OXIMETER"])
plt.show()


wf.tsplot(["CTD", "OXIMETER"])
plt.show()

wf.to_pickle("egim_temps.pkl")

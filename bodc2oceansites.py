""" Modify existing NetCDF files"""
import datetime
from mooda.access import Bodc
import matplotlib.pyplot as plt


PATH = r"C:\Users\rbard\Google Drive\ok\code\web_emso\work\files\emso\pap\mooda\bodc\timeseries\48.9833N_16.4240W\2002\pap-bodc-ts_200210090000_200307081200_d40.0.nc"


def main():
    """
    Main
    """

    wf = Bodc.from_nc_to_waterframe(PATH)

    qc_info = wf.info_qc()
    print("QC INFO INICIO:", qc_info)
    print(wf.info_metadata())

    # print(wf.meaning["MINWDIST"])
    # exit()
    # QC Tests
    # wf.reset_flag()
    # wf.spike_test(flag=9, threshold=5)
    # wf.range_test(flag=9)
    # wf.flat_test(flag=9)
    # wf.flag2flag()
    # # Change to nan all bad values
    # wf.value2nan(flags=9)

    # qc_info = wf.info_qc()
    # print("QC INFO DESPUES DE TESTS:", qc_info)

    # Look for QC flags != 1
    bad_qc = []
    for parameter in wf.parameters():
        for key in qc_info[parameter]:
            if key != 1:
                bad_qc.append(key)
    # Change to nan all bad values
    wf.value2nan(flags=bad_qc)

    qc_info = wf.info_qc()
    print("QC INFO DESPUES AUTO FLAGS:", qc_info)

    # Drop parameters
    # wf.drop(keys="DOX1")

    # qc_info = wf.info_qc()
    # print("QC INFO DESPUES DE DROP:", qc_info)

    # Resample daily
    wf.resample(rule="D")
    wf.flag2flag()

    qc_info = wf.info_qc()
    print("QC INFO DESPUES RESAMPLE:", qc_info)

    # Delete columns with less than "threshold" not nan values
    threshold = 10
    for parameter in wf.parameters():
        if wf[parameter].notnull().values.sum() < threshold:
            wf.drop(keys=parameter)
            print(f"There less than {threshold} not nan values in {parameter}")

    qc_info = wf.info_qc()
    print("QC INFO DESPUES DEL COLUMNS WITH NAN:", qc_info)

    wf.data.dropna(how="all", subset=wf.parameters(), inplace=True)

    qc_info = wf.info_qc()
    print("QC INFO DESPUES DEL ROWS WITH NAN:", qc_info)

    # wf.qcplot('DOX1')
    plt.show()

    # Add some metadata
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    wf.metadata['date_modified'] = now
    print(PATH.split("\\")[-1].split("_d")[1][:-3])
    wf.metadata['geospatial_lat_min'] = PATH.split("\\")[14].split("_")[0][:-1]
    wf.metadata['geospatial_lat_max'] = PATH.split("\\")[14].split("_")[0][:-1]
    wf.metadata['geospatial_vertical_min'] = PATH.split("\\")[-1].split("_d")[1][:-3]
    wf.metadata['geospatial_vertical_max'] = PATH.split("\\")[-1].split("_d")[1][:-3]
    wf.metadata['geospatial_lon_min'] = "-" + PATH.split("\\")[14].split("_")[1][:-1]
    wf.metadata['geospatial_lon_max'] = "-" + PATH.split("\\")[14].split("_")[1][:-1]

    if 'history' in wf.metadata:
        wf.metadata['history'] += f'. {now} Dataset modified with mooda v0.5.1 (DOI: ' + \
                                '10.5281/zenodo.2864645): Only data with QC=1, averaged daily.'
    else:
        wf.metadata['history'] = f'. {now} Dataset modified with mooda v0.5.0 (DOI: ' + \
                                '10.5281/zenodo.2864645): Only data with QC=1, averaged daily.'

    path_to_save = PATH[:-3] + "_D_QC1.nc"
    wf.to_netcdf(path_to_save)

main()

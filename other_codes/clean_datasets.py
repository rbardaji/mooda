""" Modify existing NetCDF files"""
import datetime
from mooda import WaterFrame
import matplotlib.pyplot as plt


PATH = r"YOUR PATH"


def main():
    """
    Main
    """

    wf = WaterFrame(PATH)

    qc_info = wf.info_qc()
    print("QC INFO INICIO:", qc_info)

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
    wf.metadata['history'] += f'. {now} Dataset modified with mooda v0.5.0 (DOI: ' + \
                              '10.5281/zenodo.2643207): Only data with QC=1, averaged daily.'

    path_to_save = PATH[:-3] + "_D_QC1.nc"
    wf.to_netcdf(path_to_save)

main()

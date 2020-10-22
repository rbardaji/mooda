import mooda as md

# Configuration variables
dataset_location = r'.\docs\examples\data\test_qc.pkl'
# QC tests
## Flat test
window_flat = 2
## Range test
limits = [1, 40]
## Spike test
window_spike = 100
threshold = 3.5
influence = 0.5

def show_result(wf, chart_title=''):
    # Change name of flags
    wf2 = wf.copy()
    qc_labels = {0: 'No QC', 1: 'Good data', 4: 'Bad data'}
    wf2.data['TEMP_QC'].replace(qc_labels, inplace=True)

    fig = wf2.iplot_line(
        'TEMP',
        color='TEMP_QC',
        marginal_y=None,
        line_shape='linear',
        rangeslider_visible=False,
        line_dash_sequence=['dot', 'dot'],
        title=chart_title)
    fig.show()


# Open file
wf = md.read_pkl(dataset_location)
show_result(wf, 'Values without apply any QC test')

# QC tests
wf.qc_flat_test()
show_result(
    wf, 'Values after apply the flat test. ' + \
        f' Configuration flat test: window = {window_flat}')

wf.qc_range_test(limits=limits)
show_result(
    wf, 'Values after apply the flat test and the range test.' + \
        f'Configuration range test: limits = {limits}')

wf.qc_spike_test(window=window_spike, influence=influence, threshold=threshold)
show_result(
    wf, 'Values after apply the flat test, the range test and the spike test.' + \
        f' Configuration spike test: window = {window_spike}, influence = {influence}, ' + \
        f'threshold = {threshold}')

wf.qc_replace()
show_result(wf,f'Final result')

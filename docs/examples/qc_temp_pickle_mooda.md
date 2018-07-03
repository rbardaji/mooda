# Quality Control Flag generation in temperature time series from a pickle file

In this example, we are going to analyze a time series of water temperature to know what data seems to be good or bad. We will generate the QC flags of our time series that is saved in a pickle file. We are going to use the MOODA app.

The pickle file is placed into the [example_data](https://github.com/rbardaji/oceanobs/tree/master/docs/example_data) folder, with the name "bad_temp.pkl."

Customarily, we open MOODA from a terminal just writing "mooda":

```bash
> mooda
```

Now we load the pickle file. Click on **File->Open** and look for the file. You should select **"*.pkl"** to view the pickle files (see Figure 1).

![Opening the file](../img/examples/mooda/open_bad_Temp.PNG)

Figure 1: Selection of *.pkl files

The file contains the parameter "seawater temperature" with the name "TEMP." Figure 2 shows the result, where we see a bar chart that indicates that the time series is composed of a parameter called TEMP, which contains more than 40,000 values with QC Flag = 0. In our case, this means that no QC test has been passed.

![Main window with pickle file](../img/examples/mooda/bad_temp_opened.PNG)

Figure 2: Main window

We are going to see the time series in relation with the QC flags. Click on **QC of the parameter**, select the **TEMP** parameter and then click on the **Plot** button. Again, Figure 3 shows that the time series only contains data with the flag of QC = 0.

![TEMP with QC=0](../img/examples/mooda/temp_qc_with_errors_mooda.PNG)

Figure 3: Graph of time series in relation to the QC flags.

Now we are going to pass the QC tests. Click on Data-> QC-> Preferences to see the options of the QC tests.
First, we will set all flags to 0. This step would not be necessary since the flags are already at 0.
Then, we will set the not-passed-value of the test range to 4. In the same way, we assign the value 3 to the Flat Test and 2 to the Spike Test.
Finally, if after passing the tests, flags follow 0, it means that values are correct and we will change them from 0 to 1.
Click Apply and wait for the data to be processed. Figure 4 shows the result, where a spike and an out-of-range value was detected. Mooda also identified two zones with flat values. The bar chart shows the number of values that are in each QC Flag. The counts for the QC Flags 2 and 4 does not appear in the graph due to the zoom settings.

![TEMP with QC tests](../img/examples/mooda/temp_qc_with_errors_test_mooda.PNG)

Figure 4: Time series after QC tests.

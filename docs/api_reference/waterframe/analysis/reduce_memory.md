# WaterFrame.reduce_memory(*inplace*=*True*)

## Reference

Data in a WaterFrame is saved in a pandas DataFrame. By default, the obtained dataset can be very heavy in memory because column types of the pandas DataFrame are defined to accept heavy value types. This method redefine the column types ad typically reduced the dataset size in memory by 30% - 50%. Ref: https://www.kaggle.com/arjanso/reducing-dataframe-memory-size-by-65

### Parameters

* inplace: If false, the method will return a new WaterFrame. Otherwise, it returns True (bool)

### Returns

* True or a new WaterFrame

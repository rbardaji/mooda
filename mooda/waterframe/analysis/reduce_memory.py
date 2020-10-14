""" Implementation of WaterFrame.reduce_memory() """
import numpy as np


def reduce_memory(self, inplace=True):
    """
    Data in a WaterFrame is saved in a pandas DataFrame. By default, the obtained dataset can be
    very heavy in memory because column types of the pandas DataFrame are defined to accept heavy
    value types. This method redefine the column types ad typically reduced the dataset size in
    memory by 30% - 50%.
    Ref: https://www.kaggle.com/arjanso/reducing-dataframe-memory-size-by-65

    Parameters
    ----------
        inplace: bool
            If false, the method will return a new WaterFrame. Otherwise, it returns True
    """

    def reduce_mem_usage(props):

        NAlist = [] # Keeps track of columns that have missing values filled in. 
        for col in props.columns:
            if props[col].dtype != object:  # Exclude strings
                
                # make variables for Int, max and min
                IsInt = False
                mx = props[col].max()
                mn = props[col].min()
                    
                # test if column can be converted to an integer
                asint = props[col].fillna(0).astype(np.int64)
                result = (props[col] - asint)
                result = result.sum()
                if result > -0.01 and result < 0.01:
                    IsInt = True

                try:
                    # Make Integer/unsigned Integer datatypes
                    if IsInt:
                        if mn >= 0:
                            if mx < 255:
                                props[col] = props[col].astype(np.uint8)
                            elif mx < 65535:
                                props[col] = props[col].astype(np.uint16)
                            elif mx < 4294967295:
                                props[col] = props[col].astype(np.uint32)
                            else:
                                props[col] = props[col].astype(np.uint64)
                        else:
                            if mn > np.iinfo(np.int8).min and mx < np.iinfo(np.int8).max:
                                props[col] = props[col].astype(np.int8)
                            elif mn > np.iinfo(np.int16).min and mx < np.iinfo(np.int16).max:
                                props[col] = props[col].astype(np.int16)
                            elif mn > np.iinfo(np.int32).min and mx < np.iinfo(np.int32).max:
                                props[col] = props[col].astype(np.int32)
                            elif mn > np.iinfo(np.int64).min and mx < np.iinfo(np.int64).max:
                                props[col] = props[col].astype(np.int64)    
                    
                    # Make float datatypes 32 bit
                    else:
                        props[col] = props[col].astype(np.float32)
                except ValueError:
                    # There are nans
                    props[col] = props[col].astype(np.float32)

        return props, NAlist

    df = self.data.copy()
    df, _ = reduce_mem_usage(df)

    if inplace:
        self.data = df.copy()
    else:
        wf = self.copy()
        wf.data = df.copy()
        return wf

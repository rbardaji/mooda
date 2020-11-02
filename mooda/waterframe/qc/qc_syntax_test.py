""" Implementation of wf.qc_syntax_test() """

def qc_syntax_test(self):
    """
    It verifies that wf.data contains the recomentated data structure to pass
    the rest of the QC test. Each parameter (for example, TEMP) and each index
    (for example, TIME) must have a column with the flags of the values
    (for example, TEMP_QC and TIME_QC).

    Returns
    -------
        success: bool
            The test has been successfully passed.
    """
    # Get all columns and indices
    all_columns = list(self.data.keys())
    all_columns += list(self.data.index.names)
    # Get only the names without _QC
    columns_no_qc = [column_name for column_name in all_columns if '_QC' not in column_name]

    success = True
    
    for column_no_qc in columns_no_qc:
        if f'{column_no_qc}_QC' not in all_columns:
            success = False

    return success

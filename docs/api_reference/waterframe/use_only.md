# WaterFrame.use_only(*parameters*=None, *flags*=*None*, *dropnan*=*False*)

Drop all parameters not presented in the input list with QC flags different than given in the input flags.

## Parameters

    parameters: list of str, str, optional
        Parameter to save in the WaterFrame.
    flags: list of int, int, None, optional
        QC Flag of the parameter to save.
    dropnan: Bool, optional
        Drop all lines of self.data that contain a nan in any of their columns.

## Returns

    True: bool
        The operations is successful.

Return to the [WaterFrame Index](index_waterframe.md).

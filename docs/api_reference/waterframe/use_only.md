# WaterFrame.use_only(*parameters*=None, *flags*=*None*, *dropnan*=*False*)

Drop all parameters not presented in the input list with QC flags different than given in the input flags.

Parameters | Description | Type
--- | --- | ---
parameters | Parameters to save in the WaterFrame. If parameters is None, all parameters will be used.| list of str, str, None
flags | QC Flag of the parameter to save. | list of int, int, None
dropnan | Drop all lines of self.data that contain a nan in any of their columns. | Bool

Return to the [WaterFrame Index](index_waterframe.md).

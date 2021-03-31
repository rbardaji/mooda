# Enhenced QC

Key | Entry Term | Abbreviated term | Term definition
--- | --- | --- | ---
0 | no quality control | none | No quality control procedures have been applied to the data value. This is the initial status for all data values entering the working archive.
1 | good value | good | Good quality data value that is not part of any identified malfunction and has been verified as consistent with real phenomena during the quality control process.
2 | probably good value | probably_good | Data value that is probably consistent with real phenomena but this is unconfirmed or data value forming part of a malfunction that is considered too 
small to affect the overall quality of the data object of 
which it is a part.
3 | probably bad value | probably_bad | Data value recognised as unusual during quality control that forms part of a feature that is probably inconsistent with real phenomena.
4 | bad value | bad | An obviously erroneous data value.
5 | changed value | changed | Data value adjusted during quality control. Best practice strongly recommends that the value before the change be preserved in the data or its accompanying metadata.
6 | value below detection | DB | The level of the measured phenomenon was too small to be quantified by the technique employed to measure it. The accompanying value is the detection limit for the technique or zero if that value is unknown.
7 | value in excess | excess | The level of the measured phenomenon was too large to be quantified by the technique employed to measure it. The accompanying value is the measurement limit 
for the technique.
8 | interpolated value | interpolated | This value has been derived by interpolation from other values in the data object.
9 | missing value | missing | The data value is missing. Any accompanying value will be a magic number representing absent data.
A | value phenomenon uncertain | ID_uncertain | There is uncertainty in the description of the measured phenomenon associated with the value such as chemical species or biological entity.

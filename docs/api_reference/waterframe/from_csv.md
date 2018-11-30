# from_csv(*path*, *metadata*=*None*, *meaning*=*None*, ***kwds*)

From mooda v0.2.0.

It reads data from a CSV vile.

It uses the pandas.read_csv(). All parameters of read_csv() can be input here.

Parameters | Description | Type
--- | --- | ---
path | Path of the CSV file. | string
metadata | Metadata dictionary. | dictionary
meaning | Meaning dictionary. | dictionary
**kwds | Meaning All arguments from pandas.read_csv(). | arguments

Returns | Description | Type
--- | --- | ---
True |Operation successful. | bool

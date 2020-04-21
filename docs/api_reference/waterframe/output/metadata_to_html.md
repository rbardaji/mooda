# WaterFrame.metadata_to_html(*filename*=*None*, *logo_link*=*None*, *footer_text*=*None*)

## Reference

Make a html file with the metadata information.

## Parameters

* filename: Filename and path of the html file. If filename is None, the file will be saved in the root folder with the name of the metadata['id']. (str)
* logo_link: URL with the logo to be placed on the medatada file. (str)
* footer_text: Text to be placced on the footer of the html file. (str)

## Returns

* filename: Name of the html file. (str)

## Example

To reproduce the example, download the NetCDF file [MO_TS_MO_OBSEA_201402.nc](http://data.emso.eu/files/emso/obsea/mo/ts/2014/MO_TS_MO_OBSEA_201402.nc) and save it in the same python script folder.

```python
import mooda as md

path_netcdf = 'MO_TS_MO_OBSEA_201402.nc'  # Path of the NetCDF file

wf = md.read_nc_emodnet(path_netcdf)

logo_link = 'http://data.emso.eu/img/logo/logo-EMSO-ERIC.png'
footer_text = 'Disclaimer: EMSO ERIC makes no guarantee of the quality, reliability, ' \
    'usability, availability, or suitability of any EMSO ERIC data for any particular purpose. ' \
    'Users assume all risks and liabilities, direct or indirect, associated with any use of EMSO ' \
    'ERIC data (http://emso.eu/privacy-policy/).'

metadata_path = wf.metadata_to_html(logo_link=logo_link, footer_text=footer_text)
print(metadata_path)
```

Output:

```shell
MO_TS_MO_OBSEA_201402.html
```

Screenshot of the metadata html:

![OBSEA metadata][obsea-metadata]

Return to [mooda.WaterFrame](../waterframe.md).

[obsea-metadata]: ../img_waterframe/metadata-html-obsea.png

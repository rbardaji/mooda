** oceanobs is a Python package that provides a wide range of tools to analyze data from marine observatories, including procedures for feature extraction, quality control generation, filtering methods and content visualization.**

Check the documentation on [oceanobs.readthedocs.io](http://oceanobs.readthedocs.io/).

This work is performed in the framework of the European Multidisciplinary Seafloor and Water-Column Observatory development ([EMSOdev](http://www.emsodev.eu/)).

# Why use *oceanobs*?

The main problem when analyzing marine data from different research infrastructures is th lack of a unique data format and nomenclature. Regardless of the type of file i.e., CSV, NetCDF, HDF, XML, names that describe measurements (vocabularies) may vary depending on the provider/source. Although there is some effort to produce and provide documentation with standard vocabulary, until now, no consensus has been reached concerning the use of a common nomenclature to describe the measurements. For example, water temperature values can be listed as ‘TEMP,’ ‘temp,’ ‘sea_temp,’ or ‘temperature.’

Another problem with the marine data is the Quality Control (QC). Some platforms offer to download a processed dataset with QC Flags, but others, like [EMSODev](http://www.emsodev.eu), only give the option to download raw data. In some occasions, for an environmental scientist, it is hard to discriminate if data is adequate for a particular study.

*oceanobs* offers the possibility to open data in different formats and vocabularies. With *oceanobs*, the original data are translated into a WaterFrame object. Thus, all data analysis functions can be used independently of the data source format. 

Some of the features that *oceanobs* offers are:

* Open data in different formats;
* Download data from [EGIMs](http://www.emsodev.eu);
* Generation of QC Flags;
* Data filtering methods;
* Complex visualization tools;
* Summary reports of data;
* Specific data analysis functions for various scientific disciplines;

# Compatible data input

The compatible input data are from the following observatories:

* [EMSO](http://www.emso-eu.org/) Generic Instrument Module ([EGIM](http://www.emsodev.eu)) in pickle file format.

* [OBSEA](http://www.upc.edu/cdsarti/OBSEA/) in text files with CSV format.

* [EMODNET](http://www.emodnet-physics.eu/Map/) and [JERICO](http://www.jerico-ri.eu/data-access/) in [NetCDF](http://www.oceansites.org/data/) format.

# No knowledge of Python is needed!

*oceanobs* contains a Graphical User Interface (GUI) called Module for Ocean Observatory Data Analysis (**MOODA**).

![MOODA screenshot](/docs/img/home/mooda_screenshot.png)

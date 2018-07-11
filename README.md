# MOODA - Module for Ocean Observatory Data Analysis

Mooda is a python package designed mainly for oceanographers and marine science students. It is based on a power scripting system for:

* direct data access;
* data filtering methods;
* complex visualization tools;
* quality control generation;
* specific data analysis tools for different scientific disciplines.

The package is designed to be open, adaptable and scalable allowing future contributions from researchers and developers from all the marine science disciplines.

This work is performed in the framework of the European Multidisciplinary Seafloor and Water-Column Observatory development ([EMSOdev](http://www.emsodev.eu/)).

Check the documentation on [mooda.readthedocs.io](http://mooda.readthedocs.io/).

## Why use *mooda*

The main problem when analyzing marine data from different research infrastructures is th lack of a unique data format and nomenclature. Regardless of the type of file i.e., CSV, NetCDF, HDF, XML, names that describe measurements (vocabularies) may vary depending on the provider/source. Although there is some effort to produce and provide documentation with standard vocabulary, until now, no consensus has been reached concerning the use of a common nomenclature to describe the measurements. For example, water temperature values can be listed as ‘TEMP,’ ‘temp,’ ‘sea_temp,’ or ‘temperature.’

Another problem with the marine data is the Quality Control (QC). Some platforms offer to download a processed data set with QC Flags, but others, like [EMSODev](http://www.emsodev.eu), only give the option to download raw data. In some occasions, for an environmental scientist, it is hard to discriminate if data is adequate for a particular study.

*Mooda* offers the possibility to read data in different formats and vocabularies. Source data are translated into an internal format, a WaterFrame. Thus, all data analysis functions can be used independently of the data source format.

## Compatible data input

For the moment, the compatible source data can be from the following observatories:

* [EMSO](http://www.emso-eu.org/) Generic Instrument Module ([EGIM](http://www.emsodev.eu)).
* [JERICO](http://www.jerico-ri.eu/data-access/) in NetCDF.
* Mooring time series from [EMODNET-physics](http://www.emodnet-physics.eu/Map/) in NetCDF.

## No knowledge of Python is needed

*Mooda* can be executed through a graphical interface with which a large part of the implemented functions can be performed.

![MOODA screenshot](/docs/img/home/mooda_screenshot.png)

## More information

* [Git Repository Structure](/docs/github_struct.md): Describes the git repository structure and branching model used for the mooda project.
* [Package Overview](/docs/package.md): The Python package is located in the [mooda folder](/mooda). This document describes how the python modules within the package have been structured.
* [Installation](/docs/installation.md): Step by step manual of the installation of mooda. The document contains an installation guide for people without python knowledge but also for people who have already used python before.
* [API reference](/docs/api.md): Explanation of the modules and functions of the package.
* [Examples](/docs/examples/index_examples.md): Set of examples to use mooda by writing python code or running MOODA.
* [Version log](/docs/news.md)
* [License](LICENSE)

# GitHub repository structure

If you are not a regular user of GitHub, it is possible that the structure of data and directories in this repository is confusing. For this reason, we will explain that it contains each folder of the project and its most essential files.

The GitHub repository of the mooda project is structured as follows:

```bash
    mooda
    ├─ docs
    |   ├─ example_data
    |   ├─ examples
    |   └─ img
    |       ├─ examples
    |       |   ├─ emso
    |       |   ├─ map
    |       |   ├─ mooda
    |       |   ├─ netcdf
    |       |   └─ pickle
    |       ├─ home
    |       └─ package
    ├─ mooda
    |   ├─ access
    |   └─ app
    |       └─ mooda_gui
    ├─ other codes
    └─ tests
        └─ data
```

Most of the files that are in the root contain code or information specific to git. If you do not want to clone the project or use a git client, they are not necessary files for you. However, we describe them below:

* [.gitignore](https://github.com/rbardaji/mooda/blob/master/.gitignore): In the process to sync your local git directory with the GitHub repository, files are usually built artifacts, and machine-generated data should otherwise not be uploaded. In this file, you can find the code to ignore this type of files.
* [LICENSE](https://github.com/rbardaji/mooda/blob/master/LICENSE): Public repositories on GitHub are often used to share open source software. We use an MIT License.
* [MANIFEST.in](https://github.com/rbardaji/mooda/blob/master/MANIFEST.in): It is used to collect all the files that will go into the final installer.
* [README.md](https://github.com/rbardaji/mooda/blob/master/README.md): Contains the text that you see on the repository [home page](https://github.com/rbardaji/mooda).
* [mkdocs.yml](https://github.com/rbardaji/mooda/blob/master/mkdocs.yml): Sets the theme and theme specific configuration of the [documentation site](https://mooda.readthedocs.io/).
* [requirements-access-egim.txt](requirements-access-egim.txt): List of required python libraries to execute the module mooda.access.egim.py.
* [requirements-app-mooda_gui.txt](https://github.com/rbardaji/mooda/blob/master/requirements-app-mooda_gui.txt): List of required python libraries to execute the package mooda.app.mooda_gui.
* [requirements-waterframe.txt](https://github.com/rbardaji/mooda/blob/master/requirements-waterframe.txt): List of required python libraries to execute the module mooda.waterframe.py.
* [setup.cfg](https://github.com/rbardaji/mooda/blob/master/setup.cfg): It contains package metadata.
* [setup.py](https://github.com/rbardaji/mooda/blob/master/setup.py): It is the python code to install the package into a python environment.

The directories contain the following information:

* [docs](https://github.com/rbardaji/mooda/tree/master/docs): It contains the texts that are displayed on the [documentation site](https://mooda.readthedocs.io/).
* [docs/example_data](https://github.com/rbardaji/mooda/tree/master/docs/example_data): It contains the data files used in the example documentation.
* [docs/examples](https://github.com/rbardaji/mooda/tree/master/docs/examples): It contains the texts of the example documentation.
* [docs/img](https://github.com/rbardaji/mooda/tree/master/docs/img): It contains the images of the documentation.
* [docs/img/examples](../docs/img/examples): It contains the images of the example documentation.
* [docs/img/home](https://github.com/rbardaji/mooda/tree/master/docs/img/home): It contains the images of the main page documentation.
* [docs/img/package](https://github.com/rbardaji/mooda/tree/master/docs/img/package): It contains the images of the package overview documentation.
* [mooda](https://github.com/rbardaji/mooda): **It contains the mooda python package.**
* [tests](https://github.com/rbardaji/mooda/tree/master/tests): It contains the python code to test the mooda package. We are not using any standard to check mooda. We write our test routines.
* [other_codes](https://github.com/rbardaji/mooda/tree/master/other_codes): It contains a set of python scripts that uses the mooda package.

# GitHub repository structure

If you are not a regular user of GitHub, it is possible that the structure of data and directories in this repository is confusing. For this reason, we will explain that it contains each folder of the project and its most essential files.

The GitHub repository of the oceanobs project is structured as follows:

    oceanobs
    ├─ .vscode
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
    ├─ oceanobs
    |   ├─ access
    |   └─ app
    |       └─ mooda
    ├─ other codes
    └─ tests
        └─ data

Most of the files that are in the root contain code or information specific to git. If you do not want to clone the project or use a git client, they are not necessary files for you. However, we describe them below:

* [.gitignore](.gitignore): In the process to sync your local git directory with the GitHub repository, files are usually built artifacts, and machine-generated data should otherwise not be uploaded. In this file, you can find the code to ignore this type of files.
* [LICENSE](LICENSE): Public repositories on GitHub are often used to share open source software. We use an MIT License.
* [MANIFEST.in](MANIFEST.in): It is used to collect all the files that will go into the final installer.
* [README.md](README.md): Contains the text that you see on the repository [home page](https://github.com/rbardaji/oceanobs).
* [mkdocs.yml](mkdocs.yml): Sets the theme and theme specific configuration of the [documentation site](https://oceanobs.readthedocs.io/).
* [requirements-access-egim.txt](requirements-access-egim.txt): List of required python libraries to execute the module oceanobs.access.egim.py.
* [requirements-app-mooda.txt](requirements-app-mooda.txt): List of required python libraries to execute the package oceanobs.app.mooda.
* [requirements-waterframe.txt](requirements-waterframe.txt): List of required python libraries to execute the module oceanobs.waterframe.py.
* [setup.cfg](setup.cfg): It contains package metadata.
* [setup.py](setup.py): It is the python code to install the package into a python environment.

The directories contain the following information:

* [.vscode](../.vscode): If you use the oceanobs package with the Visual Studio Code editor, maybe this folder could be useful. Here, you can find the settings that we use.
* [docs](../docs): It contains the texts that are displayed on the [documentation site](https://oceanobs.readthedocs.io/).
* [docs/example_data](../docs/example_data): It contains the data files used in the example documentation.
* [docs/examples](../docs/examples): It contains the texts of the example documentation.
* [docs/img](../docs/img): It contains the images of the documentation.
* [docs/img/examples](../docs/img/examples): It contains the images of the example documentation.
* [docs/img/home](../docs/img/home): It contains the images of the main page documentation.
* [docs/img/package](../docs/img/package): It contains the images of the package overview documentation.
* [oceanobs](../oceanobs): **It contains the oceanobs python package.**
* [tests](../tests): It contains the python code to test the oceanobs package. We are not using any standard to check oceanobs. We write our test routines.
* [other_codes](../other_codes): It contains a set of python scripts that uses the oceanobs package.

Return to [main page](../README.md).

# GitHub repository structure

If you are not a regular user of GitHub, it is possible that the structure of data and directories in this repository is confusing. For this reason, we will explain that it contains each folder of the project and its most essential files.

The GitHub repository of the mooda project is structured as follows:

```bash
    mooda
    ├─ docs
    ├─ mooda
    |   └─ access
    └─ other codes
```

Most of the files that are in the root contain specific code for the configuration of the GitHub directory. If you do not want to clone the project or use a git client, they are not necessary files for you. However, we describe them below:

* [.gitignore](https://github.com/rbardaji/mooda/blob/master/.gitignore): In the process to sync your local git directory with the GitHub repository, files are usually built artifacts, and machine-generated data should otherwise not be uploaded. In this file, you can find the code to ignore this type of files.
* [LICENSE](https://github.com/rbardaji/mooda/blob/master/LICENSE): Public repositories on GitHub are often used to share open source software. We use an MIT License.
* [MANIFEST.in](https://github.com/rbardaji/mooda/blob/master/MANIFEST.in): It is used to collect all the files that will go into the final installer.
* [README.md](https://github.com/rbardaji/mooda/blob/master/README.md): Contains the text that you see on the repository [home page](https://github.com/rbardaji/mooda).
* [requirements-access-egim.txt](requirements-access-egim.txt): List of required python libraries to execute the module mooda.access.egim.py.
* [requirements-waterframe.txt](https://github.com/rbardaji/mooda/blob/master/requirements-waterframe.txt): List of required python libraries to execute the module mooda.waterframe.py.
* [setup.cfg](https://github.com/rbardaji/mooda/blob/master/setup.cfg): It contains package metadata.
* [setup.py](https://github.com/rbardaji/mooda/blob/master/setup.py): It is the python code to install the package into a python environment.

The directories contain the following information:

* [docs](https://github.com/rbardaji/mooda/tree/master/docs): It contains the mooda documentation.
* [mooda](https://github.com/rbardaji/mooda): **It contains the mooda python package.**
* [other_codes](https://github.com/rbardaji/mooda/tree/master/other_codes): It contains a set of python scripts that uses the mooda package.

Return to the [Docs Index](../index_docs.md).

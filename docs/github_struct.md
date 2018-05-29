# GitHub repository structure

If you are not a regular user of GitHub, it is possible that the structure of data and directories in this repository is confusing. For this reason, we will explain that it contains each folder of the project and its most essential files.

The GitHub repository of the oceanobs project is structured as follows:

<pre><code>oceanobs
├─ .vscode
├─ docs
├─ oceanobs
|   ├─ access
|   └─ app
|       └─ mooda
└─ tests
    └─ data
</code></pre>

Most of the files that are in the root contain code or information specific to git. If you do not want to clone the project or use a git client, they are not necessary files for you. However, we describe them below:

* [.gitignore](.gitignore): In the process to sync your local git directory with the GitHub repository, files are usually built artifacts, and machine-generated data should otherwise not be uploaded. In this file, you can find the code to ignore this type of files.
* [LICENSE](LICENSE): Public repositories on GitHub are often used to share open source software. We use an MIT License.
* [README.md](README.md): Contains the text that you see on the repository [home page](https://github.com/rbardaji/oceanobs).
* [mkdocs.yml](mkdocs.yml): Sets the theme and theme specific configuration of the [documentation site](https://oceanobs.readthedocs.io/).

The directories contain the following information:

* [.vscode](../.vscode): If you use the oceanobs package with the Visual Studio Code editor, maybe this folder could be useful. Here, you can find the settings that we use.
* [docs](../docs): It contains the texts and images that are displayed on the [documentation site](https://oceanobs.readthedocs.io/).
* [oceanobs](../oceanobs): **It contains the oceanobs python package.**
* [tests](../docs): It contains the python code to test the oceanobs package. We are not using any standard to check oceanobs. We write our test routines.

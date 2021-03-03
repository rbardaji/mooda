# Directory: rbardaji/mooda

* **.github**: This folder hosts files that are used by the GitHub platform itself. In our case, this folder only contains the form templates to report bugs or request new functionalities, but in other repositories, this folder may contain more files.
* [**docs**](rbardaji_mooda_docs.md): This folder contains the Markdown files for mooda documentation.
* [**mooda**](rbardaji_mooda_mooda.md): This is the most important folder in the repository and contains the code for the mooda library.
* .gitignore: A gitignore file specifies intentionally untracked files that Git should ignore. Files already tracked by Git are not affected.
* LICENSE: File to define all license details. We use the MIT license.
* MANIFEST.in: Code that allows to include files in source distributions. When building a source distribution for the package by default, only a minimal set of files are included. We want to include extra files in the source distribution, such as the requirements file (requirements.txt), that the setup file (setup.py) need to instal all dependencies of the package. [more info](https://packaging.python.org/guides/using-manifest-in/).
* README.md: This Markdown documentation file is shown as "home" documentation/page of the GitHub repository and the GitHub page environment.
* _config.yml: GitHub Pages are public webpages hosted and easily published through GitHub. The quickest way to get up and running is by using the Jekyll Theme Chooser to load a pre-made theme. This file contains the settings required to generate a GitHub-pages.
* requirements.txt: List of python packages required to run mooda successfully.
* setup.py: The setup.py file contains information about mooda that PyPi needs to publish install the package, like its name, a description, the requeriments, the current version etc.

Return to [index](../index_docs.md).

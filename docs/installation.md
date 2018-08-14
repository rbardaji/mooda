# Installation

Documentation under construction.

For the moment, only the latest version of oceanobs can be [installed from source](#Installing_from_source).

## Python version support

Officially [Python](https://www.python.org/downloads/) >= 3.4.

## Installing with pip

You can install mooda via pip with the following command:

```bat
pip install mooda
```

If you want to use the PlotMap object, you also need to download the *basemap* library. There are many ways to install the basemap library. The easiest is through conda.

```bat
conda install -c conda-forge basemap
```

## Installing from source

There are many ways to clone or download the source code from [GitHub](https://github.com/rbardaji/mooda) on your computer. If you do not have a git client, you can press the *Download ZIP* button, which is located under the *Clone or Download* drop-down of the [GitHub page](https://github.com/rbardaji/mooda).

Now, you only need to install the package directly from the downloaded folder. Go to the downloaded folder and write the following instruction in a terminal.

```bat
python setup.py install
```

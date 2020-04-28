---
layout: post
title: "Installation of CAVIAR"
category: using-caviar
author: jr
short-description: How to install CAVIAR?
---

-----

### Downloading and installing the software  
The best way to get CAVIAR is to install the Anaconda package manager for Python.
Start by downloading the Python 3.x Anaconda installer on the [--> Anaconda website <--](https://www.anaconda.com/distribution/) and install it.

Once Anaconda is installed, create a new environment in your terminal for CAVIAR:
```conda create -n caviar -c jr-marchand caviar ```

### Activating the environment  
Activate your environment (*always activate it* in the terminal you're lauching CAVIAR from):
```conda activate caviar ```

And that is it! CAVIAR is accessible with the ```caviar``` command, and the user interface via the ```caviar-gui``` command.

### Notes  

- PyMOL and visualization: if you want to use the PyMOL functionalities for vizualising cavities in the GUI, please make sure that you have a PyMOL executable accessible as ```pymol``` in the command line.
In case you do not have PyMOL yet, you can install a version (accessible in the caviar conda environment) with:
> ```conda install -n caviar -c schrodinger pymol```  


- Architecture: CAVIAR is fully written in python and should be compatible with any OS. However, it was developped on a Linux system, and is restricted to the limitations of the external libraries it relies on (especially PyQT for the GUI). We expect it to work on any Linux or MacOS architecture supporting conda, but it does not function yet on Windows.

- The source code is also available on [--> GitHub <--](https://github.com/jr-marchand/CAVIAR) and can be installed locally, providing that the dependencies are present in the active python environment.
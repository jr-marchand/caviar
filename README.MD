<p align="center">
	<img src="https://github.com/jr-marchand/caviar/blob/master/docs/assets/toc.png" alt="CAVIAR banner" width="500"/>
</p>

## CAVIAR - CAVity Identification And Rationalization -- GUI and command line tool

[![ChemRxiv shield](https://img.shields.io/badge/ChemRxiv-10.26434%2Fchemrxiv.12806819-red)](https://doi.org/10.26434/chemrxiv.12806819)


CAVIAR is an open source tool for protein cavity identification and rationalization, written in python and available as command line and as a GUI. It comprises a subcavity segmentation algorithm that produces meaningful decomposition of cavities, fully focused on the protein structure and agnostic of any ligand information. These subcavities reproduce subpockets as defined empirically with medicinal chemistry knowledge.

### Website and manual

[https://jr-marchand.github.io/caviar](https://jr-marchand.github.io/caviar) contains extended information about installation, usage and news/changelog.   


### Main functionalities

1. Advanced parsing of structure files: PDB file format (including metadata retrieval from header), mmCIF files from cryoEM, DCD trajectory files from molecular dynamics simulations.
2. Selection of interesting objects (one or more specific chains)
3. Fast and reliable identification of protein cavities
4. Decomposition of cavities into subpockets, which may be used for engineering potency or selectivity of a ligand
5. Printing out of tables summing up information of cavities and subcavities (hydrophobicity, size, pharmacophore types...)
6. Outputing files containing the cavities/subcavities in a simple PDB format, alongside pymol pml files to visualize the cavities/subcavities painlessly.

Current development efforts are focused on:  
 - automatic comparison of cavities, similarity estimation  
 - storage in database format (SQL/postgresql)  
 - ... let's keep some surprises for the future :)  

### How to install

Detailed information on [dedicated website](https://jr-marchand.github.io/caviar/using-caviar/installation).
This package is hosted on anaconda.org. To install it in a new environment, simply run:  
```conda create -n caviar -c jr-marchand caviar```  

To install it manually from the git repository:   
Create a virtual environement (see the documentation on [the Python Packaging authority website](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/))  
Install the necessary dependencies (cf conda.recipe/meta.yaml), most likely from [PyPI](https://pypi.org/), [User Guide](https://packaging.python.org/)  
With the virtual environement activated: ```python setup.py install```   
/!\ Check that you have the correct dependencies/libraries  
cf conda.recipe/meta.yaml, requirements section /!\  

### How to use

Detailed information on the dedicated website [for the GUI](https://jr-marchand.github.io/caviar/using-caviar/caviar-gui) and [for the command line use](https://jr-marchand.github.io/caviar/using-caviar/caviar-cmdline).

- GUI  
Run ```caviar_gui``` from the command line  
The first window that will open is to give the PDB file / PDB code to download from the RCSB PDB. You can also select one or more chains to work on, and decide whether to open pymol with the results and the coloring scheme.  
Once you click the run button, a second window will open, for subcavity decomposition. You can either decompose all cavities detected earlier, or choose one. Same remark for pymol.  
  
- Command line tool  
The python command line tool is accessible via the command ```caviar```. More information with the -h option  

### Credits

Project led by Jean-Rémy Marchand  
Collaboration with **Finton Sirockin**, Peter Ertl and Bernard Pirard  


This package relies on external open source software and libraries:  
* python 3   
* pyparse and configargparse for arguments parsing  
* scipy, numpy, networkx for cavity identification  
* scikit-image for subcavity decomposition  
* scikit-learn for ligandability predictions  
* PyQt5 for the GUI   
* Pandas for storing and exporting descriptors  

File parsing is based on the parsers provided by the [ProDy team](https://github.com/prody/ProDy) a huge thanks for their amazing work!
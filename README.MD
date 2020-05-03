# CAVIAR

CAVity Identification And Rationalization -- GUI and command line tool

CAVIAR is a new open source tool for protein cavity identification and rationalization, written in python and available as command line and as a GUI. It comprises a subcavity segmentation algorithm that produces meaningful decomposition of cavities, fully focused on the protein structure and agnostic of any ligand information. 

### Website and manual

https://jr-marchand.github.io/caviar contains extended information about installation, usage, and an extended manual.   


## General information

This project aims at creating a python platform to:
 - Download/parse PDB files and fetch as much information from the header as possible
 - Select interesting protein chains with advanced automatic selection (eg, longest protein chain and contacting chains with more than X contacts, keep metal, well structured structural waters)
 - Identify cavities (grid based algorithm based on buriedness)
 - Decompose them in subcavities and print their properties
 - Much more to come!

## How to install

This package is hosted on anaconda.org

To install it, simply run:
conda -c jr-marchand caviar

To install it in a brand new environment:

conda create -n caviar -c jr-marchand caviar

To install it locally from the git repository:

python setup.py install
/!\ Check that you have the correct dependencies/libraries
cf conda.recipe/meta.yaml, requirements section
/!\ 

## How to use

- GUI

Run "caviar_gui" from the command line 

The first window that will open is to give the PDB file / PDB code to download from the RCSB PDB. You can also select one or more chains to work on, and decide whether to open pymol with the results and the coloring scheme.

Once you click the run button, a second window will open, for subcavity decomposition. You can either decompose all cavities detected earlier, or choose one. Same remark for pymol.

- Command line tool

The python command line tool is accessible via the command "caviar". More information with the -h option

## Credits

Project by Jean-Rémy Marchand, initiated by Joakim Deheuvels (proof of concept)

Mentoring from Finton Sirockin

Weekly discussions with Peter Ertl and Bernard Pirard


This package relies on open source software:
* python 3 
* pyparse for arguments parsing
* scipy, numpy, networkx for cavity identification
* skimage (scikit-image) for subcavity decomposition
* sklearn for ligandability predictions
* PyQt5 for the GUI 

# CAVIAR-GUI

CAVity Identification And Rationalization GUI

## General information

This is the user interface that relates to the Caviar / Cavitome project

This project aims at creating a python plateform to:
 - Download/parse PDB files and fetch as much information from the header as possible
 - Select interesting protein chains with advanced automatic selection (eg, longest protein chain and contacting chains with more than X contacts, keep metal, well structured structural waters)
 - Identify cavities (grid based algorithm based on buriedness)
 - Decompose them in subcavities and print their properties
 - Much more to come!

## How to install

This package is hosted on anaconda.org

To install it, simply run:
conda -c jr-marchand caviar_gui

To install it in a brand new environment:

conda create -n myenv -c jr-marchand python=3.7 caviar_gui

To install it locally from the git repository:

python setup.py install
/!\ Check that you have the correct dependencies/libraries
cf conda.recipe/meta.yaml, requirements/run section
/!\ 

## How to use

Run "caviar_gui" from the command line 

The first window that will open is to give the PDB file / PDB code to download from the RCSB PDB. You can also select one or more chains to work on, and decide whether to open pymol with the results and the coloring scheme.

Once you click the run button, a second window will open, for subcavity decomposition. You can either decompose all cavities detected earlier, or choose one. Same remark for pymol.


## Credits

Project by Jean-Rémy Marchand, initiated by Joakim Deheuvels (proof of concept)

Mentoring from Finton Sirockin

Weekly discussions with Peter Ertl and Bernard Pirard


This package relies on open source software:
* python 3 (< 3.8)
* pyparse for arguments parsing
* scipy, numpy, networkx for cavity identification
* skimage (scikit-image) for subcavity decomposition
* PyQt5 for the GUI -- restricted to version pyqt 5.9.2


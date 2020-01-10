# -*- coding: utf-8 -*-
"""
This module defines classes and functions to fetch, parse, and write
structural data files, execute structural analysis programs, and to access
and search structural databases, e.g. `ProteinDataBank <http://wwpdb.org>`_.

The code was borrowed and adapted from ProDy: http://prody_parser.csb.pitt.edu

## DELETED functionalities: ##
BLAST
PQR
mmCIF
DSSP
STRIDE
EMD
alignment/comparison
pdbclusters
showProtein

PDB resources
=============

  * :func:`.fetchPDB` - retrieve PDB files
  * :func:`.fetchPDBviaFTP` - download PDB
  * :func:`.fetchPDBviaHTTP` - download PDB files

You can use following functions to manage PDB file resources:

  * :func:`.pathPDBFolder` - local folder for storing PDB files
  * :func:`.pathPDBMirror` - local PDB mirror path
  * :func:`.wwPDBServer` - set wwPDB FTP/HTTP server for downloads

Following functions can be used to handle local PDB files:

  * :func:`.findPDBFiles` - return a dictionary containing files in a path
  * :func:`.iterPDBFilenames` - yield file names in a path or local PDB mirror


Parse/write PDB files
=====================

Following ProDy functions are for parsing and writing :file:`.pdb` files:

  * :func:`.parsePDB` - parse :file:`.pdb` formated file
  * :func:`.parsePDBStream` - parse :file:`.pdb` formated stream
  * :func:`.writePDB` - write :file:`.pdb` formatted file
  * :func:`.writePDBStream`  write :file:`.pdb` formated stream

.. seealso::

   Atom data (coordinates, atom names, residue names, etc.) parsed from
   PDB files are stored in :class:`~.AtomGroup` instances.
   See :mod:`~prody_parser.atomic` module documentation for more details.


Edit structures
===============

Following functions allow editing structures using structural data from PDB
header records:

  * :func:`.assignSecstr` - add secondary structure data from header to atoms
  * :func:`.buildBiomolecules` - build biomolecule from header records


PDB header data
===============

Use the following to parse and access header data in PDB files:

  * :func:`.parsePDBHeader` - parse header data from :file:`.pdb` files
  * :class:`.Chemical` - store PDB chemical (heterogen) component data
  * :class:`.Polymer` - store PDB polymer (macromolecule) component data
  * :class:`.DBRef` - store polymer sequence database reference records

Ligand data
===========

Following function can be used to fetch meta data on PDB ligands:

  * :func:`.fetchPDBLigand` - retrieve ligand from Ligand-Expo

"""

__all__ = []

from . import localpdb
from .localpdb import *
__all__.extend(localpdb.__all__)

from . import wwpdb
from .wwpdb import *
__all__.extend(wwpdb.__all__)

from . import pdbligands
from .pdbligands import *
__all__.extend(pdbligands.__all__)

from . import header
from .header import *
__all__.extend(header.__all__)

from . import pdbfile
from .pdbfile import *
__all__.extend(pdbfile.__all__)

from .pdbfile import PDBParseError


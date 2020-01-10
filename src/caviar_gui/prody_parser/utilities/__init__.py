# -*- coding: utf-8 -*-
"""This module provides utility functions and classes for handling files,
logging, type checking, etc.  Contents of this module are not included in
ProDy namespace, as it is not safe to import them all due to name conflicts.
Required or classes should be imported explicitly, e.g.
``from cavitome_gui.prody_parser.utilities import PackageLogger, openFile``.

Deleted files:
rm catchall.py drawtools.py legacy.py logger.py settings.py 

Package utilities
===============================================================================

  * :class:`.PackageLogger`
  * :class:`.PackageSettings`
  * :func:`.getPackagePath`
  * :func:`.setPackagePath`

Type/Value checkers
===============================================================================

  * :func:`.checkCoords`
  * :func:`.checkWeights`
  * :func:`.checkTypes`

Path/file handling
===============================================================================

  * :func:`.gunzip`
  * :func:`.openFile`
  * :func:`.openDB`
  * :func:`.openSQLite`
  * :func:`.openURL`
  * :func:`.copyFile`
  * :func:`.isExecutable`
  * :func:`.isReadable`
  * :func:`.isWritable`
  * :func:`.makePath`
  * :func:`.relpath`
  * :func:`.which`
  * :func:`.pickle`
  * :func:`.unpickle`
  * :func:`.glob`


Documentation tools
===============================================================================

  * :func:`.joinRepr`
  * :func:`.joinRepr`
  * :func:`.joinTerms`
  * :func:`.tabulate`
  * :func:`.wrapText`


Miscellaneous tools
===============================================================================

  * :func:`.rangeString`
  * :func:`.alnum`
  * :func:`.importLA`
  * :func:`.dictElement`

"""

__all__ = []

from .checkers import *
__all__.extend(checkers.__all__)
from .logger import *
__all__.extend(logger.__all__)
from .settings import *
__all__.extend(settings.__all__)
from .misctools import *
__all__.extend(misctools.__all__)
from .pathtools import *
__all__.extend(pathtools.__all__)
from .doctools import *
__all__.extend(doctools.__all__)

#from . import catchall
#from .catchall import *
#__all__.extend(catchall.__all__)

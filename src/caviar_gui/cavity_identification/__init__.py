# -*- coding: utf-8 -*-
"""This module defines classes and functions to generate the cavities of the protein.

Geometry functionalities
========================
  * :class:`Point` store/work with 3D points
    * :func:`.dist` - Calculates the distance between two points
    * :func:`.in_range` - Determines if two points are within a distance
    * :func:`.direction` - Determines the direction vector between two points
    * :func:`.dist2` - Squared distance

  * :class:`Vector` store/work with vectors
    * :func:`.get_perpendicular` - Calculates the perpendicular vector to 2 vectors
    * :func:`.normalized` - Returns the normalized vector
    * :func:`.angle` - Calculates the angle between two vectors

  * :class:`SetOfPoints` store/work with sets of 3D points (ie, sets of coordinates)
    * :func:`.get_coord_range` - Returns the maximum coordinates of the set
    * :func:`.in_range_set` - Investigates whether a point is within distance of a set of points 
    * :func:`.center` - Determines the mean x,y,z value of a set of points 

"""

__all__ = ['geometry', 'selectchains', 'cavitydetect', 'gridtools']

from . import geometry
from .geometry import *
__all__.extend(geometry.__all__)

from . import selectchains
from .selectchains import *
__all__.extend(selectchains.__all__)

from . import cavitydetect
from .cavitydetect import *
__all__.extend(cavitydetect.__all__)

from . import gridtools
from .gridtools import *
__all__.extend(gridtools.__all__)


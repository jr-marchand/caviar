"""ProDy is a package for Protein Dynamics, Sequence, and Structure Analysis"""

import sys

if sys.version_info[0] == 3:
    if sys.version_info[1] < 4:
        sys.stderr.write('Python 3.4 and older is not supported\n')
        sys.exit()

try:
    import numpy as np
except ImportError:
    raise ImportError('Numpy is a required package for ProDy')
else:
    if tuple(map(int, np.__version__.split('.')[:2])) < (1, 10):
        raise ImportError('Numpy v1.10 or later is required for ProDy')

__all__ = ['confProDy', 'startLogfile', 'closeLogfile', 'plog']

from . import utilities
from .utilities import *
from .utilities import PackageLogger, PackageSettings
from .utilities import getPackagePath, joinRepr, tabulate
__all__.extend(utilities.__all__)
__all__.append('utilities')

LOGGER = PackageLogger('.prody_parser')

SETTINGS = PackageSettings('prody_parser', logger=LOGGER)
SETTINGS.load()

from . import atomic
from .atomic import *
__all__.extend(atomic.__all__)
__all__.append('atomic')

from .atomic import SELECT

from . import proteins
from .proteins import *
__all__.extend(proteins.__all__)
__all__.append('proteins')

from . import measure
from .measure import *
__all__.extend(measure.__all__)
__all__.append('measure')

from caviar import prody_parser
__all__.append('prody_parser')

# default, acceptable values, setter
CONFIGURATION = {
    'backup': (False, None, None),
    'backup_ext': ('.BAK', None, None),
    'auto_show': (False, None, None),
    'ligand_xml_save': (False, None, None),
    'typo_warnings': (True, None, None),
    'check_updates': (0, None, None),
    'auto_secondary': (False, None, None),
    'selection_warning': (True, None, None),
    'verbosity': ('debug', list(utilities.LOGGING_LEVELS),
                  LOGGER._setverbosity),
    'pdb_mirror_path': ('', None, proteins.pathPDBMirror),
    'local_pdb_folder': ('', None, proteins.pathPDBFolder),
}


def confProDy(*args, **kwargs):
    """Configure ProDy."""

    if args:
        values = []
        for option in args:
            try:
                values.append(SETTINGS[option])
            except KeyError:
                raise KeyError('{0:s} is not a valid configuration option'
                               .format(repr(option)))
        if len(values) == 1:
            return values[0]
        else:
            return values

    for option, value in kwargs.items():
        try:
            default, acceptable, setter = CONFIGURATION[option]
        except KeyError:
            raise KeyError('{0:s} is not a valid configuration option'
                           .format(repr(option)))
        else:
            try:
                value = type(default)(value)
            except ValueError:
                raise TypeError('{0:s} must be a {1:s}'
                                .format(option, type(default).__name__))
            if acceptable is not None and value not in acceptable:
                raise ValueError('{0:s} must be one of {1:s}'.format(option,
                                 joinRepr(acceptable, sort=True,
                                          last=', or ')))

            SETTINGS[option] = value
            LOGGER.info('ProDy is configured: {0:s}={1:s}'
                        .format(option, repr(value)))
            SETTINGS.save()
            if setter is not None:
                setter(value)

_keys = list(CONFIGURATION)
_keys.sort()
_vals = []
for _key in _keys:
    default, acceptable, setter = CONFIGURATION[_key]
    try:
        if not setter.func_name.startswith('_'):
            seealso = ' See also :func:`.' + setter.func_name + '`.'
    except AttributeError:
        seealso = ''

    if acceptable is None:
        _vals.append(repr(default) + seealso)
    else:
        _vals.append(repr(default) + ' (' +
                     joinRepr(acceptable, sort=True, last=', or ') + ')' +
                     seealso)
    if _key not in SETTINGS:
        SETTINGS[_key] = default

LOGGER._setverbosity(confProDy('verbosity'))

confProDy.__doc__ += '\n\n' + tabulate(['Option'] + _keys,
                                       ['Default (acceptable values)'] + _vals
                                       ) + """

Usage example::

    confProDy('backup')
    confProDy('backup', 'backup_ext')
    confProDy(backup=True, backup_ext='.bak')
    confProDy(backup_ext='.BAK')"""


def plog(*text):
    """Log *text* using ProDy logger at log level info.  Multiple arguments
    are accepted.  Each argument will be converted to string and joined using
    a white space as delimiter."""

    LOGGER.info(' '.join([str(s) for s in text]))


def startLogfile(filename, **kwargs):

    LOGGER.start(filename, **kwargs)

startLogfile.__doc__ = LOGGER.start.__doc__


def closeLogfile(filename):
    """Close logfile with *filename*."""

    LOGGER.close(filename)


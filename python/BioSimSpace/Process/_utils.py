######################################################################
# BioSimSpace: Making biomolecular simulation a breeze!
#
# Copyright: 2017-2019
#
# Authors: Lester Hedges <lester.hedges@gmail.com>
#
# BioSimSpace is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# BioSimSpace is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BioSimSpace. If not, see <http://www.gnu.org/licenses/>.
#####################################################################

"""
Utility functions.
"""

from ._amber import *
from ._gromacs import *
from ._namd import *
from ._process_runner import *
from ._somd import *

__author__ = "Lester Hedges"
__email_ = "lester.hedges@gmail.com"

__all__ = ["packages", "createProcess"]

# Create a list of the supported molecular dynamics packages.
_packages = []
_package_dict = {}
import sys as _sys
_namespace = _sys.modules[__name__]
for _var in dir():
    if _var[0] != "_" and _var != "ProcessRunner":
        _packages.append(_var)
        _package_dict[_var] = getattr(_namespace, _var)
del _namespace
del _sys
del _var

def packages():
    """Return a list of the supported Molecular Dynamics packages.

       Returns
       -------

       packages : [str]
           The list of supported Molecular Dynamics packages.
    """
    return _packages

def createProcess(system, protocol, package):
    """Create a simulation process.

       Parameters
       ----------

       system : :class:`System <BioSimSpace._SireWrappers.System>`
           The molecular system.

       protocol : :class:`Protocol <BioSimSpace.Protocol>`
           The protocol for the process.

       package : str
           The name of the simulation package.

       Returns
       -------

       process : :class:`Process <BioSimSpace.Process>`
           The process object for the specific simulation package.
    """

    if package not in _package_dict:
        raise KeyError("Unsupported package '%s', supported packages are %s" % (package, _packages))

    return _package_dict[package](system, protocol)

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
Length units.
"""

from ...Types import Length as _Length

__author__ = "Lester Hedges"
__email_ = "lester.hedges@gmail.com"

__all__ = ["meter", "centimeter", "millimeter",
           "nanometer", "angstrom", "picometer"]

meter = _Length(1, "meter")
centimeter = _Length(1, "centimeter")
millimeter = _Length(1, "millimeter")
nanometer = _Length(1, "nanometer")
angstrom = _Length(1, "angstrom")
picometer = _Length(1, "picometer")

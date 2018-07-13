######################################################################
# BioSimSpace: Making biomolecular simulation a breeze!
#
# Copyright: 2017-2018
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
Tools for plotting data.
Author: Lester Hedges <lester.hedges@gmail.com>
"""

from BioSimSpace import _is_interactive

import BioSimSpace.Types._type as _Type

from warnings import warn as _warn

from os import environ as _environ

# Check to see if DISPLAY is set.
if "DISPLAY" in _environ:
    _display = _environ.get("DISPLAY")
else:
    _display = ""
del(_environ)

if _display is not "":
    _has_display = True
    try:
        import matplotlib.pyplot as _plt
        _has_matplotlib = True
    except ImportError:
        _has_matplotlib = False
else:
    _has_matplotlib = False
    _has_display = False
    _warn("The DISPLAY environment variable is unset. Plotting functionality disabled!")
del(_display)

__all__ = ["plot"]

if _has_matplotlib:
    # Define font sizes.
    _SMALL_SIZE = 14
    _MEDIUM_SIZE = 16
    _BIGGER_SIZE = 18

    # Set font sizes.
    _plt.rc('font', size=_SMALL_SIZE)          # controls default text sizes
    _plt.rc('axes', titlesize=_SMALL_SIZE)     # fontsize of the axes title
    _plt.rc('axes', labelsize=_MEDIUM_SIZE)    # fontsize of the x and y labels
    _plt.rc('xtick', labelsize=_SMALL_SIZE)    # fontsize of the tick labels
    _plt.rc('ytick', labelsize=_SMALL_SIZE)    # fontsize of the tick labels
    _plt.rc('legend', fontsize=_SMALL_SIZE)    # legend fontsize
    _plt.rc('figure', titlesize=_BIGGER_SIZE)  # fontsize of the figure title

def plot(x=None, y=None, xlabel=None, ylabel=None, logx=False, logy=False):
    """A simple function to create x/y plots with matplotlib.

       Keyword arguments:

       x      -- A list of x data values.
       y      -- A list of y data values.
       xlabel -- The x axis label string.
       ylabel -- The y axis label string.
       logx   -- Whether the x axis is logarithmic.
       logy   -- Whether the y axis is logarithmic.
    """

    # Make sure were running interactively.
    if not _is_interactive():
        _warn("You can only use BioSimSpace.Notebook.plot when running interactively.")
        return None

    # Matplotlib failed to import.
    if not _has_matplotlib and _has_display:
        _warn("BioSimSpace.Notebook.plot is disabled as matplotlib failed "
            "to load. Please check your matplotlib installation.")
        return None

    # Convert tuple to a list.
    if type(x) is tuple:
        x = list(x)
    if type(y) is tuple:
        y = list(y)

    # Whether we need to convert the x and y data to floats.
    is_unit_x = False
    is_unit_y = False

    if x is None:
        if y is None:
            raise ValueError("'y' data must be defined!")

        # No x data, use array index as value.
        x = [x for x in range(0, len(y))]

    else:
        # No y data, we assume that the user wants to plot the x
        # data as a series.
        if y is None:
            y = x
            x = [x for x in range(0, len(y))]

    # The x argument must be a list of data records.
    if type(x) is not list:
        raise TypeError("'x' must be of type 'list'")

    else:
        # Make sure all records are of the same type.
        _type = type(x[0])
        if not all(isinstance(xx, _type) for xx in x):
            raise TypeError("All 'x' data values must be of same type")

        # Does this type have units?
        if isinstance(x[0], _Type.Type):
            is_unit_x = True

    # The y argument must be a list of data records.
    if type(y) is not list:
        raise TypeError("'y' must be of type 'list'")

    else:
        # Make sure all records are of the same type.
        _type = type(y[0])
        if not all(isinstance(yy, _type) for yy in y):
            raise TypeError("All 'y' data values must be of same type")

        # Does this type have units?
        if isinstance(y[0], _Type.Type):
            is_unit_y = True

    # Lists must contain the same number of records.
    # Truncate the longer list to the length of the shortest.
    if len(x) != len(y):
        _warn("Mismatch in list sizes: len(x) = %d, len(y) = %d"
            % (len(x), len(y)))

        len_x = len(x)
        len_y = len(y)

        if len_x < len_y:
            y = y[:len_x]
        else:
            x = x[:len_y]

    if xlabel is not None:
        if type(xlabel) is not str:
            raise TypeError("'xlabel' must be of type 'str'")
    else:
        if isinstance(x[0], _Type.Type):
            xlabel = x[0].__class__.__qualname__ + " (" + x[0]._print_format[x[0].unit()] + ")"

    if ylabel is not None:
        if type(ylabel) is not str:
            raise TypeError("'ylabel' must be of type 'str'")
    else:
        if isinstance(y[0], _Type.Type):
            ylabel = y[0].__class__.__qualname__ + " (" + y[0]._print_format[y[0].unit()] + ")"

    # Convert the x and y values to floats.
    if is_unit_x:
        x = [x.magnitude() for x in x]
    if is_unit_y:
        y = [y.magnitude() for y in y]

    # Set the figure size.
    _plt.figure(figsize=(8, 6))

    # Create the plot.
    _plt.plot(x, y, "-bo")

    # Add axis labels.
    if xlabel is not None:
        _plt.xlabel(xlabel)
    if ylabel is not None:
        _plt.ylabel(ylabel)

    # Scale the axes.
    if logx:
        _plt.xscale("log")
    if logy:
        _plt.yscale("log")

    # Turn on grid.
    _plt.grid()

    return _plt.show()

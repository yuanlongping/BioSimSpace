.. _ref_install:

============
Installation
============

Conda install
=============

The easiest way to install BioSimSpace is using our `conda channel <https://anaconda.org/michellab/repo>`__:

.. code-block:: bash

    conda install -c rdkit -c conda-forge -c omnia -c michellab biosimspace

To install the latest development version you can use:

.. code-block:: bash

    conda install -c rdkit -c conda-forge -c omnia -c michellab/label/dev biosimspace

Following this, you'll need to use ``pip`` to install some additional, non-conda,
packages into your environment:

.. code-block:: bash

    pip install fileupload pygtail pypdb

Unless you add the required channels to your Conda configuration, then you'll
need to add them when updating, e.g., for the development package:

.. code-block:: bash

    conda update -c rdkit -c conda-forge -c omnia -c michellab/label/dev biosimspace

Note that on OS X you will need to run Python scripts with the ``sire_python``
interpreter. This is due to an issue with the default Python interpreter that
is installed via Conda. (This applies to all installation methods.)

Binary install
==============

The self-extracting binary for the 2019.1.0 release of BioSimSpace
can be downloaded from one of the following links:

* Linux: `biosimspace_2019_1_0_linux.run <https://objectstorage.eu-frankfurt-1.oraclecloud.com/p/uM4T7NjDaeLBOt0cBXSEyW7p4XcPhcKewlytEheX3HA/n/chryswoods/b/biosimspace_releases/o/biosimspace_2019_1_0_linux.run>`__
* Mac OS X: `biosimspace_2019_1_0_osx.run <https://objectstorage.eu-frankfurt-1.oraclecloud.com/p/yFhNo6rPsh2QtWpjNNsx6DGr45idI3AZ_-cc6L7k51g/n/chryswoods/b/biosimspace_releases/o/biosimspace_2019_1_0_osx.run>`__

The latest self-extracting binary for the development version of BioSimSpace
can be downloaded from one of the following links:

* Linux: `biosimspace_devel_latest_linux.run <https://objectstorage.eu-frankfurt-1.oraclecloud.com/p/ZH4wscDHe59T28yVJtrMH8uqifI_ih0NL5IyqxXQjSo/n/chryswoods/b/biosimspace_releases/o/biosimspace_devel_latest_linux.run>`__
* Mac OS X: `biosimspace_devel_latest_osx.run <https://objectstorage.eu-frankfurt-1.oraclecloud.com/p/whcwfvWfndjA4RxupM-4gsVsjcdR0w5I9aP1RJKPruQ/n/chryswoods/b/biosimspace_releases/o/biosimspace_devel_latest_osx.run>`__

(These are portable X86-64 binaries that should work on any Linux distribution released
since ~2011, or any OS X >= 10.9 [Mavericks, released 2013]. Note that they are compiled
with AVX enabled, so will only work on modern (>2011) X86-64 Intel/AMD processors.)

Once downloaded, the binary can be unpacked as follows, e.g. for the Linux
development package:

.. code-block:: bash

   chmod +x biosimspace_devel_latest_linux.run
   ./biosimspace_devel_latest_linux.run

This will let you choose where to install BioSimSpace. By default, this will be
into ``$HOME/biosimspace.app``.

For developers
==============

The following documents a full installation of BioSimSpace from source. Before
starting, you'll need a working `Git <https://git-scm.com>`__ installation.

1. BioSimSpace is built on top of the `Sire <https://github.com/michellab/Sire>`__
   molecular simulation framework. To download and install Sire:

.. code-block:: bash

   git clone https://github.com/michellab/Sire
   cd Sire
   ./compile_sire.sh

Assuming the default installation path, this will install Sire into ``$HOME/sire.app``.

(Note that the installation is slow and can take in excess of an hour.)

2. Next you will need to download BioSimSpace and install it into your Sire
   application. (The following assumes the default Sire installation path.)

.. code-block:: bash

   git clone https://github.com/michellab/BioSimSpace
   cd BioSimSpace/python
   $HOME/sire.app/bin/python setup.py install

Once finished, you can test the installation by running:

.. code-block:: bash

   $HOME/sire.app/bin/ipython

Then try importing the BioSimSpace package:

.. code-block:: python

   import BioSimSpace as BSS

When developing you may not wish to continually re-install BioSimSpace and its
associated dependencies. To avoid this, you can either make use of ``PYTHONPATH``,
e.g.

.. code-block:: bash

   PYTHONPATH=$HOME/Code/BioSimSpace/python $HOME/sire.app/bin/python script.py

or use the ``develop`` argument when running the ``setup.py`` script, i.e.

.. code-block:: bash

   PYTHONPATH=$HOME/sire.app/bin/python setup.py develop

You can also skip installation of external dependencies by setting the
environment variable ``BSS_SKIP_DEPENDENCIES``, e.g.

.. code-block:: bash

   BSS_SKIP_DEPENDENCIES=True $HOME/sire.app/bin/python setup.py install

OpenMM compatibility
====================

Some BioSimSpace functionality requires `OpenMM <http://openmm.org>`__. Although
a bundled version is provided as part of the installation, this may not
be appropriate for your GPU drivers. To automatically detect and install
a suitable version of OpenMM, simply run the following command post-install:

.. code-block:: bash

    optimise_openmm

(Note that, depending on your installation method, ``optimise_openmm`` may
be located in ``$HOME/sire.app/bin``.)

Alternatively, to manually install a particular version of OpenMM you can
use a specific Conda label, e.g.:

.. code-block:: bash

    conda install -c omnia/label/cuda90 openmm

If you have compiled Sire against a custom OpenMM installation, then you'll
need to set the ``OPENMM_PLUGIN_DIR`` environment variable to point to the
correct plugin location. By default this variable is set to the plugin
directory of the bundled OpenMM package.

Common issues
=============

* If you experience problems with `Matplotlib <https://matplotlib.org>`__ when
  importing BioSimSpace on macOS, e.g.

.. code-block:: bash

   RuntimeError**: Python is not installed as a framework.

simply add the following to ``~/.matplotlib/matplotlibrc``

.. code-block:: bash

   backend: TkAgg

Note that plotting functionality will be disabled if you are using
BioSimSpace on a remote server without X forwarding.

* If you experience problems with `Jupyter <https://jupyter.org>`__ permissions,
  try removing ``$HOME/.jupyter`` or ``$HOME/.local/share/jupyter``

External dependencies
=====================

Several additional packages are required for full access to all of BioSimSpace's
functionality. Please download and install these packages according to their
recommended installation instructions.

* `Amber / AmberTools <http://ambermd.org>`__ -- *Dynamics / Parameterisation*
* `Gromacs <http://www.gromacs.org>`__ -- *Dynamics / Parameterisation / Solvation*
* `Namd <http://www.ks.uiuc.edu/Research/namd>`__ -- *Dynamics*

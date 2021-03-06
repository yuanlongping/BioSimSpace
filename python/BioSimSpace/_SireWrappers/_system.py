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
A thin wrapper around Sire.System. This is an internal package and should
not be directly exposed to the user.
"""

import Sire.Maths as _SireMaths
import Sire.Mol as _SireMol
import Sire.System as _SireSystem
import Sire.Vol as _SireVol

from .._Exceptions import IncompatibleError as _IncompatibleError
from ..Types import Length as _Length

import BioSimSpace.Units as _Units

__author__ = "Lester Hedges"
__email_ = "lester.hedges@gmail.com"

__all__ = ["System"]

class _MolWithResName(_SireMol.MolWithResID):
    def __init__(self, resname):
        super().__init__(_SireMol.ResName(resname))

class System():
    """A container class for storing molecular systems."""

    def __init__(self, system):
        """Constructor.

           Parameters
           ----------

           system : Sire.System.System, :class:`System <BioSimSpace._SireWrappers.System>`, \
                    Sire.Mol.Molecule, :class:`Molecule <BioSimSpace._SireWrappers.Molecule>`, \
                    [:class:`Molecule <BioSimSpace._SireWrappers.Molecule>`]
               A Sire or BioSimSpace System object, a Sire or BioSimSpace Molecule object,
               or a list of BioSimSpace molecule objects.
        """

        # Check that the system is valid.

        # Convert tuple to a list.
        if type(system) is tuple:
            system = list(system)

        # A Sire System object.
        if type(system) is _SireSystem.System:
            self._sire_system = system.__deepcopy__()

        # Another BioSimSpace System object.
        elif type(system) is System:
            self._sire_system = system._sire_system.__deepcopy__()

        # A Sire Molecule object.
        elif type(system) is _SireMol.Molecule:
            self._sire_system = _SireSystem.System("BioSimSpace System.")
            self.addMolecules(_Molecule(system))

        # A BioSimSpace Molecule object.
        elif type(system) is _Molecule:
            self._sire_system = _SireSystem.System("BioSimSpace System.")
            self.addMolecules(system)

        # A list of BioSimSpace Molecule objects.
        elif type(system) is list:
            if not all(isinstance(x, _Molecule) for x in system):
                raise TypeError("'system' must contain a list of 'BioSimSpace._SireWrappers.Molecule' types.")
            else:
                self._sire_system = _SireSystem.System("BioSimSpace System.")
                self.addMolecules(system)

        # Invalid type.
        else:
            raise TypeError("'system' must be of type 'Sire.System._System.System', 'BioSimSpace._SireWrappers.System', "
                            " Sire.Mol._Mol.Molecule', 'BioSimSpace._SireWrappers.Molecule', "
                            "or a list of 'BioSimSpace._SireWrappers.Molecule' types.")

    def __str__(self):
        """Return a human readable string representation of the object."""
        return "<BioSimSpace.System: nMolecules=%d>" % self.nMolecules()

    def __repr__(self):
        """Return a string showing how to instantiate the object."""
        return "<BioSimSpace.System: nMolecules=%d>" % self.nMolecules()

    def __add__(self, other):
        """Addition operator."""

        # Create a copy of the current system.
        system = System(self._sire_system.__deepcopy__())

        # Add the new molecules.
        if type(other) is System:
            system.addMolecules(other.getMolecules())
        else:
            system.addMolecules(other)

        # Return the combined system.
        return system

    def __sub__(self, other):
        """Subtraction operator."""

        # Create a copy of the current system.
        system = System(self._sire_system.__deepcopy__())

        # Remove the molecules from the other system.
        if type(other) is System:
            system.removeMolecules(other.getMolecules())
        else:
            system.removeMolecules(other)

        # Return the new system.
        return system

    def copy(self):
        """Return a copy of this system.

           Returns
           -------

           system : :class:`System <BioSimSpace._SireWrappers.System>`
               A copy of the system.
        """
        return System(self)

    def nMolecules(self):
        """Return the number of molecules in the system.

           Returns
           -------

           num_molecules : int
               The number of molecules in the system.
        """
        return self._sire_system.nMolecules()

    def nResidues(self):
        """Return the number of residues in the system.

           Returns
           -------

           num_residues : int
               The number of residues in the system.
        """

        tally = 0

        for n in self._sire_system.molNums():
            tally += self._sire_system[n].nResidues()

        return tally

    def nChains(self):
        """Return the number of chains in the system.

           Returns
           -------

           num_chains : int
               The number of chains in the system.
        """

        tally = 0

        for n in self._sire_system.molNums():
            tally += self._sire_system[n].nChains()

        return tally

    def nAtoms(self):
        """Return the number of atoms in the system.

           Returns
           -------

           num_atoms : int
               The number of atoms in the system.
        """

        tally = 0

        for n in self._sire_system.molNums():
            tally += self._sire_system[n].nAtoms()

        return tally

    def charge(self, property_map={}, is_lambda1=False):
        """Return the total molecular charge.

           Parameters
           ----------

           property_map : dict
               A dictionary that maps system "properties" to their user defined
               values. This allows the user to refer to properties with their
               own naming scheme, e.g. { "charge" : "my-charge" }

           is_lambda1 : bool
              Whether to use the charge at lambda = 1 if the molecule is merged.

           Returns
           -------

           charge : :class:`Charge <BioSimSpace.Types.Charge>`
               The molecular charge.
        """

        # Zero the charge.
        charge = 0 * _Units.Charge.electron_charge

        # Loop over all molecules and add the charge.
        for mol in self.getMolecules():
            # Reset the map.
            _property_map = property_map.copy()

            # If the molecule is merged, then re-map the charge property.
            if mol.isMerged():
                if is_lambda1:
                    _property_map = { "charge" : "charge1" }
                else:
                    _property_map = { "charge" : "charge0" }

            # Add the charge.
            try:
                charge += mol.charge(_property_map)
            except:
                pass

        # Return the total charge.
        return charge

    def fileFormat(self, property_map={}):
        """Return the file formats associated with the system.

           Parameters
           ----------

           property_map : dict
               A dictionary that maps system "properties" to their user defined
               values. This allows the user to refer to properties with their
               own naming scheme, e.g. { "charge" : "my-charge" }

           Returns
           -------

           format : str
              The file formats associated with the system.
        """

        if type(property_map) is not dict:
            raise TypeError("'property_map' must be of type 'dict'")

        prop = property_map.get("fileformat", "fileformat")

        try:
            return self._sire_system.property(prop).value()
        except:
            return None

    def addMolecules(self, molecules):
        """Add a molecule, or list of molecules to the system.

           Parameters
           ----------

           molecules : :class:`Molecule <BioSimSpace._SireWrappers.Molecule>`, \
                       [:class:`Molecule <BioSimSpace._SireWrappers.Molecule>`]
              A Molecule, or list of Molecule objects.
        """

        # Convert tuple to a list.
        if type(molecules) is tuple:
            molecules = list(molecules)

        # A Molecule object.
        if type(molecules) is _Molecule:
            molecules = [molecules]

        # A list of Molecule objects.
        elif type(molecules) is list and all(isinstance(x, _Molecule) for x in molecules):
            pass

        # Invalid argument.
        else:
            raise TypeError("'molecules' must be of type 'BioSimSpace._SireWrappers.Molecule' "
                            "or a list of 'BioSimSpace._SireWrappers.Molecule' types.")

        # The system is empty: create a new Sire system from the molecules.
        if self._sire_system.nMolecules() == 0:
            self._sire_system = self._createSireSystem(molecules)

        # Otherwise, add the molecules to the existing "all" group.
        else:
            for mol in molecules:
                self._sire_system.add(mol._sire_molecule, _SireMol.MGName("all"))

    def removeMolecules(self, molecules):
        """Remove a molecule, or list of molecules from the system.

           Parameters
           ----------

           molecules : :class:`Molecule <BioSimSpace._SireWrappers.Molecule>`, \
                       [:class:`Molecule <BioSimSpace._SireWrappers.Molecule>`]
              A Molecule, or list of Molecule objects.
        """

        # Convert tuple to a list.
        if type(molecules) is tuple:
            molecules = list(molecules)

        # A Molecule object.
        if type(molecules) is _Molecule:
            molecules = [molecules]

        # A list of Molecule objects.
        elif type(molecules) is list and all(isinstance(x, _Molecule) for x in molecules):
            pass

        # Invalid argument.
        else:
            raise TypeError("'molecules' must be of type 'BioSimSpace._SireWrappers.Molecule' "
                            "or a list of 'BioSimSpace._SireWrappers.Molecule' types.")

        # Remove the molecules in the system.
        for mol in molecules:
            self._sire_system.remove(mol._sire_molecule.number())

    def removeWaterMolecules(self):
        """Remove all of the water molecules from the system."""

        # Get the list of water molecules.
        waters = self.getWaterMolecules()

        # Remove the molecules in the system.
        for mol in waters:
            self._sire_system.remove(mol._sire_molecule.number())

    def updateMolecules(self, molecules):
        """Update a molecule, or list of molecules in the system.

           Parameters
           ----------

           molecules : :class:`Molecule <BioSimSpace._SireWrappers.Molecule>`, \
                       [:class:`Molecule <BioSimSpace._SireWrappers.Molecule>`]
              A Molecule, or list of Molecule objects.
        """

        # Convert tuple to a list.
        if type(molecules) is tuple:
            molecules = list(molecules)

        # A Molecule object.
        if type(molecules) is _Molecule:
            molecules = [molecules]

        # A list of Molecule objects.
        elif type(molecules) is list and all(isinstance(x, _Molecule) for x in molecules):
            pass

        # Invalid argument.
        else:
            raise TypeError("'molecules' must be of type 'BioSimSpace._SireWrappers.Molecule' "
                            "or a list of 'BioSimSpace._SireWrappers.Molecule' types.")

        # Update each of the molecules.
        # TODO: Currently the Sire.System.update method doesn't work correctly
        # for certain changes to the Molecule molInfo object. As such, we remove
        # the old molecule from the system, then add the new one in.
        for mol in molecules:
            try:
                self._sire_system.update(mol._sire_molecule)
            except:
                self._sire_system.remove(mol._sire_molecule.number())
                self._sire_system.add(mol._sire_molecule, _SireMol.MGName("all"))

    def getMolecules(self, group="all"):
        """Return a list containing all of the molecules in the specified group.

           Parameters
           ----------

           group : str
               The name of the molecule group.

           Returns
           -------

           molecules : [:class:`Molecule <BioSimSpace._SireWrappers.Molecule>`]
               The list of molecules in the group.
        """

        if type(group) is not str:
            raise TypeError("'group' must be of type 'str'")

        # Try to extract the molecule group.
        try:
            molgrp = self._sire_system.group(_SireMol.MGName(group))
        except:
            raise ValueError("No molecules in group '%s'" % group)

        # Create a list to store the molecules.
        mols = []

        # Get a list of the MolNums in the group and sort them.
        nums = molgrp.molNums()

        # Loop over all of the molecules in the group and append to the list.
        for num in nums:
            mols.append(_Molecule(molgrp.molecule(num)))

            # This is a merged molecule.
            if mols[-1]._sire_molecule.hasProperty("is_perturbable"):
                mols[-1]._is_merged = True

        return mols

    def getWaterMolecules(self):
        """Return a list containing all of the water molecules in the system.

           Returns
           -------

           molecules : [:class:`Molecule <BioSimSpace._SireWrappers.Molecule>`]
               A list of water molecule objects.
        """

        waters = []

        for mol in self._sire_system.search("water"):
            waters.append(_Molecule(mol))

        return waters

    def nWaterMolecules(self):
        """Return the number of water molecules in the system.

           Returns
           -------

           num_waters : int
               The number of water molecules in the system.
        """
        return len(self.getWaterMolecules())

    def getPerturbableMolecules(self):
        """Return a list containing all of the perturbable molecules in the system.

           Returns
           -------

           molecules : [:class:`Molecule <BioSimSpace._SireWrappers.Molecule>`]
               A list of perturbable molecules.
        """

        molecules = []

        for mol in self._sire_system.search("perturbable"):
            molecules.append(_Molecule(mol))

        return molecules

    def nPerturbableMolecules(self):
        """Return the number of perturbable molecules in the system.

           Returns
           -------

           num_perturbable : int
               The number of perturbable molecules in the system.
        """
        return len(self.getPerturbableMolecules())

    def getMolWithResName(self, resname):
        """Return the molecule containing the given residue.

           Parameters
           ----------

           resname : str
               The name of a residue unique to the molecule.

           Returns
           -------

           molecule : :class:`Molecule <BioSimSpace._SireWrappers.Molecule>`
               The matching molecule.
        """
        try:
            return _Molecule(self._sire_system[_MolWithResName(resname)])
        except:
            raise KeyError("System does not contain residue '%s'" % resname)

    def setBox(self, size, property_map={}):
        """Set the size of the periodic simulation box.

           Parameters
           ----------

           size : [:class:`Length <BioSimSpace.Types.Length>`]
               The size of the box in each dimension.

           property_map : dict
               A dictionary that maps system "properties" to their user defined
               values. This allows the user to refer to properties with their
               own naming scheme, e.g. { "charge" : "my-charge" }

        """

        # Convert tuple to list.
        if type(size) is tuple:
            size = list(size)

        # Validate input.
        if type(size) is not list or not all(isinstance(x, _Length) for x in size):
            raise TypeError("'size' must be a list of 'BioSimSpace.Types.Length' objects.")

        if len(size) != 3:
            raise ValueError("'size' must contain three items.")

        # Convert sizes to Anstrom.
        vec = [x.angstroms().magnitude() for x in size]

        # Create a periodic box object.
        box = _SireVol.PeriodicBox(_SireMaths.Vector(vec))

        # Set the "space" property.
        self._sire_system.setProperty(property_map.get("space", "space"), box)

    def getBox(self, property_map={}):
        """Get the size of the periodic simulation box.

           Parameters
           ----------

           property_map : dict
               A dictionary that maps system "properties" to their user defined
               values. This allows the user to refer to properties with their
               own naming scheme, e.g. { "charge" : "my-charge" }

           Returns
           -------

           box_size : [:class:`Length <BioSimSpace.Types.Length>`]
               The size of the box in each dimension.
       """

        # Get the "space" property and convert to a list of BioSimSpace.Type.Length
        # objects.
        try:
            box = self._sire_system.property(property_map.get("space", "space"))
            box = [ _Length(x, "Angstrom") for x in box.dimensions() ]
        except:
            box = None

        return box

    def translate(self, vector, property_map={}):
        """Translate the system.

           Parameters
           ----------

           vector : [:class:`Length <BioSimSpace.Types.Length>`]
               The translation vector.

           property_map : dict
               A dictionary that maps system "properties" to their user defined
               values. This allows the user to refer to properties with their
               own naming scheme, e.g. { "charge" : "my-charge" }
        """

        # Convert tuple to a list.
        if type(vector) is tuple:
            vector = list(vector)

        # Validate input.
        if type(vector) is list:
            vec = []
            for x in vector:
                if type(x) is int:
                    vec.append(float(x))
                elif type(x) is float:
                    vec.append(x)
                elif type(x) is _Length:
                    vec.append(x.angstroms().magnitude())
                else:
                    raise TypeError("'vector' must contain 'int', 'float', or "
                                    "'BioSimSpace.Types.Length' types only!")
        else:
            raise TypeError("'vector' must be of type 'list' or 'tuple'")

        if type(property_map) is not dict:
            raise TypeError("'property_map' must be of type 'dict'")

        # Translate each of the molecules in the system.
        for n in self._sire_system.molNums():
            # Copy the property map.
            _property_map = property_map.copy()

            # If this is a perturbable molecule, use the coordinates at lambda = 0.
            if self._sire_system.molecule(n).hasProperty("is_perturbable"):
                _property_map["coordinates"] = "coordinates0"

            mol = self._sire_system[n].move().translate(_SireMaths.Vector(vec), _property_map).commit()
            self._sire_system.update(mol)

    def _getSireSystem(self):
        """Return the full Sire System object.

           Returns
           -------

           system : Sire.System.System
               The underlying Sire system object.
        """
        return self._sire_system

    def _getAABox(self, property_map={}):
        """Get the axis-aligned bounding box for the molecular system.

           Parameters
           ----------

           property_map : dict
               A dictionary that maps system "properties" to their user defined
               values. This allows the user to refer to properties with their
               own naming scheme, e.g. { "charge" : "my-charge" }

           Returns
           -------

           aabox : Sire.Vol.AABox
               The axis-aligned bounding box for the molecule.
        """

        # Initialise the coordinates vector.
        coord = []

        # Get all of the molecules in the system.
        mols = self.getMolecules()

        # Loop over all of the molecules.
        for idx, mol in enumerate(mols):

            # Extract the atomic coordinates and append them to the vector.
            try:
                if "coordinates" in property_map:
                    prop = property_map["coordinates"]
                else:
                    if mol.isMerged():
                        prop = "coordinates0"
                    else:
                        prop = "coordinates"
                coord.extend(mol._sire_molecule.property(prop).toVector())

            except UserWarning:
                raise UserWarning("Molecule %d has no 'coordinates' property." % idx) from None

        # Return the AABox for the coordinates.
        return _SireVol.AABox(coord)

    def _renumberMolecules(self, molecules, is_rebuild=False):
        """Helper function to renumber the molecules to be consistent with the
           system.

           Parameters
           ----------

           molecules : [:class:`Molecule <BioSimSpace._SireWrappers.Molecule>`]
               A list of molecule objects.

           Returns
           -------

           molecules : [:class:`Molecule <BioSimSpace._SireWrappers.Molecule>`]
               The renumber list of molecule objects.
        """

        # Renumber everything.
        if is_rebuild:
            num_molecules = 0
            num_residues = 0
            num_atoms = 0

        # Get the current number of molecules, residues, and atoms.
        else:
            num_molecules = self.nMolecules()
            num_residues = self.nResidues()
            num_atoms = self.nAtoms()

        # Create a list to hold the modified molecules.
        new_molecules = []

        # Loop over all of the molecules.
        for mol in molecules:

            # Create a copy of the molecule.
            new_mol = _Molecule(mol)

            # Get the Sire molecule and make it editable.
            edit_mol = new_mol._sire_molecule.edit()

            # Renumber the molecule.
            edit_mol = edit_mol.renumber(_SireMol.MolNum(num_molecules+1)).molecule()
            num_molecules += 1

            # A hash mapping between old and new numbers.
            num_hash = {}

            # Loop over all residues and add them to the hash.
            for res in edit_mol.residues():
                num_hash[res.number()] = _SireMol.ResNum(num_residues+1)
                num_residues += 1

            # Renumber the residues.
            edit_mol = edit_mol.renumber(num_hash).molecule()

            # Clear the hash.
            num_hash = {}

            # Loop over all of the atoms and add them to the hash.
            for atom in edit_mol.atoms():
                num_hash[atom.number()] = _SireMol.AtomNum(num_atoms+1)
                num_atoms += 1

            # Renumber the atoms.
            edit_mol = edit_mol.renumber(num_hash).molecule()

            # Commit the changes and replace the molecule.
            new_mol._sire_molecule = edit_mol.commit()

            # Append to the list of molecules.
            new_molecules.append(new_mol)

        # Return the renumbered molecules.
        return new_molecules

    def _updateCoordinates(self, system, property_map0={}, property_map1={},
            is_lambda1=False):
        """Update the coordinates of atoms in the system.

           Parameters
           ----------

           system : :class:`System <BioSimSpace._SireWrappers.System>`
               A system containing the updated coordinates.

           property_map0 : dict
               A dictionary that maps system "properties" to their user defined
               values in this system.

           property_map1 : dict
               A dictionary that maps system "properties" to their user defined
               values in the passed system.

           is_lambda1 : bool
              Whether to update coordinates of perturbed molecules at lambda = 1.
              By default, coordinates at lambda = 0 are used.
        """

        # Validate the system.
        if type(system) is not System:
            raise TypeError("'system' must be of type 'BioSimSpace._SireWrappers.System'")

        # Check that the passed system contains the same number of molecules.
        if self.nMolecules() != system.nMolecules():
            raise _IncompatibleError("The passed 'system' contains a different number of "
                                     "molecules. Expected '%d', found '%d'"
                                     % (self.nMolecules, system.nMolecules()))

        # Check that each molecule in the system contains the same number of atoms.
        for idx in range(0, self.nMolecules()):
            # Extract the number of atoms in the molecules.
            num_atoms0 = self._sire_system.molecule(_SireMol.MolIdx(idx)).nAtoms()
            num_atoms1 = self._sire_system.molecule(_SireMol.MolIdx(idx)).nAtoms()

            if num_atoms0 != num_atoms1:
                raise _IncompatibleError("Mismatch in atom count for molecule '%d': "
                                         "Expected '%d', found '%d'" % (num_atoms0, num_atoms1))

        # Work out the name of the "coordinates" property.
        prop0 = property_map0.get("coordinates0", "coordinates")
        prop1 = property_map1.get("coordinates1", "coordinates")

        # Loop over all molecules and update the coordinates.
        for idx in range(0, self.nMolecules()):
            # Extract the molecules from each system.
            mol0 = self._sire_system.molecule(_SireMol.MolIdx(idx))
            mol1 = system._sire_system.molecule(_SireMol.MolIdx(idx))

            # Check whether the molecule is perturbable.
            if mol0.hasProperty("is_perturbable"):
                if is_lambda1:
                    prop = "coordinates1"
                else:
                    prop = "coordinates0"
            else:
                prop = prop0

            # Try to update the coordinates property.
            try:
                mol0 = mol0.edit().setProperty(prop, mol1.property(prop1)).molecule().commit()
            except:
                raise _IncompatibleError("Unable to update 'coordinates' for molecule index '%d'" % idx)

            # Update the molecule in the original system.
            self._sire_system.update(mol0)

    @staticmethod
    def _createSireSystem(molecules):
        """Create a Sire system from a list of molecules.

           Parameters
           ----------

           molecules : [:class:`Molecule <BioSimSpace._SireWrappers.Molecule>`]

           Returns
           -------

           system : Sire.System.System
               A Sire system object.
        """

        # Create an empty Sire System.
        system = _SireSystem.System("BioSimSpace System")

        # Create a new "all" molecule group.
        molgrp = _SireMol.MoleculeGroup("all")

        # Add the molecules to the group.
        for mol in molecules:
            molgrp.add(mol._sire_molecule)

        # Add the molecule group to the system.
        system.add(molgrp)

        return system

# Import at bottom of module to avoid circular dependency.
from ._molecule import Molecule as _Molecule


# coding: utf-8

# Author: Julien Michel
# 
# email: julien.michel@ed.ac.uk

# # PrepareFEP
# Loads a pair of input files, perform mapping between the first molecule of each input. Write down input files for a SOMD FEP calculation.

# In[15]:


import BioSimSpace as BSS
import os


# In[2]:


def writeLog(ligA, ligB, mapping):
    """ Human readable report on atoms used for the mapping."""
    atoms_in_A = list(mapping.keys())
    stream = open('somd.mapping','w')
    for atAidx in atoms_in_A:
        atA = ligA._sire_molecule.select(atAidx)
        atB = ligB._sire_molecule.select(mapping[atAidx])
        stream.write("%s --> %s\n" % (atA.name(),atB.name()))
    stream.close()


# In[3]:


node = BSS.Gateway.Node("A node to generate input files for a SOMD relative free energy calculation.")


# In[4]:


node.addAuthor(name="Julien Michel", email="julien.michel@ed.ac.uk", affiliation="University of Edinburgh")
node.setLicense("GPLv3")


# In[5]:


node.addInput("input1", BSS.Gateway.FileSet(help="A topology and coordinates file"))
node.addInput("input2", BSS.Gateway.FileSet(help="A topology and coordinates file"))
node.addInput("output", BSS.Gateway.String(help="The root name for the files describing the perturbation input1->input2."))


# In[6]:


# Optional input, dictionary of Atom indices that should be matched in the search. 
prematch = {}


# In[7]:


node.addOutput("nodeoutput", BSS.Gateway.FileSet(help="SOMD input files for a perturbation of input1->input2."))


# In[8]:


node.showControls()


# In[9]:


# Load system 1
system1 = BSS.IO.readMolecules(node.getInput("input1"))


# In[10]:


# Load system 2
system2 = BSS.IO.readMolecules(node.getInput("input2"))


# In[11]:


# We assume the molecules to perturb are the first molecules in each system
lig1 = system1.getMolecules()[0]
lig2 = system2.getMolecules()[0]


# In[12]:


# Return a maximum of 10 matches, scored by RMSD and sorted from best to worst.
mappings = BSS.Align.matchAtoms(lig1, lig2, matches=10, prematch=prematch)
# We retain the top mapping
mapping = mappings[0]


# In[13]:


# Align lig2 to lig1 based on the best mapping. The molecule is aligned based
# on a root mean squared displacement fit to find the optimal translation vector
# (as opposed to merely taking the difference of centroids).
lig2 = BSS.Align.rmsdAlign(lig2, lig1, mapping)
# Merge the two ligands based on the mapping.
merged = BSS.Align.merge(lig1, lig2, mapping)
# Create a composite system
system1.removeMolecules(lig1)
system1.addMolecules(merged)


# In[16]:


# Log the mapping used
writeLog(lig1, lig2, mapping)
BSS.IO.saveMolecules("merged_at_lam0.pdb", merged, "PDB", { "coordinates" : "coordinates0" , "element": "element0" })
# Generate package specific input
protocol = BSS.Protocol.FreeEnergy(runtime = 2*BSS.Units.Time.femtosecond, num_lam=3)
process = BSS.Process.Somd(system1, protocol)
process.getOutput()
cmd = "unzip -o somd.zip"
os.system(cmd)


# In[20]:


root = node.getInput("output")
mergedpdb = "%s.mergeat0.pdb" % root
pert = "%s.pert" % root
prm7 = "%s.prm7" % root
rst7 = "%s.rst7" % root
mapping = "%s.mapping" % root


# In[21]:


cmd = "mv merged_at_lam0.pdb %s ; mv somd.pert %s ; mv somd.prm7 %s ; mv somd.rst7 %s ; mv somd.mapping %s ; rm somd.zip ; rm somd.cfg ; rm somd.err; rm somd.out" % (mergedpdb,pert,prm7,rst7,mapping)
#print (cmd)
os.system(cmd)


# In[23]:


node.setOutput("nodeoutput",[mergedpdb, pert, prm7, rst7, mapping])


# In[24]:


node.validate()


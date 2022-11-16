from ase import neighborlist
from ase import geometry
from ase.build import molecule
from ase.io import read
from scipy import sparse
import copy
import glob
import shutil
import os
import sys


folder=sys.argv[1]
files=glob.glob(folder+"/*")
os.mkdir("filter_result")
print(files)

for file in files:
        print(file)
        mol=read(file)
        cutOff = neighborlist.natural_cutoffs(mol)
        neighborList = neighborlist.NeighborList(cutOff, self_interaction=False, bothways=True)
        neighborList.update(mol)
        matrix = neighborList.get_connectivity_matrix(sparse=False)
        n_components, component_list = sparse.csgraph.connected_components(matrix)
        if n_components==1:
            shutil.copy(file,"filter_result/"+file.split("/")[1])
	

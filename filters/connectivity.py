from ase import neighborlist
from ase import geometry
from ase.build import molecule
from ase.io import read
from scipy import sparse
import copy
import glob
import os

#file='H3Cu6Zn5Cps5Mes_structures_pbe/H3Cu6Zn5Cps5Mes_009.xyz'
file = input("Inform adress of reference geometry:")
folder = input("Inform the folder to be filtered:")


mol=read(file)
cutOff = neighborlist.natural_cutoffs(mol)
neighborList = neighborlist.NeighborList(cutOff, self_interaction=False, bothways=True)
neighborList.update(mol)
ideal_matrix = neighborList.get_connectivity_matrix(sparse=False)
n_components, component_list = sparse.csgraph.connected_components(ideal_matrix)

print(ideal_matrix)

ncomplexos=[]
estruturas=[]
#for file in sorted(glob.glob('H3Cu6Zn5Cps5Mes_structures_pbe/*.xyz')):
for file in sorted(glob.glob(folder+'/*.xyz')):

  mol=read(file)
  cutOff = neighborlist.natural_cutoffs(mol)
  neighborList = neighborlist.NeighborList(cutOff, self_interaction=False, bothways=True)
  neighborList.update(mol)
  matrix = neighborList.get_connectivity_matrix()
  matrix_nosparse = neighborList.get_connectivity_matrix(sparse=False)
  n_components, component_list = sparse.csgraph.connected_components(matrix)
  #teste=True
  soma=0
  for i in [11,12,13]:
    for j in [11,12,13]:        #range(14,len(matrix_nosparse)):
      #teste=teste and (matrix_nosparse[i][j]==ideal_matrix[i][j])
      soma=soma+matrix_nosparse[i][j]
  soma=soma/2
  
  teste_H_lig=True
  for i in [11,12,13]:
    for j in range(14,len(matrix_nosparse)):
      teste_H_lig=teste_H_lig and (matrix_nosparse[i][j]==ideal_matrix[i][j])
  
  teste_lig_lig=True
  for i in range(14,len(matrix_nosparse)):
    for j in range(14,len(matrix_nosparse)):
      teste_lig_lig=teste_lig_lig and (matrix_nosparse[i][j]==ideal_matrix[i][j])

  
  print(file,n_components,int(soma),teste_H_lig,teste_lig_lig)
  ncomplexos.append(n_components)
  estruturas.append(file)

print("Max number of fregments: ", max(ncomplexos))
cont=[]
indexlist=[]
for i in range(max(ncomplexos)):
  cont.append(0)
  indexlist.append([])

for i in range(len(ncomplexos)):
  cont[(ncomplexos[i]-1)]=cont[ncomplexos[i]-1]+1
  indexlist[(ncomplexos[i]-1)].append(estruturas[i][-7:-4])

for i in range(max(ncomplexos)):
  print(cont[i], indexlist[i])

                             
exit()
#################################################################################    
                             
                             
                             
file='HCu8Zn3Cps4Mes3_structures_pbe/HCu8Zn3Cps4Mes3_221.xyz'

mol=read(file)
cutOff = neighborlist.natural_cutoffs(mol)
neighborList = neighborlist.NeighborList(cutOff, self_interaction=False, bothways=True)
neighborList.update(mol)
ideal_matrix = neighborList.get_connectivity_matrix(sparse=False)
n_components, component_list = sparse.csgraph.connected_components(ideal_matrix)

print(ideal_matrix)

ncomplexos=[]
estruturas=[]
for file in sorted(glob.glob('HCu8Zn3Cps4Mes3_structures_pbe/*.xyz')):

  mol=read(file)
  cutOff = neighborlist.natural_cutoffs(mol)
  neighborList = neighborlist.NeighborList(cutOff, self_interaction=False, bothways=True)
  neighborList.update(mol)
  matrix = neighborList.get_connectivity_matrix()
  matrix_nosparse = neighborList.get_connectivity_matrix(sparse=False)
  n_components, component_list = sparse.csgraph.connected_components(matrix)
    
  teste_H_lig=True
  for i in [11]:
    for j in range(12,len(matrix_nosparse)):
      teste_H_lig=teste_H_lig and (matrix_nosparse[i][j]==ideal_matrix[i][j])
  
  teste_lig_lig=True
  for i in range(12,len(matrix_nosparse)):
    for j in range(12,len(matrix_nosparse)):
      teste_lig_lig=teste_lig_lig and (matrix_nosparse[i][j]==ideal_matrix[i][j])

      
  print(file,n_components,teste_H_lig,teste_lig_lig)
  ncomplexos.append(n_components)
  estruturas.append(file)

from google.colab import drive
drive.mount('/content/drive')

print("Numero maximo de particoes: ", max(ncomplexos))
cont=[]
indexlist=[]
for i in range(max(ncomplexos)):
  cont.append(0)
  indexlist.append([])

for i in range(len(ncomplexos)):
  cont[(ncomplexos[i]-1)]=cont[ncomplexos[i]-1]+1
  indexlist[(ncomplexos[i]-1)].append(estruturas[i][-7:-4])

for i in range(max(ncomplexos)):
  print(cont[i], indexlist[i])


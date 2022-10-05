#import pandas as pd
import numpy as np
import os
from glob import glob
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
#from sklearn import metrics
#from sklearn.manifold import TSNE
#from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm
import copy
from shutil import copyfile
from ase import neighborlist
from ase import geometry
from ase.build import molecule
from ase.io import read
from scipy import sparse
import math as m

#tresh=2*m.sqrt(11+6)*0.1
#element="Cu11Zn6"
element=input("Chemical formula of the nanocluster:")
n=input("Number of atoms on this cluster:")
tresh=2*m.sqrt(int(n))*0.1

def xyzRead(fname):
    fin = open(fname, "r")
    line1 = fin.readline().split()
    natoms = int(line1[0])
    comments = fin.readline()[:-1]
    coords = np.zeros([natoms, 3], dtype="float64")
    atomtypes = []
    for x in coords:
        line = fin.readline().split()
        atomtypes.append(line[0])
        x[:] = list(map(float, line[1:4]))

    return natoms, atomtypes, coords;

def getCharge(element):
    f = open("mol.txt")
    atomicnum = [line.split()[1] for line in f if line.split()[0] == element]
    f.close()
    return int(atomicnum[0])

def coulombMatrix(fname):
    natoms, atomtypes, coords = xyzRead(fname)
    i=0 ; j=0    
    colM = np.zeros((natoms,natoms))
    chargearray = np.zeros((natoms,1))
    charge = [getCharge(symbol)  for symbol in atomtypes]
    for i in range(0,natoms):
        colM[i,i]=0.5*charge[i]**2.4   # Diagonal term described by Potential energy of isolated atom
        for j in range(i+1,natoms):
            dist= np.linalg.norm(coords[i,:] - coords[j,:])   
            colM[j,i] = charge[i]*charge[j]/dist   #Pair-wise repulsion 
            colM[i,j] = colM[j,i]
    return colM
 

def eigenCoulomb(fname, num):
    sCoulomb = coulombMatrix(fname)
    sCoulomb = sCoulomb.astype(int)
    eigValues = -np.sort(-np.linalg.eigvals(sCoulomb))
    if np.any(np.iscomplex(eigValues)) == False:
        return eigValues[0:num]
    else:
        print('\nWARNING: complex (coulomb matrix) engenvalues for ' + fname + ' employing np.linalg.eigvals function.\n') 
        eigValues = -np.sort(-np.linalg.eigvalsh(sCoulomb))
        if np.any(np.iscomplex(eigValues)):
            print('\nWARNING: complex (coulomb matrix) engenvalues for ' + fname + ' employing np.linalg.eigvalsh function.\n WARNING: only the real part will be returned.\n')
            return eigValues.real[0:num]
        else :
            return eigValues[0:num]
params=9999



dataxyz = []
NAME=[]
ENERGY=[]

path=os.getcwd()
direc=input("Name of filtered structures directory:")
list_subfolders = [direc]#[f.path for f in os.scandir(path) if f.is_dir()]
print(list_subfolders)
for i in list_subfolders:    
    if "selected*" in i:
        pass
    else:
        i=str(i)
        o = [f for f in listdir(i) if isfile(join(i, f))]
        o.sort()
        for b in o:
            if ".gjf" in b:
                o.remove(b)
        for c in o:
            file = open(os.path.join(i, c), "r")
            e=file.readlines()[1]
            print(file)       #Print
            ee=(e.split(" ")[5])
            if ee=="":
                pass
            else:   
                ee=float(ee)
                mol=read(os.path.join(i, c))
                cutOff = neighborlist.natural_cutoffs(mol)
                neighborList = neighborlist.NeighborList(cutOff, self_interaction=False, bothways=True)
                neighborList.update(mol)
                matrix = neighborList.get_connectivity_matrix()
                n_components, _ = sparse.csgraph.connected_components(matrix)
                if  n_components==1: #and ee>-25 and ee<-17.5:
                    NAME.append(os.path.join(i, c))
                    ENERGY.append(ee)
                    natoms, atomtypes, coords = xyzRead(os.path.join(i, c))
                    if natoms < params:
                        params = natoms
                    mat = eigenCoulomb(os.path.join(i, c),params)
                    dataxyz.append(mat)

ax1 = plt.axes(label="Energies") 
ax1.scatter(np.arange(len(ENERGY)),ENERGY)
plt.savefig("energy.png")
ENERGY=np.array(ENERGY)



X = np.array(dataxyz)
XX=copy.deepcopy(X)
X = StandardScaler().fit_transform(X)
tsnee = PCA(n_components=2) ####
X = tsnee.fit_transform(X) ####
kmeans=cluster.AgglomerativeClustering(distance_threshold=tresh,n_clusters=None,compute_distances=True)
ax2 = plt.axes(label="PCA Reduced Coulomb Matrix Eigenvalues")

cluster_labels = kmeans.fit_predict(X)

ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7, c=ENERGY,edgecolor='k',cmap="jet")

plt.savefig("selected.png")

def uniqueIndexes(l):
    seen = set()
    res = []
    for i, n in enumerate(l):
        if n not in seen:
            res.append(i)
            seen.add(n)
    return res

res=uniqueIndexes(cluster_labels)

unique=[]
for i in res:
    unique.append(NAME[i])


b=[]
c=[]
for i in unique:
    a=[]
    a=i.split("/")
    #b.append(str(a[-3])+"_"+str(a[-1]))
    c.append(str(a[-1]))
print(len(unique))
os.system("mkdir selected")
for i in range(len(unique)):
    copyfile(str(unique[i]), 'selected/'+str(c[i]))



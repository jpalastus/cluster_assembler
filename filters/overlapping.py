import sys

from numpy.linalg import norm
import os
from os import listdir
from os.path import isfile, join

def _readXYZ(file):

    with open(str(file), "r") as xyz:
        # SKip the first two lines.
        next(xyz)
        next(xyz)
        for line in xyz:
            atom = line.split()
            yield [
                atom[0],  # atom symbol
                float(atom[1]),  # X
                float(atom[2]),  # Y
                float(atom[3])   # Z
            ]


def _readGeometryIn(file):

    with open(str(file), "r") as xyz:
        for line in xyz:
            atom = line.split()[1:]
            yield [
                atom[3],  # atom symbol
                float(atom[0]),  # X
                float(atom[1]),  # Y
                float(atom[2])   # Z
            ]


def readFile(file):

    if str(file).endswith(".in"):
        return list(_readGeometryIn(file))
    return list(_readXYZ(file))


def is_overlapping(xyz, t, cov):

    for x in range(1, len(xyz)):
        for y in range(x):
            dist = norm([xyz[x][1]-xyz[y][1], xyz[x][2] -
                         xyz[y][2], xyz[x][3]-xyz[y][3]])
            if (dist <= ((cov[xyz[x][0]] + cov[xyz[y][0]]) * t)):
                return True
    return False







if __name__ == "__main__":
	os.system('mkdir filtered')
	kk=0 
	of = [f for f in listdir('.') if isfile(join('.', f))] 
	of.remove('overlapping.py') 
	for i in of:
		#print(i)
		file = i
		t=0.8
		cov = {'H': 0.371, 'Li': 1.292, 'Be': 0.93, 'B': 0.848, 'C': 0.795, 'N': 0.759, 'O': 0.732, 'F': 0.706, 'Na': 1.613, 'Mg': 1.45, 'Al': 1.2, 'Si': 1.124, 'P': 1.08, 'S': 1.072, 'Cl': 0.994, 'K': 1.952, 'Ca': 1.723, 'Sc': 1.395, 'Ti': 1.294, 'V': 1.26, 'Cr': 1.25, 'Mn': 1.31, 'Fe': 1.235, 'Co': 1.225, 'Ni': 1.187, 'Cu': 1.14, 'Zn': 1.199, 'Ga': 1.233, 'Ge': 1.234, 'As': 1.23, 'Se': 1.17, 'Br': 1.141, 'Rb': 2.077, 'Sr': 1.88, 'Y': 1.52, 'Zr': 1.43, 'Nb': 1.49, 'Mo': 1.38, 'Tc': 1.31, 'Ru': 1.3, 'Rh': 1.26, 'Pd': 1.2, 'Ag': 1.35, 'Cd': 1.34, 'In': 1.45, 'Sn': 1.432, 'Sb': 1.425, 'Te': 1.34, 'I': 1.333, 'Cs': 2.2, 'Ba': 2.0, 'La': 1.72, 'Ce': 1.64, 'Pr': 1.64, 'Nd': 1.63, 'Pm': 1.62, 'Sm': 1.62, 'Eu': 1.61, 'Gd': 1.6, 'Tb': 1.6, 'Dy': 1.59, 'Ho': 1.58, 'Er': 1.57, 'Tm': 1.57, 'Yb': 1.56, 'Lu': 1.55, 'Hf': 1.428, 'Ta': 1.37, 'W': 1.355, 'Re': 1.345, 'Os': 1.35, 'Ir': 1.3, 'Pt': 1.22, 'Au': 1.2, 'Hg': 1.316, 'Tl': 1.58, 'Pb': 1.565, 'Bi': 1.535, 'Po': 1.45, 'At': 1.44}
		xyz = readFile(file)
		if is_overlapping(xyz, t, cov):
			kk+=1
			os.system('rm '+str(file))
#			print("Molecule with overlapping.")
		else:
			os.system('mv '+str(file)+' filtered')
	print(kk)					

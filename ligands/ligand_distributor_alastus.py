#!/usr/bin/python

from glob import glob
import sys
import os

print(sys.argv)
#if len(sys.argv) != 11:
#	print("Wrong number of parameters");
#	print("\nUsage: \n")
#	print("\t$ ./script input_xyz mes.xyz num_particles1 min_dist1 cps.xyz num_particles2 min_dist2 num_samples \n\n");
#	print("\t python3 ligand_distributor3.py mes.xyz 5 3.5 cp.xyz 2 2.6 10\n");
#	print("\t i.e. $ python3 ligand_distributor3.py opt mes.xyz 0 2.7 cp.xyz 5 2.7 100000 \n");
#	exit();


import numpy as np
from tools_alastus import *

baseFolder = glob(str(sys.argv[1])+'/*.xyz')
baseFolder.sort()



inputMol2 = sys.argv[2]
num_p1= int(sys.argv[3])
where1 = str(sys.argv[5])
min_dist2 = float(sys.argv[4])
inputMol3 = sys.argv[6]
num_p2 = int(sys.argv[7])
where2 = str(sys.argv[9])
min_dist1 = float(sys.argv[8])
num_samples = int(sys.argv[10])




natoms_par1, atomtypes_par1, coords_par1 = xyzRead(inputMol2)

natoms_par2, atomtypes_par2, coords_par2 = xyzRead(inputMol3)

num_p=num_p1+num_p2
#print("Running...")

factor=min_dist2/min_dist1
start=0
numm=num_samples+start
#print("\nComputing samples:")
for s in range(start,numm):
	inputMol1 = np.random.choice(baseFolder)
	natoms, atomtypes, coords = xyzRead(inputMol1)
	#xyz = evolveParticles4(num_p, maxRadius(coords)+min_dist1, coords)
	xyz = evolveParticles_alastus(num_p, maxRadius(coords)+min_dist1, coords, num_p1, num_p2, where1, where2, atomtypes)
	#array_sum = np.sum(xyz)
	#array_has_nan = np.isnan(array_sum)
	#print(s,"Evolve Particles has NaN: ", array_has_nan)
	##xyz = rotMatrix(xyz)
	#array_sum = np.sum(xyz)
	#array_has_nan = np.isnan(array_sum)
	#print(s,"Rot Matrix has NaN: ", array_has_nan)
	#sample = getSample4(xyz, min_dist1, coords) #ESTES SAO OS PONTOS ONDE O LIGANTE IRA
	sample = getSample_alastus(xyz, min_dist1, coords,num_p1,num_p2, where1,where2) #ESTES SAO OS PONTOS ONDE O LIGANTE IRA
	#array_sum = np.sum(sample)
	#array_has_nan = np.isnan(array_sum)
	#print(s,"Get Samples has NaN: ", array_has_nan)
	

	#np.random.shuffle(sample)
	#np.random.shuffle(sample)
	
	sample1, atomtypes_par1 = adjustMol1(sample,atomtypes_par1,coords_par1,num_p1,factor, coords)
	sample2, atomtypes_par2 = adjustMol2(sample,atomtypes_par2,coords_par2,num_p2,num_p1, coords)
	if (s+1)<10:
		n="000000"+str(s+1)
	if (s+1)<100 and (s+1)>9:
		n="00000"+str(s+1)
	if (s+1)<1000 and (s+1)>99:
		n="0000"+str(s+1)
	if (s+1)<10000 and (s+1)>999:
		n="000"+str(s+1)
	if (s+1)<100000 and (s+1)>9999:
		n="00"+str(s+1)
	if (s+1)<1000000 and (s+1)>99999:
		n="0"+str(s+1)


	fileName = 'coords_'+str(n)+'.xyz'
	#print("Sphere deformation %d - [%s]" %(s+1, fileName))

	with open(fileName, 'w') as f:
		#f.write("  %d X_CG, Y_CG, Z_CG 0.000000 0.000000 0.000000\n\n" %(natoms+(num_p1*natoms_par1)+(num_p2*natoms_par2)))
		f.write("  %d \n\n" %(natoms+(num_p1*natoms_par1)+(num_p2*natoms_par2)))
		for coor, ato in zip(coords, atomtypes):
			f.write("%s \t%.18g \t%.18g \t%.18g\n" %(ato, coor[0], coor[1], coor[2]))
		for coor, ato in zip(sample1, atomtypes_par1):
			f.write("%s \t%.18g \t%.18g \t%.18g\n" %(ato, coor[0], coor[1], coor[2]))
		for coor, ato in zip(sample2, atomtypes_par2):
			f.write("%s \t%.18g \t%.18g \t%.18g\n" %(ato, coor[0], coor[1], coor[2]))

os.system('mkdir geom')
os.system('mv coords* geom')






#!/usr/bin/python
import os
import time
import sys
import matplotlib.cm as cm
import matplotlib.pyplot as plt


if len(sys.argv) != 3:
    print("\nUsage: \n")
    print("\t\t$ python main.py 1 10 \n\n")
    print("- 1 and 10 represent the initial end final step you whant to execute.")
    print("- Steps 7 and 10 will stop the code and call for external intervention.")
    print("- The work folder most me the provided cluster_assembler (or a copy).")
    exit()

start=int(sys.argv[1])
end=int(sys.argv[2])
list=range(start,end+1)
if start<1 or end>10 or start>end:
    print("\n\n ERROR: The interval you provided is not valid...\n\n")
    exit() 


#1. Core generation that can be performed via
##Permutation
##ABCluster
if 1 in list:
	print("1. Metalic Core Generation:")
	print("\t 1 - Already generated using external source.")
	print("\t 2 - Generate now via abcluster.\n")
	option = input("Type your option: ")
	if int(option)==1:
		adress=input("Type the adress: ")
	if int(option)==2:
		print("The submission script in cluster_assembler/core/job.pbs will be executed now.")
		print("The version originaly there was set for very speciffic computational facility,")
		print("and probably will need some adaptations to be runned at other machines.\n")
		cont=input("If the script is set, press any key to continue...")
		os.system("python core/abcluster_submission.py cube")
		adress="all_xyz"
		
		
	if int(option)<1 or int(option)>2:
		exit("Invalid input...")
	

#2. Connectivity test to exclude systems that not correspond to the expect number of metalic atoms
if 2 in list:
	print("2. Connectivity test:")
	os.system("python  core/connectivity.py "+adress)
	print("\nBefore you continue, check filter_result to see if all XYZ have been processed.")
	cont=input("If yes, press any key to continue...")

#3. K-means clustering to select relevant cores to use
if 3 in list:
	exit("WIP...")
	
#4. Ligands distribution around the metalic core
if 4 in list:
	exit("WIP...")

#5. Overlap Filter
if 5 in list:
	exit("WIP...")

#6. K-means selection of nanoclusters to optimize via DFT
if 6 in list:
	exit("WIP...")

#7. DFT optimization with light/weak criteria
if 7 in list:
	exit("WIP...")

#8. Donnectivity verification to check if any chemical bond was made or broken during DFT optimization
if 8 in list:
	exit("WIP...")
	

#9. K-means selection of nanoclusters to post optimization via DFT
if 9 in list:
	exit("WIP...")

#10. DFT optimization with tight/strong criteria
if 10 in list:
	exit("WIP...")
	
	
exit("---DONE---")

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

	
	
print("""    ~?JJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJJ?!     
   P&#P55555555555555555555555555555555555B&#:    
   P&P                                    ?&B:    
   P&P            ^YPPPPPPPP5!            J&B:    
   P&P           7#&5??????J#&J           J&B:    
   P&P          J&#7        ~B&5:         J&B:    
   P&P   ^!~~~~5&B~          :P&G!~~~~^   J&B:    
   P&P   JBBBBB##J            !#&BBBBBP.  J&B:    
   P&P   ......7##J          7##Y......   J&B:    
   P&P          ~B&5:      .J##?          J&B:    
   P&P           :P&BGGGGGGG&#!           J&B:    
   P&P            .!7777777?B#5.          J&B:    
   P&P                      ^G&G^         J&B:    
   P&P                       .?!.         ?&B:    
   P&B?????????????^ .^^^^. .?????????????P&#:    
   7PPPPPPPPPPPPPPG! .~~~~: :PPPPPPPPPPPPPPPY.   
""")

print("\n\n         QTNano Cluster Assembler \n\n")

#1. Core generation that can be performed via
##Permutation
##ABCluster
if 1 in list:
	print("1. Metalic Core Generation:")
	print("\t 1 - Already generated using external source.")
	print("\t 2 - Generate now via abcluster [advanced].\n")
	option = input("Type your option: ")
	if int(option)==1:
		adress=input("Type the adress: ")
	if int(option)==2:
		print("""
##############################################################################
##  Autor comments:                                                         ##
##   ABCluster is a very usifull tool that needs some training to be used.  ##
##  We strogly recomend the user to visit                                   ##
##                 http://www.zhjun-sci.com/abcluster/doc/                  ##
##  and try to unsderstand exactly how the program works, how to install it ##
##  and to run some tests before using it here                              ##
##  We thank Zhang's group for making this incredible tool available or the ##
##  materials community!                                                    ##
##############################################################################""")
		os.system("cd core && python3 abcluster_unary.py")
		print("\nThe submission script in cluster_assembler/core/job.pbs will be executed now.")
		print("The version originaly there was set for a very specific computational facility,")
		print("and probably will need some in house adaptations to be runned.\n")
		cont=input("If the script is set, press any key to continue...")
		os.system("python3 core/abcluster_submission.py cube")
		adress="all_xyz"
		
		
	if int(option)<1 or int(option)>2:
		exit("Invalid input...")
	

#2. Connectivity test to exclude systems that not correspond to the expect number of metalic atoms
if 2 in list:
	print("2. Connectivity test:")
	os.system("python3  core/connectivity.py "+adress)
	print("\nBefore you continue, check filter_result to see if all XYZ have been processed.")
	cont=input("If yes, press any key to continue...")

#3. K-means clustering to select relevant cores to use
if 3 in list:
	print("3. K-means clustering to select relevant cores to use:")
	if adress != "all_xyz":
		os.system("mv "+adress+" all_xyz ")
	os.system("python3  core/clustering.py")
	
#4. Ligands distribution around the metalic core
### OBS.: The comented ines herever to experimental version of the ligand distributor that tries to bias the element where the ligand will be fixed.
###       IT IS A EXPERIMENTAL FEATURE AND SHOULD NOT BE USED (UNLESS YOU ARE SURE AND DID SOME PROPER TESTS). 
if 4 in list:
	print("4. Ligands distribution around the metalic core")
	print("\nThis step will use the already criated and filtered structures selected in step 3.")
	print("Check the place where those structures are saved.")
	inp1=input("Inform the folder with selectec metalic cores:")
	inp2=input("Inform the adress of the XYZ of the first ligand:")
	inp3=input("Inform how many of this ligand to add:")
	inp4=input("Inform a trial bondlegth:")
	#el1=input("Chemical specie to bond:")
	test=input("Add a secund ligand? (Y/N)\n")
	if test=="Y":
		inp5=input("Inform the adress of the XYZ of the second ligand:")
		inp6=input("Inform how many of this ligand to add:")
		inp7=input("Inform a trial bondlegth:")
		#el2=input("Chemical specie to bond:")
	else:
		inp5=inp2
		inp6="0"
		inp7="1.0"
		#el2=el1
	inp8=input("How much samples to generate? ")
	#print("====> Calling $"+"python3  ligands/ligand_distributor_alastus.py "+inp1+" "+inp2+" "+inp3+" "+inp4+" "+el1+" "+inp5+" "+inp6+" "+inp7+" "+el2+" "+inp8)
	#os.system("python3  ligands/ligand_distributor_alastus.py "+inp1+" "+inp2+" "+inp3+" "+inp4+" "+el1+" "+inp5+" "+inp6+" "+inp7+" "+el2+" "+inp8)
	print("====> Calling $"+"python3  ligands/ligand_distributor3.py "+inp1+" "+inp2+" "+inp3+" "+inp4+" "+inp5+" "+inp6+" "+inp7+" "+inp8)
	os.system("python3  ligands/ligand_distributor3.py "+inp1+" "+inp2+" "+inp3+" "+inp4+" "+inp5+" "+inp6+" "+inp7+" "+inp8)
	
#5. Overlap Filter
if 5 in list:
	print("5. Overlap Filter")
	os.system("cp filters/overlapping.py geom/.")
	os.system("cd geom && python3 overlapping.py")
	os.system("cp -r geom/filtered filtered_step_5")
	print("\nBefore continuing, check filtered_step_5 to see if all XYZ have been processed.")
	cont=input("If yes, press any key to continue...")

#6. K-means selection of nanoclusters to optimize via DFT
if 6 in list:
	print("6. K-means selection of nanoclusters to optimize via DFT")
	inp1=input("Inform the folder with the result from the Overlap Filter (standard name is filtered_step_5):")
	inp2=input("Inform how many representative structures to select:")
	os.system("cp filters/kmeans/* .")
	os.system("python3 silscript.py 1 "+inp1+" "+inp2)
	os.system("mv "+inp1+"/selected_"+inp1+" to_dft_light")
	os.system("rm -rf job_kmeans_new mol.txt silscript.py tools.py")

#7. DFT optimization with light/weak criteria
if 7 in list:
	print("7. DFT optimization with light/weak criteria")
	print("\nFor generality, this step is to be performed by the user.")
	print("Take care of organazing the outiputs as informed on a single folder with all optimized geometries.")
	exit("Please, perform the apropriate DFT calculations and restart the program at step 8...")

#8. Connectivity verification to check if any chemical bond was made or broken during DFT optimization
if 8 in list:
	print("8. Connectivity verification to check if any chemical bond was made or broken during DFT optimization")
	print("On this process, you will be asked to provide a folder with structures optimized with DFT,")
	print("as well  as  a reference structure that has the  expected chemical formula. This structure")
	print("can be buld specificaly for this finality, just take care to preserve the atomic ordering.")
	cont=input("Press any key to continue if you have this information ready...")
	os.system("python3 filters/connectivity.py")
	
#9. K-means selection of nanoclusters to post optimization via DFT
if 9 in list:
	print("9. K-means selection of nanoclusters to post optimization via DFT")
	inp1=input("Inform the folder with the result from the Connectivity Filter (standard name is ********):")
	inp2=input("Inform how many representative structures to select:")
	os.system("cp filters/kmeans/* .")
	os.system("python3 silscript.py 1 "+inp1+" "+inp2)
	os.system("mv "+inp1+"/selected_"+inp1+" to_dft_tight")
	os.system("rm -rf job_kmeans_new mol.txt silscript.py tools.py")

#10. DFT optimization with tight/strong criteria
if 10 in list:
	print("10. DFT optimization with tight/strong criteria")
	print("\nFor generality, this step is to be performed by the user.")
	print("\n\n\t\t\t Thanks for using our code!!!\n\n")
	exit("Please, perform the apropriate DFT calculations...")
	
	
exit("---DONE---")

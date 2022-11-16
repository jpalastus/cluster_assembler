#!/usr/bin/python
import os
import time
import sys
import matplotlib.cm as cm
import matplotlib.pyplot as plt



if len(sys.argv) != 3:
    print("\nUsage: \n")
    print("\t\t$ python main.py 1 10 \n\n")
    print("- Steps 1 and 10 represent the initial end final steps you whant to execute.")
    print("- Steps 7 and 10 will stop the code and call for external intervention.")
    print("- The work folder must be provided, i.e., cluster_assembler (or a copy).")
    exit()

start=int(sys.argv[1])
end=int(sys.argv[2])
adress="xxxxx"
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
	print("1. Core Generation:")
	print("\t 1 - Already generated using an external source.")
	print("\t 2 - Generate now via ABCluster [advanced].\n")
	option = input("Type your option: ")
	if int(option)==1:
		adress=input("Type the adress: ")
	if int(option)==2:
		print("""
##############################################################################
##  Autors comments:                                                        ##
##  ABCluster is a very useful and powerful software, developed by Jun      ##
## Zhang to perform global optimization and conformation search. Therefore, ##
## we strogly recomend the user to visit the following site for additional  ##
## informations about the software functionalization:                       ##               
##                 http://www.zhjun-sci.com/abcluster/doc/                  ## 
## Finally, we thank Zhang's group for making this incredible tool          ##
## available for the materials community!                                   ##
##############################################################################""")
		os.system("cd core && python3 abcluster_unary.py")
		print("\nThe submission script in cluster_assembler/core/job.pbs will be executed now.")
		print("This original version  was set for a very specific computational facility,")
		print("and probably will need some in-house adaptations to be runned.\n")
		cont=input("If the script is set, press any key to continue...")
		os.system("python3 core/abcluster_submission.py cube")
		adress="all_xyz"
		
		
	if int(option)<1 or int(option)>2:
		exit("Invalid input...")
	

#2. Connectivity test to exclude systems that not correspond to the expect number of core atoms
if 2 in list:
	print("2. Connectivity test:")
	os.system("python3  core/connectivity.py "+adress)
	print("\nBefore you continue, check filter_result to see if all XYZ have been processed.")
	cont=input("If yes, press any key to continue...")

#3. K-means clustering to select relevant cores to use
if 3 in list:
	print("3. K-means clustering to select relevant cores to use:")
#	if adress != "all_xyz":
#		os.system("mv "+adress+" all_xyz ")
	os.system("python3  core/clustering.py")
	
#4. Ligands distribution around the core
### P.S.: The following lines are experimental version of the ligand distributor that tries to bias the element where the ligand will be fixed.
###       IT IS ON DEVELOPMENT AND SHOULD NOT BE USED (UNLESS YOU ARE SURE AND DID SOME PREVIOUS PROPER TESTS). 
if 4 in list:
	print("4. Ligands distribution around the core")
	print("\nThis step will use the already created and filtered structures selected in Step 3.")
	print("Please, check the place where those structures are saved.")
	print("\nWould you like to indicate in which atomic species the ligand should be attached?(EXPERIMENTAL FEATURE)")
	option=input("Type Y/N (***Y implies in a W.I.P. feature***):")
	inp1=input("Inform the folder with selected cores:")
	print("The XYZ files with the ligands should be prepared as follows:")
	print("   1) The origen ((0,0,0)) should be the point from which the ligand will be bind.")
	print("   2) The negative x direction should represent the direction in which the ligand will be attached to the cluster.")
	inp2=input("Inform the adress of the XYZ of the first ligand:")
	inp3=input("Inform how many of this ligand to add:")
	inp4=input("Inform a trial bondlength:")
	if option=="Y":
		el1=input("Chemical specie to bond:")
	test=input("Add a second ligand? (Y/N)\n")
	if test=="Y":
		inp5=input("Inform the adress of the XYZ of the second ligand:")
		inp6=input("Inform how many of this ligand to add:")
		inp7=input("Inform a trial bondlength:")
		if option=="Y":
			el2=input("Chemical specie to bond:")
	else:
		inp5=inp2
		inp6="0"
		inp7="1.0"
		if option=="Y":
			el2=el1
	inp8=input("How much samples to generate? ")
	if option=="Y":
		print("====> Calling $"+"python3  ligands/ligand_distributor_alastus.py "+inp1+" "+inp2+" "+inp3+" "+inp4+" "+el1+" "+inp5+" "+inp6+" "+inp7+" "+el2+" "+inp8)
		os.system("python3  ligands/ligand_distributor_alastus.py "+inp1+" "+inp2+" "+inp3+" "+inp4+" "+el1+" "+inp5+" "+inp6+" "+inp7+" "+el2+" "+inp8)
	else:
		print("====> Calling $"+"python3  ligands/ligand_distributor3.py "+inp1+" "+inp2+" "+inp3+" "+inp4+" "+inp5+" "+inp6+" "+inp7+" "+inp8)
		os.system("python3  ligands/ligand_distributor3.py "+inp1+" "+inp2+" "+inp3+" "+inp4+" "+inp5+" "+inp6+" "+inp7+" "+inp8)
	
#5. Overlap Filter
if 5 in list:
	print("5. Overlap Filter")
	os.system("cp filters/overlapping.py geom/.")
	os.system("cd geom && python3 overlapping.py")
	os.system("cp -r geom/filtered filtered_step_5")
	print("\nBefore continuing, check the filtered_step_5 folder to see if all XYZ have been processed.")
	cont=input("If yes, press any key to continue...")

#6. K-means selection of nanoclusters to optimize via DFT
if 6 in list:
	print("6. K-means selection to optimize via DFT")
	inp1=input("Inform the folder with previous results from the Overlap Filter (standard name is filtered_step_5):")
	inp2=input("Inform how many representative structures to select:")
	os.system("cp filters/kmeans/* .")
	os.system("python3 silscript.py 1 "+inp1+" "+inp2)
	os.system("mv "+inp1+"/selected_"+inp1+" to_dft_light")
	os.system("rm -rf job_kmeans_new silscript.py tools.py")

#7. DFT optimization with light/weak criteria
if 7 in list:
	print("7. DFT optimization with light/weak criteria")
	print("\nFor generality, this step is to be external performed by the user.")
	print("Please, pay attention of outputs organizatioan as should be informed on a single folder with all optimized geometries.")
	exit("Please, perform the DFT calculations and restart the program at Step 8...")

#8. Connectivity verification to check if any chemical bond was made or broken during DFT optimization
if 8 in list:
	print("8. Connectivity filter to verify if any chemical bond was made or broken during DFT optimization")
	print("On this process, you will be asked to provide a folder with the DFT optmized structures,")
	print("as well as a reference structure that has the expected chemical formula. This structure")
	print("can be buld specifically for this finality, just pay attention to preserve the atomic ordering.")
	cont=input("Press any key to continue, if you have this information ready...")
	os.system("python3 filters/connectivity.py")
	
#9. K-means selection to post-optimization via DFT 
if 9 in list:
	print("9. K-means selection to post-optimization via DFT")
	inp1=input("Inform the folder with the results from the Connectivity Filter (standard name is final_representatives):")
	inp2=input("Inform how many representatives structures to select:")
	os.system("cp filters/kmeans/* .")
	os.system("python3 silscript.py 1 "+inp1+" "+inp2)
	os.system("mv "+inp1+"/selected_"+inp1+" to_dft_tight")
	os.system("rm -rf job_kmeans_new silscript.py tools.py")

#10. DFT optimization with tight/strong criteria
if 10 in list:
	print("10. DFT optimization with tight/strong criteria")
	print("\nFor generality, this step should be performed externally by the user.")
	print("\n\n\t\t\t Thanks for using our code!!!\n\n")
	exit("Please, perform the DFT calculations...")
	
	
exit("---DONE---")

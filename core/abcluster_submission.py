import os
import sys
import glob
import time

print("\n\n --- AUTOMATION OF ABCLUSTER USAGE --- ")
print("ATENTION: Some HPC centers have laws against scripts that submit jobs.")
cont=input("Type 'YES' if you want to continue: ")
if cont != "YES":
	exit("Leaving...")

os.system("mkdir all_xyz")
#print("Prepare folder for each execution inside 'core'. The folders most contain a adapted copy of job.pbs and abcluster.inp.")
cont=input("What name you put on the output file (first entry on the ABCLUSTER input):")

###Run it Local
i=1
for folder in glob.glob("core/*/"):
	os.system("cd "+folder+"&& ./job.sh ")
	os.system("cd "+folder+cont+"_LM/ && for file in *.xyz; do cp $file ../../../all_xyz/"+str(i)+"$file; done")
	i=i+1

	
####Run in cluster
#for folder in glob.glob("core/*/"):
#	os.system("cd "+folder+"&& qsub job.pbs")
#time.sleep(3600)  # tune this value so the cluster waits the computations finish 
#i=1
#for folder in glob.glob("core/*/"):
#	os.system("cd "+folder+cont+"_LM/ && for file in *.xyz; do cp $file ../../../all_xyz/"+str(i)+"$file; done")
#	i=i+1

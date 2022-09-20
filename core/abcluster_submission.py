import os
import sys

NUM=9

################### CUBE
for k in range(0,NUM+1):
	Type=str(sys.argv[1]+str(k))
	os.system("cd "+Type+"&& qsub job.pbs")
###################



"""
################### SPHERE
for k in range(1,NUM+1):
	Type='sphere'+str(k)
	os.system("qsub "+Type+'/job.pbs')
###################


################### LINE
for k in range(1,NUM+1):
	Type='line'+str(k)
	os.system("qsub "+Type+'/job.pbs')
###################


################### PLANE
for k in range(1,NUM+1):
	Type='plane'+str(k)
	os.system("qsub "+Type+'/job.pbs')
###################


################### RING
for k in range(1,NUM+1):
	Type='ring'+str(k)
	os.system("qsub "+Type+'/job.pbs')
###################
"""

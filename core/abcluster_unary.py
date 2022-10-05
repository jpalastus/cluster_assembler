import os

MNUMCALC='200'
el1='Cu'
n1='3'
el2='Zn'
n2='4'
NUM=9
Cube=" 3 3 3"
Plane=" 3 3"


FNAME=str(el1)+str(n1)+str(el2)+str(n2)
COMPOSITION=str(el1)+' '+str(n1)+' '+str(el2)+' '+str(n2)
with open("abcluster.inp" ,'r+') as f:   
	lines = f.readlines()
f.close()

lines = [w.replace('FNAME', FNAME) for w in lines]
lines = [w.replace('COMPOSITION', COMPOSITION) for w in lines]
lines = [w.replace('MNUMCALC', MNUMCALC) for w in lines]

with open("job.pbs" ,'r+') as fi:   
	lin = fi.readlines()
fi.close()

lin = [w.replace('FNAME', FNAME) for w in lin]

################### CUBE
for k in range(0,NUM+1):
	Type='cube'+str(k)
	os.system("mkdir "+Type)
	l = [w.replace('STRUCTYPE', Type[:-1]+str(Cube)) for w in lines]
	new= open(Type+'/'+str(el1)+str(n1)+str(el2)+str(n2)+'.inp', 'w+')
	for i in l:
		new.write(i) 
	new.close()

	new= open(Type+'/job.pbs', 'w+')
	for i in lin:
		new.write(i) 
	new.close()
#	os.system("qsub "+Type+'/job.pbs')
###################


################### SPHERE
for k in range(0,NUM+1):
	Type='sphere'+str(k)
	os.system("mkdir "+Type)
	l = [w.replace('STRUCTYPE', Type[:-1]) for w in lines]
	new= open(Type+'/'+str(el1)+str(n1)+str(el2)+str(n2)+'.inp', 'w+')
	for i in l:
		new.write(i) 
	new.close()

	new= open(Type+'/job.pbs', 'w+')
	for i in lin:
		new.write(i) 
	new.close()
#	os.system("qsub "+Type+'/job.pbs')
###################


################### LINE
for k in range(0,NUM+1):
	Type='line'+str(k)
	os.system("mkdir "+Type)
	l = [w.replace('STRUCTYPE', Type[:-1]) for w in lines]
	new= open(Type+'/'+str(el1)+str(n1)+str(el2)+str(n2)+'.inp', 'w+')
	for i in l:
		new.write(i) 
	new.close()

	new= open(Type+'/job.pbs', 'w+')
	for i in lin:
		new.write(i) 
	new.close()
	#os.system("qsub "+Type+'/job.pbs')
###################


################### PLANE
for k in range(0,NUM+1):
	Type='plane'+str(k)
	os.system("mkdir "+Type)
	l = [w.replace('STRUCTYPE', Type[:-1]+str(Plane)) for w in lines]
	new= open(Type+'/'+str(el1)+str(n1)+str(el2)+str(n2)+'.inp', 'w+')
	for i in l:
		new.write(i) 
	new.close()

	new= open(Type+'/job.pbs', 'w+')
	for i in lin:
		new.write(i) 
	new.close()
#	os.system("qsub "+Type+'/job.pbs')
###################



################### RING
for k in range(0,NUM+1):
	Type='ring'+str(k)
	os.system("mkdir "+Type)
	l = [w.replace('STRUCTYPE', Type[:-1]) for w in lines]
	new= open(Type+'/'+str(el1)+str(n1)+str(el2)+str(n2)+'.inp', 'w+')
	for i in l:
		new.write(i) 
	new.close()

	new= open(Type+'/job.pbs', 'w+')
	for i in lin:
		new.write(i) 
	new.close()
#	os.system("qsub "+Type+'/job.pbs')
###################


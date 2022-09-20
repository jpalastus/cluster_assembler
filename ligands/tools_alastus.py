# -*- Coding: UTF-8 -*-
#coding: utf-8

import numpy as np
import sys
import secrets


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


def maxRadius(coords):
	norm = np.linalg.norm(coords,axis=1)
	return np.amax(norm)


def evolveParticles_alastus(num_p, radius, coords, num_p1, num_p2, where1, where2, atomTypes):
	particles = np.random.rand(num_p,3)-0.5
	norm = np.linalg.norm(particles,axis=1)
	norm = norm.reshape((num_p,1))
	norm = np.repeat(norm,3,axis=1)
	norm /= radius
	if where1 in atomTypes:
		pos=[]
		for i in range(len(atomTypes)):
			if atomTypes[i]==where1:
				pos.append(i)
		for i in range(num_p1):
			ipos=secrets.choice(pos)
			particles[i]=1.2*coords[ipos]
	if where2 in atomTypes:
		pos=[]
		for i in range(len(atomTypes)):
			if atomTypes[i]==where2:
				pos.append(i)
		for i in range(num_p1, num_p):
			ipos=secrets.choice(pos)
			particles[i]=1.2*coords[ipos]
	
	particles = np.divide(particles,norm)
	#array_sum = np.sum(particles)
	#array_has_nan = np.isnan(array_sum)
	#print("Inside Evolve Particles has NaN: ", array_has_nan)
	
	t = 0
    
	while True:
	
		step = np.zeros((num_p,3))
		mdistv = []
		mindistV = []
		for i in range(num_p):
			diff = particles[i,:] - particles
			norm = np.linalg.norm(diff,axis=1)/radius
			norm[i] = sys.maxsize
			mindistV.append(np.amin(norm))
			sim = np.exp(-norm).reshape((num_p,1))
			step -= sim*diff / norm.reshape((num_p,1))

		dmin = np.amin(mindistV)
		dmax = np.amax(mindistV)
		ddiff = abs(dmin-dmax)
        

		if (ddiff < 0.01 or t>5000):
            #print("\n\nThe shortest distances between 1-neighbor particles (before deformation): ")
            #print(mindistV)
			break
		t += 1
		particles += step
		for i in range(num_p):
			norm = np.linalg.norm(particles[i,:])
			norm /= radius
			particles[i,:] /= norm

	return particles

def evolveParticles4(num_p, radius, coords):
	particles = np.random.rand(num_p,3)-0.5
	norm = np.linalg.norm(particles,axis=1)
	norm = norm.reshape((num_p,1))
	norm = np.repeat(norm,3,axis=1)
	norm /= radius
	particles = np.divide(particles,norm)
	t = 0
    
	while True:
		step = np.zeros((num_p,3))
		mdistv = []
		mindistV = []
		for i in range(num_p):
			diff = particles[i,:] - particles
			norm = np.linalg.norm(diff,axis=1)/radius
			norm[i] = sys.maxsize
			mindistV.append(np.amin(norm))
			sim = np.exp(-norm).reshape((num_p,1))
			step -= sim*diff / norm.reshape((num_p,1))

		dmin = np.amin(mindistV)
		dmax = np.amax(mindistV)
		ddiff = abs(dmin-dmax)
        

		if (ddiff < 0.01 or t>5000):
            #print("\n\nThe shortest distances between 1-neighbor particles (before deformation): ")
            #print(mindistV)
			break
		t += 1
		particles += step
		for i in range(num_p):
			norm = np.linalg.norm(particles[i,:])
			norm /= radius
			particles[i,:] /= norm

	return particles

def getSample_alastus(xyz, radius, coords,num_p1,num_p2, where1,where2):
	num_p = np.shape(xyz)[0]
	num_a = np.shape(coords)[0]
    
    # expanding the cluster with radius
	norm = np.linalg.norm(coords,axis=1).reshape((num_a,1))
	inc = np.divide(coords,norm.repeat(3,axis=1))
	new_coords = coords# + np.multiply(inc,radius)

	particles = xyz
	step = np.zeros((num_p,3))
	learning = -np.ones(num_p)*0.1
	signal = np.ones(num_p)
	
	t = 1
	while True:
		diferenca = np.zeros(num_p)
		for i in range(num_p):
			diff = particles[i,:] - new_coords
			norm = np.linalg.norm(diff,axis=1)
			
			j1=0
			for i1 in range(1, len(norm)):
				if norm[j1]>norm[i1]:
					j1=i1
			#mindist1 = np.amin(norm)
			#if len(np.where(norm == mindist1))==1:
			#	j1 = np.where(norm == mindist1)
			#else:
			#	j1 = np.where(norm == mindist1)[0]
			j1 = np.array([j1])
			norm_j1 = np.linalg.norm(new_coords[j1,:])
			norm_i = np.linalg.norm(particles[i,:])
			diff_ij = norm_j1 - norm_i
			
			diferenca[i] = norm[j1]
            
			if (radius - diferenca[i])*signal[i] > 0:
				signal[i] = -signal[i]
				learning[i] *= -0.7

			normalization = norm_i+learning[i]*diferenca[i]
			if normalization < norm_j1:
				normalization = norm_j1
			particles[i,:] /= norm_i
			particles[i,:] *= normalization
		t += 1
		if (t>200):
			break
	
	return particles

def getSample4(xyz, radius, coords):
	num_p = np.shape(xyz)[0]
	num_a = np.shape(coords)[0]
    
    # expanding the cluster with radius
	norm = np.linalg.norm(coords,axis=1).reshape((num_a,1))
	inc = np.divide(coords,norm.repeat(3,axis=1))
	new_coords = coords# + np.multiply(inc,radius)

	particles = xyz
	step = np.zeros((num_p,3))
	learning = -np.ones(num_p)*0.1
	signal = np.ones(num_p)
	t = 1
	while True:
		diferenca = np.zeros(num_p)
		for i in range(num_p):
			diff = particles[i,:] - new_coords
			norm = np.linalg.norm(diff,axis=1)

			mindist1 = np.amin(norm)
			j1 = np.where(norm == mindist1)
			norm_j1 = np.linalg.norm(new_coords[j1,:])
			norm_i = np.linalg.norm(particles[i,:])
			diff_ij = norm_j1 - norm_i

			diferenca[i] = norm[j1]
            
			if (radius - diferenca[i])*signal[i] > 0:
				signal[i] = -signal[i]
				learning[i] *= -0.7

			normalization = norm_i+learning[i]*diferenca[i]
			if normalization < norm_j1:
				normalization = norm_j1
			particles[i,:] /= norm_i
			particles[i,:] *= normalization
		t += 1
		if (t>200):
			break

	return particles

def distMin(xyz, num_p):
	dist = np.ones((num_p))*10
	for i in range(num_p):
		for j in range(num_p):
			if j==i:
				continue
			norm = np.linalg.norm(xyz[i,:] - xyz[j,:])
			if norm < dist[i]:
				dist[i] = norm
	return dist

import math
from random import random

def rotMatrix(coords):
	theta = random()*math.pi*2
	co = math.cos(theta)
	si = math.sin(theta)
	rx = np.array([[1,0,0],[0,co,-si],[0, si, co]])
	ry = np.array([[co,0,si],[0,1,0],[-si, 0, co]])
	rz = np.array([[co,-si,0],[si,co,0],[0, 0, 1]])
	R = np.matmul(rz, np.matmul(ry,rx))
	newcoords = np.matmul(coords,R)
	return newcoords


def rotation_matrix_from_vectors(vec1, vec2):
	""" Find the rotation matrix that aligns vec1 to vec2
	:param vec1: A 3d "source" vector
	:param vec2: A 3d "destination" vector
	:return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
	"""
	a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (vec2 / np.linalg.norm(vec2)).reshape(3)
	v = np.cross(a, b)
	c = np.dot(a, b)
	s = np.linalg.norm(v)
	kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
	rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
	return rotation_matrix


def adjustMol1(xyz,atomtypes_par,coords_par,num_p1,factor, coords):
	num_p = num_p1 #numero de pontos onde o ligante ira
	num_a = np.shape(atomtypes_par)[0] #numero de atomos no ligante
	xyz_new = []
	atomTypes = []
	ato=0
	
	for i in range(num_p):
		norm = np.linalg.norm(xyz[i,:]) #distancia de cada ponto da origem
		vector1=np.array([0.0,0.0,1.0],dtype=float)
		
		#closest=0
		#dist0=np.linalg.norm(xyz[i]-coords[0])
		#for j in range(1, len(coords)):
		#	disti=np.linalg.norm(xyz[i]-coords[j])
		#	if disti<dist0:
		#		dist0=disti
		#		closest=j
		#print(closest)
		#exit()
		
		repul=np.array([0.0,0.0,0.0],dtype=float)
		for j in range(len(coords)):
			disti=np.linalg.norm(xyz[i]-coords[j])
			repul+=(1.0/disti**8)*(xyz[i]-coords[j])
		
		
		#vector2=np.array(factor*(xyz[i]-coords[closest])/(np.linalg.norm(factor*(xyz[i]-coords[closest]))),dtype=float)
		vector2=np.array(factor*repul/(np.linalg.norm(factor*repul)),dtype=float)
		R=rotation_matrix_from_vectors(vector2, vector1)
		for p in range(len(coords_par)):
			coords_par2=np.dot(coords_par, R)
			xyz_new.append(coords_par2[p]+xyz[ato]*factor)
			atomTypes.append(atomtypes_par[p])
		ato += 1
	return np.array(xyz_new), atomTypes

def adjustMol2(xyz,atomtypes_par,coords_par,num_p2,num_p1, coords):
	num_p = num_p2 #numero de pontos onde o ligante ira
	num_a = np.shape(atomtypes_par)[0] #numero de atomos no ligante
	xyz_new = []
	atomTypes = []
	ato=num_p1
	for i in range(num_p):
		norm = np.linalg.norm(xyz[i+num_p1,:]) #distancia de cada ponto da origem
		vector1=np.array([0.0,0.0,1.0],dtype=float)
		
		#closest=0
		#dist0=np.linalg.norm(xyz[i]-coords[0])
		#for j in range(1, len(coords)):
		#	disti=np.linalg.norm(xyz[i]-coords[j])
		#	if disti<dist0:
		#		dist0=disti
		#		closest=j
		#print(closest)
		#exit()
		
		repul=np.array([0.0,0.0,0.0],dtype=float)
		for j in range(len(coords)):
			disti=np.linalg.norm(xyz[i+num_p1]-coords[j])
			repul+=(1.0/disti**8)*(xyz[i+num_p1]-coords[j])
		
		#vector2=np.array((xyz[i+num_p1]-coords[closest])/(np.linalg.norm(xyz[i+num_p1]-coords[closest])),dtype=float)
		vector2=np.array(repul/(np.linalg.norm(repul)),dtype=float)
		R=rotation_matrix_from_vectors(vector2, vector1)
		for p in range(len(coords_par)):
			coords_par2=np.dot(coords_par, R)
			xyz_new.append(coords_par2[p]+xyz[ato])
			atomTypes.append(atomtypes_par[p])
		ato += 1
	return np.array(xyz_new), atomTypes



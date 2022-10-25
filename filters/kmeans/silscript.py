#!/usr/bin/python
# Active Selection of Molecules (Short task 01)
# Marcos Quiles / Marinalva Soares

# INPUT1 - XYZ files (folder)
# INPUT2 - Text file - Additional information (Energy_T, Delta_E, etc.)
# INPUT3 - #number of outputs
import os
import time
start=time.time()
import sys
# print(len(sys.argv))
import matplotlib.cm as cm
import matplotlib.pyplot as plt
if len(sys.argv) != 4 and len(sys.argv) != 5:
    print("\nUsage: \n")
    print("\tOption 1: Only structural information (xyz) \n")
    print("\t\t$ python script1.py 1 folder_xyz_files #samples\n\n");
    print("\tOption 2: Structural information (xyz) + Energy_T\n")
    print("\t\t$ python script1.py 2 folder_xyz_files #samples extra_data.txt \n\n");
    print("\tOption 3: Structural information (xyz) + {Energy_T, Delta_E, m_T, ECN, d_av}\n")
    print("\t\t$ python script1.py 3 folder_xyz_files #samples extra_data.txt \n\n");
    exit();


opt = int(sys.argv[1])
if opt not in range(1,4):
    print("Wrong option\n\n");
    exit() 

params = {'eigen': 9999999,
            'n_clusters': int(sys.argv[3])}

import pandas as pd
from glob import glob
from os import makedirs, getcwd, path
from tools import *

baseFolder = glob(str(sys.argv[2])+'/*.xyz')
# print(type(baseFolder))
baseFolder.sort()
dataxyz = []
ids = []
num_files = 1

for fin in baseFolder:
    # print(fin)
    natoms, atomtypes, coords = xyzRead(fin)
    if natoms < params['eigen']:
        params['eigen'] = natoms
    mat = eigenCoulomb(fin,params['eigen'])
    dataxyz.append(mat)
    ids.append(num_files)
    num_files+=1

end = time.time()
tot=end - start
#print('para ler '+str(tot))


if opt in range(2,4):
    pdata2 = pd.read_csv(sys.argv[4], sep="\t");
    columns = pdata2.columns.tolist()
    # print(columns)
    pdata2.sort_values(columns[1], axis=0, ascending=True, inplace=True)
    print(pdata2)
    pdata2.sort_values(columns[0], axis=0, ascending=True, inplace=True)
    # ids = pdata2.values[:,0]
    if opt == 2:
        data2 = pdata2.loc[:,['Energy_T']]#.values[:,1:]
    else:
        data2 = pdata2.loc[:,['Energy_T', 'Delta_E ', 'm_T', 'ECN', 'd_av']]#.values[:,1:]
    data2 = data2.values
    X = np.concatenate((data2,np.array(dataxyz)), axis=1)
else:
    X = np.array(dataxyz)

# print(np.shape(X))

# exit()

from sklearn import cluster, datasets, mixture
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_samples, silhouette_score


X = StandardScaler().fit_transform(X) 

tsnee = TSNE(n_components=2) ####


X = tsnee.fit_transform(X) ####

kmeans = cluster.KMeans(init='random', #'k-means++', 
        n_clusters=params['n_clusters'], n_init=10, random_state=0)
# kmeans = cluster.KMeans(init='random', 
#         n_clusters=params['n_clusters'])


#########

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.set_size_inches(18, 7)

    # The 1st subplot is the silhouette plot
    # The silhouette coefficient can range from -1, 1 but in this example all
    # lie within [-0.1, 1]
ax1.set_xlim([-0.1, 1])
    # The (n_clusters+1)*10 is for inserting blank space between silhouette
    # plots of individual clusters, to demarcate them clearly.
ax1.set_ylim([0, len(X) + (params['n_clusters'] + 1) * 10])



#clusterer =cluster.KMeans(n_clusters=params['n_clusters'], random_state=10) tem o meu
cluster_labels = kmeans.fit_predict(X)

    # The silhouette_score gives the average value for all the samples.
    # This gives a perspective into the density and separation of the formed
    # clusters
silhouette_avg = silhouette_score(X, cluster_labels)
print("For n_clusters =", params['n_clusters'],
          "The average silhouette_score is :", silhouette_avg)

    # Compute the silhouette scores for each sample
sample_silhouette_values = silhouette_samples(X, cluster_labels)


y_lower = 10
for i in range(params['n_clusters']):
        # Aggregate the silhouette scores for samples belonging to
        # cluster i, and sort them
	ith_cluster_silhouette_values = \
	sample_silhouette_values[cluster_labels == i]

	ith_cluster_silhouette_values.sort()

	size_cluster_i = ith_cluster_silhouette_values.shape[0]
	y_upper = y_lower + size_cluster_i

	color = cm.nipy_spectral(float(i) / params['n_clusters'])
	ax1.fill_betweenx(np.arange(y_lower, y_upper),0, ith_cluster_silhouette_values, facecolor=color, edgecolor=color, alpha=0.7)

        # Label the silhouette plots with their cluster numbers at the middle
	ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))

        # Compute the new y_lower for next plot
	y_lower = y_upper + 10  # 10 for the 0 samples

ax1.set_title("The silhouette plot for the various clusters.")
ax1.set_xlabel("The silhouette coefficient values")
ax1.set_ylabel("Cluster label")

# The vertical line for average silhouette score of all the values
ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

ax1.set_yticks([])  # Clear the yaxis labels / ticks
ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])

    # 2nd Plot showing the actual clusters formed
colors = cm.nipy_spectral(cluster_labels.astype(float) / params['n_clusters'])
ax2.scatter(X[:, 0], X[:, 1], marker='.', s=30, lw=0, alpha=0.7, c=colors, edgecolor='k')

    # Labeling the clusters
centers = kmeans.cluster_centers_
    # Draw white circles at cluster centers
ax2.scatter(centers[:, 0], centers[:, 1], marker='o',c="white", alpha=1, s=200, edgecolor='k')

for i, c in enumerate(centers):
	ax2.scatter(c[0], c[1], marker='$%d$' % i, alpha=1, s=50, edgecolor='k')

ax2.set_title("The visualization of the clustered data.")
ax2.set_xlabel("Feature space for the 1st feature")
ax2.set_ylabel("Feature space for the 2nd feature")

plt.suptitle(("Silhouette analysis for k-means clustering on sample data of "+str(sys.argv[2])+" " " with n_clusters = %d" % params['n_clusters']), fontsize=14, fontweight='bold')

#plt.show()
plt.savefig('sil_'+str(sys.argv[2])+'.png', format='png')









##################
# Obtaining the most representative molecules
selected1 = []
clusters = []
kmeans.fit(X)
centroids = kmeans.cluster_centers_

if opt==1:
    # for clus in centroids:
    for clus in range(params['n_clusters']):
        idsIn = np.where(kmeans.labels_==clus)
        sel = idsIn[0][0]
        dMin = np.linalg.norm(centroids[clus,:] - X[idsIn[0][0],:])
        for sample in idsIn[0][1:]:
            dist = np.linalg.norm(centroids[clus,:] - X[sample,:])
            if dist < dMin:
                dMin = dist
                sel = sample
        selected1.append(int(ids[sel]))
        clusters.append(idsIn)
else:
    for clus in range(params['n_clusters']):
        idsIn = np.where(kmeans.labels_==clus)
        sel = idsIn[0][0]
        enMin = data2[sel,0]
        for sample in idsIn[0][1:]:
            energy = data2[sample,0]
            if energy < enMin:
                enMin = energy
                sel = sample
        selected1.append(int(ids[sel]))
        clusters.append(idsIn)

#print("Selected [op1]: ")
#print(selected1)

a=selected1

os.system('mkdir '+str(sys.argv[2])+'/selected_'+str(sys.argv[2]))

for y in a:
    
    #print(y)
    yy=baseFolder[y-1]
    print(yy)

    os.system('cp  '+str(yy)+' '+str(sys.argv[2])+'/selected_'+str(sys.argv[2])) #elements may change according to filenames


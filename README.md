# cluster_assembler

This is a WIP project for QTNano's cluster-ligands assembling proseadure. Contributions ongoing.


## General Process for Nanoclusters Generation

1. Core generation that can be performed via
 	- Permutation
 	- ABCluster

2. Connectivity test to exclude systems that not correspond to the expect number of metalic atoms

3. K-means clustering to select relevant cores to use

4. Ligands distribution around the metalic core

5. Overlap Filter 

6. K-means selection of nanoclusters to optimize via DFT

7. DFT optimization with light/weak criteria

8. Donnectivity verification to check if any chemical bond was made or broken during DFT optimization

9. K-means  selection of nanoclusters to post optimization via DFT

10. DFT optimization with tight/strong criteria


Steps 7 and 10 most be done externaly, and can be automated using appropriate quantuym chemistry software. The other steps can be done using the tools we provide here.

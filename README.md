![alt text](https://qtnano.iqsc.usp.br/wp-content/themes/qtnano/images/logo_foot2.png)
# cluster_assembler

This is a WIP project for QTNano's cluster-ligands assembling proseadure. Contributions ongoing.


## General Process for Nanoclusters Generation

1. Core generation that can be performed via
 	- User provided structures
 	- Supervised use of ABCluster

2. Connectivity test to exclude systems that not correspond to the expected chemical formula

3. K-means clustering to select relevant cores to use

4. Ligands distribution around the metalic core

5. Filter to remuve structures with overlaping atoms 

6. K-means selection of nanoclusters to optimize via DFT

7. DFT optimization with light/weak criteria

8. Connectivity verification to check if any chemical bond was made or broken during DFT optimization

9. K-means  selection of nanoclusters to post optimization via DFT

10. DFT optimization with tight/strong criteria


Steps 7 and 10 most be done externaly, and can be automated using appropriate quantuym chemistry software. 

## How to run: 
This steps can be done using:
```
python main.py 1 10
```
1 and 10 in this command can be changed to the appropriate interval of tasks on the list above.


# -*- coding: utf-8 -*-
"""
Analysis of a trajectory file:
Clustering of pockets in frames and printing out cluster centers and stability of pocket
"""

__all__ = ['wrapper_traj_anal']

import numpy as np
from scipy.cluster import hierarchy as h

def wrapper_traj_anal(file_cav_res, nframe, agglo_function = "average", dist_threshold = 0.4, min_occu = 5.0):
	"""
	This is the wrapper to perform the analysis of cavities in a DCD trajectory file or a 
	NMR multimodels file. Here is a short description of how it works:
	- Extraction of the list of residues for each cavities
	- Calculation of the distance between two list of residues (i've toyed around with Tanimoto/Dice)
	An artificial max distance of 1 for cavities of the same frame is set up
	- Clustering of the distances (dbscan and different hierarchical/agglomerative clustering algorithms are available)
	- Extraction of the frequency of a cavity during the trajectory (how many elements in the cluster / number of frames)
	and of the "centroid" (or at least the point with the minimum distance to all other points of the cluster).
 
	On the minus side : since I don't really know how to validate it, there's many parameters that aren't clear to me and that could be optimized:
	- which distance, which clustering algorithm, what threshold of distance to fix for clusters?
	"""

	# Read the data: Change?
	#import ast

	
	cav_res = []
	if nframe > 1:
		for line in file_cav_res:
			cavs = []
			if type(line) == list:
				for el in line:
					cavs.append(el)
			else: # it's probably a set because there's only one cavity
				cavs.append(line)
			cav_res.append(cavs)
	else:
		print("There's only one frame, no clustering analysis triggered")
		return None
	
	# Get dictionary of correspondance (flat) index vs frame number and cavity number
	dict_corresp = get_dict_conversion(cav_res)
	# Generate the distance dictionary
	dict_distances = create_dict_distances(dict_corresp, cav_res)
	# Extract the values as a flat list
	list_distances = []
	for key, item in dict_distances.items():
		list_distances.append(item)

	# number of frames
	n_fr = len(cav_res)
	from scipy.spatial.distance import squareform
	# convert to matrix and fill in the diagona
	matrix_distances = squareform(list_distances)
	np.fill_diagonal(matrix_distances, 1.0)
	
	# Cluster and print out results
	if "dbscan"  in agglo_function or "optics" in agglo_function:
		clusters = cluster_print_sklearn(list_distances, matrix_distances, dict_corresp, n_fr, dist_threshold = dist_threshold, clustering=agglo_function, min_occu = min_occu)
	else:
		clusters = cluster_print(list_distances, matrix_distances, dict_corresp, n_fr, dist_threshold = dist_threshold, agglo_function=agglo_function, min_occu = min_occu)
	
	# Generate dictionary of frame/cav number to cluster number
	dict_clusters = dict()
	for i in range(len(clusters)):
		dict_clusters[dict_corresp[i]] = clusters[i]
		
	return dict_clusters
	
def get_dict_conversion(cav_res):
	"""
	Generates a dictionary that contains for each index in a flat array of all cavities
	(flat as in: the original file is a nested list. The higher level contains a list of frames,
	and each frame contains a list of cavities (containing sets of residues))
	Here, index 0 is frame 1 cavity 1 and is linearly unwrapped.
	The index is the key of the dictionary and the value is a string encoding f_X_cav_Y
	where X is frame number and Y cavity number in frame X.
	"""
	f_id = 0
	idx = 0
	dict_corresp = dict()
	for frame in cav_res:
		for i in range(len(frame)):
			dict_corresp[idx] = str(f'f_{f_id+1}_cav_{i+1}')
			idx +=1
		#list_nbs.append([f_id+1, len(frame)])
		f_id += 1
	
	return dict_corresp

def dice(cav1, cav2):
	"""
	calculates the dice similarity between
	two lists of texts
	"""
	return 1 - 2*len(cav1.intersection(cav2))/(len(cav1)+len(cav2))

def tani(cav1, cav2):
	"""
	calculates the dice similarity between
	two lists of texts
	"""
	intersect = len(cav1.intersection(cav2)) 
	return 1 - (intersect/(len(cav1)+len(cav2) - intersect))
	
def create_dict_distances(dict_corresp, cav_res, dist_function = dice):
	"""
	Creates a dictionary in which the key is the name of the two cavities involved (as in dict_corresp) separated by a semicolon
	and the value is the distance. Cavities from the same frame are assigned arbitrarily a distance of 1.0
	values possible for dist_function = dice and tani
	"""
	arr = np.array(cav_res, dtype=object)
	f_id = 0
	idx_ref = 0
	dict_distances = dict()
	idx_all = 0
	for frame in cav_res:
		id_r_t = 0
		for el in frame:
			idx_comp = 1
			# Go over remaining cavities of the same frame
			for same in frame[id_r_t+1:]:
				dict_distances[str(dict_corresp[idx_ref]+";"+dict_corresp[idx_ref+idx_comp])] = 1.0
				idx_comp += 1
			# Go over cavities of the next frames
			for rest in [item for sublist in cav_res[f_id+1:] for item in sublist]:
				dict_distances[str(dict_corresp[idx_ref]+";"+dict_corresp[idx_ref+idx_comp])] = dist_function(el, rest)
				idx_comp += 1
			idx_ref += 1
			id_r_t += 1
			
		
		f_id += 1
	
	return dict_distances

def cluster_print(list_distances, matrix_distances, dict_corresp, n_fr, dist_threshold = 0.4, agglo_function = "average", min_occu = 5.0):
	"""
	Performs clustering and print results of cavities
	agglo_function can be any of the choices in https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html#scipy.cluster.hierarchy.linkage
	ie single, complete, average, weighted, centroid, median or ward
	"""
	methods = {
	'single': h.single,
	'complete': h.complete,
	'average': h.average,
	'weighted': h.weighted,
	'centroid': h.centroid,
	'median': h.centroid,
	'ward': h.ward,
	}
	arr_dist = np.array(list_distances)
	agglo = methods[agglo_function](arr_dist)
	clusters = h.fcluster(agglo, t=dist_threshold, criterion="distance")
	
	u, count=np.unique(clusters, return_counts= 1)
	count_sort_ind = np.argsort(-count) # sort descending by occupancy/size
	clust_names = u[count_sort_ind]  # sort descending by occupancy/size
	counts = count[count_sort_ind]  # sort descending by occupancy/size

	for i in range(len(clust_names)):
		occupancy = np.round((counts[i]/n_fr)*100, 1)
		if occupancy > float(min_occu):
			cluster_of_int = np.where(clusters == clust_names[i])[0]
			if len(cluster_of_int) > 1: # crashes with clusters of unique structure
				center = find_center(cluster_of_int, dict_corresp, matrix_distances)
				print(f"Cluster {clust_names[i]} has an occupancy of {occupancy}% and the representative structure is {center[0]}, with an average distance of {np.round(center[1], 2)} to other cluster members")
	
	return clusters

def cluster_print_sklearn(list_distances, matrix_distances, dict_corresp, n_fr, dist_threshold = 0.2, clustering = "dbscan", min_occu = 5.0):
	"""
	Same as cluster_print but using sklearn's dbscan and optics clustering methods (https://scikit-learn.org/stable/modules/clustering.html)
	"""

	import sklearn.cluster as c
	if clustering == "dbscan":
		model = c.DBSCAN(eps=0.2, metric="precomputed").fit(matrix_distances)
	elif clustering == "optics":
		model = c.OPTICS(metric="precomputed").fit(matrix_distances)
	clusters = model.labels_

	u, count=np.unique(clusters, return_counts= 1)
	count_sort_ind = np.argsort(-count) # sort descending by occupancy/size
	clust_names = u[count_sort_ind]  # sort descending by occupancy/size
	counts = count[count_sort_ind]  # sort descending by occupancy/size

	for i in range(len(clust_names)):
		occupancy = np.round((counts[i]/n_fr)*100, 1)
		if clust_names[i] > -1 and occupancy > float(min_occu):
			cluster_of_int = np.where(clusters == clust_names[i])[0]
			center = find_center(cluster_of_int, dict_corresp, matrix_distances)
			print(f"Cluster {clust_names[i]} has an {occupancy}% and the representative structure is {center[0]}, with an average distance of {np.round(center[1], 2)} to other cluster members")
	
	return clusters

def find_center(cluster_of_int, dict_corresp, matrix_distances):
	"""
	Identifies the point with the shorted average distance to other points in cluster
	and defines it as the center
	"""
	list_avg=[]
	for i in range(len(cluster_of_int)):
		other_idx = np.delete(cluster_of_int, i)
		dist_for_i = np.take(matrix_distances[cluster_of_int[i]], other_idx)
		list_avg.append(np.average(dist_for_i))

	# This was for printing 5 random members of the cluster
	#index = np.random.choice(len(cluster_of_int), 5, replace=False)  
	#for i in index:
	#	print(dict_corresp[cluster_of_int[i]])
		
	# return the cluster representative
	return dict_corresp[cluster_of_int[int(np.argwhere(list_avg == np.amin(list_avg))[0])]], np.amin(list_avg)
	

# -*- coding: utf-8 -*-
"""
This module defines some functions aiming at describing subcavities
and caracterize their shapes
"""

import os
import numpy as np
from scipy import ndimage
from skimage.feature import peak_local_max
from skimage.morphology import watershed
from caviar.cavity_identification.gridtools import get_index_of_coor_list
from caviar.misc_tools.misc import export_pdb_subcavities
from .cavity import Cavity

__all__ = ['wrapper_subcavities']


def wrapper_subcavities(final_cavities, cav_of_interest, grid_min, grid_shape, cavities, code, out, sourcedir, list_ligands,
	seeds_mindist = 3, merge_subcavs = True, minsize_subcavs = 50, min_contacts = 0.667, v = False,
	printv = False, print_pphores_subcavs = False, export_subcavs = False, gridspace = 1.0, frame = None):
	"""
	Wraps transform_cav2im3d, find_subcav_watershed, map_subcav_in_cav
	merge_small_enclosed_subcavs, print_subcavs_pphores and export_pdb_subcavities
	as one function
	"""

	# Convert to a 3D image for skimage
	im3d = transform_cav2im3d(final_cavities[cav_of_interest], grid_min,
		grid_shape) #filtered_pharma[order][cav_of_interest])
	# Perform the watershed algorithm, including entropy of pharmacophores 
	labels = find_subcav_watershed(im3d, seeds_mindist)
	# Map results of watershed to grid points of cavity
	#subcavs = map_subcav_in_cav(cavities, cav_of_interest, labels, args.code, grid_min, grid_shape)
	subcavs = map_subcav_in_cav(labels, grid_min)
	if merge_subcavs == True:
		subcavs = merge_small_enclosed_subcavs(subcavs, minsize_subcavs = minsize_subcavs,
			min_contacts = min_contacts, v = v)
	subcavs_table = print_subcavs_pphores(cavities, subcavs, cav_of_interest, code, grid_min, grid_shape, frame)


	# Export
	if export_subcavs:
		try:
			os.mkdir(out)
		except:
			pass
		if frame:
			export_pdb_subcavities(subcavs, code[:-4]+"_"+str(frame), grid_min, grid_shape,
				cavid = cav_of_interest, gridspace = gridspace, outdir = out,
				listlig = list_ligands, oridir = sourcedir)
		else:
			export_pdb_subcavities(subcavs, code[:-4], grid_min, grid_shape,
				cavid = cav_of_interest, gridspace = gridspace, outdir = out,
				listlig = list_ligands, oridir = sourcedir)

	return subcavs_table

def transform_cav2im3d(cavity_coords, grid_min, grid_shape):
	"""
	Takes coordinates of grid points and outputs an im3d for skimage
	could be done in many ways but this one does the job 
	"""
	
	# Simpler version with indices and array reshaping
	#im1d = np.zeros(grid_shape[0]*grid_shape[1]*grid_shape[2])
	#im1d[get_index_of_coor_list(cavity_coords, grid_min, grid_shape)] = 1
	#im3d = np.reshape(im1d, grid_shape)
	# Somehow doesnt' work always


	# Generate an im3d object of correct size for the cavity
	im3d = np.zeros(grid_shape)
	# Align the cavity to zero and convert the silly floats to ints
	aligned_cav = cavity_coords - grid_min
	# np.around because stupid python cant broadcast from floats to ints because floating point error
	# I am losing so much time with this kind of stupid behavior, seriously, WTF is this?
	newtypes_cav = np.around(np.array(aligned_cav, dtype=np.float)).astype(int)
	# Set as 1 the indices corresponding to cavity grid points in the im3d
	im3d[newtypes_cav[:,0], newtypes_cav[:,1], newtypes_cav[:,2]] = True
	# np.flatnonzero(im3d) should give the same result as
	# get_index_of_coor_list(cavity_coords, grid_min, grid_shape)

	return im3d


def find_subcav_watershed(im3d, seeds_mindist = 3):
	"""
	Uses skimage to perform a watershed algorithm in order to 
	identify subcavities. Seeds of the watershed algorithm are
	defined by maximum local distance to the end of the cavity
	Explanation here: https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_watershed.html
	"""

	# Euclidian distance transform
	distance = ndimage.distance_transform_edt(im3d, sampling=None, return_distances=True,
		return_indices=False, distances=None, indices=None) # Default
	# Find peaks in the image
	# min_distance can be tuned to change the definition of seeds for the watershed algorithm
	# Peaks are separated by at least min_distance
	# increasing the value decreases the number of seeds and thus subpockets
	#print(seeds_mindist)
	local_maxi = peak_local_max(distance, min_distance = int(seeds_mindist), # 
		threshold_abs=None, threshold_rel=None, exclude_border=True, # default
		indices=False, # Modified to return boolean mask
		footprint=None, labels=None,# default
		num_peaks_per_label= 1)#, num_peaks = inf,) # Not several seeds in same label zone
	# label the seeds
	markers = ndimage.label(local_maxi)[0]
	# 
	labels = watershed(-distance, markers = markers, mask=im3d,
		connectivity = 1, offset = None, compactness = 0, watershed_line = False)

	# Labels is of dimension grid_shape and contains integer values corresponding 
	# to the subcavity a point is issued from

	return labels


def transform_cav2im3d_entropy(cavity_coords, grid_min, grid_shape, pharmaco):
	"""
	Takes coordinates of grid points and outputs an im3d for skimage
	Uses entropy at 3A of pharmacophores as values to set the "greyscale"
	"""

	# First we simply the pharmacophores
	names = np.array([0, 1, 1, 3, 3, 3, 4, 5, 0, 0, 0]) # type None & other, hydrophobic, polar, negative, positive
	pharmacophores = names[pharmaco]

	from scipy.spatial import cKDTree
	from scipy.stats import entropy
	
	tree1 = cKDTree(cavity_coords)
	neighbors = tree1.query_ball_point(cavity_coords, r=3)
	list_entropy = []
	for i in neighbors:
		pharma = pharmacophores[:,0][i]
		list_entropy.append(entropy(pharma))

	# Generate an im3d object of correct size for the cavity
	im3d = np.zeros(grid_shape)
	# Align the cavity to zero and convert the silly floats to ints
	aligned_cav = cavity_coords - grid_min
	# np.around because stupid python cant broadcast from floats to ints because floating point error
	# I am lsoing so much time with this kind of stupid behavior, seriously, WTF is this?
	newtypes_cav = np.around(aligned_cav).astype(int)
	# Set as 1 the indices corresponding to cavity grid points in the im3d
	im3d[newtypes_cav[:,0], newtypes_cav[:,1], newtypes_cav[:,2]] = 1/np.array(list_entropy)
	# np.flatnonzero(im3d) should give the same result as
	# get_index_of_coor_list(cavity_coords, grid_min, grid_shape)

	return im3d


def find_subcav_watershed_entropy(im3d, seeds_mindist = 3):
	"""
	Uses skimage to perform a watershed algorithm in order to 
	identify subcavities. Seeds of the watershed algorithm are
	defined by maximum local distance to the end of the cavity
	Explanation here: https://scikit-image.org/docs/dev/auto_examples/segmentation/plot_watershed.html
	"""

	# Euclidian distance transform
	distance = ndimage.distance_transform_edt(im3d, sampling=None, return_distances=True,
		return_indices=False, distances=None, indices=None) + np.round(im3d, 1)
	# Find peaks in the image
	# min_distance can be tuned to change the definition of seeds for the watershed algorithm
	# Peaks are separated by at least min_distance
	# increasing the value decreases the number of seeds and thus subpockets
	local_maxi = peak_local_max(distance, min_distance = seeds_mindist, # 
		threshold_abs=None, threshold_rel=None, exclude_border=True, # default
		indices=False, # Modified to return boolean mask
		footprint=None, labels=None,# default
		num_peaks_per_label= 1)#, num_peaks = inf,) # Not several seeds in same label zone
	# label the seeds
	markers = ndimage.label(local_maxi)[0]
	# 
	labels = watershed(-distance, markers = markers, mask=im3d,
		connectivity = 1, offset = None, compactness = 0, watershed_line = False)

	# Labels is of dimension grid_shape and contains integer values corresponding 
	# to the subcavity a point is issued from

	return labels

def merge_small_enclosed_subcavs(subcavs, minsize_subcavs = 50, min_contacts = 0.667, v = False):
	"""
	The watershed algorithm tends to overspan a bit, even when optimizing seeds.
	This function aims at identifying small pockets (< minsize_subcavs)
	that are heavily in contact with other subcavs (> min_contacts)
	These subcavites are probably at the interface between 2 main subcavities,
	or on their surface.
	"""
	# Create a copy of the subcavs array to not change in place, in case
	_subcavs = subcavs.copy()
	# lengths of each subcavity
	lengths = [len(x) for x in subcavs]
	#Smaller ones than min_contacts
	smallsubcavs = [[x, lengths[x]] for x in range(0, len(lengths)) if lengths[x] < minsize_subcavs]
	
	if not smallsubcavs:
		return subcavs
	
	from scipy.spatial.distance import cdist
	
	to_del = {}
	
	for small in smallsubcavs:
		contacts = []
		contact = 0.
		total_contact = 0.
		i = 0
		# Check the contact between the small subcavity and the others
		for other_subcavs in subcavs:
			if i == small[0]:
				contacts.append(0)
				i+=1
				continue
			contact = len(set(np.nonzero(cdist(subcavs[small[0]], other_subcavs) < 1.01)[0]))
			contacts.append(contact)
			total_contact += contact/small[1]
			i+=1
		# If a small subcavity has more than min_contacts with neighbors, be ready to add it to the 
		# subcavity with which it has the more contacts
		if total_contact >= min_contacts:
			if v == True: print(f"Subcavity {small[0]} is small and enclosed {total_contact*100:.2f}% in other subcavs.\nIt will be added to subcavity {np.argmax(contacts)} (original numbering of subcavs from 0)")
			to_del[small[0]] = np.argmax(contacts)
	# to_del is dict which contains key = index of subcav to delete; value = index of subcav to merge it with
	# If there's any subcavities to merge
	# It's a mess because it's not easy to merge different array elements together and/or delete some...
	if to_del:
		dels = []
		for index in range(0, len(subcavs)):
			if index in to_del.keys():
				# original version: works generally, except in some cases in which we merge and replace 2 equally sized small arrays (memory issue?)
				try:
					# _tmp contains the merged subcavity 
					_tmp = np.concatenate((_subcavs[to_del[index]], _subcavs[index]), axis = 0)
					# now we assign the merged subcavity to the index of the main subcav
					_subcavs[to_del[index]] = _tmp
				# dirty work around: change to lists, and play with lists, and come back to array...
				except:
					_tmp = np.array(_subcavs[to_del[index]]).tolist() + np.array(_subcavs[index]).tolist()
					_subcavs[to_del[index]] = np.array(_tmp)
				dels.append(index)
		subcavlist = []
		for x in _subcavs:
			# there is also here a mix of lists and arrays. Why?
			try:
				subcavlist.append(x.tolist())
			except:
				subcavlist.append(x)
		for _del in sorted(dels, reverse=True):
			del subcavlist[_del]
		merged_subcavs = [np.array(x) for x in subcavlist]
		return merged_subcavs

	else:
		return subcavs


def map_subcav_in_cav(labels, grid_min):
	"""
	Extract information from subcavities: return the coordinates as subcavs, 
	/! function cut with print_subcavs_pphores in case we merged small subcavities
	"""

	subcavs = []
	for i in range(1, np.amax(labels)+1):
		
		subcav = np.argwhere(labels == i) + grid_min
		subcavs.append(subcav)

	return subcavs


def transform_im3d2cav(im3d, grid):
	"""
	Invert of original function. It's a simple command but nice to have it here with a good name
	"""
	cav_coor = grid[np.flatnonzero(im3d)]

	return cav_coor


def print_subcavs_pphores(cavities, subcavs, cav_of_interest, pdbcode, grid_min, grid_shape, frame = None):
	"""
	print information about PP environment
	and in particular, set in cavities object (class) the subcavity indices
	"""

	#names = ["none", "aliphatic", "aromatic", "donor", "acceptor", "doneptor", "negative",
	# "positive", "cys", "his", "metal"]
	# Dictionary of pharmacophore types to print
	import networkx as nx

	names = ["shouldnotbethere", "hydrophobic", "shouldnotbethere", "polar non charged", "shouldnotbethere", "shouldnotbethere",
	"negative", "positive", "other", "shouldnotbethere", "shouldnotbethere"]
	subcavs_table = ""
	for i in range(0, len(subcavs)):
		# Find the corresponding indices in cavities[cav_of_interest]
		subcav = subcavs[i]

		oricav_indices = np.intersect1d(get_index_of_coor_list(subcav, grid_min, grid_shape),
			get_index_of_coor_list(np.array([x.coords for x in cavities[cav_of_interest].gp]), grid_min, grid_shape),
			return_indices=True)[2]
		# Update the cavity object
		cavities[cav_of_interest].subcavities[i+1] = oricav_indices # to not start at 0
		# Update the graph
		my_dict = {value: {"subcavs": i+1} for value in oricav_indices} # to not start at 0
		nx.set_node_attributes(cavities[cav_of_interest].graph, my_dict)

		# Find the pharmacophore types of the gridpoints of the subcavity
		listouille = [cavities[cav_of_interest].gp[x].pharma[0] for x in oricav_indices]

		# Convert types aromatic into "hydrophobic" alongside aliphatic (original nb1)
		listouille = np.where(np.array(listouille)==2, 1, listouille)
		# Convert types acceptor and doneptor into "polar non charged" (originally donor)
		listouille = np.where(np.array(listouille)==4, 3, listouille)
		listouille = np.where(np.array(listouille)==5, 3, listouille)
		# Convert None, cys, his, metal to the same "other"
		listouille = np.where(np.array(listouille)==0, 8, listouille)
		listouille = np.where(np.array(listouille)==9, 8, listouille)
		listouille = np.where(np.array(listouille)==10, 8, listouille)
	
		# Count occurences of each value
		values, counts = np.unique(listouille, return_counts=True)
		total = np.sum(counts)
		# create a dummy dictionary to store values better for printing
		# set it up with 0 in case some values are absent
		dico = {1: 0, 3: 0, 6: 0, 7: 0, 8: 0}
		# Replace the 0 by the actual values
		for aa in range(len(values)):
			dico[values[aa]] = np.divide(counts[aa], total)

		# create the table with subcavs information, that we may print or not
		# Will be: PDB_chain cav_id subcav_id size hydroph polar neg pos other
		if frame:
			name = str(pdbcode[0:-4] + "_" + cavities[cav_of_interest].chains + "_" + str(frame))
		else:
			name = str(pdbcode[0:-4] + "_" + cavities[cav_of_interest].chains)
		subcavs_table += f"{name:<12}"
		subcavs_table += f"{cav_of_interest+1:^7d}{i+1:^8d}{len(oricav_indices):^6d}"
		subcavs_table += f"{str(int(np.around(dico[1]*100)))+'%':^10}{str(int(np.around(dico[3]*100)))+'%':^7}"
		subcavs_table += f"{str(int(np.around(dico[6]*100)))+'%':^6}{str(int(np.around(dico[7]*100)))+'%':^6}{str(int(np.around(dico[8]*100)))+'%':^6}"
		subcavs_table += f"\n"

	return subcavs_table
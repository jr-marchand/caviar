# -*- coding: utf-8 -*-
"""
This module contains miscellaneous functions
used to gather and export cavity descriptors for ML approach

global cavity descriptors:
 size
 statistics of distribution of pharmacophores
 and buriedness (average, median, quantiles),
 scorecavity, 
 list of residues,
 hydrophobicity
 count of subcavities

local descriptors NetworkX graph and as 3D image:
 buriedness,
 pharmacophore,
 local asphericity,
 scoretrim 
 subcavity affiliation.

"""

__all__ = ['get_descriptors']

import pandas as pd
import numpy as np
import networkx as nx

def get_descriptors(cavities, pdbcode, grid_min, grid_shape):
	"""
	Gather all global descriptors in a panda dataframe object
	size
	statistics of distribution of pharmacophores
	and buriedness (average, median, quantiles),
	scorecavity, 
	list of residues,
	hydrophobicity
	count of subcavities
	"""

	def calculate_global_descriptors(cavities, cavid, pdbcode):
		"""
		Calculates the global descriptors and returns a dataframe
		"""

		size = cavities[cavid].size

		# Buriedness related
		burlist = [gp.bur for gp in cavities[cavid].gp]
		avgbur = np.mean(burlist)
		medbur = np.median(burlist)
		quantbur = np.quantile(burlist, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
		# calculate distributions of buriedness
		bur8 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 8])/size
		bur9 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 9])/size
		bur10 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 10])/size
		bur11 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 11])/size
		bur12 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 12])/size
		bur13 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 13])/size
		bur14 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 14])/size

		# General
		#size = cavities[cavid].size
		score_cav = cavities[cavid].score
		n_subcavs = len(cavities[0].subcavities.keys())
		# Residues
		n_residues = len(cavities[cavid].residues)
		list_residues = [x[:3] for x in cavities[cavid].residues]

		# Ph4
		# calculate distributions of pharmacophores
		#f0 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 0])/size # do we want none types?
		f1 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 1])/size
		f2 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 2])/size
		f3 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 3])/size
		f4 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 4])/size
		f5 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 5])/size
		f6 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 6])/size
		f7 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 7])/size
		f8 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 8])/size
		f9 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 9])/size
		f10 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 10])/size # contains also the information if cavity is metaled
		fpolar = f3+f4+f5
		fcharged = f6+f7
		fother = f8+f9+f10
		fhydrophob = cavities[cavid].hydrophobicity

		dict_forpandas = {"pdb_cavid":  [str(pdbcode)+'_'+str(cavid)], "bur_avg": [avgbur], "bur_med": [medbur], "bur_q1": [quantbur[0]], "bur_q2": [quantbur[1]], "bur_q3": [quantbur[2]],
		"bur_q4": [quantbur[3]], "bur_q5": [quantbur[4]], "bur_q6": [quantbur[5]], "bur_q7": [quantbur[6]], "bur_q8": [quantbur[7]], "bur_q9": [quantbur[8]], 
		"bur_percent8": [bur8], "bur_percent9": [bur9], "bur_percent10": [bur10], "bur_percent11": [bur11],	"bur_percent12": [bur12], "bur_percent13": [bur13], "bur_percent14": [bur14],
		"cav_size": [size], "cav_score": [score_cav], "subcavs_n": [n_subcavs], "cavres_n": [n_residues], "list_residues": [" ".join(list_residues)],
		"ph4_aliph": [f1], "ph4_arom": [f2], "ph4_donor": [f3], "ph4_acceptor": [f4], "ph4_doneptor": [f5], 
		"ph4_neg": [f6], "ph4_pos": [f7], "ph4_cys": [f8], "ph4_his": [f9], "ph4_metal": [f10], "ph4_polar": [fpolar], "ph4_charged": [fcharged], "ph4_other": [fother],
		"ph4_hydrophob": [fhydrophob]}
		global_descr = pd.DataFrame(dict_forpandas)
	

		return global_descr

	def calculate_local_descriptors(cavities, cavid, grid_min, grid_shape):
		"""
		local descriptors NetworkX graph and as 3D image:
		buriedness,
  		pharmacophore,
		local asphericity,
		scoretrim 
		subcavity affiliation
		"""

		# Contains everything already
		g = cavities[cavid].graph 

		# Retrieve data from the graph to generate the 3D image
		coordinates = np.array([g.nodes[x]["coords"] for x in g.nodes])
		channels = np.array([[g.nodes[x]["bur"], g.nodes[x]["pp"], g.nodes[x]["asph"], g.nodes[x]["subcavs"]] for x in g.nodes])

		# Create a 3D image of the same dimensions as the grid, and have a channel for "colors" of dimension 4 (the 4 descriptors) 
		im3d_local_descriptors = np.full_like(np.empty([grid_shape[0], grid_shape[1], grid_shape[2], 4]), fill_value=np.nan, dtype=np.float16)
		# Align the cavity to zero and convert the floats to ints
		aligned_cav = coordinates - grid_min
		# np.around because stupid python cant broadcast from floats to ints because floating point error
		newtypes_cav = np.around(np.array(aligned_cav, dtype=np.float)).astype(int)
		# Set as the channels the indices corresponding to cavity grid points in the im3d
		im3d_local_descriptors[newtypes_cav[:,0], newtypes_cav[:,1], newtypes_cav[:,2], :] = channels

		return g, im3d_local_descriptors

	global_descr = pd.DataFrame(data = None, columns = ["pdb_cavid", "bur_avg", "bur_med", "bur_q1", "bur_q2", "bur_q3",
		"bur_q4", "bur_q5", "bur_q6", "bur_q7", "bur_q8", "bur_q9", 
		"bur_percent8", "bur_percent9", "bur_percent10", "bur_percent11", "bur_percent12", "bur_percent13", "bur_percent14",
		"cav_size", "cav_score", "subcavs_n", "cavres_n", "list_residues",
		"ph4_aliph", "ph4_arom", "ph4_donor", "ph4_acceptor", "ph4_doneptor", 
		"ph4_neg", "ph4_pos", "ph4_cys", "ph4_his", "ph4_metal", "ph4_polar", "ph4_charged", "ph4_other",
		"ph4_hydrophob"])
	graph_local_descriptors = []
	im3d_local_descriptors = []
	for cavid in range(len(cavities)):
		# Panda frames that already contains global desctiptors, before adding the local ones
		global_descr = global_descr.append(calculate_global_descriptors(cavities, cavid, pdbcode)) # append dataframe to dataframe, there should not be too many cavities so it's ok
		# Calculate the local descriptors, as graph and as im3d
		_graph, _im3d = calculate_local_descriptors(cavities, cavid, grid_min, grid_shape)
		graph_local_descriptors.append(_graph)
		im3d_local_descriptors.append(_im3d)


	#dict_descriptors["graph_local_descriptors"] = graph_local_descriptors
	#dict_descriptors["im3d_local_descriptors"] = im3d_local_descriptors
	#all_descriptors = pd.DataFrame(dict_forpandas)

	return global_descr, graph_local_descriptors, im3d_local_descriptors
# -*- coding: utf-8 -*-
"""
Defines a class Cavity with its information
"""

from caviar.cavity_identification.geometry import SetOfPoints, Point
from caviar.cavity_identification.gridtools import get_index_of_coor_list, get_index_of_coor


__all__ = ['CavGridPoint', 'Cavity', 'fill_cavities_object']


class CavGridPoint(Point):
	"""
	A class to store a cavity grid point coordinates, buriedness, pharmacophore type, asphericity
	"""
	def __init__(self, coords, pharma, bur, index, asph): 
		self.coords = coords
		self.pharma = pharma
		self.bur = bur
		self.asph = asph
		self.index = index
		self.bfactor = None
		self.dssp = None
	
	def __str__(self):
		return f"GridPoint(buriedness: {self.bur}, type: {self.pharma})"

class Cavity(set):
	"""
	A class containing all the information of a cavity: coordinates of grid points,
	surroundings, ...
	"""
	def __init__(self, ID, residues, chains, missing, score, size, median_bur, bur_7thq, hydrophobicity, interchain,
		altlocs, metaled, watered, subcavities):
		self.metaled = metaled
		self.liganded = None
		self.ligfull = None #never sets, delete?
		self.sizelig = None
		self.ligsmi = None
		self.ligsmiOE = None
		self.cavcov = None
		self.ligcov = None
		self.ligandability = None
		self.graph = None
		self.watered = watered
		self.gp = []
		self.ID = ID
		self.residues = residues
		self.chains = chains
		self.missing = missing
		self.score = score
		self.size = size
		self.median_bur = median_bur
		self.bur_7thq = bur_7thq
		self.hydrophobicity = hydrophobicity
		self.interchain = interchain
		self.altlocs = altlocs
		self.subcavities = {} # a dictionary containing as key the subcav ID and value the indices of cavity gp

	def __str__(self):
		return f"Cavity {self.ID} size {self.size} median_bur {self.median_bur} hydrophobicity {self.hydrophobicity}"
	

def fill_cavities_object(dict_all_info, final_cavities, final_pharma, grid_decomposition,
	grid_min, grid_shape, list_asph, gridspace = 1.0):
	"""
	Uses the two classes above and the data previously generated to create
	a clean list of cavities, which contains all the data easily accessible
	(hopefully)
	It might be useful to port this earlier to not duplicate similar objects?
	"""
	cavities = []
	import numpy as np
	
	for i in range(len(final_cavities)):
		
		# Check if we have metal types in the fp
		metaled = False
		if 10 in final_pharma[i]:
			metaled = True
		# Or water
		watered = False
		if list(filter(lambda x: "HOH" in x, dict_all_info[i]["cavity_residues"])):
			watered = True

		cav = Cavity(ID = i, residues = dict_all_info[i]["cavity_residues"], chains = dict_all_info[i]["chains"],
			missing = dict_all_info[i]["missingatoms"] + dict_all_info[i]["missingres"],
			score = dict_all_info[i]["score"], size = dict_all_info[i]["size"],
			median_bur = dict_all_info[i]["median_buriedness"], bur_7thq = dict_all_info[i]["7thq_buriedness"],
			hydrophobicity = dict_all_info[i]["hydrophobicity"], interchain = dict_all_info[i]["interchain"],
			altlocs = dict_all_info[i]["altlocs"], metaled = metaled, watered = watered, subcavities = {})

		import networkx as nx
		# Recreate a graph of grid points, in addition to the rest
		# This is dirty, functionality added later. Maybe should be optimized
		# Copied from cavitydetect

		setcav = SetOfPoints(final_cavities[i])
		diag = gridspace + 0.1# +0.1 because floating point #*np.sqrt(3) was for the diagonal connections
		# but it ended up overspanning
		dist_mat = setcav.print_indices_within(final_cavities[i], diag, turnon = False)
		list_edges = dist_mat[["i","j"]]
		G = nx.Graph() # Initialize graph
		G.add_edges_from(list_edges)
		
		dict_info_for_G = {}
		
		# Add points to cavity object
		point_nb = 0
		for point in final_cavities[i]:
			index_point = get_index_of_coor(point, grid_min, grid_shape, gridspace = gridspace)
			cav.gp.append(CavGridPoint(coords = point, pharma = final_pharma[i][point_nb],
					bur = grid_decomposition[int(index_point)], asph = list_asph[i][point_nb],
					index = index_point))
			dict_info_for_G[point_nb] = {"bur": grid_decomposition[int(index_point)], "pp": final_pharma[i][point_nb][0],
			"coords": point, "asph": list_asph[i][point_nb], "subcavs": np.nan}#, "bfactor": "", "dssp": ""} # placeholders
			point_nb += 1

		nx.set_node_attributes(G, dict_info_for_G)
		cav.graph = G

		cavities.append(cav)

	
	return cavities



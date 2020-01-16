# -*- coding: utf-8 -*-
"""
Defines a class Cavity with its information
"""

from caviar_gui.cavity_identification.geometry import SetOfPoints, Point
from caviar_gui.cavity_identification.gridtools import get_index_of_coor_list, get_index_of_coor


__all__ = ['CavGridPoint', 'Cavity', 'fill_cavities_object']


class CavGridPoint(Point):
	"""
	A class to store a cavity grid point coordinates, buriedness, pharmacophore type, asphericity
	"""
	def __init__(self, coords, pharma, bur, index): #asph
		self.coords = coords
		self.pharma = pharma
		self.bur = bur
		self.asph = 0 #asph
		self.index = index
	
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
		self.ligandability = 0.
		self.watered = watered
		self.fp1 = []
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
	

def fill_cavities_object(dict_all_info, order, filtered_cavities, filtered_pharma, grid_decomposition,
	grid_min, grid_shape, gridspace = 1.0):  # list_asph,
	"""
	Uses the two classes above and the data previously generated to create
	a clean list of cavities, which contains all the data easily accessible
	(hopefully)
	It might be useful to port this earlier to not duplicate similar objects?
	"""
	cavities = []
	
	for i in range(len(order)):
		ID = int(order[i])
		
		# Check if we have metal types in the fp
		metaled = False
		if 10 in filtered_pharma[ID]:
			metaled = True
		# Or water
		watered = False
		if list(filter(lambda x: "HOH" in x, dict_all_info[ID]["cavity_residues"])):
			watered = True

		cav = Cavity(ID = ID, residues = dict_all_info[ID]["cavity_residues"], chains = "A",
					missing = dict_all_info[ID]["missingatoms"] + dict_all_info[ID]["missingres"],
					score = dict_all_info[ID]["score"], size = dict_all_info[ID]["size"],
					median_bur = dict_all_info[ID]["median_buriedness"], bur_7thq = dict_all_info[ID]["7thq_buriedness"],
					hydrophobicity = dict_all_info[ID]["hydrophobicity"], interchain = dict_all_info[ID]["interchain"],
					altlocs = dict_all_info[ID]["altlocs"], metaled = metaled, watered = True, subcavities = {})
		# Add points to cavity object
		point_nb = 0
		for point in filtered_cavities[ID]:
			index_point = get_index_of_coor(point, grid_min, grid_shape, gridspace = gridspace)
			cav.gp.append(CavGridPoint(coords = point, pharma = filtered_pharma[ID][point_nb],
					bur = grid_decomposition[int(index_point)], #asph = list_asph[i][point_nb],
					index = index_point))
			point_nb += 1
		cavities.append(cav)
	
	return cavities

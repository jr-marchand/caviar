# -*- coding: utf-8 -*-
"""
This module contains tools that characterize grid point properties
The most important function is set_pharmacophore_type that scans neighbors of 
cavity grid points for setting the pharmacophore type of the grid point
export_hydrophobicity calculates the proportion of hydrophobic (aliphatic
or aromatic) grid points in the cavity
combine_filterhydro filters out cavities with an hydrophobicity above 
a threshold and combine some information
check_protein_res 
"""

from caviar_gui.prody_parser.atomic.select import *
from caviar_gui.cavity_identification.geometry import SetOfPoints, calc_moments_of_inertia, calc_asphericity
from caviar_gui.cavity_identification.gridtools import list_transform_indices2, get_index_of_coor, get_index_of_coor_list
import numpy as np
from scipy.spatial import cKDTree
from itertools import product

__all__ = ['set_pharmacophore_type', 'export_hydrophobicity', 'combine_filterhydro', 'check_protein_res', 'get_local_asph_point',
			'get_local_weight', 'trim_cavity_bylocalweight', 'get_list_asph']


def set_pharmacophore_type(cavities, selection_protein, selection_coords):
	"""
	Assign the pharmacophore types to grid points.
	The grid points are aliphatic, aromatic, donor, acceptor, doneptor (both donor/acceptor),
	negative, positive, CYS, HIS, metal
	It assigns the type from the closest protein atom, with a max distance of 5A
	In order to include some fuzziness, it actually detects the 3 closest neighbors and 
	assigns a triplet of types from the 3 closest neighbors within 5A (if > 5A => type 0)
	Unlike the previous version, this one doesnt include any threshold distance within these 5A
	Otherwise that would be a loss of time within the loops, and the fuzziness should somehow 
	reduce potential errors.
	The idea is to have a main pp type (the first value of the triplet), and 2 neighboring values
	
	Types are assigned as integers: 0 for none, and starts at 2 for aliphatic, with a final
	of 11 for metals, in the same order as described earlier
	Returns an array of arrays (array of cavities). Each array contains the pharmacophore integers at each indice of
	the cavity point from the input data "cavities".
	"""

	# Select the different pharmacophores 
	aliphatic_atoms_sel = selection_protein.select("(resname ALA and (name C or name CA or name CB)) or (resname ARG and (name C or name CA or name CB or name CG or name CD)) or (resname ASN and (name C or name CA or name CB or name CG)) or (resname ASP and (name C or name CA or name CB)) or (resname CYS and (name C or name CA or name CB)) or (resname GLN and (name C or name CA or name CB or name CG or name CD)) or (resname GLU and (name C or name CA or name CB or name CG)) or (resname GLY and (name C or name CA)) or (resname HIS and (name C or name CA or name CB)) or (resname ILE and (sidechain or name C or name CA)) or (resname LEU and (sidechain or name C or name CA)) or (resname LYS and (name C or name CA or name CB or name CG or name D)) or (resname MET and (sidechain or name C or name CA)) or (resname PHE and (name C or name CA or name CB)) or (resname PRO and (name C or name CA or name CD or name CB or name CG or name N)) or (resname SER and (name C or name CA or name CG)) or (resname THR and (name C or name CA or name CB or name CG2)) or (resname TRP and (name C or name CA or name CB)) or (resname TYR and (name C or name CA or name CB)) or (resname VAL and (sidechain or name C or name CA))")
	aromatic_atoms_sel = selection_protein.select("(resname PHE and (name CG or name CD1 or name CE1 or name CZ or name CE2 or name CD2)) or (resname TYR and (name CG or name CD1 or name CE1 or name CZ or name CE2 or name CD2)) or (resname TRP and (name CG or name CD1 or name CE2 or name CD2 or name CE3 or name CZ3 or name CH2 or name CZ2))")
	donor_atoms_sel = selection_protein.select("(resname TRP and (name NE1)) or (name N and not resname PRO)")
	acceptor_atoms_sel = selection_protein.select("(name O)")
	doneptor_atoms_sel = selection_protein.select("(resname SER and (name OG)) or (resname TYR and (name OH)) or (resname THR and (name OG1)) or (resname ASN and (name OD1 or name ND2)) or (resname GLN and (name OE1 or name NE2)) or (resname HOH)")
	negative_atoms_sel = selection_protein.select("(resname ASP and (name OD1 or name OD2 or name CG)) or (resname GLU and (name OE1 or name OE2 or name CD))")
	positive_atoms_sel = selection_protein.select("(resname ARG and (name NE or name CZ or name NH1 or name NH2)) or (resname LYS and (name CE or name NZ))")
	cys_atoms_sel = selection_protein.select("(resname CYS and (name SG))")
	his_atoms_sel = selection_protein.select("(resname HIS and (name CG or name ND1 or name CD2 or name NE2 or name CE1))")
	metal_atoms_sel = selection_protein.select("resname CO or resname ZN or resname MG or resname FE or resname GA or resname IN or resname NI or resname RE or resname PB or resname AS or resname BE or resname CU or resname V or resname AL or resname MN or resname CA")

	
	# Store their pharmacophore types as their indices in an array
	arrays_prot_pharmatypes = np.zeros(len(selection_coords)+1, dtype="i")
	# getIndices from prody only returns the original indices
	# from the PDB file and not 
	list_protindices = selection_protein.getIndices()
	
	arrays_prot_pharmatypes[np.in1d(list_protindices, aliphatic_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 1
	# Bugged once because no aromatic atoms?
	try:
		arrays_prot_pharmatypes[np.in1d(list_protindices, aromatic_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 2
	except:
		None
	try:
		arrays_prot_pharmatypes[np.in1d(list_protindices, donor_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 3
	except:
		None
	try:
		arrays_prot_pharmatypes[np.in1d(list_protindices, acceptor_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 4
	except:
		None
	try:
		arrays_prot_pharmatypes[np.in1d(list_protindices, doneptor_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 5
	except:
		None
	try:
		arrays_prot_pharmatypes[np.in1d(list_protindices, negative_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 6
	except:
		None
	try:
		arrays_prot_pharmatypes[np.in1d(list_protindices, positive_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 7
	except:
		None
	# If there is no cys/his/metal, it crashes because of a None object
	# Didnt extend this to the former selections because they're unlikely to be empty
	try:
		arrays_prot_pharmatypes[np.in1d(list_protindices, cys_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 8
	except:
		None
	try:
		arrays_prot_pharmatypes[np.in1d(list_protindices, his_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 9
	except:
		None
	try:
		arrays_prot_pharmatypes[np.in1d(list_protindices, metal_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 10
	except:
		None

	# Add a none cavity point for when the tree query later returns a dummy
	# index when distances are > threshold (query returns this value as dummy index when there is not "hit" within dist)
	arrays_prot_pharmatypes[len(selection_coords)] = 0
	# Identify grid points within distance of 
	# protein points with the aforementioned grid types
	cav_properties = []
	for cav in cavities:
		# Generate a list of 0 corresponding to cavity point indices
		cav_indices = np.zeros(shape=(len(cav), 3), dtype = "i")
		
		tree = cKDTree(selection_coords, compact_nodes = False, balanced_tree = False)
		# Here we find the list of the 3 closest neighbors

		dist, prot_indices = tree.query(cav, k = 3, distance_upper_bound = 5.0)
		
		cav_indices = arrays_prot_pharmatypes[prot_indices]

		cav_properties.append(cav_indices)

	return cav_properties



def export_hydrophobicity(pharmacophore_types, cavid):
	"""
	Prints the % of hydrophobicity of the cavity
	"""
	unique, counts = np.unique(pharmacophore_types[cavid][:,0], return_counts=True)
	dico = dict(zip(unique, counts))
	size = len(pharmacophore_types[cavid])
	try: hydro = (dico[1]+dico[2])/size
	except:
		try:
			hydro = dico[1]/size
		except:
			# WTF no aliphatic atoms in pocket????
			try:
				hydro = dico[2]/size
			except:
				# No aliph and no arom in pocket, that sounds weird
				hydro = 0.
				
	return hydro

def combine_filterhydro(cavities_info, cavities, pharmacophore_types, max_hydrophobicity = 0.8):
	"""
	Combines information from cavities_info, calculate hydrophobicity of the cavity, filter
	cavities with an hydrophobicity above threshold
	"""

	exclusion_list = []
	info_list = []
	for key, value in cavities_info.items():
		hydro = export_hydrophobicity(pharmacophore_types, key)
		if hydro > max_hydrophobicity: 
			exclusion_list.append(key)
		else:
			cavities_info[key].insert(4, hydro)
			info_list.append([key - len(exclusion_list), value[3], value[0], value[1], value[2], value[4]])

	try:
		final_cav = np.delete(cavities, exclusion_list, 0)
		final_pharma = np.delete(pharmacophore_types, exclusion_list, 0)
	except:
		# No exclusion
		None

	return final_cav, final_pharma, info_list

def check_protein_res(cavities, selection_coords, selection_protein, dict_pdb_info):
	"""
	Investigates what protein atoms are lining the cavity
	Checks if the cavity is between protein chains, if there is residues
	with alternative conformations, missing atoms or residues
	"""
	
	set_of_prot = SetOfPoints(selection_coords)
	cavid = 0
	cav_dict = {}
	# Extract list of missing residues /!\ not atoms, which are easier to deal with
	try:
		missres = dict_pdb_info["MissingRes"]
		missres_noname = [x[4:] for x in missres]
	except:
		missres_noname = None

	for cavity in cavities:
		cav_dict[cavid] = {}
		within = set_of_prot.print_indices_within(cavity, max_distance = 5.0)
		vicinity = np.unique(within["i"])
		sel = selection_protein[vicinity]
		# Check if the cavity is within a chain of interchain
		if len(np.unique(sel.getChids())) == 1:
			cav_dict[cavid]["interchain"] = 0
			cav_dict[cavid]["chains"] = "".join(np.unique(sel.getChids()))
		else:
			cav_dict[cavid]["chains"] = "".join(np.unique(sel.getChids()))
			cav_dict[cavid]["interchain"] = 1
		# Check if there is residues with alternative conformations
		if len(np.unique(sel.getAltlocs())) == 1:
			cav_dict[cavid]["altlocs"] = 0
		else:
			cav_dict[cavid]["altlocs"] = 1

		list_prot_vicinity = []
		for i in range(0, len(sel)):
			list_prot_vicinity.append("{0:<3s} {1}{2:>4d}".format(sel.getResnames()[i], sel.getChids()[i], sel.getResnums()[i]))
		uniq_prot_vicinity = set(list_prot_vicinity)
		# Store cavity surroundings, in case it's useful
		cav_dict[cavid]["cavity_residues"] = uniq_prot_vicinity
		# If there's an intersection between the two lists, flag the cavity
		if (uniq_prot_vicinity & set(dict_pdb_info["MissingAtomsRes"])):
			cav_dict[cavid]["missingatoms"] = 1
		else:
			cav_dict[cavid]["missingatoms"] = 0
		
		# flag if missing atom, check +/- 1 position of missing residues?
		currres_noname = [x[4:] for x in uniq_prot_vicinity]
		# Check residues at +1 and -1 of protein residues forming the cavity
		# if there's missing residues
		curres_plusminusone = [[f'{x[0]}{int(x[1:])-1:>4d}', f'{x[0]}{int(x[1:])+1:>4d}']
					for x in currres_noname]
		flat_list = [item for sublist in curres_plusminusone for item in sublist]
		if (set(flat_list) & set(missres_noname)):
			cav_dict[cavid]["missingres"] = 1
		else:
			cav_dict[cavid]["missingres"] = 0


		cavid += 1


	return cav_dict

def get_local_asph_point(point, cavity_coords, grid, grid_min, grid_shape, radius = 3):
	"""
	Returns the asphericity of the cavity (at cubic radius X) of a grid point,
	centered on that grid point
	"""
	# Get list based transformation vectors
	# Here we don't scan the 14 directions but 
	# rather find all grid points of the cube of radius X
	transf_indices = list_transform_indices2(product(range(-radius,radius+1), repeat = 3), grid_shape)
	index_point = get_index_of_coor(point, grid_min, grid_shape)
	# Get transformation indices around index_point, excluding negative values
	flatten = lambda l: [item + index_point for item in l if item + index_point >= 0]
	surrounding_indices = flatten(transf_indices)
	# Check if these indices belong to the cavity
	indices_cav = get_index_of_coor_list(cavity_coords, grid_min, grid_shape)
	truth = np.isin(surrounding_indices, indices_cav, assume_unique = True)
	kept_indices = np.array(surrounding_indices, dtype=int)[np.nonzero(truth)[0]]
	coords_cube = grid[kept_indices]
	IA, IB, IC = calc_moments_of_inertia(coords_cube, point)
	asph = calc_asphericity(IA, IB, IC)
	return asph#, coords_cube, kept_indices

def get_list_asph(final_cavities, grid, grid_min, grid_shape, radius = 3):
	"""
	Uses previous function to return a list of lists of asphericities
	"""

	list_asph = []
	for cav in final_cavities:
		list_asph_cavtmp = []
		for point in cav:
			asph = get_local_asph_point(point, cav, grid, grid_min, grid_shape, radius)
			list_asph_cavtmp.append(asph)
		list_asph.append(list_asph_cavtmp)

	return list_asph

###### Not used right now in the main.py script, but kept in case
def get_local_weight(cavity_coords, grid_min, grid_shape, grid_decomposition, radius = 2):
	"""
	This function aims at calculating a "weight score" for a point
	For each grid point, the cubic vicinity is investigated at radius (3)
	At radius 3, 343 points cavity points max can be around. We first calculate 
	how many cavity points there is.
	Then we calculate their average buriedness. The score is defined as number of
	points * (10 ** (avg_buriedness/10))
	On one side, this score may be used to trim cavity points: below a certain threshold
	=> exclude the point. The lowest the score, the less cavity neighbors it has and
	the less buried its neighbors are. The original idea was to cut "tubes" that 
	connects two cavities, or when cavities overspan. This is slightly inspired by
	PASS probe weight function
	On the other side, that can also be used to identify "hotspots" for binding
	A point that is very buried and very surrounded by cavity points may be an interesting
	point to target for putting the anchor headgroup of a ligand.
	"""
	scores = []
	indices_cav = get_index_of_coor_list(cavity_coords, grid_min, grid_shape)
	for point in cavity_coords:
		index_point = get_index_of_coor(point, grid_min, grid_shape)
		# Get list based transformation vectors
		# Here we don't scan the 14 directions but 
		# rather find all grid points of the cube of radius X
		transf_indices = list_transform_indices2(product(range(-radius,radius+1), repeat = 3), grid_shape)
		# Get transformation indices around index_point, excluding negative values
		flatten = lambda l: [item + index_point for item in l if item + index_point >= 0]
		surrounding_indices = flatten(transf_indices)
		# Check if these indices belong to the cavity
		truth = np.isin(surrounding_indices, indices_cav, assume_unique = True)
		kept_indices = np.array(surrounding_indices, dtype=int)[np.nonzero(truth)[0]]
		average_buriedness = np.average(grid_decomposition[kept_indices])
		score = round((10**(average_buriedness/10)) * len(kept_indices))
		#print(score)
		scores.append(score)
	return scores

def trim_cavity_bylocalweight(cavities_coords, grid_min, grid_shape, grid_decomposition, radius = 2, score = 500):
	"""
	Function related to get_local_weight used to filter out cavity points with a score < X
	"""
	#trimmed_array_cavs = []
	#for cavity in cavities_coords:
	to_trim = None
	scores_cav = get_local_weight(cavities_coords, grid_min, grid_shape, grid_decomposition, radius)
	to_trim = np.where(np.array(scores_cav) < score)[0]
	trimmed_cav = np.delete(arr = cavities_coords, obj = to_trim, axis = 0)
	#trimmed_array_cavs.append(trimmed_cav)
	
	return trimmed_cav








######## OLD FUNCITOSN IN CASE


#def set_pharmacophore_type(cavities, selection_protein, selection_coords):
#	"""
#	Assign the pharmacophore types to grid points.
#	The grid points are aliphatic, aromatic, donor, acceptor, doneptor (both donor/acceptor),
#	negative, positive, CYS, HIS, metal
#	It assigns the type from the closest protein atom, with a max distance of 5A
#	In the case of donor/acceptor/doneptor, a second threshold is set as a maximum distance
#	of 3.9A. If this criterium is not met, the grid point is assigned to the second closest
#	protein atom neighbor (if it is not an acceptor/donor/doneptor, which would necessarily be
#	at a larger distance than 3.9A). Same for CYS/HIS with 4.01A.
#	The investigation is stopped at the second neighbor. If the second neigbor is still an 
#	HBD/HBA/doneptor, the type "none" is assigned, as for any point not contacting the protein
#	at 5A.
#	Types are assigned as integers: 0 for none, and starts at 2 for aliphatic, with a final
#	of 11 for metals, in the same order as described earlier
#	Returns an array of arrays (array of cavities). Each array contains the pharmacophore integers at each indice of
#	the cavity point from the input data "cavities".
#	"""
#
#	# Select the different pharmacophores 
#	aliphatic_atoms_sel = selection_protein.select("(resname ALA and (name C or name CA or name CB)) or (resname ARG and (name C or name CA or name CB or name CG or name CD)) or (resname ASN and (name C or name CA or name CB or name CG)) or (resname ASP and (name C or name CA or name CB)) or (resname CYS and (name C or name CA or name CB)) or (resname GLN and (name C or name CA or name CB or name CG or name CD)) or (resname GLU and (name C or name CA or name CB or name CG)) or (resname GLY and (name C or name CA)) or (resname HIS and (name C or name CA or name CB)) or (resname ILE and (sidechain or name C or name CA)) or (resname LEU and (sidechain or name C or name CA)) or (resname LYS and (name C or name CA or name CB or name CG or name D)) or (resname MET and (sidechain or name C or name CA)) or (resname PHE and (name C or name CA or name CB)) or (resname PRO and (name C or name CA or name CD or name CB or name CG)) or (resname SER and (name C or name CA or name CG)) or (resname THR and (name C or name CA or name CB or name CG2)) or (resname TRP and (name C or name CA or name CB)) or (resname TYR and (name C or name CA or name CB)) or (resname VAL and (sidechain or name C or name CA))")
#	aromatic_atoms_sel = selection_protein.select("(resname PHE and (name CG or name CD1 or name CE1 or name CZ or name CE2 or name CD2)) or (resname TYR and (name CG or name CD1 or name CE1 or name CZ or name CE2 or name CD2)) or (resname TRP and (name CG or name CD1 or name CE2 or name CD2 or name CE3 or name CZ3 or name CH2 or name CZ2))")
#	donor_atoms_sel = selection_protein.select("(resname TRP and (name NE1)) or (name N and not resname PRO)")
#	acceptor_atoms_sel = selection_protein.select("(name O) or (name N and resname PRO)")
#	doneptor_atoms_sel = selection_protein.select("(resname SER and (name OG)) or (resname TYR and (name OH)) or (resname THR and (name OG1)) or (resname ASN and (name OD1 or name ND2)) or (resname GLN and (name OE1 or name NE2)) or (resname HOH)")
#	negative_atoms_sel = selection_protein.select("(resname ASP and (name OD1 or name OD2 or name CG)) or (resname GLU and (name OE1 or name OE2 or name CD))")
#	positive_atoms_sel = selection_protein.select("(resname ARG and (name NE or name CZ or name NH1 or name NH2)) or (resname LYS and (name CE or name NZ))")
#	cys_atoms_sel = selection_protein.select("(resname CYS and (name SG))")
#	his_atoms_sel = selection_protein.select("(resname HIS and (name CG or name ND1 or name CD2 or name NE2 or name CE1))")
#	metal_atoms_sel = selection_protein.select("resname CO or resname ZN or resname MG or resname FE or resname GA or resname IN or resname NI or resname RE or resname PB or resname AS or resname BE or resname CU or resname V or resname AL or resname MN or resname CA")
#
#	
#	# Store their pharmacophore types as their indices in an array
#	arrays_prot_pharmatypes = np.zeros(len(selection_coords), dtype="i")
#	# getIndices from prody only returns the original indices
#	# from the PDB file and not 
#	list_protindices = selection_protein.getIndices()
#	
#	arrays_prot_pharmatypes[np.in1d(list_protindices, aliphatic_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 2
#	# Bugged once because no aromatic atoms?
#	try:
#		arrays_prot_pharmatypes[np.in1d(list_protindices, aromatic_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 3
#	except:
#		None
#	try:
#		arrays_prot_pharmatypes[np.in1d(list_protindices, donor_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 4
#	except:
#		None
#	try:
#		arrays_prot_pharmatypes[np.in1d(list_protindices, acceptor_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 5
#	except:
#		None
#	try:
#		arrays_prot_pharmatypes[np.in1d(list_protindices, doneptor_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 6
#	except:
#		None
#	try:
#		arrays_prot_pharmatypes[np.in1d(list_protindices, negative_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 7
#	except:
#		None
#	try:
#		arrays_prot_pharmatypes[np.in1d(list_protindices, positive_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 8
#	except:
#		None
#	# If there is no cys/his/metal, it crashes because of a None object
#	# Didnt extend this to the former selections because they're unlikely to be empty
#	try:
#		arrays_prot_pharmatypes[np.in1d(list_protindices, cys_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 9
#	except:
#		None
#	try:
#		arrays_prot_pharmatypes[np.in1d(list_protindices, his_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 10
#	except:
#		None
#	try:
#		arrays_prot_pharmatypes[np.in1d(list_protindices, metal_atoms_sel.getIndices(), assume_unique=True).nonzero()[0]] = 11
#	except:
#		None
#	# Identify grid points within distance of 
#	# protein points with the aforementioned grid types
#	cav_properties = []
#	for cav in cavities:
#		# Generate a list of 0 corresponding to cavity point indices
#		cav_indices = np.zeros(shape=len(cav), dtype = "i")
#		
#		tree = cKDTree(selection_coords, compact_nodes = False, balanced_tree = False)
#		# Here we find the list of the two closest neighbors
#		# in case the first one is HBD/HBA/etc and falls after the other
#		# distance cutoff, to set the type as the second closest neighbor
#		dist, prot_indices = tree.query(cav, k = 2, distance_upper_bound = 5.0)
#		idx = 0
#		for cavpoint in cav:
#			dist1 = dist[idx][0]
#			dist2 = dist[idx][1]
#			if dist1 > 5:
#				cav_indices[idx] = 0
#			else:
#				type1 = arrays_prot_pharmatypes[prot_indices[idx][0]]
#				try:
#					type2 = arrays_prot_pharmatypes[prot_indices[idx][1]]
#				except:
#					type2 = 0
#				
#				if type1 != 2 and type1 != 3 and type1 != 4 and type1 != 9 and type1 != 10:
#					cav_indices[idx] = type1
#				else:
#					if type1 != 9 and type1 != 10:
#						if dist1 < 3.9:
#							cav_indices[idx] = type1
#						else:
#							if dist2 > 5:
#								cav_indices[idx] = 0
#							else:
#								if type2 != 2 and type2 != 3 and type2 != 4:
#									cav_indices[idx] = type2
#								else:
#									cav_indices[idx] = 0
#					else:
#						if dist1 < 4.01:
#							cav_indices[idx] = type1
#						else:
#							if dist2 > 5:
#								cav_indices[idx] = 0
#							else:
#								if type2 != 2 and type2 != 3 and type2 != 4 and type2 !=9 and type2 !=10:
#									cav_indices[idx] = type2
#								else:
#									cav_indices[idx] = 0 
#	
#			idx+=1
#	
#		cav_properties.append(cav_indices)
#
#	return cav_properties
#
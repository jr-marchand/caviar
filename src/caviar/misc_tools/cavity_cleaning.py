# -*- coding: utf-8 -*-
"""
This module contains miscellaneous functions
used as support in main.py
The goal is to put here all the functions related to postprocessing the cavity ensembles
At the end of cavity identification
"""

import numpy as np
from caviar.cavity_identification.geometry import SetOfPoints

__all__ = ['cavity_cleansing']


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

def join_information_cavities(cav_flags, filtered_cavities, info_list, exclude_missing = True, exclude_interchain = True,
	exclude_altlocs = False):
	"""
	This function aims at combining information in cav_flags and info_list in a dictionary
	that contains everything
	This dictionary will be filtered according to flags: do we want interchain cavities?
	Do we want to exclude cavities with missing atoms/residues? With alternative locations?

	The resulting dictionary will have as keys the cavities passing the filters
	and as values the keys of a dictionary
	This subdictionary has all the information as keys:
	interchain (bool)
	altlocs (bool)
	cavity_residues (list)
	missingatoms (bool)
	missingres (bool)
	score (float)
	size (int)
	median_buriedness (int)
	7thq_buriedness (int)
	hydrophobicity (float, is a percentage)
	"""

	dict_all_info = {}

	for i in range(0,len(filtered_cavities)):
		cav_flags[i]["score"] = info_list[i][1]
		cav_flags[i]["size"] = info_list[i][2]
		cav_flags[i]["median_buriedness"] = info_list[i][3]
		cav_flags[i]["7thq_buriedness"] = info_list[i][4]
		cav_flags[i]["hydrophobicity"] = round(info_list[i][5], 2)
	
		if exclude_missing == True and exclude_interchain == False and exclude_altlocs == False:
			if cav_flags[i]["missingres"] == 0 and cav_flags[i]["missingatoms"] == 0:
				dict_all_info[i] = cav_flags[i]
		elif exclude_missing == True and exclude_interchain == True and exclude_altlocs == False:
			if cav_flags[i]["missingres"] == 0 and cav_flags[i]["missingatoms"] == 0 and cav_flags[i]["interchain"] == 0:
				dict_all_info[i] = cav_flags[i]
		elif exclude_missing == True and exclude_interchain == True and exclude_altlocs == True:
			if cav_flags[i]["missingres"] == 0 and cav_flags[i]["missingatoms"] == 0 and cav_flags[i]["interchain"] == 0 and cav_flags[i]["altlocs"] == 0:
				dict_all_info[i] = cav_flags[i]
		elif exclude_missing == False and exclude_interchain == True and exclude_altlocs == False:
			if cav_flags[i]["interchain"] == 0:
				dict_all_info[i] = cav_flags[i]
		elif exclude_missing == False and exclude_interchain == True and exclude_altlocs == True:
			if cav_flags[i]["interchain"] == 0 and cav_flags[i]["altlocs"] == 0:
				dict_all_info[i] = cav_flags[i]
		elif exclude_missing == False and exclude_interchain == False and exclude_altlocs == True:
			if cav_flags[i]["altlocs"] == 0:
				dict_all_info[i] = cav_flags[i]
		elif exclude_missing == True and exclude_interchain == False and exclude_altlocs == True:
			if cav_flags[i]["missingres"] == 0 and cav_flags[i]["missingatoms"] == 0 and cav_flags[i]["altlocs"] == 0:
				dict_all_info[i] = cav_flags[i]
	if exclude_missing == False and exclude_interchain == False and exclude_altlocs == False:
		dict_all_info = cav_flags

	return dict_all_info


def get_final_sorted_cavs(dict_all_info, filtered_cavities):
	"""
	Uses dict_all_info to rank cavities for further exploitation (FP, export as PDB...)
	and exclude few more cavities
	"""
	# scores will contain the scores of filtered cavities
	scores = []
	# ori_order will contain the original indices of the cavities 
	# in filtered_cavities
	ori_order = []
	for keys, items in dict_all_info.items():
		scores.append(dict_all_info[keys]["score"])
		ori_order.append(keys)
	order = sorted(range(len(scores)), key=lambda k: scores[k], reverse = True)
	final_cavities = filtered_cavities[ori_order][order]

	return final_cavities, [ori_order[x] for x in order]


def cavity_cleansing(cavities_info, cavities, pharmacophore_types, max_hydrophobicity,
	selection_coords, selection_protein, dict_pdb_info,
	exclude_missing, exclude_interchain, exclude_altlocs):
	"""
	Takes what was previously in main.py in the aforecoded functions and wraps them as one here
	Combine information, exclude the cavities that were filtered before + cavities that are too
	hydrophobic (max_hydrophobicity), find residues lining the cavities, and lots of information
	And ranks cavities
	"""

	# Combine information, exclude the cavities that were filtered before + cavities that are too
	# hydrophobic (max_hydrophobicity)
	filtered_cavities, filtered_pharma, info_list = combine_filterhydro(cavities_info, cavities, pharmacophore_types,
		max_hydrophobicity)

	# Check if cavities are interchain cavities, miss residues/atoms, contain altloc atoms
	cav_flags = check_protein_res(filtered_cavities, selection_coords, selection_protein, dict_pdb_info)
	# Join this information with the scores previously calculated in a dictionary containing everything
	dict_all_info = join_information_cavities(cav_flags, filtered_cavities, info_list, exclude_missing,
								exclude_interchain, exclude_altlocs)

	# Rank cavities for futher exploitation, exclude if flags (defined in the previous function)
	final_cavities, order = get_final_sorted_cavs(dict_all_info, filtered_cavities)

	dict_info_correct_ID = {}
	idx = 0
	final_pharma = []
	for cavid in order:
		final_pharma.append(filtered_pharma[cavid])
		dict_info_correct_ID[idx] = dict_all_info[cavid]
		idx+=1

	return final_cavities, final_pharma, dict_info_correct_ID

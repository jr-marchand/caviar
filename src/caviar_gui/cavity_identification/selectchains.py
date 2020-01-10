# -*- coding: utf-8 -*-
"""
This module contains algorithms to choose what PDB atoms to keep for further investigation.
According to the keyword in main.py, one can choose to keep all protein chains, only the 
longest, or the longest + its neighbors. One can also keep metals, or very well coordinated
water molecules (>= 3 hydrogen bonds with the protein)
"""

import sys
from cavitome_gui.prody_parser.atomic.atomgroup import AtomGroup
from cavitome_gui.prody_parser.atomic import select
from cavitome_gui.prody_parser.proteins.pdbfile import parsePDB
from .geometry import SetOfPoints, Point
from cavitome_gui.misc_tools.misc import get_residues_fromsel

__all__ = ['find_longest_chain', 'find_contacting_chains', 'get_chains_of_interest', 'select_objects', 'get_ligand']


def find_longest_chain(protein_selection, threshold_nres = 30):
	"""
	Finds the longest protein chain in the PDB
	Self is a AtomGroup type (from parsePDB().select("protein"))
	(ie a selection object from ProDy)
	Returns a list containing an array (index 0)
	with the coordinates of the longest chain
	and a string (index 1) with its chain ID
	"""

	list_of_chains = set(protein_selection.getChids())
	biggest = ""
	size = 0
	onlypeptide = True
	for chain in list_of_chains:
		test = protein_selection.select(f"chain {chain}")
		if len(set(test.getResindices())) <= threshold_nres:
			# Too small, skip
			continue
		else:
			onlypeptide = False
			tmp = test.numAtoms()
			if tmp > size:
				biggest = chain
				size = tmp
	if onlypeptide:
		# Nothing is big enough
		return None, None
	
	longest_coords = protein_selection.select(f"chain {biggest}").getCoords()
	return longest_coords, biggest;


def find_contacting_chains(atomgroup1, longest_chain, protein_selection,
	distance = 5, threshold_nres = 30, min_contacts = 75):
	"""
	Finds chains in contact with a certain chain of interest in the PDB
	The distance for a contact is defaulted at 5A
	The threshold for a "protein chain" rather than a peptide
	is put at 30 by default
	Returns a list of chains
	"""
	list_of_chains = set(protein_selection.getChids())
	list_of_chains.remove(longest_chain)
	contact_chains = []
	for chain in list_of_chains:
		selection = protein_selection.select(f"chain {chain}")
		if len(set(selection.getResindices())) > threshold_nres:
			test = selection.getCoords()
			# Not only we look for the contacting chains
			# But also possibility to put a threshold of a minimum
			# number of contacts: symmetric units may have fewer contacts
			# than actual 
			contacts = SetOfPoints(atomgroup1).in_range_settoset(test, distance, asbool = False)
			#print(len(contacts[0]), len(contacts[1]))
			if len(contacts[0]) >= min_contacts:
				#print(len(contacts[0]), min_contacts)
				contact_chains.append(chain)

	return contact_chains;

def get_chains_of_interest(protein_selection, distance = 5, threshold_nres = 30, userspecified = False, min_contacts = 75):
	"""
	Uses find_longest_chain() and find_contacting_chains()
	to return an array containing the coordinates of the
	(protein) points of interest, ie, longest chain and 
	its neighbours at a distance "distance", default to 5
	and with a minimum number of residue (30) to exclude peptides
	Returns coordinates as np.array
	"""

	if userspecified:
		chains_selection = protein_selection.select(f"chain {' or chain '.join([x for x in userspecified])}")
		try:
			return chains_selection.getCoords(), chains_selection
		except:
			return None, None
	
	else:
		longest, longest_id = find_longest_chain(protein_selection, threshold_nres)
		
		try:
			longest.any()
			# Too small, again
		except:
			return None, None
	
	
		chains_of_interest = find_contacting_chains(longest, longest_id, protein_selection,
			distance, threshold_nres, min_contacts = min_contacts)
		chains_of_interest.append(longest_id)
		tmpstr = " ".join(chains_of_interest)
		chains_selection = protein_selection.select(f"chain {tmpstr}")
		return chains_selection.getCoords(), chains_selection;


def select_objects(pdbobject, metal = False, water = False, threshold_nres = 30, what = "allproteins", userspecified = False,
	min_contacts = 75, structural_ligand = False):
	"""
	Calls ProDy selection algebra in order to select objects in the PDB (eg protein chains 
	with more than threshold_nres residues)
	By default, it selects only the protein, but can also export metals and waters
	The what keyword defines if we should keep all of the protein chains, or simply the longest chain
	or the largest + contacting chains. Possible keywords: "allproteins", "longestchain", "longestandcontacting"
	"""
	pdb_coords = SetOfPoints(pdbobject.getCoords())
	protein_selection = pdbobject.select("protein and not hydrogen")

	if not protein_selection:
		# No protein in file
		return None

	### Define what part of the protein do we keep
	### all chains, longest chain, longest+contacting chains
	# Flag if only peptides
	onlypeptide = True
	if what == "allproteins":
		list_of_chains = set(protein_selection.getChids())
		prot_sel = "protein and not hydrogen"
		# Why did I wrote all of that?
		# Ah for excluding peptides ofc
		tmp = " and (chain "
		flag = False
		for chain in list_of_chains:
			ch_sel = protein_selection.select(f"chain {chain}")
			if len(set(ch_sel.getResindices())) > threshold_nres:
				if flag:
					tmp += f" or chain {chain}"
				else:
					tmp += f"{chain}"
					flag = True 
					onlypeptide = False
		prot_sel += tmp
		prot_sel += ")"
		if onlypeptide:
			# There is no protein chain long enough
			return None

	elif what == "longestchain":
		dummy, selected_l_c = get_chains_of_interest(protein_selection, distance = 0, threshold_nres = threshold_nres, 
			userspecified = userspecified)
		try:
			prot_sel = selected_l_c.getSelstr()
		except:
			# too small!
			return None
	elif what == "longestandcontacting":
		dummy, selected_l_c = get_chains_of_interest(protein_selection, distance = 5, threshold_nres = threshold_nres,
			userspecified = userspecified, min_contacts = min_contacts)
		try:
			prot_sel = selected_l_c.getSelstr()
		except:
			# too small!
			return None

	else:
		print("Fatal: what keyword should be chosen within these possibilites:"
			"'allproteins', 'longestchain', 'longestandcontacting' ")
		sys.exit(-1)
	
	selection = prot_sel
	water_sel = ""
	metal_sel = ""

	### Add metals to the selection 
	if metal:
		metal_sel = " or resname CO or resname ZN or resname MG or resname FE or resname GA or resname IN or resname NI"
		"or resname RE or resname PB or resname AS or resname BE or resname CU or resname V or resname AL or resname MN or resname CA"
		selection += metal_sel

	### Add "structural waters" to the selection
	if water:
		## Keep water if they are within 3A of at least 3 HBD/A of the protein
		try: # Maybe there's no water, then that would crash
			all_waters = pdbobject.select("water")
			prot_hbad = pdbobject.select(f"{prot_sel} and (element N or element O)")
			index = 0
			tmpwatkeep = []
			for wat in all_waters.getCoords():
				counter = 0
				for atom in prot_hbad.getCoords():
					if Point(wat).in_range(atom, 3.1):
						counter+=1
				if counter > 2:
					tmpwatkeep.append(index)
				index += 1
			bla = all_waters[tmpwatkeep].getIndices()
			water_sel = " or index "
			water_sel += " or index ".join(str(x) for x in bla.tolist())
			selection += water_sel
		except:
			water_sel = ""

	### Add metals to the selection 
	if structural_ligand:
		lig_sel = f" or resname {structural_ligand}"
		selection += lig_sel

	
	return selection

def get_ligand(pdbobject, tabu_list = "misc_tools/tabu_lists/tabulist_ligand_min_peptides_nucleic_sugars",
	returnsel = False, lig_id = False):
	"""
	Function to select potential ligands
	Reads a tabu list (full path) to exclude HETATM that are
	most likely either protein, RNA, sugar, cofactors, metals,
	cosolvent for crystallography...
	Default list from www.ccp4.ac.uk/html/refmac5/dictionary/list-of-ligands.html
	"""

	# Start with generating the selection string from the tabu_list
	if lig_id:
		hetatm = pdbobject.select(f"resname {lig_id}")
		if not hetatm:
			if returnsel:
				return None, None, None
			else:
				return None, None
		else:
			# Return a list of coordinates for each ligand and a list of names!
			uniq_res = get_residues_fromsel(hetatm)
			list_ligands = []
			list_lig_coords = []
			list_lig_sel = []
			for ligand in uniq_res:
				list_ligands.append(ligand)
				# Here if the ligand has a negative number it will crash. Happened with 1NWT and 3mg9
				if int(ligand[5:9]) > 0:
					tmpsel = hetatm.select(f"resname {ligand[0:3]} and chain {ligand[4]} and resnum {ligand[5:9]}")
					list_lig_sel.append(tmpsel)
					coords = tmpsel.getCoords()
					list_lig_coords.append(coords)

	else:
		tabu_string = "hetero and not hydrogen "
		if tabu_list:
			with open(tabu_list) as tabulist:
				for tabures in tabulist:
					if tabures[0] != "#":
						tabu_string += f"and not resname {tabures[:3]} "
		hetatm = pdbobject.select(tabu_string)
	
		if not hetatm:
			if returnsel:
				return None, None, None
			else:
				return None, None
		else:
			# Return a list of coordinates for each ligand and a list of names!
			uniq_res = get_residues_fromsel(hetatm)
			list_ligands = []
			list_lig_coords = []
			list_lig_sel = []
			for ligand in uniq_res:
				list_ligands.append(ligand)
				# Here if the ligand has a negative number it will crash. Happened with 1NWT and 3mg9
				if int(ligand[5:9]) > 0:
					tmpsel = hetatm.select(f"resname {ligand[0:3]} and chain {ligand[4]} and resnum {ligand[5:9]}")
					list_lig_sel.append(tmpsel)
					coords = tmpsel.getCoords()
					list_lig_coords.append(coords)

	if returnsel:
		return list_ligands, list_lig_coords, list_lig_sel
	else:
		return list_ligands, list_lig_coords


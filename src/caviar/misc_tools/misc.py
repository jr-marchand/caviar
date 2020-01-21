# -*- coding: utf-8 -*-
"""
This module contains miscellaneous functions
used as support in main.py
These functions don't really belong anywhere else
The first function gets information from the PDB header
The second function gathers all cavity information from different functions
and exports them in a joined dictionary

The last function exports cavities as a PDB file for vizualisation
"""

from caviar.prody_parser.proteins import pdbfile
from caviar.prody_parser.proteins.header import parsePDBHeader
from caviar.cavity_identification.gridtools import get_index_of_coor_list
import numpy as np
from caviar.cavity_identification.geometry import SetOfPoints

__all__ = ['get_information_header', 'kill_from_header', 'get_residues_fromsel', 'export_pdb_cavity',
			'print_scores', 'find_ligand_presence', 'simple_export_pdb_noinfo', 'simple_export_pdb_onecav',
			'export_clean_cav_ligand_info', 'export_pdb_subcavities']


def get_information_header(pdbfile):
	"""
	This function aims at storing data from the PDB header
	Notably: B factors, missing residues, missing atoms,
	resolution, caveat, obsolete, source, DOI, PDB version
	revision, R values, deposition date, experiment type, 
	space group, title, classification, chemicals, dbrefs,
	mutations, engineered, EC, ...
	Keywords are self explanatory
	"""

	dict_pdb_info = {}

	try:
		header_info = parsePDBHeader(pdbfile)
	except:
		print(pdbfile, "does not exist")
		return None

	try:
		dict_pdb_info["experiment"] = header_info["experiment"]
	except:
		dict_pdb_info["experiment"] = "absent"
	try:
		dict_pdb_info["resolution"] = header_info["resolution"]
	except:
		dict_pdb_info["resolution"] = "absent"
	try:
		dict_pdb_info["pdbversion"] = header_info["version"]
	except:
		dict_pdb_info["pdbversion"] = "absent"
	try:
		dict_pdb_info["doi"] = header_info["reference"]["doi"]
	except:
		dict_pdb_info["doi"] = "absent"
	
	# These information are bool values (presence/absence)
	try:
		dict_pdb_info["caveat"] = header_info["caveat"]
	except:
		dict_pdb_info["caveat"] = 0
	try:
		dict_pdb_info["obsolete"] = header_info["obsolete"]
	except:
		dict_pdb_info["obsolete"] = 0
	# Not bool but there's already an except
	try:
		dict_pdb_info["MissingRes"] = header_info["MissingRes"]
	except:
		dict_pdb_info["MissingRes"] = 0
	try:
		dict_pdb_info["MissingAtomsRes"] = header_info["MissingAtomsRes"]
	except:
		dict_pdb_info["MissingAtomsRes"] = 0
	
	# This returns a dictionary of dictionaries
	# eg, dict_pdb_info["source"]["1"]["orga_sci"]
	# returns 'HOMO SAPIENS'
	try:
		dict_pdb_info["revision"] = header_info["revision"]
	except:
		dict_pdb_info["revision"] = "absent"
	
	# This returns a list with R free and R value
	try:
		dict_pdb_info["Rvalues"] = header_info["Rvalues"]
	except:
		dict_pdb_info["Rvalues"] = "absent"
	try:
		dict_pdb_info["deposition_date"] = header_info["deposition_date"]
	except:
		dict_pdb_info["deposition_date"] = "absent"
	try:
		dict_pdb_info["title"] = header_info["title"]
	except:
		dict_pdb_info["title"] = "absent"
	try:
		dict_pdb_info["space_group"] = header_info["space_group"]
	except:
		dict_pdb_info["space_group"] = "absent"
	try:
		dict_pdb_info["classification"] = header_info["classification"]
	except:
		dict_pdb_info["classification"] = "absent"
	
	# Information about heteroatoms
	# The key returns a list of lists, with resname, number of atoms, chain ID, residue number
	dict_pdb_info["chemicals"] = []
	try:
		for el in header_info["chemicals"]:
   			dict_pdb_info["chemicals"].insert(0, [el.resname, el.natoms, el.chain, el.resnum])
	except:
		dict_pdb_info["chemicals"] = "absent"
	
	# Information about polymers
	dict_pdb_info["polymer_chain_info"] = {}
	dict_pdb_info["modifications"] = []
	# Not a try because the information should be existing (or keys containing None)
	try:
		header_info["polymers"]
		info_poly = True
	except:
		info_poly = False
	if info_poly == True:
		for el in header_info["polymers"]:
			modif = el.modified
			if modif:
				dict_pdb_info["modifications"].insert(0, modif)
			dict_pdb_info["polymer_chain_info"][el.chid] = {}
			dict_pdb_info["polymer_chain_info"][el.chid]["name"] = el.name
			dict_pdb_info["polymer_chain_info"][el.chid]["EC"] = el.ec
			dict_pdb_info["polymer_chain_info"][el.chid]["engineered"] = el.engineered
			dict_pdb_info["polymer_chain_info"][el.chid]["modres"] = modif
			dict_pdb_info["polymer_chain_info"][el.chid]["mutations"] = el.mutation
			dbrefs = el.dbrefs
			flag = False
			for ref in dbrefs:
				flag = False
				if ref.database == "UniProt":
					dict_pdb_info["polymer_chain_info"][el.chid]["uniprot"] = ref.accession
					flag = True
			if flag == False:
				dict_pdb_info["polymer_chain_info"][el.chid]["uniprot"] = "absent"

	return dict_pdb_info

def kill_from_header(dict_pdb_info, onlyxr = True, resolution_filter = False, resolution = 2.5, pdbversion_filter = False, 
	pdbversion = 3.30, caveat = True, obsolete = True, deposition_date_filter = False, date = 2010, printvv = False):
	"""
	Kill the process if this is not the PDB you're looking for
	"""

	def printv(msg):
		"""Prints messages in stdout if verbose is on"""
		if printvv:
			print(msg)

	killswitch = False
	try:
		if onlyxr:
			if not "X-R" in dict_pdb_info["experiment"]:
				killswitch = True
				return killswitch
	except:
		printv("Can't read information: XR")
	try:
		if resolution_filter and float(dict_pdb_info["resolution"]) > resolution:
			killswitch = True
			return killswitch
	except:
		printv("Can't read information: resolution")
	try:
		if pdbversion_filter and float(dict_pdb_info["pdbversion"]) < pdbversion:
			killswitch = True
			return killswitch
	except:
		printv("Can't read information: pdbversion")
	try:
		if caveat and dict_pdb_info["caveat"]:
			killswitch = True
			return killswitch
	except:
		printv("Can't read information: caveat")
	try:
		if obsolete and dict_pdb_info["obsolete"]:
			killswitch = True
			return killswitch
	except:
		printv("Can't read information: obsolete")
	try:
		if deposition_date_filter:
			tmpdate = int(dict_pdb_info["deposition_date"][-2:])
			if tmpdate > 50:
				date = tmpdate + 1900
			elif tmpdate < 50:
				date = tmpdate + 2000
			tmprev = int(dict_pdb_info["revision"][-2:])
			if tmprev > 50:
				revdate = tmprev + 1900
			elif tmprev < 50:
				revdate = tmprev + 2000
			if date < revision_date and revdate < revision_date:
				killswitch = True
				return killswitch
	except:
		printv("Can't read information: date")

	return killswitch


def get_residues_fromsel(selection):
	"""
	From a selection of atoms from ProDy
	Returns a set containing unique "residues names"
	(formatted as PDB: RESNAME CHAIN RESNUM)
	"""
	list_residues = []
	for i in range(0, len(selection)):
		list_residues.append(("{0:<3s} {1}{2:>4d}".format(selection.getResnames()[i], selection.getChids()[i],
			selection.getResnums()[i])))
	uniq = set(list_residues)

	return uniq

def find_ligand_presence(final_cavities, list_ligands, list_lig_coords, pdbcode, printflag = True,
	ligsizeflag = True, ligminsize = 8, tocenter = False):
	"""
	Find if the ligands are enclosed in one of the detected cavities
	returns a dictionary of correspondance key = ligand index in list_ligand
	and value = cavid in (ordered) final_cavities
	"""

	def check_lig_cavity(ligand, final_cavities):
		"""
		Check if ligand is within 1 A of any cavity point
		"""
		size_lig = len(ligand)
		setofpoints_lig = SetOfPoints(ligand)
		idx_cavity = 0
		value = None
		covered = None
		coverage = 0.
		for cav in final_cavities:
			if setofpoints_lig.in_range_settoset(cav, dist_range = 1, asbool = True):
				value = str(idx_cavity)
				covered = len(np.unique(setofpoints_lig.in_range_settoset(cav, dist_range = 1, asbool = False)[0]))
				cav_covered_by_lig = len(np.unique(setofpoints_lig.in_range_settoset(cav, dist_range = 3., asbool = False)[1]))
				size_cav = len(cav) # not really proof for any use, watch out!
				break
			idx_cavity+=1
		try:
			coverage = covered / size_lig
			coverage_cav = cav_covered_by_lig / size_cav # not really proof for any use, watch out!
		except:
			value = "LIG NOT FOUND IN CAVITIES"
			coverage = 0.
			coverage_cav = 0.

		return value, coverage, coverage_cav
	
	def check_lig_center_cavity(ligand, centers):
		"""
		Check if ligand is within 4 A of the center of the cavity
		"""
		setofpoints_lig = SetOfPoints(ligand)
		idx_cavity = 0
		value = None
		for center in centers:
			if setofpoints_lig.in_range_settoset(center, dist_range = 4.0, asbool = True):
				value = str(idx_cavity)
			idx_cavity+=1
		try:
			value
		except:
			value = "LIG NOT FOUND CLOSE TO ANY CAVITY CENTER"
		return value

	if tocenter == True:
		# calculate centers of cavities
		c = []
		for cav in final_cavities:
			c.append(cav.mean(axis = 0))
		centers = np.array(c)

	idx_lig = 0
	dict_coverage = {}
	howbig = []
	if not list_lig_coords:
		if printflag:
			print(f"No ligand")
		return None
	for ligand in list_lig_coords:
		howbig.append(len(ligand))
		if ligsizeflag:
			if howbig[idx_lig] >= ligminsize:
				if tocenter:
					value = check_lig_center_cavity(ligand, centers)
					dict_coverage[str(idx_lig)] = str(value)
				else:
					value, coverage, coverage_cav = check_lig_cavity(ligand, final_cavities)
					dict_coverage[str(idx_lig)] = [str(value), coverage]
			else:
				dict_coverage[str(idx_lig)] = ["LIG IS TOO SMALL", 0.]
		else:
			if tocenter:
				value = check_lig_center_cavity(ligand, centers)
				dict_coverage[str(idx_lig)] = str(value)
			else:
				value, coverage, coverage_cav = check_lig_cavity(ligand, final_cavities)
				dict_coverage[str(idx_lig)] = [str(value), coverage, coverage_cav]
		idx_lig +=1			

	if printflag:
		if tocenter:
			for key, value in dict_coverage.items():
				print(f"Ligand {str(list_ligands[int(key)])} ({howbig[int(key)]} atoms) is found within 4A"
					f" of the center of cavity {str(value)} of {pdbcode}")
		else:
			for key, value in dict_coverage.items():
				print(f"Ligand {str(list_ligands[int(key)])} ({howbig[int(key)]} atoms) is found in cavity {value[0]} of {pdbcode} and has {value[1]*100}% of atoms covered")

	return dict_coverage

def export_clean_cav_ligand_info(dict_coverage, list_ligands, list_lig_coords, cavities):
	"""
	Helpful for storage because with what's above it's a horrible mess
	"""
	try:
		dict_coverage.items()
	except:
		return None, None
	list_covered_ligands = []
	dict_cavid_lig_bool = {}
	for ligid, value in dict_coverage.items():
		if value[1] > 0.3:
			ligname = list_ligands[int(ligid)]
			ligsize = len(list_lig_coords[int(ligid)])
			resname = ligname[0:3]
			chid = ligname[4]
			resnb = ligname[5:]
			# 3 letters code, cavity chain ID, chain ID, residue number, lig size, coverage % 
			list_covered_ligands.append([resname, value[0], chid, resnb, ligsize, value[1]])
			cavities[int(value[0])].liganded = resname
			dict_cavid_lig_bool[value[0]] = 1
		else:
			dict_cavid_lig_bool[value[0]] = 0


	return list_covered_ligands, dict_cavid_lig_bool

def print_scores(dict_all_info, pdbcode, cavities):
	"""
	Returns the information with the order for export (final_cavities)
	"""
	idx = 0
	print(f"PDB_chain  CavID  Ligab.   Score   Size  Hydrophob  Interchain  AltLocs  MissAtoms")
	for cav in range(len(cavities)):
		print(f'{pdbcode}_{dict_all_info[cav]["chains"]}\t{idx+1:>8d}    '
			f'{cavities[idx].ligandability}      '
			f'{dict_all_info[cav]["score"]:>4.1f} '
			f'  {dict_all_info[cav]["size"]:>5d}   '
			f'{dict_all_info[cav]["hydrophobicity"]*100:>8.0f}%         '
			f'{bool(dict_all_info[cav]["interchain"])}          {bool(dict_all_info[cav]["altlocs"])}'
			f'          {bool(dict_all_info[cav]["missingatoms"]+dict_all_info[cav]["missingres"])}')
		idx += 1
		
	return None

def export_pdb_cavity(final_cavities, final_pharma, pdbcode, grid_min, grid_shape,
	grid_decomposition, selection_protein, gridspace = 1.0, outdir = "./", withprot = True,
	listlig = None, oridir = "/db/pdb/"):
	"""
	For visualization purposes: exports a pdb containing 
	"S" atoms for the cavity grid points. The B factor 
	corresponds to the burial level (9-14, 2 for middle
	cavity grid points)
	The occupancy relates to the pharmacophore type (cf correspondance list in
	cavity_characterization.gridpoint_properties set_pharmacophore_type())
	"""

	if withprot:
		from caviar.prody_parser import writePDB
		writePDB(outdir + pdbcode + "_cavs.pdb", selection_protein)
		if listlig:
			ligs = ""
			a = open(oridir+"/"+pdbcode+".pdb", "r")
			file = a.readlines()
			for lig in listlig:
				ligs+="".join([x for x in file if lig in x])
			a.close()
			a = open(outdir + pdbcode + "_cavs.pdb", "a")
			a.write(ligs)
			a.close()

	pdbdummy = []
	cav_indices = get_index_of_coor_list(np.vstack(final_cavities), grid_min, grid_shape, gridspace = gridspace)

	idx = 0
	cavid = 0
	for cavity in final_cavities:
		cavid += 1
		idx_ = 0
		for coordinates in cavity:
			pdbdummy.append(f"HETATM    1  S   GRI A {cavid:>3}    {coordinates[0]:8.3f}{coordinates[1]:8.3f}{coordinates[2]:8.3f}"
				f"  {final_pharma[cavid-1][idx_][0]:>3.2f} {grid_decomposition[cav_indices[idx]]:>5.2f}           S\n")
			idx += 1
			idx_ += 1
	a = open(outdir + pdbcode + "_cavs.pdb", "a")
	a.write("".join(pdbdummy))
	a.close()

	return None


def simple_export_pdb_noinfo(final_cavities, grid_min, grid_shape, gridspace = 1.0):
	"""
	For visualization purposes: exports a pdb containing 
	"S" atoms for the cavity grid points. The B factor 
	corresponds to the burial level (9-14, 2 for middle
	cavity grid points)
	The occupancy relates to the pharmacophore type (cf correspondance list in
	cavity_characterization.gridpoint_properties set_pharmacophore_type())
	"""
	pdbdummy = []
	cav_indices = get_index_of_coor_list(np.vstack(final_cavities), grid_min, grid_shape, gridspace = gridspace)

	idx = 0
	cavid = 0
	for cavity in final_cavities:
		cavid += 1
		idx_ = 0
		for coordinates in cavity:
			pdbdummy.append(f"HETATM    1  S   GRI A {cavid:>3}    {coordinates[0]:8.3f}{coordinates[1]:8.3f}{coordinates[2]:8.3f}"
				f"  1.00   1.00           S\n")
			idx += 1
			idx_ += 1
	a = open("test_cavs.pdb", "w")
	a.write("".join(pdbdummy))
	a.close()

	return None

def simple_export_pdb_onecav(cavity, grid_min, grid_shape, gridspace = 1.0):
	"""
	For visualization purposes: exports a pdb containing 
	"S" atoms for the cavity grid points. The B factor 
	corresponds to the burial level (9-14, 2 for middle
	cavity grid points)
	The occupancy relates to the pharmacophore type (cf correspondance list in
	cavity_characterization.gridpoint_properties set_pharmacophore_type())
	"""
	pdbdummy = []
	cav_indices = get_index_of_coor_list(np.vstack(cavity), grid_min, grid_shape, gridspace = gridspace)

	idx = 0
	cavid = 1
	for coordinates in cavity:
		pdbdummy.append(f"HETATM    1  S   GRI A {cavid:>3}    {coordinates[0]:8.3f}{coordinates[1]:8.3f}{coordinates[2]:8.3f}"
			f"  1.00   1.00           S\n")
	a = open("test_cavs.pdb", "w")
	a.write("".join(pdbdummy))
	a.close()

	return None


def export_pdb_subcavities(subcavs, pdbcode, grid_min, grid_shape, cavid = 1, gridspace = 1.0, outdir = "./",
	listlig = None, oridir = "/db/pdb/"):
	"""

	"""

	if listlig:
		ligs = ""
		a = open(oridir+"/"+pdbcode+".pdb", "r")
		file = a.readlines()
		for lig in listlig:
			ligs+="".join([x for x in file if lig in x])
		a.close()
		a = open(outdir + pdbcode + "_subcavs.pdb", "a")
		a.write(ligs)
		a.close()


	for i in range(0, len(subcavs)):
		pdbdummy = []
		for coordinates in subcavs[i]:
			pdbdummy.append(f"HETATM    1  N   SUB {chr(int(cavid)+96+1).upper()}{i+1:>4}    {coordinates[0]:8.3f}{coordinates[1]:8.3f}"
				f"{coordinates[2]:8.3f}  1.00   1.00           N\n")
		a = open(outdir + pdbcode + "_subcavs.pdb", "a")
		a.write("".join(pdbdummy))
		a.close()

	return None

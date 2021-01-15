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
#from caviar.prody_parser.proteins.ciffile import parseMMCIF
from caviar.prody_parser.proteins.header import parsePDBHeader
from caviar.cavity_identification.gridtools import get_index_of_coor_list
import numpy as np
from caviar.cavity_identification.geometry import SetOfPoints
import os

__all__ = ['get_information_header', 'kill_from_header', 'get_residues_fromsel', 'export_pdb_cavity',
			'print_scores', 'find_ligand_presence', 'simple_export_pdb_noinfo', 'simple_export_pdb_onecav',
			'export_clean_cav_ligand_info', 'export_pdb_subcavities']


def get_information_header(pdbfile, cif = False):
	"""
	This function aims at storing data from the PDB header
	Notably: B factors, missing residues, missing atoms,
	resolution, caveat, obsolete, source, DOI, PDB version
	revision, R values, deposition date, experiment type, 
	space group, title, classification, chemicals, dbrefs,
	mutations, engineered, EC, ...
	Keywords are self explanatory
	"""

	dict_pdb_info = {"experiment": None, "resolution": None, "pdbversion": None, "doi": None, "caveat": None,
	"obsolete": None, "MissingRes": None, "MissingAtomsRes": None, "revision": None, "Rvalues": [None, None],
	"deposition_date": None, "title": None, "space_group": None, "classification": None, "chemicals": None, 
	"polymer_chain_info": {}, "modifications": [], "resolutionEM": None, "pdbxversion": None}

	if cif == True:
			cif_dico = MMCIF2Dict(pdbfile)
			try:
				dict_pdb_info["experiment"] = "".join(cif_dico["_exptl.method"])
			except:
				None
			if "X-R" in dict_pdb_info["experiment"]:
				try:
					dict_pdb_info["resolution"] = "".join(cif_dico["_reflns.d_resolution_high"])
				except:
					None
			else:
				try:
					dict_pdb_info["resolutionEM"] = "".join(cif_dico["_em_3d_reconstruction.resolution"])
				except:
					None
			try:
				dict_pdb_info["pdbxversion"] = "".join(cif_dico['_audit_conform.dict_version'])
			except:
				None
			try:
				dict_pdb_info["doi"] = cif_dico["_citation.pdbx_database_id_DOI"]
			except:
				None
			try:
				dict_pdb_info["caveat"] = cif_dico["_database_PDB_caveat.id"]
			except:
				None				
			try:
				if "obsolete" in str(cif_dico["_pdbx_audit_revision_details.description"]).lower():
					dict_pdb_info["obsolete"] = True
			except:
				None				
			try:
				dict_pdb_info["MissingRes"] = cif_dico["pdbx_missing_residue_list"]
			except:
				None				
			try:
				dict_pdb_info["MissingAtomsRes"] = cif_dico["_rcsb_missing_atom_poly.atom_name"]
			except:
				None				
			try:
				_tmp = cif_dico["_pdbx_audit_revision_history.revision_date"]
				if type(_tmp) == list:
					dict_pdb_info["revision"]  = "".join(_tmp[-1])
				else:
					dict_pdb_info["revision"]  = "".join(_tmp)
			except:
				None				
			try:
				dict_pdb_info["Rvalues"] = ["".join(cif_dico["_refine.ls_R_factor_R_free"]), "".join(cif_dico["_refine.ls_R_factor_R_work"])]
			except:
				None				
			try:
				dict_pdb_info["deposition_date"] = "".join(cif_dico["_pdbx_database_status.recvd_initial_deposition_date"])
			except:
				None				
			try:
				dict_pdb_info["title"] = "".join(cif_dico["_struct.title"])
			except:
				None				
			try:
				dict_pdb_info["space_group"] = "".join(cif_dico["_symmetry.space_group_name_H-M"])
			except:
				None				
			try:
				dict_pdb_info["classification"] = "".join(cif_dico["_struct_keywords.pdbx_keywords"])
			except:
				None				
			return dict_pdb_info
	else:
		try:
			header_info = parsePDBHeader(pdbfile)
		except:
			print(pdbfile, "does not exist")
			return dict_pdb_info

	try:
		dict_pdb_info["experiment"] = header_info["experiment"]
	except:
		dict_pdb_info["experiment"] = None
	try:
		dict_pdb_info["resolution"] = header_info["resolution"]
	except:
		dict_pdb_info["resolution"] = None
	try:
		dict_pdb_info["pdbversion"] = header_info["version"]
	except:
		dict_pdb_info["pdbversion"] = None
	try:
		dict_pdb_info["doi"] = header_info["reference"]["doi"]
	except:
		dict_pdb_info["doi"] = None
	
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
		if len(header_info["MissingRes"]) > 0:
			dict_pdb_info["MissingRes"] = header_info["MissingRes"]
		else:
			dict_pdb_info["MissingRes"] = None
	except:
		dict_pdb_info["MissingRes"] = None
	try:
		if len(header_info["MissingAtomsRes"]) > 0:
			dict_pdb_info["MissingAtomsRes"] = header_info["MissingAtomsRes"]
		else:
			dict_pdb_info["MissingAtomsRes"] = None
	except:
		dict_pdb_info["MissingAtomsRes"] = None
	
	# This returns a dictionary of dictionaries
	# eg, dict_pdb_info["source"]["1"]["orga_sci"]
	# returns 'HOMO SAPIENS'
	try:
		dict_pdb_info["revision"] = header_info["revision"]
	except:
		dict_pdb_info["revision"] = None
	
	# This returns a list with R free and R value
	try:
		dict_pdb_info["Rvalues"] = header_info["Rvalues"]
	except:
		dict_pdb_info["Rvalues"] = [None, None]
	try:
		dict_pdb_info["deposition_date"] = header_info["deposition_date"]
	except:
		dict_pdb_info["deposition_date"] = None
	try:
		dict_pdb_info["title"] = header_info["title"]
	except:
		dict_pdb_info["title"] = None
	try:
		dict_pdb_info["space_group"] = header_info["space_group"]
	except:
		dict_pdb_info["space_group"] = None
	try:
		dict_pdb_info["classification"] = header_info["classification"]
	except:
		dict_pdb_info["classification"] = None
	#print(dict_pdb_info)
	# Information about heteroatoms
	# The key returns a list of lists, with resname, number of atoms, chain ID, residue number
	dict_pdb_info["chemicals"] = []
	try:
		for el in header_info["chemicals"]:
   			dict_pdb_info["chemicals"].insert(0, [el.resname, el.natoms, el.chain, el.resnum])
	except:
		dict_pdb_info["chemicals"] = None
	
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
				dict_pdb_info["polymer_chain_info"][el.chid]["uniprot"] = None

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
			value = "666"
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
			print(f"{pdbcode} : does not have the specified ligand")
		return dict_coverage
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
				print(f"{pdbcode} : Ligand {str(list_ligands[int(key)])} ({howbig[int(key)]} atoms) is found within 4A"
					f" of the center of cavity {str(value)}")
		else:
			for key, value in dict_coverage.items():
				print(f"{pdbcode} : Ligand {str(list_ligands[int(key)])} ({howbig[int(key)]} atoms) is found in cavity {value[0]} and has {value[1]*100}% of atoms covered")

	return dict_coverage

def export_clean_cav_ligand_info(dict_coverage, list_ligands, list_lig_coords, cavities):
	"""
	Helpful for the database storage because with what's above it's a horrible mess
	"""
	try:
		dict_coverage.items()
	except:
		return None, None
	list_covered_ligands = []
	dict_cavid_lig_bool = {}
	for ligid, value in dict_coverage.items():
		if value[1] > 0.01:
			ligname = list_ligands[int(ligid)]
			ligsize = len(list_lig_coords[int(ligid)])
			resname = ligname[0:3]
			chid = ligname[4]
			resnb = ligname[5:]
			# 3 letters code, cavity chain ID, chain ID, residue number, lig size, coverage % 
			list_covered_ligands.append([resname, value[0], chid, resnb, ligsize, value[1]])
			cavities[int(value[0])].liganded = resname
			# Get ligand smiles from epdb API
			try:
				from urllib.request import urlopen
				from json import loads
				import ssl
				# That's a heavy load of imports, but we somehow need to create
				# also a ssl certificate otherwise it crashes
				ssl._create_default_https_context = ssl._create_unverified_context
				with urlopen(f'https://www.ebi.ac.uk/pdbe/api/pdb/compound/summary/{resname}') as response:
					data = loads(response.read().decode('utf8'))
				cavities[int(value[0])].ligsmi = data[resname][0]["smiles"][0]["name"] # 0 is cactvs
				try:
					cavities[int(value[0])].ligsmiOE = data[resname][0]["smiles"][1]["name"] # 1 is openeye
				except:
					cavities[int(value[0])].ligsmiOE = None
			except:
				cavities[int(value[0])].ligsmi = None
			cavities[int(value[0])].sizelig = ligsize
			cavities[int(value[0])].cavcov = value[2]
			cavities[int(value[0])].ligcov = value[1]
			dict_cavid_lig_bool[value[0]] = 1
		else:
			dict_cavid_lig_bool[value[0]] = 0


	return list_covered_ligands, dict_cavid_lig_bool

def print_scores(dict_all_info, pdbcode, cavities, subcavs = False, frame = None):
	"""
	Returns the information with the order for export (final_cavities)
	"""
	# Frame is in case of an NMR with more than one model or DCD file with an MD trajectory
	#  It just appends "_FRAME" with FRAME = model/frame number to the PDB code

	if subcavs:
		print(f"{'PDB_chain':<12}{'CavID':^7}{'Ligab':^6}{'Score':^7}{'Size':^6}{'Hydrophob':^9}"
			f"{'InterCh':^10}{'AltLoc':^6}{'Miss':^6}{'Subcavs':^9}")
		for cav in range(len(cavities)):
			if frame:
				name = str(pdbcode + "_" + dict_all_info[cav]["chains"] + "_"+str(frame))
			else:
				name = str(pdbcode + "_" + dict_all_info[cav]["chains"])
			print(f'{name:<12}{cav+1:^7d}{cavities[cav].ligandability:^6.1f}'
				f'{dict_all_info[cav]["score"]:^7.1f}{dict_all_info[cav]["size"]:^6d}'
				f'{str(int(np.around(dict_all_info[cav]["hydrophobicity"]*100)))+"%":^9}'
				f'{dict_all_info[cav]["interchain"]:^10d}{dict_all_info[cav]["altlocs"]:^6d}'
				f'{dict_all_info[cav]["missingatoms"]+dict_all_info[cav]["missingres"]:^6d}'
				f'{len(cavities[cav].subcavities):^9d}')
	else:
		print(f"{'PDB_chain':<12}{'CavID':^7}{'Ligab':^6}{'Score':^7}{'Size':^6}{'Hydrophob':^9}"
			f"{'InterCh':^10}{'AltLoc':^6}{'Miss':^6}")
		for cav in range(len(cavities)):
			if frame:
				name = str(pdbcode + "_" + dict_all_info[cav]["chains"] + "_"+str(frame))
			else:
				name = str(pdbcode + "_" + dict_all_info[cav]["chains"])
			print(f'{name:<12}{cav+1:^7d}{cavities[cav].ligandability:^6.1f}'
				f'{dict_all_info[cav]["score"]:^7.1f}{dict_all_info[cav]["size"]:^6d}'
				f'{str(int(np.around(dict_all_info[cav]["hydrophobicity"]*100)))+"%":^9}'
				f'{dict_all_info[cav]["interchain"]:^10d}{dict_all_info[cav]["altlocs"]:^6d}'
				f'{dict_all_info[cav]["missingatoms"]+dict_all_info[cav]["missingres"]:^6d}')

	return None

def _print_scores(dict_all_info, order, pdbcode):
	"""
	Returns the information with the order for export (final_cavities)
	"""
	idx = 0
	print(f"PDB  Cavity_ID, score, size, median_bur, 7thq_bur, hydrophob, interchain, altlocs, missingatoms_res")
	for cav in order:
		print(f'{pdbcode} {idx:<10d}{dict_all_info[cav]["score"]:>5.1f}{dict_all_info[cav]["size"]:>7d}{int(dict_all_info[cav]["median_buriedness"]):>8d}'
			f'{int(dict_all_info[cav]["7thq_buriedness"]):>10d}{dict_all_info[cav]["hydrophobicity"]:>10.2f}{dict_all_info[cav]["interchain"]:>10d}'
			f'{dict_all_info[cav]["altlocs"]:>10d}{dict_all_info[cav]["missingatoms"]+dict_all_info[cav]["missingres"]:>10d}')
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
		writePDB(os.path.join(outdir, pdbcode + "_cavs.pdb"), selection_protein)
		if listlig:
			ligs = ""
			if "_f" in pdbcode:
				a = open(os.path.join(oridir, pdbcode.split("_f")[0]+".pdb"), "r")
			else:
				a = open(os.path.join(oridir, pdbcode+".pdb"), "r")
			file = a.readlines()
			for lig in listlig:
				ligs+="".join([x for x in file if lig in x])
			a.close()
			a = open(os.path.join(outdir, pdbcode + "_cavs.pdb"), "a")
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
			pdbdummy.append(f"HETATM	1  S   GRI A {cavid:>3}	{coordinates[0]:8.3f}{coordinates[1]:8.3f}{coordinates[2]:8.3f}"
				f"  {final_pharma[cavid-1][idx_][0]:>3.2f} {grid_decomposition[cav_indices[idx]]:>5.2f}		   S\n")
			idx += 1
			idx_ += 1
	a = open(os.path.join(outdir, pdbcode + "_cavs.pdb"), "a")
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
			pdbdummy.append(f"HETATM	1  S   GRI A {cavid:>3}	{coordinates[0]:8.3f}{coordinates[1]:8.3f}{coordinates[2]:8.3f}"
				f"  1.00   1.00		   S\n")
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
		pdbdummy.append(f"HETATM	1  S   GRI A {cavid:>3}	{coordinates[0]:8.3f}{coordinates[1]:8.3f}{coordinates[2]:8.3f}"
			f"  1.00   1.00		   S\n")
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
		if "_f" in pdbcode:
			a = open(os.path.join(oridir, pdbcode.split("_f")[0]+".pdb"), "r")
		else:
			a = open(os.path.join(oridir, pdbcode+".pdb"), "r")
		file = a.readlines()
		for lig in listlig:
			ligs+="".join([x for x in file if lig in x])
		a.close()
		a = open(os.path.join(outdir, pdbcode + "_subcavs.pdb"), "a")
		a.write(ligs)
		a.close()


	for i in range(0, len(subcavs)):
		pdbdummy = []
		for coordinates in subcavs[i]:
			pdbdummy.append(f"HETATM	1  N   SUB {chr(cavid+96+1).upper()} {i+1:>3}	{coordinates[0]:8.3f}{coordinates[1]:8.3f}"
				f"{coordinates[2]:8.3f}  1.00   1.00		   N\n")
		a = open(os.path.join(outdir, pdbcode + "_subcavs.pdb"), "a")
		a.write("".join(pdbdummy))
		a.close()

	return None



class MMCIF2Dict(dict):
	"""Parse a mmCIF file and return a dictionary."""

	def __init__(self, filename):
		"""Parse a mmCIF file and return a dictionary.
		Arguments:
		 - file - name of the PDB file OR an open filehandle
		"""
		self.quote_chars = ["'", '"']
		self.whitespace_chars = [" ", "\t"]
		with open(filename, "r") as handle:
			loop_flag = False
			key = None
			tokens = self._tokenize(handle)
			try:
				token = next(tokens)
			except StopIteration:
				return  # for Python 3.7 and PEP 479
			self[token[0:5]] = token[5:]
			i = 0
			n = 0
			for token in tokens:
				if token.lower() == "loop_":
					loop_flag = True
					keys = []
					i = 0
					n = 0
					continue
				elif loop_flag:
					# The second condition checks we are in the first column
					# Some mmCIF files (e.g. 4q9r) have values in later columns
					# starting with an underscore and we don't want to read
					# these as keys
					if token.startswith("_") and (n == 0 or i % n == 0):
						if i > 0:
							loop_flag = False
						else:
							self[token] = []
							keys.append(token)
							n += 1
							continue
					else:
						self[keys[i % n]].append(token)
						i += 1
						continue
				if key is None:
					key = token
				else:
					self[key] = [token]
					key = None

	# Private methods

	def _splitline(self, line):
		# See https://www.iucr.org/resources/cif/spec/version1.1/cifsyntax for the syntax
		in_token = False
		# quote character of the currently open quote, or None if no quote open
		quote_open_char = None
		start_i = 0
		for (i, c) in enumerate(line):
			if c in self.whitespace_chars:
				if in_token and not quote_open_char:
					in_token = False
					yield line[start_i:i]
			elif c in self.quote_chars:
				if not quote_open_char and not in_token:
					quote_open_char = c
					in_token = True
					start_i = i + 1
				elif c == quote_open_char and (
					i + 1 == len(line) or line[i + 1] in self.whitespace_chars
				):
					quote_open_char = None
					in_token = False
					yield line[start_i:i]
			elif c == "#" and not in_token:
				# Skip comments. "#" is a valid non-comment char inside of a
				# quote and inside of an unquoted token (!?!?), so we need to
				# check that the current char is not in a token.
				return
			elif not in_token:
				in_token = True
				start_i = i
		if in_token:
			yield line[start_i:]
		if quote_open_char:
			raise ValueError("Line ended with quote open: " + line)

	def _tokenize(self, handle):
		empty = True
		for line in handle:
			empty = False
			if line.startswith("#"):
				continue
			elif line.startswith(";"):
				# The spec says that leading whitespace on each line must be
				# preserved while trailing whitespace may be stripped.  The
				# trailing newline must be stripped.
				token_buffer = [line[1:].rstrip()]
				for line in handle:
					line = line.rstrip()
					if line.startswith(";"):
						yield "\n".join(token_buffer)
						line = line[1:]
						if line and not line[0] in self.whitespace_chars:
							raise ValueError("Missing whitespace")
						break
					token_buffer.append(line)
				else:
					raise ValueError("Missing closing semicolon")
			yield from self._splitline(line.strip())
		if empty:
			raise ValueError("Empty file.")
# -*- coding: utf-8 -*-
"""
Main wrapper of CAVIAR
"""

import sys, os
from caviar.prody_parser import *
from caviar.cavity_identification import *
from caviar.cavity_characterization import *
from caviar.misc_tools import *
import time
import argparse

# get path of main.py
root = os.path.dirname(__file__)
home = os.getcwd()


def arguments():
	"""
	Advanced argument passing with argparse and configparse
	Takes as input a configuration file and potentially command line arguments
	"""
	
	def str2bool(v):
		"""
		The python argument parser does not really understand
		bool options (can set True, but can't set False)
		This function overrides the type=bool with type=str2bool
		"""
		if v.lower() in ('yes', 'true', 't', 'y', '1'):
			return True
		elif v.lower() in ('no', 'false', 'f', 'n', '0'):
			return False
		else:
			raise argparse.ArgumentTypeError('Boolean value expected.')


	# Create a temporary parser for storing parameters from a configuration file
	parent_parser = argparse.Namespace()

	# Create a dummy parser for the first two arguments, without 
	# creating a help, so that we can have all help with the real parser
	init_parser = argparse.ArgumentParser(add_help=False)
	#Im not sure if its the smartest way to do it, probably parent_parser could be avoided

	# Start by parsing which preset configuration file to use
	init_parser.add_argument('-preset_config', required=False, help='Chose one of the three standard configuration: default, cavities_only, subcavities_only\n',
		default = "default", choices=["default", "cavities_only", "subcavities_only"])
	# Also parse a potential custom configuration file -- in addition to the preset
	init_parser.add_argument('-custom_config', required=False, help='Custom configuration file that can contain any custom parameters, the rest being read from the preset_config\n')

	init_parser.parse_known_args(namespace=parent_parser)

	# Access the dictionary of the parameter values to modify it (currently empy)
	d = vars(parent_parser)
	# And update it with the configuration file parameters: magically it updates also parent_parser
	d.update(get_default_parameters(preset_choice = parent_parser.preset_config))
	# Update it with custom configuration
	if parent_parser.custom_config:
		d.update(get_custom_parameters(file = parent_parser.custom_config))

	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawTextHelpFormatter,
		description=str(""
		"\_________________________________________________________________________ /\n"
		" \                   Welcome to the Cavitome Project!                     /\n"
		"  \    You can use this program to identify and characterize cavities    /\n"
		"   \                    ... And soon much more ...                      /\n"
		"    \__________________________________________________________________/\n\n\n"


		"You may write all command line parameters in a custom configuration file \n"
		"with the -custom_config option. The default configuration file is located at \n"
		f"{os.path.realpath(os.path.join(root, 'config//default_caviar.yaml'))}\n"
		"alongside the two other default configurations (cavities_only, subcavities_only)\n"
		"You may reuse any of the keywords of these configuration files for creating a -custom_config\n"
		"You can also give simple arguments to the command line, such as the pdb code,\n"
		"to use with automatically set default parameters\n"),
		parents = [init_parser])


	# Add other parameters from command line 
	parser.add_argument("-cif", type = str2bool, help = ": Parse a mmCIF file rather than a PDB file \n(default = False)\n",
							default = False)
	parser.add_argument("-dcd", type = str, help = ": Parse a trajectory file in DCD format IN ADDITION to a PDB file"
							"(reference)\n This is the full path to the DCD file \n(default = None)\n",
							default = None)

	parser.add_argument("-sourcedir", type = str, help = ": Path of the directory where the pdb files are.\n")
	
	parser.add_argument("-code", type = str, help = ": PDB code of the file to  be computed.\n"
						"If the file isn't in given directory (-sourcedir), this program will try to download it from RCSB.\n")
	parser.add_argument("-codeslist", type = str, help = ": List of PDB files (in a file).\n"
						"If the file isn't in given directory (-sourcedir), this program will try to download it from RCSB.\n")
	
	parser.add_argument("-what", type = str, help = ": Keyword defining what protein chains "
						"to keep for cavity detection: all protein chains (above threshold_nres)\n"
						", just the longest chain, or the longest chain plus contacting chains (at 5A) \n"
						"  (default: 'allproteins'; other possibilities: 'longestchain', 'longestandcontacting')\n")
	
	parser.add_argument("-chain_id", type = str, help = ": User-specified chain ID to investigate (e.g., A).\n"
						"Is compatible with -what => overseeds the lookup for the longest chain.\n"
						"You can select this chain + contacting one (-what longestandcontacting)\n"
						"  (default: None)\n")
	
	parser.add_argument("-subcavs_decomp", type = str2bool, help = ": Activates the subcavities decomposition \n(default = True)\n")

	parser.add_argument("-color_cavs_by", type = str, help = ": write a session *.pml file for pymol to open the output and color cavities by chain/buriedness/pharmacophore\n"
						"(default = bychain\n", default = "bychain", choices=["bychain", "buriedness", "pharmacophore"])

	parser.add_argument("-out", type = str, help = ":  Path to outfolder.\n(default = ./caviar_out/)\n  ")

	parser.add_argument("-v", action = "store_true", help = ": turn verbosity on\n")


	# Parse cmd line arguments
	args = parser.parse_args(namespace = parent_parser)

	#Needs at least a code
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)

	if args.sourcedir != '':
		#if not args.sourcedir.endswith('/'):
		#	args.sourcedir += '/'
		if args.sourcedir[0] != '/' and args.sourcedir[0] != '~':
			args.sourcedir = os.path.join(os.getcwd(),args.sourcedir)
	if not args.code and not args.codeslist:
		print("Fatal Error: need a pdb code")
		#sys.exit(-1)
	if args.code:
		if not "pdb" in args.code:
			args.code = args.code + ".pdb"

	return args



def printv(msg):
	"""
	Prints messages in stdout if verbose is on
	"""
	if args.v:
		print(msg)


def parse_run(arguments):
	"""
	First function, parsing the data: PDB, PDB header... and killing before running cavity
	identification if needed.

	"""


	# ------------------------------------------------------------------------------------------- #
	# ----------------------------- GENERAL INPUT & KILL SWITCHES ------------------------------- #
	# ------------------------------------------------------------------------------------------- #


	global args
	args = arguments
	# ===== RUN ===== #
	printv("> verbose on")

	if args.cif:
		print("Attention! The CIF parser does not parse CIF(PDB) header metadata for the time being.")
		try:
			args.code = str(args.code).replace(".pdb", ".cif")
			pdbobject = parseMMCIF(os.path.join(args.sourcedir, args.code))
		except:
			args.sourcedir = "./"
			try:
				# Download
				print("mmCIF " + str(args.code) + " not found in -sourcedir, downloading from RCSB PDB")
				import urllib.request
				urllib.request.urlretrieve('http://files.rcsb.org/download/'+str(args.code), str(args.code))
				pdbobject = parseMMCIF(os.path.join(args.sourcedir, args.code))
			except:
				print("mmCIF " + str(args.code) + " not found on RCSB PDB webservers neither.")
				return None
	else:
		### Read PDB file
		try:
			pdbobject = parsePDB(os.path.join(args.sourcedir, args.code))
		except:
			# Download
			args.sourcedir = "./"
			print("PDB " + str(args.code) + " not found in -sourcedir, downloading from RCSB PDB")
			try:
				import urllib.request
				urllib.request.urlretrieve('http://files.rcsb.org/download/'+str(args.code), str(args.code))
				pdbobject = parsePDB(os.path.join(args.sourcedir, args.code))
			except:
				print("PDB " + str(args.code) + " not found on RCSB PDB webservers neither. Checking CIF files on RCSB PDB...")
				try:
					args.code = str(args.code).replace(".pdb", ".cif")
					urllib.request.urlretrieve('http://files.rcsb.org/download/'+str(args.code), str(args.code))
					pdbobject = parseMMCIF(os.path.join(args.sourcedir, args.code))
					args.cif = True
					print("PDB " + str(args.code) + " was found as mmCIF format!")
					print("Attention! The CIF parser does not parse PDB header metadata for the time being.")
				except:
					print("mmCIF " + str(args.code) + " not found on RCSB PDB webservers neither.")
					return None
	
	### Read information from the PDB header
	dict_pdb_info = get_information_header(os.path.join(args.sourcedir, args.code), cif = args.cif)

	# Here options to exclude non XR, resolution...
	killswitch = kill_from_header(dict_pdb_info, onlyxr = args.onlyxr,
		resolution_filter = args.resolution_filter,	resolution = args.resolution,
		pdbversion_filter = args.pdbversion_filter, pdbversion = args.pdbversion,
		caveat = args.caveat, obsolete = args.obsolete,	deposition_date_filter = args.deposition_date_filter,
		date = args.date)
	if killswitch:
		print(f"{args.code[0:-4]} was skipped because of a kill switch (e.g., not XR, resolution, caveat...)")
		return None
	print(dict_pdb_info)

	### Get selection objects from the PDB object
	### from arguments sourcedir, code. Can include or not metals, waters,
	### use the longest protein chain, with its contacting chains, or all chains
	### Threshold on the minimum protein chain size to exclude peptides
	# Generate the selection string

	## Added the option for user specifying a chain
	if args.chain_id:
		# If the user forgot to specify longestchain
		if "allproteins" in args.what:
			args.what = "longestchain"
		# user specified chains so it doesnt make sense to discard peptides
		args.threshold_nres = 1
		selection = select_objects(pdbobject = pdbobject, metal = args.metal, water = args.water,
			threshold_nres = args.threshold_nres, what = args.what, userspecified = args.chain_id,
			structural_ligand = args.structural_ligand)
		if selection:
			# Select what's wanted
			selection_protein = pdbobject.select(selection)
			# Get the coordinates of selected atoms
			selection_coords = selection_protein.getCoords()
		else:
			print(f"{args.code[0:-4]} chain(s) {args.chain_id} is/are a wrong input (do they exist?)")
			return None
	# Original code
	else:
		selection = select_objects(pdbobject = pdbobject, metal = args.metal, water = args.water,
			threshold_nres = args.threshold_nres, what = args.what, structural_ligand = args.structural_ligand)
		# Select what's wanted
		if selection:
			selection_protein = pdbobject.select(selection)
			# Get the coordinates of selected atoms
			selection_coords = selection_protein.getCoords()
		else:
			print(f"{args.code[0:-4]} was skipped because of composed only of peptides below threshold")
			return None


	# Exception case: dcd MD trajectory => one PDB code
	# can hold more than one atom group.
	# we'll run the cavity identification on all MD frames
	frame = None
	if args.dcd:
		print("We are going into DCD trajectory analysis. Several tables and PDBs will be printed, corresponding to each frame")
		print("Take care, that might write a lot of stuff and take a lot of memory")
		_dcd = DCDFile(args.dcd)
		_dcd.setCoords(pdbobject) # the data in dcd and in the pdb need to be consistent
		_dcd.link(pdbobject) # the data in dcd and in the pdb need to be consistent
		_dcd.setAtoms(selection_protein) # here we restrict to the subset of interest
		#ensemble.setAtoms(selection_protein) # the data in dcd and in the pdb need to be consistent
		#ensemble.setCoords(pdbobject) # the data in dcd and in the pdb need to be consistent
		#print(repr(ensemble))
		#ensemble.setAtoms(selection_protein) # here we restrict to the subset of interest
		print(repr(_dcd))
		#ensemble.addCoordset(selection_protein.getCoordsets())
		frame = 1
		allcavs_resids = []
		for conformation in _dcd.iterCoordsets():
			# CAV ROUTINES
			frm_txt = "f"+str(frame)
			# Object that will be parser to cluster pockets and determine cluster centers
			allcavs_resids.append(run(args, conformation, selection_protein, pdbobject, dict_pdb_info, frm_txt))
			frame += 1

		# Cluster pockets and print centroids / occupancy
		dict_clusters = wrapper_traj_anal(allcavs_resids, nframe = frame, agglo_function = args.agglo_function, dist_threshold = args.dist_threshold, min_occu = args.min_occu)
		if args.print_clusters:
			print(dict_clusters)
			
	# Exception case: NMR structures => one PDB code
	# can hold more than one atom group.
	# we'll run the cavity identification on all NMR models
	# frame will hold the MODEL number, or frame number in the DCD file
	elif dict_pdb_info["experiment"] and "NMR" in dict_pdb_info["experiment"]:
		print("That's an NMR structure. Several tables and PDBs will be printed, corresponding to each MODEL entry")
		ensemble = Ensemble("nmr struc")
		ensemble.setCoords(selection_protein)
		ensemble.addCoordset(selection_protein.getCoordsets())
		frame = 1
		for conformation in ensemble._confs:
			# CAV ROUTINES
			frm_txt = "f"+str(frame)
			run(args, conformation, selection_protein, pdbobject, dict_pdb_info, frm_txt)
			frame += 1
	# Main use case: XR structure, or mmCIF
	else:
		run(args, selection_coords, selection_protein, pdbobject, dict_pdb_info, frame)



	# ------------------------------------------------------------------------------------------- #
	# ----------------------------- CAVITY IDENTIFICATION ROUTINES ------------------------------ #
	# ------------------------------------------------------------------------------------------- #

def run(args, selection_coords, selection_protein, pdbobject, dict_pdb_info, frame):
	"""
	Main running function
	It contains annotations about the different routines
	
	1- Cavity identification routines are going on
	2- Followed by some cavity cleaning and filtering passes
	2bis- If needed, ligand-based cavity validation is performed
	3- Cavities are decomposed into subcavities
	
	"""

	# ===== RUN ===== #

	# Build a grid around the protein
	grid, grid_shape, grid_min = build_grid(selection_coords, boxmargin = args.boxmargin,
		gridspace = args.gridspace, size_limit = args.size_limit)
	try:
		grid.any()
	except:	
		print(f"{args.code[0:-4]} was killed because it is too big! The grid size is above the threshold: {args.size_limit}"
			f"\n Please change this parameter if you really want to investigate this structure. You'll need *a lot* of RAM!")
		return None
	grid_set = SetOfPoints(grid)
	size = len(grid)

	
	start = time.time()

	# Main wrapper for cavity identification. A bit of cavity filtering is done here too
	# but it's all geometry based. More will be done afterwards with pharmacophores
	early_cavities, cavities_info, grid_decomposition = wrapper_early_cav_identif(grid,
		grid_min, grid_shape, selection_protein, selection_coords,
		size_probe = args.size_probe, 
		maxdistance = args.max_distance, radius_cube = args.radius_cube, min_burial = args.min_burial,
		radius_cube_enc = args.radius_cube_enc, min_burial_enc = args.min_burial_enc,
		gridspace = args.gridspace, min_degree = args.min_degree, radius = 2,
		trim_score = args.trim_score, min_points = args.min_points, min_burial_q = args.min_burial_q,
		quantile = args.quantile)
	try:
		early_cavities[0]
	except:
		if frame:
			print(f"{args.code[0:-4]}_{frame} does not have a cavity")
		else:
			print(f"{args.code[0:-4]} does not have a cavity")
		return None
	
	end = time.time()
	printv(f"It took {round(end - start, 3)} seconds to identify and filter (non final) cavities")


	# ------------------------------------------------------------------------------------------- #
	# ------------------------------- CAVITY FILTERING ROUTINES --------------------------------- #
	# ------------------------------------------------------------------------------------------- #


	# Set pharmacophore properties to cavity grid points
	a = time.time()
	pharmacophore_types = set_pharmacophore_type(early_cavities, selection_protein, selection_coords)
	b = time.time()
	printv(f"It took {round(b-a, 3)} seconds to set the pharmacophore types of cavity points")

	# Combine information, exclude the cavities that were filtered before + cavities that are too
	# hydrophobic (max_hydrophobicity), find residues lining the cavities, and lots of information
	# And ranks cavities
	a = time.time()
	final_cavities, final_pharma, dict_all_info = cavity_cleansing(cavities_info, early_cavities,
		pharmacophore_types, args.max_hydrophobicity,
		selection_coords, selection_protein, dict_pdb_info,
		args.exclude_missing, args.exclude_interchain, args.exclude_altlocs)

	try:
		if not final_cavities.any():
			print(f"{args.code[0:-4]} does not have a cavity")
			return None
	except:
		None

	b = time.time()
	printv(f"It took {round(b-a, 3)} seconds to clean all the cavity information")
	

	# ------------------------------------------------------------------------------------------- #
	# ------------------------------- LIGAND VALIDATION ROUTINES -------------------------------- #
	# ------------------------------------------------------------------------------------------- #


	############### Check for ligand presence ########################

	if args.check_if_lig:
		if not args.excl_ligs:
			args.lig_tabu_list = False
		if args.lig_id:
			list_ligands, list_lig_coords = get_ligand(pdbobject, tabu_list = args.lig_tabu_list,
				lig_id = args.lig_id)
		else:
			list_ligands, list_lig_coords = get_ligand(pdbobject, tabu_list = args.lig_tabu_list)
		if args.iflig_print:
			dict_coverage = find_ligand_presence(final_cavities, list_ligands, list_lig_coords,
				pdbcode = args.code[0:-4], printflag = True,
				ligsizeflag = args.ligsizeflag, ligminsize = args.ligminsize, tocenter = args.lig_tocenter)
		else:
			dict_coverage = find_ligand_presence(final_cavities, list_ligands, list_lig_coords,
				pdbcode = args.code[0:-4], printflag = False,
				ligsizeflag = args.ligsizeflag, ligminsize = args.ligminsize, tocenter = args.lig_tocenter)
	else:
		dict_coverage = {} # empty
		list_ligands = []
		list_lig_coords = []
	if args.export_cavities:
		try:
			os.mkdir(args.out)
		except:
			pass
		if frame:
			export_pdb_cavity(final_cavities, final_pharma, args.code[0:-4]+"_"+str(frame), grid_min, grid_shape,
			grid_decomposition, selection_protein = selection_protein,
			gridspace = args.gridspace, outdir = args.out, withprot = args.withprot, listlig = list_ligands,
			oridir = args.sourcedir)
		else:
			export_pdb_cavity(final_cavities, final_pharma, args.code[0:-4], grid_min, grid_shape,
			grid_decomposition, selection_protein = selection_protein,
			gridspace = args.gridspace, outdir = args.out, withprot = args.withprot, listlig = list_ligands,
			oridir = args.sourcedir)

		# Works only if XR/mmCIF, not with NMR/DCD
		if args.write_pml_cavs:
			write_pmlfile(cavity_file = os.path.join(args.out, args.code[0:-4] + "_cavs.pdb"), what = args.color_cavs_by, outputfile = str(args.code[0:-4]+"_cavities.pml"))



	# Creates cavity object to try to put all of the information
	cavities = fill_cavities_object(dict_all_info, final_cavities, final_pharma,
		grid_decomposition, grid_min, grid_shape, gridspace = args.gridspace) # list_asph

	# store ligandability information
	for cava in range(len(cavities)):
		ligandability = float(calculate_ligandability(cavities, cava))
		cavities[cava].ligandability = ligandability

	# Updates the cavities also with presence/absence of ligand
		
	list_covered_ligands, dict_cavid_lig_bool = export_clean_cav_ligand_info(dict_coverage,
		list_ligands, list_lig_coords, cavities)


	# ------------------------------------------------------------------------------------------- #
	# -------------------------------- SUBCAVITIES ROUTINES ------------------------------------- #
	# ------------------------------------------------------------------------------------------- #

	if args.subcavs_decomp:
		# Open a file and write the protein if requested 
		if args.export_subcavs:
			try:
				os.mkdir(args.out)
			except:
				pass
			if frame:
				writePDB(os.path.join(args.out, args.code[:-4]+"_"+str(frame) + "_subcavs.pdb"), selection_protein)
			else:
				writePDB(os.path.join(args.out, args.code[:-4] + "_subcavs.pdb"), selection_protein)
			if args.write_pml_subcavs:
				write_pmlsubcavs(os.path.join(args.out, args.code[:-4] + "_subcavs.pdb"), outputfile = str(args.code[0:-4]+"_subcavities.pml"))
				
		subcavs_table = ""
		if len(final_cavities) == 1: # Don't go over everything if there's only one cavity!				
			subcavs_table += wrapper_subcavities(final_cavities, 0, grid_min, grid_shape,
			cavities, args.code, args.out, args.sourcedir, list_ligands,
			seeds_mindist = args.seeds_mindist, merge_subcavs = args.merge_subcavs, minsize_subcavs = 50,
			min_contacts = 0.667, v = False, export_subcavs = args.export_subcavs,
			gridspace = args.gridspace, frame = frame)
		# Iterate over liganded cavities only 
		elif args.subcavs_lig_only:
			try: #Could be activated without ligand
				for key,value in dict_coverage.items():
					cav_of_interest = int(value[0])
					subcavs_table += wrapper_subcavities(final_cavities, cav_of_interest, grid_min, grid_shape,
					cavities, args.code, args.out, args.sourcedir, list_ligands,
					seeds_mindist = args.seeds_mindist, merge_subcavs = args.merge_subcavs, minsize_subcavs = 50,
					min_contacts = 0.667, v = False, export_subcavs = args.export_subcavs,
					gridspace = args.gridspace, frame = frame)

			except:
				print(f"{args.code[0:-4]} does not have a liganded cavity for subcavity decomposition"
					". Please review the -subcavs_lig_only option")
		# Iterate all cavities
		else:
			for cav_of_interest in range(len(cavities)):
				subcavs_table += wrapper_subcavities(final_cavities, cav_of_interest, grid_min, grid_shape,
				cavities, args.code, args.out, args.sourcedir, list_ligands,
				seeds_mindist = args.seeds_mindist, merge_subcavs = args.merge_subcavs, minsize_subcavs = 50,
				min_contacts = 0.667, v = False, export_subcavs = args.export_subcavs,
				gridspace = args.gridspace, frame = frame)


	# Print formatted information
	if args.print_cav_info:
		# print with subcavities information if subcavs_decomp was activated
		print_scores(dict_all_info, args.code[0:-4], cavities, subcavs = args.subcavs_decomp, frame = frame)

	# Print formatted information for subcavities 
	if args.subcavs_decomp and args.print_pphores_subcavs:
		print(f"{'PDB_chain':<12}{'CavID':^7}{'SubCavID':^8}{'Size':^6}{'Hydrophob.':^10}"
			f"{'Polar':^7}{'Neg':^6}{'Pos':^6}{'Other':^6}")
		print(subcavs_table)


	# ------------------------------------------------------------------------------------------- #
	# ----------------------------------- THIS IS THE END! -------------------------------------- #
	# ------------------------------------------------------------------------------------------- #

	# If trajectory, return a string containing sets of cavity residues
	if args.dcd:
		cavs_inthisframe = []
		for cava in range(len(cavities)):
			cavs_inthisframe.append(cavities[cava].residues)

		return cavs_inthisframe

	return None


def main():
	args = arguments()
	if args.codeslist:
		with open(args.codeslist) as pdblist:
			for tmppdb in pdblist:
				if len(tmppdb) < 4:
					# empty line or weird, skip
					continue
				elif tmppdb[0] == "#":
					# Commented line, skip
					continue
				else:
					if not ".pdb" in tmppdb:
						args.code = f"{tmppdb.split()[0].split(sep = '_')[0]}.pdb"
					else:
						args.code = tmppdb.split()[0]
					if args.liglist_in_pdblist:
						try:
							args.lig_id = tmppdb.split()[1][0:3]
						except:
							print("You specified liglist_in_pdblist but there is no second column with lig ID")
					if args.chainid_in_pdblist:
						try:
							args.chain_id = tmppdb.split()[0].split(sep = "_")[1]
						except:
							print("Something wrong with chainid_in_pdblist")
				if not os.path.isfile(str(args.sourcedir)+str(args.code)):
					print(f"{args.code} is not a valid filename or a valid PDB identifier.")
					continue
				parse_run(args)
	else:
		parse_run(args)
	sys.exit()



if __name__ == "__main__":

	main()

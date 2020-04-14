# -*- coding: utf-8 -*-
"""
Main wrapper of the cavitome program
Contains: str2bool(), arguments(), printv(), and run()
"""

import sys, os
from caviar.prody_parser import *
from caviar.cavity_identification import *
from caviar.cavity_characterization import *
from caviar.misc_tools import *
from caviar.cavity_comparisons import *
from caviar.database_functions import *
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
	parser.add_argument("-sourcedir", type = str, help = ": Path of the directory where the pdb files are.\n")
	
	parser.add_argument("-code", type = str, help = ": PDB code of the file to  be computed.\n"
						"If the file isn't in given directory (-sourcedir), this program will try to download it from RCSB.\n")
	
	parser.add_argument("-what", type = str, help = ": Keyword defining what protein chains "
						"to keep for cavity detection: all protein chains (above threshold_nres)"
						", just the longest chain, or the longest chain plus contacting chains (at 5A) \n"
						"  (default: 'allproteins'; other possibilities: 'longestchain', 'longestandcontacting')")
	
	parser.add_argument("-chain_id", type = str, help = ": User-specified chain ID to investigate (e.g., A).\n"
						"Is compatible with -what => overseeds the lookup for the longest chain."
						"You can select this chain + contacting one (-what longestandcontacting)\n"
						"  (default: None)")
	
	parser.add_argument("-subcavs_decomp", type = str2bool, help = ": Activates the subcavities decomposition \n(default = False)\n")
	
	parser.add_argument("-out", type = str, help = ":  Path to outfolder.\n  ")

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
	if args.code and not "pdb" in args.code:
		args.code = args.code + ".pdb"

	return args



def printv(msg):
	"""
	Prints messages in stdout if verbose is on
	"""
	if args.v:
		print(msg)


def run(arguments):
	"""
	Main running function
	It contains annotations about the different routines
	
	1- The program starts by reading the input and killing the process if some kill switches are
	activated (eg, only XR structures)
	2- Then the cavity identification routines are going on
	3- Followed by some cavity cleaning and filtering passes
	3bis- If needed, ligand-based cavity validation is performed
	4- Cavities are decomposed into subcavities
	
	"""


	# ------------------------------------------------------------------------------------------- #
	# ----------------------------- GENERAL INPUT & KILL SWITCHES ------------------------------- #
	# ------------------------------------------------------------------------------------------- #


	global args
	args = arguments
	# ===== RUN ===== #
	printv("> verbose on")

	### Read PDB file
	try:
		pdbobject = parsePDB(os.path.join(args.sourcedir, args.code))
	except:
		# Download
		print("PDB " + str(args.code) + " not found in -sourcedir, downloading from RCSB PDB")
		import urllib.request
		urllib.request.urlretrieve('http://files.rcsb.org/download/'+str(args.code), str(args.code))
		try:
			pdbobject = parsePDB(str(args.code))
		except:
			print("PDB " + str(args.code) + " not found on RCSB PDB webservers neither")
			return None
	### Read information from the PDB header
	dict_pdb_info = get_information_header(os.path.join(args.sourcedir, args.code))
	# Here options to exclude non XR, resolution...
	killswitch = kill_from_header(dict_pdb_info, onlyxr = args.onlyxr,
		resolution_filter = args.resolution_filter,	resolution = args.resolution,
		pdbversion_filter = args.pdbversion_filter, pdbversion = args.pdbversion,
		caveat = args.caveat, obsolete = args.obsolete,	deposition_date_filter = args.deposition_date_filter,
		date = args.date)
	if killswitch:
		print(f"{args.code[0:-4]} was skipped because of a kill switch (e.g., not XR, resolution, caveat...)")
		return None

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


	# ------------------------------------------------------------------------------------------- #
	# ----------------------------- CAVITY IDENTIFICATION ROUTINES ------------------------------ #
	# ------------------------------------------------------------------------------------------- #


	# Build a grid around the protein
	grid, grid_shape, grid_min = build_grid(selection_coords, boxmargin = args.boxmargin,
		gridspace = args.gridspace)
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

	if args.export_cavities:
		try:
			os.mkdir(args.out)
		except:
			pass
		export_pdb_cavity(final_cavities, final_pharma, args.code[0:-4], grid_min, grid_shape,
			grid_decomposition, selection_protein = selection_protein,
		gridspace = args.gridspace, outdir = args.out, withprot = args.withprot, listlig = list_ligands,
		oridir = args.sourcedir)


	#dict_coverage['0'][0]	# Kills here the process if detection mode
	if args.detect_only:
		return None


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

	# Print formatted information
	if args.print_cav_info:
		print_scores(dict_all_info, args.code[0:-4], cavities)

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
			writePDB(os.path.join(args.out, args.code[:-4] + "_subcavs.pdb"), selection_protein)
		if len(final_cavities) == 1: # Don't go over everything if there's only one cavity!				
			wrapper_subcavities(final_cavities, 0, grid_min, grid_shape,
			cavities, args.code, args.out, args.sourcedir, list_ligands,
			seeds_mindist = args.seeds_mindist, merge_subcavs = args.merge_subcavs, minsize_subcavs = 50,
			min_contacts = 0.667, v = False, printv = args.print_pphores_subcavs,
			print_pphores_subcavs = args.print_pphores_subcavs, export_subcavs = args.export_subcavs,
			gridspace = args.gridspace)
		# Iterate over liganded cavities only 
		elif args.subcavs_lig_only:
			try: #Could be activated without ligand
				for key,value in dict_coverage.items():
					cav_of_interest = int(value[0])
					wrapper_subcavities(final_cavities, cav_of_interest, grid_min, grid_shape,
					cavities, args.code, args.out, args.sourcedir, list_ligands,
					seeds_mindist = args.seeds_mindist, merge_subcavs = args.merge_subcavs, minsize_subcavs = 50,
					min_contacts = 0.667, v = False, printv = args.print_pphores_subcavs,
					print_pphores_subcavs = args.print_pphores_subcavs, export_subcavs = args.export_subcavs,
					gridspace = args.gridspace)

			except:
				print(f"{args.code[0:-4]} does not have a liganded cavity for subcavity decomposition"
					". Please review the -subcavs_lig_only option")
		# Iterate all cavities
		else:
			for cav_of_interest in range(len(cavities)):
				wrapper_subcavities(final_cavities, cav_of_interest, grid_min, grid_shape,
				cavities, args.code, args.out, args.sourcedir, list_ligands,
				seeds_mindist = args.seeds_mindist, merge_subcavs = args.merge_subcavs, minsize_subcavs = 50,
				min_contacts = 0.667, v = False, printv = args.print_pphores_subcavs,
				print_pphores_subcavs = args.print_pphores_subcavs, export_subcavs = args.export_subcavs,
				gridspace = args.gridspace)



	# ------------------------------------------------------------------------------------------- #
	# -------------------------------- FINGERPRINT ROUTINES ------------------------------------- #
	# ------------------------------------------------------------------------------------------- #


	if args.gen_fp:
	#### PLEASE PUT OPTIONS AND ARGUMENTS 
		a = time.time()
		for index in range(len(cavities)):
			dist_fillings, buri_fillings, pp_fillings, iterations = prep_data_for_fp(cavities, index,
				min_burial = args.min_burial, n_pp = 11)
			fp = fp_construction(dist_fillings, buri_fillings, pp_fillings)
			# update cavities with fp1
			cavities[index].fp1 = fp
			#print(fp)
		b = time.time()
		printv(f"It took {round(b-a, 3)} seconds to generate the fingerprint")


	# ------------------------------------------------------------------------------------------- #
	# ----------------------------- DATABASE INSERTION ROUTINES --------------------------------- #
	# ------------------------------------------------------------------------------------------- #


	if args.db_write == True:
	#### PLEASE PUT OPTIONS AND ARGUMENTS 
		conn, cursor = connect_database(database = args.db_name, user = "marchje7", host="127.0.0.1")
		# Write metadata about the PDB file (from header!)
		write_pdb(conn, cursor, dict_pdb_info, pdbcode = args.code[0:-4], v = False)
		# Write metadata about the protein chains
		write_pdbchains(conn, cursor, dict_pdb_info, pdbcode = args.code[0:-4], v = False)
		# Write cavities
		write_cavities(conn, cursor, dict_all_info, cavities_object = cavities, pdbcode = args.code[0:-4], v = False)



	# ------------------------------------------------------------------------------------------- #
	# ----------------------------------- THIS IS THE END! -------------------------------------- #
	# ------------------------------------------------------------------------------------------- #


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
						args.code = tmppdb.split()[0].split(sep = "_")[0]
					if args.liglist_in_pdblist:
						try:
							args.lig_id = tmppdb.split()[1][0:3]
						except:
							print("You specified liglist_in_pdblist but there is no second column with lig ID")
					if args.chainid_in_pdblist:
						try:
							args.chain_id = tmppdb.split()[0].split(sep = "_")[1]
						except:
							printv("Something wrong with chainid_in_pdblist")
				if not os.path.isfile(str(args.sourcedir)+str(args.code)):
					print(f"{args.code} is not a valid filename or a valid PDB identifier.")
					continue
				run(args)
	else:
		run(args)
	sys.exit()



if __name__ == "__main__":

	main()

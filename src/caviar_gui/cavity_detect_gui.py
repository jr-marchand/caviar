# -*- coding: utf-8 -*-
"""
Main wrapper of the caviar program
Contains: str2bool(), arguments(), printv(), and run()
"""

import sys, os
from caviar_gui.prody_parser import parsePDB
from caviar_gui.cavity_identification import *
from caviar_gui.cavity_characterization import *
from caviar_gui.misc_tools.misc import export_pdb_cavity, export_pdb_subcavities, get_information_header,\
join_information_cavities, get_final_sorted_cavs, print_scores
from argparse import ArgumentParser, ArgumentTypeError, RawTextHelpFormatter
import textwrap


# get path of main.py
if os.path.dirname(__file__):
	home = os.path.dirname(__file__) + "/"
else:
	home = "./"


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
		raise ArgumentTypeError('Boolean value expected.')


def arguments():
	"""
	Advanced argument passing via (pyparse) argparse module
	"""
	

	parser = ArgumentParser(
		formatter_class=RawTextHelpFormatter,
		description=textwrap.dedent('''
   \_________________________________________________________________________ /
    \                   Welcome to the Cavitome Project!                     /
     \    You can use this program to identify and characterize cavities    /
      \                    ... And soon much more ...                      /
       \__________________________________________________________________/
    
    1) Reads the PDB file and its header, filter out unwanted properties
    2) Builds a grid, identify cavities, set their properties (buriedness, pharmacophores)
    3) Cures cancer
         '''))


# --------------------------------- INPUT --------------------------------- #


	parser.add_argument("-sourcedir", type = str, help = ": Path of the directory "
						"where are the pdb files.\n"
						"  (default: /db/pdb/)", default = "/db/pdb/")
	parser.add_argument("-code", type = str, help = ": PDB code of the file to "
						"be computed.\n  If the file isn't in given directory "
						"(-sourcedir),\n  this program will try to download it"
						" from RCSB.\n  (no default)\n")
	parser.add_argument("-codeslist", type = str, help = ": List of PDB codes to "
						"be computed.\n  If the files aren't in given directory "
						"(-sourcedir),\n  this program will try to download it"
						" from RCSB.\n  (no default)\n")


# ----------------------------- GENERAL & KILL SWITCHES ------------------------------- #


	parser.add_argument("-v", type = str2bool, help = ": turn verbosity on.\n"
						"  (default: False)", default = False)
	parser.add_argument("-onlyxr", type = str2bool, help = ": Only work with XR structures (True/False) \n"
						"  (default: False)", default = False)
	parser.add_argument("-resolution_filter", type = str2bool, help = ": Define a resolution filter (True/False)\n"
						"  (default: False)", default = False)
	parser.add_argument("-resolution", type = float, help = ": Value for the resolution filter \n"
						"  (default: 3.0)", default = 3.0)
	parser.add_argument("-pdbversion_filter", type = bool, help = ": Define a filter on the PDB version\n"
						"  (default: False)", default = False)
	parser.add_argument("-pdbversion", type = float, help = ": Minimal PDB version\n"
						"  (default: 3.30)", default = 3.30)
	parser.add_argument("-caveat", type = str2bool, help = ": Exclude PDB tagged with CAVEATS\n"
						"  (default: False)", default = False)
	parser.add_argument("-obsolete", type = str2bool, help = ": Exclude PDB tagged with OBSOLETE\n"
						"  (default: False)", default = False)
	parser.add_argument("-deposition_date_filter", type = bool, help = ": Exclude PDB deposited/reviewed before a date\n"
						"  (default: False)", default = False)
	parser.add_argument("-date", type = int, help = ": Minimal deposition/revision date\n"
						"  (default: 2010)", default = 2010)


# --------------------------------- OUTPUT --------------------------------- #


	parser.add_argument("-out", type = str, help = ":  Path/to/outfolder.\n  "
						"(default: ./caviar_out/", default="./caviar_out/")
	parser.add_argument("-export_cavities", type = str2bool, help = ": Export PDB files with cavities (True/False) \n"
						"  (default: True)", default = True)
	parser.add_argument("-withprot", type = str2bool, help = ": Export it with the protein (True/False) \n"
						"  (default: True)", default = True)
	parser.add_argument("-print_cav_info", type = str2bool, help = ": print a report on cavity identification) \n"
						" (default = True)\n", default = True)


# ---------------------------- OBJECT SELECTION ----------------------------- #


	parser.add_argument("-metal", type = str2bool, help = ": Keep metals\n"
						"  (default: True)", default = True)
	parser.add_argument("-water", type = str2bool, help = ": Keep waters molecules "
						"that make at least 3 HB with protein atoms\n"
						"  (default: True)", default = True)
	parser.add_argument("-structural_ligand", type = str, help = ": Keep structural ligand \n"
						"(give 3 letters resname code)\n"
						"  (default: False)", default = False)
	parser.add_argument("-threshold_nres", type = int, help = ": Minimum number of residues "
						"in a protein chain to keep it \n"
						"  (default: 30)", default = 30)
	parser.add_argument("-what", type = str, help = ": Keyword defining what protein chains "
						"to keep for cavity detection: all protein chains (above threshold_nres)"
						", just the longest chain, or the longest chain plus contacting chains (at 5A) \n"
						"  (default: 'allproteins'; other possibilities: 'longestchain', 'longestandcontacting')",
						default = "allproteins")
	parser.add_argument("-min_contacts", type = int, help = ": In case you choose longestandcontacting with"
						" option -what, this keyword controls how many contacts between the main chain \n"
						" and the 'contacting' chain should be at minimum present. These are interatomic "
						" contacts at 5A, so be loose with the number. The aim is to keep only chains \n"
						" of the PDB that are functionally in contact and not simply symmetric chains \n"
						" of the same domain in the crystal unit.\n"
						"  (default: 75)", default = 75)
	parser.add_argument("-user_chain", type = str2bool, help = ": Activates the option to user specify a chain ID "
						" to investigate. The chain ID needs to be given with -chainID option\n"
						"  (default: False)", default = False)
	parser.add_argument("-chain_id", type = str, help = ": User-specified chain ID to investigate "
						"(e.g., A).\n Is compatible with -what => overseeds the lookup for the longest chain."
						"You can select this chain + contacting one (-what longestandcontacting)\n"
						"  (default: A)", default = "A")
	parser.add_argument("-chainid_in_pdblist", type = str2bool, help = ": Same chain_id but implemented in input list "
						"\n rather than passed as explicit argument. Same warning as -chain_id.\n"
						"The chain identifier (e.g. A, B...) should be given after an underscore to the\n"
						"PDB code. For example 1AAA_A for chain A of PDB 1AAA.\n"
						"In case you want to specify more than one chain, just put all of them, e.g., 1AAA_ABC for chains A, B, and C.\n"
						"  (default: False)", default = False)


# ---------------------- CAVITY IDENTIFICATION ----------------------- #


	parser.add_argument("-boxmargin", type = float, help=": Margin around the protein \n"
						"  (default: 2.0)", default = 2.0)
	parser.add_argument("-maxdistance", type = float, help=": Maximum distance for a solvent grid point to the protein \n"
						"  (default: 6.0)", default = 6.0)
	parser.add_argument("-gridspace", type=float, help=": Grid spacing \n"
						"  (default: 1.0)", default = 1.0)
	parser.add_argument("-filevdwsizes", type=str, help=": file (with path) containing van der Waals radius of"
						" protein atoms. \n (default: cavity_identification/vdw_size_atoms.dat",
						default = home+"cavity_identification/vdw_size_atoms.dat")
	parser.add_argument("-sizeprobe", type = float, help=": Size of the probe for defining protein points."
						" This size is added to the vdW radius from vdw_size_atoms.dat."
						"\n (default: 1.0)", default = 1.0)
	parser.add_argument("-radius_cube", type=int, help=": Size of the cubic solvation shell"
						" to investigate burial of cavity points (in number of grid points).\n"
						" (default: 4)", default = 4)
	parser.add_argument("-min_burial", type = int, help=": Minimum number of grid-protein contacts"
						" for a grid point (within -radius_cube) to consider it as potential"
						" cavity point. This number is between 0 and 14 because we scan in the "
						" 14 cubic directions\n (default: 8)", default = 8)
	parser.add_argument("-radius_cube_enc", type = int, help=": Same as radius_cube, but for the second pass"
						"to identify buried cavity points. This second pass aims to find 'middle' cavity points"
						"that are not in direct contact with the protein [within radius_cube] but surrounded "
						"by grid cavity points (middle of a large pocket). \n (default: 3)", default = 3)
	parser.add_argument("-min_burial_enc", type = int, help=": Equivalent to min_burial but for the"
						" second pass (cf help of radius_cube_enc). \n (default: 8)", default = 8)


# ---------------------- CAVITY FILTERING ----------------------- #


	parser.add_argument("-min_points", type = int, help=": Minimum number of points to consider a group of cavity points"
						" as an actual cavity. Is modified by gridspace argument (real value = min_points * 1 / gridspace).\n"
						"If gridspace = 0.5, the real value used for min_points is doubled."
						"\n(default: 50)", default = 50)
	parser.add_argument("-trim_score", type = int, help=": Scoring value for excluding potential cavity points.\n"
						" Points within 2 grid spacing (in cubic directions, 125 points max) are detected. The score equals the\n"
						" number of points times 10**(average_buriedness/10). Buriedness ranges from 9 to 14, len(points) from \n"
						" 0 to 125. The maximum value of this score is 3139 (125*(10**(14/10)). The default is 600. \n"
						" This corresponds roughly to an environement of 60 neighbors (out of 125 maximum, half) and an avg buriedness of 10."
						"\n(default: 500)", default = 500)
	parser.add_argument("-min_degree", type = int, help=": Minimum node degree to keep it, ie, minimum number of "
						" connections with other nodes. \n (default: 3)", default = 3)
	parser.add_argument("-min_burial_q", type = int, help=": Minimum buriedness value of grid points at the xth quantile "
						" (strictly greater than) [parameter -quantile]. \n (default: 10)", default = 10)
	parser.add_argument("-quantile", type = float, help=": Quantile related to min_burial_q \n (default: 0.8)", default = 0.8)
	parser.add_argument("-max_hydrophobicity", type = float, help=": Maximum percentage of hydrophobic points in the cavity."
						" \n (default: 1.0)", default = 1.0)
	parser.add_argument("-exclude_interchain", type = str2bool, help=": Exclude cavities that are in between different protein chains."
						" \n (default: False)", default = False)
	parser.add_argument("-exclude_missing", type = str2bool, help=": Exclude cavities that have missing atoms/residues."
						" \n (default: False)", default = False)
	parser.add_argument("-exclude_altlocs", type = str2bool, help=": Exclude cavities that have alternative conformation of residues."
						" \n (default: False)", default = False)


# ----------------------- LIGAND VALIDATION OPTIONS ------------------------ #


	parser.add_argument("-excl_ligs", type = str2bool, help=": Activate an explicit the tabu list for the ligand."
						" \n (default: True)", default = True)
	parser.add_argument("-lig_tabu_list", type = str, help=": Explicit the tabu list for the ligand."
						" \n (default: misc_tools/tabu_lists/tabulist_ligand_maximal)",
						default = home+"misc_tools/tabu_lists/tabulist_ligand_maximal")
	parser.add_argument("-iflig_print", type = str2bool, help=": Print what was found if -check_if_lig was activated."
						" \n (default: False)", default = False)
	parser.add_argument("-ligsizeflag", type = str2bool, help=": Flag to define a minimal size for the ligand."
						" \n (default: False)", default = False)
	parser.add_argument("-ligminsize", type = int, help=": Minimal size for the ligand if ligsizeflag is activated."
						" \n (default: 8)", default = 8)
	parser.add_argument("-lig_id", type = str, help = ": Ligand 3 letters ID code"
						" in the PDB file, to check for presence in cavities \n (no default)\n")
	parser.add_argument("-liglist_in_pdblist", type = str2bool, help = ": Specify ligand 3 letters ID code"
						"in the second in the second column of the PDB list file (to check for presence in cavities)\n"
						" (default = False)\n", default = False)
	parser.add_argument("-lig_tocenter", type = str2bool, help = ": Ask to check if a ligand atom is within 4.0 A"
						"of the geometric center of the pocket rather than within 1A of any cavity point \n"
						" (default = False)\n", default = False)


# -------------------------------- SUBCAVITY DECOMPOSITION ------------------------------- #


	parser.add_argument("-subcavs_decomp", type = str2bool, help = ": Activates the subcavities decomposition \n"
						" (default = False)\n", default = False)
	parser.add_argument("-subcavs_lig_only", type = str2bool, help = ": Find subcavities only for liganded cavities \n"
						" (default = False)\n", default = False)
	parser.add_argument("-export_subcavs", type = str2bool, help = ": Export subcavities in pdb file \n"
						" (default = False)\n", default = False)
	parser.add_argument("-seeds_mindist", type = int, help = ": Minimum distance between seed points in the"
						" watershed algorithm \n"
						" (default = 3)\n", default = 3)

	
	return parser


def printv(msg):
	"""
	Prints messages in stdout if verbose is on
	"""
	if args.v:
		print(msg)

from io import StringIO
from contextlib import redirect_stdout
def run(arguments):
	"""
	Main running function
	It contains annotations about the different routines
	
	1- The program starts by reading the input and killing the process if some kill switches are
	activated (eg, only XR structures)
	2- Then the cavity identification routines are going on
	3- Followed by some cavity cleaning and filtering passes
	3bis- If needed, ligand-based cavity validation is performed
	
	"""

	# ------------------------------------------------------------------------------------------- #
	# ----------------------------- GENERAL INPUT & KILL SWITCHES ------------------------------- #
	# ------------------------------------------------------------------------------------------- #


	with StringIO() as buf, redirect_stdout(buf):

		global args
		args = arguments
		# ===== RUN ===== #
		printv("> verbose on")
		if not args.out.endswith('/'):
			args.out += '/'
		try:
			os.mkdir(args.out)
		except:
			pass

		### Read PDB file
		try:
			pdbobject = parsePDB(str(args.sourcedir)+str(args.code))
		except:
			# Download
			print("PDB " + str(args.code) + " not found in directory, downloading from RCSB PDB")
			import urllib.request
			urllib.request.urlretrieve('http://files.rcsb.org/download/'+str(args.code), str(args.code))
			try:
				pdbobject = parsePDB(str(args.code))
			except:
				print("PDB " + str(args.code) + " not found on RCSB PDB webservers neither")
				return buf.getvalue()
		### Read information from the PDB header
		dict_pdb_info = get_information_header(str(args.sourcedir)+str(args.code))
		# Here options to exclude non XR, resolution...
		#killswitch = kill_from_header(dict_pdb_info, onlyxr = args.onlyxr, resolution_filter = args.resolution_filter, resolution = args.resolution,
		#pdbversion_filter = args.pdbversion_filter, pdbversion = args.pdbversion, caveat = args.caveat, obsolete = args.obsolete,
		#deposition_date_filter = args.deposition_date_filter, date = args.date)
		#if killswitch:
		#	print(f"{args.code[0:-4]} was skipped because of a kill switch (e.g., not XR, resolution, caveat...)")
		#	return buf.getvalue()
	
		### Get selection objects from the PDB object
		### from arguments sourcedir, code. Can include or not metals, waters,
		### use the longest protein chain, with its contacting chains, or all chains
		### Threshold on the minimum protein chain size to exclude peptides
		# Generate the selection string
	
		## Added the option for user specifying a chain
		if args.user_chain and args.chain_id:
			# If the user forgot to specify longestchain
			if "allproteins" in args.what:
				args.what = "longestchain"
			
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
				return buf.getvalue()
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
				return buf.getvalue()
	
	
		# ------------------------------------------------------------------------------------------- #
		# ----------------------------- CAVITY IDENTIFICATION ROUTINES ------------------------------ #
		# ------------------------------------------------------------------------------------------- #
	
	
		# Build a grid around the protein
		grid, grid_shape, grid_min = build_grid(selection_coords, boxmargin = args.boxmargin, gridspace = args.gridspace)
		grid_set = SetOfPoints(grid)
		size = len(grid)
	
		# Identify points of the grid that are within the surface of the protein

		grid_protein, grid_solv, grid_decomposition_0 = find_protein_points_variablevolume(grid, selection_protein,
			file_sizes = args.filevdwsizes, size_probe = args.sizeprobe)

		## Filter out bulk solvent, ie solvent grid points that are > args.maxdistance from the protein
		## due to the cubic shape of the box

		nonbulk_gridsolv = filter_out_bulksolvent(selection_coords = selection_coords, grid = grid, grid_solv = grid_solv, maxdistance = args.maxdistance)

		# Most time consuming function (less now that we trim out bulk solvent)
		# Scans solvent grid points to set the buriedness of all grid points and identify
		# potential cavity grid points

		grid_decomposition = set_burial_scandir_np(grid_solv = nonbulk_gridsolv, grid_decomposition = grid_decomposition_0, grid_protein = grid_protein,
			grid_shape = grid_shape, radius_cube = args.radius_cube, min_burial = args.min_burial,
			radius_cube_enc = args.radius_cube_enc, min_burial_enc = args.min_burial_enc)

		# Generate a graph from potential grid points. Filter out self loops, bridges, not well connected nodes
		# (with min_degree)

		G, cav = generate_graph(grid_decomposition, grid, grid_min, grid_shape, gridspace = args.gridspace,
			min_degree = args.min_degree, radius = 2, score = args.trim_score)
		if G == None:
			print(f"{args.code[0:-4]} does not have a cavity")
			return buf.getvalue() 
	
	
		# ------------------------------------------------------------------------------------------- #
		# ------------------------------- CAVITY FILTERING ROUTINES --------------------------------- #
		# ------------------------------------------------------------------------------------------- #
	
	
		# Filter out small cavities
		array_cavs_coords = get_large_cavities_from_graph(G, cav, min_points = args.min_points * 1/args.gridspace) # adapt number of points with gridspace
		# Score cavities, filter out cavities that have less that 1-quantile grid points
		# buried with a min_burial_q
		cavities, cavities_info = filter_cavities(array_cavs_coords, grid_decomposition, grid_min, grid_shape, gridspace = args.gridspace,
			min_burial_q = args.min_burial_q, quantile = args.quantile)

	
		# Set pharmacophore properties to cavity grid points

		pharmacophore_types = set_pharmacophore_type(cavities, selection_protein, selection_coords)

	
		# Combine information, exclude the cavities that were filtered before + cavities that are too
		# hydrophobic (max_hydrophobicity)

		filtered_cavities, filtered_pharma, info_list = combine_filterhydro(cavities_info, cavities, pharmacophore_types,
			max_hydrophobicity = args.max_hydrophobicity)
	
		# Check if cavities are interchain cavities, miss residues/atoms, contain altloc atoms
		cav_flags = check_protein_res(filtered_cavities, selection_coords, selection_protein, dict_pdb_info)
		# Join this information with the scores previously calculated in a dictionary containing everything
		dict_all_info = join_information_cavities(cav_flags, filtered_cavities, info_list, exclude_missing = args.exclude_missing,
									exclude_interchain = args.exclude_interchain, exclude_altlocs = args.exclude_altlocs)
	
		# Rank cavities for futher exploitation, exclude if flags (defined in the previous function)
		final_cavities, order = get_final_sorted_cavs(dict_all_info, filtered_cavities)
		try:
			if not final_cavities.any():
				print(f"{args.code[0:-4]} does not have a cavity")
				return buf.getvalue()
		except:
			None
	
		# Get information about asphericity of cavity points	
		#list_asph = get_list_asph(final_cavities = final_cavities, grid = grid, grid_min = grid_min, grid_shape = grid_shape, radius = 3)
	
		# Creates cavity object to try to put all of the information together
		cavities = fill_cavities_object(dict_all_info, order, filtered_cavities, filtered_pharma,
		grid_decomposition, grid_min, grid_shape, gridspace = args.gridspace) # list_asph
		
		#from ligandability import calculate_ligandability
		#print("mais bite??")
		for cava in range(0, len(cavities)):
			ligability = float(calculate_ligandability(cavities, cava))
			cavities[cava].ligandability = ligability

		# Print formatted information
		print_scores(dict_all_info, order, pdbcode = args.code[0:-4])
	
		# Export a dummy pdb containing the filtered, ranked cavities with buriedness data (in B factor column)
		# and pharmacophore types (in occupancy column)
		export_pdb_cavity(final_cavities, filtered_pharma, args.code[0:-4], grid_min, grid_shape,
			grid_decomposition, order, selection_protein = pdbobject,
		gridspace = args.gridspace, outdir = args.out, withprot = args.withprot, #listlig = list_ligands,
		oridir = str(args.sourcedir))


		# ------------------------------------------------------------------------------------------- #
		# ----------------------------------- THIS IS THE END! -------------------------------------- #
		# ------------------------------------------------------------------------------------------- #
	
		#print(f"{args.code[0:-4]}_cavs.pdb written in ./caviar_out/")
		fn = f"{args.code[0:-4]}_cavs.pdb"

		data_forsubcav_routines = [filtered_cavities, order, grid_min, grid_shape, filtered_pharma,
		cavities, pdbobject]
		
		return buf.getvalue(), fn, data_forsubcav_routines


def runsubcavities(data_forsubcav_routines, args, cavid = None):

	# ------------------------------------------------------------------------------------------- #
	# -------------------------------- SUBCAVITIES ROUTINES ------------------------------------- #
	# ------------------------------------------------------------------------------------------- #
	# Read the input data
	filtered_cavities = data_forsubcav_routines[0]
	order = data_forsubcav_routines[1]
	grid_min = data_forsubcav_routines[2]
	grid_shape = data_forsubcav_routines[3]
	filtered_pharma = data_forsubcav_routines[4]
	cavities = data_forsubcav_routines[5]
	pdbobject = data_forsubcav_routines[6]
	print(args.out)
	with StringIO() as bufsubcav, redirect_stdout(bufsubcav):
		from caviar_gui.prody_parser import writePDB
		writePDB(f"./caviar_out/{args.code[0:-4]}_subcavs.pdb", pdbobject)
			# Iterate over liganded cavities only 
		if len(filtered_cavities) == 1: # Don't go over everything if there's only one cavity!
			cav_of_interest = 0 # We have cavities from 0 but for comprehension we print from 1
			im3d = transform_cav2im3d(filtered_cavities[0],
				grid_min, grid_shape)#, filtered_pharma[0])
			labels = find_subcav_watershed(im3d, seeds_mindist = args.seeds_mindist)
			subcavs = map_subcav_in_cav(cavities, cav_of_interest, labels,
				args.code[:-4], grid_min, grid_shape)
			subcavs = merge_small_enclosed_subcavs(subcavs, minsize_subcavs = 50, min_contacts = 0.667, v = False)
			export_pdb_subcavities(subcavs, args.code[:-4], grid_min, grid_shape,
				gridspace = 1.0, outdir = args.out, oridir = str(args.sourcedir))

		elif cavid:
			#try: #Could be a wrong cavity ID
				cav_of_interest = int(cavid) - 1 # We have cavities from 0 but for comprehension we print from 1
				im3d = transform_cav2im3d(filtered_cavities[order][cav_of_interest],
					grid_min, grid_shape)#, filtered_pharma[order][cav_of_interest])
				labels = find_subcav_watershed(im3d, seeds_mindist = args.seeds_mindist)
				subcavs = map_subcav_in_cav(cavities, cav_of_interest, labels,
					args.code[:-4], grid_min, grid_shape)
				subcavs = merge_small_enclosed_subcavs(subcavs, minsize_subcavs = 50, min_contacts = 0.667, v = False)
				export_pdb_subcavities(subcavs, args.code[:-4], grid_min, grid_shape, cavid = cavid,
					gridspace = 1.0, outdir = args.out, oridir = str(args.sourcedir))
			#except:
			#	print(f"Are you sure the cavity ID is an existing cavity?")
		# Iterate all cavities
		else:
			for cav_of_interest in range(0, len(cavities)):
				im3d = transform_cav2im3d(filtered_cavities[order][cav_of_interest], grid_min,
					grid_shape)#, filtered_pharma[order][cav_of_interest])
				labels = find_subcav_watershed(im3d, seeds_mindist = args.seeds_mindist)
				subcavs = map_subcav_in_cav(cavities, cav_of_interest, labels, args.code[:-4], grid_min, grid_shape)
				subcavs = merge_small_enclosed_subcavs(subcavs, minsize_subcavs = 50, min_contacts = 0.667, v = False)
				export_pdb_subcavities(subcavs, args.code[:-4], grid_min, grid_shape, cavid = cav_of_interest,
				gridspace = 1.0, outdir = args.out, oridir = str(args.sourcedir))
	
		fn = f"{args.code[0:-4]}_subcavs.pdb"
		return bufsubcav.getvalue(), fn


if __name__ == "__main__":
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
							printv("You specified liglist_in_pdblist but there is no second column with lig ID")
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


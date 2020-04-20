# -*- coding: utf-8 -*-

"""
Parser function for reading parameter files
"""


__all__ = ['get_default_parameters', 'get_custom_parameters']

def get_default_parameters(preset_choice = "default"):
	"""
	Parses default parameter files
	can take a preset value: default, cavities_only, subcavities_only
	"""
	import configparser, os
    
	root = os.path.dirname(__file__) # =< 
	#root = "/home/marchje7/cavities/dev_caviar/caviar/src/caviar/"

	conffile = configparser.ConfigParser(inline_comment_prefixes ="#", allow_no_value = True, empty_lines_in_values =False, interpolation = None)
	conffile.read(os.path.realpath(os.path.join(root, "..", 'config', preset_choice+'.yaml')))
	
	# Starts a dictionary and then we simply put everything by hand, did not find a better solution
	args = {}
	#Input section
	args["sourcedir"] = conffile["input"]["sourcedir"]
	args["v"] = conffile["input"].getboolean("v")
	args["code"] = conffile["input"]["code"]
	args["codeslist"] = conffile["input"]["codeslist"]
	args["onlyxr"] = conffile["input"].getboolean("onlyxr")
	args["resolution_filter"] = conffile["input"].getboolean("resolution_filter")
	args["resolution"] = conffile["input"].getfloat("resolution")
	args["pdbversion_filter"] = conffile["input"].getboolean("pdbversion_filter")
	args["pdbversion"] = conffile["input"].getfloat("pdbversion")
	args["caveat"] = conffile["input"].getboolean("caveat")
	args["obsolete"] = conffile["input"].getboolean("obsolete")
	args["deposition_date_filter"] = conffile["input"].getboolean("deposition_date_filter")
	args["date"] = conffile["input"].getint("date")
	#Output section
	args["out"] = conffile["output"]["out"]
	args["export_cavities"] = conffile["output"].getboolean("export_cavities")
	args["withprot"] = conffile["output"].getboolean("withprot")
	args["write_pml_cavs"] = conffile["output"].getboolean("write_pml_cavs")
	args["color_cavs_by"] = conffile["output"]["color_cavs_by"]
	args["print_cav_info"] = conffile["output"].getboolean("print_cav_info")
	args["detect_only"] = conffile["output"].getboolean("detect_only")
	args["gen_fp"] = conffile["output"].getboolean("gen_fp")
	args["db_write"] = conffile["output"].getboolean("db_write")
	args["db_name"] = conffile["output"]["db_name"]
	#Selection section
	args["metal"] = conffile["selection"].getboolean("metal")
	args["water"] = conffile["selection"].getboolean("water")
	args["threshold_nres"] = conffile["selection"].getint("threshold_nres")
	args["structural_ligand"] = conffile["selection"]["structural_ligand"]
	args["what"] = conffile["selection"]["what"]
	args["min_contacts"] = conffile["selection"].getint("min_contacts")
	args["chain_id"] = conffile["selection"]["chain_id"]
	args["chainid_in_pdblist"] = conffile["selection"].getboolean("chainid_in_pdblist")
	#Cavity_identification section
	args["boxmargin"] = conffile["cavity_identification"].getfloat("boxmargin")
	args["max_distance"] = conffile["cavity_identification"].getfloat("max_distance")
	args["gridspace"] = conffile["cavity_identification"].getfloat("gridspace")
	#args["filevdwsizes"] = conffile["cavity_identification"]["filevdwsizes"]
	args["size_probe"] = conffile["cavity_identification"].getfloat("size_probe")
	args["radius_cube"] = conffile["cavity_identification"].getint("radius_cube")
	args["min_burial"] = conffile["cavity_identification"].getint("min_burial")
	args["radius_cube_enc"] = conffile["cavity_identification"].getint("radius_cube_enc")
	args["min_burial_enc"] = conffile["cavity_identification"].getint("min_burial_enc")
	args["min_points"] = conffile["cavity_identification"].getint("min_points")
	args["trim_score"] = conffile["cavity_identification"].getint("trim_score")
	args["min_degree"] = conffile["cavity_identification"].getint("min_degree")
	#Cavity_filtering section
	args["min_burial_q"] = conffile["cavity_filtering"].getint("min_burial_q")
	args["quantile"] = conffile["cavity_filtering"].getfloat("quantile")
	args["max_hydrophobicity"] = conffile["cavity_filtering"].getfloat("max_hydrophobicity")
	args["exclude_interchain"] = conffile["cavity_filtering"].getboolean("exclude_interchain")
	args["exclude_missing"] = conffile["cavity_filtering"].getboolean("exclude_missing")
	args["exclude_altlocs"] = conffile["cavity_filtering"].getboolean("exclude_altlocs")
	#Ligand_check section
	args["iflig_print"] = conffile["ligand_check"].getboolean("iflig_print")
	args["excl_ligs"] = conffile["ligand_check"].getboolean("excl_ligs")
	args["lig_tabu_list"] = conffile["ligand_check"]["lig_tabu_list"]
	args["ligsizeflag"] = conffile["ligand_check"].getboolean("ligsizeflag")
	args["ligminsize"] = conffile["ligand_check"].getint("ligminsize")
	args["lig_id"] = conffile["ligand_check"]["lig_id"]
	args["liglist_in_pdblist"] = conffile["ligand_check"].getboolean("liglist_in_pdblist")
	args["lig_tocenter"] = conffile["ligand_check"].getboolean("lig_tocenter")
	#Sucavity_routines section
	args["subcavs_decomp"] = conffile["subcavity_routines"].getboolean("subcavs_decomp")
	args["subcavs_lig_only"] = conffile["subcavity_routines"].getboolean("subcavs_lig_only")
	args["export_subcavs"] = conffile["subcavity_routines"].getboolean("export_subcavs")
	args["write_pml_subcavs"] = conffile["subcavity_routines"].getboolean("write_pml_subcavs")
	args["seeds_mindist"] = conffile["subcavity_routines"].getfloat("seeds_mindist")
	args["merge_subcavs"] = conffile["subcavity_routines"].getboolean("merge_subcavs")
	args["print_pphores_subcavs"] = conffile["subcavity_routines"].getboolean("print_pphores_subcavs")

	return args

def get_custom_parameters(file):
	"""
	Parses a custom parameter files
	"""
	import configparser, os
    
	conffile = configparser.ConfigParser(inline_comment_prefixes ="#")
	conffile.read(file)
	
	from ast import literal_eval
	args = {}
	for section in conffile.sections():
		for param in conffile[section]:
			# literal_eval does not like strings, if crashes: set as (default) string
			try: args[param] = literal_eval(conffile[section][param])
			except: args[param] = conffile[section][param]

	return args

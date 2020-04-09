load ../pdb_cleaned/1c70.pdb
hide everything, 1c70 
show cartoon, 1c70
util.cbc 1c70
load 1c70_gps_P_1.pdb
load 1c70_gps_P_2.pdb
load 1c70_gps_P_3.pdb
load 1c70_gps_P_4.pdb
load 1c70_gps_P_2_1.pdb
load 1c70_gps_P_2_2.pdb
load 1c70_gps_P_3_1.pdb
load 1c70_gps_P_3_2.pdb
set sphere_scale, 0.1
group 1c70_poc_grids, 1c70_gps_P_1 1c70_gps_P_2 1c70_gps_P_3 1c70_gps_P_4 
hide everything, 1c70_poc_grids 
show spheres, 1c70_poc_grids 
set sphere_scale, 0.1
group 1c70_spoc_grids, 1c70_gps_P_2_1 1c70_gps_P_2_2 1c70_gps_P_3_1 1c70_gps_P_3_2 
hide everything, 1c70_spoc_grids 
show spheres, 1c70_spoc_grids 
show sticks, HETATM and 1c70 and not resn HOH
util.cbay("HETATM and 1c70 and not resn HOH")
hide everything, hydrogens
zoom 1c70 

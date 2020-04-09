load ../pdb_cleaned/2fwz.pdb
hide everything, 2fwz 
show cartoon, 2fwz
util.cbc 2fwz
load 2fwz_gps_P_1.pdb
load 2fwz_gps_P_2.pdb
load 2fwz_gps_P_3.pdb
load 2fwz_gps_P_4.pdb
load 2fwz_gps_P_5.pdb
load 2fwz_gps_P_1_1.pdb
load 2fwz_gps_P_1_2.pdb
load 2fwz_gps_P_1_3.pdb
load 2fwz_gps_P_1_4.pdb
load 2fwz_gps_P_2_1.pdb
load 2fwz_gps_P_2_2.pdb
load 2fwz_gps_P_2_3.pdb
load 2fwz_gps_P_3_1.pdb
load 2fwz_gps_P_3_2.pdb
load 2fwz_gps_P_4_1.pdb
load 2fwz_gps_P_4_2.pdb
load 2fwz_gps_P_4_3.pdb
set sphere_scale, 0.1
group 2fwz_poc_grids, 2fwz_gps_P_1 2fwz_gps_P_2 2fwz_gps_P_3 2fwz_gps_P_4 2fwz_gps_P_5 
hide everything, 2fwz_poc_grids 
show spheres, 2fwz_poc_grids 
set sphere_scale, 0.1
group 2fwz_spoc_grids, 2fwz_gps_P_1_1 2fwz_gps_P_1_2 2fwz_gps_P_1_3 2fwz_gps_P_1_4 2fwz_gps_P_2_1 2fwz_gps_P_2_2 2fwz_gps_P_2_3 2fwz_gps_P_3_1 2fwz_gps_P_3_2 2fwz_gps_P_4_1 2fwz_gps_P_4_2 2fwz_gps_P_4_3 
hide everything, 2fwz_spoc_grids 
show spheres, 2fwz_spoc_grids 
show sticks, HETATM and 2fwz and not resn HOH
util.cbay("HETATM and 2fwz and not resn HOH")
hide everything, hydrogens
zoom 2fwz 

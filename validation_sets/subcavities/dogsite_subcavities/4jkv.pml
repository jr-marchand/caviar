load ../pdb_cleaned/4jkv.pdb
hide everything, 4jkv 
show cartoon, 4jkv
util.cbc 4jkv
load 4jkv_gps_P_1.pdb
load 4jkv_gps_P_2.pdb
load 4jkv_gps_P_3.pdb
load 4jkv_gps_P_4.pdb
load 4jkv_gps_P_5.pdb
load 4jkv_gps_P_6.pdb
load 4jkv_gps_P_7.pdb
load 4jkv_gps_P_8.pdb
load 4jkv_gps_P_9.pdb
load 4jkv_gps_P_10.pdb
load 4jkv_gps_P_11.pdb
load 4jkv_gps_P_12.pdb
load 4jkv_gps_P_13.pdb
load 4jkv_gps_P_14.pdb
load 4jkv_gps_P_15.pdb
load 4jkv_gps_P_1_1.pdb
load 4jkv_gps_P_1_2.pdb
load 4jkv_gps_P_1_3.pdb
load 4jkv_gps_P_1_4.pdb
load 4jkv_gps_P_2_1.pdb
load 4jkv_gps_P_2_2.pdb
load 4jkv_gps_P_2_3.pdb
load 4jkv_gps_P_3_1.pdb
load 4jkv_gps_P_3_2.pdb
load 4jkv_gps_P_3_3.pdb
load 4jkv_gps_P_4_1.pdb
load 4jkv_gps_P_4_2.pdb
load 4jkv_gps_P_4_3.pdb
set sphere_scale, 0.1
group 4jkv_poc_grids, 4jkv_gps_P_1 4jkv_gps_P_2 4jkv_gps_P_3 4jkv_gps_P_4 4jkv_gps_P_5 4jkv_gps_P_6 4jkv_gps_P_7 4jkv_gps_P_8 4jkv_gps_P_9 4jkv_gps_P_10 4jkv_gps_P_11 4jkv_gps_P_12 4jkv_gps_P_13 4jkv_gps_P_14 4jkv_gps_P_15 
hide everything, 4jkv_poc_grids 
show spheres, 4jkv_poc_grids 
set sphere_scale, 0.1
group 4jkv_spoc_grids, 4jkv_gps_P_1_1 4jkv_gps_P_1_2 4jkv_gps_P_1_3 4jkv_gps_P_1_4 4jkv_gps_P_2_1 4jkv_gps_P_2_2 4jkv_gps_P_2_3 4jkv_gps_P_3_1 4jkv_gps_P_3_2 4jkv_gps_P_3_3 4jkv_gps_P_4_1 4jkv_gps_P_4_2 4jkv_gps_P_4_3 
hide everything, 4jkv_spoc_grids 
show spheres, 4jkv_spoc_grids 
show sticks, HETATM and 4jkv and not resn HOH
util.cbay("HETATM and 4jkv and not resn HOH")
hide everything, hydrogens
zoom 4jkv 

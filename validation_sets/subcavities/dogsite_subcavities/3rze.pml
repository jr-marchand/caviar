load ../pdb_cleaned/3rze.pdb
hide everything, 3rze 
show cartoon, 3rze
util.cbc 3rze
load 3rze_gps_P_1.pdb
load 3rze_gps_P_2.pdb
load 3rze_gps_P_3.pdb
load 3rze_gps_P_4.pdb
load 3rze_gps_P_5.pdb
load 3rze_gps_P_6.pdb
load 3rze_gps_P_7.pdb
load 3rze_gps_P_8.pdb
load 3rze_gps_P_9.pdb
load 3rze_gps_P_1_1.pdb
load 3rze_gps_P_1_2.pdb
load 3rze_gps_P_1_3.pdb
load 3rze_gps_P_2_1.pdb
load 3rze_gps_P_2_2.pdb
load 3rze_gps_P_3_1.pdb
load 3rze_gps_P_3_2.pdb
load 3rze_gps_P_3_3.pdb
load 3rze_gps_P_4_1.pdb
load 3rze_gps_P_4_2.pdb
set sphere_scale, 0.1
group 3rze_poc_grids, 3rze_gps_P_1 3rze_gps_P_2 3rze_gps_P_3 3rze_gps_P_4 3rze_gps_P_5 3rze_gps_P_6 3rze_gps_P_7 3rze_gps_P_8 3rze_gps_P_9 
hide everything, 3rze_poc_grids 
show spheres, 3rze_poc_grids 
set sphere_scale, 0.1
group 3rze_spoc_grids, 3rze_gps_P_1_1 3rze_gps_P_1_2 3rze_gps_P_1_3 3rze_gps_P_2_1 3rze_gps_P_2_2 3rze_gps_P_3_1 3rze_gps_P_3_2 3rze_gps_P_3_3 3rze_gps_P_4_1 3rze_gps_P_4_2 
hide everything, 3rze_spoc_grids 
show spheres, 3rze_spoc_grids 
show sticks, HETATM and 3rze and not resn HOH
util.cbay("HETATM and 3rze and not resn HOH")
hide everything, hydrogens
zoom 3rze 

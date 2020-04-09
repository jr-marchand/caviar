load ../pdb_cleaned/1xkk.pdb
hide everything, 1xkk 
show cartoon, 1xkk
util.cbc 1xkk
load 1xkk_gps_P_1.pdb
load 1xkk_gps_P_2.pdb
load 1xkk_gps_P_3.pdb
load 1xkk_gps_P_4.pdb
load 1xkk_gps_P_5.pdb
load 1xkk_gps_P_6.pdb
load 1xkk_gps_P_7.pdb
load 1xkk_gps_P_1_1.pdb
load 1xkk_gps_P_1_2.pdb
load 1xkk_gps_P_1_3.pdb
load 1xkk_gps_P_1_4.pdb
load 1xkk_gps_P_1_5.pdb
load 1xkk_gps_P_2_1.pdb
load 1xkk_gps_P_2_2.pdb
load 1xkk_gps_P_3_1.pdb
load 1xkk_gps_P_3_2.pdb
load 1xkk_gps_P_3_3.pdb
load 1xkk_gps_P_4_1.pdb
load 1xkk_gps_P_4_2.pdb
set sphere_scale, 0.1
group 1xkk_poc_grids, 1xkk_gps_P_1 1xkk_gps_P_2 1xkk_gps_P_3 1xkk_gps_P_4 1xkk_gps_P_5 1xkk_gps_P_6 1xkk_gps_P_7 
hide everything, 1xkk_poc_grids 
show spheres, 1xkk_poc_grids 
set sphere_scale, 0.1
group 1xkk_spoc_grids, 1xkk_gps_P_1_1 1xkk_gps_P_1_2 1xkk_gps_P_1_3 1xkk_gps_P_1_4 1xkk_gps_P_1_5 1xkk_gps_P_2_1 1xkk_gps_P_2_2 1xkk_gps_P_3_1 1xkk_gps_P_3_2 1xkk_gps_P_3_3 1xkk_gps_P_4_1 1xkk_gps_P_4_2 
hide everything, 1xkk_spoc_grids 
show spheres, 1xkk_spoc_grids 
show sticks, HETATM and 1xkk and not resn HOH
util.cbay("HETATM and 1xkk and not resn HOH")
hide everything, hydrogens
zoom 1xkk 

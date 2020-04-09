load ../pdb_cleaned/4ib4.pdb
hide everything, 4ib4 
show cartoon, 4ib4
util.cbc 4ib4
load 4ib4_gps_P_1.pdb
load 4ib4_gps_P_2.pdb
load 4ib4_gps_P_3.pdb
load 4ib4_gps_P_4.pdb
load 4ib4_gps_P_5.pdb
load 4ib4_gps_P_6.pdb
load 4ib4_gps_P_7.pdb
load 4ib4_gps_P_8.pdb
load 4ib4_gps_P_1_1.pdb
load 4ib4_gps_P_1_2.pdb
load 4ib4_gps_P_1_3.pdb
load 4ib4_gps_P_1_4.pdb
load 4ib4_gps_P_1_5.pdb
load 4ib4_gps_P_1_6.pdb
load 4ib4_gps_P_2_1.pdb
load 4ib4_gps_P_2_2.pdb
load 4ib4_gps_P_2_3.pdb
load 4ib4_gps_P_2_4.pdb
load 4ib4_gps_P_3_1.pdb
load 4ib4_gps_P_3_2.pdb
load 4ib4_gps_P_3_3.pdb
load 4ib4_gps_P_5_1.pdb
load 4ib4_gps_P_5_2.pdb
set sphere_scale, 0.1
group 4ib4_poc_grids, 4ib4_gps_P_1 4ib4_gps_P_2 4ib4_gps_P_3 4ib4_gps_P_4 4ib4_gps_P_5 4ib4_gps_P_6 4ib4_gps_P_7 4ib4_gps_P_8 
hide everything, 4ib4_poc_grids 
show spheres, 4ib4_poc_grids 
set sphere_scale, 0.1
group 4ib4_spoc_grids, 4ib4_gps_P_1_1 4ib4_gps_P_1_2 4ib4_gps_P_1_3 4ib4_gps_P_1_4 4ib4_gps_P_1_5 4ib4_gps_P_1_6 4ib4_gps_P_2_1 4ib4_gps_P_2_2 4ib4_gps_P_2_3 4ib4_gps_P_2_4 4ib4_gps_P_3_1 4ib4_gps_P_3_2 4ib4_gps_P_3_3 4ib4_gps_P_5_1 4ib4_gps_P_5_2 
hide everything, 4ib4_spoc_grids 
show spheres, 4ib4_spoc_grids 
show sticks, HETATM and 4ib4 and not resn HOH
util.cbay("HETATM and 4ib4 and not resn HOH")
hide everything, hydrogens
zoom 4ib4 

load ../pdb_cleaned/2hha.pdb
hide everything, 2hha 
show cartoon, 2hha
util.cbc 2hha
load 2hha_gps_P_1.pdb
load 2hha_gps_P_2.pdb
load 2hha_gps_P_3.pdb
load 2hha_gps_P_4.pdb
load 2hha_gps_P_5.pdb
load 2hha_gps_P_6.pdb
load 2hha_gps_P_7.pdb
load 2hha_gps_P_8.pdb
load 2hha_gps_P_9.pdb
load 2hha_gps_P_10.pdb
load 2hha_gps_P_11.pdb
load 2hha_gps_P_12.pdb
load 2hha_gps_P_13.pdb
load 2hha_gps_P_14.pdb
load 2hha_gps_P_15.pdb
load 2hha_gps_P_16.pdb
load 2hha_gps_P_17.pdb
load 2hha_gps_P_18.pdb
load 2hha_gps_P_19.pdb
load 2hha_gps_P_20.pdb
load 2hha_gps_P_21.pdb
load 2hha_gps_P_22.pdb
load 2hha_gps_P_23.pdb
load 2hha_gps_P_24.pdb
load 2hha_gps_P_1_1.pdb
load 2hha_gps_P_1_2.pdb
load 2hha_gps_P_1_3.pdb
load 2hha_gps_P_1_4.pdb
load 2hha_gps_P_1_5.pdb
load 2hha_gps_P_1_6.pdb
load 2hha_gps_P_1_7.pdb
load 2hha_gps_P_1_8.pdb
load 2hha_gps_P_1_9.pdb
load 2hha_gps_P_2_1.pdb
load 2hha_gps_P_2_2.pdb
load 2hha_gps_P_2_3.pdb
load 2hha_gps_P_2_4.pdb
load 2hha_gps_P_3_1.pdb
load 2hha_gps_P_3_2.pdb
load 2hha_gps_P_3_3.pdb
load 2hha_gps_P_4_1.pdb
load 2hha_gps_P_4_2.pdb
load 2hha_gps_P_6_1.pdb
load 2hha_gps_P_6_2.pdb
load 2hha_gps_P_7_1.pdb
load 2hha_gps_P_7_2.pdb
load 2hha_gps_P_18_1.pdb
load 2hha_gps_P_18_2.pdb
set sphere_scale, 0.1
group 2hha_poc_grids, 2hha_gps_P_1 2hha_gps_P_2 2hha_gps_P_3 2hha_gps_P_4 2hha_gps_P_5 2hha_gps_P_6 2hha_gps_P_7 2hha_gps_P_8 2hha_gps_P_9 2hha_gps_P_10 2hha_gps_P_11 2hha_gps_P_12 2hha_gps_P_13 2hha_gps_P_14 2hha_gps_P_15 2hha_gps_P_16 2hha_gps_P_17 2hha_gps_P_18 2hha_gps_P_19 2hha_gps_P_20 2hha_gps_P_21 2hha_gps_P_22 2hha_gps_P_23 2hha_gps_P_24 
hide everything, 2hha_poc_grids 
show spheres, 2hha_poc_grids 
set sphere_scale, 0.1
group 2hha_spoc_grids, 2hha_gps_P_1_1 2hha_gps_P_1_2 2hha_gps_P_1_3 2hha_gps_P_1_4 2hha_gps_P_1_5 2hha_gps_P_1_6 2hha_gps_P_1_7 2hha_gps_P_1_8 2hha_gps_P_1_9 2hha_gps_P_2_1 2hha_gps_P_2_2 2hha_gps_P_2_3 2hha_gps_P_2_4 2hha_gps_P_3_1 2hha_gps_P_3_2 2hha_gps_P_3_3 2hha_gps_P_4_1 2hha_gps_P_4_2 2hha_gps_P_6_1 2hha_gps_P_6_2 2hha_gps_P_7_1 2hha_gps_P_7_2 2hha_gps_P_18_1 2hha_gps_P_18_2 
hide everything, 2hha_spoc_grids 
show spheres, 2hha_spoc_grids 
show sticks, HETATM and 2hha and not resn HOH
util.cbay("HETATM and 2hha and not resn HOH")
hide everything, hydrogens
zoom 2hha 

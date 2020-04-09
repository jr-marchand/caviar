load ../pdb_cleaned/4a5s.pdb
hide everything, 4a5s 
show cartoon, 4a5s
util.cbc 4a5s
load 4a5s_gps_P_1.pdb
load 4a5s_gps_P_2.pdb
load 4a5s_gps_P_3.pdb
load 4a5s_gps_P_4.pdb
load 4a5s_gps_P_5.pdb
load 4a5s_gps_P_6.pdb
load 4a5s_gps_P_7.pdb
load 4a5s_gps_P_8.pdb
load 4a5s_gps_P_9.pdb
load 4a5s_gps_P_10.pdb
load 4a5s_gps_P_11.pdb
load 4a5s_gps_P_12.pdb
load 4a5s_gps_P_13.pdb
load 4a5s_gps_P_14.pdb
load 4a5s_gps_P_15.pdb
load 4a5s_gps_P_16.pdb
load 4a5s_gps_P_17.pdb
load 4a5s_gps_P_18.pdb
load 4a5s_gps_P_19.pdb
load 4a5s_gps_P_20.pdb
load 4a5s_gps_P_21.pdb
load 4a5s_gps_P_22.pdb
load 4a5s_gps_P_23.pdb
load 4a5s_gps_P_24.pdb
load 4a5s_gps_P_1_1.pdb
load 4a5s_gps_P_1_2.pdb
load 4a5s_gps_P_1_3.pdb
load 4a5s_gps_P_1_4.pdb
load 4a5s_gps_P_2_1.pdb
load 4a5s_gps_P_2_2.pdb
load 4a5s_gps_P_3_1.pdb
load 4a5s_gps_P_3_2.pdb
load 4a5s_gps_P_4_1.pdb
load 4a5s_gps_P_4_2.pdb
load 4a5s_gps_P_4_3.pdb
load 4a5s_gps_P_5_1.pdb
load 4a5s_gps_P_5_2.pdb
load 4a5s_gps_P_8_1.pdb
load 4a5s_gps_P_8_2.pdb
load 4a5s_gps_P_9_1.pdb
load 4a5s_gps_P_9_2.pdb
load 4a5s_gps_P_13_1.pdb
load 4a5s_gps_P_13_2.pdb
load 4a5s_gps_P_15_1.pdb
load 4a5s_gps_P_15_2.pdb
load 4a5s_gps_P_16_1.pdb
load 4a5s_gps_P_16_2.pdb
load 4a5s_gps_P_19_1.pdb
load 4a5s_gps_P_19_2.pdb
set sphere_scale, 0.1
group 4a5s_poc_grids, 4a5s_gps_P_1 4a5s_gps_P_2 4a5s_gps_P_3 4a5s_gps_P_4 4a5s_gps_P_5 4a5s_gps_P_6 4a5s_gps_P_7 4a5s_gps_P_8 4a5s_gps_P_9 4a5s_gps_P_10 4a5s_gps_P_11 4a5s_gps_P_12 4a5s_gps_P_13 4a5s_gps_P_14 4a5s_gps_P_15 4a5s_gps_P_16 4a5s_gps_P_17 4a5s_gps_P_18 4a5s_gps_P_19 4a5s_gps_P_20 4a5s_gps_P_21 4a5s_gps_P_22 4a5s_gps_P_23 4a5s_gps_P_24 
hide everything, 4a5s_poc_grids 
show spheres, 4a5s_poc_grids 
set sphere_scale, 0.1
group 4a5s_spoc_grids, 4a5s_gps_P_1_1 4a5s_gps_P_1_2 4a5s_gps_P_1_3 4a5s_gps_P_1_4 4a5s_gps_P_2_1 4a5s_gps_P_2_2 4a5s_gps_P_3_1 4a5s_gps_P_3_2 4a5s_gps_P_4_1 4a5s_gps_P_4_2 4a5s_gps_P_4_3 4a5s_gps_P_5_1 4a5s_gps_P_5_2 4a5s_gps_P_8_1 4a5s_gps_P_8_2 4a5s_gps_P_9_1 4a5s_gps_P_9_2 4a5s_gps_P_13_1 4a5s_gps_P_13_2 4a5s_gps_P_15_1 4a5s_gps_P_15_2 4a5s_gps_P_16_1 4a5s_gps_P_16_2 4a5s_gps_P_19_1 4a5s_gps_P_19_2 
hide everything, 4a5s_spoc_grids 
show spheres, 4a5s_spoc_grids 
show sticks, HETATM and 4a5s and not resn HOH
util.cbay("HETATM and 4a5s and not resn HOH")
hide everything, hydrogens
zoom 4a5s 

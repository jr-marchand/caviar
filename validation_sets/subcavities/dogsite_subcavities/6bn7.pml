load ../pdb_cleaned/6bn7.pdb
hide everything, 6bn7 
show cartoon, 6bn7
util.cbc 6bn7
load 6bn7_gps_P_1.pdb
load 6bn7_gps_P_2.pdb
load 6bn7_gps_P_3.pdb
load 6bn7_gps_P_4.pdb
load 6bn7_gps_P_5.pdb
load 6bn7_gps_P_6.pdb
load 6bn7_gps_P_7.pdb
load 6bn7_gps_P_8.pdb
load 6bn7_gps_P_9.pdb
load 6bn7_gps_P_10.pdb
load 6bn7_gps_P_11.pdb
load 6bn7_gps_P_12.pdb
load 6bn7_gps_P_13.pdb
load 6bn7_gps_P_14.pdb
load 6bn7_gps_P_15.pdb
load 6bn7_gps_P_16.pdb
load 6bn7_gps_P_17.pdb
load 6bn7_gps_P_18.pdb
load 6bn7_gps_P_19.pdb
load 6bn7_gps_P_20.pdb
load 6bn7_gps_P_1_1.pdb
load 6bn7_gps_P_1_2.pdb
load 6bn7_gps_P_1_3.pdb
load 6bn7_gps_P_2_1.pdb
load 6bn7_gps_P_2_2.pdb
load 6bn7_gps_P_4_1.pdb
load 6bn7_gps_P_4_2.pdb
load 6bn7_gps_P_5_1.pdb
load 6bn7_gps_P_5_2.pdb
load 6bn7_gps_P_6_1.pdb
load 6bn7_gps_P_6_2.pdb
load 6bn7_gps_P_6_3.pdb
load 6bn7_gps_P_7_1.pdb
load 6bn7_gps_P_7_2.pdb
load 6bn7_gps_P_7_3.pdb
load 6bn7_gps_P_9_1.pdb
load 6bn7_gps_P_9_2.pdb
load 6bn7_gps_P_9_3.pdb
load 6bn7_gps_P_10_1.pdb
load 6bn7_gps_P_10_2.pdb
load 6bn7_gps_P_10_3.pdb
load 6bn7_gps_P_11_1.pdb
load 6bn7_gps_P_11_2.pdb
load 6bn7_gps_P_13_1.pdb
load 6bn7_gps_P_13_2.pdb
load 6bn7_gps_P_15_1.pdb
load 6bn7_gps_P_15_2.pdb
set sphere_scale, 0.1
group 6bn7_poc_grids, 6bn7_gps_P_1 6bn7_gps_P_2 6bn7_gps_P_3 6bn7_gps_P_4 6bn7_gps_P_5 6bn7_gps_P_6 6bn7_gps_P_7 6bn7_gps_P_8 6bn7_gps_P_9 6bn7_gps_P_10 6bn7_gps_P_11 6bn7_gps_P_12 6bn7_gps_P_13 6bn7_gps_P_14 6bn7_gps_P_15 6bn7_gps_P_16 6bn7_gps_P_17 6bn7_gps_P_18 6bn7_gps_P_19 6bn7_gps_P_20 
hide everything, 6bn7_poc_grids 
show spheres, 6bn7_poc_grids 
set sphere_scale, 0.1
group 6bn7_spoc_grids, 6bn7_gps_P_1_1 6bn7_gps_P_1_2 6bn7_gps_P_1_3 6bn7_gps_P_2_1 6bn7_gps_P_2_2 6bn7_gps_P_4_1 6bn7_gps_P_4_2 6bn7_gps_P_5_1 6bn7_gps_P_5_2 6bn7_gps_P_6_1 6bn7_gps_P_6_2 6bn7_gps_P_6_3 6bn7_gps_P_7_1 6bn7_gps_P_7_2 6bn7_gps_P_7_3 6bn7_gps_P_9_1 6bn7_gps_P_9_2 6bn7_gps_P_9_3 6bn7_gps_P_10_1 6bn7_gps_P_10_2 6bn7_gps_P_10_3 6bn7_gps_P_11_1 6bn7_gps_P_11_2 6bn7_gps_P_13_1 6bn7_gps_P_13_2 6bn7_gps_P_15_1 6bn7_gps_P_15_2 
hide everything, 6bn7_spoc_grids 
show spheres, 6bn7_spoc_grids 
show sticks, HETATM and 6bn7 and not resn HOH
util.cbay("HETATM and 6bn7 and not resn HOH")
hide everything, hydrogens
zoom 6bn7 

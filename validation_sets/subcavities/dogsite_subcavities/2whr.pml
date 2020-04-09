load ../pdb_cleaned/2whr.pdb
hide everything, 2whr 
show cartoon, 2whr
util.cbc 2whr
load 2whr_gps_P_1.pdb
load 2whr_gps_P_2.pdb
load 2whr_gps_P_3.pdb
load 2whr_gps_P_4.pdb
load 2whr_gps_P_5.pdb
load 2whr_gps_P_6.pdb
load 2whr_gps_P_7.pdb
load 2whr_gps_P_8.pdb
load 2whr_gps_P_9.pdb
load 2whr_gps_P_10.pdb
load 2whr_gps_P_11.pdb
load 2whr_gps_P_12.pdb
load 2whr_gps_P_13.pdb
load 2whr_gps_P_14.pdb
load 2whr_gps_P_15.pdb
load 2whr_gps_P_16.pdb
load 2whr_gps_P_1_1.pdb
load 2whr_gps_P_1_2.pdb
load 2whr_gps_P_1_3.pdb
load 2whr_gps_P_1_4.pdb
load 2whr_gps_P_1_5.pdb
load 2whr_gps_P_2_1.pdb
load 2whr_gps_P_2_2.pdb
load 2whr_gps_P_2_3.pdb
load 2whr_gps_P_2_4.pdb
load 2whr_gps_P_2_5.pdb
load 2whr_gps_P_3_1.pdb
load 2whr_gps_P_3_2.pdb
load 2whr_gps_P_3_3.pdb
load 2whr_gps_P_4_1.pdb
load 2whr_gps_P_4_2.pdb
load 2whr_gps_P_6_1.pdb
load 2whr_gps_P_6_2.pdb
load 2whr_gps_P_7_1.pdb
load 2whr_gps_P_7_2.pdb
load 2whr_gps_P_9_1.pdb
load 2whr_gps_P_9_2.pdb
load 2whr_gps_P_10_1.pdb
load 2whr_gps_P_10_2.pdb
load 2whr_gps_P_11_1.pdb
load 2whr_gps_P_11_2.pdb
set sphere_scale, 0.1
group 2whr_poc_grids, 2whr_gps_P_1 2whr_gps_P_2 2whr_gps_P_3 2whr_gps_P_4 2whr_gps_P_5 2whr_gps_P_6 2whr_gps_P_7 2whr_gps_P_8 2whr_gps_P_9 2whr_gps_P_10 2whr_gps_P_11 2whr_gps_P_12 2whr_gps_P_13 2whr_gps_P_14 2whr_gps_P_15 2whr_gps_P_16 
hide everything, 2whr_poc_grids 
show spheres, 2whr_poc_grids 
set sphere_scale, 0.1
group 2whr_spoc_grids, 2whr_gps_P_1_1 2whr_gps_P_1_2 2whr_gps_P_1_3 2whr_gps_P_1_4 2whr_gps_P_1_5 2whr_gps_P_2_1 2whr_gps_P_2_2 2whr_gps_P_2_3 2whr_gps_P_2_4 2whr_gps_P_2_5 2whr_gps_P_3_1 2whr_gps_P_3_2 2whr_gps_P_3_3 2whr_gps_P_4_1 2whr_gps_P_4_2 2whr_gps_P_6_1 2whr_gps_P_6_2 2whr_gps_P_7_1 2whr_gps_P_7_2 2whr_gps_P_9_1 2whr_gps_P_9_2 2whr_gps_P_10_1 2whr_gps_P_10_2 2whr_gps_P_11_1 2whr_gps_P_11_2 
hide everything, 2whr_spoc_grids 
show spheres, 2whr_spoc_grids 
show sticks, HETATM and 2whr and not resn HOH
util.cbay("HETATM and 2whr and not resn HOH")
hide everything, hydrogens
zoom 2whr 

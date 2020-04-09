load ../pdb_cleaned/5eqb.pdb
hide everything, 5eqb 
show cartoon, 5eqb
util.cbc 5eqb
load 5eqb_gps_P_1.pdb
load 5eqb_gps_P_2.pdb
load 5eqb_gps_P_3.pdb
load 5eqb_gps_P_4.pdb
load 5eqb_gps_P_5.pdb
load 5eqb_gps_P_6.pdb
load 5eqb_gps_P_7.pdb
load 5eqb_gps_P_8.pdb
load 5eqb_gps_P_9.pdb
load 5eqb_gps_P_10.pdb
load 5eqb_gps_P_11.pdb
load 5eqb_gps_P_12.pdb
load 5eqb_gps_P_13.pdb
load 5eqb_gps_P_14.pdb
load 5eqb_gps_P_15.pdb
load 5eqb_gps_P_16.pdb
load 5eqb_gps_P_17.pdb
load 5eqb_gps_P_18.pdb
load 5eqb_gps_P_1_1.pdb
load 5eqb_gps_P_1_2.pdb
load 5eqb_gps_P_1_3.pdb
load 5eqb_gps_P_1_4.pdb
load 5eqb_gps_P_1_5.pdb
load 5eqb_gps_P_1_6.pdb
load 5eqb_gps_P_1_7.pdb
load 5eqb_gps_P_1_8.pdb
load 5eqb_gps_P_1_9.pdb
load 5eqb_gps_P_1_10.pdb
load 5eqb_gps_P_2_1.pdb
load 5eqb_gps_P_2_2.pdb
load 5eqb_gps_P_3_1.pdb
load 5eqb_gps_P_3_2.pdb
load 5eqb_gps_P_4_1.pdb
load 5eqb_gps_P_4_2.pdb
load 5eqb_gps_P_5_1.pdb
load 5eqb_gps_P_5_2.pdb
load 5eqb_gps_P_7_1.pdb
load 5eqb_gps_P_7_2.pdb
load 5eqb_gps_P_8_1.pdb
load 5eqb_gps_P_8_2.pdb
load 5eqb_gps_P_12_1.pdb
load 5eqb_gps_P_12_2.pdb
load 5eqb_gps_P_16_1.pdb
load 5eqb_gps_P_16_2.pdb
set sphere_scale, 0.1
group 5eqb_poc_grids, 5eqb_gps_P_1 5eqb_gps_P_2 5eqb_gps_P_3 5eqb_gps_P_4 5eqb_gps_P_5 5eqb_gps_P_6 5eqb_gps_P_7 5eqb_gps_P_8 5eqb_gps_P_9 5eqb_gps_P_10 5eqb_gps_P_11 5eqb_gps_P_12 5eqb_gps_P_13 5eqb_gps_P_14 5eqb_gps_P_15 5eqb_gps_P_16 5eqb_gps_P_17 5eqb_gps_P_18 
hide everything, 5eqb_poc_grids 
show spheres, 5eqb_poc_grids 
set sphere_scale, 0.1
group 5eqb_spoc_grids, 5eqb_gps_P_1_1 5eqb_gps_P_1_2 5eqb_gps_P_1_3 5eqb_gps_P_1_4 5eqb_gps_P_1_5 5eqb_gps_P_1_6 5eqb_gps_P_1_7 5eqb_gps_P_1_8 5eqb_gps_P_1_9 5eqb_gps_P_1_10 5eqb_gps_P_2_1 5eqb_gps_P_2_2 5eqb_gps_P_3_1 5eqb_gps_P_3_2 5eqb_gps_P_4_1 5eqb_gps_P_4_2 5eqb_gps_P_5_1 5eqb_gps_P_5_2 5eqb_gps_P_7_1 5eqb_gps_P_7_2 5eqb_gps_P_8_1 5eqb_gps_P_8_2 5eqb_gps_P_12_1 5eqb_gps_P_12_2 5eqb_gps_P_16_1 5eqb_gps_P_16_2 
hide everything, 5eqb_spoc_grids 
show spheres, 5eqb_spoc_grids 
show sticks, HETATM and 5eqb and not resn HOH
util.cbay("HETATM and 5eqb and not resn HOH")
hide everything, hydrogens
zoom 5eqb 

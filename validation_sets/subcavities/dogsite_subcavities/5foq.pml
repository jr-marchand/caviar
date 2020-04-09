load ../pdb_cleaned/5foq.pdb
hide everything, 5foq 
show cartoon, 5foq
util.cbc 5foq
load 5foq_gps_P_1.pdb
load 5foq_gps_P_2.pdb
load 5foq_gps_P_3.pdb
load 5foq_gps_P_4.pdb
load 5foq_gps_P_5.pdb
load 5foq_gps_P_6.pdb
load 5foq_gps_P_7.pdb
load 5foq_gps_P_8.pdb
load 5foq_gps_P_9.pdb
load 5foq_gps_P_10.pdb
load 5foq_gps_P_11.pdb
load 5foq_gps_P_12.pdb
load 5foq_gps_P_13.pdb
load 5foq_gps_P_14.pdb
load 5foq_gps_P_15.pdb
load 5foq_gps_P_1_1.pdb
load 5foq_gps_P_1_2.pdb
load 5foq_gps_P_1_3.pdb
load 5foq_gps_P_1_4.pdb
load 5foq_gps_P_1_5.pdb
load 5foq_gps_P_1_6.pdb
load 5foq_gps_P_1_7.pdb
load 5foq_gps_P_1_8.pdb
load 5foq_gps_P_2_1.pdb
load 5foq_gps_P_2_2.pdb
load 5foq_gps_P_2_3.pdb
load 5foq_gps_P_3_1.pdb
load 5foq_gps_P_3_2.pdb
load 5foq_gps_P_3_3.pdb
load 5foq_gps_P_3_4.pdb
load 5foq_gps_P_4_1.pdb
load 5foq_gps_P_4_2.pdb
load 5foq_gps_P_6_1.pdb
load 5foq_gps_P_6_2.pdb
load 5foq_gps_P_6_3.pdb
load 5foq_gps_P_8_1.pdb
load 5foq_gps_P_8_2.pdb
load 5foq_gps_P_9_1.pdb
load 5foq_gps_P_9_2.pdb
load 5foq_gps_P_10_1.pdb
load 5foq_gps_P_10_2.pdb
set sphere_scale, 0.1
group 5foq_poc_grids, 5foq_gps_P_1 5foq_gps_P_2 5foq_gps_P_3 5foq_gps_P_4 5foq_gps_P_5 5foq_gps_P_6 5foq_gps_P_7 5foq_gps_P_8 5foq_gps_P_9 5foq_gps_P_10 5foq_gps_P_11 5foq_gps_P_12 5foq_gps_P_13 5foq_gps_P_14 5foq_gps_P_15 
hide everything, 5foq_poc_grids 
show spheres, 5foq_poc_grids 
set sphere_scale, 0.1
group 5foq_spoc_grids, 5foq_gps_P_1_1 5foq_gps_P_1_2 5foq_gps_P_1_3 5foq_gps_P_1_4 5foq_gps_P_1_5 5foq_gps_P_1_6 5foq_gps_P_1_7 5foq_gps_P_1_8 5foq_gps_P_2_1 5foq_gps_P_2_2 5foq_gps_P_2_3 5foq_gps_P_3_1 5foq_gps_P_3_2 5foq_gps_P_3_3 5foq_gps_P_3_4 5foq_gps_P_4_1 5foq_gps_P_4_2 5foq_gps_P_6_1 5foq_gps_P_6_2 5foq_gps_P_6_3 5foq_gps_P_8_1 5foq_gps_P_8_2 5foq_gps_P_9_1 5foq_gps_P_9_2 5foq_gps_P_10_1 5foq_gps_P_10_2 
hide everything, 5foq_spoc_grids 
show spheres, 5foq_spoc_grids 
show sticks, HETATM and 5foq and not resn HOH
util.cbay("HETATM and 5foq and not resn HOH")
hide everything, hydrogens
zoom 5foq 

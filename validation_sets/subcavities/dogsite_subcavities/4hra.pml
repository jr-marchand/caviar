load ../pdb_cleaned/4hra.pdb
hide everything, 4hra 
show cartoon, 4hra
util.cbc 4hra
load 4hra_gps_P_1.pdb
load 4hra_gps_P_2.pdb
load 4hra_gps_P_3.pdb
load 4hra_gps_P_4.pdb
load 4hra_gps_P_5.pdb
load 4hra_gps_P_6.pdb
load 4hra_gps_P_7.pdb
load 4hra_gps_P_8.pdb
load 4hra_gps_P_9.pdb
load 4hra_gps_P_10.pdb
load 4hra_gps_P_11.pdb
load 4hra_gps_P_12.pdb
load 4hra_gps_P_13.pdb
load 4hra_gps_P_14.pdb
load 4hra_gps_P_15.pdb
load 4hra_gps_P_16.pdb
load 4hra_gps_P_17.pdb
load 4hra_gps_P_18.pdb
load 4hra_gps_P_19.pdb
load 4hra_gps_P_20.pdb
load 4hra_gps_P_21.pdb
load 4hra_gps_P_22.pdb
load 4hra_gps_P_23.pdb
load 4hra_gps_P_24.pdb
load 4hra_gps_P_1_1.pdb
load 4hra_gps_P_1_2.pdb
load 4hra_gps_P_1_3.pdb
load 4hra_gps_P_2_1.pdb
load 4hra_gps_P_2_2.pdb
load 4hra_gps_P_4_1.pdb
load 4hra_gps_P_4_2.pdb
load 4hra_gps_P_6_1.pdb
load 4hra_gps_P_6_2.pdb
load 4hra_gps_P_7_1.pdb
load 4hra_gps_P_7_2.pdb
load 4hra_gps_P_7_3.pdb
load 4hra_gps_P_8_1.pdb
load 4hra_gps_P_8_2.pdb
load 4hra_gps_P_9_1.pdb
load 4hra_gps_P_9_2.pdb
load 4hra_gps_P_12_1.pdb
load 4hra_gps_P_12_2.pdb
load 4hra_gps_P_15_1.pdb
load 4hra_gps_P_15_2.pdb
set sphere_scale, 0.1
group 4hra_poc_grids, 4hra_gps_P_1 4hra_gps_P_2 4hra_gps_P_3 4hra_gps_P_4 4hra_gps_P_5 4hra_gps_P_6 4hra_gps_P_7 4hra_gps_P_8 4hra_gps_P_9 4hra_gps_P_10 4hra_gps_P_11 4hra_gps_P_12 4hra_gps_P_13 4hra_gps_P_14 4hra_gps_P_15 4hra_gps_P_16 4hra_gps_P_17 4hra_gps_P_18 4hra_gps_P_19 4hra_gps_P_20 4hra_gps_P_21 4hra_gps_P_22 4hra_gps_P_23 4hra_gps_P_24 
hide everything, 4hra_poc_grids 
show spheres, 4hra_poc_grids 
set sphere_scale, 0.1
group 4hra_spoc_grids, 4hra_gps_P_1_1 4hra_gps_P_1_2 4hra_gps_P_1_3 4hra_gps_P_2_1 4hra_gps_P_2_2 4hra_gps_P_4_1 4hra_gps_P_4_2 4hra_gps_P_6_1 4hra_gps_P_6_2 4hra_gps_P_7_1 4hra_gps_P_7_2 4hra_gps_P_7_3 4hra_gps_P_8_1 4hra_gps_P_8_2 4hra_gps_P_9_1 4hra_gps_P_9_2 4hra_gps_P_12_1 4hra_gps_P_12_2 4hra_gps_P_15_1 4hra_gps_P_15_2 
hide everything, 4hra_spoc_grids 
show spheres, 4hra_spoc_grids 
show sticks, HETATM and 4hra and not resn HOH
util.cbay("HETATM and 4hra and not resn HOH")
hide everything, hydrogens
zoom 4hra 

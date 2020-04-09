load ../pdb_cleaned/3fc2.pdb
hide everything, 3fc2 
show cartoon, 3fc2
util.cbc 3fc2
load 3fc2_gps_P_1.pdb
load 3fc2_gps_P_2.pdb
load 3fc2_gps_P_3.pdb
load 3fc2_gps_P_4.pdb
load 3fc2_gps_P_5.pdb
load 3fc2_gps_P_6.pdb
load 3fc2_gps_P_7.pdb
load 3fc2_gps_P_8.pdb
load 3fc2_gps_P_9.pdb
load 3fc2_gps_P_10.pdb
load 3fc2_gps_P_11.pdb
load 3fc2_gps_P_12.pdb
load 3fc2_gps_P_13.pdb
load 3fc2_gps_P_14.pdb
load 3fc2_gps_P_1_1.pdb
load 3fc2_gps_P_1_2.pdb
load 3fc2_gps_P_1_3.pdb
load 3fc2_gps_P_2_1.pdb
load 3fc2_gps_P_2_2.pdb
load 3fc2_gps_P_6_1.pdb
load 3fc2_gps_P_6_2.pdb
load 3fc2_gps_P_6_3.pdb
load 3fc2_gps_P_7_1.pdb
load 3fc2_gps_P_7_2.pdb
load 3fc2_gps_P_8_1.pdb
load 3fc2_gps_P_8_2.pdb
load 3fc2_gps_P_12_1.pdb
load 3fc2_gps_P_12_2.pdb
set sphere_scale, 0.1
group 3fc2_poc_grids, 3fc2_gps_P_1 3fc2_gps_P_2 3fc2_gps_P_3 3fc2_gps_P_4 3fc2_gps_P_5 3fc2_gps_P_6 3fc2_gps_P_7 3fc2_gps_P_8 3fc2_gps_P_9 3fc2_gps_P_10 3fc2_gps_P_11 3fc2_gps_P_12 3fc2_gps_P_13 3fc2_gps_P_14 
hide everything, 3fc2_poc_grids 
show spheres, 3fc2_poc_grids 
set sphere_scale, 0.1
group 3fc2_spoc_grids, 3fc2_gps_P_1_1 3fc2_gps_P_1_2 3fc2_gps_P_1_3 3fc2_gps_P_2_1 3fc2_gps_P_2_2 3fc2_gps_P_6_1 3fc2_gps_P_6_2 3fc2_gps_P_6_3 3fc2_gps_P_7_1 3fc2_gps_P_7_2 3fc2_gps_P_8_1 3fc2_gps_P_8_2 3fc2_gps_P_12_1 3fc2_gps_P_12_2 
hide everything, 3fc2_spoc_grids 
show spheres, 3fc2_spoc_grids 
show sticks, HETATM and 3fc2 and not resn HOH
util.cbay("HETATM and 3fc2 and not resn HOH")
hide everything, hydrogens
zoom 3fc2 

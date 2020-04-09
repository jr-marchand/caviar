load ../pdb_cleaned/3cs9.pdb
hide everything, 3cs9 
show cartoon, 3cs9
util.cbc 3cs9
load 3cs9_gps_P_1.pdb
load 3cs9_gps_P_2.pdb
load 3cs9_gps_P_3.pdb
load 3cs9_gps_P_4.pdb
load 3cs9_gps_P_5.pdb
load 3cs9_gps_P_6.pdb
load 3cs9_gps_P_7.pdb
load 3cs9_gps_P_8.pdb
load 3cs9_gps_P_9.pdb
load 3cs9_gps_P_10.pdb
load 3cs9_gps_P_1_1.pdb
load 3cs9_gps_P_1_2.pdb
load 3cs9_gps_P_1_3.pdb
load 3cs9_gps_P_2_1.pdb
load 3cs9_gps_P_2_2.pdb
load 3cs9_gps_P_2_3.pdb
load 3cs9_gps_P_5_1.pdb
load 3cs9_gps_P_5_2.pdb
load 3cs9_gps_P_6_1.pdb
load 3cs9_gps_P_6_2.pdb
load 3cs9_gps_P_6_3.pdb
set sphere_scale, 0.1
group 3cs9_poc_grids, 3cs9_gps_P_1 3cs9_gps_P_2 3cs9_gps_P_3 3cs9_gps_P_4 3cs9_gps_P_5 3cs9_gps_P_6 3cs9_gps_P_7 3cs9_gps_P_8 3cs9_gps_P_9 3cs9_gps_P_10 
hide everything, 3cs9_poc_grids 
show spheres, 3cs9_poc_grids 
set sphere_scale, 0.1
group 3cs9_spoc_grids, 3cs9_gps_P_1_1 3cs9_gps_P_1_2 3cs9_gps_P_1_3 3cs9_gps_P_2_1 3cs9_gps_P_2_2 3cs9_gps_P_2_3 3cs9_gps_P_5_1 3cs9_gps_P_5_2 3cs9_gps_P_6_1 3cs9_gps_P_6_2 3cs9_gps_P_6_3 
hide everything, 3cs9_spoc_grids 
show spheres, 3cs9_spoc_grids 
show sticks, HETATM and 3cs9 and not resn HOH
util.cbay("HETATM and 3cs9 and not resn HOH")
hide everything, hydrogens
zoom 3cs9 

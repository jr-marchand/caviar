load ../pdb_cleaned/4an2.pdb
hide everything, 4an2 
show cartoon, 4an2
util.cbc 4an2
load 4an2_gps_P_1.pdb
load 4an2_gps_P_2.pdb
load 4an2_gps_P_3.pdb
load 4an2_gps_P_4.pdb
load 4an2_gps_P_5.pdb
load 4an2_gps_P_6.pdb
load 4an2_gps_P_7.pdb
load 4an2_gps_P_8.pdb
load 4an2_gps_P_9.pdb
load 4an2_gps_P_1_1.pdb
load 4an2_gps_P_1_2.pdb
load 4an2_gps_P_2_1.pdb
load 4an2_gps_P_2_2.pdb
load 4an2_gps_P_5_1.pdb
load 4an2_gps_P_5_2.pdb
load 4an2_gps_P_6_1.pdb
load 4an2_gps_P_6_2.pdb
set sphere_scale, 0.1
group 4an2_poc_grids, 4an2_gps_P_1 4an2_gps_P_2 4an2_gps_P_3 4an2_gps_P_4 4an2_gps_P_5 4an2_gps_P_6 4an2_gps_P_7 4an2_gps_P_8 4an2_gps_P_9 
hide everything, 4an2_poc_grids 
show spheres, 4an2_poc_grids 
set sphere_scale, 0.1
group 4an2_spoc_grids, 4an2_gps_P_1_1 4an2_gps_P_1_2 4an2_gps_P_2_1 4an2_gps_P_2_2 4an2_gps_P_5_1 4an2_gps_P_5_2 4an2_gps_P_6_1 4an2_gps_P_6_2 
hide everything, 4an2_spoc_grids 
show spheres, 4an2_spoc_grids 
show sticks, HETATM and 4an2 and not resn HOH
util.cbay("HETATM and 4an2 and not resn HOH")
hide everything, hydrogens
zoom 4an2 

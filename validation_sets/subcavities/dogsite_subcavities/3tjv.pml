load ../pdb_cleaned/3tjv.pdb
hide everything, 3tjv 
show cartoon, 3tjv
util.cbc 3tjv
load 3tjv_gps_P_1.pdb
load 3tjv_gps_P_2.pdb
load 3tjv_gps_P_3.pdb
load 3tjv_gps_P_4.pdb
load 3tjv_gps_P_5.pdb
load 3tjv_gps_P_6.pdb
load 3tjv_gps_P_7.pdb
load 3tjv_gps_P_8.pdb
load 3tjv_gps_P_9.pdb
load 3tjv_gps_P_10.pdb
load 3tjv_gps_P_1_1.pdb
load 3tjv_gps_P_1_2.pdb
load 3tjv_gps_P_1_3.pdb
load 3tjv_gps_P_2_1.pdb
load 3tjv_gps_P_2_2.pdb
load 3tjv_gps_P_2_3.pdb
load 3tjv_gps_P_3_1.pdb
load 3tjv_gps_P_3_2.pdb
load 3tjv_gps_P_4_1.pdb
load 3tjv_gps_P_4_2.pdb
load 3tjv_gps_P_5_1.pdb
load 3tjv_gps_P_5_2.pdb
load 3tjv_gps_P_6_1.pdb
load 3tjv_gps_P_6_2.pdb
load 3tjv_gps_P_7_1.pdb
load 3tjv_gps_P_7_2.pdb
set sphere_scale, 0.1
group 3tjv_poc_grids, 3tjv_gps_P_1 3tjv_gps_P_2 3tjv_gps_P_3 3tjv_gps_P_4 3tjv_gps_P_5 3tjv_gps_P_6 3tjv_gps_P_7 3tjv_gps_P_8 3tjv_gps_P_9 3tjv_gps_P_10 
hide everything, 3tjv_poc_grids 
show spheres, 3tjv_poc_grids 
set sphere_scale, 0.1
group 3tjv_spoc_grids, 3tjv_gps_P_1_1 3tjv_gps_P_1_2 3tjv_gps_P_1_3 3tjv_gps_P_2_1 3tjv_gps_P_2_2 3tjv_gps_P_2_3 3tjv_gps_P_3_1 3tjv_gps_P_3_2 3tjv_gps_P_4_1 3tjv_gps_P_4_2 3tjv_gps_P_5_1 3tjv_gps_P_5_2 3tjv_gps_P_6_1 3tjv_gps_P_6_2 3tjv_gps_P_7_1 3tjv_gps_P_7_2 
hide everything, 3tjv_spoc_grids 
show spheres, 3tjv_spoc_grids 
show sticks, HETATM and 3tjv and not resn HOH
util.cbay("HETATM and 3tjv and not resn HOH")
hide everything, hydrogens
zoom 3tjv 

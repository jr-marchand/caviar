load ../pdb_cleaned/2bqw.pdb
hide everything, 2bqw 
show cartoon, 2bqw
util.cbc 2bqw
load 2bqw_gps_P_1.pdb
load 2bqw_gps_P_2.pdb
load 2bqw_gps_P_3.pdb
load 2bqw_gps_P_4.pdb
load 2bqw_gps_P_5.pdb
load 2bqw_gps_P_6.pdb
load 2bqw_gps_P_7.pdb
load 2bqw_gps_P_8.pdb
load 2bqw_gps_P_9.pdb
load 2bqw_gps_P_10.pdb
load 2bqw_gps_P_11.pdb
load 2bqw_gps_P_1_1.pdb
load 2bqw_gps_P_1_2.pdb
load 2bqw_gps_P_1_3.pdb
load 2bqw_gps_P_2_1.pdb
load 2bqw_gps_P_2_2.pdb
load 2bqw_gps_P_3_1.pdb
load 2bqw_gps_P_3_2.pdb
load 2bqw_gps_P_4_1.pdb
load 2bqw_gps_P_4_2.pdb
load 2bqw_gps_P_7_1.pdb
load 2bqw_gps_P_7_2.pdb
set sphere_scale, 0.1
group 2bqw_poc_grids, 2bqw_gps_P_1 2bqw_gps_P_2 2bqw_gps_P_3 2bqw_gps_P_4 2bqw_gps_P_5 2bqw_gps_P_6 2bqw_gps_P_7 2bqw_gps_P_8 2bqw_gps_P_9 2bqw_gps_P_10 2bqw_gps_P_11 
hide everything, 2bqw_poc_grids 
show spheres, 2bqw_poc_grids 
set sphere_scale, 0.1
group 2bqw_spoc_grids, 2bqw_gps_P_1_1 2bqw_gps_P_1_2 2bqw_gps_P_1_3 2bqw_gps_P_2_1 2bqw_gps_P_2_2 2bqw_gps_P_3_1 2bqw_gps_P_3_2 2bqw_gps_P_4_1 2bqw_gps_P_4_2 2bqw_gps_P_7_1 2bqw_gps_P_7_2 
hide everything, 2bqw_spoc_grids 
show spheres, 2bqw_spoc_grids 
show sticks, HETATM and 2bqw and not resn HOH
util.cbay("HETATM and 2bqw and not resn HOH")
hide everything, hydrogens
zoom 2bqw 

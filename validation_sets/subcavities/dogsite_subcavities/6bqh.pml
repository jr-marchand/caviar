load ../pdb_cleaned/6bqh.pdb
hide everything, 6bqh 
show cartoon, 6bqh
util.cbc 6bqh
load 6bqh_gps_P_1.pdb
load 6bqh_gps_P_2.pdb
load 6bqh_gps_P_3.pdb
load 6bqh_gps_P_4.pdb
load 6bqh_gps_P_5.pdb
load 6bqh_gps_P_6.pdb
load 6bqh_gps_P_7.pdb
load 6bqh_gps_P_1_1.pdb
load 6bqh_gps_P_1_2.pdb
load 6bqh_gps_P_1_3.pdb
load 6bqh_gps_P_1_4.pdb
load 6bqh_gps_P_1_5.pdb
load 6bqh_gps_P_1_6.pdb
load 6bqh_gps_P_1_7.pdb
load 6bqh_gps_P_1_8.pdb
load 6bqh_gps_P_2_1.pdb
load 6bqh_gps_P_2_2.pdb
load 6bqh_gps_P_2_3.pdb
load 6bqh_gps_P_5_1.pdb
load 6bqh_gps_P_5_2.pdb
load 6bqh_gps_P_6_1.pdb
load 6bqh_gps_P_6_2.pdb
set sphere_scale, 0.1
group 6bqh_poc_grids, 6bqh_gps_P_1 6bqh_gps_P_2 6bqh_gps_P_3 6bqh_gps_P_4 6bqh_gps_P_5 6bqh_gps_P_6 6bqh_gps_P_7 
hide everything, 6bqh_poc_grids 
show spheres, 6bqh_poc_grids 
set sphere_scale, 0.1
group 6bqh_spoc_grids, 6bqh_gps_P_1_1 6bqh_gps_P_1_2 6bqh_gps_P_1_3 6bqh_gps_P_1_4 6bqh_gps_P_1_5 6bqh_gps_P_1_6 6bqh_gps_P_1_7 6bqh_gps_P_1_8 6bqh_gps_P_2_1 6bqh_gps_P_2_2 6bqh_gps_P_2_3 6bqh_gps_P_5_1 6bqh_gps_P_5_2 6bqh_gps_P_6_1 6bqh_gps_P_6_2 
hide everything, 6bqh_spoc_grids 
show spheres, 6bqh_spoc_grids 
show sticks, HETATM and 6bqh and not resn HOH
util.cbay("HETATM and 6bqh and not resn HOH")
hide everything, hydrogens
zoom 6bqh 

load ../pdb_cleaned/2rh1.pdb
hide everything, 2rh1 
show cartoon, 2rh1
util.cbc 2rh1
load 2rh1_gps_P_1.pdb
load 2rh1_gps_P_2.pdb
load 2rh1_gps_P_3.pdb
load 2rh1_gps_P_4.pdb
load 2rh1_gps_P_5.pdb
load 2rh1_gps_P_6.pdb
load 2rh1_gps_P_7.pdb
load 2rh1_gps_P_8.pdb
load 2rh1_gps_P_9.pdb
load 2rh1_gps_P_10.pdb
load 2rh1_gps_P_11.pdb
load 2rh1_gps_P_1_1.pdb
load 2rh1_gps_P_1_2.pdb
load 2rh1_gps_P_1_3.pdb
load 2rh1_gps_P_1_4.pdb
load 2rh1_gps_P_1_5.pdb
load 2rh1_gps_P_1_6.pdb
load 2rh1_gps_P_2_1.pdb
load 2rh1_gps_P_2_2.pdb
load 2rh1_gps_P_2_3.pdb
load 2rh1_gps_P_2_4.pdb
load 2rh1_gps_P_2_5.pdb
load 2rh1_gps_P_2_6.pdb
load 2rh1_gps_P_3_1.pdb
load 2rh1_gps_P_3_2.pdb
load 2rh1_gps_P_4_1.pdb
load 2rh1_gps_P_4_2.pdb
load 2rh1_gps_P_10_1.pdb
load 2rh1_gps_P_10_2.pdb
load 2rh1_gps_P_11_1.pdb
load 2rh1_gps_P_11_2.pdb
set sphere_scale, 0.1
group 2rh1_poc_grids, 2rh1_gps_P_1 2rh1_gps_P_2 2rh1_gps_P_3 2rh1_gps_P_4 2rh1_gps_P_5 2rh1_gps_P_6 2rh1_gps_P_7 2rh1_gps_P_8 2rh1_gps_P_9 2rh1_gps_P_10 2rh1_gps_P_11 
hide everything, 2rh1_poc_grids 
show spheres, 2rh1_poc_grids 
set sphere_scale, 0.1
group 2rh1_spoc_grids, 2rh1_gps_P_1_1 2rh1_gps_P_1_2 2rh1_gps_P_1_3 2rh1_gps_P_1_4 2rh1_gps_P_1_5 2rh1_gps_P_1_6 2rh1_gps_P_2_1 2rh1_gps_P_2_2 2rh1_gps_P_2_3 2rh1_gps_P_2_4 2rh1_gps_P_2_5 2rh1_gps_P_2_6 2rh1_gps_P_3_1 2rh1_gps_P_3_2 2rh1_gps_P_4_1 2rh1_gps_P_4_2 2rh1_gps_P_10_1 2rh1_gps_P_10_2 2rh1_gps_P_11_1 2rh1_gps_P_11_2 
hide everything, 2rh1_spoc_grids 
show spheres, 2rh1_spoc_grids 
show sticks, HETATM and 2rh1 and not resn HOH
util.cbay("HETATM and 2rh1 and not resn HOH")
hide everything, hydrogens
zoom 2rh1 

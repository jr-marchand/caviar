load ../pdb_cleaned/5wiu.pdb
hide everything, 5wiu 
show cartoon, 5wiu
util.cbc 5wiu
load 5wiu_gps_P_1.pdb
load 5wiu_gps_P_2.pdb
load 5wiu_gps_P_3.pdb
load 5wiu_gps_P_4.pdb
load 5wiu_gps_P_5.pdb
load 5wiu_gps_P_6.pdb
load 5wiu_gps_P_7.pdb
load 5wiu_gps_P_8.pdb
load 5wiu_gps_P_9.pdb
load 5wiu_gps_P_1_1.pdb
load 5wiu_gps_P_1_2.pdb
load 5wiu_gps_P_1_3.pdb
load 5wiu_gps_P_1_4.pdb
load 5wiu_gps_P_1_5.pdb
load 5wiu_gps_P_1_6.pdb
load 5wiu_gps_P_1_7.pdb
load 5wiu_gps_P_3_1.pdb
load 5wiu_gps_P_3_2.pdb
load 5wiu_gps_P_4_1.pdb
load 5wiu_gps_P_4_2.pdb
load 5wiu_gps_P_4_3.pdb
load 5wiu_gps_P_5_1.pdb
load 5wiu_gps_P_5_2.pdb
load 5wiu_gps_P_6_1.pdb
load 5wiu_gps_P_6_2.pdb
set sphere_scale, 0.1
group 5wiu_poc_grids, 5wiu_gps_P_1 5wiu_gps_P_2 5wiu_gps_P_3 5wiu_gps_P_4 5wiu_gps_P_5 5wiu_gps_P_6 5wiu_gps_P_7 5wiu_gps_P_8 5wiu_gps_P_9 
hide everything, 5wiu_poc_grids 
show spheres, 5wiu_poc_grids 
set sphere_scale, 0.1
group 5wiu_spoc_grids, 5wiu_gps_P_1_1 5wiu_gps_P_1_2 5wiu_gps_P_1_3 5wiu_gps_P_1_4 5wiu_gps_P_1_5 5wiu_gps_P_1_6 5wiu_gps_P_1_7 5wiu_gps_P_3_1 5wiu_gps_P_3_2 5wiu_gps_P_4_1 5wiu_gps_P_4_2 5wiu_gps_P_4_3 5wiu_gps_P_5_1 5wiu_gps_P_5_2 5wiu_gps_P_6_1 5wiu_gps_P_6_2 
hide everything, 5wiu_spoc_grids 
show spheres, 5wiu_spoc_grids 
show sticks, HETATM and 5wiu and not resn HOH
util.cbay("HETATM and 5wiu and not resn HOH")
hide everything, hydrogens
zoom 5wiu 

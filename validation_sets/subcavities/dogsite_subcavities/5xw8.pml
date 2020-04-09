load ../pdb_cleaned/5xw8.pdb
hide everything, 5xw8 
show cartoon, 5xw8
util.cbc 5xw8
load 5xw8_gps_P_1.pdb
load 5xw8_gps_P_2.pdb
load 5xw8_gps_P_3.pdb
load 5xw8_gps_P_4.pdb
load 5xw8_gps_P_5.pdb
load 5xw8_gps_P_1_1.pdb
load 5xw8_gps_P_1_2.pdb
load 5xw8_gps_P_1_3.pdb
load 5xw8_gps_P_4_1.pdb
load 5xw8_gps_P_4_2.pdb
set sphere_scale, 0.1
group 5xw8_poc_grids, 5xw8_gps_P_1 5xw8_gps_P_2 5xw8_gps_P_3 5xw8_gps_P_4 5xw8_gps_P_5 
hide everything, 5xw8_poc_grids 
show spheres, 5xw8_poc_grids 
set sphere_scale, 0.1
group 5xw8_spoc_grids, 5xw8_gps_P_1_1 5xw8_gps_P_1_2 5xw8_gps_P_1_3 5xw8_gps_P_4_1 5xw8_gps_P_4_2 
hide everything, 5xw8_spoc_grids 
show spheres, 5xw8_spoc_grids 
show sticks, HETATM and 5xw8 and not resn HOH
util.cbay("HETATM and 5xw8 and not resn HOH")
hide everything, hydrogens
zoom 5xw8 

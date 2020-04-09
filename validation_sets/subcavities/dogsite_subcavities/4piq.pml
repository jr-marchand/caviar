load ../pdb_cleaned/4piq.pdb
hide everything, 4piq 
show cartoon, 4piq
util.cbc 4piq
load 4piq_gps_P_1.pdb
load 4piq_gps_P_2.pdb
load 4piq_gps_P_3.pdb
load 4piq_gps_P_4.pdb
load 4piq_gps_P_5.pdb
load 4piq_gps_P_6.pdb
load 4piq_gps_P_7.pdb
load 4piq_gps_P_8.pdb
load 4piq_gps_P_1_1.pdb
load 4piq_gps_P_1_2.pdb
load 4piq_gps_P_1_3.pdb
load 4piq_gps_P_2_1.pdb
load 4piq_gps_P_2_2.pdb
load 4piq_gps_P_6_1.pdb
load 4piq_gps_P_6_2.pdb
load 4piq_gps_P_6_3.pdb
set sphere_scale, 0.1
group 4piq_poc_grids, 4piq_gps_P_1 4piq_gps_P_2 4piq_gps_P_3 4piq_gps_P_4 4piq_gps_P_5 4piq_gps_P_6 4piq_gps_P_7 4piq_gps_P_8 
hide everything, 4piq_poc_grids 
show spheres, 4piq_poc_grids 
set sphere_scale, 0.1
group 4piq_spoc_grids, 4piq_gps_P_1_1 4piq_gps_P_1_2 4piq_gps_P_1_3 4piq_gps_P_2_1 4piq_gps_P_2_2 4piq_gps_P_6_1 4piq_gps_P_6_2 4piq_gps_P_6_3 
hide everything, 4piq_spoc_grids 
show spheres, 4piq_spoc_grids 
show sticks, HETATM and 4piq and not resn HOH
util.cbay("HETATM and 4piq and not resn HOH")
hide everything, hydrogens
zoom 4piq 

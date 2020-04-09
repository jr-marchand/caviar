load ../pdb_cleaned/3pbl.pdb
hide everything, 3pbl 
show cartoon, 3pbl
util.cbc 3pbl
load 3pbl_gps_P_1.pdb
load 3pbl_gps_P_2.pdb
load 3pbl_gps_P_3.pdb
load 3pbl_gps_P_4.pdb
load 3pbl_gps_P_5.pdb
load 3pbl_gps_P_6.pdb
load 3pbl_gps_P_7.pdb
load 3pbl_gps_P_8.pdb
load 3pbl_gps_P_9.pdb
load 3pbl_gps_P_10.pdb
load 3pbl_gps_P_1_1.pdb
load 3pbl_gps_P_1_2.pdb
load 3pbl_gps_P_1_3.pdb
load 3pbl_gps_P_1_4.pdb
load 3pbl_gps_P_1_5.pdb
load 3pbl_gps_P_1_6.pdb
load 3pbl_gps_P_2_1.pdb
load 3pbl_gps_P_2_2.pdb
load 3pbl_gps_P_4_1.pdb
load 3pbl_gps_P_4_2.pdb
load 3pbl_gps_P_5_1.pdb
load 3pbl_gps_P_5_2.pdb
load 3pbl_gps_P_10_1.pdb
load 3pbl_gps_P_10_2.pdb
set sphere_scale, 0.1
group 3pbl_poc_grids, 3pbl_gps_P_1 3pbl_gps_P_2 3pbl_gps_P_3 3pbl_gps_P_4 3pbl_gps_P_5 3pbl_gps_P_6 3pbl_gps_P_7 3pbl_gps_P_8 3pbl_gps_P_9 3pbl_gps_P_10 
hide everything, 3pbl_poc_grids 
show spheres, 3pbl_poc_grids 
set sphere_scale, 0.1
group 3pbl_spoc_grids, 3pbl_gps_P_1_1 3pbl_gps_P_1_2 3pbl_gps_P_1_3 3pbl_gps_P_1_4 3pbl_gps_P_1_5 3pbl_gps_P_1_6 3pbl_gps_P_2_1 3pbl_gps_P_2_2 3pbl_gps_P_4_1 3pbl_gps_P_4_2 3pbl_gps_P_5_1 3pbl_gps_P_5_2 3pbl_gps_P_10_1 3pbl_gps_P_10_2 
hide everything, 3pbl_spoc_grids 
show spheres, 3pbl_spoc_grids 
show sticks, HETATM and 3pbl and not resn HOH
util.cbay("HETATM and 3pbl and not resn HOH")
hide everything, hydrogens
zoom 3pbl 

load ../pdb_cleaned/5dsg.pdb
hide everything, 5dsg 
show cartoon, 5dsg
util.cbc 5dsg
load 5dsg_gps_P_1.pdb
load 5dsg_gps_P_2.pdb
load 5dsg_gps_P_3.pdb
load 5dsg_gps_P_4.pdb
load 5dsg_gps_P_5.pdb
load 5dsg_gps_P_6.pdb
load 5dsg_gps_P_7.pdb
load 5dsg_gps_P_1_1.pdb
load 5dsg_gps_P_1_2.pdb
load 5dsg_gps_P_1_3.pdb
load 5dsg_gps_P_1_4.pdb
load 5dsg_gps_P_1_5.pdb
load 5dsg_gps_P_1_6.pdb
load 5dsg_gps_P_1_7.pdb
load 5dsg_gps_P_2_1.pdb
load 5dsg_gps_P_2_2.pdb
load 5dsg_gps_P_2_3.pdb
load 5dsg_gps_P_2_4.pdb
load 5dsg_gps_P_3_1.pdb
load 5dsg_gps_P_3_2.pdb
set sphere_scale, 0.1
group 5dsg_poc_grids, 5dsg_gps_P_1 5dsg_gps_P_2 5dsg_gps_P_3 5dsg_gps_P_4 5dsg_gps_P_5 5dsg_gps_P_6 5dsg_gps_P_7 
hide everything, 5dsg_poc_grids 
show spheres, 5dsg_poc_grids 
set sphere_scale, 0.1
group 5dsg_spoc_grids, 5dsg_gps_P_1_1 5dsg_gps_P_1_2 5dsg_gps_P_1_3 5dsg_gps_P_1_4 5dsg_gps_P_1_5 5dsg_gps_P_1_6 5dsg_gps_P_1_7 5dsg_gps_P_2_1 5dsg_gps_P_2_2 5dsg_gps_P_2_3 5dsg_gps_P_2_4 5dsg_gps_P_3_1 5dsg_gps_P_3_2 
hide everything, 5dsg_spoc_grids 
show spheres, 5dsg_spoc_grids 
show sticks, HETATM and 5dsg and not resn HOH
util.cbay("HETATM and 5dsg and not resn HOH")
hide everything, hydrogens
zoom 5dsg 

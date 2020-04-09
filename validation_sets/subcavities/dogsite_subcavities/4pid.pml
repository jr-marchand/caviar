load ../pdb_cleaned/4pid.pdb
hide everything, 4pid 
show cartoon, 4pid
util.cbc 4pid
load 4pid_gps_P_1.pdb
load 4pid_gps_P_2.pdb
load 4pid_gps_P_3.pdb
load 4pid_gps_P_4.pdb
load 4pid_gps_P_5.pdb
load 4pid_gps_P_6.pdb
load 4pid_gps_P_7.pdb
load 4pid_gps_P_8.pdb
load 4pid_gps_P_1_1.pdb
load 4pid_gps_P_1_2.pdb
load 4pid_gps_P_2_1.pdb
load 4pid_gps_P_2_2.pdb
load 4pid_gps_P_3_1.pdb
load 4pid_gps_P_3_2.pdb
load 4pid_gps_P_6_1.pdb
load 4pid_gps_P_6_2.pdb
set sphere_scale, 0.1
group 4pid_poc_grids, 4pid_gps_P_1 4pid_gps_P_2 4pid_gps_P_3 4pid_gps_P_4 4pid_gps_P_5 4pid_gps_P_6 4pid_gps_P_7 4pid_gps_P_8 
hide everything, 4pid_poc_grids 
show spheres, 4pid_poc_grids 
set sphere_scale, 0.1
group 4pid_spoc_grids, 4pid_gps_P_1_1 4pid_gps_P_1_2 4pid_gps_P_2_1 4pid_gps_P_2_2 4pid_gps_P_3_1 4pid_gps_P_3_2 4pid_gps_P_6_1 4pid_gps_P_6_2 
hide everything, 4pid_spoc_grids 
show spheres, 4pid_spoc_grids 
show sticks, HETATM and 4pid and not resn HOH
util.cbay("HETATM and 4pid and not resn HOH")
hide everything, hydrogens
zoom 4pid 

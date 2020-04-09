load ../pdb_cleaned/6q9h.pdb
hide everything, 6q9h 
show cartoon, 6q9h
util.cbc 6q9h
load 6q9h_gps_P_1.pdb
load 6q9h_gps_P_2.pdb
load 6q9h_gps_P_3.pdb
load 6q9h_gps_P_1_1.pdb
load 6q9h_gps_P_1_2.pdb
load 6q9h_gps_P_1_3.pdb
load 6q9h_gps_P_2_1.pdb
load 6q9h_gps_P_2_2.pdb
set sphere_scale, 0.1
group 6q9h_poc_grids, 6q9h_gps_P_1 6q9h_gps_P_2 6q9h_gps_P_3 
hide everything, 6q9h_poc_grids 
show spheres, 6q9h_poc_grids 
set sphere_scale, 0.1
group 6q9h_spoc_grids, 6q9h_gps_P_1_1 6q9h_gps_P_1_2 6q9h_gps_P_1_3 6q9h_gps_P_2_1 6q9h_gps_P_2_2 
hide everything, 6q9h_spoc_grids 
show spheres, 6q9h_spoc_grids 
show sticks, HETATM and 6q9h and not resn HOH
util.cbay("HETATM and 6q9h and not resn HOH")
hide everything, hydrogens
zoom 6q9h 

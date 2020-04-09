load ../pdb_cleaned/3kee.pdb
hide everything, 3kee 
show cartoon, 3kee
util.cbc 3kee
load 3kee_gps_P_1.pdb
load 3kee_gps_P_2.pdb
load 3kee_gps_P_3.pdb
load 3kee_gps_P_4.pdb
load 3kee_gps_P_1_1.pdb
load 3kee_gps_P_1_2.pdb
set sphere_scale, 0.1
group 3kee_poc_grids, 3kee_gps_P_1 3kee_gps_P_2 3kee_gps_P_3 3kee_gps_P_4 
hide everything, 3kee_poc_grids 
show spheres, 3kee_poc_grids 
set sphere_scale, 0.1
group 3kee_spoc_grids, 3kee_gps_P_1_1 3kee_gps_P_1_2 
hide everything, 3kee_spoc_grids 
show spheres, 3kee_spoc_grids 
show sticks, HETATM and 3kee and not resn HOH
util.cbay("HETATM and 3kee and not resn HOH")
hide everything, hydrogens
zoom 3kee 

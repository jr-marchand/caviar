load ../pdb_cleaned/5b5p.pdb
hide everything, 5b5p 
show cartoon, 5b5p
util.cbc 5b5p
load 5b5p_gps_P_1.pdb
load 5b5p_gps_P_2.pdb
load 5b5p_gps_P_3.pdb
load 5b5p_gps_P_4.pdb
load 5b5p_gps_P_5.pdb
load 5b5p_gps_P_6.pdb
load 5b5p_gps_P_7.pdb
load 5b5p_gps_P_1_1.pdb
load 5b5p_gps_P_1_2.pdb
load 5b5p_gps_P_1_3.pdb
load 5b5p_gps_P_4_1.pdb
load 5b5p_gps_P_4_2.pdb
load 5b5p_gps_P_4_3.pdb
load 5b5p_gps_P_5_1.pdb
load 5b5p_gps_P_5_2.pdb
set sphere_scale, 0.1
group 5b5p_poc_grids, 5b5p_gps_P_1 5b5p_gps_P_2 5b5p_gps_P_3 5b5p_gps_P_4 5b5p_gps_P_5 5b5p_gps_P_6 5b5p_gps_P_7 
hide everything, 5b5p_poc_grids 
show spheres, 5b5p_poc_grids 
set sphere_scale, 0.1
group 5b5p_spoc_grids, 5b5p_gps_P_1_1 5b5p_gps_P_1_2 5b5p_gps_P_1_3 5b5p_gps_P_4_1 5b5p_gps_P_4_2 5b5p_gps_P_4_3 5b5p_gps_P_5_1 5b5p_gps_P_5_2 
hide everything, 5b5p_spoc_grids 
show spheres, 5b5p_spoc_grids 
show sticks, HETATM and 5b5p and not resn HOH
util.cbay("HETATM and 5b5p and not resn HOH")
hide everything, hydrogens
zoom 5b5p 

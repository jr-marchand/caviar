load ../pdb_cleaned/4g9l.pdb
hide everything, 4g9l 
show cartoon, 4g9l
util.cbc 4g9l
load 4g9l_gps_P_1.pdb
load 4g9l_gps_P_2.pdb
load 4g9l_gps_P_3.pdb
load 4g9l_gps_P_4.pdb
load 4g9l_gps_P_5.pdb
load 4g9l_gps_P_6.pdb
load 4g9l_gps_P_1_1.pdb
load 4g9l_gps_P_1_2.pdb
load 4g9l_gps_P_1_3.pdb
load 4g9l_gps_P_1_4.pdb
load 4g9l_gps_P_1_5.pdb
load 4g9l_gps_P_2_1.pdb
load 4g9l_gps_P_2_2.pdb
load 4g9l_gps_P_2_3.pdb
load 4g9l_gps_P_3_1.pdb
load 4g9l_gps_P_3_2.pdb
set sphere_scale, 0.1
group 4g9l_poc_grids, 4g9l_gps_P_1 4g9l_gps_P_2 4g9l_gps_P_3 4g9l_gps_P_4 4g9l_gps_P_5 4g9l_gps_P_6 
hide everything, 4g9l_poc_grids 
show spheres, 4g9l_poc_grids 
set sphere_scale, 0.1
group 4g9l_spoc_grids, 4g9l_gps_P_1_1 4g9l_gps_P_1_2 4g9l_gps_P_1_3 4g9l_gps_P_1_4 4g9l_gps_P_1_5 4g9l_gps_P_2_1 4g9l_gps_P_2_2 4g9l_gps_P_2_3 4g9l_gps_P_3_1 4g9l_gps_P_3_2 
hide everything, 4g9l_spoc_grids 
show spheres, 4g9l_spoc_grids 
show sticks, HETATM and 4g9l and not resn HOH
util.cbay("HETATM and 4g9l and not resn HOH")
hide everything, hydrogens
zoom 4g9l 

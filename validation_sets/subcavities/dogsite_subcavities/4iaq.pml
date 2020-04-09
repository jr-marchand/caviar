load ../pdb_cleaned/4iaq.pdb
hide everything, 4iaq 
show cartoon, 4iaq
util.cbc 4iaq
load 4iaq_gps_P_1.pdb
load 4iaq_gps_P_2.pdb
load 4iaq_gps_P_3.pdb
load 4iaq_gps_P_4.pdb
load 4iaq_gps_P_5.pdb
load 4iaq_gps_P_6.pdb
load 4iaq_gps_P_7.pdb
load 4iaq_gps_P_8.pdb
load 4iaq_gps_P_9.pdb
load 4iaq_gps_P_10.pdb
load 4iaq_gps_P_1_1.pdb
load 4iaq_gps_P_1_2.pdb
load 4iaq_gps_P_1_3.pdb
load 4iaq_gps_P_1_4.pdb
load 4iaq_gps_P_2_1.pdb
load 4iaq_gps_P_2_2.pdb
load 4iaq_gps_P_2_3.pdb
load 4iaq_gps_P_2_4.pdb
load 4iaq_gps_P_5_1.pdb
load 4iaq_gps_P_5_2.pdb
set sphere_scale, 0.1
group 4iaq_poc_grids, 4iaq_gps_P_1 4iaq_gps_P_2 4iaq_gps_P_3 4iaq_gps_P_4 4iaq_gps_P_5 4iaq_gps_P_6 4iaq_gps_P_7 4iaq_gps_P_8 4iaq_gps_P_9 4iaq_gps_P_10 
hide everything, 4iaq_poc_grids 
show spheres, 4iaq_poc_grids 
set sphere_scale, 0.1
group 4iaq_spoc_grids, 4iaq_gps_P_1_1 4iaq_gps_P_1_2 4iaq_gps_P_1_3 4iaq_gps_P_1_4 4iaq_gps_P_2_1 4iaq_gps_P_2_2 4iaq_gps_P_2_3 4iaq_gps_P_2_4 4iaq_gps_P_5_1 4iaq_gps_P_5_2 
hide everything, 4iaq_spoc_grids 
show spheres, 4iaq_spoc_grids 
show sticks, HETATM and 4iaq and not resn HOH
util.cbay("HETATM and 4iaq and not resn HOH")
hide everything, hydrogens
zoom 4iaq 

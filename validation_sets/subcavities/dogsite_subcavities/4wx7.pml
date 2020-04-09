load ../pdb_cleaned/4wx7.pdb
hide everything, 4wx7 
show cartoon, 4wx7
util.cbc 4wx7
load 4wx7_gps_P_1.pdb
load 4wx7_gps_P_2.pdb
load 4wx7_gps_P_3.pdb
load 4wx7_gps_P_4.pdb
load 4wx7_gps_P_5.pdb
load 4wx7_gps_P_6.pdb
load 4wx7_gps_P_7.pdb
load 4wx7_gps_P_1_1.pdb
load 4wx7_gps_P_1_2.pdb
load 4wx7_gps_P_1_3.pdb
load 4wx7_gps_P_2_1.pdb
load 4wx7_gps_P_2_2.pdb
load 4wx7_gps_P_4_1.pdb
load 4wx7_gps_P_4_2.pdb
set sphere_scale, 0.1
group 4wx7_poc_grids, 4wx7_gps_P_1 4wx7_gps_P_2 4wx7_gps_P_3 4wx7_gps_P_4 4wx7_gps_P_5 4wx7_gps_P_6 4wx7_gps_P_7 
hide everything, 4wx7_poc_grids 
show spheres, 4wx7_poc_grids 
set sphere_scale, 0.1
group 4wx7_spoc_grids, 4wx7_gps_P_1_1 4wx7_gps_P_1_2 4wx7_gps_P_1_3 4wx7_gps_P_2_1 4wx7_gps_P_2_2 4wx7_gps_P_4_1 4wx7_gps_P_4_2 
hide everything, 4wx7_spoc_grids 
show spheres, 4wx7_spoc_grids 
show sticks, HETATM and 4wx7 and not resn HOH
util.cbay("HETATM and 4wx7 and not resn HOH")
hide everything, hydrogens
zoom 4wx7 

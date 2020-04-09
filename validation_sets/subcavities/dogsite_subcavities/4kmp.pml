load ../pdb_cleaned/4kmp.pdb
hide everything, 4kmp 
show cartoon, 4kmp
util.cbc 4kmp
load 4kmp_gps_P_1.pdb
load 4kmp_gps_P_2.pdb
load 4kmp_gps_P_3.pdb
load 4kmp_gps_P_4.pdb
load 4kmp_gps_P_5.pdb
load 4kmp_gps_P_1_1.pdb
load 4kmp_gps_P_1_2.pdb
load 4kmp_gps_P_1_3.pdb
load 4kmp_gps_P_1_4.pdb
load 4kmp_gps_P_1_5.pdb
load 4kmp_gps_P_4_1.pdb
load 4kmp_gps_P_4_2.pdb
set sphere_scale, 0.1
group 4kmp_poc_grids, 4kmp_gps_P_1 4kmp_gps_P_2 4kmp_gps_P_3 4kmp_gps_P_4 4kmp_gps_P_5 
hide everything, 4kmp_poc_grids 
show spheres, 4kmp_poc_grids 
set sphere_scale, 0.1
group 4kmp_spoc_grids, 4kmp_gps_P_1_1 4kmp_gps_P_1_2 4kmp_gps_P_1_3 4kmp_gps_P_1_4 4kmp_gps_P_1_5 4kmp_gps_P_4_1 4kmp_gps_P_4_2 
hide everything, 4kmp_spoc_grids 
show spheres, 4kmp_spoc_grids 
show sticks, HETATM and 4kmp and not resn HOH
util.cbay("HETATM and 4kmp and not resn HOH")
hide everything, hydrogens
zoom 4kmp 

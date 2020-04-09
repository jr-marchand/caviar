load ../pdb_cleaned/6cm4.pdb
hide everything, 6cm4 
show cartoon, 6cm4
util.cbc 6cm4
load 6cm4_gps_P_1.pdb
load 6cm4_gps_P_2.pdb
load 6cm4_gps_P_3.pdb
load 6cm4_gps_P_4.pdb
load 6cm4_gps_P_5.pdb
load 6cm4_gps_P_6.pdb
load 6cm4_gps_P_7.pdb
load 6cm4_gps_P_8.pdb
load 6cm4_gps_P_9.pdb
load 6cm4_gps_P_1_1.pdb
load 6cm4_gps_P_1_2.pdb
load 6cm4_gps_P_1_3.pdb
load 6cm4_gps_P_1_4.pdb
load 6cm4_gps_P_1_5.pdb
load 6cm4_gps_P_1_6.pdb
load 6cm4_gps_P_3_1.pdb
load 6cm4_gps_P_3_2.pdb
set sphere_scale, 0.1
group 6cm4_poc_grids, 6cm4_gps_P_1 6cm4_gps_P_2 6cm4_gps_P_3 6cm4_gps_P_4 6cm4_gps_P_5 6cm4_gps_P_6 6cm4_gps_P_7 6cm4_gps_P_8 6cm4_gps_P_9 
hide everything, 6cm4_poc_grids 
show spheres, 6cm4_poc_grids 
set sphere_scale, 0.1
group 6cm4_spoc_grids, 6cm4_gps_P_1_1 6cm4_gps_P_1_2 6cm4_gps_P_1_3 6cm4_gps_P_1_4 6cm4_gps_P_1_5 6cm4_gps_P_1_6 6cm4_gps_P_3_1 6cm4_gps_P_3_2 
hide everything, 6cm4_spoc_grids 
show spheres, 6cm4_spoc_grids 
show sticks, HETATM and 6cm4 and not resn HOH
util.cbay("HETATM and 6cm4 and not resn HOH")
hide everything, hydrogens
zoom 6cm4 

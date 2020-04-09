load ../pdb_cleaned/6tz7.pdb
hide everything, 6tz7 
show cartoon, 6tz7
util.cbc 6tz7
load 6tz7_gps_P_1.pdb
load 6tz7_gps_P_2.pdb
load 6tz7_gps_P_3.pdb
load 6tz7_gps_P_4.pdb
load 6tz7_gps_P_5.pdb
load 6tz7_gps_P_6.pdb
load 6tz7_gps_P_7.pdb
load 6tz7_gps_P_8.pdb
load 6tz7_gps_P_9.pdb
load 6tz7_gps_P_10.pdb
load 6tz7_gps_P_11.pdb
load 6tz7_gps_P_12.pdb
load 6tz7_gps_P_13.pdb
load 6tz7_gps_P_14.pdb
load 6tz7_gps_P_15.pdb
load 6tz7_gps_P_16.pdb
load 6tz7_gps_P_1_1.pdb
load 6tz7_gps_P_1_2.pdb
load 6tz7_gps_P_2_1.pdb
load 6tz7_gps_P_2_2.pdb
load 6tz7_gps_P_2_3.pdb
load 6tz7_gps_P_3_1.pdb
load 6tz7_gps_P_3_2.pdb
load 6tz7_gps_P_4_1.pdb
load 6tz7_gps_P_4_2.pdb
load 6tz7_gps_P_5_1.pdb
load 6tz7_gps_P_5_2.pdb
load 6tz7_gps_P_11_1.pdb
load 6tz7_gps_P_11_2.pdb
load 6tz7_gps_P_14_1.pdb
load 6tz7_gps_P_14_2.pdb
set sphere_scale, 0.1
group 6tz7_poc_grids, 6tz7_gps_P_1 6tz7_gps_P_2 6tz7_gps_P_3 6tz7_gps_P_4 6tz7_gps_P_5 6tz7_gps_P_6 6tz7_gps_P_7 6tz7_gps_P_8 6tz7_gps_P_9 6tz7_gps_P_10 6tz7_gps_P_11 6tz7_gps_P_12 6tz7_gps_P_13 6tz7_gps_P_14 6tz7_gps_P_15 6tz7_gps_P_16 
hide everything, 6tz7_poc_grids 
show spheres, 6tz7_poc_grids 
set sphere_scale, 0.1
group 6tz7_spoc_grids, 6tz7_gps_P_1_1 6tz7_gps_P_1_2 6tz7_gps_P_2_1 6tz7_gps_P_2_2 6tz7_gps_P_2_3 6tz7_gps_P_3_1 6tz7_gps_P_3_2 6tz7_gps_P_4_1 6tz7_gps_P_4_2 6tz7_gps_P_5_1 6tz7_gps_P_5_2 6tz7_gps_P_11_1 6tz7_gps_P_11_2 6tz7_gps_P_14_1 6tz7_gps_P_14_2 
hide everything, 6tz7_spoc_grids 
show spheres, 6tz7_spoc_grids 
show sticks, HETATM and 6tz7 and not resn HOH
util.cbay("HETATM and 6tz7 and not resn HOH")
hide everything, hydrogens
zoom 6tz7 

load ../pdb_cleaned/3pmz.pdb
hide everything, 3pmz 
show cartoon, 3pmz
util.cbc 3pmz
load 3pmz_gps_P_1.pdb
load 3pmz_gps_P_2.pdb
load 3pmz_gps_P_3.pdb
load 3pmz_gps_P_4.pdb
load 3pmz_gps_P_5.pdb
load 3pmz_gps_P_6.pdb
load 3pmz_gps_P_7.pdb
load 3pmz_gps_P_8.pdb
load 3pmz_gps_P_9.pdb
load 3pmz_gps_P_10.pdb
load 3pmz_gps_P_11.pdb
load 3pmz_gps_P_12.pdb
load 3pmz_gps_P_13.pdb
load 3pmz_gps_P_14.pdb
load 3pmz_gps_P_15.pdb
load 3pmz_gps_P_1_1.pdb
load 3pmz_gps_P_1_2.pdb
load 3pmz_gps_P_1_3.pdb
load 3pmz_gps_P_1_4.pdb
load 3pmz_gps_P_1_5.pdb
load 3pmz_gps_P_2_1.pdb
load 3pmz_gps_P_2_2.pdb
load 3pmz_gps_P_2_3.pdb
load 3pmz_gps_P_2_4.pdb
load 3pmz_gps_P_3_1.pdb
load 3pmz_gps_P_3_2.pdb
load 3pmz_gps_P_3_3.pdb
load 3pmz_gps_P_3_4.pdb
load 3pmz_gps_P_6_1.pdb
load 3pmz_gps_P_6_2.pdb
load 3pmz_gps_P_7_1.pdb
load 3pmz_gps_P_7_2.pdb
load 3pmz_gps_P_7_3.pdb
load 3pmz_gps_P_8_1.pdb
load 3pmz_gps_P_8_2.pdb
load 3pmz_gps_P_11_1.pdb
load 3pmz_gps_P_11_2.pdb
load 3pmz_gps_P_12_1.pdb
load 3pmz_gps_P_12_2.pdb
load 3pmz_gps_P_13_1.pdb
load 3pmz_gps_P_13_2.pdb
set sphere_scale, 0.1
group 3pmz_poc_grids, 3pmz_gps_P_1 3pmz_gps_P_2 3pmz_gps_P_3 3pmz_gps_P_4 3pmz_gps_P_5 3pmz_gps_P_6 3pmz_gps_P_7 3pmz_gps_P_8 3pmz_gps_P_9 3pmz_gps_P_10 3pmz_gps_P_11 3pmz_gps_P_12 3pmz_gps_P_13 3pmz_gps_P_14 3pmz_gps_P_15 
hide everything, 3pmz_poc_grids 
show spheres, 3pmz_poc_grids 
set sphere_scale, 0.1
group 3pmz_spoc_grids, 3pmz_gps_P_1_1 3pmz_gps_P_1_2 3pmz_gps_P_1_3 3pmz_gps_P_1_4 3pmz_gps_P_1_5 3pmz_gps_P_2_1 3pmz_gps_P_2_2 3pmz_gps_P_2_3 3pmz_gps_P_2_4 3pmz_gps_P_3_1 3pmz_gps_P_3_2 3pmz_gps_P_3_3 3pmz_gps_P_3_4 3pmz_gps_P_6_1 3pmz_gps_P_6_2 3pmz_gps_P_7_1 3pmz_gps_P_7_2 3pmz_gps_P_7_3 3pmz_gps_P_8_1 3pmz_gps_P_8_2 3pmz_gps_P_11_1 3pmz_gps_P_11_2 3pmz_gps_P_12_1 3pmz_gps_P_12_2 3pmz_gps_P_13_1 3pmz_gps_P_13_2 
hide everything, 3pmz_spoc_grids 
show spheres, 3pmz_spoc_grids 
show sticks, HETATM and 3pmz and not resn HOH
util.cbay("HETATM and 3pmz and not resn HOH")
hide everything, hydrogens
zoom 3pmz 

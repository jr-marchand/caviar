load ../pdb_cleaned/4mkc.pdb
hide everything, 4mkc 
show cartoon, 4mkc
util.cbc 4mkc
load 4mkc_gps_P_1.pdb
load 4mkc_gps_P_2.pdb
load 4mkc_gps_P_3.pdb
load 4mkc_gps_P_4.pdb
load 4mkc_gps_P_5.pdb
load 4mkc_gps_P_6.pdb
load 4mkc_gps_P_7.pdb
load 4mkc_gps_P_8.pdb
load 4mkc_gps_P_9.pdb
load 4mkc_gps_P_10.pdb
load 4mkc_gps_P_11.pdb
load 4mkc_gps_P_1_1.pdb
load 4mkc_gps_P_1_2.pdb
load 4mkc_gps_P_1_3.pdb
load 4mkc_gps_P_1_4.pdb
load 4mkc_gps_P_1_5.pdb
load 4mkc_gps_P_1_6.pdb
load 4mkc_gps_P_2_1.pdb
load 4mkc_gps_P_2_2.pdb
load 4mkc_gps_P_2_3.pdb
load 4mkc_gps_P_2_4.pdb
load 4mkc_gps_P_3_1.pdb
load 4mkc_gps_P_3_2.pdb
load 4mkc_gps_P_3_3.pdb
load 4mkc_gps_P_5_1.pdb
load 4mkc_gps_P_5_2.pdb
load 4mkc_gps_P_6_1.pdb
load 4mkc_gps_P_6_2.pdb
load 4mkc_gps_P_11_1.pdb
load 4mkc_gps_P_11_2.pdb
set sphere_scale, 0.1
group 4mkc_poc_grids, 4mkc_gps_P_1 4mkc_gps_P_2 4mkc_gps_P_3 4mkc_gps_P_4 4mkc_gps_P_5 4mkc_gps_P_6 4mkc_gps_P_7 4mkc_gps_P_8 4mkc_gps_P_9 4mkc_gps_P_10 4mkc_gps_P_11 
hide everything, 4mkc_poc_grids 
show spheres, 4mkc_poc_grids 
set sphere_scale, 0.1
group 4mkc_spoc_grids, 4mkc_gps_P_1_1 4mkc_gps_P_1_2 4mkc_gps_P_1_3 4mkc_gps_P_1_4 4mkc_gps_P_1_5 4mkc_gps_P_1_6 4mkc_gps_P_2_1 4mkc_gps_P_2_2 4mkc_gps_P_2_3 4mkc_gps_P_2_4 4mkc_gps_P_3_1 4mkc_gps_P_3_2 4mkc_gps_P_3_3 4mkc_gps_P_5_1 4mkc_gps_P_5_2 4mkc_gps_P_6_1 4mkc_gps_P_6_2 4mkc_gps_P_11_1 4mkc_gps_P_11_2 
hide everything, 4mkc_spoc_grids 
show spheres, 4mkc_spoc_grids 
show sticks, HETATM and 4mkc and not resn HOH
util.cbay("HETATM and 4mkc and not resn HOH")
hide everything, hydrogens
zoom 4mkc 

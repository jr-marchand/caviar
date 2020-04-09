load ../pdb_cleaned/1hwk.pdb
hide everything, 1hwk 
show cartoon, 1hwk
util.cbc 1hwk
load 1hwk_gps_P_1.pdb
load 1hwk_gps_P_2.pdb
load 1hwk_gps_P_3.pdb
load 1hwk_gps_P_4.pdb
load 1hwk_gps_P_5.pdb
load 1hwk_gps_P_6.pdb
load 1hwk_gps_P_7.pdb
load 1hwk_gps_P_8.pdb
load 1hwk_gps_P_9.pdb
load 1hwk_gps_P_10.pdb
load 1hwk_gps_P_11.pdb
load 1hwk_gps_P_12.pdb
load 1hwk_gps_P_13.pdb
load 1hwk_gps_P_14.pdb
load 1hwk_gps_P_15.pdb
load 1hwk_gps_P_16.pdb
load 1hwk_gps_P_17.pdb
load 1hwk_gps_P_18.pdb
load 1hwk_gps_P_19.pdb
load 1hwk_gps_P_20.pdb
load 1hwk_gps_P_21.pdb
load 1hwk_gps_P_22.pdb
load 1hwk_gps_P_1_1.pdb
load 1hwk_gps_P_1_2.pdb
load 1hwk_gps_P_1_3.pdb
load 1hwk_gps_P_1_4.pdb
load 1hwk_gps_P_2_1.pdb
load 1hwk_gps_P_2_2.pdb
load 1hwk_gps_P_2_3.pdb
load 1hwk_gps_P_3_1.pdb
load 1hwk_gps_P_3_2.pdb
load 1hwk_gps_P_4_1.pdb
load 1hwk_gps_P_4_2.pdb
load 1hwk_gps_P_5_1.pdb
load 1hwk_gps_P_5_2.pdb
load 1hwk_gps_P_6_1.pdb
load 1hwk_gps_P_6_2.pdb
load 1hwk_gps_P_6_3.pdb
load 1hwk_gps_P_11_1.pdb
load 1hwk_gps_P_11_2.pdb
load 1hwk_gps_P_12_1.pdb
load 1hwk_gps_P_12_2.pdb
set sphere_scale, 0.1
group 1hwk_poc_grids, 1hwk_gps_P_1 1hwk_gps_P_2 1hwk_gps_P_3 1hwk_gps_P_4 1hwk_gps_P_5 1hwk_gps_P_6 1hwk_gps_P_7 1hwk_gps_P_8 1hwk_gps_P_9 1hwk_gps_P_10 1hwk_gps_P_11 1hwk_gps_P_12 1hwk_gps_P_13 1hwk_gps_P_14 1hwk_gps_P_15 1hwk_gps_P_16 1hwk_gps_P_17 1hwk_gps_P_18 1hwk_gps_P_19 1hwk_gps_P_20 1hwk_gps_P_21 1hwk_gps_P_22 
hide everything, 1hwk_poc_grids 
show spheres, 1hwk_poc_grids 
set sphere_scale, 0.1
group 1hwk_spoc_grids, 1hwk_gps_P_1_1 1hwk_gps_P_1_2 1hwk_gps_P_1_3 1hwk_gps_P_1_4 1hwk_gps_P_2_1 1hwk_gps_P_2_2 1hwk_gps_P_2_3 1hwk_gps_P_3_1 1hwk_gps_P_3_2 1hwk_gps_P_4_1 1hwk_gps_P_4_2 1hwk_gps_P_5_1 1hwk_gps_P_5_2 1hwk_gps_P_6_1 1hwk_gps_P_6_2 1hwk_gps_P_6_3 1hwk_gps_P_11_1 1hwk_gps_P_11_2 1hwk_gps_P_12_1 1hwk_gps_P_12_2 
hide everything, 1hwk_spoc_grids 
show spheres, 1hwk_spoc_grids 
show sticks, HETATM and 1hwk and not resn HOH
util.cbay("HETATM and 1hwk and not resn HOH")
hide everything, hydrogens
zoom 1hwk 

load ../pdb_cleaned/1jff.pdb
hide everything, 1jff 
show cartoon, 1jff
util.cbc 1jff
load 1jff_gps_P_1.pdb
load 1jff_gps_P_2.pdb
load 1jff_gps_P_3.pdb
load 1jff_gps_P_4.pdb
load 1jff_gps_P_5.pdb
load 1jff_gps_P_6.pdb
load 1jff_gps_P_7.pdb
load 1jff_gps_P_8.pdb
load 1jff_gps_P_9.pdb
load 1jff_gps_P_10.pdb
load 1jff_gps_P_11.pdb
load 1jff_gps_P_12.pdb
load 1jff_gps_P_13.pdb
load 1jff_gps_P_14.pdb
load 1jff_gps_P_15.pdb
load 1jff_gps_P_16.pdb
load 1jff_gps_P_17.pdb
load 1jff_gps_P_18.pdb
load 1jff_gps_P_19.pdb
load 1jff_gps_P_1_1.pdb
load 1jff_gps_P_1_2.pdb
load 1jff_gps_P_1_3.pdb
load 1jff_gps_P_2_1.pdb
load 1jff_gps_P_2_2.pdb
load 1jff_gps_P_2_3.pdb
load 1jff_gps_P_2_4.pdb
load 1jff_gps_P_2_5.pdb
load 1jff_gps_P_3_1.pdb
load 1jff_gps_P_3_2.pdb
load 1jff_gps_P_3_3.pdb
load 1jff_gps_P_5_1.pdb
load 1jff_gps_P_5_2.pdb
load 1jff_gps_P_9_1.pdb
load 1jff_gps_P_9_2.pdb
load 1jff_gps_P_10_1.pdb
load 1jff_gps_P_10_2.pdb
load 1jff_gps_P_11_1.pdb
load 1jff_gps_P_11_2.pdb
load 1jff_gps_P_13_1.pdb
load 1jff_gps_P_13_2.pdb
set sphere_scale, 0.1
group 1jff_poc_grids, 1jff_gps_P_1 1jff_gps_P_2 1jff_gps_P_3 1jff_gps_P_4 1jff_gps_P_5 1jff_gps_P_6 1jff_gps_P_7 1jff_gps_P_8 1jff_gps_P_9 1jff_gps_P_10 1jff_gps_P_11 1jff_gps_P_12 1jff_gps_P_13 1jff_gps_P_14 1jff_gps_P_15 1jff_gps_P_16 1jff_gps_P_17 1jff_gps_P_18 1jff_gps_P_19 
hide everything, 1jff_poc_grids 
show spheres, 1jff_poc_grids 
set sphere_scale, 0.1
group 1jff_spoc_grids, 1jff_gps_P_1_1 1jff_gps_P_1_2 1jff_gps_P_1_3 1jff_gps_P_2_1 1jff_gps_P_2_2 1jff_gps_P_2_3 1jff_gps_P_2_4 1jff_gps_P_2_5 1jff_gps_P_3_1 1jff_gps_P_3_2 1jff_gps_P_3_3 1jff_gps_P_5_1 1jff_gps_P_5_2 1jff_gps_P_9_1 1jff_gps_P_9_2 1jff_gps_P_10_1 1jff_gps_P_10_2 1jff_gps_P_11_1 1jff_gps_P_11_2 1jff_gps_P_13_1 1jff_gps_P_13_2 
hide everything, 1jff_spoc_grids 
show spheres, 1jff_spoc_grids 
show sticks, HETATM and 1jff and not resn HOH
util.cbay("HETATM and 1jff and not resn HOH")
hide everything, hydrogens
zoom 1jff 

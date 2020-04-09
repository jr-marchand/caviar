load ../pdb_cleaned/5y7k.pdb
hide everything, 5y7k 
show cartoon, 5y7k
util.cbc 5y7k
load 5y7k_gps_P_1.pdb
load 5y7k_gps_P_2.pdb
load 5y7k_gps_P_3.pdb
load 5y7k_gps_P_4.pdb
load 5y7k_gps_P_5.pdb
load 5y7k_gps_P_6.pdb
load 5y7k_gps_P_7.pdb
load 5y7k_gps_P_8.pdb
load 5y7k_gps_P_9.pdb
load 5y7k_gps_P_10.pdb
load 5y7k_gps_P_11.pdb
load 5y7k_gps_P_12.pdb
load 5y7k_gps_P_13.pdb
load 5y7k_gps_P_14.pdb
load 5y7k_gps_P_15.pdb
load 5y7k_gps_P_16.pdb
load 5y7k_gps_P_17.pdb
load 5y7k_gps_P_18.pdb
load 5y7k_gps_P_19.pdb
load 5y7k_gps_P_20.pdb
load 5y7k_gps_P_21.pdb
load 5y7k_gps_P_22.pdb
load 5y7k_gps_P_23.pdb
load 5y7k_gps_P_24.pdb
load 5y7k_gps_P_25.pdb
load 5y7k_gps_P_26.pdb
load 5y7k_gps_P_27.pdb
load 5y7k_gps_P_28.pdb
load 5y7k_gps_P_29.pdb
load 5y7k_gps_P_1_1.pdb
load 5y7k_gps_P_1_2.pdb
load 5y7k_gps_P_1_3.pdb
load 5y7k_gps_P_2_1.pdb
load 5y7k_gps_P_2_2.pdb
load 5y7k_gps_P_2_3.pdb
load 5y7k_gps_P_3_1.pdb
load 5y7k_gps_P_3_2.pdb
load 5y7k_gps_P_4_1.pdb
load 5y7k_gps_P_4_2.pdb
load 5y7k_gps_P_5_1.pdb
load 5y7k_gps_P_5_2.pdb
load 5y7k_gps_P_5_3.pdb
load 5y7k_gps_P_6_1.pdb
load 5y7k_gps_P_6_2.pdb
load 5y7k_gps_P_6_3.pdb
load 5y7k_gps_P_11_1.pdb
load 5y7k_gps_P_11_2.pdb
set sphere_scale, 0.1
group 5y7k_poc_grids, 5y7k_gps_P_1 5y7k_gps_P_2 5y7k_gps_P_3 5y7k_gps_P_4 5y7k_gps_P_5 5y7k_gps_P_6 5y7k_gps_P_7 5y7k_gps_P_8 5y7k_gps_P_9 5y7k_gps_P_10 5y7k_gps_P_11 5y7k_gps_P_12 5y7k_gps_P_13 5y7k_gps_P_14 5y7k_gps_P_15 5y7k_gps_P_16 5y7k_gps_P_17 5y7k_gps_P_18 5y7k_gps_P_19 5y7k_gps_P_20 5y7k_gps_P_21 5y7k_gps_P_22 5y7k_gps_P_23 5y7k_gps_P_24 5y7k_gps_P_25 5y7k_gps_P_26 5y7k_gps_P_27 5y7k_gps_P_28 5y7k_gps_P_29 
hide everything, 5y7k_poc_grids 
show spheres, 5y7k_poc_grids 
set sphere_scale, 0.1
group 5y7k_spoc_grids, 5y7k_gps_P_1_1 5y7k_gps_P_1_2 5y7k_gps_P_1_3 5y7k_gps_P_2_1 5y7k_gps_P_2_2 5y7k_gps_P_2_3 5y7k_gps_P_3_1 5y7k_gps_P_3_2 5y7k_gps_P_4_1 5y7k_gps_P_4_2 5y7k_gps_P_5_1 5y7k_gps_P_5_2 5y7k_gps_P_5_3 5y7k_gps_P_6_1 5y7k_gps_P_6_2 5y7k_gps_P_6_3 5y7k_gps_P_11_1 5y7k_gps_P_11_2 
hide everything, 5y7k_spoc_grids 
show spheres, 5y7k_spoc_grids 
show sticks, HETATM and 5y7k and not resn HOH
util.cbay("HETATM and 5y7k and not resn HOH")
hide everything, hydrogens
zoom 5y7k 

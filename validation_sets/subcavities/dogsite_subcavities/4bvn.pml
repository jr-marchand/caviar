load ../pdb_cleaned/4bvn.pdb
hide everything, 4bvn 
show cartoon, 4bvn
util.cbc 4bvn
load 4bvn_gps_P_1.pdb
load 4bvn_gps_P_2.pdb
load 4bvn_gps_P_3.pdb
load 4bvn_gps_P_4.pdb
load 4bvn_gps_P_5.pdb
load 4bvn_gps_P_6.pdb
load 4bvn_gps_P_7.pdb
load 4bvn_gps_P_1_1.pdb
load 4bvn_gps_P_1_2.pdb
load 4bvn_gps_P_1_3.pdb
load 4bvn_gps_P_2_1.pdb
load 4bvn_gps_P_2_2.pdb
load 4bvn_gps_P_2_3.pdb
load 4bvn_gps_P_2_4.pdb
load 4bvn_gps_P_2_5.pdb
load 4bvn_gps_P_3_1.pdb
load 4bvn_gps_P_3_2.pdb
load 4bvn_gps_P_3_3.pdb
load 4bvn_gps_P_3_4.pdb
set sphere_scale, 0.1
group 4bvn_poc_grids, 4bvn_gps_P_1 4bvn_gps_P_2 4bvn_gps_P_3 4bvn_gps_P_4 4bvn_gps_P_5 4bvn_gps_P_6 4bvn_gps_P_7 
hide everything, 4bvn_poc_grids 
show spheres, 4bvn_poc_grids 
set sphere_scale, 0.1
group 4bvn_spoc_grids, 4bvn_gps_P_1_1 4bvn_gps_P_1_2 4bvn_gps_P_1_3 4bvn_gps_P_2_1 4bvn_gps_P_2_2 4bvn_gps_P_2_3 4bvn_gps_P_2_4 4bvn_gps_P_2_5 4bvn_gps_P_3_1 4bvn_gps_P_3_2 4bvn_gps_P_3_3 4bvn_gps_P_3_4 
hide everything, 4bvn_spoc_grids 
show spheres, 4bvn_spoc_grids 
show sticks, HETATM and 4bvn and not resn HOH
util.cbay("HETATM and 4bvn and not resn HOH")
hide everything, hydrogens
zoom 4bvn 

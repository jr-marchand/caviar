load ../pdb_cleaned/4gid.pdb
hide everything, 4gid 
show cartoon, 4gid
util.cbc 4gid
load 4gid_gps_P_1.pdb
load 4gid_gps_P_2.pdb
load 4gid_gps_P_3.pdb
load 4gid_gps_P_4.pdb
load 4gid_gps_P_5.pdb
load 4gid_gps_P_6.pdb
load 4gid_gps_P_7.pdb
load 4gid_gps_P_8.pdb
load 4gid_gps_P_9.pdb
load 4gid_gps_P_10.pdb
load 4gid_gps_P_11.pdb
load 4gid_gps_P_12.pdb
load 4gid_gps_P_13.pdb
load 4gid_gps_P_1_1.pdb
load 4gid_gps_P_1_2.pdb
load 4gid_gps_P_1_3.pdb
load 4gid_gps_P_1_4.pdb
load 4gid_gps_P_3_1.pdb
load 4gid_gps_P_3_2.pdb
load 4gid_gps_P_4_1.pdb
load 4gid_gps_P_4_2.pdb
load 4gid_gps_P_4_3.pdb
load 4gid_gps_P_5_1.pdb
load 4gid_gps_P_5_2.pdb
load 4gid_gps_P_7_1.pdb
load 4gid_gps_P_7_2.pdb
set sphere_scale, 0.1
group 4gid_poc_grids, 4gid_gps_P_1 4gid_gps_P_2 4gid_gps_P_3 4gid_gps_P_4 4gid_gps_P_5 4gid_gps_P_6 4gid_gps_P_7 4gid_gps_P_8 4gid_gps_P_9 4gid_gps_P_10 4gid_gps_P_11 4gid_gps_P_12 4gid_gps_P_13 
hide everything, 4gid_poc_grids 
show spheres, 4gid_poc_grids 
set sphere_scale, 0.1
group 4gid_spoc_grids, 4gid_gps_P_1_1 4gid_gps_P_1_2 4gid_gps_P_1_3 4gid_gps_P_1_4 4gid_gps_P_3_1 4gid_gps_P_3_2 4gid_gps_P_4_1 4gid_gps_P_4_2 4gid_gps_P_4_3 4gid_gps_P_5_1 4gid_gps_P_5_2 4gid_gps_P_7_1 4gid_gps_P_7_2 
hide everything, 4gid_spoc_grids 
show spheres, 4gid_spoc_grids 
show sticks, HETATM and 4gid and not resn HOH
util.cbay("HETATM and 4gid and not resn HOH")
hide everything, hydrogens
zoom 4gid 

load ../pdb_cleaned/5cxv.pdb
hide everything, 5cxv 
show cartoon, 5cxv
util.cbc 5cxv
load 5cxv_gps_P_1.pdb
load 5cxv_gps_P_2.pdb
load 5cxv_gps_P_3.pdb
load 5cxv_gps_P_4.pdb
load 5cxv_gps_P_5.pdb
load 5cxv_gps_P_6.pdb
load 5cxv_gps_P_7.pdb
load 5cxv_gps_P_8.pdb
load 5cxv_gps_P_1_1.pdb
load 5cxv_gps_P_1_2.pdb
load 5cxv_gps_P_1_3.pdb
load 5cxv_gps_P_1_4.pdb
load 5cxv_gps_P_2_1.pdb
load 5cxv_gps_P_2_2.pdb
load 5cxv_gps_P_2_3.pdb
load 5cxv_gps_P_2_4.pdb
set sphere_scale, 0.1
group 5cxv_poc_grids, 5cxv_gps_P_1 5cxv_gps_P_2 5cxv_gps_P_3 5cxv_gps_P_4 5cxv_gps_P_5 5cxv_gps_P_6 5cxv_gps_P_7 5cxv_gps_P_8 
hide everything, 5cxv_poc_grids 
show spheres, 5cxv_poc_grids 
set sphere_scale, 0.1
group 5cxv_spoc_grids, 5cxv_gps_P_1_1 5cxv_gps_P_1_2 5cxv_gps_P_1_3 5cxv_gps_P_1_4 5cxv_gps_P_2_1 5cxv_gps_P_2_2 5cxv_gps_P_2_3 5cxv_gps_P_2_4 
hide everything, 5cxv_spoc_grids 
show spheres, 5cxv_spoc_grids 
show sticks, HETATM and 5cxv and not resn HOH
util.cbay("HETATM and 5cxv and not resn HOH")
hide everything, hydrogens
zoom 5cxv 

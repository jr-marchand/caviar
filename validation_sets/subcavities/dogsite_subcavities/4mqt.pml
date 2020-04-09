load ../pdb_cleaned/4mqt.pdb
hide everything, 4mqt 
show cartoon, 4mqt
util.cbc 4mqt
load 4mqt_gps_P_1.pdb
load 4mqt_gps_P_2.pdb
load 4mqt_gps_P_3.pdb
load 4mqt_gps_P_4.pdb
load 4mqt_gps_P_5.pdb
load 4mqt_gps_P_6.pdb
load 4mqt_gps_P_7.pdb
load 4mqt_gps_P_8.pdb
load 4mqt_gps_P_9.pdb
load 4mqt_gps_P_1_1.pdb
load 4mqt_gps_P_1_2.pdb
load 4mqt_gps_P_4_1.pdb
load 4mqt_gps_P_4_2.pdb
set sphere_scale, 0.1
group 4mqt_poc_grids, 4mqt_gps_P_1 4mqt_gps_P_2 4mqt_gps_P_3 4mqt_gps_P_4 4mqt_gps_P_5 4mqt_gps_P_6 4mqt_gps_P_7 4mqt_gps_P_8 4mqt_gps_P_9 
hide everything, 4mqt_poc_grids 
show spheres, 4mqt_poc_grids 
set sphere_scale, 0.1
group 4mqt_spoc_grids, 4mqt_gps_P_1_1 4mqt_gps_P_1_2 4mqt_gps_P_4_1 4mqt_gps_P_4_2 
hide everything, 4mqt_spoc_grids 
show spheres, 4mqt_spoc_grids 
show sticks, HETATM and 4mqt and not resn HOH
util.cbay("HETATM and 4mqt and not resn HOH")
hide everything, hydrogens
zoom 4mqt 

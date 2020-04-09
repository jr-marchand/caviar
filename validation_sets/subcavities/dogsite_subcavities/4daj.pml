load ../pdb_cleaned/4daj.pdb
hide everything, 4daj 
show cartoon, 4daj
util.cbc 4daj
load 4daj_gps_P_1.pdb
load 4daj_gps_P_2.pdb
load 4daj_gps_P_3.pdb
load 4daj_gps_P_4.pdb
load 4daj_gps_P_5.pdb
load 4daj_gps_P_6.pdb
load 4daj_gps_P_7.pdb
load 4daj_gps_P_8.pdb
load 4daj_gps_P_9.pdb
load 4daj_gps_P_10.pdb
load 4daj_gps_P_1_1.pdb
load 4daj_gps_P_1_2.pdb
load 4daj_gps_P_1_3.pdb
load 4daj_gps_P_1_4.pdb
load 4daj_gps_P_1_5.pdb
load 4daj_gps_P_1_6.pdb
load 4daj_gps_P_1_7.pdb
load 4daj_gps_P_2_1.pdb
load 4daj_gps_P_2_2.pdb
load 4daj_gps_P_2_3.pdb
load 4daj_gps_P_2_4.pdb
load 4daj_gps_P_2_5.pdb
load 4daj_gps_P_3_1.pdb
load 4daj_gps_P_3_2.pdb
load 4daj_gps_P_3_3.pdb
set sphere_scale, 0.1
group 4daj_poc_grids, 4daj_gps_P_1 4daj_gps_P_2 4daj_gps_P_3 4daj_gps_P_4 4daj_gps_P_5 4daj_gps_P_6 4daj_gps_P_7 4daj_gps_P_8 4daj_gps_P_9 4daj_gps_P_10 
hide everything, 4daj_poc_grids 
show spheres, 4daj_poc_grids 
set sphere_scale, 0.1
group 4daj_spoc_grids, 4daj_gps_P_1_1 4daj_gps_P_1_2 4daj_gps_P_1_3 4daj_gps_P_1_4 4daj_gps_P_1_5 4daj_gps_P_1_6 4daj_gps_P_1_7 4daj_gps_P_2_1 4daj_gps_P_2_2 4daj_gps_P_2_3 4daj_gps_P_2_4 4daj_gps_P_2_5 4daj_gps_P_3_1 4daj_gps_P_3_2 4daj_gps_P_3_3 
hide everything, 4daj_spoc_grids 
show spheres, 4daj_spoc_grids 
show sticks, HETATM and 4daj and not resn HOH
util.cbay("HETATM and 4daj and not resn HOH")
hide everything, hydrogens
zoom 4daj 

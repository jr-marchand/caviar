load ../pdb_cleaned/1ppi.pdb
hide everything, 1ppi 
show cartoon, 1ppi
util.cbc 1ppi
load 1ppi_gps_P_1.pdb
load 1ppi_gps_P_2.pdb
load 1ppi_gps_P_3.pdb
load 1ppi_gps_P_4.pdb
load 1ppi_gps_P_5.pdb
load 1ppi_gps_P_6.pdb
load 1ppi_gps_P_7.pdb
load 1ppi_gps_P_8.pdb
load 1ppi_gps_P_9.pdb
load 1ppi_gps_P_10.pdb
load 1ppi_gps_P_11.pdb
load 1ppi_gps_P_12.pdb
load 1ppi_gps_P_13.pdb
load 1ppi_gps_P_14.pdb
load 1ppi_gps_P_1_1.pdb
load 1ppi_gps_P_1_2.pdb
load 1ppi_gps_P_3_1.pdb
load 1ppi_gps_P_3_2.pdb
load 1ppi_gps_P_3_3.pdb
load 1ppi_gps_P_5_1.pdb
load 1ppi_gps_P_5_2.pdb
load 1ppi_gps_P_5_3.pdb
load 1ppi_gps_P_6_1.pdb
load 1ppi_gps_P_6_2.pdb
load 1ppi_gps_P_9_1.pdb
load 1ppi_gps_P_9_2.pdb
load 1ppi_gps_P_10_1.pdb
load 1ppi_gps_P_10_2.pdb
set sphere_scale, 0.1
group 1ppi_poc_grids, 1ppi_gps_P_1 1ppi_gps_P_2 1ppi_gps_P_3 1ppi_gps_P_4 1ppi_gps_P_5 1ppi_gps_P_6 1ppi_gps_P_7 1ppi_gps_P_8 1ppi_gps_P_9 1ppi_gps_P_10 1ppi_gps_P_11 1ppi_gps_P_12 1ppi_gps_P_13 1ppi_gps_P_14 
hide everything, 1ppi_poc_grids 
show spheres, 1ppi_poc_grids 
set sphere_scale, 0.1
group 1ppi_spoc_grids, 1ppi_gps_P_1_1 1ppi_gps_P_1_2 1ppi_gps_P_3_1 1ppi_gps_P_3_2 1ppi_gps_P_3_3 1ppi_gps_P_5_1 1ppi_gps_P_5_2 1ppi_gps_P_5_3 1ppi_gps_P_6_1 1ppi_gps_P_6_2 1ppi_gps_P_9_1 1ppi_gps_P_9_2 1ppi_gps_P_10_1 1ppi_gps_P_10_2 
hide everything, 1ppi_spoc_grids 
show spheres, 1ppi_spoc_grids 
show sticks, HETATM and 1ppi and not resn HOH
util.cbay("HETATM and 1ppi and not resn HOH")
hide everything, hydrogens
zoom 1ppi 

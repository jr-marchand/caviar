load ../pdb_cleaned/1dwc.pdb
hide everything, 1dwc 
show cartoon, 1dwc
util.cbc 1dwc
load 1dwc_gps_P_1.pdb
load 1dwc_gps_P_2.pdb
load 1dwc_gps_P_3.pdb
load 1dwc_gps_P_4.pdb
load 1dwc_gps_P_5.pdb
load 1dwc_gps_P_6.pdb
load 1dwc_gps_P_7.pdb
load 1dwc_gps_P_8.pdb
load 1dwc_gps_P_9.pdb
load 1dwc_gps_P_10.pdb
load 1dwc_gps_P_11.pdb
load 1dwc_gps_P_1_1.pdb
load 1dwc_gps_P_1_2.pdb
load 1dwc_gps_P_1_3.pdb
load 1dwc_gps_P_1_4.pdb
load 1dwc_gps_P_1_5.pdb
load 1dwc_gps_P_8_1.pdb
load 1dwc_gps_P_8_2.pdb
set sphere_scale, 0.1
group 1dwc_poc_grids, 1dwc_gps_P_1 1dwc_gps_P_2 1dwc_gps_P_3 1dwc_gps_P_4 1dwc_gps_P_5 1dwc_gps_P_6 1dwc_gps_P_7 1dwc_gps_P_8 1dwc_gps_P_9 1dwc_gps_P_10 1dwc_gps_P_11 
hide everything, 1dwc_poc_grids 
show spheres, 1dwc_poc_grids 
set sphere_scale, 0.1
group 1dwc_spoc_grids, 1dwc_gps_P_1_1 1dwc_gps_P_1_2 1dwc_gps_P_1_3 1dwc_gps_P_1_4 1dwc_gps_P_1_5 1dwc_gps_P_8_1 1dwc_gps_P_8_2 
hide everything, 1dwc_spoc_grids 
show spheres, 1dwc_spoc_grids 
show sticks, HETATM and 1dwc and not resn HOH
util.cbay("HETATM and 1dwc and not resn HOH")
hide everything, hydrogens
zoom 1dwc 

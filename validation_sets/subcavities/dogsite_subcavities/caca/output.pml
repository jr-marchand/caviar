load ../../pdb_cleaned/2fwz.pdb
hide everything, 2fwz 
show cartoon, 2fwz
util.cbc 2fwz
load output_gps_P_1.pdb
load output_gps_P_2.pdb
load output_gps_P_3.pdb
load output_gps_P_4.pdb
load output_gps_P_5.pdb
load output_gps_P_1_1.pdb
load output_gps_P_1_2.pdb
load output_gps_P_1_3.pdb
load output_gps_P_1_4.pdb
load output_gps_P_2_1.pdb
load output_gps_P_2_2.pdb
load output_gps_P_2_3.pdb
load output_gps_P_3_1.pdb
load output_gps_P_3_2.pdb
load output_gps_P_4_1.pdb
load output_gps_P_4_2.pdb
load output_gps_P_4_3.pdb
set sphere_scale, 0.1
group output_poc_grids, output_gps_P_1 output_gps_P_2 output_gps_P_3 output_gps_P_4 output_gps_P_5 
hide everything, output_poc_grids 
show spheres, output_poc_grids 
set sphere_scale, 0.1
group output_spoc_grids, output_gps_P_1_1 output_gps_P_1_2 output_gps_P_1_3 output_gps_P_1_4 output_gps_P_2_1 output_gps_P_2_2 output_gps_P_2_3 output_gps_P_3_1 output_gps_P_3_2 output_gps_P_4_1 output_gps_P_4_2 output_gps_P_4_3 
hide everything, output_spoc_grids 
show spheres, output_spoc_grids 
show sticks, HETATM and 2fwz and not resn HOH
util.cbay("HETATM and 2fwz and not resn HOH")
hide everything, hydrogens
zoom 2fwz 

load ../pdb_cleaned/4flp.pdb
hide everything, 4flp 
show cartoon, 4flp
util.cbc 4flp
load 4flp_gps_P_1.pdb
load 4flp_gps_P_2.pdb
load 4flp_gps_P_3.pdb
load 4flp_gps_P_1_1.pdb
load 4flp_gps_P_1_2.pdb
set sphere_scale, 0.1
group 4flp_poc_grids, 4flp_gps_P_1 4flp_gps_P_2 4flp_gps_P_3 
hide everything, 4flp_poc_grids 
show spheres, 4flp_poc_grids 
set sphere_scale, 0.1
group 4flp_spoc_grids, 4flp_gps_P_1_1 4flp_gps_P_1_2 
hide everything, 4flp_spoc_grids 
show spheres, 4flp_spoc_grids 
show sticks, HETATM and 4flp and not resn HOH
util.cbay("HETATM and 4flp and not resn HOH")
hide everything, hydrogens
zoom 4flp 

load ../pdb_cleaned/4ogj.pdb
hide everything, 4ogj 
show cartoon, 4ogj
util.cbc 4ogj
load 4ogj_gps_P_1.pdb
load 4ogj_gps_P_2.pdb
load 4ogj_gps_P_3.pdb
load 4ogj_gps_P_4.pdb
load 4ogj_gps_P_1_1.pdb
load 4ogj_gps_P_1_2.pdb
set sphere_scale, 0.1
group 4ogj_poc_grids, 4ogj_gps_P_1 4ogj_gps_P_2 4ogj_gps_P_3 4ogj_gps_P_4 
hide everything, 4ogj_poc_grids 
show spheres, 4ogj_poc_grids 
set sphere_scale, 0.1
group 4ogj_spoc_grids, 4ogj_gps_P_1_1 4ogj_gps_P_1_2 
hide everything, 4ogj_spoc_grids 
show spheres, 4ogj_spoc_grids 
show sticks, HETATM and 4ogj and not resn HOH
util.cbay("HETATM and 4ogj and not resn HOH")
hide everything, hydrogens
zoom 4ogj 

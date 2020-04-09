load ../pdb_cleaned/6esm.pdb
hide everything, 6esm 
show cartoon, 6esm
util.cbc 6esm
load 6esm_gps_P_1.pdb
load 6esm_gps_P_2.pdb
load 6esm_gps_P_3.pdb
load 6esm_gps_P_4.pdb
load 6esm_gps_P_2_1.pdb
load 6esm_gps_P_2_2.pdb
load 6esm_gps_P_4_1.pdb
load 6esm_gps_P_4_2.pdb
set sphere_scale, 0.1
group 6esm_poc_grids, 6esm_gps_P_1 6esm_gps_P_2 6esm_gps_P_3 6esm_gps_P_4 
hide everything, 6esm_poc_grids 
show spheres, 6esm_poc_grids 
set sphere_scale, 0.1
group 6esm_spoc_grids, 6esm_gps_P_2_1 6esm_gps_P_2_2 6esm_gps_P_4_1 6esm_gps_P_4_2 
hide everything, 6esm_spoc_grids 
show spheres, 6esm_spoc_grids 
show sticks, HETATM and 6esm and not resn HOH
util.cbay("HETATM and 6esm and not resn HOH")
hide everything, hydrogens
zoom 6esm 

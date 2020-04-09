load ../pdb_cleaned/6fg6.pdb
hide everything, 6fg6 
show cartoon, 6fg6
util.cbc 6fg6
load 6fg6_gps_P_1.pdb
load 6fg6_gps_P_2.pdb
load 6fg6_gps_P_3.pdb
load 6fg6_gps_P_1_1.pdb
load 6fg6_gps_P_1_2.pdb
set sphere_scale, 0.1
group 6fg6_poc_grids, 6fg6_gps_P_1 6fg6_gps_P_2 6fg6_gps_P_3 
hide everything, 6fg6_poc_grids 
show spheres, 6fg6_poc_grids 
set sphere_scale, 0.1
group 6fg6_spoc_grids, 6fg6_gps_P_1_1 6fg6_gps_P_1_2 
hide everything, 6fg6_spoc_grids 
show spheres, 6fg6_spoc_grids 
show sticks, HETATM and 6fg6 and not resn HOH
util.cbay("HETATM and 6fg6 and not resn HOH")
hide everything, hydrogens
zoom 6fg6 

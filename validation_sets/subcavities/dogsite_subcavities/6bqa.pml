load ../pdb_cleaned/6bqa.pdb
hide everything, 6bqa 
show cartoon, 6bqa
util.cbc 6bqa
load 6bqa_gps_P_1.pdb
load 6bqa_gps_P_2.pdb
load 6bqa_gps_P_1_1.pdb
load 6bqa_gps_P_1_2.pdb
set sphere_scale, 0.1
group 6bqa_poc_grids, 6bqa_gps_P_1 6bqa_gps_P_2 
hide everything, 6bqa_poc_grids 
show spheres, 6bqa_poc_grids 
set sphere_scale, 0.1
group 6bqa_spoc_grids, 6bqa_gps_P_1_1 6bqa_gps_P_1_2 
hide everything, 6bqa_spoc_grids 
show spheres, 6bqa_spoc_grids 
show sticks, HETATM and 6bqa and not resn HOH
util.cbay("HETATM and 6bqa and not resn HOH")
hide everything, hydrogens
zoom 6bqa 

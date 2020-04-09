load ../pdb_cleaned/5i7y.pdb
hide everything, 5i7y 
show cartoon, 5i7y
util.cbc 5i7y
load 5i7y_gps_P_1.pdb
load 5i7y_gps_P_2.pdb
load 5i7y_gps_P_1_1.pdb
load 5i7y_gps_P_1_2.pdb
load 5i7y_gps_P_2_1.pdb
load 5i7y_gps_P_2_2.pdb
set sphere_scale, 0.1
group 5i7y_poc_grids, 5i7y_gps_P_1 5i7y_gps_P_2 
hide everything, 5i7y_poc_grids 
show spheres, 5i7y_poc_grids 
set sphere_scale, 0.1
group 5i7y_spoc_grids, 5i7y_gps_P_1_1 5i7y_gps_P_1_2 5i7y_gps_P_2_1 5i7y_gps_P_2_2 
hide everything, 5i7y_spoc_grids 
show spheres, 5i7y_spoc_grids 
show sticks, HETATM and 5i7y and not resn HOH
util.cbay("HETATM and 5i7y and not resn HOH")
hide everything, hydrogens
zoom 5i7y 

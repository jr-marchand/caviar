load ../pdb_cleaned/2z65.pdb
hide everything, 2z65 
show cartoon, 2z65
util.cbc 2z65
load 2z65_gps_P_1.pdb
load 2z65_gps_P_2.pdb
load 2z65_gps_P_3.pdb
load 2z65_gps_P_4.pdb
load 2z65_gps_P_5.pdb
load 2z65_gps_P_1_1.pdb
load 2z65_gps_P_1_2.pdb
load 2z65_gps_P_1_3.pdb
set sphere_scale, 0.1
group 2z65_poc_grids, 2z65_gps_P_1 2z65_gps_P_2 2z65_gps_P_3 2z65_gps_P_4 2z65_gps_P_5 
hide everything, 2z65_poc_grids 
show spheres, 2z65_poc_grids 
set sphere_scale, 0.1
group 2z65_spoc_grids, 2z65_gps_P_1_1 2z65_gps_P_1_2 2z65_gps_P_1_3 
hide everything, 2z65_spoc_grids 
show spheres, 2z65_spoc_grids 
show sticks, HETATM and 2z65 and not resn HOH
util.cbay("HETATM and 2z65 and not resn HOH")
hide everything, hydrogens
zoom 2z65 

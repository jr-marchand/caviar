# -*- coding: utf-8 -*-
"""
This module aims at identifying cavities. It contains a modified
version of the LigSiteCS algorithm
The protein is projected onto a cubic regular 3D grid (cf gridtools.py).
Since the grid is regular, most of the work is not made in the Cartesian 3D space, but 
is projected on the indices of the grid (a mathematical rule can be made to identify
the indices of the neighbors of a certain index point of the grid).
Characteristics of the grid points are projected in an array, grid_decomposition.
This array contains n values (corresponding to indices of grid points, of length
size of the grid), which are either 0 (solvent grid point), 1 (protein grid point)
or >=2 (potential cavity grid point). Grid points that fall within the van der Waals +
probe volume of the protein are labelled as "protein", ie, "1".
This is the function "find_protein_points_variablevolume". A file contains the information
on the size of protein atoms. At this stage, grid points are either tagged as 0 or as 1.
Then, each "0" grid point (solvent) undergoes an evaluation of its burial.
The neighboring grid points around the grid point of interest are checked. The algorithm
works in a cubic fashion, ie, points in the 14 cubic directions around the point
of interest are investigated up to a certain number of cubes around said grid points.
If a protein grid point (ie, "1") is found in one of the 14 directions within "radius_cube",
the burial is incremented by one and the next direction is investigated.
That gives a burial between 0 (no protein grid point within radius_cube around the grid point
of interest) and 14 (protein grid points are found in the 14 directions around the grid point
of interest within radius_cube). The function performing this task is "set_burial_scandir_np".
Grid points that have a burial >= min_burial (9 by default) are kept as potential grid points.
A second pass is made within the same function. If a cavity is large, it can very well be that 
some cavity grid points "in the middle of the cavity" are not in direct contact with the protein,
but enclosed enough within cavity grid points and should be part of the cavity. This scenario is 
investigated using the same rational than aforementioned, except that instead of checking if a
solvent point is in contact with the protein in cubic directions, here, its contact with cavity
grid points ("2") is checked, within "cube_radius_enc" and "min_burial_enc".
At the end, the indices of grid points with a buriedness >= min_burial in grid_decomposition 
are assigned values between min_burial and 14 (their buriedness), or 2 ("middle cavity points")
(in opposition to 0 for solvent and 1 for protein)

This data is then fed into a graph, for which nodes are potential cavity grid points,
and edges are built between cavity grid points that are in cubic contact. Bridges in the graph, self
loops, as well as nodes that are not well connected (min_degree = 3) are excluded.
Only cavities of size > min_points (80 by default ~ volume of benzene) are ultimately retained.

The final function filter_cavities calculates a cavity score:
(size_cav/100)*(median buriedness)*(7th quantile of buriedness value)/100
in order to rank cavities. It also filters out cavities that have fewer than X% (30% within quantile = 0.7) grid points 
with a buriedness >= min_burial_q = 11 and prints out information (size of the cavity in grid points, median
buriedness, 7th quantile of buriedness, score)

"""

from caviar.prody_parser.atomic.atomgroup import AtomGroup
from .geometry import SetOfPoints
import numpy as np
import networkx as nx
from .gridtools import get_index_of_coor_list, list_transform_indices, get_transformation_vectors
from caviar.cavity_characterization.gridpoint_properties import trim_cavity_bylocalweight
# from bisect import bisect_left
#import time 

__all__ = ['wrapper_early_cav_identif']

import os

#@profile
def find_protein_points_variablevolume(gridpoints, protselection,
	file_sizes = os.path.join(os.path.dirname(__file__), "vdw_size_atoms.dat"), size_probe = 1.0):
	"""
	Identifies grid points that are belonging to protein atoms (sizes in file_sizes)
	size_probe is the size of the solvent sphere
	Returns two objects: the indices in grid that correspond to protein points
	and those that are solvent
	Is 3 to 4 times slower than the parent function with only one size
	"""

	# convert the grid to a set of points
	gridset = SetOfPoints(gridpoints)

	# Read file containing vdw sizes and iterate over it
	grid_protein_dupl = np.array([], dtype=int)
	with open(file_sizes) as all_sizes:
		for line in all_sizes:
			if len(line.split()) == 2:
				new_sel = protselection.select(f"element {line.split()[0]}")
				if new_sel:
					new_sel_coord = new_sel.getCoords()
					dist_range = float(line.split()[1]) + size_probe
					# This function takes 77-95% of the CPU time (expected). Doesn't scale well
					dist_max = gridset.print_indices_within(new_sel_coord, dist_range)
					tmp = np.unique(dist_max["i"])
					# np.append is slow, takes 2-4% of the CPU time. Why not work on lists?
					grid_protein_dupl = np.append(grid_protein_dupl, tmp)

	grid_protein = np.unique(grid_protein_dupl)
	grid_indices = np.arange(start = 0, stop = len(gridpoints), step = 1, dtype=int)
	grid_solv = np.delete(grid_indices, np.array(grid_protein, dtype=int), axis=0)

	# Generate a list of grid points. If indice = 0 => solvent
	# If indice = 1 => protein point
	# and later, indice = 2 => cavity point 
	grid_decomposition = np.zeros(shape=len(gridpoints), dtype = int)
	grid_decomposition[grid_protein] = 1

	return grid_protein, grid_solv, grid_decomposition

def filter_out_bulksolvent(selection_coords, grid, grid_solv, maxdistance = 5.0):
	"""
	We generate a cubic grid around an irregular shaped protein
	Thus there are many grid points that are very far from the protein and 
	eat computational time for no reason
	This function is simply discarding bulk solvent points, ie, grid points
	that are above a threshold (8A by default) to any protein point.
	Returns an indice list that replaces grid_solv from find_protein_points_variablevolume
	It takes a bit of computational time, but saves a lot for set_burial_scandir_np()
	BTW, the lower maxdistance, the lower the CPU time
	"""
	setofprot = SetOfPoints(selection_coords)
	solv_inrange = np.unique(setofprot.print_indices_within(grid[grid_solv], max_distance = maxdistance)["j"])
	ori_indices_inrange = grid_solv[solv_inrange]

	return ori_indices_inrange

#@profile
def set_burial_scandir_np(grid_solv, grid_decomposition, grid_protein, grid_shape,
	radius_cube = 5, min_burial = 9, startingpoint_radius = 3, radius_cube_enc = 4, min_burial_enc = 7,
	startingpoint_radius_enc = 1):
	"""
	This function sets the burial level of solvent grid points. If this burial is above
	min_burial, the point is considered as potential cavity point. It works in two steps.
	The first one investigates the number of protein contacts in the 14 cubic directions 
	around a grid point of interest (up to radius_cube cubic gridspacing).
	Then it tags as "2" the points with a burial > min_burial in grid_decomposition.
	The second step is to identify points that are in the "middle" of cavities: they are
	enclosed in a space of potential grid points but since the cavity is big, they are
	not in direct contact with protein grid points within radius_cube distance.
	The variables ending with "_enc" (for enclosed) are related to the second pass.
	"""
	if radius_cube <= startingpoint_radius:
		print("radius_cube should be strictly greater than startingpoint_radius")
	# Step 1, generate all the directions to scan
	transform_vectors = get_transformation_vectors(radius_cube = radius_cube, startingpoint = startingpoint_radius)
	transform_ind = list_transform_indices(transform_vectors = transform_vectors, grid_shape = grid_shape)

	# Step 2 generate all indices in the 14 directions * radius_cube -3
	allindices = []
	indices_1dir = []
	for direction in transform_ind:
		for transf in direction:
			indices_1dir.append(grid_solv + transf)
		allindices.append(indices_1dir)
		indices_1dir = []
	
	combined_indices = np.array(allindices)
	
	# Identify which of these indices exist in grid_protein
	# This is the function that takes most of the time
	# Takes 48% of the time (expected, the other half is the second call to isin)
	# Scales well with size
	truth = np.isin(combined_indices, grid_protein)
	# Recapitulate this data into burial data
	# Count non zero elements in the dimension of the radius_cube-3 and then
	# in each of the 14 dimensions (to get the burial between 0 and 14)
	bur1 = np.count_nonzero(np.count_nonzero(truth, axis = 1), axis = 0)
	bli1 = np.where(bur1 >= min_burial)[0]
	# Don't forget that the indices here are those in grid_solv
	# and not in the original grid array!
	grid_decomposition[grid_solv[bli1]] = bur1[bli1]
	# This sets the value of burial for grid indices that are above the threshold
	# grid_decomposition will now have values: 0 (solvent), 1 (protein), 9/10/11/12/13/14 (burial)

	##########################################################################
	## Do a second pass for the "middle cavity points", ie, not directly in
	# contact with the protein at 5 grid spacing values, but that are enclosed
	# inside other cavity points (and should thus be part of the cavity)
	##########################################################################
	grid_cav_tmp = np.argwhere(grid_decomposition > 1)
	grid_solv_tmp = np.argwhere(grid_decomposition == 0)
	# Now repeat the same exact procedure with grid_cav_tmp instead of
	# grid_protein and grid_solv_tmp instead of grid_solv
	
	transform_vectors_enc = get_transformation_vectors(radius_cube = radius_cube_enc,
		startingpoint = startingpoint_radius_enc)
	transform_ind_enc = list_transform_indices(transform_vectors = transform_vectors_enc, grid_shape = grid_shape)
	allindices = []
	indices_1dir = []
	for direction in transform_ind:
		for transf in direction:
			indices_1dir.append(grid_solv_tmp + transf)
		allindices.append(indices_1dir)
		indices_1dir = []	
	combined_indices = np.array(allindices)
	# Takes 44% of the time (expected, the other half is the first call to isin)
	truth = np.isin(combined_indices, grid_cav_tmp)
	bur = np.count_nonzero(np.count_nonzero(truth, axis = 1), axis = 0)
	bli = np.where(bur >= min_burial_enc)[0]
	grid_decomposition[grid_solv_tmp[bli]] = 2
	# In that case we just set the additional points as a value "2"
	# grid_decomposition will now have values: 0 (solvent), 1 (protein), 9/10/11/12/13/14 (burial)
	# or 2 ("middle cavity points")

	return grid_decomposition

#@profile
def generate_graph(grid_decomposition, gridpoints, grid_min, grid_shape, gridspace = 1.0,
	min_degree = 3, radius = 2, score = 500):
	"""
	Generate a graph from cavity points. It connects nodes if they are within gridspace
	distance. It removes self loops and bridges.

	################# ADDED TRIMMING OF CAVITY POINTS #################################
	Uses trim_cavity_bylocalweight
	which is in cavity_characterization.gridpoint_properties.py
	Originally this function was supposed to trim cavities later

	"""
	# Find cavity points indices and extract their coordinates
	cavity_point = np.where(grid_decomposition > 1)[0]
	cav_coor = gridpoints[cavity_point]

	trimmed_cavs = trim_cavity_bylocalweight(cav_coor, grid_min, grid_shape, grid_decomposition,
                                               radius, score)

	setcav = SetOfPoints(trimmed_cavs)

	diag = gridspace + 0.1# +0.1 because floating point #*np.sqrt(3) was for the diagonal connections
	# but it ended up overspanning
	if len(trimmed_cavs) == 0:
		return None, None
	dist_mat = setcav.print_indices_within(trimmed_cavs, diag, turnon = False)
	list_edges = dist_mat[["i","j"]]
	G = nx.Graph() # Initialize graph
	G.add_edges_from(list_edges)
	# Remove self edges
	G.remove_edges_from(nx.selfloop_edges(G)) 

	# Remove nodes with few connections
	remove = [node for node,degree in dict(G.degree()).items() if degree < min_degree]
	G.remove_nodes_from(remove) 
	# List and remove bridges. There should probably not be any?
	bridges = list(nx.bridges(G))
	G.remove_edges_from(bridges)

	return G, trimmed_cavs

def get_large_cavities_from_graph(G, cav, min_points = 60):
	"""
	Returns a list of cavities coordinates from the graph, with a minimal size in number of points
	min_points is defaulted to 80, which is a bit smaller than the size of a benzene molecule (88A3)
	"""
	large_cavities = [x for x in nx.connected_components(G) if len(x) > min_points]
	list_cavs_coords = []
	for cavity in large_cavities:
		list_cavs_coords.append(np.take(a = cav, indices = list(cavity), axis = 0))
	
	if len(list_cavs_coords) > 1: # deprecation with numpy 1.19
		# https://numpy.org/doc/stable/release/1.19.0-notes.html#deprecate-automatic-dtype-object-for-ragged-input
		array_cavs_coords = np.array(list_cavs_coords, dtype=object)
	else:
		array_cavs_coords = np.array(list_cavs_coords)
	return array_cavs_coords

def filter_cavities(array_cavs_coords, grid_decomposition, grid_min, grid_shape, gridspace = 1.0,
	min_burial_q = 10, quantile = 0.8, maxsize = 3000):
	"""
	Scores cavities ((size cavity/100)*(median buriedness)*(7th quantile buriedness)/100)
	Exports data (size, median buriedness, 7th quantile buriedness, score)
	Filters out cavities with less than 1-quantile % of points with a min_burial_q = 10 
	"""
	cavid = 0
	
	cavs_curated = []
	cavs_info = {}
	for cavity in array_cavs_coords:
		size_cav = len(cavity)
		cav_indices = get_index_of_coor_list(cavity, grid_min, grid_shape, gridspace)
		median_bur = np.median(grid_decomposition[cav_indices])
		q_7 = np.quantile(grid_decomposition[cav_indices], q = 0.7)
		if np.quantile(grid_decomposition[cav_indices], q = quantile) > min_burial_q and size_cav < maxsize:
			score = np.around((size_cav/100)*(median_bur)*(q_7)/100, decimals=1)
			cavs_curated.append(cavity)
			cavs_info[cavid] = [size_cav, median_bur, q_7, score]
			#print(median_bur)
			cavid += 1

	if len(cavs_curated) > 1: # deprecation with numpy 1.19
		# https://numpy.org/doc/stable/release/1.19.0-notes.html#deprecate-automatic-dtype-object-for-ragged-input
		cavs_cur = np.array(cavs_curated, dtype=object)
	else:
		cavs_cur = np.array(cavs_curated)


	return cavs_cur, cavs_info


def wrapper_early_cav_identif(grid, grid_min, grid_shape, selection_protein, selection_coords,
	size_probe = 1.0, maxdistance = 6.0,
	radius_cube = 4, min_burial = 8, radius_cube_enc = 3, min_burial_enc = 8, gridspace = 1.0, min_degree = 3,
	radius = 2, trim_score = 500, min_points = 40, min_burial_q = 10, quantile = 0.8, maxsize = 3000):
	"""
	In order to lower the overhead from importing modules in main.py
	we combine all of the afore-coded functions as one wrapper
	"""
	# Identify points of the grid that are within the surface of the protein
	grid_protein, grid_solv, grid_decomposition_0 = find_protein_points_variablevolume(gridpoints = grid,
		protselection = selection_protein, size_probe =  size_probe)
	## Filter out bulk solvent, ie solvent grid points that are > args.maxdistance from the protein
	## due to the cubic shape of the box
	nonbulk_gridsolv = filter_out_bulksolvent(selection_coords = selection_coords, grid = grid,
		grid_solv = grid_solv, maxdistance = maxdistance)
	# Most time consuming function (less now that we trim out bulk solvent)
	# Scans solvent grid points to set the buriedness of all grid points and identify
	# potential cavity grid points
	grid_decomposition = set_burial_scandir_np(grid_solv = nonbulk_gridsolv, grid_decomposition = grid_decomposition_0,
		grid_protein = grid_protein, grid_shape = grid_shape, radius_cube = radius_cube,
		min_burial = min_burial, radius_cube_enc = radius_cube_enc, min_burial_enc = min_burial_enc)
	# Generate a graph from potential grid points. Filter out self loops, bridges, not well connected nodes
	# (with min_degree)
	G, cav = generate_graph(grid_decomposition, grid, grid_min, grid_shape, gridspace,
		min_degree, radius, trim_score)
	if G == None:
		return None, None, None
	# Filter out small cavities
	array_cavs_coords = get_large_cavities_from_graph(G, cav, min_points = min_points * 1/gridspace) # adapt number of points with gridspace
	# Score cavities, filter out cavities that have less that 1-quantile grid points
	# buried with a min_burial_q
	cavities, cavities_info = filter_cavities(array_cavs_coords, grid_decomposition, grid_min,
		grid_shape, gridspace, min_burial_q, quantile)


	return cavities, cavities_info, grid_decomposition



###### NOT IN main.py for now, kept in case
def point_in_hull(point, hull, tolerance=1e-12):
	"""
	The convex hull can be represented as a list of outward facing facets.
	A sufficient check for being outside the convex hull is to check the point
	against each facet and surface normal to see which side it is on.
	The surface normals for each facet is access by hull.equations (3 first column,
	and the offset is in the 4th column).
	A point that is outside any convex hull triangle is outside the entire convex hull. 
	"""
	if np.any(np.dot(hull.equations[:,:-1], point) + hull.equations[:,-1] >= tolerance):
		return "it's out"
	else:
		return False

def get_gridpoint_in_protein_convexhull(selection_coords, grid_solv_coords):
	"""
	Unused function because it is not faster than the current implementation
	Was designed to exclude uninteresting solvent point and work only
	on solvent grid points that are within the convex hull of the protein
	A protein cavity being nothing but solvent within the convex hull of the protein
	In three dimensions, the convex hull is the smallest volume convex polyhedron that
	contains all the surface points
	"""
	from scipy.spatial import ConvexHull # Could import generally but since it's not used...
	hull = ConvexHull(selection_coords)
	
	idx=0
	solv_idx_inhull = []
	for point in grid_solv_coords:
		if not point_in_hull(point, hull):
			solv_idx_inhull.append(idx)
		idx += 1

	return solv_idx_inhull

def set_burial_scandir_onepass(grid_solv, grid_decomposition, grid_protein, grid_shape,
	radius_cube = 5, min_burial = 9, startingpoint_radius = 3):
	"""
	This function sets the burial level of solvent grid points. If this burial is above
	min_burial, the point is considered as potential cavity point. It works in two steps.
	The first one investigates the number of protein contacts in the 14 cubic directions 
	around a grid point of interest (up to radius_cube cubic gridspacing).
	Then it tags as "2" the points with a burial > min_burial in grid_decomposition.
	This function doesn't do a second pass. It is meant to be used with get_large_cavities_from_graph_add_fromhull
	in which we re-add potential middle cavity points as mathematically defined
	as the solvent grid points that are within the convex hull of a cavity
	"""
	if radius_cube <= startingpoint_radius:
		print("radius_cube should be strictly greater than startingpoint_radius")
	# Step 1, generate all the directions to scan
	transform_vectors = get_transformation_vectors(radius_cube = radius_cube, startingpoint = startingpoint_radius)
	transform_ind = list_transform_indices(transform_vectors = transform_vectors, grid_shape = grid_shape)

	# Step 2 generate all indices in the 14 directions * radius_cube -3
	allindices = []
	indices_1dir = []
	for direction in transform_ind:
		for transf in direction:
			indices_1dir.append(grid_solv + transf)
		allindices.append(indices_1dir)
		indices_1dir = []
	
	combined_indices = np.array(allindices)
	
	# Identify which of these indices exist in grid_protein
	# This is the function that takes most of the time
	# Takes 48% of the time (expected, the other half is the second call to isin)
	# Scales well with size
	truth = np.isin(combined_indices, grid_protein)
	# Recapitulate this data into burial data
	# Count non zero elements in the dimension of the radius_cube-3 and then
	# in each of the 14 dimensions (to get the burial between 0 and 14)
	bur1 = np.count_nonzero(np.count_nonzero(truth, axis = 1), axis = 0)
	bli1 = np.where(bur1 >= min_burial)[0]
	# Don't forget that the indices here are those in grid_solv
	# and not in the original grid array!
	grid_decomposition[grid_solv[bli1]] = bur1[bli1]
	# This sets the value of burial for grid indices that are above the threshold
	# grid_decomposition will now have values: 0 (solvent), 1 (protein), 9/10/11/12/13/14 (burial)

	return grid_decomposition

def get_large_cavities_from_graph_add_fromhull(G, cav, grid, grid_decomposition, min_points = 60):
	"""
	Returns a list of cavities coordinates from the graph, with a minimal size in number of points
	min_points is defaulted to 80, which is a bit smaller than the size of a benzene molecule (88A3)
	"""

	solvent = grid[grid_decomposition == 0]
	large_cavities = [x for x in nx.connected_components(G) if len(x) > min_points]
	list_cavs_coords = []
	list_cavs_coords_hull = []
	for cavity in large_cavities:
		thiscav = np.take(a = cav, indices = list(cavity), axis = 0)
		list_cavs_coords.append(thiscav)
		id_solv_inhull_thiscav = get_gridpoint_in_protein_convexhull(thiscav, solvent)
		prout = solvent[id_solv_inhull_thiscav]
		thiscav_hull = np.vstack((thiscav, solvent[id_solv_inhull_thiscav]))
		list_cavs_coords_hull.append(thiscav_hull)

	array_cavs_coords = np.array(list_cavs_coords)
	array_cavs_coords_hull = np.array(list_cavs_coords_hull)

	return array_cavs_coords, array_cavs_coords_hull


################################
#### DEPRECATED FUNCTIONS ######
################################

#def probe_weight_pass():
#	"""
#	Do I want to implement this?
#	"""

#def export_dummy_pdb_points(solv, prot, cav, array_cavs_coords):
#	"""
#	For visualization purposes: exports a pdb containing 
#	"O" atoms for the solvent grid and "N" atoms for the grid
#	points enclosed in the protein
#	"""
#
#	pdbdummy = []
#	for coordinates in solv:
#		pdbdummy.append("HEATM    1  O   GRI A   1    %8.3f%8.3f%8.3f  1.00 52.42           O\n" % (coordinates[0], coordinates[1], coordinates[2]))
#	for coordinates in prot:
#		pdbdummy.append("HEATM    1  N   GRI A   1    %8.3f%8.3f%8.3f  1.00 52.42           O\n" % (coordinates[0], coordinates[1], coordinates[2]))
#	for coordinates in cav:
#		pdbdummy.append("HEATM    1  C   GRI A   1    %8.3f%8.3f%8.3f  1.00 52.42           O\n" % (coordinates[0], coordinates[1], coordinates[2]))
#	for cavity in array_cavs_coords:
#		for coordinates in cavity:
#			pdbdummy.append("HEATM    1  S   GRI A   1    %8.3f%8.3f%8.3f  1.00 52.42           O\n" % (coordinates[0], coordinates[1], coordinates[2]))
#
#	return pdbdummy


# def find_protein_pointsold(gridpoints, proteinpoints, size_atoms = 2.7):#, radius_shell = 5.5):
# 	"""
# 	Identifies grid points that are belonging to protein atoms (at size_atoms)
# 	size_atoms is a conservative value for the size of all protein atoms,
# 	although a finer grain would be to have a size per atom type
# 	Returns three objects: the indices in grid that correspond to protein points
# 	and the coordinates of grid points that are protein and those that are solvent
# 	"""
# 	grid = SetOfPoints(gridpoints)
# 	tmp = grid.in_range_settoset(proteinpoints, size_atoms, asbool = False)
# 	grid_protein = np.unique(tmp[0])
# 	coor_prot_point = gridpoints[grid_protein]
# 	coor_solv_point = np.delete(gridpoints, grid_protein, axis=0)
# 	return grid_protein, coor_prot_point, coor_solv_point

#def find_protein_points(all_dist, gridpoints, dist_range = 2.7):
#	"""
#	Identifies grid points that are belonging to protein atoms (at size_atoms)
#	size_atoms is a conservative value for the size of all protein atoms,
#	although a finer grain would be to have a size per atom type
#	Returns three objects: the indices in grid that correspond to protein points
#	and the coordinates of grid points that are protein and those that are solvent
#	"""
#	whoinrange = in_range_from_matrix(all_dist, dist_range)
#	grid_protein = np.unique(whoinrange[0])
#	grid_indices = np.arange(start = 0, stop = len(gridpoints), step = 1)
#	grid_solv = np.delete(grid_indices, grid_protein, axis=0)
#	#coor_prot_point = gridpoints[grid_protein]
#	#coor_solv_point = np.delete(gridpoints, grid_protein, axis=0)
#	return grid_protein, grid_solv#, coor_prot_point, coor_solv_point

# def find_protein_points(gridpoints, protpoints, dist_range = 2.7):
# 	"""
# 	Identifies grid points that are belonging to protein atoms (at size_atoms)
# 	size_atoms is a conservative value for the size of all protein atoms,
# 	although a finer grain would be to have a size per atom type
# 	Returns 2 objects: the indices in grid that correspond to protein points
# 	and those that are solvent
# 	"""
# 	gridset = SetOfPoints(gridpoints)
# 	grid_protein_withdupli = gridset.print_indices_within(protpoints, dist_range)
# 	grid_protein = np.unique(grid_protein_withdupli)
# 	grid_indices = np.arange(start = 0, stop = len(gridpoints), step = 1, dtype=int)
# 	grid_solv = np.delete(grid_indices, np.array(grid_protein, dtype=int), axis=0)
# 
# 	return grid_protein, grid_solv 

## def set_burial(gridpoints, protpoints, radius_shell = 5.5):
## 	"""
## 	Returns the number of atomic coordinates within a solvation shell
## 	"""
## 	boolarr = all_dist < radius_shell
## 	# this gives an array for which each indice correspond to 
## 	# a grid point and contains the number of protein coordinates 
## 	# within radius_shell
## 	list_burial = np.count_nonzero(boolarr, axis=1)
## 	return list_burial

#def set_burial(gridpoints, protpoints, radius_shell = 5.5):
#	"""
#	Returns a list (each position corresponds to the indice in gridpoints)
#	containing the count of protpoints in radius_shell
#	"""
#	grid_set = SetOfPoints(gridpoints)
#	matrix = grid_set.print_indices_within(protpoints, radius_shell)
#	unique, counts = np.unique(matrix, return_counts = True)
#	list_burial = np.zeros(len(gridpoints), dtype = np.int32)
#	np.put(a = list_burial, ind = unique, v = counts)
#	# this gives a list for which each indice correspond to 
#	# a grid point and contains the number of protein coordinates 
#	# within radius_shell
#	return list_burial

# def isainx(a, x):
# 	"""
# 	Binary search implementation
# 	"""
#     i = bisect_left(a, x)
#     if i != len(a) and a[i] == x:
#         return i
#     else:
#         return None

#def set_burial_scandir(gridpoints, grid_solv, grid_protein, grid_min, grid_shape,
#	radius_cube = 5, gridspace = 1.0, min_burial = 9):
#	"""
#
#	"""
#	directions = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 1, 1], [-1, 1, 1], [1, -1, 1], [1, 1, -1],
#                     [0, 0, -1], [0, -1, 0], [-1, 0, 0], [-1, -1, -1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]])
#	dict_burial = {}
#	index = 0
#	for point in gridpoints[grid_solv]:
#		burial = 0
#		for vector in directions:
#			flagnext = False
#			vector_rad = [vector*x for x in range(2, 6)]
#			points_dir = [v + point for v in vector_rad]
#			idx_lst = np.array(get_index_of_coor_list(points_dir, grid_min, grid_shape, gridspace = 1.0), dtype=int)
#			if np.any(np.in1d(idx_lst, grid_protein, assume_unique=True)):
#				burial += 1
#				continue
#		
#		if burial >= min_burial:
#			dict_burial[grid_solv[index]] = burial
#		index += 1
#
#	return dict_burial

#def find_cavity_points_new(grid_decomposition, grid_shape, grid_solv, 
#						   gridspace = 1.0, min_burial = 9, radius_cube = 5,
#						   radius_cube_enc = 4, min_burial_enc = 7, startingpoint_radius = 1):
#	"""
#	Returns potential cavity points: if more than min_prot_contacts within
#	radius_shell of cavity point (excluding protein points)
#	
#	Returns two lists (of indices), one with "full solvent" points
#	and one with potential cavity points.
#	Then, the points need to be clustered in order to identify cavities
#	"""
#	# First pass between non protein grid points and protein
#	#start = time.time()
#	grid_decomposition_1 = set_burial_scandir(grid_solv, np.ndarray.tolist(grid_decomposition),
#		grid_shape, radius_cube, gridspace, min_burial)
#
#	# Second pass between potential solvent points and potential
#	# grid points (for finding 'middle points')
#	grid_decomposition_2 = find_enclosed_solvpoints_in_cavity(grid_decomposition_1, grid_shape,
#		radius_cube_enc, gridspace, min_burial_enc, startingpoint_radius)
#
#	#end = time.time()
#	#print(f"It took {end-start} seconds to generate theburial list")
#
#	return grid_decomposition_2
#
###@profile
#def set_burial_scandir(grid_solv, grid_decomposition, grid_shape,
#	radius_cube = 5, gridspace = 1.0, min_burial = 9):
#	"""
#
#	"""
#	if radius_cube < 4:
#		print("radius_cube should be strictly greater than 3")
#	# Step 1, generate all the directions to scan
#	transform_vectors = get_transformation_vectors(gridspace, radius_cube)
#	transform_ind = list_transform_indices(transform_vectors, grid_shape)
#	bla = np.ndarray.tolist(grid_solv)
#
#	maxval = len(grid_decomposition)
#	for idx in bla:
#		burial = 0
#		# Loop over the 14 directions
#		for transfs in transform_ind:
#			# Loop over the x cubes of each direction
#			for transf in transfs:
#				investigated_gridpoint_ind = idx + transf
#				if investigated_gridpoint_ind < 0:
#					continue
#				elif investigated_gridpoint_ind >= maxval:
#					continue
#				elif grid_decomposition[investigated_gridpoint_ind]:
#					burial += 1
#					break
#	
#		if burial >= min_burial:
#				grid_decomposition[idx] = 2
#
#
#	return grid_decomposition
# #@profile
#def find_enclosed_solvpoints_in_cavity(grid_decomposition, grid_shape,
#	radius_cube_enc = 4, gridspace = 1.0, min_burial_enc = 7, startingpoint_radius = 1):
#	"""
#
#	"""
#	if radius_cube_enc < 2:
#		print("radius_cube_enc should be strictly greater than 1")
#	# Step 1, generate all the directions to scan
#	transform_vectors = get_transformation_vectors(gridspace, radius_cube_enc, startingpoint_radius)
#	transform_ind = list_transform_indices(transform_vectors, grid_shape)
#	
#	index = 0
#	still_solvent_points = []
#	for x in grid_decomposition:
#		if x == 0:
#			still_solvent_points.append(index)
#		index += 1
#	
#	maxval = len(grid_decomposition)
#	for idx in still_solvent_points:
#		burial = 0
#		# Loop over the 14 directions
#		for transfs in transform_ind:
#			# Loop over the x cubes of each direction
#			for transf in transfs:
#				investigated_gridpoint_ind = idx + transf
#				if investigated_gridpoint_ind < 0:
#					continue
#				elif investigated_gridpoint_ind >= maxval:
#					continue
#				elif grid_decomposition[investigated_gridpoint_ind] == 2:
#					burial += 1
#					break
#	
#		if burial >= min_burial_enc:
#				grid_decomposition[idx] = 2
#
#
#	return grid_decomposition

#def find_cavity_points(gridpoints, protpoints, grid_protein, grid_solv, radius_shell = 5.5,
#	min_prot_contacts = 15, secondpass_shell = 3.0, min_secondpass_contacts = 25):
#	"""
#	Returns potential cavity points: if more than min_prot_contacts within
#	radius_shell of cavity point (excluding protein points)
#	
#	Returns two lists (of indices), one with "full solvent" points
#	and one with potential cavity points.
#	Then, the points need to be clustered in order to identify cavities
#	"""
#	# grid_indices = np.arange(start = 0, stop = len(gridpoints), step = 1, dtype=int)
#	# First pass between non protein grid points and protein
#	list_burial = set_burial(gridpoints[grid_solv], protpoints, radius_shell)
#	whonotsolvent = np.nonzero(list_burial > min_prot_contacts)[0]
#	# Needs to be related to original order in grid_indices
#	ori_whonotsolv = grid_solv[whonotsolvent]
#	solvent_around = np.setdiff1d(grid_solv, ori_whonotsolv, assume_unique = True)
#
#	# Second pass between potential solvent points and potential
#	# grid points (for finding 'middle points')
#
#	list_secondpass = set_burial(gridpoints[solvent_around], gridpoints[ori_whonotsolv]
#		, secondpass_shell)
#	# The indices in list_secondpass are indices in solvent_around. Is it?
#	# One needs to convert from solvent_around to go back to indices from gridpoints
#	whonotsolvent2 = np.nonzero(list_secondpass > min_secondpass_contacts)[0]
#	# Needs to be related to original order in grid_indices
#	ori_whonotsolv2 = solvent_around[whonotsolvent2]
#	solvent_around_2 = np.setdiff1d(grid_solv, ori_whonotsolv2, assume_unique = True)
#
#	all_potential_cavity_points = np.unique(np.concatenate((ori_whonotsolv, ori_whonotsolv2)))
#	all_solvent_around = np.unique(np.concatenate((solvent_around, solvent_around_2)))
#
#	return all_potential_cavity_points, all_solvent_around
#
#def find_cavity_points_scandir(gridpoints, grid_solv, grid_protein, grid_min, grid_shape,
#	radius_cube = 5, gridspace = 1.0, min_burial = 9, secondpass_radius = 2, min_secondpass_contacts = 9):
#	"""
#	Returns potential cavity points: if more than min_prot_contacts within
#	radius_shell of cavity point (excluding protein points)
#	
#	Returns two lists (of indices), one with "full solvent" points
#	and one with potential cavity points.
#	Then, the points need to be clustered in order to identify cavities
#	"""
#	# grid_indices = np.arange(start = 0, stop = len(gridpoints), step = 1, dtype=int)
#	# First pass between non protein grid points and protein
#	dict_burial = set_burial_scandir(gridpoints, grid_solv, grid_protein, grid_min, grid_shape, radius_cube, gridspace)
#	whonotsolvent = [key for key, value in dict.items() if value >= 9] 
#	# Needs to be related to original order in grid_indices
#	ori_whonotsolv = grid_solv[whonotsolvent]
#	solvent_around = np.setdiff1d(grid_solv, ori_whonotsolv, assume_unique = True)
#
#	# Second pass between potential solvent points and potential
#	# grid points (for finding 'middle points')
#
#	list_secondpass = set_burial(gridpoints[solvent_around], gridpoints[ori_whonotsolv]
#		, secondpass_shell)
#	# The indices in list_secondpass are indices in solvent_around. Is it?
#	# One needs to convert from solvent_around to go back to indices from gridpoints
#	whonotsolvent2 = np.nonzero(list_secondpass > min_secondpass_contacts)[0]
#	# Needs to be related to original order in grid_indices
#	ori_whonotsolv2 = solvent_around[whonotsolvent2]
#	solvent_around_2 = np.setdiff1d(grid_solv, ori_whonotsolv2, assume_unique = True)
#
#	all_potential_cavity_points = np.unique(np.concatenate((ori_whonotsolv, ori_whonotsolv2)))
#	all_solvent_around = np.unique(np.concatenate((solvent_around, solvent_around_2)))
#
#	return all_potential_cavity_points, all_solvent_around

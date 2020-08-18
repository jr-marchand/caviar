# -*- coding: utf-8 -*-
"""
This module contains grid related tools.
"""

from caviar.prody_parser.atomic.atomgroup import AtomGroup
from .geometry import SetOfPoints
import numpy as np

__all__ = ['build_grid', 'get_index_of_coor', 'get_index_of_coor_list', 'list_transform_indices', 'list_transform_indices2',
			'get_transformation_vectors']


def build_grid(atomgroup, boxmargin = 2.0, gridspace = 1.0, size_limit = 10000000):
	"""
	Build the grid around the chains of interest within
	boxmargin (5A) and a gridspace (1A)
	Takes as input an array of coordinates
	Returns the grid points, the shape of the grid, and the
	minimum coordinates
	"""
	atoms = SetOfPoints(atomgroup) # protein
	max_coord, min_coord = atoms.get_coord_range()
	grid_min = min_coord - boxmargin
	grid_max = max_coord + boxmargin
	# nx, ny, nz = grid_max - grid_min
	# printv("> Grid of "+str(nx)+" x "+str(ny)+" x "+str(nz)+" = "+str(nx*ny*nz)
	#	   + " cubic angstroms")
	# Generate the grid points from coordinate min to coordinate
	# max in x, y, z direction with the spacing gridspace
	grid_x = np.arange(grid_min[0], np.ceil(grid_max[0]), gridspace) # np.ceil to get a value slightly above and get the last one
	grid_y = np.arange(grid_min[1], np.ceil(grid_max[1]), gridspace) # np.ceil to get a value slightly above and get the last one
	grid_z = np.arange(grid_min[2], np.ceil(grid_max[2]), gridspace) # np.ceil to get a value slightly above and get the last one
	grid_shape = (len(grid_x), len(grid_y), len(grid_z))
	if size_limit: # kill everything is the protein is too big: that may happen with some cryoEM structures
	# it's not really relevant to work on multi protein complexes blindly
	# 10m grid points is about 13 gb in memory max use
		grid_size = len(grid_x)*len(grid_y)*len(grid_z)
		if grid_size > int(size_limit):
			return None, None, None
	# Combine the 3 lists into a grid
	grid_noform = np.meshgrid(grid_x, grid_y, grid_z, indexing = "ij")
	# There may be a better way to do this
	# Now we reshape each dimension of the grid so that we can
	# stack them
	x = grid_noform[0].reshape(-1,1)
	y = grid_noform[1].reshape(-1,1)
	z = grid_noform[2].reshape(-1,1)
	# Stack
	grid = np.hstack((x,y,z))
	return grid, grid_shape, grid_min

def get_index_of_coor(point_coor, grid_min, grid_shape, gridspace = 1.0):
	"""
	Returns the index in the grid object corresponding to a 
	grid point coordinate
	Should double check the effect of a grid space which is not 1A
	Useful for finding characteristics of neighbors of a point
	without calculating all distances
	"""
	position = (point_coor - grid_min) * 1/gridspace # this should be gridspace proof
	#print(position, point_coor, grid_min)
	indice = position[0]*grid_shape[1]*grid_shape[2] + position[1]*grid_shape[2] + position[2]
	if indice >= 0:
		return round(indice)
	else:
		return int(-1)

def get_index_of_coor_list(point_coor_list, grid_min, grid_shape, gridspace = 1.0):
	"""
	Performs the function above on a list of coordinates, returns
	a list of indices
	"""
	positions = (point_coor_list - grid_min) * 1/gridspace
	tmpindices = positions[:,0]*grid_shape[1]*grid_shape[2] + positions[:,1]*grid_shape[2] + positions[:,2]
	indices = np.array(tmpindices[tmpindices >= 0], dtype='i')
	
	return indices


def list_transform_indices(transform_vectors, grid_shape):
	"""
	Equivalent of get_index_of_coor to find the indice of a transformation
	vector in relative space without going through cartesian coordinates space
	Used in set_burial_gridscan, notably. 
	Returns a list of lists
	"""
	transform_ind = []
	for vectors in transform_vectors:
		tmplist = []
		for vec in vectors:
			tmplist.append(round(vec[0]*grid_shape[1]*grid_shape[2] + vec[1]*grid_shape[2] + vec[2]))
		transform_ind.append(tmplist)
	return transform_ind

def list_transform_indices2(transform_vectors, grid_shape):
	"""
	Same as previous but simply for a list of vectors and not a list of lists
	"""
	transform_ind = []
	for vectors in transform_vectors:
		transform_ind.append(round(vectors[0]*grid_shape[1]*grid_shape[2] + vectors[1]*grid_shape[2] + vectors[2]))
	return transform_ind

def get_transformation_vectors(radius_cube, startingpoint = 3):
	"""
	Generate the list of transformation vectors to investigate the 14 cubic directions around
	a grid point. Generates a list of 14 lists, each sublist containing the transformation vectors
	of 1 direction between 3A and radius_cube A.
	Deletion of mention to gridspace, because here it is not needed. We can to scan between
	3A and xA for protein points, there is no point in thinking in "grid points" rather than 
	distance
	"""
	directions = [[0, 0, 1], [0, 1, 0], [1, 0, 0], [1, 1, 1], [-1, 1, 1], [1, -1, 1], [1, 1, -1],
	[0, 0, -1], [0, -1, 0], [-1, 0, 0], [-1, -1, -1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]
	biglist = []
	for coor in directions:
		tmplist = []
		for rad in range(startingpoint, radius_cube+1):
			tmplist.append([rad*coor[x] for x in range(0,3)])
		biglist.append(tmplist)
	
	transform_vectors = np.array(biglist)
	return transform_vectors


################################
#### DEPRECATED FUNCTIONS ######
################################

# def in_range_from_matrix(all_dist, dist_range):
# 	"""
# 	Parses the matrix generated by geometry.dist_allvall to return
# 	the correspondance list of who's within dist_range of who
# 	"""
# 	whoinrange = np.nonzero(all_dist < dist_range)
# 	return whoinrange
# 
# def build_cube(point_coor, grid_min, grid_shape, onion_level = 1, gridspace = 1.0):
# 	"""
# 	Gets the list of grid points of the cube around a grid point
# 	Works on "onion_level", which represents the number of "gridspaces"
# 	around a point of interest we want to investigate (for the cubic FP)
# 	"""
# 	mincube = point_coor + onion_level*np.array([-1,-1,-1])
# 	maxcube = point_coor + onion_level*np.array([+1,+1,+1])
# 	cube_x = np.arange(mincube[0], maxcube[0]+1, gridspace)
# 	cube_y = np.arange(mincube[1], maxcube[1]+1, gridspace)
# 	cube_z = np.arange(mincube[2], maxcube[2]+1, gridspace)
# 	cube_noform = np.meshgrid(cube_x, cube_y, cube_z, indexing = "ij")
# 	# There may be a better way to do this
# 	# Now we reshape each dimension of the grid so that we can
# 	# stack them
# 	x = cube_noform[0].reshape(-1,1)
# 	y = cube_noform[1].reshape(-1,1)
# 	z = cube_noform[2].reshape(-1,1)
# 	# Stack
# 	cube = np.hstack((x,y,z))
# 	arr_cube_indices = np.array(get_index_of_coor_list(cube, grid_min, grid_shape))
# 	# Get the index of the center of the cube, ie the point we were investigating
# 	oripoint_index = int(len(arr_cube_indices)/2 -0.5)
# 	# And remove it from the list and the cube
# 	# Get None indices for non existing grid points
# 	nones = np.where(arr_cube_indices == -1)[0]
# 	nones_and_ori = np.append(nones, [oripoint_index])
# 	cube_indices = np.delete(arr_cube_indices, nones_and_ori, axis=0)
# 	cleancube = np.delete(cube, nones_and_ori, axis=0)
# 
# 	return cube_indices, cleancube
# 
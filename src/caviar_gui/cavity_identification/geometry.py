# -*- coding: utf-8 -*-
"""
This module defines some basic 3D functionalities
"""

import numpy as np
from numpy import linalg as LA
from scipy.spatial import distance
from scipy.spatial import cKDTree

__all__ = ['Point', 'Vector', 'SetOfPoints', 'calc_moments_of_inertia', 'calc_asphericity', 'calc_eccentricity',
            'calc_inertialshapefactor', 'rotate_pdb_via_prody']

class Point(object):
    
    """
    A class for working with 3D points.
    Takes as argument a np.array() (3D point, .reshape(-1,3))
    """

    def __init__(self, coords):
        self.coords = coords

    def __str__(self):
        return ' '.join(str(self.coords[i]) for i in range(3))

    def __arrayfrompoint___(self):
        return np.squeeze(self.coords)

    def dist(self, point):
        """
        Returns the distance between self and point
        """
        if type(point) == Point:
            array_point = point.__arrayfrompoint___()
        elif type(point) == np.ndarray:
            array_point = point
        else:
            print("Wrong type for second point (it should be a np.array or a Point)")
        return LA.norm(self.coords-array_point)

    def in_range(self, point, dist_range):
        """
        Returns true if point is within range of self
        """
        if type(point) == Point:
            array_point = point.__arrayfrompoint___()
        elif type(point) == np.ndarray:
            array_point = point
        else:
            print("Wrong type for second point (it should be a np.array or a Point)")
        distance = self.dist(array_point)
        if distance > dist_range:
            return False
        else:
            return True

    def direction(self, point):
        """
        Returns the normalized direction vector self ==> point.
        """
        if type(point) == Point:
            array_point = point.__arrayfrompoint___()
        elif type(point) == np.ndarray:
            array_point = point
        else:
            print("Wrong type for second point (it should be a np.array or a Point)")
        v = Vector(array_point - self.coords)
        return v.normalized().squeeze()

    def dist2(self, point):
        """
        Returns the squared distance between self and point
        """
        if type(point) == Point:
            array_point = point.__arrayfrompoint___()
        elif type(point) == np.ndarray:
            array_point = point
        else:
            print("Wrong type for second point (it should be a np.array or a Point)")
        return np.square(self.dist(array_point))


class Vector(object):

    """
    A class for working with vectors.
    Takes as argument a np.array() (3D vector) 
    """

    def __init__(self, vector):
        self.vector = vector.reshape(-1,3)

    def __arrayfromvec___(self):
        return np.squeeze(self.vector)

    def get_perpendicular(self, v):
        """
        Returns a vector perpendicular to the two vectors
        (ie, to the plan formed by self and v)
        """
        if type(v) == Vector:
            v_array = v.__arrayfromvec___()
        elif type(v) == np.ndarray:
            v_array = v
        else:
            print("Wrong type for second vector (it should be a np.array or a Vector)")
        w = np.cross(self.vector, v_array)
        return Vector(w).normalized().squeeze()

    def normalized(self):
        """
        Returns the normalized vector
        """
        norm = self.vector / LA.norm(self.vector)
        return norm.squeeze()

    def angle(self, v, oriented = True):
        """ 
        Returns the angle (in degree) between the vectors
        self and v. Please specify if oriented.
        """
        if type(v) == Vector:
            v_array = v.__arrayfromvec___()
        elif type(v) == np.ndarray:
            v_array = v
        else:
            print("Wrong type for second vector (it should be a np.array or a Vector)")
        cosang = np.dot(self.vector, v_array)
        sinang = LA.norm(np.cross(self.vector, v_array))
        if oriented:
            angl = np.arctan2(sinang, cosang)  # oriented
        else:
            angl = np.arctan2(np.absolute(sinang), cosang)  # non oriented
        return np.rad2deg(angl)


class SetOfPoints(object):
    
    """
    A class for working with numpy.array(), i.e., a 3D coordinate set.
    Is-a numpy.array(), and can take as input a getCoordsets() from
    ProDy parser
    """

    def __init__(self, setofcoord):
        self.setofcoord = setofcoord.reshape(-1,3)

    def __arrayfromset___(self):
        return self.setofcoord

    def get_coord_range(self):
        """
        Returns [xmax, ymax, zmax] from the set
        """
        return np.max(self.setofcoord, axis=0), np.min(self.setofcoord, axis=0)

    def in_range_set(self, point, dist_range, asbool = True):
        """
        Returns true if point is in dist_range of one of the coordinates of setofcoord
        If asbool = False, it returns an indices from self within dist_range of point
        This list corresponds to the indices in the original sets (up to the PDB parser
        object) and can be used to retrieved what atoms are in distance to point
        """
        if type(point) == Point:
            array_point = point.__arrayfrompoint___()
        elif type(point) == np.ndarray:
            array_point = point
        else:
            print("Wrong type for second point (it should be a np.array or a Point)")
        all_dist = distance.cdist(self.setofcoord, array_point.reshape(1,3))
        if asbool == True:
            min_dist = np.min(all_dist)
            if min_dist > float(dist_range):
                return False
            else:
                return True
        else:
            return list(np.nonzero(all_dist < dist_range)[0])


    def in_range_settoset(self, setofcoord, dist_range, asbool = True):
        """
        Returns true (if asbool = True) if a set of points is in dist_range of one of the
        coordinates of self (which itself is a set of points)
        Useful to check if two (protein) chains are within X angstroms
        """
        if type(setofcoord) == SetOfPoints:
            array_set = setofcoord.__arrayfromset___()
        elif type(setofcoord) == np.ndarray:
            array_set = setofcoord
        else:
            print("Wrong type for second point (it should be a np.array or a SetOfPoints)")
        all_dist = distance.cdist(self.setofcoord, array_set.reshape(-1,3))
        if asbool == True:
            min_dist = np.min(all_dist)
            if min_dist > float(dist_range):
                return False
            else:
                return True
        else:
            return np.nonzero(all_dist < dist_range)

    def dist_allvall(self, setofcoord):
        """
        Returns the distance of all coordinates of self versus all 
        coordinates of setofcoords.
        May overseed the 2 functions above
        """
        if type(setofcoord) == SetOfPoints:
            array_set = setofcoord.__arrayfromset___()
        elif type(setofcoord) == np.ndarray:
            array_set = setofcoord
        else:
            print("Wrong type for second point (it should be a np.array or a SetOfPoints)")
        all_dist = distance.cdist(self.setofcoord, array_set.reshape(-1,3))
        return all_dist

    def center(self):
        """
        Returns the mean value for x,y,z in setofcoord
        """
        return np.mean(self.setofcoord, axis=0) # may be an array


    def print_indices_within(self, setofcoord, max_distance, turnon = False):
        """
        Overseeds dist_allvall, in_range_set, in_range_settoset (probably)
        Uses cKDTree from scipy to generate a sparse matrix of distances
        Writes in memory only if within max_distance. Replaces cdist, which
        can't handle cases where there is too many points.
        Returns a list of indices from self that are within max_distance
        of setofcoord.
        """
        if type(setofcoord) == SetOfPoints:
            array_set = setofcoord.__arrayfromset___()
        elif type(setofcoord) == np.ndarray:
            array_set = setofcoord

        tree1 = cKDTree(self.setofcoord, compact_nodes = turnon, balanced_tree = turnon)
        tree2 = cKDTree(array_set, compact_nodes = turnon, balanced_tree = turnon)
        within = tree1.sparse_distance_matrix(tree2, max_distance = max_distance, output_type = "ndarray")
        #listtuples = list(within[["i","j"]])
        #list_indices_within = np.unique(within["i"])

        return within #list_indices_within, listtuples


def calc_moments_of_inertia(coords, origin):
    """
    
    Returns moments of inertia centered on origin
    If origin is the center of the coords, then 
    they are the PMI
    Else, they are moments of inertia centered at origin (well...)
    """
    # Center coordinates
    coords = coords - origin
    # Compute inertia terms
    xx = np.sum(coords[:,1]**2 + coords[:,2]**2)
    yy = np.sum(coords[:,0]**2 + coords[:,2]**2)
    zz = np.sum(coords[:,0]**2 + coords[:,1]**2)
    xy = - np.sum(coords[:,0] * coords[:,1])
    xz = - np.sum(coords[:,0] * coords[:,2])
    yz = - np.sum(coords[:,1] * coords[:,2])
    # Generate the inertia matrix
    matrix = np.vstack([[xx, xy, xz],
                        [xy, yy, yz],
                        [xz, yz, zz]])
    moments, axes = LA.eig(matrix)
    return np.sort(moments)  # IA, IB, IC
    
def calc_asphericity(IA, IB, IC):
    """
    Anisometry descriptor for the deviation from the spherical shape
    0 = spherical
    1 = flat (linear or oblate/disk shaped)
    ~ 0.25 = prolate (cigar shaped)
    """
    asph = 0.5 * ( (IA - IB)**2 + (IA - IC)**2 + (IB - IC)**2 ) / (IA**2 + IB**2 + IC**2)
    return asph

def calc_eccentricity(IA, IB, IC):
    """
    Shape descriptor based on PMI
    0 = spherical
    1 = linear or oblate (disk shaped)
    """
    eccen = (IA**2 - IC**2)**0.5 / (IA)
    return eccen

def calc_inertialshapefactor(IA, IB, IC):
    """
    Shape descriptor based on PMI
    Cannot be calculated for plannar surfaces
    """
    Si = IB / (IA*IC)
    return Si






###################### HEREON SOME FUNCTION TO VALIDATE THE ALGORITHM, NOT TO 
########### BE USED ROUTINELY
##################### ie rotate coordinates, with or without prody
######### prody is useful because it can transform the whole object, keeping
##################### information on atom types and so on
###### Not all functions are exporter

def rotateY3D(coords, theta = 3.1415926):
    """
    Function used to investigate the influence of the grid orientation around the protein
    in the cavity detection/comparison algorithm.
    It rotates around the Y axis of an angle theta, in radian units
    Rotates a set of coordinates
    Source: https://petercollingridge.appspot.com/3D-tutorial/rotating-objects
    """

    sin_t = np.sin(theta)
    cos_t = np.cos(theta)
    
    rotated = np.array([coords[:,0]*cos_t - coords[:,2]*sin_t, coords[:,1], coords[:,2]*cos_t + coords[:,0]*sin_t]).T

    return rotated

def getrotationmatrix_Z3D(theta):
    """
    Function used to investigate the influence of the grid orientation around the protein
    in the cavity detection/comparison algorithm.
    It generates the rotation matrix (3,3) around the Z axis
    This one uses degrees as input instead of radianss 
    Source: https://en.wikipedia.org/wiki/Rotation_matrix
    To be used with prody_parser.measure import transform, unlike the previous function which works on coordinates sets
    """

    theta = np.deg2rad(theta)
    rot_matrix = np.array([np.cos(theta), -np.sin(theta), 0, np.sin(theta), np.cos(theta), 0, 0, 0, 1])

    return rot_matrix.reshape(3,3)

def rotate_pdb_via_prody(pdboject, theta = 30):
    """
    Rotates via prody the entire pdb object (with atom types, protein, ligands...)
    """
    from cavitome_gui.prody_parser.measure import transform

    rot_matrix = getrotationmatrix_Z3D(theta)
    transf_class = transform.Transformation(rot_matrix, np.array([0,0,0])) # here it also wants a translation matrix, which we dont care
    # Transformation is a class in prody_parser.measure.transform

    new_pdbobject = transform.applyTransformation(transf_class, pdboject)
    # applyTransformation is a function in the same package

    return new_pdbobject
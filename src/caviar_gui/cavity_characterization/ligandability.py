# -*- coding: utf-8 -*-
"""
This module aims at calculating descriptors for ligandability
and calculate said ligandability
Uses the same dataset as 10.1021/ci300184x and 10.1021/ci200454v
for the ML (ie, the non redundant druggability dataset NRDD)
We've tested several classifier with default parameters in sklearn 0.22.1:
sklearn.linear_model import LogisticRegression
sklearn.tree import DecisionTreeClassifier
sklearn.neighbors import KNeighborsClassifier
sklearn.discriminant_analysis import LinearDiscriminantAnalysis
sklearn.naive_bayes import GaussianNB, BernoulliNB, CategoricalNB, ComplementNB, MultinomialNB
sklearn.svm import SVC (tried different kernels, gamma, etc)

knn was best according to: precision (weighted 0.89, macro 0.91),
accuracy (0.86), recall(weighted 0.86, macro 0.82), f1-score (weighted 0.86, macro 0.84)
& MCC (0.73)

"""

import numpy as np
import os

__all__ = ['calculate_ligandability']

path = os.path.dirname(__file__)


def calculate_ligandability(cavities, cavid, scaler_pickle = path+"/scaler.pickle", knn_pickle = path+"/knn.pickle"):
	"""
	Uses pickled functions (from sklearn) to predict ligandability
	Not much really, just opens the files and apply predict_proba on the array of 27 descriptors
	"""

	def calculate_27descriptors(cavities, cavid):
		"""
		Side function, to use the data generated before and 
		export it as a 27 descriptor-array
		Quite ugly but it does the job and is not much of a computational overhead
		in comparison to cavity detection algo
		"""
		avgbur = np.mean([gp.bur for gp in cavities[cavid].gp])
		size = cavities[cavid].size
		# calculate distributions of buriedness
		bur8 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 8])/size
		bur9 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 9])/size
		bur10 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 10])/size
		bur11 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 11])/size
		bur12 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 12])/size
		bur13 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 13])/size
		bur14 = len([gp.bur for gp in cavities[cavid].gp if gp.bur == 14])/size
		# calculate distributions of pharmacophores
		f1 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 1])/size
		f2 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 2])/size
		f3 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 3])/size
		f4 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 4])/size
		f5 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 5])/size
		f6 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 6])/size
		f7 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 7])/size
		f8 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 8])/size
		f9 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 9])/size
		f10 = len([gp.pharma[0] for gp in cavities[cavid].gp if gp.pharma[0] == 10])/size
		fpolar = f3+f4+f5
		fcharged = f6+f7
		fother = f8+f9+f10
	
		arrayof27 = np.array([[size, cavities[cavid].score, len(cavities[cavid].residues),
			cavities[cavid].median_bur, cavities[cavid].bur_7thq, avgbur, cavities[cavid].hydrophobicity, bur8,
			bur9, bur10, bur11, bur12, bur13, bur14, f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, fpolar, fcharged, fother]])

		return arrayof27

	arrayof27 = calculate_27descriptors(cavities, cavid)

	import pickle

	pickled_datascaler = open(scaler_pickle,"rb")
	pickled_model = open(knn_pickle,"rb")
	
	datascaler = pickle.load(pickled_datascaler)
	model = pickle.load(pickled_model)

	predict_ligandability = model.predict_proba(datascaler.transform(arrayof27))[:,1]

	return predict_ligandability

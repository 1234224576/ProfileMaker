# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
from sklearn.cross_validation import StratifiedKFold
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
#http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC
#http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.KFold.html#sklearn.cross_validation.KFold
# http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html#sklearn.decomposition.PCA


def classify(X_train,X_test,y_train,y_test):


if __name__ == '__main__':

	data = np.loadtxt("train.csv",delimiter=",")
	# np.random.shuffle(data)
	scaler = StandardScaler()
	scaler.fit(data[:,:9])
	data[:,:9] = scaler.transform(data[:,:9])
	data_num = data.shape[0]

	X = data[:,:9]
	y = data[:,9:10].reshape(1,data_num)[0]

	skf = StratifiedKFold(y, n_folds=10)
	for train_index, test_index in skf:
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = y[train_index], y[test_index]
		classify(X_train,X_test,y_train,y_test)

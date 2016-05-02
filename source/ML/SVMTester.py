# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
from sklearn.cross_validation import StratifiedKFold
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib

class SVMTester:
	def __init__(self,C,gamma,data):
		self.C = C
		self.gamma = gamma
		self.data = data

	def preprocessing(self,isPCA=False,div=2,isPickel=False):
		data = self.data
		scaler = StandardScaler()
		scaler.fit(data[:,:13])

		if isPickel:
			joblib.dump(scaler,"StandardScaler.pkl")

		data[:,:13] = scaler.transform(data[:,:13])
		data_num = data.shape[0]

		X = data[:,:13]
		y = data[:,14:15].reshape(1,data_num)[0]
		if isPCA:
			pca = PCA(n_components=div)
			pca.fit(X)
			X = pca.transform(X)
		return (X,y)

	def experiment(self,X,y):
		skf = StratifiedKFold(y, n_folds=10)
		score = 0
		count = 0
		for train_index, test_index in skf:
			count += 1
			X_train, X_test = X[train_index], X[test_index]
			y_train, y_test = y[train_index], y[test_index]
			score += self.classify(X_train,X_test,y_train,y_test)
		score /= 10.0
		return score

	def classify(self,X_train,X_test,y_train,y_test):
		clf = SVC(C=self.C,kernel="rbf",gamma=self.gamma)
		clf.fit(X_train,y_train)

		return clf.score(X_test,y_test)

	def createPickel(self,filename):
		X,y = self.preprocessing(isPCA=False,isPickel=False)

		clf = SVC(C=self.C,kernel="rbf",gamma=self.gamma)
		clf.fit(X,y)
		joblib.dump(clf,filename)


	# def draw(clf,X,X_test,y,y_test):
		# 	h = .02
		# 	x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
		# 	y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
		# 	xx, yy = np.meshgrid(np.arange(x_min, x_max, h),np.arange(y_min, y_max, h))

		# 	Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

		# 	Z = Z.reshape(xx.shape)

		# 	plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)

		# 	plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired)
		# 	plt.xlabel('Sepal length')
		# 	plt.ylabel('Sepal width')
		# 	plt.xlim(xx.min(), xx.max())
		# 	plt.ylim(yy.min(), yy.max())
		# 	plt.xticks(())
		# 	plt.yticks(())
		# 	plt.show()
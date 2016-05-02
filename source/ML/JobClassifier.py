# -*- coding: utf-8 -*-
import numpy as np
from sklearn.cross_validation import StratifiedKFold
import SVMTester as sv
import math

data = np.loadtxt("train2.csv",delimiter=",")

tester = sv.SVMTester(C=16.0,gamma=0.000244,data=data)
tester.createPickel("./model/CatchCopyClassifier.pkl")
# max_score = 0
# best_c = 0
# best_gamma = 0

# recm_c = []
# recm_gamma = []

# for i in range(0,10):
# 	for j in range(-20,0):
# 		c = math.pow(2,i)
# 		gamma = math.pow(2,j)
# 		tester = sv.SVMTester(C=c,gamma=gamma,data=data)
# 		X,y = tester.preprocessing()
# 		score = tester.experiment(X,y)
# 		if score > max_score:
# 			max_score = score
# 			best_c = c
# 			best_gamma = gamma
# 		if score > 0.34:
# 			recm_c.append((c,gamma))

# 		print str(score)

# print("最適:C=%lf,gamma=%lf,正答率=%lf")%(best_c,best_gamma,max_score)
# print("おすすめCとガンマ:"+str(recm_c))

# def classify(X_train,X_test,y_train,y_test,isDrawGraph=False):
# 	clf = SVC(C=0.5,kernel="linear",degree=2)
# 	clf.fit(X_train,y_train)

# 	if isDrawGraph:
# 		draw(clf,X_train,X_test,y_train,y_test)
# 	return clf.score(X_test,y_test)

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

# if __name__ == '__main__':

# 	data = np.loadtxt("train.csv",delimiter=",")
# 	# np.random.shuffle(data)
# 	scaler = StandardScaler()
# 	scaler.fit(data[:,:9])
# 	data[:,:9] = scaler.transform(data[:,:9])
# 	data_num = data.shape[0]

# 	X = data[:,:9]
# 	y = data[:,9:10].reshape(1,data_num)[0]

# 	pca = PCA(n_components=2)
# 	pca.fit(X)
# 	X = pca.transform(X)

# 	skf = StratifiedKFold(y, n_folds=10)
# 	score = 0
# 	count = 0
# 	for train_index, test_index in skf:
# 		count += 1
# 		X_train, X_test = X[train_index], X[test_index]
# 		y_train, y_test = y[train_index], y[test_index]
# 		score += classify(X_train,X_test,y_train,y_test,(count==10))
# 	score /= 10.0
# 	print("平均正答率:"+str(score))


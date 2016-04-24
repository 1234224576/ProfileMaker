# -*- coding: utf-8 -*-
import os
import sys
from gevent.server import StreamServer
from mprpc import RPCServer
from sklearn.externals import joblib

class ClassifierServer(RPCServer):
	def predict(self,data):
		print(data)
		# scaler = joblib.load("./model/StandardScaler.pkl")
		# data[:13] = scaler.transform(data[:13])
		# X = data[:13]
		# clf = joblib.load("./model/JobClassifier.pkl")
		# #今は職業に関する予測値のみ返している
		# r = clf.predict(X)
		return 1

server = StreamServer(('127.0.0.1', 6000), ClassifierServer())
server.serve_forever()
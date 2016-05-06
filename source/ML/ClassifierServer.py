# -*- coding: utf-8 -*-
import os
import sys
from gevent.server import StreamServer
from mprpc import RPCServer
from sklearn.externals import joblib
import sqlite3
import SentenceMaker as sm

class ClassifierServer(RPCServer):
	def predict(self,data):
		scaler = joblib.load("./model/StandardScaler.pkl")
		data = data.split(",")
		data = [float(x) for x in data]
		data[:13] = scaler.transform(data[:13])
		X = data[:13]
		jobClf = joblib.load("./model/JobClassifier.pkl")
		copyClf = joblib.load("./model/CatchCopyClassifier.pkl")
		#今は職業に関する予測値のみ返している
		r = jobClf.predict(X)
		l = copyClf.predict(X)
		return [r[0],l[0]]

server = StreamServer(('127.0.0.1', 6000), ClassifierServer())
server.serve_forever()
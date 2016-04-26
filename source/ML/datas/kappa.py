#coding:utf-8
import numpy as np

nisinaka = {}
iwamoto = {}

for line in open('nisinaka.csv', 'r'):
	datas = line.split(",")
	nisinaka[datas[0]] = datas[1]
for line in open('iwamoto.csv', 'r'):
	datas = line.split(",")
	iwamoto[datas[0]] = datas[1]

box = [[0 for i in range(8)] for j in range(8)]
for i in range(2,101):
	try:
		a = int(nisinaka["face_"+str(i)+".jpg"]) - 1
		b = int(iwamoto["face_"+str(i)+".jpg"]) - 1
		box[a][b] += 1
	except Exception, e:
		print e

for i in range(801,900):
	try:
		a = int(nisinaka["face_"+str(i)+".jpg"]) - 1
		b = int(iwamoto["face_"+str(i)+".jpg"]) - 1
		box[a][b] += 1
	except Exception, e:
		print e

n = np.sum(box)
same = sum(np.diag(box))
row_sum = np.sum(box, axis=0)
col_sum = np.sum(box, axis=1)

alpha = float(same)/n
beta = 0
for i in range(0,8):
	beta += (float(row_sum[i])/n) * (float(col_sum[i])/n)

kappa = (alpha - beta)/(1 - beta)
print box
print kappa

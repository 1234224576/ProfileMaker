# -*- coding: utf-8 -*-
import os
import sys
import TFIDFCalculator
import sqlite3

calculator = TFIDFCalculator.TFIDFCalculator()

for i in range(1,105):
	index = "{0:03d}".format(i)
	filename = "./datas/PR_txt/" +index + ".txt"
	text = ""
	try:
		for line in open(filename, 'r'):
			text += line
		calculator.addSentence(text)
	except:
		print "err"

calculator.calc()

# f = open('./datas/tfidf_filter.txt', 'a')
# for sentence in calculator.tfidf:
# 	text = ""
# 	for tfidf in sentence:
# 		if len(tfidf[0]) > 9:
# 			text += tfidf[0] + ":" + str(tfidf[1]) +","
# 	text += "\n"
# 	f.write(text)
# f.close()

conn = sqlite3.connect('./profilemaker.db')
f = open('./datas/tfidf_filter.txt', 'a')

for sentence in calculator.tfidf:
	text = ""
	for tfidf in sentence:
		if len(tfidf[0]) > 9:
			try:
				sql = "insert into catchcopy values ('"+tfidf[0]+"')"
				conn.execute(sql)
				f.write(tfidf[0]+"\n")
			except:
				print "unique"
f.close()

conn.commit()
conn.close()


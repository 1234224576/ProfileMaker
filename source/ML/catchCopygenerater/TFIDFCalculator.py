# -*- coding: utf-8 -*-
import MeCab
import os

class TFIDFCalculator:
	def __init__(self,sentences = []):
		self._corpus = sentences
		self._tfCount = []
		self._idfCount = {}
		self.tfidf = []

	def addSentence(self,sentence):
		self._corpus.append(sentence)

	def _wordsAnalys(self,sentence):
		mt = MeCab.Tagger("mecabrc")
		res = mt.parseToNode(sentence)
		tfArray = {}
		while res:
			arr = res.feature.split(",")
			if arr[0] == "名詞":
				if res.surface in tfArray:
					tfArray[res.surface] += 1
				else:
					tfArray[res.surface] = 1
			res = res.next
		self._tfCount.append(tfArray)
	
	def _idfCalclator(self):
		for tfArray in self._tfCount:
			for word,tf in tfArray.items():
				if word in self._idfCount:
					self._idfCount[word] += tf
				else:
					self._idfCount[word] = tf

	def calc(self):
		for sentence in self._corpus:
			self._wordsAnalys(sentence)
		self._idfCalclator()

		for tfArray in self._tfCount:
			result = {}
			for word,tf in tfArray.items():
				result[word] = float(tf) / float(self._idfCount[word])
			result = sorted(result.items(), key=lambda x: x[1],reverse=True)
			self.tfidf.append(result)
		return self.tfidf

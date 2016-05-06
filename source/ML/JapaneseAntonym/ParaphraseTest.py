#coding:utf-8
import word2vec
from JapaneseAntonym import JapaneseAntonym
import MeCab
import random

class TextChanger:
	def __init__(self,model,parts=["名詞"],threadhold=0.0,randomLimit=0):
		self.model = model
		self.mt = MeCab.Tagger("mecabrc")
		self.ja = JapaneseAntonym()
		self.parts = parts
		self.threadhold = threadhold
		self.randomLimit = randomLimit

	def setConvertPart(self,pats):
		self.parts.extend(parts)

	def setThreadhold(self,th):
		self.threadhold = th

	def setRandomLimit(self,rm):
		self.randomLimit = rm

	def _isAntonymWord(self,preword,afword):
		antonymWord = self.ja.getAntonym(preword)
		if afword in antonymWord:
			print preword+"＜ー＞"+antonymWord[0]+"\n"
			return True
		return False

	def changeText(self,target):
		res = self.mt.parseToNode(target)
		while res:
		    arr = res.feature.split(",")
		    if arr[0] in self.parts:
		    	try:
		    		rand = random.randint(0,self.randomLimit)
		    		words,sims = self.model.cosine(unicode(res.surface,'utf8'))
		    		word = self.model.vocab[words[rand]].encode('utf8')
		    		sim = sims[rand]
		    		if sim > self.threadhold and not self._isAntonymWord(res.surface,word):
		    			target = target.replace(res.surface,word)
		    	except Exception, e:
		    		print e
		    res = res.next
		return target

if __name__ == '__main__':
	model = word2vec.load('/Users/sowa/word2vec-read-only/wikipedia_corpus.bin')

	target = """御社の曽和修平という社員は真面目で良い好青年ですが、少々太りすぎではないでしょうか。"""

	tc = TextChanger(model,["名詞","動詞"],0.0,3)
	r = tc.changeText(target)
	print r
	print "========================"
	tc = TextChanger(model,["名詞","動詞"],0.5,5)
	r = tc.changeText(target)
	print r
	print "========================"
	tc = TextChanger(model,["名詞","動詞","助詞","連体詞","助動詞"],0.0,3)
	r = tc.changeText(target)
	print r
	print "========================"
	tc = TextChanger(model,["名詞","動詞","助詞","連体詞","助動詞"],0.7,0)
	r = tc.changeText(target)
	print r
	print "========================"
	tc = TextChanger(model,["名詞"],0.0,3)
	r = tc.changeText(target)
	print r
	print "========================"

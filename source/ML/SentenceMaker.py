# -*- coding: utf-8 -*- 
import random
import sqlite3

class SentenceMaker:
    def __init__(self):
        self.connector = sqlite3.connect("./profilemaker.db")
    # def createFirstSentence(self,copyNo):
    #     #aa

class FirstSentenceMaker:
    def __init__(self,connector,copyNo):
        self.connector = connector
        self.no = copyNo

    def getCatchCopy(self):
        cursor = connector.cursor()
        cursor.execute('select * from catchcopy where id = %d'%self.no)
        catchcopy = ""
        for row in cursor.fetchall():
            catchcopy = row[1]
        return catchcopy

    def createFirstSentence(self):
        cursor = connector.cursor()
        cursor.execute('select * from firstSentence where catchcopy_id = %d'%self.no)
        sentence = []
        for row in cursor.fetchall():
            sentence.append(row[2])
        return sentence[random.randint(0,2)]

if __name__ == "__main__":

    connector = sqlite3.connect("./profilemaker.db")
    print FirstSentenceMaker(connector,3).createFirstSentence()
    # cursor  = connector.cursor()
    # cursor.execute("select * from test_table order by code")
 
    # result = cursor.fetchall()

    # for row in result:
    #     print "===== Hit! ====="
    #     print "code -- " + unicode(row[0])
    #     print "name -- " + unicode(row[1])

    # cursor.close()
    connector.close()

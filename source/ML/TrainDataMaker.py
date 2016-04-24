# -*- coding: utf-8 -*-
import os
import sys
import urllib
import urllib2
import json
import time

response ={}

def createTrainData(img_name,job_id,catchcopy_id):
	try:
		url = "http://api.us.faceplusplus.com/detection/detect?api_key=54fe659b6b6484074e0d161226e8e441&api_secret=B-3Xcd1vEWras_OGkKnT5ROLfeZwKD3b"
		url += "&url=http://deeptoneworks.com/profilemaker/faces/"+img_name+"&attribute=glass,pose,gender,age,race,smiling"

		req = urllib2.Request(url)
		res = urllib2.urlopen(req)
		response["body"] = res.read()
		response["headers"] =  res.info().dict
		data = json.loads(response["body"])

		age = data["face"][0]["attribute"]["age"]["value"]
		gender = 0
		if data["face"][0]["attribute"]["gender"]["value"] == "Female":
			gender = 1
		smiling = data["face"][0]["attribute"]["smiling"]["value"]

		glass = 0
		if data["face"][0]["attribute"]["glass"]["value"] == "Normal":
			glass = 1
		elif data["face"][0]["attribute"]["glass"]["value"] == "Dark":
			glass = 2

		yaw = data["face"][0]["attribute"]["pose"]["yaw_angle"]["value"]
		pitch = data["face"][0]["attribute"]["pose"]["pitch_angle"]["value"]
		roll = data["face"][0]["attribute"]["pose"]["roll_angle"]["value"]

		eye_x = data["face"][0]["position"]["eye_right"]["x"] - data["face"][0]["position"]["eye_left"]["x"]
		eye_y = (data["face"][0]["position"]["eye_left"]["y"]+data["face"][0]["position"]["eye_right"]["y"])/2.0
		mouth_x = data["face"][0]["position"]["mouth_right"]["x"] - data["face"][0]["position"]["mouth_left"]["x"]
		mouth_y = (data["face"][0]["position"]["mouth_left"]["y"]+data["face"][0]["position"]["mouth_right"]["y"])/2.0
		nose_x = data["face"][0]["position"]["nose"]["x"]
		nose_y = data["face"][0]["position"]["nose"]["y"]

		result = str(age)+","+str(gender)+","+str(smiling)+","+str(glass)+","+str(yaw)+","+str(pitch)+","+str(roll)+","+str(eye_x)+","+str(eye_y)+","+str(mouth_x)+","+str(mouth_y)+","+str(nose_x)+","+str(nose_y)+","+str(job_id)+","+str(catchcopy_id)
		# print("age:%f,gender:%d,smiling:%f,eye_x:%f,eye_y:%f,mouth_x:%f,mouth_y:%f,nose_x:%f,nose_y:%f")%(age,gender,smiling,eye_x,eye_y,mouth_x,mouth_y,nose_x,nose_y)
		print("eye_x:%f,eye_y:%f,mouth_x:%f,mouth_y:%f,nose_x:%f,nose_y:%f")%(eye_x,eye_y,mouth_x,mouth_y,nose_x,nose_y)
	
		f = open('train2.csv', 'a')
		f.writelines(result+"\n")
		f.close()
	except Exception, e:
		print e

if __name__ == '__main__':
	filepath = "./datas/801_1600.txt"
	# filepath = "./datas/1_800.txt"
	f = open(filepath)
	for line in f.readlines():
		datas = line.split(",")
		img_name = datas[0]
		job_id = datas[1]
		catchcopy_id = datas[2].replace("\n","")
		createTrainData(img_name,job_id,catchcopy_id)
		time.sleep(1)

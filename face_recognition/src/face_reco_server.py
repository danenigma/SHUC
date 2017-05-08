#!/usr/bin/env python
#-*- coding:utf-8 -*-

import rospy
from service_tutorial.srv import FaceRecognition,FaceRecognitionResponse
class FaceRecognitionServer:
	NODE_NAME = "FaceRecognition"

	def __init__(self):
		rospy.init_node(self.NODE_NAME)
		service = rospy.Service('face_recognition', FaceRecognition, self.recognize)
	def recognize(self,request):
		result  = "hello"
		return FaceRecognitionResponse(result)

if __name__=="__main__":
	frs = FaceRecognitionServer()
	try:	
		rospy.spin()
	except:
		rospy.loginfo("error!!")



#!/usr/bin/env python
#-*- coding:utf-8 -*-

import rospy
from service_tutorial.srv import FaceRecognition
import sys
import cv2
from cv_bridge import CvBridge, CvBridgeError
class FaceRecognitionClient:
	NODE_NAME = "face_client"
	def __init__(self):
		rospy.init_node(self.NODE_NAME)
		rospy.wait_for_service('face_recognition')
		self.face_recognizer = rospy.ServiceProxy('face_recognition', FaceRecognition)
		
if __name__ == "__main__":
	frc = FaceRecognitionClient()
	img  = cv2.imread("/home/dan/Desktop/service_tutorial/catkin_ws/src/service_tutorial/src/my-passport-photo.jpg")
		
	bridge = CvBridge()
        try:
   	        cv_image = bridge.cv2_to_imgmsg(img, "bgr8")
		result =frc.face_recognizer(cv_image).result
		print result
        except CvBridgeError as e:
        	print(e)



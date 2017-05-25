#!/usr/bin/env python
#-*- coding:utf-8 -*-

import rospy
import cv2
import actionlib
from cv_bridge import CvBridge, CvBridgeError
from face_recognition_action.msg import FaceRecognitionAction,FaceRecognitionGoal, FaceRecognitionResult
import os
class FaceRecognitionClient():
	NODE_NAME = "face_recognition_client"
	def __init__(self):
		rospy.init_node(self.NODE_NAME)
		self.client = actionlib.SimpleActionClient('FaceRecognition', FaceRecognitionAction)
		self.client.wait_for_server()
		self.bridge = CvBridge()	
		self.largest_id_path = rospy.get_param('/face_recognition_action/largest_id_path','.')
		if os.path.exists(self.largest_id_path):
			self.largest_id = int(open(self.largest_id_path,'r').readline())	
		self.goal = FaceRecognitionGoal()
		self.goal.goal_type = "training"
		self.client.send_goal(self.goal,None)
		self.client.wait_for_result()
		rospy.logwarn(self.client.get_result())

		self.goal.goal_type= "add_new_person"
		self.goal.new_person_name = "daniel"
		self.goal.new_person_id   = str(self.largest_id+1)
		self.goal.number_of_examples = 50
		self.client.send_goal(self.goal,feedback_cb=self.feedback_cb)
		self.client.wait_for_result()
		rospy.logwarn(self.client.get_result())
		with open(self.largest_id_path,'w') as f:
			f.write(str(self.largest_id+1))

		self.goal.goal_type = "testing"
		self.client.send_goal(self.goal,None)
		self.client.wait_for_result()
		rospy.logwarn(self.client.get_result())

	def feedback_cb(self,data):
		rospy.logwarn(data)

if __name__ == "__main__":
	frc = FaceRecognitionClient()


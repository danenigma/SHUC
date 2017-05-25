#!/usr/bin/env python
#-*- coding:utf-8 -*-

import rospy
import cv2, os 
import numpy as np 
import csv
import pickle 
from util import *
from std_msgs.msg import Int8
from sensor_msgs.msg import Image
import time
import actionlib
from cv_bridge import CvBridge, CvBridgeError
from face_recognition_action.msg import FaceRecognitionAction,FaceRecognitionGoal, FaceRecognitionResult,FaceRecognitionFeedback
class FaceRecognition():
	NODE_NAME = 'face_recognition_lite'

	def __init__(self):

		rospy.init_node(self.NODE_NAME)
		
		self.train_path     = rospy.get_param("~train_path",'.') 
		self.test_path      = rospy.get_param("~test_path",'.') 

		self.model_path     = rospy.get_param("~model_path",'.') 
		self.num_training_examples = rospy.get_param("~num_training_examples",'50')
		self.confidence_value = rospy.get_param("~confidence_value",'100')
		self.face_pub 	    = rospy.Publisher("/face_recognition_lite/faces",Int8,queue_size=1)
		self.haar_path      = rospy.get_param("~cascadePath",'.')
		self.bridge  =  CvBridge()
		self.face_cascade = cv2.CascadeClassifier(self.haar_path)
		rospy.Subscriber('/camera/rgb/image_raw',Image,self.image_cb)
		self.image  = None
		self.recognizer     = cv2.createLBPHFaceRecognizer()
		self.id_to_names    = dict([name.split('.') for name in os.listdir(self.train_path)])
		self.bridge = CvBridge()
		self.result = FaceRecognitionResult()
		self.feedback = FaceRecognitionFeedback()
		try:
			self.recognizer.load(self.model_path)
			rospy.logwarn("recognizer already trained")
			rospy.logwarn(self.id_to_names)
			
		except:
			rospy.logwarn("there is no trained model")
			rospy.logwarn("trying to retrain......")
			try:					
				self.train()
			except:
				rospy.logwarn("no images in my database!!!!")
		time.sleep(2)
		self.server = actionlib.SimpleActionServer('FaceRecognition', FaceRecognitionAction, self.do_face_recognition, False)
		self.server.start()
		
	def do_face_recognition(self,goal):
		rospy.logwarn(goal.goal_type)
		if   goal.goal_type == "recognition":
			cv_face_image  = self.bridge.imgmsg_to_cv2(goal.face_image,"mono8")
			try:
				label,conf     = self.predict(cv_face_image)
				self.result.success = "successful"
				self.result.person_name = self.id_to_names[str(label)]
				self.result.confidence_value = conf
				self.server.set_succeeded(self.result)
			except:
				self.result.success = "recognition failed!!"
				self.server.set_succeeded(self.result)
		elif goal.goal_type == "training":
			try:
				self.train()
				self.result.success = "training done!!"
				self.server.set_succeeded(self.result)
			except:
				self.result.success = "training failed!! no images for training"
				self.server.set_succeeded(self.result)
				rospy.logwarn("training failed")
		elif goal.goal_type == "add_new_person":
			self.add_new_person(goal.new_person_name,goal.new_person_id,goal.number_of_examples)
			self.result.success = "adding new person done!!"
			self.server.set_succeeded(self.result)
		elif goal.goal_type == "testing":
			try:

				test_images,test_lables = self.get_training_images_and_labels(self.test_path)
				self.result.success  = "testing done!!"
				self.result.accuracy = self.test(test_images,test_lables)
				rospy.logwarn(self.result.accuracy)
				self.server.set_succeeded(self.result)
				self.result.accuracy = 0#to avoid latching
			except:
				self.result.success = "testing failed!!"
				self.server.set_succeeded(self.result)
		else:
			self.result.success = "wrong goal!!"
			self.server.set_succeeded(self.result)	
	def train(self):
		rospy.logwarn("recognizer not trained yet")
		rospy.logwarn("getting images and labels")
		
		training_images,training_labels = self.get_training_images_and_labels(self.train_path)
		rospy.logwarn("done!! getting images")
		rospy.logwarn("training.........")
		self.recognizer.train(training_images, training_labels)
		rospy.logwarn("done!!")
		self.recognizer.save(self.model_path)
	def update(self,images,labels):
		self.recognizer.update(images,labels)
		self.recognizer.save(self.model_path)	
	def predict(self,img):
		return self.recognizer.predict(img)

	def add_new_person(self,person_name,person_id,number_of_examples):
		self.face_count  = 0
		folder_name  = person_id+"."+ person_name
		if not os.path.exists(os.path.join(self.train_path,folder_name)):
			os.makedirs(os.path.join(self.train_path,folder_name))
		if not os.path.exists(os.path.join(self.test_path,folder_name)):
			os.makedirs(os.path.join(self.test_path,folder_name))	
		while self.face_count<number_of_examples:
			
			if self.image is not None:
				face_image = self.detect_face(self.image)
				rospy.logwarn("getting face images")
				if face_image is not None:
				
					image_name  = str(self.face_count)+'.jpg'
					if self.face_count<0.8*number_of_examples:
						image_path  = os.path.join(self.train_path,folder_name,image_name)
					else:
						image_path  = os.path.join(self.test_path,folder_name,image_name)
					
					cv2.imwrite(image_path,face_image)		
					self.face_count+=1
					rospy.logwarn("face_count: "+ str(self.face_count))
					self.feedback.number_of_faces_gathered = str(self.face_count)
					self.server.publish_feedback(self.feedback)	
				else:
					self.feedback.number_of_faces_gathered = "no face detected"
					rospy.logwarn("no face detected!!")
		self.face_count = 0
		rospy.logwarn("done!!")
		new_images,new_labels = self.extract_images_and_labels(person_name,person_id,self.train_path)
		self.update(new_images,np.array(new_labels))
	def test(self,test_images,test_lables):
		number_of_correct  = 0
		for index in range (len(test_lables)):
			nbr_predicted, conf = self.recognizer.predict(test_images[index]) 
			if nbr_predicted ==test_lables[index]: 
				rospy.logwarn("{} is Correctly Recognized with confidence {}".format(test_lables[index], conf))
				number_of_correct+=1
			else:
	 
				rospy.logwarn("{} is Incorrectly Recognized as {}".format(test_lables[index], nbr_predicted)) 

		return (number_of_correct*1./len(test_lables))*100	
	def extract_images_and_labels(self,person_name,person_id,path):
		folder_name = person_id+'.'+person_name
		imgs = [os.path.join(path+'/'+folder_name+'/',d) for d in os.listdir(os.path.join(path,folder_name))]
		images = [cv2.cvtColor(cv2.imread(img),cv2.COLOR_BGR2GRAY) for img in imgs]
		labels = len(images)*[int(person_id)]
		return images,labels
	def get_training_images_and_labels(self,path):
		all_images = []
		all_labels = []
		self.id_to_names    = dict([name.split('.') for name in os.listdir(path)])
		for key,value in self.id_to_names.items():
			person_name   =  key+'.'+value
			images,labels = self.extract_images_and_labels(value,key,path)
			all_labels +=labels
			all_images +=images
		return all_images,np.array(all_labels)
	def detect_face(self,img):	
		img   =  cv2.equalizeHist(img)	
		faces =  self.face_cascade.detectMultiScale(img, 1.3, 5)
		if len(faces)==1:
			(x,y,w,h) = faces[0]
			draw = 	img[y: y + h, x: x + w].copy()	
			return img[y: y + h, x: x + w]
		else:
			return None
	def image_cb(self,img):

		self.image = cv2.cvtColor(self.bridge.imgmsg_to_cv2(img,'rgb8'),cv2.COLOR_RGB2GRAY)

if __name__=="__main__":
	fr = FaceRecognition()

	try:
		rospy.spin()
	except:
		rospy.logwarn("error!!! ")

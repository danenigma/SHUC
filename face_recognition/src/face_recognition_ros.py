#!/usr/bin/env python2
#
# Example to run classifier on webcam stream.
# Brandon Amos & Vijayenthiran
# 2016/06/21
#
# Copyright 2015-2016 Carnegie Mellon University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is  on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Contrib: Vijayenthiran
# This example file shows to run a classifier on webcam stream. You need to
# run the classifier.py to generate classifier with your own dataset.
# To run this file from the openface home dir:
# ./demo/classifier_webcam.py <path-to-your-classifier>


import time
import cv2
import os
import pickle
import numpy as np
from sklearn.mixture import GMM
import openface
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg  import Image
from service_tutorial.srv import FaceRecognition,FaceRecognitionResponse
class FaceRecognitionServer():
	NODE_NAME = "face_recogntion"
	def __init__(self):
		rospy.init_node(self.NODE_NAME)
		self.fileDir = os.path.dirname(os.path.realpath(__file__))
		self.modelDir = os.path.join(self.fileDir, 'models')
		self.dlibModelDir = os.path.join(self.modelDir, 'dlib')
		self.openfaceModelDir = os.path.join(self.modelDir, 'openface')
		self.start = time.time()
		self.bridge 	  = CvBridge()
		self.imgDim        = 96
		self.width         = 320
		self.height        = 240
		self.captureDevice = 0
		self.threshold     = 0.5

		np.set_printoptions(precision=2)
		self.service = rospy.Service('face_recognition', FaceRecognition, self.recognize)
		
		self.align = openface.AlignDlib(os.path.join(
		    self.dlibModelDir,
		    "shape_predictor_68_face_landmarks.dat"))
		self.net = openface.TorchNeuralNet(
		os.path.join(
		    self.openfaceModelDir,
		    'nn4.small2.v1.t7'),
		imgDim=self.imgDim)
	        self.classifierModel = os.path.join(self.modelDir, 'trained','classifier.pkl')
	        with open(self.classifierModel, 'r') as f:
			(self.le, self.clf) = pickle.load(f)  # le - label and clf - classifer
		#self.face_reco_pub = rospy.Publisher("/face_recogntion/faces",String,queue_size=1)
	def recognize(self,request):

		self.cv_image   = self.bridge.imgmsg_to_cv2(request.img, "bgr8")
		persons, confidences = self.infer(self.cv_image)
		print "P: " + str(persons) + " C: " + str(confidences)
		try:
		    confidenceList.append('%.2f' % confidences[0])
		except:
		    pass
		for i, c in enumerate(confidences):
		    if c <= self.threshold:  # 0.5 is kept as threshold for known face.
			persons[i] = "_unknown"
		result = persons[0]
		return FaceRecognitionResponse(result)
	def getRep(self,bgrImg):
	    self.start = time.time()
	    if bgrImg is None:
		raise Exception("Unable to load image/frame")
	    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
	    if 1:
		print("  + Original size: {}".format(rgbImg.shape))
	    if 1:
		print("Loading the image took {} seconds.".format(time.time() - self.start))
	    self.start = time.time()
	    bb = self.align.getAllFaceBoundingBoxes(rgbImg)
	    
	    if bb is None:
		return None
	    if 1:
		print("Face detection took {} seconds.".format(time.time() - self.start))
	    self.start = time.time()
	    alignedFaces = []
	    for box in bb:
		alignedFaces.append(
		    self.align.align(
		        self.imgDim,
		        rgbImg,
		        box,
		        landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE))

	    if alignedFaces is None:
		raise Exception("Unable to align the frame")
	    if 1:
		print("Alignment took {} seconds.".format(time.time() - self.start))
	    self.start = time.time()
	    reps = []
	    for alignedFace in alignedFaces:
		reps.append(self.net.forward(alignedFace))
	    if 1:
		print("Neural network forward pass took {} seconds.".format(
		    time.time() - self.start))
	    return reps
	def infer(self,img):
	    reps = self.getRep(img)
	    persons = []
	    confidences = []
	    for rep in reps:
		try:
		    rep = rep.reshape(1, -1)
		except:
		    print "No Face detected"
		    return (None, None)
		self.start = time.time()
		predictions = self.clf.predict_proba(rep).ravel()
		maxI = np.argmax(predictions)
		persons.append(self.le.inverse_transform(maxI))
		confidences.append(predictions[maxI])        
		print("Prediction took {} seconds.".format(time.time() - self.start))
		if isinstance(self.clf, GMM):
		    dist = np.linalg.norm(rep - self.clf.means_[maxI])
		    print("  + Distance from the mean: {}".format(dist))
		    pass
	    return (persons, confidences)


if __name__ == '__main__':
	fr = FaceRecognitionServer()
	try:
		rospy.spin()
	except:
		rospy.loginfo("error!!")

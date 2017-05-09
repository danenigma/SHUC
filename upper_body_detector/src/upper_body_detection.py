#!/usr/bin/env python
#-*- coding:utf-8 -*-
import rospy
import cv2 
from sensor_msgs.msg  import Image
from upper_body_detector.msg import Ubodies
from sensor_msgs.msg import RegionOfInterest
from cv_bridge import CvBridge, CvBridgeError

class UpperBodyDetector:
	NODE_NAME = "upper_body_detector"
	def __init__(self):
		rospy.init_node(self.NODE_NAME)
		self.cascade_path = rospy.get_param("~cascade_path",".")
		self.body_cascade = cv2.CascadeClassifier(self.cascade_path)
		self.ub_pub = rospy.Publisher("/upper_body_detector/u_bodies",Ubodies,queue_size=0)
		self.ub_image_pub = rospy.Publisher("/upper_body_detector/frame",Image,queue_size=0)
		self.sub    = rospy.Subscriber("/camera/rgb/image_raw",Image,self.image_cb)
		self.bridge = CvBridge()

	def image_cb(self,img):

		body_list = []
		cv_image = self.bridge.imgmsg_to_cv2(img, "bgr8")
		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)		
		bodies= self.body_cascade.detectMultiScale(gray, 1.3, 5)
		roi = RegionOfInterest()
		for body in bodies:
			roi.x_offset  = body[0] # Leftmost pixel of the ROI
			roi.y_offset  = body[1] # Topmost pixel of the ROI
      			roi.height    = body[2] # Height of ROI
			roi.width     = body[3]
			cv2.rectangle(cv_image,(body[0],body[1]),(body[0]+body[2],body[1]+body[3]),(0,0,255),15)
			body_list.append(roi)
		self.ub_image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
		self.ub_pub.publish(body_list)


if __name__ == "__main__":
	ubd = UpperBodyDetector()
	try:
		rospy.spin()
	except:
		rospy.loginfo("error!!")

#!/usr/bin/env python
#-*- coding:utf-8 -*-
import rospy
from std_msgs.msg import String


class ShucSoundSelector():
	NODE_NAME = "shuc_sound_selector"	
	def __init__(self):
		rospy.init_node(self.NODE_NAME)
		self.sound_pub = rospy.Publisher('/shuc_sound_selector/sound',String,queue_size=1)
		rospy.Subscriber("/shuc_emotion/audio_emotion",String,self.emotion_response_callback)
	def emotion_response_callback(self,emotion):
		self.sound_pub.publish(emotion.data)
	def run_test(self,param):
		self.sound_pub.publish(param)





if __name__=="__main__":
	sss = ShucSoundSelector()
	try:
		rospy.spin()
	except:
		rospy.loginfo("error "+sss.NODE_NAME)

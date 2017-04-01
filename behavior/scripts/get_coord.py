#!/usr/bin/env python
#-*- coding:utf-8 -*-


import rospy 
from std_msgs.msg import String
from geometry_msgs.msg import PoseWithCovarianceStamped
import pickle


class GetCoord:
	NODE_NAME = "remember_place"
	def __init__(self):
		rospy.init_node(self.NODE_NAME)
		self.get_it_sub = rospy.Subscriber('/get_it',String,self.get_it_callback)
		self.get_pos_sub = rospy.Subscriber('/amcl_pose',PoseWithCovarianceStamped,self.get_pos_callback)
		self.save_pos = None
		self.current_pos = None
	def get_it_callback(self,get_it):
		self.save_pos = get_it.data
		#open('src/shuk_gazebo/'+self.save_pos,'w').write(str(self.current_pos))
		print self.save_pos
		with open('src/shuk_gazebo/locations/'+self.save_pos+'.pickle', 'wb') as f:
			  pickle.dump(self.current_pos,f)
		print "dumping done!!!!"
	def get_pos_callback(self,pos):
		self.current_pos = pos


if __name__=="__main__":
	try:	
		g = GetCoord()
		rospy.spin()
	except:
		print "error get_coord"

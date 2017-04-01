#!/usr/bin/env python
#-*- coding:utf-8 -*-
import rospy
import actionlib
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from move_base_msgs.msg import *
import pickle
import os
class Goto():
	def __init__(self):
	    rospy.init_node('shuk_goto')
	    rospy.on_shutdown(self.shutdown)
	    self.sac = actionlib.SimpleActionClient('move_base', MoveBaseAction)
	     # Wait up to timeout seconds for the action server to become
	    try:
		self.sac.wait_for_server(rospy.Duration(3))
	    except: 
		rospy.loginfo("Timed out connecting to the action server "+ action)
	    self.goal = MoveBaseGoal()
	    self.go_to_cmd_sub = rospy.Subscriber('/go_to',String,self.go_to_callback)
	    self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
	    self.done_voice_pub= rospy.Publisher('/chatbot_responses',String,queue_size=1)
	    self.current_goal = None
	    self.setup_locations()
	    #print self.locations
	def go_to_callback(self,data):
	    #print "going to the " ,data.data
	    try:
		    #with open('src/shuk_gazebo/locations/'+ data.data + '.pickle', 'rb') as f:
		    pos = self.locations[data.data+'.pickle']
		    self.goal.target_pose.pose.position.x = pos.pose.pose.position.x
		    self.goal.target_pose.pose.orientation.w = pos.pose.pose.orientation.w
		    self.goal.target_pose.pose.position.y = pos.pose.pose.position.y
		    self.goal.target_pose.pose.orientation.z = pos.pose.pose.orientation.z	    
		    self.goal.target_pose.header.frame_id = 'map'
		    self.goal.target_pose.header.stamp = rospy.Time.now()
		    self.current_goal = data.data
		    self.done_voice_pub.publish('going to the ' + self.current_goal)
		    #start listner
		    self.sac.wait_for_server()

		    #send goal
		    self.sac.send_goal(self.goal, done_cb=self.done_cb)

		    #finish
		    self.sac.wait_for_result()

		    #print result
		   
	    except:
			rospy.loginfo('location unknown')
			self.done_voice_pub.publish('I do not know where that is')


	def done_cb(self,status,result):
		self.done_voice_pub.publish('i have reached the ' + self.current_goal)
	def setup_locations(self):
		self.locations = dict()
		self.path      = rospy.get_param("~locations_path")
		for filename in os.listdir(self.path):
			if filename.endswith(".pickle"):
				with open(self.path+filename,'rb') as f:
					pos = pickle.load(f)
					self.locations[filename]=pos
	def shutdown(self):
	        rospy.loginfo("Stopping the robot...")
	        self.sac.cancel_all_goals()
	        self.cmd_vel_pub.publish(Twist())
	        rospy.sleep(1)
	
if __name__ == '__main__':
    try:
        g = Goto()
	rospy.spin()
    except rospy.ROSInterruptException:
        print "Keyboard Interrupt"

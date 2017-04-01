#!/usr/bin/env python
#-*- coding:utf-8 -*-
__author__ = 'daniel'	
#flask imports
from flask import Flask,render_template,request

#ros imports
import roslib
from std_msgs.msg       import Int32,String,Float64,Header
from sensor_msgs.msg    import JointState
from android_server.msg import FaceControl
import rospy
#os imports
import socket
import fcntl
import struct


app = Flask(__name__)

############################helper func############################## 
def get_ip_address(ifname):
    """get ip address of interface"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

#####################################################################
@app.route('/speech/',methods=['POST'])
def speech():
	"""publish speech recognition output"""
	speech_pub.publish(request.form['text'])
	return render_template('robot.html')
@app.route('/cmd_vel/',methods=['POST'])
def android_cmd_vel():
	"""publish speech recognition output"""
	android_cmd_vel_pub.publish(request.form['text'])#[TODO MAY NEED PREPROCESSING]
	return render_template('robot.html')

@app.route('/face_control/',methods=['POST'])
def face_control():
	"""publish face configration"""
	face_config  = FaceControl()
	face_config.neck_servo_pan  = request.form['text']['neck_pan']
	face_config.neck_servo_tilt = request.form['text']['neck_tilt']
	face_config.eye_servo_pan   = request.form['text']['eye_pan']
	face_config.eye_servo_tilt  = request.form['text']['eye_tilt']
	face_control_pub.publish(face_config)

	return render_template('robot.html')

#######################################################################


#init node
rospy.init_node("android_server") 
#publishers
face_control_pub     = rospy.Publisher('/shuc/face_control',FaceControl,queue_size = 1)  
android_cmd_vel_pub  = rospy.Publisher('/android/cmd_vel',Int32,queue_size = 1)
speech_pub           = rospy.Publisher('/speech',String,queue_size = 1)  
#setup approprait port and ip
android_server_ip    = get_ip_address(rospy.get_param('~interface', 'wlan0'))
android_server_port  = rospy.get_param('~port',8000)

rospy.loginfo("WEB SERVER RUNNING ON THIS ADDRESS : "+ android_server_ip)
rospy.set_param('/web_video_server/address',android_server_ip)#for the video server

if __name__ == "__main__":
	app.run(debug = True,host=android_server_ip,port=int(android_server_port))
	



#!/usr/bin/env python
#-*- coding:utf-8 -*-
#!/usr/bin/env python
import rospy, os, sys
from sound_play.msg import SoundRequest
from sound_play.libsoundplay import SoundClient
from std_msgs.msg import String

class ShucSoundPlayer():
	NODE_NAME = "shuc_sound_player"	
	def __init__(self):
		rospy.init_node(self.NODE_NAME)
		# directory with sound assets - change as needed
		self.soundAssets = '/home/dan/Desktop/audio/catkin_ws/src/shuc_audio/audio/'#change 
		# duration of yak throttle
		self.throttle = 3 # seconds
		self.soundhandle = SoundClient()
    		rospy.Subscriber('/shuc_sound_selector/sound', String, self.sound_translator)
		self.allow_yak = rospy.Time.now()
	def sound_translator(self,data):
	    if rospy.Time.now() <= self.allow_yak: # Throttles yak to avoid
		print("Sound throttled")      # SoundClient segfault
		return
	    self.allow_yak = rospy.Time.now() + rospy.Duration.from_sec(self.throttle)
	    self.soundhandle.playWave(self.soundAssets + data.data)

if __name__ == '__main__':
    ssp = ShucSoundPlayer()
    rospy.sleep(1)
    try:
	rospy.spin()
    except:
	rospy.loginfo("error: "+ssp.NODE_NAME)
   

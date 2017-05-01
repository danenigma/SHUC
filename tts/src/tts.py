#!/usr/bin/env python
#-*- coding:utf-8 -*-


import rospy
import festival
from espeak import espeak
import subprocess
from std_msgs.msg import String

class Tts():
	NODE_NAME = 'tts'
	def __init__(self):
		rospy.init_node(self.NODE_NAME)
		self.sub = rospy.Subscriber('/tts_mux',String,self.tts_callback)
		self.tts_type = rospy.get_param("~tts_type","espeak")
		if self.tts_type=="espeak":
			espeak.set_voice("en")

	def tts_callback(self,text):
		rospy.logwarn(text.data)
		if self.tts_type=="espeak":
			espeak.synth(text.data)
		elif self.tts_type=="festival":
			festival.sayText(txt)
		elif self.tts_type=="mimic":
			subprocess.call(["mimic", "-t", txt])
		else:
			rospy.logwarn("PLEASE SELECT A TTS")

if __name__ == "__main__":
	t = Tts()
	try:
		rospy.spin()
	except:
		rospy.logwarn("TTS Error!")
			
"""
		self.tts = talkey.Talkey(
		preferred_languages=['en', 'af', 'el', 'fr'],
 		preferred_factor=80.0,

    		engine_preference=['espeak'],

    		espeak={
    	    # Specify the engine options:
    	    'options': {
    	        'enabled': True,
    		    },

    	    # Specify some default voice options
    	    'defaults': {
                'words_per_minute': 150,
                'variant': 'f4',
    		    },

	        'languages': {
	            'en': {
	                'voice': 'english-mb-en1',
	                'words_per_minute': 130
	        	    },
	        	}
	    		}
		)
"""


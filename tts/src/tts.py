#!/usr/bin/env python
#-*- coding:utf-8 -*-


import rospy
#import talkey
import espeak
from std_msgs.msg import String

class Tts():
	NODE_NAME = 'tts'
	def __init__(self):
		rospy.init_node(self.NODE_NAME)
		self.sub = rospy.Subscriber('/tts_mux',String,self.tts_callback)
		self.es  = espeak.ESpeak()
	def tts_callback(self,text):
		rospy.logwarn(text.data)
		self.es.say(text.data)

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


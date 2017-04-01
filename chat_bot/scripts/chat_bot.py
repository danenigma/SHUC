#!/usr/bin/env python

import aiml
import rospy
import os
import sys

from std_msgs.msg import String

class Chatbot():
  def __init__(self):
    self._kernel = aiml.Kernel()
    rospy.init_node('chat_bot')
    rospy.Subscriber('/chat_bot/chat_input', 
	String, 
	self._request_callback
    )
    self._response_publisher = rospy.Publisher(
   	'/chat_bot/speech_output',
    	String
	,queue_size =1
    )

  def initialize(self, aiml_dir):
    self._kernel.learn(os.sep.join([aiml_dir, '*.aiml']))
    properties_file = open(os.sep.join([aiml_dir, 'bot.properties']))
    for line in properties_file:
      parts = line.split('=')
      key = parts[0]
      value = parts[1]
      self._kernel.setBotPredicate(key, value)
    rospy.logwarn('Done initializing chatbot.')
    rospy.spin()
  def _request_callback(self, chat_message):
    response = self._kernel.respond(chat_message.data)
    self._response_publisher.publish(response)
def main():
  chatbot = Chatbot()
  aiml_dir = sys.argv[1]
  chatbot.initialize(aiml_dir)
    
if __name__ == '__main__':
  	main()

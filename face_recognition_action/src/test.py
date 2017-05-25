
import cv2
import numpy as np
import os
test_path = "/home/dan/Desktop/vision/my_vision/catkin_ws/src/face_recognition_action/dataset/test"
id_to_names    = dict([name.split('.') for name in os.listdir(test_path)])

def extract_images_and_labels(person_name,person_id):
		folder_name = person_id+'.'+person_name
		imgs = [os.path.join(test_path+'/'+folder_name+'/',d) for d in os.listdir(os.path.join(test_path,folder_name))]
		images = [cv2.cvtColor(cv2.imread(img),cv2.COLOR_BGR2GRAY) for img in imgs]
		labels = len(images)*[int(person_id)]
		return images,labels
def get_training_images_and_labels():
	training_images = []
	training_labels = []

	for key,value in id_to_names.items():
		person_name   =  key+'.'+value
		images,labels =  extract_images_and_labels(value,key)
		training_labels +=labels
		training_images +=images
	return training_images,np.array(training_labels)

training_images,training_labels = get_training_images_and_labels()

recognizer  = cv2.createLBPHFaceRecognizer()
recognizer.load("/home/dan/Desktop/vision/my_vision/catkin_ws/src/face_recognition_action/models/recognizer.yml")


def test(training_images,training_labels):
	number_of_correct  = 0
	for index in range (len(training_labels)):
	

		nbr_predicted, conf = recognizer.predict(training_images[index]) 
		if nbr_predicted == training_labels[index]: 
			print "{} is Correctly Recognized with confidence {}".format(training_labels[index], conf)
			number_of_correct+=1
		else:
 
			print "{} is Incorrectly Recognized as {}".format(training_labels[index], nbr_predicted) 


	return (number_of_correct*1./len(training_labels))*100

print test(training_images,training_labels)

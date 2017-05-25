import os
import csv
from PIL import Image
import numpy as np
import cv2


def csv_to_dict(csv_path):
	with open(csv_path) as f:
		records = csv.DictReader(f)
		for row in records:
			return row
def dict_to_csv(my_dict,csv_path):
	with open(csv_path, 'wb') as f: 
		w = csv.DictWriter(f, my_dict.keys())
		w.writeheader()
		w.writerow(my_dict)

def get_images_and_labels(path,faceCascade,str_labels):
	images = []
	labels = []	
	for f in os.listdir(path):
		folder_path =  [os.path.join(path, f)]
		for image_path in folder_path:
			imgs = [os.path.join(image_path, d) for d in os.listdir(image_path)]
			for img in imgs:
				image_pil = Image.open(img).convert('L') 
				image = np.array(image_pil, 'uint8') 
				nbr   = int(str_labels[f])
				faces = faceCascade.detectMultiScale(image) 
				for (x, y, w, h) in faces: 
					images.append(image[y: y + h, x: x + w]) 
					labels.append(nbr) 
#					cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w]) 
#					cv2.waitKey(50) 	
			
	return images,np.array(labels)


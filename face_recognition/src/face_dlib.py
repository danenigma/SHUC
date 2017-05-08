import cv2
import dlib

cap = cv2.VideoCapture(0)
win = dlib.image_window()
detector = dlib.get_frontal_face_detector()
while 1:
	_,img  = cap.read()
	if not _:continue
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	dets = detector(gray, 1)
	print "Number of faces detected: {}".format(len(dets))
	for i, d in enumerate(dets):
		print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
		i, d.left(), d.top(), d.right(), d.bottom()))

	cv2.imshow("image",gray)
	if cv2.waitKey(10)==ord('q'):
		break


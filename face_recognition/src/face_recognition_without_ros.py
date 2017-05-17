#!/usr/bin/env python2
#
# Example to run classifier on webcam stream.
# Brandon Amos & Vijayenthiran
# 2016/06/21
#
# Copyright 2015-2016 Carnegie Mellon University
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Contrib: Vijayenthiran
# This example file shows to run a classifier on webcam stream. You need to
# run the classifier.py to generate classifier with your own dataset.
# To run this file from the openface home dir:
# ./demo/classifier_webcam.py <path-to-your-classifier>


import time
import cv2
import os
import pickle
import numpy as np
from sklearn.mixture import GMM
import openface

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')

start = time.time()
np.set_printoptions(precision=2)

def getRep(bgrImg):
    start = time.time()
    if bgrImg is None:
        raise Exception("Unable to load image/frame")
    rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
    if 1:
        print("  + Original size: {}".format(rgbImg.shape))
    if 1:
        print("Loading the image took {} seconds.".format(time.time() - start))
    start = time.time()
    bb = align.getAllFaceBoundingBoxes(rgbImg)
    if bb is None:
        return None
    if 1:
        print("Face detection took {} seconds.".format(time.time() - start))
    start = time.time()
    alignedFaces = []
    for box in bb:
        alignedFaces.append(
            align.align(
                imgDim,
                rgbImg,
                box,
                landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE))

    if alignedFaces is None:
        raise Exception("Unable to align the frame")
    if 1:
        print("Alignment took {} seconds.".format(time.time() - start))
    start = time.time()
    reps = []
    for alignedFace in alignedFaces:
        reps.append(net.forward(alignedFace))
    if 1:
        print("Neural network forward pass took {} seconds.".format(
            time.time() - start))
    return reps
def infer(img):
    classifierModel = os.path.join(modelDir, 'trained','classifier.pkl')
    with open(classifierModel, 'r') as f:
        (le, clf) = pickle.load(f)  # le - label and clf - classifer
    reps = getRep(img)
    persons = []
    confidences = []
    for rep in reps:
        try:
            rep = rep.reshape(1, -1)
        except:
            print "No Face detected"
            return (None, None)
        start = time.time()
        predictions = clf.predict_proba(rep).ravel()
        maxI = np.argmax(predictions)
        persons.append(le.inverse_transform(maxI))
        confidences.append(predictions[maxI])        
        print("Prediction took {} seconds.".format(time.time() - start))
        if isinstance(clf, GMM):
            dist = np.linalg.norm(rep - clf.means_[maxI])
            print("  + Distance from the mean: {}".format(dist))
            pass
    return (persons, confidences)


if __name__ == '__main__':

    imgDim        = 96
    width         = 320
    height        = 240
    captureDevice = 0
    threshold     = 0.5

    align = openface.AlignDlib(os.path.join(
            dlibModelDir,
            "shape_predictor_68_face_landmarks.dat"))
    net = openface.TorchNeuralNet(
        os.path.join(
            openfaceModelDir,
            'nn4.small2.v1.t7'),
        imgDim=imgDim)

    video_capture = cv2.VideoCapture(captureDevice)
    video_capture.set(3, width)
    video_capture.set(4, height)
    confidenceList = []
    while True:
        ret, frame = video_capture.read()
        persons, confidences = infer(frame)
        print "P: " + str(persons) + " C: " + str(confidences)
        try:
            confidenceList.append('%.2f' % confidences[0])
        except:
            pass
        for i, c in enumerate(confidences):
            if c <= threshold:  # 0.5 is kept as threshold for known face.
                persons[i] = "_unknown"
        cv2.putText(frame, "P: {} C: {}".format(persons, confidences),
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.imshow('', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
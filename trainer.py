# this file gets all captured images from the dataSet folder in order to determine which ID belongs to which face.
import cv2
# to get the pictures, we need the relative path of the images, so use os library
import os
import numpy as np
# for images
from PIL import Image

#create a recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# to get all images at all levels create a method
def train_classifier(path):
    #from the dataSet folder, list all directories (images) and puts it to f then appends filename to the path and create a list
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    #create empty face list
    faceSamples=[]
    #create empty ID list
    Ids=[]
    #Loop through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #open the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Convert the PIL image into numpy array, OpenCV works with numpy arrays
        imageNp=np.array(pilImage,'uint8')
        #get the Id from the image by splitting the path using the last element , again with the dot split to get the ith index then convert into integer
        USERID=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces=detector.detectMultiScale(imageNp)
        #If a face is there then store that in the list as well as Id of it
        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(USERID)
    # return facesamples and Ids but first convert integer array to a numpy array
    return faceSamples, np.array(Ids)

faces,Ids = train_classifier('dataSet')
# train the recognizer using faces and Ids
recognizer.train(faces, Ids)
#save the recognizer to a folder in order to access it later
recognizer.save('trainner/trainner.yml')
#call the method
train_classifier("dataSet")
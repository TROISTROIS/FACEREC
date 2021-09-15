import cv2
import numpy as np

def detect_face():
    faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #capture images from live camera
    cam = cv2.VideoCapture(0)
    #create the recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    #load trained data to the recognizer using the path
    recognizer.read('trainner/trainner.yml')
    Id = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    while (True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceDetect.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (34, 197, 85), 3)
            # predict the id
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            # give name on the face
            if (conf < 90):
                if Id == 1:
                    Id = "FRANCISCA NGENO"

            else:
                Id = "Unknown"
            cv2.putText(img, str(Id), (x, y - 40), font, 0.7, (18, 8, 133), 2)
        cv2.imshow("Face", img)
        if (cv2.waitKey(1) == ord('q')):
            break
    cam.release()
    cv2.destroyAllWindows()
detect_face()
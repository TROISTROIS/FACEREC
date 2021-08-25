import tkinter as tk
from tkinter import messagebox
import mysql.connector
# this file gets all captured images from the dataSet folder in order to determine which ID belongs to which face.
import cv2

# to get the pictures, we need the relative path of the images, so use os library
import os
import numpy as np
# for images
from PIL import Image

from datetime import datetime
#create the main window and give it a name
root = tk.Tk()
root.title("FACE RECOGNITION SYSTEM")

head = tk.Label(root, text="Click the button below to mark your attendance using face recognition!!!",bg='#afeeee',font=('times', 17, ' bold ') )
head.place(x=40,y=0)


# Label and text field
l1 = tk.Label(root, text="LESSON ID", font=("Arial", 15), bg='#afeeee')
l1.place(x=0, y=60)
t1 = tk.Entry(root, bd=3, width=40, bg='#40e0d0')
t1.place(x=300, y=60, height=40)

# Button and action performed when the button(FACE DETECTION) is clicked. It generates a detects a face.
def detect_face():
    # if all the fields are not filled correctly, display the message or else generate a datset,.
    if (t1.get() == ""):
        messagebox.showinfo('Result', 'ENTER YOUR LESSON ID')
    else:
        faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # capture images from live camera
        cam = cv2.VideoCapture(0)
        # create the recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        # load trained data to the recognizer using the path
        recognizer.read('trainner/trainner.yml')
        font = cv2.FONT_HERSHEY_SIMPLEX
        while (True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = faceDetect.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (34, 197, 85), 3)
                USERID, conf = recognizer.predict(gray[y:y + h, x:x + w])
                # to collect the name of the user from the database
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="",
                    database="REGISTEREDSTUDENTS"
                )
                mycursor = mydb.cursor()
                mycursor.execute("SELECT STUDENTNAME FROM STUDENTDETAILS WHERE USERID=" + str(USERID))
                Name = mycursor.fetchone()
                # convert the name from tuple into string
                Name = '' + ''.join(Name)

                if conf > 81:
                    # write the extracted name
                    cv2.putText(img, Name, (x, y - 40), font, 0.7, (18, 8, 133), 2)

                    mycursor.execute("SELECT * FROM studentdetails WHERE STUDENTNAME = '%s'" % Name)
                    reg = mycursor.fetchone()[2]
                    print("REG NUMBER OF {Name} is {reg}")

                    mycursor.execute("SELECT * FROM attendance WHERE REGNUMBER='%s' AND LESSON_ID='%s'" % (reg,t1.get()))
                    x = mycursor.fetchall()
                    if not x:
                        sql = "INSERT INTO attendance(LESSON_ID, DATE,REGNUMBER ) values(%s,%s,%s)"
                        # values is extracted from input
                        val = (t1.get(), str(datetime.now().date()), reg)
                        mycursor.execute(sql, val)
                        mydb.commit()
                    else:
                        print("USER IS SAVED ALREADY...")
                        print(mycursor.fetchone())

                else:
                    # if it does not identify a user it prits "UNKNOWN"
                    cv2.putText(img, "UNKNOWN", (x, y - 40), font, 0.7, (18, 8, 133), 2)
                cv2.imshow("Face", img)
            if (cv2.waitKey(1) == ord('q')):
                break
        cam.release()
    cv2.destroyAllWindows()


b1 = tk.Button(root, text="FACE RECOGNITION", font=("Arial", 15), bg='#afeeee', command=detect_face)
b1.place(x=300, y=150, width=230)

head1 = tk.Label(root, text="Click the button below to register if you are a new student!!!",bg='#afeeee',font=('times', 17, ' bold ') )
head1.place(x=50,y=250)

def new_student():
    # create the main window and give it a name
    window = tk.Toplevel(root)
    window.title("STUDENT DETAILS")

    head = tk.Label(window, text="For New Registrations, fill in your details below !!!", bg='#afeeee',
                    font=('times', 17, ' bold '))
    head.grid(row=0, column=0)

    # Label and text field
    l1 = tk.Label(window, text="STUDENT NAME: ", font=("Arial", 15), bg='#afeeee')
    l1.place(x=0, y=60)
    t1 = tk.Entry(window, bd=3, width=40, bg='#40e0d0')
    t1.place(x=340, y=60, height=40)

    l2 = tk.Label(window, text="REGISTRATION NUMBER: ", font=("Arial", 15), bg='#afeeee')
    l2.place(x=0, y=120)
    t2 = tk.Entry(window, bd=3, width=40, bg='#40e0d0')
    t2.place(x=340, y=120, height=40)

    l3 = tk.Label(window, text="COURSE NAME:", font=("Arial", 15), bg='#afeeee')
    l3.place(x=0, y=180)
    t3 = tk.Entry(window, bd=3, width=40, bg='#40e0d0')
    t3.place(x=340, y=180, height=40)

    l4 = tk.Label(window, text="UNIT CODE: ", font=("Arial", 15), bg='#afeeee')
    l4.place(x=0, y=240)
    t4 = tk.Entry(window, bd=3, width=40, bg='#40e0d0')
    t4.place(x=340, y=240, height=40)

    # Button and action performed when the button(REGISTER YOUR FACE) is clicked. It generates a dataset.
    def generate_dataset():
        # if all the fields are not filled correctly, display the message or else generate a datset,.
        if (t1.get() == "" or t2.get() == "" or t3.get() == "" or t4.get() == ""):
            messagebox.showinfo('Result', 'Please fill in all the details')
        else:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",
                database="REGISTEREDSTUDENTS"
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM STUDENTDETAILS")
            myresult = mycursor.fetchall()
            # userid is gotten from row interval in the database , initial is set to 1
            USERID = 1
            for x in myresult:
                USERID += 1
            # table properties and values
            sql = "INSERT INTO STUDENTDETAILS(USERID,STUDENTNAME ,REGISTRATIONNUMBER,COURSENAME,UNITCODE) values(%s,%s,%s,%s,%s)"
            # values is extracted from input
            val = (USERID, t1.get(), t2.get(), t3.get(), t4.get())
            mycursor.execute(sql, val)
            mydb.commit()
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

            sampleNum = 0

            while True:
                # capture image
                ret, img = cam.read()
                # convert the image into grayscale because the viola-jones algorithm will segregate the image through the
                # brightness of a pixel from black to gray and white
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
                    # increment the sample number by one each time it detects a face
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("dataSet/User." + str(USERID) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                    # live frame from camera to show up
                    cv2.imshow('frame', img)

                # wait for 100 milliseconds to capture 100 images or quit the operation using "q"
                if cv2.waitKey(1) == 13 or int(sampleNum) == 100:
                    break
                # break if the sample number is more than 100
                #elif sampleNum > 100:
                    #break

            cam.release()
            cv2.destroyAllWindows()
            # show message on the screen
            messagebox.showinfo('Result', 'Dataset has been generated successfully!!!')

    b1 = tk.Button(window, text="REGISTER YOUR FACE", font=("Arial", 15), bg='#afeeee', command=generate_dataset)
    b1.place(x=150, y=350, width=280)

    def training():


        # create a recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        # to get all images at all levels create a method
        def train_classifier(path):
            # from the dataSet folder, list all directories (images) and puts it to f then appends filename to the path and create a list
            imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
            # create empty face list
            faceSamples = []
            # create empty ID list
            Ids = []
            # Loop through all the image paths and loading the Ids and the images
            for imagePath in imagePaths:
                # open the image and converting it to gray scale
                pilImage = Image.open(imagePath).convert('L')
                # Convert the PIL image into numpy array, OpenCV works with numpy arrays
                imageNp = np.array(pilImage, 'uint8')
                # get the Id from the image by splitting the path using the last element , again with the dot split to get the ith index then convert into integer
                USERID = int(os.path.split(imagePath)[-1].split(".")[1])
                # extract the face from the training image sample
                faces = detector.detectMultiScale(imageNp)
                # If a face is there then store that in the list as well as Id of it
                for (x, y, w, h) in faces:
                    faceSamples.append(imageNp[y:y + h, x:x + w])
                    Ids.append(USERID)
            # return facesamples and Ids but first convert integer array to a numpy array
            return faceSamples, np.array(Ids)

        faces, Ids = train_classifier('dataSet')
        # train the recognizer using faces and Ids
        recognizer.train(faces, Ids)
        # save the recognizer to a folder in order to access it later
        recognizer.save('trainner/trainner.yml')
        # call the method
        train_classifier("dataSet")
        messagebox.showinfo('Result', 'Your data has been trainned successfully!!!')


    b2 = tk.Button(window, text="TRAIN YOUR DATA", font=("Arial", 15), bg='#afeeee', command=training)
    b2.place(x=150, y=450, width=280)

    b3 = tk.Button(window, text="FACE RECOGNITION", font=("Arial", 15), bg='#afeeee', command=detect_face)
    b3.place(x=150, y=550, width=280)


    # set window size
    window.geometry("600x620")
    # set window color
    window['background'] = '#dda0dd'
    window.mainloop()


b4 = tk.Button(root, text="NEW STUDENT", font=("Arial", 15), bg='#afeeee', command=new_student)
b4.place(x=300, y=330, width=230)


# set window size
root.geometry("800x400")
# set window color
root['background'] = '#dda0dd'
root.mainloop()

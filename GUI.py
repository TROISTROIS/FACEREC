import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os
import mysql.connector
import cv2
import csv
import numpy as np
from PIL import Image
from datetime import datetime

#AskforQUIT
def on_closing():
    if messagebox.askyesno("Quit", "You are exiting window.Do you want to quit?"):
        window.destroy()
#contact
def contact():
    messagebox._show(title="Contact Me",message="If you have any questions contact me on 'siennefr@gmail.com'")

#about
def about():
    messagebox._show(title="About",message="This Attendance System is used to mark student attendance. A new student is required to register their details while a student who is already registered only needs to take the attendance. The Attendance will be marked and recorded in a csv file for the lecturer to see. ")

#clearbutton
def clear():
    txt.delete(0, 'end')
    txt2.delete(0, 'end')
    txt3.delete(0, 'end')
    txt4.delete(0, 'end')
    res = "1)Take Images  ===> 2)Save Profile"
    message.configure(text=res)

window = tkinter.Tk()
window.title("Face Recognition For Class Attendance")
window.geometry("1280x720")
window.resizable(True,True)
window.configure(background='#355454')

#Help menubar----------------------------------------------
menubar=Menu(window)
help=Menu(menubar,tearoff=0)
help.add_command(label="Contact Us",command=contact)
help.add_separator()
help.add_command(label="Exit",command=on_closing)
menubar.add_cascade(label="Help",menu=help)

# add ABOUT label to menubar-------------------------------
menubar.add_command(label="About",command=about)

#This line will attach our menu to window
window.config(menu=menubar)

#main window------------------------------------------------
message3 = tkinter.Label(window, text="Face Recognition For Class Attendance",fg="white",bg="#355454",width=60 ,height=1,font=('times', 29, ' bold '))
message3.place(x=10, y=10,relwidth=1)

#frames-------------------------------------------------
frame1 = tkinter.Frame(window, bg="white")
frame1.place(relx=0.11, rely=0.15, relwidth=0.39, relheight=4)

frame2 = tkinter.Frame(window, bg="white")
frame2.place(relx=0.55, rely=0.15, relwidth=0.39, relheight=0.80)

#frame_header
fr_head1 = tkinter.Label(frame1, text="Register New Student", fg="white",bg="black" ,font=('times', 17, ' bold ') )
fr_head1.place(x=0,y=0,relwidth=1)

fr_head2 = tkinter.Label(frame2, text="Mark Student's attendance", fg="white",bg="black" ,font=('times', 17, ' bold ') )
fr_head2.place(x=0,y=0,relwidth=1)

#registration frame
lbl = tkinter.Label(frame1, text="STUDENT NAME",width=20  ,height=1  ,fg="black"  ,bg="white" ,font=('times', 15, ' bold ') )
lbl.place(x=0, y=55)

txt = tkinter.Entry(frame1,width=32 ,fg="black",bg="#e1f2f2",highlightcolor="#00aeff",highlightthickness=3,font=('times', 15, ' bold '))
txt.place(x=55, y=88,relwidth=0.75)

lbl2 = tkinter.Label(frame1, text="REGISTRATION NUMBER",width=30  ,fg="black"  ,bg="white" ,font=('times', 15, ' bold '))
lbl2.place(x=0, y=140)

txt2 = tkinter.Entry(frame1,width=32 ,fg="black",bg="#e1f2f2",highlightcolor="#00aeff",highlightthickness=3,font=('times', 15, ' bold ')  )
txt2.place(x=55, y=173,relwidth=0.75)

lbl3 = tkinter.Label(frame1, text="COURSE NAME",width=20,fg="black"  ,bg="white" ,font=('times', 15, ' bold '))
lbl3.place(x=0, y=225)

txt3 = tkinter.Entry(frame1,width=32 ,fg="black",bg="#e1f2f2",highlightcolor="#00aeff",highlightthickness=3,font=('times', 15, ' bold ')  )
txt3.place(x=55, y=255,relwidth=0.75)

lbl4 = tkinter.Label(frame1, text="UNIT CODE",width=20  ,fg="black"  ,bg="white" ,font=('times', 15, ' bold '))
lbl4.place(x=0, y=310)

txt4 = tkinter.Entry(frame1,width=32 ,fg="black",bg="#e1f2f2",highlightcolor="#00aeff",highlightthickness=3,font=('times', 15, ' bold ')  )
txt4.place(x=55, y=340,relwidth=0.75)

message = tkinter.Label(frame1, text="" ,bg="white" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
message.place(x=0, y=590)


#BUTTONS----------------------------------------------

clearButton = tkinter.Button(frame1, text="Clear", command=clear, fg="white", bg="#13059c", width=11, activebackground = "white", font=('times', 12, ' bold '))
clearButton.place(x=55, y=390,relwidth=0.29)


def generate_dataset():
    # if all the fields are not filled correctly, display the message or else generate a dataset,.
    if (txt.get() == "" or txt2.get() == "" or txt3.get() == "" or txt4.get() == ""):
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
        val = (USERID, txt.get(), txt2.get(), txt3.get(), txt4.get())
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
            faces = detector.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # increment the sample number by one each time it detects a face
                sampleNum = sampleNum + 1
                # saving the captured face in the dataset folder
                cv2.imwrite("dataSet/User." + str(USERID) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                # live frame from camera to show up
                cv2.imshow('frame', img)

            # wait for 100 milliseconds to capture 100 images or quit the operation using "q"
            if cv2.waitKey(100)  & 0xFF == ord('q'):
                break
            # break if the sample number is more than 100
            elif sampleNum > 50:
                break

        cam.release()
        cv2.destroyAllWindows()
        # show message on the screen
        messagebox.showinfo('Result', 'Dataset has been generated successfully!!!')

takeImg = tkinter.Button(frame1, text="ADD FACE",command=generate_dataset,fg="black", bg="#00aeff", width=34, height=1, activebackground = "white", font=('times', 16, ' bold '))
takeImg.place(x=30, y=450,relwidth=0.89)


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

takeImg = tkinter.Button(frame1, text="TRAIN CLASSIFIER",command=training,fg="black", bg="#00aeff", width=34, height=1, activebackground = "white", font=('times', 16, ' bold '))
takeImg.place(x=30, y=500,relwidth=0.89)

def detect_face():
    # if all the fields are not filled correctly, display the message or else generate a dataset
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
            faces = faceDetect.detectMultiScale(gray, 1.2, 5)
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
                mycursor.execute("SELECT UNITCODE FROM STUDENTDETAILS WHERE USERID=" + str(USERID))
                unit = mycursor.fetchone()
                # convert the name from tuple into string
                unit = '' + ''.join(unit)
                mycursor.execute("SELECT * FROM studentdetails WHERE STUDENTNAME = '%s'" % Name)
                reg = mycursor.fetchone()[2]


                if (conf>71):
                    # write the extracted name
                    cv2.putText(img, Name, (x, y - 40), font, 0.7, (18, 8, 133), 2)
                    mycursor.execute("SELECT * FROM attendance WHERE REGNUMBER='%s' AND UNITCODE='%s' AND STUDENT_NAME='%s'" % (reg,unit,Name))
                    x = mycursor.fetchall()
                    #print attendance list using a table
                    style = ttk.Style()
                    style.configure("mystyle.Treeview", highlightthickness=0, bd=0,font=('Calibri', 11))
                    # Modify the font of the body
                    style.configure("mystyle.Treeview.Heading",font=('times', 13, 'bold'))
                    # Modify the font of the headings
                    style.layout("mystyle.Treeview",[('mystyle.Treeview.treearea', {'sticky': 'nswe'})])
                    # Remove the borders and choose frame

                    tb = ttk.Treeview(frame2,selectmode='browse',style="mystyle.Treeview")
                    #choose position for the table
                    tb.grid(row=1, column=1, padx=(30,0), pady=(150,0))
                    tb["columns"]=("1","2","3","4","5")
                    tb['show']='headings'
                    #table columns
                    tb.column("1", width=100)
                    tb.column("2", width=80)
                    tb.column("3", width=80)
                    tb.column("4", width=80)
                    tb.column("5", width=80)
                    #table headings
                    tb.heading("1", text='UNITCODE')
                    tb.heading("2", text='NAME')
                    tb.heading("3", text='REGNO')
                    tb.heading("4", text='DATE')
                    tb.heading("5", text='TIME')

                    #print values from the database in GUI
                    print(len(x))
                    for att in x:
                        tb.insert("",'end',iid=att[0],values=(att[0],att[1],att[2],att[3],att[4]))

                    if not x:
                        sql = "INSERT INTO attendance(UNITCODE,STUDENT_NAME,REGNUMBER,DATE,TIME) values(%s,%s,%s,%s,%s)"
                        # values is extracted from input
                        val = (unit,Name,reg,str(datetime.now().date()),str(datetime.now().time()))
                        mycursor.execute(sql, val)
                        mydb.commit()
                    else:
                        print(mycursor.fetchone())
                else:
                    # if it does not identify a user it prits "UNKNOWN"
                    cv2.putText(img, "UNKNOWN", (x, y - 40), font, 0.7, (18, 8, 133), 2)
                cv2.imshow("Face", img)
            if (cv2.waitKey(1) == ord('q')):
                break
        cam.release()
cv2.destroyAllWindows()

trackImg = tkinter.Button(frame2, text="Take Attendance", command=detect_face, fg="black", bg="#00aeff", height=1, activebackground = "white" ,font=('times', 16, ' bold '))
trackImg.place(x=30,y=60,relwidth=0.89)

def att():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="REGISTEREDSTUDENTS"
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM attendance")

    # To convert the data in the database into strings on the given object, use csv.writer() method.

    with open('attendance.csv', 'w', newline='\n') as f:
        writer = csv.writer(f)

        for row in mycursor.fetchall():
            writer.writerow(row)
    att()

#Viewatt = tkinter.Button(frame2, text="View Attendance", command=lambda: .insert(END,fetchstud), fg="black", bg="#00aeff",width=35, height=1,activebackground = "white",font=('times', 16, ' bold '))
#Viewatt.place(x=30,y=120,relwidth=0.89)

quitWindow = tkinter.Button(frame2, text="Quit", command=window.destroy, fg="white", bg="#13059c", width=35, height=1, activebackground = "white", font=('times', 16, ' bold '))
quitWindow.place(x=30, y=450,relwidth=0.89)

#closing lines------------------------------------------------
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
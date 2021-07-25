import tkinter as tk
from tkinter import messagebox
import cv2
import mysql.connector

from datetime import datetime

# create the main window and give it a name
window = tk.Tk()
window.title("FACE RECOGNITION SYSTEM")

head = tk.Label(window, text="Click the button below to mark your attendance using face recognition!!!",bg='#afeeee',font=('times', 17, ' bold ') )
head.place(x=40,y=0)

# Label and text field
l1 = tk.Label(window, text="LESSON ID", font=("Arial", 15), bg='#afeeee')
l1.place(x=0, y=60)
t1 = tk.Entry(window, bd=3, width=40, bg='#40e0d0')
t1.place(x=340, y=60, height=40)

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

                if (conf > 71):
                    # write the extracted name
                    cv2.putText(img, Name, (x, y - 40), font, 0.7, (18, 8, 133), 2)

                    mycursor.execute("SELECT * FROM studentdetails WHERE STUDENTNAME = '%s'" % Name)
                    reg = mycursor.fetchone()[2]
                    print(f"REG NUMBER OF {Name} is {reg}")

                    mycursor.execute("SELECT * FROM attendance WHERE REGNUMBER='%s' AND LESSON_ID='%s'" % (reg,t1.get()))
                    x = mycursor.fetchall()
                    if not x:
                        sql = "INSERT INTO attendance(LESSON_ID, DATE,REGNUMBER ) values(%s,%s,%s)"
                        # values is extracted from input
                        val = (t1.get(), str(datetime.now().date()), reg)
                        mycursor.execute(sql, val)
                        mydb.commit()
                    else:
                        print("USER IS SAVED ALREAD...")
                        print(mycursor.fetchone())

                else:
                    # if it does not identify a user it prits "UNKNOWN"
                    cv2.putText(img, "UNKNOWN", (x, y - 40), font, 0.7, (18, 8, 133), 2)
                cv2.imshow("Face", img)
            if (cv2.waitKey(1) == ord('q')):
                break
        cam.release()
    cv2.destroyAllWindows()


b1 = tk.Button(window, text="FACE RECOGNITION", font=("Arial", 15), bg='#afeeee', command=detect_face)
b1.place(x=300, y=150, width=230)

# set window size
window.geometry("800x300")
# set window color
window['background'] = '#dda0dd'
window.mainloop()

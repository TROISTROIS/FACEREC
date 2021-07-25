import tkinter as tk
from tkinter import messagebox
import cv2
import mysql.connector


# create the main window and give it a name
window = tk.Tk()
window.title("STUDENT DETAILS")

head = tk.Label(window, text="For New Registrations, fill in your details below !!!",bg='#afeeee',font=('times', 17, ' bold ') )
head.grid(row=0,column=0)

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

            # wait for 100 milliseconds to capture 20 images or quit the operation using "q"
            if cv2.waitKey(1) == 13 or int(sampleNum) == 30:
                break
            # break if the sample number is more than 20
            elif sampleNum > 20:
                break

        cam.release()
        cv2.destroyAllWindows()
        # show message on the screen
        messagebox.showinfo('Result', 'Dataset has been generated successfully!!!')


b1 = tk.Button(window, text="REGISTER YOUR FACE", font=("Arial", 15), bg='#afeeee', command=generate_dataset)
b1.place(x=150, y=350, width=280)


# set window size
window.geometry("600x420")
# set window color
window['background'] = '#dda0dd'
window.mainloop()

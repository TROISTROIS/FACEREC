import mysql.connector
mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="REGISTEREDSTUDENTS"

)

# create a table called STUDENTDETAILS
mycursor=mydb.cursor()
mycursor.execute("CREATE TABLE STUDENTDETAILS(USERID varchar(50),STUDENTNAME varchar (50),REGISTRATIONNUMBER varchar(50) primary key,COURSENAME varchar(50),UNITCODE varchar(50))")

# create a table called LECTURERDETAILS
mycursor=mydb.cursor()
mycursor.execute("CREATE TABLE LECTURERDETAILS(LECTURERNAME varchar(50),LECTURERID varchar(50) primary key, UNITCODE varchar(50))")

# create a table called attendance
mycursor=mydb.cursor()
mycursor.execute("CREATE TABLE attendance(LESSON_ID varchar(50),DATE date, REGNUMBER varchar(50))")


#LESSON ID, DATE, REGISTRATION NUMBER
#with open('attendance.csv', 'w') as write_file:
    #writer = csv.writer(write_file)
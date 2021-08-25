# This file writes attendance information from the database into a csv file.
import csv
import mysql.connector

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
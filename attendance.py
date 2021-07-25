from datetime import datetime

def markAttendance(name):
    with open('attendance.csv', 'r+',) as f:
        allLines=.readlines()
        attendanceList=[]
        for line in allLines:
            entry=line.split(',')
            attendanceList.append(entry[0])
        if name not in attendanceList:
            now=datetime.now()
            dtString=now.strftime('%d/%b/%Y', '%H:%M:%%S')
            f.writelines(f'\n{name},{dtString}')

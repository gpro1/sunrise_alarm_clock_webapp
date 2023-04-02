import time
import datetime
import serial
import sys

ser = serial.Serial('/dev/serial0')

alarm_time = str(sys.argv[1])
alarm_time = alarm_time.split(':')
alarm_hour = int(alarm_time[0])
alarm_min = int(alarm_time[1])

while(True):
    t = datetime.datetime.today()
    future = datetime.datetime(t.year, t.month, t.day, alarm_hour, alarm_min)
    future -= datetime.timedelta(minutes=15)
    if t.timestamp() > future.timestamp():
        future += datetime.timedelta(days=1)
    time.sleep((future-t).total_seconds())
    ser.write(b'GB23 sunrise \r\n')

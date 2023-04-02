import time
import datetime
import serial
import sys

alarm_time = str(argv[1])
alarm_time = alarm_time.split(':')
alarm_hour = int(alarm_time[1])
alarm_min = int(alarm_time[2])

while(True):
    t = datetime.datetime.today()
    future = datetime.datetime(t.year, t.month, t.day, alarm_hour, alarm_minute)
    future -= datetime.timedelta(minutes=30)
    if t.timestamp() > future.timestamp():
        future += datetime.timedelta(days=1)
    time.sleep((future-t).total_seconds())
    ser.write(b'GB23 sunrise \r\n')
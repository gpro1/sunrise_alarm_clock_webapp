from flask import Flask, render_template, request, flash
import serial
import subprocess
import time
import os
import signal
import json
ser = serial.Serial('/dev/serial0')

app = Flask(__name__)
app.secret_key = "peepeepoopoo"

alarm_process = None
current_alarm_time = None

def save_alarm_data(alarm_time, pid):
    with open('alarm_time.json', 'w') as f:
        json.dump({'alarm_time': alarm_time, 'alarm_pid': pid}, f)
 
def load_alarm_time():
    try:
        with open('alarm_time.json', 'r') as f:
            data = json.load(f)
            return data['alarm_time']
    except FileNotFoundError:
        return None
    except KeyError:
        return None

def save_alarm_pid(pid):
    with open('alarm_time.json', 'w') as f:
        json.dump({'alarm_pid': str(pid)}, f)
 
def load_alarm_pid():
    try:
        with open('alarm_time.json', 'r') as f:
            data = json.load(f)
            return data['alarm_pid']
    except FileNotFoundError:
        return None
    except KeyError:
        return None
 
def is_pid_running(pid):
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False
 
def set_alarm(alarm_time):
    global alarm_process
    # Load the PID of the existing subprocess, if any
    alarm_pid = load_alarm_pid()
 
    # Check if the subprocess is still running
    if alarm_pid is not None and is_pid_running(alarm_pid):
        # Terminate the existing subprocess
        os.kill(alarm_pid, signal.SIGTERM)
 
    # Start a new subprocess
    alarm_process = subprocess.Popen(["python", "sunrise_alarm.py", alarm_time])
    # Save the new subprocess PID
    save_alarm_data(alarm_time, alarm_process.pid)
 
def disable_alarm():
    alarm_pid = load_alarm_pid()
    if alarm_pid is not None and is_pid_running(alarm_pid):
        os.kill(alarm_pid, signal.SIGTERM)

    # Remove the alarm PID file or set it to None
    save_alarm_data(None, None)
    current_alarm_time = None

@app.route('/')
def index():
    global current_alarm_time
    flash("Enter a command:")
    return render_template("index.html", alarm_time=current_alarm_time)

@app.route("/send", methods=["post", "get"])
def send():
    global current_alarm_time
    ser.write(bytes(request.form['name_input'], 'utf-8') + b' \r\n')
    flash("Sent the following command: " + request.form['name_input'])
    return render_template("index.html", alarm_time=current_alarm_time)

@app.route("/rainbow", methods=["post", "get"])
def rainbow():
    global current_alarm_time
    ser.write(b'GB23 rainbow \r\n')
    flash("Enter a command:")
    return render_template("index.html", alarm_time=current_alarm_time)

@app.route("/moonlight", methods=["post", "get"])
def moonlight():
    global current_alarm_time
    ser.write(b'GB23 brightness 0.1 \r\n')
    ser.write(b'GB23 moonlight \r\n')
    flash("Enter a command:")
    return render_template("index.html", alarm_time=current_alarm_time)

@app.route("/off", methods=["post", "get"])
def off():
    global current_alarm_time
    ser.write(b'GB23 off \r\n')
    flash("Enter a command:")
    return render_template("index.html", alarm_time=current_alarm_time)

@app.route("/colour", methods=["post", "get"])
def colour():
    global current_alarm_time
    colour = str(request.form['color_input'])
    brightness = float(request.form['brightness_input'])/100
    red = int(colour[1] + colour[2], 16)
    green = int(colour[3] + colour[4], 16)
    blue = int(colour[5] + colour[6], 16)
    command = ("GB23 brightness " + str(brightness) + " \r\n")
    ser.write(bytes(command,'utf-8'))
    command = ("GB23 colour " + str(red) + " " + str(green) + " " + str(blue) + " \r\n")
    ser.write(bytes(command,'utf-8'))
    flash("Enter a command:")
    return render_template("index.html", alarm_time=current_alarm_time)

@app.route("/setAlarm", methods = ["post", "get"])
def setAlarm():
    global alarm_process
    global current_alarm_time
    #get alarm arguments
    current_alarm_time = str(request.form['alarmTime'])

    set_alarm(current_alarm_time)

    #render template
    flash("Enter a command:")
    return render_template("index.html", alarm_time=current_alarm_time)

    
@app.route("/disableAlarm", methods=["post", "get"])
def disableAlarm():
    global alarm_process
    global current_alarm_time

    current_alarm_time = "not set!"

    disable_alarm();
      
    flash("Enter a command:")
    return render_template("index.html", alarm_time=current_alarm_time)

if __name__ == '__main__':
    pid = load_alarm_pid()
    previous_time = load_alarm_time()
    #Restore alarm if there was one set
    if ((pid is not None) and (previous_time is not None)):
        set_alarm(previous_time)
        current_alarm_time = previous_time
    else:
        disable_alarm()
        current_alarm_time = None
    app.run(host='0.0.0.0', port=5000)
    

from flask import Flask, render_template, request, flash
import serial
import subprocess
import time
ser = serial.Serial('/dev/serial0')

app = Flask(__name__)
app.secret_key = "peepeepoopoo"

alarm_process = None
current_alarm_time = None

def set_alarm(alarm_time):
    global alarm_process
    alarm_process = subprocess.Popen(["python", "sunrise_alarm.py", alarm_time])

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


    if alarm_process is not None:
        alarm_process.kill()
        alarm_process.wait(timeout=0.5)

    set_alarm(current_alarm_time)

    #render template
    flash("Enter a command:")
    return render_template("index.html", alarm_time=current_alarm_time)

    
@app.route("/disableAlarm", methods=["post", "get"])
def disableAlarm():
    global alarm_process
    global current_alarm_time

    current_alarm_time = "not set!"

    if alarm_process is not None:
        alarm_process.kill()
        alarm_process.wait(timeout=0.5)

#    while alarm_process is not None:
#        alarm_process.kill()
#        while not alarm_process.poll():
#            time.sleep(0.1)
      
    flash("Enter a command:")
    return render_template("index.html", alarm_time=current_alarm_time)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    

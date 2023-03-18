from flask import Flask, render_template, request, flash
import serial
ser = serial.Serial('COM6')

app = Flask(__name__)
app.secret_key = "peepeepoopoo"

@app.route('/')
def index():
    flash("Enter a command:")
    return render_template("index.html")

@app.route("/send", methods=["post", "get"])
def send():
    ser.write(bytes(request.form['name_input'], 'utf-8') + b' \r\n')
    flash("Sent the following command: " + request.form['name_input'])
    return render_template("index.html")


@app.route("/rainbow", methods=["post", "get"])
def rainbow():
    ser.write(b'GB23 rainbow \r\n')
    flash("Enter a command:")
    return render_template("index.html")

@app.route("/moonlight", methods=["post", "get"])
def moonlight():
    ser.write(b'GB23 off \r\n')
    flash("Enter a command:")
    return render_template("index.html")

@app.route("/off", methods=["post", "get"])
def off():
    ser.write(b'GB23 off \r\n')
    flash("Enter a command:")
    return render_template("index.html")

@app.route("/colour", methods=["post", "get"])
def colour():
    colour = str(request.form['color_input'])
    red = int(colour[1] + colour[2], 16)
    green = int(colour[3] + colour[4], 16)
    blue = int(colour[5] + colour[6], 16)
    command = ("GB23 colour " + str(red) + " " + str(green) + " " + str(blue) + " \r\n")
    ser.write(bytes(command,'utf-8'))
    flash("Enter a command:")
    return render_template("index.html")
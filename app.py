from flask import Flask, render_template, request, flash
import serial
ser = serial.Serial('COM6')
ser.write(b'OFF\r\n')

app = Flask(__name__)
app.secret_key = "peepeepoopoo"

@app.route("/hello")
def index():
    flash("Enter a command:")
    return render_template("index.html")

@app.route("/send", methods=["post", "get"])
def send():
    ser.write(bytes(request.form['name_input'], 'utf-8') + b'\r\n')
    flash("Sent the following command: " + request.form['name_input'])
    return render_template("index.html")
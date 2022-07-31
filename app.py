import RPi.GPIO as GPIO
from time import sleep
from flask import Flask, render_template, request
import os
import pika

# Converts the hex to RGB value    
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

# Changes the LED color as given RGB value
def updateHue(R, G, B):
    RED.start(100)
    GREEN.start(100)
    BLUE.start(100)
    RED.ChangeDutyCycle(0)
    GREEN.ChangeDutyCycle(0)
    BLUE.ChangeDutyCycle(0)  
    rVal = 100 - (R/255.0)*100
    gVal = 100 - (G/255.0)*100
    bVal = 100 - (B/255.0)*100
    RED.ChangeDutyCycle(rVal)
    GREEN.ChangeDutyCycle(gVal)
    BLUE.ChangeDutyCycle(bVal)  

# Blink LED thrice with red color showing that it is turning off and clean up the GPIO pins
def turnoff():
    updateHue(255,0,0)
    sleep(0.5)
    updateHue(0,0,0)
    sleep(0.5)
    updateHue(255,0,0)
    sleep(0.5)
    updateHue(0,0,0)
    sleep(0.5)
    updateHue(255,0,0)
    sleep(0.5)
    print("\n")
    GPIO.cleanup()


COLOR = ["ffffff"]
os.environ.pop("FLASK_RUN_FROM_CLI")
os.environ.pop("FLASK_ENV")
pins = [17,27,22]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(True)
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
RED = GPIO.PWM(pins[0], 100)
GREEN = GPIO.PWM(pins[1], 100)
BLUE = GPIO.PWM(pins[2], 100)
RED.start(0)
GREEN.start(0)
BLUE.start(0)

app = Flask(__name__,template_folder="/home/pi/RGBled_with_sock")
@app.route("/color",methods=['GET']) #Receive the color to be set via get param "set"
def color():
    args = request.args
    args.get("set")
    COLOR[0] = args.get("set")
    value = hex_to_rgb(args.get("set"))
    red,green,blue = value
    updateHue(int(red),int(green),int(blue))
    return render_template('index.html')
    
@app.route("/fetch") # Send the current color when the page loads to be updated
def fetch():
    return COLOR[0]
    
@app.route("/index") # Renders index.html
def index():
    return render_template('index.html')

@app.route("/stomp.js")
def stomp():
    return render_template('stomp.js')
    
@app.route("/main.js")
def mainjs():
    return render_template('main.js')    
   
app.run(host="0.0.0.0")
turnoff()
exit()

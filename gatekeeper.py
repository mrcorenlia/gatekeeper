#!/usr/bin/python
import bottle
from bottle import route, run, response
#Import the package needed for GPIO controls
import RPi.GPIO as GPIO
#Just take the 'sleep' component from the time package
from time import sleep

@route('/', method='GET')
def homepage():
    return 'Hello world!'
 
@route('/status', method='GET')
def getDoorStatus():
    response.content_type = 'application/json'
    response.headers['Access-Control-Allow-Origin'] = '*'

    #press = not GPIO.input(15)
    press = isDoorOpen()
    if press == True:
        return "{ \"open\": true }"
    else:
        return "{ \"open\": false }"
    
@route('/close', method='POST')
def closeDoor():
    if isDoorOpen() == True:
        toggleDoor()
        return
    else:
        return "Door is already closed!"

@route('/open', method='POST')
def openDoor():
    if isDoorOpen() == False:
        toggleDoor()
        return
    else:
        return "Door is already open!"

@route('/toggle', method='POST')
def toggleDoor():
    #Reset GPIO
    GPIO.cleanup()
    #Use 1-up numbering on the pysical board (rather than the internal addressing)
    GPIO.setmode(GPIO.BOARD)
    #Pin 11 is output
    GPIO.setup(11, GPIO.OUT)

    #Signal door
    GPIO.output(11, True)
    #Hold signal
    sleep(5)
    #Release
    GPIO.output(11, False)

def isDoorOpen():
    #Reset GPIO
    GPIO.cleanup()
    #Use 1-up numbering on the pysical board (rather than the internal addressing)
    GPIO.setmode(GPIO.BOARD)
    #Pin 15 is input
    GPIO.setup(15, GPIO.IN)

    return not GPIO.input(15)
    
bottle.debug(True) 
run(host='0.0.0.0', reloader=True)

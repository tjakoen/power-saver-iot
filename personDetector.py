from omrond6t import *
from timer import RepeatingTimer 
from time import sleep
import RPi.GPIO as GPIO
import os

GPIO.cleanup()
pinMotionIn = 17
pinLightOut = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinMotionIn, GPIO.IN)
GPIO.setup(pinLightOut, GPIO.OUT)

firstRun = True

def setGPIOLow():
    GPIO.output(pinLightOut, GPIO.HIGH)
    print 'Timer Complete'

t = RepeatingTimer(10, setGPIOLow)

def startTimer():
    global firstRun
    if firstRun:
        firstRun = False
        print 'Timer Started'
        t.start()
    else:
        print 'Timer Reset'
        t.cancel()
        t.start()
    sleep(5)
	

size = 16
hitTemp = 35.5
omron = OmronD6T(arraySize=size)

while True:
    sleep(0.25)
    hits = 0
    bytesRead, temperature = omron.read()

    print(omron.roomTemp)    
    motionOccured = GPIO.input(pinMotionIn)
    
    if ( omron.roomTemp >= 35 ):
        print("Room temp too high for body heat detection!")
    else:
        for i in range(size):
            if temperature[i] > omron.roomTemp or temperature[i] > 35:
                hits+=1
    if motionOccured or hits > 1:
        if motionOccured:
            print 'Motion Occured'
        elif hits > 1:
            print 'Human Detected'
        GPIO.output(pinLightOut, GPIO.LOW)
	startTimer()
    else:
        print 'No Human Detected'

    print temperature
    print motionOccured

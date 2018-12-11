from omrond6t import *
from reset_timer import TimerReset 
from time import sleep
import RPi.GPIO as GPIO
import os

GPIO.cleanup()
pinMotionIn = 17
pinLightOut = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(pinMotionIn, GPIO.IN)
GPIO.setup(pinLightOut, GPIO.OUT)

size = 16
hitTemp = 35.5
omron = OmronD6T(arraySize=size)

try:
    while True:
        sleep(0.5)
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

        if hits > 1:
            print 'Human Detected'
            GPIO.output(pinLightOut, GPIO.HIGH)
    	    sleep(10)
        elif motionOccured:
            print 'Motion Occured'
            GPIO.output(pinLightOut, GPIO.HIGH)
	    sleep(10)
        else:
            print 'No Human Detected'
            GPIO.output(pinLightOut, GPIO.LOW)

        print temperature
        print motionOccured
except:
    os.system("sudo reboot")
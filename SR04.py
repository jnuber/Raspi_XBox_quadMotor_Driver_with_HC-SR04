#!/usr/bin/python3
# Source: https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
# https://www.tutorialspoint.com/python/python_multithreading.htm
# John Nuber
# March 2018
# Multithreaded HC-SR04 sonar sensor controller by Raspberry Pi 3 via GPIO
#
import RPi.GPIO as GPIO
import threading
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#Vss GPIO Pin 2 - 5vdc
#Gnd GPIO Pin 6 - gnd 
#set GPIO Pins
GPIO_TRIGGER = 18 # Yellow lead phy pin 12
GPIO_ECHO = 24    # Orange lead phy Pin 18
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

class ChkDist(threading.Thread):
   def __init__(self, threadID, name):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
   def run(self):
      #print("Starting ", self.name)
      getDist()
      return
      #print("Exiting ",self.name)

def getDist():
    return distance()

def stop():
    print("Measurement stopped by User")
    GPIO.cleanup()
    ChkDist.exit()
    time.sleep(2)
    return
  
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def calDist(): 
    print("Beginning HC-SR04 Sonar ping...")
    try:
        while True:
            dist = distance()                            # cm Units
            inches = dist * 0.39370078740158             # calculate inches
            feet = inches / 12                           # calculate feet
            if(dist <= 6):
                print("\nHelp!!!! STOP!!!\n")
            else: 
                print ("Distance: {0:0,.2f}cm | {1:0,.2f}in | {2:0,.2f} ft".format(dist,inches,feet))                
            time.sleep(1)
             
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        ChkDist.exit()
        GPIO.cleanup()
        time.sleep(2)
    return



# Create new thread and start it.
# DistThread = ChkDist(1,"ChkDist-1")
# DistThread.start()

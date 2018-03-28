# #!/usr/bin/python3
# Calculating Angle
#
#                                             /|
#                                            / |
#                                           /  |
#                                          /   |
# Tan x(Degree) = x/y (Opposite/Adjacent) /____|
# Inverse Tan of x/y = Angle-degrees
#
# NOTE: This was tested using an XBox USB wireless controller.
#
# Upate March 2018 - Added HC-SR04 Sonic sensor module. In this case, 
#     we are looking to determne if an opbject is within 10cm/4 inches 
#    'in front' or forward of us. If so, initate a stop or alternate 
#     manuver. 
#
#==========================================================================

import math
import sys
import MotorDrv
import pygame
from time import sleep
import piplates.MOTORplate as MOTOR          #import the MOTORplate module
import SR04                                  # RPi HC-SR04 multi-threaded 


def PygameHandler(events):
# Read pygame events for axis and button entries
	global y
	global x
	
	for event in events:
		if event.type == joystick.JOYAXISMOTION:
			y = float(joystick.get_axis(0))
			x = float(joystick.get_axis(1))
	
	return

# Function to set all drives off
def MotorOff():
    print("Stopping Motor")
    motor.dcSTOP(ctl,FL)
    motor.dcSTOP(ctl,FR)
    motor.dcSTOP(ctl,RL)
    motor.dcSTOP(ctl,RR)
        
    status = "stopped"
    return status

def resetCtl():
	MOTOR.clrLED(ctl)
	sleep(1)
	MOTOR.RESET(ctl)
	return

def initMotor(FLdir,FRdir,RLdir,RRdir):
	#print("Setting: ",rotation)
	motor.dcCONFIG(ctl,FL,FLdir,0.0,0.0)
	motor.dcCONFIG(ctl,FR,FRdir,0.0,0.0)
	motor.dcCONFIG(ctl,RL,RLdir,0.0,0.0)
	motor.dcCONFIG(ctl,RR,RRdir,0.0,0.0)
	
	motor.dcSTART(ctl,FL)
	motor.dcSTART(ctl,FR)
	motor.dcSTART(ctl,RL)
	motor.dcSTART(ctl,RR)
	
	if   (FLdir == FRdir == RLdir == RRdir  == "cw") : 
		status = "forward"
		return
	elif (FLdir == FRdir == RLdir == RRdir  == "ccw"): 
		status = "reverse" 
		return
	elif (FLdir == RLdir == "cw"  and FRdir == RRdir == "ccw"):
		status = "left"
	elif (FLdir == RLdir == "ccw" and FRdir == RRdir == "cw"):
		status = "right"
	else:
		 status = 'something not right'
	
	return status 

def fwd(FLspeed,FRspeed,RLspeed,RRspeed):
	# print("Forward motion called. CTL: ",ctl)
	status = initMotor('cw','cw','cw','cw')
	motor.dcSTART(ctl, FL)
	motor.dcSTART(ctl, FR)
	motor.dcSTART(ctl, RL)
	motor.dcSTART(ctl, RR)
	
	status = "forward"
	return status

def reverse(FLspeed,FRspeed,RLspeed,RRspeed):
	print("Reverse motion called. CTL: ",ctl)
	status = initMotor('ccw','ccw','ccw','ccw')
	motor.dcSTART(ctl, FL)
	motor.dcSTART(ctl, FR)
	motor.dcSTART(ctl, RL)
	motor.dcSTART(ctl, RR)
	
	status = "reverse"
	return status

def left(FLspeed,FRspeed,RLspeed,RRspeed):
	status = initMotor('ccw','cw','ccw','cw')
	motor.dcSTART(ctl,FL)
	motor.dcSTART(ctl,FR)
	motor.dcSTART(ctl,RL)
	motor.dcSTART(ctl,RR)
	
	status = 'left'
	return status

def right(FLspeed,FRspeed,RLspeed,RRspeed):
	status = initMotor('cw','ccw','cw','ccw')
	motor.dcSTART(ctl,FL)
	motor.dcSTART(ctl,FR)
	motor.dcSTART(ctl,RL)
	motor.dcSTART(ctl,RR)
	
	status = 'right'
	return status

def motorSpeed(FLspeed,FRspeed,RLspeed,RRspeed):
	motor.dcSPEED(ctl,FL,FLspeed)
	motor.dcSPEED(ctl,FR,FRspeed)
	motor.dcSPEED(ctl,RL,RLspeed)
	motor.dcSPEED(ctl,RR,RRspeed)

def fwdObstruction():
	inches = distance * 0.39370078740158         # calculate inches
	feet = inches / 12                           # calculate feet
	print("Panic, we are {0:0,.2f} inches from an object".format(inches))
	status = MotorOff()                          # kill motors
	sleep(2)                                     # pause for 2 seconds
	leftSpeed = rightSpeed = leftSpeed = rightSpeed = 20
	status = reverse(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
	sleep(2)
	status = MotorOff()
	status = 'obstruction'
	print("WOW...that was close...\n") 
	return status

#=======================================================================
#	Initialize Variables, processes, threads
#=======================================================================

#   Initialize multi-threaded HC-SR04 sonic sensor
DistThread = SR04.ChkDist(1,"ChkDist-1")
DistThread.start()

# Define Motors
FL = 1				# Define Motor 1 = Front Left   - FL
FR = 2  			# Define Motor 2 = Fright Right - FR
RL = 3  			# Defome Motor 3 = Rear Left    - RL
RR = 4  			# Define Motor 4 = Rear Right   - RR
global status

#Initalized the Xbox controller via the pygame module
pygame.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print("JS Initialized: ",joystick.get_init())  # Return 1 or True if Successful
print(joystick.get_name())

#PiPlate Motor controller
motorDrvVersion = MotorDrv.version()
print("Motor Controller: {0}".format(motorDrvVersion))

motor = MOTOR
ctl = 1
resetCtl()
status = initMotor('ccw','ccw','ccw','ccw')
for i in range(10):
	motor.clrLED(ctl)
	sleep(.0625)
	motor.setLED(ctl)
	sleep(.0625)
print("Reset and initalize controller {0} and motors".format(ctl))

axisMax = 1
minSpeed = 5 


#=======================================================================
# Main Logic Loop Start 
#=======================================================================
#            Forward
#         (-179 / 179)
#              180
#               |
#               |
#Left   270 ----+------ 90  Right
#      (-90)    |
#               |
#            360 / 0
#           (-1 / 1)
#            Reverse		
#=======================================================================

while True:
	leftSpeed  = 100
	rightSpeed = 100
	sleep(.25)

	for event in pygame.event.get():
		if event.type == pygame.JOYBUTTONDOWN:
			B = joystick.get_button(1)
			if (B == 1):
				print("Button B:",B)
				status = MotorOff()
				# status = "Motors Off"

		if event.type == pygame.JOYAXISMOTION:
			y = joystick.get_axis(1)
			x = joystick.get_axis(0) 
			speed = joystick.get_axis(2)
		    
			angle = math.degrees(math.atan2(x,y))
			
	
	#===========================================================================================
	# Determining drive direction is based on the calculated angle of the joystick's
	# x and y offset from each other.
	# NOTE: depending on the direction, forward, forward right, forward left, 
	#       left, right, reverse left, reverse right, the speed of the left or 
	#       right axels are adjusted by the x and y values. Right and left
	#       axels speeds are determined by the x OR y offset values from its axis.
	# 
	# Up/down or forward/reverse speed is determined by the veritical Y axis.
	# Left/Right speed is determined by the horizontal X axis. 
	#
	# ==========================================================================================

			if(angle < 0):
				angle = angle  + 360

			# Hard Forward
			if(angle ==  180):
				leftSpeed  = abs((y/axisMax * 100))
				rightSpeed = abs((y/axisMax * 100))
				if status != 'forward':
					status = MotorOff()
					status = fwd(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
				motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
				status = "forward"

			#1/8 Forward Left Turning Angle 
			if(angle > 100 and angle < 260 and angle != 180):
				#leftSpeed  = abs((((y-x) /axisMax) * 100))
				leftSpeed  = abs((x/axisMax * 100))
				rightSpeed = abs((y/axisMax * 100))
				if leftSpeed <=39:
					leftSpeed = 40	
				if status != 'forward':
					status = MotorOff()
					status = fwd(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
				motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
			

			#Hard Left
			if(angle > 260 and angle < 280):
				leftSpeed  = abs((x/axisMax * 100))
				rightSpeed = abs((x/axisMax * 100))
				if status != 'left':
					status = MotorOff()
					status = left(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
				motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
				status = "left"

			# Hard Reverse
			if(angle == 0 ):
				leftSpeed  = abs((y/axisMax * 100))
				rightSpeed = abs((y/axisMax * 100))
				if status != 'reverse':
					status = MotorOff()
					status = reverse(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
				motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
				status = "reverse"

			# Reverse turning left
			if( (angle < 90 or angle > 280) and angle !=0):
				leftSpeed  = abs((x/axisMax * 100))
				rightSpeed = abs((y/axisMax * 100))
				if status != 'reverse':
					status = MotorOff()
					status = reverse(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
				motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
				status = "reverse"

			#Hard Right Turn
			if(angle == 90.0):
				leftSpeed  = abs((x/axisMax * 100))
				rightSpeed = abs((x/axisMax * 100))
				if status != 'right':
					status = MotorOff()					
					status = right(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
				motorSpeed(leftSpeed,rightSpeed,leftSpeed,rightSpeed)
				status = "right"

			print('x: {0:>6.3f} y:{1:>6.3f} = {2:.0f} Degrees Speed(L/R): {3:.2f} : {4:.2f} Status: {5}'.format(abs(x)*100,abs(y)*100,angle,abs(leftSpeed),abs(rightSpeed),status))		
			
		distance = SR04.getDist()

		if distance < 10:
			if status != 'obstruction':
				status = fwdObstruction()
			else:
				print("Status is: {0}".format(status))
				status != 'obstruction'
			sleep(2)
			
SR04.stop()

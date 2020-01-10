#!/usr/bin/env python
# license removed for brevity

import RPi.GPIO as GPIO
import rospy
import numpy as np
from std_msgs.msg import String

#Disables warnings and sets up BCM GPIO numbering
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#Sets GPIO out pins
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

F = 490

#Creates PWM instances (channel,frequency)
pwm_A1 = GPIO.PWM(24,F)
pwm_B1 = GPIO.PWM(25,F)
pwm_A2 = GPIO.PWM(4,F)
pwm_B2 = GPIO.PWM(17,F)
pwm_A3 = GPIO.PWM(22,F)
pwm_B3 = GPIO.PWM(23,F)
pwm_A4 = GPIO.PWM(18,F)
pwm_B4 = GPIO.PWM(27,F)

#Initial PWM, for DC motors it is always 0
pwm_A1.start(0)
pwm_B1.start(0)
pwm_A2.start(0)
pwm_B2.start(0)
pwm_A3.start(0)
pwm_B3.start(0)
pwm_A4.start(0)
pwm_B4.start(0)

Vg = 30

def callback(data):

    try:
		v = data.data
		cmd = v.split("/")
		#F1 para eje Y
		#F2 para eje X
		F1 = int(cmd[0])
		Vy = int(cmd[1])
		F2 = int(cmd[2])
		Vx = int(cmd[3])
		Pl = int(cmd[4])
		Pr = int(cmd[5])

		if (Pl == 1 or Pr == 1):

			if (Pl == 1 and Pr == 0):
				C = [0,Vg,Vg,0,0,Vg,Vg,0]
			elif (Pr == 1 and Pl == 0):
				C = [Vg,0,0,Vg,Vg,0,0,Vg]
			else:
				C = [0,0,0,0,0,0,0,0]

		else:

			if (Vx > 0 and Vy == 0):
				if (F2 == 1):
					#Adelante
					C = [Vx,0,Vx,0,Vx,0,Vx,0]
				elif (F2 == 0):
					#Atras
					C = [0,Vx,0,Vx,0,Vx,0,Vx]

			elif (Vx == 0 and Vy > 0):
				if (F1 == 0):
					#Izquierda
					C = [0,Vy,Vy,0,Vy,0,0,Vy]
				elif (F1 == 1):
					#Derecha
					C = [Vy,0,0,Vy,0,Vy,Vy,0]

			elif (Vx > 0 and Vy > 0):

				if (Vx > Vy):
					if (F1 == 0 and F2 == 0):
						C = [0,Vx,Vy,0,Vy,0,0,Vx]
					elif (F1 == 0 and F2 == 1):
						C = [0,Vy,Vx,0,Vx,0,0,Vy]
					elif (F1 == 1 and F2 == 0):
						C = [Vy,0,0,Vx,0,Vx,Vy,0]
					elif (F1 == 1 and F2 == 1):
						C = [Vx,0,0,Vy,0,Vy,Vx,0]

				elif (Vy > Vx):
					if (F1 == 0 and F2 == 0):
						C = [0,Vy,Vx,0,Vx,0,0,Vy]
					elif (F1 == 0 and F2 == 1):
						C = [0,Vx,Vy,0,Vy,0,0,Vx]
					elif (F1 == 1 and F2 == 0):
						C = [Vx,0,0,Vy,0,Vy,Vx,0]
					elif (F1 == 1 and F2 == 1):
						C = [Vy,0,0,Vx,0,Vx,Vy,0]

				elif (Vx == Vy):
					if (F1 == 0 and F2 == 0):
						C = [0,Vy,Vx,0,Vx,0,0,Vy]
					elif (F1 == 0 and F2 == 1):
						C = [0,Vx,Vy,0,Vy,0,0,Vx]
					elif (F1 == 1 and F2 == 0):
						C = [Vx,0,0,Vy,0,Vy,Vx,0]
					elif (F1 == 1 and F2 == 1):
						C = [Vy,0,0,Vx,0,Vx,Vy,0]

			elif (Vy == 0 and Vx == 0):
				C = [0,0,0,0,0,0,0,0]

		#print C

		pwm_A1.ChangeDutyCycle(C[0])
		pwm_B1.ChangeDutyCycle(C[1])
		pwm_A2.ChangeDutyCycle(C[2])
		pwm_B2.ChangeDutyCycle(C[3])
		pwm_A3.ChangeDutyCycle(C[4])
		pwm_B3.ChangeDutyCycle(C[5])
		pwm_A4.ChangeDutyCycle(C[6])
		pwm_B4.ChangeDutyCycle(C[7])

    except:
        pass

def inicio():
	rospy.init_node('principal', anonymous=True)
	rospy.Subscriber("batinito_topic", String, callback)
	rospy.spin()

if __name__ == '__main__':
	inicio()

#!/usr/bin/env python
# license removed for brevity

from __future__ import division
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

#rospy.init_node('principal', anonymous=True)
 
def inicio():
   
    pwm_A1.ChangeDutyCycle(0)
    pwm_B1.ChangeDutyCycle(0)
    pwm_A2.ChangeDutyCycle(0)
    pwm_B2.ChangeDutyCycle(0)
    pwm_A3.ChangeDutyCycle(0)
    pwm_B3.ChangeDutyCycle(0)
    pwm_A4.ChangeDutyCycle(0)
    pwm_B4.ChangeDutyCycle(0)


if __name__ == '__main__':
    try:
        inicio()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python

from __future__ import division
import serial
import rospy
from std_msgs.msg import String  #String message type for publishing

#Map function from arduino
def map(x,in_min,in_max,out_min,out_max):
    return (x-in_min)*(out_max-out_min)/(in_max-in_min)+out_min

#Initializes serial communication (if there is an error 'no suchfile or directory found' try changing '/dev/ttyACM0' to '/dev/ttyACM1')
arduino = serial.Serial('/dev/ttyACM0',9600)

#Initial readings to prevent errors
for i in range(50):
    a = arduino.readline()
    #print a

#Initial flag values
FlagXP = 0
FlagXS = 1
FlagXN = 0
FlagYP = 0
FlagYS = 1
FlagYN = 0

#Sets maximum PWM values for X,Y, and turns velocities
VX_MAX = 30
VFG_MAX = 60
VBG_MAX = 60

#Declares that this node is publishing to the 'joystick_topic' topic using the message type String
pub = rospy.Publisher('joystick_topic', String, queue_size = 10)
pub2 = rospy.Publisher('batinito_topic',String, queue_size = 10)
#Tells rospy the name of the node
rospy.init_node('Rjoystick', anonymous = True)

#Variable for Robot velocities
M = "Robot Movement"
M2 = "batinito"

try:
    while not rospy.is_shutdown():
        
        #Gets the data that is being sent from the arduino
        joystick=arduino.readline()
        l = joystick.split("/") #Splits the data in X and Y readings
        
        #Assigns the data to variables 
        DX = int(l[0])
        DY = int(l[1])

        #Maps the values to PWM
        Velxfront = int(round(map(DX,516,1023,0,VX_MAX),0))
        Velxback = int(round(map(DX,515,0,0,VX_MAX),0))
        Velyright = int(round(map(DY,517,1023,0,VY_MAX),0))
        Velyleft  = int(round(map(DY,517,0,0,VY_MAX),0))

        Velxfrontright = int(round(map(DY,517,1023,Velxfront,VFG_MAX),0))
        Velxfrontleft = int(round(map(DY,517,0,Velxfront,VFG_MAX),0))
        Velxbackright = int(round(map(DY,517,1023,Velxback,VBG_MAX),0))
        Velxbackleft = int(round(map(DY,517,0,Velxback,VBG_MAX),0))

        #Conditions for flag values
        if (DX>519):
            FlagXP = 1
            FlagXS = 0
            FlagXN = 0
    
        if (DX>511 and DX<519):
            FlagXS = 1
            FlagXP = 0
            FlagXN = 0
    
        if (DX<511):
            FlagXN = 1
            FlagXS = 0
            FlagXP = 0
    
        if (DY>518):
            FlagYP = 1
            FlagYS = 0
            FlagYN = 0
    
        if (DY>515 and DY<518):
            FlagYS = 1
            FlagYP = 0
            FlagYN = 0
    
        if (DY<515):
            FlagYN = 1
            FlagYS = 0
            FlagYP = 0

        #Conditions for robot movement that change the value of M
        if (FlagXS == True and FlagYS == True):
            M = str(0)+"/"+str(0)+"/"+str(0)+"/"+str(0)
            M2 = str(1)+"/"+str(0)+"/"+str(1)+"/"+str(0)
            
        elif (FlagYP == True and FlagXS == True):
            M = str(Velyright)+"/"+str(0)+"/"+str(0)+"/"+str(Velyright)
            M2 = str(0)+"/"+str(Velyright)+"/"+str(1)+"/"+str(0)
            
        elif (FlagYN == True and FlagXS == True):
            M = str(0)+"/"+str(Velyleft)+"/"+str(Velyleft)+"/"+str(0)
            M2 = str(1)+"/"+str(Velyleft)+"/"+str(1)+"/"+str(0)
            
        elif (FlagXP == True and FlagYS == True):
            M = str(0)+"/"+str(Velxfront)+"/"+str(0)+"/"+str(Velxfront)
            M2 = str(1)+"/"+str(0)+"/"+str(1)+"/"+str(Velxfront)
            
        elif (FlagXN == True and FlagYS == True):
            M = str(Velxback)+"/"+str(0)+"/"+str(Velxback)+"/"+str(0)
            M2 = str(1)+"/"+str(0)+"/"+str(0)+"/"+str(Velxback)
            
        elif (FlagXP == True and FlagYS == False):

            if(FlagYP == True):
                DerB = Velxfrontright
                IzqB = Velxfront
                M2 = str(0)+"/"+str(Velyright)+"/"+str(0)+"/"+str(Velxfront)

            elif(FlagYN == True):
                DerB = Velxfront
                IzqB = Velxfrontleft
                M2 = str(1)+"/"+str(Velyleft)+"/"+str(0)+"/"+str(Velxfront)

            M = str(0)+"/"+str(DerB)+"/"+str(0)+"/"+str(IzqB)
            
        elif (FlagXN == True and FlagYS == False):

            if (FlagYP == 1):
                DerA = Velxbackright
                IzqA = Velxback
                M2 = str(1)+"/"+str(Velyright)+"/"+str(0)+"/"+str(Velxback)

            elif (FlagYN == 1):
                DerA = Velxback
                IzqA = Velxbackleft
                M2 = str(0)+"/"+str(Velyleft)+"/"+str(0)+"/"+str(Velxback)

            M = str(DerA)+"/"+str(0)+"/"+str(IzqA)+"/"+str(0)
            
        #Publishes the string M to the 'joystick_topic' topic
        pub.publish(M)
        pub2.publish(M2)      

except rospy.ROSInterruptException:
    pass
import pyfirmata
import time
import math


def establishConnection(portName):
	try:
		arduino=pyfirmata.Arduino(portName)
		print("Connected to Arduino at "+portName)
	except:
		print("Failed to connect to Arduino at "+portName)
	iter8=pyfirmata.util.Iterator(arduino)
	iter8.start()
	return arduino

def initializeServos(arduino,pins):
	servoLookup={}
	for pinNumber in pins:
		pinID='d:'+str(pinNumber)+':s'
		servoObject=arduino.get_pin(pinID)
		servoLookup[pinNumber]=servoObject
	return servoLookup

def writeServo(pin,val):
	pin.write(val)

def getServoAngles(x,y,l0,l1):
	d=math.sqrt((x**2)+(y**2))
	theta_0=math.acos(((l1**2)-(l0**2)-(d**2))/(-2*l0*d))
	theta_1=math.acos(((d**2)-(l0**2)-(l1**2))/(-2*l0*l1))
	theta_b=math.atan(y/x)
	x1=l0*math.cos(theta_0+theta_b)
	y1=l0*math.sin(theta_0+theta_b)
	theta_a=math.atan((y-y1)/(x-x1))
	
	return (theta_0+theta_b,theta_a)


######################
#ANIMATION CODE BEGINS
######################

from tkinter import *

def init(data):
	data.pos=[50,50]
	data.l0=100
	data.l1=100

def mousePressed(event,data):
	data.pos=[event.x,data.height-event.y]

def keyPressed(event,data):
    pass

def redrawAll(canvas,data):
	canvas.create_rectangle(0,0,data.width,data.height,fill='white')
	x,y=data.pos
	l0,l1=data.l0,data.l1
	angles=getServoAngles(x,y,l0,l1)
	theta_0,theta_1=angles
	print(math.degrees(angles[0]),math.degrees(angles[1]))
	x1=l0*math.cos(theta_0)
	y1_math=l0*math.sin(theta_0)
	y1_visual=data.height-(l0*math.sin(theta_0))
	x2=x1+(l1*math.cos(theta_1))
	y2_visual=data.height-(y1_math+(l1*math.sin(theta_1)))
	canvas.create_line(0,data.height,x1,y1_visual,fill='black')
	canvas.create_line(x1,y1_visual,x2,y2_visual,fill='black')

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)






######################
#ANIMATION CODE ENDS
######################


def runSweepDemo():
	portName='/dev/tty.usbmodem14201'
	arduino=establishConnection(portName)
	lookup=initializeServos(arduino,[9])
	increaseAngle=True
	initialTime=time.time()
	angle=90
	while time.time()-initialTime<10:
		if increaseAngle==True:
			angle+=1
		elif increaseAngle==False:
			angle-=1
		if angle==0:
			increaseAngle=True
		elif angle==180:
			increaseAngle=False
		time.sleep(0.03)
		print(angle)
		writeServo(lookup[9],angle)
	print("Demo finished")



runSweepDemo()



import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import math
import time

def getServoAngles(x,y,l0,l1):
	d=math.sqrt((x**2)+(y**2))
	theta_0=math.acos(((l1**2)-(l0**2)-(d**2))/(-2*l0*d))
	theta_1=math.acos(((d**2)-(l0**2)-(l1**2))/(-2*l0*l1))
	theta_b=math.atan(y/x)
	x1=l0*math.cos(theta_0+theta_b)
	y1=l0*math.sin(theta_0+theta_b)
	theta_a=math.atan((y-y1)/(x-x1))
	return (theta_0+theta_b,theta_a)

def set3D(x_world,y_world,z_world):
    l0,l1=100,100
    x_math=math.sqrt((x_world**2)+(y_world**2))
    y_math=z_world
    theta_base=math.atan(y_world/x_world)
    theta_0,theta_1=getServoAngles(x_math,y_math,l0,l1)
    x_vals,y_vals,z_vals=[],[],[]
    x0,y0,z0=0,0,0
    x1=math.cos(theta_base)*(l0*math.cos(theta_0))
    y1=math.sin(theta_base)*(l0*math.cos(theta_0))
    z1=(l0*math.sin(theta_0))
    x2=x1+(math.cos(theta_base)*(l1*math.cos(theta_1)))
    y2=y1+(math.sin(theta_base)*(l1*math.cos(theta_1)))
    z2=z1+(l1*math.sin(theta_1))
    return ((x0,x1,x2),(y0,y1,y2),(z0,z1,z2))

fig=plt.figure()
ax=fig.add_subplot(111, projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
def animate(i):
    x_vals,y_vals,z_vals=[],[],[]
    for x in range(1,50,5):
        y=50
        z=0.00001
        x_vals.extend(set3D(x,y,z)[0])
        y_vals.extend(set3D(x,y,z)[1])
        z_vals.extend(set3D(x,y,z)[2])
    ax.clear()
    ax.plot(x_vals,y_vals,z_vals)
    time.sleep(.005)
ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()




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


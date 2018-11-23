from tkinter import *
from PIL import Image,ImageTk
from Button import Button
from arduinoControl import arduinoControl
import glob
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
#from pykinect2 import PyKinectRuntime
def drawFinishedScreen(canvas):
    canvas.create_rectangle(0,0,data.height,data.width,fill='white')

def drawManualControlScreen(canvas):
    canvas.create_rectangle(0,0,data.width,data.height,fill='white')
    canvas.create_text(data.width//2,data.height//2,text='End Effector Position ')

def get2DImage(frame):
    imageWidth,imageHeight=512,424
    row,col,i=0,0,0
    image=[]
    for row in range(imageHeight):
        image.append([0]*imageWidth)
    while i<len(frame):
        if i%imageWidth==0:
            row+=1
            col=0
        else:
            col+=1
        image[row][col]=frame[i]
        i+=1
    return image

def drawDepthFrame(canvas):
    kinect=data.kinect
    if kinect.has_new_depth_frame():
        frame=kinect.get_last_depth_frame
        image=get2DImage(frame)
        myarray=np.array(image)
        img = Image.fromarray(np.uint8(cm.gist_earth(myarray)*255))
        newImg = ImageTk.PhotoImage(img)  
        canvas.create_image(20,20, anchor=NW, image=newImg)   
        










def runScanScreen(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill='white')
    data.scanButton.drawButton(canvas)
    drawDepthFrame(canvas)

def runUsbScreen(canvas,data):
    canvas.create_text(data.width//2,0,text="What port is the Arduino connected to?",font='Arial 40',anchor='n')
    canvas.create_text(data.width//2,data.usbButton.y-(data.usbButton.h//2),text=data.errorMessage,font='Arial 30',anchor='s')
    for button in data.portButtons:
        button.drawButton(canvas)
    data.usbButton.drawButton(canvas)


def drawStartScreen(canvas,data):
    canvas.create_rectangle(0,0,data.width,data.height,fill='white')
    canvas.create_text(data.width//2,0,text='Robot Arm Pathfinder',font='Arial 50',anchor='n')
    data.startButton.drawButton(canvas)

def init(data):
    data.arduinoPort=""
    '''
    data.startScreenOn=True
    data.usbScreenOn=False
    data.scanScreenOn=False
    data.humanControlOn=False
    data.redoScreenOn=False
    '''
    data.startScreenOn=False
    data.usbScreenOn=False
    data.scanScreenOn=True
    data.humanControlOn=False
    data.redoScreenOn=False

    data.startButton=Button(data.width//2,data.height//2,150,100,'Start',fontSize=35)
    data.usbButton=Button(data.width//2,data.height*(3/4),300,100,'Done?',fontSize=35,)
    data.scanButton=Button(data.width//2,data.height*(3/4),300,100,'Run Scan',fontSize=40)
    data.humanControlButton=Button(data.width//2,data.height//2,200,200,'Manual Control',fontSize=40)
    portsList=glob.glob('/dev/tty.*')
    widthPortButtons=len(max(portsList,key=len))*17
    data.portButtons=[]
    data.portSelected=False
    data.errorMessage=""
    for i in range(len(portsList)):
        w,h=widthPortButtons,50
        newButton=Button(data.width//4,150+(i*h),w,h,str(portsList[i]),fontSize=30)
        data.portButtons.append(newButton)
    data.depthImage=Image
    data.kinect=PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth)


def mousePressed(event,data):
    if data.startScreenOn and data.startButton.isPressed(event):
        data.startScreenOn=False
        data.usbScreenOn=True
    elif data.usbScreenOn:
        for button in data.portButtons:
            if button.isPressed(event):
                if data.portSelected==False:
                    button.color='red'
                    data.portSelected=True
                else:
                    button.color='white'
                    data.portSelected=False
        if data.usbButton.isPressed(event):
            for button in data.portButtons:
                if button.color=='red':
                    data.arduinoPort=button.text
            if arduinoControl.establishConnection(data.arduinoPort)==True:
                data.usbScreenOn=False
                data.scanScreenOn=True
            else:
                data.errorMessage="Failed to connect to Arduino at "+data.arduinoPort


            
    elif data.scanScreenOn and data.scanButton.isPressed(event):
        pass
    elif data.redoScreenOn==True and data.humanControlButton.isPressed(event):
        data.humanControlOn=True




def keyPressed(event,data):
    pass


def redrawAll(canvas,data):
    if data.startScreenOn:
        drawStartScreen(canvas,data)
    elif data.usbScreenOn:
        runUsbScreen(canvas,data)
    elif data.scanScreenOn:
        runScanScreen(canvas,data)
    elif data.humanControlOn:
        pass
    



def run(width,height):
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

    ###EDITS START HERE###
    root.attributes("-fullscreen",True)
    ###EDITS END HERE###
    mainFrame=Frame(root)
    ports=glob.glob('/dev/tty.*')
    variable=StringVar(root)
    variable.set(ports[0])

    ports=set(ports)
    popupMenu=OptionMenu(mainFrame,variable,*ports)
    Label(mainFrame, text="Choose a dish").grid(row = 1, column = 1)
    popupMenu.grid(row = 2, column =1)
    '''w=OptionMenu(root,variable,"one","two","three")
    w.pack()'''


    ###EDITS END HERE###
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(1300,800)
import math
class Button(object):
	def __init__(self,x,y,w,h,text,fontSize=40,color='white'):
		self.x=x
		self.y=y
		self.w=w
		self.h=h
		self.text=text
		self.color=color
		self.font='Arial '+str(int(fontSize))

	def drawButton(self,canvas):
		xL,xR=self.x-(self.w//2),self.x+(self.w//2)
		yL,yR=self.y-(self.h//2),self.y+(self.h//2)
		canvas.create_rectangle(xL,yL,xR,yR,fill=self.color)
		canvas.create_text(self.x,self.y,font=self.font,text=self.text,anchor='c',fill='black')

	def isPressed(self,event):
		mX,mY=event.x,event.y
		x,y=self.x,self.y
		w,h=self.w,self.h
		if mX<(x+(w/2)) and mX>(x-(w/2)):
			if mY<(y+(h/2)) and mY>(y-(h/2)):
				return True
		return False
#!/usr/bin/python
# -*- coding: utf-8 -*-


from Tkinter import *
from ttk import Frame, Button, Label, Style
import Image, ImageTk, sys, math
import regatta_api as myapi
import regatta_tools as mytools

SQUARE_SIZE = 34


class RegattaMainFrame(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.sea = myapi.Sea()
        self.parent = parent
	self.longitude_start=-50
	self.latitude_start=-40
	self.longitude_end=-40
	self.latitude_end=-30

    def set_sea_screen(self,longitude_start,latitude_start,longitude_end,latitude_end ):
        self.longitude_start=longitude_start
	self.latitude_start=latitude_start
	self.longitude_end=longitude_end
	self.latitude_end=latitude_end

    def initUI(self):
      
        self.parent.title("Windows")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        lbl = Label(self, text="Windows")
        lbl.grid( column=0)


	self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.grid(row=0, column=1, rowspan=15, sticky=E+W+S+N)
	
	self.showSea(self.longitude_start,self.latitude_start,self.longitude_end,self.latitude_end,0)
        
        abtn = Button(self, text="0H",command=self.button_0h)
        abtn.grid(row=1, column=0)

        cbtn = Button(self, text="12H",command=self.button_12h)
        cbtn.grid(row=2, column=0)

        cbtn = Button(self, text="24H",command=self.button_24h)
        cbtn.grid(row=3, column=0)

        cbtn = Button(self, text="Close",command=self.button_close)
        cbtn.grid(row=5, column=0)
        
        #hbtn = Button(self, text="Help")
        #hbtn.grid(row=5, column=0, padx=5)

        #obtn = Button(self, text="OK")
        #obtn.grid(row=5, column=3)

    def set_sea(self,sea):
	self.sea = sea

    def get_sea(self,sea):
	return self.sea
        
    def showSea(self,longitude_start,latitude_start,longitude_end,latitude_end,hour_prevision=0):
	for i in self.sea.get_squares() :
		if i.get_x() >= longitude_start and i.get_x() <= longitude_end and i.get_y() <= latitude_start and i.get_y() >= latitude_end :
			self.showWindSquareBlock(i,longitude_start,latitude_start)
			self.showWindSquarePosition(i,longitude_start,latitude_start)
			self.showWindSquareWind(i,longitude_start,latitude_start,hour_prevision)
	self.showBoat(-51,-45,longitude_start,latitude_start)
		#else :
			#print "bad block in:("+str(i.get_x())+","+str(i.get_y())+")"
        
    def showBoat(self,x,y,longitude_start,latitude_start):
	LEN_CIRCLE=6
	x_draw = (x - longitude_start)*SQUARE_SIZE
	y_draw = (y - latitude_start)*-1*SQUARE_SIZE
	#print "x:"+str(x_draw)+" y:"+str(y_draw)
	self.canvas.create_oval(x_draw-LEN_CIRCLE/2,y_draw-LEN_CIRCLE/2,x_draw+LEN_CIRCLE/2,y_draw+LEN_CIRCLE/2,fill="green")

    def showWindSquarePosition(self,ws,longitude_start,latitude_start):
        self.canvas.create_text((ws.get_x()-longitude_start)*SQUARE_SIZE+1,-1*(ws.get_y()-latitude_start)*SQUARE_SIZE+7,
		anchor=W,
            	text=str(ws.get_y()*(-1))+","+str(ws.get_x()*(-1)))

    def showWindSquareBlock(self,ws,longitude_start,latitude_start):
	self.canvas.create_rectangle((ws.get_x()-longitude_start)*SQUARE_SIZE, -1*(ws.get_y()-latitude_start)*SQUARE_SIZE,
		(ws.get_x()-longitude_start)*SQUARE_SIZE+SQUARE_SIZE, -1*(ws.get_y()-latitude_start)*SQUARE_SIZE+SQUARE_SIZE,
		outline="#000", fill="#05f") 

    def showWindSquareWind(self,ws,longitude_start,latitude_start,hour_prevision=0):
	LEN_ARROW=mytools.do_ratio(ws.get_forces()[hour_prevision/12],50,SQUARE_SIZE)
	start_x = end_x = middle_square_x = (ws.get_x()-longitude_start)*SQUARE_SIZE+(SQUARE_SIZE/2)
	start_y = end_y = middle_square_y = -1*(ws.get_y()-latitude_start)*SQUARE_SIZE+(SQUARE_SIZE/2)
	
	start_x,start_y = mytools.calculate_polare_mouvement(middle_square_x,middle_square_y,-1*(LEN_ARROW/2),ws.get_angles()[hour_prevision/12])

	end_x,end_y = mytools.calculate_polare_mouvement(middle_square_x,middle_square_y,LEN_ARROW/2,ws.get_angles()[hour_prevision/12])

	self.canvas.create_line(start_x,start_y,
		end_x,end_y,
		arrow=LAST,fill="red")

	self.canvas.create_text((ws.get_x()-longitude_start)*SQUARE_SIZE+(SQUARE_SIZE/2),-1*(ws.get_y()-latitude_start)*SQUARE_SIZE+(SQUARE_SIZE/2),
		anchor=W,
            	text=str(ws.get_forces()[hour_prevision/12]))
	
    def button_0h(self,*args):
	self.showSea(self.longitude_start,self.latitude_start,self.longitude_end,self.latitude_end,0)
	
    def button_12h(self,*args):
	self.showSea(self.longitude_start,self.latitude_start,self.longitude_end,self.latitude_end,12)

    def button_24h(self,*args):
	self.showSea(self.longitude_start,self.latitude_start,self.longitude_end,self.latitude_end,24)
	
    def button_close(self,*args):
	sys.exit()

    def button_update(self,*args):
	#self.sea.generate_random_sea()
	self.showSea(-50,-40,-40,-30)

              




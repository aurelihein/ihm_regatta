#!/usr/bin/python
# -*- coding: utf-8 -*-


from Tkinter import *
from ttk import Frame, Button, Label, Style
import Image, ImageTk, sys, math
import regatta_api as myapi
import regatta_tools as mytools

SQUARE_SIZE = 50


class RegattaMainFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.sea = myapi.Sea()
        self.parent = parent
	self.longitude_start=-50
	self.latitude_start=-40
	self.longitude_end=-40
	self.latitude_end=-30
	self.myLongitude = 0
	self.myLatitude = 0
	self.myCap = 0
	self.objectif=[0,0,0,0]
	self.text_distance=StringVar()
	self.text_distance.set("0km")
	self.text_angle=StringVar()
	self.text_angle.set("0°")
	self.text_wind_angle=StringVar()
	self.text_wind_angle.set("0°")
	self.text_debug=StringVar()
	self.text_debug.set("debug:")
	self.myCalcCSV=[]

    def setMyCalcCSV(self,calc):
	self.myCalcCSV=calc

    def motion(self,event):
	click_x = (event.x/(SQUARE_SIZE*1.0))+self.longitude_start
	click_y = (event.y/(SQUARE_SIZE*1.0))-self.latitude_start
	delta_x = abs(click_x - self.myLongitude)
	delta_y = abs(click_y + self.myLatitude)
	distance = mytools.calculate_pythagore(mytools.convert_horaires_to_km(delta_x),mytools.convert_horaires_to_km(delta_y))
	#self.update_text_distance_label("Distance: "+str((mytools.convert_horaires_to_km(delta_x)**2+mytools.convert_horaires_to_km(delta_y)**2)**0.5)+" km")
	self.update_text_distance_label("Distance: "+str(distance)+" km")
	
	calculate_new_angle = mytools.calculate_angle_degree_between_points(
			(self.myLongitude-self.longitude_start),
			(self.myLatitude-self.latitude_start),
			(click_x-self.longitude_start),
			((click_y+self.latitude_start)*-1.0))
	calculate_new_angle=int(calculate_new_angle)
	self.update_text_angle_label("Boat angle:"+str(calculate_new_angle)+"°")
	the_square = self.sea.get_squares_at(self.myLongitude,self.myLatitude)
	wind_angle=mytools.calculate_angle_au_vent(calculate_new_angle,the_square.get_angles()[0]-90)
	self.update_text_wind_angle_label("Wind Angle:"+str(wind_angle)+"°")
	calculate_speed=mytools.find_closest_calc(the_square.get_forces()[0],wind_angle,self.myCalcCSV)
	self.update_text_debug_label("Calculate speed:"+str(round(calculate_speed[0],1))+"Km/h")

    def click_left(self,event):
	click_x = (event.x/(SQUARE_SIZE*1.0))+self.longitude_start
	click_y = (event.y/(SQUARE_SIZE*1.0))-self.latitude_start
	delta_x = abs(click_x - self.myLongitude)
	delta_y = abs(click_y + self.myLatitude)
	print "Clic gauche détecté en X=" + str(click_x) +",Y=" + str(click_y)+ ",DX=" + str(delta_x) +",DY=" + str(delta_y)
	self.showClick(event.x,event.y)

    def click_right(self,event):
	click_x = (event.x/(SQUARE_SIZE*1.0))+self.longitude_start
	click_y = (event.y/(SQUARE_SIZE*1.0))-self.latitude_start
	delta_x = abs(click_x - self.myLongitude)
	delta_y = abs(click_y + self.myLatitude)
	print "Clic droit détecté en X=" + str(click_x) +",Y=" + str(click_y)+ ",DX=" + str(delta_x) +",DY=" + str(delta_y)
	print ("Distance: dx="+str(mytools.convert_horaires_to_km(delta_x))+",dy="+str(mytools.convert_horaires_to_km(delta_y)))
	self.showClick(event.x,event.y)

    def set_sea_screen(self,longitude_start,latitude_start,longitude_end,latitude_end ):
        self.longitude_start=longitude_start
	self.latitude_start=latitude_start
	self.longitude_end=longitude_end
	self.latitude_end=latitude_end

    def initUI(self):
      
        self.parent.title("IHM Virtual Regatta")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=1)
        #self.columnconfigure(3, pad=7)
        self.rowconfigure(6, weight=1)
        #self.rowconfigure(5, pad=7)
        
	user_btn = Button(self, text="User",command=self.button_update)
        user_btn.grid(row=0, column=0)
        help_btn = Button(self, text="Help")
        help_btn.grid(row=1, column=0)
	ok_btn = Button(self, text="OK")
        ok_btn.grid(row=2, column=0)
	update_btn = Button(self, text="Update",command=self.button_update)
        update_btn.grid(row=3, column=0)

	text_distance_label = Label(self, textvariable=self.text_distance)
	text_distance_label.grid(row=0,column=1)
	text_angle_label = Label(self, textvariable=self.text_angle)
	text_angle_label.grid(row=1,column=1)
	text_wind_angle_label = Label(self, textvariable=self.text_wind_angle)
	text_wind_angle_label.grid(row=2,column=1)
	text_debug_label = Label(self, textvariable=self.text_debug)
	text_debug_label.grid(row=3,column=1)

	if False :
		self.canvas = Canvas(self,
			width=(self.longitude_start-self.longitude_end)*SQUARE_SIZE,
			height=(self.latitude_end-self.latitude_start)*SQUARE_SIZE)
	else :
		self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.grid(row=6, column=1, columnspan=3, sticky=E+W+S+N)
	self.canvas.bind("<Button-1>", self.click_left)
	self.canvas.bind("<Button-2>", self.click_right)
	self.canvas.bind("<Motion>", self.motion)
	

	#self.imageTk = ImageTk.PhotoImage(Image.open("saved_png/map_6_10_11.png"))
	#self.canvas.create_image(0,0, anchor=NW, image=self.imageTk)

	self.showSea(self.longitude_start,self.latitude_start,self.longitude_end,self.latitude_end)
               

	zero_btn = Button(self, text="0H",command=self.button_0h)
        zero_btn.grid(row=0, column=2)
        douze_btn = Button(self, text="12H",command=self.button_12h)
        douze_btn.grid(row=1, column=2)
        vingtquatre_btn = Button(self, text="24H",command=self.button_24h)
        vingtquatre_btn.grid(row=2, column=2)
        close_btn = Button(self, text="Close",command=self.button_close)
        close_btn.grid(row=4, column=2)

    def update_text_debug_label(self,text):
	self.text_debug.set(text)
    def update_text_distance_label(self,text):
	self.text_distance.set(text)
    def update_text_wind_angle_label(self,text):
	self.text_wind_angle.set(text)
    def update_text_angle_label(self,text):
	self.text_angle.set(text)
    def set_objectif(self,x1,y1,x2,y2):
	self.objectif=[x1,y1,x2,y2]

    def set_myposition(self,longitude,latitude,cap):
	self.myLongitude=longitude
	self.myLatitude=latitude
	self.myCap=cap

    def set_sea(self,sea):
	self.sea = sea

    def get_sea(self,sea):
	return self.sea
        
    def showSea(self,longitude_start,latitude_start,longitude_end,latitude_end,hour_prevision=0):
	for i in self.sea.get_squares() :
		if i.get_x() >= longitude_start and i.get_x() <= longitude_end and i.get_y() <= latitude_start and i.get_y() >= latitude_end :
			self.showWindSquareBlock(i,longitude_start+0.5,latitude_start-0.5)
			self.showWindSquarePosition(i,longitude_start+0.5,latitude_start-0.5)
			self.showWindSquareWind(i,longitude_start+0.5,latitude_start-0.5,hour_prevision)
		#else :
			#print "bad block in:("+str(i.get_x())+","+str(i.get_y())+")"
	self.showBoat(self.myLongitude,self.myLatitude,longitude_start,latitude_start)
	self.showObjectif(self.objectif,longitude_start,latitude_start)
	#self.showArrivalFromStartPointWithTime(self.myLongitude,self.myLatitude,3600*12,hour_prevision)
     
    def showArrivalFromStartPointWithTimeAndAngle(self,x,y,time,twelve_hours,angle):
	the_square = self.sea.get_squares_at(x,y)
	wind_angle=mytools.calculate_angle_au_vent(angle,the_square.get_angles()[twelve_hours/12]-90)
	speed_calculate = mytools.find_closest_calc(the_square.get_forces()[twelve_hours/12],wind_angle,self.myCalcCSV)
	arrival = mytools.calculate_arrival(x,y,speed_calculate[0],angle,time)
	return arrival
   
    def showArrivalFromStartPointWithTime(self,x,y,time,twelve_hours):
	for angle in range(0,360):
		arrival = self.showArrivalFromStartPointWithTimeAndAngle(x,y,time,twelve_hours,angle)	
		self.showElement(arrival[0],arrival[1])
		#print arrival


    def showElement(self,x,y):
	LEN_CIRCLE=2
	x_draw = (x - self.longitude_start)*SQUARE_SIZE
	y_draw = (y - self.latitude_start)*-1*SQUARE_SIZE
	#print "x:"+str(x_draw)+" y:"+str(y_draw)
	self.canvas.create_oval(x_draw-LEN_CIRCLE/2,y_draw-LEN_CIRCLE/2,x_draw+LEN_CIRCLE/2,y_draw+LEN_CIRCLE/2,fill="yellow")


    def showClick(self,x,y):
	LEN_CIRCLE=4
        x_draw = x
	y_draw = y
	#print "x:"+str(x_draw)+" y:"+str(y_draw)
	self.canvas.create_oval(x_draw-LEN_CIRCLE/2,y_draw-LEN_CIRCLE/2,x_draw+LEN_CIRCLE/2,y_draw+LEN_CIRCLE/2,fill="yellow")

    def showBoat(self,x,y,longitude_start,latitude_start):
	LEN_CIRCLE=6
	x_draw = (x - longitude_start)*SQUARE_SIZE
	y_draw = (y - latitude_start)*-1*SQUARE_SIZE
	#print "x:"+str(x_draw)+" y:"+str(y_draw)
	self.canvas.create_oval(x_draw-LEN_CIRCLE/2,y_draw-LEN_CIRCLE/2,x_draw+LEN_CIRCLE/2,y_draw+LEN_CIRCLE/2,fill="green")

    def showObjectif(self,objectif,longitude_start,latitude_start):
	#print objectif
	self.canvas.create_line((objectif[0]-longitude_start)*SQUARE_SIZE,(objectif[1]-latitude_start)*-1*SQUARE_SIZE,
		(objectif[2]-longitude_start)*SQUARE_SIZE,(objectif[3]-latitude_start)*-1*SQUARE_SIZE,
		arrow=BOTH,fill="yellow", width=5)	

    def showWindSquarePosition(self,ws,longitude_start,latitude_start):
        self.canvas.create_text((ws.get_x()-longitude_start)*SQUARE_SIZE+1,-1*(ws.get_y()-latitude_start)*SQUARE_SIZE+7,
		anchor=W,
            	text=str(ws.get_y()*(-1))+","+str(ws.get_x()*(-1)))

    def showWindSquareBlock(self,ws,longitude_start,latitude_start):
	self.canvas.create_rectangle((ws.get_x()-longitude_start)*SQUARE_SIZE, -1*(ws.get_y()-latitude_start)*SQUARE_SIZE,
		(ws.get_x()-longitude_start)*SQUARE_SIZE+SQUARE_SIZE, -1*(ws.get_y()-latitude_start)*SQUARE_SIZE+SQUARE_SIZE,
		outline="#000", fill="#0af") 

    def showWindSquareWind(self,ws,longitude_start,latitude_start,hour_prevision=0):
	LEN_ARROW=mytools.do_ratio(ws.get_forces()[hour_prevision/12],SQUARE_SIZE,40)
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

              




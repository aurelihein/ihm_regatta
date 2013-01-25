#!/usr/bin/python
# -*- coding: utf-8 -*-


from Tkinter import *
from ttk import Frame, Button, Label, Style
import Image, ImageTk, sys, math
import regatta_ihm as myihm
import regatta_api as myapi
import regatta_tools as mytools
import regatta_connect as myconnect

default_userid="2350414"
default_checksum="a235bc2578dd67a5d262745d68c56452"
default_getuser_checksum="edb7c4033a505de839d9fb9fe438e109975ce103"

if __name__ == '__main__':

	if True :
		longitude_start=-42.5
		latitude_start=-10.5
		longitude_end=-24.5
		latitude_end=-24.5
	else :
		longitude_start=-50
		latitude_start=-30
		longitude_end=-40
		latitude_end=-40

	sea = myapi.Sea()
	connection = myconnect.RegattaConnection("","")
	connection.set_debug(1)
	#connection.try_login()
	connection.set_login(default_userid,default_checksum,default_getuser_checksum)
	connection.get_maps()

	connection.get_position_and_winddate()
	sea.set_squares(myapi.get_squares_from_to(connection=connection,
		longitude_start=longitude_start,latitude_start=latitude_start,
		longitude_end=longitude_end,latitude_end=latitude_end))
	root = Tk()
	root.geometry("1200x850+300+300")
	ihm = myihm.RegattaMainFrame(root)
	ihm.setMyCalcCSV(mytools.read_vent_vitesse_csv("voile-vitesses-full.csv"))
	ihm.set_sea(sea)
	ihm.set_sea_screen(longitude_start,latitude_start,longitude_end,latitude_end)
	ihm.set_myposition(connection.get_my_position()[0],connection.get_my_position()[1],connection.get_my_position()[2])
	#ihm.set_objectif(-41,-22,-31,-22)
	#ihm.set_myposition(-41.9,-33.1,80)
	the_square=sea.get_squares_at(connection.get_my_position()[0],connection.get_my_position()[1])
	print "myCap:"+str(connection.get_my_position()[2])+",wind angle:"+str(the_square.get_angles()[0])
	print "calcul:"+str(360-connection.get_my_position()[2]-the_square.get_angles()[0])
	ihm.initUI()
	#ihm.showArrivalFromStartPointWithTime(connection.get_my_position()[0],connection.get_my_position()[1],3600*2,0)
	res=ihm.showArrivalFromStartPointWithTimeAndAngle(connection.get_my_position()[0],connection.get_my_position()[1],3600*12,0,90)
	mytools.showElement(res[0],res[1])
	root.mainloop()


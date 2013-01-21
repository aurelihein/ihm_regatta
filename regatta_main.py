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

if __name__ == '__main__':

	if True :
		longitude_start=-52
		latitude_start=-30
		longitude_end=-25
		latitude_end=-46	
	else :
		longitude_start=-50
		latitude_start=-30
		longitude_end=-40
		latitude_end=-40

	sea = myapi.Sea()
	connection = myconnect.RegattaConnection("","")
	connection.set_debug(1)
	#connection.try_login()
	connection.set_login(default_userid,default_checksum)
	sea.set_squares(myapi.get_squares_from_to(connection=connection,
		longitude_start=longitude_start,latitude_start=latitude_start,
		longitude_end=longitude_end,latitude_end=latitude_end))
	root = Tk()
	root.geometry("1200x900+300+300")
	app = myihm.RegattaMainFrame(root)
	app.set_sea(sea)
	app.set_sea_screen(longitude_start,latitude_start,longitude_end,latitude_end)
	app.initUI()
	root.mainloop()


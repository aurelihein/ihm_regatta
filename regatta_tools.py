#!/usr/bin/python
# -*- coding: utf-8 -*-

import regatta_api as myapi
import math
import xml.etree.ElementTree as ET

debug = 1

def calculate_polare_mouvement(x,y,length,angle):
	new_x = x + length * math.cos(math.pi*angle/180)
	new_y = y + length * math.sin(math.pi*angle/180)
	return new_x,new_y

def do_ratio(value,max_equivalent,max):
	return ((value*max_equivalent*1.0)/(max*1.0))

def transform_wind_xml_into_WindsSquare(xml):

	squares = []
	if xml == "" :
		print "No XML in input"
		return squares
	previsions = ET.fromstring(xml)
	#for prevision in previsions :
	prevision = previsions[0]
	x_origin = int(previsions.get("LONGITUDESTART"))
	y_origin = int(previsions.get("LATITUDESTART"))
	x = 0
	y = 0
	#creation
	for a_wind in prevision :
		if y <= -10 :
			y  = 0
			x = x + 1
		#print a_wind.attrib
		force = int(a_wind.get("V"))
		angle = int(a_wind.get("D"))+90
		#print "force:"+str(force)+",angle:"+str(angle)
		squares.append(myapi.WindSquare(x+x_origin,y+y_origin,[force],[angle]))
		y = y - 1
	
	prevision = previsions[1]
	i = 0
	#insertion
	for a_wind in prevision :
		#print a_wind.attrib
		force = int(a_wind.get("V"))
		angle = int(a_wind.get("D"))+90
		squares[i].set_forces(squares[i].get_forces()+[force])
		squares[i].set_angles(squares[i].get_angles()+[angle])
		#print "force:"+str(force)+",angle:"+str(angle)
		#print "forces:"+str(squares[i].get_forces())+",angles:"+str(squares[i].get_angles())
		i = i + 1

	prevision = previsions[2]
	i = 0
	#insertion
	for a_wind in prevision :
		#print a_wind.attrib
		force = int(a_wind.get("V"))
		angle = int(a_wind.get("D"))+90
		squares[i].set_forces(squares[i].get_forces()+[force])
		squares[i].set_angles(squares[i].get_angles()+[angle])
		#print "force:"+str(force)+",angle:"+str(angle)
		#print "forces:"+str(squares[i].get_forces())+",angles:"+str(squares[i].get_angles())
		i = i + 1

	return squares
				
	

	#version = root.find("version").text
	#urlMaps = root.find("UrlMaps").text
	#urlWinds = root.find("UrlWinds").text
	#urlVPP = root.find("UrlVPP").text

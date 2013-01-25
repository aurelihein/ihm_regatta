#!/usr/bin/python
# -*- coding: utf-8 -*-

import regatta_api as myapi
import math,csv
import xml.etree.ElementTree as ET

debug = 1

CONVERSION_HORAIRE_KM=111.195
CONVERSION_NOEUD_KM_H=1.852

def read_vent_vitesse_csv(url):
	print ("reading CSV:"+url);
	speeds = csv.reader(open(url), delimiter=';', quotechar='"')
	rows = []
	for row in speeds:
		#print ', '.join(row)
		#afoc2.append(float(row[0]))
		#foc2.append(float(row[1]))
		#for i in row:
		rows.append(row)
	return rows

def find_closest_calc(wind_speed,angle_au_vent,calc):
	#print "find closest speed from :"+str(wind_speed)+",angle:"+str(angle_au_vent)+"°"
	##calc[Colonnes des angles][Ligne des vitesses]
	wind_speed_noeud = round((wind_speed*1.0 / CONVERSION_NOEUD_KM_H),4)
	ordonnee = 0
	found=""
	for i in range(1,len(calc[0])):
		if float(wind_speed_noeud) == float(calc[0][i]):
			ordonnee=i
	for i in range(1,len(calc)):
		if angle_au_vent==int(calc[i][0]):
			found = calc[i][ordonnee]
		if angle_au_vent < int(calc[i][0]):
			found = calc[i-1][ordonnee]
		if not found == "":
			returned = found.split(":")
			returned[0] = float(returned[0])*CONVERSION_NOEUD_KM_H
			return returned
	return [ 0,'0']

def do_ratio(value,max_equivalent,max):
	return ((value*max_equivalent*1.0)/(max*1.0))

def convert_horaires_to_km(heure):
	return ((heure*1.0)*CONVERSION_HORAIRE_KM)

def calculate_arrival(x,y,speed,angle,time):
	print("speed:"+str(speed))
	speed_in_sec = speed*1.0/3600		#speed in Km/sec
	distance_in_time = speed_in_sec * time	#distance in Km for 'time' seconds
	distance_in_polare = distance_in_time/100
	print("distance_in_polare:"+str(distance_in_polare))
	return calculate_polare_mouvement(x,y,distance_in_polare,angle)

def calculate_pythagore(cote_a,cote_b):
	return ((cote_a*1.0)**2+(cote_b*1.0)**2)**0.5

def calculate_angle_degree_between_points(x1,y1,x2,y2):
	returned = ((180*math.atan2(x2-x1,y2-y1))/math.pi)
	if returned < 0 :
		returned = returned + 360
	return returned

def calculate_angle_au_vent(angle_du_bateau,angle_du_vent):
	#print("calculate_angle_au_vent("+str(angle_du_bateau)+","+str(angle_du_vent)+")")
	angle_au_vent=360-angle_du_bateau+angle_du_vent
	if angle_au_vent > 360 :
		angle_au_vent = angle_au_vent -360
	if angle_au_vent > 180 :
		angle_au_vent = 360 - angle_au_vent
	return angle_au_vent

def calculate_polare_mouvement(x,y,length,angle):
	new_x = x + length * math.cos(math.pi*angle/180)
	new_y = y + length * math.sin(math.pi*angle/180)
	return new_x,new_y

def get_windDate_from_user_xml(xml):
	if xml == "" :
		print "No XML in input"
		return ""
	result = ET.fromstring(xml)
	for child in result:
		if child.tag=="user":
			return child.attrib.get("windDate")

def get_position_from_user_xml(xml):
	longitude = 0
	latitude = 0
	cap = 0
	speed = 0
	if xml == "" :
		print "No XML in input"
		return ""
	result = ET.fromstring(xml)
	for child in result:
		if child.tag=="user":
			for min_child in child :
				if min_child.tag=="position":
					for min_min_child in min_child :
						if min_min_child.tag == "longitude":
							longitude = float(min_min_child.text)
						if min_min_child.tag == "latitude":
							latitude = float(min_min_child.text)
						if min_min_child.tag == "cap":
							cap = int(min_min_child.text)
						if min_min_child.tag == "vitesse":
							speed = float(min_min_child.text)#*CONVERSION_NOEUD_KM_H
	return [longitude, latitude, cap,speed ]
					

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

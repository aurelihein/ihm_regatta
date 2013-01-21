#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import regatta_ihm as myihm
import regatta_api as myapi
import regatta_tools as mytools
import regatta_connect as myconnect

class WindSquare(object):
    def __init__(self, x,y, forces, angles):
	self.x = x
	self.y = y
	self.forces = forces
	self.angles = angles
    def get_x(self):
	return self.x
    def get_y(self):
	return self.y
    def get_angles(self):
	return self.angles
    def get_forces(self):
	return self.forces
    def set_angles(self,angles):
	self.angles = angles
    def set_forces(self,forces):
	self.forces=forces
    def __str__(self):
	return "("+str(self.x)+","+str(self.y)+")=F:"+str(self.forces)+",A:"+str(self.angles)


class Sea(object):
    def __init__(self,dim_x=10,dim_y=10):
	self.dim_x = dim_x
	self.dim_y = dim_y
	self.squares=[]
    def generate_random_sea(self):
	for x in range(self.dim_x) :
		for y in range(self.dim_y) :
			self.squares.append(WindSquare(x,y,random.randint(0,60),random.randint(0,359)))
    def set_squares(self,squares):
	self.squares = squares
    def get_dim_x(self):
	return self.dim_x
    def get_dim_y(self):
	return self.dim_y
    def get_squares(self):
	return self.squares
    def get_squares_at(self,x,y):
	for i in self.squares :
		if i.get_x() == x and i.get_y() == y :
			return i
    def __str__(self):
	all_str=""

	if len(self.get_squares()) == 0 :
		return "NULL"
	for i in self.get_squares():
		all_str = all_str+str(i)+'\n'
	return all_str

def get_squares_from_to(connection,longitude_start,latitude_start,longitude_end,latitude_end):
	if longitude_start >= longitude_end or latitude_start <= latitude_end :
		raise ValueError("It should be longitude_start < longitude_end et latitude_start > latitude_end")
	longitude_start_searched = (longitude_start /10)*10
	latitude_start_searched = (latitude_start /10)*10
	longitude_end_searched = (longitude_end /10)*10
	latitude_end_searched = (latitude_end /10)*10
	#if longitude_start % 10 or longitude_end % 10 or latitude_start % 10 or latitude_end % 10 :
	#	raise ValueError("longitude_start,longitude_end,latitude_start,latitude_end has to be modulo 10")
	nb_longitude_to_ask=(longitude_start_searched - longitude_end_searched)*-1 / 10
	nb_latitude_to_ask=(latitude_start_searched - latitude_end_searched) / 10
	#print "nb_longitude_to_ask:"+str(nb_longitude_to_ask)
	#print "nb_latitude_to_ask:"+str(nb_latitude_to_ask)
	squares=[]	
	for lon in range(0,nb_longitude_to_ask) :
		for lat in range(0,nb_latitude_to_ask) :
			winds_xml = connection.get_winds_xml(longitude=str(longitude_start_searched+10*lon),latitude=str(latitude_start_searched-10*lat))
			squares = squares + mytools.transform_wind_xml_into_WindsSquare(winds_xml)
	return squares

if __name__ == '__main__':
	sea = Sea()
	sea.generate_random_sea()
	print sea

#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv, sys

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
	##calc[Colonnes des angles][Ligne des vitesses]
	wind_speed_noeud = round((wind_speed*1.0 / 1.852),4)
	ordonnee = 0
	found=""
	for i in range(1,len(calc[0])):
		if float(wind_speed_noeud) == float(calc[0][i]):
			ordonnee=i
			print ("ordonnee="+str(ordonnee))
	for i in range(1,len(calc)):
		if angle_au_vent==int(calc[i][0]):
			found = calc[i][ordonnee]
		if angle_au_vent < int(calc[i][0]):
			found = calc[i-1][ordonnee]
		if not found == "":
			returned = found.split(":")
			returned[0] = float(returned[0])*1.852
			return returned
	return [ 0,'0']

def calculate_angle_au_vent(angle_du_bateau,angle_du_vent):
	angle_au_vent=360-angle_du_bateau+angle_du_vent
	if angle_au_vent > 360 :
		angle_au_vent = angle_au_vent -360
	if angle_au_vent > 180 :
		angle_au_vent = 360 - angle_au_vent
	return angle_au_vent


if __name__ == '__main__':

	calc = read_vent_vitesse_csv("voile-vitesses-full.csv")
	print find_closest_calc(21,147,calc)
	
	sys.exit()

	print "Calcul de l'angle au vent"
	angle_du_vent=int(raw_input("angle du vent:"))
	force_du_vent=int(raw_input("force du vent:"))

	while True :
		angle_du_bateau=int(raw_input("angle du bateau:"))
		print "resultat :"+str(calculate_angle_au_vent(angle_du_bateau,angle_du_vent))

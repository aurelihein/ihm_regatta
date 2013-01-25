import cookielib, urllib, urllib2, sys, time
import regatta_tools as mytools

base_path="http://vendeeglobevirtuel.virtualregatta.com/core/Service/ServiceCaller.php"

class RegattaConnection(object):
	def __init__(self,mail,password):
		self.mail = mail
		self.password = password
		self.debug = 0
		self.userid=""
		self.checksum=""
		self.getuser_checksum=""
		self.winddate=""
		self.myLongitude=0
		self.myLatitude=0
		self.myCap=0
		self.mySpeed=0
	def __str__(self):
		return "userid:"+str(self.userid)+"-checksum:"+str(self.checksum)
	def get_maps(self):
		directory_saved="saved_png/"
		very_base_url = "http://datacenter.manyplayers.com/maps/dalles/4227081/"
		a = 5
		for b in range(0,12) :
			for c in range(0,8):
				continuous_url = "/"+str(a)+"/"+str(int(b/10))+"/"+str(int(c/10))+"/"
				png_url = "map_"+str(a)+"_"+str(b)+"_"+str(c)+".png"
				try :
					with open(directory_saved+png_url) as f:
						#we already have it in directory
						returned = f.read()
						#print "Get xml from file"
				except :
					#download it because we don't have it yet
					img = self.get_a_map_png(very_base_url+continuous_url+png_url)
					if not img == "":
						open(directory_saved+png_url,"wb").write(img)
		a = 6
		for b in range(0,24) :
			for c in range(0,16):
				continuous_url = "/"+str(a)+"/"+str(int(b/10))+"/"+str(int(c/10))+"/"
				png_url = "map_"+str(a)+"_"+str(b)+"_"+str(c)+".png"
				try :
					with open(directory_saved+png_url) as f:
						#we already have it in directory
						returned = f.read()
						#print "Get xml from file"
				except :
					#download it because we don't have it yet
					img = self.get_a_map_png(very_base_url+continuous_url+png_url)
					if not img == "":
						open(directory_saved+png_url,"wb").write(img)

	def get_a_map_png(self,url):
		returned = ""
		try :
			returned = urllib2.urlopen(url).read()
			print("Fetching png url:"+url)
		except urllib2.HTTPError, e:
			print "bad url:"+str(e.code)+"=>"+url
		return returned

	def get_login(self):
		return str(self)
	def set_login(self,userid,checksum,getuser_checksum):
		self.userid = userid
		self.checksum = checksum
		self.getuser_checksum = getuser_checksum
	def set_debug(self,value):
		self.debug = value
	def try_login(self):
		cookiejar = cookielib.CookieJar()
		self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
		values = {'mail':self.mail, 'pass':self.password}
		data = urllib.urlencode(values)
		request_headers = { 'User-Agent': 'Firefox/3.0.4' }
		request = urllib2.Request("http://www.virtualregatta.com/login.php?destination=/", data, request_headers)
		url = self.urlOpener.open(request)
		page = url.read(500000)

		if "login=false" in page :
			raise ValueError, "Login failed with login=%s, password=%s" % (mail, password)
			return False

		if not 'PHPSESSID' in [cookie.name for cookie in cookiejar]:
			raise ValueError, "Login failed with login=%s, password=%s" % (mail, password)
			return False

		if self.debug > 0:
		  print "We are logged in !"
		  print '------------------'
		  for cookie in cookiejar:
		    print cookie.name
		    #print cookie
		  print '------------------'

		request = urllib2.Request("http://www.virtualregatta.com/index_vgv2012.php", '', request_headers)
		get_userid =self.urlOpener.open(request).read(500000)

		self.userid =  get_userid.partition("id_user=")[2].split("&")[0]
		self.checksum =  get_userid.partition("checksum=")[2].split("&")[0]
		return True

	def is_connected(self):
		if self.userid == "" or self.checksum == "" :
			return False
		return True

	def get_position_and_winddate(self):
		if self.is_connected() == False :
			raise ValueError, "Unable to get_position without being logged in"
			return False
		url=base_path+"?service=GetUser&id_user="+self.userid+"&lang=FR&light=1&checksum="+self.getuser_checksum
		print url
		get_position_xml = urllib2.urlopen(url).read(500000)
		self.winddate=mytools.get_windDate_from_user_xml(get_position_xml)
		self.myLongitude,self.myLatitude,self.myCap,self.mySpeed=mytools.get_position_from_user_xml(get_position_xml)
		#print "windDate:"+self.winddate
		print "position:"+str(self.myLongitude)+","+str(self.myLatitude)+"|cap:"+str(self.myCap)+"|speed:"+str(self.mySpeed)
		return get_position_xml

	def get_my_position(self):
		return self.myLongitude,self.myLatitude,self.myCap,self.mySpeed

	def get_winds_xml(self,longitude,latitude):
		magic_numbers=["075849","115805","075922","115839"]
		if self.is_connected() == False :
			raise ValueError, "Unable to get_winds_xml without being logged in"
			return False
		today=time.strftime("%Y%m%d")
		if time.strftime("%p")=='AM' :
			magic_number=magic_numbers[2]
		else:
			magic_number=magic_numbers[3]

		url = "http://datacenter.manyplayers.com/winds/dated_1x1/"
		if self.winddate=="":
			url = url + "/"+latitude+"/meteo_"+today+magic_number+"_"+longitude+"_"+latitude+".xml"
		else :
			url = url + "/"+latitude+"/meteo_"+self.winddate+"_"+longitude+"_"+latitude+".xml"
		fileurl="meteo_"+today+"_"+longitude+"_"+latitude+".xml"
		try :
			with open("saved_xml/"+fileurl) as f:
				returned = f.read()
				#print "Get xml from file"
		except :
			returned = self.get_a_winds_xml(url)
			myFile = open("saved_xml/"+fileurl,'w')
			myFile.write(returned)
			myFile.close()
			print "Get xml from web"		
		return returned

	def get_a_winds_xml(self,url):
		returned = ""
		try :
			returned = urllib2.urlopen(url).read(500000)
		except urllib2.HTTPError, e:
			print "bad url:"+str(e.code)+"=>"+url
		return returned
		#for latitude in latitudes :
		#	url = base_path+latitude+"/meteo_"+"20130116"+"115955_-70_"+latitude+".xml"
		#	get_wind_xml = urllib2.urlopen(url).read(500000)
		#	print "----------------------- latitude :"+latitude+"----------------"
		#	print get_wind_xml

if __name__ == '__main__':

	userid,checksum = get_login()
	#userid,checksum = get_default_login()


	print "userid:"+str(userid)
	print "checksum:"+str(checksum)


	#get_position(base_path,userid,checksum)

	#sys.exit()

	#datas_path="http://vendeeglobevirtuel.virtualregatta.com/index_vr.php?id_user="
	#datas_path=datas_path+str(userid)+"&checksum="+str(checksum)

	get_datas_xml = urllib2.urlopen(base_path+"?service=GetConfigFlash&test=1&checksum="+str(checksum)).read(500000)

	import xml.etree.ElementTree as ET
	root = ET.fromstring(get_datas_xml)

	version = root.find("version").text
	urlMaps = root.find("UrlMaps").text
	urlWinds = root.find("UrlWinds").text
	urlVPP = root.find("UrlVPP").text

	print "Version:"+str(version)
	print "urlWinds:"+str(urlWinds)

	get_winds_xml(urlWinds)




	#print get_datas
	sys.exit()

	values = {'id_user':userid, 'checksum':checksum}
	data = urllib.urlencode(values)
	request = urllib2.Request("http://vendeeglobe.virtualregatta.com/index_vr.php", data, request_headers)
	get_user = urlOpener.open(request).read(500000)
	print "get_user:"+str(get_user)



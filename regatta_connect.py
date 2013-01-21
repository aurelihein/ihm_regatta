import cookielib, urllib, urllib2, sys, time

base_path="http://vendeeglobevirtuel.virtualregatta.com/core/Service/ServiceCaller.php"

class RegattaConnection(object):
	def __init__(self,mail,password):
		self.mail = mail
		self.password = password
		self.debug = 0
		self.userid=""
		self.checksum=""
	def __str__(self):
		return "userid:"+str(self.userid)+"-checksum:"+str(self.checksum)
	def get_login(self):
		return str(self)
	def set_login(self,userid,checksum):
		self.userid = userid
		self.checksum = checksum
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

	def get_position(self):
		if self.is_connected() == False :
			raise ValueError, "Unable to get_position without being logged in"
			return False
		url=base_path+"?service=GetUser&id_user="+self.userid+"&lang=FR&light=1&auto=1&checksum="+self.checksum
		get_position_xml = urllib2.urlopen(url).read(500000)
		print "---------------------------------------"
		print get_position_xml

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
		url = url + "/"+latitude+"/meteo_"+today+magic_number+"_"+longitude+"_"+latitude+".xml"
		fileurl="meteo_"+today+"_"+longitude+"_"+latitude+".xml"
		try :
			with open("saved_xml/"+fileurl) as f:
				returned = f.read()
				print "Get xml from file"
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



import urllib2
import MySQLdb
import json
token = "c73c2803f8f0a8077be703fc6c8e2de301FFB148F5161DDB57CA17397743DE4C7518AF7D"
response = urllib2.urlopen('https://hst-api.wialon.com/wialon/ajax.html?svc=token/login&params={"token":"'+token+'"}')

#html = json.loads(response.read())
#eid=html['eid']
#print html
# https://hst-api.wialon.com/wialon/ajax.html?svc=report/exec_report&
# params={
#     "reportResourceId":8, //  Resource ID
#     "reportTemplateId":1, /// Report ID
#     "reportObjectId":13109362, // Unit ID
#     "reportObjectSecId":0,
#     "interval":{
#         "from":'.$fec1.',
#         "to":'.$fec2.',
#         "flags":0x00
#     }
# }&sid='.$sid
#response = urllib2.urlopen('https://hst-api.wialon.com/wialon/ajax.html?svc=report/exec_report&params={"reportResourceId":12217978,"reportTemplateId":8,"reportObjectId":13673232,"reportObjectSecId":0,"interval":{"from":1460937600,"to":1461024000,"flags":0x00}}&sid='+html['eid'])

# response = urllib2.urlopen('https://hst-api.wialon.com/wialon/ajax.html?svc=core/search_items&params={"spec":{"itemsType":"avl_resource","propName":"sys_name","propValueMask":"*","sortType":"sys_name"},"force":1,"flags":0x00000001,"from":0,"to":0}&sid='+eid)
# html= json.loads(response.read())
# print html
# # for item in html['items']:
#  	# response = urllib2.urlopen('https://hst-api.wialon.com/wialon/ajax.html?svc=report/exec_report&params={"reportResourceId":12217978,"reportTemplateId":8,"reportObjectId":'+str(item['id'])+',"reportObjectSecId":0,"interval":{"from":1460937600,"to":1461024000,"flags":0x00}}&sid='+eid)
# # 	try:
# # 		print html['reportLayer']['units']
# # 	except Exception,e:
# # 		pass

db= MySQLdb.connect("karshingenset.cmd1hqfd8bvh.us-west-2.rds.amazonaws.com","adityajain","pogo123","karshin" )
cursor = db.cursor()


sql_vehicles = "SELECT unitid, vehiclename, displayname FROM vehicle_master WHERE milage_counter = 1" 
cursor.execute(sql_vehicles)
data=cursor.fetchall()
for datapoint in data:
	print datapoint[0], datapoint[2]
	url= 'https://hst-api.wialon.com/wialon/ajax.html?svc=report/exec_report&params={"reportResourceId":12217978,"reportTemplateId":7,"reportObjectId":'+str(datapoint[0])+',"reportObjectSecId":0,"interval":{"from":1460937600,"to":1461024000,"flags":0x00}}&sid='+eid
	print url
	response = urllib2.urlopen(url)
	html= json.loads(response.read())
	print html

db.close()



# input_stop=raw_input("thank you press any key")
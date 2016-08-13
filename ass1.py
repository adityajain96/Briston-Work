import urllib2
import MySQLdb
import json
import numpy as np
import matplotlib.pyplot as plt

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


def fuellevel_list(bristonid,adclist):
    ######################### DB connection  ##############################
    db = MySQLdb.connect("karshingenset.cmd1hqfd8bvh.us-west-2.rds.amazonaws.com","adityajain","pogo123","karshin" )
    cursor = db.cursor()
    ######################### ^^^^^DB connection^^^^^  ####################


    ######################### Get Lookup Table  ##############################
    sql= "SELECT  lookupid FROM vehicle_master WHERE bristonid= " + str(bristonid) 
    cursor.execute(sql)
    data=cursor.fetchall()

    sql2="SELECT fuelid,fuellevel FROM lookup_"+str(data[0][0])
    cursor.execute(sql2)
    data=cursor.fetchall()
    ######################### ^^^^^^Get Lookup Table^^^^^  ##############################
    

    ######################### Convert to Fuel Level ##############################
    fuel_list=[]
    for adc in adclist:
        i=0
        fuellevel=0
        try:
            if (adc< data[0][0]):
                fuellevel=data[0][1]
                fuel_list.append(fuellevel)
            elif (adc> data[len(data)-1][0]):
                fuellevel=data[len(data)-1][1]
                fuel_list.append(fuellevel)
            else:
                for levels in data:
                    if (data[i][0] > adc):
                        fuellevel= (((adc-data[i-1][0])*(data[i][1]-data[i-1][1]))/(data[i][0]-data[i-1][0]))+data[i-1][1]
                        fuel_list.append(fuellevel)
                        break
                    i=i+1
                    
        except Exception,e:
            if (DEBUG==True):
                raise
            fuellevel=0.0
            fuel_list.append(fuellevel)
    ######################### ^^^^^^ Convert to Fuel Level ^^^^^^^^^^ ##############################

    return fuel_list

db= MySQLdb.connect("karshingenset.cmd1hqfd8bvh.us-west-2.rds.amazonaws.com","adityajain","pogo123","karshin" )
cursor = db.cursor()


sql_vehicles = "SELECT vehiclename, bristonid FROM vehicle_master WHERE username = 'srehitech'" 
cursor.execute(sql_vehicles)
data=cursor.fetchall()
bid_list=[]
for datapoint in data:
	print datapoint[0], datapoint[1]
	# url= 'https://hst-api.wialon.com/wialon/ajax.html?svc=report/exec_report&params={"reportResourceId":12217978,"reportTemplateId":7,"reportObjectId":'+str(datapoint[0])+',"reportObjectSecId":0,"interval":{"from":1460937600,"to":1461024000,"flags":x00}}&sid='+eid
	# #print url
	# response = urllib2.urlopen(url)
	# html= json.loads(response.read())
	bid_list.append(datapoint[1])
	#print html


for bristonid in bid_list[4:]:
	sql_voltages = "SELECT voltage,unixdatetime FROM gurtam_"+str(bristonid)+" WHERE unixdatetime between 1469432000 and 1469433000"
	#print sql_voltages 
	cursor.execute(sql_voltages)
	front=cursor.fetchall()
	#print front
	adc_list1=[]  #This will have the fuel level
	adc_list2=[]  #This has the date information
	fuel = [] 	  #This will hold the fuel level corresponding to the voltage level
	fuel_litre = []

	for voltages in front:
		adc_list1.append(voltages[0])
		adc_list2.append(voltages[1])
		fuel = fuellevel_list(bristonid,adc_list1)
		scl = 1000
		fuel_litre = [x/scl for x in fuel]
		#print voltages[1], voltages[0]
	
	

	plt.xlabel('Unix Timestamp')
	plt.ylabel('FuelLevel (in litres)')
	plt.title(bristonid)
	plt.plot(adc_list2, fuel_litre)
	plt.axis([1469432000, 1469433000, 0, 1500])
	plt.show()	
	#print fuellevel_list(bristonid,adc_list1)
	#print front[1]

#print fuellevel_list(bristonid,adc_list1) #This prints data of the last briston id bcz it is out of the loop






db.close()


# input_stop=raw_input("thank you press any key")

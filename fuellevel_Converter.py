def fuellevel_list(bristonid,adclist):
    ######################### DB connection  ##############################
    db = MySQLdb.connect("karshingenset.cmd1hqfd8bvh.us-west-2.rds.amazonaws.com","karshin","karshin1.1","karshin" )
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
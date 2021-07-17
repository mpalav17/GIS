import mysql.connector
import re
mydb = mysql.connector.connect(
    host = "localhost",
    database = "boondv1",
    user = "root",
    password = "root"
)
fw_id = 'M0001'
mycursor = mydb.cursor()
print("select district_name,tehsil_name,village_name from village_details where fw_id ='"+fw_id+"'")
mycursor.execute("select district_name,tehsil_name,village_name from village_details where fw_id ='"+fw_id+"'")
for d,t,v in mycursor:
    v="".join(re.split("[^a-zA-Z]*", v))
    print(d,t,v)

#Work pending
#Extract the rainfall from secondary source and do not hard-code it

def rainfall(area,village_name):
    if(village_name=='Konambe'):
        rainfall_amt=780#621
    elif(village_name=='Shastrinagar'):
        rainfall_amt=650#1031
    elif(village_name=='Kanhur'):
        rainfall_amt=500#550
    elif(village_name=='Kirtangali'):
        rainfall_amt=718#550
    rainfall_avail=(rainfall_amt*area)/100
    return rainfall_avail
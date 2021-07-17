import math

def seepage_canal(canal_type,minor_no,minor_length,bed_gradient,base_width,design_depth,water_top,water_mid,water_tail,days):
    #minor_length=minor_length/2
    surface_water=[]
    recharge_TCM=[]
    water_TCM=[]
    water=[water_top,water_mid,water_tail]
    for i in range(0,len(water)):
        water_head=water[i]
        total_water=water_head*0.028*24*days*60*60/1000
        water_TCM.append(total_water)
        wetted_perimeter=(2*0.6*design_depth/math.sin(math.atan(bed_gradient)))+base_width
        wetted_area=(wetted_perimeter*minor_length*1000/3)/(math.pow(10,6))
        #assumtion that the canal is unlined with some clay content along with sand
        #1.8 cumecs require 15 ham/day/million sq.m
        seepage_factor=water_head*0.028*15/1.8 
        if(canal_type=='lined'):
            seepage_factor=0.2*seepage_factor
        recharge=seepage_factor*wetted_area*days*10
        recharge_TCM.append(recharge)
        surface_water.append(total_water-recharge)
    print('The water alloted for the minor ',minor_no,' is ',water_TCM)
    print('The recharge for the minor ',minor_no,' is ',recharge_TCM)
    print('The surface water for the minor ',minor_no,' is ',surface_water)
    return water_TCM,recharge_TCM,surface_water
#seepage_canal('Waghad',12,2.04,0.00066,0.6,0.6,[18,3,1.24],5)
#seepage_canal('Waghad',12,2.04,0.00066,0.6,0.6,[16,3,1.24],4)

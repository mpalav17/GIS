
def supply_advisories(v,t,d,runoff,seepage,surface_water):
    total_runoff_arrested=(seepage*2)+surface_water
    total_runoff_arrested_percent=(total_runoff_arrested/runoff)*100
    print('Total runoff arrested is',total_runoff_arrested,' TCM or ',total_runoff_arrested_percent,'%')
    maximum_runoff=0.7*runoff
    print('Maximum runoff that can be arrested is',maximum_runoff,' TCM or 70%')
    if((maximum_runoff-total_runoff_arrested)<50):
        return 0
    else:
        rem_runoff=maximum_runoff-total_runoff_arrested
        print('Availability of the surplus surface runoff ',rem_runoff,' TCM')
        rem_runoff_actual=0.7*rem_runoff#at 70% efficiency
        return rem_runoff_actual
    
    

"""
 Created by Chouayakh Mahdi                                                       
 23/08/2010                                                                       
 The package contains functions that                                         
 Functions:                                                                       
                      
"""
from dialog.resources_manager import ResourcePool


"""
Statement of lists
"""
day_list = ResourcePool().days_list
month_list = ResourcePool().months_list



def refine_val(x,y,time,valeur):
    while x>=valeur:
        time[y]=time[x]/valeur
        time[x]=time[x]%valeur
    return time



def refine_clock(time):
    i=0
    time=refine_val('second','minute',time,60)
    time=refine_val('minute','hour',time,60)
    time=refine_val('hour','day',time,24)
    while i < len(month_list):
        if month_list[i][2]==time['month']:
            while month_list[i][1]<=time['day']:
                time['day']=time['day']-month_list[i][1]
                time['month']=time['month']+1
                i=i+1
            break
        else:
            i=i+1
            
    time=refine_val('month','year',time,12)
    
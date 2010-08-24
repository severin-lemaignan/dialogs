
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
adverb = ResourcePool().time_adverbs


def refine_val(x,y,time,valeur):
    time[y]=str(int(time[y])+int((time[x]))/valeur)
    time[x]=str(int(time[x])%valeur)
    return time


def negative_day(time):
    i=len(month_list)-1
    while i >= 0: 
        if int(time['day'])<=0:
            if month_list[i][0]==time['month']:
                if i==0:
                    i=len(month_list)-1
                    time['year']=str(int(time['year'])-1)
                else:
                    i=i-1
                if month_list[i][0]=='February' and int(time['year'])%4==0 and int(time['year'])%100!=0:
                    time['day']=str(int(time['day'])+29)
                else:
                    time['day']=str(int(time['day'])+int(month_list[i][1]))
                time['month']=month_list[i][0]
            else:
                i=i-1
        else:
            return time
    
    
    

def refine_clock(time):
    i=0
    time=refine_val('second','minute',time,60)
    time=refine_val('minute','hour',time,60)
    time=refine_val('hour','day',time,24)
    
    while i < len(month_list):
        if month_list[i][0]==time['month']:
          
            if time['month']=='February' and int(time['year'])%4==0 and int(time['year'])%100!=0:
                if int(time['day'])<=29:
                    return negative_day(time)
                else:
                    time['day']=str(int(time['day'])-29)
                    time['month']=month_list[i+1][0]
            else:
                if int(time['day'])<=int(month_list[i][1]):
                    return negative_day(time)
                else:
                    time['day']=str(int(time['day'])-int(month_list[i][1]))
                    if i==11:
                        time['month']=month_list[0][0]
                    else:
                        time['month']=month_list[i+1][0]
        if i==11:
            i=-1
            time['year']=str(int(time['year'])+1)

        i=i+1
  
    return negative_day(time)



def day_period(time, period):
    if period==1:
        time_beg={'year':time['year'],'month':time['month'],'day':time['day'],'hour':'4','minute':'0','second':'0'}
        time_end={'year':time['year'],'month':time['month'],'day':time['day'],'hour':'12','minute':'59','second':'59'}
        action_time={'time_begin':time_beg, 'time_end':time_end}
    elif period==2:
        time_beg={'year':time['year'],'month':time['month'],'day':time['day'],'hour':'13','minute':'0','second':'0'}
        time_end={'year':time['year'],'month':time['month'],'day':time['day'],'hour':'17','minute':'59','second':'59'}
        action_time={'time_begin':time_beg, 'time_end':time_end}
    elif period==3:
        time_beg={'year':time['year'],'month':time['month'],'day':time['day'],'hour':'18','minute':'0','second':'0'}
        time_end={'year':time['year'],'month':time['month'],'day':time['day'],'hour':'3','minute':'59','second':'59'}
        action_time={'time_begin':time_beg, 'time_end':time_end}
    elif period==0:
        time_beg={'year':time['year'],'month':time['month'],'day':time['day'],'hour':time['hour'],'minute':time['minute'],'second':time['second']}
        action_time={'time_begin':time_beg, 'time_end':time_beg}
    return action_time



def timescale_adverb(time, adv):
    
    #init
    action_time=None
    
    for i in adverb:
        if adv==i[0]:
            if i[1]=='day':
                time['day']=int(time['day'])+int(i[2])
                refine_clock(time)
                time_beg={'year':time['year'],'month':time['month'],'day':time['day'],'hour':'0','minute':'0','second':'0'}
                time_end={'year':time['year'],'month':time['month'],'day':time['day'],'hour':'23','minute':'59','second':'59'}
                action_time={'time_begin':time_beg, 'time_end':time_end}
            elif i[1]=='hour':
                action_time=day_period(time, int(i[2]))     
    return action_time



def adverbs_interpretation(time, adv_list):
    for i in adv_list:
        action_time=timescale_adverb(time,i)
        if action_time!=None:
            time=action_time['time_begin']
    return action_time
    
        




"""
###############   Tests   ###################
"""
def print_time(time):
    print 'year: ', time['year']
    print 'month: ', time['month']
    print 'day: ', time['day']
    print 'hour: ', time['hour']
    print 'minute: ', time['minute']
    print 'second: ', time['second']


time1={'year':'2011','month':'December','day':'1','hour':'22','minute':'0','second':'-60'}
time2={'year':'2011','month':'December','day':'91','hour':'22','minute':'62','second':'3622'}
time3={'year':'2010','month':'December','day':'91','hour':'22','minute':'63','second':'3610'}
time4={'year':'0','month':'January','day':'1','hour':'15','minute':'0','second':'0'}
"""
action_time2=timescale_adverb(time2, 'yesterday')
action_time3=timescale_adverb(time3, 'tomorrow')
"""

#action_time=adverbs_interpretation(time1, ['here', 'now'])
#action_time=adverbs_interpretation(time1, ['here', 'tomorrow'])
action_time=adverbs_interpretation(time4, ['here', 'yesterday'])
#action_time=adverbs_interpretation(time1, ['yesterday', 'tomorrow'])
#action_time=adverbs_interpretation(time1, ['here','yesterday','tonight'])
print_time(action_time['time_begin'])
print_time(action_time['time_end'])

    

"""
 Created by Chouayakh Mahdi                                                       
 23/08/2010                                                                       
 The package contains functions that make operation with time
 Here we will perform the interpretation of some adverbs and indirect complements                                      
 Functions:
    refine_val : to make operation to refine time if it is not correct
    compare : to compare 2 times
    negative_day : to correct value of day if it is negative                                                                       
    refine_clock : to refine time if it is not correct
    day_period : to divide the day into several time
    timescale_i_cmpl : to perform interpretation of an indirect complement
    adverbs_interpretation : to perform interpretation of all adverb list
"""
from dialog.resources_manager import ResourcePool


"""
Statement of lists
"""
day_list = ResourcePool().days_list
month_list = ResourcePool().months_list
adverb = ResourcePool().time_adverbs


def refine_val(x,y,time,value):
    """
    This function make operation to refine time if it is not correct
    Input=2 objects of time, the ratio between these objects and time
    Output=time   
    """
    
    time[y]=str(int(time[y])+int((time[x]))/value)
    time[x]=str(int(time[x])%value)
    return time



def compare(time1, time2):
    """
    This function compare 2 times
    Input=time           Output=1 if these times are different and 0 if not   
    """
    
    if time1['year']!=time2['year'] or time1['month']!=time2['month'] or time1['day']!=time2['day'] or time1['hour']!=time2['hour']:
        return 1
    if time1['minute']!=time2['minute'] or time1['second']!=time2['second']:
        return 1
    return 0



def negative_day(time):
    """
    This function correct value of day if it is negative
    Input=time                                Output=time   
    """
    
    #init
    i=len(month_list)-1
    
    while i >= 0: 
        #If there is negative value of day else we can break the loop
        if int(time['day'])<=0:
            if month_list[i][0]==time['month']:
                
                if i==0:
                    #If it is the first month we have to loop with the last one
                    i=len(month_list)-1
                    #We delete a year
                    time['year']=str(int(time['year'])-1)
                else:
                    i=i-1
                
                if month_list[i][0]=='February' and int(time['year'])%4==0 and int(time['year'])%100!=0:
                    #If it is February and we have 29 days in it
                    time['day']=str(int(time['day'])+29)
                else:
                    time['day']=str(int(time['day'])+int(month_list[i][1]))
                time['month']=month_list[i][0]
            
            else:
                i=i-1
        else:
            return time
    
    

def refine_clock(time):
    """
    This function refine time if it is not correct
    Input=time                                Output=time   
    """
    
    #init
    i=0
    
    time=refine_val('second','minute',time,60)
    time=refine_val('minute','hour',time,60)
    time=refine_val('hour','day',time,24)
    
    #For month we don't have number but literal name => special operation 
    while i < len(month_list):
        if month_list[i][0]==time['month']:
            
            #If the month in February with 29 days
            if time['month']=='February' and int(time['year'])%4==0 and int(time['year'])%100!=0:
                if int(time['day'])<=29:
                    #It is OK we return time
                    return negative_day(time)
                else:
                    time['day']=str(int(time['day'])-29)
                    time['month']=month_list[i+1][0]
            
            else:
                if int(time['day'])<=int(month_list[i][1]):
                    #It is OK we return time
                    return negative_day(time)
                else:
                    time['day']=str(int(time['day'])-int(month_list[i][1]))
                    #If it is the last month, 
                    if i==11:
                        time['month']=month_list[0][0]
                    else:
                        time['month']=month_list[i+1][0]
                        
        #If it is the last month, we have to loop with the first one
        if i==11:
            i=-1
            #We add a year
            time['year']=str(int(time['year'])+1)

        i=i+1
    return negative_day(time)



def day_period(time, period):
    """
    This function divide the day into several time
    Input=time and the reference of the period    
    Output=the action period   
    """
    
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
        time_end={'year':time['year'],'month':time['month'],'day':time['day'],'hour':'22','minute':'59','second':'59'}
        action_time={'time_begin':time_beg, 'time_end':time_end}
    elif period==4:
        time_beg={'year':time['year'],'month':time['month'],'day':time['day'],'hour':'23','minute':'0','second':'0'}
        time_end={'year':time['year'],'month':time['month'],'day':time['day'],'hour':'3','minute':'59','second':'59'}
        action_time={'time_begin':time_beg, 'time_end':time_end}
    elif period==0:
        time_beg={'year':time['year'],'month':time['month'],'day':time['day'],'hour':time['hour'],'minute':time['minute'],'second':time['second']}
        action_time={'time_begin':time_beg, 'time_end':time_beg}
    return action_time



def timescale_adverb(time, adv):
    """
    This function perform interpretation of an adverb
    Input=time and the adverb         Output=the action period   
    """
    
    #init
    action_time=None
    
    for i in adverb:
        if adv==i[0]:
            #If the adverb is about a day (like tomorrow)
            if i[1]=='day':
                time['day']=int(time['day'])+int(i[2])
                refine_clock(time)
                #We have to recover the period
                time_beg={'year':time['year'],'month':time['month'],'day':time['day'],'hour':'0','minute':'0','second':'0'}
                time_end={'year':time['year'],'month':time['month'],'day':time['day'],'hour':'23','minute':'59','second':'59'}
                action_time={'time_begin':time_beg, 'time_end':time_end}
            
            #If the adverb is about a day (like tonight)
            elif i[1]=='hour':
                action_time=day_period(time, int(i[2]))     
    
    #We return the action period although it is none
    return action_time



def adverbs_interpretation(time, adv_list):
    """
    This function perform interpretation of all adverb list
    Input=time and the adverb list         Output=the action period   
    """
    
    for i in adv_list:
        #For each adverb we have more information about the action time
        action_time=timescale_adverb(time,i)
        #To mix information, we have to use the time of begin of action
        if action_time!=None:
            time=action_time['time_begin']
    return action_time
    


def timescale_i_cmpl(indirect_cmpl, action_time):
    """
    This function perform interpretation of an indirect complement
    Input=indirect complement and action time       Output=the action time   
    """
    
    #We know that all prepositions are for future 
    for j in indirect_cmpl:
        #If we have number for determinant
        if j._quantifier=='DIGIT':
            if j.noun==['year'] or j.noun==['month'] or j.noun==['day'] or j.noun==['hour'] or j.noun==['minute'] or j.noun==['second']:
                if action_time['effective_time']==None:
                    action_time['effective_time']=str(int(action_time['action_period']['time_begin'][j.noun[0]])+int(j.det[0]))
                else:
                    action_time['effective_time']=str(int(action_time['effective_time'][j.noun[0]])+int(j.det[0]))
                
            elif j.noun==["o'clock"]:
                if action_time['effective_time']==None:
                    action_time['effective_time']=str(int(action_time['action_period']['time_begin']['hour'])+int(j.det[0]))
                else:
                    action_time['effective_time']=str(int(action_time['effective_time']['hour'])+int(j.det[0]))
                
            elif j.noun==['morning']:
                if action_time['effective_time']==None:
                    action_time['action_period']=day_period(action_time['action_period']['time_begin'], 1)
                else:
                        action_time['action_period']=day_period(action_time['effective_time'], 1)
            elif j.noun==['afternoon']:
                if action_time['effective_time']==None:
                    action_time['action_period']=day_period(action_time['action_period']['time_begin'], 1)
                else:
                    action_time['action_period']=day_period(action_time['effective_time'], 2)
            elif j.noun==['evening']:
                if action_time['effective_time']==None:
                    action_time['action_period']=day_period(action_time['action_period']['time_begin'], 1)
                else:
                    action_time['action_period']=day_period(action_time['effective_time'], 3)      
                    
    return action_time




def indirect_cmpl_interpretation(action_time):
    """
    This function perform interpretation of an indirect complement
    Input=indirect complement and action time       Output=the action time   
    """
    
    return action_time



def timescale_sentence(indirect_cmpl,adv_list,time):
    """
    This function perform interpretation of an indirect complement
    Input=indirect complement and action time       Output=the action time   
    """
    
    action_time={'action_period':adverbs_interpretation(time,adv_list),'effective_time':None}
    if compare(action_time['action_period']['time_begin'],action_time['action_period']['time_begin'])==0:
        action_time['action_period']=None
        action_time['effective_time']=action_time['action_period']['time_begin']
    if action_time['action_period']==None and action_time['effective_time']==None:
        action_time['effective_time']=time
    action_time=indirect_cmpl_interpretation(indirect_cmpl,action_time)
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


time1={'year':'2011','month':'December','day':'1','hour':'22','minute':'0','second':'3622'}
time2={'year':'2011','month':'December','day':'1','hour':'22','minute':'0','second':'3622'}
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
print compare(time1, time2)

    
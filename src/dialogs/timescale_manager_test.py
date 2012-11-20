
"""
 Created by Chouayakh Mahdi                                                       
 26/08/2010                                                                       
 The package contains the unit test of timescale_manager function                                       
    unit_tests : to perform unit tests                                           
"""
import unittest
import logging
from dialogs.sentence import *
import timescale_manager


def print_time(time):
    print time['year']+'/'+time['month']+'/'+time['day']
    print time['hour']+':'+time['minute']+':'+time['second']
    
    
class TestTimescale(unittest.TestCase):
    """
    Function to perform unit tests                                                   
    """ 
    
    def test_01(self):
        print ''
        print ('######################## test 1.1 ##############################')
        print "Object of this test : Without indirect complement and without adverb"
        print ''
        
        d_time={'year':'2010','month':'August','day':'27','hour':'10','minute':'0','second':'0'}
        sentence=Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'future simple', 
                    [Nominal_Group(['a'],['guitar'],[],[],[]),Nominal_Group(['a'],['piano'],[],[],[]),Nominal_Group(['a'],['violon'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "I will play a guitar a piano and a violon."
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print_time(time['action_period']['time_begin'])
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
            
        rslt={'action_period':None,'effective_time':d_time}
    
        self.assertEquals(time,rslt)
        print ''
     
    def test_02(self):
        print ''
        print ('######################## test 1.2 ##############################')
        print "Object of this test : With just an indirect complement but not for time"
        print ''
        
        d_time={'year':'2010','month':'August','day':'27','hour':'10','minute':'0','second':'0'}
        sentence=Sentence('statement', '',
                [Nominal_Group(['the'],['bottle'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [],
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                    [], [] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "the bottle is on the table"
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print_time(time['action_period']['time_begin'])
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':d_time}
    
        self.assertEquals(time,rslt)
        print ''
    
    def test_03(self):
        print ''
        print ('######################## test 1.3 ##############################')
        print "Object of this test : With just an indirect complement but not for time"
        print ''
        
        d_time={'year':'2010','month':'August','day':'27','hour':'10','minute':'0','second':'0'}
        sentence=Sentence('statement', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['prepare'], [],'present progressive', 
                    [Nominal_Group(['the'],['car'],[],[],[]),Nominal_Group(['the'],['moto'],[],[Nominal_Group(['my'],['father'],[],[],[])],[])], 
                    [Indirect_Complement(['at'],[Nominal_Group(['the'],['time'],[['same',[]]],[],[])])],
                    [], [] ,'negative',[])])
        
        print 'The sentence that we will process is : '
        print "you are not preparing the car and the moto of my father at the same time"
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print_time(time['action_period']['time_begin'])
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':d_time}
    
        self.assertEquals(time,rslt)
        print ''
    
    def test_04(self):
        print ''
        print ('######################## test 1.4 ##############################')
        print "Object of this test : With an indirect complement and adverb"
        print ''
        
        d_time={'year':'2010','month':'August','day':'27','hour':'10','minute':'0','second':'0'}
        sentence=Sentence('w_question', 'description', 
                [Nominal_Group(['the'],['weather'],[],[],[])], 
                [Verbal_Group(['like'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['in'],[Nominal_Group(['the'],['winter'],[],[],[])])],
                    [], ['here'] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "what is the weather like here in the winter?"
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print_time(time['action_period']['time_begin'])
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':d_time}
    
        self.assertEquals(time,rslt)
        print ''
    
    def test_05(self):
        print ''
        print ('######################## test 1.5 ##############################')
        print "Object of this test : Adverb 'now' alone is like we have nothing"
        print ''
        
        d_time={'year':'2010','month':'August','day':'27','hour':'10','minute':'0','second':'0'}
        sentence=Sentence('yes_no_question', '', 
                [Nominal_Group([],['he'],[],[],[])], 
                [Verbal_Group(['do'], [],'present progressive', 
                    [Nominal_Group(['his'],['homework'],[],[],[]), Nominal_Group(['his'],['game'],[],[],[])], 
                    [],
                    [], ['now'] ,'negative',[])])
        
        print 'The sentence that we will process is : '
        print "is not he doing his homework and his game now"
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : ' 
            print_time(time['action_period']['time_begin'])
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':d_time}
    
        self.assertEquals(time,rslt)
        print ''
    
    def test_06(self):
        print ''
        print ('######################## test 1.6 ##############################')
        print "Object of this test : Adverb 'today' represent a period of this day"
        print ''
        
        d_time={'year':'2010','month':'August','day':'27','hour':'10','minute':'0','second':'0'}
        sentence=Sentence('w_question', 'situation', 
                [],  
                [Verbal_Group(['must+happen'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['in'],[Nominal_Group(['the'],['company'],[],[],[])])],
                    [], ['today'] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "what must happen in the company today."
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print 'From : ' 
            print_time(time['action_period']['time_begin'])
            print 'To : '
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':None}
        rslt['action_period']={'time_begin':{'year':d_time['year'],'month':d_time['month'],'day':d_time['day'],'hour':'0','minute':'0','second':'0'},
                               'time_end':{'year':d_time['year'],'month':d_time['month'],'day':d_time['day'],'hour':'23','minute':'59','second':'59'}}
    
        self.assertEquals(time,rslt)
        print ''
        
    def test_07(self):
        print ''
        print ('######################## test 1.7 ##############################')
        print "Object of this test : With many indirect complement but not about time"
        print ''
        
        d_time={'year':'2010','month':'August','day':'27','hour':'10','minute':'0','second':'0'}
        sentence=Sentence('statement', '',
                [Nominal_Group(['the'],['bottle'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [],
                    [Indirect_Complement(['next+to'],[Nominal_Group(['the'],['table'],[],[],[])]),
                     Indirect_Complement(['in+front+of'],[Nominal_Group(['the'],['kitchen'],[],[],[])])],
                    [], [] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "the bottle is next to the table and in front of the kitchen"
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print 'From : ' 
            print_time(time['action_period']['time_begin'])
            print 'To : '
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':d_time}
    
        self.assertEquals(time,rslt)
        print ''

    def test_08(self):
        print ''
        print ('######################## test 1.8 ##############################')
        print "Object of this test : Tomorrow"
        print ''
        
        d_time={'year':'2010','month':'August','day':'27','hour':'10','minute':'0','second':'0'}
        sentence=Sentence('w_question', 'thing', 
                [Nominal_Group([],['Jido'],[],[],[])], 
                [Verbal_Group(['do'], [], 'future simple', 
                    [], 
                    [],
                    [], ['tomorrow'] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "what will Jido do tomorrow."
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print 'From : ' 
            print_time(time['action_period']['time_begin'])
            print 'To : '
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':None}
        rslt['action_period']={'time_begin':{'year':d_time['year'],'month':d_time['month'],'day':'28','hour':'0','minute':'0','second':'0'},
                               'time_end':{'year':d_time['year'],'month':d_time['month'],'day':'28','hour':'23','minute':'59','second':'59'}}
    
        self.assertEquals(time,rslt)
        print ''
    
    def test_09(self):
        print ''
        print ('######################## test 1.9 ##############################')
        print "Object of this test : Yesterday"
        print ''
        
        d_time={'year':'2010','month':'August','day':'27','hour':'10','minute':'0','second':'0'}
        sentence=Sentence('statement', '', 
                        [Nominal_Group([],['I'],[],[],[])],  
                        [Verbal_Group(['buy'],[],'past simple', 
                            [Nominal_Group(['the'],['guitar'],[],[],[])], 
                            [],
                            [], ['yesterday'] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "I bought the guitar yesterday."
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print 'From : ' 
            print_time(time['action_period']['time_begin'])
            print 'To : '
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':None}
        rslt['action_period']={'time_begin':{'year':d_time['year'],'month':d_time['month'],'day':'26','hour':'0','minute':'0','second':'0'},
                               'time_end':{'year':d_time['year'],'month':d_time['month'],'day':'26','hour':'23','minute':'59','second':'59'}}
    
        self.assertEquals(time,rslt)
        print ''
     
    def test_10(self):
        print ''
        print ('######################## test 1.10 ##############################')
        print "Object of this test : Tonight"
        print ''
        
        d_time={'year':'2010','month':'August','day':'27','hour':'10','minute':'0','second':'0'}
        sentence=Sentence('w_question', 'long', 
                [Nominal_Group(['the'],['store'],[],[Nominal_Group(['your'],['uncle'],[],[],[])],[])],  
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],[],[['open',[]]],[],[])], 
                    [],
                    [], ['tonight'] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "how long the store of your uncle is open tonight?"
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print 'From : ' 
            print_time(time['action_period']['time_begin'])
            print 'To : '
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':None}
        rslt['action_period']={'time_begin':{'year':d_time['year'],'month':d_time['month'],'day':d_time['day'],'hour':'23','minute':'0','second':'0'},
                               'time_end':{'year':d_time['year'],'month':d_time['month'],'day':'28','hour':'3','minute':'59','second':'59'}}
    
        self.assertEquals(time,rslt)
        print ''
    
    def test_11(self):
        print ''
        print ('######################## test 1.10 ##############################')
        print "Object of this test : using adverb with specific effective time"
        print ''
        
        d_time={'year':'2010','month':'August','day':'30','hour':'10','minute':'0','second':'0'}
        sentence=Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['come+back'], [],'future simple', 
                    [], 
                    [Indirect_Complement(['at'],[Nominal_Group(['7'],["o'clock"],[],[],[])])],
                    [], ['tomorrow'] ,'affirmative',[])])
        sentence.sv[0].i_cmpl[0].gn[0]._quantifier="DIGIT"
        
        print 'The sentence that we will process is : '
        print "I will come back at 7 o'clock tomorrow."
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print 'From : ' 
            print_time(time['action_period']['time_begin'])
            print 'To : '
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':None}
        rslt['action_period']={'time_begin':{'year':d_time['year'],'month':d_time['month'],'day':'31','hour':'0','minute':'0','second':'0'},
                               'time_end':{'year':d_time['year'],'month':d_time['month'],'day':'31','hour':'23','minute':'59','second':'59'}}
        rslt['effective_time']={'year':d_time['year'],'month':d_time['month'],'day':'31','hour':'7','minute':'0','second':'0'}
        
        self.assertEquals(time,rslt)
        print ''
    
    def test_12(self):
        print ''
        print ('######################## test 1.11 ##############################')
        print "Object of this test : DIGIT in indirect complement"
        print ''
        
        d_time={'year':'2010','month':'September','day':'8','hour':'16','minute':'11','second':'0'}
        sentence=Sentence('statement', '', 
                [Nominal_Group([],['he'],[],[],[])], 
                [Verbal_Group(['finish'], [],'present simple', 
                    [Nominal_Group(['the'],['project'],[],[],[])], 
                    [Indirect_Complement(['before'],[Nominal_Group(['10'],['minute'],[],[],[])])],
                    [], [] ,'affirmative',[])])
        sentence.sv[0].i_cmpl[0].gn[0]._quantifier="DIGIT"
        
        print 'The sentence that we will process is : '
        print "He finish the project 10 minutes before."
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print 'From : ' 
            print_time(time['action_period']['time_begin'])
            print 'To : '
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':None}
        rslt['effective_time']={'year':d_time['year'],'month':d_time['month'],'day':d_time['day'],'hour':'16','minute':'1','second':'0'}
        
        self.assertEquals(time,rslt)
        print ''
    
    def test_13(self):
        print ''
        print ('######################## test 1.12 ##############################')
        print "Object of this test : Using pm as a time"
        print ''
        
        d_time={'year':'2010','month':'September','day':'8','hour':'16','minute':'11','second':'0'}
        sentence=Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['come'], [],'future simple', 
                    [], 
                    [Indirect_Complement([],[Nominal_Group(['a'],['evening'],[],[],[])])],
                    [], ['tomorrow'] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "I will come tomorrow evening."
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print 'From : ' 
            print_time(time['action_period']['time_begin'])
            print 'To : '
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':None}
        rslt['action_period']={'time_begin':{'year':d_time['year'],'month':d_time['month'],'day':'9','hour':'18','minute':'0','second':'0'},
                               'time_end':{'year':d_time['year'],'month':d_time['month'],'day':'9','hour':'22','minute':'59','second':'59'}}
    
        self.assertEquals(time,rslt)
        print ''
        
        
    def test_14(self):
        print ''
        print ('######################## test 1.13 ##############################')
        print "Object of this test : Using pm as a time"
        print ''
        
        d_time={'year':'2010','month':'September','day':'8','hour':'16','minute':'11','second':'0'}
        sentence=Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'past simple', 
                    [Nominal_Group(['a'],['guitar'],[],[],[])], 
                    [Indirect_Complement(['ago'],[Nominal_Group(['a'],['year'],[],[],[])])],
                    [], [] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "I played a guitar a year ago."
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print 'From : ' 
            print_time(time['action_period']['time_begin'])
            print 'To : '
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':None}
        rslt['action_period']={'time_begin':{'year':d_time['year'],'month':d_time['month'],'day':'9','hour':'18','minute':'0','second':'0'},
                               'time_end':{'year':d_time['year'],'month':d_time['month'],'day':'9','hour':'22','minute':'59','second':'59'}}
    
        self.assertEquals(time,rslt)
        print ''
    
    def test_15(self):
        print ''
        print ('######################## test 1.14 ##############################')
        print "Object of this test : Using pm as a time"
        print ''
        
        d_time={'year':'2010','month':'September','day':'8','hour':'16','minute':'11','second':'0'}
        sentence=Sentence('statement', '', 
                        [Nominal_Group([],['we'],[],[],[])], 
                        [Verbal_Group(['win'], [],'past simple', 
                            [Nominal_Group(['the'],['award'],[],[],[])], 
                            [Indirect_Complement(['in'],[Nominal_Group(['the'],['year'],[['next',[]]],[],[])])],
                            [], [] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "we won in the next years."
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print 'From : ' 
            print_time(time['action_period']['time_begin'])
            print 'To : '
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':None}
        rslt['action_period']={'time_begin':{'year':d_time['year'],'month':d_time['month'],'day':'9','hour':'18','minute':'0','second':'0'},
                               'time_end':{'year':d_time['year'],'month':d_time['month'],'day':'9','hour':'22','minute':'59','second':'59'}}
    
        self.assertEquals(time,rslt)
        print ''
        
    def test_16(self):
        print ''
        print ('######################## test 1.15 ##############################')
        print "Object of this test : Using pm as a time"
        print ''
        
        d_time={'year':'2010','month':'September','day':'8','hour':'16','minute':'11','second':'0'}
        sentence=Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['come'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['at'],[Nominal_Group(['10'],['pm'],[],[],[])])],
                    [], [] ,'affirmative',[])])
        sentence.sv[0].i_cmpl[0].gn[0]._quantifier="DIGIT"
        
        print 'The sentence that we will process is : '
        print "I come at 10pm."
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print 'From : ' 
            print_time(time['action_period']['time_begin'])
            print 'To : '
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':None}
        rslt['effective_time']={'year':d_time['year'],'month':d_time['month'],'day':d_time['day'],'hour':'22','minute':'0','second':'0'}
        
        self.assertEquals(time,rslt)
        print ''
    
    def test_17(self):
        print ''
        print ('######################## test 1.16 ##############################')
        print "Object of this test : Using pm as a time"
        print ''
        
        d_time={'year':'2010','month':'September','day':'9','hour':'16','minute':'11','second':'0'}
        sentence=Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['come+back'], [],'future simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group([],['Monday'],[],[],[])])],
                    [], [] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "I will come back on monday."
        
        print ''
        print 'The time of speaking sentence is : '
        print_time(d_time)
        
        time=timescale_manager.timescale_sentence(sentence.sv[0].i_cmpl,sentence.sv[0].advrb, d_time)
        if time['action_period']!=None:
            print ''
            print 'The period of the action is : '
            print 'From : ' 
            print_time(time['action_period']['time_begin'])
            print 'To : '
            print_time(time['action_period']['time_end'])
        
        if time['effective_time']!=None:
            print ''
            print 'The effective time of the action is : '
            print_time(time['effective_time'])
        
        rslt={'action_period':None,'effective_time':None}
        rslt['effective_time']={'year':d_time['year'],'month':d_time['month'],'day':d_time['day'],'hour':'22','minute':'0','second':'0'}
        
        self.assertEquals(time,rslt)
        print ''
  
    
def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestTimescale)
    
    return suite

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    
    unittest.TextTestRunner(verbosity=2).run(test_suite())


"""
 Created by Chouayakh Mahdi                                                       
 26/08/2010                                                                       
 The package contains the unit test of timescale_manager function                                       
    unit_tests : to perform unit tests                                           
"""
import unittest
import logging
from dialog.sentence import *
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
        print "I bought the bottle yesterday."
        
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
        print "I bought the bottle yesterday."
        
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
        print "I bought the bottle yesterday."
        
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
        print "I bought the bottle yesterday."
        
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
        print "I bought the bottle yesterday."
        
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
        print "I bought the bottle yesterday."
        
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
        print "I bought the bottle yesterday."
        
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
                [Verbal_Group(['do'], [], 'past simple', 
                    [], 
                    [],
                    [], ['tomorrow'] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "I bought the bottle yesterday."
        
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
        sentence=Sentence('relative', 'that', 
                        [Nominal_Group([],['I'],[],[],[])],  
                        [Verbal_Group(['buy'],[],'past simple', 
                            [Nominal_Group(['the'],['guitar'],[],[],[])], 
                            [],
                            [], ['yesterday'] ,'affirmative',[])])
        
        print 'The sentence that we will process is : '
        print "I bought the bottle yesterday."
        
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
        print "I bought the bottle yesterday."
        
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
                               'time_end':{'year':d_time['year'],'month':d_time['month'],'day':d_time['day'],'hour':'3','minute':'59','second':'59'}}
    
        self.assertEquals(time,rslt)
        print ''
        
    def test_11(self):
        print ''
        print ('######################## test 1.10 ##############################')
        print "Object of this test : Yesterday"
        print ''
        
        d_time={'year':'2010','month':'August','day':'30','hour':'10','minute':'0','second':'0'}
        sentence=Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['come+back'], [],'future simple', 
                    [], 
                    [Indirect_Complement(['at'],[Nominal_Group(['7'],["o'clock"],[],[],[])])],
                    [], ['tomorrow'] ,'affirmative',[])])
        sentence.sv[0].i_cmpl[0].nominal_group[0]._quantifier="DIGIT"
        
        print 'The sentence that we will process is : '
        print "I bought the bottle yesterday."
        
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
 
    
    
    
    """
    def test_75(self):
        print''
        print ('######################## test 8.6 ##############################')
        utterance=" He finish the project 10 minutes before."
        print "Object of this test : To use the complement of the noun and the duplication with 'and'"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[,
            Sentence('statement', '', 
                [Nominal_Group([],['he'],[],[],[])], 
                [Verbal_Group(['finish'], [],'present simple', 
                    [Nominal_Group(['the'],['project'],[],[],[])], 
                    [Indirect_Complement(['before'],[Nominal_Group(['10'],['minute'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        
        rslt[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="DIGIT"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
   
    
    def test_32(self):
        print ''
        print ('######################## test 4.2 ##############################')
        utterance="Which salesperson's competition won the award which we won in the last years"
        print "Object of this test : Using different cases of what question with relative" 
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'choice', 
                [Nominal_Group(['the'],['competition'],[],[Nominal_Group(['the'],['salesperson'],[],[],[])],[])], 
                [Verbal_Group(['win'], [],'past simple', 
                    [Nominal_Group(['the'],['award'],[],[],[Sentence('relative', 'which', 
                        [Nominal_Group([],['we'],[],[],[])], 
                        [Verbal_Group(['win'], [],'past simple', 
                            [Nominal_Group(['the'],['award'],[],[],[])], 
                            [Indirect_Complement(['in'],[Nominal_Group(['the'],['year'],[['last',[]]],[],[])])],
                            [], [] ,'affirmative',[])])])], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sv[0].d_obj[0].relative[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="ALL"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    

    def test_35(self):
        print ''
        print ('######################## test 4.5 ##############################')
        utterance="what is wrong with him? I'll play a guitar or a piano and a violon. I played a guitar a year ago."
        print "Object of this test : Using wrong in the what questions, using the 'or' and moving preposition like 'ago'"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'thing', 
                [Nominal_Group([],[],['wrong'],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['with'],[Nominal_Group([],['him'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'future simple', 
                    [Nominal_Group(['a'],['guitar'],[],[],[]),Nominal_Group(['a'],['piano'],[],[],[]),Nominal_Group(['a'],['violon'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'past simple', 
                    [Nominal_Group(['a'],['guitar'],[],[],[])], 
                    [Indirect_Complement(['ago'],[Nominal_Group(['a'],['year'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
    
        rslt[1].sv[0].d_obj[1]._conjunction="OR"
        rslt[1].sv[0].d_obj[0]._quantifier="SOME"
        rslt[1].sv[0].d_obj[1]._quantifier="SOME"
        rslt[1].sv[0].d_obj[2]._quantifier="SOME"
        rslt[2].sv[0].d_obj[0]._quantifier="SOME"
        rslt[2].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
   
    
    
    def test_48(self):
        print ''
        print ('######################## test 5.8 ##############################')
        utterance="What must be happened in the company today? The building shouldn't be built fastly. You can be here."
        print "Object of this test : Process be+verb+ed"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'situation', 
                [],  
                [Verbal_Group(['must+happen'], [],'present passive', 
                    [], 
                    [Indirect_Complement(['in'],[Nominal_Group(['the'],['company'],[],[],[])])],
                    [], ['today'] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group(['the'],['building'],[],[],[])],  
                [Verbal_Group(['should+build'],[],'passive conditional', 
                    [], 
                    [],
                    ['fastly'], [] ,'negative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['you'],[],[],[])],  
                [Verbal_Group(['can+be'],[],'present simple', 
                    [], 
                    [],
                    [], ['here'] ,'affirmative',[])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    
 
    
    def test_73(self):
        print ''
        print ('######################## test 8.4 ##############################')
        utterance="I will come back on monday. I'll play with guitar. I'll play football"
        print "Object of this test : Using sentences like 'agree' with another sentence (seperatite by comma)"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['come+back'], [],'future simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group([],['Monday'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'future simple', 
                    [], 
                    [Indirect_Complement(['with'],[Nominal_Group(['a'],['guitar'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'future simple', 
                    [Nominal_Group(['a'],['football'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        rslt[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
        rslt[2].sv[0].d_obj[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)                   
    
    
   
   def test_77(self):
        print''
        print ('######################## test 8.8 ##############################')
        utterance="The time of speaking sentence is the best. I come at 10pm. I will come tomorrow evening"
        print "Object of this test : Add test to take off determinant and for timescale"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['the'],['time'],[],[Nominal_Group(['a'],['sentence'],[['speaking',[]]],[],[])],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group(['the'],[],[['best',[]]],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['come'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['at'],[Nominal_Group(['10'],['pm'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['come'], [],'future simple', 
                    [], 
                    [Indirect_Complement([],[Nominal_Group(['a'],['evening'],[],[],[])])],
                    [], ['tomorrow'] ,'affirmative',[])])]
        
        rslt[0].sn[0].noun_cmpl[0]._quantifier='SOME'
        rslt[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="DIGIT"
        rslt[2].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    """
    
    
    
def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestTimescale)
    
    return suite

if __name__ == '__main__':
    
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    
    unittest.TextTestRunner(verbosity=2).run(test_suite())
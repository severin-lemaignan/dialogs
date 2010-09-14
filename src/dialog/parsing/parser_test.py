#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Created by Chouayakh Mahdi 
 06/07/2010  
 The package contains the parser unit tests + functions to perform test
 It is more used for the subject 
 Functions:
    compare_nom_gr : to compare 2 nominal groups
    compare_icompl : to compare 2 indirect complements
    compare_vs : to compare 2 verbal structures
    compare_sentence : to compare 2 sentences
    compare_utterance : to compare 2 replies
    display_ng : to display nominal group
    display : to display class Sentence
"""

import unittest
import logging

from dialog.sentence import *
import preprocessing
import analyse_sentence


def compare_nom_gr(ng,rslt_ng):
    """
    Function to compare 2 nominal groups                                            
    """

    #init
    i=0
    j=0
    
    if len(ng)!=len(rslt_ng):
        return 1
    else:
        while i < len(rslt_ng):
            if rslt_ng[i].det!=ng[i].det or rslt_ng[i].adj!=ng[i].adj or rslt_ng[i].noun!=ng[i].noun:
                return 1
            
            #We compare the noun complement
            if compare_nom_gr(rslt_ng[i].noun_cmpl, ng[i].noun_cmpl)==1:
                return 1
            
            #We compare the relative
            if len(rslt_ng[i].relative)!= len(ng[i].relative):
                return 1
            else:
                while j < len(rslt_ng[i].relative):
                    if compare_sentence(rslt_ng[i].relative[j], ng[i].relative[j])==1:
                        return 1
                    j=j+1
                    
                #reinit
                j=0
            
            #We compare the flag (if there is an 'or' or an 'and')
            if rslt_ng[i]._conjunction!=ng[i]._conjunction:
                return 1
            if rslt_ng[i]._quantifier!=ng[i]._quantifier:
                return 1
            i=i+1
        return 0
    
    
  
def compare_icompl(icompl, rslt_icompl):
    """
    Function to compare 2 indirect complements                                      
    """  

    #init
    i=0

    if len(icompl)!=len(rslt_icompl):
        return 1
    else:
        while i < len(rslt_icompl):
            if rslt_icompl[i].prep!=icompl[i].prep:
                return 1
            if compare_nom_gr(rslt_icompl[i].nominal_group,icompl[i].nominal_group) ==1:
                return 1
            i=i+1
        return 0



def compare_vs(vs, rslt_vs):
    """
    Function to compare 2 verbal structures                                          
    """ 

    #init
    i=0
    j=0

    if len(vs)!=len(rslt_vs):
        return 1
    
    else:
        while i < len(rslt_vs):
            if vs[i].vrb_main!=rslt_vs[i].vrb_main or vs[i].vrb_tense!=rslt_vs[i].vrb_tense or vs[i].state!=rslt_vs[i].state:
                return 1
            if vs[i].advrb!=rslt_vs[i].advrb or vs[i].vrb_adv!=rslt_vs[i].vrb_adv:
                return 1
            
            #We compare the d_obj
            if compare_nom_gr(vs[i].d_obj,rslt_vs[i].d_obj)==1:
                return 1
            
            #We compare the i_cmpl
            if compare_icompl(vs[i].i_cmpl, rslt_vs[i].i_cmpl)==1:
                return 1
            if compare_vs(vs[i].sv_sec, rslt_vs[i].sv_sec)==1:
                return 1
            
            #We compare the vrb_sub_sentence
            if len(rslt_vs[i].vrb_sub_sentence)!= len(vs[i].vrb_sub_sentence):
                return 1
            else:
                while j < len(rslt_vs[i].vrb_sub_sentence):
                    if compare_sentence(vs[i].vrb_sub_sentence[j], rslt_vs[i].vrb_sub_sentence[j])==1:
                        return 1
                    j=j+1
            
            i=i+1
        
        return 0
    
    
   
def compare_sentence(stc, stc_rslt):
    """
    Function to compare 2 sentences                                                  
    """  
    if stc.data_type!=stc_rslt.data_type or stc.aim!=stc_rslt.aim:
        return 1
    if compare_nom_gr(stc.sn,stc_rslt.sn)==1:
        return 1
    if compare_vs(stc.sv, stc_rslt.sv)==1:
        return 1

    return 0



def compare_utterance(utterance, rslt_utterance, sentence_list):
    """
    Function to compare 2 replies                                                    
    """ 

    #init
    i=0

    if len(utterance)!=len(rslt_utterance):
        print 'There is a problem with the analyse utterance : length(utterance)!=length(result)'
    else:
        while i < len(rslt_utterance):
            
            print "The sentence after the analyse utterance is :"
            if i<len (sentence_list):
                print sentence_list[i]
            
            print (str(utterance[i]))
            
            for a in utterance[i].sv:
                for z in a.comparator:
                    print "The comparison in the sentence is : "
                    print z['object']
                    print (str(z['nom_gr'][0]))
            
            flag=compare_sentence(utterance[i], rslt_utterance[i])
            if flag==1:
                print "There is a problem with parsing this sentence"
                print ''
                return 1
            elif flag==0:
                print "############### Parsing is OK ###############"
                print ''
            
            i=i+1
    return 0


class TestParsing(unittest.TestCase):
    """
    Function to perform unit tests                                                   
    """
    
    def test_01(self):
        print''
        print ('######################## test 1.1 ##############################')
        utterance="The bottle is on the table. The bottle is blue. the bottle is Blue"
        print "Object of this test : To use different cases with a state's verb"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '',
                [Nominal_Group(['the'],['bottle'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [],
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '',
                [Nominal_Group(['the'],['bottle'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [Nominal_Group([],[],[['blue',[]]],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '',
                [Nominal_Group(['the'],['bottle'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [Nominal_Group([],['Blue'],[],[],[])],
                    [],
                    [], [] ,'affirmative',[])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
        
    def test_02(self):
        print''
        print ('######################## test 1.2 ##############################')
        utterance="Jido's blue bottle is on the table. I'll play a guitar, a piano and a violon."
        print "Object of this test : To use the complement of the noun and the duplication with 'and'"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['the'],['bottle'],[['blue',[]]],[Nominal_Group([],['Jido'],[],[],[])],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'future simple', 
                    [Nominal_Group(['a'],['guitar'],[],[],[]),Nominal_Group(['a'],['piano'],[],[],[]),Nominal_Group(['a'],['violon'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        rslt[1].sv[0].d_obj[0]._quantifier="SOME"
        rslt[1].sv[0].d_obj[1]._quantifier="SOME"
        rslt[1].sv[0].d_obj[2]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
        
    
    
    def test_03(self):
        print ''
        print ('######################## test 1.3 ##############################')
        utterance="It's on the table. I give it to you. give me the bottle. I don't give the bottle to you."
        print "Object of this test : Present the duality between the direct and indirect complement"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group([],['it'],[],[],[])], 
                    [Indirect_Complement(['to'],[Nominal_Group([],['you'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('imperative', '', 
                [], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['the'],['bottle'],[],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])],
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['the'],['bottle'],[],[],[])], 
                    [Indirect_Complement(['to'],[Nominal_Group([],['you'],[],[],[])])],
                    [], [] ,'negative',[])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_04(self):
        print ''
        print ('######################## test 1.4 ##############################')
        utterance="you aren't preparing the car and my father's moto at the same time. is the bottle of my brother in your right?"
        print "Object of this test : To have more information in sentence and trying the yes or no question"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['prepare'], [],'present progressive', 
                    [Nominal_Group(['the'],['car'],[],[],[]),Nominal_Group(['the'],['moto'],[],[Nominal_Group(['my'],['father'],[],[],[])],[])], 
                    [Indirect_Complement(['at'],[Nominal_Group(['the'],['time'],[['same',[]]],[],[])])],
                    [], [] ,'negative',[])]),
            Sentence('yes_no_question', '', 
                [Nominal_Group(['the'],['bottle'],[],[Nominal_Group(['my'],['brother'],[],[],[])],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['in'],[Nominal_Group(['your'],['right'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
        
    def test_05(self):
        print ''
        print ('######################## test 1.5 ##############################')
        utterance="You shouldn't drive his poorest uncle's wife's big new car. Should I give you the bottle? shall I go"
        print "Object of this test : Using different case of modal"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['should+drive'], [],'present conditional', 
                    [Nominal_Group(['the'],['car'],[['big',[]], ['new',[]]],
                        [Nominal_Group(['the'],['wife'],[],
                            [Nominal_Group(['his'],['uncle'],[['poorest',[]]],[], [])],[])],[])], 
                    [],
                    [], [] ,'negative',[])]),
            Sentence('yes_no_question', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['should+give'], [],'present conditional', 
                    [Nominal_Group(['the'],['bottle'],[],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['you'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('yes_no_question', '', 
                [Nominal_Group([],['I'],[],[],[])],  
                [Verbal_Group(['shall+go'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_06(self):
        print ''
        print ('######################## test 1.6 ##############################')
        utterance="Isn't he doing his homework and his game now? Can't he take this bottle. good afternoon"
        print "Object of this test : Using different case of modal and start dialogue"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('yes_no_question', '', 
                [Nominal_Group([],['he'],[],[],[])], 
                [Verbal_Group(['do'], [],'present progressive', 
                    [Nominal_Group(['his'],['homework'],[],[],[]), Nominal_Group(['his'],['game'],[],[],[])], 
                    [],
                    [], ['now'] ,'negative',[])]),
            Sentence('yes_no_question', '', 
                [Nominal_Group([],['he'],[],[],[])],  
                [Verbal_Group(['can+take'], [],'present simple', 
                    [Nominal_Group(['this'],['bottle'],[],[],[])], 
                    [],
                    [], [] ,'negative',[])]),
            Sentence('start', 'good afternoon.', [], [])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_07(self):
        print ''
        print ('######################## test 1.7 ##############################')
        utterance="Don't quickly give me the blue bottle. I wanna play with my guitar. I'd like to go to the cinema."
        print "Object of this test : Using the second verb of the sentence"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('imperative', '', 
                [], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    ['quickly'], [] ,'negative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['want'], [Verbal_Group(['play'], 
                        [],'', 
                        [], 
                        [Indirect_Complement(['with'],[Nominal_Group(['my'],['guitar'],[],[],[])])],
                        [], [] ,'affirmative',[])], 
                    'present simple',
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])],  
                [Verbal_Group(['like'], [Verbal_Group(['go'], 
                        [],'', 
                        [], 
                        [Indirect_Complement(['to'],[Nominal_Group(['the'],['cinema'],[],[],[])])],
                        [], [] ,'affirmative',[])], 
                    'present conditional',
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    
    def test_08(self):
        print ''
        print ('######################## test 1.8 ##############################')
        utterance="the man, who talks, has a new car. I play the guitar, that I bought yesterday,."
        print "Object of this test : Using relative with subject and object"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        print sentence_list
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['the'],['man'],[],[],[Sentence('relative', 'who', 
                    [],  
                    [Verbal_Group(['talk'],[],'present simple', 
                        [], 
                        [],
                        [], [] ,'affirmative',[])])])],  
                [Verbal_Group(['have'], [],'present simple', 
                    [Nominal_Group(['a'],['car'],[['new',[]]],[],[])],
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])],  
                [Verbal_Group(['play'], [],'present simple', 
                    [Nominal_Group(['the'],['guitar'],[],[],[Sentence('relative', 'that', 
                        [Nominal_Group([],['I'],[],[],[])],  
                        [Verbal_Group(['buy'],[],'past simple', 
                            [Nominal_Group(['the'],['guitar'],[],[],[])], 
                            [],
                            [], ['yesterday'] ,'affirmative',[])])])],
                    [],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sv[0].d_obj[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    
    
    def test_11(self):
        print ''
        print ('######################## test 2.1 ##############################')
        utterance="don't quickly give me the bottle which is on the table, and the glass which I cleaned yesterday, at my left"
        print "Object of this test : Using nested relative with he duplication with 'and'"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('imperative', '', 
                [],  
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'], [],'present simple', 
                            [],
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                            [], [] ,'affirmative',[])])]),
                    Nominal_Group(['the'],['glass'],[],[],[Sentence('relative', 'which', 
                        [Nominal_Group([],['I'],[],[],[])],  
                        [Verbal_Group(['clean'], [],'past simple', 
                            [Nominal_Group(['the'],['glass'],[],[],[])],
                            [],
                            [], ['yesterday'] ,'affirmative',[])])])],
                [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])]), Indirect_Complement(['at'],[Nominal_Group(['my'],['left'],[],[],[])])],
                ['quickly'], [] ,'negative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_12(self):
        print ''
        print ('######################## test 2.2 ##############################')
        utterance="The bottle that I bought from the store which is in the shopping center, , is yours."
        print "Object of this test : Using relative"
        print utterance
        print '#################################################################'
        print ''
        print 
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'that', 
                    [Nominal_Group([],['I'],[],[],[])],  
                    [Verbal_Group(['buy'], [],'past simple', 
                        [Nominal_Group(['the'],['bottle'],[],[],[])], 
                        [Indirect_Complement(['from'],[Nominal_Group(['the'],['store'],[],[],[Sentence('relative', 'which', 
                            [],  
                            [Verbal_Group(['be'], [],'present simple', 
                                [], 
                                [Indirect_Complement(['in'],[Nominal_Group(['the'],['center'],[['shopping',[]]],[],[])])],
                                [], [] ,'affirmative',[])])])])],
                        [], [] ,'affirmative',[])])])],  
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],['yours'],[],[],[])],
                    [],
                    [], [] ,'affirmative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_13(self):
        print ''
        print ('######################## test 2.3 ##############################')
        utterance="When won't the planning session take place? when must you take the bus"
        print "Object of this test : Using different cases of when questions"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'date', 
                [Nominal_Group(['the'],['session'],[['planning',[]]],[],[])], 
                [Verbal_Group(['take+place'], [],'future simple', 
                    [], 
                    [],
                    [], [] ,'negative',[])]),
            Sentence('w_question', 'date', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['must+take'], [],'present simple', 
                    [Nominal_Group(['the'],['bus'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_14(self):
        print ''
        print ('######################## test 2.4 ##############################')
        utterance="Where is Broyen ? where are you going. Where must Jido and you be from?"
        print "Object of this test : Using different cases of where questions"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'place', 
                [Nominal_Group([],['Broyen'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'place', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['go'], [],'present progressive', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'origin', 
                [Nominal_Group([],['Jido'],[],[],[]),Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['must+be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_15(self):
        print ''
        print ('######################## test 2.5 ##############################')
        utterance="What time is the news on TV? What size do you wear? the code is written by me. Mahdi is gonna the Laas?"
        print "Object of this test : Using different cases of what questions and forced yes no question"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'time', 
                [Nominal_Group(['the'],['news'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group([],['TV'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'size', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['wear'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group(['the'],['code'],[],[],[])], 
                [Verbal_Group(['write'], [],'present passive', 
                    [], 
                    [Indirect_Complement(['by'],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('yes_no_question', '', 
                [Nominal_Group([],['Mahdi'],[],[],[])], 
                [Verbal_Group(['go'], [],'present progressive', 
                    [], 
                    [Indirect_Complement(['to'],[Nominal_Group(['the'],['Laas'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_16(self):
        print ''
        print ('######################## test 2.6 ##############################')
        utterance="what is the weather like in the winter here? what were you doing? What isn't Jido going to do tomorrow"
        print "Object of this test : Using different cases of what questions"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'description', 
                [Nominal_Group(['the'],['weather'],[],[],[])], 
                [Verbal_Group(['like'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['in'],[Nominal_Group(['the'],['winter'],[],[],[])])],
                    [], ['here'] ,'affirmative',[])]),
            Sentence('w_question', 'thing', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['do'], [],'past progressive', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'thing', 
                [Nominal_Group([],['Jido'],[],[],[])], 
                [Verbal_Group(['go'], [Verbal_Group(['do'], 
                        [],'', 
                        [], 
                        [],
                        [], ['tomorrow'] ,'affirmative',[])],
                    'present progressive', 
                    [], 
                    [],
                    [], [] ,'negative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_17(self):
        print ''
        print ('######################## test 2.7 ##############################')
        utterance="What's happening. What must happen in the company today? What didn't happen here. no. Sorry."
        print "Object of this test : Using different cases of what questions and disagree"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'situation', 
                [], 
                [Verbal_Group(['happen'], [],'present progressive', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'situation', 
                [],  
                [Verbal_Group(['must+happen'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['in'],[Nominal_Group(['the'],['company'],[],[],[])])],
                    [], ['today'] ,'affirmative',[])]),
            Sentence('w_question', 'situation', 
                [],  
                [Verbal_Group(['happen'], [],'past simple', 
                    [], 
                    [],
                    [], ['here'] ,'negative',[])]),
            Sentence('disagree', 'no.', [], []),
            Sentence('disagree', 'sorry.', [], [])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_18(self):
        print ''
        print ('######################## test 2.8 ##############################')
        utterance="What is the biggest bottle's color on your left. What does your brother do for a living?"
        print "Object of this test : Using different cases of what questions"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'thing', 
                [Nominal_Group(['the'],['color'],[],[Nominal_Group(['the'],['bottle'],[['biggest',[]]],[],[])],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['your'],['left'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'explication', 
                [Nominal_Group(['your'],['brother'],[],[],[])], 
                [Verbal_Group(['do'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['for'],[Nominal_Group(['a'],[],[['living',[]]],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        rslt[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    

    
    def test_21(self):
        print ''
        print ('######################## test 3.1 ##############################')
        utterance="What type of people don't read this magazine? what kind of music must he listen to everyday"
        print "Object of this test : Using different cases of what questions"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'classification+people', 
                [], 
                [Verbal_Group(['read'], [],'present simple', 
                    [Nominal_Group(['this'],['magazine'],[],[],[])], 
                    [],
                    [], [] ,'negative',[])]),
            Sentence('w_question', 'classification+music', 
                [Nominal_Group([],['he'],[],[],[])], 
                [Verbal_Group(['must+listen+to'], [],'present simple', 
                    [], 
                    [Indirect_Complement([],[Nominal_Group([],['everyday'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_22(self):
        print ''
        print ('######################## test 3.2 ##############################')
        utterance="What kind of sport is your favorite? what is the problem with him? what is the matter with this person"
        print "Object of this test : Using different cases of what questions"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'classification+sport', 
                [Nominal_Group(['your'],[],[['favorite',[]]],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'thing', 
                [Nominal_Group(['the'],['problem'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['with'],[Nominal_Group([],['him'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'thing', 
                [Nominal_Group(['the'],['matter'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['with'],[Nominal_Group(['this'],['person'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_23(self):
        print ''
        print ('######################## test 3.3 ##############################')
        utterance="How old are you? how long is your uncle's store opened tonight? how long is your uncle's store open tonight?"
        print "Object of this test : Using different cases of how questions"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'old', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'long', 
                [Nominal_Group(['the'],['store'],[],[Nominal_Group(['your'],['uncle'],[],[],[])],[])], 
                [Verbal_Group(['open'], [],'present passive', 
                    [], 
                    [],
                    [], ['tonight'] ,'affirmative',[])]),
            Sentence('w_question', 'long', 
                [Nominal_Group(['the'],['store'],[],[Nominal_Group(['your'],['uncle'],[],[],[])],[])],  
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],[],[['open',[]]],[],[])], 
                    [],
                    [], ['tonight'] ,'affirmative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_24(self):
        print ''
        print ('######################## test 3.4 ##############################')
        utterance="how far is it from the hotel to the restaurant? how soon can you be here? How often does Jido go skiing?"
        print "Object of this test : Using different cases of how questions"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'far', 
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['from'],[Nominal_Group(['the'],['hotel'],[],[],[])]),
                    Indirect_Complement(['to'],[Nominal_Group(['the'],['restaurant'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'soon', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['can+be'], [],'present simple', 
                    [], 
                    [],
                    [], ['here'] ,'affirmative',[])]),
            Sentence('w_question', 'often', 
                [Nominal_Group([],['Jido'],[],[],[])],  
                [Verbal_Group(['go+skiing'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_25(self):
        print ''
        print ('######################## test 3.5 ##############################')
        utterance="how much water should they transport? how many guests weren't at the party? how much does the motocycle cost"
        print "Object of this test : Using different cases of how questions of quantity"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'quantity', 
                [Nominal_Group([],['they'],[],[],[])], 
                [Verbal_Group(['should+transport'], [],'present conditional', 
                    [Nominal_Group(['a'],['water'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'quantity', 
                [Nominal_Group(['a'],['guests'],[],[],[])], 
                [Verbal_Group(['be'], [],'past simple', 
                    [], 
                    [Indirect_Complement(['at'],[Nominal_Group(['the'],['party'],[],[],[])])],
                    [], [] ,'negative',[])]),
            Sentence('w_question', 'quantity', 
                [Nominal_Group(['the'],['motocycle'],[],[],[])],  
                [Verbal_Group(['cost'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_26(self):
        print ''
        print ('######################## test 3.6 ##############################')
        utterance="How about going to the cinema? how have not they gotten a loan for their business? OK"
        print "Object of this test : Using different cases of how questions and agree"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'invitation', 
                [], 
                [Verbal_Group(['go'], [],'present progressive', 
                    [], 
                    [Indirect_Complement(['to'],[Nominal_Group(['the'],['cinema'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'manner', 
                [Nominal_Group([],['they'],[],[],[])], 
                [Verbal_Group(['get'], [],'present perfect', 
                    [Nominal_Group(['a'],['loan'],[],[],[])], 
                    [Indirect_Complement(['for'],[Nominal_Group(['their'],['business'],[],[],[])])],
                    [], [] ,'negative',[])]),
            Sentence('agree', 'OK.',[],[])]
        
        rslt[1].sv[0].d_obj[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_27(self):
        print ''
        print ('######################## test 3.7 ##############################')
        utterance="How did you like Steven Spilburg's new movie. how could I get to the restaurant from here"
        print "Object of this test : Using different cases of how questions"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'opinion', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['like'], [],'past simple', 
                    [Nominal_Group(['the'],['movie'],[['new',[]]],[Nominal_Group([],['Steven Spilburg'],[],[],[])],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'manner', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['could+get+to'], [],'present conditional', 
                    [Nominal_Group(['the'],['restaurant'],[],[],[])], 
                    [Indirect_Complement(['from'],[Nominal_Group([],['here'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_28(self):
        print ''
        print ('######################## test 3.8 ##############################')
        utterance="Why should she go to Toulouse? who could you talk to on the phone. Whose blue bottle and red glass are these."
        print "Object of this test : Using different cases of why, who and Whose questions"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'reason', 
                [Nominal_Group([],['she'],[],[],[])], 
                [Verbal_Group(['should+go'], [],'present conditional', 
                    [], 
                    [Indirect_Complement(['to'],[Nominal_Group([],['Toulouse'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'people', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['could+talk'], [],'present conditional', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['phone'],[],[],[])]),
                     Indirect_Complement(['to'],[Nominal_Group([],['it'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'owner', 
                [Nominal_Group(['that'],['bottle'],[['blue',[]]],[],[]), Nominal_Group(['that'],['glass'],[['red',[]]],[],[])], 
                [Verbal_Group(['be'], [],'', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
        
    
    def test_31(self):
        print ''
        print ('######################## test 4.1 ##############################')
        utterance="What are you thinking about the idea that I present you? what color is the bottle that you bought,"
        print "Object of this test : Using different cases of what question with relative" 
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'opinion', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['think+about'], [],'present progressive', 
                    [Nominal_Group(['the'],['idea'],[],[],[Sentence('relative', 'that', 
                        [Nominal_Group([],['I'],[],[],[])], 
                        [Verbal_Group(['present'], [],'present simple', 
                            [Nominal_Group(['the'],['idea'],[],[],[])], 
                            [Indirect_Complement([],[Nominal_Group([],['you'],[],[],[])])],
                            [], [] ,'affirmative',[])])])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'color', 
                [Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'that', 
                    [Nominal_Group([],['you'],[],[],[])], 
                    [Verbal_Group(['buy'], [],'past simple', 
                        [Nominal_Group(['the'],['bottle'],[],[],[])], 
                        [],
                        [], [] ,'affirmative',[])])])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]
    
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
    
    def test_33(self):
        print ''
        print ('######################## test 4.3 ##############################')
        utterance="what'll your house look like? what do you think of the latest novel which Jido wrote"
        print "Object of this test : Using different cases of what question with relative"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'description', 
                [Nominal_Group(['your'],['house'],[],[],[])], 
                [Verbal_Group(['look+like'], [],'future simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'opinion', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['think+of'], [],'present simple', 
                    [Nominal_Group(['the'],['novel'],[['latest',[]]],[],[Sentence('relative', 'which', 
                        [Nominal_Group([],['Jido'],[],[],[])], 
                        [Verbal_Group(['write'], [],'past simple', 
                            [Nominal_Group(['the'],['novel'],[['latest',[]]],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])], 
                [],
                [], [] ,'affirmative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_34(self):
        print ''
        print ('######################## test 4.4 ##############################')
        utterance="learn that I want you to give me the blue bottle,. If you do your job, you will be happy."
        print "Object of this test : Using different cases of what question with relative" 
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('imperative', '', 
                [], 
                [Verbal_Group(['learn'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence+statement', 'that', 
                        [Nominal_Group([],['I'],[],[],[])], 
                        [Verbal_Group(['want'], [Verbal_Group(['give'], [],'', 
                                [Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[])], 
                                [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                                [], [] ,'affirmative',[])],'present simple', 
                            [Nominal_Group([],['you'],[],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])]),
            Sentence('statement', '', 
                    [Nominal_Group([],['you'],[],[],[])], 
                    [Verbal_Group(['be'], [],'future simple', 
                        [Nominal_Group([],[],[['happy',[]]],[],[])], 
                        [],
                        [], [] ,'affirmative',[Sentence('subsentence+statement', 'if', 
                            [Nominal_Group([],['you'],[],[],[])], 
                            [Verbal_Group(['do'], [],'present simple', 
                                [Nominal_Group(['your'],['job'],[],[],[])], 
                                [],
                                [], [] ,'affirmative',[])])])])]
    
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
    
    def test_36(self):
        print ''
        print ('######################## test 4.6 ##############################')
        utterance="this is a bottle. There is a bottle on the table"
        print "Object of this test : To use different demonstrative determinant" 
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '',
                [Nominal_Group(['this'],[],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [Nominal_Group(['a'],['bottle'],[],[],[])],
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '',
                [Nominal_Group(['a'],['bottle'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sv[0].d_obj[0]._quantifier="SOME"
        rslt[1].sn[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_37(self):
        print ''
        print ('######################## test 4.7 ##############################')
    
        utterance="What do you do for a living in this building? What does your brother do for a living here"
        print "Object of this test : Correct duality between nominal group with and without noun" 
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'explication', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['do'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['for'],[Nominal_Group(['a'],[],[['living',[]]],[],[])]),
                     Indirect_Complement(['in'],[Nominal_Group(['this'],['building'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'explication', 
                [Nominal_Group(['your'],['brother'],[],[],[])], 
                [Verbal_Group(['do'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['for'],[Nominal_Group(['a'],[],[['living',[]]],[],[])])],
                    [], ['here'] ,'affirmative',[])])]
        
        rslt[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
        rslt[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_38(self):
        print ''
        print ('######################## test 4.8 ##############################')
        utterance="To whom are you talking? you should have the bottle. would you have played a guitar. you would have played a guitar"
        print "Object of this test : Using 'to whom' and passive conditional"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'people', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['talk+to'], [],'present progressive', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['should+have'], [],'present conditional', 
                    [Nominal_Group(['the'],['bottle'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('yes_no_question', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['play'], [],'past conditional', 
                    [Nominal_Group(['a'],['guitar'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['play'], [],'past conditional', 
                    [Nominal_Group(['a'],['guitar'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        rslt[2].sv[0].d_obj[0]._quantifier="SOME"
        rslt[3].sv[0].d_obj[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    

    
    def test_41(self):
        print ''
        print ('######################## test 5.1 ##############################')
        utterance="you'd like the blue bottle or the glass? the green or blue bottle is on the table. the green or the blue glass is mine?"
        print "Object of this test : Process 'OR'"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('yes_no_question', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['like'], [],'present conditional', 
                    [Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[]),Nominal_Group(['the'],['glass'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),       
            Sentence('statement', '', 
                [Nominal_Group(['the'],['bottle'],[['green',[]]],[],[]),Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                    [], [] ,'affirmative',[])]), 
            Sentence('yes_no_question', '', 
                [Nominal_Group(['the'],['glass'],[['green',[]]],[],[]),Nominal_Group(['the'],['glass'],[['blue',[]]],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],['mine'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sv[0].d_obj[1]._conjunction="OR"
        rslt[1].sn[1]._conjunction="OR"
        rslt[2].sn[1]._conjunction="OR"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_42(self):
        print ''
        print ('######################## test 5.2 ##############################')
    
        utterance="learn that I want you to give me the blue bottle that is blue."
        print "Object of this test : Duality between 'that' derminant and 'that' of adverbial"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('imperative', '', 
                [], 
                [Verbal_Group(['learn'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence+statement', 'that', 
                        [Nominal_Group([],['I'],[],[],[])], 
                        [Verbal_Group(['want'], [Verbal_Group(['give'], [],'', 
                                [Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[Sentence('relative', 'that', 
                                    [], 
                                    [Verbal_Group(['be'], [],'present simple', 
                                        [Nominal_Group([],[],[['blue',[]]],[],[])], 
                                        [],
                                        [], [] ,'affirmative',[])])])], 
                                [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                                [], [] ,'affirmative',[])],'present simple', 
                            [Nominal_Group([],['you'],[],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
        
    def test_43(self):
        print ''
        print ('######################## test 5.3 ##############################')
        utterance="The bottle is behind to me. The bottle is next to the table in front of the kitchen."
        print "Object of this test : Using preposition with more than one word"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '',
                [Nominal_Group(['the'],['bottle'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [],
                    [Indirect_Complement(['behind+to'],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '',
                [Nominal_Group(['the'],['bottle'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [],
                    [Indirect_Complement(['next+to'],[Nominal_Group(['the'],['table'],[],[],[])]),
                     Indirect_Complement(['at'],[Nominal_Group(['the'],['front'],[],[Nominal_Group(['the'],['kitchen'],[],[],[])],[])])],
                    [], [] ,'affirmative',[])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_44(self):
        print ''
        print ('######################## test 5.4 ##############################')
        utterance="Take the bottle carefully. I take that bottle that I drink in. I take twenty two bottles."
        print "Object of this test : Find adverb after verb, duplicate information in relative and include numbers"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('imperative', '', 
                [], 
                [Verbal_Group(['take'], [],'present simple', 
                    [Nominal_Group(['the'],['bottle'],[],[],[])], 
                    [],
                    ['carefully'], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])],  
                [Verbal_Group(['take'], [],'present simple', 
                    [Nominal_Group(['that'],['bottle'],[],[],[Sentence('relative', 'that', 
                        [Nominal_Group([],['I'],[],[],[])],  
                        [Verbal_Group(['drink'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['in'],[Nominal_Group(['that'],['bottle'],[],[],[])])],
                            [], [] ,'affirmative',[])])])],
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])],  
                [Verbal_Group(['take'], [],'present simple', 
                    [Nominal_Group(['22'],['bottle'],[],[],[])],
                    [],
                    [], [] ,'affirmative',[])])]
        
        rslt[2].sv[0].d_obj[0]._quantifier="DIGIT"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_45(self):
        print ''
        print ('######################## test 5.5 ##############################')
        utterance="I'll play Jido's guitar, a saxophone, a piano of the wife of my oncle and Patrick's violon."
        print "Object of this test : Process with many 'of' and 'and'"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'future simple', 
                    [Nominal_Group(['the'],['guitar'],[],[Nominal_Group([],['Jido'],[],[],[])],[]),
                     Nominal_Group(['a'],['saxophone'],[],[],[]),
                     Nominal_Group(['a'],['piano'],[],[Nominal_Group(['the'],['wife'],[],[Nominal_Group(['my'],['oncle'],[],[],[])],[])],[]),
                     Nominal_Group(['the'],['violon'],[],[Nominal_Group([],['Patrick'],[],[],[])],[])], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sv[0].d_obj[1]._quantifier="SOME"
        rslt[0].sv[0].d_obj[2]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
        
    def test_46(self):
        print ''
        print ('######################## test 5.6 ##############################')
        utterance="Give me two or three bottles. the bottle is blue, big and fanny. give me the bottle on the table"
        print "Object of this test : Using numbers, many adjectives and transform indirect complement into relative"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('imperative', '', 
                [], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['2'],['bottle'],[],[],[]),
                     Nominal_Group(['3'],['bottle'],[],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group(['the'],['bottle'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],[],[['blue',[]], ['big',[]], ['fanny',[]]],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('imperative', '', 
                [], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                            [], [] ,'affirmative',[])])])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sv[0].d_obj[1]._conjunction="OR"
        rslt[0].sv[0].d_obj[0]._quantifier="DIGIT"
        rslt[0].sv[0].d_obj[1]._quantifier="DIGIT"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
        
    def test_47(self):
        print ''
        print ('######################## test 5.7 ##############################')
        utterance="the boys' ball is blue. He ask me to do something. is any person courageous on the laboratory"
        print "Object of this test : 'of' in plural and using more determinant"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['the'],['ball'],[],[Nominal_Group(['the'],['boy'],[],[],[])],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],[],[['blue',[]]],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['he'],[],[],[])], 
                [Verbal_Group(['ask'], [Verbal_Group(['do'], [],'', 
                    [Nominal_Group([],['something'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])],'present simple', 
                [Nominal_Group([],['me'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])]),
            Sentence('yes_no_question', '', 
                [Nominal_Group(['any'],['person'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],[],[['courageous',[]]],[],[])], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['laboratory'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sn[0].noun_cmpl[0]._quantifier="ALL"
        rslt[2].sn[0]._quantifier="ANY"
        
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
    
    
    
    def test_51(self):
        print ''
        print ('######################## test 6.1 ##############################')
        utterance="what size is the best one? What object is blue? How good is this"
        print "Object of this test : Generalize the w question"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('w_question', 'size', 
                [Nominal_Group(['the'],['one'],[['best',[]]],[],[])],  
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'object', 
                [],  
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],[],[['blue',[]]],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'good', 
                [Nominal_Group(['this'],[],[],[],[])],  
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_52(self):
        print ''
        print ('######################## test 6.2 ##############################')
        utterance="He Patrick, the bottle is on the table. give it to me"
        print "Object of this test : Using interjection in different cases"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('interjection', '', 
                [Nominal_Group([],['Patrick'],[],[],[])],  
                []),
            Sentence('statement', '', 
                [Nominal_Group(['the'],['bottle'],[],[],[])],  
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('imperative', '', 
                [Nominal_Group([],['Patrick'],[],[],[])],  
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group([],['it'],[],[],[])], 
                    [Indirect_Complement(['to'],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_53(self):
        print ''
        print ('######################## test 6.3 ##############################')
        utterance="Jido, give me the bottle. Jido, Patrick and you will go to the cinema. Jido, Patrick and you, give me the bottle"
        print "Object of this test : Using interjection in different cases"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('interjection', '', 
                [Nominal_Group([],['Jido'],[],[],[])],  
                [Verbal_Group([], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('imperative', '', 
                [Nominal_Group([],['Jido'],[],[],[])],  
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['the'],['bottle'],[],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['Jido'],[],[],[]),Nominal_Group([],['Patrick'],[],[],[]),Nominal_Group([],['you'],[],[],[])],  
                [Verbal_Group(['go'], [],'future simple', 
                    [], 
                    [Indirect_Complement(['to'],[Nominal_Group(['the'],['cinema'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('interjection', '', 
                [Nominal_Group([],['Jido'],[],[],[]),Nominal_Group([],['Patrick'],[],[],[]),Nominal_Group([],['you'],[],[],[])],  
                [Verbal_Group([], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('imperative', '', 
                [Nominal_Group([],['Jido'],[],[],[]),Nominal_Group([],['Patrick'],[],[],[]),Nominal_Group([],['you'],[],[],[])],  
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['the'],['bottle'],[],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
    
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_54(self):
        print ''
        print ('######################## test 6.4 ##############################')
    
        utterance="The bottle is not blue but it is red. It is not the glass but the bottle. it is blue or red"
        print "Object of this test : Process 'BUT' as conjunction and adverbial"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['the'],['bottle'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],[],[['blue',[]]],[],[])], 
                    [],
                    [], [] ,'negative',[Sentence('subsentence+statement', 'but', 
                        [Nominal_Group([],['it'],[],[],[])], 
                        [Verbal_Group(['be'], [],'present simple', 
                            [Nominal_Group([],[],[['red',[]]],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])]),
            Sentence('statement', '', 
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group(['the'],['glass'],[],[],[]),Nominal_Group(['the'],['bottle'],[],[],[])], 
                    [],
                    [], [] ,'negative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],[],[['blue',[]]],[],[]),Nominal_Group([],[],[['red',[]]],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        rslt[1].sv[0].d_obj[1]._conjunction="BUT"
        rslt[2].sv[0].d_obj[1]._conjunction="OR"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_55(self):
        print ''
        print ('######################## test 6.5 ##############################')
    
        utterance="It is not red but blue. this is my banana. bananas are fruits."
        print "Object of this test : Process plural"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],[],[['red',[]]],[],[]),Nominal_Group([],[],[['blue',[]]],[],[])], 
                    [],
                    [], [] ,'negative',[])]),
            Sentence('statement', '', 
                [Nominal_Group(['this'],[],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group(['my'],['banana'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['banana'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],['fruit'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sv[0].d_obj[1]._conjunction="BUT"
        rslt[2].sn[0]._quantifier="ALL"
        rslt[2].sv[0].d_obj[0]._quantifier="ALL"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_56(self):
        print ''
        print ('######################## test 6.6 ##############################')
        utterance="there are no bananas. All bananas are here. give me more information about the bottle."
        print "Object of this test : More determinants and transformation of the indirect complement" 
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['no'],['banana'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group(['all'],['banana'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], ['here'] ,'affirmative',[])]),
            Sentence('imperative', '', 
                [], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['more'],['information'],[],[],[Sentence('relative', 'which', 
                        [], 
                        [Verbal_Group(['be'], [],'present simple', 
                            [], 
                            [Indirect_Complement(['about'],[Nominal_Group(['the'],['bottle'],[],[],[])])],
                            [], [] ,'affirmative',[])])])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sn[0]._quantifier="SOME"
        rslt[0].sn[0]._quantifier="ANY"
        rslt[1].sn[0]._quantifier="ALL"
        rslt[2].sv[0].d_obj[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_57(self):
        print ''
        print ('######################## test 6.7 ##############################')
        utterance="Jido, tell me where you go. Goodbye. Bye. there is nothing. it is another one."
        print "Object of this test : More determinants and ending the dialog" 
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('interjection', '', 
                [Nominal_Group([],['Jido'],[],[],[])],  
                [Verbal_Group([], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('imperative', '', 
                [Nominal_Group([],['Jido'],[],[],[])], 
                [Verbal_Group(['tell'], [],'present simple', 
                    [], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])]),
                     Indirect_Complement([],[Nominal_Group(['the'],['location'],[],[],[Sentence('relative', 'where', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['go'], [],'present simple', 
                            [], 
                            [],
                            [], [] ,'affirmative',[])])])])],
                    [], [] ,'affirmative',[])]),
            Sentence('end', '', [], []),
            Sentence('end', '', [], []),
            Sentence('statement', '', 
                [Nominal_Group([],['nothing'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group(['another'],['one'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        rslt[4].sn[0]._quantifier="NONE"
        rslt[5].sv[0].d_obj[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_58(self):
        print ''
        print ('######################## test 6.8 ##############################')
        utterance="The bottle becomes blue. One piece could become two, if you smoldered it."
        print "Object of this test : More state verb and numbers" 
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['the'],['bottle'],[],[],[])], 
                [Verbal_Group(['become'], [],'present simple', 
                    [Nominal_Group([],[],[['blue',[]]],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group(['1'],['piece'],[],[],[])], 
                [Verbal_Group(['could+become'], [],'present conditional', 
                    [Nominal_Group(['2'],[],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence+statement', 'if', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['smolder'], [],'past simple', 
                            [Nominal_Group([],['it'],[],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])])]
        
        rslt[1].sn[0]._quantifier="DIGIT"
        rslt[1].sv[0].d_obj[0]._quantifier="DIGIT"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)

    
    
    def test_61(self):
        print ''
        print ('######################## test 7.1 ##############################')
        utterance="This one is not the bottle of my uncle but it is the bottle of my brother. It is not on the table but on the shelf."
        print "Object of this test : Using 'but' with indirect complement"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['this'],['one'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group(['the'],['bottle'],[],[Nominal_Group(['my'],['uncle'],[],[],[])],[])], 
                    [],
                    [], [] ,'negative',[Sentence('subsentence+statement', 'but', 
                        [Nominal_Group([],['it'],[],[],[])], 
                        [Verbal_Group(['be'], [],'present simple', 
                            [Nominal_Group(['the'],['bottle'],[],[Nominal_Group(['my'],['brother'],[],[],[])],[])], 
                            [],
                            [], [] ,'affirmative',[])])])]),
            Sentence('statement', '', 
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[]),Nominal_Group(['the'],['shelf'],[],[],[])])],
                    [], [] ,'negative',[])])]
        
        rslt[1].sv[0].i_cmpl[0].nominal_group[1]._conjunction="BUT"
      
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_62(self):
        print ''
        print ('######################## test 7.2 ##############################')
        utterance="Give me the fourth and seventh bottle. Give me the one thousand ninth and the thirty thousand twenty eighth bottle."
        print "Object of this test : Porcess adjective numbers"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('imperative', '', 
                [], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['the'],['bottle'],[['4th',[]]],[],[]),
                     Nominal_Group(['the'],['bottle'],[['7th',[]]],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('imperative', '', 
                [], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['the'],['bottle'],[['1009th',[]]],[],[]),
                     Nominal_Group(['the'],['bottle'],[['30028th',[]]],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
      
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_63(self):
        print ''
        print ('######################## test 7.3 ##############################')
        utterance="the evil tyrant is in the laboratory. I don't know what are you talking about."
        print "Object of this test : Adjectives can't be noun and complete indirect coomplement" 
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['the'],['tyrant'],[['evil',[]]],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['in'],[Nominal_Group(['the'],['laboratory'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['know'], [],'present simple', 
                    [Nominal_Group(['the'],['thing'],[],[],[Sentence('relative', 'that', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['talk'], [],'present progressive', 
                            [Nominal_Group(['the'],['thing'],[],[],[])], 
                            [Indirect_Complement(['about'],[Nominal_Group([],['it'],[],[],[])])],
                            [], [] ,'affirmative',[])])])], 
                    [],
                    [], [] ,'negative',[])])]
      
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)     
    
    
    def test_64(self):
        print ''
        print ('######################## test 7.4 ##############################')
        utterance="I go to the place where I was born. I study where you studied. I study where you build your house where you put the bottle."
        print "Object of this test : Duality between relative and adverbial" 
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['go'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['to'],[Nominal_Group(['the'],['place'],[],[],[Sentence('relative', 'where', 
                        [Nominal_Group([],['I'],[],[],[])], 
                        [Verbal_Group(['be'], [],'past simple', 
                            [Nominal_Group([],[],[['born',[]]],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['study'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['in'],[Nominal_Group(['the'],['location'],[],[],[Sentence('relative', 'where', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['study'], [],'past simple', 
                            [], 
                            [],
                            [], [] ,'affirmative',[])])])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['study'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['in'],[Nominal_Group(['the'],['location'],[],[],[Sentence('relative', 'where', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['build'], [],'present simple', 
                            [Nominal_Group(['your'],['house'],[],[],[Sentence('relative', 'where', 
                                [Nominal_Group([],['you'],[],[],[])], 
                                [Verbal_Group(['put'], [],'present simple', 
                                    [Nominal_Group(['the'],['bottle'],[],[],[])], 
                                    [],
                                    [], [] ,'affirmative',[])])])], 
                            [],
                            [], [] ,'affirmative',[])])])])],
                    [], [] ,'affirmative',[])])]
      
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
        
    def test_65(self):
        print ''
        print ('######################## test 7.5 ##############################')
        utterance="apples grow on trees and plants. give me three apples."
        print "Object of this test : Plural with duplication"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['apple'],[],[],[])], 
                [Verbal_Group(['grow'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group([],['tree'],[],[],[]),Nominal_Group([],['plant'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('imperative', '', 
                [], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['3'],['apple'],[],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sn[0]._quantifier="ALL"
        rslt[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="ALL"
        rslt[0].sv[0].i_cmpl[0].nominal_group[1]._quantifier="ALL"
        rslt[1].sv[0].d_obj[0]._quantifier="DIGIT"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)

    def test_66(self):
        print ''
        print ('######################## test 7.6 ##############################')
        utterance="When your father came, we was preparing the dinner. While I phoned, he made a sandwich with bacons."
        print "Object of this test : Process adverbial at the beginning of the sentence"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['we'],[],[],[])], 
                [Verbal_Group(['prepare'], [],'past progressive', 
                    [Nominal_Group(['the'],['dinner'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence+statement', 'when', 
                        [Nominal_Group(['your'],['father'],[],[],[])], 
                        [Verbal_Group(['come'], [],'past simple', 
                             [], 
                             [],
                             [], [] ,'affirmative',[])])])]),
            Sentence('statement', '', 
                [Nominal_Group([],['he'],[],[],[])], 
                [Verbal_Group(['make'], [],'past simple', 
                    [Nominal_Group(['a'],['sandwich'],[],[],[Sentence('relative', 'which', 
                        [], 
                        [Verbal_Group(['be'], [],'present simple', 
                            [], 
                            [Indirect_Complement(['with'],[Nominal_Group([],['bacon'],[],[],[])])],
                            [], [] ,'affirmative',[])])])], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence+statement', 'while', 
                        [Nominal_Group([],['I'],[],[],[])], 
                        [Verbal_Group(['phone'], [],'past simple', 
                             [], 
                             [],
                             [], [] ,'affirmative',[])])])])]
        
        rslt[1].sv[0].d_obj[0]._quantifier="SOME"
        rslt[1].sv[0].d_obj[0].relative[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="ALL"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_67(self):
        print ''
        print ('######################## test 7.7 ##############################')
        utterance="the big and very strong man is on the corner. the too big and very strong man is on the corner."
        print "Object of this test : Add contifier for adjectives"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['the'],['man'],[['big',[]],['strong',['very']]],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['corner'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group(['the'],['man'],[['big',['too']],['strong',['very']]],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['corner'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)

    def test_68(self):
        print ''
        print ('######################## test 7.8 ##############################')
        utterance="red apples grow on green trees and plants. a kind of thing. It can be played by thirty thousand twenty eight players."
        print "Object of this test : Using adjectives wuth plural"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['apple'],[['red',[]]],[],[])], 
                [Verbal_Group(['grow'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group([],['tree'],[['green',[]]],[],[]),Nominal_Group([],['plant'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                    [Nominal_Group(['a'],['kind'],[],[Nominal_Group(['a'],['thing'],[],[],[])],[])], 
                    [Verbal_Group([], [],'present simple', 
                        [], 
                        [],
                        [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                        [Nominal_Group([],['it'],[],[],[])],  
                        [Verbal_Group(['can+play'],[],'present passive', 
                            [], 
                            [Indirect_Complement(['by'],[Nominal_Group(['30028'],['player'],[],[],[])])],
                            [], [] ,'affirmative',[])])]
        
        rslt[0].sn[0]._quantifier="ALL"
        rslt[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="ALL"
        rslt[0].sv[0].i_cmpl[0].nominal_group[1]._quantifier="ALL"
        rslt[1].sn[0]._quantifier="SOME"
        rslt[1].sn[0].noun_cmpl[0]._quantifier="SOME"
        rslt[2].sv[0].i_cmpl[0].nominal_group[0]._quantifier="DIGIT"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    
    
    def test_70(self):
        print ''
        print ('######################## test 8.1 ##############################')
        utterance="let the man go to the cinema. Is it the time to let you go. And where is the other tape."
        print "Object of this test : Porcess verb with many second verbs"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('imperative', '', 
                [], 
                [Verbal_Group(['let'], [Verbal_Group(['go'], 
                        [],'', 
                        [], 
                        [Indirect_Complement(['to'],[Nominal_Group(['the'],['cinema'],[],[],[])])],
                        [], [] ,'affirmative',[])],'present simple', 
                    [Nominal_Group(['the'],['man'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('yes_no_question', '', 
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [Verbal_Group(['let'], 
                        [Verbal_Group(['go'], 
                            [],'', 
                            [], 
                            [],
                            [], [] ,'affirmative',[])],'', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [],
                        [], [] ,'affirmative',[])],'present simple', 
                    [Nominal_Group(['the'],['time'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'place', 
                [Nominal_Group(['the'],['tape'],[['other',[]]],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_71(self):
        print ''
        print ('######################## test 8.2 ##############################')
        utterance="And now, can you reach the tape. it could have been them. It is just me at the door. A strong clause can stand on its own"
        print "Object of this test : Process with 'and' in the beginning and more examples"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('yes_no_question', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['can+reach'], [],'present simple', 
                    [Nominal_Group(['the'],['tape'],[],[],[])], 
                    [],
                    [], ['now'] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['could+be'], [],'passive conditional', 
                    [Nominal_Group([],['them'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],['me'],[],[],[])], 
                    [Indirect_Complement(['at'],[Nominal_Group(['the'],['door'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group(['a'],['clause'],[['strong',[]]],[],[])], 
                [Verbal_Group(['can+stand'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['its'],['own'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        rslt[3].sn[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)    
    
    def test_72(self):
        print ''
        print ('######################## test 8.3 ##############################')
        utterance="tell me what to do. No, I can not reach it."
        print "Object of this test : Using sentences like 'agree' with another sentence (seperatite by comma)"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('imperative', '', 
                [], 
                [Verbal_Group(['tell'], [],'present simple', 
                    [], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])]),
                     Indirect_Complement([],[Nominal_Group(['the'],['thing'],[],[],[Sentence('relative', 'that', 
                        [], 
                        [Verbal_Group(['be'], [Verbal_Group(['do'], [],'', 
                                [], 
                                [],
                                [], [] ,'affirmative',[])],'present simple', 
                            [], 
                            [],
                            [], [] ,'affirmative',[])])])])],
                    [], [] ,'affirmative',[])]),
            Sentence('disagree', 'no.',[],[]), 
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['can+reach'], [],'present simple', 
                    [Nominal_Group([],['it'],[],[],[])], 
                    [],
                    [], [] ,'negative',[])])]
        
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
    
    def test_74(self):
        print''
        print ('######################## test 8.5 ##############################')
        utterance="I'll play guitar, piano and violon. I'll play with guitar, piano and violon. give me everything"
        print "Object of this test : To take off determinant"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'future simple', 
                    [Nominal_Group(['a'],['guitar'],[],[],[]),Nominal_Group(['a'],['piano'],[],[],[]),Nominal_Group(['a'],['violon'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'future simple', 
                    [], 
                    [Indirect_Complement(['with'],[Nominal_Group(['a'],['guitar'],[],[],[]),
                                                   Nominal_Group(['a'],['piano'],[],[],[]),
                                                   Nominal_Group(['a'],['violon'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('imperative', '', 
                [], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group([],['everything'],[],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sv[0].d_obj[0]._quantifier="SOME"
        rslt[0].sv[0].d_obj[1]._quantifier="SOME"
        rslt[0].sv[0].d_obj[2]._quantifier="SOME"
        rslt[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
        rslt[1].sv[0].i_cmpl[0].nominal_group[1]._quantifier="SOME"
        rslt[1].sv[0].i_cmpl[0].nominal_group[2]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_75(self):
        print''
        print ('######################## test 8.6 ##############################')
        utterance="I will come back at seven o'clock tomorrow. He finish the project 10 minutes before."
        print "Object of this test : Process some time with digit"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['come+back'], [],'future simple', 
                    [], 
                    [Indirect_Complement(['at'],[Nominal_Group(['7'],["o'clock"],[],[],[])])],
                    [], ['tomorrow'] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['he'],[],[],[])], 
                [Verbal_Group(['finish'], [],'present simple', 
                    [Nominal_Group(['the'],['project'],[],[],[])], 
                    [Indirect_Complement(['before'],[Nominal_Group(['10'],['minute'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="DIGIT"
        rslt[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="DIGIT"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_76(self):
        print''
        print ('######################## test 8.7 ##############################')
        utterance="I'll play a guitar a piano and a violon. I'll play with a guitar a piano and a violon. the boss you and me are here"
        print "Object of this test : To take off comma between the nominal groups"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'future simple', 
                    [Nominal_Group(['a'],['guitar'],[],[],[]),Nominal_Group(['a'],['piano'],[],[],[]),Nominal_Group(['a'],['violon'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'future simple', 
                    [], 
                    [Indirect_Complement(['with'],[Nominal_Group(['a'],['guitar'],[],[],[]),
                                                   Nominal_Group(['a'],['piano'],[],[],[]),
                                                   Nominal_Group(['a'],['violon'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group(['the'],['boss'],[],[],[]),Nominal_Group([],['you'],[],[],[]),Nominal_Group([],['me'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], ['here'] ,'affirmative',[])])]
        
        rslt[0].sv[0].d_obj[0]._quantifier="SOME"
        rslt[0].sv[0].d_obj[1]._quantifier="SOME"
        rslt[0].sv[0].d_obj[2]._quantifier="SOME"
        rslt[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
        rslt[1].sv[0].i_cmpl[0].nominal_group[1]._quantifier="SOME"
        rslt[1].sv[0].i_cmpl[0].nominal_group[2]._quantifier="SOME"
        
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
    
        
    
    def test_81(self):
        print''
        print ('######################## test 9.1 ##############################')
        utterance="I think that I know who is he. see you. So I want to go"
        print "Object of this test : Process relative without object, so we duplicate the nominal group"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
        
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['think'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence+statement', 'that', 
                        [Nominal_Group([],['I'],[],[],[])], 
                        [Verbal_Group(['know'], [],'present simple', 
                            [Nominal_Group([],['he'],[],[],[Sentence('relative', 'who', 
                                [], 
                                [Verbal_Group(['be'], [],'present simple', 
                                    [Nominal_Group([],['he'],[],[],[])], 
                                    [],
                                    [], [] ,'affirmative',[])])])], 
                            [],
                            [], [] ,'affirmative',[])])])]),
            Sentence('end', '', [], []),
            Sentence('', '', [], 
                [Verbal_Group([], [],'', [], [],[], [] ,'affirmative',
                    [Sentence('subsentence+statement', 'so', 
                        [Nominal_Group([],['I'],[],[],[])], 
                        [Verbal_Group(['want'], [Verbal_Group(['go'], [],'', 
                                [], 
                                [],
                                [], [] ,'affirmative',[])],'present simple', 
                            [], 
                            [],
                            [], [] ,'affirmative',[])])])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_82(self):
        print''
        print ('######################## test 9.2 ##############################')
        utterance="the interpretation is to find a defenition or a rule for something. and in a dialog, there is an interaction between them"
        print "Object of this test : Put indirect complement or second verb before the sentence"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['the'],['interpretation'],[],[],[])], 
                [Verbal_Group(['be'], [Verbal_Group(['find'], [],'', 
                        [Nominal_Group(['a'],['defenition'],[],[],[]),
                         Nominal_Group(['a'],['rule'],[],[],[])], 
                        [Indirect_Complement(['for'],[Nominal_Group([],['something'],[],[],[])])],
                        [], [] ,'affirmative',[])],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group(['an'],['interaction'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['between'],[Nominal_Group([],['them'],[],[],[])]),
                     Indirect_Complement(['in'],[Nominal_Group(['a'],['dialog'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sv[0].sv_sec[0].d_obj[0]._quantifier="SOME"
        rslt[0].sv[0].sv_sec[0].d_obj[1]._quantifier="SOME"
        rslt[0].sv[0].sv_sec[0].d_obj[1]._conjunction="OR"
        rslt[1].sn[0]._quantifier="SOME"
        rslt[1].sv[0].i_cmpl[1].nominal_group[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_83(self):
        print''
        print ('######################## test 9.3 ##############################')
        utterance="To have a dialog, we need more than 1 protagonist. I finish the dialog, and I check many problems"
        print "Object of this test : Having indirect complement before the sentence and to have more one sentence in utterance"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['we'],[],[],[])], 
                [Verbal_Group(['need'], [Verbal_Group(['have'], [],'', 
                        [Nominal_Group(['a'],['dialog'],[],[],[])], 
                        [],
                        [], [] ,'affirmative',[])],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['finish'], [],'present simple', 
                    [Nominal_Group(['the'],['dialog'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['check'], [],'present simple', 
                    [Nominal_Group([],['problem'],[['many',[]]],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sv[0].sv_sec[0].d_obj[0]._quantifier="SOME"
        rslt[2].sv[0].d_obj[0]._quantifier="ALL"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)

    def test_84(self):
        print''
        print ('######################## test 9.4 ##############################')
        utterance="the left of what? Jido, what do you do? throw one of them. Very good"
        print "Object of this test : Question at the end of sentence"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['the'],['left'],[],[Nominal_Group(['a'],['what'],[],[],[])],[])], 
                [Verbal_Group([], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('interjection', '', 
                [Nominal_Group([],['Jido'],[],[],[])],  
                [Verbal_Group([], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'thing', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['do'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('imperative', '', 
                [Nominal_Group([],['Jido'],[],[],[])], 
                [Verbal_Group(['throw'], [],'present simple', 
                    [Nominal_Group(['1'],[],[],[Nominal_Group([],['them'],[],[],[])],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('agree', 'good.', [], [])]
        
        rslt[0].sn[0].noun_cmpl[0]._quantifier="SOME"
        rslt[3].sv[0].d_obj[0]._quantifier="DIGIT"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_85(self):
        print''
        print ('######################## test 9.5 ##############################')
        utterance="the bottle on the table, is blue. where is this tape"
        print "Object of this test : add relative and process nominal group with this as determinant and be as a verb"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                    [], 
                    [Verbal_Group(['be'], [],'present simple', 
                        [], 
                        [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                        [], [] ,'affirmative',[])])])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],[],[['blue',[]]],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'place', 
                [Nominal_Group(['this'],['tape'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_86(self):
        print''
        print ('######################## test 9.6 ##############################')
        utterance="the bottle of Jido which is blue, is on the table. I do my homework before he comes"
        print "Object of this test : nominal group with relative and noun complement and using before as subsentence"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
        rslt=[Sentence('statement', '', 
                [Nominal_Group(['the'],['bottle'],[],[Nominal_Group([],['Jido'],[],[],[])],[Sentence('relative', 'which', 
                    [], 
                    [Verbal_Group(['be'], [],'present simple', 
                        [Nominal_Group([],[],[['blue',[]]],[],[])], 
                        [],
                        [], [] ,'affirmative',[])])])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['do'], [],'present simple', 
                    [Nominal_Group(['my'],['homework'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence+statement', 'before', 
                        [Nominal_Group([],['he'],[],[],[])], 
                        [Verbal_Group(['come'], [],'present simple', 
                            [], 
                            [],
                            [], [] ,'affirmative',[])])])])]
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_87(self):
        print''
        print ('######################## test 9.7 ##############################')
        utterance="before he comes, I do my homework. I have played foot since I was a young boy."
        print "Object of this test : Using proposal like 'before' as subsentence, i_cmpl and adjective"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['do'], [],'present simple', 
                    [Nominal_Group(['my'],['homework'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence+statement', 'before', 
                        [Nominal_Group([],['he'],[],[],[])], 
                        [Verbal_Group(['come'], [],'present simple', 
                            [], 
                            [],
                            [], [] ,'affirmative',[])])])]),
        Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'present perfect', 
                    [Nominal_Group(['a'],['foot'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence+statement', 'since', 
                        [Nominal_Group([],['I'],[],[],[])], 
                        [Verbal_Group(['be'], [],'past simple', 
                            [Nominal_Group(['a'],['boy'],[['young',[]]],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])])]
        
        rslt[1].sv[0].d_obj[0]._quantifier="SOME"
        rslt[1].sv[0].vrb_sub_sentence[0].sv[0].d_obj[0]._quantifier="SOME"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
    def test_88(self):
        print''
        print ('######################## test 9.8 ##############################')
        utterance="They haven't played tennis since 1987. give me the glass the paper and the bottle."
        print "Object of this test : Final test with present perfect and parsing and with many nominal group"
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
        rslt=[Sentence('statement', '', 
                [Nominal_Group([],['they'],[],[],[])], 
                [Verbal_Group(['play'], [],'present perfect', 
                    [Nominal_Group(['a'],['tennis'],[],[],[])], 
                    [Indirect_Complement(['since'],[Nominal_Group(['1987'],[],[],[],[])])],
                    [], [] ,'negative',[])]),
            Sentence('imperative', '', 
                [], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['the'],['glass'],[],[],[]),
                     Nominal_Group(['the'],['paper'],[],[],[]),
                     Nominal_Group(['the'],['bottle'],[],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        rslt[0].sv[0].d_obj[0]._quantifier="SOME"
        rslt[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="DIGIT"
        
        result_test=compare_utterance(class_list,rslt,sentence_list)
        self.assertEquals(result_test, 0)
    
   
    
def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestParsing)
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite())

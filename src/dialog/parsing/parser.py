#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Created by Chouayakh Mahdi                                                       
 06/07/2010                                                                       
 The package contains functions to perform test                                   
 It is more used for the subject                                                  
 Functions:                                                                       
    compare_nom_gr : to compare 2 nominal groups                                  
    compare_icompl : to compare 2 indirect complements                            
    compare_vs : to compare 2 verbal structures                                   
    compare_sentence : to compare 2 sentences                                     
    compare_utterance : to compare 2 replies                                          
    display_ng : to display nominal group                                         
    display : to display class Sentence                                           
    unit_tests : to perform unit tests                                           
"""
from sentence import *
import logging
import preprocessing
import analyse_sentence



class Parser:
    def __init__(self):
        pass
    
    def parse(self, nl_input, active_sentence = None):

        #Return active_sentence if not empty, possibly send from Dialog.
        if active_sentence:
            return [active_sentence]
	
	#Do all basic replacements (like capitals, n't -> not, etc) + splits in several 
        #sentence with points.
        self._sentence_list = preprocessing.process_sentence(nl_input)
        
        #Do the actual grammatical parsing
        self._class_list = analyse_sentence.sentences_analyzer(self._sentence_list)
        
        for s in self._class_list:
            logging.debug(str(s))
        
        return self._class_list
             
       

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
                print vs[i].state
                print rslt_vs[i].state
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
            print sentence_list[i]
            
            print (str(utterance[i]))
            
            flag=compare_sentence(utterance[i], rslt_utterance[i])
            if flag==1:
                print "There is a problem with parsing this sentence"
                print ''
            elif flag==0:
                print "############### Parsing is OK ###############"
                print ''
            
            i=i+1
                   

def unit_tests():
    """
    Function to perform unit tests                                                   
    """ 
    """
    """
    ## Aim of this test : To use different cases with a state's verb 
    """
    print ''
    print ('######################## test 1.1 ##############################')

    utterance="The bottle is on the table. The bottle is blue. the bottle is Blue"
    print 'The object of our test is this utterance :'
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
                [Nominal_Group([],[],['blue'],[],[])], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '',
            [Nominal_Group(['the'],['bottle'],[],[],[])],
            [Verbal_Group(['be'], [],'present simple',
                [Nominal_Group([],['Blue'],[],[],[])],
                [],
                [], [] ,'affirmative',[])])]
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : To use the complement of the noun and the duplication with 'and'
    """
    print ''
    print ('######################## test 1.2 ##############################')

    utterance="Jido's blue bottle is on the table. I'll play a guitar, a piano and a violon."
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('statement', '', 
            [Nominal_Group(['the'],['bottle'],['blue'],[Nominal_Group([],['Jido'],[],[],[])],[])], 
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
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Present the duality between the direct and indirect complement
    """
    print ''
    print ('######################## test 1.3 ##############################')

    utterance="It's on the table. I give it to you. give me the bottle. I don't give the bottle to you."
    print 'The object of our test is this utterance :'
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
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : To have more information in sentence and trying the yes or no question
    """
    print ''
    print ('######################## test 1.4 ##############################')

    utterance="you aren't preparing the car and my father's moto at the same time. is the bottle of my brother in your right?"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('statement', '', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['prepare'], [],'present progressive', 
                [Nominal_Group(['the'],['car'],[],[],[]),Nominal_Group(['the'],['moto'],[],[Nominal_Group(['my'],['father'],[],[],[])],[])], 
                [Indirect_Complement(['at'],[Nominal_Group(['the'],['time'],['same'],[],[])])],
                [], [] ,'negative',[])]),
        Sentence('yes_no_question', '', 
            [Nominal_Group(['the'],['bottle'],[],[Nominal_Group(['my'],['brother'],[],[],[])],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['in'],[Nominal_Group(['your'],['right'],[],[],[])])],
                [], [] ,'affirmative',[])])]
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''

    
    
    """
    ## Aim of this test : Using different case of modal
    """
    print ''
    print ('######################## test 1.5 ##############################')

    utterance="You shouldn't drive his poorest uncle's wife's big new car. Should I give you the bottle? shall I go"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('statement', '', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['should+drive'], [],'present conditional', 
                [Nominal_Group(['the'],['car'],['big', 'new'],[Nominal_Group(['the'],['wife'],[],[Nominal_Group(['his'],['uncle'],['poorest'],[], [])],[])],[])], 
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
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different case of modal and start dialogue
    """
    print ''
    print ('######################## test 1.6 ##############################')

    utterance="Isn't he doing his homework and his game now? Can't he take this bottle. good afternoon"
    print 'The object of our test is this utterance :'
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
        Sentence('start', '', [], [])]
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using the second verb of the sentence
    """
    print ''
    print ('######################## test 1.7 ##############################')

    utterance="Don't quickly give me the blue bottle. I wanna play with my guitar. I'd like to go to the cinema."
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('imperative', '', 
            [], 
            [Verbal_Group(['give'], [],'present simple', 
                [Nominal_Group(['the'],['bottle'],['blue'],[],[])], 
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
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using relative with subject and object
    """
    print ''
    print ('######################## test 1.8 ##############################')

    utterance="the man, who talks, has a new car. I play the guitar, that I bought yesterday,."
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('statement', '', 
            [Nominal_Group(['the'],['man'],[],[],[Sentence('relative', 'who', 
                [],  
                [Verbal_Group(['talk'],[],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])])],  
            [Verbal_Group(['have'], [],'present simple', 
                [Nominal_Group(['a'],['car'],['new'],[],[])],
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
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    """
    
    """
    """
    ## Aim of this test : Using nested relative with he duplication with 'and' 
    """
    print ''
    print ('######################## test 2.1 ##############################')

    utterance="don't quickly give me the bottle which is on the table, and the glass which I cleaned yesterday, at my left"
    print 'The object of our test is this utterance :'
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

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using relative
    """
    print ''
    print ('######################## test 2.2 ##############################')

    utterance="The bottle that I bought from the store which is in the shopping center, , is yours."
    print 'The object of our test is this utterance :'
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
                            [Indirect_Complement(['in'],[Nominal_Group(['the'],['center'],['shopping'],[],[])])],
                            [], [] ,'affirmative',[])])])])],
                    [], [] ,'affirmative',[])])])],  
            [Verbal_Group(['be'], [],'present simple', 
                [Nominal_Group([],['yours'],[],[],[])],
                [],
                [], [] ,'affirmative',[])])]

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of when questions
    """
    print ''
    print ('######################## test 2.3 ##############################')

    utterance="When won't the planning session take place? when must you take the bus"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('w_question', 'date', 
            [Nominal_Group(['the'],['session'],['planning'],[],[])], 
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

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of where questions
    """
    print ''
    print ('######################## test 2.4 ##############################')

    utterance="Where is Broyen ? where are you going. Where must Jido and you be from?"
    print 'The object of our test is this utterance :'
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

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what questions and forced yes no question
    """
    print ''
    print ('######################## test 2.5 ##############################')

    utterance="What time is the news on TV? What size do you wear? the code is written by me. Mahdi is gonna the Laas?"
    print 'The object of our test is this utterance :'
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

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what questions
    """
    print ''
    print ('######################## test 2.6 ##############################')

    utterance="what is the weather like in the winter here? what were you doing? What isn't Jido going to do tomorrow"
    print 'The object of our test is this utterance :'
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

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what questions and disagree
    """
    print ''
    print ('######################## test 2.7 ##############################')

    utterance="What's happening. What must happen in the company today? What didn't happen here. no. Sorry."
    print 'The object of our test is this utterance :'
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
        Sentence('disagree', '', [], []),
        Sentence('disagree', '', [], [])]

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what questions
    """
    print ''
    print ('######################## test 2.8 ##############################')

    utterance="What is the biggest bottle's color on your left. What does your brother do for a living?"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('w_question', 'thing', 
            [Nominal_Group(['the'],['color'],[],[Nominal_Group(['the'],['bottle'],['biggest'],[],[])],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['on'],[Nominal_Group(['your'],['left'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'explication', 
            [Nominal_Group(['your'],['brother'],[],[],[])], 
            [Verbal_Group(['do'], [],'present simple', 
                [], 
                [Indirect_Complement(['for'],[Nominal_Group(['a'],[],['living'],[],[])])],
                [], [] ,'affirmative',[])])]
    
    rslt[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what questions
    """
    print ''
    print ('######################## test 2.9 ##############################')

    utterance="What type of people don't read this magazine? what kind of music must he listen to everyday"
    print 'The object of our test is this utterance :'
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
                [],
                [], ['everyday'] ,'affirmative',[])])]

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    """
    ## Aim of this test : Using different cases of what questions
    """
    print ''
    print ('######################## test 2.10 ##############################')

    utterance="What kind of sport is your favorite? what is the problem with him? what is the matter with this person"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('w_question', 'classification+sport', 
            [Nominal_Group(['your'],[],['favorite'],[],[])], 
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

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    """
    
    """
    """
    ## Aim of this test : Using different cases of how questions
    """
    print ''
    print ('######################## test 3.1 ##############################')

    utterance="How old are you? how long is your uncle's store opened tonight? how long is your uncle's store open tonight?"
    print 'The object of our test is this utterance :'
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
                [Nominal_Group([],[],['open'],[],[])], 
                [],
                [], ['tonight'] ,'affirmative',[])])]

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of how questions
    """
    print ''
    print ('######################## test 3.2 ##############################')

    utterance="how far is it from the hotel to the restaurant? how soon can you be here? How often does Jido go skiing?"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('w_question', 'far', 
            [Nominal_Group([],['it'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['from'],[Nominal_Group(['the'],['hotel'],[],[],[])]),Indirect_Complement(['to'],[Nominal_Group(['the'],['restaurant'],[],[],[])])],
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

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of how questions of quantity
    """
    print ''
    print ('######################## test 3.3 ##############################')

    utterance="how much water should they transport? how many guests weren't at the party? how much does the motocycle cost"
    print 'The object of our test is this utterance :'
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

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of how questions and agree
    """
    print ''
    print ('######################## test 3.4 ##############################')

    utterance="How about going to the cinema? how have not they gotten a loan for their business? OK"
    print 'The object of our test is this utterance :'
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
        Sentence('agree', '',[],[])]
    
    rslt[1].sv[0].d_obj[0]._quantifier="SOME"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of how questions 
    """
    print ''
    print ('######################## test 3.5 ##############################')

    utterance="How did you like Steven Spilburg's new movie. how could I get to the restaurant from here"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('w_question', 'opinion', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['like'], [],'past simple', 
                [Nominal_Group(['the'],['movie'],['new'],[Nominal_Group([],['Steven', 'Spilburg'],[],[],[])],[])], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'manner', 
            [Nominal_Group([],['I'],[],[],[])], 
            [Verbal_Group(['could+get+to'], [],'present conditional', 
                [Nominal_Group(['the'],['restaurant'],[],[],[])], 
                [],
                [], ['here'] ,'affirmative',[])])]

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of why, who and Whose questions 
    """
    print ''
    print ('######################## test 3.6 ##############################')

    utterance="Why should she go to Toulouse? who could you talk to on the phone. Whose blue bottle and red glass are these."
    print 'The object of our test is this utterance :'
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
            [Verbal_Group(['could+talk+to'], [],'present conditional', 
                [], 
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['phone'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'owner', 
            [Nominal_Group(['that'],['bottle'],['blue'],[],[]), Nominal_Group(['that'],['glass'],['red'],[],[])], 
            [Verbal_Group(['be'], [],'', 
                [], 
                [],
                [], [] ,'affirmative',[])])]

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what question with relative 
    """
    print ''
    print ('######################## test 3.7 ##############################')

    utterance="What are you thinking about the idea that I present you? what color is the bottle that you bought,"
    print 'The object of our test is this utterance :'
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

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what question with relative 
    """
    print ''
    print ('######################## test 3.8 ##############################')

    utterance="Which salesperson's competition won the award which we won in the last years"
    print 'The object of our test is this utterance :'
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
                        [Indirect_Complement(['in'],[Nominal_Group(['the'],['year'],['last'],[],[])])],
                        [], [] ,'affirmative',[])])])], 
                [],
                [], [] ,'affirmative',[])])]
    
    rslt[0].sv[0].d_obj[0].relative[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="ALL"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what question with relative 
    """
    print ''
    print ('######################## test 3.9 ##############################')

    utterance="what'll your house look like? what do you think of the latest novel which Jido wrote"
    print 'The object of our test is this utterance :'
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
                [Nominal_Group(['the'],['novel'],['latest'],[],[Sentence('relative', 'which', 
                    [Nominal_Group([],['Jido'],[],[],[])], 
                    [Verbal_Group(['write'], [],'past simple', 
                        [Nominal_Group(['the'],['novel'],['latest'],[],[])], 
                        [],
                        [], [] ,'affirmative',[])])])], 
            [],
            [], [] ,'affirmative',[])])]

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    """
    
    """
    """
    ## Aim of this test : Using different cases of what question with relative 
    """
    print ''
    print ('######################## test 4.1 ##############################')

    utterance="learn that I want you to give me the blue bottle,. If you do your job, you will be happy."
    print 'The object of our test is this utterance :'
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
                [], [] ,'affirmative',[Sentence('subsentence', 'that', 
                    [Nominal_Group([],['I'],[],[],[])], 
                    [Verbal_Group(['want'], [Verbal_Group(['give'], [],'', 
                            [Nominal_Group(['the'],['bottle'],['blue'],[],[])], 
                            [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                            [], [] ,'affirmative',[])],'present simple', 
                        [], 
                        [Indirect_Complement([],[Nominal_Group([],['you'],[],[],[])])],
                        [], [] ,'affirmative',[])])])]),
        Sentence('statement', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['be'], [],'future simple', 
                    [Nominal_Group([],[],['happy'],[],[])], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence', 'if', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['do'], [],'present simple', 
                            [Nominal_Group(['your'],['job'],[],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])])]

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using wrong in the what questions, using the 'or' and moving preposition like 'ago'
    """
    print ''
    print ('######################## test 4.2 ##############################')

    utterance="what is wrong with him? I'll play a guitar or a piano and a violon. I played a guitar a year ago."
    print 'The object of our test is this utterance :'
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
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : To use different cases with a state's verb 
    """
    print ''
    print ('######################## test 4.3 ##############################')

    utterance="this is a bottle. There is a bottle on the table"
    print 'The object of our test is this utterance :'
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
            [Nominal_Group(['there'],[],[],[],[])],
            [Verbal_Group(['be'], [],'present simple',
                [Nominal_Group(['a'],['bottle'],[],[],[])], 
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                [], [] ,'affirmative',[])])]
    
    rslt[0].sv[0].d_obj[0]._quantifier="SOME"
    rslt[1].sv[0].d_obj[0]._quantifier="SOME"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : To use different cases with a state's verb 
    """
    print ''
    print ('######################## test 4.4 ##############################')

    utterance="What do you do for a living in this building? What does your brother do for a living here"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('w_question', 'explication', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['do'], [],'present simple', 
                [], 
                [Indirect_Complement(['for'],[Nominal_Group(['a'],[],['living'],[],[])]),
                 Indirect_Complement(['in'],[Nominal_Group(['this'],['building'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'explication', 
            [Nominal_Group(['your'],['brother'],[],[],[])], 
            [Verbal_Group(['do'], [],'present simple', 
                [], 
                [Indirect_Complement(['for'],[Nominal_Group(['a'],[],['living'],[],[])])],
                [], ['here'] ,'affirmative',[])])]
    
    rslt[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
    rslt[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : To use different cases with a state's verb 
    """
    print ''
    print ('######################## test 4.5 ##############################')

    utterance="To whom are you talking? you should have the bottle. would you have played a guitar. you would have played a guitar"
    print 'The object of our test is this utterance :'
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
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : To use different cases with a state's verb 
    """
    print ''
    print ('######################## test 4.6 ##############################')

    utterance="you'd like the blue bottle or the glass? the green or blue bottle is on the table. the green or the blue glass is mine?"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('yes_no_question', '', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['like'], [],'present conditional', 
                [Nominal_Group(['the'],['bottle'],['blue'],[],[]),Nominal_Group(['the'],['glass'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])]),       
        Sentence('statement', '', 
            [Nominal_Group(['the'],['bottle'],['green'],[],[]),Nominal_Group(['the'],['bottle'],['blue'],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                [], [] ,'affirmative',[])]), 
        Sentence('yes_no_question', '', 
            [Nominal_Group(['the'],['glass'],['green'],[],[]),Nominal_Group(['the'],['glass'],['blue'],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [Nominal_Group([],['mine'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])])]
    
    rslt[0].sv[0].d_obj[1]._conjunction="OR"
    rslt[1].sn[1]._conjunction="OR"
    rslt[2].sn[1]._conjunction="OR"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what question with relative 
    """
    print ''
    print ('######################## test 4.7 ##############################')

    utterance="learn that I want you to give me the blue bottle that is blue."
    print 'The object of our test is this utterance :'
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
                [], [] ,'affirmative',[Sentence('subsentence', 'that', 
                    [Nominal_Group([],['I'],[],[],[])], 
                    [Verbal_Group(['want'], [Verbal_Group(['give'], [],'', 
                            [Nominal_Group(['the'],['bottle'],['blue'],[],[Sentence('relative', 'that', 
                                [], 
                                [Verbal_Group(['be'], [],'present simple', 
                                    [Nominal_Group([],[],['blue'],[],[])], 
                                    [],
                                    [], [] ,'affirmative',[])])])], 
                            [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                            [], [] ,'affirmative',[])],'present simple', 
                        [], 
                        [Indirect_Complement([],[Nominal_Group([],['you'],[],[],[])])],
                        [], [] ,'affirmative',[])])])])]

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    print ''
    print ('######################## test 4.8 ##############################')

    utterance="The bottle is behind to me. The bottle is next to the table in front of the kitchen."
    print 'The object of our test is this utterance :'
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
                 Indirect_Complement(['in+front+of'],[Nominal_Group(['the'],['kitchen'],[],[],[])])],
                [], [] ,'affirmative',[])])]
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using relative with subject and object
    """
    print ''
    print ('######################## test 4.9 ##############################')

    utterance="Take the bottle carefully. I take that bottle that I drink in. I take twenty two bottles."
    print 'The object of our test is this utterance :'
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
                [Nominal_Group(['twenty+two'],['bottle'],[],[],[])],
                [],
                [], [] ,'affirmative',[])])]
    
    rslt[2].sv[0].d_obj[0]._quantifier="DIGIT"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    """

    """
    """
    ## Aim of this test : To use the complement of the noun and the duplication with 'and'
    """
    print ''
    print ('######################## test 5.1 ##############################')

    utterance="I'll play Jido's guitar, a saxophone, a piano of the wife of my oncle and Patrick's violon."
    print 'The object of our test is this utterance :'
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
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    """
    ## Aim of this test : To use the complement of the noun and the duplication with 'and'
    """
    print ''
    print ('######################## test 5.2 ##############################')

    utterance="Give me two or three bottles. the bottle is blue, big and fanny. give me the bottle on the table"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('imperative', '', 
            [], 
            [Verbal_Group(['give'], [],'present simple', 
                [Nominal_Group(['two'],['bottle'],[],[],[]),
                 Nominal_Group(['three'],['bottle'],[],[],[])], 
                [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group(['the'],['bottle'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [Nominal_Group([],[],['blue', 'big', 'fanny'],[],[])], 
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
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what question with relative 
    """
    print ''
    print ('######################## test 5.3 ##############################')

    utterance="the boys' ball is blue. He ask me to do something. is any person courageous on the laboratory"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('statement', '', 
            [Nominal_Group(['the'],['ball'],[],[Nominal_Group(['the'],['boy'],[],[],[])],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [Nominal_Group([],[],['blue'],[],[])], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['he'],[],[],[])], 
            [Verbal_Group(['ask'], [Verbal_Group(['do'], [],'', 
                [Nominal_Group([],['something'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])],'present simple', 
            [], 
            [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
            [], [] ,'affirmative',[])]),
        Sentence('yes_no_question', '', 
            [Nominal_Group(['any'],['person'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [Nominal_Group([],[],['courageous'],[],[])], 
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['laboratory'],[],[],[])])],
                [], [] ,'affirmative',[])])]
    
    rslt[0].sn[0].noun_cmpl[0]._quantifier="ALL"
    rslt[2].sn[0]._quantifier="ANY"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what questions and disagree
    """
    print ''
    print ('######################## test 5.4 ##############################')

    utterance="What must be happened in the company today? The building shouldn't be built fastly. You can be here. It can be played by twenty players"
    print 'The object of our test is this utterance :'
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
                [], ['here'] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['it'],[],[],[])],  
            [Verbal_Group(['can+play'],[],'present passive', 
                [], 
                [Indirect_Complement(['by'],[Nominal_Group(['twenty'],['player'],[],[],[])])],
                [], [] ,'affirmative',[])])]
    
    rslt[3].sv[0].i_cmpl[0].nominal_group[0]._quantifier="DIGIT"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what questions and disagree
    """
    print ''
    print ('######################## test 5.5 ##############################')

    utterance="what size is the best one? What object is blue? How good is this"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('w_question', 'size', 
            [Nominal_Group(['the'],['one'],['best'],[],[])],  
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'object', 
            [],  
            [Verbal_Group(['be'], [],'present simple', 
                [Nominal_Group([],[],['blue'],[],[])], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('w_question', 'good', 
            [Nominal_Group(['this'],[],[],[],[])],  
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [],
                [], [] ,'affirmative',[])])]

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    """
    ## Aim of this test : Using different cases of what questions and disagree
    """
    print ''
    print ('######################## test 5.6 ##############################')

    utterance="He Patrick, the bottle is on the table. give it to me"
    print 'The object of our test is this utterance : '
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
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what questions and disagree
    """
    print ''
    print ('######################## test 5.7 ##############################')

    utterance="Jido, give me the bottle. Jido, Patrick and you will go to the cinema. Jido, Patrick and you, give me the bottle"
    print 'The object of our test is this utterance : '
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('interjection', '', 
            [Nominal_Group([],['Jido'],[],[],[])],  
            []),
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
            []),
        Sentence('imperative', '', 
            [Nominal_Group([],['Jido'],[],[],[]),Nominal_Group([],['Patrick'],[],[],[]),Nominal_Group([],['you'],[],[],[])],  
            [Verbal_Group(['give'], [],'present simple', 
                [Nominal_Group(['the'],['bottle'],[],[],[])], 
                [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                [], [] ,'affirmative',[])])]

    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what question with relative 
    """
    print ''
    print ('######################## test 5.8 ##############################')

    utterance="The bottle is not blue but it is red. It is not the glass but the bottle. it is blue or red"
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('statement', '', 
            [Nominal_Group(['the'],['bottle'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [Nominal_Group([],[],['blue'],[],[])], 
                [],
                [], [] ,'negative',[Sentence('subsentence', 'but', 
                    [Nominal_Group([],['it'],[],[],[])], 
                    [Verbal_Group(['be'], [],'present simple', 
                        [Nominal_Group([],[],['red'],[],[])], 
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
                [Nominal_Group([],[],['blue'],[],[]),Nominal_Group([],[],['red'],[],[])], 
                [],
                [], [] ,'affirmative',[])])]
    
    rslt[1].sv[0].d_obj[1]._conjunction="BUT"
    rslt[2].sv[0].d_obj[1]._conjunction="OR"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    """
    
    
    """
    ## Aim of this test : Using different cases of what question with relative 
    """
    print ''
    print ('######################## test 6.1 ##############################')

    utterance="It is not red but blue. a kind of thing. this is my banana. bananas are fruits."
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('statement', '', 
            [Nominal_Group([],['it'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [Nominal_Group([],[],['red'],[],[]),Nominal_Group([],[],['blue'],[],[])], 
                [],
                [], [] ,'negative',[])]),
        Sentence('statement', '', 
            [Nominal_Group(['a'],['kind'],[],[Nominal_Group(['a'],['thing'],[],[],[])],[])], 
            [Verbal_Group(['.'], [],'present simple', 
                [], 
                [],
                [], [] ,'affirmative',[])]),
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
    rslt[1].sn[0]._quantifier="SOME"
    rslt[1].sn[0].noun_cmpl[0]._quantifier="SOME"
    rslt[3].sn[0]._quantifier="ALL"
    rslt[3].sv[0].d_obj[0]._quantifier="ALL"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what question with relative 
    """
    print ''
    print ('######################## test 6.2 ##############################')

    utterance="there are no bananas. All bananas are here. give me more information about the bottle."
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('statement', '', 
            [Nominal_Group(['there'],[],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [Nominal_Group(['no'],['banana'],[],[],[])], 
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
                [Nominal_Group(['more'],['information'],[],[],[])], 
                [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])]),
                 Indirect_Complement(['about'],[Nominal_Group(['the'],['bottle'],[],[],[])])],
                [], [] ,'affirmative',[])])]
    
    rslt[0].sn[0]._quantifier="SOME"
    rslt[0].sv[0].d_obj[0]._quantifier="ANY"
    rslt[1].sn[0]._quantifier="ALL"
    rslt[2].sv[0].d_obj[0]._quantifier="SOME"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what question with relative 
    """
    print ''
    print ('######################## test 6.3 ##############################')

    utterance="Jido, tell me where you go. Goodbye. Bye. there is nothing. it is another one."
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('interjection', '', 
            [Nominal_Group([],['Jido'],[],[],[])],  
            []),
        Sentence('imperative', '', 
            [Nominal_Group([],['Jido'],[],[],[])], 
            [Verbal_Group(['tell'], [],'present simple', 
                [], 
                [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                [], [] ,'affirmative',[Sentence('subsentence', 'where', 
                    [Nominal_Group([],['you'],[],[],[])], 
                    [Verbal_Group(['go'], [],'present simple', 
                        [], 
                        [],
                        [], [] ,'affirmative',[])])])]),
        Sentence('end', '', [], []),
        Sentence('end', '', [], []),
        Sentence('statement', '', 
            [Nominal_Group(['there'],[],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [Nominal_Group([],['nothing'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group([],['it'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [Nominal_Group(['another'],['one'],[],[],[])], 
                [],
                [], [] ,'affirmative',[])])]
    
    rslt[4].sv[0].d_obj[0]._quantifier="NONE"
    rslt[5].sv[0].d_obj[0]._quantifier="SOME"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what question with relative 
    """
    print ''
    print ('######################## test 6.4 ##############################')

    utterance="The bottle becomes blue. One piece could become two, if you smoldered it."
    print 'The object of our test is this utterance :'
    print utterance
    print '#################################################################'
    print ''
    sentence_list=preprocessing.process_sentence(utterance)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    
    rslt=[Sentence('statement', '', 
            [Nominal_Group(['the'],['bottle'],[],[],[])], 
            [Verbal_Group(['become'], [],'present simple', 
                [Nominal_Group([],[],['blue'],[],[])], 
                [],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '', 
            [Nominal_Group(['one'],['piece'],[],[],[])], 
            [Verbal_Group(['could+become'], [],'present conditional', 
                [Nominal_Group(['two'],[],[],[],[])], 
                [],
                [], [] ,'affirmative',[Sentence('subsentence', 'if', 
                    [Nominal_Group([],['you'],[],[],[])], 
                    [Verbal_Group(['smolder'], [],'past simple', 
                        [Nominal_Group([],['it'],[],[],[])], 
                        [],
                        [], [] ,'affirmative',[])])])])]
    
    rslt[1].sn[0]._quantifier="DIGIT"
    rslt[1].sv[0].d_obj[0]._quantifier="DIGIT"
    
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    """
    ## Aim of this test : Using different cases of what question with relative 
    """
    print ''
    print ('######################## test 6.5 ##############################')

    utterance="This one is not the bottle of my uncle but it is the bottle of my brother. It is not on the table but on the shelf."
    print 'The object of our test is this utterance :'
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
                [], [] ,'negative',[Sentence('subsentence', 'but', 
                    [Nominal_Group([],['it'],[],[],[])], 
                    [Verbal_Group(['be'], [],'present simple', 
                        [Nominal_Group(['the'],['bottle'],[],[Nominal_Group(['my'],['brother'],[],[],[])],[])], 
                        [],
                        [], [] ,'affirmative',[])])])]),
        Sentence('statement', '', 
            [Nominal_Group([],['it'],[],[],[])], 
            [Verbal_Group(['be'], [],'present simple', 
                [], 
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])]),
                 Indirect_Complement(['on'],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                [], [] ,'negative',[])])]
    
    rslt[1].sv[0].i_cmpl[1].nominal_group[0]._conjunction="BUT"
  
    compare_utterance(class_list,rslt,sentence_list)
    print ''
    
    
    
    
if __name__ == '__main__':
    unit_tests()

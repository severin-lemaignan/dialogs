#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
######################################################################################
## Created by Chouayakh Mahdi                                                       ##
## 08/07/2010                                                                       ##
## The package contains functions to perform test                                   ##
## It is more used for the subject                                                  ##
## Functions:                                                                       ##

##    unit_tests : to perform unit tests                                            ##
######################################################################################
"""

__author__ =  'Séverin Lemaignan'

import logging
import unittest

from sentence import *

import utterance_recovery

class Verbalizer:
    """Implements the verbalization module: Verbalizer.verbalize() takes as
    input a Sentence object and build from it a sentence in natural language.
    """
    def verbalize(self, sentence):
        logging.debug("Verbalizing now...")
        nl_sentence = utterance_recovery.verbalising(sentence)
        logging.debug("Rebuild sentence to: \"" + nl_sentence + "\"")
        return nl_sentence


"""
######################################################################################
## Function to compare 2 nominal groups                                             ##
######################################################################################
"""
class TestVerbalization(unittest.TestCase):
    
    def test_01(self):
        print ''
        print '######################## test 1.1 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="The bottle is on the table. The bottle is blue. the bottle is Blue"
        
        sentences=[Sentence('statement', '',
                [Nominal_Group(['the'],['bottle'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [],
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '',
                [Nominal_Group(['the'],['bottle'],['blue'],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '',
                [Nominal_Group(['the'],['bottle'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [Nominal_Group([],['Blue'],[],[],[])],
                    [],
                    [], [] ,'affirmative',[])])]
        
        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_02(self):
        
        print ''
        print '######################## test 1.2 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Jido's blue bottle is on the table. I'll play a guitar, a piano and a violon."
     
        sentences=[Sentence('statement', '', 
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
        
        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)

    def test_03(self):
        
        print ''
        print '######################## test 1.3 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="It's on the table. I give it to you. give me the bottle. I don't give the bottle to you."
        
        sentences=[Sentence('statement', '', 
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
        
        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_04(self):
        
        print ''
        print '######################## test 1.4 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="you aren't preparing the car and my father's moto at the same time. is the bottle of my brother in your right?"
        
        sentences=[Sentence('statement', '', 
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
        
        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)

    def test_05(self):
    
        print ''
        print '######################## test 1.5 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="You shouldn't drive his poorest uncle's wife's big new car. Should I give you the bottle? shall I go"
        
        sentences=[Sentence('statement', '', 
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
        
        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_06(self):
    
        print ''
        print '######################## test 1.6 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Isn't he doing his homework and his game now? Cann't he take this bottle. good afternoon"
        
        sentences=[Sentence('yes_no_question', '', 
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
        
        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_07(self):
        
        print ''
        print '######################## test 1.7 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Don't quickly give me the blue bottle. I wanna play with my guitar. I'd like to go to the cinema."
        
        sentences=[Sentence('imperative', '', 
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
        
        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_08(self):
        
        print ''
        print '######################## test 1.8 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="the man which talks ; has a new car. I play the guitar which I bought yesterday ; ."
        
        sentences=[Sentence('statement', '', 
                [Nominal_Group(['the'],['man'],[],[],[Sentence('relative', '', 
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
                    [Nominal_Group(['the'],['guitar'],[],[],[Sentence('relative', '', 
                        [Nominal_Group([],['I'],[],[],[])],  
                        [Verbal_Group(['buy'],[],'past simple', 
                            [], 
                            [],
                            [], ['yesterday'] ,'affirmative',[])])])],
                    [],
                    [], [] ,'affirmative',[])])]

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_09(self):
        
        print ''
        print '######################## test 1.9 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="don't quickly give me the bottle which is on the table ; and the glass which I cleaned yesterday ; at my left"
        
        sentences=[Sentence('imperative', '', 
                [],  
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', '', 
                        [],  
                        [Verbal_Group(['be'], [],'present simple', 
                            [],
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                            [], [] ,'affirmative',[])])]),
                    Nominal_Group(['the'],['glass'],[],[],[Sentence('relative', '', 
                        [Nominal_Group([],['I'],[],[],[])],  
                        [Verbal_Group(['clean'], [],'past simple', 
                            [],
                            [],
                            [], ['yesterday'] ,'affirmative',[])])])],
                [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])]), Indirect_Complement(['at'],[Nominal_Group(['my'],['left'],[],[],[])])],
                ['quickly'], [] ,'negative',[])])]

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_10(self):
        
        print ''
        print '######################## test 1.10 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="The bottle which I bought from the store which is in the shopping centre ; ; is yours."
        
        sentences=[Sentence('statement', '', 
                [Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', '', 
                    [Nominal_Group([],['I'],[],[],[])],  
                    [Verbal_Group(['buy'], [],'past simple', 
                        [], 
                        [Indirect_Complement(['from'],[Nominal_Group(['the'],['store'],[],[],[Sentence('relative', '', 
                            [],  
                            [Verbal_Group(['be'], [],'present simple', 
                                [], 
                                [Indirect_Complement(['in'],[Nominal_Group(['the'],['centre'],['shopping'],[],[])])],
                                [], [] ,'affirmative',[])])])])],
                        [], [] ,'affirmative',[])])])],  
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],['yours'],[],[],[])],
                    [],
                    [], [] ,'affirmative',[])])]

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_11(self):
        
        print ''
        print '######################## test 1.11 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="When won't the planning session take place? when must you take the bus"
        
        sentences=[Sentence('w_question', 'date', 
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

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    def test_12(self):
        
        print ''
        print '######################## test 1.12 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Where is Broyen ? where are you going. Where must Jido and you be from?"
        
        sentences=[Sentence('w_question', 'place', 
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

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_13(self):
        
        print ''
        print '######################## test 1.13 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What time is the news on TV? What size do you wear? the code is written by me. Mahdi is gonna to the Laas?"
        
        sentences=[Sentence('w_question', 'time', 
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

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_14(self):
        
        print ''
        print '######################## test 1.14 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="what is the weather like in the winter here? what were you doing? What isn't Jido going to do tomorrow"
        
        sentences=[Sentence('w_question', 'description', 
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

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_15(self):
        
        print ''
        print '######################## test 1.15 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What's happening. What must happen in the company today? What didn't happen here. no. Sorry."
        
        sentences=[Sentence('w_question', 'situation', 
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

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_16(self):
        
        print ''
        print '######################## test 1.16 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What is the bigest bottle's color on your left. What does your brother do for a living?"
        
        sentences=[Sentence('w_question', 'thing', 
                [Nominal_Group(['the'],['color'],[],[Nominal_Group(['the'],['bottle'],['bigest'],[],[])],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['your'],['left'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'explication', 
                [Nominal_Group(['your'],['brother'],[],[],[])], 
                [Verbal_Group(['do'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['for'],[Nominal_Group(['a'],['living'],[],[],[])])],
                    [], [] ,'affirmative',[])])]

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_17(self):
        
        print ''
        print '######################## test 1.17 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What type of people don't read this magazine? what kind of music must he listen to everyday"
        
        sentences=[Sentence('w_question', 'classification+people', 
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

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_18(self):
        
        print ''
        print '######################## test 1.18 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What kind of sport is your favourite? what is the problem with him? what is the matter with this person"
        
        sentences=[Sentence('w_question', 'classification+sport', 
                [Nominal_Group(['your'],['favourite'],[],[],[])], 
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

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_19(self):
        
        print ''
        print '######################## test 1.19 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="How old are you? how long is your uncle's store opened tonight? how long is your uncle's store open tonight?"
        
        sentences=[Sentence('w_question', 'age', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'duration', 
                [Nominal_Group(['the'],['store'],[],[Nominal_Group(['your'],['uncle'],[],[],[])],[])], 
                [Verbal_Group(['open'], [],'present passive', 
                    [], 
                    [],
                    [], ['tonight'] ,'affirmative',[])]),
            Sentence('w_question', 'duration', 
                [Nominal_Group(['the'],['store'],['open'],[Nominal_Group(['your'],['uncle'],[],[],[])],[])],  
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_20(self):
        
        print ''
        print '######################## test 1.20 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="how far is it from the hotel to the restaurant? how soon can you be here? How often does Jido go skiing?"
        
        sentences=[Sentence('w_question', 'distance', 
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['from'],[Nominal_Group(['the'],['hotel'],[],[],[])]),Indirect_Complement(['to'],[Nominal_Group(['the'],['restaurant'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'time', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['can+be'], [],'present simple', 
                    [], 
                    [],
                    [], ['here'] ,'affirmative',[])]),
            Sentence('w_question', 'frequency', 
                [Nominal_Group([],['Jido'],[],[],[])],  
                [Verbal_Group(['go+skiing'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_21(self):
        
        print ''
        print '######################## test 1.21 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="how much water should they transport? how many guests weren't at the party? how much does the motocycle cost"
        
        sentences=[Sentence('w_question', 'quantity', 
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

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_22(self):
        
        print ''
        print '######################## test 1.22 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="How about going to the cinema? how have not they gotten a loan for their business? OK"
        
        sentences=[Sentence('w_question', 'invitation', 
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

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_23(self):
        
        print ''
        print '######################## test 1.23 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="How did you like Steven Spilburg's new movie. how could I get to the restaurant from here"
        
        sentences=[Sentence('w_question', 'opinion', 
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

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_24(self):
        
        print ''
        print '######################## test 1.24 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Why should she go to Toulouse? who could you talk to on the phone. Whose blue bottle and red glass are these."
        
        sentences=[Sentence('w_question', 'reason', 
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
            Sentence('w_question', 'possession', 
                [Nominal_Group(['that'],['bottle'],['blue'],[],[]), Nominal_Group(['that'],['glass'],['red'],[],[])], 
                [Verbal_Group(['be'], [],'', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
       
    def test_25(self):
       
        print ''
        print '######################## test 1.25 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="What are you thinking about the idea which I present you ; ? what color is the bottle which you bought ;"
        
        sentences=[Sentence('w_question', 'opinion', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['think+about'], [],'present progressive', 
                    [Nominal_Group(['the'],['idea'],[],[],[Sentence('relative', '', 
                        [Nominal_Group([],['I'],[],[],[])], 
                        [Verbal_Group(['present'], [],'present simple', 
                            [Nominal_Group([],['you'],[],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'color', 
                [Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', '', 
                    [Nominal_Group([],['you'],[],[],[])], 
                    [Verbal_Group(['buy'], [],'past simple', 
                        [], 
                        [],
                        [], [] ,'affirmative',[])])])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_26(self):
        
        print ''
        print '######################## test 1.26 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="Which competition's salesperson won the award which we won in the last years ;."
        
        sentences=[Sentence('w_question', 'choice', 
                [Nominal_Group(['the'],['salesperson'],[],[Nominal_Group(['the'],['competition'],[],[],[])],[])], 
                [Verbal_Group(['win'], [],'past simple', 
                    [Nominal_Group(['the'],['award'],[],[],[Sentence('relative', '', 
                        [Nominal_Group([],['we'],[],[],[])], 
                        [Verbal_Group(['win'], [],'past simple', 
                            [], 
                            [Indirect_Complement(['in'],[Nominal_Group(['the'],['years'],['last'],[],[])])],
                            [], [] ,'affirmative',[])])])], 
                    [],
                    [], [] ,'affirmative',[])])]

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_27(self):
        
        print ''
        print '######################## test 1.27 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="what'll your house look like? what do you think of the latest novel which Jido wrote ;"
        
        sentences=[Sentence('w_question', 'descrition', 
                [Nominal_Group(['your'],['house'],[],[],[])], 
                [Verbal_Group(['look+like'], [],'future simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'opinion', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['think+of'], [],'present simple', 
                    [Nominal_Group(['the'],['novel'],['latest'],[],[Sentence('relative', '', 
                        [Nominal_Group([],['Jido'],[],[],[])], 
                        [Verbal_Group(['write'], [],'past simple', 
                            [], 
                            [],
                            [], [] ,'affirmative',[])])])], 
                [],
                [], [] ,'affirmative',[])])]

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_28(self):
        
        print ''
        print '######################## test 1.28 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="learn that I want you to give me the blue bottle ;. If you do your job ; you will be happy."
        
        sentences=[Sentence('imperative', '', 
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
                            [Nominal_Group([],['you'],[],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])]),
            Sentence('statement', '', 
                [Nominal_Group([],['you'],['happy'],[],[])], 
                [Verbal_Group(['be'], [],'future simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence', 'if', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['do'], [],'present simple', 
                            [Nominal_Group(['your'],['job'],[],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])])]

        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
       
   
    def test_29(self):
        print ''
        print '######################## test 1.29 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="you will be happy if you do your job ; .do you want the blue bottle or the green bottle ?"
        
        sentences=[Sentence('statement', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['be'], [],'future simple', 
                    [Nominal_Group([],[],['happy'],[],[])], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence', 'if', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['do'], [],'present simple', 
                            [Nominal_Group(['your'],['job'],[],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])]),
            Sentence('yes_no_question', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['want'], [], 
                    'present simple',
                    [Nominal_Group(['the'],[],['blue'],[],[]),Nominal_Group([],['bottle'],['green'],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])]

        sentences[1].sv[0].d_obj[1]._conjunction="OR"
        
        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
        
        
    def test_30(self):
        print ''
        print '######################## test 1.30 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="To whom are you talking? would you have played a guitar. you would have played a guitar"
        
        sentences=[Sentence('w_question', 'people', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['talk+to'], [],'present progressive', 
                [], 
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
        
        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
       
       
        
    def test_31(self):
        print ''
        print '######################## test 1.31 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="To whom are you talking? would you have played a guitar. you would have played a guitar"
        
        sentences=[Sentence('w_question', 'people', 
            [Nominal_Group([],['you'],[],[],[])], 
            [Verbal_Group(['talk+to'], [],'present progressive', 
                [], 
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
        
        utterance=utterance_recovery.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is : ", utterance
        
        self.assertEquals(original_utterance, utterance)
    
    
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format="%(message)s")
       
    # executing verbalization tests
    suiteVerbalization = unittest.TestLoader().loadTestsFromTestCase(TestVerbalization)

    
    unittest.TextTestRunner(verbosity=2).run(suiteVerbalization)
    

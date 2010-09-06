#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Created by Chouayakh Mahdi  
 08/07/2010                                                                       
 The package contains functions to perform test                                   
 It is more used for the subject                                                  
 Functions:                                                                       
    unit_tests : to perform unit tests                                            
"""

import unittest
import logging
logger = logging.getLogger("dialog")

from dialog.dialog_core import Dialog

from dialog.parsing.parser import Parser
from dialog.sentence import *
import utterance_rebuilding


class TestVerbalization(unittest.TestCase):
    """
    Function to compare 2 nominal groups   
    """
    
    
    def test_01(self):
        logger.info('\n######################## test 1.1 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="The bottle is on the table. The bottle is blue. The bottle is Blue."
        
        sentences=[Sentence('statement', '',
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_02(self):
        
        logger.info('\n######################## test 1.2 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Jido's blue bottle is on the table. I'll play a guitar, a piano and a violon."
     
        sentences=[Sentence('statement', '', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
        
    def test_03(self):
        
        logger.info('\n######################## test 1.3 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="It's on the table. I give it to you. Give me the bottle. I don't give the bottle to you."
        
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_04(self):
        
        logger.info('\n######################## test 1.4 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="You aren't preparing the car and my father's moto at the same time. Is my brother's bottle in your right?"
        
        sentences=[Sentence('statement', '', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_05(self):
    
        logger.info('\n######################## test 1.5 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="You shouldn't drive his poorest uncle's wife's big new car. Should I give you the bottle? Shall I go?"
        
        sentences=[Sentence('statement', '', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    
    
    def test_06(self):
    
        logger.info('\n######################## test 1.6 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Isn't he doing his homework and his game now? Can't he take this bottle? Hello."
        
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_07(self):
        
        logger.info('\n######################## test 1.7 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Don't quickly give me the blue bottle. I want to play with my guitar. I'd like to go to the cinema."
        
        sentences=[Sentence('imperative', '', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_08(self):
        
        logger.info('\n######################## test 1.8 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="The man who talks, has a new car. I play the guitar that I bought yesterday."
        
        sentences=[Sentence('statement', '', 
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
                            [], 
                            [],
                            [], ['yesterday'] ,'affirmative',[])])])],
                    [],
                    [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_09(self):
        
        logger.info('\n######################## test 1.9 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Don't quickly give me the bottle which is on the table, and the glass which I cleaned yesterday, at my left."
        
        sentences=[Sentence('imperative', '', 
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
                            [],
                            [],
                            [], ['yesterday'] ,'affirmative',[])])])],
                [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])]), Indirect_Complement(['at'],[Nominal_Group(['my'],['left'],[],[],[])])],
                ['quickly'], [] ,'negative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_10(self):
        
        logger.info('\n######################## test 1.10 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="The bottle that I bought from the store which is in the shopping center, is yours."
        
        sentences=[Sentence('statement', '', 
                [Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'that', 
                    [Nominal_Group([],['I'],[],[],[])],  
                    [Verbal_Group(['buy'], [],'past simple', 
                        [], 
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

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_11(self):
        
        logger.info('\n######################## test 1.11 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="When won't the planning session take place? When must you take the bus?"
        
        sentences=[Sentence('w_question', 'date', 
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

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_12(self):
        
        logger.info('\n######################## test 1.12 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Where is Broyen? Where are you going? Where must Jido and you be from?"
        
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

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_13(self):
        
        logger.info('\n######################## test 1.13 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="What time is the news on TV? What size do you wear? The code is written by me. Is Mahdi going to the Laas?"
        
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

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_14(self):
        
        logger.info('\n######################## test 1.14 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="What's the weather like in the winter here? What were you doing? What isn't Jido going to do tomorrow?"
        
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

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_15(self):
        
        logger.info('\n######################## test 1.15 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="What's happening? What must happen in the company today? What didn't happen here? No, sorry."
        
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
            Sentence('disagree', '', [], [])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_16(self):
        
        logger.info('\n######################## test 1.16 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="What's the biggest bottle's color on your left? What does your brother do for a living?"
        
        sentences=[Sentence('w_question', 'thing', 
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

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_17(self):
        
        logger.info('\n######################## test 1.17 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="What kind of people don't read this magazine? What kind of music must he listen to everyday?"
        
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

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_18(self):
        
        logger.info('\n######################## test 1.18 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="What kind of sport is your favorite? What's the problem with him? What's the matter with this person?"
        
        sentences=[Sentence('w_question', 'classification+sport', 
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

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_19(self):
        
        logger.info('\n######################## test 1.19 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="How old are you? How long is your uncle's store opened tonight? How long is your uncle's store open tonight?"
        
        sentences=[Sentence('w_question', 'old', 
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

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_20(self):
        
        logger.info('\n######################## test 1.20 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="How far is it from the hotel to the restaurant? How soon can you be here? How often does Jido go skiing?"
        
        sentences=[Sentence('w_question', 'far', 
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

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_21(self):
        
        logger.info('\n######################## test 1.21 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="How much water should they transport? How much guests weren't at the party? How much does the motocycle cost?"
        
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

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_22(self):
        
        logger.info('\n######################## test 1.22 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="How about going to the cinema? How haven't they gotten a loan for their business? OK."
        
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

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_23(self):
        
        logger.info('\n######################## test 1.23 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="What did you think of Steven Spilburg's new movie? How could I get to the restaurant from here?"
        
        sentences=[Sentence('w_question', 'opinion', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['like'], [],'past simple', 
                    [Nominal_Group(['the'],['movie'],[['new',[]]],[Nominal_Group([],['Steven', 'Spilburg'],[],[],[])],[])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'manner', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['could+get+to'], [],'present conditional', 
                    [Nominal_Group(['the'],['restaurant'],[],[],[])], 
                    [Indirect_Complement(['from'],[Nominal_Group([],['here'],[],[],[])])],
                    [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_24(self):
        
        logger.info('\n######################## test 1.24 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Why should she go to Toulouse? Who could you talk to on the phone? Whose blue bottle and red glass are these?"
        
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
            Sentence('w_question', 'owner', 
                [Nominal_Group([],['bottle'],[['blue',[]]],[],[]), Nominal_Group([],['glass'],[['red',[]]],[],[])], 
                [Verbal_Group(['be'], [],'', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance) 
    
    def test_25(self):
       
        logger.info('\n######################## test 1.25 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="What are you thinking about the idea that I present you? What color is the bottle which you bought?"
        
        sentences=[Sentence('w_question', 'opinion', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['think+about'], [],'present progressive', 
                    [Nominal_Group(['the'],['idea'],[],[],[Sentence('relative', 'that', 
                        [Nominal_Group([],['I'],[],[],[])], 
                        [Verbal_Group(['present'], [],'present simple', 
                            [], 
                            [Indirect_Complement([],[Nominal_Group([],['you'],[],[],[])])],
                            [], [] ,'affirmative',[])])])], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('w_question', 'color', 
                [Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                    [Nominal_Group([],['you'],[],[],[])], 
                    [Verbal_Group(['buy'], [],'past simple', 
                        [], 
                        [],
                        [], [] ,'affirmative',[])])])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_26(self):
        
        logger.info('\n######################## test 1.26 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Which salesperson's competition won the award which we won in the last years?"
        
        sentences=[Sentence('w_question', 'choice', 
                [Nominal_Group(['the'],['competition'],[],[Nominal_Group(['the'],['salesperson'],[],[],[])],[])], 
                [Verbal_Group(['win'], [],'past simple', 
                    [Nominal_Group(['the'],['award'],[],[],[Sentence('relative', 'which', 
                        [Nominal_Group([],['we'],[],[],[])], 
                        [Verbal_Group(['win'], [],'past simple', 
                            [], 
                            [Indirect_Complement(['in'],[Nominal_Group(['the'],['year'],[['last',[]]],[],[])])],
                            [], [] ,'affirmative',[])])])], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        sentences[0].sv[0].d_obj[0].relative[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="ALL"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_27(self):
        
        logger.info('\n######################## test 1.27 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="What will your house look like? What do you think of the latest novel which Jido wrote?"
        
        sentences=[Sentence('w_question', 'description', 
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
                            [], 
                            [],
                            [], [] ,'affirmative',[])])])], 
                [],
                [], [] ,'affirmative',[])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_28(self):
        
        logger.info('\n######################## test 1.28 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Learn that I want you to give me the blue bottle. You'll be happy, if you do your job."
        
        sentences=[Sentence('imperative', '', 
                [], 
                [Verbal_Group(['learn'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence', 'that', 
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
                        [], [] ,'affirmative',[Sentence('subsentence', 'if', 
                            [Nominal_Group([],['you'],[],[],[])], 
                            [Verbal_Group(['do'], [],'present simple', 
                                [Nominal_Group(['your'],['job'],[],[],[])], 
                                [],
                                [], [] ,'affirmative',[])])])])]

        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
       
   
    def test_29(self):
        logger.info('\n######################## test 1.29 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="You'll be happy, if you do your job. Do you want the blue or green bottle?"
        
        sentences=[Sentence('statement', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['be'], [],'future simple', 
                    [Nominal_Group([],[],[['happy',[]]],[],[])], 
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
                    [Nominal_Group(['the'],[],[['blue',[]]],[],[]),Nominal_Group([],['bottle'],[['green',[]]],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])]

        sentences[1].sv[0].d_obj[1]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_30(self):
        logger.info('\n######################## test 1.30 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="What's wrong with him? I'll play a guitar or a piano and a violon. I played a guitar a year ago."
        
        sentences=[Sentence('w_question', 'thing', 
                [Nominal_Group([],[],[['wrong',[]]],[],[])], 
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
        
        sentences[1].sv[0].d_obj[1]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
         
    def test_31(self):
        logger.info('\n######################## test 1.31 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Who are you talking to? You should have the bottle. Would you've played a guitar? You'd have played a guitar."
        
        sentences=[Sentence('w_question', 'people', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_32(self):
        logger.info('\n######################## test 1.32 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="What do you do for a living in this building? What does your brother do for a living here?"
        
        sentences=[Sentence('w_question', 'explication', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
        
    def test_33(self):
        logger.info('\n######################## test 1.33 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="This is a bottle. There is a bottle on the table."
        
        sentences=[Sentence('statement', '',
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)

    def test_34(self):
        logger.info('\n######################## test 1.34 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Is it on the table or the shelf?"
        
        sentences=[Sentence('yes_no_question', '',
                [Nominal_Group([],['it'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [],
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])]),
                     Indirect_Complement([],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        sentences[0].sv[0].i_cmpl[1].nominal_group[0]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)

    def test_35(self):
        
        logger.info('\n######################## test 1.35 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Where is it? On the table or on the shelf?"
     
        sentences=[Sentence('w_question', 'place',
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('yes_no_question', '', 
                [], 
                [Verbal_Group([], [],'', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])]),
                     Indirect_Complement(['on'],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        sentences[1].sv[0].i_cmpl[1].nominal_group[0]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_36(self):
        
        logger.info('\n######################## test 1.36 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Is it on your left or in front of you?"
        
        sentences=[Sentence('yes_no_question', '',
                [Nominal_Group([],['it'],[],[],[])],
                [Verbal_Group(['be'], [],'present simple',
                    [],
                    [Indirect_Complement(['on'],[Nominal_Group(['your'],['left'],[],[],[])]),
                     Indirect_Complement(['in+front+of'],[Nominal_Group([],['you'],[],[], [])])],
                    [], [] ,'affirmative',[])])]
        
        sentences[0].sv[0].i_cmpl[1].nominal_group[0]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_37(self):
        
        logger.info('\n######################## test 1.37 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Where is it? On your left or in front of you?"
        
        sentences=[Sentence('w_question', 'place',
                [Nominal_Group([],['it'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('yes_no_question', '',
                [Nominal_Group([],[],[],[],[])],
                [Verbal_Group([], [],'',
                    [],
                    [Indirect_Complement(['on'],[Nominal_Group(['your'],['left'],[],[],[])]),
                     Indirect_Complement(['in+front+of'],[Nominal_Group([],['you'],[],[], [])])],
                    [], [] ,'affirmative',[])])]
        
        sentences[1].sv[0].i_cmpl[1].nominal_group[0]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_38(self):
        
        logger.info('\n######################## test 1.38 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="The blue bottle? What do you mean?"
        
        sentences=[Sentence('yes_no_question', '', 
                        [Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[])], 
                        []),
                    Sentence('w_question', 'thing', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['mean'], [],'present simple', [], [], [], [] ,'affirmative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)    
   
    def test_39(self):
        
        logger.info('\n######################## test 1.39 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Would you like the blue bottle or the glass? The green or blue bottle is on the table. Is the green or blue glass mine?"
     
        sentences=[Sentence('yes_no_question', '', 
                [Nominal_Group([],['you'],[],[],[])], 
                [Verbal_Group(['like'], [],'present conditional', 
                    [Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[]),Nominal_Group(['the'],['glass'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])]),       
            Sentence('statement', '', 
                [Nominal_Group(['the'],[],[['green',[]]],[],[]),Nominal_Group([],['bottle'],[['blue',[]]],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                    [], [] ,'affirmative',[])]), 
            Sentence('yes_no_question', '', 
                [Nominal_Group(['the'],[],[['green',[]]],[],[]),Nominal_Group([],['glass'],[['blue',[]]],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],['mine'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        sentences[0].sv[0].d_obj[1]._conjunction="OR"
        sentences[1].sn[1]._conjunction="OR"
        sentences[2].sn[1]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_40(self):
        
        logger.info('\n######################## test 1.40 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Learn that I want you to give me the blue bottle that's blue."
        
        sentences=[Sentence('imperative', '', 
                [], 
                [Verbal_Group(['learn'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence', 'that', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_41(self):
        
        logger.info('\n######################## test 1.41 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="The bottle is behind to me. The bottle is next to the table in front of the kitchen."
        
        sentences=[Sentence('statement', '',
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_42(self):
        
        logger.info('\n######################## test 1.42 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Carefully take the bottle. I take that bottle that I drink in. I take 22 bottles."
        
        sentences=[Sentence('imperative', '', 
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
                            [Indirect_Complement(['in'],[])],
                            [], [] ,'affirmative',[])])])],
                    [],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])],  
                [Verbal_Group(['take'], [],'present simple', 
                    [Nominal_Group(['22'],['bottle'],[],[],[])],
                    [],
                    [], [] ,'affirmative',[])])]
        
        sentences[2].sv[0].d_obj[0]._quantifier="DIGIT"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)    
        
    
    def test_43(self):
        
        logger.info('\n######################## test 1.43 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="I'll play Jido's guitar, a saxophone, my oncle's wife's piano and Patrick's violon."
        
        sentences=[Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['play'], [],'future simple', 
                    [Nominal_Group(['the'],['guitar'],[],[Nominal_Group([],['Jido'],[],[],[])],[]),
                     Nominal_Group(['a'],['saxophone'],[],[],[]),
                     Nominal_Group(['a'],['piano'],[],[Nominal_Group(['the'],['wife'],[],[Nominal_Group(['my'],['oncle'],[],[],[])],[])],[]),
                     Nominal_Group(['the'],['violon'],[],[Nominal_Group([],['Patrick'],[],[],[])],[])], 
                    [],
                    [], [] ,'affirmative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_44(self):
        
        logger.info('\n######################## test 1.44 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Give me 2 or 3 bottles. The bottle is blue big funny. Give me the bottle which is on the table."
        
        sentences=[Sentence('imperative', '', 
                [], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['2'],[],[],[],[]),
                     Nominal_Group(['3'],['bottle'],[],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group(['the'],['bottle'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],[],[['blue',[]], ['big',[]], ['funny',[]]],[],[])], 
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
                
        sentences[0].sv[0].d_obj[1]._conjunction="OR"
        sentences[0].sv[0].d_obj[0]._quantifier="DIGIT"
        sentences[0].sv[0].d_obj[1]._quantifier="DIGIT"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_45(self):
        
        logger.info('\n######################## test 1.45 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="The boys' ball is blue. He asks me to do something. Is any person courageous on the laboratory?"
        
        sentences=[Sentence('statement', '', 
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
        
        
        sentences[0].sn[0].noun_cmpl[0]._quantifier="ALL"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)    
    
    def test_46(self):
        
        logger.info('\n######################## test 1.46 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="What must be happened in the company today? The building shouldn't fastly be built. You can be here."
        
        sentences=[Sentence('w_question', 'situation', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_47(self):
        
        logger.info('\n######################## test 1.47 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="What size is the best one? What object is blue? How good is this?"
        
        sentences=[Sentence('w_question', 'size', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)
    
    def test_48(self):
        
        logger.info('\n######################## test 1.48 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Patrick, the bottle is on the table. Give it to me."
        
        sentences=[Sentence('interjection', '', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)  
    
    def test_49(self):
        
        logger.info('\n######################## test 1.49 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Jido, give me the bottle. Jido, Patrick and you will go to the cinema. Jido, Patrick and you, give me the bottle."
        
        sentences=[Sentence('interjection', '', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)  
    
    def test_50(self):
        
        logger.info('\n######################## test 1.50 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="The bottle isn't blue but it's red. It isn't the glass but the bottle. It's blue or red."
        
        sentences=[Sentence('statement', '', 
                [Nominal_Group(['the'],['bottle'],[],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [Nominal_Group([],[],[['blue',[]]],[],[])], 
                    [],
                    [], [] ,'negative',[Sentence('subsentence', 'but', 
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
                
        sentences[1].sv[0].d_obj[1]._conjunction="BUT"
        sentences[2].sv[0].d_obj[1]._conjunction="OR"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance) 
       
    def test_51(self):
        
        logger.info('\n######################## test 1.51 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="It isn't red but blue. This is my banana. Bananas are fruits."
        
        sentences=[Sentence('statement', '', 
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
        
        sentences[0].sv[0].d_obj[1]._conjunction="BUT"
        sentences[2].sn[0]._quantifier="ALL"
        sentences[2].sv[0].d_obj[0]._quantifier="ALL"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)  
    
    def test_52(self):
        
        logger.info('\n######################## test 1.52 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="There are no bananas. All bananas are here. Give me more information which are about the bottle."
        
        sentences=[Sentence('statement', '', 
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
                    [Nominal_Group(['more'],['information'],[],[],[Sentence('relative', 'which', 
                        [], 
                        [Verbal_Group(['be'], [],'present simple', 
                            [], 
                            [Indirect_Complement(['about'],[Nominal_Group(['the'],['bottle'],[],[],[])])],
                            [], [] ,'affirmative',[])])])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        sentences[0].sn[0]._quantifier="SOME"
        sentences[0].sv[0].d_obj[0]._quantifier="ANY"
        sentences[1].sn[0]._quantifier="ALL"
        sentences[2].sv[0].d_obj[0]._quantifier="SOME"
    
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)  
    
    def test_53(self):
        
        logger.info('\n######################## test 1.53 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Jido, tell me where you go. Goodbye. There is nothing. It's another one."
        
        sentences=[Sentence('interjection', '', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance) 
    
    
    def test_54(self):
        
        logger.info('\n######################## test 1.54 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="The bottle becomes blue. 1 piece could become 2, if you smoldered it."
        
        sentences=[Sentence('statement', '', 
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
                    [], [] ,'affirmative',[Sentence('subsentence', 'if', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['smolder'], [],'past simple', 
                            [Nominal_Group([],['it'],[],[],[])], 
                            [],
                            [], [] ,'affirmative',[])])])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance) 
        
    def test_55(self):
        
        logger.info('\n######################## test 1.55 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="This one isn't my uncle's bottle but it's my brother's bottle. It isn't on the table but on the shelf."
        
        sentences=[Sentence('statement', '', 
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
                    [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[]),Nominal_Group(['the'],['shelf'],[],[],[])])],
                    [], [] ,'negative',[])])]
        
        sentences[1].sv[0].i_cmpl[0].nominal_group[1]._conjunction="BUT"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)        
        
    def test_56(self):
        
        logger.info('\n######################## test 1.56 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Give me the fourth and seventh bottle. Give me the one thousand ninth and the thirty thousand twenty eighth bottle."
        
        sentences=[Sentence('imperative', '', 
                [], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['the'],[],[['fourth',[]]],[],[]),
                     Nominal_Group([],['bottle'],[['seventh',[]]],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('imperative', '', 
                [], 
                [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group(['the'],[],[['one+thousand+ninth',[]]],[],[]),
                     Nominal_Group(['the'],['bottle'],[['thirty+thousand+twenty+eighth',[]]],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])])],
                    [], [] ,'affirmative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)       
    
    def test_57(self):
        
        logger.info('\n######################## test 1.57 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="The evil tyrant is in the laboratory. I don't know what you're talking about."
        
        sentences=[Sentence('statement', '', 
                [Nominal_Group(['the'],['tyrant'],[['evil',[]]],[],[])], 
                [Verbal_Group(['be'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['in'],[Nominal_Group(['the'],['laboratory'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['know'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'negative',[Sentence('subsentence', 'what', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['talk'], [],'present progressive', 
                            [], 
                            [Indirect_Complement(['about'],[])],
                            [], [] ,'affirmative',[])])])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance) 
    
    
    def test_58(self):
        
        logger.info('\n######################## test 1.58 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="I go to the place where I was born. I study where you studied. I study where you build your house where you put the bottle."
        
        sentences=[Sentence('statement', '', 
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
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence', 'where', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['study'], [],'past simple', 
                            [], 
                            [],
                            [], [] ,'affirmative',[])])])]),
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['study'], [],'present simple', 
                    [], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence', 'where', 
                        [Nominal_Group([],['you'],[],[],[])], 
                        [Verbal_Group(['build'], [],'present simple', 
                            [Nominal_Group(['your'],['house'],[],[],[Sentence('relative', 'where', 
                                [Nominal_Group([],['you'],[],[],[])], 
                                [Verbal_Group(['put'], [],'present simple', 
                                    [Nominal_Group(['the'],['bottle'],[],[],[])], 
                                    [],
                                    [], [] ,'affirmative',[])])])], 
                            [],
                            [], [] ,'affirmative',[])])])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance) 
    
    def test_59(self):
        
        logger.info('\n######################## test 1.59 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Apples grow on trees and plants. Give me 3 apples."
        
        sentences=[Sentence('statement', '', 
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
        
        sentences[0].sn[0]._quantifier="ALL"
        sentences[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="ALL"
        sentences[0].sv[0].i_cmpl[0].nominal_group[1]._quantifier="ALL"
        sentences[1].sv[0].d_obj[0]._quantifier="DIGIT"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)        
    
    def test_60(self):
        
        logger.info('\n######################## test 1.56 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="We were preparing the dinner when your father came. He made a sandwich which is with bacon, while I phoned."
        
        sentences=[Sentence('statement', '', 
                [Nominal_Group([],['we'],[],[],[])], 
                [Verbal_Group(['prepare'], [],'past progressive', 
                    [Nominal_Group(['the'],['dinner'],[],[],[])], 
                    [],
                    [], [] ,'affirmative',[Sentence('subsentence', 'when', 
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
                    [], [] ,'affirmative',[Sentence('subsentence', 'while', 
                        [Nominal_Group([],['I'],[],[],[])], 
                        [Verbal_Group(['phone'], [],'past simple', 
                             [], 
                             [],
                             [], [] ,'affirmative',[])])])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)             
     
    def test_61(self):
        
        logger.info('\n######################## test 1.54 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="The big very strong man is on the corner. The too big very strong man is on the corner."
        
        sentences=[Sentence('statement', '', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance) 
    
    def test_62(self):
        
        logger.info('\n######################## test 1.55 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Red apples grow on green trees and plants. A kind of thing. It can be played by 30028 players."
        
        sentences=[Sentence('statement', '', 
                [Nominal_Group([],['apple'],[['red',[]]],[],[])], 
                [Verbal_Group(['grow'], [],'present simple', 
                    [], 
                    [Indirect_Complement(['on'],[Nominal_Group([],['tree'],[['green',[]]],[],[]),Nominal_Group([],['plant'],[],[],[])])],
                    [], [] ,'affirmative',[])]),
            Sentence('statement', '', 
                    [Nominal_Group(['a'],['kind'],[],[Nominal_Group(['a'],['thing'],[],[],[])],[])], 
                    []),
            Sentence('statement', '', 
                        [Nominal_Group([],['it'],[],[],[])],  
                        [Verbal_Group(['can+play'],[],'present passive', 
                            [], 
                            [Indirect_Complement(['by'],[Nominal_Group(['30028'],['player'],[],[],[])])],
                            [], [] ,'affirmative',[])])]
        
        sentences[0].sn[0]._quantifier="ALL"
        sentences[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="ALL"
        sentences[0].sv[0].i_cmpl[0].nominal_group[1]._quantifier="ALL"
        sentences[1].sn[0]._quantifier="SOME"
        sentences[1].sn[0].noun_cmpl[0]._quantifier="SOME"
        sentences[2].sv[0].i_cmpl[0].nominal_group[0]._quantifier="DIGIT"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)        
        
    def test_63(self):
        
        logger.info('\n######################## test 1.56 ##############################')
        logger.info('#################################################################\n')
        
        original_utterance="Let the man go to the cinema. Is it the time to let you go? Where is the other tape?"
        
        sentences=[Sentence('imperative', '', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        logger.info("The original utterance is : " + original_utterance)
        logger.info("The result obtained is :    " + utterance)
        
        self.assertEquals(original_utterance, utterance)

    def test_64(self):
        
        print ''
        print '######################## test 1.57 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="And now, can you reach the tape. it could have been them. It is just me at the door. A strong clause can stand on its own."
        
        sentences=[Sentence('yes_no_question', '', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)

    def test_65(self):
        
        print ''
        print '######################## test 1.58 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="tell me what to do. No, I can not reach it."
        
        sentences=[Sentence('imperative', '', 
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
            Sentence('disagree', '',[],[]), 
            Sentence('statement', '', 
                [Nominal_Group([],['I'],[],[],[])], 
                [Verbal_Group(['can+reach'], [],'present simple', 
                    [Nominal_Group([],['it'],[],[],[])], 
                    [],
                    [], [] ,'negative',[])])]
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_66(self):
        
        print ''
        print '######################## test 1.59 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="I'll come back on Monday. I'll play with guitar. I'll play football"
        
        sentences=[Sentence('statement', '', 
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
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_67(self):
        
        print ''
        print '######################## test 1.60 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="I'll play a guitar, a piano and a violon. I'll play with a guitar, a piano and a violon. Give me everything."
        
        sentences=[Sentence('statement', '', 
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
        
        sentences[0].sv[0].d_obj[0]._quantifier="SOME"
        sentences[0].sv[0].d_obj[1]._quantifier="SOME"
        sentences[0].sv[0].d_obj[2]._quantifier="SOME"
        sentences[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
        sentences[1].sv[0].i_cmpl[0].nominal_group[1]._quantifier="SOME"
        sentences[1].sv[0].i_cmpl[0].nominal_group[2]._quantifier="SOME"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
          
    def test_68(self):
        
        print ''
        print '######################## test 1.61 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="I'll come back at 7 o'clock tomorrow. He finishes the project 10 minutes before."
        
        sentences=[Sentence('statement', '', 
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
        
        sentences[0].sv[0].i_cmpl[0].nominal_group[0]._quantifier="DIGIT"
        sentences[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="DIGIT"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)

    def test_69(self):
        
        print ''
        print '######################## test 1.62 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="I'll play a guitar, a piano and a violon. I'll play with a guitar, a piano and a violon. The boss, you and me are here."
        
        sentences=[Sentence('statement', '', 
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
        
        sentences[0].sv[0].d_obj[0]._quantifier="SOME"
        sentences[0].sv[0].d_obj[1]._quantifier="SOME"
        sentences[0].sv[0].d_obj[2]._quantifier="SOME"
        sentences[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
        sentences[1].sv[0].i_cmpl[0].nominal_group[1]._quantifier="SOME"
        sentences[1].sv[0].i_cmpl[0].nominal_group[2]._quantifier="SOME"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
        
    def test_70(self):
        
        print ''
        print '######################## test 1.63 ##############################'
        print '#################################################################'
        print ''
        
        original_utterance="A speaking sentence's time is the best. I come at 10 pm. I'll come an evening tomorrow."
        
        sentences=[Sentence('statement', '', 
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
                    [Indirect_Complement([],[Nominal_Group(['an'],['evening'],[],[],[])])],
                    [], ['tomorrow'] ,'affirmative',[])])]
        
        sentences[0].sn[0].noun_cmpl[0]._quantifier='SOME'
        sentences[1].sv[0].i_cmpl[0].nominal_group[0]._quantifier="DIGIT"
        sentences[2].sv[0].i_cmpl[0].nominal_group[0]._quantifier="SOME"
        
        utterance=utterance_rebuilding.verbalising(sentences)
        
        print "The original utterance is : ", original_utterance
        print "The result obtained is :    ", utterance
        
        self.assertEquals(original_utterance, utterance)
    


        
class TestVerbalizationCompleteLoop(unittest.TestCase):
        
    def setUp(self):
            self.dialog = Dialog()
            self.dialog.start()
        
    def tearDown(self):
            self.dialog.stop()
            self.dialog.join()
        
    def test_verbalize1(self):
           
        logger.info("\n##################### test_verbalize1: simple statements ########################\n")
        myP = Parser()                            
        stmt = "The cup is on the desk."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)
        
        logger.info("\n####\n")
        
        stmt = "The green bottle is next to Joe."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)

    def test_verbalize2(self):
        
        logger.info("\n##################### test_verbalize2: yes/no questions ########################\n")
        myP = Parser()

        stmt = "Are you a robot?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)


    def test_verbalize3(self):
        
        logger.info("\n##################### test_verbalize3: orders ########################\n")
        myP = Parser()

        stmt = "Put the yellow banana on the shelf."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)
        
        logger.info("\n####\n")
        
        stmt = "Give me the green banana."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)
        
        logger.info("\n####\n")
        
        stmt = "Give the green banana to me."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)

        logger.info("\n####\n")
        
        stmt = "Get the box which is on the table."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)
        
        logger.info("\n####\n")

        stmt = "Get the box which is in the trashbin."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)

    def test_verbalize4(self):
        
        logger.info("\n##################### test_verbalize4: W questions ########################\n")
        myP = Parser()
        
        stmt = "Where is the box?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)
        
        logger.info("\n####\n")
        
        stmt = "What are you doing now?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('input: ' + stmt)
        logger.info('output:' + res)
        self.assertEquals(stmt, res)


    def test_verbalize5(self):
        
        logger.info("\n##################### test_verbalize5 ########################\n")
        myP = Parser()
        
        stmt = "Jido, tell me where you go."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)
        
    def test_verbalize6(self):
        
        logger.info("\n##################### test_verbalize 6 ########################\n")
        myP = Parser()
        
        stmt = "What blue object do you know?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        logger.info('>> input: ' + stmt)
        logger.info('<< output: ' + res)
        self.assertEquals(stmt, res)
        
def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestVerbalization)
    suite.addTests( unittest.TestLoader().loadTestsFromTestCase(TestVerbalizationCompleteLoop))
    
    return suite
    
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite())

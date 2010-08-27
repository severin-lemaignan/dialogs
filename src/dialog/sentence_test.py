#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger("dialog")
import unittest

from dialog.sentence import *
from parsing import preprocessing
from parsing import analyse_sentence
from parsing import parser

from parsing.parser_test import compare_nom_gr

class TestSentence(unittest.TestCase):
    def test_sentence(self):
        """Tests the creation of several type of Sentence objects.
        """

        sentence1 = Sentence('w_question',
                            'location',
                            [Nominal_Group(['the'],  ['mother'],[],[], [])],
                            [Verbal_Group(['be'], [],'present simple',[], [],['today'], [], [], [])])
        
        logger.info("*********************************")
        logger.info(sentence1)
        
        sentence2 = Sentence('statement', 
                            '', 
                            [Nominal_Group([],["Jido"],[],[],[]), Nominal_Group([],["Danny"],[],[],[])], 
                            [Verbal_Group(["want"],[], 'infinitive',[],[],[],[],'affirmative', [])])
        
        logger.info("*********************************")
        logger.info(sentence2)
        
        sentence3 = Sentence('statement', 
                            '', 
                            [Nominal_Group([],["Holmes"],[],[],[]), Nominal_Group([],["Sherlock"],[],[],[])], 
                            [Verbal_Group(["want"],
                                        [Verbal_Group(["eat"],[], 'infinitive',[],[],[],[],'affirmative', [])], 
                                        'past simple',
                                        [],
                                        [],
                                        [],
                                        [],
                                        'negative', 
                                        [])])
        
        logger.info("*********************************")
        logger.info(sentence3)
        
        sentence4 = Sentence('statement',
                            '',
                            [Nominal_Group( ['the'],  
                                            ['bottle'],
                                            ['blue', 'gray'],
                                            [Nominal_Group(['my'],  ['mother'],[],[], [sentence2]), Nominal_Group(['my'],  ['father'],[],[], [])], 
                                            [])], 
                            [Verbal_Group(['know'], 
                                        [],
                                        'present simple',
                                        [Nominal_Group(['the'],  ["land"],['old'],[], []), Nominal_Group(['the'],  ["brand"],['lazy'],[], [])],
                                        [
                                            Indirect_Complement(['in'], 
                                                                [Nominal_Group(['the'],  ['garden'],['green'],[], [])]), 
                                            Indirect_Complement(['to'], 
                                                                [Nominal_Group(['the'],  ['car'],['red'],[], [])])
                                        ],
                                        ["slowly"], 
                                        ["now"], 
                                        "affirmative", 
                                        [sentence3])])
        logger.info("*********************************")
        logger.info(sentence4)
        
        
        
        sentence4bis = Sentence('statement',
                            '',
                            [Nominal_Group( ['the'],  
                                            ['bottle'],
                                            ['blue', 'gray'],
                                            [Nominal_Group(['my'],  ['mother'],[],[], [sentence2]), Nominal_Group(['my'],  ['father'],[],[], [])], 
                                            [])], 
                            [Verbal_Group(['know'], 
                                        [],
                                        'present simple',
                                        [Nominal_Group(['the'],  ["land"],['old'],[], []), Nominal_Group(['the'],  ["brand"],['lazy'],[], [])],
                                        [
                                            Indirect_Complement(['in'], 
                                                                [Nominal_Group(['the'],  ['garden'],['green'],[], [])]), 
                                            Indirect_Complement(['to'], 
                                                                [Nominal_Group(['the'],  ['car'],['red'],[], [])])
                                        ],
                                        ["slowly"], 
                                        ["now"], 
                                        "affirmative", 
                                        [sentence3])])
        logger.info("*********************************")
        logger.info(sentence4bis)
        
        
        logger.info("*************  Sentence Comparison ****************")
        
        cmp = Comparator()    
        logger.info("sentence4 == sentence4bis: " + str(cmp.compare(sentence4, sentence4bis)))
        logger.info("sentence3 == sentence4: " + str(cmp.compare(sentence3, sentence4)))
        
        logger.info("*************  Nominal group adjective only ****************")
        logger.info("Nominal_Group(['the'],['man'],[],[],[]) is adjective only: " + str(Nominal_Group(['the'],['man'],[],[],[]).adjectives_only()))
        logger.info("Nominal_Group([],[],['blue'],[],[]) is adjective only: " + str(Nominal_Group([],[],['blue'],[],[]).adjectives_only()))
        

class TestRemerge(unittest.TestCase):
    """
    Function to perform unit tests                                                   
    """ 
    
    def test_01(self):
        logger.info('\n######################## test 1.1 ##############################')
    
        utterance="sorry"
        logger.info('It is an empty test with SUCCESS')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')

        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
    
    def test_02(self):

        logger.info('\n######################## test 1.2 ##############################')
    
        utterance="sorry"
        logger.info('It is an empty test with FAILURE')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')

        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        

    def test_03(self):
        logger.info('\n######################## test 1.3 ##############################')
    
        utterance="the too blue one"
        logger.info('Add adjectives if we have SUCCESS')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[['big',['very']]],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['big',['very']],['blue',['too']]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_04(self):
        logger.info('\n######################## test 1.4 ##############################')
    
        utterance="the blue one. I mean"
        logger.info('Add adjectives if we have FAILURE')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_05(self):
        logger.info('\n######################## test 1.5 ##############################')
    
        utterance="it is on the table"
        logger.info('Add adverbial as a relative this case is only for SUCCESS')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_06(self):    
        logger.info('\n######################## test 1.6 ##############################')
    
        utterance="the bottle on the table"
        logger.info('Add adverbial as a relative this case is only for SUCCESS')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
    
    def test_07(self):
        logger.info('\n######################## test 1.7 ##############################')
    
        utterance="I'm talking about the green bottle"
        logger.info('Correct adjective this case is only for FAILURE')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['green',[]]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
    
    def test_08(self):    
        logger.info('\n######################## test 1.8 ##############################')
    
        utterance="sorry. I mean the green one"
        logger.info('Correct adjective this case is only for FAILURE')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['green',[]]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_09(self):
        logger.info('\n######################## test 1.9 ##############################')
    
        utterance="sorry. I want to say the too dark one"
        logger.info('Correct adjective this case is only for FAILURE')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['dark',['too']]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
    
    def test_10(self):
        logger.info('\n######################## test 1.10 ##############################')
    
        utterance="sorry. I want to say this plush"
        logger.info('Correct noun this case is only for FAILURE')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bear'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['this'],['plush'],[],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_11(self):
        logger.info('\n######################## test 1.11 ##############################')
    
        utterance="No. He means the one which he bought yesterday."
        logger.info('Add relative if we have FAILURE')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [Nominal_Group([],['he'],[],[],[])],  
                        [Verbal_Group(['buy'], [],'past simple', 
                            [Nominal_Group(['the'],['bottle'],[],[],[])],
                            [],
                            [], ['yesterday'] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_12(self):    
        logger.info('\n######################## test 1.12 ##############################')
    
        utterance="No. He means the one which he bought yesterday."
        logger.info('Add relative if we have SUCCESS')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [Nominal_Group([],['he'],[],[],[])],  
                        [Verbal_Group(['buy'], [],'past simple', 
                            [Nominal_Group(['the'],['bottle'],[],[],[])],
                            [],
                            [], ['yesterday'] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_13(self):    
        logger.info('\n######################## test 1.13 ##############################')
    
        utterance="I mean the bottle of Jido"
        logger.info('Add noun complement if we have SUCCESS')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[Nominal_Group([],['Jido'],[],[],[])],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_14(self):    
        logger.info('\n######################## test 1.14 ##############################')
    
        utterance="I mean the bottle of Jido"
        logger.info('Add noun complement if we have FAILURE')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[Nominal_Group([],['Jido'],[],[],[])],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
    
    def test_15(self):
        logger.info('\n######################## test 1.15 ##############################')
    
        utterance="Sorry. it is the best one"
        logger.info('Case of SUCCESS used with FAILURE')
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['best',[]]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_16(self):
        logger.info('\n######################## test 1.16 ##############################')
    
        utterance="He means that he want the bottle of Jido"
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[Nominal_Group([],['Jido'],[],[],[])],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)

    def test_17(self):
        logger.info('\n######################## test 1.17 ##############################')
    
        utterance="no. The bottle is not blue. It is red"
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['red',[]]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)

    def test_18(self):
        logger.info('\n######################## test 1.18 ##############################')
    
        utterance="no. The bottle is not on the table. It is on the shelf."
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_19(self):    
        logger.info('\n######################## test 1.19 ##############################')
    
        utterance="no. The bottle is not on the table. It is on the shelf."
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)    
        
    def test_20(self):    
        logger.info('\n######################## test 1.20 ##############################')
    
        utterance="no. it is not blue but red."
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['red',[]]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_21(self):
        logger.info('\n######################## test 1.21 ##############################')
    
        utterance="This one is not mine but it is the bottle of my brother."
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[Nominal_Group(['my'],['brother'],[],[],[])],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_22(self):
        logger.info('\n######################## test 1.22 ##############################')
    
        utterance="This one is not the bottle of my uncle but it is the bottle of my brother."
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[Nominal_Group(['my'],['uncle'],[],[],[])],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[Nominal_Group(['my'],['brother'],[],[],[])],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
    
    def test_23(self):
        logger.info('\n######################## test 1.23 ##############################')
    
        utterance="no. It is not on the table but on the shelf."
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)

    def test_24(self):
        logger.info('\n######################## test 1.24 ##############################')
    
        utterance="no. It is not on the table but on the shelf."
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0) 
        
    def test_25(self):
        logger.info('\n######################## test 1.25 ##############################')
    
        utterance="no. I mean the bottle."
        logger.info('The speaker said :')
        logger.info(utterance)
        logger.info('#################################################################\n')
        
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group([],['it'],[],[],[])
        logger.info('the nominal group of the last out put')
        logger.info(str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        logger.info('the nominal group after processing')
        logger.info(str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSentence)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestRemerge))
    
    return suite
    
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite())

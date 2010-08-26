#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
 Created by Chouayakh Mahdi                                                       
 23/07/2010                                                                       
 The package contains the unit test of remerge function                                       
    unit_tests : to perform unit tests                                           
"""
import logging
logging.basicConfig(level=logging.DEBUG, format="%(message)s")
import unittest

from dialog.sentence import *
import preprocessing
import analyse_sentence
import parser

from parser_test import compare_nom_gr


class TestRemerge(unittest.TestCase):
    """
    Function to perform unit tests                                                   
    """ 
    
    def test_01(self):
        print ''
        print ('######################## test 1.1 ##############################')
    
        utterance="sorry"
        print 'It is an empty test with SUCCESS'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
    
    def test_02(self):
        print ''
        print ('######################## test 1.2 ##############################')
    
        utterance="sorry"
        print 'It is an empty test with FAILURE'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        

    def test_03(self):
        print ''
        print ('######################## test 1.3 ##############################')
    
        utterance="the too blue one"
        print 'Add adjectives if we have SUCCESS'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[['big',['very']]],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['big',['very']],['blue',['too']]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_04(self):
        print ''
        print ('######################## test 1.4 ##############################')
    
        utterance="the blue one. I mean"
        print 'Add adjectives if we have FAILURE'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_05(self):
        print ''
        print ('######################## test 1.5 ##############################')
    
        utterance="it is on the table"
        print 'Add adverbial as a relative this case is only for SUCCESS'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_06(self):    
        print ''
        print ('######################## test 1.6 ##############################')
    
        utterance="the bottle on the table"
        print 'Add adverbial as a relative this case is only for SUCCESS'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
    
    def test_07(self):
        print ''
        print ('######################## test 1.7 ##############################')
    
        utterance="I'm talking about the green bottle"
        print 'Correct adjective this case is only for FAILURE'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['green',[]]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
    
    def test_08(self):    
        print ''
        print ('######################## test 1.8 ##############################')
    
        utterance="sorry. I mean the green one"
        print 'Correct adjective this case is only for FAILURE'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['green',[]]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_09(self):
        print ''
        print ('######################## test 1.9 ##############################')
    
        utterance="sorry. I want to say the too dark one"
        print 'Correct adjective this case is only for FAILURE'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['dark',['too']]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
    
    def test_10(self):
        print ''
        print ('######################## test 1.10 ##############################')
    
        utterance="sorry. I want to say this plush"
        print 'Correct noun this case is only for FAILURE'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bear'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['this'],['plush'],[],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_11(self):
        print ''
        print ('######################## test 1.11 ##############################')
    
        utterance="No. He means the one which he bought yesterday."
        print 'Add relative if we have FAILURE'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [Nominal_Group([],['he'],[],[],[])],  
                        [Verbal_Group(['buy'], [],'past simple', 
                            [Nominal_Group(['the'],['bottle'],[],[],[])],
                            [],
                            [], ['yesterday'] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_12(self):    
        print ''
        print ('######################## test 1.12 ##############################')
    
        utterance="No. He means the one which he bought yesterday."
        print 'Add relative if we have SUCCESS'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [Nominal_Group([],['he'],[],[],[])],  
                        [Verbal_Group(['buy'], [],'past simple', 
                            [Nominal_Group(['the'],['bottle'],[],[],[])],
                            [],
                            [], ['yesterday'] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_13(self):    
        print ''
        print ('######################## test 1.13 ##############################')
    
        utterance="I mean the bottle of Jido"
        print 'Add noun complement if we have SUCCESS'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[Nominal_Group([],['Jido'],[],[],[])],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_14(self):    
        print ''
        print ('######################## test 1.14 ##############################')
    
        utterance="I mean the bottle of Jido"
        print 'Add noun complement if we have FAILURE'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[Nominal_Group([],['Jido'],[],[],[])],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
    
    def test_15(self):
        print ''
        print ('######################## test 1.15 ##############################')
    
        utterance="Sorry. it is the best one"
        print 'Case of SUCCESS used with FAILURE'
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['best',[]]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_16(self):
        print ''
        print ('######################## test 1.16 ##############################')
    
        utterance="He means that he want the bottle of Jido"
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[Nominal_Group([],['Jido'],[],[],[])],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)

    def test_17(self):
        print ''
        print ('######################## test 1.17 ##############################')
    
        utterance="no. The bottle is not blue. It is red"
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['red',[]]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)

    def test_18(self):
        print ''
        print ('######################## test 1.18 ##############################')
    
        utterance="no. The bottle is not on the table. It is on the shelf."
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_19(self):    
        print ''
        print ('######################## test 1.19 ##############################')
    
        utterance="no. The bottle is not on the table. It is on the shelf."
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)    
        
    def test_20(self):    
        print ''
        print ('######################## test 1.20 ##############################')
    
        utterance="no. it is not blue but red."
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[['blue',[]]],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[['red',[]]],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_21(self):
        print ''
        print ('######################## test 1.21 ##############################')
    
        utterance="This one is not mine but it is the bottle of my brother."
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='FAILURE'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[Nominal_Group(['my'],['brother'],[],[],[])],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
    def test_22(self):
        print ''
        print ('######################## test 1.22 ##############################')
    
        utterance="This one is not the bottle of my uncle but it is the bottle of my brother."
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[Nominal_Group(['my'],['uncle'],[],[],[])],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[Nominal_Group(['my'],['brother'],[],[],[])],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
    
    def test_23(self):
        print ''
        print ('######################## test 1.23 ##############################')
    
        utterance="no. It is not on the table but on the shelf."
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)

    def test_24(self):
        print ''
        print ('######################## test 1.24 ##############################')
    
        utterance="no. It is not on the table but on the shelf."
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[Sentence('relative', 'which', 
                        [],  
                        [Verbal_Group(['be'],[],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                            [], [] ,'affirmative',[])])])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0) 
        
    def test_25(self):
        print ''
        print ('######################## test 1.25 ##############################')
    
        utterance="no. I mean the bottle."
        print 'The speaker said :'
        print utterance
        print '#################################################################'
        print ''
        sentence_list=preprocessing.process_sentence(utterance)
        class_list=analyse_sentence.sentences_analyzer(sentence_list)
        flag='SUCCESS'
        
        nom_gr_struc=Nominal_Group([],['it'],[],[],[])
        print 'the nominal group of the last out put'
        print (str(nom_gr_struc))
        
        nom_gr_struc=nom_gr_remerge(class_list, flag , nom_gr_struc)
        print 'the nominal group after processing'
        print (str(nom_gr_struc))
        
        rslt=Nominal_Group(['the'],['bottle'],[],[],[])
        
        result_test=compare_nom_gr([nom_gr_struc],[rslt])
        self.assertEquals(result_test, 0)
        
def test_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestRemerge)
    
if __name__ == '__main__':
    
    unittest.TextTestRunner(verbosity=2).run(test_suite())

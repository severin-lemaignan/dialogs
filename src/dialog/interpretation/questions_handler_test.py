#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger("dialog")

import unittest

from dialog.resources_manager import ResourcePool
from dialog.dialog_core import Dialog
from dialog.interpretation.questions_handler import QuestionHandler
from dialog.sentence import SentenceFactory, Sentence
from dialog.interpretation.statements_builder import *
from dialog.interpretation.resolution import Resolver
from dialog.interpretation.statements_builder_test import check_results

class TestQuestionHandler(unittest.TestCase):
    def setUp(self):
        try:
            ResourcePool().ontology_server.reset()
            
            ResourcePool().ontology_server.add(['SPEAKER rdf:type Human', 'SPEAKER rdfs:label "Patrick"',
                     'blue_cube rdf:type Cube',
                     'blue_cube hasColor blue',
                     'blue_cube isOn table1',
                     
                     'another_cube rdf:type Cube',
                     'another_cube isAt shelf1',
                     'another_cube belongsTo SPEAKER',
                     'another_cube hasSize small',
                     
                     'shelf1 rdf:type Shelf',
                     'table1 rdf:type Table',
                     
                     'myself sees shelf1',
                     
                     'take_blue_cube performedBy myself',
                     'take_blue_cube rdf:type Get',
                     'take_blue_cube actsOnObject blue_cube',
                     
                     'take_my_cube canBePerformedBy SPEAKER',
                     'take_my_cube involves another_cube',
                     'take_my_cube rdf:type Take',
                     
                     'SPEAKER focusesOn another_cube',
                     
                     'id_danny rdfs:label "Danny"',
                     
                     'give_another_cube rdf:type Give',
                     'give_another_cube performedBy id_danny',
                     'give_another_cube receivedBy SPEAKER',
                     'give_another_cube actsOnObject another_cube',
                     
                     'id_danny sees SPEAKER',
                     ])
        except AttributeError: #the ontology server is not started or doesn't know the method
            pass
        
        try:
            ResourcePool().ontology_server.addForAgent('SPEAKER',
                    [
                     'SPEAKER rdfs:label "Patrick"',
                     'blue_cube rdf:type Cube',
                     'blue_cube hasColor blue',
                     'blue_cube isOn table1',
                     
                     'another_cube rdf:type Cube',
                     'another_cube isAt shelf1',
                     'another_cube belongsTo SPEAKER',
                     'another_cube hasSize small',
                     
                     'shelf1 rdf:type Shelf',
                     'table1 rdf:type Table',
                     
                     'myself sees shelf1',
                     
                     'take_blue_cube performedBy myself',
                     'take_blue_cube rdf:type Get',
                     'take_blue_cube actsOnObject blue_cube',
                     
                     'take_my_cube canBePerformedBy SPEAKER',
                     'take_my_cube involves another_cube',
                     'take_my_cube rdf:type Take',
                     
                     'SPEAKER focusesOn another_cube',
                     
                     'id_danny rdfs:label "Danny"',
                     
                     'give_another_cube rdf:type Give',
                     'give_another_cube performedBy id_danny',
                     'give_another_cube receivedBy SPEAKER',
                     'give_another_cube actsOnObject another_cube',
                     
                     'id_danny sees SPEAKER',
                     ])
        except AttributeError: #the ontology server is not started or doesn't know the method
            pass
        
        self.qhandler = QuestionHandler("SPEAKER")
        self.resolver = Resolver()
    """
    def test_1_where_question(self):
        logger.info("\n*************  test_1_where_question ******************")
        logger.info("Where is the blue cube?")
        sentence = Sentence("w_question", "place", 
                             [Nominal_Group(['the'],
                                            ['cube'],
                                            [['blue',[]]],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present_simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])]) 
        expected_result = 'table1'
        self.process(sentence ,expected_result)

    def test_2_where_question(self):
        logger.info("\n*************  test_2_where_question ******************")
        logger.info("Where is the small cube?")
        sentence = Sentence("w_question", "place", 
                             [Nominal_Group(['the'],
                                            ['cube'],
                                            [['small',[]]],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present_simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = 'shelf1'
        
        self.process(sentence ,expected_result)
    
    
    def test_3_what_question(self):
        logger.info("\n*************  test_3_what_question ******************")
        logger.info("What do you see?")
        sentence = Sentence("w_question", "thing", 
                             [Nominal_Group([],
                                            ['you'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['see'],
                                           [],
                                           'present_simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = 'shelf1'
        
        self.process(sentence ,expected_result)
    
    def test_8_what_question(self):
        logger.info("\n*************  test_8_what_question ******************")
        logger.info("what is blue?")
        sentence = Sentence("w_question", "thing", 
                             [],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                          [],
                                                          [['blue',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = 'blue_cube'        
        self.process(sentence ,expected_result) 
    
    def test_9_what_question_this(self):
        logger.info("\n*************  test_9_what_question_this ******************")
        logger.info("what is this?")
        sentence = Sentence("w_question", "thing", 
                             [Nominal_Group(['this'],
                                            [],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = 'another_cube'
        self.process(sentence ,expected_result) 
    
    def test_10_what_question(self):
        logger.info("\n*************  test_10_w_question ******************")
        logger.info("what object is blue?")
        sentence = Sentence("w_question", "object", 
                             [],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                          [],
                                                          [['blue',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = 'blue_cube'
        self.process(sentence ,expected_result)
    
    def test_11_what_question(self):
        logger.info("\n*************  test_11_w_question ******************")
        logger.info("what size is this?")
        sentence = Sentence("w_question", "size", 
                             [Nominal_Group(['this'],
                                            [],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = 'small'
        self.process(sentence ,expected_result)
    
    def test_12_what_question(self):
        logger.info("\n*************  test_12_what_question ******************")
        logger.info("what color is the blue_cube?")
        sentence = Sentence("w_question", "color", 
                             [Nominal_Group(['the'],
                                            ['blue_cube'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = 'blue'
        self.process(sentence ,expected_result)
    
    def test_13_who_question(self):
        logger.info("\n*************  test_13_who_question ******************")
        logger.info("who is the SPEAKER?")
        sentence = Sentence("w_question", "people", 
                             [Nominal_Group(['the'],
                                            ['SPEAKER'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = 'SPEAKER'
        self.process(sentence ,expected_result)
    
    def test_14_who_question(self):
        logger.info("\n*************  test_14_who_question ******************")
        logger.info("who sees Patrick?")
        sentence = Sentence("w_question", "people", 
                             [],                                         
                             [Verbal_Group(['see'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                          ['Patrick'],
                                                          [],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = 'id_danny'
        
        self.process(sentence ,expected_result)
    
    
    def test_15_who_question(self):
        logger.info("\n*************  test_15_who_question ******************")
        logger.info("who does Danny give the small cube?")
        sentence = Sentence("w_question", "people", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['give'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['the'],
                                                          ['cube'],
                                                          [['small',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = 'SPEAKER'
        self.process(sentence ,expected_result)
    
    
    def test_4_y_n_question(self):
        logger.info("\n*************  test_4_y_n_question action verb******************")
        logger.info("Did you get the blue cube?")
        sentence = Sentence("yes_no_question", "", 
                             [Nominal_Group([],
                                            ['you'],
                                            [''],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['get'],
                                           [],
                                           'past simple',
                                           [Nominal_Group(['the'],
                                                          ['cube'],
                                                          [['blue',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = True        
        self.process(sentence ,expected_result)
        
    
    def test_5_y_n_question(self):
        logger.info("\n*************  test_5_y_n_question verb to be followed by complement******************")
        logger.info("Is the blue cube on the table1?")
        sentence = Sentence("yes_no_question", "", 
                             [Nominal_Group(['the'],
                                            ['cube'],
                                            [['blue',[]]],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [Indirect_Complement(['on'],
                                                                [Nominal_Group(['the'],
                                                                               ['table1'],
                                                                               [],
                                                                               [],
                                                                               [])])],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = True        
        self.process(sentence ,expected_result)
    
    
    def test_6_y_n_question(self):
        logger.info("\n*************  test_6_y_n_question ******************")
        logger.info("Is the small cube blue?")
        sentence = Sentence("yes_no_question", "", 
                             [Nominal_Group(['the'],
                                            ['cube'],
                                            [['small',[]]],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                            [],
                                                            [['blue',[]]],
                                                            [],
                                                            [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = False        
        self.process(sentence ,expected_result)
        
    
    def test_7_y_n_question(self):
        logger.info("\n*************  test_7_y_n_question verb to be ******************")
        logger.info("Is my cube on the table1?")
        sentence = Sentence("yes_no_question", "", 
                             [Nominal_Group(['my'],
                                            ['cube'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [Indirect_Complement(['on'],
                                                                [Nominal_Group(['the'],
                                                                               ['table1'],
                                                                               [],
                                                                               [],
                                                                               [])])],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = False        
        self.process(sentence ,expected_result) 
    
    def test_9_how_question(self):
        logger.info("\n*************  test_9_how_question ******************")
        logger.info("How is my car?")
        sentence = Sentence("w_question", "manner", 
                             [Nominal_Group(['my'],
                                            ['cube'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = [['blue',[]]]        
        self.process(sentence ,expected_result)
        
    """
    def process(self, sentence ,expected_result):
        sentence = dump_resolved(sentence, 'SPEAKER', 'myself', self.resolver)
        res = self.qhandler.process_sentence(sentence)
        
        #Statements Built for querying Ontology
        logger.info("Query Statement ...")
        for s in self.qhandler._statements:
            logger.info("\t>>" + s)
        logger.info("--------------- >>\n")
        
        #Result from the ontology
        logger.info("Expected Result:" + str(expected_result))
        logger.debug("Result Found in the Ontology: " + str(self.qhandler._answer))
        
        self.qhandler.clear_statements()
        
        if sentence.data_type == "w_question":
            self.assertTrue(expected_result in val[1] for val in res)
                 # res may be a list of several IDs that match the question. Here the result succeed if the expected one is among them
        
        if sentence.data_type == "yes_no_question":
            self.assertEquals(expected_result, res)


class TestQuestionHandlerDialog(unittest.TestCase):
    """Tests the processing of question by the Dialog module.
    This must be tested with oro-server using the testsuite.oro.owl ontology.
    """
    
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.start()
        
        self.oro = ResourcePool().ontology_server
        
        try:
            self.oro.add(['shelf1 rdf:type Shelf',
                        'table1 rdf:type Table', 
                        'table2 rdf:type Table', 
                        'table2 hasColor blue', 
                        'Banana rdfs:subClassOf Plant',
                        'y_banana rdf:type Banana',
                        'y_banana hasColor yellow',
                        'y_banana isOn shelf1',
                        'y_banana isAt LEFT',
                        'y_banana isAt shelf1_front', 'shel1_front rdf:type Location',
                        'LEFT isLeftOf myself', 'LEFT rdf:type Location',
                        'shelf1_front isFrontOf shelf1',
                        'green_banana rdf:type Banana',
                        'green_banana hasColor green',
                        'green_banana isOn table2',
                        'green_banana isAt FRONT', 'FRONT rdf:type Location',
                        'FRONT isFrontOf myself', 
                        'myself focusesOn y_banana',
                        'myself rdfs:label "Jido"',
                        'myself sees id_tom',
                        'myself sees y_banana',
                        'myself sees shelf1',
                        'myself_name rdf:type Name',
                        'myself_name belongsTo myself',
                        'myself_name rdfs:label "Jido"',
                        'id_tom rdf:type Human',
                        'id_tom rdfs:label "Tom"',
                        'id_tom isNextTo myself',
                        ])
            
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass
    
    def test_question1_where(self):

        logger.info("\n##################### test_question1_where ########################\n")
        
        ####
        stmt = "Where is the green banana?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        logger.info( ">> input: " + stmt)
        
        self.assertEquals(res[1][1], "The green banana is on the blue table in front of me.")
    
    
    def test_question2_what(self):

        logger.info("\n##################### test_question2_what ########################\n")
        
        ####
        stmt = "What is yellow?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "The yellow banana.")
    
    def test_question3_what(self):
        logger.info("\n##################### test_question3_what ########################\n")
        
        stmt = "What object is yellow?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "The yellow banana.")
        
    
    def test_question4_what(self):    
        logger.info("\n##################### test_question4_what ########################\n")
        
        stmt = "What color is the banana that is on the table?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "The banana that's on the table, is green.")
    
    def test_question5_what(self):    
        logger.info("\n##################### test_question5_what ########################\n")
        
        stmt = "What is this?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "This is the yellow banana.")

    
    def test_question6_who(self):

        logger.info("\n##################### test_question6_who ########################\n")
        
        ####
        stmt = "Who are you?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "I am Jido.")
    
    def test_question6_who(self):

        logger.info("\n##################### test_question6_who_bis ########################\n")
        
        ####
        stmt = "What is your name?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "My name is Jido.")
        
    
    def test_question7_who(self):
        logger.info("\n##################### test_question7_who ########################\n")
        
        stmt = "Who is the myself?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertTrue(val in res[1][1] for val in ["The myself","Jido"])
    
    def test_question8_who(self):
        logger.info("\n##################### test_question8_who ########################\n")
        
        stmt = "Who do you see?"

        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "I see Tom.")
    
    def test_question8_what(self):    
        logger.info("\n##################### test_question8_what ########################\n")
        stmt = "What do you see?"

        res = self.dialog.test('myself', stmt)
        self.assertTrue(val in res[1][1] for val in ["I see", "Tom", "the yellow banana", "and", "the shelf"])
       
    def test_question9_who(self):
        logger.info("\n##################### test_question9_who ########################\n")
        
        stmt = "Who is Tom?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "Tom is Tom.")
        
    
    def test_question10(self):
        logger.info("\n##################### test_question10 ########################\n")
        
        stmt = "Do you see the yellow banana?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "Yes. I see the yellow banana.")
        
    def test_question11(self):
        logger.info("\n##################### test_question11 ########################\n")
        
        stmt = "is the yellow banana on the shelf?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "Yes. The yellow banana is on the shelf.")
    
    def test_question12(self):
        logger.info("\n##################### Check label ########################\n")
        
        stmt = "What human do you see?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "I see Tom.")
    
    def test_question13(self):
        logger.info("\n##################### Check label ########################\n")
        
        stmt = "What human do you know?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertTrue(val in res[1][1] for val in ["I know Tom"])
    
    def test_question14(self):
        logger.info("\n##################### KNOW ########################\n")
        
        stmt = "What object do you know?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertTrue(val in res[1][1] for val in ["I know", "Tom", "the yellow banana", "the green banana","the table", "and", "the shelf"])
    
    def test_question15(self):
        logger.info("\n##################### KNOW ########################\n")
        
        stmt = "do you know the yellow banana?"
        ####
        
        ###
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "Yes. I know the yellow banana.")

class TestQuestionHandlerScenarioMovingToLondon(unittest.TestCase):
    """Tests the processing of question by the Dialog module.
    This must be tested with oro-server using the testsuite.oro.owl ontology.
    """
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.start()
        
        self.oro = ResourcePool().ontology_server
        
        try:
            
            self.oro.add([  'ACHILLE rdf:type Human',
                            'ACHILLE rdfs:label Achille',
                            'JULIE rdf:type Human', 
                            'JULIE rdfs:label Julie',
                            'TABLE rdf:type Table',
                            'Trashbin rdfs:subClassOf Box',
                            'CardBoardBox rdfs:subClassOf Box',
                            'CardBoardBox rdfs:label "cardboard box"',
                            'TRASHBIN rdf:type Trashbin',
                            'CARDBOARD_BOX rdf:type CardBoardBox',
                            'CARDBOARD_BOX isOn TABLE',
                            'TAPE1 rdf:type VideoTape', 
                            'TAPE1 rdfs:label "The Lords of the robots"', 
                            'TAPE1 isOn TABLE',
                            'TAPE2 rdf:type VideoTape', 
                            'TAPE2 rdfs:label "Jido-E"', 
                            'TAPE2 isOn TABLE',
                            
                            'VideoTape owl:equivalentClass Tape',
                            'TAPE1 owl:differentFrom TAPE2',
                            ])
        except AttributeError:
            pass
            
        
        try:
            
            self.oro.addForAgent('ACHILLE',
                            ['ACHILLE rdf:type Human',
                            'ACHILLE rdfs:label Achille',
                            'JULIE rdf:type Human', 
                            'JULIE rdfs:label Julie',
                            'TABLE rdf:type Table',
                            'Trashbin rdfs:subClassOf Box',
                            'CardBoardBox rdfs:subClassOf Box',
                            'CardBoardBox rdfs:label "cardboard box"',
                            'TRASHBIN rdf:type Trashbin',
                            'CARDBOARD_BOX rdf:type CardBoardBox',
                            'CARDBOARD_BOX isOn TABLE',
                            'TAPE1 rdf:type VideoTape', 
                            'TAPE1 rdfs:label "The Lords of the robots"', 
                            'TAPE1 isOn TABLE',
                            'TAPE2 rdf:type VideoTape', 
                            'TAPE2 rdfs:label "Jido-E"', 
                            'TAPE2 isOn TABLE',
                            
                            'VideoTape owl:equivalentClass Tape',
                            
                            'TAPE1 owl:differentFrom TAPE2',
                            ])
        except AttributeError:
            pass
    
    def test1(self):
        
        self.oro.add(['TAPE1 isIn CARDBOARD_BOX'])
        self.oro.removeForAgent('ACHILLE',['ACHILLE focusesOn TAPE2'])
        self.oro.addForAgent('ACHILLE',['ACHILLE focusesOn CARDBOARD_BOX'])
        
        stmt = "Jido, what is in the box?"
        answer = "This box"
        ####
        self.assertEquals(self.dialog.test('ACHILLE', stmt, answer)[1][1],"The Lords of the robots.")
    
    
    def test2(self):
        #Fill in the history
        stmt = " the TAPE1 is in the CARDBOARD_BOX"
        self.dialog.test('ACHILLE', stmt)
        
        stmt = "Ok. And where is the other tape?"
        ####
        self.assertEquals(self.dialog.test('ACHILLE', stmt)[1][1],"Alright. The other tape is on the table.")
    
    def test3(self):
        stmt = "Ok thank you."
        self.assertEquals(self.dialog.test('ACHILLE', stmt)[1][1],"Alright.")
        
    def test3_2(self):
        stmt = "thank you."
        self.assertEquals(self.dialog.test('ACHILLE', stmt)[1][1],"You're welcome.")
    
    
    def test4(self):
        self.oro.update(['TAPE2 isReachable false'])
                            
        stmt = "can you take Jido-E?"
        ####
        res = self.dialog.test('ACHILLE', stmt)
        
        expected_result = ['ACHILLE desires *',
                  '* rdf:type Get',
                  '* performedBy myself',
                  '* actsOnObject TAPE2']
        
        self.assertTrue(check_results(res[0], expected_result))
        self.assertEquals(res[1][1], "")
    
    def test_5(self):
        self.oro.update(['TAPE2 isReachable false'])
                            
        stmt = "can you take Jido-E?"
        ####
        res = self.dialog.test('ACHILLE', stmt)
        
        expected_result = ['ACHILLE desires *',
                  '* rdf:type Get',
                  '* performedBy myself',
                  '* actsOnObject TAPE2']
        
        self.assertTrue(check_results(res[0], expected_result))
        self.assertEquals(res[1][1], "")
    
    def test_6(self):
        
        ###
        self.oro.removeForAgent('ACHILLE',['ACHILLE focusesOn CARDBOARD_BOX'])
        self.oro.addForAgent('ACHILLE',['ACHILLE focusesOn TAPE2'])
        stmt = "Jido, can you reach this tape?"
        ####
        ## expected to check['myself reaches TAPE2']
        self.assertEquals(self.dialog.test('ACHILLE', stmt)[1][1],"I don't know, if I can reach it.")
        
    
    def test_7(self):
        self.oro.update(['TAPE2 isReachable true'])
        #Feel history
        self.dialog.dialog_history = []
        stmt = "can you reach Jido-E?"
        res = self.dialog.test('ACHILLE', stmt)
        ###
        stmt = "can you take it?"
        ####
        answer = "yes"
        ###
        res = self.dialog.test('ACHILLE', stmt, answer)
        
        expected_result = ['ACHILLE desires *',
                  '* rdf:type Get',
                  '* performedBy myself',
                  '* actsOnObject TAPE2']
        
        self.assertTrue(check_results(res[0], expected_result))
    
    def test_8(self):
        ###
        stmt = "can you take the tape?"
        ####
        answer = "forget it"
        ###
        res = self.dialog.test('ACHILLE', stmt, answer)
        
        expected_result = []
        
        self.assertTrue(check_results(res[0], expected_result))
    
def dump_resolved(sentence, current_speaker, current_listener, resolver):
    sentence = resolver.references_resolution(sentence,
                                                    current_speaker, None, None, None)
    sentence = resolver.noun_phrases_resolution(sentence,
                                                      current_speaker, None, None)    
    sentence = resolver.verbal_phrases_resolution(sentence)
    
    return sentence


def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQuestionHandler)
    suite.addTests( unittest.TestLoader().loadTestsFromTestCase(TestQuestionHandlerDialog))
    suite.addTests( unittest.TestLoader().loadTestsFromTestCase(TestQuestionHandlerScenarioMovingToLondon))
    
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestQuestionHandlerScenarioMovingToLondon)
    
    
    return suite
    
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite())


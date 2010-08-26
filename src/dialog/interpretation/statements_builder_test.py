#!/usr/bin/python
# -*- coding: utf-8 -*-

import inspect
import unittest
from dialog.resources_manager import ResourcePool

import logging
logging.basicConfig(level=logging.DEBUG, format="%(message)s")

from dialog.dialog_core import Dialog
from dialog.interpretation.statements_builder import *
from dialog.interpretation.statements_safe_adder import StatementSafeAdder
from dialog.sentence import Sentence

class TestStatementBuilder(unittest.TestCase):

    def setUp(self):
        
        try:
            ResourcePool().ontology_server.safeAdd(['SPEAKER rdf:type Human',
                                                'SPEAKER rdfs:label "Patrick"'])
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass
        
        try:
            
            ResourcePool().ontology_server.safeAddForAgent('SPEAKER', ['id_danny rdfs:label "Danny"',
                          'id_danny rdf:type Human',
                          
                          'volvo hasColor blue', 
                          'volvo rdf:type Car',
                          'volvo belongsTo SPEAKER',
                          
                          'id_jido rdf:type Robot',
                          'id_jido rdfs:label "Jido"',
                          
                          'twingo rdf:type Car',
                          'twingo hasSize small',
                          'twingo_key rdf:type Key',
                          'twingo_key belongsTo twingo',
                          
                          'a_man rdf:type Man',
                          
                          'id_see rdf:type See', 'id_see actsOnObject a_man', 'id_see performedBy SPEAKER',
                          'id_talk performedBy a_man', 'id_talk rdf:type Talk',
                          
                          'fiat belongsTo id_tom',
                          'fiat rdf:type Car',
                          'fiat hasColor black',
                          
                          'id_tom rdfs:label "Tom"',
                          'id_tom rdf:type Brother',
                          'id_tom belongsTo id_danny',
                          
                          'id_toulouse rdfs:label "Toulouse"',
                          'blue_cube rdf:type Cube', 'blue_cube hasColor blue',
                          
                          'SPEAKER focusesOn another_cube',
                          'another_cube belongsTo SPEAKER', 
                          'another_cube rdf:type Cube',
                          
                          'shelf1 rdf:type Shelf',
                          'green_bottle hasColor green',
                          'green_bottle rdf:type Bottle',
                          'a_bottle rdf:type Bottle',
                          'a_bottle isIn twingo',
                          ])
            
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass
        
        self.stmt = StatementBuilder("SPEAKER")
        self.adder = StatementSafeAdder()
        
    """
        Please write your test below using the following template
    """
    """
    def test_my_unittest():
        print "**** Test My unit test  *** "
        print "Danny drives a car"  
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['drive'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['a'],['car'],[],[],[])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])    
        
        expected_result = ['* rdfs:label "Danny"',
                           '* rdf:type Drive',
                           '* performedBy *',
                           '* involves *',
                           '* rdf:type Car']
        return self.process(sentence, expected_result)
        
        #in order to print the statements resulted from the test, uncomment the line below:
        #self.process(sentence, expected_result, display_statement_result = True)
        #
        #otherwise, use the following if you want to hide the statements 
        #return self.process(sentence, expected_result)
        #    or
        #return self.process(sentence, expected_result, display_statement_result = False)
        #
    """
    
    def test_1(self):
        print "\n**** Test 1  *** "
        print "Danny drives the blue car"  
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['drive'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['the'],['car'],[['blue',[]]],[],[])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])    
        
        expected_result = ['* rdf:type Drive',
                           '* performedBy id_danny',
                           '* involves volvo']
        
        self.process(sentence, expected_result, display_statement_result = True)
        
        print "\n**** Test 1 Thematic roles on direct object *** "
        self.stmt.clear_statements()
        self.stmt._unclarified_ids = []
        self.stmt._statements_to_remove = []
        print "Danny gets the blue car"
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['get'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['the'],['car'],[['blue',[]]],[],[])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = [ '* rdf:type Get',
                            '* performedBy id_danny',
                            '* actsOnObject volvo']   
        self.process(sentence, expected_result, display_statement_result = True)
        
        print "\n**** Test 1 Thematic roles on indirect complements *** "
        self.stmt.clear_statements()
        self.stmt._unclarified_ids = []
        self.stmt._statements_to_remove = []
        print "Danny put the blue cube next to the blue car"
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['put'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['the'],['cube'],[['blue',[]]],[],[])],
                                           [Indirect_Complement(['next+to'],
                                                                [Nominal_Group(['the'],['car'],[['blue',[]]],[],[])])],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = [ '* rdf:type Put',
                            '* performedBy id_danny',
                            '* actsOnObject blue_cube',
                            '* isNexto volvo']   
        self.process(sentence, expected_result, display_statement_result = True)
       

    def test_1_goal_verb(self):
        print "\n**** Test 1  *** "
        print "Danny wants the blue car"  
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['would+like'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['the'],['car'],[['blue',[]]],[],[])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])    
        
        expected_result = ['id_danny desires *',
                            '* involves volvo']
        
        self.process(sentence, expected_result, display_statement_result = True)
    
        print "\n**** Test 1  second verb*** "
        print "Danny wants to drive the blue car"  
        self.stmt.clear_statements()
        self.stmt._unclarified_ids = []
        self.stmt._statements_to_remove = []
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['would+like'],
                                           [Verbal_Group(['drive'],
                                                                   [],
                                                                   'present simple',
                                                                   [Nominal_Group(['the'],['car'],[['blue',[]]],[],[])],
                                                                   [],
                                                                   [],
                                                                   [],
                                                                   'affirmative',
                                                                   [])],
                                           'present simple',
                                           [],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])    
        
        expected_result = ['id_danny desires *',
                            '* rdf:type Drive',
                            '* involves volvo']
        
        self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_2(self):
        print "\n**** Test 2  *** "
        print "my car is blue"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['my'],
                                            ['car'],
                                            [],
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
        expected_result = ['volvo hasColor blue']   
        self.process(sentence, expected_result, display_statement_result = True)
        
    
    def test_3_quantifier_one_some(self):
        print "\n**** test_3_quantifier_one_some *** "
        print "Jido is a robot"
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Jido'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['a'],['robot'],[],[],[])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                          [])]) 
        #quantifier
        sentence.sv[0].d_obj[0]._quantifier = 'SOME' # robot
        
        expected_result = ['id_jido rdf:type Robot']   
        self.process(sentence, expected_result, display_statement_result = True)
        
    
    def test_4(self):
        print "\n**** Test 4  *** "
        print "the man that I saw , has a small car"
        relative4 = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['I'],
                                            [],
                                            [],
                                            [])], 
                            [Verbal_Group(['see'],
                                          [],
                                          'past_simple',
                                          [Nominal_Group(['the'],['man'], [], [], [])],
                                          [],
                                          [],
                                          [],
                                          'affirmative',
                                          [])])
         
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['the'],
                                            ['man'],
                                            [],
                                            [],
                                            [relative4])],                                         
                             [Verbal_Group(['have'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(
                                                          ['a'],
                                                          ['car'],
                                                          [['small',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])]) 
        expected_resut = ['* rdf:type Have',
                          '* performedBy a_man',
                          '* involves twingo']
        return self.process(sentence, expected_resut, display_statement_result = True)
        
    
    def test_5(self):
        print "\n**** Test 5  *** "
        print "the man that talks , has a small car"
        relative5 = Sentence("statement", "", 
                            [], 
                            [Verbal_Group(['talk'],
                                          [],
                                          'past_simple',
                                          [],
                                          [],
                                          [],
                                          [],
                                          'affirmative',
                                          [])]) 
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['the'],
                                            ['man'],
                                            [],
                                            [],
                                            [relative5])],                                         
                             [Verbal_Group(['have'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(
                                                          ['a'],
                                                          ['car'],
                                                          [['small',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])    
        
        expected_resut = ['* rdf:type Have',
                          '* performedBy a_man',
                          '* involves twingo']
        return self.process(sentence, expected_resut, display_statement_result = True)
            
    
    def test_6(self):
        
        print "\n**** Test 6  *** "
        print "I gave you the car of the brother of Danny"   
        sentence = Sentence("statement", 
                             "",
                             [Nominal_Group([],
                                            ['I'],
                                            [],
                                            [],
                                            [])], 
                              [Verbal_Group(['give'],
                                            [],
                                            'past_simple',
                                            [Nominal_Group(['the'],
                                                           ['car'],
                                                           [],
                                                           [Nominal_Group(['the'],
                                                                          ['brother'],
                                                                          [],
                                                                          [Nominal_Group([],
                                                                                         ['Danny'],
                                                                                         [],
                                                                                         [],
                                                                                         [])],
                                                                          [])],
                                                            [])] , 
                                            [Indirect_Complement([],
                                                                 [Nominal_Group([],
                                                                                ['you'],
                                                                                [],
                                                                                [],
                                                                                [])])], 
                                            [],
                                            [],
                                            'affirmative', 
                                            [])])
        expected_resut = ['* rdf:type Give',
                          '* performedBy SPEAKER',
                          '* actsOnObject fiat',
                          '* receivedBy myself']
        
        return self.process(sentence, expected_resut, display_statement_result = True)
    
        
    def test_7(self):
        
        print "\n**** Test 7  *** "
        print "I went to Toulouse"
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['I'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['go'],
                                           [],
                                           'past simple',
                                           [],
                                           [Indirect_Complement(['to'], [Nominal_Group([],['Toulouse'],[],[],[])])],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['* rdf:type Go',
                          '* performedBy SPEAKER',
                          '* hasGoal id_toulouse',
                          '* eventOccurs PAST']
        return self.process(sentence, expected_resut, display_statement_result = True)
    
    def test_8(self):
        print "\n**** Test 8  *** "
        print "put the green bottle in the blue car"
        sentence = Sentence("imperative", "", 
                             [],                                         
                             [Verbal_Group(['put'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['the'],['bottle'],[['green',[]]],[],[])],
                                           [Indirect_Complement(['in'],
                                                                [Nominal_Group(['the'],['car'],[['blue',[]]],[],[])]) ],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['SPEAKER desires *',
                          '* rdf:type Put',
                          '* performedBy myself',
                          '* actsOnObject green_bottle',
                          '* isIn volvo']  
        

        return self.process(sentence, expected_resut, display_statement_result = True)
    
    
    def test_8_relative(self):
        print "\n**** Test 8 relative *** "
        print "show me the bottle that is in the twingo"
        relative8 = Sentence("statement", "", 
                            [], 
                            [Verbal_Group(['be'],
                                          [],
                                          'past_simple',
                                          [],
                                          [Indirect_Complement(['in'],
                                                                [Nominal_Group(['the'],['twingo'],[],[],[])]) ],
                                          [],
                                          [],
                                          'affirmative',
                                          [])])
        sentence = Sentence("imperative", "", 
                             [],                                         
                             [Verbal_Group(['show'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['the'],
                                                          ['bottle'],
                                                          [],
                                                          [],
                                                          [relative8])],
                                           [Indirect_Complement([],
                                                                [Nominal_Group([],['me'],[],[],[])]) ],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['SPEAKER desires *',
                          '* rdf:type Show',
                          '* performedBy myself',
                          '* actsOnObject a_bottle',
                          '* receivedBy SPEAKER']  
        

        return self.process(sentence, expected_resut, display_statement_result = True)
    
    def test_9_this(self):
        
        print "\n**** test_9_this  *** "
        print "this is a blue cube"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['this'],
                                            [],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['a'],
                                                          ['cube'],
                                                          [['blue',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        #Quantifier
        sentence.sv[0].d_obj[0]._quantifier = 'SOME' # a blue cube
        expected_resut = ['another_cube rdf:type Cube',
                            'another_cube hasColor blue']
                          
        another_expected_resut = ['SPEAKER focusesOn blue_cube']
        
        return self.process(sentence, expected_resut, display_statement_result = True)
    
   
    def test_9_this_my(self):
        
        print "\n**** test_9_this_my  *** "
        print "this is my cube"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['this'],
                                            [],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['my'],
                                                          ['cube'],
                                                          [],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['another_cube belongsTo SPEAKER']
                          
        another_expected_resut = ['SPEAKER focusesOn blue_cube']
        
        return self.process(sentence, expected_resut, display_statement_result = True)
    
    def test_10_this(self):
        
        print "\n**** test_10_this  *** "
        print "this is on the shelf1"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['this'],
                                            [],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [Indirect_Complement(['on'],
                                                                [Nominal_Group(['the'],['shelf1'],[],[],[])]) ],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['another_cube isOn shelf1']
        another_expected_resut = ['SPEAKER focusesOn blue_cube']
        
        return self.process(sentence, expected_resut, display_statement_result = True)
    
    
    def test_11_this(self):
        
        print "\n**** test_11_this  *** "
        print "this goes to the shelf1"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['this'],
                                            [],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['go'],
                                           [],
                                           'present simple',
                                           [],
                                           [Indirect_Complement(['to'],
                                                                [Nominal_Group(['the'],['shelf1'],[],[],[])]) ],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['* rdf:type Go',
                          '* performedBy another_cube',
                          '* hasGoal shelf1']
        another_expected_resut = ['SPEAKER focusesOn something']#with [* rdf:type Go, * performedBy something, * hasGoal shelf1] in the ontology
        return self.process(sentence, expected_resut, display_statement_result = True)
    
    
    def test_12_this(self):
        
        print "\n**** test_12_this  *** "
        print "this cube goes to the shelf1"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['this'],
                                            ['cube'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['go'],
                                           [],
                                           'present simple',
                                           [],
                                           [Indirect_Complement(['to'],
                                                                [Nominal_Group(['the'],['shelf1'],[],[],[])]) ],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['* rdf:type Go',
                          '* performedBy another_cube',
                          '* hasGoal shelf1']
        
        return self.process(sentence, expected_resut, display_statement_result = True)
    
    
    
    def test_13_this(self):
        
        print "\n**** test_13_this  *** "
        print "this cube is blue "
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['this'],
                                            ['cube'],
                                            [],
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
        expected_resut = ['another_cube hasColor blue']
        
        return self.process(sentence, expected_resut, display_statement_result = True)

    
    
    def test_14_quantifier_all_all(self):        
        print "\n**** test_14_quantifier_all_all  *** "
        print "Apples are fruits"
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['apple'],#apple is common noun. Therefore, do not capitalize.
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                        ['fruit'],
                                                        [],
                                                        [],
                                                        [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                            [])])
        
        #quantifier
        sentence.sn[0]._quantifier = 'ALL' # apples
        sentence.sv[0].d_obj[0]._quantifier = 'ALL' # fruits
        expected_resut = ['Apple rdfs:subClassOf Fruit']
        
        return self.process(sentence, expected_resut, display_statement_result = True)
    
    def test_15_quantifier_some_some(self):        
        print "\n**** test_15_quantifier_some_some  *** "
        print "an apple is a fruit"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['an'],
                                            ['apple'],#apple is common noun. Therefore, do not capitalize.
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['a'],
                                                        ['fruit'],
                                                        [],
                                                        [],
                                                        [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                            [])])
        
        #quantifier
        sentence.sn[0]._quantifier = 'SOME' # apples
        sentence.sv[0].d_obj[0]._quantifier = 'SOME' # fruits
        expected_resut = ['Apple rdfs:subClassOf Fruit']
        
        return self.process(sentence, expected_resut, display_statement_result = True)
    
    
    def test_15_quantifier_action_verb(self):        
        print "\n**** test_15_quantifier_action_verb  *** "
        print "an apple grows on a tree"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['an'],
                                            ['apple'],#apple is common noun. Therefore, do not capitalize.
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['grow'],
                                           [],
                                           'present simple',
                                           [],
                                           [Indirect_Complement(['on'],
                                                                [Nominal_Group(['a'],
                                                                                ['tree'],
                                                                                [],
                                                                                [],
                                                                                [])])],
                                           [],
                                           [],
                                           'affirmative',
                                            [])])
        
        #quantifier
        sentence.sn[0]._quantifier = 'SOME' # an apple
        sentence.sv[0].i_cmpl[0].nominal_group[0]._quantifier = 'SOME' # a tree
        expected_resut = ['? ? ?']
        
        return self.process(sentence, expected_resut, display_statement_result = True)
    
    
    #Action adverbs
    def test_16_adverb(self):
        print "\n**** test_16_adverb *** "
        print "Danny slowly drives the blue car"
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['drive'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['the'],
                                                          ['car'],
                                                          [['blue',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           ['quickly'],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = ['* rdf:type Drive', 
                            '* performedBy id_danny',
                            '* involves volvo',
                            '* actionSupervisionMode QUICK']   
        self.process(sentence, expected_result, display_statement_result = True)
    
    
    #Verb tense approach
    def test_17_verb_tense(self):
        print "\n**** test_17_verb_tense *** "
        print "Danny will drive the blue car"
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['drive'],
                                           [],
                                           'future simple',
                                           [Nominal_Group(['the'],
                                                          ['car'],
                                                          [['blue',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           ['quickly'],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = ['* rdf:type Drive', 
                            '* performedBy id_danny',
                            '* involves volvo',
                            '* eventOccurs FUTUR']   
        self.process(sentence, expected_result, display_statement_result = True)
    
    
    #Negative approach
    def test_18_negative(self):
        
        print "Danny drives the blue car"
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['drive'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['the'],
                                                          ['car'],
                                                          [['blue',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = [ '* rdf:type Drive', 
                            '* performedBy id_danny',
                            '* involves volvo']   
        self.process(sentence, expected_result, display_statement_result = True)
        
        
        print "\n**** test_18_negative *** "
        self.stmt.clear_statements()
        self.stmt._unclarified_ids = []
        self.stmt._statements_to_remove = []
        print "Danny doesn't drive the blue car"
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['drive'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['the'],
                                                          ['car'],
                                                          [['blue',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'negative',
                                           [])])
        expected_result = [ '* rdf:type Drive', #REMOVE after finding *
                            '* performedBy id_danny',
                            '* involves volvo']   
        self.process(sentence, expected_result, display_statement_result = True)
        
        
        print "\n**** test_18_negative_bis *** "
        print "Danny is not in Toulouse"
        self.stmt.clear_statements()
        self.stmt._unclarified_ids = []
        self.stmt._statements_to_remove = []
        
        sentence = Sentence("statement", "",
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [],
                                           [Indirect_Complement(['in'], [Nominal_Group([],['Toulouse'],[],[],[])])],
                                           [],
                                           [],
                                           'negative',
                                           [])])
        expected_result = [ 'id_danny isIn *',
                            '* owl:differentFrom id_toulouse']

        self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_18_negative_relative(self):
        print "\n**** test_18_negative_relative *** "
        print "Danny drives the car that is not blue"
        
        relative18 = Sentence("relative", "", 
                            [], 
                            [Verbal_Group(['be'],
                                          [],
                                          'past_simple',
                                          [Nominal_Group([],[],[['blue',[]]],[],[])],
                                          [],
                                          [],
                                          [],
                                          'negative',
                                          [])])
                                          
        
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['drive'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['the'],
                                                          ['car'],
                                                          [],
                                                          [],
                                                          [relative18])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = [ '* rdf:type Drive', 
                            '* performedBy id_danny',
                            '* involves fiat']
        self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_19_negative(self):
        print "\n**** test_19_negative *** "
        print "Jido is not a human"
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Jido'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['a'],
                                                          ['human'],
                                                          [],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'negative',
                                           [])])
        
        #quantifier
        sentence.sv[0].d_obj[0]._quantifier = 'SOME' # Human
       
        expected_result = [ 'id_jido rdf:type ComplementOfHuman']   
        self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_20_negative(self):
        print "\n**** test_20_negative *** "
        print "the shelf1 is not green"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['the'],
                                            ['shelf1'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                          [],
                                                          [['green',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'negative',
                                           [])])
        expected_result = [ 'shelf1 hasColor *']   
        self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_20_negative_inconsistent(self):
        print "\n**** test_20_negative *** "
        print "the shelf1 is green"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['the'],
                                            ['shelf1'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                          [],
                                                          [['green',[]]],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = ['shelf1 hasColor green']   
        self.process(sentence, expected_result, display_statement_result = True)
        
        print "\n**** test_20_negative_bis *** "
        print "the shelf1 is red"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['the'],
                                            ['shelf1'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                          [],
                                                          ['red'],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = ['shelf1 hasColor red']   
        self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_21_negative(self):
        print "\n**** test_21_negative *** "
        print "this is not the shelf1"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['this'],
                                            [],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['the'],
                                                          ['shelf1'],
                                                          [],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'negative',
                                           [])])
        
        expected_result = ['another_cube owl:differentFrom shelf1']   
        self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_22_negative(self):
        print "\n**** test_22_negative *** "
        print "Fruits are not humans"
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['fruit'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                          ['human'],
                                                          [],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'negative',
                                           [])])
                                           
        
        #quantifier
        sentence.sn[0]._quantifier = 'ALL' # Fruits
        sentence.sv[0].d_obj[0]._quantifier = 'ALL' # Humans
        
        expected_result = [ 'Fruit rdfs:subClassOf ComplementOfHuman']   
        self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_23_negative(self):
        print "\n**** test_23_negative *** "
        print "you are not me"
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['you'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                          ['me'],
                                                          [],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'negative',
                                           [])])
        
        expected_result = [ 'myself owl:differentFrom SPEAKER']   
        self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_24_negative(self):
        print "\n**** test_24_negative *** "
        print "the blue car is not my car"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['the'],
                                            ['car'],
                                            [['blue',[]]],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['my'],
                                                          ['car'],
                                                          [],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'negative',
                                           [])])
        
        expected_result = [ 'volvo owl:differentFrom volvo']   
        self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_25_negative(self):
        print "\n**** test_25_negative *** "
        print "I am not the brother of Danny"
        sentence = sentence = Sentence("statement", 
                             "",
                             [Nominal_Group([],
                                            ['I'],
                                            [],
                                            [],
                                            [])], 
                              [Verbal_Group(['be'],
                                            [],
                                            'present simple',
                                            [Nominal_Group(['the'],
                                                            ['brother'],
                                                            [],
                                                            [Nominal_Group([],
                                                                            ['Danny'],
                                                                            [],
                                                                            [],
                                                                            [])],
                                                            [])], 
                                            [], 
                                            [],
                                            [],
                                            'negative', 
                                            [])])
                                            
        expected_result = [ 'SPEAKER owl:differentFrom id_tom']   
        self.process(sentence, expected_result, display_statement_result = True)
    

    
    """
    def test_26_subsentences(self):
        print "\n**** test_26_subsentences *** "
        print "you will drive the car if you get the keys'."
        
        subsentence = Sentence('subsentence', 'if', 
                                [Nominal_Group([],['you'],[],[],[])], 
                                [Verbal_Group(['get'], [],'present simple', 
                                    [Nominal_Group(['the'],['key'],[],[],[])], 
                                    [],
                                    [], 
                                    [] ,
                                    'affirmative',
                                    [])])
                                    
        sentence = Sentence('statement', '', 
                                [Nominal_Group([],['you'],[],[],[])], 
                                [Verbal_Group(['drive'],
                                    [],
                                    'future simple', 
                                    [Nominal_Group(['the'],['car'],[],[],[])], 
                                    [],
                                    [], 
                                    [],
                                    'affirmative',
                                    [subsentence])])
                                            
        expected_result = [ '* rdf:type Drive',
                            '* performedBy myself',
                            '* involves twingo',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject twingo_key']   
        self.process(sentence, expected_result, display_statement_result = True)
    

    def test_27_subsentences(self):
        print "\n**** test_27_subsentences *** "
        print "learn that apple are fruits."
        
        subsentence = Sentence('subsentence', 'that', 
                                [Nominal_Group([],['apple'],[],[],[])], 
                                [Verbal_Group(['be'], [],'present simple', 
                                    [Nominal_Group([],['fruit'],[],[],[])], 
                                    [],
                                    [], 
                                    [] ,
                                    'affirmative',
                                    [])])
        #Quantifier
        subsentence.sn[0]._quantifier = 'ALL' # Apples
        subsentence.sv[0].d_obj[0]._quantifier = 'ALL' # Fruits
                                    
        sentence = Sentence('imperative', '', 
                                [],
                                [Verbal_Group(['learn'], [], 'present simple',[], [], [],[], 
                                    'affirmative', 
                                    [subsentence])])
                                            
        expected_result = [ '* rdf:type Learn',
                            '* performedBy myself',
                            'SPEAKER desires *',
                            'Apple rdfs:subClassOf Fruit']
        self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_28_subsentences(self):
        print "\n**** test_28_subsentences *** "
        print "I am going to toulouse when you get the small car."
        
        subsentence = Sentence('subsentence', 'when', 
                                [Nominal_Group([],['you'],[],[],[])], 
                                [Verbal_Group(['get'], [],'present simple', 
                                    [Nominal_Group(['the'],['car'],[['small',[]]],[],[])], 
                                    [],
                                    [], 
                                    [] ,
                                    'affirmative',
                                    [])])
                                    
        sentence = Sentence('statement', '', 
                                [Nominal_Group([],['I'],[],[],[])], 
                                [Verbal_Group(['go'],
                                    [],
                                    'present processive', 
                                    [],
                                    [Indirect_Complement(['to'], 
                                                        [Nominal_Group([],
                                                                        ['Toulouse'],
                                                                        [],
                                                                        [],
                                                                        [])])],
                                    [], 
                                    [] ,
                                    'affirmative',
                                    [subsentence])])
                                            
        expected_result = ['* rdf:type Go',
                            '* performedBy SPEAKER', 
                            '* hasGoal id_toulouse',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject twingo']   
                            
        self.process(sentence, expected_result, display_statement_result = True)
    
    """
    
    def process(self, sentence, expected_result, display_statement_result = False):
        #Dump resolution
        sentence = dump_resolved(sentence, self.stmt._current_speaker, 'myself')
        
        #StatementBuilder
        res = self.stmt.process_sentence(sentence)
        
        #Statement Safe Adder
        self.adder._unclarified_ids = self.stmt._unclarified_ids
        self.adder._statements = res
        self.adder._statements_to_remove = self.stmt._statements_to_remove
        res = self.adder.process()
        
        #Assert result
        self.assertTrue(check_results(res, expected_result))
        
                
class TestBaseSentenceDialog(unittest.TestCase):
    """Tests the processing of simple sentence by the Dialog module.
    These sentences don't require discrimination.
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
                        'y_banana belongsTo myself',
                        'green_banana rdf:type Banana',
                        'green_banana hasColor green',
                        'green_banana isOn table2',
                        'myself focusesOn y_banana',
                        'big_tree rdf:type Tree',
                        'big_tree hasSize big',
                        'red_apple rdf:type Apple',
                        'red_apple hasColor red'
                        ])
            
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass

    def test_sentence1(self):

        print("\n##################### test_sentence1 ########################\n")
        
        ####
        stmt = "put the yellow banana on the shelf"
        ####

        expected_result = [ 'myself desires *',
                            '* rdf:type Place',
                            '* performedBy myself',
                            '* actsOnObject y_banana',
                            '* receivedBy shelf1']
        ###
        res = self.dialog.test('myself', stmt)
        self.assertTrue(check_results(res[0], expected_result))
        

    def test_sentence2(self):
        
        print("\n##################### test_sentence2 ########################\n")

        ####
        stmt = "give me the green banana"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Give',
                            '* performedBy myself',
                            '* actsOnObject green_banana',
                            '* receivedBy myself']
        ###
        res = self.dialog.test('myself', stmt)
        self.assertTrue(check_results(res[0], expected_result))
        

    def test_sentence3(self):
        
        print("\n##################### Simple statements ########################\n")              
                
        ####
        stmt = "the yellow banana is green"
        ####
        expected_result = ['y_banana hasColor green']
        ###
        res = self.dialog.test('myself', stmt)
        
        ###Check ontology consistency
        self.assertFalse(self.oro.safeAdd(res))
        ### Check result
        self.assertTrue(check_results(res[0], expected_result))
        
        
        ####
        stmt = "the green banana is good"
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['green_banana hasFeature good']
        self.assertTrue(check_results(res[0], expected_result))
        
    def test_sentence4(self):
        
        print("\n##################### Subclasses ########################\n")
        ####
        stmt = "bananas are fruits"
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['Banana rdfs:subClassOf Fruit']
        self.assertTrue(check_results(res[0], expected_result))
        
        
        ####
        stmt = "A banana is a fruit"
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['Banana rdfs:subClassOf Fruit']
        self.assertTrue(check_results(res[0], expected_result))
    
        
        
    def test_sentence5(self):
        
        print("\n##################### test_sentence5 - THIS ########################\n")
        ####
        stmt = "This is my banana"
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['y_banana belongsTo myself']
        self.assertTrue(check_results(res[0], expected_result))
        
        stmt = "This is a green banana" ## ERROR -> y_banana can not be green
        ####
        res = self.dialog.test('myself', stmt)
        ###
        self.assertFalse(self.oro.safeAdd(res))
        
        stmt = "This is a fruit" 
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['y_banana rdf:type Fruit']

        self.assertTrue(check_results(res[0], expected_result))

    def test_sentence6(self):
        
        print("\n##################### test_sentence6 - it ########################\n")
        #Fill up History
        
        ##sentence1
        stmt = "the red apple is on the big tree"
        res = self.dialog.test('myself', stmt)
        
        
        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)
        
        ##sentence3
        stmt = "I see it"
        ###
        answer = "yes. I meant the green one"
        res = self.dialog.test('myself', stmt, answer)
        
        expected_result = ['* rdf:type See',
                            '* performedBy myself',
                            '* actsOnObject green_banana']
                            
        self.assertTrue(check_results(res[0], expected_result))
        
    
    def test_sentence7(self):
        
        print("\n##################### test_sentence7 - it ########################\n")
        
        #Fill up History
        
        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)
        
        ##sentence3
        stmt = "I see it"
        ###
        answer = "No. I mean the red apple"
        res = self.dialog.test('myself', stmt, answer)
        
        expected_result = ['* rdf:type See',
                            '* performedBy myself',
                            '* actsOnObject red_apple']
                            

        self.assertTrue(check_results(res[0], expected_result))
    
    
    def test_sentence8(self):
        
        print("\n##################### test_sentence8 - THIS NO FOCUS########################\n")
        #Fill up History
        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)
        
        ##sentence3
        self.oro.remove(['myself focusesOn y_banana'])
        
        stmt = "I see this"
        ###
        ### Expected Question: Do you mean the green banana?
        answer = "No. I mean the red apple"
        res = self.dialog.test('myself', stmt, answer)
        expected_result = ['* rdf:type See',
                            '* performedBy myself',
                            '* actsOnObject red_apple']
        
        self.oro.add(['myself focusesOn y_banana'])
        
        self.assertTrue(check_results(res[0], expected_result))
        
        
    def test_sentence8_bis(self):
        
        print("\n##################### test_sentence8 bis - THIS NO FOCUS########################\n")
        #Fill up History
        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)
        
        ##sentence3
        self.oro.remove(['myself focusesOn y_banana'])
        
        stmt = "I see this one"
        ###
        ### Expected Question: Do you mean the green banana?
        answer = "No. I mean the red apple"
        res = self.dialog.test('myself', stmt, answer)
        expected_result = ['* rdf:type See',
                            '* performedBy myself',
                            '* actsOnObject red_apple']
        
        self.oro.add(['myself focusesOn y_banana'])
        self.assertTrue(check_results(res[0], expected_result))
    
    def test_sentence8_ter(self):
        
        print("\n##################### test_sentence8 ter - THIS NO FOCUS########################\n")
        #Fill up History
        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)
        
        ##sentence3
        self.oro.remove(['myself focusesOn y_banana'])
        
        stmt = "I see this apple"
        ###
        res = self.dialog.test('myself', stmt)
        
        expected_result = ['* rdf:type See',
                            '* performedBy myself',
                            '* actsOnObject red_apple']
        
        self.oro.add(['myself focusesOn y_banana'])
        self.assertTrue(check_results(res[0], expected_result))
        
        
    def test_sentence9(self):
        
        print("\n##################### test_sentence9 - OTHER ########################\n")
        #Fill up History
        ##sentence1
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)
        
        ##sentence2
        stmt = "the other banana is on the shelf."
        ###
        res = self.dialog.test('myself', stmt)
        
        expected_result = ['y_banana isOn shelf1']
        self.assertTrue(check_results(res[0], expected_result))
    
    def test_sentence9_bis(self):
        
        print("\n##################### test_sentence9_bis - OTHER ########################\n")
        #Fill up History
        ##sentence1
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)
        
        ##sentence2
        stmt = "the other one is on the shelf."
        ###
        ### expected question: Do you mean the other banana?
        answer = "yes. the yellow banana"
        res = self.dialog.test('myself', stmt, answer)
        
        expected_result = ['y_banana isOn shelf1']
        self.assertTrue(check_results(res[0], expected_result))
    
    def test_sentence9_ter(self):
        
        print("\n##################### test_sentence9_ter - THIS OTHER ########################\n")
        #Fill up History
        ##sentence1
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)
        
        ##sentence2
        self.oro.remove(['myself focusesOn y_banana'])
        
        stmt = "this other one is on the shelf."
        ###
        ### expected question: Do you mean the other banana?
        answer = "yes. the yellow banana"
        res = self.dialog.test('myself', stmt, answer)
        
        expected_result = ['y_banana isOn shelf1']
        
        self.oro.add(['myself focusesOn y_banana'])
        self.assertTrue(check_results(res[0], expected_result))
    
    def test_sentence9_quater(self):
        
        print("\n##################### test_sentence9_quater - THIS OTHER ########################\n")
        #Fill up History
        ##sentence1
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)
        
        ##sentence2
        self.oro.remove(['myself focusesOn y_banana'])
        
        stmt = "this other banana is on the shelf."
        ###
        res = self.dialog.test('myself', stmt)
        
        expected_result = ['y_banana isOn shelf1']
        
        self.oro.add(['myself focusesOn y_banana'])
        self.assertTrue(check_results(res[0], expected_result))
    
    
    def test_sentence10(self):
        
        print("\n##################### test_sentence10 - SAME ########################\n")
        #Fill up History
        
        ##sentence1
        stmt = "the red apple is on the big tree"
        res = self.dialog.test('myself', stmt)
        
        
        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)
        
        ##sentence3
        stmt = "I see the same one"
        ###
        answer = "yes. I meant the green one"
        res = self.dialog.test('myself', stmt, answer)
        
        expected_result = ['* rdf:type See',
                            '* performedBy myself',
                            '* actsOnObject green_banana']
        
        
        self.assertTrue(check_results(res[0], expected_result))
    
    def test_sentence10_bis(self):
        
        print("\n##################### test_sentence10_bis - SAME ########################\n")
        #Fill up History
        
        ##sentence1
        stmt = "the red apple is on the big tree"
        res = self.dialog.test('myself', stmt)
        
        
        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)
        
        ##sentence3
        stmt = "I see the same apple"
        ###
        res = self.dialog.test('myself', stmt)
        
        expected_result = ['* rdf:type See',
                            '* performedBy myself',
                            '* actsOnObject red_apple']
        
        
        self.assertTrue(check_results(res[0], expected_result))
    
    
    def test_sentence11(self):
        
        print("\n##################### test_sentence11 - MODALS ########################\n")
        #Fill up History
        ##sentence1
        stmt = "I can take the green banana"
        res = self.dialog.test('myself', stmt)
        
        expected_result = ['myself canPerforms *',
                           '* rdf:type Get',
                           '* actsOnObject green_banana']
                           
        self.assertTrue(check_results(res[0], expected_result))
    
  
    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()
 


"""
    The following functions are implemented for test purpose only
"""

def check_results(res, expected):
    def check_triplets(tr , te):
        tr_split = tr.split()
        te_split = te.split()
        
        return  (not '?' in tr_split[0]) and \
                (not '?' in tr_split[2]) and \
                (tr_split[0] == te_split[0] or te_split[0] == '*') and\
                (tr_split[1] == te_split[1]) and\
                (tr_split[2] == te_split[2] or te_split[2] == '*') 
       
    while res:
        r = res.pop()
        for e in expected:
            if check_triplets(r, e):
                expected.remove(e)
    if expected:
        print "\t**** /Missing statements in result:   "
        print "\t", expected, "\n"
           
    return expected == res



def dump_resolved(sentence, current_speaker, current_listener):
    def resolve_ng(ngs, builder):        
        for ng in ngs:
            if ng._quantifier != 'ONE':
                logging.info("\t...No Statements sended to Resolution for discrmination for this nominal group...")
                
            else:
                #Statement for resolution
                logging.info("Statements sended to Resolution for discrmination for this nominal group...")
                builder.process_nominal_group(ng, '?concept', None, False)
                stmts = builder.get_statements()
                
                if builder.process_on_demonstrative_det:# More complicated processing of "this" in Resolution module
                    stmts.append(current_speaker + " focusesOn ?concept")
                
                builder.clear_statements()
                
                for s in stmts:
                    logging.info("\t>>" + s)
                    
                logging.info("--------------<<\n")
                
            #Dump resolution for StatementBuilder test ONLY
            logging.info("Dump resolution for statement builder test ONLY ...")
            
            resolved = True
                    
            if ng._resolved:
                pass
                
            elif ng.adjectives_only():
                ng.id = '*'
            
            #personal pronoun
            elif ng.noun in [['me'], ['Me'],['I']]:
                ng.id = current_speaker
            elif ng.noun in [['you'], ['You']]:
                ng.id = current_listener       
            
            elif ng.noun:
                
                onto_class = ''
                try:
                    onto_class =  ResourcePool().ontology_server.lookupForAgent(current_speaker, ng.noun[0])
                except AttributeError: #the ontology server is not started of doesn't know the method
                    pass
                
                if ng._quantifier != 'ONE':
                    logging.debug("... Found nominal group with quantifier " + ng._quantifier)
                    ng.id = get_class_name(ng.noun[0], onto_class)
                
                elif [ng.noun[0], 'INSTANCE'] in onto_class:    
                    ng.id = ng.noun[0]
                
                else:
                    onto = ''
                    try:
                        onto =  ResourcePool().ontology_server.findForAgent(current_speaker, '?concept',stmts)
                    except AttributeError: #the ontology server is not started of doesn't know the method
                        pass
                            
                    
                    if onto:    
                        ng.id = onto[0]
                        
            else:
                onto = ''
                try:
                    onto =  ResourcePool().ontology_server.findForAgent(current_speaker, '?concept',stmts)
                except AttributeError: #the ontology server is not started of doesn't know the method
                    pass
                        
                
                if onto:    
                    ng.id = onto[0]
                        
            
            #Other Nominal group attibutes
            if ng.noun_cmpl and not ng._resolved:
                res_noun_cmpl = resolve_ng(ng.noun_cmpl, builder)
                ng.noun_cmpl =res_noun_cmpl[0]
                
            if ng.relative and not ng._resolved:
                for rel in ng.relative:
                    rel = dump_resolved(rel, current_speaker, current_listener)
            
            #Nominal group resolved?
            if ng.id:
                logging.info("\tAssign to ng: " + colored_print(ng.id, 'white', 'blue'))
                ng._resolved = True
                
            resolved = resolved and ng._resolved
            
        return [ngs, resolved]
    
    
    def resolve_sv(vgs):
        for sv in vgs:
            sv._resolved = True
            
            if sv.d_obj:
                res_d_obj = resolve_ng(sv.d_obj, builder)
                sv.d_obj = res_d_obj[0]
                sv._resolved = sv._resolved and res_d_obj[1]
                
            if sv.i_cmpl:
                for i_cmpl in sv.i_cmpl:
                    res_i_cmpl = resolve_ng(i_cmpl.nominal_group, builder)                    
                    i_cmpl = res_i_cmpl[0]
                    sv._resolved = sv._resolved and res_i_cmpl[1]
            
            if sv.vrb_sub_sentence:
                for sub in sv.vrb_sub_sentence:
                    sub = dump_resolved(sub, current_speaker, current_listener)
                    
                    
            if sv.sv_sec:
                sv.sv_sec = resolve_sv(sv.sv_sec)
                
        return vgs
    
    

    builder = NominalGroupStatementBuilder(None, current_speaker)
        
    if sentence.sn:
        res_sn = resolve_ng(sentence.sn, builder)
        sentence.sn = res_sn[0]
        
    
    if sentence.sv:
        sentence.sv = resolve_sv(sentence.sv)
            
    
    print(sentence)
    print "Sentence resolved ... " , sentence.resolved()
    
    return sentence


def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStatementBuilder)
    suite.addTests( unittest.TestLoader().loadTestsFromTestCase(TestBaseSentenceDialog))

    return suite
    
if __name__ == '__main__':
       
    # executing verbalization tests
    unittest.TextTestRunner(verbosity=2).run(test_suite())

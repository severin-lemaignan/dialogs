#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import time

logger = logging.getLogger("dialogs")

import inspect
import unittest
from dialogs.resources_manager import ResourcePool

from dialogs.helpers.helpers import check_results, get_console_handler, get_file_handler

from dialogs.dialog_core import Dialog
from dialogs.interpretation.statements_builder import *
from dialogs.interpretation.statements_safe_adder import StatementSafeAdder
from dialogs.sentence import Sentence
from dialogs.interpretation.resolution import Resolver


class TestStatementBuilder(unittest.TestCase):
    def setUp(self):
        ResourcePool().ontology_server.reset()

        ResourcePool().ontology_server.add(['SPEAKER rdf:type Human',
                                            'SPEAKER rdfs:label "Patrick"'])

        ResourcePool().ontology_server.addForAgent('SPEAKER', ['id_danny rdfs:label "Danny"',
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

                                                               'SPEAKER sees a_man',
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

                                                               'a_candy rdf:type Candy',
                                                               'location_left isLeftOf SPEAKER',
                                                               'location_left rdf:type Location',
        ])

        self.stmt = StatementBuilder("SPEAKER")
        self.adder = StatementSafeAdder()
        self.resolver = Resolver()

    """
        Please write your test below using the following template
    """
    """
    def test_my_unittest():
        logger.info("**** Test My unit test  *** ")
        logger.info("Danny drives a car")
        sentence = Sentence(STATEMENT, "", 
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
                                           Verbal_Group.affirmative,
                                           [])])    
        
        expected_result = ['* rdfs:label "Danny"',
                           '* rdf:type Drive',
                           '* performedBy *',
                           '* involves *',
                           '* rdf:type Car']
        self.process(sentence, expected_result)
        
        #in order to print the statements resulted from the test, uncomment the line below:
        #self.process(sentence, expected_result, display_statement_result = True)
        #
        #otherwise, use the following if you want to hide the statements 
        #self.process(sentence, expected_result)
        #    or
        #self.process(sentence, expected_result, display_statement_result = False)
        #
    """

    def test_01(self):
        logger.info("\n**** Test 1  *** ")
        logger.info("Danny drives the blue car")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group([],
                                ['Danny'],
                                [],
                                [],
                                [])],
                            [Verbal_Group(['drive'],
                                [],
                                          'present simple',
                                          [Nominal_Group(['the'], ['car'], [['blue', []]], [], [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])

        expected_result = ['* rdf:type Drive',
                           '* performedBy id_danny',
                           '* involves volvo']

        self.process(sentence, expected_result, display_statement_result=True)

        logger.info("\n**** Test 1 Thematic roles on direct object *** ")
        self.stmt.clear_statements()
        self.stmt._unclarified_ids = []
        self.stmt._statements_to_remove = []
        logger.info("Danny gets the blue car")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group([],
                                ['Danny'],
                                [],
                                [],
                                [])],
                            [Verbal_Group(['get'],
                                [],
                                          'present simple',
                                          [Nominal_Group(['the'], ['car'], [['blue', []]], [], [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['* rdf:type Get',
                           '* performedBy id_danny',
                           '* actsOnObject volvo']
        self.process(sentence, expected_result, display_statement_result=True)

        logger.info("\n**** Test 1 Thematic roles on indirect complements *** ")
        self.stmt.clear_statements()
        self.stmt._unclarified_ids = []
        self.stmt._statements_to_remove = []
        logger.info("Danny put the blue cube next to the blue car")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group([],
                                ['Danny'],
                                [],
                                [],
                                [])],
                            [Verbal_Group(['put'],
                                [],
                                          'present simple',
                                          [Nominal_Group(['the'], ['cube'], [['blue', []]], [], [])],
                                          [Indirect_Complement(['next+to'],
                                                               [Nominal_Group(['the'], ['car'], [['blue', []]], [],
                                                                   [])])],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['* rdf:type Put',
                           '* performedBy id_danny',
                           '* actsOnObject blue_cube',
                           '* isNextTo volvo']
        self.process(sentence, expected_result, display_statement_result=True)


    def test_01_goal_verb(self):
        logger.info("\n**** Test 1  *** ")
        logger.info("Danny wants the blue car")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group([],
                                ['Danny'],
                                [],
                                [],
                                [])],
                            [Verbal_Group(['want'],
                                [],
                                          'present simple',
                                          [Nominal_Group(['the'], ['car'], [['blue', []]], [], [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])

        expected_result = ['id_danny desires *',
                           '* involves volvo']

        self.process(sentence, expected_result, display_statement_result=True)

        logger.info("\n**** Test 1  second verb*** ")
        logger.info("Danny wants to drive the blue car")
        self.stmt.clear_statements()
        self.stmt._unclarified_ids = []
        self.stmt._statements_to_remove = []
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group([],
                                ['Danny'],
                                [],
                                [],
                                [])],
                            [Verbal_Group(['want'],
                                          [Verbal_Group(['drive'],
                                              [],
                                                        'present simple',
                                                        [Nominal_Group(['the'], ['car'], [['blue', []]], [], [])],
                                              [],
                                              [],
                                              [],
                                                        Verbal_Group.affirmative,
                                              [])],
                                          'present simple',
                                [],
                                [],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])

        expected_result = ['id_danny desires *',
                           '* rdf:type Drive',
                           '* involves volvo']

        self.process(sentence, expected_result, display_statement_result=True)


    def test_02(self):
        logger.info("\n**** Test 2  *** ")
        logger.info("my car is blue")
        sentence = Sentence(STATEMENT, "",
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
                                              [['blue', []]],
                                              [],
                                              [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['volvo hasColor blue']
        self.process(sentence, expected_result, display_statement_result=True)


    def test_03_quantifier_one_some(self):
        logger.info("\n**** test_3_quantifier_one_some *** ")
        logger.info("Jido is a robot")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group([],
                                ['Jido'],
                                [],
                                [],
                                [])],
                            [Verbal_Group(['be'],
                                [],
                                          'present simple',
                                          [Nominal_Group(['a'], ['robot'], [], [], [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        #quantifier
        sentence.sv[0].d_obj[0]._quantifier = 'SOME' # robot

        expected_result = ['id_jido rdf:type Robot']
        self.process(sentence, expected_result, display_statement_result=True)


    def test_04(self):
        logger.info("\n**** Test 4  *** ")
        logger.info("the man that I saw , has a small car")
        relative4 = Sentence(STATEMENT, "",
                             [Nominal_Group([],
                                 ['I'],
                                 [],
                                 [],
                                 [])],
                             [Verbal_Group(['see'],
                                 [],
                                           'past_simple',
                                           [Nominal_Group(['the'], ['man'], [], [], [])],
                                 [],
                                 [],
                                 [],
                                           Verbal_Group.affirmative,
                                 [])])

        sentence = Sentence(STATEMENT, "",
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
                                              [['small', []]],
                                              [],
                                              [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['* rdf:type Have',
                           '* performedBy a_man',
                           '* involves twingo']
        return self.process(sentence, expected_result, display_statement_result=True)


    def test_05(self):
        logger.info("\n**** Test 5  *** ")
        logger.info("the man that talks , has a small car")
        relative5 = Sentence(STATEMENT, "",
            [],
                             [Verbal_Group(['talk'],
                                 [],
                                           'past_simple',
                                 [],
                                 [],
                                 [],
                                 [],
                                           Verbal_Group.affirmative,
                                 [])])
        sentence = Sentence(STATEMENT, "",
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
                                              [['small', []]],
                                              [],
                                              [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])

        expected_result = ['* rdf:type Have',
                           '* performedBy a_man',
                           '* involves twingo']
        return self.process(sentence, expected_result, display_statement_result=True)


    def test_06(self):
        logger.info("\n**** Test 6  *** ")
        logger.info("I gave you the car of the brother of Danny")
        sentence = Sentence(STATEMENT,
                            "",
                            [Nominal_Group([],
                                ['I'],
                                [],
                                [],
                                [])],
                            [Verbal_Group(['give'],
                                [],
                                          'past simple',
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
                                              [])],
                                          [Indirect_Complement([],
                                              [Nominal_Group([],
                                                  ['you'],
                                                  [],
                                                  [],
                                                  [])])],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['* rdf:type Give',
                           '* performedBy SPEAKER',
                           '* actsOnObject fiat',
                           '* receivedBy myself']

        return self.process(sentence, expected_result, display_statement_result=True)


    def test_07(self):
        logger.info("\n**** Test 7  *** ")
        logger.info("I went to Toulouse")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group([],
                                ['I'],
                                [],
                                [],
                                [])],
                            [Verbal_Group(['go'],
                                [],
                                          'past simple',
                                [],
                                          [Indirect_Complement(['to'], [Nominal_Group([], ['Toulouse'], [], [], [])])],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['* rdf:type Move',
                           '* performedBy SPEAKER',
                           '* hasGoal id_toulouse',
                           '* eventOccurs PAST']
        return self.process(sentence, expected_result, display_statement_result=True)

    def test_08(self):
        logger.info("\n**** Test 8  *** ")
        logger.info("put the green bottle in the blue car")
        sentence = Sentence(IMPERATIVE, "",
            [],
                            [Verbal_Group(['place'],
                                [],
                                          'present simple',
                                          [Nominal_Group(['the'], ['bottle'], [['green', []]], [], [])],
                                          [Indirect_Complement(['in'],
                                                               [Nominal_Group(['the'], ['car'], [['blue', []]], [],
                                                                   [])])],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['SPEAKER desires *',
                           '* rdf:type Put',
                           '* performedBy myself',
                           '* actsOnObject green_bottle',
                           '* isIn volvo']

        return self.process(sentence, expected_result, display_statement_result=True)


    def test_08_relative(self):
        logger.info("\n**** Test 8 relative *** ")
        logger.info("show me the bottle that is in the twingo")
        relative8 = Sentence(STATEMENT, "",
            [],
                             [Verbal_Group(['be'],
                                 [],
                                           'past_simple',
                                 [],
                                           [Indirect_Complement(['in'],
                                                                [Nominal_Group(['the'], ['twingo'], [], [], [])])],
                                 [],
                                 [],
                                           Verbal_Group.affirmative,
                                 [])])
        sentence = Sentence(IMPERATIVE, "",
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
                                              [Nominal_Group([], ['me'], [], [], [])])],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['SPEAKER desires *',
                           '* rdf:type Show',
                           '* performedBy myself',
                           '* actsOnObject a_bottle',
                           '* receivedBy SPEAKER']

        return self.process(sentence, expected_result, display_statement_result=True)

    def test_09_this(self):
        logger.info("\n**** test_9_this  *** ")
        logger.info("this is a blue cube")
        sentence = Sentence(STATEMENT, "",
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
                                                         [['blue', []]],
                                              [],
                                              [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        #Quantifier
        sentence.sv[0].d_obj[0]._quantifier = 'SOME' # a blue cube
        expected_result = ['another_cube rdf:type Cube',
                           'another_cube hasColor blue']

        another_expected_result = ['SPEAKER focusesOn blue_cube']

        return self.process(sentence, expected_result, display_statement_result=True)


    def test_09_this_my(self):
        logger.info("\n**** test_9_this_my  *** ")
        logger.info("this is my cube")
        sentence = Sentence(STATEMENT, "",
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
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['another_cube belongsTo SPEAKER']

        another_expected_result = ['SPEAKER focusesOn blue_cube']

        return self.process(sentence, expected_result, display_statement_result=True)

    def test_10_this(self):
        logger.info("\n**** test_10_this  *** ")
        logger.info("this is on the shelf1")
        sentence = Sentence(STATEMENT, "",
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
                                                               [Nominal_Group(['the'], ['shelf1'], [], [], [])])],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['another_cube isOn shelf1']
        another_expected_result = ['SPEAKER focusesOn blue_cube']

        return self.process(sentence, expected_result, display_statement_result=True)


    def test_11_this(self):
        logger.info("\n**** test_11_this  *** ")
        logger.info("this goes to the shelf1")
        sentence = Sentence(STATEMENT, "",
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
                                                               [Nominal_Group(['the'], ['shelf1'], [], [], [])])],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['* rdf:type Move',
                           '* performedBy another_cube',
                           '* hasGoal shelf1']
        another_expected_result = [
            'SPEAKER focusesOn something']#with [* rdf:type Move, * performedBy something, * hasGoal shelf1] in the ontology
        return self.process(sentence, expected_result, display_statement_result=True)

    def test_12_this(self):
        logger.info("\n**** test_12_this  *** ")
        logger.info("this cube goes to the shelf1")
        sentence = Sentence(STATEMENT, "",
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
                                                               [Nominal_Group(['the'], ['shelf1'], [], [], [])])],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['* rdf:type Move',
                           '* performedBy another_cube',
                           '* hasGoal shelf1']

        return self.process(sentence, expected_result, display_statement_result=True)


    def test_13_this(self):
        logger.info("\n**** test_13_this  *** ")
        logger.info("this cube is blue ")
        sentence = Sentence(STATEMENT, "",
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
                                              [['blue', []]],
                                              [],
                                              [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['another_cube hasColor blue']

        return self.process(sentence, expected_result, display_statement_result=True)


    def test_14_quantifier_all_all(self):
        logger.info("\n**** test_14_quantifier_all_all  *** ")
        logger.info("Apples are fruits")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group([],
                                ['apple'], #apple is common noun. Therefore, do not capitalize.
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
                                          Verbal_Group.affirmative,
                                [])])

        #quantifier
        sentence.sn[0]._quantifier = 'ALL' # apples
        sentence.sv[0].d_obj[0]._quantifier = 'ALL' # fruits
        expected_result = ['Apple rdfs:subClassOf Fruit']

        return self.process(sentence, expected_result, display_statement_result=True)

    def test_15_quantifier_some_some(self):
        logger.info("\n**** test_15_quantifier_some_some  *** ")
        logger.info("an apple is a fruit")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group(['an'],
                                           ['apple'], #apple is common noun. Therefore, do not capitalize.
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
                                          Verbal_Group.affirmative,
                                [])])

        #quantifier
        sentence.sn[0]._quantifier = 'SOME' # apples
        sentence.sv[0].d_obj[0]._quantifier = 'SOME' # fruits
        expected_result = ['Apple rdfs:subClassOf Fruit']

        self.process(sentence, expected_result, display_statement_result=True)


    def test_15_quantifier_action_verb(self):
        logger.info("\n**** test_15_quantifier_action_verb  *** ")
        logger.info("a mango grows on a tree")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group(['a'],
                                           ['mango'], #mango is common noun. Therefore, do not capitalize.
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
                                          Verbal_Group.affirmative,
                                [])])

        #quantifier
        sentence.sn[0]._quantifier = 'SOME' # a mango
        sentence.sv[0].i_cmpl[0].gn[0]._quantifier = 'SOME' # a tree
        expected_result = ['* rdf:type Mango',
                           '* rdf:type Grow',
                           '* performedBy *',
                           '* involves *',
                           '* rdf:type Tree']

        self.process(sentence, expected_result, display_statement_result=True)


    #Action adverbs
    def test_16_adverb(self):
        logger.info("\n**** test_16_adverb *** ")
        logger.info("Danny slowly drives the blue car")
        sentence = Sentence(STATEMENT, "",
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
                                                         [['blue', []]],
                                              [],
                                              [])],
                                [],
                                          ['quickly'],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['* rdf:type Drive',
                           '* performedBy id_danny',
                           '* involves volvo',
                           '* actionQualification QUICK']
        self.process(sentence, expected_result, display_statement_result=True)


    #Verb tense approach
    def test_17_verb_tense(self):
        logger.info("\n**** test_17_verb_tense *** ")
        logger.info("Danny will drive the blue car")
        sentence = Sentence(STATEMENT, "",
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
                                                         [['blue', []]],
                                              [],
                                              [])],
                                [],
                                          ['quickly'],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['* rdf:type Drive',
                           '* performedBy id_danny',
                           '* involves volvo',
                           '* eventOccurs FUTUR']
        self.process(sentence, expected_result, display_statement_result=True)


    #Negative approach
    def test_18_negative(self):
        logger.info("Danny drives the blue car")
        sentence = Sentence(STATEMENT, "",
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
                                                         [['blue', []]],
                                              [],
                                              [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['* rdf:type Drive',
                           '* performedBy id_danny',
                           '* involves volvo']
        self.process(sentence, expected_result, display_statement_result=True)

        logger.info("\n**** test_18_negative *** ")
        self.stmt.clear_statements()
        self.stmt._unclarified_ids = []
        self.stmt._statements_to_remove = []
        logger.info("Danny doesn't drive the blue car")
        sentence = Sentence(STATEMENT, "",
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
                                                         [['blue', []]],
                                              [],
                                              [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.negative,
                                [])])
        expected_result = ['* rdf:type Drive', #REMOVE after finding *
                           '* performedBy id_danny',
                           '* involves volvo']
        self.process(sentence, expected_result, display_statement_result=True)

        logger.info("\n**** test_18_negative_bis *** ")
        logger.info("Danny is not in Toulouse")
        self.stmt.clear_statements()
        self.stmt._unclarified_ids = []
        self.stmt._statements_to_remove = []

        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group([],
                                ['Danny'],
                                [],
                                [],
                                [])],
                            [Verbal_Group(['be'],
                                [],
                                          'present simple',
                                [],
                                          [Indirect_Complement(['in'], [Nominal_Group([], ['Toulouse'], [], [], [])])],
                                [],
                                [],
                                          Verbal_Group.negative,
                                [])])
        expected_result = ['id_danny isIn *',
                           '* owl:differentFrom id_toulouse']

        self.process(sentence, expected_result, display_statement_result=True)


    def test_18_negative_relative(self):
        logger.info("\n**** test_18_negative_relative *** ")
        logger.info("Danny drives the car that is not blue")

        relative18 = Sentence("relative", "",
            [],
                              [Verbal_Group(['be'],
                                  [],
                                            'past_simple',
                                            [Nominal_Group([], [], [['blue', []]], [], [])],
                                  [],
                                  [],
                                  [],
                                            Verbal_Group.negative,
                                  [])])

        sentence = Sentence(STATEMENT, "",
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
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['* rdf:type Drive',
                           '* performedBy id_danny',
                           '* involves fiat']
        self.process(sentence, expected_result, display_statement_result=True)


    def test_19_negative(self):
        logger.info("\n**** test_19_negative *** ")
        logger.info("Jido is not a human")
        sentence = Sentence(STATEMENT, "",
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
                                          Verbal_Group.negative,
                                [])])

        #quantifier
        sentence.sv[0].d_obj[0]._quantifier = 'SOME' # Human

        expected_result = ['id_jido rdf:type ComplementOfHuman']
        self.process(sentence, expected_result, display_statement_result=True)


    def test_20_negative(self):
        logger.info("\n**** test_20_negative *** ")
        logger.info("the candy is not green")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group(['the'],
                                           ['candy'],
                                [],
                                [],
                                [])],
                            [Verbal_Group(['be'],
                                [],
                                          'present simple',
                                          [Nominal_Group([],
                                              [],
                                              [['green', []]],
                                              [],
                                              [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.negative,
                                [])])
        expected_result = ['a_candy hasColor *']
        self.process(sentence, expected_result, display_statement_result=True)


    def test_20_negative_inconsistent(self):
        logger.info("\n**** test_20_negative *** ")
        logger.info("the candy is green")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group(['the'],
                                           ['candy'],
                                [],
                                [],
                                [])],
                            [Verbal_Group(['be'],
                                [],
                                          'present simple',
                                          [Nominal_Group([],
                                              [],
                                              [['green', []]],
                                              [],
                                              [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['a_candy hasColor green']
        self.process(sentence, expected_result, display_statement_result=True)

        logger.info("\n**** test_20_negative_bis *** ")
        logger.info("the candy is red")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group(['the'],
                                           ['candy'],
                                [],
                                [],
                                [])],
                            [Verbal_Group(['be'],
                                [],
                                          'present simple',
                                          [Nominal_Group([],
                                              [],
                                              [['red', []]],
                                              [],
                                              [])],
                                [],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['a_candy hasColor red']
        self.process(sentence, expected_result, display_statement_result=True)


    def test_21_negative(self):
        logger.info("\n**** test_21_negative *** ")
        logger.info("this is not the shelf1")
        sentence = Sentence(STATEMENT, "",
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
                                          Verbal_Group.negative,
                                [])])

        expected_result = ['another_cube owl:differentFrom shelf1']
        self.process(sentence, expected_result, display_statement_result=True)


    def test_22_negative(self):
        logger.info("\n**** test_22_negative *** ")
        logger.info("Fruits are not humans")
        sentence = Sentence(STATEMENT, "",
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
                                          Verbal_Group.negative,
                                [])])


        #quantifier
        sentence.sn[0]._quantifier = 'ALL' # Fruits
        sentence.sv[0].d_obj[0]._quantifier = 'ALL' # Humans

        expected_result = ['Fruit rdfs:subClassOf ComplementOfHuman']
        self.process(sentence, expected_result, display_statement_result=True)


    def test_23_negative(self):
        logger.info("\n**** test_23_negative *** ")
        logger.info("you are not me")
        sentence = Sentence(STATEMENT, "",
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
                                          Verbal_Group.negative,
                                [])])

        expected_result = ['myself owl:differentFrom SPEAKER']
        self.process(sentence, expected_result, display_statement_result=True)


    def test_24_negative(self):
        logger.info("\n**** test_24_negative *** ")
        logger.info("the blue car is not my car")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group(['the'],
                                           ['car'],
                                           [['blue', []]],
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
                                          Verbal_Group.negative,
                                [])])

        expected_result = ['volvo owl:differentFrom volvo']
        self.process(sentence, expected_result, display_statement_result=True)


    def test_25_negative(self):
        logger.info("\n**** test_25_negative *** ")
        logger.info("I am not the brother of Danny")
        sentence = sentence = Sentence(STATEMENT,
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
                                                     Verbal_Group.negative,
                                           [])])

        expected_result = ['SPEAKER owl:differentFrom id_tom']
        self.process(sentence, expected_result, display_statement_result=True)

    """
    def test_26_subsentences(self):
        logger.info("\n**** test_26_subsentences *** ")
        logger.info("you will drive the car if you get the keys'.")
        
        subsentence = Sentence('subsentence', 'if', 
                                [Nominal_Group([],['you'],[],[],[])], 
                                [Verbal_Group(['get'], [],'present simple', 
                                    [Nominal_Group(['the'],['key'],[],[],[])], 
                                    [],
                                    [], 
                                    [] ,
                                    Verbal_Group.affirmative,
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
                                    Verbal_Group.affirmative,
                                    [subsentence])])
                                            
        expected_result = [ '* rdf:type Drive',
                            '* performedBy myself',
                            '* involves twingo',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject twingo_key']   
        self.process(sentence, expected_result, display_statement_result = True)
    

    def test_27_subsentences(self):
        logger.info("\n**** test_27_subsentences *** ")
        logger.info("learn that apple are fruits.")
        
        subsentence = Sentence('subsentence', 'that', 
                                [Nominal_Group([],['apple'],[],[],[])], 
                                [Verbal_Group(['be'], [],'present simple', 
                                    [Nominal_Group([],['fruit'],[],[],[])], 
                                    [],
                                    [], 
                                    [] ,
                                    Verbal_Group.affirmative,
                                    [])])
        #Quantifier
        subsentence.sn[0]._quantifier = 'ALL' # Apples
        subsentence.sv[0].d_obj[0]._quantifier = 'ALL' # Fruits
                                    
        sentence = Sentence('imperative', '', 
                                [],
                                [Verbal_Group(['learn'], [], 'present simple',[], [], [],[], 
                                    Verbal_Group.affirmative, 
                                    [subsentence])])
                                            
        expected_result = [ '* rdf:type Learn',
                            '* performedBy myself',
                            'SPEAKER desires *',
                            'Apple rdfs:subClassOf Fruit']
        self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_28_subsentences(self):
        logger.info("\n**** test_28_subsentences *** ")
        logger.info("I am going to toulouse when you get the small car.")
        
        subsentence = Sentence('subsentence', 'when', 
                                [Nominal_Group([],['you'],[],[],[])], 
                                [Verbal_Group(['get'], [],'present simple', 
                                    [Nominal_Group(['the'],['car'],[['small',[]]],[],[])], 
                                    [],
                                    [], 
                                    [] ,
                                    Verbal_Group.affirmative,
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
                                    Verbal_Group.affirmative,
                                    [subsentence])])
                                            
        expected_result = ['* rdf:type Move',
                            '* performedBy SPEAKER', 
                            '* hasGoal id_toulouse',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject twingo']   
                            
        self.process(sentence, expected_result, display_statement_result = True)
    
    """

    def test_29_directions(self):
        logger.info("\n**** Test 29 direction  *** ")
        logger.info("the twingo is at the left")
        sentence = Sentence(STATEMENT, "",
                            [Nominal_Group(['the'],
                                           ['twingo'],
                                [],
                                [],
                                [])],
                            [Verbal_Group(['be'],
                                [],
                                          'present simple',
                                [],
                                          [Indirect_Complement(['at'], [Nominal_Group(['the'], ['left'], [], [], [])])],
                                [],
                                [],
                                          Verbal_Group.affirmative,
                                [])])
        expected_result = ['twingo isAt location_left']
        return self.process(sentence, expected_result, display_statement_result=True)


    def process(self, sentence, expected_result, display_statement_result=False):
        #Dump resolution
        sentence = dump_resolved(sentence, self.stmt._current_speaker, 'myself', self.resolver)

        #StatementBuilder
        res, sitid = self.stmt.process_sentence(sentence)

        #Statement Safe Adder
        self.adder._unclarified_ids = self.stmt._unclarified_ids
        self.adder._statements = res
        self.adder._statements_to_remove = self.stmt._statements_to_remove
        res = self.adder.process()

        if display_statement_result:
            print("Created statements:\n" + str(res))
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

        self.oro.reset()

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
                      'red_apple hasColor red',
                      'myself_left isLeftOf myself', 'myself_left rdf:type Location',
                      'myself_right isRightOf myself', 'myself_right rdf:type Location',
                      'myself_front isFrontOf myself', 'myself_front rdf:type Location',
                      'myself_back isBackOf myself', 'myself_back rdf:type Location',
                      'TOP isTopOf myself', 'TOP rdf:type Location',
                      'BOTTOM isBottomOf myself', 'BOTTOM rdf:type Location',
                      'shelf1_front isFrontOf shelf1', 'shelf1_front rdf:type Location',
                      'green_banana_left isLeftOf green_banana', 'green_banana_left rdf:type Location',
        ])


    def test_sentence1(self):
        logger.info("\n##################### test_sentence1 ########################\n")

        ####
        stmt = "put the yellow banana on the shelf"
        ####

        expected_result = ['myself desires *',
                           '* rdf:type Put',
                           '* performedBy myself',
                           '* actsOnObject y_banana',
                           '* receivedBy shelf1']
        ###
        res = self.dialog.test('myself', stmt)
        self.assertTrue(check_results(res[0], expected_result))


    def test_sentence2(self):
        logger.info("\n##################### test_sentence2 ########################\n")

        ####
        stmt = "give me the green banana"
        ####
        expected_result = ['myself desires *',
                           '* rdf:type Give',
                           '* performedBy myself',
                           '* actsOnObject green_banana',
                           '* receivedBy myself']
        ###
        res = self.dialog.test('myself', stmt)
        self.assertTrue(check_results(res[0], expected_result))


    def test_sentence3(self):
        logger.info("\n##################### Simple statements ########################\n")

        ####
        stmt = "the yellow banana is green"
        ####
        expected_result = ['y_banana hasColor green']
        ###
        res = self.dialog.test('myself', stmt)

        ###Check ontology consistency
        self.assertFalse(self.oro.safeAdd(res[0]))
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
        logger.info("\n##################### Subclasses ########################\n")
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
        logger.info("\n##################### test_sentence5 - THIS ########################\n")
        ####
        stmt = "This is my banana"
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['y_banana belongsTo myself']
        self.assertTrue(check_results(res[0], expected_result))

        stmt = "This is a green banana" ## INCONSISTENCY -> y_banana can not be green
        ####
        res = self.dialog.test('myself', stmt)
        ###
        self.oro.safeAdd(res[0])
        #self.assertFalse(self.oro.safeAdd(res))

        stmt = "This is a fruit"
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['y_banana rdf:type Fruit']

        self.assertTrue(check_results(res[0], expected_result))

    def test_sentence6(self):
        logger.info("\n##################### test_sentence6 - it ########################\n")
        #Fill up History
        self.dialog.dialog_history = []

        ##sentence1
        stmt = "the red apple is on the big tree"
        res = self.dialog.test('myself', stmt)


        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)

        ##sentence3
        stmt = "I eat it"
        ###
        answer = "yes. I meant the green one"
        res = self.dialog.test('myself', stmt, answer)

        expected_result = ['* rdf:type Eat',
                           '* performedBy myself',
                           '* involves green_banana']

        self.assertTrue(check_results(res[0], expected_result))

    def test_sentence7(self):
        logger.info("\n##################### test_sentence7 - it ########################\n")

        #Fill up History
        self.dialog.dialog_history = []

        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)

        ##sentence3
        stmt = "I eat it"
        ###
        answer = "No. I mean the red apple"
        res = self.dialog.test('myself', stmt, answer)

        expected_result = ['* rdf:type Eat',
                           '* performedBy myself',
                           '* involves red_apple']

        self.assertTrue(check_results(res[0], expected_result))


    def test_sentence8(self):
        logger.info("\n##################### test_sentence8 - THIS NO FOCUS########################\n")
        #Fill up History
        self.dialog.dialog_history = []

        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)

        ##sentence3
        self.oro.remove(['myself focusesOn y_banana'])

        stmt = "I eat this"
        ###
        ### Expected Question: Do you mean the green banana?
        answer = "No. I mean the red apple"
        res = self.dialog.test('myself', stmt, answer)
        expected_result = ['* rdf:type Eat',
                           '* performedBy myself',
                           '* involves red_apple']

        self.oro.add(['myself focusesOn y_banana'])

        self.assertTrue(check_results(res[0], expected_result))


    def test_sentence8_bis(self):
        logger.info("\n##################### test_sentence8 bis - THIS NO FOCUS########################\n")
        #Fill up History
        self.dialog.dialog_history = []

        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)

        ##sentence3
        self.oro.remove(['myself focusesOn y_banana'])

        stmt = "I want this one"
        ###
        ### Expected Question: Do you mean the green banana?
        answer = "No. I mean the red apple"
        res = self.dialog.test('myself', stmt, answer)
        expected_result = ['myself desires *',
                           '* involves red_apple']

        self.oro.add(['myself focusesOn y_banana'])
        self.assertTrue(check_results(res[0], expected_result))

    def test_sentence8_ter(self):
        logger.info("\n##################### test_sentence8 ter - THIS NO FOCUS########################\n")
        #Fill up History
        self.dialog.dialog_history = []

        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)

        ##sentence3
        self.oro.remove(['myself focusesOn y_banana'])

        stmt = "I want this apple"
        ###
        res = self.dialog.test('myself', stmt)

        expected_result = ['myself desires *',
                           '* involves red_apple']

        self.oro.add(['myself focusesOn y_banana'])
        self.assertTrue(check_results(res[0], expected_result))


    def test_sentence9(self):
        logger.info("\n##################### test_sentence9 - OTHER ########################\n")
        #Fill up History
        self.dialog.dialog_history = []

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
        logger.info("\n##################### test_sentence9_bis - OTHER ########################\n")
        #Fill up History
        self.dialog.dialog_history = []

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
        logger.info("\n##################### test_sentence9_ter - THIS OTHER ########################\n")
        #Fill up History
        self.dialog.dialog_history = []

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
        logger.info("\n##################### test_sentence9_quater - THIS OTHER ########################\n")
        #Fill up History
        self.dialog.dialog_history = []

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
        logger.info("\n##################### test_sentence10 - SAME ########################\n")
        #Fill up History
        self.dialog.dialog_history = []

        ##sentence1
        stmt = "the red apple is on the big tree"
        res = self.dialog.test('myself', stmt)


        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)

        ##sentence3
        stmt = "I eat the same one"
        ###
        answer = "yes. I meant the green one"
        res = self.dialog.test('myself', stmt, answer)

        expected_result = ['* rdf:type Eat',
                           '* performedBy myself',
                           '* involves green_banana']

        self.assertTrue(check_results(res[0], expected_result))

    def test_sentence10_bis(self):
        logger.info("\n##################### test_sentence10_bis - SAME ########################\n")
        #Fill up History

        ##sentence1
        stmt = "the red apple is on the big tree"
        res = self.dialog.test('myself', stmt)


        ##sentence2
        stmt = "the green banana is next to the red apple"
        res = self.dialog.test('myself', stmt)

        ##sentence3
        stmt = "I eat the same apple"
        ###
        res = self.dialog.test('myself', stmt)

        expected_result = ['* rdf:type Eat',
                           '* performedBy myself',
                           '* involves red_apple']

        self.assertTrue(check_results(res[0], expected_result))


    def test_sentence11(self):
        logger.info("\n##################### test_sentence11 - MODALS ########################\n")
        #Fill up History
        self.dialog.dialog_history = []

        ##sentence1
        stmt = "I can take the green banana"
        res = self.dialog.test('myself', stmt)

        expected_result = ['* performedBy myself',
                           '* rdf:type Get',
                           '* actsOnObject green_banana']

        self.assertTrue(check_results(res[0], expected_result))

    def test_sentence11_bis(self):
        logger.info("\n##################### test_sentence11 - verbs with preposition ########################\n")
        #Fill up History
        self.dialog.dialog_history = []

        ##sentence1
        stmt = "I am looking for the green banana"
        res = self.dialog.test('myself', stmt)

        expected_result = ['* performedBy myself',
                           '* rdf:type Lookfor',
                           '* involves green_banana']

        self.assertTrue(check_results(res[0], expected_result))

    def test_sentence12(self):
        logger.info("\n##################### Check question on learning initiative ########################\n")
        #Ontolgy force missing concept
        self.oro.remove(['Crow rdfs:subClassOf Bird'])

        ##sentence1
        stmt = "A crow is a bird"
        res = self.dialog.test('myself', stmt)

        expected_result = ['Crow rdfs:subClassOf Bird']

        self.assertTrue(check_results(res[0], expected_result))
        self.assertEquals(res[1][1], "A crow is a bird. What are a crow and a bird?")

    def test_sentence13(self):
        logger.info(
            "\n##################### sentence that are neither statements, imperatives nor questions ########################\n")

        ##sentence
        stmt = "Hello"
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "Hello.")

    def test_sentence13_bis(self):
        logger.info(
            "\n##################### sentence that are neither statements, imperatives nor questions ########################\n")
        ##sentence
        stmt = "Goodbye"
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "Goodbye.")

    def test_sentence13_ter(self):
        logger.info(
            "\n##################### sentence that are neither statements, imperatives nor questions ########################\n")
        ##sentence
        stmt = "thank you"
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "You're welcome.")

    def test_sentence13_quater(self):
        logger.info(
            "\n##################### sentence that are neither statements, imperatives nor questions ########################\n")
        ##sentence
        stmt = "yes"
        res = self.dialog.test('myself', stmt)
        self.assertEquals(res[1][1], "Alright.")


    def test_sentence14(self):
        logger.info(
            "\n##################### sentence with directions LEFT , RIGHT , FRONT, BACK ########################\n")
        ##sentence
        stmt = "the yellow banana is at my left"
        res = self.dialog.test('myself', stmt)

        expected_result = ['y_banana isAt myself_left']

        self.assertTrue(check_results(res[0], expected_result))

    def test_sentence15(self):
        logger.info(
            "\n##################### sentence with directions LEFT , RIGHT , FRONT, BACK ########################\n")
        ##sentence
        stmt = "the yellow banana is at the left"
        res = self.dialog.test('myself', stmt)

        expected_result = ['y_banana isAt myself_left'] #Here left is related to the agent
        self.assertTrue(check_results(res[0], expected_result))

    def test_sentence16(self):
        logger.info(
            "\n##################### sentence with directions LEFT , RIGHT , FRONT, BACK ########################\n")
        ##sentence
        stmt = "the yellow banana is at the front of the shelf"
        res = self.dialog.test('myself', stmt)

        expected_result = ['y_banana isAt shelf1_front']

        self.assertTrue(check_results(res[0], expected_result))

    def test_sentence17(self):
        logger.info(
            "\n##################### sentence with directions LEFT , RIGHT , FRONT, BACK ########################\n")
        ##sentence
        stmt = "the green banana is at the front"
        res = self.dialog.test('myself', stmt)

        expected_result = ['green_banana isAt myself_front'] #Here front is related to the agent

        self.assertTrue(check_results(res[0], expected_result))

    def test_sentence18(self):
        logger.info("\n##################### sentence with KNOW ########################\n")
        ##sentence
        stmt = "I know the yellow banana"

        res = self.dialog.test('myself', stmt)

        expected_result = []
        self.assertTrue(res[0] == expected_result)

    def test_sentence19(self):
        logger.info("\n##################### sentence learn that########################\n")
        ##sentence
        stmt = "learn that the yellow banana is on the blue table"

        res = self.dialog.test('myself', stmt)

        expected_result = ['y_banana isOn table2']
        self.assertTrue(res[0] == expected_result)

    def test_sentence20(self):
        logger.info("\n##################### sentence learn that########################\n")
        ##sentence
        stmt = "learn that the yellow banana is next to the blue screen"
        #blue screen is unknown in the onotlogy

        res = self.dialog.test('myself', stmt)

        expected_result = ['y_banana isNextTo *']
        self.assertTrue(check_results(res[0], expected_result))

    def test_sentence21(self):
        logger.info("\n##################### sentence learn that########################\n")
        ##sentence
        stmt = "the green banana is next to the green table"
        #green table is unknown in the onotlogy
        ####
        answer = "learn it"
        #####
        res = self.dialog.test('myself', stmt, answer)

        expected_result = ['green_banana isNextTo *']
        self.assertTrue(check_results(res[0], expected_result))

    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()


"""
    The following functions are implemented for test purpose only
"""


def check_results(res, expected):
    def check_triplets(tr, te):
        tr_split = tr.split()
        te_split = te.split()

        return (not '?' in tr_split[0]) and \
               (not '?' in tr_split[2]) and \
               (tr_split[0] == te_split[0] or te_split[0] == '*') and \
               (tr_split[1] == te_split[1]) and \
               (tr_split[2] == te_split[2] or te_split[2] == '*')

    while res:
        r = res.pop()
        for e in expected:
            if check_triplets(r, e):
                expected.remove(e)
    if expected:
        logger.info("\t**** /Missing statements in result:   ")
        logger.info("\t" + str(expected) + "\n")

    return expected == res


def dump_resolved(sentence, current_speaker, current_listener, resolver):
    sentence = resolver.references_resolution(sentence,
                                              current_speaker, None, None, None)
    sentence = resolver.noun_phrases_resolution(sentence,
                                                current_speaker, None, None)
    sentence = resolver.verbal_phrases_resolution(sentence)

    return sentence


def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStatementBuilder)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBaseSentenceDialog))

    return suite


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)

    logger.addHandler(get_console_handler())
    #logger.addHandler(get_file_handler("statements.log"))

    # executing verbalization tests
    unittest.TextTestRunner(verbosity=2).run(test_suite())

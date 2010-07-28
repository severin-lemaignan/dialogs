#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import unittest

from dialog import Dialog

from resources_manager import ResourcePool

# raquel
from sentence import *
from parsing.parser import Parser

#sentence="take the blue cube."
#sentence="give me the small orange bottle."
#sentence="help me with this blueish thing."

#sentence="The bottle that is blue, is on the table"

#sentence="Could you take the blue cube?"
#sentence="Can you take my cube?"
#sentence="I want you to show me the black tape."
#sentence="Please take the blue cube."
#sentence="Please take the blue cube."
#sentence="put the grey tape next to the blue cube."
#sentence="put the tape on the table, next to the blue cube."
#sentence="put my tape in the trashbin."
#sentence="Where is the blue cube?"
#sentence="Where are the cubes?"
#sentence="What do you see?"
#sentence="Jido, I need the grey tape!"

#sentence="I want you to help the man that wants to bring me the blue car."

class TestBaseSentenceDialog(unittest.TestCase):
    """Tests the processing of simple sentence by the Dialog module.
    These sentences don't require discrimination.
    This must be tested with oro-server using the testsuite.oro.owl ontology.
    """

    def check_results(self, res, expected):
        def check_triplets(tr , te):
            tr_split = tr.split()
            te_split = te.split()
            
            return (tr_split[0] == te_split[0] or te_split[0] == '*') and\
                    (tr_split[1] == te_split[1]) and\
                    (tr_split[2] == te_split[2] or te_split[2] == '*')       
        while res:
            r = res.pop()
            for e in expected:
                if check_triplets(r, e):
                    expected.remove(e)
        return expected == res
    
    
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
                        'y_banana isOn shelf',
                        'green_banana rdf:type Banana',
                        'green_banana hasColor green',
                        'green_banana isOn table2',
                        'Fruit rdfs:subClassOf Thing',
                        'myself focusesOn y_banana'
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
                            '* receivedBy shelf']
        ###
        res = self.dialog.test('myself', stmt)
        self.assertTrue(self.check_results(res, expected_result))
        

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
        self.assertTrue(self.check_results(res, expected_result))
        

    def test_sentence3(self):
        
        print("\n##################### Simple statements ########################\n")              
                
        ####
        stmt = "the yellow banana is green"
        ####
        expected_result = ['y_banana hasColor green']
        ###
        res = self.dialog.test('myself', stmt)
        self.assertTrue(self.check_results(res, expected_result))
        self.assertFalse(oro.safeAdd(res)) #Check that we enforce consistency
    
        ####
        stmt = "the green banana is good"
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['green_banana hasFeature good']
        self.assertTrue(self.check_results(res, expected_result))
    
    def test_sentence4(self):
        
        print("\n##################### Subclasses ########################\n")
        ####
        stmt = "bananas are fruits"
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['Banana rdfs:subClassOf Fruit']
        self.assertTrue(self.check_results(res, expected_result))
        
        ####
        stmt = "A banana is a fruit"
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['Banana rdfs:subClassOf Fruit']
        self.assertTrue(self.check_results(res, expected_result))
        
    def test_sentence5(self):
        
        print("\n##################### test_sentence5 - THIS ########################\n")
        ####
        stmt = "This is my banana"
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['y_banana belongsTo myself']
        self.assertTrue(self.check_results(res, expected_result))
        
        stmt = "This is a green banana" ## ERROR -> y_banana can not be green
        ####
        res = self.dialog.test('myself', stmt)
        ###
        self.assertFalse(oro.safeAdd(res))
        
        stmt = "This is a fruit" ## ERROR -> y_banana can not be green
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['y_banana rdf:type Fruit']
        self.assertTrue(self.check_results(res, expected_result))
        

    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()
        
class TestVerbalizeDialog(unittest.TestCase):
    """Tests the verbalization features of the Dialog module.
    """
    
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.start()

    def test_verbalize1(self):
           
        print("\n##################### test_verbalize1: simple statements ########################\n")
        myP = Parser()                            
        stmt = "The cup is on the desk."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)
        
        print "\n####\n"
        
        stmt = "The green bottle is next to Joe."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)

    def test_verbalize2(self):
        
        print("\n##################### test_verbalize2: yes/no questions ########################\n")
        myP = Parser()

        stmt = "Are you a robot?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)


    def test_verbalize3(self):
        
        print("\n##################### test_verbalize3: orders ########################\n")
        myP = Parser()

        stmt = "Put the yellow banana on the shelf."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)
        
        print "\n####\n"
        
        stmt = "Give me the green banana."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)
        
        print "\n####\n"
        
        stmt = "Give the green banana to me."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)

        print "\n####\n"
        
        stmt = "Get the box which is on the table."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)
        
        print "\n####\n"

        stmt = "Get the box which is in the trashbin."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)

    def test_verbalize4(self):
        
        print("\n##################### test_verbalize4: W questions ########################\n")
        myP = Parser()
        
        stmt = "Where is the box?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)
        
        print "\n####\n"
        
        stmt = "What are you doing now?"
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)


    def test_verbalize5(self):
        
        print("\n##################### test_verbalize5 ########################\n")
        myP = Parser()
        
        stmt = "Jido, tell me where you go."
        sentence = myP.parse(stmt)
        res = self.dialog._verbalizer.verbalize(sentence)
        print '>> input: ', stmt
        print '<< output:', res
        self.assertEquals(stmt, res)
        
    def test_verbalize6(self):
        
        print("\n##################### test_verbalize6 ########################\n")
        myP = Parser()
        stmt = "Give me more information about the bottle."
        #stmt = "Give more information to me about the bottle."
        sentences = [Sentence('imperative', '', 
                    [], 
                    [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group([],['information'],['more'],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])]),
                     Indirect_Complement(['about'],[Nominal_Group(['the'],['bottle'],[],[],[])])],
                     [], [] ,'affirmative',[])])]

        res = self.dialog._verbalizer.verbalize(sentences)
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)

    def test_verbalize7(self):
        
        print("\n##################### test_verbalize7 ########################\n")
        myP = Parser()
        stmt = "Give me new information about the object."
        #stmt = "Give new information to me about the object."
        
        sentences = [Sentence('imperative', '', 
                    [], 
                    [Verbal_Group(['give'], [],'present simple', 
                    [Nominal_Group([],['information'],['new'],[],[])], 
                    [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])]),
                     Indirect_Complement(['about'],[Nominal_Group(['the'],['object'],[],[],[])])],
                     [], [] ,'affirmative',[])])]

        res = self.dialog._verbalizer.verbalize(sentences)
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)

    def test_verbalize8(self):
        
        print("\n##################### test_verbalize8 ########################\n")
        myP = Parser()
        stmt = "Which color is the bottle? Blue or yellow."
        sentences = [Sentence('w_question', 'choice', 
                        [Nominal_Group([],['color'],[],[],[])], 
                        [Verbal_Group(['be'], [],'present simple', 
                        [Nominal_Group(['the'],['bottle'],[],[],[])], 
                        [], [], [] ,'affirmative',[])]),
                    Sentence('statement', '',
                        [Nominal_Group([],[],['blue'],[],[]), 
                        Nominal_Group([],[],['yellow'],[],[])],
                        [])
                    ]
                    
        sentences[1].sn[1]._conjunction = 'OR'
        

        res = self.dialog._verbalizer.verbalize(sentences)
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)

    def test_verbalize9(self):
        
        print("\n##################### test_verbalize9 ########################\n")
        myP = Parser()
        stmt = "Where is it? On the table or on the shelf?"
        
        sentences = [Sentence('w_question', 'place',
                        [Nominal_Group([],['it'],[],[],[])], 
                        [Verbal_Group(['be'], [],'present simple', 
                        [], [], [], [] ,'affirmative',[])]),
                    Sentence('yes_no_question', '', 
                        [], 
                        [Verbal_Group([], [],'', 
                        [], 
                        [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])]),
                        Indirect_Complement(['on'],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                        [], [] ,'affirmative',[])])]
        
        sentences[1].sv[0].i_cmpl[1].nominal_group[0]._conjunction="OR"

        res = self.dialog._verbalizer.verbalize(sentences)
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)
        
    def test_verbalize10(self):
        print("\n##################### test_verbalize10 ########################\n")
        myP = Parser()
        stmt = "Is it on the table or on the shelf?"

        sentences = [Sentence('yes_no_question', '',
                        [Nominal_Group([],['it'],[],[],[])],
                        [Verbal_Group(['be'], [],'present simple',
                            [],
                            [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])]),
                             Indirect_Complement(['on'],[Nominal_Group(['the'],['shelf'],[],[],[])])],
                            [], [] ,'affirmative',[])])]
        
        sentences[0].sv[0].i_cmpl[1].nominal_group[0]._conjunction="OR"

        res = self.dialog._verbalizer.verbalize(sentences)
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)
        
    def test_verbalize11(self):
        
        print("\n##################### test_verbalize11 ########################\n")
        myP = Parser()
        stmt = "Is it on your left or on your right?"

        sentences = [Sentence('yes_no_question', '', 
                        [Nominal_Group([],['it'],[],[],[])], 
                        [Verbal_Group(['be'], [],'present simple', 
                            [], 
                            [Indirect_Complement(['on'],[Nominal_Group(['your'],['left'],[],[],[])]),
                             Indirect_Complement(['on'],[Nominal_Group(['your'],['right'],[],[],[])])],
                        [], [] ,'affirmative',[])])]
                    
        sentences[0].sv[0].i_cmpl[1].nominal_group[0]._conjunction = 'OR'
        
        
        res = self.dialog._verbalizer.verbalize(sentences)
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)    


    def test_verbalize12(self):
        
        print("\n##################### test_verbalize12 ########################\n")
        myP = Parser()

        stmt = "Where is it? Is it on your left or in front of you?"
        
        sentences = [Sentence('w_question', 'place',
                        [Nominal_Group([],['it'],[],[],[])], 
                        [Verbal_Group(['be'], [],'present simple', 
                        [], [], [], [] ,'affirmative',[])]),
                    Sentence('yes_no_question', '',
                        [Nominal_Group([],['it'],[],[],[])],
                        [Verbal_Group(['be'], [],'present simple',
                        [],
                        [Indirect_Complement(['on'],[Nominal_Group(['your'],['left'],[],[],[])]),
                        Indirect_Complement(['in+front+of'],[Nominal_Group([],['you'],[],[], [])])],
                        [], [] ,'affirmative',[])])]
        
        sentences[1].sv[0].i_cmpl[1].nominal_group[0]._conjunction="OR"

        res = self.dialog._verbalizer.verbalize(sentences)
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)    

    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()
        
        
class TestDiscriminateDialog(unittest.TestCase):
    """Tests the differents features of the Dialog module.
    This must be tested with oro-server using the testsuite.oro.owl ontology.
    """

    def check_results(self, res, expected):
        def check_triplets(tr , te):
            tr_split = tr.split()
            te_split = te.split()
            
            return (tr_split[0] == te_split[0] or te_split[0] == '*') and\
                    (tr_split[1] == te_split[1]) and\
                    (tr_split[2] == te_split[2] or te_split[2] == '*')       
        while res:
            r = res.pop()
            for e in expected:
                if check_triplets(r, e):
                    expected.remove(e)
        return expected == res
    
    
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.start()
        
        self.oro = ResourcePool().ontology_server
        
        try:
            self.oro.add(['shelf1 rdf:type Shelf',
                        'table1 rdf:type Table', 
                        'table2 rdf:type Table', 'table2 hasColor blue', 
                        'Banana rdfs:subClassOf Plant',
                        'y_banana rdf:type Banana','y_banana hasColor yellow','y_banana isOn shelf1',
                        'green_banana rdf:type Banana','green_banana hasColor green','green_banana isOn table2',
                        'ACCESSKIT rdf:type Gamebox', 'ACCESSKIT hasColor white', 'ACCESSKIT hasSize big', 'ACCESSKIT isOn table1',
                        'ORANGEBOX rdf:type Gamebox', 'ORANGEBOX hasColor orange', 'ORANGEBOX hasSize big', 'ORANGEBOX isOn ACCESSKIT',
                        'MYBOX rdf:type Gamebox', 'MYBOX hasColor orange', 'MYBOX hasSize small', 'MYBOX isOn ACCESSKIT',
                        'SPACENAVBOX rdf:type Gamebox', 'SPACENAVBOX hasColor white', 'SPACENAVBOX hasSize big', 'SPACENAVBOX isOn ACCESSKIT',
                        'y_bottle rdf:type Bottle', 'y_bottle isLocated RIGHT',
                        'r_bottle rdf:type Bottle', 'r_bottle isLocated FRONT',
                        'b_bottle rdf:type Bottle', 'b_bottle isLocated BACK'
                        ])
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass

    def test_discriminate1(self):
        """ Color discriminant should be found"""
        
        print("\n##################### test_discriminate1 ########################\n")
        ####
        stmt = "the banana is good"
        answer = "the green one"
        ####
        res = self.dialog.test('myself', stmt, answer)
        expected_result = ['green_banana hasFeature good']
        self.assertTrue(self.check_results(res, expected_result))
    

    def test_discriminate2(self):
        """ Color discriminant should be found"""
        
        print("\n##################### test_discriminate2 ########################\n")
        ####
        stmt = "the banana is good"
        answer = "the yellow one"
        ####
        res = self.dialog.test('myself', stmt, answer)
        expected_result = ['y_banana hasFeature good']
        self.assertTrue(self.check_results(res, expected_result))
        
    def test_discriminate3(self):
        """ Color discriminant should be found"""
        
        print("\n##################### test_discriminate3 ########################\n")
        ####
        stmt = "give me the banana"
        answer = "the green one"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Give',
                            '* performedBy myself',
                            '* actsOnObject green_banana',
                            '* receivedBy myself']
        ###
        res = self.dialog.test('myself', stmt, answer)
        print res
        self.assertTrue(self.check_results(res, expected_result))
        
        
    def test_discriminate4(self):
        """No ambiguity."""
        
        print("\n##################### test_discriminate4 ########################\n")
        ####
        stmt = "get the gamebox which is on the table"
        answer = None
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject MYBOX',
                            '* receivedBy myself']
        ###
        res = self.dialog.test('myself', stmt, answer)
        print res
        self.assertTrue(self.check_results(res, expected_result))
        
    def test_discriminate5(self):
        """ Size discriminant should be found """

        print("\n##################### test_discriminate5 ########################\n")
        ####
        stmt = "get the orange gamebox"
        answer = "the big one"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject ORANGEBOX']
        ###
        res = self.dialog.test('myself', stmt, answer)
        print res
        self.assertTrue(self.check_results(res, expected_result))

    def test_discriminate6(self):
        """No complete discriminant found. More info required"""
        
        print("\n##################### test_discriminate6 ########################\n")
        ####
        stmt = "get the big gamebox"
        answer = "the orange one"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject ORANGEBOX']
        ###
        res = self.dialog.test('myself', stmt, answer)
        print res
        self.assertTrue(self.check_results(res, expected_result))


    def test_discriminate7(self):
        """ Location discriminant should be found """
        
        print("\n##################### test_discriminate7 ########################\n")
        ####
        stmt = "get the white gamebox"
        answer = "the one which is on the table1"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject ACCESSKIT']
        ###
        res = self.dialog.test('myself', stmt, answer)
        print res
        self.assertTrue(self.check_results(res, expected_result))
    
    def test_discriminate8(self):
        """ Location wrt robot discriminant should be found """
        
        print("\n##################### test_discriminate8 ########################\n")
        ####
        stmt = "get the bottle"
        answer = "the one which is in front of you"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject r_bottle']
        ###
        res = self.dialog.test('myself', stmt, answer)
        print res
        self.assertTrue(self.check_results(res, expected_result))

    def test_discriminate9(self):
        print("\n##################### Class grounding ########################\n")
        ####
        stmt = "a fruit is a plant"
        answer = "a kind of thing"
        ####
        expected_result = [ 'Plant rdfs:subClassOf Thing', 'Fruit rdfs:subClassOf Plant' ]
        ###
        res = self.dialog.test('myself', stmt, answer)
        self.assertTrue(self.check_results(res, expected_result))

    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()


class TestISUDialog(unittest.TestCase):
    """Tests the differents features of the Dialog module.
    This must be tested with oro-server using the testsuite.oro.owl ontology.
    """

    def check_results(self, res, expected):
        def check_triplets(tr , te):
            tr_split = tr.split()
            te_split = te.split()
            
            return (tr_split[0] == te_split[0] or te_split[0] == '*') and\
                    (tr_split[1] == te_split[1]) and\
                    (tr_split[2] == te_split[2] or te_split[2] == '*')       
        while res:
            r = res.pop()
            for e in expected:
                if check_triplets(r, e):
                    expected.remove(e)
        return expected == res
    
    
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.start()
        
        self.oro = ResourcePool().ontology_server
        
        try:
            
            self.oro.add(['ACHILE_HUMAN1 rdf:type Human', 'HRP2TABLE rdf:type Table',
                        'BLUE_TRASHBIN rdf:type Trashbin',
                        'PINK_TRASHBIN rdf:type Trashbin',
                        'BLACK_TAPE rdf:type VideoTape', 'BLACK_TAPE isIn BLUE_TRASHBIN',
                        'GREY_TAPE rdf:type VideoTape', 'GREY_TAPE isOn HRP2TABLE'])
                        
            self.oro.addForAgent('ACHILE_HUMAN1',
                        ['BLUE_TRASHBIN rdf:type Trashbin',
                        'PINK_TRASHBIN rdf:type Trashbin',
                        'BLACK_TAPE rdf:type VideoTape', 'BLACK_TAPE isIn PINK_TRASHBIN',
                        'GREY_TAPE rdf:type VideoTape', 'GREY_TAPE isOn HRP2TABLE'])
                        
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass

    def test_ISU1(self):
        """"""
        
        print("\n##################### test_discriminate1 ########################\n")
        ####
        stmt = "give me the videotape which is in the PINK_TRASHBIN."
        answer = None
        ####
        res = self.dialog.test('ACHILE_HUMAN1', stmt, answer)
         
        expected_result = ['* rdf:type Give',
                            '* performedBy myself',
                            'ACHILE_HUMAN1 desires *',
                            '* actsOnObject BLACK_TAPE'
                            '* receivedBy ACHILE_HUMAN1']

        self.assertTrue(self.check_results(res, expected_result))
    

    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()

        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format="%(message)s")
    
    # all tests
    #unittest.main()
    """
    # executing only some tests
    suiteSimpleSentences = unittest.TestSuite()
    suiteSimpleSentences.addTest(TestBaseSentenceDialog('test_sentence1'))
    suiteSimpleSentences.addTest(TestBaseSentenceDialog('test_sentence2'))
    suiteSimpleSentences.addTest(TestBaseSentenceDialog('test_sentence3'))
    #suiteSimpleSentences.addTest(TestBaseSentenceDialog('test_sentence4'))
    #suiteSimpleSentences.addTest(TestBaseSentenceDialog('test_sentence5'))
    
    suiteVerbalization = unittest.TestSuite()
    suiteVerbalization.addTest(TestVerbalizeDialog('test_verbalize1'))
    suiteVerbalization.addTest(TestVerbalizeDialog('test_verbalize2'))
    suiteVerbalization.addTest(TestVerbalizeDialog('test_verbalize3'))
    suiteVerbalization.addTest(TestVerbalizeDialog('test_verbalize4'))
    #suiteVerbalization.addTest(TestVerbalizeDialog('test_verbalize5'))
    suiteVerbalization.addTest(TestVerbalizeDialog('test_verbalize10'))
    """
    suiteDiscriminate = unittest.TestSuite()
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate1'))
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate2'))
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate3'))
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate4'))
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate5'))
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate6'))
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate7'))
    suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate8'))
    #suiteDiscriminate.addTest(TestDiscriminateDialog('test_discriminate9'))
    """
    suiteISU = unittest.TestSuite()
    suiteISU.addTest(TestISUDialog('test_ISU1'))
    """
    #unittest.TextTestRunner(verbosity=2).run(suiteSimpleSentences)
    #unittest.TextTestRunner(verbosity=2).run(suiteVerbalization)
    unittest.TextTestRunner(verbosity=2).run(suiteDiscriminate)
    #unittest.TextTestRunner(verbosity=2).run(suiteISU)


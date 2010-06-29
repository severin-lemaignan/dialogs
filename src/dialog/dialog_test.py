#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import unittest

from dialog import Dialog

from pyoro import Oro

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

class TestDialog(unittest.TestCase):
    """Tests the differents features of the Dialog module.
    This must be tested with oro-server using the testsuite.oro.owl ontology.
    """

    def check_results(self, res, expected):
        for c in zip(expected, res):
            for d in zip(c[0].split(), c[1].split()):
                if not d[0] == '*':
                    if d[0] != d[1]:
                        return False
        return True
    
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.start()
        
        self.oro = Oro('localhost', 6969)
        
        self.oro.add(['shelf rdf:type Shelf',
                    'table1 rdf:type Table', 
                    'table2 rdf:type Table', 
                    'table2 hasColor blue', 
                    'Banana rdfs:subClassOf Plant',
                    'banana rdf:type Banana',
                    'banana hasColor yellow',
                    'banana isOn shelf',
                    'green_banana rdf:type Banana',
                    'green_banana hasColor green',
                    'green_banana isOn table2',
                    'ACCESSKIT rdf:type Box', 'ACCESSKIT hasColor white', 'ACCESSKIT hasSize big',
                    'ORANGEBOX rdf:type Box', 'ORANGEBOX hasColor orange', 'ORANGEBOX hasSize big',
                    'MYBOX rdf:type Box', 'MYBOX hasColor orange', 'MYBOX hasSize small',
                    'SPACENAVBOX rdf:type Box', 'SPACENAVBOX hasColor white'
                    ])

    def test_sentence1(self):

        print("\n##################### test_sentence1 ########################\n")
        
        ####
        stmt = "put the yellow banana on the shelf"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Place',
                            '* performedBy myself',
                            '* actsOnObject banana',
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
        
        print("\n##################### test_sentence3 ########################\n")
        ####
        stmt = "the yellow banana is big"
        ####
        expected_result = ['banana hasSize big']
        ###
        res = self.dialog.test('myself', stmt)
        self.assertTrue(self.check_results(res, expected_result))
    
    
    def test_sentence4(self):
        
        print("\n##################### test_sentence4 ########################\n")
        ####
        stmt = "the green banana is good"
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = ['green_banana hasFeature good']
        self.assertTrue(self.check_results(res, expected_result))
   
    
    def test_sentence5(self):
        
        print("\n##################### test_sentence5 ########################\n")
        ####
        stmt = "the banana is good"
        answer = "the green one"
        ####
        res = self.dialog.test('myself', stmt, answer)
        expected_result = [ 'green_banana hasFeature good']
        self.assertTrue(self.check_results(res, expected_result))
    

    def test_sentence6(self):
        
        print("\n##################### test_sentence6 ########################\n")
        ####
        stmt = "the banana is good"
        answer = "the yellow one"
        ####
        res = self.dialog.test('myself', stmt, answer)
        expected_result = [ 'banana hasFeature good']
        self.assertTrue(self.check_results(res, expected_result))
        
    def test_sentence7(self):
        
        print("\n##################### test_sentence7 ########################\n")
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

       
    def test_verbalize1(self):
        
        print("\n##################### test_verbalize1 ########################\n")
        myP = Parser()
                            
        stmt = "the cup is on the desk"
        sentence = myP.parse(stmt.split())
        res = self.dialog._verbalizer.verbalize(sentence[0])
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)

    def test_verbalize2(self):
        
        print("\n##################### test_verbalize2 ########################\n")
        myP = Parser()
        stmt = "the green bottle is next to Joe"
        sentence = myP.parse(stmt.split())
        res = self.dialog._verbalizer.verbalize(sentence[0])
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)

    def test_verbalize3(self):
        
        print("\n##################### test_verbalize3 ########################\n")
        myP = Parser()
        stmt = "give me the green banana"
        expected_result = "give the green banana to me"
        sentence = myP.parse(stmt.split())
        res = self.dialog._verbalizer.verbalize(sentence[0])
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(expected_result, res)
        
    def test_verbalize4(self):
        
        print("\n##################### test_verbalize4 ########################\n")
        myP = Parser()
        stmt = "put the yellow banana on the shelf"
        sentence = myP.parse(stmt.split())
        res = self.dialog._verbalizer.verbalize(sentence[0])
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)

    def test_verbalize5(self):
        
        print("\n##################### test_verbalize5 ########################\n")
        myP = Parser()
        stmt = "give the green banana to me"
        #stmt = "give me the green banana"
        sentence = myP.parse(stmt.split())
        res = self.dialog._verbalizer.verbalize(sentence[0])
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)


    def test_discrimanate1(self):
        
        print("\n##################### test_discrimanate1 ########################\n")
        ####
        stmt = "get the box on the table"
        answer = "the orange one"
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
        
    def test_discrimanate2(self):
        
        print("\n##################### test_discrimanate1 ########################\n")
        ####
        stmt = "get the orange box"
        answer = "the one on ACCESSKIT"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject ORANGEBOX',
                            '* receivedBy myself']
        ###
        res = self.dialog.test('myself', stmt, answer)
        print res
        self.assertTrue(self.check_results(res, expected_result))

    def test_discrimanate3(self):
        
        print("\n##################### test_discrimanate3 ########################\n")
        ####
        stmt = "get the orange box"
        answer = "the small one"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject ORANGEBOX',
                            '* receivedBy myself']
        ###
        res = self.dialog.test('myself', stmt, answer)
        print res
        self.assertTrue(self.check_results(res, expected_result))


    def test_discrimanate4(self):
        
        print("\n##################### test_discrimanate4 ########################\n")
        ####
        stmt = "get the big box"
        answer = "get the big orange box"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Get',
                            '* performedBy myself',
                            '* actsOnObject ORANGEBOX',
                            '* receivedBy myself']
        ###
        res = self.dialog.test('myself', stmt, answer)
        print res
        self.assertTrue(self.check_results(res, expected_result))


    def test_discrimanate5(self):
        
        print("\n##################### test_discrimanate5 ########################\n")
        ####
        stmt = "get me the yellow banana that is on the shelf ,"
        #answer = "get the big orange box"
        ####
        expected_result = [ 'myself desires *',
                            '* rdf:type Banana',
                            '* isOn shelf']
        ###
        res = self.dialog.test('myself', stmt)
        print res
        self.assertTrue(self.check_results(res, expected_result))

    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()
        
        self.oro.close()
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format="%(message)s")
    
    # all tests
    #unittest.main()
    
    # executing only some tests
    suiteFew = unittest.TestSuite()
    #suiteFew.addTest(TestDialog("test_sentence1"))
    #suiteFew.addTest(TestDialog("test_sentence3"))
    #suiteFew.addTest(TestDialog("test_sentence7"))
    #suiteFew.addTest(TestDialog("test_verbalize5"))
    suiteFew.addTest(TestDialog("test_discrimanate5"))
    unittest.TextTestRunner(verbosity=2).run(suiteFew)

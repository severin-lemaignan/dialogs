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
        
        self.oro.add([   'shelf rdf:type Shelf',
                    'table1 rdf:type Table', 
                    'table2 rdf:type Table', 
                    'table2 hasColor blue', 
                    'Banana rdfs:subClassOf Plant',
                    'banana rdf:type Banana',
                    'banana hasColor yellow',
                    'green_banana rdf:type Banana',
                    'green_banana hasColor green'])

    def test_sentence1(self):

        print("\n#############################################\n")
        
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
        
        print("\n#############################################\n")

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
        
        print("\n#############################################\n")
        ####
        stmt = "the yellow banana is big"
        ####
        expected_result = [ 'banana hasSize big']
        ###
                            
        res = self.dialog.test('myself', stmt)

        self.assertTrue(self.check_results(res, expected_result))
    
    def test_sentence4(self):
        
        print("\n#############################################\n")
        ####
        stmt = "the yellow banana is good"
        ####
        res = self.dialog.test('myself', stmt)
        ###
        expected_result = [ 'banana hasFeature good']
        ###
    

        self.assertTrue(self.check_results(res, expected_result))
   
        
    def test_verbalize1(self):
        
        print("\n#############################################")
        print('-------- verbalize ----------\n')
        myP = Parser()
                            
        stmt = "the cup is on the desk"
        sentence = myP.parse(stmt.split())
        res = self.dialog._verbalizer.verbalize(sentence[0])
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)

        stmt = "the green bottle is next to Joe"
        sentence = myP.parse(stmt.split())
        res = self.dialog._verbalizer.verbalize(sentence[0])
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)

        stmt = "give me the green banana"
        expected_result = "give the green banana to me"
        sentence = myP.parse(stmt.split())
        res = self.dialog._verbalizer.verbalize(sentence[0])
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(expected_result, res)
        
        stmt = "put the yellow banana on the shelf"
        sentence = myP.parse(stmt.split())
        res = self.dialog._verbalizer.verbalize(sentence[0])
        print 'input: ', stmt
        print 'output:', res
        self.assertEquals(stmt, res)

        #sentence = Sentence('w_question',
                            #'place',
                            #[Nominal_Group(['the'],  ['son'],['old','big'],
                                            #[Nominal_Group(['my'],['aunt'],None,None,None)], None),
                             #Nominal_Group(['the'],  ['father'],[],None, None)],
                            #Verbal_Group(['be'], None,'present simple',None, None,['today'], None, None, None))
        #self.dialog._verbalizer.verbalize(sentence)


    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()
        
        self.oro.close()
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                    format="%(message)s")
    
    unittest.main()

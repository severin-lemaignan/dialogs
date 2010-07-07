#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import unittest

from statements_builder import NominalGroupStatementBuilder
from statements_builder import VerbalGroupStatementBuilder
from pyoro import Oro
from resources_manager import ResourcePool

from dialog_exceptions import DialogError
from dialog_exceptions import GrammaticalError


class QuestionHandler:
	
	def __init__(self, current_speaker = None):
		self._sentence = None
		self._statement = None
		self._current_speaker = current_speaker
		#This field takes the value True or False when processing a Yes-No-question 
		#		and takes a list of returned values from the ontology when processing a Wh-question 
		self._answer = None
		
		
	def process_sentence(self, sentence):
		"""
		if not sentence.resolved():
		raise DialogError("Trying to process an unresolved sentence!")
		
		self._sentence = sentence
		"""
		self._sentence = dump_resolved(sentence, self._current_speaker, 'myself')#TODO: dumped_resolved is only for the test of query builder. Need to be replaced as commented above
		#Case the question is a Y_n_question
		if sentence.data_type == 'y_n_question':
			self._answer = self.process_y_n_question(sentence)
		#Case the question is a wh-question
		if sentence.data_type == 'w_question':
			#Case the question is about the subject
			#Case the question is about the verb
			#Case the question is about the 
			self.process_w_question(sentence)
	
		
	def process_y_n_question(self, sentence):
		oro = Oro("localhost", 6969)
		builder = Sta


	"""		
	case:
		y_n_question
		Do
		can
		must
		
		
		e.g.  Do you know Ramses 
			  -> yes, I do
			  Can I you give me a bottle?
			  -> yes, I can  No, I cannot
	
	
	
	Case: Wh-Question => data_type = w_question
		see http://www.eslgold.com/grammar/wh_questions.html
		
		
		what aim => 'thing'
			what kind => aim = 'thing', sn = [the kind of]
			what type => aim = 'thing' , sn = [the type of]
			what time => aim = 'time'
		which aim => 'choice'
		when  aim => 'date'
		where aim => 'Place'
			where (from) => 'origin'
		why   aim => 'purpose'
		who   aim => 'person'
		whose aim => 'owner'
		whom  aim => 'person'
		how   aim => 'place'
			how long  => aim = 'duration'
			how far   => aim = 'distance'
 			how often => aim = 'Frequency'
 			How much  => aim = 'Quantity'
			How many  => aim = 'Quantity'
	"""	

def setUp():

	""" We want to process the following questions:
	#sentence="Where is the blue cube?"
	#sentence="Where are the cubes?"
	#sentence="What do you see?"
	#sentence="Could you take the blue cube?"
	#sentence="Can you take my cube?"
	"""
	oro = Oro("localhost", 6969)
	oro.add(['SPEAKER rdf:type Human', 'SPEAKER rdfs:label "Patrick"',
			 
			 'blue_cube rdf:type Cube',
			 'blue_cube hasColor blue',
			 'blue_cube isOn table1',
			 'another_cube isOn shelf1',
			 'another_cube belongsTo SPEAKER'
			 
			 'shelf1 rdf:type Shelf',
			 'table1 rdf:type Table',
			 
			 'see_shelf rdf:type See',
			 'see_shelf performedBy myself',
			 'see_shelf involves shelf1',
			 
			 'take_blue_cube canBePerformedBy myself',
			 'take_blue_cube rdf:type Take',
			 'take_blue_cube involves blue_cube',
			 
			 'take_my_cube canBePerformedBy SPEAKER',
			 'take_my_cube involves another_cube',
			 'take_my_cube rdf:type Take'])
	oro.close()
	

def test_w_question_1():
	print "*************  test_w_question_1 ******************"
	print "Where is the blue cube?"
	sentence = Sentence("w_question", "location", 
                         [Nominal_Group(['the'],
                                        ['cube'],
                                        ['blue'],
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
	statement_query = ['blue_cube isOn ?concept']
	expected_result = ['table1']
	test(sentence , statement_query, expected_result)
	
def test_w_question_2():
	print "*************  test_w_question_2 ******************"
	print "Where is the cube?"
	sentence = Sentence("w_question", "location", 
                         [Nominal_Group(['the'],
                                        ['cube'],
                                        [''],
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
	#TODO:Discriminate the right cube.2 possibles answers are expected here.
	#We are not discriminating here.
	statement_query = ['blue_cube isOn ?concept']
	expected_result = ['table1']
	
	#statement_query = ['another_cube isOn ?concept']
	#expected_result = ['shelf1']
	
	test(sentence , statement_query, expected_result)


def test_w_question_3():
	print "*************  test_w_question_2 ******************"
	print "What do you see?"
	sentence = Sentence("w_question", "thing", 
                         [Nominal_Group([],
                                        ['you'],
                                        [''],
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
	#TODO:there might be severals action ID that are instances of See
	# ?Concept may hold several results 
	statement_query = ['* rdf:type See',
					   '* performedBy myself',
					   '* involves ?concept']
	expected_result = ['shelf1']
	
	test(sentence , statement_query, expected_result)




def test_y_n_question_1():
	print "*************  test_y_n_question_1 ******************"
	print "Could you take the blue cube?"
	sentence = Sentence("y_n_question", "", 
                         [Nominal_Group([],
                                        ['you'],
                                        [''],
                                        [],
                                        [])],                                         
                         [Verbal_Group(['Can+Take'],
                                       [],
                                       'present_simple',
                                       [Nominal_Group(['the'],
                                                      ['cube'],
				                                      ['blue'],
				                                      [],
				                                      [])],
                                       [],
                                       [],
                                       [],
                                       'affirmative',
                                       [])])
	statement_query = ['* rdf:type Take',
					   '* canBePerformedBy myself',
					   '* involves blue_cube']
	expected_result = True
	
	test(sentence , statement_query, expected_result)



def test(sentence , statement_query, expected_result):
	qhandler = QuestionHandler("SPEAKER")
	res = qhandler.process_sentence(sentence)
	print res
	
	
def dump_resolved(sentence, current_speaker, current_recipient):
	return


def unit_tests():
	"""This function tests the main features of the class QuestionHandler"""
	
	print("This is a test...")
	
	test_w_question_1()
	test_w_question_2()
	test_w_question_3()
	test_y_n_question_1()

if __name__ == '__main__':
	unit_tests()

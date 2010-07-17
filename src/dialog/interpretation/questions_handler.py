#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import unittest
from resolution import Resolver
from statements_builder import StatementBuilder
from statements_builder import NominalGroupStatementBuilder
from statements_builder import VerbalGroupStatementBuilder
from sentence import *
from resources_manager import ResourcePool
from pyoro import OroServerError
from dialog_exceptions import DialogError
from dialog_exceptions import GrammaticalError


class QuestionHandler:
	
	def __init__(self, current_speaker = None):
		self._sentence = None
		self._statements = []
		self._current_speaker = current_speaker
		
		#This field takes the value True or False when processing a Yes-No-question 
		#		and takes a list of returned values from the ontology when processing a w_question 
		self._answer = False
	
	
	def clear_statements(self):
		self._statements = []
	
	
	def process_sentence(self, sentence):
		
		if not sentence.resolved():
			raise DialogError("Trying to process an unresolved sentence!")	
		
		self._sentence = sentence
		
		#StatementBuilder
		builder = StatementBuilder(self._current_speaker)
		self._statements = builder.process_sentence(self._sentence)
		logging.info("statement from Statement Builder: " + str(self._statements))
		
		#Case the question is a y_n_question
		if sentence.data_type == 'yes_no_question':
			self._statements = self._resolve_action_verb_reference(self._statements)
			logging.debug("Checking on the ontology: check(" + str(self._statements) + ")")
			
			self._answer = ResourcePool().ontology_server.check(self._statements)
			
		#Case the question is a w_question		
		if sentence.data_type == 'w_question':
			self._statements = self._extend_statement_from_sentence_aim(self._statements)
			self._statements =  self._remove_statements_with_no_unbound_tokens(self._statements)
			logging.debug("Searching the ontology: find(?concept, " + str(self._statements) + ")")
			
			self._answer = ResourcePool().ontology_server.find('?concept', self._statements)
		
		return self._answer
		
	def _resolve_action_verb_reference(self, statements):
		stmts = []
		try: 
			sit_id = ResourcePool().ontology_server.find('?event', statements)
			if sit_id:
				logging.debug("\t/Found a staticSituation matching the yes_no_question query to be checked: "+ str(sit_id))
				for s in statements:
					#TODO:the ontology might find severals sit ID matching the query. Should we take this consideration?
					#The longer the query, the better the result of sit_id
					stmts.append(s.replace('?event', sit_id[0]))
		except OroServerError:
			stmts = statements
			
		return stmts
	
	
	def _extend_statement_from_sentence_aim(self, current_statements):
		#Case: the statement is complete from statement builder e.g: what is in the box? =>[?concept isIn ?id_box, ?id_box rdf:type Box]
		for s in current_statements:
			if '?concept' in s.split():
				return current_statements
		#case: the statement is partially build from; statement builder
		stmts = []
		for sn in self._sentence.sn:
			for sv in self._sentence.sv:	
				for verb in sv.vrb_main:
					if verb.lower() == 'be':
						stmts.append(sn.id + self.get_role_from_sentence_aim(verb) +'?concept')
					else:
						stmts.append('?event' + self.get_role_from_sentence_aim(verb) +'?concept')
		return current_statements + stmts
	
	
	def get_role_from_sentence_aim(self, verb):
		#'What-question':
		#	Case 
		#		e.g: what do you see? 
		#		append in statement [?event involves ?concept]
		#	Case
		#		e.g: what is a cube?
		#		append in statement [id_cube rdf:type ?concept]
		#	Case
		#		e.g: what is 'in' the blue cube?
		#		append in statement []
		
		
		
		
		#TODO:See how to use resourcePool in order to perform the line below
		#has_goal = get_all_verb_from_resource_pool_where(object_property = 'hasGoal')
		has_goal = ['go','put']#TODO: Replace this line by the above one, when complete
		
		#TODO:See how to use resourcePool in order to perform the line below
		#acts_on_object = get_all_verb_from_resource_pool_where(object_property = 'acts_on_object')
		acts_on_object = ['put', 'give', 'show']#TODO: Replace this line by the above one, when complete
		
		#TODO in resource pool: Create dictionary files
		#Dictionary for sentence.aim = 'place' 
		dic_place={'be':'isAt',  
				   None:'receivedBy',
				   'has_goal':'hasGoal'}
		#Dictionary for sentence.aim = 'thing' 
		dic_thing={'be':'rdf:type', 
				   None:'involves',
				   'acts_on_object':'actsOnObject'}
		
		#Dictionary for sentence.aim = 'aim' 
		dic_manner={'be':'?sub_feature'}
		
		#TODO:With dictionary from resource pool
		#dic_aim = resourcePool.Dictionary(dic_aim)
		#Dictionary for all
		dic_aim = {'thing':dic_thing,
				   'place':dic_place,
				   'manner':dic_manner}
		
		if verb in has_goal:
			role = dic_aim[self._sentence.aim]['has_goal']
			
		elif verb in acts_on_object:
			role = dic_aim[self._sentence.aim]['acts_on_object']
			
		elif verb.lower() == 'be':
			role = dic_aim[self._sentence.aim][verb.lower()]
		else:
			role = dic_aim[self._sentence.aim][None]
			
		
		return (' ' + role + ' ')
	
	
	"""			
		what aim => 'thing'
			what kind => aim = 'thing', sn = [the kind of]
			what type => aim = 'thing' , sn = [the type of]
			what time => aim = 'time'
		which aim => 'choice'
		when  aim => 'date'
		where aim => 'Place'
			where (from) => 'origin'
		why   aim => 'reason'
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

	
	def _remove_statements_with_no_unbound_tokens(self, statements):
		stmts = []
		for s in statements:
			if '?' in s:
				stmts.append(s)
				
		return stmts
	
	
class TestQuestionHandler(unittest.TestCase):
	def setUp(self):
	
		""" We want to process the following questions:
		#sentence="Where is the blue cube?"
		#sentence="Where are the cubes?"
		#sentence="What do you see?"
		#sentence="Could you take the blue cube?"
		#sentence="Can you take my cube?"
		#sentence="What is this?
		#sentence="what object do you see?"
		#sentence="what do I see?
		#sentence="what is blue?"
		#sentence="what is reachable?"
		"""
		"""Further test
		#what did I give you?
		#who has a small car?
		#how is my bottle?
		#what does Danny drive?
		"""
		ResourcePool().ontology_server.add(['SPEAKER rdf:type Human', 'SPEAKER rdfs:label "Patrick"',
				 
				 'blue_cube rdf:type Cube',
				 'blue_cube hasColor blue',
				 'blue_cube isOn table1',
				 'another_cube rdf:type Cube',
				 'another_cube isOn shelf1',
				 'another_cube belongsTo SPEAKER',
				 'another_cube hasSize small',
				 
				 'shelf1 rdf:type Shelf',
				 'table1 rdf:type Table',
				 
				 'see_shelf rdf:type See',
				 'see_shelf performedBy myself',
				 'see_shelf involves shelf1',
				 
				 'take_blue_cube performedBy myself',
				 'take_blue_cube rdf:type Get',
				 'take_blue_cube actsOnObject blue_cube',
				 
				 'take_my_cube canBePerformedBy SPEAKER',
				 'take_my_cube involves another_cube',
				 'take_my_cube rdf:type Take',
				 
				 'SPEAKER focusesOn another_cube'])
		
		
		self.qhandler = QuestionHandler("SPEAKER")
	
	def test_1_w_question(self):
		print "\n*************  test_1_w_question ******************"
		print "Where is the blue cube?"
		sentence = Sentence("w_question", "place", 
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
		self.process(sentence , statement_query, expected_result)
		
	def test_2_w_question(self):
		print "\n*************  test_2_w_question ******************"
		print "Where is the small cube?"
		sentence = Sentence("w_question", "place", 
	                         [Nominal_Group(['the'],
	                                        ['cube'],
	                                        ['small'],
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
		statement_query = ['another_cube isOn ?concept']
		expected_result = ['shelf1']
		
		self.process(sentence , statement_query, expected_result)
	
	
	def test_3_w_question(self):
		print "\n*************  test_3_w_question ******************"
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
		
		self.process(sentence , statement_query, expected_result)
	
	def test_8_w_question(self):
		print "\n*************  test_8_w_question ******************"
		print "what is blue?"
		sentence = Sentence("w_question", "thing", 
	                         [Nominal_Group([],
	                                        [],
	                                        ['blue'],
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
		statement_query = ['?concept hasColor blue']
		expected_result = ['blue_cube']		
		self.process(sentence , statement_query, expected_result) 
		
		
	
	def test_9_w_question_this(self):
		print "\n*************  test_9_w_question_this ******************"
		print "what is this?"
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
		statement_query = ['SPEAKER focusesOn ?concept']
		expected_result = ['another_cube']		
		self.process(sentence , statement_query, expected_result) 
		
	
	"""
	
	def test_4_y_n_question(self):
		print "\n*************  test_4_y_n_question action verb******************"
		print "Did you get the blue cube?"
		sentence = Sentence("yes_no_question", "", 
	                         [Nominal_Group([],
	                                        ['you'],
	                                        [''],
	                                        [],
	                                        [])],                                         
	                         [Verbal_Group(['get'],
	                                       [],
	                                       'past_simple',
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
		statement_query = ['* rdf:type Get',
						   '* performedBy myself',
						   '* actsOnObject blue_cube']
		expected_result = True		
		self.process(sentence , statement_query, expected_result)
		
		
	def test_5_y_n_question(self):
		print "\n*************  test_5_y_n_question verb to be followed by complement******************"
		print "Is the blue cube on the table?"
		sentence = Sentence("yes_no_question", "", 
	                         [Nominal_Group(['the'],
	                                        ['cube'],
	                                        ['blue'],
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
		statement_query = ['blue_cube isOn table1']
		expected_result = True		
		self.process(sentence , statement_query, expected_result)
	
	
	def test_6_y_n_question(self):
		print "\n*************  test_6_y_n_question verb to be not followed by complement and sentence resolved******************"
		print "Is the cube blue?"
		sentence = Sentence("yes_no_question", "", 
	                         [Nominal_Group(['the'],
	                                        ['cube'],
	                                        ['blue'],
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
		statement_query = []
		expected_result = True		
		self.process(sentence , statement_query, expected_result)
		
	
	def test_7_y_n_question(self):
		print "\n*************  test_7_y_n_question verb to be ******************"
		print "Is my cube on the table1?"
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
		statement_query = ['another_cube isOn table1']
		expected_result = False		
		self.process(sentence , statement_query, expected_result) 
	
	"""
	
	
		
	"""
	def test_9_w_question(self):
		print "\n*************  test_9_w_question ******************"
		print "How is my car?"
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
		statement_query = ['?concept hasColor blue']
		expected_result = ['blue']		
		self.process(sentence , statement_query, expected_result) 
	"""
		
	def process(self, sentence , statement_query, expected_result):
		sentence = dump_resolved(sentence, 'SPEAKER', 'myself')#TODO: dumped_resolved is only for the test of query builder
		res = self.qhandler.process_sentence(sentence)
		logging.debug("Result: " + str(res))
		
		print "Query Statement:", str(self.qhandler._statements)
		print "Expected Result:", expected_result
		print "Result Found: ", str(self.qhandler._answer)
		
		self.qhandler.clear_statements()
		self.assertEqual(res, expected_result)

def dump_resolved(sentence, current_speaker, current_recipient = None):
	resolver = Resolver()
	#Resolution
	sentence = resolver.references_resolution(sentence,
                                              current_speaker, 
                                              None)
	
	sentence = resolver.noun_phrases_resolution(sentence,
											    current_speaker)
	sentence = resolver.verbal_phrases_resolution(sentence)
	return sentence


def unit_tests():
	"""This function tests the main features of the class QuestionHandler"""
	logging.basicConfig(level=logging.DEBUG,format="%(message)s")
	print("This is a test...")
	unittest.main()
	
	
if __name__ == '__main__':
	unit_tests()



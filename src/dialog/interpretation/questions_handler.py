#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import unittest
from resolution import Resolver
from statements_builder import StatementBuilder
from statements_builder import NominalGroupStatementBuilder
from statements_builder import VerbalGroupStatementBuilder
from sentence import *
from pyoro import Oro
from resources_manager import ResourcePool

from dialog_exceptions import DialogError
from dialog_exceptions import GrammaticalError


class QuestionHandler:
	
	def __init__(self, current_speaker = None):
		self._sentence = None
		self._statements = []
		self._current_speaker = current_speaker
		#This field takes the value True or False when processing a Yes-No-question 
		#		and takes a list of returned values from the ontology when processing a Wh-question 
		self._answer = False
		#connection to Oro
		self._oro = Oro("localhost", 6969)
		
	def process_sentence(self, sentence):
		"""
		if not sentence.resolved():
		raise DialogError("Trying to process an unresolved sentence!")
		
		self._sentence = sentence
		"""
		self._sentence = dump_resolved(sentence, self._current_speaker, 'myself')#TODO: dumped_resolved is only for the test of query builder. Need to be replaced as commented above
		
		builder = StatementBuilder(self._current_speaker)
		self._statements = builder.process_sentence(self._sentence)
		#Case the question is a y_n_question
		if sentence.data_type == 'yes_no_question':
			self._answer = self._oro.check(self._resolve_action_verb_reference(self._statements))
			
			
		#Case the question is a w_question		
		if sentence.data_type == 'w_question':
			pass
			"""
			self._statements.append(?????)
			logging.debug("Ontologie:find('?concept', " + str(self._statements) + ")")
			self.process_w_question(sentence)
			"""
		
		
		self._oro.close()
		return self._answer
		
	def _resolve_action_verb_reference(self, statements):
		
		
		sit_id = self._oro.find('?event', statements)
		if not sit_id:
			return statements
		
		else:
			stmts = []
			logging.debug("/Found a staticSituation matching the yes_no_question query to be checked: "+ str(sit_id))
			for s in statements:
				#TODO:the ontology might find severals sit ID matching the query. Should we take this consideration?
				#The longer the query, the better the result of sit_id
				stmts.append(s.replace('?event', sit_id[0]))
			return stmts
	
	def process_w_question(self, sentence):
		"""
		if not sentence.resolved():
			raise DialogError("Trying to process an unresolved sentence!")
		
		self._sentence = sentence
		"""
		
		#Case the question is about the subject
		#Case the question is about the verb
		#Case the question is about the objects
		
		if sentence.sv:
			self.process_w_question_verbal_group(self, sentence.sv)
			
			
			
			
			
			
			
			
			vg_stmt_builder = VerbalGroupStatementBuilder(sentence.sv, self._current_speaker)
			for sn in sentence.sn:
				self._statements.extend(vg_stmt_builder._process(sn.id))					
		
		self.get_statements_based_on_aim(sentence.aim, id = sn.id)
		#Query performed on the ontology
		logging.debug("Ontologie:find('?concept', " + str(self._statements) + ")")
		
		return self._oro.find('?concept', self._statements)
		
	
	def process_w_question_verbal_groups(self, verbal_groups, id = None):
		for vg in verbal_groups:
			self.process_verb(vg, id)
	
	def process_verb(self, verbal_group, id = None):
		for verb in verbal_group.vrb_main:
			#State verb w question processing
			if verb == "be":
				self.get_statements_based_on_aim(self._sentence.aim, id)
			#Action verb w_question processing
			else:
				self.get_statements_based_on_aim(self._sentence.aim, '?event')
			
			
	
	
	def get_statements_based_on_aim(self, aim, id = None):
		aim_dic = {'place':' isOn ',
				    'thing':' involves '				    
				    }
		if id:
			self._statements.append(id + aim_dic[aim]+ '?concept')


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


class TestQuestionHandler(unittest.TestCase):
	def setUp(self):
	
		""" We want to process the following questions:
		#sentence="Where is the blue cube?"
		#sentence="Where are the cubes?"
		#sentence="What do you see?"
		#sentence="Could you take the blue cube?"
		#sentence="Can you take my cube?"
		"""
		self.oro = Oro("localhost", 6969)
		self.oro.add(['SPEAKER rdf:type Human', 'SPEAKER rdfs:label "Patrick"',
				 
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
				 'take_my_cube rdf:type Take'])
		
		
		self.qhandler = QuestionHandler("SPEAKER")
	
	"""
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
	"""
	
	
	
	def test_4_y_n_question(self):
		print "\n*************  test_4_y_n_question ******************"
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
	
	
	
	def process(self, sentence , statement_query, expected_result):
		res = self.qhandler.process_sentence(sentence)
		logging.debug("Result: " + str(res))
		self.assertEqual(res, expected_result)
	
	def tearDown(self):
		self.oro.close()



def dump_resolved(sentence, current_speaker, current_recipient = None):
	resolver = Resolver()
	#Resolution
	sentence = resolver.references_resolution(sentence,
                                              current_speaker, 
                                              None)
	
	sentence = resolver.noun_phrases_resolution(sentence,
											    current_speaker)
	sentence = resolver.verbal_phrases_resolution(sentence)
	print "RRREEEEOOOSC", sentence
	return sentence


def unit_tests():
	"""This function tests the main features of the class QuestionHandler"""
	
	print("This is a test...")
	#unittest.main()
	
	oro = Oro("localhost", 6969)
	oro.add(['oo rdf:type OO'])
	print oro.check(['oo rdf:type OO'])
	
	
if __name__ == '__main__':
	unit_tests()

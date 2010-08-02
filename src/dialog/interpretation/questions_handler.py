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
        #        and takes a list of returned values from the ontology when processing a w_question 
        self._answer = False
        
        #This field is set to 'None' when the answer of the question (wh-question) that is being processed aims to give information about the subject.
        #It also holds the flags 'QUERY_ON_DIRECT_OBJ' and 'QUERY_ON_INDIRECT_OBJ'.
        self._query_on_field = None
        
    def clear_statements(self):
        self._statements = []
    
    
    def set_current_speaker(self, current_speaker):
        self._current_speaker = current_speaker
    
    def get_query_on_field(self):
        return self._query_on_field
        
    def process_sentence(self, sentence):
        self._sentence = sentence
        #StatementBuilder
        builder = StatementBuilder(self._current_speaker)
        self._statements = builder.process_sentence(self._sentence)
        logging.info("statement from Statement Builder: " + str(self._statements))
        
        #Case the question is a y_n_question : check the fact in the ontology
        if sentence.data_type == 'yes_no_question':
            self._statements = self._set_situation_id(self._statements)
            
            try:
                logging.debug("Checking on the ontology: check(" + str(self._statements) + ")")
                self._answer = ResourcePool().ontology_server.check(self._statements)
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
            
        #Case the question is a w_question : find the concept the concept that answers the question
        if sentence.data_type == 'w_question':
            
            #
            self._query_on_field = self._set_query_on_field(sentence)
            self._statements =  self._remove_statements_with_no_unbound_tokens(self._statements)
            self._statements = self._extend_statement_from_sentence_aim(self._statements)
            
            if self._statements:
                try:
                    logging.debug("Searching the ontology: find(?concept, " + str(self._statements) + ")")
                    self._answer = ResourcePool().ontology_server.find('?concept', self._statements)
                except AttributeError: #the ontology server is not started of doesn't know the method
                    pass
            else:
                pass

        
        return self._answer
        
    def _set_situation_id(self, statements):
        stmts = []
        try:

            sit_id = []
            
            try:
                sit_id = ResourcePool().ontology_server.find('?event', statements)
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
                
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
        #case: the statement is partially build from statement builder
        
        stmts = []
                    
        for sn in self._sentence.sn:
            for sv in self._sentence.sv:
                for verb in sv.vrb_main:
                    role = self.get_role_from_sentence_aim(self._query_on_field, verb)
                    if verb.lower() == 'be':
                        stmts.append(sn.id + ' '+ role + ' ?concept')
                    else:
                        stmts.append('?event ' + role + ' ?concept')
        
        
        return current_statements + stmts
    
    
    
    def _set_query_on_field(self, sentence):
        
        if sentence.aim == 'place':
            return 'QUERY_ON_INDIRECT_OBJ'
        
        if not sentence.sn:
            return None
                   
        if sentence.sv:
            if not sentence.sv[0].d_obj:
                query_on_field = 'QUERY_ON_DIRECT_OBJ'
            
            else:
                query_on_field = 'QUERY_ON_INDIRECT_OBJ'
        
        return query_on_field
        
            
    
    def get_role_from_sentence_aim(self, query_on_field, verb):
        """
        Info:
            (A): A is optional
            <A|B>: either A or B
            {A}: A may be replaced
        
        'What-question': 
            Case  # query on a direct object
                e.g: what do you see? 
                append in statement [?event involves ?concept]
                                
                e.g: what(<object|thing>) is <this|the small cube>?
                append in statement [* owl:sameAs ?concept]
                
                e.g: what <feature|color|size> is <the small cube|this>? #Feature or subClassOf Feature
                append in statement [* hasFeature ?concept]
                
            Case # query on the subject
                e.g: what is 'in' <the blue cube|this>?
                append in statement [] # query completed from statementBuilder
                 
                e.g: what(<object|thing>) is blue?
                append in statement [* hasFeature ?concept]
                
            Case # query on the a direct object but answer replacing subject
                e.g: what(object) is a cube?             
                append in statement [* {rdf:type} ?concept]
                
            
        'Who-question':
            
            Case # query on the subject
                e.g: who sees the man?
                append in statement [* performedBy ?concept] 
            
            Case # query on a direct object with state verb
                e.g: who is the man?
                append in statement [* rdfs:label ?concept] 
                
            Case # query on a direct object with action verb
                e.g: who does the man see?
                append in statement [* actsOnObject ?concept]
            
            Case # query on an indirect object
                e.g: who does the man give a cube
                append in statement [* receivedBy ?concept]         
        """
        #TODO in resource pool: Create dictionary files
        dic_on_indirect_obj = {'be':None,
                            'put':'hasGoal',
                            'give':'hasGoal',
                            'show':'hasGoal', 
                            None:'receivedBy'}
                            
        dic_on_direct_obj = {'be':'owl:sameAs',
                            'put':'actsOnObject',
                            'give':'actsOnObject',
                            'show':'actsOnObject', 
                            None:'involves'}
    
        #Dictionary for sentence.aim = 'place' 
        dic_place={None:dic_on_indirect_obj.copy()}
        dic_place[None]['be'] = 'isAt'
                        
        #Dictionary for sentence.aim = 'thing' 
        dic_thing={None:dic_on_direct_obj.copy()}
                
        #Dictionary for sentence.aim = 'manner' 
        dic_manner={'be':'?sub_feature'}
        
        #Dictionary for sentence.aim = 'people'
        dic_people={'QUERY_ON_DIRECT_OBJ':dic_on_direct_obj.copy(),                                                                                              
                    'QUERY_ON_INDIRECT_OBJ':dic_on_indirect_obj.copy()}
        
        #Dictionary for all
        #dic_aim = resourcePool.Dictionary(dic_aim)
        dic_aim = {
                   #What-question
                   'thing':dic_thing,
                   'color':{None:{'be':'hasColor'}},
                   'size':{None:{'be':'hasSize'}},
                   
                   #Who-question
                   'people':dic_people,
                   
                   #Where-question
                   'place':dic_place,
                   
                   #How-Question
                   'manner':dic_manner                   
                   }
        
        
        try:
            if verb.lower() in dic_aim[self._sentence.aim][query_on_field]:
                role = dic_aim[self._sentence.aim][query_on_field][verb.lower()]
            else:
                role = dic_aim[self._sentence.aim][query_on_field][None]
        except KeyError:
            if verb.lower() in dic_aim[self._sentence.aim][None]:
                role = dic_aim[self._sentence.aim][None][verb.lower()]
            else:
                role = dic_aim[self._sentence.aim][None][None]

        return role
    
    
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
        
        try:
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
                     
                     'see_shelf rdf:type See',
                     'see_shelf performedBy myself',
                     'see_shelf involves shelf1',
                     
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
                     'give_another_cube hasGoal SPEAKER',
                     'give_another_cube actsOnObject another_cube',
                     
                     'see_some_one rdf:type See',
                     'see_some_one performedBy id_danny',
                     'see_some_one actsOnObject SPEAKER',
                     ])
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass
        
        
        try:
            ResourcePool().ontology_server.addForAgent('SPEAKER', ['SPEAKER rdf:type Human', 'SPEAKER rdfs:label "Patrick"',
                     'blue_cube rdf:type Cube',
                     'shelf1 rdf:type Shelf',
                     'id_danny rdfs:label "Danny"',
                     'another_cube rdf:type Cube',
                     ])
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass
                
                
        
        self.qhandler = QuestionHandler("SPEAKER")
        self.sfactory = SentenceFactory()
    """
    def test_1_where_question(self):
        print "\n*************  test_1_where_question ******************"
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

    def test_2_where_question(self):
        print "\n*************  test_2_where_question ******************"
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
    
    
    def test_3_what_question(self):
        print "\n*************  test_3_what_question ******************"
        print "What do you see?"
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
        #TODO:there might be severals action ID that are instances of See
        # ?Concept may hold several results 
        statement_query = ['* rdf:type See',
                           '* performedBy myself',
                           '* involves ?concept']
        expected_result = ['shelf1']
        
        self.process(sentence , statement_query, expected_result)

    def test_8_what_question(self):
        print "\n*************  test_8_what_question ******************"
        print "what is blue?"
        sentence = Sentence("w_question", "thing", 
                             [],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                          [],
                                                          ['blue'],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['blue_cube owl:sameAs ?concept']
        expected_result = ['blue_cube']        
        self.process(sentence , statement_query, expected_result) 
    

    
    def test_9_what_question_this(self):
        print "\n*************  test_9_what_question_this ******************"
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
    
    
    def test_10_what_question(self):
        print "\n*************  test_10_w_question ******************"
        print "what object is blue?"
        sentence = Sentence("w_question", "object", 
                             [],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present simple',
                                           [Nominal_Group([],
                                                          [],
                                                          ['blue'],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['?concept owl:sameAs blue_cube']
        expected_result = ['blue_cube']        
        self.process(sentence , statement_query, expected_result)
    
    def test_11_what_question(self):
        print "\n*************  test_11_w_question ******************"
        print "what size is this?"
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
        statement_query = ['another_cube hasSize ?concept']
        expected_result = ['small']        
        self.process(sentence , statement_query, expected_result)
    
    def test_12_what_question(self):
        print "\n*************  test_12_what_question ******************"
        print "what color is the blue_cube?"
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
        statement_query = ['blue_cube hasColor ?concept']
        expected_result = ['blue']        
        self.process(sentence , statement_query, expected_result)
    
    def test_13_who_question(self):
        print "\n*************  test_13_who_question ******************"
        print "who is the SPEAKER?"
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
        statement_query = ['SPEAKER owl:sameAs ?concept']
        expected_result = ['SPEAKER']        
        self.process(sentence , statement_query, expected_result)
    
    def test_14_who_question(self):
        print "\n*************  test_14_who_question ******************"
        print "who sees Patrick?"
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
        statement_query = ['* performedBy ?concept',
                           '* rdf:type See',
                           '* involves SPEAKER']
                           
        expected_result = ['id_danny']        
        self.process(sentence , statement_query, expected_result)
    
    def test_15_who_question(self):
        print "\n*************  test_15_who_question ******************"
        print "who does Danny give the small cube?"
        sentence = Sentence("w_question", "people", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['give'],
                                           [],
                                           'present simple',
                                           [Nominal_Group(['a'],
                                                          ['cube'],
                                                          ['small'],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        statement_query = ['* performedBy id_danny',
                           '* rdf:type Give',
                           '* hasGoal ?concept'
                           '* actsOnObject another_cube']
                            
        expected_result = ['SPEAKER']        
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
        
    """
    def test_5_y_n_question(self):
        print "\n*************  test_5_y_n_question verb to be followed by complement******************"
          "Is the blue cube on the table?"
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
    
    
    
    
    
    
    def test_9_how_question(self):
        print "\n*************  test_9_how_question ******************"
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
        
        #Statements Built for querying Ontology
        logging.info("Query Statement ...")
        for s in self.qhandler._statements:
            logging.info("\t>>" + s)
        logging.info("--------------- >>\n")
        
        #Result from the ontology
        logging.info("Expected Result:" + str(expected_result))
        logging.debug("Result Found in the Ontology: " + str(self.qhandler._answer))
        
        #Response in sentence
        logging.info("************************************************")
        logging.info("* Factory: Sentence towards Verbalization .... *")
        logging.info("************************************************")
        
        res_factory = []
        if sentence.data_type == 'w_question':
            res_factory = self.sfactory.create_w_question_answer(sentence, self.qhandler._answer, self.qhandler._query_on_field)
            
        elif sentence.data_type == 'yes_no_question':
            res_factory = self.sfactory.create_yes_no_answer(sentence, self.qhandler._answer)
        else:
            pass
        
        for rep in res_factory:
            logging.debug(str(rep))
            logging.debug(str(rep.flatten()))
        
        self.qhandler.clear_statements()
        self.assertEqual(res, expected_result)

def dump_resolved(sentence, current_speaker, current_recipient = None):
    def resolve_ng(ngs, builder):        
        for ng in ngs:
            #Statement for resolution
            logging.info("********************************************************")
            logging.info("* Sentence: Nominal group Towards StatementBuilder ... *")
            logging.info("********************************************************")
            logging.info(str(ng))
            logging.info("*******************************************************")
            logging.info("* SatementBuilder: Statements towards Resolution .... *")
            logging.info("*******************************************************")
            builder.process_nominal_group(ng, '?concept')
            stmts = builder.get_statements()
            builder.clear_statements()
            for s in stmts:
                logging.info("\t>>" + s)
                
            logging.info("--------------<<\n")
            
            #Dump resolution for StatementBuilder test ONLY
            logging.info("**************************************************")
            logging.info("* QuestionHandler: Dump resolution....           *")
            logging.info("**************************************************")
            
            resolved = True
                            
            if ng._resolved:
                pass
            #personal pronoun
            elif ng.noun in [['me'], ['Me'],['I']]:
                ng.id = current_speaker
            elif ng.noun in [['you'], ['You']]:
                ng.id = current_recipient                       
            
            #Existing ID from the onotlogy
            elif ng.noun:                
                onto = ''
                try:
                    onto =  ResourcePool().ontology_server.lookup(ng.noun[0])
                except AttributeError: #the ontology server is not started of doesn't know the method
                    pass
                
                    
                if onto and [ng.noun[0], 'INSTANCE'] in onto:
                    ng.id = ng.noun[0]
                
            #Find Existing ID from the onotlogy
            if not ng.id and stmts:
                onto = ''
                try:
                    onto =  ResourcePool().ontology_server.find('?concept', stmts)
                except AttributeError: #the ontology server is not started of doesn't know the method
                    pass
                
                    
                if onto:
                    logging.info("\tFound in the Ontology " + str(onto) + " matching the statements send to resolution")
                    ng.id = onto[0]
    
            #Nominal group resolved?
            if ng.id:
                logging.info("\tAssign to ng: " + colored_print(ng.id, 'white', 'blue'))
                ng._resolved = True
                
            resolved = resolved and ng._resolved
            
        return [ngs, resolved]
    
    
    builder = NominalGroupStatementBuilder(None, current_speaker)
        
    if sentence.sn:
        res_sn = resolve_ng(sentence.sn, builder)
        sentence.sn = res_sn[0]
        
    
    if sentence.sv:
        for sv in sentence.sv:
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
    
    logging.info(str(sentence))
    logging.info("Sentence resolved? ... " + str(sentence.resolved()))
    
    return sentence




def unit_tests():
    """This function tests the main features of the class QuestionHandler"""
    logging.basicConfig(level=logging.DEBUG,format="%(message)s")
    print("This is a test...")
    unittest.main()
    
    
if __name__ == '__main__':
    unit_tests()



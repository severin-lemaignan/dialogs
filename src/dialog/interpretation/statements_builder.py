#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from helpers import colored_print

import random
import inspect
import unittest
from resources_manager import ResourcePool
from statements_safe_adder import StatementSafeAdder, generate_id, printer

from dialog_exceptions import DialogError, GrammaticalError, EmptyNominalGroupId



from sentence import *

"""This module implements ...

"""

class StatementBuilder:
    """ Build statements related to a sentence"""
    def __init__(self,current_speaker = None):
        self._sentence = None
        self._current_speaker = current_speaker
        self._statements = []
        self._unresolved_ids = []
        

    def clear_statements(self):
        self._statements = []
    
    def set_current_speaker(self, current_speaker):
        self._current_speaker = current_speaker
    
    def process_sentence(self, sentence):
        """
        if not sentence.resolved():
            raise DialogError("Trying to process an unresolved sentence!")
        """
        self._sentence = sentence
        
        if sentence.sn:
            self.process_nominal_groups(self._sentence.sn)
        if sentence.sv:
            self.process_verbal_groups(self._sentence)
        
                                 
        return self._statements
    
    
    def process_nominal_groups(self, nominal_groups):
        ng_stmt_builder = NominalGroupStatementBuilder(nominal_groups, self._current_speaker)
        self._statements.extend(ng_stmt_builder.process())
        self._unresolved_ids.extend(ng_stmt_builder._unresolved_ids)
        
    def process_verbal_groups(self, sentence):
        #VerbalGroupStatementBuilder
        vg_stmt_builder = VerbalGroupStatementBuilder(sentence.sv, self._current_speaker)
        
        #Setting up attribute of verbalGroupStatementBuilder:
        #    process_on_imperative
        #    process_on_question
        vg_stmt_builder.set_attribute_on_data_type(sentence.data_type)
        
        if not sentence.sn:
            self._statements.extend(vg_stmt_builder.process())
            self._unresolved_ids.extend(vg_stmt_builder._unresolved_ids)
            
        for sn in sentence.sn:
            if not sn.id:
                raise EmptyNominalGroupId("Nominal group ID not resolved or not affected yet")
            
            self._statements.extend(vg_stmt_builder.process(sn.id))
            self._unresolved_ids.extend(vg_stmt_builder._unresolved_ids)

class NominalGroupStatementBuilder:
    """ Build statements related to a nominal group"""
    def __init__(self, nominal_groups, current_speaker = None):
        self._nominal_groups = nominal_groups
        self._current_speaker = current_speaker
        self._statements = []
        
        self._unresolved_ids = []
        
    def clear_statements(self):
        self._statements = []
        
        
    def process(self):
        """ The following function builds a list of statement from a list of nominal group
        A NominalGroupStatementBuilder needs to have been instantiated before"""
        
        for ng in self._nominal_groups:
            if not ng.id:
                ng.id = generate_id()

                print "GENERATE NominalGroupStatementBuilder process" , ng.id
                self._unresolved_ids.append(ng.id)          
            
            self.process_nominal_group(ng, ng.id)
                                    
        return self._statements
    
    def get_statements(self):
        return self._statements
    
    def process_nominal_group(self, ng, ng_id):
        """ The following function processes a single nominal_group"""
        if ng.det:
            self.process_determiners(ng, ng_id)
        if ng.noun:
            self.process_noun_phrases(ng, ng_id)
        if ng.adj:
            self.process_adjectives(ng, ng_id)
        if ng.noun_cmpl:
            self.process_noun_cmpl(ng, ng_id)
        if ng.relative:
            self.process_relative(ng, ng_id)
            

    def process_determiners(self, nominal_group, ng_id):
        for det in nominal_group.det:
            #logging.debug("Found determiner:\"" + det + "\"")
            # Case 1: definite article : the"""
            # Case 2: demonstratives : this, that, these, those"""
            if det in ['this', 'that', 'these', 'those']:
                self._statements.append(self._current_speaker + " focusesOn " + ng_id)
            # Case 3: possessives : my, your, his, her, its, our, their """
            if det == "my":
                self._statements.append(ng_id + " belongsTo " + self._current_speaker)
            elif det == "your":
                self._statements.append(ng_id + " belongsTo myself")
            # Case 4: general determiners: See http://www.learnenglish.de/grammar/determinertext.htm"""
            
    
    def process_noun_phrases(self, nominal_group, ng_id):
        for noun in nominal_group.noun:
            #logging.debug("Found a noun phrase:\"" + noun + "\"")
                        
            # Case : existing ID
            onto_id = ''
            try:
                onto_id = ResourcePool().ontology_server.lookup(noun)
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
            
            if onto_id and [noun,"INSTANCE"] in onto_id:
                pass #Just to be checked. The Id has already been resolved
                
            # Case : common noun
            elif nominal_group.det:
                self._statements.append(ng_id + " rdf:type " + noun.capitalize())            
                
            #Case : proper noun or personal pronoun
            else:
                #TODO: the list ["I", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "their"] needs to be inserted in ResourcePool
                """
                if not noun in ResourcePool().personal_determiner
                """
                if not noun in ["I", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "their"]:
                    self._statements.append(ng_id + " rdfs:label \"" + noun + "\"")
                
                    
    
    def process_adjectives(self, nominal_group, ng_id):
        """For any adjectives, we add it in the ontology with the objectProperty 
        'hasFeature' except if a specific category has been specified in the 
        adjectives list.
        """
        for adj in nominal_group.adj:
            #logging.debug("Found adjective:\"" + adj + "\"")
            try:
                self._statements.append(ng_id + " has" + ResourcePool().adjectives[adj] + " " + adj)
            except KeyError:
                self._statements.append(ng_id + " hasFeature " + adj)
    
    
    def process_noun_cmpl(self, nominal_group, ng_id):
        #logging.debug("processing noun complement:")
        for noun_cmpl in nominal_group.noun_cmpl:
            if noun_cmpl.id:
                noun_cmpl_id = noun_cmpl.id
            else:
                noun_cmpl_id = generate_id()
                
            self.process_nominal_group(noun_cmpl, noun_cmpl_id)
            self._statements.append(ng_id + " belongsTo " + noun_cmpl_id)
    
    def process_relative(self, nominal_group, ng_id):
        """ The following processes the relative clause of the subject of a sentence.           
           case 1: the subject of the sentence is complement of the relative clause
                    e.g. the man that you heard from is my boss
                          => the man is my boss + you heard from the man
                          => sn != []
            
           case 2: the subject of the sentence is subject of the relative clause.
                   we process only the verbal group of the relative.
                    e.g. the man who is talking, is tall
                         => the man is tall and is talking
                         => sn == []
        """
        for rel in nominal_group.relative:
            #logging.debug("processing relative:")    
            #case 1   
            if rel.sn:
                logging.warning("Don't know how to resolve a relative clause in this situation yet")
                #TODO: find or Write a function that compare instance of classes (Nominal_Group) 
                #    if sn == d_obj
                #        d_obj.id = sn.id
                #        process_direct_object()
                #    elif sn == i_cmpl:
                #        i_cmpl.id = sn.id
                #        process_indirect_object()
                #
                #
                """
                for ng in rel.sn:
                    if ng._resolved:
                        ng_rel_id = ng.id
                    else:
                        ng_rel_id = "Blagnac_Aircraft"                    
                    self.process_nominal_group(ng, ng_rel_id)
                
                if rel.sv:
                    rel_vg_stmt_builder = VerbalGroupStatementBuilder(rel.sv)    
                    rel_vg_stmt_builder.process_verbal_groups(rel.sv, ng_rel_id, ng_id)
                    self._statements.append(rel_vg_stmt_builder._statements)
                    rel_vg_stmt_builder.clear_statements()
                """
            #case 2        
            else:
                if rel.sv:
                    rel_vg_stmt_builder = VerbalGroupStatementBuilder(rel.sv, self._current_speaker)
                    rel_vg_stmt_builder.process_verbal_groups(rel.sv, ng_id)
                    self._statements.extend(rel_vg_stmt_builder._statements)
                    self._unresolved_ids.extend(rel_vg_stmt_builder._unresolved_ids)
                    

class VerbalGroupStatementBuilder:
    """ Build statements related to a verbal group"""
    def __init__(self, verbal_groups, current_speaker = None):
        self._verbal_groups = verbal_groups
        self._current_speaker = current_speaker
        self._statements = []
        self._unresolved_ids = []
        #This field holds the value True when the active sentence is of yes_no_question or w_question data_type
        self._process_on_question = False
        
        #This field holds the value True when the active sentence is of imperative data_type
        self._process_on_imperative = False

    def set_attribute_on_data_type(self, data_type):
        if data_type == 'imperative':
            self._process_on_imperative = True
        if data_type in ['yes_no_question', 'w_question']:
            self._process_on_question = True
        
    def clear_statements(self):
        self._statements = [] 
    
    def process(self, subject_id = None):
        #Case: an imperative sentence does not contain an sn attribute,
        #      we will assume that it is implicitly an order from the current speaker.
        #      performed by the recipient of the order.
        #      Therefore, the subject_id holds the value 'myself'
        if self._process_on_imperative:
            subject_id = 'myself'
            
        if not subject_id:
            subject_id = '?concept'       
        
            
        self.process_verbal_groups(self._verbal_groups  , subject_id)                
        return self._statements
   
    def get_statements(self):
        return self._statements
    
    
    
    def process_verbal_groups(self, verbal_groups, subject_id, subject_rel_id = None):
        
        for vg in verbal_groups:          
            self.process_state(vg)
            if vg.vrb_main:
                self.process_verb(vg, subject_id)
            
            if vg.advrb:
                self.process_adverbial_sentence(vg)
            if vg.vrb_adv:
                self.process_adverb(vg)
            if vg.vrb_sub_sentence:
                self.process_adverb(vg)   

    #TODO:   
    def process_state(self, state):
        """For A != B, Shall we use owl:complementOf => see Negation in http://www.co-ode.org/resources/tutorials/intro/slides/OWLFoundationsSlides.pdf """
        pass
    
    def process_verb(self, verbal_group, subject_id):
         
        for verb in verbal_group.vrb_main:
         
            #TODO: modal verbs e.g can+go
            
            #Case 1:  the linking verb 'to be'/"""
            #Case 2:  actions or stative verbs with a specified 'goal' role:
            #                          see '../../share/dialog/thematic_roles'
            #Case 3:  other action or stative verbs
            
            goal_verbs = ResourcePool().goal_verbs 
            
            #Case 1:
            if verb == "be":
                sit_id = subject_id
                
            else:
                if self._process_on_question:
                    sit_id = '?event'
                else:
                    sit_id = generate_id()  #means the subject_id might not have been resolved
                    if not '?' in subject_id:#means the subject_id has been resolved
                        sit_id = sit_id.lstrip('?')
                
                
                #Case 2:                
                if verb in goal_verbs:
                    self._statements.append(subject_id + " desires " + sit_id)
                    
                    if verbal_group.verb_sec:
                        self.process_vrb_sec(verbal_group)                      
                #Case 3:   
                else:
                    self._statements.append(sit_id + " rdf:type " + verb.capitalize())
                    self._statements.append(sit_id + " performedBy " + subject_id)
                    
            
            
            if self._process_on_imperative:
                self._statements.append(self._current_speaker + " desires " + sit_id)
            
            #Direct object
            if verbal_group.d_obj:
                self.process_direct_object(verbal_group.d_obj, verb, sit_id)
            
            
            #Indirect Complement
            if verbal_group.i_cmpl:
                self.process_indirect_complement(verbal_group.i_cmpl, verb, sit_id)
            
                    
                    
                
            
    def process_vrb_sec(self, verbal_group):
        for verb in verbal_group.vrb_sec:
            #logging.debug("Found verb:\"" + verb + "\"")
            pass
            
    def process_direct_object(self, d_objects, verb, id):
        #logging.debug("Processing direct object d_obj:")
        d_obj_stmt_builder = NominalGroupStatementBuilder(d_objects, self._current_speaker)
        
        #Thematic roles
        thematic_roles = ResourcePool().thematic_roles
       
        try:
            d_obj_role = thematic_roles.get_next_cmplt_role(verb, True)
        except:
            d_obj_role = None
        
        #nominal groups
        for d_obj in d_objects:
            #Case 1: The direct object follows the verb 'to be'.
            #        We process the d_obj with the same id as the subject of the sentence
            if verb == "be":
                d_obj_id = id
            
            
            #Case 2: The direct object follows another stative or action verb.
            #        we process the d_obj as involved by the situation
            else:
                if d_obj.id:
                    d_obj_id = d_obj.id
                else:
                    d_obj_id = generate_id()    
                    d_obj_stmt_builder._unresolved_ids.append(d_obj_id)
                #If there is an existing role matching the current verb
                if d_obj_role:
                    self._statements.append(id + d_obj_role + d_obj_id)
                else:
                    self._statements.append(id + " involves " + d_obj_id)
            
            d_obj_stmt_builder.process_nominal_group(d_obj, d_obj_id)
            
        self._statements.extend(d_obj_stmt_builder._statements)
        self._unresolved_ids.extend(d_obj_stmt_builder._unresolved_ids)
        
        
            
    def process_indirect_complement(self, indirect_cmpls,verb, sit_id):
        
        #Thematic roles
        thematic_roles = ResourcePool().thematic_roles
        
        for ic in indirect_cmpls:
            #logging.debug("Processing indirect complement i_cmpl:")
            
            # Case 1: if there is no preposition, the indirect complement is obviously an indirect object.
            #        Therefore, it receives the action
            #            e.g. I gave you a ball also means I gave a ball 'to' you
            #        see http://www.englishlanguageguide.com/english/grammar/indirect-object.asp
            
            #Case 2: if there is a preposition, the indirect complement is either an indirect object or an adverbial
            #        if the main verb is specified as a thematic role, we extract the matching object_property to the preposition.
            #            e.g I moved the bottle 'to' the table. The object_property takes the value "hasGoal"
            # 
            #        if the preposition is 'to' , by default we assume the indirect complement is an indirect object
            #            e.g. I gave a ball to Jido. The object_property takes the value "receivedBy"
            #        otherwise, the default processing is to create an object_property by concatenating is and the preposition
            #            e.g. I bought a ball for Jido. The object_property takes the value "isFor"
            
            
            i_stmt_builder = NominalGroupStatementBuilder(ic.nominal_group, self._current_speaker)
            for ic_noun  in ic.nominal_group:
                #Proposition role
                try:
                    icmpl_role = thematic_roles.get_cmplt_role_for_preposition(verb, ic.prep[0], True)
                except:
                    icmpl_role = None
                
                #Nominal group
                if ic_noun.id:
                    ic_noun_id = ic_noun.id
                else:
                    ic_noun_id = generate_id()
                    self._unresolved_ids.append(ic_noun_id)
                    
                if not ic.prep:
                    self._statements.append(sit_id + " receivedBy " + ic_noun_id)
                    
                elif icmpl_role:
                    self._statements.append(sit_id + icmpl_role + ic_noun_id)
                else:
                    self._statements.append(sit_id + " is" + ic.prep[0].capitalize()+ " " + ic_noun_id)
                
                
                i_stmt_builder.process_nominal_group(ic_noun, ic_noun_id)
                
            self._statements.extend(i_stmt_builder._statements)
            self._unresolved_ids.extend(i_stmt_builder._unresolved_ids)
            
                
                
    #TODO:      
    def process_adverbial_sentence(self, advrb):
        for adv in advrb:
            logging.debug("Found adverbial phrase:\"" + adv + "\"")
            
    #TODO:       
    def process_adverb(self, advrb):
        for adv in advrb:
            logging.debug("Found adverb:\"" + adv + "\"")
            
    #TODO:
    def vrb_subsentence(self, vrb_sub_sentence):
        for sub in vrb_sub_sentence:
            logging.debug("Processing adverbial clauses:")
            
            

        
"""
    The following functions are implemented for test purpose only
"""


def dump_resolved(sentence, current_speaker, current_listener):
    def resolve_ng(ngs):
        #TODO: remove connection. Use a variable that will be set up for a single connection to ORO

        for ng in ngs:
            ng._resolved = False
            
            onto_focus = ''
            try:
                onto_focus =  ResourcePool().ontology_server.find('?concept', [current_speaker + ' focusesOn ?concept'])
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
            
            if ng.noun in [['me'], ['Me'],['I']]:
                ng.id = current_speaker
            elif ng.noun in [['you'], ['You']]:
                ng.id = current_listener
                       
            elif ng.noun == ['Danny']:
                ng.id = 'id_danny'
                
            elif [ng.noun, ng.adj] == [['car'], ['blue']]:
                ng.id = 'blue_car'
            elif [ng.noun, ng.adj] == [['car'], ['small']]:
                ng.id = 'twingo'
            elif ng.noun == ['Tom']:
                ng.id = 'id_tom'
            elif ng.noun == ['shelf1']:
                ng.id = 'shelf1'
            elif onto_focus and ng.det in ['this', 'that']:
                ng.id = onto_focus[0]
            else:
                pass
            
            if ng.noun_cmpl:
                ng.noun_cmpl = resolve_ng(ng.noun_cmpl)

            if ng.relative:
                for rel in ng.relative:
                    rel = dump_resolved(rel, current_speaker, current_listener)

        return ngs

    if sentence.sn:
        sentence.sn = resolve_ng(sentence.sn)


    if sentence.sv:
        for sv in sentence.sv:
            sv._resolved = False

            if sv.d_obj:
                sv.d_obj = resolve_ng(sv.d_obj)

            if sv.i_cmpl:
                for i_cmpl in sv.i_cmpl:
                    i_cmpl = resolve_ng(i_cmpl.nominal_group)

    return sentence


        
class TestStatementBuilder(unittest.TestCase):

    def setUp(self):
        
        try:
            ResourcePool().ontology_server.add(['id_danny rdfs:label "Danny"',
                          'id_danny rdf:type Human',
                          'blue_volvo hasColor blue', 
                          'blue_volvo rdf:type Car',
                          'blue_volvo belongsTo SPEAKER',
                          'id_jido rdf:type Robot',
                          'id_jido rdfs:label "Jido"',
                          'twingo rdf:type Car',
                          'twingo hasSize small',
                          'a_man rdf:type Man',
                          'fiat belongsTo id_tom',
                          'fiat rdf:type Car',
                          'id_tom rdfs:label "Tom"',
                          'id_tom rdf:type Brother',
                          'id_tom belongsTo id_danny',
                          'id_toulouse rdfs:label "Toulouse"',
                          'blue_cube rdf:type Cube', 'blue_cube hasColor blue',
                          'SPEAKER focusesOn another_cube'])
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass
        
        self.stmt = StatementBuilder("SPEAKER")
        self.stmt_adder = StatementSafeAdder()
        
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
                                           'present_simple',
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
        #return self.process(sentence, expected_result, display_statement_result = True)
        #
        #otherwise, use the following if you want to hide the statements 
        #return self.process(sentence, expected_result)
        #    or
        #return self.process(sentence, expected_result, display_statement_result = False)
        #
    
                        
    """
    def test_1(self):
        print "\n**** Test 1  *** "
        print "Danny drives a blue car"  
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['drive'],
                                           [],
                                           'present_simple',
                                           [Nominal_Group(['a'],['car'],['blue'],[],[])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])    
        
        expected_result = ['id_danny rdfs:label "Danny"',
                           '* rdf:type Drive',
                           '* performedBy *',
                           '* involves *',
                           '* rdf:type Car',
                           '* hasColor blue']
        
        return self.process(sentence, expected_result, display_statement_result = True)
    
        
    
    def test_2(self):
        print "\n**** Test 2  *** "
        print "my car is blue"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['my'],
                                            ['car'],
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
        expected_result = ['* rdf:type Car',
                           '* hasColor blue',
                           '* belongsTo SPEAKER']   
        return self.process(sentence, expected_result, display_statement_result = True)
        
        
    def test_3(self):
        print "\n**** Test 3  *** "
        print "Jido is a robot"
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Jido'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           None,
                                           'present_simple',
                                           [Nominal_Group(['a'],['robot'],[],[],[])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                          [])])  
        expected_result = ['* rdfs:label "Jido"',
                           '* rdf:type Robot']   
        return self.process(sentence, expected_result, display_statement_result = True)
        
    
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
                                            [relative4])],                                         
                             [Verbal_Group(['have'],
                                           [],
                                           'present_simple',
                                           [Nominal_Group(
                                                          ['a'],
                                                          ['car'],
                                                          ['small'],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])]) 
        expected_resut = ['* rdf:type Man',
                          '* performedBy SPEAKER',
                          '* rdf:type See',
                          '* involves *',
                          '* rdf:type Have',
                          '* performedBy *',
                          '* rdf:type Car *',
                          '* hasSize small *']
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
                                           'present_simple',
                                           [Nominal_Group(
                                                          ['a'],
                                                          ['car'],
                                                          ['small'],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])    
        
        expected_resut = ['* rdf:type Man',
                          '* rdf:type Talk',
                          '* performedBy *',
                          '* rdf:type Have',
                          '* involves *',
                          '* rdf:type Car *',
                          '* hasSize small *']
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
                                                           [Nominal_Group(
                                                                          ['the'],
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
                          '* actsOnObject *',
                          '* rdf:type Car',
                          '* belongsTo *',
                          '* rdf:type Brother',
                          '* belongsTo *',
                          '* rdfs:label "Danny"',
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
                                           'present_simple',
                                           [],
                                           [Indirect_Complement(['to'], [Nominal_Group([],['Toulouse'],[],[],[])])],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['* rdf:type Go',
                          '* performedBy SPEAKER',
                          '* hasGoal *',
                          '* rdfs:label "Toulouse"']
        return self.process(sentence, expected_resut, display_statement_result = True)
        
    
    def test_8(self):
        print "\n**** Test 8  *** "
        print "put the bottle in the cardbox"
        sentence = Sentence("imperative", "", 
                             [],                                         
                             [Verbal_Group(['put'],
                                           [],
                                           'present_simple',
                                           [Nominal_Group(['the'],['bottle'],[],[],[])],
                                           [Indirect_Complement(['in'],
                                                                [Nominal_Group(['the'],['cardbox'],[],[],[])]) ],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['SPEAKER desires *',
                          '* rdf:type Put',
                          '* performedBy myself',
                          '* actsOnObject *',
                          '* rdf:type Bottle',
                          '* isIn *',
                          '* rdf:type Cardbox']  
        

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
                                           'present_simple',
                                           [Nominal_Group(['a'],
                                                          ['cube'],
                                                          ['blue'],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['SPEAKER focusesOn *',
                          '* hasColor blue',
                          '* rdf:type Cube']
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
                                           'present_simple',
                                           [],
                                           [Indirect_Complement(['on'],
                                                                [Nominal_Group(['the'],['shelf1'],[],[],[])]) ],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['SPEAKER focusesOn *',
                          '* isOn shelf1']
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
                                           'present_simple',
                                           [],
                                           [Indirect_Complement(['to'],
                                                                [Nominal_Group(['the'],['shelf1'],[],[],[])]) ],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['SPEAKER focusesOn *',
                          '* rdf:type Go',
                          '* performedBy *',
                          '* hasGoal shelf1']
        
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
                                           'present_simple',
                                           [],
                                           [Indirect_Complement(['to'],
                                                                [Nominal_Group(['the'],['shelf1'],[],[],[])]) ],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['SPEAKER focusesOn *',
                          '* rdf:type Cube',
                          '* rdf:type Go',
                          '* performedBy *',
                          '* hasGoal shelf1']
        
        return self.process(sentence, expected_resut, display_statement_result = True)
    
    
    
    def test_13_this(self):
        
        print "\n**** test_13_this  *** "
        print "this cube is blue => this blue cube is"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['this'],
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
        expected_resut = ['SPEAKER focusesOn *',
                          '* rdf:type Cube',
                          '* hasColor blue']
        
        return self.process(sentence, expected_resut, display_statement_result = True)
      
    
       
    def process(self, sentence, expected_result, display_statement_result = False):
         
        sentence = dump_resolved(sentence, self.stmt._current_speaker, 'myself')#TODO: dumped_resolved is only for the test of statement builder. Need to be replaced as commented above
        res_stmt_builder = self.stmt.process_sentence(sentence)        
        self.stmt_adder._statements = res_stmt_builder
        self.stmt_adder._unresolved_ids = self.stmt._unresolved_ids
        self.stmt_adder.process(sentence.resolved())
        res = self.stmt_adder._statements
        
        
        if display_statement_result:
            logging.info( "*** StatementSafeAdder result from " + inspect.stack()[1][3] + " ****")
            printer(res)
        self.assertTrue(self.check_results(res, expected_result))
        
        



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
        if expected:
            print "\t**** /Missing statements in result:   "
            print "\t", expected, "\n"
               
        return expected == res
        
        
def unit_tests():
    """This function tests the main features of the class StatementBuilder"""
    logging.basicConfig(level=logging.DEBUG,format="%(message)s")
    print("This is a test...")
    unittest.main()
     
if __name__ == '__main__':
    unit_tests()
    

    


#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from dialog.helpers import colored_print

import random
import inspect
import unittest
from dialog.resources_manager import ResourcePool
from statements_safe_adder import StatementSafeAdder

from dialog.dialog_exceptions import DialogError, GrammaticalError



from dialog.sentence import *

"""This module implements ...

"""

class StatementBuilder:
    """ Build statements related to a sentence"""
    def __init__(self,current_speaker = None):
        #This field keeps record of the sentence that is being processed
        self._sentence = None
        
        #This field identifies the current speaker
        self._current_speaker = current_speaker
        
        
        #This holds the statements created from the main clause of a sentence
        self._statements = []
        
        #This holds the statements that are to be removed from the ontology
        #   Possibly after processing a negative sentence
        self._statements_to_remove = []
        
        #This holds unidentified IDs that are generated while creating the statements of a resolved sentence.
        #   Possibly in the case of a negative sentence involving an action that is to be identity in the module StatementSafeAdder
        self._unclarified_ids = []
        
        #This field holds concepts for class grounding
        self.lear_more_concept = []
        

    def clear_statements(self):
        self._statements = []
    
    def set_current_speaker(self, current_speaker):
        self._current_speaker = current_speaker
    
    def process_sentence(self, sentence):
        if not sentence.resolved():
            raise DialogError("Trying to process an unresolved sentence!")
        
        self._sentence = sentence
        
        if sentence.sn:
            self.process_nominal_groups(self._sentence.sn)
        if sentence.sv:
            self.process_verbal_groups(self._sentence)
        
                                 
        return self._statements
    
    
    def process_nominal_groups(self, nominal_groups):
        ng_stmt_builder = NominalGroupStatementBuilder(nominal_groups, self._current_speaker)
        ng_stmt_builder.process()
        
        self._statements.extend(ng_stmt_builder._statements)
        self._unclarified_ids.extend(ng_stmt_builder._unclarified_ids)
        self.lear_more_concept.extend(ng_stmt_builder.lear_more_concept)
        
    def process_verbal_groups(self, sentence):
        #VerbalGroupStatementBuilder
        vg_stmt_builder = VerbalGroupStatementBuilder(sentence.sv, self._current_speaker)
        
        #Setting up attribute of verbalGroupStatementBuilder:
        #    process_on_imperative
        #    process_on_question
        vg_stmt_builder.set_attribute_on_data_type(sentence.data_type)
        vg_stmt_builder._process_on_resolved_sentence = sentence.resolved()
        
        if not sentence.sn:
            vg_stmt_builder.process()
            
            self._statements.extend(vg_stmt_builder._statements)
            self._unclarified_ids.extend(vg_stmt_builder._unclarified_ids)
            self.lear_more_concept.extend(vg_stmt_builder.lear_more_concept)
            
            # Case of statement to remove due to some case of negation
            if vg_stmt_builder.process_statements_to_remove:
                self._statements_to_remove.extend(vg_stmt_builder._statements)
            
        for sn in sentence.sn:
            if not sn.id:
                raise EmptyNominalGroupId("Nominal group ID not resolved or not affected yet")
            
            vg_stmt_builder.process(subject_id = sn.id, subject_quantifier = sn._quantifier)
            
            self._statements.extend(vg_stmt_builder._statements)
            self._unclarified_ids.extend(vg_stmt_builder._unclarified_ids)
            self.lear_more_concept.extend(vg_stmt_builder.lear_more_concept)
            
            # Case of statement to remove due to some case of negation
            if vg_stmt_builder.process_statements_to_remove:
                self._statements_to_remove.extend(vg_stmt_builder._statements)

class NominalGroupStatementBuilder:
    """ Build statements related to a nominal group"""
    def __init__(self, nominal_groups, current_speaker = None):
        #This field keeps record of the nominal group that is being processed
        self._nominal_groups = nominal_groups
        
        #This field identifies the current speaker
        self._current_speaker = current_speaker
        
        #This holds the statements created from the main clause of a sentence
        self._statements = []
        
        #This holds unidentified IDs that are generated while creating the statements of a resolved sentence.
        #   Possibly in the case of a negative sentence involving an action that is to be identity in the module StatementSafeAdder
        self._unclarified_ids = []
        
        #This field holds concepts for class grounding
        self.lear_more_concept = []
        
        #This field is True when the special case of "other" occurs
        #   E.g: Give me the "other" tape
        self.process_on_other = False
        
    def clear_statements(self):
        self._statements = []
    
    def process(self):
        """ The following function builds a list of statement from a list of nominal group
        A NominalGroupStatementBuilder has to be instantiated before"""
        
        for ng in self._nominal_groups:
            if not ng.id:
                ng.id = self.set_nominal_group_id(ng)      
            
            self.process_nominal_group(ng, ng.id, None, False)
                                    
        return self._statements
    
    def get_statements(self):
        return self._statements
    
    def set_nominal_group_id(self, ng):
        if ng.id:
            return ng.id
            
        onto = ''
        try:
            onto =  ResourcePool().ontology_server.lookupForAgent(self._current_speaker, ng.noun[0])
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass
        
        if onto and [ng.noun[0],"INSTANCE"] in onto:
            return ng.noun[0]
        
        if ng.noun[0].lower() in ['i', 'me']:
            return self._current_speaker
        
        if ng.noun[0].lower() == 'you':
            return 'myself'
        
        id = generate_id()
        self._unclarified_ids.append(id)
        return id
    
    
    def process_nominal_group(self, ng, ng_id, subject_quantifier, negative_object):
        """ The following function processes a single nominal_group with a given resolved ID and quantifier
            the parameter 'negative_object' is to meant that the sentence hold a negative form involving the nominal group being processed
        """
        
        def process_all_component_of_a_nominal_group(nom_grp, id, quantifier, negative):
            """This processes all the components of a given nominal group 'nom_grp'. """
            if nom_grp.noun:
                self.process_noun_phrases(nom_grp, id, quantifier, negative)
            if nom_grp.det:
                self.process_determiners(nom_grp, id, negative)
            if nom_grp.adj:
                self.process_adjectives(nom_grp, id, negative)
            if nom_grp.noun_cmpl:
                self.process_noun_cmpl(nom_grp, id, negative)
            if nom_grp.relative:
                self.process_relative(nom_grp, id)
                
        # End of process_all_component_of_a_nominal_group()
        
        def get_concept_to_learn(nom_grp):
            if nom_grp._quantifier == 'ONE':
                return [] #Concept already known for sure
            
            learn_more = []
            
            for noun in nom_grp.noun:
                onto = ''
                try:
                    onto = ResourcePool().ontology_server.lookupForAgent(self._current_speaker, noun)
                except AttributeError:
                    pass
                
                if not onto: 
                    learn_more.append(noun)
            
            return learn_more
        # End of get_concept_to_learn ()
        
        
        # Case of resolved nominal group
        if ng._resolved:
            
            #Trying to learn more concept
            self.lear_more_concept = get_concept_to_learn(ng)
            
            # Case: Adjectives only
            if ng.adjectives_only():
                self.process_adjectives(ng, ng_id, negative_object)
            
            #Case: Quantifier of the nominal group being processed. 
            elif subject_quantifier:
                # Case of an finite nominal group described by either a finite or an infinite one
                #
                # E.g "this is 'a blue cube'" provides:
                #   [something hasColor blue, something rdf:type Cube] where something is known in the ontology as [* focusesOn something]
                # E.g "this is 'my cube'" should provide [something belongsTo *]
                if subject_quantifier == 'ONE':
                    process_all_component_of_a_nominal_group(ng, ng_id, subject_quantifier, negative_object)
                
                # Case of an infinite nominal group
                # E.g "Apples are Yellow Fruits",  or "An apple is a yellow fruit"
                #   it is wrong to create the statement [Apples hasColor yellow], as it transforms "Apple" into on instance
                elif ng.noun and \
                    subject_quantifier in ['SOME', 'ALL'] and \
                        ng._quantifier in ['SOME', 'ALL']:
                    self.process_noun_phrases(ng, ng_id, subject_quantifier, negative_object)
            
        #Case of a not resolved nominal group
        else:
            process_all_component_of_a_nominal_group(ng, ng_id, subject_quantifier, negative_object)
                
            

    def process_determiners(self, nominal_group, ng_id, negative_object):
        for det in nominal_group.det:
            #logging.debug("Found determiner:\"" + det + "\"")
            # Case 1: definite article : the"""
            # Case 2: demonstratives : this, that, these, those"""
            if det in ResourcePool().demonstrative_det: #['this', 'that', 'these', 'those']:
                self._statements.append(self._current_speaker + " focusesOn " + ng_id)
            # Case 3: possessives : my, your, his, her, its, our, their """
            if det == "my" and not negative_object:
                self._statements.append(ng_id + " belongsTo " + self._current_speaker)
            elif det == "your" and not negative_object:
                self._statements.append(ng_id + " belongsTo myself")
            # Case 4: general determiners: See http://www.learnenglish.de/grammar/determinertext.htm"""
            
    
    def process_noun_phrases(self, nominal_group, ng_id, ng_quantifier, negative_object):
        
        def get_object_property(subject_quantifier, object_quantifier):
            """ The following returns the appropriate object property relationship between two nominal groups; the subject and the object.
                These are the rule:
                    - ONE + ONE => rdf:type ; 
                        E.g: [The blue cube] is [small]. 
                        Here, both nominal groups of 'the blue cube' and 'small' hold the quantifier 'ONE'
                    
                    - ONE + SOME => rdf:type; 
                        E.g: [The blue object] is [a robot]. 
                        Here, the nominal group of robot holds the indefinite quantifier 'SOME'
                    
                    - SOME + SOME => rdfs:subClassOf;
                        E.g: [an apple] is [a fruit].
                        Both the quantifier of the nominal groups of "apple" and "fruit" are 'SOME'.
                        This is a convention for all nomina group with an indefinite determiner
                        
                    - ALL + ALL => rdfs:subClassOf ;
                        E.g: [Apples] are [fruits].
                        E.g: [the apples] are [the fruits].
                        Here, both Apples and Fruits hold the quantifier 'ALL'. 
                        This is a convention for all nominal group with plural nouns
                    
                    for more details about quantifiers, see sentence.py 
            """
            if [subject_quantifier, object_quantifier] in [['SOME', 'SOME'],
                                                               ['ALL', 'ALL']]:
                return ' rdfs:subClassOf '
                
            else:#default case
                return ' rdf:type '
                
        # End of def get_object_property()
        
        
        for noun in nominal_group.noun:
            # Case : existing ID
            onto_id = ''
            try:
                onto_id = ResourcePool().ontology_server.lookupForAgent(self._current_speaker, noun)
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
            
            if onto_id and [noun,"INSTANCE"] in onto_id:
                logging.info("... \t" + noun + " is an existing ID in " + self._current_speaker + "'s model.")            
                #Case of Negation
                if negative_object:
                    self._statements.append(ng_id + " owl:differentFrom " + noun)
                
                #Case of affirmative form
                else:
                    pass
            
            # Case : Personal pronoun
            elif not nominal_group.det and noun in ["I", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "their"]:
                # Case of negation
                if negative_object:
                    # assign noun_id == current_speaker ID or Current receipient, or so on
                    noun_id = None
                    
                    if noun in ["I", "me"]:
                        noun_id = self._current_speaker
                    elif noun in ["you"]:
                        noun_id = "myslef"
                    
                    if noun_id:
                        self._statements.append(ng_id + " owl:differentFrom " + noun_id)
                    else:
                        logging.debug("Aie Aie!! Personal pronoun " + noun + " Not implemented yet!")
                
                # Case of affirmative form
                else:
                    pass
            
            #Case : proper noun (Always Capitalized in sentence, and never follows a determiner) 
            elif not nominal_group.det and noun.istitle():
                logging.info("... \t" + noun + " is being processed as a proper noun in  " + self._current_speaker + "'s model.")            
                self._statements.append(ng_id + " rdfs:label \"" + noun + "\"")
            
            # Case : common noun    
            else:
                logging.info("... \t" + noun + " is being processed as a common noun in " + self._current_speaker + "'s model.")            
                # get the exact class name (capitalized letters where needed)
                class_name = get_class_name(noun, onto_id)
                
                # get the exact object property (subClassOf or type)
                object_property = get_object_property(ng_quantifier, nominal_group._quantifier)
                
                # Case of negation
                if negative_object:
                    # Case of a definite concept
                    if nominal_group._quantifier == 'ONE':
                        self._statements.append(ng_id + " owl:differentFrom " + nominal_group.id)
                    
                    # Case of an indefinite concept
                    else:
                        #Committing ComplementOf class
                        try:
                            ResourcePool.ontology_server.safeAdd(["ComplementOf" + class_name + " owl:complementOf " + class_name,
                                                                    "ComplementOf" + class_name + " rdfs:subClassOf ComplementClasses"])
                        except AttributeError:
                            pass
                            
                        self._statements.append(ng_id + object_property + "ComplementOf" + class_name)
                    
                    
                # Case of affirmative sentence
                else:
                    self._statements.append(ng_id + object_property + class_name)
                    
    
    def process_adjectives(self, nominal_group, ng_id, negative_object):
        """For any adjectives, we add it in the ontology with the objectProperty 
        'hasFeature' except if a specific category has been specified in the 
        adjectives list.
        """
        for adj in nominal_group.adj:
            #Case of 'other'
            # E.g: the other cube:
            if adj[0].lower() == "other":
                self.process_on_other = True
                pass
                #self._statements.append(ng_id + " owl:differentFrom " + nominal_group.id)
                
            
            #TODO: case of class Feature
            # Apple are yellow fruits
            
            # Case of features
            else:
                #Getting the object property if there exists a specific class
                object_property = ''
                try:
                    object_property = " has" + ResourcePool().adjectives[adj[0]] + " "
                
                #Default case, creating hasFeature object Property
                except KeyError:
                    object_property = " hasFeature "
                    
                #Case negative assertion
                if negative_object:
                    negative_adj = generate_id(with_question_mark = not nominal_group._resolved)
                    
                    self._statements.append(ng_id + object_property + negative_adj)
                    self._statements.append(negative_adj + ' owl:differentFrom ' + adj[0])
                
                #Case Affirmative assertion
                else:
                    self._statements.append(ng_id + object_property + adj[0])
                        
    
    
    def process_noun_cmpl(self, nominal_group, ng_id, negative_object):
        """This attempts to process the noun complment attribute of a nominal group:
            E.g: The car of Danny
            This example should provide the statements [danny_car rdf:type Car, 
                                                        danny_car belongsTo DANNY]
            where 'danny_car' is the existing ID od the car of Danny in the ontology and
            'DANNY' is the ID of an existing agent named 'Danny'
        """
        
        for noun_cmpl in nominal_group.noun_cmpl:
            if noun_cmpl.id:
                noun_cmpl_id = noun_cmpl.id
            else:
                noun_cmpl_id = self.set_nominal_group_id(noun_cmpl)
            
            self.process_nominal_group(noun_cmpl, noun_cmpl_id, None, False)
            
            # Case of affirmation
            if not negative_object:
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
        def set_relative_object_id_with_parent_nominal_goup_id(parent_ng, current_relative, parent_ng_id):
            #get parent ng with no relative
            current_ng = parent_ng
            current_ng.relative = []
            
            #set comparator
            cmp = Comparator()
            
            #Start comparison between current_ng and current_relative
            for sv in current_relative.sv:
                #direct object
                for d_obj in sv.d_obj:
                    if cmp.compare(d_obj, current_ng):
                        d_obj.id = parent_ng_id
                
                #indirect object
                for i_cmpl in sv.i_cmpl:
                    for i_cmpl_ng in i_cmpl.nominal_group:
                        if cmp.compare(i_cmpl_ng, current_ng):
                            i_cmpl_ng.id = parent_ng_id

        for rel in nominal_group.relative:
            #logging.debug("processing relative:")
            if rel.sv:
                rel_vg_stmt_builder = VerbalGroupStatementBuilder(rel.sv, self._current_speaker)
            #case 1   
            if rel.sn:
                set_relative_object_id_with_parent_nominal_goup_id(nominal_group, rel, ng_id)
                
                rel_ng_stmt_builder = NominalGroupStatementBuilder(rel.sn, self._current_speaker)
                for ng in rel.sn:
                    ng.id = rel_ng_stmt_builder.set_nominal_group_id(ng)
                    
                    rel_ng_stmt_builder.process_nominal_group(ng, ng.id, None, False)    
                    rel_vg_stmt_builder.process_verbal_groups(rel.sv, ng.id, None)
                    
                self._statements.extend(rel_ng_stmt_builder._statements)
                self._unclarified_ids.extend(rel_ng_stmt_builder._unclarified_ids)
                self.lear_more_concept.extend(rel_ng_stmt_builder.lear_more_concept)
            #case 2        
            else:
                rel_vg_stmt_builder.process_verbal_groups(rel.sv, ng_id, None)
            
            self._statements.extend(rel_vg_stmt_builder._statements)
            self._unclarified_ids.extend(rel_vg_stmt_builder._unclarified_ids)
            self.lear_more_concept.extend(rel_vg_stmt_builder.lear_more_concept)

class VerbalGroupStatementBuilder:
    """ Build statements related to a verbal group"""
    def __init__(self, verbal_groups, current_speaker = None):
        #This field keeps record of the verbal group that is being processed
        self._verbal_groups = verbal_groups
        
        #This field identifies the current speaker
        self._current_speaker = current_speaker
        
        #This holds the statements created from the main clause of a sentence
        self._statements = []
        
        #This holds unidentified IDs that are generated while creating the statements of a resolved sentence.
        #   Possibly in the case of a negative sentence involving an action that is to be identity in the module StatementSafeAdder
        self._unclarified_ids = []        
        
        #This field holds the value True when the active sentence is of yes_no_question or w_question data_type
        self._process_on_question = False
        
        #This field holds the value True when the active sentence is of imperative data_type
        self._process_on_imperative = False
        
        #This field holds the value True when the active sentence is fully resolved
        self._process_on_resolved_sentence = False
        
        #this field is True when the verbal group is in the negative form
        self._process_on_negative = False
        
        #this fiels is True when the sentence that is being processed holds a negative state and 
        # more particualrly in the case of action verbs where a static situation reference is generated
        self.process_statements_to_remove = False
        
        #This field holds concepts for class grounding
        self.lear_more_concept = []

    def set_attribute_on_data_type(self, data_type):
        if data_type == 'imperative':
            self._process_on_imperative = True
        if data_type in ['yes_no_question', 'w_question']:
            self._process_on_question = True
        
    def clear_statements(self):
        self._statements = []
    
    def process(self, subject_id = None, subject_quantifier = None):
        """This processes a sentence sv attribute, given the (resolved) ID and quantifier of the subject
            and return a set of RDF statements.
        """
        #Case: an imperative sentence does not contain an sn attribute,
        #      we will assume that it is implicitly an order from the current speaker.
        #      performed by the recipient of the order.
        #      Therefore, the subject_id holds the value 'myself'
        if self._process_on_imperative:
            subject_id = 'myself'
            
        if not subject_id:
            subject_id = '?concept'       
        
        self.process_verbal_groups(self._verbal_groups, subject_id, subject_quantifier)                
        return self._statements
   
    def get_statements(self):
        return self._statements
    
    
    
    def process_verbal_groups(self, verbal_groups, subject_id, subject_quantifier, second_verb_sit_id = None):
        """This processes every single verbal group in the sentence sv, given the (resolved) ID and quantifier of the subject.
        """
        for vg in verbal_groups:         
            #Verbal group state : Negative or affirmative
            self.process_state(vg)
            
            #Main verb
            if vg.vrb_main:
                self.process_verb(vg, subject_id, subject_quantifier, second_verb_sit_id)
            
            if vg.advrb:
                self.process_sentence_adverb(vg)
            
            # Subordinating clause
            if vg.vrb_sub_sentence:
                self.process_vrb_subsentence(vg)   

    
    def process_state(self, verbal_group):
        if verbal_group.state == 'negative':
            self._process_on_negative = True
        else:
            self._process_on_negative = False
    
    
    def process_verb(self, verbal_group, subject_id, subject_quantifier, second_verb_sit_id):
         
        for verb in verbal_group.vrb_main:
         
            #TODO: modal verbs e.g can+go
            
            #Case 1:  the linking verb 'to be'/"""
            #Case 2:  actions or stative verbs with a specified 'goal' or 'thematic' role:
            #                          see '../../share/dialog/thematic_roles'
            #Case 3:  other action or stative verbs
            
            goal_verbs = ResourcePool().goal_verbs 
            
            
            #Case 1:
            if verb == "be":
                sit_id = subject_id
                
            else:
                #Case : the verbal group that is being processed is the second verbs . i.e : it is held in the field sentence.sv.sv_sec
                if second_verb_sit_id:
                    sit_id = second_verb_sit_id
                
                # Case of question
                elif self._process_on_question:
                    sit_id = '?event'
                
                #case of negation : Creating a fake ID that is to find in the ontology for later removal
                #   Setting up the field process_statement_to_remove to True
                elif self._process_on_negative:
                    sit_id = generate_id(with_question_mark = True)
                    self._unclarified_ids.append(sit_id)
                    self.process_statements_to_remove = True
                    
                else:
                    sit_id = generate_id(with_question_mark = not self._process_on_resolved_sentence)
                
                #Case 2:                
                if verb in goal_verbs:
                    self._statements.append(subject_id + " desires " + sit_id)
                    
                    if verbal_group.sv_sec:
                        self.process_vrb_sec(verbal_group, subject_id, subject_quantifier, sit_id)                      
                #Case 3:   
                else:
                    # Modals verbs. E.g: can, must, ...
                    #                   verb = must+do 
                    if '+' in verb:
                        [modal, verb] = verb.split('+')
                        self._statements.append(sit_id + " rdf:type " + verb.capitalize())
                        self._statements.append(subject_id+ " " + modal +"Performs " + sit_id)
                    
                    else:
                        self._statements.append(sit_id + " rdf:type " + verb.capitalize())
                        self._statements.append(sit_id + " performedBy " + subject_id)
            
            #Imperative specification, add the goal verb 'desire'
            if self._process_on_imperative:
                self._statements.append(self._current_speaker + " desires " + sit_id)
            
            
            #Direct object
            if verbal_group.d_obj:
                self.process_direct_object(verbal_group.d_obj, verb, sit_id, subject_quantifier)
            
            
            #Indirect Complement
            if verbal_group.i_cmpl:
                self.process_indirect_complement(verbal_group.i_cmpl, verb, sit_id)
            
            # Adverbs modifiying the manner of an action verb
            if verbal_group.vrb_adv:
                self.process_action_verb_adverb(verbal_group.vrb_adv, verb, sit_id)
            
            
            #verb tense
            if verbal_group.vrb_tense:
                self.process_verb_tense(verbal_group.vrb_tense, verb, sit_id)
            
            
    def process_vrb_sec(self, verbal_group, subject_id, subject_quantifier, sit_id):
        vrb_sec_builder = VerbalGroupStatementBuilder(verbal_group.sv_sec, self._current_speaker)
        vrb_sec_builder.process_verbal_groups(verbal_group.sv_sec, subject_id, subject_quantifier, sit_id)
        self._statements.extend(vrb_sec_builder._statements)
        self._unclarified_ids.extend(vrb_sec_builder._unclarified_ids)
        self.lear_more_concept.extend(vrb_sec_builder.lear_more_concept)
            
    def process_direct_object(self, d_objects, verb, id, quantifier):
        """This processes the attribute d_obj of a sentence verbal groups."""
        #logging.debug("Processing direct object d_obj:")
        d_obj_stmt_builder = NominalGroupStatementBuilder(d_objects, self._current_speaker)
        
        #Thematic roles
        """
        #TODO: Bug on Thematic Role - Need to check deterministic behaviour with the roles given by Resources pool manager
        thematic_roles = ResourcePool().thematic_roles
       
        try:
            d_obj_role = thematic_roles.get_next_cmplt_role(verb, True)
        except:
            d_obj_role = " involves "
        """
        #TODO with thematic Role
        if verb.lower() in ['get','take','pick', 'put', 'give', 'see', 'show', 'bring', 'move', 'go', 'hide', 'place']:
            d_obj_role = " actsOnObject "
        else:
            d_obj_role = " involves "
        #nominal groups
        for d_obj in d_objects:
            #Case 1: The direct object follows the verb 'to be'.
            #        We process the d_obj with the same id as the subject of the sentence
            if verb == "be":
                d_obj_id = id
                d_obj_quantifier = quantifier
            
            
            #Case 2: The direct object follows another stative or action verb.
            #        we process the d_obj as involved by the situation
            else:
                if d_obj.id:
                    d_obj_id = d_obj.id
                else:
                    d_obj_id = d_obj_stmt_builder.set_nominal_group_id(d_obj)
                
                if d_obj_role:
                    self._statements.append(id + d_obj_role + d_obj_id)
                    
                d_obj_quantifier = None
            
            d_obj_stmt_builder.process_nominal_group(d_obj, d_obj_id, d_obj_quantifier, self._process_on_negative)
            
        self._statements.extend(d_obj_stmt_builder._statements)
        self._unclarified_ids.extend(d_obj_stmt_builder._unclarified_ids)
        self.lear_more_concept.extend(d_obj_stmt_builder.lear_more_concept)
        
            
    def process_indirect_complement(self, indirect_cmpls,verb, sit_id):
        
        #Thematic roles
        thematic_roles = ResourcePool().thematic_roles
        
        for ic in indirect_cmpls:
           
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
                
                #Indirect object ID
                if ic_noun.id:
                    ic_noun_id = ic_noun.id
                else:
                    ic_noun_id = i_stmt_builder.set_nominal_group_id(ic_noun)
                
                
                #Proposition role
                icmpl_role = None
                
                # Case of no preposition
                if not ic.prep:
                    icmpl_role = " receivedBy " 
                    
                # Case of a preposition. Attempt to get from thematic roles
                else:
                    try:
                        icmpl_role = thematic_roles.get_cmplt_role_for_preposition(verb, ic.prep[0], True)
                    except:
                        icmpl_role = None
                    
                    #TODO in ResourcePool()
                    if not icmpl_role:
                        if ic.prep[0].lower() == 'in+front+of':
                            icmpl_role = " isLocated "
                            ic_noun_id = "FRONT"
                        
                        elif ic.prep[0].lower() == 'next+to':
                            icmpl_role = " isNexto "
                        
                        elif ic.prep[0].lower() == 'behind':
                            icmpl_role = " isLocated "
                            ic_noun_id = "BACK"
                        elif ic.prep[0].lower() == 'for' :
                            icmpl_role = " isRelatedTo "
                    
                # Case of prepostion but thematic roles not found
                if not icmpl_role and ic.prep:
                    icmpl_role = " is" + ic.prep[0].capitalize() + " "
                
                
                #Creating statements
                # Case of negation
                if self._process_on_negative:
                    negative_ic_noun_id = generate_id(with_question_mark = False)
                    self._statements.append(sit_id + icmpl_role + negative_ic_noun_id)
                    self._statements.append(negative_ic_noun_id + ' owl:differentFrom ' + ic_noun_id)
                    
                # Case of affirmation
                else:
                    self._statements.append(sit_id + icmpl_role + ic_noun_id)
                
                
                i_stmt_builder.process_nominal_group(ic_noun, ic_noun_id, None, False)
                
            self._statements.extend(i_stmt_builder._statements)
            self._unclarified_ids.extend(i_stmt_builder._unclarified_ids)
            self.lear_more_concept.extend(i_stmt_builder.lear_more_concept)
                
                
    #TODO:      
    def process_sentence_adverb(self, advrb, verb, id):
        for adv in advrb:
            logging.debug("Found adverbial phrase:\"" + adv + "\"")
            
    
    def process_action_verb_adverb(self, advrb ,verb, id):
        """This provides a solution in order to process adverbs modifying the meaning of the action verbs.
            Stative verbs are not taken into consideration.
            
            Eg: Danny 'slowly' drives the blue car.
            In this example, we may want to create the following statements: 
                [ * rdf:type Drive, 
                  * performedBy id_dany,
                  * involves id_blue_car,
                  ...
                  * actionSupervisionMode SLOW]
            
            However, this solution is not appropriate for stative verb. It wouldn't make sense to say "Danny is slowly a human".
        """
        
        if verb == 'be':
            info.debug("Trying to process an adverb that aim to modify an action verb with the sative verb 'To Be' ... No method implemented!")
        else:
            for adv in advrb:
                #Creating statement [id actionSupervisionMode pattern], where if adv == carefully then pattern = CAREFUL, if adv == slowly then pattern = SLOW, ...
                self._statements.append(id + " actionSupervisionMode "+ adv[:len(adv) - 2].upper())
            
            
    def process_verb_tense(self, vrb_tense, verb, id):
        """This provides a solution to process verb tense for action verbs ONLY.
        we create the object property 'eventOccurs' and bind it with the flag PAST or FUTUR
        
            E.g: Danny 'went' to Toulouse.
            In this example we may want to create the statements:
            [* rdf:type Go,
             * performedBy id_anny,
             * hasGoal id_toulouse,
             ...
             
             * eventOccurs PAST]
             
            Although, we do not implement this for stative verb, it may be adapted in the case of describing objects feature, location, and so on.
            Therefore, we need to create new object properties.
                E.g : 'hasFeature' may be turned into 'hadFeature' and 'willHaveFeature'
                      'isOn' may be turned into 'wasOn' and 'willBeOn'.
            
            It would not work for object type or class, as it does not make sense to say "Fruits were Plants".
        """
        
        #Assiging the variable 'tense' with either PAST or FUTUR
        tense = '' #Nothing to do if the verb tense involves the present
        
        #PAST
        if vrb_tense in ['past simple', 'present perfect']:
            tense = 'PAST'
        
        #FUTUR
        if vrb_tense in ['future simple', 'future progressive']:
            tense = 'FUTUR'
        
        if verb != 'be' and tense:
            self._statements.append(id + ' eventOccurs ' + tense)
            
            
    def process_vrb_subsentence(self, verbal_group):
        pass
        
            
"""
    The following function are not implemented for a specific class
"""
def get_class_name(noun,conceptL):
    """Simple function to obtain the exact class name"""
    for c in conceptL:
        if 'CLASS' in c: return c[0]
    
    return noun.capitalize()
     

def generate_id(with_question_mark = True):
    sequence = "0123456789abcdefghijklmopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sample = random.sample(sequence, 5)
    return ("?" + "".join(sample)) if with_question_mark else ("".join(sample))


"""
    The following functions are implemented for test purpose only
"""
        
def dump_resolved(sentence, current_speaker, current_listener):
    def resolve_ng(ngs, builder):        
        for ng in ngs:
            if ng._quantifier != 'ONE':
                logging.info("\t...No Statements sended to Resolution for discrmination for this nominal group...")
                
            else:
                #Statement for resolution
                logging.info("Statements sended to Resolution for discrmination for this nominal group...")
                print(ng)
                builder.process_nominal_group(ng, '?concept', None, False)
                stmts = builder.get_statements()
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


        
class TestStatementBuilder(unittest.TestCase):

    def setUp(self):
        
        try:
            ResourcePool().ontology_server.add(['SPEAKER rdf:type Human',
                                                'SPEAKER rdfs:label "Patrick"'])
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass
        
        try:
            
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
        #return self.process(sentence, expected_result, display_statement_result = True)
        #
        #otherwise, use the following if you want to hide the statements 
        #return self.process(sentence, expected_result)
        #    or
        #return self.process(sentence, expected_result, display_statement_result = False)
        #
    """
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
                                           [Nominal_Group(['the'],['car'],['blue'],[],[])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])    
        
        expected_result = ['* rdf:type Drive',
                           '* performedBy id_danny',
                           '* involves volvo']
        
        return self.process(sentence, expected_result, display_statement_result = True)
    
    
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
                                           [Nominal_Group(['the'],['car'],['blue'],[],[])],
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
                                                                   [Nominal_Group(['the'],['car'],['blue'],[],[])],
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
                                                          ['blue'],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_result = ['volvo hasColor blue']   
        return self.process(sentence, expected_result, display_statement_result = True)
        
    
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
                                                          ['small'],
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
                                                          ['small'],
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
                                           [Nominal_Group(['the'],['bottle'],['green'],[],[])],
                                           [Indirect_Complement(['in'],
                                                                [Nominal_Group(['the'],['car'],['blue'],[],[])]) ],
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
    """
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
                                                          ['blue'],
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
    
    
    """
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
                                            ['blue'],
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
                                                          ['blue'],
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
        return self.process(sentence, expected_result, display_statement_result = True)
    
    
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
                                                          ['blue'],
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
        return self.process(sentence, expected_result, display_statement_result = True)
    
    
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
                                                          ['blue'],
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
                                                          ['blue'],
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
                                          [Nominal_Group([],[],['blue'],[],[])],
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
        return self.process(sentence, expected_result, display_statement_result = True)
    
    
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
        return self.process(sentence, expected_result, display_statement_result = True)
    
    
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
                                                          ['green'],
                                                          [],
                                                          [])],
                                           [],
                                           [],
                                           [],
                                           'negative',
                                           [])])
        expected_result = [ 'shelf1 hasColor *']   
        return self.process(sentence, expected_result, display_statement_result = True)
    
    
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
                                                          ['green'],
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
        return self.process(sentence, expected_result, display_statement_result = True)
    
    
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
        return self.process(sentence, expected_result, display_statement_result = True)
    
    
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
        return self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_24_negative(self):
        print "\n**** test_24_negative *** "
        print "the blue car is not my car"
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['the'],
                                            ['car'],
                                            ['blue'],
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
        return self.process(sentence, expected_result, display_statement_result = True)
    
    
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
        return self.process(sentence, expected_result, display_statement_result = True)
    
    """
    
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
        return self.process(sentence, expected_result, display_statement_result = True)
    

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
        return self.process(sentence, expected_result, display_statement_result = True)
    
    
    def test_28_subsentences(self):
        print "\n**** test_28_subsentences *** "
        print "I am going to toulouse when you get the small car."
        
        subsentence = Sentence('subsentence', 'when', 
                                [Nominal_Group([],['you'],[],[],[])], 
                                [Verbal_Group(['get'], [],'present simple', 
                                    [Nominal_Group(['the'],['car'],['small'],[],[])], 
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
                            
        return self.process(sentence, expected_result, display_statement_result = True)
    
    """
    
    def process(self, sentence, expected_result, display_statement_result = False):
        #Dump resolution
        sentence = dump_resolved(sentence, self.stmt._current_speaker, 'myself')#TODO: dumped_resolved is only for the test of statement builder. Need to be replaced as commented above
        
        #StatementBuilder
        res = self.stmt.process_sentence(sentence)
        
        #Statement Safe Adder
        self.adder._unclarified_ids = self.stmt._unclarified_ids
        self.adder._statements = res
        self.adder._statements_to_remove = self.stmt._statements_to_remove
        res = self.adder.process()
        
        #Assert result
        self.assertTrue(self.check_results(res, expected_result))
        
        

    def check_results(self, res, expected):
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
        
        
def unit_tests():
    """This function tests the main features of the class StatementBuilder"""
    logging.basicConfig(level=logging.DEBUG,format="%(message)s")
    print("This is a test...")
    unittest.main()
     
if __name__ == '__main__':
    unit_tests()
    

    


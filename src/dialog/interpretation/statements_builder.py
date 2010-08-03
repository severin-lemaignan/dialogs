#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from helpers import colored_print

import random
import inspect
import unittest
from resources_manager import ResourcePool
from statements_safe_adder import StatementSafeAdder

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
        self._statements.extend(ng_stmt_builder.process())
        self._unresolved_ids.extend(ng_stmt_builder._unresolved_ids)
        
    def process_verbal_groups(self, sentence):
        #VerbalGroupStatementBuilder
        vg_stmt_builder = VerbalGroupStatementBuilder(sentence.sv, self._current_speaker)
        
        #Setting up attribute of verbalGroupStatementBuilder:
        #    process_on_imperative
        #    process_on_question
        vg_stmt_builder.set_attribute_on_data_type(sentence.data_type)
        vg_stmt_builder._process_on_resolved_sentence = sentence.resolved()
        
        if not sentence.sn:
            self._statements.extend(vg_stmt_builder.process())
            self._unresolved_ids.extend(vg_stmt_builder._unresolved_ids)
            
        for sn in sentence.sn:
            if not sn.id:
                raise EmptyNominalGroupId("Nominal group ID not resolved or not affected yet")
            
            self._statements.extend(vg_stmt_builder.process(subject_id = sn.id, subject_quantifier = sn._quantifier))
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
        A NominalGroupStatementBuilder has to be instantiated before"""
        
        for ng in self._nominal_groups:
            if not ng.id:
                ng.id = self.set_nominal_group_id(ng)      
            
            self.process_nominal_group(ng, ng.id, None)
                                    
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
        self._unresolved_ids.append(id)
        return id
    
    
    def process_nominal_group(self, ng, ng_id, subject_quantifier):
        """ The following function processes a single nominal_group with a given resolved ID and quantifier"""
        
        def process_all_component_of_a_nominal_group(nom_grp, id, quantifier):
            """This processes all the components of a given nominal group 'nom_grp'. """
            if nom_grp.noun:
                self.process_noun_phrases(nom_grp, id, quantifier)
            if nom_grp.det:
                self.process_determiners(nom_grp, id)
            if nom_grp.adj:
                self.process_adjectives(nom_grp, id)
            if nom_grp.noun_cmpl:
                self.process_noun_cmpl(nom_grp, id)
            if nom_grp.relative:
                self.process_relative(nom_grp, id)
                
        # End of process_all_component_of_a_nominal_group()
        
        
        # Case of resolved nominal group
        if ng._resolved:
            # Case: Adjectives only
            if ng.adjectives_only():
                self.process_adjectives(ng, ng_id)
            
            #Case: indifinite Quantifier of the nominal group being processed. 
            #       E.g: "jido is a robot" => 'robot' is in a nominal group with an indifinite quantifier 'SOME'
            if subject_quantifier:
                if ng._quantifier != 'ONE' :
                        
                    # Case of an finite nominal group described by an infinite one
                    #
                    # E.g "this is 'a blue cube'" provides:
                    #   [something hasColor blue, something rdf:type Cube] where something is known in the ontology as [* focusesOn something]
                    # However, in E.g "Apples are Yellow Fruits", 
                    #   it is wrong to create the statement [Apples hasColor yellow], as it transforms "Apple" into on instance
                    process_all_component_of_a_nominal_group(ng, ng_id, subject_quantifier)
                    
                else:
                    if ng.noun:
                        self.process_noun_phrases(ng, ng_id, subject_quantifier)
            
        #Case of a not resolved nominal group
        else:
            process_all_component_of_a_nominal_group(ng, ng_id, subject_quantifier)
                
            

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
            
    
    def process_noun_phrases(self, nominal_group, ng_id, ng_quantifier):
        
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
            if [subject_quantifier, object_quantifier] in [['ONE', 'ONE'],
                                                            ['ONE', 'SOME']]:
                return ' rdf:type '
                
            elif [subject_quantifier, object_quantifier] in [['SOME', 'SOME'],
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
                pass
            
            # Case : Personal pronoun
            elif not nominal_group.det and noun in ["I", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "their"]:
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
                
                # get the exac object property (subClass or type)
                object_property = get_object_property(ng_quantifier, nominal_group._quantifier)
                self._statements.append(ng_id + object_property + class_name)            
            
    
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
                noun_cmpl_id = self.set_nominal_group_id(noun_cmpl)
                
            self.process_nominal_group(noun_cmpl, noun_cmpl_id, None)
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
                    
                    rel_ng_stmt_builder.process_nominal_group(ng, ng.id, None)    
                    rel_vg_stmt_builder.process_verbal_groups(rel.sv, ng.id, None)
                    
                self._statements.extend(rel_ng_stmt_builder._statements)
                self._unresolved_ids.extend(rel_ng_stmt_builder._unresolved_ids)
                
            #case 2        
            else:
                rel_vg_stmt_builder.process_verbal_groups(rel.sv, ng_id, None)
            
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
        
        #This fiels holds the value True when the active sentence is fully resolved
        self._process_on_resolved_sentence = False

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
    
    
    
    def process_verbal_groups(self, verbal_groups, subject_id, subject_quantifier):
        """This processes every single verbal group in the sentence sv, given the (resolved) ID and quantifier of the subject.
        """
        for vg in verbal_groups:          
            self.process_state(vg)
            if vg.vrb_main:
                self.process_verb(vg, subject_id, subject_quantifier)
            
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
    
    def process_verb(self, verbal_group, subject_id, subject_quantifier):
         
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
                    sit_id = generate_id(with_question_mark = not self._process_on_resolved_sentence)
                
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
                self.process_direct_object(verbal_group.d_obj, verb, sit_id, subject_quantifier)
            
            
            #Indirect Complement
            if verbal_group.i_cmpl:
                self.process_indirect_complement(verbal_group.i_cmpl, verb, sit_id)
            
                    
                    
                
            
    def process_vrb_sec(self, verbal_group):
        for verb in verbal_group.vrb_sec:
            #logging.debug("Found verb:\"" + verb + "\"")
            pass
            
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
            
            d_obj_stmt_builder.process_nominal_group(d_obj, d_obj_id, d_obj_quantifier)
            
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
                    ic_noun_id = i_stmt_builder.set_nominal_group_id(ic_noun)
                    
                if not ic.prep:
                    self._statements.append(sit_id + " receivedBy " + ic_noun_id)
                    
                elif icmpl_role:
                    self._statements.append(sit_id + icmpl_role + ic_noun_id)
        
                elif ic.prep[0].lower() == 'in+front+of':#TODO in ressource Pool
                    self._statements.append(sit_id + " isLocated FRONT")
                elif ic.prep[0].lower() == 'next+to':#TODO in ressource Pool
                    self._statements.append(sit_id + " isNexto " + ic_noun_id)
                elif ic.prep[0].lower() == 'behind':#TODO in ressource Pool
                    self._statements.append(sit_id + " isLocated BACK")
                    
                else:
                    self._statements.append(sit_id + " is" + ic.prep[0].capitalize()+ " " + ic_noun_id)
                
                
                i_stmt_builder.process_nominal_group(ic_noun, ic_noun_id, None)
                
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
                builder.process_nominal_group(ng, '?concept', None)
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
            
            elif ng._quantifier != 'ONE':
                
                logging.debug("... Found nominal group with quantifier " + ng._quantifier)
                onto_class = ''
                try:
                    onto_class =  ResourcePool().ontology_server.lookupForAgent(current_speaker, ng.noun[0])
                except AttributeError: #the ontology server is not started of doesn't know the method
                    pass
                
                ng.id = get_class_name(ng.noun[0], onto_class)
                
                
            elif ng.adjectives_only():
                ng.id = '*'
            
            #personal pronoun
            elif ng.noun in [['me'], ['Me'],['I']]:
                ng.id = current_speaker
            elif ng.noun in [['you'], ['You']]:
                ng.id = current_listener                       
            
            #common noun
            elif [ng.noun, ng.det, ng.adj] == [['car'], ['my'],[]]:
                ng.id = 'volvo'                
            elif [ng.noun, ng.det, ng.adj] == [['bottle'], ['the'], []]:
                ng.id = 'a_bottle'
            elif [ng.noun, ng.det, ng.adj] == [['man'], ['the'], []]:
                ng.id = 'a_man'
            elif [ng.noun, ng.adj, ng.det] == [['car'], ['blue'], ['the']]:
                ng.id = 'blue_car'
            elif [ng.noun, ng.adj, ng.det] == [['cube'], ['blue'], ['a']]:
                ng.id = 'blue_cube'
            elif [ng.noun, ng.adj, ng.det] == [['car'], ['small'], ['a']]:
                ng.id = 'twingo'
            
            
            #proper noun
            elif ng.noun == ['Danny']:
                ng.id = 'id_danny' 
            elif ng.noun == ['Jido']:
                ng.id = 'id_jido'
            elif ng.noun == ['Toulouse']:
                ng.id = 'id_toulouse'
                   
            #existing ID
            elif ng.noun == ['twingo']:
                ng.id = 'twingo'            
            elif ng.noun == ['shelf1']:
                ng.id = 'shelf1'
            
            #existing ID with lookupForAgent on the ontology 
            elif ng.det in [['this'], ['that']]:
                onto_focus = ''
                try:
                    onto_focus =  ResourcePool().ontology_server.findForAgent(current_speaker, '?concept', [current_speaker + ' focusesOn ?concept'])
                except AttributeError: #the ontology server is not started of doesn't know the method
                    pass
                    
                if onto_focus:
                    ng.id = onto_focus[0]
                    
            elif [ng.noun, ng.det, ng.adj] == [['car'], ['the'],[]]:
                onto_fiat = ''
                try:
                    onto_fiat =  ResourcePool().ontology_server.findForAgent(current_speaker, '?concept',['?concept belongsTo ?a', '?concept rdf:type Car','?a belongsTo id_danny'])
                except AttributeError: #the ontology server is not started of doesn't know the method
                    pass
                    
                if onto_fiat:    
                    ng.id = onto_fiat[0]
                
            #Else
            else:
                pass
            
            
            #Other Nominal group attibutes
            if ng.noun_cmpl and not ng._resolved:
                ng.noun_cmpl = resolve_ng(ng.noun_cmpl, builder)
            if ng.relative and not ng._resolved:
                for rel in ng.relative:
                    rel = dump_resolved(rel, current_speaker, current_listener)
            
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
        print "Danny drives the blue car"  
        sentence = Sentence("statement", "", 
                             [Nominal_Group([],
                                            ['Danny'],
                                            [],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['drive'],
                                           [],
                                           'present_simple',
                                           [Nominal_Group(['the'],['car'],['blue'],[],[])],
                                           [],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])    
        
        expected_result = ['* rdf:type Drive',
                           '* performedBy id_danny',
                           '* involves blue_car']
        
        return self.process(sentence, expected_result, display_statement_result = True)
    
        
    
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
                                           'present_simple',
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
                                           None,
                                           'present_simple',
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
                                           'present_simple',
                                           [],
                                           [Indirect_Complement(['to'], [Nominal_Group([],['Toulouse'],[],[],[])])],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['* rdf:type Go',
                          '* performedBy SPEAKER',
                          '* hasGoal id_toulouse']
        return self.process(sentence, expected_resut, display_statement_result = True)
        
    
    def test_8(self):
        print "\n**** Test 8  *** "
        print "put the bottle in the blue car"
        sentence = Sentence("imperative", "", 
                             [],                                         
                             [Verbal_Group(['put'],
                                           [],
                                           'present_simple',
                                           [Nominal_Group(['the'],['bottle'],[],[],[])],
                                           [Indirect_Complement(['in'],
                                                                [Nominal_Group(['the'],['car'],['blue'],[],[])]) ],
                                           [],
                                           [],
                                           'affirmative',
                                           [])])
        expected_resut = ['SPEAKER desires *',
                          '* rdf:type Put',
                          '* performedBy myself',
                          '* actsOnObject a_bottle',
                          '* isIn blue_car']  
        

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
                                           'present_simple',
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
        #Quantifier
        sentence.sv[0].d_obj[0]._quantifier = 'SOME' # a blue cube
        expected_resut = ['another_cube rdf:type Cube',
                            'another_cube hasColor blue']
                          
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
                                           'present_simple',
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
                                           'present_simple',
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
                                           'present_simple',
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
    
    
    
    def test_13_this(self):
        
        print "\n**** test_13_this  *** "
        print "this cube is blue "
        sentence = Sentence("statement", "", 
                             [Nominal_Group(['this'],
                                            ['cube'],
                                            ['blue'],
                                            [],
                                            [])],                                         
                             [Verbal_Group(['be'],
                                           [],
                                           'present_simple',
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
                                           'present_simple',
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
                                           'present_simple',
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
    
    
    def process(self, sentence, expected_result, display_statement_result = False):
         
        sentence = dump_resolved(sentence, self.stmt._current_speaker, 'myself')#TODO: dumped_resolved is only for the test of statement builder. Need to be replaced as commented above
        res_stmt_builder = self.stmt.process_sentence(sentence)        
        self.stmt_adder._statements = res_stmt_builder
        self.stmt_adder._unresolved_ids = self.stmt._unresolved_ids
        self.stmt_adder.process(sentence.resolved())
        res = self.stmt_adder._statements
        
        
        if display_statement_result:
            logging.info( "*** StatementSafeAdder result from " + inspect.stack()[1][3] + " ****")
            for s in res:
                logging.info("\t >> " + s)            
            logging.info("\t --------------  << ")
        
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
    

    


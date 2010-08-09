#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from helpers import colored_print

from dialog_exceptions import UnsufficientInputError, UnknownVerb, UnresolvedAnaphora
from resources_manager import ResourcePool
from statements_builder import NominalGroupStatementBuilder, get_class_name #for nominal group discrimination
from discrimination import Discrimination
from anaphora_matching import AnaphoraMatcher
from sentence import SentenceFactory, Comparator

class Resolver:
    """Implements the concept resolution mechanisms.
    Three operations may be conducted:
     - references + anaphors resolution (replacing "I, you, me..." and "it, one"
     by the referred concepts)
     - noun phrase resolution (replacing "the bottle on the table" by the right
     bottle ID). This is achieved in the discrimination module.
     - verbal phrase resolution (replacing action verbs by verbs known to the 
     robot, by looking for the semantically closest one). This is done by the
     action_matcher module.
    
    """
    def __init__(self, sentences_store = []):
        self._current_sentence = None
        self.sentences_store = sentences_store
        
    def references_resolution(self, sentence, current_speaker, current_object):
              
        logging.info(colored_print("-> Resolving references and anaphors...", 'green'))
        #Record of current sentence
        self._current_sentence = sentence
        
        
        #Anaphoric resolution
        matcher = AnaphoraMatcher()
        
        #sentence sn nominal groups reference resolution
        if sentence.sn:
            sentence.sn = self._resolve_groups_references(sentence.sn, matcher, current_speaker)
        
        
        #sentence sv nominal groups reference resolution
        for sv in sentence.sv:
            if sv.d_obj:
                sv.d_obj = self._resolve_groups_references(sv.d_obj,
                                                            matcher,
                                                            current_speaker)
            if sv.i_cmpl:
                resolved_i_cmpl = []
                for i_cmpl in sv.i_cmpl:
                    i_cmpl.nominal_group = self._resolve_groups_references(i_cmpl.nominal_group, 
                                                                                matcher,
                                                                                current_speaker)
                    resolved_i_cmpl.append(i_cmpl)
                
                sv.i_cmpl = resolved_i_cmpl

        return sentence
        
    def noun_phrases_resolution(self, sentence, current_speaker, uie_object, uie_object_with_more_info):
        logging.info(colored_print("-> Resolving noun phrases", 'green'))
        
        #Nominal group replacement possibly after uie_object and uie_object_with_more_info are sent from Dialog to resolve missing content
        if uie_object and uie_object_with_more_info:
            sentence = self.noun_phrases_replace_with_ui_exception(sentence, uie_object, uie_object_with_more_info)
            
            #No uie_objects needed after replacement
            uie_object = None
            uie_object_with_more_info = None
        
        #Record of current sentence
        self._current_sentence = sentence
        
        #NominalGroupStatementBuilder
        builder = NominalGroupStatementBuilder(None,current_speaker)
        
        #Discrimination
        discriminator = Discrimination()
        
        #sentence.sn nominal groups nouns phrase resolution
        if sentence.sn:
            sentence.sn = self._resolve_groups_nouns(sentence.sn, 
                                                    current_speaker,
                                                    discriminator,
                                                    builder)
        #sentence.sv nominal groups nouns phrase resolution
        for sv in sentence.sv:
            if sv.d_obj:
                sv.d_obj = self._resolve_groups_nouns(sv.d_obj, 
                                                     current_speaker,
                                                     discriminator,
                                                     builder)  
            if sv.i_cmpl:
                resolved_i_cmpl = []
                for i_cmpl in sv.i_cmpl:
                    i_cmpl.nominal_group = self._resolve_groups_nouns(i_cmpl.nominal_group, 
                                                       current_speaker,
                                                       discriminator,
                                                       builder)
                    resolved_i_cmpl.append(i_cmpl)
                sv.i_cmpl = resolved_i_cmpl
                        
        return sentence
        
        
    def noun_phrases_replace_with_ui_exception(self, sentence, uie_object, uie_object_with_more_info):
        
        #Comparator
        cmp = Comparator()
        
        #Trying to replace in sentence sn
        if sentence.sn:
            for sn in sentence.sn:
                if cmp.compare(sn, uie_object):
                    sn = uie_object_with_more_info
                    return sentence
                            
        #Trying to replace in sentence sv nomina groups
        for sv in sentence.sv:
            for d_obj in sv.d_obj:
                if cmp.compare(d_obj, uie_object):
                    d_obj = uie_object_with_more_info                    
                    return sentence                    
            
            for i_cmpl in sv.i_cmpl:
                for ng in i_cmpl.nominal_group:
                    if cmp.compare(ng , uie_object):
                        ng = uie_object_with_more_info                        
                        return sentence       
        
        return sentence

        
    def verbal_phrases_resolution(self, sentence):
        logging.info(colored_print("-> Resolving verbal groups", 'green'))
        for sv in sentence.sv:
            sv = self._resolve_verbs(sv)
                    
        return sentence
        
    def _resolve_references(self, nominal_group, matcher, current_speaker, onto = None):
        
        if nominal_group._resolved: #already resolved: possible after asking human for more details.
            return nominal_group
        
        if nominal_group.adjectives_only():#E.g, 'big' in 'the yellow banana is big'.
            nominal_group.id = '*'
            nominal_group._resolved = True
            return nominal_group
        
        
        if nominal_group._quantifier != 'ONE': # means the nominal group holds an indefinite determiner. E.g a robot, every plant, fruits, ...
            nominal_group.id = get_class_name(nominal_group.noun[0], onto)
            nominal_group._resolved = True
            return nominal_group
        
        
        if not nominal_group.noun:# Nominal group with no noun.
            return nominal_group
        
        #In the following , if there are two nouns in the same sentence
        #they will be split into two different nominal groups. Therefore we can use noun[0]
        if onto and [nominal_group.noun[0],"INSTANCE"] in onto:
            nominal_group.id = nominal_group.noun[0]
            nominal_group._resolved = True
            
        if current_speaker and nominal_group.noun[0].lower() in ['me','i']:
            logging.debug("Replaced \"me\" or \"I\" by \"" + current_speaker + "\"")
            nominal_group.id = current_speaker
            nominal_group._resolved = True
        
        if nominal_group.noun[0].lower() in ['you']:
            logging.debug("Replaced \"you\" by \"myself\"")
            nominal_group.id = 'myself'
            nominal_group._resolved = True
        """
        if current_object and nominal_group.noun[0].lower() in ['it', 'one']:
            logging.debug("Replaced the anaphoric reference \"it\" by " + current_object)
            nominal_group.id = current_object
            nominal_group._resolved = True
        """
        
        if nominal_group.noun[0].lower() in ['it', 'one']:
            try:
                object = matcher.match_first_object(get_last(self.sentences_store, 3))
            except IndexError:
                logging.debug("History empty")
            
            
            if object and object[1] == "FAILLURE":
                sf = SentenceFactory()
                raise UnresolvedAnaphora({'status':'FAILURE', 'question':sf.create_do_you_mean_reference(object[0])}) #raise UnresolvedAnaphora("Plante")
            else:
                raise DialogError("OOoooops!!!")
        return nominal_group
    
    def _resolve_groups_references(self, array_sn, matcher, current_speaker):
        #TODO: We should start with resolved_sn filled with sentence.sn and replace
        # 'au fur et a mesure' to avoid re-resolve already resolved nominal groups
        resolved_sn = []
        for sn in array_sn:
            onto = None
            if sn.noun:
                try:
                    onto = ResourcePool().ontology_server.lookup(sn.noun[0])
                except AttributeError: #the ontology server is not started or doesn't know the method
                    pass
            
            resolved_sn.append(self._resolve_references(sn, matcher, current_speaker, onto))
           
        return resolved_sn
    
    def _resolve_nouns(self, nominal_group, current_speaker, discriminator, builder):

        if nominal_group._resolved: #already resolved: possible after asking human for more details.
            return nominal_group
        
        
        logging.debug(str(nominal_group))
        builder.process_nominal_group(nominal_group, '?concept', None, False)
        stmts = builder.get_statements()
        builder.clear_statements()
        logging.debug("Trying to identify this concept in "+ current_speaker + "'s model: " + colored_print('[' + ', '.join(stmts) + ']', 'bold'))
        
        #Trying to discriminate 
        description = [[current_speaker, '?concept', stmts]]
        try:
            id = discriminator.clarify(description)
        except UnsufficientInputError as uie:
            sf = SentenceFactory()
            uie.value['question'][:0] = sf.create_what_do_you_mean_reference(nominal_group)
            uie.value['object'] = nominal_group
            uie.value['sentence'] = self._current_sentence
            uie.value['object_with_more_info'] = None
            raise uie
        
        logging.debug(colored_print("Hurra! Found \"" + id + "\"", 'magenta'))
        
        nominal_group.id = id
        nominal_group._resolved = True
        
        return nominal_group
    
    def _resolve_groups_nouns(self, nominal_groups, current_speaker, discriminator, builder):
        resolved_sn = []
        for ng in nominal_groups:
            resolved_sn.append(self._resolve_nouns(ng, current_speaker, discriminator, builder))
            
        return resolved_sn
    
    def _resolve_verbs(self, verbal_group):        
        if verbal_group.resolved(): #already resolved: possible after asking human for more details.
            return verbal_group
        
        resolved_verbs = []
        for verb in verbal_group.vrb_main:
            logging.debug("* \"" + verb + "\"")
            try:
                if verb == "be":
                    resolved_verb = "be"
                else: 
                    resolved_verb = ResourcePool().thematic_roles.get_ref(verb)
                
                if verb == resolved_verb:
                    logging.debug("Keeping \"" + verb + "\"")
                else:
                    logging.debug("Replacing \"" + verb + "\" by synonym \"" + 
                              resolved_verb + "\"")
                verbal_group._resolved = True
            except UnknownVerb:
                resolved_verb = verb
                logging.debug("Unknown verb \"" + verb + "\": keeping it like that, but I won't do much with it.")
            resolved_verbs.append(resolved_verb)
        
        verbal_group.vrb_main = resolved_verbs
        
        if verbal_group.sv_sec:
            verbal_group.sv_sec = self._resolve_verbs(verbal_group.sv_sec)
            
        return verbal_group



def get_last(list, nb):
    """This returns the last 'Nb' elements of the history from in the reverse order"""
    last = len(list)
    
    if last > 0 and last > nb:
        stnts = list[(last - nb):last]
    else:
        stnts = list[last]
        
    stnts.reverse()
    
    return stnts



def unit_tests():
    """This function tests the main features of the class Resolver"""
    print("This is a test...")

if __name__ == '__main__':
    unit_tests()

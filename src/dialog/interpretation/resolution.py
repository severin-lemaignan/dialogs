#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from helpers import colored_print

from dialog_exceptions import UnsufficientInputError, UnknownVerb
from resources_manager import ResourcePool
from statements_builder import NominalGroupStatementBuilder #for nominal group discrimination
from discrimination import Discrimination

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
    
    def references_resolution(self, sentence, current_speaker, current_object):
        logging.info(colored_print("-> Resolving references and anaphors...", 'green'))
        
        #sentence sn nominal groups reference resolution
        if sentence.sn:
            sentence.sn = self._resolve_groups_references(sentence.sn, current_speaker, current_object)
        
        
        #sentence sv nominal groups reference resolution
        for sv in sentence.sv:
            if sv.d_obj:
                sv.d_obj = self._resolve_groups_references(sv.d_obj,
                                                               current_speaker,
                                                               current_object)
            if sv.i_cmpl:
                resolved_i_cmpl = []
                for i_cmpl in sv.i_cmpl:
                    i_cmpl.nominal_group = self._resolve_groups_references(i_cmpl.nominal_group, 
                                                                    current_speaker, 
                                                                    current_object)
                    resolved_i_cmpl.append(i_cmpl)
                
                sv.i_cmpl = resolved_i_cmpl

        return sentence
        
    def noun_phrases_resolution(self, sentence, current_speaker):
        logging.info(colored_print("-> Resolving noun phrases", 'green'))
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
        
        
    def verbal_phrases_resolution(self, sentence):
        logging.info(colored_print("-> Resolving verbal groups", 'green'))
        for sv in sentence.sv:
            sv = self._resolve_verbs(sv)
        
        return sentence
        
    def _resolve_references(self, nominal_group, current_speaker, current_object, onto = None):
        
        if nominal_group._resolved: #already resolved: possible after asking human for more details.
            return nominal_group
        
        if not nominal_group.noun:
            return nominal_group
        
        #In the following , if there are two nouns in the same sentence
        #they will be split into two different nominal groups
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
        
        if current_object and nominal_group.noun[0].lower() in ['it', 'one']:
            logging.debug("Replaced the anaphoric reference \"it\" by " + current_object)
            nominal_group.id = current_object
            nominal_group._resolved = True


        return nominal_group
    
    def _resolve_groups_references(self, array_sn, current_speaker, current_object):
        #TODO: We should start with resolved_sn filled with sentence.sn and replace
        # 'au fur et a mesure' to avoid re-resolve already resolved nominal groups
         
        resolved_sn = []
        for sn in array_sn:
            if sn.noun:
                try:
                    onto = ResourcePool().ontology_server.lookup(sn.noun[0])
                    resolved_sn.append(self._resolve_references(sn, current_speaker, current_object, onto))
                except AttributeError: #the ontology server is not started of doesn't know the method
                    pass

        return resolved_sn
    
    def _resolve_nouns(self, nominal_group, current_speaker, discriminator, builder):
        
        if nominal_group._resolved: #already resolved: possible after asking human for more details.
            return nominal_group
            
        logging.debug(str(nominal_group))
        builder.process_nominal_group(nominal_group, '?concept')
        stmts = builder.get_statements()
        #TODO: See the problem below with current speaker.
        #logging.debug("Trying to identify this concept in "+ current_speaker + "'s model:")
        #For Question handler test ONLY, I have turned the above line into:
        logging.debug("Trying to identify this concept in "+ current_speaker + "'s model: " + colored_print('[' + ', '.join(stmts) + ']', 'bold'))
        
        builder.clear_statements()
        #TODO: Problem with the following line when current_speaker holds a different value from  'myself'
        #In order to solve it, Try to catch an exception and report it to user
        #description = [[current_speaker, '?concept', stmts]]
        #For Question handler test ONLY, I have turned the above line into.
        description = [[current_speaker, '?concept', stmts]]

        id = discriminator.clarify(description)
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

def unit_tests():
	"""This function tests the main features of the class Resolver"""
	print("This is a test...")

if __name__ == '__main__':
	unit_tests()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from dialog_exceptions import UnsufficientInputError, UnknownVerb
from resources_manager import ResourcePool

from statements_builder import StatementBuilder #for nominal group discrimination
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
    
    def resolve_references(self, nominal_group, current_speaker, current_object):
        
        if nominal_group._resolved: #already resolved: possible after asking human for more details.
            return nominal_group
        
        if not nominal_group.noun:
            return nominal_group
        
        #TODO: noun[0] is bad! noun should be changed to be a single value instead of an array
        if current_speaker and nominal_group.noun[0].lower() in ['me', 'i']:
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
    
    def resolve_groups_references(self, array_sn, current_speaker, current_object):
        #TODO: We should start with resolved_sn filled with sentence.sn and replace
        # 'au fur et a mesure' to avoid re-resolve already resolved nominal groups
        resolved_sn = []
        for sn in array_sn:
            resolved_sn.append(self.resolve_references(sn, current_speaker, current_object))

        return resolved_sn
            
    def references_resolution(self, sentence, current_speaker, current_object):
        logging.debug("Resolving references and anaphors...")
        
        if sentence.sn:
            sentence.sn = self.resolve_groups_references(sentence.sn, current_speaker, current_object)
        
        
        if sentence.sv.d_obj:
            sentence.sv.d_obj = self.resolve_groups_references(sentence.sv.d_obj,
                                                               current_speaker,
                                                               current_object)
        
        resolved_i_cmpl = []
        for i_cmpl in sentence.sv.i_cmpl:
            i_cmpl.nominal_group = self.resolve_groups_references(i_cmpl.nominal_group, 
                                                            current_speaker, 
                                                            current_object)
            resolved_i_cmpl.append(i_cmpl)
        
        sentence.sv.i_cmpl = resolved_i_cmpl

        return sentence
    
    def resolve_nouns(self, nominal_group, current_speaker, discriminator, builder):
        
        if nominal_group._resolved: #already resolved: possible after asking human for more details.
            return nominal_group
            
        logging.debug("Resolving \"" + str(nominal_group) + "\"")      
        stmts = builder.processNominalGroup([nominal_group], '?concept',{0:'query'})        
        logging.debug("Trying to identify this concept in "+ current_speaker + "'s model:")
        for s in stmts:
            logging.debug(s)
        
        builder.clear_statements()
        
        description = [[current_speaker, '?concept', stmts]]
        
        id = discriminator.clarify(description)
        logging.debug("Hurra! Found \"" + id + "\"")
        
        nominal_group.id = id
        nominal_group._resolved = True
        
        return nominal_group
    
    def resolve_groups_nouns(self, array_sn, current_speaker, discriminator, builder):
        #TODO: We should start with resolved_sn filled with sentence.sn and replace
        # 'au fur et a mesure' to avoid re-resolve already resolved nominal groups
        resolved_sn = []
        for sn in array_sn:
            resolved_sn.append(self.resolve_nouns(sn, current_speaker, discriminator, builder))

        return resolved_sn
        
    def noun_phrases_resolution(self, sentence, current_speaker):
        
        builder = StatementBuilder(current_speaker)
        builder._sentence = sentence
        
        discriminator = Discrimination()

        if sentence.sn:
            sentence.sn = self.resolve_groups_nouns(sentence.sn, current_speaker, discriminator, builder)
        
        
        """
        process d_obj 
        """
        if sentence.sv.d_obj:
            """
            process d_obj : case: the yellow banana is good. yellow_banana hasFeature good. Where good is in the sentence.sv.d_obj[0].adj
            There is no noun in this  nominal group, so no resolve_groups_nouns here.
            """
            if sentence.sv.vrb_main == ["be"] and\
                     sentence.sv.d_obj[0].adj != [] and\
                     sentence.sv.d_obj[0].noun == [] and\
                     sentence.sv.d_obj[0].noun_cmpl == []:
                               
                sentence.sv.d_obj[0]._resolved = True
                #TODO: move the adjective to the subject instead of moving the subject as a "fake" direct obj.
                sentence.sv.d_obj[0].id = sentence.sn[0].id
                
            else:
                sentence.sv.d_obj = self.resolve_groups_nouns(
                                            sentence.sv.d_obj,
                                            current_speaker, 
                                            discriminator, 
                                            builder)
        
        
        resolved_i_cmpl = []
        for i_cmpl in sentence.sv.i_cmpl:
            i_cmpl.nominal_group = self.resolve_groups_nouns(i_cmpl.nominal_group, 
                                                            current_speaker, 
                                                            discriminator, 
                                                            builder)
            resolved_i_cmpl.append(i_cmpl)
        
        sentence.sv.i_cmpl = resolved_i_cmpl
            
        return sentence
    
    
    
    
    
    def resolve_verbs(self, verbal_group):
        
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
            verbal_group.sv_sec = self.resolve_verbs(verbal_group.sv_sec)
            
        return verbal_group
    
    def verbal_phrases_resolution(self, sentence):
        logging.debug("Resolving verbs...")
        sentence.sv = self.resolve_verbs(sentence.sv)
        
        return sentence

def unit_tests():
	"""This function tests the main features of the class Resolver"""
	print("This is a test...")

if __name__ == '__main__':
	unit_tests()

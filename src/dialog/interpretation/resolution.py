#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from dialog_exceptions import UnsufficientInputError, UnknownVerb
from resources_manager import ResourcePool

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
        logging.debug("References and anaphors resolution not yet implemented")
        return sentence
        
    def noun_phrases_resolution(self, sentence):
        logging.debug("Noun phrases resolution not yet implemented")
        #raise UnsufficientInputError("What apple are you talking of?")
        return sentence
    
    def resolve_verbs(self, verbs):
        resolved_verbs = []
        for verb in verbs:
            try:
                resolved_verb = ResourcePool().thematic_roles.get_ref(verb)
                if verb == resolved_verb:
                    logging.debug("Keeping \"" + verb + "\"")
                else:
                    logging.debug("Replacing \"" + verb + "\" by synonym \"" + 
                              resolved_verb + "\"")
            except UnknownVerb:
                resolved_verb = verb
                logging.debug("Unknown verb \"" + verb + "\": keeping it like that, but I won't do much with it.")
            
            resolved_verbs.append(resolved_verb)
        return resolved_verbs
    
    def verbal_phrases_resolution(self, sentence):
        sentence.sv.vrb_main = self.resolve_verbs(sentence.sv.vrb_main)
        return sentence

def unit_tests():
	"""This function tests the main features of the class Resolver"""
	print("This is a test...")

if __name__ == '__main__':
	unit_tests()

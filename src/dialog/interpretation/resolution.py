#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from dialog_exceptions import UnsufficientInputError

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
        raise UnsufficientInputError("What apple are you talking of?")
        return sentence
    
    def verbal_phrases_resolution(self, sentence):
        logging.debug("Verbal phrases resolution not yet implemented")
        return sentence

def unit_tests():
	"""This function tests the main features of the class Resolver"""
	print("This is a test...")

if __name__ == '__main__':
	unit_tests()

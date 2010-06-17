#!/usr/bin/python
# -*- coding: utf-8 -*-
"""The Verbalization module

This module is in charge of generating sentence in natural language from Python
Sentence objects.

It contains a single important class: Verbalizer.
"""
__author__ =  'Séverin Lemaignan'

import logging

from sentence import *

import reconstitution_replique

class Verbalizer:
    """Implements the verbalization module: Verbalizer.verbalize() takes as
    input a Sentence object and build from it a sentence in natural language.
    """
    def verbalize(self, sentence):
        logging.debug("Verbalizing now...")
        nl_sentence = reconstitution_replique.recon_replique(sentence)
        logging.debug("Rebuild sentence to: \"" + nl_sentence + "\"")
        return nl_sentence

def unit_tests():
    """This function tests the main features of the class Verbalizer"""
    
    verbalizer = Verbalizer()
    
    sentence1 = Sentence('w_question',
                        'place',
                        [Nominal_Group(['the'],  ['mother'],None,None, None)],
                        Verbal_Group(['be'], None,'present simple',None, None,['today'], None, None, None))

    print("TEST1: Should print: \"where is the mother today?\"")
    verbalizer.verbalize(sentence1)
    
    sentence2 = Sentence('statement', 
                        '', 
                        [Nominal_Group([],["Jido"],[],[],None), Nominal_Group([],["Danny"],[],[],None)], 
                        Verbal_Group(["want"],None, 'infinitive',[],[],[],[],'affirmative', None))
    
    
    sentence3 = Sentence('statement', 
                        '', 
                        [Nominal_Group([],["Holmes"],[],[],None), Nominal_Group([],["Sherlock"],[],[],None)], 
                        Verbal_Group(["want"],
                                    Verbal_Group(["eat"],None, 'infinitive',[],[],[],[],'affirmative', None), 
                                    'past simple',
                                    [],
                                    [],
                                    [],
                                    [],
                                    'negative', 
                                    None))
    
    sentence4 = Sentence('statement',
                        '',
                        [Nominal_Group( ['the'],  
                                        ['bottle'],
                                        ['blue', 'gray'],
                                        [Nominal_Group(['my'],  ['mother'],[],[], [sentence2]), Nominal_Group(['my'],  ['father'],[],[], None)], 
                                        None)], 
                        Verbal_Group(['know'], 
                                    None,
                                    'present simple',
                                    [Nominal_Group(['the'],  ["land"],['old'],[], None), Nominal_Group(['the'],  ["brand"],['lazy'],[], None)],
                                    [
                                        Indirect_Complement(['in'], 
                                                            [Nominal_Group(['the'],  ['garden'],['green'],[], None)]), 
                                        Indirect_Complement(['to'], 
                                                            [Nominal_Group(['the'],  ['car'],['red'],[], None)])
                                    ],
                                    ["slowly"], 
                                    ["now"], 
                                    "affirmative", 
                                    [sentence3]))

    print("TEST2: Should print: [smthg complicated]")
    verbalizer.verbalize(sentence4)


if __name__ == '__main__':
    unit_tests()

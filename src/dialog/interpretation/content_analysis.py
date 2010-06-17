#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from interpretation.statements_builder import StatementBuilder

"""This module implements ...

"""

class ContentAnalyser:
    def __init__(self):
        self.builder = StatementBuilder()
        
    def analyse(self, sentence, current_speaker):
        if sentence.data_type == 'imperative':
            logging.debug("Processing the content of an imperative sentence")
            return self.process_order(sentence, current_speaker)
            
    def process_order(self, sentence, current_speaker):
        flags = ['order', '', '', '', '', '', []]
        stmts = self.builder.processOrderSentence(
                            sentence, 
                            current_speaker, 
                            flags)
        logging.info("Generated statements: ")
        for s in stmts:
            logging.info(">> " + s)
        
        return stmts

def unit_tests():
    """This function tests the main features of the class ContentAnalysis"""
    print("This is a test...")

if __name__ == '__main__':
    unit_tests()

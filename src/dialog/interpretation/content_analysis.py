#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
from helpers import colored_print

from interpretation.statements_builder import StatementBuilder, StatementSafeAdder, QuestionHandler
from sentence import SentenceFactory

"""This module implements ...

"""

class ContentAnalyser:
    def __init__(self):
        self.builder = StatementBuilder()
        self.question_handler = QuestionHandler()
        self.sfactory = SentenceFactory()
        self.safeAdder = StatementSafeAdder()
        
    def analyse(self, sentence, current_speaker):
        """analyse an imperative or statement data_type sentence"""
        if sentence.data_type in ['imperative', 'statement']:
            logging.debug("Processing the content of " +  ("an imperative " if sentence.data_type == 'imperative' else "a statement ") + "data_type sentence")
            return self.process_sentence(sentence, current_speaker)
        """
        if sentence.data_type in ['w_question', 'yes_no_question']:
            logging.debug("Processing the content of " +  ("a w_question " if sentence.data_type == 'w_question' else "a yes_no_question ") + "data_type sentence")
            return self.process_question(sentence, current_speaker)
        """

            
    def process_sentence(self, sentence, current_speaker):
        self.builder.set_current_speaker(current_speaker)
        stmts = self.builder.process_sentence(sentence)
        
        logging.info("Generated statements: ")
        for s in stmts:
            logging.info(">> " + colored_print(s, None, 'magenta'))
        
        logging.info("Adding New statements in Ontology")
        self.safeAdder.safeAdd(stmts)
        
        return stmts
    """
    def process_question(self, sentence, current_speaker):
        self.question_handler.set_current_speaker(current_speaker)
        answer = self.question_handler.process_sentence(sentence)
        
        lgging.info("Found: \n \t>>" + answer)
        if sentence.data_type == 'w_question':
            return self.sfactory.create_w_question_answer(sentence, answer, self.qhandler.get_query_on_field())
        
        if sentence.data_type == 'yes_no_question':
            return self.sfactory.create_yes_no_answer(sentence, answer)
    """    

    

def unit_tests():
    """This function tests the main features of the class ContentAnalysis"""
    print("This is a test...")

if __name__ == '__main__':
    unit_tests()

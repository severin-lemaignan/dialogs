#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger("dialog")

from dialog.helpers import colored_print

from dialog.interpretation.statements_builder import StatementBuilder
from dialog.interpretation.statements_safe_adder  import StatementSafeAdder
from dialog.interpretation.questions_handler import QuestionHandler
from dialog.sentence import SentenceFactory
from dialog.resources_manager import ResourcePool
"""This module implements ...

"""

class ContentAnalyser:
    def __init__(self):
        self.builder = StatementBuilder()
        self.adder = StatementSafeAdder()
        self.question_handler = QuestionHandler()
        self.sfactory = SentenceFactory()
        
        self.output_sentence = []
        
    def analyse(self, sentence, current_speaker):
        """analyse an imperative or statement data_type sentence"""
        if sentence.data_type in ['imperative', 'statement']:
            logger.debug("Processing the content of " +  ("an imperative " if sentence.data_type == 'imperative' else "a statement ") + "data_type sentence")
            return self.process_sentence(sentence, current_speaker)
        
        if sentence.data_type in ['w_question', 'yes_no_question']:
            logger.debug("Processing the content of " +  ("a w_question " if sentence.data_type == 'w_question' else "a yes_no_question ") + "data_type sentence")
            return self.process_question(sentence, current_speaker)
        

            
    def process_sentence(self, sentence, current_speaker):
        self.builder.set_current_speaker(current_speaker)
        stmts = self.builder.process_sentence(sentence)
        
        logger.info("Generated statements: ")
        for s in stmts:
            logger.info(">> " + colored_print(s, None, 'magenta'))
        
        logger.info("Adding New statements in Ontology")
        
        self.adder._unclarified_ids = self.builder._unclarified_ids
        self.adder._statements = stmts
        self.adder._statements_to_remove = self.builder._statements_to_remove
        stmts = self.adder.process()
        
        # Class grounding
        if self.builder.lear_more_concept:
            self.output_sentence.extend(self.sfactory.create_what_is_a_reference(sentence, self.builder.lear_more_concept))
        
        return stmts
    
    def process_question(self, sentence, current_speaker):
        self.question_handler.set_current_speaker(current_speaker)
        answer = self.question_handler.process_sentence(sentence)
        
        logger.info("Found: \n \t>>" + str(answer))
        if sentence.data_type == 'w_question':
             self.output_sentence.extend(self.sfactory.create_w_question_answer(sentence, 
                                                                                    answer, 
                                                                                    self.question_handler.get_query_on_field()))
        
        if sentence.data_type == 'yes_no_question':
             self.output_sentence.extend(self.sfactory.create_yes_no_answer(sentence, answer))
        
        return self.question_handler._statements


    def analyse_output(self):
        return self.output_sentence

def unit_tests():
    """This function tests the main features of the class ContentAnalysis"""
    print("This is a test...")

if __name__ == '__main__':
    unit_tests()

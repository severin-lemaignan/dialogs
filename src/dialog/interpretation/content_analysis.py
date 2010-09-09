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
        """analyse sentences"""

        self.builder.clear_all()
        self.output_sentence = []
        
        sentence = self.pre_analyse_content(sentence)
        
        if sentence.data_type == 'interjection':
            pass
        
        if sentence.data_type in ["start", "end"]:
            self.output_sentence.append(sentence)
            
        if sentence.data_type == "gratulation":
            self.output_sentence.extend(self.sfactory.create_gratulation_reply())
        
        if sentence.data_type in ["agree", "disagree"]:
            self.output_sentence.extend(self.sfactory.create_agree_reply())
            
        if sentence.data_type in ['imperative', 'statement']:
            logger.debug(colored_print("Processing the content of " +  ("an imperative sentence" if sentence.data_type == 'imperative' else "a statement "), "magenta"))
            return self.process_sentence(sentence, current_speaker)
        
        if sentence.data_type in ['w_question', 'yes_no_question']:
            logger.debug(colored_print("Processing the content of " +  ("a W question " if sentence.data_type == 'w_question' else "a YES/NO question"), "magenta"))
            return self.process_question(sentence, current_speaker)
        
        
            
    def process_sentence(self, sentence, current_speaker):
        self.builder.set_current_speaker(current_speaker)

        stmts = self.builder.process_sentence(sentence)
        
        if stmts:
            logger.info("Generated statements: ")
            for s in stmts:
                logger.info(">> " + colored_print(s, None, 'magenta'))
            
            self.adder._unclarified_ids = self.builder._unclarified_ids
            self.adder._statements = stmts
            self.adder._statements_to_remove = self.builder._statements_to_remove
            stmts = self.adder.process()
            
            logger.debug("...added to the ontology")
        else:
            logger.info("No statements produced")
        
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
        
    def pre_analyse_content(self, sentence):
        """ this method analyse the content of a sentence ang give it another processing purpose.
            E.g: Can you give me the bottle?
            The sentence above is of 'yes_no_question' type but should actually be processed as an order in which the current speaker
            desires 'the bottle'. 
            Therefore, we turn it into 'give me the bottle'.
        """
        # Case of : 
        #   -INPUT:  Yes_no_question + can + action verb
        #   -OUTPUT: Imperative + action verb
        #   
        
        if sentence.data_type == 'yes_no_question':
            for sv in sentence.sv:
                for verb in sv.vrb_main:
                    if 'can+' in verb:
                        
                        vrb_main = verb.lstrip('can+')
                        
                        if not vrb_main in ResourcePool().state + ResourcePool().action_verb_with_passive_behaviour.keys() + ResourcePool().goal_verbs:
                            
                            logger.debug(colored_print("Interpreting the <can + action verb> sequence as a desire.\nApplying transformation:", "magenta"))
                        
                            sv.vrb_main[sv.vrb_main.index(verb)] = verb.lstrip('can+')
                            sentence.data_type = 'imperative'
                            
                            logger.debug(str(sentence))
                            
                            return sentence
                    
            
            
        return sentence

def unit_tests():
    """This function tests the main features of the class ContentAnalysis"""
    print("This is a test...")

if __name__ == '__main__':
    unit_tests()

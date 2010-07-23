#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import getopt
import logging
from threading import Thread
from Queue import Queue, Empty
from collections import deque

from helpers import colored_print

from dialog_exceptions import UnsufficientInputError

from sentence import Sentence
import sentence

from speaker_identification import SpeakerIdentifier
from parsing.parser import Parser
from interpretation.resolution import Resolver
from interpretation.content_analysis import ContentAnalyser
from verbalization.verbalization import Verbalizer

VERSION = "0.1"

class Dialog(Thread):
    def __init__(self):
        Thread.__init__(self)
        
        self.go_on = True
        self._logger = logging.getLogger('dialog')
        
        self._speaker = SpeakerIdentifier()
        self._parser = Parser()
        self._resolver = Resolver()
        self._content_analyser = ContentAnalyser()
        self._verbalizer = Verbalizer()
        
        self._nl_input_queue = Queue()
        self._sentence_output_queue = Queue()
        
        #true when the Dialog module is within an interaction with a speaker
        self.in_interaction = False
        
        #the current set of sentences that dialog is dealing with
        self.sentences = deque()
        
        #the current sentence being worked on. Specifically, if active_sentence
        #is set, the parser will _complete_ this sentence instead of creating a
        #new one.
        self.active_sentence = None
        
        #true when, during an interaction, more infos is needed.
        self.waiting_for_more_info = False
        
        #contains the last result of a failed resolution (including the object 
        #that could not be resolved. Cf doc of UnsufficientInputError for details.
        self._last_output = None
        
        #the object currently discussed. Used to resolve anaphors (like 'this 
        # one').
        self.current_object = None
        
        #the ID of the speaker we are talking with. used to resolve references
        #like 'me', 'you', etc.
        self.current_speaker = None
        
        #the set of the statements generated by the analysis of the last sentence.
        self.last_stmts_set = []
    
    def run(self):
        while self.go_on:
                  
            try:               
                input = self._nl_input_queue.get(block = False).strip()
                self._logger.info(colored_print("###################################", 'green'))
                self._logger.info(colored_print("#             NL INPUT            #", 'green'))
                self._logger.info(colored_print("###################################\n", 'green'))
                self._logger.info(colored_print(input + "\n", 'blue'))
                self.in_interaction = True
                self.waiting_for_more_info = False
                
                try:
                    self._process(input)
                except UnsufficientInputError as uie:
                    self._logger.info(colored_print("##########################################", 'green'))
                    self._logger.info(colored_print("#  Missing content! Going back to human  #", 'green'))
                    self._logger.info(colored_print("##########################################", 'green'))
                    self._sentence_output_queue.put(uie.value['question'])
                    
                    self._last_output = uie.value

            except Empty:
                pass
            
            try:
                output = self._sentence_output_queue.get(block = False)

                self._logger.debug(colored_print("> Got output to verbalize: ", 'bold'))
                
                #TODO: Assuming here that the user is queried for info. Not true in the general case
                self.waiting_for_more_info = True

                sys.stdout.write(colored_print( \
                            self._verbalizer.verbalize(output), \
                            'red') + "\n")
                  
            except Empty:
                pass
            
            
    def stop(self):
        while(not self._nl_input_queue.empty()):
            pass
        self.go_on = False

    def input(self, input, speaker = None):
        if speaker:
            self.current_speaker = speaker
        else:
            self.current_speaker = self._speaker.get_current_speaker_id()
        
        #Here, we proceed a sentence that has not been resolved. It is saved in self.active_sentence.
        #The new input string is concatenated with the former one.
        #
        if self.waiting_for_more_info:
            #We process the input
            input=self._parser.parse(input, None)
            
            #We make the merge in the nominal group
            input = sentence.nom_gr_remerge(input._class_list, self._last_output['status'],self._last_output['object'])           
            
            input = ' '.join(input)    
        
        self._nl_input_queue.put(input)
        
    def test(self, speaker, input, answer = None):
        """This method eases the testing of dialog by returning only when a 
        sentence is completely processed.
        The optional 'answer' argument is used to answer a request for more 
        details from the resolution code.
        """
        self.in_interaction = True
        self.input(input, speaker)
        while(self.in_interaction):
            if answer and self.waiting_for_more_info:
                logging.debug(colored_print("> Automatically answering: ", 'bold'))
                logging.debug(colored_print(answer, 'red'))
                self.input(answer, speaker)
                answer = None
            elif self.waiting_for_more_info:
                return None
            pass
        
        return self.last_stmts_set

    def _process(self, nl_input):
        #Parsing
        self._logger.info(colored_print("###################################", 'green'))
        self._logger.info(colored_print("#             PARSING             #", 'green'))
        self._logger.info(colored_print("###################################", 'green'))
        self.sentences.appendleft(self._parser.parse(nl_input, self.active_sentence)[0])
        
        for s in range(len(self.sentences)): #sentences is a deque. Cannot do a simple [:] to iterate over a copy
            self.active_sentence = self.sentences.popleft()
            
            #Resolution
            self._logger.info(colored_print("###################################", 'green'))
            self._logger.info(colored_print("#       RESOLVING SENTENCE        #", 'green'))
            self._logger.info(colored_print("###################################", 'green'))

            self.active_sentence = self._resolver.references_resolution(self.active_sentence,
                                                                        self.current_speaker, 
                                                                        self.current_object)
            self.active_sentence = self._resolver.noun_phrases_resolution(self.active_sentence,
                                                                          self.current_speaker)
            self.active_sentence = self._resolver.verbal_phrases_resolution(self.active_sentence)
            
            self._logger.debug(colored_print("###################################", 'green'))
            self._logger.debug("Sentence after resolution:\n" + str(self.active_sentence))
            
            #Content analysis
            self._logger.info(colored_print("###################################", 'green'))
            self._logger.info(colored_print("#        CONTENT ANALYSIS         #", 'green'))
            self._logger.info(colored_print("###################################", 'green'))
            self.last_stmts_set = self._content_analyser.analyse(self.active_sentence, self.current_speaker)
            
        #Finalizing the processing
        self._logger.info(colored_print("\n###################################\n", 'green'))
        self.active_sentence = None
        self._logger.info(colored_print("NL sentence \"" + nl_input + "\" processed!", 'green'))
        self.in_interaction = False


def usage():
    print """The LAAS-CNRS dialog module.

Usage:
dialog.py [OPTIONS]
  -h, --help			Displays this message and exits
  -t, --test			Runs unit-tests
  -d, --debug			Sets verbosity to debug
  -s, --silent			The module won't output anything

This module reads on stdin user input in natural language, parse it, call 
resolution routines when ambiguous concepts are used, and finally generate RDF 
statements that are an interpretation of the input.

It includes as well a verbalization module that conversely turns RDF statements
into a sentence in natural language.

dialog fits into the so-called CHRIS architecture @ LAAS. More details on the 
LAAS internal Wiki:
https://intranet.laas.fr/intranet/robots/wiki/ChrisArchitecture
"""

def unit_tests():
    print("Please run the dialog_test.py Python script.")
    print()
    print("> ./dialog_test.py")

def main():

    debug_level = logging.INFO
    
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'htds', ['help', 'test', 'debug', 'silent'])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)

    for o, a in optlist:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-t", "--test"):
            unit_tests()
            sys.exit(0)
        elif o in ("-d", "--debug"):
            debug_level = logging.DEBUG
        elif o in ("-s", "--silent"):
            debug_level = logging.CRITICAL
        else:
            print "Unhandled option " + o
            usage()
            sys.exit(2)

    logging.basicConfig(level=debug_level, format="%(message)s")
    logging.info("**** DIALOG module ****")
    logging.info("v." + VERSION + "\n")

    dialog = Dialog()

    dialog.start()

    running = True
    while running:
        try:
            data = sys.stdin.readline()
            dialog.input(data)
            
        except KeyboardInterrupt:
            logging.info("Leaving now.")
            running = False
            dialog.stop()

    dialog.join()
    sys.exit()

if __name__ == '__main__':
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import getopt
import logging
from threading import Thread
from Queue import Queue, Empty

from dialog_exceptions import UnsufficientInputError

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
		self.sentences = []
		
		#the current sentence being worked on. Specifically, if active_sentence
		#is set, the parser will _complete_ this sentence instead of creating a
		#new one.
		self.active_sentence = None
		
		#the object currently discussed. Used to resolve anaphors (like 'this 
		# one').
		self.current_object = None
		
		#the ID of the speaker we are talking with. used to resolve references
		#like 'me', 'you', etc.
		self.current_speaker = None
	
	def run(self):
		while self.go_on:
			
			try:
				input = self._nl_input_queue.get(block = False)
				self._logger.debug("Got NL input \"" + input + "\"")
			
				try:
					self._process(input)
				except UnsufficientInputError as uie:
					self._sentence_output_queue.put(uie.value)
			except Empty:
				pass
			
			try:
				output = self._sentence_output_queue.get(block = False)
				self._logger.debug("Got output to verbalize")
				self._verbalizer.verbalize(output)
			except Empty:
				pass
			

	
	def input(self, input):
		self.current_speaker = self._speaker.get_current_speaker_id()
		self._nl_input_queue.put(input)
	
	def _process(self, nl_input):
		self._logger.debug("Processing NL sentence \"" + nl_input + "\"")
		
		#Parsing
		self.sentences = self._parser.parse(nl_input)
		self.active_sentence = self.sentences[0]
		
		#Resolution
		self.active_sentence = self._resolver.references_resolution(self.active_sentence,
																	self.current_speaker, 
																	self.current_object)
		self.active_sentence = self._resolver.noun_phrases_resolution(self.active_sentence)
		self.active_sentence = self._resolver.verbal_phrases_resolution(self.active_sentence)
		
		
		return self.active_sentence


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
	
	logging.basicConfig(level=logging.INFO,
						format="%(message)s")

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
			logging.basicConfig(level=logging.DEBUG)
		elif o in ("-s", "--silent"):
			logging.basicConfig(level=logging.CRITICAL)
		else:
			print "Unhandled option " + o
			usage()
			sys.exit(2)

	logging.info("**** DIALOG module ****")
	logging.info("v." + VERSION + "\n")
	
	dialog = Dialog()
	
	dialog.start()
	
	try:
		while True:
			pass
	except KeyboardInterrupt:
		logging.info("Leaving now.")
		dialog.go_on = False
	
	dialog.join()
	sys.exit()

if __name__ == '__main__':
	main()

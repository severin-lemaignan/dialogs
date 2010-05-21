#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import getopt
import logging
from threading import Thread

from speaker_identification import SpeakerIdentifier
from parsing.parser import Parser
from interpretation.content_analysis import ContentAnalyser
from verbalization.verbalization import Verbalizer

VERSION = "0.1"

class Dialog(Thread):
	def __init__(self):
		Thread.__init__(self)
		
		self._logger = logging.getLogger('dialog')
		
		self._speaker = SpeakerIdentifier()
		self._parser = Parser()
		self._content_analyser = ContentAnalyser()
		self._verbalizer = Verbalizer()
		
		self.sentences = []
		self.active_sentences = None
		
		self.current_object = None
		self.current_speaker = None
	
	def run(self):
		while True:
			pass

	
	def handle_incoming_input(self, input):
		self.current_speaker = self._speaker.get_current_speaker_id()
		self._process(input)
	
	def _process(self, nl_input):
		self._logger.debug("Processing NL sentence \"" + nl_input + "\"")
		
		sentence = self._parser.parse(nl_input)
		
		return sentence


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
		dialog.join()
	except KeyboardInterrupt:
		logging.info("Leaving now.")
		dialog.exit()
	
	sys.exit()

if __name__ == '__main__':
	main()

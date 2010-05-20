#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import getopt
from threading import Thread

from parsing.parser import Parser
from interpretation.content_analysis import ContentAnalyser
from verbalization.verbalization import Verbalizer

class Dialog(Thread):
	def __init__(self):
		Thread.__init__(self)
		
		self._parser = Parser()
		self._content_analyser = ContentAnalyser()
		self._verbalizer = Verbalizer()
	
	def run(self):
		while True:
			pass

	
	def process(self, nl_input):
		print nl_input


def usage():
	print """The LAAS-CNRS dialog module.

Usage:
dialog.py [OPTIONS]
  -h, --help			Displays this message and exits
  -t, --test			Runs unit-tests

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
	try:
		optlist, args = getopt.getopt(sys.argv[1:], 'ht', ['help', 'test'])
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
		else:
			print "Unhandled option " + o
			usage()
			sys.exit(2)

	print("Welcome in the dialog module!\nPress Ctrl+C to exit")
	dialog = Dialog()
	
	dialog.start()
	
	try:
		dialog.join()
	except KeyboardInterrupt:
		print "Leaving now."
		dialog.exit()
	
	sys.exit()

if __name__ == '__main__':
	main()

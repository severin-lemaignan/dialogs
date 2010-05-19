#!/usr/bin/python
import sys
import os
import getopt

class dialog:
	pass

def usage():
	print """The LAAS-CNRS dialog module.

Usage:
dialog.py [OPTIONS]
  -h, --help			Displays this message and exits

This module reads on stdin user input in natural language, parse it, call 
resolution routines when ambiguous concepts are used, and finally generate RDF 
statements that are an interpretation of the input.

It includes as well a verbalization module that conversely turns RDF statements
into a sentence in natural language.

dialog fits into the so-called CHRIS architecture @ LAAS. More details on the 
LAAS internal Wiki:
https://intranet.laas.fr/intranet/robots/wiki/ChrisArchitecture
"""

if __name__ == '__main__':

	try:
		optlist, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
	except getopt.GetoptError, err:
		# print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		usage()
		sys.exit(2)

	for o, a in optlist:
		if o in ("-h", "--help"):
			usage()
			sys.exit(0)
		else:
			print "Unhandled option " + o
			usage()
			sys.exit(2)

	print("Welcome in the dialog module!\nPress Ctrl+C to exit")
	
	try:
		while True:
			pass
	
	except KeyboardInterrupt:
		print "Leaving now."
		sys.exit()

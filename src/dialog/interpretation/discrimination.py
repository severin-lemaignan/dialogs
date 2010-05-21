#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module implements the clarification process for ambiguous descriptions. 
Given a description of an object (ambigouos or not) it returns, if found, the 
object's identifier in oro. If necessary, it will query the human for additional
information.
"""

import logging

from pyoro import Oro
from dialog_exceptions import UnsufficientInputError

#LOG_FILENAME = 'logging_example.out'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG) # to print output in screen

HOST = 'localhost'    # The remote host
PORT = 6969           # The same port as used by the server

 
class Discrimination():
	
	def __init__(self):
		try:
			self.oro = Oro(HOST, PORT)
		except OroServerError as ose:
			print('Oups! An error occured!')
			logging.debug(ose)
		
	# -- GET_ALL_OBJECTS_WITH_DESC ------------------------------------------------#
    # Returns all objects' ids with a given set of features (eg. green, big, etc).
    # Since we have several descriptions, we obtain a list of objects for each agent
    # and then we intersect them.
    #
    # INPUT:
    # - description: 
    #   [[agent1 '?obj' oro_query]..[[agentN '?obj' oro_query]]
    #   (oro_query= "?obj hasColor blue, ?obj hasShape box")
    # 
    # OUTPUT:
    # - empty list: no objects found fulfilling the description
    # - list: objects fulfilling the description
    # - -1: no description (or description format incorrect)
    # -----------------------------------------------------------------------------#
	def get_all_objects_with_desc(self, description):
		
		objL = -1
		
		for agent_desc in description:
			if agent_desc[0] == 'myself':
				obj_tmp = self.oro.find(agent_desc[1], '[' + agent_desc[2] + ']')
			else:
				obj_tmp = self.oro.findForAgent(agent_desc[0], agent_desc[1], '[' + agent_desc[2] + ']')
		
			# if no object found, no need to continue
			if not obj_tmp: 
				objL = []
				break
			else:
				if objL == -1:
					objL = obj_tmp
				else:
					objL = filter(lambda x:x in objL,obj_tmp)  # intersection
					
		return objL
	
	
	# -- GET_DISCRIMINANT ---------------------------------------------------------#
    # Queries the ontology for a list of discriminants. Returns the first one.
    # TODO: prioritize which discriminant to return.
    #
    # INPUT:
    # - agent
    # - object list
    # - zPartial: if 1, then partial discriminants are also returned
    # OUTPUT:
    # - discriminant: [C, discriminat] if complete, or [P, discriminant] if partial
    # -----------------------------------------------------------------------------#
	def get_discriminant(self, agent, objL, zPartial):
		if agent == "myself":
			discriminants = self.oro.discriminate(objL)
		else:
			discriminants = self.oro.discriminateForAgent(objL)
				
		logging.debug('discriminants = ' + str(discriminants))
		complete_disc = discriminants[0]
		partial_disc = discriminants[1]
		
		if complete_disc:
			return complete_disc[0]
		elif partial_disc and zPartial:
			return partial_disc[0]
		else:
			return None
	
	# -- GET_DESCRIPTOR -----------------------------------------------------------#
    # Searches for a new descriptor candidate from all agents.
    #
    # INPUT:
    # - description ([[robot isVisible true hasColor blue]...\ 
    #   [agent isVisible true hasColor blue])
    # - allowPartialDesc: consider also partial discriminants (1) or not (0) (0 default)
    #
    # OUTPUT:
    # - descriptor or None (if no discriminant for any agent found)
    # -----------------------------------------------------------------------------#
	def get_descriptor(self, description, partial_disc=0):
		objL = self.get_all_objects_with_desc(description)
		descriptor = None
		agent = None

		# bug in oro doesn't allow to search discriminants base on other agents models!!
		# we cannot search in all agents, but only in robot's model
#		for agent_desc in description:
#			descriptor = self.get_discriminant(agent_desc[0], objL, partial_disc)
			
#			if descriptor:
#				agent = agent_desc[0]
#				break

		agent = "myself"
		descriptor = self.get_discriminant(description[0][0], objL, partial_disc)
				
		return agent, descriptor
		
		
	# -- get_values_for_descriptor ------------------------------------------------#
	# Creates the information to be sent to user based on the discriminant found.
	#
	# INPUT: 
	# - agent, discriminant, objectsList
	#
	# OUTPUT
	# - list of values to ask for
	# -----------------------------------------------------------------------------#
	def get_values_for_descriptor(self, agent, descriptor, objL):
		valL = []
	
		# get values for each object
		for obj in objL:
			if agent == "myself":
				val = self.oro.find('?val','[' + obj + ' ' + descriptor + ' ?val]')
			else:
				val = self.oro.findForAgent(agent, '?val','[' + obj + ' ' + descriptor + ' ?val]')
				
			valL.append(val[0])

		return list(set(valL))
	
	
	# -- CLARIFY ------------------------------------------------------------------#
	# Searches for a new descriptor candidate. The descriptor should be as 
	# discriminating as possible.
	#
	# INPUT:
	# - description ([[robot isVisible true hasColor blue]...\ 
	#   [agent isVisible true hasColor blue])
	#
	# OUTPUT:
	# - True, objectID: ok
	# - False, "new info": no match, new info required (forget previous description)
	# - False, "descriptor value": user should indicate value for descriptor
	# - False, "add info": user should give additional info (mantain previous description)
	# -----------------------------------------------------------------------------#
	def clarify(self, description):
		objL = self.get_all_objects_with_desc(description)
		logging.debug('Clarify for objL = ' +  str(objL))
		
		if len(objL) == 0:
			raise UnsufficientInputError("New info required")
			#return "New info required"
		elif len(objL) == 1:
			return objL[0]
		else:
			agent, descriptor = self.get_descriptor(description)
		
			if descriptor:
				raise UnsufficientInputError([descriptor, self.get_values_for_descriptor(agent, descriptor, objL)])
				#return [descriptor, self.get_values_for_descriptor(agent, descriptor, objL)]
			else:
				raise("Additional info required")
				#return "Additional info required"

		
def unit_tests():
 	"""This function tests the main features of the class Discrimination"""
	
	disc = Discrimination()

	print "Test1: No ambiguity."	
	description = [['myself', '?obj', '?obj rdf:type Bottle, ?obj hasColor blue']]
	expected_result = [True, 'BLUE_BOTTLE']
	res = disc.clarify(description)
	print '\t expected res = ', expected_result
	print '\t obtained res = ', res
	print '\n*********************************'
    
	print "\nTest2: Complete discriminant in robot model found."
	description = [['myself', '?obj', '?obj rdf:type Bottle']]
	expected_result = [False, ['mainColorOfObject', ['blue', 'orange', 'yellow']]]
	res = disc.clarify(description)
	print '\t expected res = ', expected_result
	print '\t obtained res = ', res
	print "\n*********************************"
    
	print "\nTest3: No complete discriminant in robot model found."
	description = [['myself', '?obj', '?obj rdf:type Box']]
	expected_result = [False, "Additional info"]
	res = disc.clarify(description)
	print '\t expected res = ', expected_result
	print '\t obtained res = ', res
	print "\n*********************************"
    
	print "\nTest4: Including visibility constraints"
	description = [['myself', '?obj', '?obj rdf:type Bottle']]
	description.append(['raquel', '?obj', '?obj isVisible true'])
	expected_result = [False, ['mainColorOfObject', ['blue', 'orange']]]
	res = disc.clarify(description)
	print '\t expected res = ', expected_result
	print '\t obtained res = ', res
	print "\n*********************************"
    

if __name__ == '__main__':
	unit_tests()

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module implements the clarification process for ambiguous descriptions. 
Given a description of an object (ambigouos or not) it returns, if found, the 
object's identifier in oro. If necessary, it will query the human for additional
information.
"""

import logging

from pyoro import Oro
from pyoro import OroServerError
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
    #   (oro_query= ['?obj hasColor blue',.. ?obj hasShape box'])
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
                obj_tmp = self.oro.find(agent_desc[1], '[' + ', '.join(agent_desc[2]) + ']')
            else:
                obj_tmp = self.oro.findForAgent(agent_desc[0], agent_desc[1], '[' + ', '.join(agent_desc[2]) + ']')

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
    # - currentDesc: list of already used descriptors
    # - zPartial: if 1, then partial discriminants are also returned
    # OUTPUT:
    # - discriminant: [C, discriminat] if complete, or [P, discriminant] if partial
    #   The new discriminant should be different from the ones already known
    # -----------------------------------------------------------------------------#
    def get_discriminant(self, agent, objL, currentDesc, zPartial):
        if agent == "myself":
            discriminants = self.oro.discriminate(objL)
        else:
            discriminants = self.oro.discriminateForAgent(agent, objL)
        
        logging.debug('discriminants = ' + str(discriminants))
        complete_disc = discriminants[0] 
        partial_disc = discriminants[1]

        if complete_disc:
            res =  filter(lambda x: x not in currentDesc, complete_disc)
        elif partial_disc and zPartial:
            res = filter(lambda x: x not in currentDesc, partial_disc)
        else:
            res = None
            
        if res:
            return res[0]
        else:
            return None

    # -- GET_DESCRIPTOR -----------------------------------------------------------#
    # Searches for a new descriptor candidate from all agents.
    #
    # INPUT:
    # - description: 
    #   [[agent1 '?obj' oro_query]..[[agentN '?obj' oro_query]]
    #   (oro_query= ['?obj hasColor blue',.. ?obj hasShape box'])
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
#        for agent_desc in description:
#            currentDescriptors = map(lambda x: x.split()[1], agent_desc[2])
#            descriptor = self.get_discriminant(agent_desc[0], objL, currentDescriptors, partial_disc)
#
#            if descriptor:
#                agent = agent_desc[0]
#                break

        agent = "myself"
        currentDescriptors = map(lambda x: x.split()[1], description[0][2])
        descriptor = self.get_discriminant(description[0][0], objL, currentDescriptors, partial_disc)

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
            # if the discriminant is type, then look for the directClass of the obj (first found)
            # how should this work for different agents? There is no directClassForAgent
            # probably won't be necessary since all the knowledge of the human is part
            # of the robot's knowledge as well. Then we can obtain this information 
            # directly from the robot itself.
            if descriptor == 'rdf:type':
                val = self.oro.getDirectClassesOf(obj).keys()
            else:
                if agent == "myself":
                    val = self.oro.find('?val','[' + obj + ' ' + descriptor + ' ?val]')
                else:
                    val = self.oro.findForAgent(agent, '?val','[' + obj + ' ' + descriptor + ' ?val]')

            valL.append(val[0])

        # we make a set to remove repeated elements
        return list(set(valL))

    # -- get_type_description ------------------------------------------------------#
    # Returns the first type of concept in the description.
    #
    # INPUT:
    # - description
    #
    # OUTPUT:
    # - type
    # - none
    # -------------------------------------------------------------------------------#
    def get_type_description(self, description):

        def find(value, seq):
            for item in seq:
                itemL = item.split()
                if value in itemL: 
                    return itemL[2]
            return None

        type = None
        
        for desc in description:
            type = find('rdf:type', desc[2])
            if type: break
            
        return type
    
    # -- CLARIFY ------------------------------------------------------------------#
    # Searches for a new descriptor candidate. The descriptor should be as 
    # discriminating as possible.
    #
    # INPUT:
    # - description [['myself', '?obj', ['?obj rdf:type Bottle', '?obj hasColor blue']],
    #                ['agent1', '?obj', ['?obj isVisible True']]
    #
    # OUTPUT:
    # - objectID: ok
    # - UnsufficientInputError:
    #   - "new info required": no match, new info required (forget previous description)
    #   - "Which value? ..." user should indicate value for descriptor
    #   - "additional info required": user should give additional info (mantain previous description)
    # -----------------------------------------------------------------------------#
    def clarify(self, description):
        objL = self.get_all_objects_with_desc(description)
        logging.debug('Clarify recieves description = ' +  str(description))
        logging.debug('Clarify for objL = ' +  str(objL))

        if len(objL) == 0:
            raise UnsufficientInputError("I don't know what object you are talkikng about. Tell me something about it.")
            #return "I don\'t know what object you are talkikng about. Tell me something about it."
        elif len(objL) == 1:
            return objL[0]
        else:
            agent, descriptor = self.get_descriptor(description)
            object = self.get_type_description(description)

            if descriptor:
                question = None
                values = self.get_values_for_descriptor(agent, descriptor, objL)
                if not object: object = 'object'
                
                if descriptor == 'hasColor'  or  descriptor == 'mainColorOfObject':
                    question = 'Which color is the ' + object + ' ? '
                    
                elif descriptor == 'hasShape':
                    question = 'Which shape has the ' + object + ' ? '

                elif descriptor == 'hasSize':
                    question = 'Which size is the ' + object + ' ? '

                elif descriptor == 'isOn':
                    question = 'Is the ' + object + ' on '

                elif descriptor == 'isIn':
                    question = 'Is the ' + object + ' in '
                    
                elif descriptor == 'isNexto':
                    question = 'Is the ' + object + ' next to '

                elif descriptor == 'isAt':
                    question = 'Is the ' + object + ' at '

                elif descriptor == 'isLocated'  or  descriptor == 'isAt':
                    question = 'Where is the ' + object + ' placed wrt to'
                                        
                    if agent == 'myself':
                        question += ' me ? '
                    else:
                        question += ' you ? '
                
                else:
                    question = "Give me the value for the " + descriptor + " "

                question += ' or '.join(values) + ' ?'
                raise UnsufficientInputError(question)
                #return question
                    
            else:
                question = "Tell me something about the " + object
                raise UnsufficientInputError(question)
                #return "Tell me more about the the object."

    # -- ADD_DESCRIPTOR -----------------------------------------------------------#
    # Includes descriptor in description list.
    #
    # INPUT:
    # - agent: to which agent the descriptor belongs to
    # - description: current description
    # - descriptor: feature
    # - value: feature value
    #
    # OUTPUT:
    # - new description
    # -----------------------------------------------------------------------------#
    def add_descriptor(self, agent, description, descriptor, value):
        
        # return sublist index in seq containing value
        def find(value, seq):
            for index, item in enumerate(seq):
                if value in item: 
                    return index, item
                    
        idx, desc = find(agent, description)
        desc[2].append('?obj ' + descriptor + ' ' + value)
        description[idx] = desc
        
        return description
        
    # -- FIND_UNAMBIGUOUS_DESC -----------------------------------------------------#
    # Searches an unambiguous description for a given object. If not found, returns
    # the id of the object and the most complete description found.
    #
    # INPUT:
    # - objectID: object to be described
    #
    # OUTPUT:
    # - description: ok
    # - [objectID, description]: failed
    # -----------------------------------------------------------------------------#
    def find_unambiguous_desc(self, objectID):
        description = None
        # get the first class name
        type = self.oro.getDirectClassesOf(objectID).keys()[0] 
        description = [['myself','?obj',['?obj rdf:type ' + type]]]        
        objL = self.get_all_objects_with_desc(description)
         
        while len(objL) > 1:
            logging.debug('Description ' + objectID +': ' + str(description))
            logging.debug('ObjL: ' + str(objL))

            agent, descriptor = self.get_descriptor(description,1)
            
            if agent == "myself":
                val = self.oro.find('?val','[' + objectID + ' ' + descriptor + ' ?val]')
            else:
                val = self.oro.findForAgent(agent, '?val','[' + objectID + ' ' + descriptor + ' ?val]')            
            
            if not val: 
                description.insert(0,objectID)
                break
                
            description = self.add_descriptor(agent, description, descriptor, val[0])            
            objL = self.get_all_objects_with_desc(description)

        return description
    
def unit_tests():
    """This function tests the main features of the class Discrimination"""

    disc = Discrimination()

    print "Test1: No ambiguity."
    description = [['myself', '?obj', ['?obj rdf:type Bottle', '?obj hasColor blue']]]
    expected_result = "BLUE_BOTTLE"
    res = disc.clarify(description)
    print '\t expected res = ', expected_result
    print '\t obtained res = ', res
    print '\n*********************************'
    
    print "\nTest2: Complete discriminant in robot model found."
    description = [['myself', '?obj', ['?obj rdf:type Bottle']]]
    expected_result = "Which color is the object? blue or orange or yellow?"
    res = disc.clarify(description)
    print '\t expected res = ', expected_result
    print '\t obtained res = ', res
    print "\n*********************************"
    
    print "\nTest3: No complete discriminant in robot model found."
    description = [['myself', '?obj', ['?obj rdf:type Box']]]
    expected_result = "Tell me more about the the object."
    res = disc.clarify(description)
    print '\t expected res = ', expected_result
    print '\t obtained res = ', res
    print "\n*********************************"
    
    print "\nTest4: Including visibility constraints"
    description = [['myself', '?obj', ['?obj rdf:type Bottle']]]
    description.append(['raquel', '?obj', ['?obj isVisible true']])
    expected_result = "Which color is the object? blue or orange?"
    res = disc.clarify(description)
    print '\t expected res = ', expected_result
    print '\t obtained res = ', res
    print "\n*********************************"
    
    print "\nTest5: Testing location"
    description = [['myself', '?obj', ['?obj rdf:type Box', '?obj hasColor orange']]]
    expected_result = "Is the object on ACCESSKIT or HRP2TABLE?"
    res = disc.clarify(description)
    print '\t expected res = ', expected_result
    print '\t obtained res = ', res
    print "\n*********************************"
    
    print "\nTest6: Generate unambiguous description"
    objectID = 'BLUE_BOTTLE'
    expected_result = [['myself', '?obj', ['?obj rdf:type Bottle', '?obj mainColorOfObject blue']]]
    res = disc.find_unambiguous_desc(objectID)
    print '\t expected res = ', expected_result
    print '\t obtained res = ', res
    print "\n*********************************"

    print "\nTest7: Generate unambiguous description"
    objectID = 'ACCESSKIT'
    expected_result = [['myself', '?obj', ['?obj rdf:type Box', '?obj mainColorOfObject white', '?obj isUnder ORANGEBOX']]]
    res = disc.find_unambiguous_desc(objectID)
    print '\t expected res = ', expected_result
    print '\t obtained res = ', res
    print "\n*********************************"

    print "\nTest8: Generate unambiguous description"
    objectID = 'SPACENAVBOX'
    expected_result = ['SPACENAVBOX', ['myself', '?obj', ['?obj rdf:type Box', '?obj mainColorOfObject white']]]
    res = disc.find_unambiguous_desc(objectID)
    print '\t expected res = ', expected_result
    print '\t obtained res = ', res
    print "\n*********************************"


if __name__ == '__main__':
    unit_tests()

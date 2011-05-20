# -*- coding: utf-8 -*-

"""This module implements the clarification process for ambiguous descriptions. 
Given a description of an object (ambigouos or not) it returns, if found, the 
object's identifier in oro. If necessary, it will query the human for additional
information.
"""

import logging
logger = logging.getLogger("dialog")

from pyoro import OroServerError

from dialogs.resources_manager import ResourcePool
from dialogs.dialog_exceptions import UnsufficientInputError
from dialogs.sentence import *
from dialogs.sentence_factory import SentenceFactory

from random import choice

 
class Discrimination():

    def __init__(self):
        self.oro = ResourcePool().ontology_server

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
            
            obj_tmp = []

            try:
                obj_tmp = self.oro.findForAgent(agent_desc[0], agent_desc[1], '[' + ', '.join(agent_desc[2]) + ']')
            except AttributeError: # No ontology server
                pass
            except OroServerError: #The agent does not exist in the ontology
                pass

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
    # - ignoreDesc: list of descriptors not to be used
    # - zPartial: if 1, then partial discriminants are also returned
    # OUTPUT:
    # - discriminant: [C, discriminat] if complete, or [P, discriminant] if partial
    #   The new discriminant should be different from the ones already known or ignored
    # -----------------------------------------------------------------------------#
    def get_discriminant(self, agent, objL, ignoreDesc, zPartial):
        discriminants = self.oro.discriminateForAgent(agent, objL)
        logger.debug(  colored_print('Possible discriminants: ', 'magenta') +  \
                        str(colored_print(discriminants[1], 'blue')) + \
                        colored_print(" (complete discriminants: ", 'magenta') + \
                        str(colored_print(discriminants[0], 'blue')) + ")")
                        
        complete_disc = discriminants[0] 
        partial_disc = discriminants[1]

        if complete_disc:
            res =  filter(lambda x: x not in ignoreDesc, complete_disc)
        elif partial_disc and zPartial:
            res = filter(lambda x: x not in ignoreDesc, partial_disc)
        else:
            res = None
            
        if res:
            # include randomization so the same discriminant is not always returned
            return choice(res)
        else:
            return None

    # -- GET_DESCRIPTOR -----------------------------------------------------------#
    # Searches for a new descriptor candidate from all agents.
    #
    # INPUT:
    # - description: 
    #   [[agent1 '?obj' oro_query]..[[agentN '?obj' oro_query]]
    #   (oro_query= ['?obj hasColor blue',.. ?obj hasShape box'])
    # - ignoreFeatureL: list of features not to use as discriminants
    #   [feat1 ..featN]
    # - allowPartialDesc: consider also partial discriminants (1) or not (0) (0 default)
    #
    # OUTPUT:
    # - descriptor or None (if no discriminant for any agent found)
    # -----------------------------------------------------------------------------#
    def get_descriptor(self, description, ignoreFeatureL = [], partial_disc=True):
        
        objL = self.get_all_objects_with_desc(description)
        descriptor = None
        agent = None

        # bug in oro doesn't allow to search discriminants base on other agents models!!
        # we cannot search in all agents, but only in robot's model
#        for agent_desc in description:
#            # list current descriptors to not to use them anymore
#            #currentDescriptors = map(lambda x: x.split()[1], agent_desc[2])
#            descriptor = self.get_discriminant(agent_desc[0], objL, ignoreFeatureL, partial_disc)
#
#            if descriptor:
#                agent = agent_desc[0]
#                break

        agent = "myself"
        # list current descriptors to not to use them anymore
        #currentDescriptors = map(lambda x: x.split()[1], description[0][2])
        descriptor = self.get_discriminant(agent, objL, ignoreFeatureL, partial_disc)

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
                val = self.oro.findForAgent(agent, '?val','[' + obj + ' ' + descriptor + ' ?val]')

            if val:
                #TODO: we only consider the first result item!
                valL.append(val[0])
            # otherwise, the object doesn't have this descriptor, and we don't include it

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
    # - ignoreFeatureL [feat1..featN] List of features not to use as discriminators.
    #
    # OUTPUT:
    # - objectID: ok
    # - UnsufficientInputError:
    #   - [FAILURE, "new info required"]: no match, new info required (forget previous description)
    #   - [SUCCESS, "Which value? ..."]: user should indicate value for descriptor (mantain previous description)
    #   - [SUCCESS, "additional info required"]: user should give additional info (mantain previous description)
    # -----------------------------------------------------------------------------#
    def clarify(self, description, ignoreFeatureL = []):

        objL = self.get_all_objects_with_desc(description)
        
        if len(objL) == 0:
            logger.debug(colored_print('Nothing found!', "magenta"))
        else:
            logger.debug(colored_print('Found these possible concepts ID: ', "magenta") +  colored_print(str(objL), 'blue'))
        
        if not self.oro: #No ontology server
            return 'UNKNOWN_CONCEPT'
            
        if not objL:
            questions = [Sentence(IMPERATIVE, '', 
                        [], 
                        [Verbal_Group(['give'], [],'present simple', 
                        [Nominal_Group([],['information'],[['new',[]]],[],[])], 
                        [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])]),
                        Indirect_Complement(['about'],[Nominal_Group(['the'],['object'],[],[],[])])],
                        [], [] ,Verbal_Group.affirmative,[])])]
            raise UnsufficientInputError({'status':'FAILURE', 'question':questions})
            #return "Give me knew information about the object"
            
        elif len(objL) == 1:
            return objL[0]
        
        elif len(objL) == 2 and self.oro.check('[' + objL[0] + ' owl:sameAs ' + objL[1] + ']'):
            return objL[0]
        
        else:
            agent, descriptor = self.get_descriptor(description, ignoreFeatureL)
            object = self.get_type_description(description)

            if descriptor:
                sentence_builder = SentenceFactory()
                
                question = None
                values = self.get_values_for_descriptor(agent, descriptor, objL)
                if not object: object = 'object'
                
                if descriptor == 'hasColor'  or  descriptor == 'mainColorOfObject':
                    questions = sentence_builder.create_w_question_choice(object, 'color', values)
                            
                elif descriptor == 'hasShape':
                    questions = sentence_builder.create_w_question_choice(object, 'shape', values)

                elif descriptor == 'hasSize':
                    questions = sentence_builder.create_w_question_choice(object, 'size', values)

                elif descriptor == 'isOn':
                    questions = sentence_builder.create_w_question_location(object, 'on', values)

                elif descriptor == 'isIn':
                    questions = sentence_builder.create_w_question_location(object, 'in', values)
                    
                elif descriptor == 'isNextTo':
                    questions = sentence_builder.create_w_question_location(object, 'next to', values)

                elif descriptor == 'isAt':
                    questions = sentence_builder.create_w_question_location(object, 'at', values)

                elif descriptor == 'isLocated':
                    questions = sentence_builder.create_w_question_location_PT(values, agent)
                
                elif descriptor == 'rdf:type':
                    questions = sentence_builder.create_w_question_choice(object, 'type', values)
                    
                else:
                    questions = sentence_builder.create_w_question_choice(object, descriptor, values)

                raise UnsufficientInputError({'status':'SUCCESS','question':questions})
                #return questions
                    
            else:
                questions = [Sentence(IMPERATIVE, '', [], 
                            [Verbal_Group(['give'], [],'present simple', 
                            [Nominal_Group([],['information'],[['more',[]]],[],[])], 
                            [Indirect_Complement([],[Nominal_Group([],['me'],[],[],[])]),
                            Indirect_Complement(['about'],[Nominal_Group(['the'],[object],[],[],[])])],
                            [], [] ,Verbal_Group.affirmative,[])])]
                raise UnsufficientInputError({'status':'SUCCESS','question':questions})
                #return "Give me more information about the object"

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
            logger.debug('Description ' + objectID +': ' + str(description))
            logger.debug('ObjL: ' + str(objL))

            agent, descriptor = self.get_descriptor(description,1)
            val = self.oro.findForAgent(agent, '?val','[' + objectID + ' ' + descriptor + ' ?val]')            
            
            if not val: 
                description.insert(0,objectID)
                break
                
            description = self.add_descriptor(agent, description, descriptor, val[0])            
            objL = self.get_all_objects_with_desc(description)

        return description

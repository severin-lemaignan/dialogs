# -*- coding: utf-8 -*-

"""This module implements the clarification process for ambiguous descriptions. 
Given a description of an object (ambigouos or not) it returns, if found, the 
object's identifier in oro. If necessary, it will query the human for additional
information.
"""

import logging

logger = logging.getLogger("dialogs")

from kb import KbError

from dialogs.resources_manager import ResourcePool

from dialogs.dialog_exceptions import UnsufficientInputError
from dialogs.sentence import *
from dialogs.sentence_factory import SentenceFactory
from dialogs.helpers.helpers import generate_id

from random import choice


class Discrimination(object):
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
    # - None: no description (or description format incorrect)
    # -----------------------------------------------------------------------------#
    def get_all_objects_with_desc(self, description):
        obj_list = None

        for agent_desc in description:

            obj_tmp = []

            try:
                obj_tmp = self.oro.findForAgent(ResourcePool().get_model_mapping(agent_desc[0]), agent_desc[1], agent_desc[2])
            except KbError: #The agent does not exist in the ontology
                pass

            # if no object found, no need to continue
            if not obj_tmp:
                obj_list = []
                break
            else:
                if obj_list is None:
                    obj_list = obj_tmp
                else:
                    obj_list = filter(lambda x: x in obj_list, obj_tmp)  # intersection

        return obj_list

    # -- GET_DISCRIMINANT ---------------------------------------------------------#
    # Queries the ontology for a list of discriminants. Returns the first one.
    # TODO: prioritize which discriminant to return.
    #
    # INPUT:
    # - agent
    # - object list
    # - ignore_descriptors: list of descriptors not to be used
    # - include_partial: if true, then partial discriminants are also returned
    # OUTPUT:
    # - discriminant: [C, discriminat] if complete, or [P, discriminant] if partial
    #   The new discriminant should be different from the ones already known or ignored
    # -----------------------------------------------------------------------------#
    def get_discriminant(self, agent, obj_list, ignore_descriptors, include_partial):
        discriminants = self.oro.discriminateForAgent(ResourcePool().get_model_mapping(agent), obj_list)
        logger.debug(colored_print('Possible discriminants: ', 'magenta') + \
                     str(colored_print(discriminants[1], 'blue')) + \
                     colored_print(" (complete discriminants: ", 'magenta') + \
                     str(colored_print(discriminants[0], 'blue')) + ")")

        complete_disc = discriminants[0]
        partial_disc = discriminants[1]

        if complete_disc:
            res = filter(lambda x: x not in ignore_descriptors, complete_disc)
        elif partial_disc and include_partial:
            res = filter(lambda x: x not in ignore_descriptors, partial_disc)
        else:
            res = None

        if res:
            # include randomization so the same discriminant is not always returned
            return choice(res)
        else:
            # No discriminant after applying the blacklist.
            return None

    # -- GET_DESCRIPTOR -----------------------------------------------------------#
    # Searches for a new descriptor candidate from all agents.
    #
    # INPUT:
    # - description: 
    #   [[agent1 '?obj' oro_query]..[[agentN '?obj' oro_query]]
    #   (oro_query= ['?obj hasColor blue',.. ?obj hasShape box'])
    # - ignore_features: list of features not to use as discriminants
    #   [feat1 ..featN]
    # - allowPartialDesc: consider also partial discriminants (1) or not (0) (0 default)
    #
    # OUTPUT:
    # - descriptor or None (if no discriminant for any agent found)
    # -----------------------------------------------------------------------------#
    def get_descriptor(self, description, ignore_features=None, partial_disc=True):

        if not ignore_features: ignore_features = []
        objL = self.get_all_objects_with_desc(description)
        descriptor = None
        agent = None

        #TODO bug in oro doesn't allow to search discriminants base on other agents models!!
        # we cannot search in all agents, but only in robot's model
        #        for agent_desc in description:
        #            # list current descriptors to not to use them anymore
        #            #currentDescriptors = map(lambda x: x.split()[1], agent_desc[2])
        #            descriptor = self.get_discriminant(agent_desc[0], objL, ignore_features, partial_disc)
        #
        #            if descriptor:
        #                agent = agent_desc[0]
        #                break

        agent = ResourcePool().default_model
        # list current descriptors to not to use them anymore
        #currentDescriptors = map(lambda x: x.split()[1], description[0][2])
        descriptor = self.get_discriminant(agent, objL, ignore_features, partial_disc)

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
                val = self.oro.findForAgent(ResourcePool().get_model_mapping(agent), '?val', [obj + ' ' + descriptor + ' ?val'])

            if val:
                #TODO: we only consider the first result item!
                valL.append(self.oro.getLabel(val[0]))
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
                items = item.split()
                if value in items:
                    return items[2]
            return None

        type = None

        for desc in description:
            type = find('rdf:type', desc[2])
            if type: break

        return ResourcePool().ontology_server.getLabel(type)

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
    def clarify(self, description, ignoreFeatureL=None):

        if not ignoreFeatureL: ignoreFeatureL = []
        objL = self.get_all_objects_with_desc(description)

        if len(objL) == 0:
            logger.debug(colored_print('Nothing found!', "magenta"))
        else:
            logger.debug(
                colored_print('Found these possible concepts ID: ', "magenta") + colored_print(str(objL), 'blue'))

        if not self.oro: #No ontology server
            return 'UNKNOWN_CONCEPT_' + generate_id(with_question_mark=False)

        if not objL:
            questions = SentenceFactory().create_i_dont_understand()
            raise UnsufficientInputError({'status': 'FAILURE', 'question': questions})
            #return "I don't understand"

        else:
            # Check if the speaker sees only some of the object.
            # If he sees none of them, discriminate on the whole set.
            # Else, discriminate only on visible objects.
            agent = description[0][0]
            logger.debug("Checking which of these objects are visible for " + agent)
            visible_objects = self.visible_subset(agent, objL)

            if visible_objects:
                objL = visible_objects
                logger.debug(colored_print('Only ', "magenta") +
                             colored_print(str(objL), 'blue') +
                             colored_print(" are visible by " + agent, "magenta"))
            else:
                logger.debug(colored_print('None are visible by ' + agent, "magenta"))

            if len(objL) == 1:
                return objL[0]

            if len(objL) == 2 and self.oro.check(['%s owl:sameAs %s' % (objL[0], objL[1])]):
                return objL[0]

            agent, descriptor = self.get_descriptor(description, ignoreFeatureL)
            object = self.get_type_description(description)

            if descriptor:
                sentence_builder = SentenceFactory()

                question = None
                values = self.get_values_for_descriptor(agent, descriptor, objL)
                if not object: object = 'object'

                if descriptor == 'hasColor' or descriptor == 'mainColorOfObject':
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
                    questions = sentence_builder.create_w_question_generic_descriptor(object, descriptor, values)

                raise UnsufficientInputError({'status': 'SUCCESS', 'question': questions})
                #return questions

            else:
                questions = [Sentence(IMPERATIVE, '', [],
                                      [VerbalGroup(['give'], [], 'present simple',
                                                    [NominalGroup([], ['information'], [['more', []]], [], [])],
                                                    [IndirectComplement([], [NominalGroup([], ['me'], [], [], [])]),
                                                     IndirectComplement(['about'], [
                                                         NominalGroup(['the'], [object], [], [], [])])],
                                          [], [], VerbalGroup.affirmative, [])])]
                raise UnsufficientInputError({'status': 'SUCCESS', 'question': questions})
                #return "Give me more information about the object"

    def visible_subset(self, agent, id_list):
        """ Returns the list of visible objects for an agent from a list of objects.
        """

        visible_objects = self.oro.findForAgent(ResourcePool().get_model_mapping(agent), "?o", [agent + " sees ?o"])

        return list(set(id_list) & set(visible_objects))

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

    # -- FIND_UNAMBIGUOUS_DESC ---------------------------------------#
    # Searches an unambiguous description for a given object. 
    # If it fails, it returns the most complete description found.
    #
    # INPUT:
    # - objectID: object to be described
    #
    # OUTPUT:
    # - a tuple (is_unambigous, description)
    #     - is_unambigous is a boolean
    #     - description is a set of partial statements like 
    #       "?obj rdf:type Superman" describing as well as possible 
    #       the object.
    # ----------------------------------------------------------------#
    def find_unambiguous_desc(self, objectID):
        description = None
        # get the first class name
        types = [t for t in self.oro.getDirectClassesOf(objectID).keys() if t not in ["ActiveConcept"]]

        # Not type asserted/inferred? then assume this object is unique.
        if not types:
            return True, []

        type = types[0]

        myself = ResourcePool().default_model
        description = [[myself, '?obj', ['?obj rdf:type ' + type]]]
        objL = self.get_all_objects_with_desc(description)

        while len(objL) > 1:

            nbCandidates = len(objL)

            logger.debug('Description ' + objectID + ': ' + str(description))
            logger.debug('ObjL: ' + str(objL))

            agent, descriptor = self.get_descriptor(description, [], True)

            if not descriptor:
                break

            val = self.oro.findForAgent(ResourcePool().get_model_mapping(agent), '?val', [objectID + ' ' + descriptor + ' ?val'])

            if not val:
                break

            description = self.add_descriptor(agent, description, descriptor, val[0])
            objL = self.get_all_objects_with_desc(description)

            if nbCandidates == len(objL):
                logger.error("While trying to find an unambiguous description" + \
                             " of " + objectID + ", oro answered a non-discriminant" + \
                             " property. Bug in oro? Halting here for now.")
                break

        if len(objL) == 1:
            unambiguous = True
        else:
            unambiguous = False

        return unambiguous, description[0][2]

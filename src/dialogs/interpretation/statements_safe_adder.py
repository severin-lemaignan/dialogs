# coding=utf-8
import logging
logger = logging.getLogger("dialogs")

import random
from dialogs.helpers.helpers import colored_print

from dialogs.resources_manager import ResourcePool
from dialogs.dialog_exceptions import UnsufficientInputError


class StatementSafeAdder(object):
    """ This class inserts or Removes statements in the ontology,
    Handle inconsistency due to adding information in the ontology.
    """

    def __init__(self):
        #This holds the statements created from the main clause that have to be added in or removed from the ontology
        self._statements = []

        #This holds unidentified IDs that are generated while creating the statements of a resolved sentence.
        #   Possibly in the case of a negative sentence involving an action that is to be identity.
        self._unclarified_ids = []

        # This holds statements that are to be removed from the ontology.
        self._statements_to_remove = []

        # This hold the current speaker
        self._current_speaker = "myself"

    def process(self):
    # Case of Statements that are to be removed
        #   Clarify then remove
        if self._statements_to_remove:
            stmts = self.clarify(self._statements_to_remove, self._unclarified_ids)
            self.remove(stmts)
            return stmts

        # Default case
        self.safe_add(self._statements)
        return self._statements


    def clarify(self, statements, ids):
        """This attempts to identify a matching reference of the action described from the statements
            - statements: the field of statements used to query the ontology
            - ids: the field of references that are to be identified
            
            e.g: Danny doesn't drive the blue car.
            statements = [?sit rdf:type Drive, ?sit performedBy DANNY, ?sit involves BLUE_CAR]
            ids = [?sit]
            Before removing the statements set from the ontology, we determine if there is a matching action to ?sit
        """
        current_s = statements

        for id in ids:
            stmts = []

            #Attempt to find the unidentified IDs
            onto = ''
            try:
                onto = ResourcePool().ontology_server.find([id], current_s)
            except AttributeError:
                pass

            #Replace Matching IDs
            if onto:
                logger.info(
                    colored_print("... Found ID " + onto[0] + " matching description given statements.", "magenta"))
                for s in current_s:
                    stmts.append(s.replace(id, onto[0]))

                current_s = stmts

        return current_s


    def safe_add(self, statements):
        """ This process the commitment of new statements in the ontology
            and deals with adding inconsistency
        """

        models = [ResourcePool().default_model]
        if self._current_speaker:
            models.append(self._current_speaker)

        policy = {"method": "safe_add", "models": models}

        try:
            if not ResourcePool().ontology_server.revise(statements, policy):
                logger.debug(colored_print("At least one statement hasn't been " + \
                                           "pushed to the ontology server because it would lead to inconsistencies."))

        except AttributeError: #the ontology server is not started of doesn't know the method
            pass

    def remove(self, statements):
        try:
            ResourcePool().ontology_server.remove(statements)
        except AttributeError: #the ontology server is not started of doesn't know the method
            pass
        
        
        
        
def unit_tests():
    """This function tests the main features of the class StatementBuilder"""
    print("This is a test...")
     
if __name__ == '__main__':
    unit_tests()
    

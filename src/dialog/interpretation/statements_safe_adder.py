import logging
logger = logging.getLogger("dialog")

import random

from dialog.resources_manager import ResourcePool
from dialog.dialog_exceptions import UnsufficientInputError

class StatementSafeAdder():
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
        
        
    def process(self):        
        
        # Case of Statements that are to be removed
        #   Clarify then remove
        if self._statements_to_remove:
            stmts = self.clarify(self._statements_to_remove,  self._unclarified_ids)
            self.remove(stmts)
            return stmts
        
        # Default case
        self.safe_add(self._statements)
        return self._statements
        
        
    def clarify(self, statements, ids):
        """This attempts to identify the reference of the action described from the statements
            - statements: the field of statements used to query the ontology
            - ids: the field of references that are to be identified
        """
        current_s = statements
        
        for id in ids:
            stmts = []
            
            #Attempt to find the unidentified IDs
            onto = ''
            try:
                onto = ResourcePool().ontology_server.find(id, current_s)
            except AttributeError:
                pass
            
            #Replace Matching IDs
            if onto :
                logger.info(" \t... Found ID " + onto[0] + " matching description given statements.")
                for s in current_s:
                    stmts.append(s.replace(id, onto[0]))
                                        
                current_s = stmts
        
    
        return current_s
            
            
    def safe_add(self, statements):
        for s in statements:
            onto = True
            logger.info("\t ADDED... >> " + s)
            try:
                onto = ResourcePool().ontology_server.safeAdd([s])
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
                
            if not onto:
                logger.debug("\t*********************************************")
                logger.debug("\t* Ooopps!! INCONSISTENT STATEMENT    ***")
                logger.debug("\t*********************************************")
                logger.debug("\t.... >> "  + s)
                


    def remove(self, statements):
        for s in statements:            
            logger.info("\t REMOVED... << " + s)
            try:
                ResourcePool().ontology_server.remove([s])
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
        logger.info("\t....................... <<<<")
        
        
        
        
def unit_tests():
    """This function tests the main features of the class StatementBuilder"""
    print("This is a test...")
     
if __name__ == '__main__':
    unit_tests()
    

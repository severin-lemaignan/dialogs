import logging
import random

from dialog.resources_manager import ResourcePool
from dialog.dialog_exceptions import UnsufficientInputError

class StatementSafeAdder():
    """ This class inserts or Removes statements in the ontology,
    Handle inconsistency due to adding information in the ontology.
    """
    def __init__(self):
        self._statements = None
    
    def process(self, statements, ids):        
        self._statements = statements
        
        # Case of Statements to be identified then removed
        if ids:
            logging.info("Found unidentified IDs... Trying to clarify " + str(ids))        
            if self.clarify(self._statements, ids):
                self.remove(self._statements)

        
        # Case of Statements to be added
        else:
            logging.info("Adding statements in the Ontology/")
            self.safeAdd(self._statements)
        
        return self._statements
        
        
    def clarify(self, statements, ids):
        self._statements = statements
        while ids:
            id = ids.pop()
            stmts = []
            
            onto = ''
            try:
                onto = ResourcePool().ontology_server.find(id, statements)
            except AttributeError:
                pass
            
            if onto :
                logging.info(".... \t Found matching ID ... '" + id + "' has been clarified and turned into '" + onto[0] + "' .")
                for s in statements:
                    stmts.append(s.replace(id, onto[0]))
                    
                self._statements = stmts
                return True
                
            else:
                logging.info(".... \t Found NO matching ID ... '" + id + "' has not been clarified... \nNothing to be removed")
                return False
            
            
    def safeAdd(self, statements):
        for s in statements:
            onto = True
            logging.info("\t ADDED... >> " + s)
            try:
                onto = ResourcePool().ontology_server.safeAdd([s])
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
                
            if not onto:
                logging.debug("\t*********************************************")
                logging.debug("\t* Ooopps!! INCONSISTENT STATEMENT    ***")
                logging.debug("\t*********************************************")
                logging.debug("\t.... >> "  + s)
                


    def remove(self, statements):
        for s in statements:            
            logging.info("\t REMOVED... << " + s)
            try:
                ResourcePool().ontology_server.remove([s])
            except AttributeError: #the ontology server is not started of doesn't know the method
                pass
        logging.info("\t....................... <<<<")           
        
        
        
        
def unit_tests():
    """This function tests the main features of the class StatementBuilder"""
    print("This is a test...")
     
if __name__ == '__main__':
    unit_tests()
    

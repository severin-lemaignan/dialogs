import logging
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
        
        #This holds the satements that are created from a conjunctive clause
        #    i.e when the attributes sentence.sv.vrb_sub_sentence is not empty
        self._sub_statements = []
        
        #This holds unidentified IDs that are generated while creating the statements of a resolved sentence.
        #   Possibly in the case of a negative sentence involving an action that is to be identity.
        self._unresolved_ids = []   
        """
        #When this field is set to True, statement that are being processed are removed from the ontology
        self._process_on_removal = False
        """
        
    def process(self):        
        
        # Case of Statement added regarding the sub_statements
        if self._sub_statements:
            self._statements = self.retrieve_main_clause(self._statements)
            logging.info("Adding statements in the Ontology/")
            self.safeAdd(self._statements)
            return self._statements
        """
        # Case of Statements to be removed
        if self._process_on_removal:
            logging.info("Found unidentified IDs... Trying to clarify " + str(ids))        
            if self.clarify(self._statements, ids):
                self.remove(self._statements)
            
            return self._statements

        
        # Case of Statements to be added
        logging.info("Adding statements in the Ontology/")
        self.safeAdd(self._statements)
        
        return self._statements
        """
        
    def clarify(self, statements, ids):
        """This attempts to identify the reference of the action described from the statements
            - statements: the field of statements used to query the ontology
            - ids: the field of references that are to be identified
        """
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
        
        
    def process_main_clause_statements(self, statements):
        """
        
        """
        # For all the subordinative conjunctions See http://englishplus.com/grammar/00000377.htm 
        #
        # Case of 'if':
        #   E.g: I will go to Toulouse if you get the small car
        #
        #   we create the statements s1 = [go_to_toulouse rdf:type Go, go_to_toulouse performedBy current_speaker, go_to_toulouse hasGoal TOULOUSE]
        #   and the sub_statements s2 = [?xxx rdf:type Get , ?xxx performedBy myself, ?xxx actsOnObject SMALL_CAR]
        #   Then, we add the statement s1 in the ontology if there exists a reference that matches the substatements s2.
        #
        # Case of 'when' or 'before'
        #  E.g: I will go to Toulouse when you get the small car
        #
        #  We process as in the above example. 
        #  However, there should be implemented a function that retrieve when the action described by the statement started
        #
        # Case of 'after'
        #  E.g: I will go to Toulouse when you get the small car
        #  We process likewise the above example. 
        #  However, there should be implemented a function that retrieve when the action described by the statement ended
        
        # Case of 'while' or 'as long as'
        #  We process likewise the 2 preceding examples with both an ending and starting point.
        #
        # Case of 'unless'
        #   in this case, we remove the statements s1 if the s2 is retrieved
        
        
        stmts = statements
        
        #TODO
        for s in self._sub_statements:
            stmts.extend(s[1])
            
        return stmts
        
        
        
        
def unit_tests():
    """This function tests the main features of the class StatementBuilder"""
    print("This is a test...")
     
if __name__ == '__main__':
    unit_tests()
    

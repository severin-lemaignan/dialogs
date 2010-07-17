import logging
import random

from resources_manager import ResourcePool

class StatementSafeAdder():
    """ Add statement in the ontology, from statement with resolved ID"""
    def __init__(self, 
                 statements = None, 
                 ids = None):        
        self._statements = statements
        self._unresolved_ids = ids
        
    def process(self, resolved):
        if not resolved:
            logging.info("Found unresolved Sentence.")        
            self._statements = self.clarify(self._statements, self._unresolved_ids)
        logging.info("Adding statement in the Ontology/")
        #self.safeAdd(self._statements)
        #print "Statement Safe Adder:  List of unresolved Ids:", self._unresolved_ids
        
        
        
        
    def clarify(self, statements, ids):
        if not ids:
            return statements
        
        logging.info("Found unresolved ID from StatementBuilder. \n\tClarifying missing IDs: " + str(ids))
        
        while ids:
            id = ids.pop()
            stmts = []
            """
            logging.debug("Searching in Ontology an existing ID matching the assertion : find " + id + ",  " + str (statements))
            onto_id = self.oro.find(id, str(statements))
            if onto_id:
                logging.info(" Found existing ID "+ str (onto_id)+ "")
                for s in statements:
                    stmts.append(s.replace(id, onto_id[0]))
            else:
            """
            new_id = id.lstrip('?')
            logging.info("\tGenerating a new Information in the Ontology with ID:" + new_id)
            for s in statements:
                stmts.append(s.replace(id, new_id))
            
            statements = stmts 
                
        return statements
            
            
    def safeAdd(self, statements):
        ResourcePool().ontology_server.safeAdd(statements)


def generate_id(with_question_mark = True):
    sequence = "0123456789abcdefghijklmopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sample = random.sample(sequence, 5)
    return ("?" + "".join(sample)) if with_question_mark else ("".join(sample))

def printer(list):
    for l in list:
        print l

def unit_tests():
    """This function tests the main features of the class StatementBuilder"""
    print("This is a test...")
     
if __name__ == '__main__':
    unit_tests()
    

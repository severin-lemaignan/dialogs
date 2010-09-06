#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This test scenario can be invoked either as a standalone Python script or
through the dialog_test executable.
"""

import unittest
from dialog.dialog_core import Dialog
from dialog.resources_manager import ResourcePool

class TestMovingToLondonScenario(unittest.TestCase):
    """
    Scenario
    --------
    ACHILLE and JULIE are moving from Toulouse to London, and they must
    pack everything before leaving. ACHILLE is sorting its video tapes, and he 
    throws away the oldest ones. Jido is watching him.

    Setup:
      One trashbin, one cardboard box, 2 tapes on the table [TAPE1 = Lord of 
      the Rings (lotr) and TAPE2 = HotShots2 (hs2)].
    """
    
    def setUp(self):
        self.dialog = Dialog()
        self.dialog.start()
        
        self.oro = ResourcePool().ontology_server
        
        try:
            
            self.oro.reset()
            
            self.oro.add([  'ACHILLE rdf:type Human',
                            'ACHILLE rdfs:label Achille',
                            'JULIE rdf:type Human', 
                            'JULIE rdfs:label Julie',
                            'TABLE rdf:type Table',
                            'Trashbin rdfs:subClassOf Box',
                            'CardBoardBox rdfs:subClassOf Box',
                            'CardBoardBox rdfs:label "cardboard box"',
                            'TRASHBIN rdf:type Trashbin',
                            'CARDBOARD_BOX rdf:type CardBoardBox',
                            'CARDBOARD_BOX isOn TABLE',
                            'TAPE1 rdf:type VideoTape', 
                            'TAPE1 rdfs:label "The Lords of the rings"', 
                            'TAPE1 isOn TABLE',
                            'TAPE2 rdf:type VideoTape', 
                            'TAPE2 rdfs:label "Hot Shots 2"', 
                            'TAPE2 isOn TABLE',])
            """           
            self.oro.addForAgent('ACHILLE',
                        ['BLUE_TRASHBIN rdf:type Trashbin',
                        'PINK_TRASHBIN rdf:type Trashbin',
                        'BLACK_TAPE rdf:type VideoTape', 'BLACK_TAPE isIn PINK_TRASHBIN',
                        'GREY_TAPE rdf:type VideoTape', 'GREY_TAPE isOn HRP2TABLE'])
            """        
        except AttributeError: #the ontology server is not started of doesn't know the method
            print("Couldn't connect to the ontology server. Aborting the test.")
            sys.exit(0)

    def test_step1(self):
        """ACHILE puts TAPE1 in CARDBOARDBOX"""

        self.oro.add(['TAPE1 isIn CARDBOARD_BOX'])
                            
        stmt = "Jido, what is in the box?"
        answer = "This box"
        ####
        res = self.dialog.test('ACHILE', stmt, answer)
         
        expected_result = ['* rdf:type Give',
                            '* performedBy myself',
                            'ACHILE_HUMAN1 desires *',
                            '* actsOnObject BLACK_TAPE'
                            '* receivedBy ACHILE_HUMAN1']

        self.assertTrue(check_results(res[0], expected_result))
    

    def tearDown(self):
        self.dialog.stop()
        self.dialog.join()

def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMovingToLondonScenario)
    
    return suite
    
if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(test_suite())

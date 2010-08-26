"""
 Created by Chouayakh Mahdi                                                       
 06/07/2010                                                                       
 The package contains functions to perform test                                   
 It is more used for the subject                                                  
 Functions:                                                                       
    compare_nom_gr : to compare 2 nominal groups                                  
    compare_icompl : to compare 2 indirect complements                            
    compare_vs : to compare 2 verbal structures                                   
    compare_sentence : to compare 2 sentences                                     
    compare_utterance : to compare 2 replies                                          
    display_ng : to display nominal group                                         
    display : to display class Sentence                                           
    unit_tests : to perform unit tests                                           
"""
import logging

import preprocessing
import analyse_sentence



class Parser:
    def __init__(self):
        pass
    
    def parse(self, nl_input, active_sentence = None):

        #Return active_sentence if not empty, possibly send from Dialog.
        if active_sentence:
            return [active_sentence]
	
	#Do all basic replacements (like capitals, n't -> not, etc) + splits in several 
        #sentence with points.
        self._sentence_list = preprocessing.process_sentence(nl_input)
        
        #Do the actual grammatical parsing
        self._class_list = analyse_sentence.sentences_analyzer(self._sentence_list)
        
        for s in self._class_list:
            logging.debug(str(s))
        
        return self._class_list
 

import logging
logger = logging.getLogger("dialog")

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
            logger.debug(str(s))
        
        return self._class_list
 

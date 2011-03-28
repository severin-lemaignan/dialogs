
import logging
logger = logging.getLogger("dialog")

import preprocessing
import analyse_sentence



class Parser:
    def __init__(self):
        pass
   
    def preprocess(self, nl_input, active_sentence = None):

        #Return active_sentence if not empty, possibly send from Dialog.
        if active_sentence:
            return [active_sentence]

		#Do all basic replacements (like capitals, n't -> not, etc) + splits in several 
        #sentence with points.
        sentence_list = preprocessing.process_sentence(nl_input)

        return sentence_list
 

    def parse(self, preprocessed_sentences, active_sentence = None):

        #Return active_sentence if not empty, possibly send from Dialog.
        if active_sentence:
            return active_sentence
       
        self._sentence_list = preprocessed_sentences

        #Do the actual grammatical parsing
        self._class_list = analyse_sentence.sentences_analyzer(self._sentence_list)
        
        return self._class_list
 

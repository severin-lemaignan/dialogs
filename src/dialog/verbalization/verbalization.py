import logging
import utterance_rebuilding

class Verbalizer:
    """Implements the verbalization module: Verbalizer.verbalize() takes as
    input a Sentence object and build from it a sentence in natural language.
    """
    def verbalize(self, sentence):
        logging.debug("Verbalizing now...")
        nl_sentence = utterance_rebuilding.verbalising(sentence)
        logging.debug("Rebuild sentence to: \"" + nl_sentence + "\"")
        return nl_sentence

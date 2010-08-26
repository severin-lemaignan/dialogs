import logging
logger = logging.getLogger("dialog")

import utterance_rebuilding

class Verbalizer:
    """Implements the verbalization module: Verbalizer.verbalize() takes as
    input a Sentence object and build from it a sentence in natural language.
    """
    def verbalize(self, sentence):
        logger.debug("Verbalizing now...")
        nl_sentence = utterance_rebuilding.verbalising(sentence)
        logger.debug("Rebuild sentence to: \"" + nl_sentence + "\"")
        return nl_sentence

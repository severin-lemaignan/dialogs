# coding=utf-8
import logging

logger = logging.getLogger("dialogs")

from dialogs.verbalization import utterance_rebuilding


class Verbalizer(object):
    """Implements the verbalization module: Verbalizer.verbalize() takes as
    input a Sentence object and build from it a sentence in natural language.
    """

    def verbalize(self, sentences):
        logger.debug("Verbalizing now...")

        nl_sentence = utterance_rebuilding.verbalising(sentences)
        logger.debug("Rebuild sentence to: \"" + nl_sentence + "\"")

        return nl_sentence

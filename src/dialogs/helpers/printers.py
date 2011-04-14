#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from sentence_atoms import *
from helpers import colored_print

#OUTPUT_MODE = 'css'
OUTPUT_MODE = 'color'

def color_printer(text, atom):
    if atom == NOMINAL_GROUP:
        return level_marker() + colored_print('Nominal group:\n\t', 'bold') + text
    if atom == VERBAL_GROUP:
        return level_marker() + colored_print('Verbal group:\n\t', 'bold') + text
    if atom in [INDIRECT_OBJECT, DIRECT_OBJECT, RELATIVE_GRP, SUB_SENTENCE, SECONDARY_VERBAL_GROUP]:
        return level_marker() + atom.lower().replace("_", " ") + '\n\t' + text + "\n"
    if atom == NOUN_CMPLT:
        return level_marker() + '[OF] \n\t' + text + "\n"
    if atom == SENTENCE_AIM:
        if not text:
            return "\n"
        return " (aim: " + text + ")\n"
    if atom == SENTENCE_TYPE:
        return colored_print(">>" + text.upper(), 'bold')
    if atom == AGRAMMATICAL_SENTENCE:
        return colored_print(">> The sentence does not appear to be grammatically valid! <<\n", 'red') + text
    if atom == ADVERBIAL:
        return level_marker() + "Adverbials: " + colored_print(text, 'yellow') + "\n"
    if atom == VERBAL_ADVERBIAL:
        return level_marker() + "Verbal adverbials: " + colored_print(text, 'green') + "\n"
    if atom in [DETERMINER, PREPOSITION]:
        return colored_print(text, 'yellow') + " "
    if atom == VERB:
        return colored_print(text, 'magenta')
    if atom == ADJECTIVE:
        return colored_print(text, 'green') + " "
    if atom == ADJECTIVE_QUALIFIER:
        return colored_print(text, 'red') + " "
    if atom == NOUN:
        return colored_print(text, 'blue') + "\n"
    if atom == TENSE:
        return level_marker() + " (" + text + ")\n"
    if atom in [CONJUNCTION, DIGIT, QUANTIFIER]:
        return colored_print("[" + text.upper() + "] ", 'bold')
    if atom == ID:
        return colored_print(text, 'white', 'blue') + '\n'
    if atom == NEGATIVE:
        return level_marker() + colored_print('NEGATION', 'red') + " " + text
    if atom == RESOLVED:
        return text + level_marker() + colored_print('>resolved<', 'green')
    if atom == NOT_RESOLVED:
        return text + level_marker() + colored_print('>not resolved<', 'red')
    else:
        return text

def css_printer(text, atom):
    if atom in [SENTENCE, SUBJECT, NOMINAL_GROUP, VERBAL_GROUP, SECONDARY_VERBAL_GROUP, SUB_SENTENCE, DIRECT_OBJECT, INDIRECT_OBJECT, RESOLVED, NOT_RESOLVED, RELATIVE_GRP, NOUN_CMPLT, NEGATIVE]:
        return "\n<div class='" + atom.lower() + "'>\n" + text + "\n</div>\n"
    if atom in [SENTENCE_AIM, SENTENCE_TYPE, TENSE, VERB, QUANTIFIER, CONJUNCTION, DIGIT, DETERMINER, NOUN, ADJECTIVE, ADJECTIVE_QUALIFIER, VERBAL_ADVERBIAL, ID]:
        return "<span class='" + atom.lower() + "'>" + text + "</span> "
    if atom in [PREPOSITION, ADVERBIAL]:
        return "<br/><span class='" + atom.lower() + "'>" + text + "</span> "
    if atom == AFFIRMATIVE:
        return text
    if atom == AGRAMMATICAL_SENTENCE:
        return "\n<div class='sentence invalid_grammar'>\n" + text + "\n</div>\n"
    else:
        stderr.writeln("Error: " + text + "has no grammatical category!") 
        return text

def pprint(text, atom):
    if OUTPUT_MODE == "color":
        return color_printer(text, atom)
    if OUTPUT_MODE == "css":
        return css_printer(text, atom)


def level_marker(level=1, symbol='|', color='red'):
    """Insert 'symbol' at the beginning of the current line
    """
    #if OUTPUT_MODE == "color":
    #    return '\033[s\033[' + str(level) + 'G' + colored_print(symbol, color) + "\033[u\033[" + str(len(symbol) + 1) + "C"
    #else:
    return ""


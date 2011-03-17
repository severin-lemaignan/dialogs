#!/usr/bin/python
# -*- coding: utf-8 -*-

from sentence_atoms import *

OUTPUT_MODE = 'css'

def color_printer(text, atom):
    if atom == SENTENCE_TYPE:
        return colored_print(">>" + text.upper(), 'bold')
    if atom == PREPOSITION:
        return colored_print(text, 'yellow')
    else:
        return text

def css_printer(text, atom):
    if atom == SENTENCE_TYPE:
        return "<span class='sentence_type'>" + text + "</span>"
    if atom == PREPOSITION:
        return "<span class='preposition'>" + text + "</span>"
    else:
        return text

def pprint(text, atom):
    if OUTPUT_MODE == "color":
        return color_printer(text, atom)
    if OUTPUT_MODE == "css":
        return css_printer(text, atom)

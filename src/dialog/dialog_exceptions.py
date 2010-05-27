# -*- coding: utf-8 -*-

class UnsufficientInputError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class EmptyGrammaticalGroup(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UnrecognizedSentenceType(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

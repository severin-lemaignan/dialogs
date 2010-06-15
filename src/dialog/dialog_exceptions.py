# -*- coding: utf-8 -*-

class UnsufficientInputError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class GrammaticalError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
class EmptyGrammaticalGroup(GrammaticalError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UnrecognizedSentenceType(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UnknownVerb(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


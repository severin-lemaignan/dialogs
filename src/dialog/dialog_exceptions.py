# -*- coding: utf-8 -*-

class DialogError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
class UnsufficientInputError(DialogError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class GrammaticalError(DialogError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
class EmptyGrammaticalGroup(GrammaticalError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UnrecognizedSentenceType(DialogError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UnknownVerb(DialogError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
    
class EmptyNominalGroupId(DialogError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

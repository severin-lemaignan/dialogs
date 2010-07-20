# -*- coding: utf-8 -*-

class DialogError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
class UnsufficientInputError(DialogError):
    """ This exception is raised when discrimination routines need more 
    information from the user to actually find out the ID of the concept being
    resolved.
    
    It can take 3 kind of parameters:
    - (recommended) ['SUCCESS'|'FAILURE', [Sentence]]
            -> 'SUCCESS' if the discrimination could find candidates but need
            more details, 'FAILURE' if no candidates have been found.
            -> list of instances of the Sentence class to be verbalized, containing 
            the question to be asked to the user
    - Sentence -> a instance of the Sentence class to be verbalized, containing 
        the question to be asked to the user
    - String -> the text to be send to the human, in natural language
    """
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

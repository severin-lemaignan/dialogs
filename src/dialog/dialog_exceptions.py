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
    
    The expected value of the exception is a map containing 3 informations:
     - status: 'SUCCESS' if the discrimination could find candidates but need
            more details, 'FAILURE' if no candidates have been found.
     - object: the object (for instance, a nomnial group) that was being resolved
     - object_with_more_info: the object with more information to resolve the one that was being resolved
     - sentence:  if 'object' already holds a nominal group, this holds the sentence that was being resolved.
     - question: a question (as a set of instance of Sentence class) to be asked 
     to the user
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
    
class UnresolvedAnaphora(DialogError):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

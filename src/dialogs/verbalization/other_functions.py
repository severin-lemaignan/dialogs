
"""
 Created by Chouayakh Mahdi                                                       
 07/07/2010                                                                       
 The package contains functions used by all other packages                        
 Functions:   
    find_cap_lettre : to return 1 if the word starts with upper case letter     
    find_plus : to return 1 if the word containe '+'                                                           
    list_rebuilding : to return the list of strings without '+'                     
    eliminate_redundancy : to eliminate redundancy in the phrase                  
    convert_string : to return concatenate token to have a string (sentence) 
    plural : to to return 1 if the word is a plural
    plural_noun : to return 1 if the nominal group is a plural      
    number : return 1 if the word is a number and 2 if it is a adjective-number  
    is_an_adj : to know if a word is an adjective 
"""
from dialogs.resources_manager import ResourcePool



def find_cap_lettre(word):
    """
    Function return 1 if the word starts with upper case letter                       
    Input=word               Output=flag(0 if no upper case or 1 if upper case)        
    """
    if word[0] in ResourcePool().capital_letters:
        return 1
    return 0



def find_plus(word):
    """
    returns 1 if the word containe '+'                       
    Input=word                                           Output=flag       
    """
    
    if '+' in word:
        return 1
    return 0



def list_rebuilding(string):
    """
    returns the list of strings without '+'                            
    Input=the string           Output=the list of strng corresponding                
    """

    if '+' in string:
        return [string[:string.index('+')]] + list_rebuilding(string[string.index('+')+1:])
    return [string]



def eliminate_redundancy(phrase):
    """
    to eliminate redundancy in the phrase                              
    Input=phrase                                             Output=phrase           
    """

    #init
    phrase_aux=[]

    if phrase!=[]:

        phrase_aux=[phrase[0]]

        #We loop in phrase
        for i in range(1,len(phrase)):
            if phrase[i]!=phrase[i-1]:
                phrase_aux=phrase_aux+[phrase[i]]

    return phrase_aux



def convert_string(token_list):
    """
     returns concatenate token to have a string (sentence)
     Input=list of token                                    Output=sentence           
    """

    #list is empty
    if token_list==[]:
        return ''

    if len(token_list)==1:
        return token_list[0]
    else:
        return token_list[0]+' '+convert_string(token_list[1:])
    
    

def plural(word,quantifier,determinant):
    """Returns 1 if the word is a plural

    Input=list of word
    Output=flag(0 if singular or 1 if plural)
    """

    #If the word ends with 's' it is not a special one
    if word.endswith('s'):
        for n in ResourcePool().nouns_end_s:
            if n==word:
                return 0
        return 1

    #If it is a pronoun in plural
    if word=='we' or word=='I' or word=='you' or word=='they':
        return 1

    for k in ResourcePool().plural_nouns:
        if word == k[0]:
            return 1

    #If the quantifier confirm it
    if quantifier=='SOME' or quantifier=='ALL' or quantifier=='ANY':
        return 1
    if quantifier=='DIGIT' and determinant[0]!='one':
        return 1

    #Default case
    return 0

def plural_noun(sn):
    """
    Function return 1 if the nominal group is a plural                      
    Input=list of nominal group             Output=flag(0 if singular or 1 if plural)       
    """
    
    #init
    i=1
    
    #If we have many subject, we need to know the conjunction
    while i < len(sn):
        if sn[i]._conjunction!='AND':
            if plural(sn[i].noun[0], sn[i]._quantifier, sn[i].det)==1:
                return 1
        else:
            #If other conjunction, we have just one element
            return 1
        i=i+1
      
    #If we have some we can have all possibilities  
    if sn[0].noun==[] and sn[0]._quantifier!='SOME':
        return 0
    elif sn[0]._quantifier=='SOME':
        return 1
    else:
        return plural(sn[0].noun[0],sn[0]._quantifier, sn[0].det)




def number(word):
    """
    Function return 1 if the word is a number and 2 if it is a adjective-number                    
    Input=word          Output=flag(0 if no number or 1 if number or 2 adjective-number)        
    """
    
    for n in ResourcePool().numbers:
        if word.startswith(n[1]):
            return 1
        
        if word.startswith(n[0]):
            #We have adjective-number 
            if word.endswith('th'):
                return 2
            else:
                return 1
    return 0



def is_an_adj(word):
    """
    knows if a word is an adjective                                  
    Input=word                Output=1 if it is an adjective and 0 if not                     
    """
    
    #It is a noun verb pronoun or determinant so we have to return 0
    if word in ResourcePool().special_nouns+ResourcePool().special_verbs:
        return 0
    
    #For the regular adjectives
    for k in ResourcePool().adjective_rules:
        if word.endswith(k):
            return 1
    
    #For adjectives created from numbers
    if word.endswith('th') and number(word)==2:
        return 1
        
    #We use the irregular adjectives list to find it
    if word in ResourcePool().adjectives.keys()+ResourcePool().adjective_numbers+ResourcePool().adj_quantifiers:
        return 1
    
    return 0

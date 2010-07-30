
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
    is_an_adj : to know if a word is an adjective
"""
from resources_manager import ResourcePool


"""
Statement of lists
"""
cap_let_list=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
noun_end_s_sing=['news','glass', 'bus','Laas','business']
plural_name=['people']
adj_rules=['al','ous','est','ing','y','less','ble','ed','ful','ish','ive','ic']


"""
We have to read all irregular adjectives before the processing                    
"""
adjective_list = ResourcePool().adjectives.keys()


"""
We have to read all nouns which have a confusion with regular adjectives        
"""
noun_list = ResourcePool().special_nouns



def find_cap_lettre(word):
    """
    Function return 1 if the word starts with upper case letter                       
    Input=word               Output=flag(0 if no upper case or 1 if upper case)        
    """
    for i in cap_let_list:
        if word[0]==i:
            return 1
    return 0



def find_plus(word):
    """
    Function return 1 if the word containe '+'                       
    Input=word                                           Output=flag       
    """
    
    for i in word:
        if i=='+':
            return 1
    return 0



def list_rebuilding(string):
    """
    This function returns the list of strings without '+'                            
    Input=the string           Output=the list of strng corresponding                
    """

    for i in string:
        if i=='+':
            return [string[:string.index(i)]] + list_rebuilding(string[string.index(i)+1:])
    return [string]



def eliminate_redundancy(phrase):
    """
    This function to eliminate redundancy in the phrase                              
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
     This function returns concatenate token to have a string (sentence)
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
    """
    Function return 1 if the word is a plural                       
    Input=list of word             Output=flag(0 if singular or 1 if plural)       
    """
   
    if word.endswith('s'):
        for n in noun_end_s_sing:
            if n==word:
                return 0
        return 1
    if word=='we' or word=='I' or word=='you' or word=='they':
        return 1
        
    for k in plural_name:
        if word==k:
            return 1
        
    if quantifier=='SOME' or quantifier=='ALL':
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
    
    while i < len(sn):
        if sn[i]._conjunction!='AND':
            if plural(sn[i].noun[0], sn[i]._quantifier, sn[i].det)==1:
                return 1
        else:
            return 1
        i=i+1
        
    if sn[0].noun==[]:
        return 0
    else:
        return plural(sn[0].noun[0],sn[0]._quantifier, sn[0].det)
        
    return 0



def is_an_adj(word):
    """
    This function to know if a word is an adjective                                  
    Input=word                Output=1 if it is an adjective and 0 if not                     
    """
    
    #It is a noun so we have to return 1
    for j in noun_list:
        if word==j[0]:
            return 0
    
    #For the regular adjectives
    for k in adj_rules:
        if word.endswith(k):
            return 1
    
    #We use the irregular adjectives list to find it
    for i in adjective_list:
        if word==i:
            return 1
    
    return 0

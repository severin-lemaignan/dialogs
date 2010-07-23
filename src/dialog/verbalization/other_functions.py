
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
"""



"""
Statement of lists
"""
cap_let_list=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']



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
    
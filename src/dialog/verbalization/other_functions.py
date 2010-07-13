
"""
 Created by Chouayakh Mahdi                                                       
 07/07/2010                                                                       
 The package contains functions used by all other packages                        
 Functions:                                                                       
    list_recovery : to return the list of strings without '+'                     
    eliminate_redundancy : to eliminate redundancy in the phrase                  
    convert_string : to return concatenate token to have a string (sentence)      
"""



def list_recovery(string):
    """
    This function returns the list of strings without '+'                            
    Input=the string           Output=the list of strng corresponding                
    """

    for i in string:
        if i=='+':
            return [string[:string.index(i)]] + list_recovery(string[string.index(i)+1:])
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
    
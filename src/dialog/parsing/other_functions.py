#SVN:rev202

"""
 Created by Chouayakh Mahdi                                                       
 21/06/2010                                                                       
 The package contains functions used by all other packages                        
 Functions:                                                                       
    find_cap_lettre : to see if the word starts with capital letter               
    convert_to_string : to convert a list to string with '+' in place of ' '      
    recover_end_pos_sub : to find the end position of the subsentence             
"""


"""
Statement of lists
"""
cap_let_list=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']



def find_cap_lettre(word):
    """
    Function return 1 if the word starts with uppercase letter                       
    Input=word               Output=flag(0 if no uppercase or 1 if uppercase)        
    """
    for i in cap_let_list:
        if word[0]==i:
            return 1
    return 0



def convert_to_string(liste):
    """
    Function creates strings with '+' in place of ' '                                
    Input=list of string                      Output=string with + in place of ' '   
    """
    if liste==[]:
        return ''
    
    if len(liste)==1:
        return liste[0]
    else:
        return liste[0]+'+'+convert_to_string(liste[1:])



def recover_end_pos_sub(phrase, propo_sub_list):
    """
    Function to find the end position of the subsentence                             
    Input=sentence starts with relative proposal, the subsentence proposal's list    
    Output=end position of the subsentence                                          
    """
    
    #init
    nb_sub=0
    position=0

    #We loop after the first proposal
    for y in phrase:
        
        position=position+1
        for x in propo_sub_list:
            #If there is a proposal we increment nb_sub
            if y==x:
                nb_sub=nb_sub+1
                break
        
        #If there is a ';' we decrement nb_sub
        if y==';':
            nb_sub=nb_sub-1
            if nb_sub==0:
                #The of the processing is here, when there is no 'sub'
                return position
        
        if y=='.' or y=='!' or y=='?':
            return position

    #Default case
    return 0

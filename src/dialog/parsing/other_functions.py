#SVN:rev202

"""
 Created by Chouayakh Mahdi                                                       
 21/06/2010                                                                       
 The package contains functions used by all other packages                        
 Functions:                                                                       
    find_cap_lettre : to see if the word starts with capital letter               
    convert_to_string : to convert a list to string with '+' in place of ' '      
    recover_end_pos_sub : to find the end position of the subsentence             
    number : to return 1 if the word is a number and 2 if it is a adjectif-number 
"""
from dialog.resources_manager import ResourcePool


"""
Statement of lists
"""
frt_wd = ResourcePool().sentence_starts
number_list = ResourcePool().numbers
cap_let_list = ResourcePool().capital_letters



def find_cap_lettre(word):
    """
    Function return 1 if the word starts with upper case letter                       
    Input=word               Output=flag(0 if no upper case or 1 if upper case)        
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



def number(word):
    """
    Function return 1 if the word is a number and 2 if it is a adjective-number                    
    Input=word          Output=flag(0 if no number or 1 if number or 2 adjective-number)        
    """
    
    for n in number_list:
        if word.startswith(n[0]): 
            if word.endswith('th'):
                return 2
            else:
                return 1
    return 0



def word_to_digit(word):
    """
    Function convert the number from literal to digit                    
    Input=word                          Output=digit (string form)   
    """
    
    #init
    number=0
   
    for l in number_list:
        if word.startswith(l[0]):
            if word.endswith('teen'):
                number=number+l[1]+10
            elif word.endswith('ty') and word!='twenty':
                number=number+l[1]*10
            else:
                number=number+l[1]
    return number
            
            

def convert_to_digit(det):
    """
    Function convert the determinant to digit                    
    Input=word                          Output=digit (string form)   
    """
    
    #init
    num=k=0
        
    while k < len(det):
        if det[k]!='+':
            k=k+1
        else:
            
            num=num+word_to_digit(det[:k])
            det=det[k+1:]
            k=0 
                
    num=num+word_to_digit(det)
    return str(num)
                
                
                
def recover_aux_list():
    """
    This function recovers the auxiliary list                             
    Output=the auxiliary list          
    """
    
    aux_list=[]
    for x in frt_wd:
        if x[1]=='3':
            aux_list=aux_list+[x[0]]
    return aux_list

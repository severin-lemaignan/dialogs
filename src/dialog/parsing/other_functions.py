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
    word_to_digit : to convert the number from literal to digit
    convert_to_digit : to convert the determinant to digit  
    recover_aux_list : to recover the auxiliary list
    find_scd_verb_sub : to find 'to' of probably second verb and transform it into ':to'               
    recover_scd_verb_sub : to transform ':to' into 'to' if it isn't in subsentence of the subsentence
"""
from dialog.resources_manager import ResourcePool

"""
Statement of lists
"""
frt_wd = ResourcePool().sentence_starts
number_list = ResourcePool().numbers
cap_let_list = ResourcePool().capital_letters
superlative_number = ResourcePool().adjective_numbers_digit
sub_list = ResourcePool().subsentences
rel_list = ResourcePool().relatives

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
        if word.startswith(n[1]):
            return 1
        if word.startswith(n[0]): 
            if word.endswith('th'):
                return 2
            else:
                return 1
    return 0



def word_to_digit(word, number):
    """
    Function convert the number from literal to digit                    
    Input=word                          Output=digit (string form)   
    """
    
    for i in superlative_number:
        if i[0]==word:
            number=number+int(i[1])
    
    if word.endswith('th'):
        if word=='eighth':
            word=word[:len(word)-1]
        else:
            word=word[:len(word)-2]
    
    for l in number_list:
        if word.startswith(l[0]):
            if word.endswith('teen'):
                number=number+int(l[1])+10
            elif word.endswith('ty') and word!='twenty':
                number=number+int(l[1])*10
            elif l[0]=='hundred':
                number=number*int(l[1])
            elif l[0]=='thousand':   
                number=number*int(l[1])
            elif l[0]=='million':
                number=number*int(l[1])
            else:
                number=number+int(l[1])
              
    return number
            
            

def convert_to_digit(det):
    """
    Function convert the determinant to digit                    
    Input=word                          Output=digit (string form)   
    """
    
    #init
    num=k=0
    
    for n in number_list:
        if det.startswith(n[1]):
            return det
        
    while k < len(det):
        if det[k]!='+':
            k=k+1
        else:
            
            num=word_to_digit(det[:k], num)
            det=det[k+1:]
            k=0 
               
    num=word_to_digit(det, num)
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



def find_scd_verb_sub(sentence):
    """ 
    This function find 'to' of probably second verb and transform it into ':to'               
    Input=sentence                              Output=sentence                      
    """ 
    
    #init
    i=flag=0
    
    while i<len(sentence):
        
        for j in sub_list+rel_list:
            if sentence[i]==j:
                flag=flag+1
                break
        if sentence[i]==';':
            flag=flag-1
            
        if sentence[i]=='to' and flag>0:
            sentence[i]=':to'
            
        i=i+1
    return sentence



def recover_scd_verb_sub(sentence):
    """ 
    This function transform ':to' into 'to' if it isn't in subsentence of the subsentence                 
    Input=sentence                              Output=sentence                      
    """ 
    
    #init
    i=flag=0
    
    while i<len(sentence):
        
        for j in sub_list+rel_list:
            if sentence[i]==j:
                flag=flag+1
                break
        if sentence[i]==';':
            flag=flag-1
            
        if sentence[i]==':to' and flag==0:
            sentence[i]='to'
            
        i=i+1
        
    return sentence



def there_is_pronoun(list_nom_gr, nom_gr):
    flag=0
    for i in list_nom_gr:
        if flag==1 and (len(i)!=1 or find_cap_lettre(i[0])==1):
            return 1
        if len(i)==1 and find_cap_lettre(i[0])==0:
            flag=1
   
    if flag==1 and (len(i)!=1 or find_cap_lettre(nom_gr)==1):
        
        return 1
    
    return 0


"""
 Created by Chouayakh Mahdi                                                       
 06/07/2010                                                                       
 The package contains main functions of this module                               
 We return all elements of a nominal group                                        
 Functions:                                                                       
    dispatching : to dispatche the main class in corresponding function              
    adjective_pos : to return the position of the noun in the sentence             
    find_sn_pos : to return the nom_group in a given position with adjective_pos        
    find_nom_gr_list : to break phrase into nominal groups with 'of'
    create_possession_claus : to create phrase with 's
    possesion_form : to convert 'of' to possession form 's
    and_case : to convert 'and' to ',' if it is necessary
    replace_tuple : to replace some tuples
    negation : to replace not
    delete_plus : to delete '+' if there is
    delete_comma : to delete ',' if there is at the end of sentence 
    verbalising : is the basic function of this module
"""
from resources_manager import ResourcePool
import other_functions
import sentence_rebuilding


"""
Statement of lists
"""
pronoun_list=['you', 'I', 'we', 'he', 'she', 'me', 'it', 'he', 'they', 'yours', 'mine', 'him']
det_list=['the', 'a', 'an', 'your', 'his', 'my', 'this', 'her', 'their', 'these', 'that', 'every', 'there']
adj_rules=['al','ous','est','ing','y','less','ble','ed','ful','ish','ive','ic']
wques_rules=[('date',['when']),('place',['where']),('origin',['where']),('time',['what','time']),('color',['what','color']),('size',['what','size']),
             ('people',['who']),('age',['how', 'old']),('duration',['how', 'long']),('frequency',['how', 'often']),('distance',['how', 'far']),
             ('manner',['how']),('reason',['why']), ('object',['object'])]
insertion_tuples=[("'m", 'am'),("'ve", 'have'),("'re", 'are'),("'ll", 'will'),("'d", 'would'),("'s", 'is')]


"""
We have to read all irregular adjectives before the processing                    
"""
adjective_list = ResourcePool().adjectives.keys()


"""
We have to read all nouns which have a confusion with regular adjectives        
"""
noun_list = ResourcePool().special_nouns



def dispatching(analysis):
    """
    This function dispatches the main class in corresponding function                
    Input=class sentence                         Output=sentence (list of string)
    """

    #For statement
    if analysis.data_type=='statement':
        return sentence_rebuilding.statement(analysis)

    #For imperative
    elif analysis.data_type=='imperative':
        return sentence_rebuilding.imperative(analysis)

    #For yes no question
    elif analysis.data_type=='yes_no_question':
        return sentence_rebuilding.y_o_question(analysis)

    #For start
    elif analysis.data_type=='start':
        return ['hello','.']

    #For agree
    elif analysis.data_type=='agree':
        return ['OK','.']

    #For disagree
    elif analysis.data_type=='disagree':
        return ['no','.']

    #For w_question
    elif analysis.data_type=='w_question':
        for x in wques_rules:
            if x[0]==analysis.aim:
                return x[1]+sentence_rebuilding.y_o_question(analysis)

        if analysis.aim=='quantity':
            return sentence_rebuilding.quantity_ques(analysis)

        elif analysis.aim=='choice':
            return ['which']+sentence_rebuilding.statement(analysis)

        elif analysis.aim=='owner':
            return sentence_rebuilding.possession_ques(analysis)
        
        #All other cases of w_question
        else:
            return sentence_rebuilding.w_question(analysis)

    #Default case
    return ''



def adjective_pos(phrase, word_pos):
    """
    This function return the position of the end of the nominal group                
    We have to use the list of irregular adjectives                                  
    Input=the sentence (list of strings) and the position of the first adjective    
    Output=the position of the last word of the nominal group                       
    """

    #If it is the end of the phrase
    if len(phrase)-1==word_pos:
        return 1

    #It is a noun so we have to return 1
    for j in noun_list:
        if phrase[word_pos]==j[0]:
            return 1
    
    #For the regular adjectives
    for k in adj_rules:
        if phrase[word_pos].endswith(k):
            return 1+adjective_pos(phrase, word_pos+1)

    #We use the irregular adjectives list to find it
    for i in adjective_list:
        if phrase[word_pos]==i:
            adjective_pos(phrase, word_pos+1)
            return 1+ adjective_pos(phrase, word_pos+1)

    #Default case
    return 1



def find_sn_pos (phrase, begin_pos):
    """
    We will find the nominal group which is in a known position                      
    We have to use adjective_pos to return the end position of nominal group         
    Input=the sentence (list of strings) and the position of the nominal group       
    Output=the nominal group                                                         
    """

    end_pos = 1

    #If it is a pronoun
    for i in pronoun_list:
        if phrase[begin_pos]==i:
            return [phrase[begin_pos]]

    #If there is a nominal group with determinant
    for j in det_list:
        if phrase[begin_pos]==j:
            end_pos= end_pos + adjective_pos(phrase, begin_pos+1)
            return phrase[begin_pos : end_pos+begin_pos]

    #If it is a proper name
    counter=begin_pos
    while (counter<len(phrase) and other_functions.find_cap_lettre(phrase[counter])==1):
        counter=counter+1

    #Cases like 'next week'
    if phrase[begin_pos]=='next' or phrase[begin_pos]=='last':
        end_pos= end_pos + adjective_pos(phrase, begin_pos+1)
        return phrase[begin_pos-1 : end_pos+begin_pos]

    #Default case return [] => ok if counter=begin_pos
    return phrase[begin_pos : counter]



def find_nom_gr_list(phrase):
    """
    This function break phrase into nominal groups with 'of'                        
    And return also the elements number of the end of this list in the sentence       
    Input=sentence                    Output=list of nominal group                   
    """
   
    #init
    list=[]
    
    nom_gr=find_sn_pos(phrase, 0)
    nb_element=len(nom_gr)

    #We loop until there is no more nominal group
    while nom_gr!=[] and phrase[len(nom_gr)]=='of':

        list=[nom_gr]+list
        #We remove the nominal group
        phrase=phrase[len(nom_gr)+1:]
        
        #re-init phrase and nominal group
        nom_gr=find_sn_pos(phrase, 0)
        nb_element=nb_element+len(nom_gr)+1

    list=[nom_gr]+list

    #We put the elements number at the end of the list
    list=list+[nb_element]
    
    return list



def create_possession_claus(list):
    """
    This function create phrase with 's                                            
    Input=list of nominal group                 Output=phrase of nominal group       
    """
    
    #init
    i=1
    #To take the first element
    phrase=list[i-1]
    phrase[len(phrase)-1]=phrase[len(phrase)-1]+"'s"

    #We concatenate
    while i < len(list):
        
        if other_functions.find_cap_lettre(list[i][0])==1:
            phrase=phrase+list[i]
        else:
            phrase=phrase+list[i][1:]
            
        phrase[len(phrase)-1]=phrase[len(phrase)-1]+"'s"
        
        i=i+1
    
    #To remove the 's of the last word in the sentence
    word=phrase[len(phrase)-1]
    word=word[:len(word)-2]
    phrase[len(phrase)-1]=word
    return phrase



def possesion_form(sentence):
    """
    This function converts 'of' to possession form 's                                 
    Input=sentence                                     Output=sentence               
    """
    
    #init
    begin_pos=0
    flag=0
    
    while begin_pos < len(sentence):
        if sentence[begin_pos] == 'of' and sentence[begin_pos-1]!='think' and find_sn_pos(sentence, begin_pos+1)!=[]:
            #We have to find the first nominal group
            nom_gr=find_sn_pos(sentence, begin_pos)
            
            #In the case of a proper name
            while nom_gr!=[] and begin_pos!=0 and other_functions.find_cap_lettre(nom_gr[0])==1:
                begin_pos=begin_pos-1
            
                nom_gr=find_sn_pos(sentence, begin_pos)
                flag=1

            #If flag=1 => there is a proper name so we haven't decrement the begin_pos
            if flag==0:
                while nom_gr == []:
                    begin_pos=begin_pos-1
                    nom_gr=find_sn_pos(sentence, begin_pos)
            else:
                #If there is a proper name, begin_pos is wrong, we have to increment
                begin_pos=begin_pos+1
                flag=0
                
            #We recover the list of nominal groups
            nom_gr_list=find_nom_gr_list(sentence[begin_pos:])
            #We create the final phrase
            end_pos=nom_gr_list[len(nom_gr_list)-1]+begin_pos
            sentence=sentence[:begin_pos]+create_possession_claus(nom_gr_list[:len(nom_gr_list)-1])+sentence[end_pos:]

            #We continue processing from the end's position
            begin_pos=end_pos
            
        else:
            begin_pos=begin_pos+1

    return sentence



def and_case(sentence):
    """
    This function converts 'and' to ',' if it is necessary                                   
    Input=sentence                                     Output=sentence               
    """
    
    #init
    i=0
    
    while i < len(sentence):
        if sentence[i] == 'and':
            nom_gr=find_sn_pos(sentence, i+1)

            if len(sentence)>len(nom_gr)+i+1 and sentence[len(nom_gr)+i+1]=='and':
                sentence[i-1]=sentence[i-1]+','
                sentence=sentence[:i]+sentence[i+1:]
        i=i+1
        
    return sentence


def replace_tuple(sentence):
    """
    This function to replace some tuples                                   
    Input=sentence                                     Output=sentence               
    """
    
    #init
    i=0
    
    while i < len(sentence):
        
        #If there is a tuple
        for j in insertion_tuples:
            if sentence[i]==j[1]:
                
                #To perform this process we need to have a pronoun
                for k in pronoun_list:
                    if i!=0 and sentence[i-1]==k:
                        sentence[i-1]=sentence[i-1]+j[0]
                        sentence=sentence[:i]+sentence[i+1:]
                        break
        i=i+1
    
    return sentence            
    


def negation(sentence):
    """
    This function to replace not                                   
    Input=sentence                                     Output=sentence               
    """
    
    #init
    i=0
    
    while i < len(sentence):
        
        if sentence[i]=='not':
            if sentence[i-1]=='will':
                sentence[i-1]="won't"
            else:
                sentence[i-1]=sentence[i-1]+"n't"
                
            sentence=sentence[:i]+sentence[i+1:]
        i=i+1
    
    return sentence
    


def delete_plus(sentence):
    """
    This function to delete '+' if there is                                   
    Input=sentence                                     Output=sentence               
    """
    
    #init
    i=0
    
    while i < len(sentence):
        if other_functions.find_plus(sentence[i])==1:
            sentence=sentence[:i]+other_functions.list_rebuilding(sentence[i])+sentence[i+1:]
    
        i=i+1
    return sentence



def delete_comma(sentence):
    """
    This function to delete ',' if there is at the end of sentence                                   
    Input=sentence                                     Output=sentence               
    """
    
    word = sentence[len(sentence)-2]
    if word[len(word)-1]==',':
        word=word[:len(word)-1]
        sentence[len(sentence)-2]=word
    
    return sentence
                
                 
        
def verbalising(class_list):
    """
    This function is the basic function of this module                               
    Input=class sentence                                       Output=sentence       
    """

    utterance=''

    #converting all classes sentence
    for i in class_list:
        sentence = dispatching(i)
        
        #To perform some changes to have an usual sentence at the end
        sentence=possesion_form(sentence)
        sentence=and_case(sentence)
        sentence=negation(sentence)
        sentence=replace_tuple(sentence)
        sentence=delete_plus(sentence)
        sentence=delete_comma(sentence)
        
        #To have the upper case and convert the list to string
        sentence[0]=sentence[0][0].upper()+sentence[0][1:]
        sentence= other_functions.convert_string(sentence)
        
        #To concatenate the last punctuation to the last word of the sentence
        sentence=sentence[:len(sentence)-2]+sentence[len(sentence)-1]
        
        #To separate with other sentences
        sentence= sentence+' '
        
        utterance=utterance+sentence
    
    #To remove the last escape (at the end)
    return utterance[:len(utterance)-1]

"""
 Created by Chouayakh Mahdi                                                       
 06/07/2010                                                                       
 The package contains main functions of this module                               
 We return all elements of a nominal group                                        
 Functions:                                                                       
    dispatching : to dispatche the main class in corresponding function           
    verbalising : is the basic function of this module                            
"""
import other_functions
import sentence_recovery



def dispatching(analysis):
    """
    This function dispatches the main class in corresponding function                
    Input=class sentence                         Output=sentence (list of string)
    """

    #For statement
    if analysis.data_type=='statement':
        return sentence_recovery.statement(analysis)

    #For imperative
    elif analysis.data_type=='imperative':
        return sentence_recovery.imperative(analysis)

    #For yes no question
    elif analysis.data_type=='yes_no_question':
        return sentence_recovery.y_o_question(analysis)

    #For start
    elif analysis.data_type=='start':
        return ['hello']

    #For agree
    elif analysis.data_type=='agree':
        return ['OK']

    #For disagree
    elif analysis.data_type=='disagree':
        return ['no']

    #For w_question
    elif analysis.data_type=='w_question':

        if analysis.aim=='date':
            return ['when']+sentence_recovery.y_o_question(analysis)

        elif analysis.aim=='place':
            return ['where']+sentence_recovery.y_o_question(analysis)

        elif analysis.aim=='origin':
            return ['where']+sentence_recovery.y_o_question(analysis)

        elif analysis.aim=='time':
            return ['what','time']+sentence_recovery.y_o_question(analysis)

        elif analysis.aim=='color':
            return ['what','color']+sentence_recovery.y_o_question(analysis)

        elif analysis.aim=='size':
            return ['what','size']+sentence_recovery.y_o_question(analysis)

        elif analysis.aim=='people':
            return ['who']+sentence_recovery.y_o_question(analysis)

        elif analysis.aim=='age':
            return ['how', 'old']+sentence_recovery.y_o_question(analysis)

        elif analysis.aim=='duration':
            return ['how', 'long']+sentence_recovery.y_o_question(analysis)

        elif analysis.aim=='frequency':
            return ['how', 'often']+sentence_recovery.y_o_question(analysis)

        elif analysis.aim=='distance':
            return ['how', 'far']+sentence_recovery.y_o_question(analysis)

        elif analysis.aim=='manner':
            return ['how']+sentence_recovery.y_o_question(analysis)

        elif analysis.aim=='reason':
            return ['why']+sentence_recovery.y_o_question(analysis)
        
        elif analysis.aim=='quantity':
            return sentence_recovery.quantity_ques(analysis)

        elif analysis.aim=='choice':
            return ['which']+sentence_recovery.statement(analysis)

        elif analysis.aim=='owner':
            return sentence_recovery.possession_ques(analysis)
        
        #All other cases of w_question
        else:
            return sentence_recovery.w_question(analysis)

    #Default case
    return ''



def verbalising(class_list):
    """
    This function is the basic function of this module                               
    Input=class sentence                                       Output=sentence       
    """

    utterance=''

    #converting all classes sentence
    for i in class_list:
        sentence = dispatching(i)
        
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

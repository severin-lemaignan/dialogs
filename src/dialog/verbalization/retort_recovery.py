
"""
######################################################################################
## Created by Chouayakh Mahdi                                                       ##
## 06/07/2010                                                                       ##
## The package contains main functions of this module                               ##
## We return all elements of a nominal group                                        ##
## Functions:                                                                       ##
##    dispatching : to dispatche the main class in corresponding function           ##
##    verbalising : is the basic function of this module                            ##
######################################################################################
"""
import other_functions
import sentence_recovery


"""
######################################################################################
## This function dispatches the main class in corresponding function                ##
## Input=class sentence                                       Output=sentence       ##
######################################################################################
"""
def dispatching(analysis):

    #For statement
    if analysis.data_type=='statement':
        return other_functions.convert_string(sentence_recovery.statement(analysis))

    #For imperative
    elif analysis.data_type=='imperative':
        return other_functions.convert_string(sentence_recovery.imperative(analysis))

    #For yes no question
    elif analysis.data_type=='yes_no_question':
        return other_functions.convert_string(sentence_recovery.y_o_question(analysis))

    #For start
    elif analysis.data_type=='start':
        return 'hello'

    #For agree
    elif analysis.data_type=='agree':
        return 'ok'

    #For disagree
    elif analysis.data_type=='disagree':
        return 'no'

    #For w_question
    elif analysis.data_type=='w_question':

        if analysis.aim=='date':
            return other_functions.convert_string(['when']+sentence_recovery.y_o_question(analysis))

        elif analysis.aim=='place':
            return other_functions.convert_string(['where']+sentence_recovery.y_o_question(analysis))

        elif analysis.aim=='origine':
            return other_functions.convert_string(['where']+sentence_recovery.y_o_question(analysis)+['from'])

        elif analysis.aim=='time':
            return other_functions.convert_string(['what','time']+sentence_recovery.y_o_question(analysis))

        elif analysis.aim=='color':
            return other_functions.convert_string(['what','color']+sentence_recovery.y_o_question(analysis))

        elif analysis.aim=='size':
            return other_functions.convert_string(['what','size']+sentence_recovery.y_o_question(analysis))

        elif analysis.aim=='people':
            return other_functions.convert_string(['who']+sentence_recovery.y_o_question(analysis))

        elif analysis.aim=='age':
            return other_functions.convert_string(['how', 'old']+sentence_recovery.y_o_question(analysis))

        elif analysis.aim=='duration':
            return other_functions.convert_string(['how', 'long']+sentence_recovery.y_o_question(analysis))

        elif analysis.aim=='frequency':
            return other_functions.convert_string(['how', 'often']+sentence_recovery.y_o_question(analysis))

        elif analysis.aim=='distance':
            return other_functions.convert_string(['how', 'far']+sentence_recovery.y_o_question(analysis))

        elif analysis.aim=='manner' or analysis.aim=='opinion':
            return other_functions.convert_string(['how']+sentence_recovery.y_o_question(analysis))

        elif analysis.aim=='reason':
            return other_functions.convert_string(['why']+sentence_recovery.y_o_question(analysis))
        
        elif analysis.aim=='quantity':
            return other_functions.convert_string(sentence_recovery.quantity_ques(analysis))

        elif analysis.aim=='choice':
            return other_functions.convert_string(sentence_recovery.choice_ques(analysis))

        elif analysis.aim=='possession':
            return other_functions.convert_string(sentence_recovery.possession_ques(analysis))
        
        #All other cases of w_question
        else:
            return other_functions.convert_string(['what']+sentence_recovery.w_question(analysis))

    #Default case
    return ''


"""
######################################################################################
## This function is the basic function of this module                               ##
## Input=class sentence                                       Output=sentence       ##
######################################################################################
"""
def verbalising(class_list):

    retort=''

    #converting all classes sentence
    for i in class_list:
        retort=retort+dispatching(i)
        
    return retort

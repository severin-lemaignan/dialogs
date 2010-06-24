#!/usr/bin/python
# -*- coding: utf-8 -*-
# SVN:rev202 + PythonTidy

"""
cette fonction nous permet de traiter une phrase recuperee sous forme
de liste de chaine de caracteres et de retourner une liste de class
contenant les information necessaire pour interroger le serveur

v.0.2: 21:frt_wd from ResourcePool
"""

from resources_manager import ResourcePool

import analyse_grammaire
import recuperer_phrase
import recherche_mot

# fonction pour recuperer la classe grammaire
list_cap_let=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def analysis_phrase(phrase):
    frt_wd = ResourcePool().sentence_starts
    
    if phrase:
        if recuperer_phrase.amorcer(phrase):
            #if len(recuperer_phrase.amorcer(phrase)) != len(phrase):
            #    phrase = phrase[len(recuperer_phrase.amorcer(phrase)):]
            #    return [analyse_grammaire.phr_amorce()] \
            #        + analyse_phr(phrase, frt_wd)
            #else:
            return analyse_grammaire.phr_amorce()

    if len(phrase) != 1 and phrase[len(phrase) - 1] == '!':
        return analyse_grammaire.interjection('interjection')

    if recuperer_phrase.repondre(phrase) != '':
        #if len(phrase) > 2:
        #    return [analyse_grammaire.phr_agr_disa(recuperer_phrase.repondre(phrase))] \
        #        + analyse_phr(phrase[2:], frt_wd)
        #else:
        return analyse_grammaire.phr_agr_disa(recuperer_phrase.repondre(phrase))

    if len(phrase) > 1:
        for x in frt_wd:
            if phrase[0] == x[0]:

        # il s'agit d'une w_qestion

                if x[1] == '1':

          # les when question

                    if x[2] == '1':
                        return analyse_grammaire.w_quest_standar('w_question'
                                , 'date', phrase, 2)
                    elif x[2] == '2':

          # les where question

                        return analyse_grammaire.w_quest_where('w_question'
                                , 'place', phrase, 2)
                    elif x[2] == '3':

          # les what question

            # dans le cas ou le what est directement lie a un objet ou demande

                        if phrase[1] == 'time':
                            return analyse_grammaire.w_quest_standar('w_question'
                                    , 'time', phrase, 3)
                        elif phrase[1] == 'color':
                            return analyse_grammaire.w_quest_standar('w_question'
                                    , 'color', phrase, 3)
                        elif phrase[1] == 'size':
                            return analyse_grammaire.w_quest_standar('w_question'
                                    , 'size', phrase, 3)
                        elif phrase[1] == 'happened' or phrase[2] \
                            == 'be' and phrase[3] == 'happened':

            # sinon on utilise un traitement different

                            return analyse_grammaire.w_quest_happened('w_question'
                                    , 'situation', phrase)
                        elif len(phrase) > 4 and (phrase[3] == 'matter'
                                or phrase[2] == 'wrong' or phrase[3]
                                == 'wrong' and (phrase[2] == 'not'
                                or phrase[2] == 'be') or phrase[4]
                                == 'wrong' and phrase[2] == 'not'
                                and phrase[3] == 'be'):
                            return analyse_grammaire.w_quest_prob('w_question'
                                    , 'problem', phrase)
                        elif phrase[1] == 'type' or phrase[1] == 'kind':
                            return analyse_grammaire.w_quest_class('w_question'
                                    , 'classification', phrase, frt_wd,
                                    3)
                        else:
                            return analyse_grammaire.w_quest_what('w_question'
                                    , phrase, 2)
                    elif x[2] == '4':

          # les how question

                        if phrase[1] == 'old':
                            return analyse_grammaire.w_quest_standar('w_question'
                                    , 'age', phrase, 3)
                        elif phrase[1] == 'long':
                            return analyse_grammaire.w_quest_standar('w_question'
                                    , 'duration', phrase, 3)
                        elif phrase[1] == 'often':
                            return analyse_grammaire.w_quest_standar('w_question'
                                    , 'frequency', phrase, 3)
                        elif phrase[1] == 'many' or phrase[1] == 'much':
                            return analyse_grammaire.w_quest_quant('w_question'
                                    , 'quantity', phrase, frt_wd)
                        elif phrase[1] == 'far':
                            return analyse_grammaire.w_quest_standar('w_question'
                                    , 'distance', phrase, 3)
                        elif phrase[1] == 'soon':
                            return analyse_grammaire.w_quest_standar('w_question'
                                    , 'time', phrase, 3)
                        elif phrase[1] == 'about':
                            return analyse_grammaire.w_how_invit('w_question'
                                    , 'invitation', phrase)
                        else:
                            return analyse_grammaire.w_quest_how('w_question'
                                    , phrase)
                    elif x[2] == '5':

          # les why question

                        return [analyse_grammaire.w_quest_standar('w_question'
                                , 'purpose', phrase, 2)]
                    elif x[2] == '6':

          # les whose question

                        return analyse_grammaire.w_quest_whose('w_question'
                                , 'possession', phrase)
                    elif x[2] == '7':

          # les who question

                        return analyse_grammaire.w_quest_standar('w_question'
                                , 'people', phrase, 2)
                    elif x[2] == '8':

          # les which question

                        return analyse_grammaire.w_quest_which('w_question', 'choice', phrase)
                elif x[1] == '2':

        # il s'agit d'une yes_no_question

                    return analyse_grammaire.y_n_ques('yes_no_question', '', phrase, 1)
                elif x[1] == '3':

                    return analyse_grammaire.phrase_condi(phrase[1:])
                elif x[1] == '4':

                    return [analyse_grammaire.thank()]

    # il s'agit de statement ou phrase imperative

        return analyse_grammaire.autre_type_phrase(phrase, '', '')
    return None


def upper_to_lower(sentence):

    frt_wd = ResourcePool().sentence_starts
    for j in list_cap_let:
	if sentence[0][0]==j:
    		#We convert uppercase to lowercase if it is not 'I'
    		if sentence[0]=='I':
        		return sentence
    		else:
        		sentence[0]=sentence[0][0].lower()+sentence[0][1:]

	    	#If we find the word in the Beginning_sentence list
	    	for v in frt_wd:
			if sentence[0]==v[0]:
			    	return sentence

   	    	#If there is a nominal group
	    	if recherche_mot.rech_sujet (sentence, 0)!=[]:
			return sentence

		#It a propre name, we convert lowercase to uppercase
	    	sentence[0]=sentence[0][0].upper()+sentence[0][1:]
	    	return sentence


def split_reply(reply):

    word=''
    reply_splited=[]

    for i in reply:
        #Creation of the word
        if i!=' ':
            word=word+i
        #Concatenation of the word in the list
        else:
            reply_splited=reply_splited+[word]
            word=''

    #For the last word
    reply_splited=reply_splited+[word]
    return reply_splited


def analyse_phr(reply):
    sentence=[]
    for j in reply:
        if j.endswith('.') or j.endswith('?') or j.endswith('!'):
            sentence=sentence+[j[:len(j)-1]] + [j[len(j)-1]]
            upper_to_lower(sentence)
	    return analysis_phrase(sentence)
            #phrase=trait_penctu(phrase, frt_wd)
            #class_replique
            sentence=[]

        #If user put space between the last word and the punctuation
        elif j=='.' or j=='?' or j=='!':
            upper_to_lower(sentence)
            return analysis_phrase(sentence)
            #phrase=trait_penctu(phrase, frt_wd)
            #class_replique
            sentence=[]

        else:
            sentence=sentence+[j]

    #If the user forget the punctuation at the end
    if sentence!=[]:
        upper_to_lower(sentence)
        return analysis_phrase(sentence)


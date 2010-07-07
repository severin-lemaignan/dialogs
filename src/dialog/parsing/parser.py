#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
######################################################################################
## Created by Chouayakh Mahdi                                                       ##
## 06/07/2010                                                                       ##
## The package contains functions to perform test                                   ##
## It is more used for the subject                                                  ##
## Functions:                                                                       ##
##    compare_nom_gr : to compare 2 nominal groups                                  ##
##    compare_icompl : to compare 2 indirect complements                            ##
##    compare_vs : to compare 2 verbal structures                                   ##
##    compare_sentence : to compare 2 sentences                                     ##
##    compare_reply : to compare 2 replies                                          ##
##    display_ng : to display nominal group                                         ##
##    display : to display class Sentence                                           ##
##    unit_tests : to perform unit tests                                            ##
######################################################################################
"""
from sentence import Sentence
import logging
import preprocessing
import analyse_sentence

class Parser:
    def __init__(self):
        pass
    
    def parse(self, nl_input, active_sentence = None):
        
        #Do all basic replacements (like capitals, n't -> not, etc) + splits in several 
        #sentence with points.
        self._sentence_list = preprocessing.treat_sentence(nl_input)
        
        #Do the actual grammatical parsing
        self._class_list = analyse_sentence.sentences_analyzer(self._sentence_list)
        
        for s in self._class_list:
        
            logging.debug("Parsing output:\n" + str(s))
        
        return self._class_list
             
              
"""
######################################################################################
## Function to compare 2 nominal groups                                             ##
######################################################################################
"""
def compare_nom_gr(ng,rslt_ng):

    #init
    i=0
    j=0

    if len(ng)!=len(rslt_ng):
        return 1
    else:
        while i < len(rslt_ng):
            if rslt_ng[i].det!=ng[i].det or rslt_ng[i].adj!=ng[i].adj or rslt_ng[i].noun!=ng[i].noun:
                return 1
            
            #We compare the noun complement
            if compare_nom_gr(rslt_ng[i].noun_cmpl, ng[i].noun_cmpl)==1:
                return 1
            
            #We compare the relative
            if len(rslt_ng[i].relative)!= len(ng[i].relative):
                return 1
            else:
                while j < len(rslt_ng[i].relative):
                    if compare_sentence(rslt_ng[i].relative[j], ng[i].relative[j])==1:
                        return 1
                    j=j+1
            
            #We compare the flag (if there is an 'or' or an 'and')
            if rslt_ng[i]._and_or!=ng[i]._and_or:
                return 1
            i=i+1
        return 0
    
    
"""
######################################################################################
## Function to compare 2 indirect complements                                       ##
######################################################################################
"""    
def compare_icompl(icompl, rslt_icompl):

    #init
    i=0

    if len(icompl)!=len(rslt_icompl):
        return 1
    else:
        while i < len(rslt_icompl):
            if rslt_icompl[i].prep!=icompl[i].prep:
                return 1
            if compare_nom_gr(rslt_icompl[i].nominal_group,icompl[i].nominal_group) ==1:
                return 1
            i=i+1
        return 0


"""
######################################################################################
## Function to compare 2 verbal structures                                          ##
######################################################################################
""" 
def compare_vs(vs, rslt_vs):
    #init
    i=0
    j=0

    if len(vs)!=len(rslt_vs):
        return 1
    else:
        while i < len(rslt_vs):
            if vs[i].vrb_main!=rslt_vs[i].vrb_main or vs[i].vrb_tense!=rslt_vs[i].vrb_tense or vs[i].state!=rslt_vs[i].state:
                return 1
            if vs[i].advrb!=rslt_vs[i].advrb or vs[i].vrb_adv!=rslt_vs[i].vrb_adv:
                return 1
            
            #We compare the d_obj
            if compare_nom_gr(vs[i].d_obj,rslt_vs[i].d_obj)==1:
                return 1
            
            #We compare the i_cmpl
            if compare_icompl(vs[i].i_cmpl, rslt_vs[i].i_cmpl):
                return 1
            if compare_vs(vs[i].sv_sec, rslt_vs[i].sv_sec):
                return 1
            
            #We compare the vrb_sub_sentence
            if len(rslt_vs[i].vrb_sub_sentence)!= len(vs[i].vrb_sub_sentence):
                return 1
            else:
                while j < len(rslt_vs[i].vrb_sub_sentence):
                    if compare_sentence(vs[i].vrb_sub_sentence[j], rslt_vs[i].vrb_sub_sentence[j])==1:
                        return 1
                    j=j+1
            
            i=i+1
        return 0
    
    
"""
######################################################################################
## Function to compare 2 sentences                                                  ##
######################################################################################
"""     
def compare_sentence(stc, stc_rslt):
    if stc.data_type!=stc_rslt.data_type or stc.aim!=stc_rslt.aim:
        return 1
    if compare_nom_gr(stc.sn,stc_rslt.sn)==1:
        return 1
    if compare_vs(stc.sv, stc_rslt.sv)==1:
        return 1

    return 0


"""
######################################################################################
## Function to compare 2 replies                                                    ##
######################################################################################
""" 
def compare_reply(reply, rslt_reply, sentence_list):

    #init
    i=0

    if len(reply)!=len(rslt_reply):
        print 'There is a problem with the analyse reply : length(reply)!=length(result)'
    else:
        while i < len(rslt_reply):
            
            print "The sentence after the analyse reply is :"
            print sentence_list[i]
            
            display(reply[i])
            
            flag=compare_sentence(reply[i], rslt_reply[i])
            if flag==1:
                print "There is a problem with parsing this sentence"
            elif flag==0:
                print "############### Parsing is OK ###############"
            
            i=i+1
        
       
"""
######################################################################################
## Function to display nominal group                                                ##
######################################################################################
"""
def display_ng(nom_str):
    print  nom_str.det,   nom_str.adj,  nom_str.noun
    for i in nom_str.noun_cmpl:
        display_ng(i)

    for j in nom_str.relative:
        display ([j])
        print ''


"""
######################################################################################
## Function to display class Sentence                                               ##
######################################################################################
"""
def display(a):
    print ''
    print a.data_type,a.aim
    print ''

    for i in a.sn:
        print "subject:"
        display_ng(i)
        print ''

    for b in a.sv:
        print 'verb:'
        print b.state
        print b.vrb_adv
        print b.vrb_main, b.vrb_tense
        print ''
        for x in b.d_obj:
            print 'direct complement:'
            display_ng(x)
            print ''

        for j in b.i_cmpl:
            print 'indirect complement:'
            print j.prep
            for k in j.nominal_group:
                display_ng(k)
            print ''

        if b.advrb!=[]:
            print 'adverb of the sentence:'
            print b.advrb
            print ''

        for m in b.sv_sec:
            print 'the second verb:'
            print m.state
            print m.vrb_main
            if m.d_obj!=[]:
                    
                for x in m.d_obj:
                    print 'direct complement:'
                    display_ng(x)
                    print ''

                for j in m.i_cmpl:
                    print 'indirect complement:'
                    print j.prep
                    for y in j.nominal_group:
                        display_ng(y)
                    print ''

                if m.advrb!=[]:
                    print 'adverb of the sentence:'
                    print m.advrb
                    print ''

    for z in b.vrb_sub_sentence:
        print 'the content of subsentence:'
        display(z)

   
"""
######################################################################################
## Function to perform unit tests                                                   ##
######################################################################################
""" 
def unit_tests():
    
    """
    Aim of this test : To use different cases with a state's verb 
    """
    print ''
    print ('######################## test 1 ##############################')

    reply="The bottle is on the table. The bottle is blue. the bottle is Blue"
    print 'The object of our test is this reply :'
    print reply
    print '###############################################################'
    print ''
    sentence_list=analyse_reply.treat_sentence(reply,frt_wd)
    class_list= analyse_sentence.sentences_analyzer(sentence_list, frt_wd)
    rslt=[Sentence('statement', '',
            [Nominal_Group(['the'],['bottle'],[],[],[])],
            [Verbal_Group(['be'], [],'present simple',
                [],
                [Indirect_Complement(['on'],[Nominal_Group(['the'],['table'],[],[],[])])],
                [], [] ,'affirmative',[])]),
        Sentence('statement', '',
            [Nominal_Group(['the'],['bottle'],['blue'],[],[])],
        [Verbal_Group(['be'], [],'present simple',
            [], 
            [],
            [], [] ,'affirmative',[])]),
        Sentence('statement', '',
        [Nominal_Group(['the'],['bottle'],[],[],[])],
        [Verbal_Group(['be'], [],'present simple',
            [Nominal_Group([],['Blue'],[],[],[])],
            [],
            [], [] ,'affirmative',[])])]
    compare_reply(class_list,rslt,sentence_list)
    print ''
    
    
    



"""
############################## Testing ##################################
"""
reply1="Jido's blue bottle is on the table. I'll play a guitar, a piano and a violon."
reply2="It's on the table. I give it to you. Give me the bottle. I don't give the bottle to you."
reply3="you aren't preparing the car and my father's moto at the same time. is the bottle of my brother in your right?"
reply4="You shouldn't drive his poorest uncle's wife's big new car. Should I give you the bottle? shall I go"
reply5="Isn't he doing his homework and his game now? Cann't he take this bottle. good afternoon"
reply6="Don't quickly give me the blue bottle. I wanna play with my guitar. I'd like to go to the cinema. "
reply7="the man which talks ; has a new car. I play the guitar which I bought yesterday ; . "
reply8="The bottle which I bought from the store which is in the shopping centre ; ; is yours."
reply9="don't quickly give me the bottle which is on the table ; and the glass which I cleaned yesterday ; at my left"
reply10="When won't the planning session take place? when must you take the bus"
reply11="Where is Broyen ? where are you going. Where must Jido and you be from?"
reply12="What time is the news on TV? What size do you wear? the code is written by me. Mahdi is gonna to the Laas?"
reply13="what is the weather like in the winter here? what were you doing? What isn't Jido going to do tomorrow"
reply14="What's happening. What must happen in the company today? What didn't happen here. no. Sorry."
reply15="What is the bigest bottle's color on your left. What does your brother do for a living?"
reply16="What type of people don't read this magazine? what kind of music must he listen to everyday"
reply17="What kind of sport is your favourite? what is the problem with him? what is the matter with this person"
reply18="How old are you? how long is your uncle's store opened tonight? how long is your uncle's store open tonight?"
reply19="how far is it from the hotel to the restaurant? how soon can you be here? How often does Jido go skiing?"
reply20="how much water should they transport? how many guests weren't at the party? how much does the motocycle cost"
reply21="How about going to the cinema? how have not they gotten a loan for their business? OK"
reply22="How did you like Steven Spilburg's new movie. how could I get to the restaurant from here"
reply23="Why should she go to Toulouse? who could you talk to on the phone. Whose blue bottle and red glass are these."
reply24="What are you thinking about the idea which I present you ; ? what color is the bottle which you bought ;"
reply25="Which competition's salesperson won the award which we won in the last years ;."
reply26="what'll your house look like? what do you think of the latest novel which Jido wrote ;"
reply27="Learn that I want you to give me the blue bottle ;. If you do your job ; you will be happy."

  

    


if __name__ == '__main__':
    unit_tests()

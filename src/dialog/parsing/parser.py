#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
######################################################################################
## Created by Chouayakh Mahdi                                                       ##
## 06/07/2010                                                                       ##
## The package contains functions to perform test                                   ##
## It is more used for the subject                                                  ##
## Functions:                                                                       ##
##    display_ng : to display nominal group                                         ##
##    display : to display class Sentence                                           ##
######################################################################################
"""
import logging

import analyse_reply
import analyse_sentence

class Parser:
    def __init__(self):
        pass
    
    def parse(self, nl_input, active_sentence = None):
        
        self._sentence_list = analyse_reply.treat_sentence(nl_input)
        
        #self._class_list = analyse_sentence.sentences_analyzer(self._sentence_list)
     
        #logging.debug("Parsing output:\n" + str(sentence))
        
        #return [self._class_list]
              
    
"""
######################################################################################
## Function to display nominal group                                                ##
######################################################################################
"""
def display_ng(nom_str):
    
    print  nom_str.det, nom_str.adj, nom_str.noun
    if  nom_str.noun_cmpl!=[]:
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
def display(liste):
    for a in liste:
        print a.data_type,a.aim
        if a.sn!=[]:
            print ''
            print 'le sujet'
            for i in a.sn:
                display_ng(i)
                print ''
        print ''
        for b in a.sv:
            print 'verbe'
            print b.state
            print b.vrb_adv
            print b.vrb_main, b.vrb_tense
            print ''
            for x in b.d_obj:
                print 'COD'
                display_ng(x)
                print ''
            if b.i_cmpl!=[]:
                print ''
                print 'les complement circons ou COI'
                for j in b.i_cmpl:
                    print '**'
                    print j.prep
                    for k in j.nominal_group:
                        display_ng(k)
            print ''
            if b.advrb!=[]:
                print 'adverbe de la phrase'
                print b.advrb
            for m in b.sv_sec:
                print ''
                print 'le verbe secondaire (non conjugues)'
                print m.state
                print m.vrb_main
                if m.d_obj!=[]:
                    print ''
                    for x in m.d_obj:
                        print 'COD'
                        display_ng(x)
                        print ''
                if m.i_cmpl!=[]:
                    print ''
                    print 'les complement circons ou COI'
                    for j in m.i_cmpl:
                        print '**'
                        print j.prep
                        for y in j.nominal_group:
                            display_ng(y)
                print ''
                if m.advrb!=[]:
                    print 'adverbe de la phrase'
                    print m.advrb
            if b.vrb_sub_sentence!=[]:
                display(b.vrb_sub_sentence)
    
    
"""
######################################################################################
## Function to perform unit tests                                                   ##
######################################################################################
""" 
def unit_tests():
    reply0="Don't quickly give me the blue bottle. Jido's blue bottle is on the table."
    sentence_list=analyse_reply.treat_sentence(reply0)
    class_list= analyse_sentence.sentences_analyzer(sentence_list)
    display (class_list)


"""
############################## Testing ##################################
"""

reply1="I'll play a guitar, a piano and a violon. Put the bottle! It's on the table"
reply2="I don't give the bottle to you . Is he doing his homework and his game now ?"
reply3="did you play your game yesterday? is not the blue bottle of my brother in your right?"
reply4="you aren't preparing the car and my father's moto at the same time. Should I give you the bottle?"
reply5="You shouldn't drive his poorest uncle's wife's big new car. Cann't he take this bottle"
reply6="I wanna play with my guitar. I'd like to go to the cinema. shall I go"
reply7="When won't the planning session take place? when must you take the bus"
reply8="Where is Broyen ? where are you going. Where must Jido and you be from?"
reply9="What time is the news of Peter on TV? What size do you wear? the code is written by me ."
reply10="what is the weather like in the winter here? what were you doing? What isn't Jido going to do tomorrow"
reply11="What must happen in the company today? What's happening. What didn't happen here"
reply12="What is the bigest bottle's color on your left. What does your brother do for a living?"
reply13="What type of people don't read this magazine and this newspaper? what kind of music must he listen to everyday"
reply14="What kind of sport is your favourite? How old are you? how long is your uncle's store opened tonight ?"
reply15="How often does Jido go skiing? how far is it from the hotel to the restaurant? how soon can you be here"
reply16="How about going to the cinema? how have not they gotten a loan for their business?"
reply17="How did you like Steven Spilburg's new movie. how could I get to the restaurant from here"
reply18="how much water should they transport? how many guests weren't at the party? how much does the motocycle cost"
reply19="Why should she go to Toulouse? who could you talk to on the phone."
reply20="The blue bottle which I bought last week ; and the green glass that is mine ; are on Jido's table. OK"
reply21="I play the guitar that I bought yesterday ; . no. Sorry!"
reply22="The bottle which I bought from the store that is in the shopping centre ; ; is yours. "
reply23="the man that talks ; has a new car. Mahdi is gonna to the Laas ? what color is the bottle which you bought ;"
reply24="don't quickly give me the bottle that is on the table ; and the glass that I cleaned yesterday ; at my left"
reply25="Learn that I want you to give me the blue bottle which is blue ; and the green one ; . I'm in the Laas."
reply26="It's Jido's red bottle which I won't put on my pretty sister's side ;. if you do your job ; you will be happy."
reply27="Whose blue bottle and red glass are these. What are you thinking about the idea which I present you ; ?"
reply28="Which competition's salesperson won the award which we won in the last years ; . good afternoon"
reply29="how long is your uncle's store open tonight? what is the matter with this generous person"
reply30="what'll your house which you've to build ; look like? what do you think of the latest novel which Jido wrote ;"
reply31="what is the problem with him? The bottle is blue. The bottle is Blue"

  

    


if __name__ == '__main__':
    unit_tests()

#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module implements ...

"""

import logging

import analyse_phrase
import recherche_mot

class Parser:
    def __init__(self):
        pass
    
    def parse(self, nl_input, active_sentence = None):
        sentence = analyse_phrase.analyse_phr(nl_input)
        
        logging.debug("Parsing output:\n" + str(sentence))
        
        return [sentence]
    
        
    def concatener (self,phrase1, phrase2, phrase3):
        phrase=[]
        i=0
        if phrase3[0:2]==['I',"don't",'know']:
            return phrase2
        elif len(phrase2)!=0:
            if phrase2[len(phrase2)-1]== 'one':
                gr_mom=recherche_mot.rech_SN(phrase3)
                word=gr_mom[len(gr_mom)-1]
                phrase2[len(phrase2)-1]=word[:len(word)-1]
            while i<len(phrase1):
                if phrase1[i] == phrase2[0]:
                    if phrase2[len(phrase2)-1]==phrase1[i+1]:
                        phrase=phrase+phrase2+phrase1[i+2:]
                        break
                phrase=phrase+[phrase1[i]]
                i=i+1
            
            return phrase
        else:
            return phrase1
            
    
    
    
def unit_tests():
    """This function tests the main features of the class Parser
    
    Extracted from SVN:rev202:testParser.py
    """
    
    replique = ['he is playing on the piano']
    parser = Parser()
    
    def print_gn(sn):
        print   sn.det, sn.adj, sn.noun, sn.relative
        if  sn.noun_cmpl != None:
            print_gn(sn.noun_cmpl)

    print("Parsing \"" + "+".join(replique) + "\"")
    liste = parser.parse(replique)
    
    print(str(liste))
    
    for a in liste:
        print a.data_type, a.aim
        if a.sn is not None:
            print ''
            print 'le sujet'
            print_gn(a.sn)
        print ''
        if a.sv is not None:
            print 'verbe'
            print a.sv.vrb_adv
            print a.sv.vrb_main, a.sv.vrb_tense
            if a.sv.d_obj != None:
                print ''
                print 'COD'
                print_gn(a.sv.d_obj)
            if a.sv.i_cmpl != []:
                print ''
                print 'les complement circons ou COI'
                for j in a.sv.i_cmpl:
                    print '**'
                    print j.prep
                    print_gn(j.nominal_group)
            print ''
            print 'adverbe de la phrase'
            print a.sv.advrb
            print ''
            print 'les verbe secondaire (non conjugues)'
            if a.sv.sv_sec is not None:
                print a.sv.sv_sec.vrb_main
                if a.sv.sv_sec.d_obj is not None:
                    print ''
                    print 'COD'
                    print_gn(a.sv.sv_sec.d_obj)
                if a.sv.sv_sec.i_cmpl != []:
                    print ''
                    print 'les complement circons ou COI'
                    for j in a.sv.sv_sec.i_cmpl:
                        print '**'
                        print j.prep
                        print_gn(j.nominal_group)
                print ''
                print 'adverbe de la phrase'
                print a.sv.sv_sec.advrb

if __name__ == '__main__':
    unit_tests()

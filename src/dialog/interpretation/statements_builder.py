#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import re
import random
from resources_manager import ResourcePool

from dialog_exceptions import DialogError
from dialog_exceptions import GrammaticalError


"""This module implements ...

"""

class StatementBuilder:
    
    def __init__(self, current_speaker = None):
        self._sentence = None
        self._current_speaker = current_speaker
        
        """
        flags helps for bilding queries and saving some extra informations
        flags[O] takes the value 'query' or 'inform'. the latter one is the default value.
        flags[1] takes the sentence aim if flags[O] is query.
        flags[2] takes the value 'TOBE' if the main verb is a state verb
        flags[3] takes the value 'LABEL' if a query involves searching for a label. E.g. Who is the man next to me? -> Ramses
        flags[4] takes the value 'NO_SN' if a w_question has sentence.sn == [] . it helps for this type of question: Who did give you a ball?
        flags[5] takes the value 'UNKNOWN' when a concept occurs for the first time in the ontology. E.g give me that map -> if the robot doesnt know what is a map, the flag is assigned
        flags[6] takes the list of all the concepts not known yet in the ontology. It is incremented when flags[5] is assigned to 'UNKNOWN'.
        flags[7] takes list of all unresolved IDs and sent to the Discriminant module. E.g the bottle is on the table. -> we may like to know which bottle we mention , in case there are more than 2.
        """
        self._flags = {}
        #self.flags = ['inform', None, None, None, None, None, [], []]
        self._statements = []

    def clear_statements(self):
        self._statements = []
        
    """
    The following function collects information that has never been said to the robot and return a list of it
    LearnMore object
    """
    def learnMore(self, noun):
        """oro = Oro(self.host, self.port)
        toLearn = oro.lookup(noun)
        oro.close()"""
        toLearn = []

        if toLearn == [] and noun.lower() != 'thing' :
            if 6 in self._flags:
                self._flags[6] += [noun] 
            else:
                self._flags[6] = [noun]
            
            self._flags[5] = 'UNKNOWN'
            
    """
    generate a string of k characters of the range [a-zA-Z0-9]
    """
    
    
    
    def generateId(self, k):
        sequence = "0123456789abcdefghijklmopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        sample = random.sample(sequence, k)
        #concatenation
        generatedId = ''
        for i in sample:
            generatedId += i

        #TODO: NOT A GOOD IDEA TO CHECK THAT EVERY ID IS UNIQUE THIS WAY!
        
        if 0 in self._flags:
            if self._flags[0] == "inform":
                pass
            
                """
                #verify the identifier doesn't exist in the server yet
                oro = Oro(self.host, self.port)
                if oro.lookup(generatedId) != []:
                    generatedId = self.generateId(k)
                oro.close()
                """

            elif self._flags[0] == 'query':
                generatedId = '?' + generatedId
            else:
                pass

        return generatedId
        

    def processOrderSentence(self, aSentence, idSender, flags):
        #The sentence is in the imperative form. A subject might not be declared.
        #process sentence.sv
        
        if not aSentence.resolved():
            raise DialogError("Trying to process an unresolved sentence!")
        
        self._sentence = aSentence
        self._current_speaker = idSender
        self._flags = flags
        
        if aSentence.sv:
            
            print "VERBAL IMPERATIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIVE fefefefge", str(self._sentence)
            
            
            
            self.processVerbalGroup(aSentence.sv, 'myself', '')
        
        return self._statements
            
    def processSentence(self, aSentence, idSender, flags):
        #process sentence.sn
        
        if not aSentence.resolved():
            raise DialogError("Trying to process an unresolved sentence!")
        
        self._sentence = aSentence
        self._current_speaker = idSender
        self._flags = flags
        
        subjId = self.generateId(2) + '_SBJ'

        if aSentence.sn:
            subjId = aSentence.sn[0].id
    
        #process sentence.sv
        if aSentence.sv != None:
            
            
            print "VERBAL      VVEEEEEEEEEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRBBBBBBBBB  FERER fefefefge", str(self._sentence)
            
            
            self.processVerbalGroup(aSentence.sv, subjId, '')


        return self._statements
    
          

    def processNominalGroup(self, nominalGroups, mainId, flags = None):
        
        
        
        print "BUGGY TEST GROUPE NOMINAL NOMINAL", str(self._sentence)
        print "BUGGY TEST NOMINAL", str(nominalGroups[0])   
                
        
        
        
        
        
        
        if flags:
            self._flags = flags
            
        for nominalGroup in nominalGroups:
            
            #case 1: the  noun phrase is a proper name or a person pronoun
            if nominalGroup.det == []:
                #case 1.1: the phrase noun is 'I' or me
                if nominalGroup.noun != [] and re.findall(r'^I$|^i$|^me$|^Me$', nominalGroup.noun[0]) != []:
                    self._statements.append(mainId + " owl:sameAs " + self._current_speaker)
                   
                #case 1.2: the phrase noun is 'you'
                elif nominalGroup.noun != [] and re.findall(r'^You$|^you$', nominalGroup.noun[0])  != []:
                    self._statements.append(mainId + " owl:sameAs " + "myself")
                    
                    
                #case 1.3: the phrase noun is a proper name, the 3 index of the flag is updated to LABEL
                else:
                    if nominalGroup.noun != []:
                        self._statements.append(mainId + " rdfs:label \"" + nominalGroup.noun[0] + "\"")
                        self._flags[3] = 'LABEL'
            #case 2: the  noun phrase is a common name. That is, there is a determinant
            #in case 2, we can therefore have adjectives and noun complements
            else:
                #learmore
                self.learnMore(nominalGroup.noun[0].capitalize())
                self._statements.append(mainId + " rdf:type " + nominalGroup.noun[0].capitalize())
                #case 2.1: the determinant is 'this', that is, the talker sees the subject and the subject is next to him
                if re.findall(r'^this$|^This$', nominalGroup.det[0]) != []:
                    self._statements.append(self._current_speaker + " sees " + mainId)
                    self._statements.append(self._current_speaker + " isNextTo " + mainId)

                #case 2.2: the determinant is 'that'; that is the subject is far from the talker but can still see it
                if re.findall(r'^that$|^That$', nominalGroup.det[0]) != []:
                    self._statements.append(self._current_speaker + " sees " + mainId)
                    self._statements.append(self._current_speaker + " isFarFrom " + mainId)

                #case 2.3: the determinant is a possessive adjective such as my, your
                if re.findall(r'^my$|^My$', nominalGroup.det[0]) != []:
                    situationId = self.generateId(len(mainId)+1) + "_SIT"
                    self._statements.append(self._current_speaker + " has" +nominalGroup.noun[0].capitalize()+" "+ situationId)
                    self._statements.append(situationId +" rdf:type StaticSituation")
                    self._statements.append(situationId +" involves "+ mainId)

                if re.findall(r'^your$|^Your$', nominalGroup.det[0]) != []:
                    situationId = self.generateId(len(mainId)+1) + "_SIT"
                    self._statements.append("myself" + " has" +nominalGroup.noun[0].capitalize()+" "+ situationId)
                    self._statements.append(situationId +" rdf:type StaticSituation")
                    self._statements.append(situationId +" involves "+ mainId)

                #process the noun phrase complements
                if nominalGroup.noun_cmpl:
                    #we choose noun_cmpl_Id of a size bigger than mainId, in order to make sure they would not be the same
                    #And we suffix it with _NCMPL
                    noun_cmpl_Id = self.generateId(len(mainId)+1) + '_NCMPL'
                    self.processNominalGroup(nominalGroup.noun_cmpl, noun_cmpl_Id)
                    self._statements.append(mainId + " belongsTo " + noun_cmpl_Id)

            #process adjectives
            if nominalGroup.adj != []:
                self.processAdjectives(nominalGroup.adj, mainId)

            #relatives
            #case 1: the subject of the sentence is subject of the relative clause.
            #         e.g. the man who is talking, is tall => the man is tall, the man is talking
            #case : the subject of the sentence is complement of the relative clause
            #         e.g. the man that you heard from is my boss
            #               => the man is my boss + you heard from the man
            if nominalGroup.relative:
                #case 1:
               
                print "STOOOOOOOOOOOOOOOOOOPPPPPPPPPPP   RELLATIVVVVVVVEEEEE"
                print "SENTNEFENCECECENNCEN RELLALTTTTT", str(self._sentence)
                
                print "RELATIVE FFFFFFLAGS ", str(self._flags)
                
                
                if nominalGroup.relative.sn == []:
                    
                    
                    
                    print "CASE 1"
                    print "CASE 1, BuGGY SV", str(nominalGroup.relative.sv)
                    
                    if nominalGroup.relative.sv != None:
                        self.processVerbalGroup(nominalGroup.relative.sv, mainId, '')
                        
                #case 2:
                else:
                    
                    
                    print "CASE 2"
                    
                    
                    
                    #process sentence.sn
                    subjId = self.generateId(2) + '_SBJ'
                    self.processNominalGroup(nominalGroup.relative.sn, subjId)
                    #process sentence.sv
                    if nominalGroup.relative.sv:
                        self.processVerbalGroup(nominalGroup.relative.sv, subjId, mainId)
        
        return self._statements



    def processAdjectives(self, adjectives, mainId):
        """For any adjectives, we add it in the ontology with the objectProperty 
        'hasFeature' except if a specific category has been specified in the 
        adjectives list.
        """
        
        for adj in adjectives:
            #learmore
            self.learnMore(adj)
            try:
                self._statements.append(mainId + " has" + ResourcePool().adjectives[adj] + " " + adj)
            except KeyError:
                self._statements.append(mainId + " hasFeature " + adj)
    

       

    def processVerbalGroup(self, verbalGroup, subject, relativeId):
                
        desires_group = ResourcePool().goal_verbs
        thematic_roles = ResourcePool().thematic_roles
        does_group = ['do', 'perform', 'act']
        
        print "TEST VEERRRRRRRRRRBAAAAAAAAAllllll"

        #we choose sitId of a size bigger than subject, in order to make sure they would never be the same
        #and we suffix it with _SIT  as Situation = StaticSituation|Events
        sitId = self.generateId(5) + '_SIT'
        
        if verbalGroup.vrb_main != []:
            verb = verbalGroup.vrb_main[0]
            #case 1: the verb is an action verb
            logging.debug("Found an action verb: " + verb)
            if verb != "be":
                
                
                
                
                
                print "BUGGY TEST VERBAL", str(self._sentence)
                
                
                
                
                if self._sentence.data_type == "imperative":
                    
                    self._statements.append(self._current_speaker + " desires " + sitId)
                    self._statements.append(sitId + " rdf:type " + verb.capitalize())
                    self._statements.append(sitId + 
                                            thematic_roles.get_subject_role(verb, True) + 
                                            subject)
                elif verb in desires_group:
                    self._statements.append(subject + " desires " + sitId)
                    #secondary verb processing. E.g in "I want you to take a bottle". 'take' is the secondary verb
                    if verbalGroup.sv_sec:
                        self.processVerbalGroup(verbalGroup.sv_sec, subject,'', self._current_speaker, file)
                
                #this is going to be used in order to process question with do. E.g. what are you doing?
                elif verb in does_group and self._flags[0] == 'query':
                    self._statements.append(subject + " performs " + sitId)
                    self._statements.append(sitId + " rdf:type ?any")
                    self._flags[2] = "VRB_PERFRM"
                    
                    
                else:
                    self._statements.append(subject + " performs " + sitId)
                    self._statements.append(sitId + " rdf:type " + verbalGroup.vrb_main[0].capitalize())
                             
               
            #case 2: the verb is "to be" ,we update "flags" in case of a query
            #        and sitId refers to the subject
            else:
                sitId = subject
                self._flags[2] = "TOBE"
        #we process the following, only for query
        if self._flags[0] == 'query':
            self.flagsToQueryExtension(subject, sitId)

        #direct object processing    
        if verbalGroup.d_obj:
            role = thematic_roles.get_next_cmplt_role(verb, True)
            verb = verbalGroup.vrb_main[0]
            
            for d_obj in verbalGroup.d_obj:
                #in case the nominal group has a relative clause for which the subject of the sentence becomes a complement,
                #objId is affected with the value of the subject ID.
                if relativeId != '':
                    objId = relativeId
                else:
                    objId = d_obj.id

                #if a verb is an action verb, then we are dealing with a situation involving some objects 
                if re.findall(r'^be$|^Be$', verb) == []:
                    self._statements.append(sitId + role + objId)
                    
                #otherwise , we are dealing with a state verb
                else:
                    
                    print "PROCESS VERBAL GROUB DOBJ SENTECE", str(self._sentence)
                    
                    
                    self.processNominalGroup(verbalGroup.d_obj, subject)
                



        #indirect complement and adverbials processing
        if verbalGroup.i_cmpl != []:
            for i_cmpl in verbalGroup.i_cmpl:

                #case 1: the i_cmpl is refering to a person or a thing: no preposition ''
                if not i_cmpl.prep:
                    if self._flags[0] == 'order': #TODO: what else?
                        role = thematic_roles.get_next_cmplt_role(verb, True)
                        for ic_noun in i_cmpl.nominal_group:
                             self._statements.append(sitId + role + ic_noun.id)

                #case 2: Do we have a thematic role associated to the preposition?
                elif thematic_roles.get_cmplt_role_for_preposition(verb, i_cmpl.prep[0]):
                    role = thematic_roles.get_cmplt_role_for_preposition(verb, i_cmpl.prep[0], True)
                    for ic_noun in i_cmpl.nominal_group:
                         self._statements.append(sitId + role + ic_noun.id)

                #case 3: Don't know what to do: build a relation from "is" + preposition (like "isIn")
                else:
                    for ic_noun in i_cmpl.nominal_group:
                         self._statements.append(sitId + " is"+i_cmpl.prep[0].capitalize() + " " + ic_noun.id)


                        
        #adverbs processing
        if verbalGroup.advrb != []:
            for advrb in verbalGroup.advrb:
                self.processAdverb(advrb, sitId)


    def processAdverb(self, advrb, mainId):
        pass



    def flagsToQueryExtension(self, subjectId, objectId):

        id = objectId
        aims = {
            "thing":" involves ?data, ?data rdf:type ?any, ?any rdfs:subClassOf owl:Thing",
            "people": " isTo ?any",
            "place":" isIn ?any",
            "date":" onDate ?data, ?data rdf:type ?any",
            "time":" atTime ?data, ?data rdf:type ?any",
            "manner":" hasFeature ?any",
            "purpose": " isBecauseOf ?any",
            "color":" hasColor ?any",
            "size" :" hasSize ?any",
            "duration": " hasDuration ?any"}

        """
            situation
            problem
            classification
            age
            duration
            frequency
            quantity
            distance
            invitation
            opinion
            description :
            explication   : what does your brother do for the living
            possession : whose
            people : who
            choice: which


        """

        
        if 2 in self._flags and self._flags[2] == 'TOBE':
            id = subjectId
            aims['thing'] = " rdf:type ?any, ?any rdfs:subClassOf owl:Thing"
            aims['people'] = " rdfs:label ?any"

        if 3 in self._flags and self._flags[3] == 'LABEL':
            aims['people'] = " rdf:type ?any, ?any rdfs:subClassOf owl:Thing"
            
                  
        if 4 in self._flags and self._flags[4] != 'NO_SN' and 2 in self._flags and self._flags[2] != 'VRB_PERFRM' :
            if self._flags[1] in aims.keys():
                self._statements.append(id + aims[self._flags[1]])
            else:
                self._statements.append(id + ' ?data has'+self._flags[1].capitalize() + ' ?any')

def unit_tests():
	"""This function tests the main features of the class StatementBuilder"""
	print("This is a test...")

if __name__ == '__main__':
	unit_tests()
    
    

#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import re
import random
from resources_manager import ResourcePool

"""This module implements ...

"""

class StatementBuilder:
    
    def __init__(self):
        self._sentence = None
        self._current_speaker = None
        self._flags = []
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
            self._flags[6] += [noun]
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
        if self._flags[0] == "inform":
            #verify the identifier doesn't exist in the server yet
            oro = Oro(self.host, self.port)
            if oro.lookup(generatedId) != []:
                generatedId = self.generateId(k)
            oro.close()

        elif self._flags[0] == 'query':
            generatedId = '?' + generatedId
        else:
            pass

        return generatedId


    def processOrderSentence(self, aSentence, idSender, flags):
        #The sentence is in the imperative form. A subject might not be declared.
        #process sentence.sv
        
        self._sentence = aSentence
        self._current_speaker = idSender
        self._flags = flags
        
        if aSentence.sv:
            self.processVerbalGroup('myself', '')
        
        return self._statements
            
    def processSentence(self, aSentence, idSender, flags):
        #process sentence.sn
        
        self._sentence = aSentence
        self._current_speaker = idSender
        self._flags = flags
        
        subjId = self.generateId(2, self._flags) + '_SBJ'
        if aSentence.sn != []:
            self.processNominalGroup(aSentence.sn, subjId)
        #Done because of case III.4.4 in buildObjectInteractionFromObjectInteraction
        else:
            if self._flags[0] == 'query':
                subjId = '?any'
                self._flags[4] = 'NO_SN'

        #process sentence.sv
        if aSentence.sv:
            self.processVerbalGroup(aSentence.sv, subjId, '')


    def processNominalGroup(self, nominalGroups, mainId):
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
                    file.write("\n"+ self._current_speaker + " sees " + mainId + "\n" + self._current_speaker + " isNextTo " + mainId)

                #case 2.2: the determinant is 'that'; that is the subject is far from the talker but can still see it
                if re.findall(r'^that$|^That$', nominalGroup.det[0]) != []:
                    file.write("\n"+ self._current_speaker + " sees " + mainId + "\n" + self._current_speaker + " isFarFrom " + mainId)

                #case 2.3: the determinant is a possessive adjective such as my, your
                if re.findall(r'^my$|^My$', nominalGroup.det[0]) != []:
                    situationId = self.generateId(len(mainId)+1) + "_SIT"
                    file.write("\n"+ self._current_speaker + " has" +nominalGroup.noun[0].capitalize()+" "+ situationId)
                    file.write("\n"+ situationId +" rdf:type StaticSituation" + "\n" + situationId +" involves "+ mainId)

                if re.findall(r'^your$|^Your$', nominalGroup.det[0]) != []:
                    situationId = self.generateId(len(mainId)+1) + "_SIT"
                    file.write("\n"+ "myself" + " has" +nominalGroup.noun[0].capitalize()+" "+ situationId)
                    file.write("\n"+ situationId +" rdf:type StaticSituation" + "\n" + situationId +" involves "+ mainId)

                #process the noun phrase complement
                if nominalGroup.noun_cmpl != []:
                    #we vonlontary choose noun_cmpl_Id of a size bigger than mainId, inorder to make sure they would not be the same
                    #And we suffix it with _NCMPL
                    noun_cmpl_Id = self.generateId(len(mainId)+1) + '_NCMPL'
                    self.processNominalGroup(nominalGroup.noun_cmpl, noun_cmpl_Id)
                    file.write("\n"+ noun_cmpl_Id + " has"+nominalGroup.noun[0].capitalize() + " " + mainId)

            #process adjectives
            if nominalGroup.adj != []:
                self.processAdjectives(nominalGroup.adj, mainId)

            #relatives
            #case 1: the subject of the sentence is subject of the relative clause.
            #         e.g. the man who is talking, is tall => the man is tall, the man is talking
            #case : the subject of the sentence is complement of the relative clause
            #         e.g. the man that you heard from is my boss
            #               => the man is my boss + you heard from the man
            if nominalGroup.relative != None:
                #case 1:
                if nominalGroup.relative.sn == []:
                    if nominalGroup.relative.sv != None:
                        self.processVerbalGroup(nominalGroup.relative.sv, mainId, '')
                        
                #case 2:
                else:
                    #process sentence.sn
                    subjId = self.generateId(2, flags) + '_SBJ'
                    self.processNominalGroup(nominalGroup.relative.sn, subjId)
                    #process sentence.sv
                    if nominalGroup.relative.sv:
                        self.processVerbalGroup(nominalGroup.relative.sv, subjId, mainId)




    def processAdjectives(self, adjectives, mainId):
        #For any adjectives, we add it in the ontology with the objectProperty 'hasFeature'
        for adj in adjectives:
            #learmore
            self.learnMore(adj)
            self._statements.append(mainId + " has" + ResourcePool().adjectives[adj] + " " + adj)
    

       

    def processVerbalGroup(self, mainId, relativeId):

        verbalGroup = self._sentence.sv
        
        desires_group = ResourcePool().goal_verbs


        #we vonlontary choose sitId of a size bigger than mainId, inorder to make sure they would never be the same
        #and we suffix it with _SIT  as Situation = StaticSituation|Events
        sitId = self.generateId(len(mainId)+1) + '_SIT'
        
        if verbalGroup.vrb_main != []:
            verb = verbalGroup.vrb_main[0]
            #case 1: the verb is an action verb
            logging.debug("Found an action verb: " + verb)
            if re.findall(r'^be$|^Be$', verb) == []:
                if self._sentence.data_type == "imperative":
                    self._statements.append(mainId + " desires " + sitId)
                    self._statements.append(sitId + " rdf:type " + verb.capitalize())
                elif verb in desires_group:
                    self._statements.append(mainId + " desires " + sitId)
                    self._statements.append(sitId + " rdf:type StaticSituation")
                else:
                    self._statements.append(mainId + " performs " + sitId)
                    self._statements.append(sitId + " rdf:type " + verbalGroup.vrb_main[0].capitalize())
                             
               
            #case 2: the verb is "to be" ,we update "flags" in case of a query
            #        and sitId refers to the mainId
            else:
                sitId = mainId
                self._flags[2] = "TOBE"
        #we process the following, only for query
        if self._flags[0] == 'query':
            self.flagsToQueryExtension(mainId, sitId, flags)

        #direct object processing
        if verbalGroup.d_obj != []:
            #in case the nominal group has a relative clause for which the subject of the sentence becomes a complement,
            #objId is affected with the value of the subject ID.
            if relativeId != '':
                objId = relativeId
            else:
                objId = self.generateId(len(mainId)+1) + '_OBJ'

            #if a verb is an action verb, then we are dealing with a situation involving some objects
            if re.findall(r'^be$|^Be$', verbalGroup.vrb_main[0]) == []:
                self._statements.append(sitId + " involves "+ objId)
                self.processNominalGroup(verbalGroup.d_obj,objId)
            #otherwise , we are dealing with a state verb
            else:
                self.processNominalGroup(verbalGroup.d_obj, mainId)
                
        #indirect complement and adverbials processing
        if verbalGroup.i_cmpl != []:
            for i_cmpl in verbalGroup.i_cmpl:
                i_cmpl_Id = self.generateId(len(mainId)+1) + '_ICMPL'

                #case 1: the i_cmpl is refering to a person or a thing. The preposition is either to|towards|into or ''
                if i_cmpl.prep == [] or re.findall(r'to|To', i_cmpl.prep[0]) != []:
                    if i_cmpl.nominal_group != []:
                        self.processNominalGroup(i_cmpl.nominal_group, i_cmpl_Id)
                        if self._flags[0] == 'order':
                             self._statements.append(i_cmpl_Id + " desires "+ sitId)
                        else:
                            self._statements.append(sitId + " isTo "+i_cmpl_Id)

                else:
                    if i_cmpl.nominal_group != []:
                        self.processNominalGroup(i_cmpl.nominal_group, i_cmpl_Id)
                        self._statements.append(sitId + " is"+i_cmpl.prep[0].capitalize()+" "+i_cmpl_Id)
                        
        #adverbs processing
        if verbalGroup.advrb != []:
            for advrb in verbalGroup.advrb:
                self.processAdverb(advrb, sitId)

        """
        #secondary verb processing. E.g in "I want you to take a bottle". 'take' is the secondary verb
        if verbalGroup.sv_sec != None:
            self.processVerbalGroup(verbalGroup.sv_sec, mainId,'', self._current_speaker, file)
        """


    def processAdverb(self, advrb, mainId):
        file.write('\n')



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
            quatity
            distance
            invitation
            opinion
            description :
            explication   : what does your brother do for the living
            possession : whose
            people : who
            choice: which


        """

        
        if self._flags[2] == 'TOBE':
            id = subjectId
            aims['thing'] = " rdf:type ?any, ?any rdfs:subClassOf owl:Thing"
            aims['people'] = " rdfs:label ?any"

        if self._flags[3] == 'LABEL':
            aims['people'] = " rdf:type ?any, ?any rdfs:subClassOf owl:Thing"
            
                  
        if self._flags[4] != 'NO_SN' :
            if self._flags[1] in aims.keys():
                file.write('\n' + id + aims[self._flags[1]])
            else:
                file.write('\n' + id + ' ?data has'+self._flags[1].capitalize() + ' ?any')

def unit_tests():
	"""This function tests the main features of the class StatementBuilder"""
	print("This is a test...")

if __name__ == '__main__':
	unit_tests()

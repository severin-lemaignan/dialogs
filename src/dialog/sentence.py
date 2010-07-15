#!/usr/bin/python
# -*- coding: utf-8 -*-

#SVN:rev202 + PythonTidy + rewrite 'toString' methods using Python __str__ + test cases

from helpers import colored_print #to colorize the sentence output

class Sentence:
    """
    A sentence is formed from:
    sn : a nominal structure typed into a Nominal_group
    sv : a verbal structure typed into a Verbal_Group
    aim : is used for retrieveing the aim of a question
    """

    def __init__(
        self,
        data_type,
        aim,
        sn,
        sv,
        ):
        self.data_type = data_type
        self.aim = aim
        self.sn = sn
        self.sv = sv
            
    def resolved(self):
        """returns True when the whole sentence is completely resolved
        to concepts known by the robot."""
        return  reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x._resolved, self.sn), 
                        True) \
                and \
                reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x._resolved, self.sv), 
                        True)

    
    def __str__(self):
        res =   colored_print(">> " + self.data_type.upper(), 'bold')
        if self.aim:
            res += " (aim: " + self.aim + ')'
        res += '\n'
        
        if self.sn:
            for s in self.sn:
                res += colored_print('nominal grp', 'bold') + ':\n\t' + str(s).replace("\n", "\n\t") + "\n"
        if self.sv:
            for s in self.sv:
                res += colored_print('verbal grp', 'bold') + ':\n\t' + str(s).replace("\n", "\n\t") + "\n"
        
        #res += "This sentence is " + ("fully resolved." if self.resolved() else "not fully resolved.")
        return res


class Nominal_Group:
    """
    Nominal group class declaration
    det : determinant
    noun: a simple noun
    adj: a list of adjectives describing the noun
    noun_cmpl: a list of noun complements
    relative : is a relative sentence typed into Sentence
    """

    def __init__(   self,
                    det,
                    noun,
                    adj,
                    noun_cmpl,
                    relative,
                    ):
        self.det = det
        self.noun = noun
        self.adj = adj
        self.noun_cmpl = noun_cmpl
        self.relative = relative
                
        """This field is True when this nominal group is resolved to a concept
        known by the robot."""
        self._resolved = False
        
        """This field hold the ID of the concept represented by this group.
        When the group is resolved, id must be different from None
        """
        self.id = None
        
        self._conjunction = 'AND' #could be 'AND' or 'OR'. TODO: use constants!
        

    def __str__(self):
        
        if self._resolved:
            res = colored_print(self.id, 'white', 'blue') + '\n' + colored_print('>resolved<', 'green')
        else:
            res =   colored_print(self.det, 'yellow') + " " + \
                    colored_print(self.adj, 'green') + " " + \
                    colored_print(self.noun, 'blue') + '\n'
            
            if self.noun_cmpl:
                for s in self.noun_cmpl:
                    res += '[OF] \n\t' + str(s).replace("\n", "\n\t") + "\n"
            
            if self.relative:
                for rel in self.relative:
                    res += 'relative:\n\t' + str(rel).replace("\n", "\n\t") + "\n"
        
        return res
    
    
    
class Indirect_Complement:
    """
    Indirect complement class declaration
    gn : nominal group
    prep : preposition
    """
    
    def __init__(self, prep, nominal_group):
        self.prep = prep
        self.nominal_group = nominal_group
        
    def resolved(self):
        return  reduce( lambda c1,c2: c1 and c2, 
                        map(lambda x: x._resolved, self.nominal_group), 
                        True)
        
    def __str__(self):
        res = colored_print(self.prep, 'yellow') + "..."
        
        if self.nominal_group:
            for s in self.nominal_group:
                res += '\n\t' + str(s).replace("\n", "\n\t") + "\n"
        
        return res



class Verbal_Group:
    """
    Verbal_group class declaration
    vrb_main: the main verb of a sentence
    vrb_sec : an accompanying verb of the main verb
    vrb_tense: the main verb tense
    d_obj : the  direct object referred by the main verb
    i_cmpl : the indirect object referred by the main verb or an adverbial formed from a nominal group
    vrb_adv : an adverb describing the verb
    advrb : an adverb used as an adverbial of the whole sentence
    """

    def __init__(
            self,
            vrb_main,
            sv_sec,
            vrb_tense,
            d_obj,
            i_cmpl,
            vrb_adv,
            advrb,
            state,
            vrb_sub_sentence,
            ):
        self.vrb_main = vrb_main
        self.sv_sec = sv_sec
        self.vrb_tense = vrb_tense
        self.d_obj = d_obj
        self.i_cmpl = i_cmpl
        self.advrb = advrb
        self.vrb_adv = vrb_adv
        self.state = state
        self.vrb_sub_sentence = vrb_sub_sentence
        
        """This field is True when this verbal group is resolved to a concept
        known by the robot."""
        self._resolved = False
        
    def resolved(self):
        return  self._resolved \
                and \
                reduce(lambda c1,c2: c1 and c2, map(lambda x: x._resolved, self.d_obj), True) \
                and \
                reduce(lambda c1,c2: c1 and c2, map(lambda x: x.resolved(), self.i_cmpl), True) \
                and \
                (self.sv_sec.resolved() if self.sv_sec else True) \
                and \
                reduce(lambda c1,c2: c1 and c2, map(lambda x: x.resolved(), self.vrb_sub_sentence), True)
    
    def __str__(self):
        res =   colored_print(self.vrb_main, 'magenta') + " (" + str(self.vrb_tense) + ")\n"
        if self.advrb:
            res += 'adverb: ' + colored_print(self.advrb, 'yellow') + "\n"
        if self.vrb_adv:
            res += 'vrb adv: ' + colored_print(self.vrb_adv, 'green') + "\n"
                
        if self.d_obj:
            res += 'direct objects:\n'
            for cmpl in self.d_obj:
                res += '\t' + str(cmpl).replace("\n", "\n\t") + "\n"
        
        if self.i_cmpl:
            res += 'indirect objects:\n'
            for cmpl in self.i_cmpl:
                res += '\t' + str(cmpl).replace("\n", "\n\t") + "\n"
        
        if self.vrb_sub_sentence:
            for vrb_sub_s in self.vrb_sub_sentence:
                res += 'vrb_sub_sentence:\n\t' + str(vrb_sub_s).replace("\n", "\n\t") + "\n"
        
        if self.sv_sec:
                res += 'secondary verbal grp:\n\t' + str(self.sv_sec).replace("\n", "\n\t") + "\n"
        
        res += colored_print(">resolved<", 'green') if self.resolved() else colored_print(">not resolved<", 'red')
        
        return res



def union (cl1, cl2, cl3):
    return cl1


def unit_tests():

    sentence1 = Sentence('w_question',
                        'location',
                        [Nominal_Group(['the'],  ['mother'],[],[], [])],
                        [Verbal_Group(['be'], [],'present simple',[], [],['today'], [], [], [])])
    
    print("*********************************")
    print(sentence1)
    
    sentence2 = Sentence('statement', 
                        '', 
                        [Nominal_Group([],["Jido"],[],[],[]), Nominal_Group([],["Danny"],[],[],[])], 
                        [Verbal_Group(["want"],[], 'infinitive',[],[],[],[],'affirmative', [])])
    
    print("*********************************")
    print(sentence2)
    
    sentence3 = Sentence('statement', 
                        '', 
                        [Nominal_Group([],["Holmes"],[],[],[]), Nominal_Group([],["Sherlock"],[],[],[])], 
                        [Verbal_Group(["want"],
                                    Verbal_Group(["eat"],[], 'infinitive',[],[],[],[],'affirmative', []), 
                                    'past simple',
                                    [],
                                    [],
                                    [],
                                    [],
                                    'negative', 
                                    [])])
    
    print("*********************************")
    print(sentence3)
    
    sentence4 = Sentence('statement',
                        '',
                        [Nominal_Group( ['the'],  
                                        ['bottle'],
                                        ['blue', 'gray'],
                                        [Nominal_Group(['my'],  ['mother'],[],[], [sentence2]), Nominal_Group(['my'],  ['father'],[],[], [])], 
                                        [])], 
                        [Verbal_Group(['know'], 
                                    [],
                                    'present simple',
                                    [Nominal_Group(['the'],  ["land"],['old'],[], []), Nominal_Group(['the'],  ["brand"],['lazy'],[], [])],
                                    [
                                        Indirect_Complement(['in'], 
                                                            [Nominal_Group(['the'],  ['garden'],['green'],[], [])]), 
                                        Indirect_Complement(['to'], 
                                                            [Nominal_Group(['the'],  ['car'],['red'],[], [])])
                                    ],
                                    ["slowly"], 
                                    ["now"], 
                                    "affirmative", 
                                    [sentence3])])
    print("*********************************")
    print(sentence4)
    
if __name__ == '__main__':
    unit_tests()

#!/usr/bin/python
# -*- coding: utf-8 -*-

#SVN:rev202 + PythonTidy + rewrite 'toString' methods using Python __str__ + test cases

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

    def __str__(self):
        res = self.data_type + '\n' + \
                self.aim + '\n'
        
        if self.sn:
            for s in self.sn:
                res += 'sn:\n\t' + str(s).replace("\n", "\n\t") + "\n"
                
        res += (('sv:\n\t' + str(self.sv).replace("\n", "\n\t") + "\n") if self.sv else "")
        
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

    def __init__(
        self,
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
        
    def __str__(self):
        res =   'det:' + str(self.det) + "\n" + \
                'noun:' + str(self.noun) + "\n" + \
                'adj:' + str(self.adj) + "\n"

        if self.noun_cmpl:
            for s in self.noun_cmpl:
                res += 'noun_cmpl:\n\t' + str(s).replace("\n", "\n\t") + "\n"
        
        if self.relative:
            for s in self.relative:
                res += 'relative:\n\t' + str(s).replace("\n", "\n\t") + "\n"
        
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
        
    def __str__(self):
        res = 'prep:' + str(self.prep) + '\n'
        
        if self.nominal_group:
            for s in self.nominal_group:
                res += 'sn:\n\t' + str(s).replace("\n", "\n\t") + "\n"
        
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
    
    def __str__(self):
        res =   'vrb_main:' + str(self.vrb_main) + "\n" + \
                'vrb_tense:' + str(self.vrb_tense) + "\n" + \
                'advrb: ' + str(self.advrb) + "\n" + \
                'vrb_adv' + str(self.vrb_adv) + "\n"
                
        if self.d_obj:
            for cmpl in self.d_obj:
                res += 'd_obj:\n\t' + str(cmpl).replace("\n", "\n\t") + "\n"
        
        if self.i_cmpl:
            for cmpl in self.i_cmpl:
                res += 'i_cmpl:\n\t' + str(cmpl).replace("\n", "\n\t") + "\n"
        
        if self.vrb_sub_sentence:
            for vrb_sub_s in self.vrb_sub_sentence:
                res += 'vrb_sub_sentence:\n\t' + str(vrb_sub_s).replace("\n", "\n\t") + "\n"

        
        return res


class ObjectInteraction:

    def __init__(
        self,
        sentence,
        sender,
        recipient,
        date,
        time,
        ):
        self.sentence = sentence
        self.sender = sender
        self.recipient = recipient
        self.date = date
        self.time = time

def unit_tests():

    sentence1 = Sentence('w_question',
                        'location',
                        [Nominal_Group(['the'],  ['mother'],[],None, None)],
                        Verbal_Group(['be'], None,'present simple',None, None,['today'], None, None, None))
    
    print("*********************************")
    print(sentence1)
    
    sentence2 = Sentence('statement', 
                        '', 
                        [Nominal_Group([],["Jido"],[],[],None), Nominal_Group([],["Danny"],[],[],None)], 
                        Verbal_Group(["want"],None, 'infinitive',[],[],[],[],'affirmative', None))
    
    print("*********************************")
    print(sentence2)
    
    sentence3 = Sentence('statement', 
                        '', 
                        [Nominal_Group([],["Holmes"],[],[],None), Nominal_Group([],["Sherlock"],[],[],None)], 
                        Verbal_Group(["want"],
                                    Verbal_Group(["eat"],None, 'infinitive',[],[],[],[],'affirmative', None), 
                                    'past simple',
                                    [],
                                    [],
                                    [],
                                    [],
                                    'negative', 
                                    None))
    
    print("*********************************")
    print(sentence3)
    
    sentence4 = Sentence('statement',
                        '',
                        [Nominal_Group( ['the'],  
                                        ['bottle'],
                                        ['blue', 'gray'],
                                        [Nominal_Group(['my'],  ['mother'],[],[], [sentence2]), Nominal_Group(['my'],  ['father'],[],[], None)], 
                                        None)], 
                        Verbal_Group(['know'], 
                                    None,
                                    'present simple',
                                    [Nominal_Group(['the'],  ["land"],['old'],[], None), Nominal_Group(['the'],  ["brand"],['lazy'],[], None)],
                                    [
                                        Indirect_Complement(['in'], 
                                                            [Nominal_Group(['the'],  ['garden'],['green'],[], None)]), 
                                        Indirect_Complement(['to'], 
                                                            [Nominal_Group(['the'],  ['car'],['red'],[], None)])
                                    ],
                                    ["slowly"], 
                                    ["now"], 
                                    "affirmative", 
                                    [sentence3]))
    print("*********************************")
    print(sentence4)
    
if __name__ == '__main__':
    unit_tests()

#!/usr/bin/python
# -*- coding: utf-8 -*-

#SVN:rev202 + PythonTidy

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

    def getString(self):

        def printGroupNominal(name, group_nominals):
            for nom in group_nominals:
                print name + 'det:' + str(nom.det)
                print name + 'noun:' + str(nom.noun)
                print name + 'adj:' + str(nom.adj)
                if nom.relative != None:
                    print name + 'relative:'
                    nom.relative.getString()
                if nom.noun_cmpl != []:
                    print name + 'noun_cmpl:'
                    printGroupNominal(name + 'noun_cmpl:',
                            nom.noun_cmpl)

        def printVerbalGroup(name, verbal_group):
            print name + 'vrb_main:' + str(verbal_group.vrb_main)
            print name + 'vrb_tense:' + str(verbal_group.vrb_tense)
            print name + 'advrb: ' + str(verbal_group.advrb)
            print name + 'vrb_adv' + str(verbal_group.vrb_adv)
            if verbal_group.d_obj != []:
                print name + 'd_obj:'
                printGroupNominal(name + 'd_obj:', verbal_group.d_obj)
            if verbal_group.vrb_sub_sentence != None:
                print name + 'vrb_sub_sentence:'
                for vrb_sub_s in verbal_group.vrb_sub_sentence:
                    vrb_sub_s.getString()

            if verbal_group.i_cmpl != []:
                print name + 'i_cmpl:'
                for i in verbal_group.i_cmpl:
                    print name + 'i_cmpl:' + str(i.prep)
                    printGroupNominal(name + 'i_cmpl:', i.nominal_group)

        print self.data_type, '\n', self.aim, '\n'
        if self.sn != []:
            printGroupNominal('sn:', self.sn)
        if self.sv != None:
            printVerbalGroup('sv:', self.sv)


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


class Indirect_Complement:

    """
  Indirect complement class declaration
  gn : nominal group
  prep : preposition
  """

    def __init__(self, prep, nominal_group):
        self.prep = prep
        self.nominal_group = nominal_group


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



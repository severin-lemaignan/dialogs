#!/usr/bin/python
# -*- coding: utf-8 -*-
# SVN:rev202 + PythonTidy

"""
ce paquetage est le paquetage principal du module il permet de traiter les ponctuations...
le but est de simplifier le traitement qui suit en utilisant un lien qui sert a comprendre le langage naturel
comme pour les virgules qui peuvent etre des and entre des groupes nominaux ou a la fin de relative
la fonction principale du paquetage, analyse toutes les phrases d'une replique
"""

from resources_manager import ResourcePool
import analyse_phrase
import recherche_mot

liste_lettre = [
    ('A', 'a'),
    ('B', 'b'),
    ('C', 'c'),
    ('D', 'd'),
    ('E', 'e'),
    ('F', 'f'),
    ('G', 'g'),
    ('H', 'h'),
    ('I', 'i'),
    ('J', 'j'),
    ('K', 'k'),
    ('L', 'l'),
    ('M', 'm'),
    ('N', 'n'),
    ('O', 'o'),
    ('P', 'p'),
    ('Q', 'q'),
    ('R', 'r'),
    ('S', 's'),
    ('T', 't'),
    ('U', 'u'),
    ('V', 'v'),
    ('W', 'w'),
    ('X', 'x'),
    ('Y', 'y'),
    ('Z', 'z'),
    ]
list_propo_relative = ['who', 'which', 'that']
list_mot = [
    'hi',
    'hello',
    'good',
    'ok',
    'nice',
    'good',
    'yes',
    'no',
    'sorry',
    ]

# le but est de finaliser le traitement lie a une phrase precisement tel que les majescule


def trait_penctu(phrase, frt_wd):
    boolean = compteur = 0
    phr_aux = []

  # traitement de minuscul

    for u in liste_lettre:

    # dans le cas ou on a une Maj, on la transforme en Min

        if u[0] == phrase[0][0]:
            phrase[0] = u[1] + (phrase[0])[1:]

      # si le mot obtenu correspond a des cas particulier du debut de phrase on le garde en Min

            for v in frt_wd:
                if phrase[0] == v[0]:
                    boolean = 1
                    break

      # si c'est un groupe nominal on le garde en Min

            if recherche_mot.rech_sujet(phrase, 0) != []:
                boolean = 1

      # si c'est un mot d'amorce ou autre, pareil

            for w in list_mot:
                if w == phrase[0]:
                    boolean = 1
                    break

      # sinon il s'agit d'un nom propre, donc il faut le remettre en Maj

            if boolean == 0:
                phrase[0] = u[0] + (phrase[0])[1:]

  # on parcourt la phrase de droite a gauche

    m = len(phrase) - 1
    indexe = 0
    while m >= 0:

    # dans le cas ou on a 's

        if phrase[m].endswith("'s"):

      # on prend le groupe nominal de la partie droite (on lui ajoutant un determinant s'il n'en a pas

            if recherche_mot.rech_sujet(phr_aux, 0) == []:
                gr_nom = recherche_mot.rech_sujet(['the'] + phr_aux, 0)
                indexe = indexe - 1
            else:
                gr_nom = recherche_mot.rech_sujet(phr_aux, 0)

      # on cherche son complement, la boucle permet de determiner tous les complements en cascade

            compl_gr_nom = recherche_mot.rech_compl_nom(gr_nom,
                    phr_aux, 0)
            while recherche_mot.rech_compl_nom(compl_gr_nom, phr_aux,
                    len(gr_nom) + 1) != []:
                compl_gr_nom = compl_gr_nom + ['of'] \
                    + recherche_mot.rech_compl_nom(compl_gr_nom,
                        phr_aux, len(gr_nom) + 1)

      # on cree le groupe nomal de droite (avec ses complement)

            if compl_gr_nom != []:
                gr_nom = gr_nom + ['of'] + compl_gr_nom
            phr_aux = [phrase[m]] + phr_aux
            m = m - 1

      # au cour de cette boucle, on cherche le groupe nominal de gauche

            while not phrase[m].endswith("'s") \
                and recherche_mot.rech_sujet(phrase, m) == []:
                phr_aux = [phrase[m]] + phr_aux
                m = m - 1

      # si pas de determinant

            if phrase[m].endswith("'s"):
                gr_nominal_base = recherche_mot.rech_sujet(['the']
                        + phr_aux, 0)
                indexe = indexe - 1
                gr_nominal_base[len(gr_nominal_base) - 1] = \
                    (gr_nominal_base[len(gr_nominal_base)
                     - 1])[:len(gr_nominal_base[len(gr_nominal_base)
                                - 1]) - 2]
            elif recherche_mot.rech_sujet(phrase, m) != []:

      # s'il y a determinant et donc on determine le groupe nominal en entier

                gr_nominal_base = recherche_mot.rech_sujet(phrase, m)
                print gr_nominal_base
                indexe = indexe - 1
                gr_nominal_base[len(gr_nominal_base) - 1] = \
                    (gr_nominal_base[len(gr_nominal_base)
                     - 1])[:len(gr_nominal_base[len(gr_nominal_base)
                                - 1]) - 2]
                m = m - 1

      # on finit de creer la phrase auxiliaire

            phr_aux = gr_nom + ['of'] + gr_nominal_base \
                + phr_aux[len(gr_nom) + len(gr_nominal_base) + indexe:]
            indexe = 0
        else:
            phr_aux = [phrase[m]] + phr_aux
            m = m - 1

  # la phrase auxiliaire devient la phrase principale

    phrase = phr_aux

  # traitement pour la virgule utilisee avec la relative ou autre subordonne

    x = relative_trouve = 0
    while x < len(phrase):

    # dans le cas ou on trouve une relative, il nous faut une virgule de fin

        if relative_trouve == 0:
            for y in list_propo_relative:
                if phrase[x] == y:
                    relative_trouve = 1
                    break
            x = x + 1
        elif relative_trouve == 1:

    # on cherche a garder la virgule de fin de relative
      # si la relative fini la phrase, on garde malgre tout la virgule

            if x == len(phrase) - 1:
                phrase = phrase + [',']
            elif phrase[x].endswith(','):
                phrase[x] = (phrase[x])[:1]
                phrase = phrase[:x] + [','] + phrase[x + 1:]
                relative_trouve = 0
            x = x + 1
        x = x + 1
    return phrase


# c'est la fonction principale du module qui sert a analyser les repliques apres les avoir decomposees en phrases


def analyser_replique(rep):
    class_replique = phrase = replique = []
    mot = ''
    
    frt_wd = ResourcePool().sentence_starts


  # cette boucle nous permet de convertir la chaine de caracteres en liste de chaines de caracteres

    for line in rep:
        if line != ' ':
            mot = mot + line
        else:
            replique = replique + [mot]
            mot = ''
    replique = replique + [mot]

  # le but de cette boucle est de traiter les verbes simplifie

    for i in replique:

    # il s'agit de am

        if i.endswith("'m"):
            position = replique.index(i)
            replique = replique[:position + 1] + ['am'] \
                + replique[position + 1:]
            replique[position] = (replique[position])[:len(i) - 2]
        elif i.endswith("'re"):

    # il s'agit de are

            position = replique.index(i)
            replique = replique[:position + 1] + ['are'] \
                + replique[position + 1:]
            replique[position] = (replique[position])[:len(i) - 3]
        elif i.endswith("'ve"):

    # il s'agit de have

            position = replique.index(i)
            replique = replique[:position + 1] + ['have'] \
                + replique[position + 1:]
            replique[position] = (replique[position])[:len(i) - 3]
        elif i.endswith("'ll"):

    # il s'agit de will

            position = replique.index(i)
            replique = replique[:position + 1] + ['will'] \
                + replique[position + 1:]
            replique[position] = (replique[position])[:len(i) - 3]
        elif i.endswith("n't"):

    # dans le cas ou il y a une negation

            position = replique.index(i)
            replique = replique[:position + 1] + ['not'] \
                + replique[position + 1:]
            replique[position] = (replique[position])[:len(i) - 3]
        elif i.endswith("'s"):

    # il s'agit de is

            position = replique.index(i)

      # 's peut aussi etre traduit par of, ce qui explique la condition ci-dessous

            if i == "he's" or i == "she's" or i == "it's" or i \
                == "that's" or i == "He's" or i == "She's" or i \
                == "It's" or i == "what's" or i == "who's" or i \
                == "how's" or i == "What's" or i == "Who's" or i \
                == "How's":
                replique = replique[:position + 1] + ['is'] \
                    + replique[position + 1:]
                replique[position] = (replique[position])[:len(i) - 2]

  # cette boucle nous permet d'avoir les differente phrase et appeler l'analyse_phrase pour recuperer les classes

    for j in replique:
        if j.endswith('.'):
            print phrase
            phrase = phrase + [j[:len(j) - 1]]
            phrase = trait_penctu(phrase, frt_wd)

      # class_replique=class_replique+analyse_phrase.analyse_phr(phrase,frt_wd)

            print phrase
            phrase = []
        elif j.endswith('!'):
            phrase = phrase + [j[:len(j) - 1]] + ['!']
            phrase = trait_penctu(phrase, frt_wd)

      # class_replique=class_replique+analyse_phrase.analyse_phr(phrase,frt_wd)

            phrase = []
        elif j.endswith('?'):
            phrase = phrase + [j[:len(j) - 1]] + ['?']
            phrase = trait_penctu(phrase, frt_wd)

      # class_replique=class_replique+analyse_phrase.analyse_phr(phrase,frt_wd)

            phrase = []
        else:
            phrase = phrase + [j]

    phrase=trait_penctu(phrase, frt_wd)
    class_replique=class_replique+analyse_phrase.analyse_phr(phrase,frt_wd)
    return class_replique

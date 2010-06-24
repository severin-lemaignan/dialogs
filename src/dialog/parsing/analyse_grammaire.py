#!/usr/bin/python
# -*- coding: utf-8 -*-

#SVN:rev202 + PythonTidy

import recherche_mot
import analyse_verbe
import recuperer_phrase
import analyse_adjectif
from sentence import Sentence, Verbal_Group, Nominal_Group, Indirect_Complement

list_preposition = [
    'in',
    'on',
    'at',
    'from',
    'about',
    'for',
    'next',
    'last',
    'ago',
    ]
list_propo_relative = ['who', 'which', 'that', 'where', 'when']
liste_modal = [
    'must',
    'should',
    'may',
    'might',
    'can',
    'could',
    'shall',
    ]

# fonction qui determine les complement circonstanciel ou COI


def verif_prepo(reste_phrase, objet):
    if objet == []:
        return []

  # si on a une preposition on renvoie l'objet

    for i in list_preposition:
        if i == reste_phrase[reste_phrase.index(objet[0])]:
            return objet
	if i == reste_phrase[reste_phrase.index(objet[0]) - 1]:
            return [reste_phrase[reste_phrase.index(objet[0]) -1]] \
                + objet
	if i == reste_phrase[reste_phrase.index(objet[0]) - 2]:
            return [convert_string([reste_phrase[reste_phrase.index(objet[0])-2]]+[reste_phrase[reste_phrase.index(objet[0])-1]] )] \
                + objet
    if reste_phrase.index(objet[0]) == 0:
        return []
        
    return []


# fonction pour creer des strings


def convert_string(liste):
    if liste == []:
        return ''
    if len(liste) == 1:
        return liste[0]
    else:
        return liste[0] + '+' + convert_string(liste[1:])


def recup_subordonne(phrase):
    nb_relative = 0
    pos = 0
    for y in phrase[1:]:
        pos = pos + 1
        for x in list_propo_relative:
            if y == x:
                nb_relative = nb_relative + 1
                break
        if y == ',':
            if nb_relative == 1:
                break
            else:
                nb_relative = nb_relative - 1
    return pos


# une fonction qui nous permet de remplir un structure nominomiale


def recuperer_gr_nom(phrase, gr_nom, position_gr_nom):
    relative = None
    gn = Nominal_Group([], [], [], [], relative)
    compl_gr_nom = recherche_mot.rech_compl_nom(gr_nom, phrase,
            position_gr_nom)
    det = recherche_mot.rech_det(gr_nom)
    adj = recherche_mot.rech_adj(gr_nom)
    noun = recherche_mot.recup_nom(gr_nom, adj)

  # determiner les relative

    pos_relative = recherche_mot.rech_relative(gr_nom, phrase,
            position_gr_nom, list_propo_relative)
    position = recup_subordonne(phrase)
    if pos_relative != 0:
        phrase_relative = phrase[:position]
        relative = autre_type_phrase(phrase_relative[pos_relative
                + 1:], 'relative', '')

  # pour finir, il faut ressortir les compelement du groupe nominal qui est groupe nominal

    if compl_gr_nom != []:
        gn = Nominal_Group(det, noun, adj, [recuperer_gr_nom(phrase,
                           compl_gr_nom, position_gr_nom + len(gr_nom)
                           + 1)], relative)
    else:
        gn = Nominal_Group(det, noun, adj, [], relative)
    return gn


# cette fonction cherche les groupes nominaux se trouvant dans la structure verbal


def recupere_obj_iobj(reste_phrase, vg):

  # on cherche le premier groupe nominal de la phrase

    objet = recherche_mot.rech_SN(reste_phrase)
    while objet != []:

    # si ce n'est pas un COD

        if verif_prepo(reste_phrase, objet) != []:
            if len(verif_prepo(reste_phrase, objet)) == len(objet):
                prep = []
            else:
                prep = [verif_prepo(reste_phrase, objet)[0]]
            gr_objet = []
            while objet != []:

        # on commence par supprimer les relatives et le groupe nominal de base

                gr_objet = gr_objet + [recuperer_gr_nom(reste_phrase,
                        objet, reste_phrase.index(objet[0]))]
                if gr_objet[len(gr_objet) - 1].relative != None:
                    reste_phrase = reste_phrase[reste_phrase.index(',')
                        + 1:]
                else:
                    reste_phrase = \
                        recuperer_phrase.recup_phr_sans_gn(reste_phrase,
                            objet, reste_phrase.index(objet[0]))
                while len(reste_phrase) != 0 and reste_phrase[0] \
                    == 'of':
                    gr_nom = recherche_mot.rech_sujet(reste_phrase, 1)
                    reste_phrase = \
                        recuperer_phrase.recup_phr_sans_gn(reste_phrase,
                            gr_nom, 1)

        # on a un diplicata avec le and, il faut remplir la lsite

                if len(reste_phrase) != 0 and reste_phrase[0] == 'and':
                    objet = recherche_mot.rech_sujet(reste_phrase, 1)
                else:
                    objet = []
            vg.i_cmpl = vg.i_cmpl + [Indirect_Complement(prep,
                    gr_objet)]
        else:

      # si c'est un COD

            gr_objet = []

      # on reprend le meme que code de dessus

            while objet != []:
                gr_objet = gr_objet + [recuperer_gr_nom(reste_phrase,
                        objet, reste_phrase.index(objet[0]))]
                if gr_objet[len(gr_objet) - 1].relative != None:
                    reste_phrase = reste_phrase[reste_phrase.index(',')
                        + 1:]
                else:
                    reste_phrase = \
                        recuperer_phrase.recup_phr_sans_gn(reste_phrase,
                            objet, reste_phrase.index(objet[0]))
                while len(reste_phrase) != 0 and reste_phrase[0] \
                    == 'of':
                    gr_nom = recherche_mot.rech_sujet(reste_phrase, 1)
                    reste_phrase = \
                        recuperer_phrase.recup_phr_sans_gn(reste_phrase,
                            gr_nom, 1)
                if len(reste_phrase) != 0 and reste_phrase[0] == 'and':
                    objet = recherche_mot.rech_sujet(reste_phrase, 1)
                else:
                    objet = []

      # dans une phrase il n y a qu'un COD

            if vg.d_obj == []:
                vg.d_obj = gr_objet
            else:

        # sinon, le premier groupe nominal trouve n'est pas COD mais COI

                vg.i_cmpl = vg.i_cmpl + [Indirect_Complement([],
                        vg.d_obj)]
                vg.d_obj = gr_objet
        objet = recherche_mot.rech_SN(reste_phrase)
    return reste_phrase


# cela correspond au fait de representer l'etat comme etant un COD


def cas_ph_etat(reste_phrase, vg):
    gr_objet = []

  # on utilise le meme code de la fonction de dessus (ou presque)
    reste_phrase=recupere_obj_iobj(reste_phrase, vg)
    

  # les adjectifs sont pris pour des COD (meme sans nom)

    while len(reste_phrase) != 0 \
        and analyse_adjectif.reconnaitre_adj(reste_phrase[0]) == 1:
        if vg.d_obj == []:
            vg.d_obj = [Nominal_Group([], [], [], [], None)]
        vg.d_obj[0].adj = vg.d_obj[0].adj + [reste_phrase[0]]
        reste_phrase = reste_phrase[1:]
        if len(reste_phrase) != 0 and reste_phrase[0] == 'and':
            if recherche_mot.rech_sujet(reste_phrase, 1) != []:
                gr_objet = []
                objet = recherche_mot.rech_sujet(reste_phrase, 1)
                while objet != []:
                    gr_objet = gr_objet \
                        + [recuperer_gr_nom(reste_phrase, objet,
                           reste_phrase.index(objet[0]))]
                    if gr_objet[len(gr_objet) - 1].relative != None:
                        reste_phrase = \
                            reste_phrase[reste_phrase.index(',') + 1:]
                    else:
                        reste_phrase = \
                            recuperer_phrase.recup_phr_sans_gn(reste_phrase,
                                objet, reste_phrase.index(objet[0]))
                    while len(reste_phrase) != 0 and reste_phrase[0] \
                        == 'of':
                        gr_nom = recherche_mot.rech_sujet(reste_phrase,
                                1)
                        reste_phrase = \
                            recuperer_phrase.recup_phr_sans_gn(reste_phrase,
                                gr_nom, 1)
                    if len(reste_phrase) != 0 and reste_phrase[0] \
                        == 'and':
                        objet = recherche_mot.rech_sujet(reste_phrase,
                                1)
                    else:
                        objet = []
            reste_phrase = reste_phrase[1:]
    vg.d_obj = vg.d_obj + gr_objet
    return reste_phrase


# on recupere la structure nominale de la phrase


def recuperation_sn(phrase, analyse):

  # la position du sujet est au debut

    sujet = recherche_mot.rech_sujet(phrase, 0)
    while sujet != []:
        analyse.sn = analyse.sn + [recuperer_gr_nom(phrase, sujet, 0)]
        if analyse.sn[len(analyse.sn) - 1].relative != None:
            phrase = phrase[phrase.index(',') + 1:]
            while phrase[0] == ',':
                phrase = phrase[1:]
        else:

      # on recupere la structure verbale

            phrase = recuperer_phrase.recup_phr_sans_gn(phrase, sujet,
                    phrase.index(sujet[0]))
        while len(phrase) != 0 and phrase[0] == 'of':
            gr_nom = recherche_mot.rech_sujet(phrase, 1)
            phrase = recuperer_phrase.recup_phr_sans_gn(phrase, gr_nom,
                    phrase.index(gr_nom[0]))

    # si on a un and, on a un diplicata donc il faut remplir la liste

        if len(phrase) != 0 and phrase[0] == 'and':
            sujet = recherche_mot.rech_sujet(phrase, 1)
            phrase = phrase[1:]
        else:
            sujet = []
    return phrase


# cette fonction reconnait et traite les phrase declarative, sinon elle traite les phrase imperative


def autre_type_phrase(phrase, type_phrase, demande):

  # on initialise sentence et sa structure verbale

    analyse = Sentence('', '', [], None)
    vg = Verbal_Group(
        [],
        None,
        '',
        [],
        [],
        [],
        [],
        'affirmative',
        [],
        )
    modal = phrase_subordonne = []
    if recherche_mot.rech_sujet(phrase, 0) != [] or type_phrase \
        == 'relative':

    # si pas de type, c'est une statement

        if type_phrase == '':
            analyse.data_type = 'statement'
        else:
            analyse.data_type = type_phrase

    # s'il y a une demande en in de la fonction, il faut recuperer cette valeur

        if demande != '':
            analyse.aim = demande
        else:
            analyse.aim = ''
        phrase = recuperation_sn(phrase, analyse)

    # prochaine etape traitement de modal et de negation

        for m in liste_modal:
            if phrase[0] == m:
                modal = [phrase[0]]

    # il faut traiter tous les cas possible pour recuperer le temps d'une phrase

        if len(phrase) > 1 and phrase[1] == 'not':
            vg.state = 'negative'
            if phrase[0] == 'do' or phrase[0] == 'does' or phrase[0] \
                == 'did':
                vg.vrb_tense = analyse_verbe.trait_verb([phrase[0]], [])
                phrase = phrase[2:]
            elif modal != []:
                phrase = phrase[2:]
                vg.vrb_tense = 'present simple'
            else:
                phrase = [phrase[0]] + phrase[2:]
                vg.vrb_tense = analyse_verbe.trait_verb(phrase,
                        vg.vrb_adv)
            vg.vrb_adv = recherche_mot.rech_adverbe_verbe(phrase)
            base_verbe = \
                recherche_mot.rech_verb(phrase[len(vg.vrb_adv):],
                    vg.vrb_tense)
            vg.vrb_main = \
                [convert_string(analyse_verbe.verb_infin(phrase,
                 base_verbe, vg.vrb_tense))]
        else:
            if modal != []:
                phrase = phrase[1:]
            vg.vrb_adv = recherche_mot.rech_adverbe_verbe(phrase)
            vg.vrb_tense = analyse_verbe.trait_verb(phrase, vg.vrb_adv)
            base_verbe = \
                recherche_mot.rech_verb(phrase[len(vg.vrb_adv):],
                    vg.vrb_tense)
            vg.vrb_main = \
                [convert_string(analyse_verbe.verb_infin(phrase,
                 base_verbe, vg.vrb_tense))]
        reste_phrase = recuperer_phrase.recup_res_phr(phrase,
                base_verbe)

    # apres recuperation de verbe on voit si c'est un verbe d'etat

        if vg.vrb_main == ['be'] and len(reste_phrase) != 0:

      # dans ce cas, il s'agit de faire un traitement different (COD comme etant etat)

            reste_phrase = cas_ph_etat(reste_phrase, vg)
    else:

    # meme algo que dans une phrase delcarative

        analyse.data_type = 'imperative'
        analyse.aim = ''
        vg.vrb_tense = 'present simple'
        if phrase[1] == 'not':
            phrase = phrase[phrase.index('not') + 1:]
            vg.vrb_adv = recherche_mot.rech_adverbe_verbe(phrase)
            vg.state = 'negative'
            base_verbe = [phrase[0 + len(vg.vrb_adv)]]
            vg.vrb_main = \
                [convert_string(analyse_verbe.verb_infin(phrase,
                 base_verbe, vg.vrb_tense))]
        else:
            vg.vrb_adv = recherche_mot.rech_adverbe_verbe(phrase)
            base_verbe = [phrase[0 + len(vg.vrb_adv)]]
            vg.vrb_main = \
                [convert_string(analyse_verbe.verb_infin(phrase,
                 base_verbe, vg.vrb_tense))]
        reste_phrase = recuperer_phrase.recup_res_phr(phrase,
                base_verbe)

  # on voit s'il y a un verbe secondaire

    if recherche_mot.rech_vrb_scd(reste_phrase, list_preposition) != []:
        verbe_secondaire = recherche_mot.rech_vrb_scd(reste_phrase,
                list_preposition)
        reste_phrase = \
            reste_phrase[:reste_phrase.index(verbe_secondaire[0])]
        if phrase[phrase.index(verbe_secondaire[0]) - 1] == 'not':
            vg.sv_sec = Verbal_Group(
                [convert_string(analyse_verbe.verb_infin(phrase,
                 verbe_secondaire, ''))],
                None,
                '',
                [],
                [],
                [],
                [],
                'negative',
                [],
                )
        else:
            vg.sv_sec = Verbal_Group(
                [convert_string(analyse_verbe.verb_infin(phrase,
                 verbe_secondaire, ''))],
                None,
                '',
                [],
                [],
                [],
                [],
                'affirmative',
                [],
                )
        phrase_secondaire = recuperer_phrase.recup_res_phr(phrase,
                verbe_secondaire)

    # on recupere tous les adverbe de la phrase

        vg.sv_sec.advrb = recherche_mot.rech_adv(phrase_secondaire)
        phrase_secondaire = recupere_obj_iobj(phrase_secondaire,
                vg.sv_sec)

  # on voit s'il y a une subordonne

    for w in list_propo_relative:
        if len(reste_phrase) > 0 and reste_phrase[0] == w:
            position = recup_subordonne(reste_phrase)
            phrase_subordonne = reste_phrase[:position]
            vg.vrb_sub_sentence = vg.vrb_sub_sentence \
                + [autre_type_phrase(phrase_subordonne[1:], 'subordonne'
                   , '')]
            reste_phrase = reste_phrase[position + 1:]
            break
    reste_phrase = recupere_obj_iobj(reste_phrase, vg)

  # on recupere tous les adverbe de la phrase

    vg.advrb = recherche_mot.rech_adv(reste_phrase)
    if modal != []:
        vg.vrb_main = [modal[0] + '+' + vg.vrb_main[0]]
        if modal[0] == 'must' or modal[0] == 'may' or modal[0] == 'can' \
            or modal[0] == 'shall':
            vg.vrb_tense = 'present simple'
        elif modal[0] == 'should' or modal[0] == 'might' or modal[0] \
            == 'could':
            vg.vrb_tense = 'conditionnel simple'
    analyse.sv = vg
    return analyse


# une fonction qui traite les phrase ayant une invertion du sujet


def y_n_ques(
    type_phrase,
    demande,
    phrase,
    position_sujet,
    ):
    modal = []
    analyse = Sentence('', '', [], None)
    vg = Verbal_Group(
        [],
        None,
        '',
        [],
        [],
        [],
        [],
        'affirmative',
        [],
        )

  # recuperer le type de phrase et la demande (qui peut etre vide)

    analyse.data_type = type_phrase
    analyse.aim = demande

  # on recupere l'auxiliaire dans le cas ou on est oblige de le reutiliser

    aux = phrase[0]
    for m in liste_modal:
        if phrase[0] == m:
            modal = [phrase[0]]
    if phrase[1] == 'not':
        vg.state = 'negative'
        sujet = recherche_mot.rech_sujet(phrase, 2)
        if sujet == [] and type_phrase != 'w_question':
            return autre_type_phrase(phrase, type_phrase, demande)
        phrase = phrase[2:]
    else:
        sujet = recherche_mot.rech_sujet(phrase, 1)

    # on recupere la phrase presque sous forme declarative (cela depend si on a un verbe ou pas)

        phrase = phrase[1:]
    while sujet != []:
        analyse.sn = analyse.sn + [recuperer_gr_nom(phrase, sujet, 0)]
        if analyse.sn[len(analyse.sn) - 1].relative != None:
            phrase = phrase[phrase.index(',') + 1:]
        else:

      # on recupere la structure verbale

            phrase = recuperer_phrase.recup_phr_sans_gn(phrase, sujet,
                    phrase.index(sujet[0]))
        while len(phrase) != 0 and phrase[0] == 'of':
            gr_nom = recherche_mot.rech_sujet(phrase, 1)
            phrase = recuperer_phrase.recup_phr_sans_gn(phrase, gr_nom,
                    phrase.index(gr_nom[0]))
        if len(phrase) != 0 and phrase[0] == 'and':
            sujet = recherche_mot.rech_sujet(phrase, 1)
        else:
            sujet = []

  # dans l'absolu le verbe principal est le verbe etre

    if len(phrase) == 0:
        vg.vrb_tense = analyse_verbe.trait_verb(aux, vg.vrb_adv)
        vg.vrb_main = ['be']
    else:
        vg.vrb_adv = recherche_mot.rech_adverbe_verbe(phrase)
        vg.vrb_tense = analyse_verbe.trait_verb_ques(phrase, aux,
                vg.vrb_adv)
        if phrase[0] == 'like' and aux != 'would':
            vg.vrb_main = ['like']
            reste_phrase = phrase[1:]
        else:

      # on garde le meme traitement lors de la phrase declarative

            base_verbe = recherche_mot.rech_verb_ques(phrase,
                    vg.vrb_adv, aux, vg.vrb_tense)
            vg.vrb_main = \
                [convert_string(analyse_verbe.verb_infin(phrase,
                 base_verbe, vg.vrb_tense))]
            if vg.vrb_main != ['be']:
                reste_phrase = recuperer_phrase.recup_res_phr(phrase,
                        base_verbe)
            else:
                reste_phrase = phrase
        if vg.vrb_main == ['be'] and len(reste_phrase) != 0:
            reste_phrase = cas_ph_etat(reste_phrase, vg)

    # on voit s'il y a un verbe secondaire

        if recherche_mot.rech_vrb_scd(reste_phrase, list_preposition) \
            != []:
            verbe_secondaire = recherche_mot.rech_vrb_scd(reste_phrase,
                    list_preposition)
            reste_phrase = \
                reste_phrase[:reste_phrase.index(verbe_secondaire[0])]
            if phrase[phrase.index(verbe_secondaire[0]) - 1] == 'not':
                vg.sv_sec = Verbal_Group(
                    [convert_string(analyse_verbe.verb_infin(phrase,
                     verbe_secondaire, ''))],
                    None,
                    '',
                    [],
                    [],
                    [],
                    [],
                    'negative',
                    [],
                    )
            else:
                vg.sv_sec = Verbal_Group(
                    [convert_string(analyse_verbe.verb_infin(phrase,
                     verbe_secondaire, ''))],
                    None,
                    '',
                    [],
                    [],
                    [],
                    [],
                    'affirmative',
                    [],
                    )
            phrase_secondaire = recuperer_phrase.recup_res_phr(phrase,
                    verbe_secondaire)

      # on recupere tous les adverbe de la phrase

            vg.sv_sec.advrb = recherche_mot.rech_adv(phrase_secondaire)
            phrase_secondaire = recupere_obj_iobj(phrase_secondaire,
                    vg.sv_sec)
        if reste_phrase != [] and reste_phrase[0].endswith('ing'):
            vg.vrb_main[0] = vg.vrb_main[0] + '+' + reste_phrase[0]

    # on voit s'il y a une subordonne

        for w in list_propo_relative:
            if len(reste_phrase) > 0 and reste_phrase[0] == w:
                position = recup_subordonne(reste_phrase)
                phrase_subordonne = reste_phrase[:position]
                vg.vrb_sub_sentence = vg.vrb_sub_sentence \
                    + [autre_type_phrase(phrase_subordonne[1:],
                       'subordonne', '')]
                reste_phrase = reste_phrase[position + 1:]
                break
        reste_phrase = recupere_obj_iobj(reste_phrase, vg)

    # on recupere tous les adverbe de la phrase

        vg.advrb = recherche_mot.rech_adv(reste_phrase)
    if modal != []:
        vg.vrb_main = [modal[0] + '+' + vg.vrb_main[0]]
        if modal[0] == 'must' or modal[0] == 'may' or modal[0] == 'can' \
            or modal[0] == 'shall':
            vg.vrb_tense = 'present simple'
        elif modal[0] == 'should' or modal[0] == 'might' or modal[0] \
            == 'could':
            vg.vrb_tense = 'conditionnel simple'
    analyse.sv = vg
    return analyse


# quelque w_question se traitent de la meme maniere


def w_quest_standar(
    type_phrase,
    demande,
    phrase,
    position_sujet,
    ):

  # en prenant la phrase sans l'amorce (when,where,what...) elle a la forme de y_n_question

    return y_n_ques(type_phrase, demande, phrase[position_sujet - 1:],
                    1)


# pour les questions avec where


def w_quest_where(
    type_phrase,
    demande,
    phrase,
    position_sujet,
    ):

  # dans le cas ou on a from a la fin de la phrase = question sur l'origine

    if phrase[len(phrase) - 1] == 'from':
        return y_n_ques(type_phrase, 'origin', phrase[position_sujet
                        - 1:], position_sujet - 1)
    else:
        return y_n_ques(type_phrase, demande, phrase[position_sujet
                        - 1:], position_sujet - 1)


# pour la question what avec happened comme verbe, peut recuperer que la partie verbale sans verbe


def w_quest_happened(type_phrase, demande, phrase):
    modal = []
    analyse = Sentence('', '', [], None)
    vg = Verbal_Group(
        [],
        None,
        '',
        [],
        [],
        [],
        [],
        'affirmative',
        [],
        )

  # recuperer le type de phrase et la demande (qui peut etre vide)

    analyse.data_type = type_phrase
    analyse.aim = demande
    for m in liste_modal:
        if phrase[1] == m:
            modal = [phrase[1]]
    vg.vrb_tense = 'past simple'
    vg.vrb_main = [convert_string(modal + ['happen'])]
    if modal != [] and len(phrase) != 4:
        reste_phrase = phrase[4:]
    elif modal == [] and len(phrase) != 2:
        reste_phrase = phrase[2:]
    else:
        reste_phrase = []
    reste_phrase = recupere_obj_iobj(reste_phrase, vg)

  # on recupere tous les adverbe de la phrase

    vg.advrb = recherche_mot.rech_adv(reste_phrase)
    if modal != []:
        if modal[0] == 'must' or modal[0] == 'may' or modal[0] == 'can' \
            or modal[0] == 'shall':
            vg.vrb_tense = 'present simple'
        elif modal[0] == 'should' or modal[0] == 'might' or modal[0] \
            == 'could':
            vg.vrb_tense = 'conditionnel simple'
    analyse.sv = vg
    return analyse


# pour la question what au sujet d'explication de probleme


def w_quest_prob(type_phrase, demande, phrase):
    modal = []
    analyse = Sentence('', '', [], None)
    vg = Verbal_Group(
        [],
        None,
        '',
        [],
        [],
        [],
        [],
        'affirmative',
        [],
        )

  # recuperer le type de phrase et la demande (qui peut etre vide)

    analyse.data_type = type_phrase
    analyse.aim = demande
    for m in liste_modal:
        if phrase[1] == m:
            modal = [phrase[1]]
            phrase = [phrase[0]] + phrase[2:]
    vg.vrb_main = [convert_string(modal + ['be'])]
    vg.vrb_tense = analyse_verbe.trait_verb([phrase[1]], vg.vrb_adv)
    if phrase[1] == 'not':
        vg.state = 'negative'
    reste_phrase = phrase[phrase.index('with') + 1:]
    reste_phrase = recupere_obj_iobj(reste_phrase, vg)

  # on recupere tous les adverbe de la phrase

    vg.advrb = recherche_mot.rech_adv(reste_phrase)
    if modal != []:
        if modal[0] == 'must' or modal[0] == 'may' or modal[0] == 'can' \
            or modal[0] == 'shall':
            vg.vrb_tense = 'present simple'
        elif modal[0] == 'should' or modal[0] == 'might' or modal[0] \
            == 'could':
            vg.vrb_tense = 'conditionnel simple'
    analyse.sv = vg
    return analyse


# une fonction liee au kind et type


def w_quest_class(
    type_phrase,
    demande,
    phrase,
    frt_wd,
    position_sujet,
    ):
    if len(phrase) > 6 and phrase[5] == 'not':
        if recherche_mot.rech_sujet(phrase, 6) != []:

      # si apres le kind ou le type on a une forme de yes no question

            return y_n_ques(type_phrase, demande + '+'
                            + phrase[position_sujet],
                            phrase[position_sujet + 1:], 6)
        else:

      # si apres le kind ou le type on a une forme de phrase declarative

            return autre_type_phrase(['the'] + phrase[3:], type_phrase,
                    demande + '+' + phrase[3])
    else:
        for j in frt_wd:
            if phrase[4] == j[0]:
                if j[1] == '2':

          # si apres le kind ou le type on a une forme de yes no question

                    return y_n_ques(type_phrase, demande + '+'
                                    + phrase[position_sujet],
                                    phrase[position_sujet + 1:], 1)

    # si apres le kind ou le type on a une forme de phrase declarative

        return autre_type_phrase(['the'] + phrase[3:], type_phrase,
                                 demande + '+' + phrase[3])


# dans tous les autres cas de what_question on utilise cette fonction


def w_quest_what(type_phrase, phrase, position_sujet):
    a = y_n_ques(type_phrase, 'thing', phrase[position_sujet - 1:], 1)
    if a.sv.vrb_main == ['think+of'] or a.sv.vrb_main == ['think+about'
            ]:
        a.aim = 'opinion'
    elif (a.sv.vrb_main == ['like'] or a.sv.vrb_main == ['look+like']) \
        and not a.sv.vrb_tense.endswith('conditionnel'):
        a.aim = 'descrition'
    elif a.sv.vrb_main == ['do'] and a.sv.i_cmpl != [] \
        and a.sv.i_cmpl[0].nominal_group[0].noun[0].endswith('ing'):
        a.aim = 'explication'
    return a


# pour les how question


def w_quest_how(type_phrase, phrase):
    analyse = w_quest_standar(type_phrase, 'manner', phrase, 2)
    if analyse.sv.vrb_main[0] == 'like':
        analyse.aim = 'opinion'
    return analyse


# pour les how many ou how much


def w_quest_quant(
    type_phrase,
    demande,
    phrase,
    frt_wd,
    ):
    for j in frt_wd:
        if phrase[2] == j[0]:
            if j[1] == '2':

        # si apres le kind ou le type on a une forme de yes no question

                return y_n_ques(type_phrase, demande, phrase[2:], 1)
    for i in frt_wd:
        if phrase[3] == i[0]:
            if i[1] == '2':
                if len(phrase) > 5 \
                    and (recherche_mot.rech_sujet(phrase, 4) != []
                         or phrase[4] == 'not'
                         and recherche_mot.rech_sujet(phrase, 5) != []):
                    a = y_n_ques(type_phrase, demande, phrase[3:], 1)
                    a.sv.d_obj = [Nominal_Group([], [phrase[2]], [],
                                  [], None)]
                    return a

  # si apres le kind ou le type on a une forme de phrase declarative

    return autre_type_phrase(['a'] + phrase[2:], type_phrase, demande)


def w_how_invit(type_phrase, demande, phrase):
    phrase[1] = 'is'
    return w_quest_standar(type_phrase, demande, phrase, 2)


# fonction pour les question avec whose


def w_quest_whose(type_phrase, demande, phrase):
    analyse = Sentence('', '', [], None)
    vg = Verbal_Group(
        [],
        None,
        '',
        [],
        [],
        [],
        [],
        'affirmative',
        [],
        )

  # recuperer le type de phrase et la demande (qui peut etre vide)

    analyse.data_type = type_phrase
    analyse.aim = demande
    vg.vrb_main = ['be']

  # on transforme la question en un groupe nominal

    phrase[0] = 'that'

  # la position du sujet est au debut

    sujet = recherche_mot.rech_sujet(phrase, 0)
    while sujet != []:
        analyse.sn = analyse.sn + [recuperer_gr_nom(phrase, sujet, 0)]

    # on recupere la structure verbale

        phrase = recuperer_phrase.recup_phr_sans_gn(phrase, sujet,
                phrase.index(sujet[0]))
        while len(phrase) != 0 and phrase[0] == 'of':
            gr_nom = recherche_mot.rech_sujet(phrase, 1)
            phrase = recuperer_phrase.recup_phr_sans_gn(phrase, gr_nom,
                    phrase.index(gr_nom[0]))
        if len(phrase) != 0 and phrase[0] == 'and':
            phrase[0] = 'that'
            sujet = recherche_mot.rech_sujet(phrase, 0)
        else:
            sujet = []
    if phrase[1] == 'not':
        vg.state = 'negative'
    analyse.sv = vg
    return analyse


# fonction pour les question avec which


def w_quest_which(type_phrase, demande, phrase):

  # en faisant un changement au debut de phrase, on recupere une phrase declarative

    phrase[0] = 'a'
    return autre_type_phrase(phrase, type_phrase, demande)


# ces fonctions permettent de trouver les phrases ayant un type uniquement tel que l'amorce


def phr_amorce():
    return Sentence('amorce', '', [], None)


def phr_agr_disa(type_phrase):
    return Sentence(type_phrase, '', [], None)


def phrase_condi(phrase):
    phrase_conditionnel = phrase[:phrase.index(',')]
    a = autre_type_phrase(phrase[phrase.index(',') + 1:], 'statement',
                          '')
    a.sv.vrb_sub_sentence = [autre_type_phrase(phrase_conditionnel,
                             'condition', '')]
    return a


def interjection(type_phrase):
    return Sentence(type_phrase, '', [], None)


def thank():
    return Sentence('gratulation', '', [], None)



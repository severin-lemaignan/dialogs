# -*- coding: utf-8 -*-

#SVN rev.203 + Python Tidy + Use of ResourcePool

from resources_manager import ResourcePool
import reconstitution_phrase

list_verb_irreg = ResourcePool().irregular_verbs

liste_modal = [
    'can',
    'could',
    'must',
    'should',
    'may',
    'might',
    'shall',
    ]
verbe_ing = [('prepare', 'preparing'), ('take', 'taking')]


def reconstitution_sn(struc_nomi):
    gr_nom = []
    if struc_nomi:
        gr_nom +=   struc_nomi.det if struc_nomi.det else [] + \
                    struc_nomi.adj if struc_nomi.adj else [] + \
                    struc_nomi.noun
        if struc_nomi.noun_cmpl:
            gr_nom += ['of']
            gr_nom += reconstitution_sn(struc_nomi.noun_cmpl[0])
        return gr_nom

def gr_nominal(gn):
    phr = []
    if gn:
        for i in gn:
            phr = phr + reconstitution_sn(i)
            if i.relative:
                phr = phr \
                    + reconstitution_phrase.relative_sentence(i.relative)
                phr = phr + [',']
            phr = phr + ['and']
        phr = phr[:len(phr) - 1]
    return phr


def reconsitu_indirect_compl(indirect_compl):
    gr_ind_cmpl = []
    if indirect_compl:
        for i in indirect_compl:
            if i.prep:
                gr_ind_cmpl += i.prep + gr_nominal(i.nominal_group)
            else:
                if i.nominal_group[0].adj \
                    and (i.nominal_group[0].adj[0] == 'last'
                         or i.nominal_group[0].adj[0] == 'next'):
                    gr_ind_cmpl += gr_nominal(i.nominal_group)
                else:
                    gr_ind_cmpl += ['to'] + gr_nominal(i.nominal_group)
    return gr_ind_cmpl


def conjug_verb(temps, verbe, sn):
    if temps == '':
        temps = 'present simple'
    if sn == []:
        if verbe[0] == 'be':
            return ['is'] + verbe[1:]
        return verbe
    if temps == 'present simple':
        if len(sn) > 1 or sn[0].noun[0].endswith('s') or sn[0].noun \
            == ['we'] or sn[0].noun == ['I'] or sn[0].noun == ['you'] \
            or sn[0].noun == ['they']:
            if verbe[0] == 'be':
                if sn[0].noun == ['I']:
                    return ['am'] + verbe[1:]
                else:
                    return ['are'] + verbe[1:]
            return verbe
        if verbe[0] == 'be':
            return ['is'] + verbe[1:]
        if verbe[0] == 'do':
            return ['does'] + verbe[1:]
        return [verbe[0] + 's'] + verbe[1:]
    elif temps == 'present progressive':
        for m in verbe_ing:
            if m[0] == verbe[0]:
                return conjug_verb('past simple', ['be'], sn) + [m[1]] \
                    + verbe[1:]
        return conjug_verb('present simple', ['be'], sn) + [verbe[0]
                + 'ing'] + verbe[1:]
    elif temps == 'past simple':
        if verbe[0] == 'be':
            if len(sn) > 1 or sn[0].noun[0].endswith('s') or sn[0].noun \
                == ['we'] or sn[0].noun == ['I'] or sn[0].noun == ['you'
                    ] or sn[0].noun == ['they']:
                return ['were'] + verbe[1:]
            else:
                return ['was'] + verbe[1:]
        for i in list_verb_irreg:
            if verbe[0] == i[0]:
                return [i[1]] + verbe[1:]
        return [verbe[0] + 'ed'] + verbe[1:]
    elif temps == 'past progressive':
        for m in verbe_ing:
            if m[0] == verbe[0]:
                return conjug_verb('past simple', ['be'], sn) + [m[1]] \
                    + verbe[1:]
        return conjug_verb('past simple', ['be'], sn) + [verbe[0]
                + 'ing'] + verbe[1:]
    elif temps == 'present perfect':
        if len(sn) > 1 or sn[0].noun[0].endswith('s') or sn[0].noun \
            == ['we'] or sn[0].noun == ['I'] or sn[0].noun == ['you'] \
            or sn[0].noun == ['they']:
            for i in list_verb_irreg:
                if verbe[0] == i[0]:
                    return ['have'] + [i[2]] + verbe[1:]
            return ['have'] + [verbe[0] + 'ed'] + verbe[1:]
        else:
            for i in list_verb_irreg:
                if verbe[0] == i[0]:
                    return ['has'] + [i[2]] + verbe[1:]
            return ['has'] + [verbe[0] + 'ed'] + verbe[1:]
    elif temps == 'futur simple':
        return ['will'] + verbe
    return []


def inserer_adv(vrb, adverbe, temps):
    if temps == 'present simple' or temps == 'past simple':
        return adverbe + vrb
    else:
        return [vrb[0]] + adverbe + vrb[1:]


def conjuguer_verbe_sent(
    temps,
    verbe,
    adverbe,
    sn,
    state,
    ):
    if state == 'negative':
        for i in liste_modal:
            if i == verbe[0]:
                return [verbe[0]] + ['not'] + adverbe + verbe[1:]
        if verbe[0] == 'be':
            return conjug_verb(temps, [verbe[0]], sn) + ['not'] \
                + adverbe + verbe[1:]
        else:
            if temps == 'present progressive':
                for m in verbe_ing:
                    if m[0] == verbe[0]:
                        return conjug_verb('present simple', ['be'],
                                sn) + ['not'] + adverbe + [m[1]] \
                            + verbe[1:]
                return conjug_verb('present simple', ['be'], sn) \
                    + ['not'] + adverbe + [verbe[0] + 'ing'] + verbe[1:]
            elif temps == 'past progressive':
                for m in verbe_ing:
                    if m[0] == verbe[0]:
                        return conjug_verb('present simple', ['be'],
                                sn) + ['not'] + adverbe + [m[1]] \
                            + verbe[1:]
                return conjug_verb('past simple', ['be'], sn) + ['not'] \
                    + adverbe + [verbe[0] + 'ing'] + verbe[1:]
            return conjug_verb(temps, ['do'], sn) + ['not'] + adverbe \
                + verbe
    else:
        for i in liste_modal:
            if i == verbe[0]:
                return [verbe[0]] + adverbe + verbe[1:]
        return inserer_adv(conjug_verb(temps, verbe, sn), adverbe,
                           temps)


def conjuguer_verbe_ques(
    sn,
    temps,
    verbe,
    phrase,
    adverbe,
    ):
    if verbe[0] == 'be':
        return conjug_verb(temps, ['be'], sn) + phrase + adverbe \
            + verbe[1:]
    for i in liste_modal:
        if i == verbe[0]:
            return [i] + phrase + adverbe + verbe[1:]
    if temps == 'present simple':
        if len(sn) > 1 or sn[0].noun[0].endswith('s') or sn[0].noun \
            == ['we'] or sn[0].noun == ['I'] or sn[0].noun == ['you'] \
            or sn[0].noun == ['they']:
            return ['do'] + phrase + adverbe + verbe
        else:
            return ['does'] + phrase + adverbe + verbe
    if temps == 'past simple':
        return ['did'] + phrase + adverbe + verbe
    elif temps == 'futur simple':
        return ['will'] + phrase + adverbe + verbe
    elif temps == 'present perfect':
        if len(sn) > 1 or sn[0].noun[0].endswith('s') or sn[0].noun \
            == ['we'] or sn[0].noun == ['I'] or sn[0].noun == ['you'] \
            or sn[0].noun == ['they']:
            for i in list_verb_irreg:
                if verbe[0] == i[0]:
                    return ['have'] + phrase + adverbe + [i[2]] \
                        + verbe[1:]
            return ['have'] + phrase + adverbe + [verbe[0] + 'ed'] \
                + verbe[1:]
        else:
            for i in list_verb_irreg:
                if verbe[0] == i[0]:
                    return ['has'] + phrase + adverbe + [i[2]] \
                        + verbe[1:]
            return ['has'] + phrase + adverbe + [verbe[0] + 'ed'] \
                + verbe[1:]
    elif temps == 'present progressive':
        for m in verbe_ing:
            if m[0] == verbe[0]:
                return conjug_verb('present simple', ['be'], sn) \
                    + phrase + adverbe + [m[1]] + verbe[1:]
        return conjug_verb('present simple', ['be'], sn) + phrase \
            + adverbe + [verbe[0] + 'ing'] + verbe[1:]
    elif temps == 'past progressive':
        for m in verbe_ing:
            if m[0] == verbe[0]:
                return conjug_verb('past simple', ['be'], sn) + phrase \
                    + adverbe + [m[1]] + verbe[1:]
        return conjug_verb('past simple', ['be'], sn) + phrase \
            + adverbe + [verbe[0] + 'ing'] + verbe[1:]



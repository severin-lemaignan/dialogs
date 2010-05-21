#!/usr/bin/python
# -*- coding: utf-8 -*-
#SVN:rev202

from dialog.resources_manager import ResourcePool

list_aux=[('do',1), ('does',1), ('can',1), ('are',1), ('is',1),('am',1),
          ('did',2), ('was',2), ('were',2), ('have',3), ('has',3), ('had',4),
          ('will',5), ('would',6)]
verbe_ing=[('prepare','preparing'), ('take','taking')]

list_verb_irreg = ResourcePool().irregular_verbs
list_phra_verb = ResourcePool().preposition_verbs

#cette fonction renvoie le temps de conjugaison du verbe et donc le temps de la phrase
def trait_verb (phrase, adverbe):
  if phrase[len(adverbe)].endswith('ed'):
    return 'past simple'
  #dans le cas ou le passe a la meme forme que le present on prend le present
  for i in list_verb_irreg:
    if phrase[len(adverbe)]==i[1]: 
      if i[1]==i[0]:
        return 'present simple'
      else:
        return 'past simple'
  #ici il faut distinguer le present perfect
  if phrase[0]=='have' or phrase[0]=='has':
    if phrase[1+len(adverbe)].endswith('ed'):
      return 'present perfect'
    for i in list_verb_irreg:
      if phrase[1+len(adverbe)]==i[2]:
        return 'present perfect'
  #ici il faut distinguer le past perfect
  if phrase[0]=='had':
    if phrase[1+len(adverbe)].endswith('ed'):
      return 'past perfect'
    for i in list_verb_irreg:
      if phrase[1+len(adverbe)]==i[2]:
        return 'past perfect'
  #distinction des temps progressive
  if phrase[0]=='is' or phrase[0]=='are' or phrase[0]=='am':
    if len(phrase)!=1 and phrase[1+len(adverbe)].endswith('ing'):
      return 'present progressive'
  if phrase[0]=='was' or phrase[0]=='were':
    if len(phrase)!=1 and phrase[1+len(adverbe)].endswith('ing'):
      return 'past progressive'
  #pour le future
  if phrase[0]=='will':
    return 'futur simple'
  #le temps conditionnel
  if phrase[0]=='would':
    if trait_verb(phrase[1:], adverbe)=='present simple':
      return 'present conditionnel'
    else:
      return 'past conditionnel'
  #par defaut on revoie le present
  return 'present simple'

#cette fonction nous permet de recuperer le verbe sous sa forme infinitif
def infinitif (verbe, temps):
  if temps=='present simple':
    if verbe[0]=='is' or verbe[0]=='are' or verbe[0]=='am':
      return ['be']
    elif verbe[0]=='has':
      return ['have']
    elif verbe[0].endswith('s'):
      return [verbe[0][0:len(verbe[0])-1]]
  elif temps=='past simple':
    for i in list_verb_irreg:
      if i[1]==verbe[0]:
        return [i[0]]
    if verbe[0].endswith('ed'):
      return [verbe[0][0:len(verbe[0])-2]]
  elif temps=='futur simple':
    return verbe
  elif temps=='present perfect' or temps=='past perfect':
    for i in list_verb_irreg:
      if i[2]==verbe[0]:
        return [i[0]]
    if verbe[0].endswith('ed'):
      return [verbe[0][0:len(verbe[0])-2]]
  elif temps=='present progressive' or temps=='past progressive':
    for x in verbe_ing:
      if x[1]==verbe[0]:
        return [x[0]]
    return [verbe[0][0:len(verbe[0])-3]]
  elif temps=='present conditionnel':
    return infinitif (verbe, 'present simple')
  elif temps=='past conditionnel':
    return infinitif (verbe, 'past simple')
  return verbe

#dans le cas ou le verbe correspond a un verbe avec preposition on recupere tout le groupe
def verb_infin (phrase, base_verbe, temps):
  verbe=infinitif(base_verbe, temps)
  if phrase[len(phrase)-1]!=base_verbe[0]:
    #on renvoie le verbe avec la preposition
    for i in list_phra_verb:
      if verbe[0]==i[0]:
        if phrase[phrase.index(base_verbe[0])+1]==i[1]:
          if phrase[phrase.index(base_verbe[0])+1]!=phrase[len(phrase)-1]:
            if phrase[phrase.index(base_verbe[0])+2]==i[2]:
              return verbe+ [phrase[phrase.index(base_verbe[0])+1]] + [phrase[phrase.index(base_verbe[0])+2]]
            else:
              return verbe+ [phrase[phrase.index(base_verbe[0])+1]]
          else:
            return verbe+ [phrase[phrase.index(base_verbe[0])+1]]
  #sinon on renvoie le verbe a l'etat noyau
  return verbe

#traitement du temps du verbe (auxiliaire) de la question
def trait_verb_ques (phrase, aux, adverbe):
        if aux=='is' or aux=='are' or aux=='am':
          if phrase[len(adverbe)].endswith('ing'):
            return 'present progressive'
          else:
            return 'present simple'
        elif aux=='was' or aux=='were':
          if phrase[len(adverbe)].endswith('ing'):
            return 'past progressive'
          else:
            return 'past simple'
        elif aux=='have' or aux=='has':
          if phrase[len(adverbe)].endswith('ed'):
            return 'present perfect'
          for i in list_verb_irreg:
            if phrase[len(adverbe)]==i[2]:
              return 'present perfect'
        elif aux=='had':
          if phrase[len(adverbe)].endswith('ed'):
            return 'past perfect'
          for i in list_verb_irreg:
            if phrase[len(adverbe)]==i[2]:
              return 'past perfect'
        elif aux=='will':
          return 'futur simple'
        elif aux=='would':
          return trait_verb (['would']+phrase, adverbe)
        else:
          return trait_verb([aux], [])

  

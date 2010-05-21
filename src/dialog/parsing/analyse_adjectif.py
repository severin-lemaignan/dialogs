#!/usr/bin/python
# -*- coding: utf-8 -*-
#SVN:rev202
"""
ce paquetage nous permet de traiter les adjectif en utilisant des regles
de grammaires definies dans les livres ou bien en faisant des recherches
dans une liste qui contient les adjectifs irreguliers
"""

from resources_manager import ResourcePool

list_adjectif = ResourcePool().adjectives

#trouver des adjectifs pour recuperer la position du nom
def position_adj(phrase, pos_mot):
  if len(phrase)-1==pos_mot:
    return 1
  for i in list_adjectif:
    if phrase[pos_mot]==i:
      position_adj(phrase, pos_mot+1)
      return 1+ position_adj(phrase, pos_mot+1)
  if phrase[pos_mot].endswith('al'):
    return 1+position_adj(phrase, pos_mot+1)
  if phrase[pos_mot].endswith('est'):
    return 1+position_adj(phrase, pos_mot+1)
  if phrase[pos_mot].endswith('ous'):
    return 1+position_adj(phrase, pos_mot+1)
  if phrase[pos_mot].endswith('ing'):
    return 1+position_adj(phrase, pos_mot+1)
  return 1

#recuperer les adjectifs lies a un groupe nominal
def recuperer_adj(gr_nom):
    for i in list_adjectif:
      if i==gr_nom[0]:
        list_adj=gr_nom[0:]
        break
      list_adj=gr_nom[1:]
    list_adj=list_adj[:len(list_adj)-1]
    return list_adj

def reconnaitre_adj(word):
  if word.endswith('al'):
    return 1
  if word.endswith('est'):
    return 1
  if word.endswith('ous'):
    return 1
  if word.endswith('ing'):
    return 1
  for i in list_adjectif:
    if word==i:
      return 1
  return 0

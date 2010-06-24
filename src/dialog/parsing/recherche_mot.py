#SVN:rev202
import analyse_adjectif
import analyse_verbe
list_prono=['you', 'I', 'we', 'he', 'she', 'me', 'it', 'he', 'they']
list_det=['the', 'a', 'an', 'your', 'his', 'my', 'this', 'her', 'their', 'these', 'that', 'every', 'ten']
list_adv=['here','tonight', 'yesterday', 'tomorrow', 'today']
list_verb_eta=['is', 'was', 'were', 'been']
list_cap_let=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

#fonction permettant de recuperer un sujet (on connait sa position au prealable)
def rech_sujet (phrase, pos_dep):
  nb_pos = 1
  #dans le cas ou c'est un prono personnel
  for i in list_prono:
    if phrase[pos_dep]==i:
      return [phrase[pos_dep]]
  #dans le cas ou il ya un groupe nominal
  for j in list_det:
    if phrase[pos_dep]==j:
      nb_pos= nb_pos + analyse_adjectif.position_adj(phrase, pos_dep+1)
      return phrase[pos_dep : nb_pos+pos_dep]
  #dans le cas ou c'est un nom propre ou autre
  for j in list_cap_let:
    if phrase[pos_dep][0]==j:
      return [phrase[pos_dep]]
  if phrase[pos_dep]=='next' or phrase[pos_dep]=='last':
    nb_pos= nb_pos + analyse_adjectif.position_adj(phrase, pos_dep+1)
    return phrase[pos_dep-1 : nb_pos+pos_dep]
  return []

#recuperation du determinant
def rech_det (gr_nom):
  if gr_nom==[]:
    return []
  for j in list_det:
      if gr_nom[0]==j:
        #si le determinant est neutre (en prenant en compte la position du robot)
        return [j]
  return []

#fonction qui renvoie liste des adjectifs d'un groupe nominal
def rech_adj (gr_nom):
  if gr_nom==[]:
    return []
  else:
    for j in list_det:
      if gr_nom[0]==j:
        return analyse_adjectif.recuperer_adj(gr_nom)
    return analyse_adjectif.recuperer_adj(gr_nom)

#fonction nous permettant de recuperer le nom
def recup_nom (sujet, adjec):
  if sujet==[]:
    return []
  for i in list_det:
    if i==sujet[0]:
      return sujet[len(adjec)+1:]
  #s'il s'agit de nom propre ou autres pronos ne concernant pas le robot
  return sujet[len(adjec):]

#on cherche les complement d'objet d'un groupe nominal
def rech_compl_nom (gr_nom, phrase, pos):
  if gr_nom==[]:
    return []
  else:
    if phrase ==[] or len(phrase)<=len(gr_nom)+pos or len(phrase)==len(gr_nom)+pos+1:
      return []
    else:
      #un complement obtenu par l'utilisation de of
      if phrase[pos+len(gr_nom)]=='of':
        return rech_sujet(phrase, pos+len(gr_nom)+1) 
  return []

#on cherche les complement d'objet d'un groupe nominal
def rech_relative (gr_nom, phrase, pos, liste_relative):
  if gr_nom==[]:
    return 0
  else:
    if phrase ==[] or len(phrase)==len(gr_nom)+pos or len(phrase)==len(gr_nom)+pos+1:
      return 0
    else:
      #un complement obtenu par l'utilisation de of
      for i in liste_relative:
        if i == phrase[pos+len(gr_nom)]:
          return pos+len(gr_nom)
        elif phrase[pos]=='and' and i == phrase[pos+len(gr_nom)+1]:
          return pos+len(gr_nom)
  return 0

#rechercher un adverbe lie au verbe
def rech_adverbe_verbe (phrase):
  if phrase==[]:
    return []
  if phrase[0]=='have' or phrase[0]=='has' or phrase[0]=='will' or phrase[0]=='had':
    if phrase[1].endswith('ly'):
        return [phrase[1]]
  else:
    if phrase[0].endswith('ly'):
      return [phrase[0]]
  return []

#on recherche le verbe principal de la phrase
def rech_verb (phrase, temps):
  if len(phrase)==0:
    return []
  if temps=='present simple' or temps=='past simple':
    return [phrase[0]]
  if temps=='present perfect' or temps=='futur simple' or temps=='past perfect':
    return [phrase[1]]
  if temps=='present progressive' or temps=='past progressive':
    return [phrase[1]]
  if temps=='present conditionnel' or temps=='past conditionnel':
    return [phrase[1]]

#fonction permettant de chercher un groupe nominal sachant qu'on connait pas la position
def rech_SN (reste_phrase):
  nb_position=1
  if reste_phrase ==[]:
    return []
  for x in reste_phrase:
    #dans le cas ou c'est un prono personnel
    for y in list_prono:    
      if x==y:
        return [reste_phrase[reste_phrase.index(x)]]
    for j in list_det:
      if x==j:
        nb_position= nb_position + analyse_adjectif.position_adj(reste_phrase, reste_phrase.index(x)+1)
        return reste_phrase[reste_phrase.index(x) : reste_phrase.index(x)+nb_position]
    #dans le cas ou c'est un nom propre ou autre
    for n in list_cap_let:
      if x[0]==n:
        return [reste_phrase[reste_phrase.index(x)]]
    #il s'agit d'un comple circon, donc on le recupere en tant que groupe nominal
    if (x=='last' or x=='next') and reste_phrase[reste_phrase.index(x)+1]!='to':
      reste_phrase[reste_phrase.index(x)]='the'
      if rech_sujet (reste_phrase, reste_phrase.index('the'))!=[]:
        aux= [x]+(rech_sujet(reste_phrase, reste_phrase.index('the')))[1:]
        reste_phrase[reste_phrase.index('the')]=x
        return aux
  return []

#recherche d'adverbe de temps
def rech_adv (reste_phrase):
  if reste_phrase ==[]:
    return []
  for i in reste_phrase:
    for j in list_adv:
      if j==i:
        return [i]+rech_adv(reste_phrase[reste_phrase.index(i)+1:])
  for k in reste_phrase:
    if k.startswith('every'):
        return [k]+rech_adv(reste_phrase[reste_phrase.index(k)+1:])
  return []

#recherche du verbe principal dans une question
def rech_verb_ques (phrase, adv, aux, temps):
  if len(phrase)==0:
    return []
  if temps=='present progressive' or temps=='past progressive':
    return [phrase[0+len(adv)]]
  if aux=='is' or aux=='are' or aux=='am':
    if temps=='present simple':
      return [aux]
  elif aux=='was' or aux=='were':
    if temps=='past simple':
      return [aux]
  else:
    return [phrase[0+len(adv)]]
  return []
                
#recherche de verbe non conjugue dans la phrase
def rech_vrb_scd(phrase, list_preposition):
  for i in phrase:
    if i=='to':
      for j in list_preposition:
        if j==phrase[phrase.index(i)+1]:
          return []
      if rech_sujet (phrase, phrase.index(i)+1)==[] and rech_adv([phrase[phrase.index(i)+1]])==[]:
        return [phrase[phrase.index(i)+1]]
  return []

def verbe_action_etat(reste_phrase, list_preposition):
  for i in list_preposition:
    if i==reste_phrase[0]:
      return 1
  for j in list_adv:
    if j==reste_phrase[0]:
      return 1
  return 0



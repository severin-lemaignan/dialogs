#SVN:rev202
list_adv_amor=[('hi',1), ('hello',1), ('good',2)]
list_agree=['ok', 'nice', 'good', 'yes', 'OK', 'oK']
list_disagree=['no', 'sorry']

#fonction permettant de recuperer le structure verbale
def recup_phr_sans_gn(phrase, gr_nom, position_gr_nom):
  if gr_nom!=[]:
    return phrase[position_gr_nom+len(gr_nom):]
  return []


#dans le cas ou il s'agit d'une salutation
def amorcer (phrase):
  for i in list_adv_amor:
    if phrase[0]==i[0]:
      if i[1]==1:
        return [phrase[0]]
      elif i[1]==2:
        return phrase[0:2]
  return []

#recuperer une reponse negative ou positive
def repondre (phrase):
  for i in list_agree:
    if phrase[0]==i:
      return 'agree'
  for j in list_disagree:
    if phrase[0]==j:
      return 'disagree'
  return ''

#fonction qui nous permet de prendre la partie de la phrase apres le verbe principal
def recup_res_phr (phrase, verbe):
  if verbe==[]:
    return phrase
  return phrase[phrase.index(verbe[0])+len(verbe):]

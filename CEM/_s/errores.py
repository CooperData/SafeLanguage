#!/usr/bin/env python
# -*- coding: utf-8  -*-

# conda execute
# env:
#  - python >=3

import sys, getopt, re
from operator import itemgetter
import excluidos

reg = re.compile('_')                                                        
alpha = '[-a-zæǣçäëöüãâêàèìòùáéíóúñžŕA-ZÆÇÄËÖÜÃÂÊÀÈÌÒÙÁÉÍÓÚÑŽŔß_/ÐðŜŝĒēŠšÏïÞþÔôÕõŁłŌōŢţςйкŋνā]'

def lemaB(pat,src, pres='',posts=''):
    """match patterns"""                                                        
    #print "Wrong pattern: %s" % (pat)                                          
    p = reg.split(pat)
    if len (p) < 4:
        print ("Wrong pattern: %s" % (pat))
        #raise LemaExc(pat)                                                     
    if len (p) == 5:
        fl = '(?i)'
    else:
        fl = ''
    #Contexts                                                                   
    # url: '(?<!http:[\w/\-_%?&=(),]+)'                                       
    # interwiki:(?!\[\[\w+\:[^\[\]]*)                                           
    #return [(fl + '([^\w/áéíóúñÁÉÍÓÚÑ]' + p[0] + ')' + p[3] +              
    #        '(' + p[2] + '[^\w/áéíóúñÁÉÍÓÚÑ])',                            
    #        '\1' + p[1] + '\2')]                                           
    res =( [ [pres+p[0] + p[3] + p[2]+posts, src, 0] ])
    #print (res)
    return res


qte = re.compile("[']")
def lema(pat, pre=None, xpre=None, xpos=None):
  src = "lema(ur\'"+qte.sub("\\'",pat)+"\'"
  if pre is None:
    pre=''
  else:
    src+= ", pre=ur'"+pre+"'"
  xpres=''
  if xpre is not None:
      xpre.sort() 
      src+=", xpre=["
      for p in xpre:
          xpres += "(?<!"+p+")"
          src+="ur\'"+qte.sub("\\'",p)+"\', "
      src+="]"
  xposs=''
  if xpos is not None:
      xpos.sort()
      src+=", xpos=["
      for p in xpos:
          xposs += "(?!"+p+")"
          src+="ur\'"+qte.sub("\\'",p)+"\', "
      src+="]"
  src+=") + "
  #print (src)
  #print(pat)
#  return lemaB(pat,'(?<!' + alpha + ')(', ')(?!' + alpha + ')')
  return lemaB(pre+pat, src, xpres, xposs)
def retro(pat):
  return []




noCorregirEn = [
    '(?i)(?:(?:[Ii]magen?|[Ff]ile|[Aa]rchivo):[^\|\]]+(?=[\]\|]))',
    '(?i)(?:(?:https?|mailto|ftp)://[\w@/%.\$\-_¿?&=:;\'\~+,()#]+)',
    '(?i)(?:(?<=\[\[):?[-a-z]+:[^\]]+(?=\]\]))',
    '(?i)(?:\[\[ *[Cc]ategor(?:y|ía) *:[^\]]*\]\])',
    '(?i)style *= *\"[^\"]*\"',
    '(?i)<\!--[\s\S]*?-->', #Demasiado lento
    '(?i)<(ref|source|syntaxhighlight|math|code|pre|cite|blockquote|nowiki|timeline|gallery|poem)[^>]*/>', 
    '(?i)<(ref|source|syntaxhighlight|math|code|pre|cite|blockquote|nowiki|timeline|gallery|poem)[^>]*>[\s\S]*?</\1>', 
    '(?i)\{\{ *(?:audio|nihongo|lang|gMaps|fusionar|cita(?: web|)|AFI|c?qoute|desambiguacion|vocabulario portuñol|interproyecto|ipr|info|ordenar|defaultsort|NF|traducido ref|panorama|commonscat|imagen|PAGENAME|commons|indice|ta|cita libro|Galería de imágenes|sort)[^{}]*?\}\}',
    '(?i)\|\s*[- _a-z0-9áéíóúü]*\s*=',
    '«[^»]+»',
]
def compilar():
  flags = re.UNICODE
  pat = ''
  for i in range(len(noCorregirEn)):
    p = noCorregirEn[i]
    noCorregirEn[i] = re.compile(p,flags)
  for i in range(len(lemas)):
    p=lemas[i][0]
    pat = pat + '|' + p
    lemas[i][0]=re.compile('(?<!' + alpha + ')('+p+')(?!' + alpha + ')',flags)
  pat = '(?<!' + alpha + ')(?P<c>'+pat[1:]+')(?!' + alpha + ')'
#  trans = '(.*?)\\b(?P<l>.{0,40})'+pat+'(?P<r>.{0,40})\\b(.*?)'
  trans = '(?P<l>.*)'+pat+'(?P<r>.*)'
  val = '...\\g<l>\'\'\'\\g<c>\'\'\'\\g<r>...'
  #print (pat)
  return (re.compile(pat,flags),re.compile(trans,flags),val)

#Cambios ambiguos

lemasFileName = 'Los.lem'
# lemasPos= [##Eliminar ur y cambiar \b por \\b
# lema(ur'[Mm]_a_s [a-záéíóúñ]+') + 
# []][0]

lemas= [##Eliminar ur y cambiar \b por \\b
    
lema('(?:[Aa]|[Dd]e)__l (?:equipo|resto|primer|grupo|pueblo|personaje|nombre|[Rr]ey|programa|club|presidente|nuevo|álbum|municipio|planeta|número|estado|centro|trabajo|productor|padre|mundo|lugar|jugador|gobierno|país|margen|juego|incremento|gran|estudio|elenco|desarrollo|cuarto|antiguo|verdadero|usuario|[uú]ltimo|tema|poder|oeste|momento|español|otro|entonces)_ e', xpre=['(?:[Ll]ado|[Cc]ara) ', '\.', ]) + #287
lema('(?:[Ee]nero|[Ff]ebrero|[Mm]arzo|[Aa]bril|[Mm]ayo|[Jj]unio|[Jj]ulio|[Aa]gosto|[Ss]eptiembre|[Oo]ctubre|[Nn]oviembre|[Dd]iciembre)_ de_ (?:\[\[|)[1-9][0-9][0-9][0-9]_(?:,|)', xpre=['Ediciones del 4 de '], xpos=[' sullo']) + #29662
lema('(?:[Ss]emi|[Ss]ub|[Hh]iper|[Dd])esarrollar_í_a[ns]?_i') + #1
lema('Gim_é_nez_e', xpre=['Antônio ']) + #166
lema('Hait_í__i', pre='(?:\||(?:[Dd]e|[Ee]n) )', xpre=['Démocratie ', 'Volleyball '], xpos=[' (?:Sings|and)']) + #51
lema('Jim_é_nez_e', xpre=['Cláudia ']) + #420
lema('M_é_xico_e', pre='(?:[Dd]e|[Ee]n|[Ss]obre|[Pp]ara|[Pp]or|[Tt]odo) ', xpre=['Chanteur ', 'Audrain ', 'Bassin ', 'Humaines ', 'Histoire ', ], xpos=[' (?:Herpetology|City|Beach)', '[\']s', ]) + #476
lema('Medell_í_n_i', xpre=['in ', '366272\) ']) + #312
lema('Ocean_í_a_i', pre='(?:[Dd]e|[Ee]n) ', xpos=[' (?:Cruises|Rugby)']) + #5
lema('[Aa]bogac_í_as?_i', xpos=['\.es']) + #2
lema('[Aa]d_h_esivos?_', xpre=['[Cc]aso ']) + #6
lema('[Aa]narqu_í_as?_i', xpre=['amor i ']) + #13
lema('[Aa]nomal_í_as?_i', xpre=['Pichia ']) + #10
lema('[Aa]rt_í_culo_i', xpos=[' (?:mortis|meni)', ]) + #465
lema('[Aa]scen_s_ión_c', xpos=[' (?:Aguilera|[AÁ]lvarez|Alcalá|Andrade|Bonet|De los Santos|Farreras|García|Gómez|Hernández|Lencina|López|Martínez|Negrón|Nicol|Orihuela|Saucedo|Soto|Solórsano|Tepal|Vázquez)']) + #16
lema('[Aa]utom_ó_vil(?:es|)_o', xpos=[' Gesellschaft']) + #57
lema('[Bb]ater_í_as?_i', xpre=['[Rr]ainha de ']) + #171
lema('[Bb]iogeogr_á_fic[ao]s?_a', xpre=['\\bdi ']) + #8
lema('[Bb]istur_í__i', xpre=['\\bO '], xpos=[' - La', ', la']) + #1
lema('[Cc]_ó_digo_o', xpre=['<'], xpos=[' (?:Group|commercial|Manuelino|Afonsino)']) + #164
lema('[Cc]_ó_ptic[ao]s?_o', xpre=['Ptychotis ']) + #1
lema('[Cc]aminar_í_a_i', xpre=['Hexatoma ']) + #1
lema('[Cc]armes_í__i', xpre=['filla del ']) + #2
lema('[Cc]enar_í_a[ns]?_i', xpre=['(?:[Dd]e|[Ee]n)', '[Ii]slote ']) + #5
lema('[Cc]r_é_dito_e', xpre=['\\bdi ', ], xpos=[' (?:in|Italiano|Artigiano|Valtellinese|Bergamasco|Emiliano|and|per|Varessino|Esattorie)', ]) + lema('[Cc]r_é_ditos_e', xpre=['\\blo ', 'Pizze a '], xpos=[' in\\b', ]) + #26
lema('[Cc]rec_í__i', xpre=['Enrique ']) + #2
lema('[Cc]ronol_ó_gic[ao]_o', xpre=['Storia '], xpos=[' (?:dei|della|das)']) + #11
lema('[Dd]_í_a_i', pre='(?:[Hh]oy(?: en|)|[Uu]n (?:buen|cierto|duro|gran|largo|nuevo|s[oó]lo)|[Pp]rimer|[Ss]egundo|[Tt]ercer|[Cc]uarto|[Qq]uinto|[Ss]exto|[Ss][eé]ptimo) ', xpos=[' (?:da|e meio)']) + #52
lema('[Dd]egenerar_í_a_i', xpre=['Idaea ']) + #1
lema('[Dd]emogr_á_fic[ao]s?_a', xpre=['Bilancio ', 'storia ', ]) + #588
lema('[Dd]ep_ó_sitos?_o', xpre=['(?:[Ii]l|[Ll]a) ', 'Cardili, ', 'sepulcro '], xpos=[' (?:Giordani|da)']) + #114
lema('[Dd]iscogr_á_fic[ao]s?_a', xpre=['della Critica ']) + #167
lema('[Ee]_x_tendid[ao]s?_s?', xpre=['onde ']) + #4
lema('[Ee]nfermer_í_as?_i', xpos=['\.uady']) + #22
lema('[Ee]sf_é_ric[ao]s?_e', xpre=['Vorticella ', 'Lepidocyclina ']) + #7
lema('[Ff]_ó_rmulas?_o', pre='(?:[Ll]as?|[Uu]nas?|[Dd]e) ', xpre=['quién '], xpos=[' (?:One|Romani|della)', ]) + #67
lema('[Ff]or_á_ne[ao]s?_a', xpre=['battello ', 'Mythimna ']) + #3
lema('[Ff]re_í_r_i', xpre=['Frey\|']) + #3
lema('[Gg]_é_nero_e', pre='(?:[Ee]l|[Ee]ste|[Un]|[Dd]el?) ', xpre=['[Rr]ío '], xpos=['(?:…|\.com)']) + #146
lema('[Gg]e_ó_log[ao]s?_o', xpre=['Professione ']) + #3
lema('[Gg]rad_ú_a_u', xpos=['\'t']) + #3
lema('[Hh]ist_ó_ricos?_o', xpre=['Boletim ', 'romànico ', 'Illimani ', 'Études ', 'medicorum ', 'Estudo ', 'Lesbio ', '[Aa]no ', 'do Patrimonio ', ], xpos=[' (?:Naturalia|do|no|[Aa]sturiensia)\\b', ', biographico', ' et ', ]) + #429
lema('[Hh]oland_é_s_e', xpre=['permitió que el ']) + #26
lema('[Ii]c_ó_nic[ao]s?_o', xpre=['Glycyrrhiza ', 'Cousinia ', 'Conchologica ', 'Conchologia ']) + #14
lema('[Ii]m_á_genes_a', xpos=[' Librorum']) + #115
lema('[Ii]ndicar_í_a_i', xpre=['Tractatus de astrologia ']) + #2
lema('[Ii]nfanter_í_as?_i', xpre=['d\''], xpos=[' de marinha']) + #38
lema('[Jj]erarqu_í_as?_i', xpos=[' a la Responsabilitat']) + #4
lema('[Ll]_á_mparas?_a', xpre=['[A]\. ', 'Astronesthes ', 'Wishing ']) + #36
lema('[Ll]_á_tigos?_a', xpre=['for ', 'George '], xpos=[' Means']) + #4
lema('[Ll]_é_sbic[ao]s?_e', xpre=['[AI]\. ', 'Aphaenogaster ', 'Isoperla '], xpos=[' e gay']) + #4
lema('[Ll]_ó_gic(?:os|amente)_o', xpos=[' Aristotelis']) + #2
lema('[Ll]_ó_gic[ao]_o', pre='(?:[Ll]a|[Uu]na) ', xpos=[' (?:d[iu]|del)\\b']) + #4
lema('[Ll]oter_í_as?_i', xpre=['Caixa '], xpos=[' (?:Vella|sem)']) + #24
lema('[Mm]agn_í_fica_i', pre='(?:[Ll]a|[Uu]na|[Dd]e|[Ee]sta|[Ss]u|[Tt]an) ', xpos=[' (?:Cure|ni)\\b']) + #9
lema('[Mm]al_é_vol[ao]s?_e', xpre=['Euphorbia ']) + #1
lema('[Mm]an_í_as?_i', pre='(?:[Ll]as?|[Uu]nas?) ', xpos=['\.com']) + #2
lema('[Mm]ani_á_tic[ao]s?_a', xpre=['[Ii]l ']) + #1
lema('[Mm]ariner_í_as?_i', xpos=[' degli']) + #2
lema('[Mm]iscel_á_ne[ao]s?_a', xpos=[' (?:Antwerpiensia|Barcinonensia|taxinomica)']) + #17
lema('[Mm]o_v_ilidad_b', xpos=[' Bahía']) + #9
lema('[Nn]_ú_meros?_u', pre='(?:[Ll]a|[Ee]l|[UuEe]n|[Ll]os|[Uu]nos|[Ss]u|[Ss]in|[Gg]ran|[Cc]iertos?|[Ee]s(?:te|tos|se)) ', xpre=[' il '], xpos=[' (?:Piccoli|indefinito)']) + #134
lema('[Oo]rfebrer_í_as?_i', xpos=[' i\\b']) + #5
lema('[Pp]_á_jaros?_a', xpos=[' Dunes']) + #36
lema('[Pp]_ú_lico_u', pre='(?:[Aa]cceso|[Aa]cto|[Aa]seo|[Aa]cusador|[Aa]gente|[Aa]lumbrado|[Aa]l|[Aa]lboroto|[Aa]rtículo|[Áá]mbito|[Bb]achillerato|[Bb]alneario|[Bb]astante|[Bb]ien|[Cc]amino|[Cc]argo|[Cc]ar[áa]cter|[Cc][ée]sped|[Cc]olegio|[Cc]omponente|[Cc]oncurso|[Cc]onocimiento|[Cc]ontador|[Cc]on|[Cc]r[ée]dito|[Cc]rematorio|[Cc]ulto|[Dd]ebate|[Dd]el?(?: difícil|)|[Dd]erecho|[Dd]esorden|[Dd]inero|[Dd]ominio|[Dd]éficit|[Ee]dificio|[Ee]l(?: gran|)|[Ee]mpleado|[Ee]ndeudamiento|[Ee]n|[Ee]nte|[Ee]nemigo|[Ee]spacio|[Ee]spejo|[Ee]ste|[Gg]asto|[Ff]in|[Ff]uncionario|[Ii]nterés|[Ii]nstituto|[Ii]nvestigación|[Ll]lamamiento|[Ll]ugar|[Mm]anifiesto|[Mm]ercado|[Mm]inisterio|[Mm]irador|[Mm]ucho|[Nn]otario|[Nn]umeroso|[Oo]brero|[Oo]jo|[Oo]rden|[Oo]rganismo|[Pp]arking|[Pp]arque|[Pp]ersonaje|[Pp]oder|[Pp]resupuesto|[Pp]roblema|[Pp]roceso|[Pp]uesto|[Rr]egistro|[Rr]astro|[Rr]eloj|[Ss]ector|[Ss]ervicio|[Ss]ervidor|[Ss]in|[Ss]u(?: propio|)|[Tt]el[ée]fono|[Tt]ecnológico|[Tt]odo|[Tt]ransporte(?: urbano|)|[Tt]rabajo|[Uu]n|[Uu]so|entre|frontón|hacer?|hará|haría|hecho|hiciera|hicieron|hizo|mayor|más|mismo|nuevo|numeroso|para|tenía) ', xpos=['\.es']) + #1
lema('[Pp]a_í_s_i', pre='(?:[Aa]l|[Cc]ada|[Dd]el|[Ee]l|[Uu]n|[Ss]u|[Mm]i|[Nn]uestro|gran|pequeño|[Ee]ste|[Dd]icho|[Pp]or|[Cc]ualquier) ', xpre=['d\' ', 'd\'D\'Amics ', ], xpos=['\.es', ' (?:dels|Valenci[aàá]|Basc|de les caramelles)', ]) + #505
lema('[Pp]anader_í_as?_i', xpos=['\.blogspot']) + #8
lema('[Pp]arasitolog_í_as?_i', xpre=['\\be ']) + #7
lema('[Pp]atri_ó_tic[ao]s?_o', xpre=['Ação '], xpos=[' di\\b']) + #21
lema('[Pp]edi_á_tric[ao]s?_a', xpos=[' Bambino']) + #4
lema('[Pp]el_í_culas?_i', xpos=['(?:\.disneylatino|\.info|9)']) + #669
lema('[Pp]ertenec_í_(?:a[ns]?|)_i', xpre=['(?:[Ll]a|[Dd]e|[Ss]u) ', '(?:[Ll]as|[Ss]us) ']) + #16
lema('[Pp]olicl_í_nicos?_i', xpre=['estación\)\|\'\'\'', 'Viale del ', 'Nápoles\)\|', 'estación\)\|'], xpos=[' \((?:Metro de Nápoles|estación)']) + #5
lema('[Pp]on_í_a[ns]?_i', xpre=['Adiós ']) + #8
lema('[Pp]resb_í_ter[ao]s?_i', xpre=['F\. ']) + #17
lema('[Pp]resid_í_a[ns]?_i', xpre=['fueron ', 'plural \'\'\'']) + #8
lema('[Rr]adiograf_í_as?_i', xpos=[' (?:d´una|di)\\b']) + #6
lema('[Ss]acrist_í_as?_i', xpos=[' Vecchia']) + #6
lema('[Ss]ellar_í_a_i', xpre=['della ']) + #1
lema('[Ss]entir_á_[ns]?_a', xpre=['\\bet ']) + #1
lema('[Ss]ovi_é_tic[ao]s?_e', xpre=['E\. ', 'Saussurea ', 'Euglossa ', 'Unione ']) + #49
lema('[Ss]upremac_í_as?_i', xpre=['\\be ']) + #9
lema('[Tt]_é_rmica_e', xpre=['Centrale ']) + #11
lema('[Tt]ar_j_etas?_g', xpre=['amb ']) + #1
lema('[Tt]elefon_í_as?_i', xpos=[' Nas']) + #9
lema('[Vv]en_z_(?:a[ns]?|o)_s', xpre=['Sant '], xpos=[' (?:Klicic|Dolonc)']) + #1
lema('[l]e_í_a_i', xpre=['Wo ', 'Doriopsilla ']) + #3
lema('[t]ra_í_an_i', xpos=[' in\\b']) + #2
lema('_h_oland[eé]s_H', pre='\\b(?:e[ln]|del?|idioma|y) ', xpre=['Diplomado '], xpos=[' (?:[Ee]rrante|[Vv]olador)']) + #2
lema('_ha_ (?:jugado|labrado|lanzado|liberado|limitado|llegado|llenado|llevado|logrado|manejado|marcado|mantenido|matado|mejorado|mencionado|modelado|modernizado|mostrado|multiplicado|nacido|obtenido|observado|ocupado|ofrecido|ordenado|participado|peleado|perdido|permanecido|permitido|perseguido|pertenecido|podido|pose[ií]do|presentado|probado|promovido|propagado|prosperado|provocado|publicado|quedado|realizado|recibido|recuperado|regresado|registrado|renunciado|repercutido|replanteado|representado|respondido|restaurado|retenido|retratado|reunido|revelado|revisado|revolucionado|sabido|sacado|salido|señalado|separado|sido|sobrevivido|sostenido|sufrido|sugerido|superado|suspendido|sustituido|tenido|terminado|tocado|tomado|trabajado|tra[ií]do|transcurrido|transformado|trasladado|tratado|ubicado|usado|utilizado|variado|vendido|venido|viajado|visto|vivido|vuelto)_ah?', xpre=['[0-9]', ]) + #160
lema('_Á_rea (?:[Mm]etropolitana|[Cc]hica|Natural|Local|[Cc]onurbada|[Bb]iogeogr[áa]fica|[Rr]ecreativa)\\b_A', xpre=['l\'']) + #79
lema('_Á_rea de\\b_A', xpre=['Council ']) + #58
lema('_Ú_ric(?:as|os?)_U', xpos=[' Schmitdt']) + #1
lema('_é_l (?:anhela|pued[ae]|gana)_e', xpre=['l\'']) + #59
lema('_é_l (?:est(?:ar|)[aá]n?|estaba|estará|estuvo|estar[ií]an?|dijo|dir[aá]|dice|vienen?|fu[ée]|fueron|vendr[aá]n?|tiene|tuvo|ten[ií]a[ns]?|tendrán?|es|era|serán?|fue|hab[ií]a|sabe|sab[ií]a|no le)_e', xpre=['l\'']) + #112
lema('_é_l ha_e', xpre=['(?:ch\'|Af\')']) + #3
lema('_é_l[,]_e', pre='(?:[Aa]|[Dd]e|[Cc]on|[Ee]n|[Pp]or|[Hh]acia) ', xpos=[' (?:este|ya|hoy|entonces|abarrotado|en ese|relativamente|ahora|por)']) + #208
lema('_é_l[.]_e', pre='(?:[Aa]|[Dd]e|[Cc]on|[Ee]n|[Pp]or|[Hh]acia) ', xpos=['\.\.']) + #207
lema('_é_l[:]_e', pre='(?:[Aa]|[Dd]e|[Cc]on|[Ee]n|[Pp]or|[Hh]acia) ', xpre=['limita ']) + #11
lema('_é_l[;]_e', pre='(?:[Aa]|[Dd]e|[Cc]on|[Ee]n|[Pp]or|[Hh]acia) ', xpre=['limita ']) + #5
lema('_é_pic(?:as|os?)_e', xpre=['Scontro ']) + #1
lema('_é_xitos?_e', xpos=['\.com']) + #123
lema('_ú_ltima_u', pre='[Dd]e ', xpos=[' ratio']) + #8
 
[]][0]




linea=''
contenido=''
titulo=''
def proxArticulo(noElimDup, elimExcl, elimRev, excluidos, revisados):
    if len(linea)==0:
        linea = sys.stdin.readline()
    if linea:
        partes = linea.split("]]→",1)
        if len(partes)>1:
            titulo = partes[0].lstrip("[[")
            contenido = partes[1]
            linea = sys.stdin.readline()
            partes = linea.split("]]→",1)
            while titulo == partes[0]:
                contenido += partes[1]
                linea = sys.stdin.readline()
                partes = linea.split("]]→",1)
 

def quote(txt):
  txt1 = re.sub(',',',,', re.sub('"', '""', txt))
  if txt1 != txt:
    return '"'+txt1+'"'
  else:
    return txt

                
def filtrar(noElimDup, elimExcl, elimRev, excluidos, revisados):
  pat,trans,val = compilar()
  titulo=''
  tituloAnt=''
  contador = 0
  encontrados = 0
  errores = 0
 #  cada = 83660126/1024 #número de líneas 12/07
  cada = 125651742/512 #número de líneas 03/04/17
  contador = 0
  sys.stderr.write("#")
  lemaFile = open(lemasFileName, 'w')
  while True:
    linea = sys.stdin.readline()
    if linea:# and contador < 100000:
      contador +=1
      if contador>cada:
        contador = 0
        cada = cada*2
        sys.stderr.write(str(encontrados)+'+')
        lemaFile.write("#"+str(encontrados)+'+\n')
        encontrados = 0
        sys.stderr.flush()
        mostrarLemas(lemas, lemaFile, errores/10)
        lemaFile.flush()
      partes = linea.split("]]→",1)
      if len(partes)>1:
        titulo = partes[0]
        #if nuevoTitulo == 'Arte culinario':
        #  print ("****"+linea)
        if (titulo != tituloAnt or noElimDup):
          contenido = partes[1]
          for p in noCorregirEn:
              contenido = p.sub('<url>', contenido)
          match = pat.search(contenido)
          if match:
            if elimExcl:
              pal = match.group('c')
              contenido = contenido.strip()
              # match = trans.match(contenido)
              # if match:
              #     pal = match.group('c')
              #     #contenido = match.expand(val)
              #     contenido = contenido.strip()
              # else:
              #     pal="???"
              #print("pal="+pal+" contenido="+contenido)
              print (quote(pal)+','+quote(titulo+']]')+','+quote(contenido))
              sys.stdout.flush()
              tituloAnt = titulo;
              encontrados +=1
              #contador de las reglas
              for l in lemas:
                 if l[0].search(contenido):
                     l[2] += 1
                     errores += 1
          else:
            if not elimExcl:
              print(linea)
    else:
      sys.stderr.write(str(encontrados)+".\n")
      sys.stderr.flush()
      sys.stdout.write("#lemas"+"\n")
      mostrarLemas(lemas, sys.stdout, errores/10)
      sys.stdout.flush()
      break

def mostrarLemas(lemas, f, division):
  lemas.sort(key=itemgetter(1))
  lemas.sort(reverse=True, key=itemgetter(2))
  total=0
  f.write ("#########\n")
  for l in lemas:
      f.write(l[1]+"#"+str(l[2])+"\n")
      total += l[2]
      while (total>division):
          #print ("#########")
          total = total - division

def main (argv):
   elimDup = True
   elimExcl = True
   elimRev = True
   try:
      opts, args = getopt.getopt(argv,"der",['duplicados', 'excluidos', 'revisados'])
   except getopt.GetoptError:
     #print ("Error")
     print (sys.argv[0]+' [-t] < <inputfile> > <outputfile>')
     print (sys.argv[0]+' [-dh]')
     sys.exit(2)
   for opt, arg in opts:
     if opt in ('-d', '--duplicados'):
       elimDup = False
     elif opt in ('-e', '--excluidos'):
       elimExcl = False
     elif opt in ('-r', '--revisados'):
       elimRev = False
   filtrar(not elimDup, elimExcl, elimRev, excluidos.excluidos, excluidos.revisados)



if __name__ == "__main__":
   main(sys.argv[1:])

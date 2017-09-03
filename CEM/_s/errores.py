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
    
lema('[Bb]a_il_es?_li', xpos=[' (?:Peyton|Mangroe|Swart)', '’ Mangroe']) + #3
lema('[Aa]t_ó_nit[ao]s?_o', xpre=['[Ee]l ', 'cenobitismo ']) + #4
lema('[Dd]escubr_ió__(?:io|ío)', xpre=['quando ', ], xpos=[' no anno', ]) + #11
lema('Bak_ú__u', pre='(?:[Dd]e|[Ee]n) ', xpre=['acompañado '], xpos=[' Crystal', ]) + #8
lema('[Cc]ono_z_c(?:a[ns]?|amos|o)_s', xpre=['che ', 'Brincar ', 'Non ', '[TtVvLl]i ', 'cuide ', 'non lo ', ]) + #8
lema('[Ee]s__encia(?:l|les|lmente)_c', xpre=['\]', ], xpos=[' Indígena', ]) + #7
lema('[Mm]et_í_a[ns]?_i', xpre=['muestra el ', ';', 'mágico \(', 'en que ', '\\bde ', 'Lotoala ', ], xpos=[' (?:Lotoala|Interactive|Iparis|Industry)', ]) + #6
lema('[Pp]_ó_stum[ao]s_o', xpre=['op\. ', 'Atilio ', 'Vibio ', ], xpos=[' Dardano', ]) + #6
lema('[Ll]ic_ú_(?:a|as?|e[ns]?)_u', xpre=['grupo ', 'perlatum ', ], xpos=[' Labaudt', ]) + #5
lema('H_á_bil_a', xpre=['Adil ', 'Dr ', 'Dr\. ', ], xpos=[' (?:Heidelberg|Dr\.|Ahmadov)', ', (?:eraikan|Halle)', '\.', ]) + #4
lema('[Aa]cert_ó_(?! dos)_o', xpre=['Bo ']) + #4
lema('[Ff]isiol_ó_gic[ao]s?_o', xpre=[' e ', ]) + #4
lema('[Gg]al_á_ctic[ao]s?_a', xpre=[' (?:la|of) ', '\\ba ', 'Agua \(', 'Aria ', 'marca ', 'Ephemeroptera ', 'Battlestar ', 'Battlestar "', 'Battlestar\]\] ', 'Galactica\|', '2004\)\|', 'Hyde ', 'Imperium ', 'Invaders ', 'Pirámide \(', 'Saddlesore ', 'Saddlessore ', 'Sadlessore ', 'Shadow ', 'como '], xpos=[' (?:e[ns] |Donut|Discovers|Plants|Myosotis|Tornado|Tsunami|Crunch|Magnum|reúne|Year|Inflation|Scales|Superstring|1980|\((?:voz|nave))', '(?:\)\||\'\'|: The|, [Aa]stronave)', ]) + #4
lema('[Gg]en_é_tico_e', xpre=['Pomodoro ', ]) + #4
lema('[Ii]niciar_í_a[ns]?_i', xpre=['sus ', ]) + #4
lema('[Mm]ontar_í_a_i', xpos=['\]\]', ]) + #4
lema('Om_á_n_a', pre='(?:[Dd]e|[Ee]n) ', xpos=[' Air', ]) + #3
lema('[Aa]lquer_í_as_i', xpre=['sive ']) + #3
lema('[Dd]ermatolog_í_as?_i', xpos=[' (?:e venereologia|Ospedale)', ]) + #3
lema('[Dd]r_á_stic[ao]_a', xpre=['Millettia ', 'Anisomeria ', 'Euphorbia ', 'Wilbrandia ', ]) + #3
lema('[Ee]_n_ cada_m', xpre=['uma gota de sangue ', ], xpos=[' (?:rosto|esquina um)', ]) + #3
lema('[Pp]sicopedagog_í_as?_i', xpos=[' em ', '\.com', ]) + #3
lema('[Ss]ab_á_tic[ao]s?_a', xpos=['\.com', ]) + #3
lema('[Uu]n_á_nimes_a', xpos=[' [Pp]ro [Dd]eo', ]) + #3
lema('Reverter_á__a', xpre=['Nicola ', ], xpos=[' della', ]) + #2
lema('[Aa]nal_í_tic(?:as|os?)_i', xpre=['ed ', ]) + #2
lema('[Cc]os_í_a[ns]?_i', xpos=['\]', ]) + #2
lema('[Ii]deol_ó_gic[ao]_o', xpre=['galassia ', ], xpos=[' della', ]) + #2
lema('[Ll]aborar_í_a[ns]?_i', xpre=['inurri ', ]) + #2
lema('[Mm]atar_í_a[ns]?_i', xpos=['\]', ]) + #2
lema('[Mm]ineralog_í_as?_i', xpre=['di ', 'e ', ], xpos=[' Cornubiensis', ]) + #2
lema('[Nn]_í_tid(?:as|os?|amente)_i', xpos=[' [Nn]ulo', ]) + #2
lema('[Nn]obil_í_sim[ao]s?_i', xpos=[' Cæsares', ]) + #2
lema('[Pp]artir_á__a', xpre=['(?:tu|[Oo]n) ', ]) + #2
lema('[Pp]unt_ú_(?:a[ns]?|e[ns]?)_u', xpre=['eta ', ]) + #2
lema('[Ss]i_en_do_ne', xpre=['Andre ', 'Sinedo\|']) + #2
lema('[Ss]obrar_í_a[ns]?_i', xpre=[' de ', 'Juan ', ]) + #2
lema('_Á_rid(?:as|os?)_A', xpre=[' of ', ], xpos=[' movie', ]) + #2
 
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

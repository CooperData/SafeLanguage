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

lema('_ú_nico [a-zñáéíóú]+_', xpre=['[Ll]\'', 'in un ', 'in ', 'Partito ', 'quasi '], xpos=[' (?:motus|expressarum|concorrente|Amore|mercato|arbëreshë|posto|suo|la quantità|gli|norme|manuale|prima|de Espana|leggi|tra|di|nome|biblioteche|in|funivia|di|suo|della|queda|leggi|per)']) + #1


 
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


def toCSV(*cols):
    return ', '.join([quote(col) for col in cols])

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

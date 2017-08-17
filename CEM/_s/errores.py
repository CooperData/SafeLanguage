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
  if not xpre is None:
      xpre.sort() 
      src+=", xpre=["
      for p in xpre:
          xpres += "(?<!"+p+")"
          src+="ur\'"+qte.sub("\\'",p)+"\', "
      src+="]"
  xposs=''
  if not xpos is None:
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
  trans = '(.*?)\\b(?P<l>.{0,40})'+pat+'(?P<r>.{0,40})\\b(.*?)'
  val = '...\\g<l>\'\'\'\\g<c>\'\'\'\\g<r>...'
  #print (pat)
  return (re.compile(pat,flags),re.compile(trans,flags),val)

#Cambios ambiguos
#lema('_xx__[Ee]l (?:algunas|campos|cercanías|cuartos|detrás|distritos|días|estados|estudios|gobiernos|mismos|muchos|nombres|nosotros|números|objetivos|otras|partidos|personajes|playoffs|podemos|premios|primeros|principios|problemas|productos|programas|pueblos|representantes|récords|sencillos|siguientes|sitios|temas|todas|todos|varias|ámbitos|áreas|últimos)') + 
#lema('_xx__[Ee]l (?!abrebotellas|abrecartas|adi[oó]s|aguafiestas|albanés|albatros|alias|antes|análisis|apocalipsis|apófisis|aragonés|aranés|aspis|atlas|aulos|autobús|bibliobús|blues|botones|brindis|burgalés|burgués|campus|cannabis|caos|cascanueces|chasis|ciprés|clítoris|compás|cordobés|corpus|cosmos|cumpleaños|danés|despu[eé]s|dios|eibarrés|entonces|entremésasturleonés|envés|escocés|estatus|estrés|finlandés|finés|francés|frontis|galés|genovés|gris|guardaespaldas|holandés|inglés|interés|iris|irlandés|japonés|jueves|leonés|locus|los|lunes|m[áa]s|marcapasos|marqués|martes|matarlos|menos|microcosmos|mirandés|miércoles|modus|neerlandés|oasis|palmarés|parabrisas|paracaídas|paraguas|paréntesis|pasacalles|país|portaaviones|portugués|psicoanálisis|páncreas|raquis|rascacielos|revés|rompecabezas|saltamontes|seis|senegalés|status|tenis|tres|vals|viernes|virus|énfasis|éxtasis)[a-záéíóúüñ]+s') + 

lemasFileName = 'Los.lem'
# lemasPos= [##Eliminar ur y cambiar \b por \\b
# lema(ur'[Mm]_a_s [a-záéíóúñ]+') + 
# []][0]

lemas= [##Eliminar ur y cambiar \b por \\b

lema('[Hh]i_c_ieron_z', xpos=[' los capitanes']) + #32
lema('[Hh]i_z_o_s', xpre=['quispe tito ', '\| '], xpos=[' Hyakuga', '\)']) + 
lema('[Ll]_í_mites_i', pre='[Ll]os ') + #58
lema('[Ll]_í_mites?_i', pre='(?:[Ss]in(?: m[aá]s|)|[Hh]ay|[Cc]on|[Cc]omo|[Dd]el?|[Ee]ntre|[Tt]odo|[Ss]us?|[Ee]l|[Uu]n|[Uu]nos|al?|y|[Ee]st?e|[Ee]stos|[Ff]ija|[Dd]etermina|tiempo) ', xpre=['questão ', 'Froid ', 'Mondi ', 'signore ', ], xpos=[' Produções', ', d\'échang']) + #480
lema('_alemá_n_(?:Alem[aá]|alema)', pre='\\b(?:e[ln]|del?|idioma|y) ', xpre=['Sanscrito ', 'El pícaro ', ur'Casa ', ur'Hermann ', 'Columna ', 'Hermán ', 'Estudios ', 'Sanabria ', 'ojos ', 'Ortega ', 'Sayula '], xpos=['"']) + 
lema('[Pp]aran_á__a', xpre=['[H]\. ', 'Burón y ', '[Vv]iaducto de ', 'Hemigrammus ', 'Lena\)\|', 'Hololena ', 'Cryptachaea '], xpos=[' \(Lena', '(?:´i|, etc)']) + 
lema('[Cc]onfes_ó__o', xpre=['\\b(?:[Uu]n|[Ss]u|[EeÉe]l|[Ee]s) ', 'ateo ', 'caníbal ', 'incendiario\]\] ', '[Mm]elómano ', 'simpatizante ', 'asesino ', 'pagano ', 'hincha ', 'asesino ', 'seguidor ', 'anglófilo ', 'miembro ', 'convicto ', 'amor ', 'Amante ', 'halló ', 'delito ', 'suicida ', 'homicida ', 'socialista ', 'fascista ', '\\by ', 'cristiano ', 'homosexual ', 'fan ', 'autor ', 'objetivo '], xpos=[' (?:de|del|hincha|seguidor|fanático|aficionado|ladrón|amante|adicto)\\b', '\'\'']) + 
lema('[Bb]engal_í__i', xpre=['and ', 'Renault '], xpos=[' (?:English|Liberation|Tiger)']) + 
lema('[Mm]_é_ritos?_e', xpre=['\\b(?:[Yy]a|di|et|do|il|in) ', 'Libens ', 'Nilo ', 'San Fernando del ', 'Bene ', 'aedem ', 'quas ', 'Ordine al ', ], xpos=[' (?:M[ei]litensi|Sportivo|Culturale|dedicata|tali|beneficia quae|legionemque|dei|rabirrubio|della|hec|dell|del lavoro|per|civile|per|ad |di )']) +
lema('[Pp]oes_í_as?_i', xpre=['\\b[AaàeP] ', '\\b[AaàeP]\. ', '\\b(?:[Dd]a|di|na) ', 'Rainha Sofia de ', 'mia ', ur'jovem ', 'Prémio Internacional de ', 'Premi Crítica Serra d\'Or de ', 'Premi Martí Dot de ', 'Quaderns de ', 'As 7 ', 'Bon dia, ', 'món de ', 'Concert de ', 'cicle de ', 'teva ', 'Encontro maior: ', 'Ciència, fe, ', 'd[\'’]abril de ', 'València de ', 'aplech de ', 'della epica ', '\\be de ', 'amb la ', 'Introducció a la ', 'Outras ', 'Sulla ', 'Jornal de ', 'Natura, ', 'Elogi de la ', 'Quart en ', 'nella ', 'vera ', 'Premis Octubre de ', 'Pedaliodes ', 'Pronophila ', 'Premi de ', 'celobert. Antologia de ', '[Mm]elhores ', '[Rr]evista \'\'', 'Jabuti de ', 'perfetta ', 'Futura: ', 'della ', 'MSC ', 'na ', 'mig editorial de ', 'minha alma: '], xpos=[' (?:i|in|di|per|\'90|Acadèmica|dialettale|sarda e|satirica in|experimental en terres|Nova|nell|en valencià|lirica ed|sonora|kaierak|Mienia|do|Escolhidas|contemporània|Completa \(1940|espanhola|eletronica|popolare|Etna-Taormina|ed|d|en acció|egípcia antiga|argentina e brasileira|e (?:storia|Prosa|sentimento|Composição|Crônica|retorica)|de (?:les|Marian Aguiló)|Espanhola)\\b', '(?:: a paixão|, estética e política|\'\', Antonio|[:,] \[\[(?:Paolo|contos|Enrico|Alessandro|Maria Luisa Spazani|Antonella))']) + #978
 
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
 

def filtrar(noElimDup, elimExcl, elimRev, excluidos, revisados):
  pat,trans,val = compilar()
  titulo=''
  tituloAnt=''
  contador = 0
  encontrados = 0
  errores = 0
#  cada = 83660126/1024 #número de líneas 12/07
  cada = 125651742/1024 #número de líneas 03/04/17
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
              match = trans.match(contenido)
              if match:
                  pal = match.group('c')
                  contenido = match.expand(val)
              else:
                  pal="???"
              #print("pal="+pal+" contenido="+contenido)
              print (pal+';'+titulo+']]→'+contenido)
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

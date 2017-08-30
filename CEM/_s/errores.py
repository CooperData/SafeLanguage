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

# lema('[Ss]elecci_ó_n_o', xpos=[' Esportives', '\]\]es', ]) + #702
# lema('[Pp]oblaci_ó_n_o', xpre=['New ', 'North ', 'Old ', 'South ', ], xpos=[' (?:East|West)', '\]\](?:es|al|ales)', ]) + #521
# lema('[Cc]lasificaci_ó_n_o', xpos=['\]\]es', ]) + #516
# lema('[Ee]staci_ó_n_o', xpos=['\]\]es', ]) + #472
# lema('[Nn]aci_ó_n_o', xpre=['Mexicana ', ], xpos=[' Occitana', '(?:\]|\.com)', ]) + #384
# lema('[Cc]anci_ó_n_o', xpos=['\]\]es', ]) + #312
# lema('[Dd]ivisi_ó_n_o', pre='(?:[Uu]na|[Cc]ada|[Ss]u|[Pp]rimera|[Ss]egunda|[Cc]uarta) ', xpos=[' [12]\n', '\.htm', ]) + #300
# lema('[Ff]undaci_ó_n_o', xpre=['Fundación en 1987 "', ], xpos=[' Paraguaya\'s', '(?:[\]@]|2008|\.uocra)', ]) + #298
# lema('[Rr]edirecci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Cc]ampe_ó_n_o', xpos=['\]\]es', ]) + #282
# lema('[Cc]oncepci_ó_n_o', xpre=[' (?:of|ng) ', 'Araneus ', 'Immaculate ', 'Sam ', ], xpos=[' (?:Gross|\(Texas)', '(?:\]|\.cl)', ]) + #207
# lema('[Ee]dici_ó_n(?!\]|\.cl)_o') + #201
# lema('[Vv]ersi_ó_n_o', pre='(?:de|[Ll]a|[Uu]na|[Ee]sta|[Ee]sa|[Cc]ada|[Ss]u|[Ee]n|[Pp]rimera|[Ss]egunda|[Tt]ercera|[Cc]uarta|[ÚUúu]ltima|[Nn]ueva|cualquier) ', xpre=['d\'après ', 'pour ', 'pour ', ], xpos=[' (?:Cue|thebaine|restaurée|en français|française)', ]) + #198
# lema('[Gg]rabaci_ó_n_o', xpos=['\]\]es', ]) + #195
# lema('[Aa]sunci_ó_n_o', xpre=[' of ', 'd\'', 'near ', ], xpos=[' (?:Skyscraper|Golf|Business)', ]) + #188
# lema('[Pp]roduc_c_i(?:ón|ones)_s?') + #178
# lema('[Cc]oraz_ó_n_o', xpre=['D\'', 'Anya ', ], xpos=[' (?:Productions|Aquino)', '(?:\]\][a-z]+|\.cl|\.com)', ]) + #174
# lema('[Dd]irecci_ó_n_o', xpos=['(?:\]|\.tytres)', ]) + #165
# lema('[Tt]elevisi_ó_n_o', pre='[Dd]e ', xpos=[' (?:City|Without|Heaven)', ]) + #158
# lema('[Ii]nformaci_ó_n_o', xpos=['(?: *[@\]]|\.(?:com|es))', ]) + #152
# lema('[Rr]inc_ó_n_o', xpre=['\\bs ', 'cráter\)\|', 'Georgia\)\|', 'Vespo\]\] \(', 'Rincon\]\] \(', 'Vespo ', 'Chrysometa ', 'Beach ', 'Real ', 'Bonaire\)\|', 'California\)\|', 'Indiana\)\|'], xpos=[' (?:to|Valley|Beach|Mix|High|Center|Sapiencia|Point|Hill|Road|i Verdera|\((?:cráter|Georgia|Bonaire|California|Indiana))\\b', '(?:, Bonaire|\]\]es)', ]) + #146
# lema('[Cc]omisi_ó_n_o', xpos=['\]\]es', ]) + #141
# lema('[Cc]onstituci_ó_n_o', xpre=['da ', ], xpos=[' di', '\]\]', ]) + #139
# lema('[Uu]ni_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Ee]st?a) ', xpre=[' á ', 'Auto ', 'Journal de la ', 'Ridge ', 'San Fernando de ', 'of ', ], xpos=[' (?:Académique|Women|Catholique|anarchiste|County|Nazionale|Bordeaux|Sportive|Testament|Metallic|Anarco-communiste|Athletique|Avenue|Bay|Brazilian|Buildings|Carbide|Castle|Chapel|Church|City|Company|Cycliste|Elementary|Elevated|Evangelischer|Ferry|Fire|Flag|Française|Guilde|High|Hill|Internationale|Jack|League|List|Maçonnique|Mining|Mundial pro|Nationale|Oil|Pacific|Square|Station|Steamship|Stock|Street|Terminal|Theological|Trust|Turnpike|University|Vélocipédique|anarcho|calédonienne|des|fédérale|istorica|nationale|pour|socialiste|storica|de (?:Compositeurs|banques)|(?:of|do) )', ]) + #138
# lema('[Aa]sociaci_ó_n_o', xpos=['\]|\.Civil', ]) + #130
# lema('[Ee]ducaci_ó_n_o', xpos=[' Salsa', '(?:\]|\.go[bv]|\.yucatan|\.es)', ]) + #129
# lema('[Rr]elaci_ó_n_o', xpos=['\]\]es', ]) + #129
# lema('[Aa]cci_ó_n_o', xpre=['d\'', ], xpos=['\]\]es', ]) + #127
# lema('[Cc]añ_ó_n_o', xpre=['Ipyahe ', '[Mm]icropolitana ', ], xpos=[' City', '\]\]es', ]) + #117
# lema('[Pp]osici_ó_n_o', xpos=['\]\]es', ]) + #113
# lema('_Venevisió_n_(venevisi[óo]|Venevisio)', xpre=['\.', ], xpos=['\.', ]) + #109
# lema('[Pp]roducci_ó_n_o', xpos=['(?:\]|\.(?:com|gob)|\'s)', ]) + #106
# lema('[Dd]escripci_ó_n_o', xpre=['cousa ', ], xpos=[' (?:Graphica|breue|Histórico Geografía|de todas las provincias, reynos)', '\]\]es', ]) + #104
# lema('[Rr]az_ó_n_o', xpre=['Bernard ', 'Cynthia V\. ', 'Meital de ', ], xpos=[' (?:and|Copa|de aquellas muchas cabeçuelas)', '\]\]es', ]) + #98
# lema('[Aa]vi_ó_n_o', xpre=['\\b[LlDd]\'', 'CS ', 'Comme un ', 'Paul ', 'Cantón de ', 'Europe en ', 'cet ', '[Cc]antón de Avion\|', '[Cc]antón de ', 'Novi ', 'Orchestra ', 'Par ', 'Calais\)\|', 'yvate ', ], xpos=[' (?:Corporation|Travel|de (?:Transport|minuit|Combat)|Baker|Express|\(Paso|)', '(?:, (?:Pas|Grenay)|\]\]es)', ]) + #97
# lema('[Rr]evoluci_ó_n_o', xpre=['Zonda ', ], xpos=['\]\]es', ]) + #97
# lema('[Ff]ederaci_ó_n_o', xpos=[' (?:de l|Galega|d)\\b', '(?:\]|\.pe)', ]) + #92
# lema('[Rr]egi_ó_n_o', pre='(?:[Ll]a|[Uu]na) ', xpos=[' (?:de|Mediterraneenne|Centrale|alpine|himalayenne|du |Sud et|Côtier|d\'Ambovombe)', ]) + #85
# lema('[Oo]rganizaci_ó_n_o', xpos=['\]\]es', ]) + #84
# lema('[Gg]esti_ó_n_o', xpre=['Assurances ', 'Contrôle de ', 'Français de ', 'Intercommunal de ', 'Sciences de la ', 'Societé de ', 'Socièté de ', 'Société de ', 'Suisses de ', 'Syndicat de ', 'Système de ', 'contrôle de ', 'et ', 'et de ', 'européen de ', 'française de ', 'mauvaise ', 'méthodes de ', 'nouvelle ', 'pour ', 'pour la ', 'structure, ', 'supérieur de ', 'École de ', 'à la ', 'économie, ', ], xpos=[' (?:(?:et|ou) |par|pour|forestière|Privee-SIB|informatisée|publique|Patrimoniale|Animation|Bonfire|stratégique|écologique|du|des|plus|Municipale|Intégrée|de (?:Genève|classe|la qualité|la relation|documents|contenu|l\'ArchiTEcture|l\'Entreprise)|Cinématographique)', '(?:[0-9\]]|\.org)', ]) + #83
# lema('[Ii]nterpretaci_ó_n_o', xpos=['\]\]es', ]) + #81
# lema('[Pp]resentaci_ó_n_o', xpos=['\]\]es', ]) + #81
# lema('[Tt]ibur_ó_n_o', xpre=['(?:EA|[Ll]e|of|[Ii]n) ', 'Arts ', 'California\)\|', 'Hyundai ', ], xpos=[' (?:Film|Chum|Boulevard|International|Challenger|y Belvedere|Center|Peninsula|\(California)', '(?:, \[|\]\]es)', ]) + #81
# lema('[Cc]olecci_ó_n_o', xpos=['\]\]es', ]) + #80
# lema('[Cc]reaci_ó_n_o', xpos=['\]\]es', ]) + #78
# lema('[Cc]omunicaci_ó_n_o', xpos=['(?:\,umh|\]\]es|\.senado)', ]) + #77
# lema('[Pp]articipaci_ó_n_o', xpos=[' ciutadana', '\]\]es', ]) + #73
# lema('[Cc]onservaci_ó_n_o', xpos=['\]\](?:es|ista)', ]) + #72
# lema('[Ee]lecci_ó_n_o', xpos=['\]\]es', ]) + #72
# lema('[Oo]cupaci_ó_n_o', xpos=['\]\]es', ]) + #72
# lema('[Ff]ormaci_ó_n_o', xpos=['\]\]es', ]) + #71
# lema('[Pp]asi_ó_n_o', xpre=['E\. ', 'the ', ], xpos=[' (?:for|Wrestling|Dub|ni)\\b', '\.demotilla', ]) + #71
# lema('[Ss]ecci_ó_n_o', xpos=['[1-9\]]', ]) + #71
# lema('[Gg]eneraci_ó_n_o', xpre=['@1', ], xpos=['(?:\]|\.com)', ]) + #70
# lema('[Ii]lustraci_ó_n_o', xpos=['\]\]es', ]) + #69
# lema('[Pp]ercusi_ó_n_o', xpre=['and ', ], xpos=[' [Ss]et', '\]\]es', ]) + #69
# lema('[Tt]radici_ó_n_o', xpos=['\]\](?:al|es)', ]) + #67
# lema('[Ff]usi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|de|y) ', xpre=['énergie ', ], xpos=[' (?:Ford|Man|de deux|Systems|Rhône)', '\]\]es']) + #65
# lema('[Dd]ivisi_ó_n_o', pre='[Tt]ercera ', xpos=['\.cl', ]) + #30
# lema('[Dd]ivisi_ó_n_o', pre='[Ll]a ', xpos=[' (?:[12]|Interrégionale|me perd|navale|en France|of |du |politique|méthodique|Rosemont|One|Two|Three|Théorique|de l’intérieur|des |Skanderbeg, Histoire|Charlemagne|SS Das reich sème|[Oo]ne)\\b', ]) + #64
# lema('[Ii]nstituci_ó_n_o', xpos=['\]\]es', ]) + #64
# lema('[Ii]nvestigaci_ó_n_o', xpos=['\]\]es', ]) + #64
# lema('[Pp]reten_sio_nes_(?:sió|ci[oó])') + #64
# lema('[Ss]ituaci_ó_n_o', xpre=['Q[’\']', ], xpos=[' \(Abril de 1864', '\]\]es', ]) + #64
# lema('[Ee]xposici_ó_n_o', xpos=[' de la dotrina', '\]\]es', ]) + #63
# lema('[Tt]orre_ó_n_o', xpos=['\]\]es', ]) + #62
# lema('[Aa]parici_ó_n_o', xpos=['\]\]es', ]) + #61
# lema('[Dd]efinici_ó_n_o', xpos=['(?:\]|\.org|\.de)', ]) + #61
# lema('[Oo]peraci_ó_n_o', xpos=['\]\]es', ]) + #60
# lema('[Ff]icci_ó_n_o', xpos=['\]\]es', ]) + #59
# lema('[Aa]dministraci_ó_n_o', xpos=['(?:@|\]\]es)', ]) + #58
# lema('[Ff]unci_ó_n_o', xpos=['\]\]es', ]) + #57
# lema('[Pp]ublicaci_ó_n_o', xpos=['\]\]es', ]) + #55
# lema('[Uu]bicaci_ó_n_o', xpos=['\]\]es', ]) + #55
# lema('[Rr]egi_ó_n de_o', xpre=['Muscinees de la ', ]) + #54
# lema('[Aa]nimaci_ó_n_o', xpos=['\]\]es', ]) + #53
# lema('[Aa]viaci_ó_n_o', xpos=['(?:\]\]es|\.mil)', ]) + #53
# lema('[Tt]ra_nsliteració_n_sliteraci[oó]') + #53
# lema('[Aa]dmin_istració_n_(?:itraci[oó]|straci[oó]|istrac[ioó])') + #52
# lema('[Dd]rag_ó_n_[oò]', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ', xpre=['Europa ', 'Dent ', 'Rêve ', ], xpos=[' (?:Cry|Con|Dance|Hunters|Inn|Lancer|Psychic|Caesar|Ranger|School|dans|Festival|Hill|Lore|Fly|Queen|Rouge|Warrior|Boy|TV|City|Tales|Booster|Rock|Comics|Knight|Tour|Hawk|marin|[Bb]oat|Lee|[Bb]all|[Ss]layer|[Qq]uest|[Rr]apide|[Ff]all|[Aa]ge|[Ww]orld|[Gg]ate|Shot|Tail|Khan|Ash|Sound|Force|Mk\.IV|/ Falcon)', '(?:\]\]es|\'s)', ]) + #52
# lema('[Pp]rogramaci_ó_n_o', xpos=['\]\]es', ]) + #52
# lema('[Ee]ncarnaci_ó_n_o', xpos=['\]\]es', ]) + #50
# lema('[Pp]abell_ó_n_o', xpos=[' As', '\]\]es', ]) + #49
# lema('[Ss]ubcampe_ó_n_o', xpos=['\]\]es', ]) + #48
# lema('[Tt]elevisi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Ee]n|[Pp]or|Caracas) ', xpos=[' (?:Broadcasts?|Critics?|City|Parts|Preview)', ]) + #47
# lema('[Kk]ilot_ó_n_o', xpos=['\]\]es', ]) + #46
# lema('[Pp]romoci_ó_n_o', xpre=['Ròker ', ], xpos=['\]\]es', ]) + #46
# lema('[Dd]istribuci_ó_n_o', xpos=['\]\]es', ]) + #45
# lema('[Ee]lec_cio_nes_(?:i[oó]|cci[oó])') + #45
# lema('[Oo]btenci_ó_n_o', xpos=['\]\]es', ]) + #45
# lema('[Rr]iñ_ó_n_o', xpos=['\]\]es', ]) + #45
# lema('[Ii]_nauguració_n_(?:gnauraci[oó]|naguraci[oó]|nauguracio)', xpos=['\]\]es', ]) + #44
# lema('[Nn]ataci_ó_n_o', xpos=['\]\]es', ]) + #44
# lema('[Ll]esi_ó_n (?:de|en|que)\\b_o') + #43
# lema('[Pp]rocesi_ó_n_o', xpos=['\]\](?:es|al|ales)', ]) + #43
# lema('[Rr]enovaci_ó_n_o', xpos=['\]\]es', ]) + #43
# lema('[Cc]oalici_ó_n(?![0-9\]])_o') + #42
# lema('[Ee]voluci_ó_n_o', xpos=[' e desnreolo', '\]\]es', ]) + #42
# lema('[Rr]esoluci_ó_n_o', xpos=['\]\]es', ]) + #42
# lema('[Tt]romb_ó_n_o', xpos=['\]\](?:es|istas?)', ]) + #42
# lema('[Cc]onvulsi_ó_n_o', xpos=[' (?:[Tt]herapy|Group)', '\]\]es', ]) + #41
# lema('[Bb]alc_ó_n_o', xpre=['(?:[Ll]e|du|au) ', '\\b(?:por|mon) ', 'M\. ', 'Claudie ', 'Michael ', 'Jill ', 'grand ', 'relais de ', 'siendo ', ], xpos=[' (?:à|sur|Zone|en forêt|renombró)\\b', '(?:\]\](?:es|ada)|, (?:Sylvie|corridor))']) + #40
# lema('[Cc]ati_ó_n_o', xpre=['putative ', ], xpos=[' (?:denatonium|exchange|channel|in|of)', '\]\]es', ]) + #40
# lema('[Ee]cuaci_ó_n_o', xpos=['\]\]es', ]) + #40
# lema('[Ll]adr_ó_n_o', xpos=[' Peak', '\]\]es', ]) + #40
# lema('[Ss]axof_ó_n_o', xpos=['\]\]es', ]) + #40
# lema('[Oo]pini_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Ee]n|[Dd]e) ') + #39
# lema('[Pp]iñ_ó_n_o', xpre=['Jannis ', 'Kusnezov ', 'Led ', 'Pine ', 'Ramon ', ], xpos=[' (?:Hills|Pine)', '\]\]es', ]) + #39
# lema('[Pp]risi_ó_n_o', xpre=[' In ', 'Glass ', ], xpos=[' (?:ward|blues|Fellowship|Match)', '\]\]es', ]) + #39
# lema('[Cc]onfederaci_ó_n_o', xpos=['\]\]es', ]) + #38
# lema('[Cc]orporaci_ó_n_o', xpos=['\]\]es', ]) + #38
# lema('[Dd]iputaci_ó_n_o', xpos=['\]\]es', ]) + #38
# lema('[Ee]misi_ó_n_o', xpos=['\]\]es', ]) + #38
# lema('[Tt]ransmisi_ó_n_o', xpos=[' (?:Eléktrika|kon)', '\]\]es', ]) + #38
# lema('[Ll]ocalizaci_ó_n_o', xpos=['\]\]es', ]) + #37
# lema('[Mm]anifestaci_ó_n_o', xpos=['\]\]es', ]) + #37
# lema('[Tt]raducci_ó_n_o', xpos=['\]\]es', ]) + #37
# lema('[Ii]n_s_cripciones_') + #36
# lema('[Ii]ntroducci_ó_n_o', xpos=['\]\]es', ]) + #36
# lema('[Nn]ominaci_ó_n_o', xpos=[' indirècta', '\]\]es', ]) + #36
# lema('[Mm]isi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]|[Ee]st?a) ') + #35
# lema('[Pp]atr_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ', xpre=['repiè ', 'vida ', ], xpos=[' (?:de presse|and|Saint|Advisory)', ]) + #35
# lema('[Cc]esi_ó_n_o', xpos=['\]\]es', ]) + #34
# lema('[Cc]uesti_ó_n_o', xpos=['\]\]es', ]) + #34
# lema('[Oo]ca_sio_nes_(?:ci[oó]|sió)') + #34
# lema('[Pp]untuaci_ó_n_o', xpos=['\]\]es', ]) + #34
# lema('[Cc]olaboraci_ó_n_o', xpos=['\]\]es', ]) + #33
# lema('[Ss]esi_ó_n_o', xpre=['room ', '[Ii]n ', 'jam ', ], xpos=['\]\]es', ]) + #33
# lema('[Vv]isi_ó_n_o', pre='(?:[Uu]na|[Cc]ada|[Ss]u|[Ll]a|[Ee]sta) ', xpos=[' (?:City|mystique|érotique|romantique|qu|du|des|Gallery|après)\\b', ]) + #33
# lema('[Dd]uraci_ó_n_o', xpos=['\]\]es', ]) + #32
# lema('[Rr]evelaci_ó_n_o', xpos=['\]\]es', ]) + #32
# lema('[Tt]ax_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ') + #32
# lema('[Aa]tenci_ó_n_o', xpos=['\]\]es', ]) + #31
# lema('[Ss]al_ó_n_o', pre='(?:[Ee]l|[Uu]n|[Cc]ada|[Ss]u) ', xpre=['Entr\'acte: ', ], xpos=[' (?:Bovy|Indien|International|de (?:Provence|Mai|thé|la (?:Jeune|Correspondance|Société)|l\')|dans |des |d[\'’´]|du |Premium|[Rr][eé]alités?)', '(?:\]\]es|\.com)', ]) + #31
# lema('[Aa]ctuaci_ó_n_o', xpos=['\]\]es', ]) + #30
# lema('[Ii]n_n_ovaciones_') + #30
# lema('[Ii]nten_ció_n_si[oó]') + #30
# lema('[Rr]econstrucci_ó_n_o', xpos=['\]\]es', ]) + #30
# lema('[Rr]estauraci_ó_n_o', xpos=['\]\]es', ]) + #30
# lema('[Cc]oncentraci_ó_n_o', xpos=['\]\]es', ]) + #29
# lema('[Ii]nscripci_ó_n_o', xpos=['\]\]es', ]) + #29
# lema('[Cc]a_n_ciones_') + #28
# lema('[Ii]ntegraci_ó_n_o', xpos=['\]\]es', ]) + #28
# lema('[Oo]pci_ó_n_o', xpos=['\]\]es', ]) + #28
# lema('[Rr]ecepci_ó_n_o', xpos=['\]\]es', ]) + #28
# lema('[Cc]ertificaci_ó_n_o', xpos=['\]\]es', ]) + #27
# lema('[Cc]onvenci_ó_n_o', xpos=['\]\]es', ]) + #27
# lema('[Ff]inalizaci_ó_n_o', xpos=['\]\]es', ]) + #27
# lema('[Hh]abitaci_ó_n_o', xpos=['\]\]es', ]) + #27
# lema('[Ii]nfecci_ó_n_o', xpos=['\]\]es', ]) + #27
# lema('[Ee]xten_sió_n_ci[oó]') + #26
# lema('[Ii]nstrucci_ó_n_o', xpos=[' pastoral que el', '\]\]es', ]) + #26
# lema('[Mm]utaci_ó_n_o', xpos=['\]\]es', ]) + #26
# lema('[Pp]osesi_ó_n_o', xpos=['\]\]es', ]) + #26
# lema('[Cc]allej_ó_n_o', xpos=[' \(banda', '\]\]es', ]) + #25
# lema('[Cc]omposici_ó_n_o', xpos=['\]\]es', ]) + #25
# lema('[Ee]scuadr_ó_n_o', xpos=['[\]0-9]', ]) + #25
# lema('[Pp]rofesi_ó_n_o', xpos=['\]\](?:es|al|ales|istas?|almente)', ]) + #25
# lema('[Rr]eflexi_ó_n_o', xpre=['Eine ', 'Moment de ', '(?:für|und) ', 'hermeneutische ', 'banda\)\|', 'kritischen ', ], xpos=[' (?:in|über|und|de[rs]|auf|Exhibition|Masterclass|\(banda)\\b', ', (?:Stargazery|Taste)', '\]\]es', ]) + #25
# lema('[Ss]ucesi_ó_n_o', xpos=['\]\]es', ]) + #25
# lema('[Vv]ersi_ó_n en_o') + #25
# lema('[Dd]elegaci_ó_n_o', xpos=['\]\]es', ]) + #24
# lema('[Dd]epresi_ó_n_o', xpos=['\]\]es', ]) + #24
# lema('[Gg]obernaci_ó_n_o', xpos=[' de la Generalidad de Cataluna', '(?:\]|\.gob)', ]) + #24
# lema('[Hh]idroavi_ó_n_o', xpos=['\]\]es', ]) + #24
# lema('[Ii]nmigraci_ó_n_o', xpos=['\]\]es', ]) + #24
# lema('[Ii]nundaci_ó_n_o', xpos=['\]\]es', ]) + #24
# lema('[Ll]iberaci_ó_n_o', xpos=['(?:\]|: Songs)', ]) + #24
# lema('[Pp]antal_ó_n_o', xpre=['San ', '[Ll]e ', 'monsieur ', ], xpos=[' (?:est|trop|et )', '(?:\]\][a-zñ]+|\'])', ]) + #24
# lema('[Pp]rotecci_ó_n_o') + #24
# lema('[Rr]ecaudaci_ó_n_o', xpos=['\]\]es', ]) + #24
# lema('[Rr]emodelaci_ó_n_o', xpos=['\]\]es', ]) + #24
# lema('[Ss]oluci_ó_n_o', xpos=['\]\]es', ]) + #24
# lema('[Cc]icl_ó_n_o', xpos=['\]\]es', ]) + #23
# lema('[Cc]ompetici_ó_n_o', xpos=['\]\]es', ]) + #23
# lema('[Oo]posici_ó_n_o', xpos=['\]\]es', ]) + #23
# lema('[Rr]ei__vindicaciones_n') + #23
# lema('[d]ecisi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Pp]or) ') + #23
# lema('[l]e_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ', xpre=['Juusso ', ]) + #23
# lema('[Oo]ca_sió_n_(?:ci[oó]|sio)') + #22
# lema('[Rr]eedici_ó_n_o', xpos=['\]\]es', ]) + #22
# lema('[Aa]dhesi_ó_n_o', xpre=['& ', 'Macrophage ', '[Ff]ocal ', '[Ii]n ', '[Cc]ell ', ], xpos=[' (?:and|of|Prevention|molecules)', '\]\][a-z]+', ]) + #21
# lema('[Cc]ol__ecciones_l') + #21
# lema('[Cc]onexi_ó_n(?!\]|\.com)_o', xpre=['Madonna ', 'Makarras ', ]) + #21
# lema('[Cc]onstruc_ció_n_i[oó]', xpos=[' dun', ]) + #21
# lema('[Pp]erd_ó_n_o', xpre=['Gerald ', 'Luana ', 'Laurent ', 'S[ae]nt ', ], xpos=['\]\]es']) + #21
# lema('[Tt]ransici_ó_n_o', xpos=['\]\]es', ]) + #21
# lema('[Uu]rbanizaci_ó_n_o', xpos=['\]\]es', ]) + #21
# lema('[Vv]ag_ó_n_o', xpos=['\]\]es', ]) + #21
# lema('[Bb]ot_ó_n_o', xpre=['Joaquín ', ], xpos=['(?:\]|: Houghton)', ]) + #20
# lema('[Cc]elebraci_ó_n_o', xpos=['\]\]es', ]) + #20
# lema('[Dd]ecisi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #20
# lema('[Dd]enominaci_ó_n_o', xpos=['\]\]es', ]) + #20
# lema('[Jj]am_ó_n_o', xpre=['DJ ', 'Joss ', 'Kyle ', 'Nacional ', 'bruja ', ], xpos=[' (?:llega|Alfred|Lucas|Meredith|Gordon)', '\]\]es', ]) + #20
# lema('[Rr]eacci_ó_n_o', xpos=['\]\]es', ]) + #20
# lema('[Rr]ecopilaci_ó_n_o', xpos=['\]\]es', ]) + #20
# lema('[Rr]euni_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Ee]st?a) ', xpre=['Denis de ', ], xpos=[' Island', ]) + #20
# lema('[b]al_ó_n_o', xpos=['\]\]es', ]) + #20
# lema('[Aa]lgod_ó_n_o', xpos=[' Wine', '\]\](?:es|ero)', ]) + #19
# lema('[Cc]aj_ó_n_o', xpos=[' (?:Jinbiao|Run|Blvd|[Pp]ass|Summit|Transit|Boulevard|\(California|Valley|Park)', '(?:\]|\'\', sin tilde)', ', (?:California|Fresno)', ]) + #19
# lema('[Cc]omparaci_ó_n_o', xpre=['\\bE ', ], xpos=['\]\]es', ]) + #19
# lema('[Cc]orrec_c_iones_') + #19
# lema('[Cc]orrupci_ó_n_o', xpos=['\]\]es', ]) + #19
# lema('[Dd]e_cisió_n_(?:si[sc]i[oó]|cici[oó])') + #19
# lema('[Dd]imensi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Oo]tra|[Ss]u|[Dd]e|[Ee]st?a|[Tt]ercera|[Cc]uarta) ', xpos=[' (?:psychique|Films|Records|Data)', ]) + #19
# lema('[Ll]im_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpre=['Ed\. ', 'scorzeta ', ]) + #19
# lema('[Pp]elot_ó_n_o', xpre=['Oranje ', 'Solidaires en ', 'Tollo ', '[Tt]he ', ], xpos=[' (?:Association|d\')', '\]\][a-zñ]+', ]) + #19
# lema('[Pp]resi_ó_n_o', xpos=['\]\]es', ]) + #19
# lema('[Rr]edacci_ó_n_o', xpos=['\]\]es', ]) + #19
# lema('[Ss]eparaci_ó_n_o', xpos=['\]\]es', ]) + #19
# lema('[Ss]ubregi_ó_n_o', xpre=['Africa ', 'Papuan ', ], xpos=['\]\]es', ]) + #19
# lema('[Uu]ni_ó_n (?:Dem[oó]crata|Estepona|Sovi[eé]tica)_o') + #19
# lema('[Aa]daptaci_ó_n_o') + #18
# lema('[Aa]par_i_ciones_a') + #18
# lema('[Cc]olec_c_iones_') + #18
# lema('[Cc]oncesi_ó_n_o', xpos=['\]\]es', ]) + #18
# lema('[Ee]recci_ó_n_o', xpos=['\]\]es', ]) + #18
# lema('[Ee]scorpi_ó_n_o', xpre=['Di ', 'Milo de ', ], xpos=['\]\]es', ]) + #18
# lema('[Ee]valuaci_ó_n_o', xpos=['\]\]es', ]) + #18
# lema('[Ee]xcepci_ó_n_o', xpos=['\]\]es', ]) + #18
# lema('[Pp]ante_ó_n_o', xpos=['\]\]es', ]) + #18
# lema('[Dd]ifusi_ó_n_o', xpre=['Fonogram ', ], xpos=['\]\]es', ]) + #17
# lema('[Ee]liminaci_ó_n_o', xpos=['\]\]es', ]) + #17
# lema('[Ee]xpedici_ó_n_o', xpos=[' Antarctic', '\]\]es', ]) + #17
# lema('[Ee]xportaci_ó_n_o', xpos=['\]\]es', ]) + #17
# lema('[Ii]ntervenci_ó_n_o', xpre=['Ajoute ', ], xpos=['\]\]es', ]) + #17
# lema('[Oo]casi_ó_n_o', xpos=['\]\]es', ]) + #17
# lema('[Pp]e_ó_n_o', xpre=['Eddie ', 'Dictyna ', 'Carole ', 'Domínguez ', 'Lazy ', 'Olatz ', ], xpos=[' – Batería', '\]\]es', ]) + #17
# lema('[Pp]end_ó_n_o', xpre=['Dan y su ', ], xpos=['\]\]es', ]) + #17
# lema('[Pp]etici_ó_n(?!\]|\.xsd)_o') + #17
# lema('[Rr]ecuperaci_ó_n_o', xpos=['\]\]es', ]) + #17
# lema('[Ss]anci_ó_n_o', xpos=['\]\]es', ]) + #17
# lema('[Aa]grupaci_ó_n_o', xpos=['\]\]es', ]) + #16
# lema('[Cc]ongregaci_ó_n_o', xpos=['\]\]es', ]) + #16
# lema('[Dd]estituci_ó_n_o', xpos=['\]\]es', ]) + #16
# lema('[Dd]etenci_ó_n_o', xpos=['\]\]es', ]) + #16
# lema('[Jj]onr_ó_n_o', xpos=['\]\]es', ]) + #16
# lema('[Ll]egislaci_ó_n_o', xpre=['Nueva Espana\. ', ], xpos=['\]\]es', ]) + #16
# lema('[Mm]igraci_ó_n_o', xpos=['\]\]es', ]) + #16
# lema('[Mm]ill_ó_n_o', pre='([Mm]edio|[Uu]n|[Ee]l) ') + #16
# lema('[Mm]oj_ó_n_o', xpre=['Benedetto ', 'Giuseppe '], xpos=[' Records', '\]\]es', ]) + #16
# lema('[Ss]uspen_sió_n_ci[oó]') + #16
# lema('[Vv]iolaci_ó_n_o', xpos=['\]\]es', ]) + #16
# lema('[Bb]omb_ó_n_o', xpos=[' Evolution', '(?:\. Aqua|\]\]es)', ]) + #15
# lema('[Cc]amale_ó_n_o', xpos=[' Records', '\]\]es', ]) + #15
# lema('[Cc]hampiñ_ó_n_o', xpos=['\]\]es', ]) + #15
# lema('[Cc]ivilizaci_ó_n_o', xpos=['\]\]es', ]) + #15
# lema('[Ii]nvasi_ó_n_o', pre='\\b(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|otra|de|[Pp]rimera|[Ss]egunda|[Tt]ercera|[Ss]éptima) ') + #15
# lema('[Jj]urisdicci_ó_n_o', xpos=['\]\]es', ]) + #15
# lema('[Jj]uri_sdicció_n_dicci[oó]') + #1
# lema('[Jj]uri_sdiccio_nal(?:es|)_dicci[oó]') + #1
# lema('[Mm]edall_ó_n_o', xpos=['\]\]es', ]) + #15
# lema('[Nn]utrici_ó_n_o', xpos=['\]\]es', ]) + #15
# lema('[Rr]eproducci_ó_n_o', xpos=['\]\]es', ]) + #15
# lema('[Uu]nificaci_ó_n_o', xpos=['\]\]es', ]) + #15
# lema('[Cc]ombinaci_ó_n_o', xpos=['\]\]es', ]) + #14
# lema('[Cc]onstelaci_ó_n_o', xpos=['\]\]es', ]) + #14
# lema('[Cc]ontinuaci_ó_n_o') + #14
# lema('[Ee]scal_ó_n_o', xpre=['California\)\|', 'Max ', ], xpos=[' (?:de Fonton|\(California)', '\]\]es', ]) + #14
# lema('[Ee]vasi_ó_n_o', xpre=['Jailbreak ', 'Bridging ', 'Cartwheel ', 'Citro[eë]n ', 'Filter ', 'Her ', 'Matrix ', 'Roman de ', 'Somersault ', '[Ll]\'', '[Tt]ax ', 'and ', 'backflip ', 'd\'', 'legged ', ], xpos=[' (?:Films|of|par|Clause)', '(?:["\]]|, and)', ]) + #14
# lema('[Mm]aldici_ó_n_o', xpos=['\]\]es', ]) + #14
# lema('[Oo]raci_ó_n_o', xpos=['\]\]es', ]) + #14
# lema('[Pp]rot_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpos=[' *[1-9][0-9]*', ' (?:Block|Prevé|Exora|Satria|en la clase|Synchrotron)', '\]\]es', ]) + #14
# lema('[Pp]royecci_ó_n_o', xpos=['\]\]es', ]) + #14
# lema('[Tt]elevisi_ó_n (?:por|[Ss]atelital|[Pp][uú]blica)_o') + #14
# lema('[Tt]ransmi_sió_n_ci[oó]') + #14
# lema('[Vv]egetaci_ó_n_o', xpos=['\]\]es', ]) + #14
# lema('[Aa]d_aptació_n_pataci[oó]') + #13
# lema('[Aa]limentaci_ó_n_o', xpos=['(?:\]|\.es)', ]) + #13
# lema('[Aa]nfitri_ó_n_o', xpos=['\]\]es', ]) + #13
# lema('[Aa]nglosaj_ó_n_o', xpos=['\]\](?:as?|es)', ]) + #13
# lema('[Aa]plicaci_ó_n_o', pre='(?:[Dd]e|[Ll]a|[Uu]na) ') + #13
# lema('[Cc]ant_ó_n_o', pre='(?:[Ee]l|[Dd]el|[Uu]n|[Cc]ada|[Ss]u) ', xpre=['estatjants ', ], xpos=[' (?:Tech|Hall|Ticino)', ]) + #13
# lema('[Cc]om__unicaciones_m') + #13
# lema('[Cc]onducci_ó_n_o', xpos=['\]\]es', ]) + #13
# lema('[Cc]onfesi_ó_n_o', xpre=['A ', 'Yô ', ], xpos=['\]\]es', ]) + #13
# lema('[Dd]edicaci_ó_n_o', xpos=['\]\]es', ]) + #13
# lema('[Dd]esaparici_ó_n_o', xpos=['\]\]es', ]) + #13
# lema('[Dd]imisi_ó_n_o', xpos=['\]\]es', ]) + #13
# lema('[Dd]ocumentaci_ó_n_o', xpre=['Centre International de ', ], xpos=['  e poder', '\]\]es', ]) + #13
# lema('[Ee]dific__aciones_i') + #13
# lema('[Ee]lecci_o_nes_ó') + #13
# lema('[Ee]x_h_ibi(?:ó|ciones)_') + #13
# lema('[Ee]xplotaci_ó_n_o', xpos=['\]\]es', ]) + #13
# lema('[Ee]xposi_ci_ones_(?:|sici|si)') + #13
# lema('[Ee]xpresi_ó_n_o', pre='(?:[Dd]e|[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ', xpre=['L\'', ], xpos=[' t', '\.tv', ]) + #13
# lema('[Gg]orri_ó_n_o', xpos=['\]\]es', ]) + #13
# lema('[Ii]nnovaci_ó_n_o', xpos=['\]\]es', ]) + #13
# lema('[Ii]nquisici_ó_n_o', xpos=[' á ', '(?:\]|\.scd|, chronista)', ]) + #13
# lema('[Ii]nstalaci_ó_n_o', xpos=['\]\]es', ]) + #13
# lema('[Ss]alvaci_ó_n_o', xpos=['\]\]es', ]) + #13
# lema('[Tt]elecomunicaci_ó_n_o', xpos=['\]\]es', ]) + #13
# lema('[Aa]fici_ó_n_o', xpos=['\]\](?:es|ad[ao]s?)', ]) + #12
# lema('[Aa]lucinaci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Aa]mpliaci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Cc]alificaci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Cc]anci_o_nes_ó') + #12
# lema('[Cc]intur_ó_n_o', xpre=['Ride ', ], xpos=['\]\]es', ]) + #12
# lema('[Cc]ontaminaci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Cc]oordinaci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Cc]oronaci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Dd]emostraci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Ee]jecuci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Ee]stimaci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Ee]xploraci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Ee]xtinci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Ff]abricaci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Ii]luminaci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Ii]ncorporaci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Pp]articipaci_o_nes_ó') + #12
# lema('[Pp]lanificaci_ó_n_o', xpos=['(?:\]|\.gob)', ]) + #12
# lema('[Pp]reparaci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Tt]ransformaci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Vv]otaci_ó_n_o', xpos=['\]\]es', ]) + #12
# lema('[Aa]ctualizaci_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Aa]doraci_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Aa]firmaci_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Cc]irculaci_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Cc]o_nmemoració_n_(?:nmemoracio|memoraci[oó])', xpos=['\]\]es', ]) + #11
# lema('[Cc]ompilaci_ó_n_o', xpos=[' curata', '\]\]es', ]) + #11
# lema('[Cc]onformaci_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Dd]estrucci_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Ee]mbri_ó_n_o', xpos=['\]\](?:es|ari[ao]s?)', ]) + #11
# lema('[Ff]acturaci_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Ff]ermi_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Ff]racci_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Hh]omogen_eizació_n_(?:izaci[oó]|eizacio)') + #11
# lema('[Ii]ncisi_ó_n_o', xpre=['Second ', ], xpos=['\]\]es', ]) + #11
# lema('[Mm]ansi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpos=[' House', ]) + #11
# lema('[Mm]edici_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Pp]recipitaci_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Rr]educci_ó_n_o', xpos=['\.gov', '\]\]es', ]) + #11
# lema('[Rr]eglamentaci_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Rr]ehabilitaci_ó_n_o') + #11
# lema('[Rr]otaci_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Ss]imulaci_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[Tt]entaci_ó_n_o', xpos=['\]\]es', ]) + #11
# lema('[b]ill_ó_n_o', xpos=[' (?:of)', '\]\][a-zñ]+', ]) + #11
# lema('[Aa]probaci_ó_n_o', xpos=['\]\]es', ]) + #10
# lema('[Bb]uz_ó_n_o', xpre=['Beverlee ', 'Freddy ', 'Bernard ', 'du ', ], xpos=['\]\]es', ]) + #10
# lema('[Cc]ombusti_ó_n_o', pre='(?:[Ll]a|[Dd]e) ', xpos=[' (?:et|en général)']) + 
# lema('[Cc]ombusti_ó_n_o', pre='(?:[Ll]a|[Dd]e) ', xpos=[' et', ]) + #10
# lema('[Cc]ongesti_ó_n_o', xpre=['Hors ', 'ease ', 'of ', 'the ', 'traffic ', 'venous ', ], xpos=[' (?:[Aa]voidance|[Hh]andling|[Tt]hreshold|[Pp]ricing|Tax|of|Relief|Window|charges?|window|[Nn]otification|[Mm]itigation|[Ii]nterpretation|[Rr]eduction|[Cc]osts|[Cc]ontrol)', ]) + #10
# lema('[Cc]onspiraci_ó_n_o', xpos=['\]\]es', ]) + #10
# lema('[Cc]ooperaci_ó_n_o', xpos=['\]\]es', ]) + #10
# lema('[Dd]esambiguaci_ó_n(?!\])_o') + #10
# lema('[Dd]escalificaci_ó_n_o', xpos=['\]\]es', ]) + #10
# lema('[Ee]corregi_ó_n(?!\])_o') + #10
# lema('[Ee]d_i_ciones_') + #10
# lema('[Ee]spol_ó_n_o', xpos=['\]\]es', ]) + #10
# lema('[Ii]__dentificaciones_n') + #10
# lema('[Ii]dentificaci_ó_n_o', xpos=['\]\]es', ]) + #10
# lema('[Ii]mpresi_ó_n_o', xpos=[' de Felipe Mey', '\]\]es', ]) + #10
# lema('[Ii]nspiraci_ó_n_o', xpos=['\]\]es', ]) + #10
# lema('[Ll]icitaci_ó_n_o', xpos=['\]\]es', ]) + #10
# lema('[Mm]unici_ó_n_o', xpos=['(?:\]|\.org)', ]) + #10
# lema('[Oo]bservaci_ó_n_o', xpos=['\]\]es', ]) + #10
# lema('[Pp]ensi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpre=['Filles de ', ], xpos=[' des']) + #10
# lema('[Rr]ecreaci_ó_n_o', xpos=['\]\]es', ]) + #10
# lema('[Ss]umisi_ó_n_o', xpos=['\]\]es', ]) + #10
# lema('[Tt]ap_ó_n_o', xpre=['Michel ', 'Serge ', ], xpos=['\]\]es', ]) + #10
# lema('[Tt]ripulaci_ó_n_o', xpos=['\]\]es', ]) + #10
# lema('[Aa]ctuaci_o_nes_ó') + #9
# lema('[Aa]leaci_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Aa]rticulaci_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Bb]uf_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Cc]amar_ó_n_o', xpre=['J\. ', 'héros de ', ], xpos=[' (?:Marvel|Ochs|Jackson|Silverek)', '(?:\]|, la révolution)', ]) + #9
# lema('[Cc]lasificaci_o_nes_ó') + #9
# lema('[Cc]olisi_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Cc]ontrataci_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Ee]levaci_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Ee]xaltaci_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Ee]xplicaci_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Ee]xtensi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #9
# lema('[Ee]xtrusi_ó_n_o', xpre=['Screw ', 'The ', ], xpos=['(?:\]\][a-z]+|: Battlehymns)', ]) + #9
# lema('[Ff]ortificaci_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Gg]alp_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Ii]nflexi_ó_n_o', xpre=['d\'', 'and '], xpos=['\]\]es', ]) + #9
# lema('[Ii]ntera_c_ciones_') + #9
# lema('[Ii]nvestigaci_o_nes_ó') + #9
# lema('[Mm]elocot_ó_n_o', xpos=['\]\](?:es|er[ao]s?)', ]) + #9
# lema('[Mm]enci_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Pp]roporci_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Pp]ublicaci_o_nes_ó') + #9
# lema('[Pp]urificaci_ó_n_o', xpos=[' \(Peñuelas', '\]\]es', ]) + #9
# lema('[Rr]ealizaci_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Ss]educci_ó_n_o', xpos=['\]\]es', ]) + #9
# lema('[Tt]amp_ó_n_o', xpre=['\\bdu ', 'Zombie ', '[Ll]e ', ], xpos=[' Disease', '\]\]es', ]) + #9
# lema('[Vv]ersi_o_nes_ó') + #9
# lema('[Aa]dvocaci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Aa]gresi_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Aa]tracci_ó_n_o', xpos=['[\]3]', ]) + #8
# lema('[Aa]udici_ó_n_o', xpos=[' Irritable', '\]\]es', ]) + #8
# lema('[Cc]anel_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Cc]ircunvalaci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Cc]omputaci_ó_n_o', xpos=['(?:\]|\.facyt)', ]) + #8
# lema('[Cc]ondici_ó_n_o', pre='(?:[Ll]as?|[Uu]nas?|[Ss]us?) ') + #8
# lema('[Cc]onsolaci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Cc]onversaci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Cc]orrecci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Dd]ecoraci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Dd]evoci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Dd]istinci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Dd]ivisi_ó_n [Pp]ol[ií]tica_o') + #8
# lema('[Dd]onaci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Ff]og_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Ii]ndemnizaci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Ii]ntenci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Ii]nversi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpos=['\]\]es', ]) + #8
# lema('[Ll]ap_ó_n_o', xpre=['Gúdar\+Hazte ', 'Botaniques de ', 'Parlons ', '\\bDo ', '\\bun ', ], xpos=['\]\](?:as?|es)', ]) + #8
# lema('[Mm]ont_ó_n_o', xpre=['Julie ', 'Leonard ', 'de ', ], xpos=[' \(Eccles', '(?:\]|, (?:Canad[áa]|Gran|Bradley))', ]) + #8
# lema('[Nn]avegaci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Nn]otaci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Oo]vaci_ó_n(?!\]|\.pe|\.com)_o') + #8
# lema('[Pp]ercepci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Pp]eregrinaci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Pp]laneaci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Pp]lantaci_ó_n(?!\])_o') + #8
# lema('[Pp]ort_ó_n_o', xpre=['Pamela '], xpos=[' (?:d[\'’]|Down|Plantation)', '\]\]es', ]) + #8
# lema('[Pp]ropagaci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Pp]rostituci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Rr]ecolecci_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Rr]elaci_o_nes_ó') + #8
# lema('[Rr]epetici_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Ss]aj_ó_n_o', xpos=['\]\]es', ]) + #8
# lema('[Aa]dmisi_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Aa]lmid_ó_n_o', xpre=['Rosales '], xpos=['\]\]es', ]) + #7
# lema('[Aa]pag_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Cc]ertifi_cació_n_(?:a[cs]i[oó]|casi[oó])') + #7
# lema('[Cc]hicharr_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Cc]ircunscripci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Cc]ircunvoluci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Cc]olch_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Cc]olonizaci_ó_n_o', xpos=['\.com', ]) + #7
# lema('[Cc]onfirmaci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Cc]ontribuci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Cc]onurbaci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Cc]ulminaci_ó_n(?!\])_o') + #7
# lema('[Dd]isertaci_ó_n_o', xpos=['\]\]es', ' physico']) + #7
# lema('[Ee]quipaci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Ee]rupci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Ee]xcavaci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Ee]xpan_sió_n_ci[oó]') + #7
# lema('[Hh]ormig_ó_n_o', xpos=['\]\](?:es|ad[ao]s?)', ]) + #7
# lema('[Ii]mportaci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Ii]nvitaci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Jj]arr_ó_n_o', xpre=['& ', ], xpos=['\]', ' (?:Collins|Vosburg)']) + #7
# lema('[Mm]asterizaci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Pp]acificaci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Pp]enetraci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Pp]ersecuci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Pp]rivatizaci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Rr]adiodifusi_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Rr]edenci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Rr]eputaci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Rr]espiraci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Ss]ensaci_ó_n_o') + #7
# lema('[Ss]ensaci_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Tt]abl_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Tt]raici_ó_n_o', xpos=['\]\]es', ]) + #7
# lema('[Aa]decuaci_ó_n(?!\])_o') + #6
# lema('[Aa]luvi_ó_n_o', xpos=['\]\](?:es|al|ales)', ]) + #6
# lema('[Aa]mputaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Aa]nexi_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Aa]nunciaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Aa]utorizaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Cc]apacitaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Cc]odificaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Cc]ompetició_n__m?', xpos=[', reglamentacions']) + #6
# lema('[Cc]ompresi_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Cc]omuni_ó_n_o', xpre=['cathechismo de la ', ], xpos=['(?:\]|\.org)', ]) + #6
# lema('[Cc]onclusi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #6
# lema('[Cc]osmovisi_ó_n_o', xpos=[' des', '\]\]es', ]) + #6
# lema('[Dd]erivaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Dd]esignaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Dd]etecci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Dd]isposici_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Ee]migraci_ó_n_o', xpos=['(?:\.ca|\]\]es)', ]) + #6
# lema('[Ee]moci_ó_n(?![\]0-9])_o') + #6
# lema('[Ee]staci_o_nes_ó') + #6
# lema('[Ee]xplosi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #6
# lema('[Ee]xpropiaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Ff]ermentaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Gg]raduaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Ii]mplementaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Ii]nclusi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #6
# lema('[Ii]nserci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Ii]ntersecci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Ii]ntoxicaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Jj]ubilaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Ll]ecci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Ll]ocaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Mm]odificaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Nn]acionalizaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Nn]egociaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Nn]umeraci_ó_n_o') + #6
# lema('[Nn]umeraci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Oo]bsesi_ó_n_o', xpre=['l[\'’]', ], xpos=['(?:\])', ]) + #6
# lema('[Oo]rej_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Oo]rientaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Oo]xidaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Pp]artici_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Pp]ercusi_o_nes_ó') + #6
# lema('[Pp]ez_ó_n_o', xpre=['Andre ', 'Jean-Baptiste ', ], xpos=['\]\]es', ]) + #6
# lema('[Pp]orci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Pp]romulgaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Rr]eelecci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Rr]eencarnaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Rr]egi_o_nes_ó') + #6
# lema('[Rr]eligi_ó_n [Cc]at[oó]lica_o') + #6
# lema('[Rr]eligi_ó_n_o', pre='(?:[Uu]na|[Cc]ada|[Ss]u) ') + #6
# lema('[Rr]eorganizaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Rr]epresi_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Rr]eversi_ó_n_o', xpre=[';', 'Series ', 'bit ', ], xpos=[' to', '\]\]es', ]) + #6
# lema('[Ss]elecci_o_nes_ó') + #6
# lema('[Ss]eñalizaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Ss]if_ó_n(?!\])_o') + #6
# lema('[Tt]if_ó_n_o', xpos=['(?:[1-9\]])', ]) + #6
# lema('[Tt]ra_nsliteracio_nes_(?:sliteraci[oó]|nsliteració)') + #6
# lema('[Uu]tilizaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Vv]inculaci_ó_n_o', xpos=['\]\]es', ]) + #6
# lema('[Aa]creditaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Aa]cumulaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Aa]dicci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Aa]dici_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Aa]djudicaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Aa]gregaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Aa]ler_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Aa]niquilaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Aa]notaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Aa]proximaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Aa]scensi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #5
# lema('[Aa]utodeterminaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Aa]utomatizaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Bb]ar_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]l?) ', xpre=['\\bpar ', 'acuerdo ', ], xpos=[' (?:Michele|Reiter|Cohen|Corbin|Wolman|Samedi|Zemo|Gattoni)', ', el', ]) + #5
# lema('[Bb]eatificaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Bb]endici_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Bb]odeg_ó_n(?!\])_o') + #5
# lema('[Cc]aracterizaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Cc]ivilizaci_o_nes_ó') + #5
# lema('[Cc]ondecoraci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Cc]onfiguraci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Dd]emarcaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Dd]etonaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Dd]iapas_ó_n_o', xpre=['[Ll]e ', '[Tt]he ', 'revue ', ], xpos=[' (?:Découverte|Records|[Dd]|\(revista)\\b', '(?:, Scherzo|’s|\'|\]\])', ]) + #5
# lema('[Ee]scalaf_ó_n(?!\])_o') + #5
# lema('[Ee]x_cepció_n_epci[oó]') + #5
# lema('[Gg]laciaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Hh]ipertensi_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Ii]maginaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Ii]mitaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Ii]n_strucció_n_trucci[oó]', xpos=['\]\]es', ]) + #5
# lema('[Ii]nclinaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Ii]nspecci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Ii]nten_cio_nes_si[oó]') + #5
# lema('[Ii]ntimidaci_ó_n(?!\])_o') + #5
# lema('[Ii]rrigaci_ó_n(?!\])_o') + #5
# lema('[Ll]egalizaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Mm]arat_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ') + #5
# lema('[Mm]el_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ', xpre=['Saye ', 'abbati ', 'listado ', 'musicales ', ], xpos=[' (?:Music|Kinenbi)', ', Naver', ]) + #5
# lema('[Mm]odernizaci_ó_n_o', xpos=['(?:\]|\.(?:cl|gob))', ]) + #5
# lema('[Mm]otivaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Mm]ultiplicaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Nn]ominaci_o_nes_ó') + #5
# lema('[Oo]bligaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Oo]ca_sió_n_ci[oó]') + #5
# lema('[Oo]rdenaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Oo]rganizaci_o_nes_ó') + #5
# lema('[Pp]erdig_ó_n_o', xpre=['Pierre ', 'Troubadour ', ], xpos=[' d', '\]\][a-zñ]+', ]) + #5
# lema('[Pp]ostulaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Pp]recisi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Cc]on| y| de) ', xpos=[' (?:Bass|Weapons)', ]) + #5
# lema('[Pp]remiaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Rr]adiaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Rr]ebeli_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Ee]sta|[Ee]sa|[Ee]n) ', xpos=['(?:\]|\.org)', ]) + #5
# lema('[Rr]eestructuraci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Rr]efundaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Rr]egi_ó_n_o', pre='(?:[Uu]na|[Cc]ada|[Ss]u) ', xpos=[' d\'Ambovombe', ]) + #5
# lema('[Rr]egionalizaci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Rr]egulaci_ó_n_o', xpos=['(?:[\]1])', ]) + #5
# lema('[Rr]estricci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Ss]alm_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ', xpre=['áerea ', 'templo ', ], xpos=[' (?:Bay|Leap|Chase)', ' P\.', ]) + #5
# lema('[Ss]ustituci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Tt]racci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Tt]ranscripci_ó_n_o', xpos=['\]\]es', ]) + #5
# lema('[Tt]urr_ó_n_o', xpos=[' Kofi', '\]\]es', ]) + #5
# lema('[Vv]iolaci_o_nes_ó') + #5
# lema('[g]asc_ó_n_o', xpre=['[Ll]e ', 'ritme ', 'Gentilòme ', '[Cc]atonet ', '[Cc]atonet ritme ', 'dialecte ', 'gentilòme ', ], xpos=[' du\\b', '"', ]) + #5
# lema('Gab_ó_n_o', pre='(?:[Dd]e|[Ee]n) ', xpos=[' [Aa]irlines', ]) + #4
# lema('[Aa]bolici_ó_n_o', xpre=['pola ', ], xpos=['\]\]es', ]) + #4
# lema('[Aa]bsorci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Aa]claraci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Aa]dmiraci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Aa]dquisici_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Aa]glomeraci_ó_n_o', xpos=[' deu', '\]\]es', ]) + #4
# lema('[Aa]lineaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Cc]alz_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Cc]anonizaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Cc]apitulaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Cc]occi_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Cc]omprensi_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Cc]onsolidaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Cc]ontenci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Cc]ontradicci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Cc]oproducci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Cc]uraci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Dd]ataci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Dd]ecepci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Dd]educci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Dd]eforestaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Dd]eformaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Dd]efunci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Dd]iscriminaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Dd]istinci_o_nes_ó') + #4
# lema('[Dd]ivulgaci_ó_n_o', xpos=['(?:\]\][a-zñ]+|\.famaf)', ]) + #4
# lema('[Ee]dici_o_nes_ó') + #4
# lema('[Ee]laboraci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ee]lec_ció_n_i[oó]') + #4
# lema('[Ee]quitaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ee]specificaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ee]vangelizaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ee]xhibici_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ee]xposici_o_nes_ó') + #4
# lema('[Ff]iltraci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ff]rancmas_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ff]unci_o_nes_ó') + #4
# lema('[Hh]abilitaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ii]lustrac__iones_c') + #4
# lema('[Ii]mprovisaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ii]mputaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ii]nducci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ii]niciaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ii]nstituci_o_nes_ó') + #4
# lema('[Ii]nsurrecci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Mm]anipulaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Mm]editaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Mm]icrorregi_ó_n(?!\])_o') + #4
# lema('[Mm]oci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Mm]otorizaci_ó_n(?!\])_o') + #4
# lema('[Nn]ormalizaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Oo]ca_s_ionando_c') + #4
# lema('[Oo]ptimizaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Pp]o_sició_n_(?:ci[sc]i[oó]|sisi[oó]n)') + #4
# lema('[Pp]ose_sió_n_ci[oó]') + #4
# lema('[Pp]ositr_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #4
# lema('[Pp]recauci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Pp]revenci_ó_n_o') + #4
# lema('[Pp]roclamaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Pp]roducci_o_nes_ó') + #4
# lema('[Pp]rovisi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #4
# lema('[Rr]atificaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Rr]emoci_ó_n(?!\])_o') + #4
# lema('[Rr]eparaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Rr]eplicaci_ó_n(?!\])_o') + #4
# lema('[Rr]epresentaci_o_nes_ó') + #4
# lema('[Rr]evisi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #4
# lema('[Rr]oset_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ss]atisfacci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Ss]edimentaci_ó_n(?!\])_o') + #4
# lema('[Ss]upervisi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Bb]ajo) ', xpre=['sous ', ], xpos=[', Tequivo', '\]\]es', ]) + #4
# lema('[Tt]ensi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|cierta) ', xpos=[' (?:narrative|érotique)', ]) + #4
# lema('[Tt]ibur_o_nes_ó') + #4
# lema('[Tt]ransfiguraci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Tt]raslaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Vv]ibraci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[Vv]ocaci_ó_n_o', xpos=['\]\]es', ]) + #4
# lema('[p]ich_ó_n_o', xpos=[' quand', '\]\]es', ]) + #4
# lema('[Aa]bstenci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Aa]bstracci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Aa]ceptaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Aa]ctivaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Aa]gitaci_ó_n(?!\])_o') + #3
# lema('[Aa]nimaci_o_nes_ó') + #3
# lema('[Aa]parici_o_nes_ó') + #3
# lema('[Aa]pelaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Aa]portaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Aa]spiraci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Aa]utomoci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Cc]alefacci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Cc]ampe_o_nes_ó') + #3
# lema('[Cc]ancelaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Cc]añ_o_nes_ó') + #3
# lema('[Cc]ertifi_cacio_nes_(?:a[cs]i[oó]|casi[oó]|cació)') + #3
# lema('[Cc]imarr_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpre=['[Cc]ondado ', '[Mm]unicipio ', ], xpos=[' (?:Heritage|Cutoff)', ]) + #3
# lema('[Cc]o_mposició_n_(?:npo[cs]i[cs]i[oó]|mpoci[cs]i[oó]|mposisi[oó])') + #3
# lema('[Cc]oalici_o_nes_ó') + #3
# lema('[Cc]omercializaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Cc]ompensaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Cc]ompilaci_o_nes_ó') + #3
# lema('[Cc]onciliaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Cc]ond_ó_n_o', pre='(?:[Ee]l|[Dd]el|[Uu]n|[Cc]ada|[Ss]u) ', xpos=[' Clú', ]) + #3
# lema('[Cc]ondensaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Cc]onmoci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Cc]onsideraci_ó_n_o') + #3
# lema('[Cc]onsideraci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Cc]onversi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpos=[' (?:d|de l\'art|du|des)', ]) + #3
# lema('[Cc]onvicci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Cc]oraz_o_nes_ó') + #3
# lema('[Cc]reaci_o_nes_ó') + #3
# lema('[Dd]esamortizaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Dd]eserci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Dd]esolaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Dd]eterminaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Dd]icci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Dd]iferenciaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Dd]ilataci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Dd]irecci_o_nes_ó') + #3
# lema('[Dd]iscusi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpos=['\]\]es', ]) + #3
# lema('[Dd]isoluci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Dd]istracci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Dd]ivisi_o_nes_ó') + #3
# lema('[Dd]ominaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Ee]mis_io_nes_(?:sió|ió)') + #3
# lema('[Ee]misi_o_nes_ó') + #3
# lema('[Ee]mulaci_ó_n(?!\])_o') + #3
# lema('[Ee]ncuadernaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Ee]numeraci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Ee]rudici_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Ee]xplo_sió_n_cio') + #3
# lema('[Ee]xtorsi_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Ff]alsificaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Ff]ijaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Ff]ilmaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Ff]inanciaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Ff]loraci_ó_n(?!\])_o') + #3
# lema('[Ff]undici_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Gg]eolocalizaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Gg]estaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Gg]lobalizaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Gg]rabaci_o_nes_ó') + #3
# lema('[Hh]ibridaci_ó_n(?!\])_o') + #3
# lema('[Ii]nstrumentaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Ii]nterconexi_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Ii]nterrogaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Ii]nva_sio_nes_(?:ci[oó]|sió)') + #3
# lema('[Ii]nva_sió_nes_ci[oó]') + #3
# lema('[Ii]rritaci_ó_n(?!\])_o') + #3
# lema('[Jj]urisdicci_o_nes_ó') + #3
# lema('[Ll]e_o_nes_ó') + #3
# lema('[Mm]ediaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Mm]edicaci_ó_n(?!\])_o') + #3
# lema('[Mm]ejill_ó_n(?!\])_o') + #3
# lema('[Mm]enci_o_nes_ó') + #3
# lema('[Mm]odulaci_ó_n(?!\])_o') + #3
# lema('[Mm]orm_ó_n_o', pre='(?:[Ee]l|[Uu]n|[Cc]ada|[Ss]u) ', xpre=['Yu\'', ]) + #3
# lema('[Nn]arraci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Nn]egaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Nn]otificaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Oo]casi_o_nes_ó') + #3
# lema('[Oo]peraci_o_nes_ó') + #3
# lema('[Oo]scilaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Pp]ercu_sió_n_ci[oó]') + #3
# lema('[Pp]erfecci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Pp]ersonificaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Pp]ist_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpre=['Sinfonía ', 'coup ', ], xpos=[', Honegger', ]) + #3
# lema('[Pp]oblaci_o_nes_ó') + #3
# lema('[Pp]retensi_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Pp]ropulsi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ', xpos=[' (?:par |Photonique)', ]) + #3
# lema('[Rr]eactivaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Rr]ectificaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Rr]epoblaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Rr]euni_o_nes_ó') + #3
# lema('[Ss]ecesi_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Ss]ubsecci_ó_n(?!\])_o') + #3
# lema('[Ss]uspensi_ó_n(?! d[\'’]armes)_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #3
# lema('[Tt]elevisi_o_nes_ó') + #3
# lema('[Tt]im_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ', xpos=[' (?:Screech|David|Menon|of)', '\]\]es', ]) + #3
# lema('[Tt]ra_smisió_n_nsmicio') + #3
# lema('[Tt]áx_ó_n(?!\])_o') + #3
# lema('[Vv]aloraci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Vv]isitaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[Vv]ocalizaci_ó_n_o', xpos=['\]\]es', ]) + #3
# lema('[r]ay_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpre=['d\'', ], xpos=[' (?:croissant|de trois)', ]) + #3
# lema('[t]ac_ó_n_o') + #3
# lema('[Aa]bominaci_ó_n(?!\])_o') + #2
# lema('[Aa]bsoluci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Aa]celeraci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Aa]daptaci_o_nes_ó') + #2
# lema('[Aa]daptaci_o_nes_ó') + #2
# lema('[Aa]dopci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Aa]lteraci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Aa]mbici_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Aa]ntelaci_ó_n(?!\])_o') + #2
# lema('[Aa]nticipaci_ó_n(?!\])_o') + #2
# lema('[Aa]nulaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Aa]prehensi_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Aa]rgumentaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Aa]rticulaci_o_nes_ó') + #2
# lema('[Aa]signaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Aa]tol_ó_n(?!\])_o') + #2
# lema('[Aa]tracci_o_nes_ó') + #2
# lema('[Aa]veriguaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Cc]allej_o_nes_ó') + #2
# lema('[Cc]ami_o_nes_ó') + #2
# lema('[Cc]ant_ó_n_o', pre='[Aa] ', xpre=['franquicia ', 'interpretar ', 'permitió ', ], xpos=['\]\]es']) + #2
# lema('[Cc]aptaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Cc]ard_ó_n_o', pre='(?:[Ee]l|[Dd]el|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpos=[' Walker', ]) + #2
# lema('[Cc]ircuncisi_ó_n_o', xpos=[' on\\b', '\]\]es', ]) + #2
# lema('[Cc]ircunnavegaci_ó_n_o', xpos=['\]\](?:es|al|ales)', ]) + #2
# lema('[Cc]lonaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Cc]o_mposicio_nes_(?:npo[cs]i[cs]i[oó]|mpoci[cs]i[oó]|mposisi[oó]|mposició)') + #2
# lema('[Cc]ol_o_nes_ó') + #2
# lema('[Cc]olecci_o_nes_ó') + #2
# lema('[Cc]olocaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Cc]omisi_o_nes_ó') + #2
# lema('[Cc]omplicaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Cc]on_strucció_n_truccio') + #2
# lema('[Cc]ondici_o_nes_ó') + #2
# lema('[Cc]onfecci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Cc]onfecci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Cc]onfes_io_nes_(?:si[oó]|ió)', xpos=[' sacerdotum', ]) + #2
# lema('[Cc]onjugaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Cc]onmutaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Cc]onsagraci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Cc]ontracci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Cc]onvecci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Cc]orrelaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Dd]_o_nes_ó') + #2
# lema('[Dd]eclaraci_o_nes_ó') + #2
# lema('[Dd]egradaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Dd]eliberaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Dd]epredaci_ó_n(?!\])_o') + #2
# lema('[Dd]epuraci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Dd]erogaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Dd]esaparici_o_nes_ó') + #2
# lema('[Dd]escomposici_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Dd]eshidrataci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Dd]esnutrici_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Dd]estilaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Dd]esviaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Dd]evastaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Dd]evoluci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Dd]isyunci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Dd]iversi_o_nes_ó') + #2
# lema('[Dd]iversi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #2
# lema('[Ee]_o_nes_ó') + #2
# lema('[Ee]moci_o_nes_ó') + #2
# lema('[Ee]quivocaci_ó_n(?!\])_o') + #2
# lema('[Ee]scisi_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ee]speci_alizació_n(?!\]\])_(?:alizacio|lizaci[oó])') + #2
# lema('[Ee]specificaci_o_nes_ó') + #2
# lema('[Ee]sturi_ó_n(?!\])_o') + #2
# lema('[Ee]vacuaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ee]vacuaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ee]xcavaci_o_nes_ó') + #2
# lema('[Ee]xclusi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #2
# lema('[Ee]xcreci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ee]xcursi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #2
# lema('[Ee]xpansi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ', xpos=[' (?:Opposing|pak)', ]) + #2
# lema('[Ee]xportaci_o_nes_ó') + #2
# lema('[Ee]xpulsi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpos=[' de los Moriscos', '\]\]es', ]) + #2
# lema('[Ff]acci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ff]ascinaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ff]il_ó_n_o', xpre=[' du ', ' i ', 'Augustin ', 'L\. ', 'Larese ', 'Rick ', 'Robert ', 'solenaskitan ', ], xpos=[' (?:Kmita|réduit)', '\]\]es', ]) + #2
# lema('[Ff]iliaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ff]ortificaci_o_nes_ó') + #2
# lema('[Ff]ragmentaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ff]ricci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ff]rustraci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Gg]al_ó_n_o', xpre=['Ezio ', 'Rémy ', 'aventurero ', ], xpos=[' (?:hapus|lân)', '(?:\]|\'\' rebellion)', ]) + #2
# lema('[Gg]eneraci_o_nes_ó') + #2
# lema('[Gg]uarnici_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Hh]umillaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ii]_o_nes_ó') + #2
# lema('[Ii]mplantaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ii]ndicaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ii]nfiltraci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ii]nflamaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ii]nformaci_o_nes_ó') + #2
# lema('[Ii]ntenci_o_nes_ó') + #2
# lema('[Ii]nteracci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ii]nterdicci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ii]nternacionalizaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ii]nterrupci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ii]ntuici_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ii]nvocaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ii]nyecci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ll]imitaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ll]iquidaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ll]ocaci_o_nes_ó') + #2
# lema('[Ll]ocuci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Mm]aduraci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Mm]alformaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Mm]aquetaci_ó_n(?!\])_o') + #2
# lema('[Mm]asturbaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Mm]enstruaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Mm]orri_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Nn]aci_o_nes_ó') + #2
# lema('[Nn]ivelaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Oo]clusi_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Oo]presi_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Oo]rnamentaci_ó_n(?!\])_o') + #2
# lema('[Pp]abell_o_nes_ó') + #2
# lema('[Pp]atr_o_nes_ó') + #2
# lema('[Pp]enalizaci_ó_n(?!\])_o') + #2
# lema('[Pp]erdici_ó_n_o') + #2
# lema('[Pp]erforaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Pp]ersonalizaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Pp]oci_o_nes_ó') + #2
# lema('[Pp]ortaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Pp]osici_o_nes_ó') + #2
# lema('[Pp]reposici_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Pp]rescripci_ó_n(?!\])_o') + #2
# lema('[Pp]reservaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Pp]revisi_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Pp]roces_io_nes_(?:si[oó]|ió)') + #2
# lema('[Pp]rohibici_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Pp]roliferaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Pp]ronunciaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Pp]roposici_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Rr]aci_ó_n_o', xpos=[' kaj', '(?:\])', ]) + #2
# lema('[Rr]ai_o_nes_ó') + #2
# lema('[Rr]eaparici_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Rr]ecesi_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Rr]eclamaci_ó_n(?!\])_o') + #2
# lema('[Rr]eclusi_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Rr]ecombinaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Rr]ecomendaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Rr]ecordaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Rr]egeneraci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Rr]emisi_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Rr]endici_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Rr]engl_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Rr]epetici_o_nes_ó') + #2
# lema('[Rr]eposici_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Rr]estituci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Rr]evoluci_o_nes_ó') + #2
# lema('[Ss]anaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ss]egregaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ss]esi_o_nes_ó') + #2
# lema('[Ss]ill_ó_n_o', xpre=['\'', '& ', '(?:du|[Ll]e|et) ', 'Au ', 'Claude ', 'Grand ', 'Jean ', 'Mon ', 'Princesse de ', 'Victor ', ], xpos=[' (?:rhodanien|de Talbert|beach|industriel|de Bretagne|Sambre)', '\]\]es', ]) + #2
# lema('[Ss]indicaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ss]ubcampe_o_nes_ó') + #2
# lema('[Ss]ubdivisi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #2
# lema('[Ss]ublevaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ss]ujeci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ss]uperaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ss]upresi_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ss]uscripci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Ss]ustentaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Tt]ap_o_nes_ó') + #2
# lema('[Tt]ej_o_nes_ó') + #2
# lema('[Tt]ej_ó_n_o', pre='[Ee]l ', xpos=[' Ranch', ]) + #2
# lema('[Tt]el_ó_n_o', xpre=['Anagyrus ', 'Ginintuan ', ]) + #2
# lema('[Tt]elevi_sió_n_cio') + #2
# lema('[Tt]if_o_nes_ó') + #2
# lema('[Tt]inci_ó_n(?!\])_o') + #2
# lema('[Tt]radici_o_nes_ó') + #2
# lema('[Tt]ransacci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Tt]ransformaci_o_nes_ó') + #2
# lema('[Tt]ransfusi_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #2
# lema('[Tt]ranslocaci_ó_n(?!\])_o') + #2
# lema('[Tt]ransmisi_o_nes_ó') + #2
# lema('[Tt]ransportaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Tt]ransportaci_o_nes_ó') + #2
# lema('[Uu]nci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Vv]acaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Vv]ag_o_nes_ó') + #2
# lema('[Vv]ariaci_ó_n_o', xpos=['\]\]es', ]) + #2
# lema('[Vv]entilaci_ó_n_o', xpre=['Sagunto\'\', con libre', ], xpos=['\]\]es', ]) + #2
# lema('[Vv]ibraci_o_nes_ó') + #2
# lema('[b]id_ó_n_o', xpre=['Ville ', 'beau un ', ], xpos=['\]\]es', ]) + #2
# lema('[m]at_ó_n_o', xpos=[' BB1200', '\]\]es', ]) + #2
# lema('[Aa]bdicaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]berraci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]breviaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]centuaci_ó_n(?!\])_o') + #1
# lema('[Aa]ctivaci_o_nes_ó') + #1
# lema('[Aa]ctualizaci_o_nes_ó') + #1
# lema('[Aa]cumulaci_o_nes_ó') + #1
# lema('[Aa]cusaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]divinaci_ó_n(?!\])_o') + #1
# lema('[Aa]dministraci_o_nes_ó') + #1
# lema('[Aa]fectaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]filiaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]finaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]gnaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]gresi_o_nes_ó') + #1
# lema('[Aa]guij_o_nes_ó') + #1
# lema('[Aa]guij_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]lfabetizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]lienaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]locuci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]lucinaci_o_nes_ó') + #1
# lema('[Aa]lusi_o_nes_ó') + #1
# lema('[Aa]lusi_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]mplificaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]mputaci_o_nes_ó') + #1
# lema('[Aa]nfitri_o_nes_ó') + #1
# lema('[Aa]pelaci_o_nes_ó') + #1
# lema('[Aa]plicaci_o_nes_ó') + #1
# lema('[Aa]preciaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Aa]rp_ó_n(?!\])_o') + #1
# lema('[Aa]sociaci_o_nes_ó') + #1
# lema('[Aa]tol_o_nes_ó') + #1
# lema('[Aa]udici_o_nes_ó') + #1
# lema('[Aa]utenticaci_ó_n(?!\])_o') + #1
# lema('[Aa]utodestrucci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Bb]al_o_nes_ó') + #1
# lema('[Bb]arrac_o_nes_ó') + #1
# lema('[Bb]arrac_ó_n(?!\])_o') + #1
# lema('[Bb]atall_o_nes_ó') + #1
# lema('[Bb]ifurcaci_o_nes_ó') + #1
# lema('[Bb]onificaci_o_nes_ó') + #1
# lema('[Bb]oquer_o_nes_ó') + #1
# lema('[Bb]ot_o_nes_ó') + #1
# lema('[Bb]uf_o_nes_ó') + #1
# lema('[Bb]uz_o_nes_ó') + #1
# lema('[Cc]alificaci_o_nes_ó') + #1
# lema('[Cc]analizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]aparaz_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]arburaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]ard_ó_n_o', pre='[Dd]e ', xpre=['Armand ', ], xpos=[' Walker', ]) + #1
# lema('[Cc]ategorizaci_ó_n(?!\])_o') + #1
# lema('[Cc]entralizaci_ó_n(?!\])_o') + #1
# lema('[Cc]hampiñ_o_nes_ó') + #1
# lema('[Cc]intur_o_nes_ó') + #1
# lema('[Cc]ircunscripci_o_nes_ó') + #1
# lema('[Cc]itaci_ó_n(?!\])_o') + #1
# lema('[Cc]oagulaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]olaboraci_o_nes_ó') + #1
# lema('[Cc]oloraci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]ombinaci_o_nes_ó') + #1
# lema('[Cc]ompeti_ció_n_tco') + #1
# lema('[Cc]ompetici_o_nes_ó') + #1
# lema('[Cc]omplicaci_o_nes_ó') + #1
# lema('[Cc]omprobaci_ó_n(?!\])_o') + #1
# lema('[Cc]oncatenaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]oncentraci_o_nes_ó') + #1
# lema('[Cc]oncesi_o_nes_ó') + #1
# lema('[Cc]ondenaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]onjugaci_o_nes_ó') + #1
# lema('[Cc]onjunci_o_nes_ó') + #1
# lema('[Cc]onjunci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]onnotaci_ó_n(?!\])_o') + #1
# lema('[Cc]onsternaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]onstituci_o_nes_ó') + #1
# lema('[Cc]onsumaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]ontemplaci_ó_n_o', xpre=['Flor ', ], xpos=['\]\][a-zñ]+', ]) + #1
# lema('[Cc]ontestaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]ontraindicaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]ontraposici_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]ontribuci_o_nes_ó') + #1
# lema('[Cc]onvenci_o_nes_ó') + #1
# lema('[Cc]onversaci_o_nes_ó') + #1
# lema('[Cc]ooperaci_o_nes_ó') + #1
# lema('[Cc]ord_ó_n_o', pre='(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #1
# lema('[Cc]orrelaci_o_nes_ó') + #1
# lema('[Cc]otizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Cc]ristianizaci_ó_n(?!\])_o') + #1
# lema('[Dd]ataci_o_nes_ó') + #1
# lema('[Dd]efinici_o_nes_ó') + #1
# lema('[Dd]eformaci_o_nes_ó') + #1
# lema('[Dd]egollaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]egradaci_o_nes_ó') + #1
# lema('[Dd]elimitaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]emocratizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]emolici_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]emostraci_o_nes_ó') + #1
# lema('[Dd]epilaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]eposici_o_nes_ó') + #1
# lema('[Dd]epreciaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]erivaci_o_nes_ó') + #1
# lema('[Dd]escentralizaci_ó_n_o', xpos=['(?:\]\][a-zñ]+|\.gov)', ]) + #1
# lema('[Dd]escolonizaci_ó_n_o') + #1
# lema('[Dd]esconexi_ó_n(?!\])_o') + #1
# lema('[Dd]esesperaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]esilusi_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]esintegraci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]estinaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]esvinculaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]evaluaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]evastaci_o_nes_ó') + #1
# lema('[Dd]ifracci_ó_n(?!\])_o') + #1
# lema('[Dd]imensi_o_nes_ó') + #1
# lema('[Dd]iputaci_o_nes_ó') + #1
# lema('[Dd]iscreci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]isminuci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]isposici_o_nes_ó') + #1
# lema('[Dd]isyunci_o_nes_ó') + #1
# lema('[Dd]iversificaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]otaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Dd]r_o_n(?!\])_ó') + #1
# lema('[Dd]rag_o_nes_ó') + #1
# lema('[Dd]uplicaci_o_nes_ó') + #1
# lema('[Dd]uplicaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]fusi_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]lectr_o_nes_ó') + #1
# lema('[Ee]lectr_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #1
# lema('[Ee]lectrificaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]longaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]mancipaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]mis_ió_n_sió') + #1
# lema('[Ee]ntonaci_ó_n(?!\])_o') + #1
# lema('[Ee]ntronizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]rupci_o_nes_ó') + #1
# lema('[Ee]specializaci_ó_n(?!\])_o') + #1
# lema('[Ee]speculaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]standarizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]sterilizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]stimulaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]stratificaci_ó_n(?!\])_o') + #1
# lema('[Ee]vaporaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]vocaci_ó_n(?!\])_o') + #1
# lema('[Ee]xacci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]xageraci_ó_n(?!\])_o') + #1
# lema('[Ee]xcitaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]xclamaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]xcomuni_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]xcursi_o_nes_ó') + #1
# lema('[Ee]xhibici_o_nes_ó') + #1
# lema('[Ee]xpectaci_ó_n(?!\])_o') + #1
# lema('[Ee]xpedici_o_nes_ó') + #1
# lema('[Ee]xperimentaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]xplicaci_o_nes_ó') + #1
# lema('[Ee]xpresi_o_nes_ó') + #1
# lema('[Ee]xtracci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ee]xtradici_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ff]acci_o_nes_ó') + #1
# lema('[Ff]aj_ó_n(?!\])_o') + #1
# lema('[Ff]ald_ó_n(?!\])_o') + #1
# lema('[Ff]ermi_o_nes_ó') + #1
# lema('[Ff]ertilizaci_ó_n(?!\])_o') + #1
# lema('[Ff]iguraci_ó_n(?!\])_o') + #1
# lema('[Ff]iscalizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ff]isi_ó_n_o', xpre=['Celibe ', ], xpos=[' boy', '\]\]es', ]) + #1
# lema('[Ff]lotaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ff]luctuaci_ó_n(?!\])_o') + #1
# lema('[Ff]onaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ff]orestaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ff]ormaci_o_nes_ó') + #1
# lema('[Ff]ot_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpre=['oficial '], xpos=[' Motor']) + #1
# lema('[Ff]racci_o_nes_ó') + #1
# lema('[Ff]rustraci_o_nes_ó') + #1
# lema('[Ff]undaci_o_nes_ó') + #1
# lema('[Ff]undamentaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ff]usi_o_nes_ó') + #1
# lema('[Gg]ale_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #1
# lema('[Gg]esti_o_nes_ó') + #1
# lema('[Gg]ravitaci_ó_n(?!\])_o') + #1
# lema('[Gg]uarnici_o_nes_ó') + #1
# lema('[Hh]adr_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #1
# lema('[Hh]alc_o_nes_ó') + #1
# lema('[Hh]ur_o_nes_ó') + #1
# lema('[Hh]ur_ó_n_o', pre='(?:[Ee]l|[Dd]el|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpos=[' (?:University|forman|Band|Potawatomi)', ]) + #1
# lema('[Ii]lustraci_o_nes_ó') + #1
# lema('[Ii]mplantaci_o_nes_ó') + #1
# lema('[Ii]mplicaci_o_nes_ó') + #1
# lema('[Ii]mplicaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]mposici_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]mprecisi_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]mpresi_o_nes_ó') + #1
# lema('[Ii]nacci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]ncrustaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]nervaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]nfecci_o_nes_ó') + #1
# lema('[Ii]nflaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]nfracci_o_nes_ó') + #1
# lema('[Ii]nhalaci_ó_n(?!\])_o') + #1
# lema('[Ii]nhibici_o_nes_ó') + #1
# lema('[Ii]nhibici_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]niciaci_o_nes_ó') + #1
# lema('[Ii]nicializaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]nmediaci_ó_n_o', xpos=[' al Chaco', '\]\]es', ]) + #1
# lema('[Ii]nmolaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]nseminaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]nstalaci_o_nes_ó') + #1
# lema('[Ii]nstauraci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]nstrucci_o_nes_ó') + #1
# lema('[Ii]nstrumentaci_o_nes_ó') + #1
# lema('[Ii]ntegraci_o_nes_ó') + #1
# lema('[Ii]ntensificaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]nterceptaci_o_nes_ó') + #1
# lema('[Ii]ntercesi_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]ntermediaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]nterpretaci_o_nes_ó') + #1
# lema('[Ii]nterrelaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]ntervenci_o_nes_ó') + #1
# lema('[Ii]nvenci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]nversi_o_nes_ó') + #1
# lema('[Ii]nyecci_o_nes_ó') + #1
# lema('[Ii]onizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]rradiaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ii]teraci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Jj]ap_o_nes_ó') + #1
# lema('[Jj]arr_o_nes_ó') + #1
# lema('[Jj]onr_o_nes_ó') + #1
# lema('[Jj]ubilaci_o_nes_ó') + #1
# lema('[Ll]adr_o_nes_ó') + #1
# lema('[Ll]amentaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ll]ecci_o_nes_ó') + #1
# lema('[Ll]ept_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #1
# lema('[Ll]evitaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ll]iberalizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ll]imitaci_o_nes_ó') + #1
# lema('[Ll]ist_ó_n_o', pre='(?:[Ee]l|[Dd]el|[Uu]n|[Cc]ada|[Ss]u) ', xpre=['far ', ]) + #1
# lema('[Ll]ocalizaci_o_nes_ó') + #1
# lema('[Mm]aceraci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Mm]anifestaci_o_nes_ó') + #1
# lema('[Mm]anutenci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Mm]arginaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Mm]arr_o_nes_ó') + #1
# lema('[Mm]at_o_nes_ó') + #1
# lema('[Mm]ecanizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Mm]editaci_o_nes_ó') + #1
# lema('[Mm]egat_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpos=[' Hit', ]) + #1
# lema('[Mm]esorregi_ó_n(?!\])_o') + #1
# lema('[Mm]icronaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Mm]ilitarizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Mm]ill_o_nes_ó') + #1
# lema('[Mm]isti_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Mm]ovilizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Mm]unici_o_nes_ó') + #1
# lema('[Mm]utaci_o_nes_ó') + #1
# lema('[Nn]aturalizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Oo]bstrucci_o_nes_ó') + #1
# lema('[Oo]bstrucci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Oo]misi_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Oo]pini_o_nes_ó') + #1
# lema('[Oo]posici_o_nes_ó') + #1
# lema('[Oo]raci_o_nes_ó') + #1
# lema('[Oo]rientaci_o_nes_ó') + #1
# lema('[Oo]rquestaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Oo]stentaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Pp]alpitaci_ó_n(?!\])_o') + #1
# lema('[Pp]antal_o_nes_ó') + #1
# lema('[Pp]asi_o_nes_ó') + #1
# lema('[Pp]eat_ó_n(?!\])_o') + #1
# lema('[Pp]eriodizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Pp]ermutaci_o_nes_ó') + #1
# lema('[Pp]ersonificaci_o_nes_ó') + #1
# lema('[Pp]etici_o_nes_ó') + #1
# lema('[Pp]inz_o_nes_ó') + #1
# lema('[Pp]iñ_o_nes_ó') + #1
# lema('[Pp]lantaci_o_nes_ó') + #1
# lema('[Pp]olarizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Pp]olimerizaci_ó_n(?!\])_o') + #1
# lema('[Pp]ose_sio_nes_ci[oó]') + #1
# lema('[Pp]redicaci_ó_n_o', xpos=[' de la Ley', '\]\]es', ]) + #1
# lema('[Pp]redicci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Pp]redicci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Pp]reocupaci_o_nes_ó') + #1
# lema('[Pp]reparaci_o_nes_ó') + #1
# lema('[Pp]reselecci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Pp]resentaci_o_nes_ó') + #1
# lema('[Pp]revisualizaci_ó_n(?!\])_o') + #1
# lema('[Pp]rofesi_o_nes_ó') + #1
# lema('[Pp]roliferaci_o_nes_ó') + #1
# lema('[Pp]rolongaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Pp]rospecci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Pp]rovocaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Pp]udrici_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Pp]ulg_o_nes_ó') + #1
# lema('[Pp]ulsaci_o_nes_ó') + #1
# lema('[Pp]unz_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]abi_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]adiaci_o_nes_ó') + #1
# lema('[Rr]amificaci_o_nes_ó') + #1
# lema('[Rr]at_o_nes_ó') + #1
# lema('[Rr]at_ó_n_o', xpre=['(?:Le|On) ', '[Mm]esa ', '[RB]oca ', ], xpos=[' (?:section|Mesa|Pass|Municipal Airport)', '[\'\]]', ]) + #1
# lema('[Rr]eacci_o_nes_ó') + #1
# lema('[Rr]ecapitulaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]ecepci_o_nes_ó') + #1
# lema('[Rr]eclamaci_o_nes_ó') + #1
# lema('[Rr]econciliaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]econstituci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]ecreaci_o_nes_ó') + #1
# lema('[Rr]efacci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]efracci_ó_n(?!\])_o') + #1
# lema('[Rr]efrigeraci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]efutaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]egresi_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]egularizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]eimpresi_o_nes_ó') + #1
# lema('[Rr]eimpresi_ó_n_o', xpre=['5th ', ], xpos=['\]\]es', ]) + #1
# lema('[Rr]eincorporaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]einvenci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]eligi_o_nes_ó') + #1
# lema('[Rr]emodelaci_o_nes_ó') + #1
# lema('[Rr]epercusi_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]eposici_o_nes_ó') + #1
# lema('[Rr]eproducci_o_nes_ó') + #1
# lema('[Rr]esoluci_o_nes_ó') + #1
# lema('[Rr]estricci_o_nes_ó') + #1
# lema('[Rr]etroalimentaci_ó_n(?!\])_o') + #1
# lema('[Rr]etrotranspos_ó_n_o', xpos=[' superfamily', '\]\]es', ]) + #1
# lema('[Rr]everberaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Rr]evisi_o_nes_ó') + #1
# lema('[Ss]alaz_ó_n(?!\])_o') + #1
# lema('[Ss]aturaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ss]ecci_o_nes_ó') + #1
# lema('[Ss]ecreci_ó_n_o', xpos=['(?:\]|\.com)', ]) + #1
# lema('[Ss]edici_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ss]emidesintegraci_ó_n(?!\])_o') + #1
# lema('[Ss]ensibilizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ss]eñalizaci_o_nes_ó') + #1
# lema('[Ss]if_o_nes_ó') + #1
# lema('[Ss]implificaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ss]ocializaci_ó_n(?!\])_o') + #1
# lema('[Ss]oluci_o_nes_ó') + #1
# lema('[Ss]ubestaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ss]ubordinaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ss]ubsecci_o_nes_ó') + #1
# lema('[Ss]ubvenci_ó_n(?!\])_o') + #1
# lema('[Ss]uperposici_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Ss]uperstici_ó_n(?!\])_o') + #1
# lema('[Ss]uplicaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Tt]ax_o_nes_ó') + #1
# lema('[Tt]ej_ó_n_o', pre='(?:[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #1
# lema('[Tt]elecomunicaci_o_nes_ó') + #1
# lema('[Tt]ensi_o_nes_ó') + #1
# lema('[Tt]erminaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Tt]eut_ó_n(?!\])_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada) ', xpos=[' de Neville']) + #1
# lema('[Tt]raducci_o_nes_ó') + #1
# lema('[Tt]ransliteraci_ó_n(?!\])_o') + #1
# lema('[Tt]ransmigraci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Uu]bicaci_o_nes_ó') + #1
# lema('[Uu]rbanizaci_o_nes_ó') + #1
# lema('[Vv]acunaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Vv]alidaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Vv]alorizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Vv]ar_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #1
# lema('[Vv]eneraci_ó_n_o', xpre=['Ian ', 'Jun ', 'Luis ', 'Ofilada ', 'Ynez ', ], xpos=['\]\]es', ]) + #1
# lema('[Vv]erificaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Vv]isi_o_nes_ó') + #1
# lema('[Vv]isualizaci_o_nes_ó') + #1
# lema('[Vv]isualizaci_ó_n_o', xpos=['\]\]es', ]) + #1
# lema('[Vv]otaci_o_nes_ó') + #1
# lema('[b]ret_ó_n_o', pre='(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpre=['\\bd’', ], xpos=[' très', ]) + #1

# lema('[Cc]ie_mpié_s_(?:npi[eé]|mpie)') + #28
# lema('[Dd]ebutar_í_a[ns]?_i') + #22
# lema('[Pp]erder_í_a[ns]?_i') + #15
# lema('[Uu]n_í_r[mts]el[aeo]s?_i') + #13
# lema('[Cc]ongre_s_os?_') + #11
# lema('[Mm]_é_dicamente_e') + #11
# lema('[Pp]eluquer_í_as?_i') + #10
# lema('[Qq]uit_á_r[mts]el[aeo]s?_a') + #10
# lema('[Cc]omp_i_tiera[ns]?_e') + #9
# lema('[Pp]resentar_í_a[ns]?_i') + #9
# lema('[Aa]cced_í_a[ns]?_i') + #8
# lema('[Aa]s_c_enso(?:[rs]|res)_') + #8
# lema('[Pp]rincipalme_n_te_') + #8
# lema('[Tt]elev_i_sión_') + #7
# lema('[Tt]itular_í_a[ns]?_i') + #7
# lema('[Dd]_e_cidió_i') + #6
# lema('[Ee]xhib(?:ir|)_í_a[ns]?_i') + #6
# lema('[Tt]rabajar_í_a[ns]?_i') + #6
# lema('[Cc]u_m_plen_n') + #5
# lema('[Cc]ub_r_ir(?:se|)_') + #5
# lema('[Dd]ividi_d_[ao]_', pre='(?:[Ee]st[aá]|[Ff]u[eé]|[Ee]s) ') + #5
# lema('[Ii]_m_portante_n') + #5
# lema('[Ii]mpart(?:ir|)_í_a[ns]?_i') + #5
# lema('[Ii]nterpretar_í_a[ns]?_i') + #5
# lema('[Rr]epet_í_a[ns]?_i') + #5
# lema('[Tt]e_m_porada_n') + #5
# lema('[Aa]daptar_í_a[ns]?_i') + #4
# lema('[Aa]eron_á_uticas_a') + #4
# lema('[Aa]ngiograf_í_as?_i') + #4
# lema('[Aa]umentar_í_a[ns]?_i') + #4
# lema('[Cc]o_nstrui_d[ao]s?_sntruí') + #4
# lema('[Cc]onsens_ú_(?:a[ns]?|e[ns]?)_u') + #4
# lema('[Cc]onsumir_á_[ns]?_a') + #4
# lema('[Dd]evolv_é_r[mts]el[aeo]s?_e') + #4
# lema('[Dd]isf_r_uta[nrs]?_') + #4
# lema('[Ee]xpon_í_a[ns]?_i') + #4
# lema('[Gg]rabar_í_a[ns]?_i') + #4
# lema('[Hh]ac_é_r[mts]el[aeo]s?_e') + #4
# lema('[Ii]mpon_í_a[ns]?_i') + #4
# lema('[Ii]ndicar_í_a[ns]_i') + #4
# lema('[Mm]ejorar_í_a[ns]?_i') + #4
# lema('[Mm]ostrar_í_a[ns]?_i') + #4
# lema('[Oo]cupar_í_a[ns]?_i') + #4
# lema('[Ss]inverg_ü_enzas?_u') + #4
# lema('[Tt]ardar_í_a[ns]?_i') + #4
# lema('[Tt]elev_i_sión_e') + #4
# lema('[Tt]ransitar_í_a[ns]?_i') + #4
# lema('_e_quipos?_é') + #4
# lema('[M]_ó_naco_o', pre='[Ee]n ') + #3
# lema('[Aa]frontar_í_a[ns]?_i') + #3
# lema('[Aa]greg_á_r[mts]el[aeo]s?_a') + #3
# lema('[Aa]s_c_ensor(?:es|)_') + #3
# lema('[Aa]sis__tieron_i') + #3
# lema('[Aa]ñad(?:ir|)_í_a[ns]?_i') + #3
# lema('[Cc]o_m_parte_n') + #3
# lema('[Cc]oexist(?:ir|)_í_a[ns]?_i') + #3
# lema('[Cc]ol_a_boró_o') + #3
# lema('[Cc]ompeti_ci_ones_') + #3
# lema('[Cc]onectar_í_a[ns]?_i') + #3
# lema('[Cc]ons_titui_d[ao]s?_ituí') + #3
# lema('[Cc]onsolidar_í_a[ns]?_i') + #3
# lema('[Cc]ulminar_í_a[ns]?_i') + #3
# lema('[Dd]e__cidió_i') + #3
# lema('[Dd]escubi_e_rt[ao]s?_') + #3
# lema('[Dd]esempeñar_í_a[ns]?_i') + #3
# lema('[Dd]eterminar_í_a[ns]?_i') + #3
# lema('[Ee]_s_culturas?_') + #3
# lema('[Ee]migrar_í_a[ns]?_i') + #3
# lema('[Ee]namorar_í_a[ns]?_i') + #3
# lema('[Ee]ncend_í_(?:a[ns]?|)_i') + #3
# lema('[Ee]ntrenar_í_a[ns]?_i') + #3
# lema('[Ee]st_á dividid_a_a divid') + #3
# lema('[Hh]undir_á_[ns]?_a') + #3
# lema('[Ii]n_strui_d[ao]s?_truí') + #3
# lema('[Ii]ntentar_í_a[ns]?_i') + #3
# lema('[Ii]nventar_í_a[ns]?_i') + #3
# lema('[Ll]lam_á_r[mts]el[aeo]s?_a') + #3
# lema('[Mm]oment_á_ne[ao]_a') + #3
# lema('[Mm]ostr_á_r[mts]el[aeo]s?_a') + #3
# lema('[Oo]clu_i_d[ao]s?_í') + #3
# lema('[Oo]dontopediatr_í_as?_i') + #3
# lema('[Oo]ptometr_í_as?_i') + #3
# lema('[Pp]erci_b_id[ao]s?_v') + #3
# lema('[Pp]olin_ó_mic[ao]_o') + #3
# lema('[Pp]roporcionar_í_a[ns]?_i') + #3
# lema('[Pp]rotagonizar_í_a[ns]?_i') + #3
# lema('[Rr]etransmit(?:ir|)_í_a[ns]?_i') + #3
# lema('[Rr]ob_á_r[mts]el[aeo]s?_a') + #3
# lema('[Tt]ie_m_pos_n') + #3
# lema('[Tt]raumat_ó_log[ao]s?_o') + #3
# lema('[l]ic_ú_an_u') + #3
# lema('[K]atmand_ú__u', pre='(?:[Dd]e|[Ee]n) ') + #2
# lema('[Aa]cerc_á_r[mts]el[aeo]s?_a') + #2
# lema('[Aa]credit_á_r[mts]el[aeo]s?_a') + #2
# lema('[Aa]cuñar_í_a[ns]?_i') + #2
# lema('[Aa]dmi_ni_stración_') + #2
# lema('[Aa]gregar_í_a[ns]?_i') + #2
# lema('[Aa]lejar_í_a[ns]?_i') + #2
# lema('[Aa]lica_í_d[ao]s?_i') + #2
# lema('[Aa]trev_í_a[ns]?_i') + #2
# lema('[Aa]vanzar_í_a[ns]?_i') + #2
# lema('[Cc]elebrar_í_a[ns]?_i') + #2
# lema('[Cc]errar_í_a[ns]?_i') + #2
# lema('[Cc]lav_á_r[mts]el[aeo]s?_a') + #2
# lema('[Cc]oloc_á_r[mts]el[aeo]s?_a') + #2
# lema('[Cc]olocar_í_a[ns]?_i') + #2
# lema('[Cc]ompetiti__v[ao]s?_t') + #2
# lema('[Cc]oncretar_í_a[ns]?_i') + #2
# lema('[Cc]onfund(?:ir|)_í_a[ns]?_i') + #2
# lema('[Cc]onfundir_á_[ns]?_a') + #2
# lema('[Cc]onsiderar_í_a[ns]?_i') + #2
# lema('[Cc]onst_itui_d[ao]s?_uí') + #2
# lema('[Cc]onstar_í_a[ns]?_i') + #2
# lema('[Cc]onvirti_éndos_e_endoc') + #2
# lema('[Cc]onvirti_éndos_e_endoc') + #2
# lema('[Cc]onvirti_éndos_e_endoc') + #2
# lema('[Cc]onvirti_éndos_e_endoc') + #2
# lema('[Cc]onvirti_éndos_e_endoc') + #2
# lema('[Cc]re_é_r[mts]el[aeo]s?_e') + #2
# lema('[Cc]u_m_plir_n') + #2
# lema('[Dd]eclar_á_r[mts]el[aeo]s?_a') + #2
# lema('[Dd]esapare_c_er?_s') + #2
# lema('[Dd]escub_ri_dor(?:[ae]s?|)_ir') + #2
# lema('[Dd]esignar_í_a[ns]?_i') + #2
# lema('[Dd]ividir_í_a[ns]?_i') + #2
# lema('[Dd]on_á_r[mts]el[aeo]s?_a') + #2
# lema('[Ee]_m_parentado_n') + #2
# lema('[Ee]fica_z__s') + #2
# lema('[Ee]m_blemá_tic[ao]s?_plem[aá]') + #2
# lema('[Ee]ncantar_í_a[ns]?_i') + #2
# lema('[Ee]scup(?:ir|)_í_a[ns]?_i') + #2
# lema('[Ff]isiograf_í_a_i') + #2
# lema('[Ff]uncionar_í_an_i') + #2
# lema('[Gg]enerar_í_a[ns]?_i') + #2
# lema('[Hh]ablar_í_a[ns]?_i') + #2
# lema('[Ii]_m_prescindible_n') + #2
# lema('[Ii]mped_í_r[mts]el[aeo]s?_i') + #2
# lema('[Ii]ncrementar_í_a[ns]?_i') + #2
# lema('[Ii]ntegrar_í_a[ns]?_i') + #2
# lema('[Ii]nterrump(?:ir|)_í_a[ns]?_i') + #2
# lema('[Jj]er_á_rquic[ao]s?_a') + #2
# lema('[Ll]iberar_í_a[ns]?_i') + #2
# lema('[Ll]ogar_í_tmic[ao]s?_i') + #2
# lema('[Nn]eg_á_r[mts]el[aeo]s?_a') + #2
# lema('[Pp]artir_á_[ns]_a') + #2
# lema('[Pp]ermit_í_r[mts]el[aeo]s?_i') + #2
# lema('[Pp]od_ó_log[ao]s?_o') + #2
# lema('[Pp]rescribir_á_[ns]?_a') + #2
# lema('[Pp]ropon_é_r[mts]el[aeo]s?_e') + #2
# lema('[Pp]rostitu_i_d[ao]s?_í') + #2
# lema('[Qq]ued_á_r[mts]el[aeo]s?_a') + #2
# lema('[Rr]eci_b_iendo_v') + #2
# lema('[Rr]econstitu_i_d[ao]s?_í') + #2
# lema('[Rr]edise_ñ_ad[ao]s?_n') + #2
# lema('[Rr]egistrar_í_a[ns]?_i') + #2
# lema('[Rr]egrabar_í_a[ns]?_i') + #2
# lema('[Rr]egres_á_r[mts]el[aeo]s?_a') + #2
# lema('[Rr]emontar_í_a[ns]?_i') + #2
# lema('[Rr]enovar_í_a[ns]?_i') + #2
# lema('[Rr]esum(?:ir|)_í_a[ns]?_i') + #2
# lema('[Ss]ellar_í_a[ns]_i') + #1
# lema('[Ss]emiderru_i_d[ao]s?_í') + #2
# lema('[Ss]olventar_í_a[ns]?_i') + #2
# lema('[Ss]ubsist(?:ir|)_í_a[ns]?_i') + #2
# lema('[Ss]uperar_í_a[ns]?_i') + #2
# lema('[Tt]e_m_poradas_n') + #2
# lema('[Tt]ro_m_peta_n') + #2
# lema('[Uu]bicar_í_a[ns]?_i') + #2
# lema('[Vv]iajar_í_a[ns]?_i') + #2
# lema('_C_ercan[ao]s?_S') + #2
# lema('[a]lbergar_í_a[ns]?_i') + #2
# lema('[t]en_ido__dio', pre='[Hh]a(?:n?|bían?|ber) ') + #2
# lema('[C]amer_ú_n_u', pre='(?:[Ee]n) ') + #1
# lema('[Aa]_m_parar_n') + #1
# lema('[Aa]cab_a_rá_') + #1
# lema('[Aa]clar_á_r[mts]el[aeo]s?_a') + #1
# lema('[Aa]consejar_í_a[ns]?_i') + #1
# lema('[Aa]copl_á_r[mts]el[aeo]s?_a') + #1
# lema('[Aa]dministrar_í_a[ns]?_i') + #1
# lema('[Aa]gitar_í_a[ns]?_i') + #1
# lema('[Aa]gradec_é_r[mts]el[aeo]s?_e') + #1
# lema('[Aa]griar_í_a[ns]?_i') + #1
# lema('[Aa]grupar_í_a[ns]?_i') + #1
# lema('[Aa]lertar_í_a[ns]?_i') + #1
# lema('[Aa]liar_s_e_z') + #1
# lema('[Aa]mbientar_í_a[ns]?_i') + #1
# lema('[Aa]ntepen_ú_ltim[ao]s?_u') + #1
# lema('[Aa]pare_z_ca[ns]?_s') + #1
# lema('[Aa]parec_é_r[mts]el[aeo]s?_e') + #1
# lema('[Aa]plic_á_r[mts]el[aeo]s?_a') + #1
# lema('[Aa]poderar_í_a[ns]?_i') + #1
# lema('[Aa]portar_í_a[ns]?_i') + #1
# lema('[Aa]prehend_í_a[ns]?_i') + #1
# lema('[Aa]rrebat_á_r[mts]el[aeo]s?_a') + #1
# lema('[Aa]rregl_á_r[mts]el[aeo]s?_a') + #1
# lema('[Aa]rremet_í_a[ns]?_i') + #1
# lema('[Aa]rruinar_í_a[ns]?_i') + #1
# lema('[Aa]segur_á_r[mts]el[aeo]s?_a') + #1
# lema('[Aa]segurar_í_a[ns]?_i') + #1
# lema('[Aa]t_ribui_d[ao]s?_tribuí') + #1
# lema('[Aa]tacar_í_a[ns]?_i') + #1
# lema('[Aa]tar_í_an_i') + #1
# lema('[Aa]udicionar_í_a[ns]?_i') + #1
# lema('[Aa]ñad_í_r[mts]el[aeo]s?_i') + #1
# lema('[Bb]al_ompié__ónpie') + #1
# lema('[Bb]ibliograf_í_as_i') + #1
# lema('[Bb]urlar_í_a[ns]?_i') + #1
# lema('[Cc]_áno_nes_anó') + #1
# lema('[Cc]a_m_panas?_n') + #1
# lema('[Cc]a_é_r[mts]el[aeo]s?_e') + #1
# lema('[Cc]almar_í_a[ns]_i') + #1
# lema('[Cc]atapultar_í_a[ns]?_i') + #1
# lema('[Cc]err_á_r[mts]el[aeo]s?_a') + #1
# lema('[Cc]hurrasquer_í_as?_i') + #1
# lema('[Cc]ircular_í_a[ns]?_i') + #1
# lema('[Cc]o_m_patriotas_n') + #1
# lema('[Cc]o_m_pañía_n') + #1
# lema('[Cc]o_m_pendio_n') + #1
# lema('[Cc]o_m_pensada_n') + #1
# lema('[Cc]o_m_plejo_n') + #1
# lema('[Cc]o_m_positor_n') + #1
# lema('[Cc]o_m_puertas_n') + #1
# lema('[Cc]o_m_puesta_n') + #1
# lema('[Cc]ol_a_borador_o') + #1
# lema('[Cc]olaborar_í_a[ns]?_i') + #1
# lema('[Cc]om__pañeros_n') + #1
# lema('[Cc]ombatir_á_[ns]?_a') + #1
# lema('[Cc]oment_á_r[mts]el[aeo]s?_a') + #1
# lema('[Cc]omp_itió__etio') + #1
# lema('[Cc]ompar_á_r[mts]el[aeo]s?_a') + #1
# lema('[Cc]ompeti_ci_ón_') + #1
# lema('[Cc]ompeticio_ne_s_en') + #1
# lema('[Cc]ompromet_í_a[ns]?_i') + #1
# lema('[Cc]onceb_í_a[ns]?_i') + #1
# lema('[Cc]onced_é_r[mts]el[aeo]s?_e') + #1
# lema('[Cc]onfes_á_r[mts]el[aeo]s?_a') + #1
# lema('[Cc]onfirmar_í_a[ns]?_i') + #1
# lema('[Cc]onoci_éndos_e_endoc') + #1
# lema('[Cc]onservar_í_a[ns]?_i') + #1
# lema('[Cc]onst_itui_d[ao]s?_rituí') + #1
# lema('[Cc]ontactar_í_a[ns]?_i') + #1
# lema('[Cc]onte_m_poráneo_n') + #1
# lema('[Cc]ontemplar_í_a[ns]?_i') + #1
# lema('[Cc]ontestar_í_a[ns]?_i') + #1
# lema('[Cc]onvi_r_tieron_') + #1
# lema('[Cc]onvi_rtió__tio') + #1
# lema('[Cc]onvivir_á_[ns]?_a') + #1
# lema('[Cc]ooperar_í_a[ns]?_i') + #1
# lema('[Cc]oquetear_í_a[ns]?_i') + #1
# lema('[Cc]ortar_í_a[ns]?_i') + #1
# lema('[Cc]ua_d_rad[ao]s?_') + #1
# lema('[Cc]ubi_e_rt[ao]s?_') + #1
# lema('[Cc]ultivar_í_a[ns]?_i') + #1
# lema('[Cc]urar_í_a[ns]?_i') + #1
# lema('[Dd]_icié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ecie') + #1
# lema('[Dd]_uodé_cimo_úode') + #1
# lema('[Dd]econstru_i_d[ao]s?_í') + #1
# lema('[Dd]edic_á_r[mts]el[aeo]s?_a') + #1
# lema('[Dd]egenerar_í_a[ns]_i') + #1
# lema('[Dd]ej_á_r[mts]el[aeo]s?_a') + #1
# lema('[Dd]emostr_á_r[mts]el[aeo]s?_a') + #1
# lema('[Dd]emostrar_í_a[ns]?_i') + #1
# lema('[Dd]enominar_í_a[ns]?_i') + #1
# lema('[Dd]errumbar_í_a[ns]?_i') + #1
# lema('[Dd]esaperci_b_id[ao]s?_v') + #1
# lema('[Dd]esarrollar_í_a[ns]?_i') + #1
# lema('[Dd]escansar_í_a[ns]?_i') + #1
# lema('[Dd]escub_ri_eron_ir') + #1
# lema('[Dd]escub_ri_r_ir') + #1
# lema('[Dd]esinter_é_s_e') + #1
# lema('[Dd]eslumbrar_í_a[ns]?_i') + #1
# lema('[Dd]estapar_í_a[ns]?_i') + #1
# lema('[Dd]estitu_i_r(?:l[aeo]s?|se|)_í') + #1
# lema('[Dd]i_stribui_d[ao]s?_tribuí') + #1
# lema('[Dd]ic_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_e') + #1
# lema('[Dd]ici_en_do_ne') + #1
# lema('[Dd]ifund(?:ir|)_í_a[ns]?_i') + #1
# lema('[Dd]ilatar_í_a[ns]?_i') + #1
# lema('[Dd]ilu_i_r(?:l[aeo]s?|se|)_í') + #1
# lema('[Dd]isfrutar_í_a[ns]?_i') + #1
# lema('[Dd]ominar_í_a[ns]_i') + #1
# lema('[Dd]ominar_í_an_i') + #1
# lema('[Dd]otar_í_a[ns]?_i') + #1
# lema('[Ee]_m_parentados_n') + #1
# lema('[Ee]_m_pezó_n') + #1
# lema('[Ee]conom_é_tric(?:as|os?)_e') + #1
# lema('[Ee]fectuar_í_a[ns]?_i') + #1
# lema('[Ee]fica_c_es_s') + #1
# lema('[Ee]jecutar_í_a[ns]?_i') + #1
# lema('[Ee]liminar_í_a[ns]?_i') + #1
# lema('[Ee]lud(?:ir|)_í_a[ns]?_i') + #1
# lema('[Ee]mbest_í_a[ns]?_i') + #1
# lema('[Ee]mparejar_í_a[ns]?_i') + #1
# lema('[Ee]mpe_zarí_a[ns]?_sari') + #1
# lema('[Ee]ncaminar_í_a[ns]?_i') + #1
# lema('[Ee]ncender_á_[ns]?_a') + #1
# lema('[Ee]nfurecer_á_[ns]?_a') + #1
# lema('[Ee]nlistar_í_a[ns]?_i') + #1
# lema('[Ee]nojar_í_a[ns]?_i') + #1
# lema('[Ee]nseñ_á_r[mts]el[aeo]s?_a') + #1
# lema('[Ee]nv_iá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ía') + #1
# lema('[Ee]nvi_á_r[mts]el[aeo]s?_a') + #1
# lema('[Ee]scap_á_r[mts]el[aeo]s?_a') + #1
# lema('[Ee]specular_í_a[ns]?_i') + #1
# lema('[Ee]sperar_í_a[ns]?_i') + #1
# lema('[Ee]studiar_í_a[ns]?_i') + #1
# lema('[Ee]timol_ó_gic(?:[ao]s|amente)_o') + #1
# lema('[Ee]vitar_í_a[ns]?_i') + #1
# lema('[Ee]x_entá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_senta') + #1
# lema('[Ee]xc_é_ntric(?:[ao]s|amente)_e') + #1
# lema('[Ee]xhibir_á_[ns]?_a') + #1
# lema('[Ee]xig_í_r[mts]el[aeo]s?_i') + #1
# lema('[Ee]xim_í_as?_i', pre='(?:[Ll]o|[Qq]ue|[Dd]onde) ') + #1
# lema('[Ee]xplorar_í_a[ns]?_i') + #1
# lema('[Ee]xtra_ñ_(?:[ao]s|amente)_n') + #1
# lema('[Ff]ijar_í_a[ns]?_i') + #1
# lema('[Ff]lu_i_r(?:l[aeo]s?|se|)_í') + #1
# lema('[Ff]renar_í_a[ns]?_i') + #1
# lema('[Ff]und(?:ir|)_í_a[ns]?_i') + #1
# lema('[Ff]usionar_í_a[ns]?_i') + #1
# lema('[Gg]an_á_r[mts]el[aeo]s?_a') + #1
# lema('[Gg]erontolog_í_as?_i') + #1
# lema('[Gg]olp_eá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_éa') + #1
# lema('[Gg]uard_á_r[mts]el[aeo]s?_a') + #1
# lema('[Hh]aci_éndos_e_endoc') + #1
# lema('[Hh]aci_éndos_e_endoc') + #1
# lema('[Hh]eredar_í_a[ns]?_i') + #1
# lema('[Ii]_m_pacto_n') + #1
# lema('[Ii]_m_plantación_n') + #1
# lema('[Ii]_m_plica_n') + #1
# lema('[Ii]_m_popularidad_n') + #1
# lema('[Ii]_m_previsto_n') + #1
# lema('[Ii]_m_prácticos_n') + #1
# lema('[Ii]_m_pulsa_n') + #1
# lema('[Ii]_m_pulsaba_n') + #1
# lema('[Ii]_m_pulsó_n') + #1
# lema('[Ii]_m_punemente_n') + #1
# lema('[Ii]_nclui_d[ao]s?_cluí') + #1
# lema('[Ii]_ns_pirado_sn') + #1
# lema('[Ii]gualar_í_a[ns]?_i') + #1
# lema('[Ii]mprimir_á_[ns]?_a') + #1
# lema('[Ii]n_c_identes?_s') + #1
# lema('[Ii]n_s_pector_') + #1
# lema('[Ii]ncendiar_í_an_i') + #1
# lema('[Ii]nclu_i_rl[aeo]s?_í') + #1
# lema('[Ii]nclu_irá_[ns]?_íra') + #1
# lema('[Ii]nclu_irí_a[ns]?_íri') + #1
# lema('[Ii]ncorporar_í_a[ns]?_i') + #1
# lema('[Ii]ncumpl(?:ir|)_í_a[ns]?_i') + #1
# lema('[Ii]ncur_s_i(?:onar|ón|ones|on[oó]|ona[ns]?)_c') + #1
# lema('[Ii]nflu_i_r(?:l[aeo]s?|se|)_í') + #1
# lema('[Ii]ngeni_á_r[mts]el[aeo]s?_a') + #1
# lema('[Ii]nhib(?:ir|)_í_a[ns]?_i') + #1
# lema('[Ii]nsinu_á_r[mts]el[aeo]s?_a') + #1
# lema('[Ii]nstalar_í_a[ns]?_i') + #1
# lema('[Ii]nstitu_i_r(?:l[aeo]s?|se|)_í') + #1
# lema('[Ii]ntercalar_í_a[ns]?_i') + #1
# lema('[Ii]ntr_í_nsec(?:[ao]s|amente)_i') + #1
# lema('[Ii]nundar_í_a[ns]?_i') + #1
# lema('[Ii]nvalidar_í_a[ns]?_i') + #1
# lema('[Jj]ug_á_r[mts]el[aeo]s?_a') + #1
# lema('[Jj]untar_í_a[ns]?_i') + #1
# lema('[Jj]ustificar_í_a[ns]?_i') + #1
# lema('[Ll]am_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_bie') + #1
# lema('[Ll]anz_á_r[mts]el[aeo]s?_a') + #1
# lema('[Ll]avar_í_a[ns]?_i') + #1
# lema('[Ll]e_é_r[mts]el[aeo]s?_e') + #1
# lema('[Ll]evantar_í_a[ns]?_i') + #1
# lema('[Ll]evar_í_a[ns]?_i') + #1
# lema('[Ll]i_m_piamente_n') + #1
# lema('[Ll]lenar_í_a[ns]?_i') + #1
# lema('[Mm]a_m_posteados_n') + #1
# lema('[Mm]and_á_r[mts]el[aeo]s?_a') + #1
# lema('[Mm]anejar_í_a[ns]?_i') + #1
# lema('[Mm]anten_é_r[mts]el[aeo]s?_e') + #1
# lema('[Mm]arisquer_í_as?_i') + #1
# lema('[Mm]et_é_r[mts]el[aeo]s?_e') + #1
# lema('[Mm]ezclar_í_a[ns]?_i') + #1
# lema('[Mm]irar_í_a[ns]?_i') + #1
# lema('[Mm]ovilizar_í_a[ns]?_i') + #1
# lema('[Mm]ultilingü_í_stic[ao]_i') + #1
# lema('[Nn]efr_ó_tic[ao]s?_o') + #1
# lema('[Nn]eutralizar_í_a[ns]?_i') + #1
# lema('[Nn]ombrar_í_a[ns]?_i') + #1
# lema('[Oo]bedecer_á_[ns]?_a') + #1
# lema('[Oo]bservar_í_a[ns]?_i') + #1
# lema('[Oo]bstru_i_r(?:l[aeo]s?|se|)_í') + #1
# lema('[Oo]mit(?:ir|)_í_a[ns]?_i') + #1
# lema('[Oo]rgani_zacio_nes_sació') + #1
# lema('[Pp]atrocinar_í_a[ns]?_i') + #1
# lema('[Pp]ed_í_r[mts]el[aeo]s?_i') + #1
# lema('[Pp]edagog_í_as_i') + #1
# lema('[Pp]ens_á_r[mts]el[aeo]s?_a') + #1
# lema('[Pp]ercan_c_es?_s') + #1
# lema('[Pp]ermit_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #1
# lema('[Pp]ersist(?:ir|)_í_a[ns]?_i') + #1
# lema('[Pp]erten_ecerí_a_ceri') + #1
# lema('[Pp]etrograf_í_as?_i') + #1
# lema('[Pp]itar_í_a[ns]?_i') + #1
# lema('[Pp]lanear_í_a[ns]?_i') + #1
# lema('[Pp]oni_en_do_ne') + #1
# lema('[Pp]orquer_í_as?_i') + #1
# lema('[Pp]osi__ción_si') + #1
# lema('[Pp]osi_c_ionado_s') + #1
# lema('[Pp]osi_c_iones_s') + #1
# lema('[Pp]osi_c_ionó_s') + #1
# lema('[Pp]osi_ci_ón_sic') + #1
# lema('[Pp]reced_í_a[ns]?_i') + #1
# lema('[Pp]refi__riendo_e') + #1
# lema('[Pp]rend_í_a[ns]?_i') + #1
# lema('[Pp]reparar_í_a[ns]?_i') + #1
# lema('[Pp]resupon_í_a[ns]?_i') + #1
# lema('[Pp]rivar_í_a[ns]?_i') + #1
# lema('[Pp]ro_v_ocando_b') + #1
# lema('[Pp]ro_v_ocar_b') + #1
# lema('[Pp]roclamar_í_a[ns]?_i') + #1
# lema('[Pp]rogramar_í_a[ns]?_i') + #1
# lema('[Pp]romet_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #1
# lema('[Pp]romocionar_í_a[ns]?_i') + #1
# lema('[Pp]rosperar_í_a[ns]?_i') + #1
# lema('[Pp]royectar_í_a[ns]?_i') + #1
# lema('[Qq]uin_c_e(?:nal|nalmente)_[sz]') + #1
# lema('[Qq]uitar_í_a[ns]?_i') + #1
# lema('[Rr]eanudar_í_a[ns]?_i') + #1
# lema('[Rr]eclutar_í_a[ns]?_i') + #1
# lema('[Rr]econo_z_ca[ns]?_s') + #1
# lema('[Rr]econquistar_í_a[ns]?_i') + #1
# lema('[Rr]econv_i_rtió_e') + #1
# lema('[Rr]ecordar_í_a[ns]?_i') + #1
# lema('[Rr]ecortar_í_a[ns]?_i') + #1
# lema('[Rr]ecub__rimientos?_i') + #1
# lema('[Rr]edactar_í_a[ns]?_i') + #1
# lema('[Rr]edefin(?:ir|)_í_a[ns]?_i') + #1
# lema('[Rr]eescrib(?:ir|)_í_a[ns]?_i') + #1
# lema('[Rr]efundar_í_a[ns]?_i') + #1
# lema('[Rr]einiciar_í_a[ns]?_i') + #1
# lema('[Rr]elatar_í_a[ns]?_i') + #1
# lema('[Rr]emit(?:ir|)_í_a[ns]?_i') + #1
# lema('[Rr]eparar_í_a[ns]?_i') + #1
# lema('[Rr]escatar_í_a[ns]?_i') + #1
# lema('[Rr]escind(?:ir|)_í_a[ns]?_i') + #1
# lema('[Rr]espaldar_í_a[ns]?_i') + #1
# lema('[Rr]esucitar_í_a[ns]?_i') + #1
# lema('[Rr]etir_á_r[mts]el[aeo]s?_a') + #1
# lema('[Rr]etomar_í_a[ns]?_i') + #1
# lema('[Rr]etornar_í_a[ns]?_i') + #1
# lema('[Rr]evel_á_r[mts]el[aeo]s?_a') + #1
# lema('[Rr]odear_í_a[ns]?_i') + #1
# lema('[Rr]ondar_í_a[ns]?_i') + #1
# lema('[Ss]ac_á_r[mts]el[aeo]s?_a') + #1
# lema('[Ss]alt_á_r[mts]el[aeo]s?_a') + #1
# lema('[Ss]alvar_í_a[ns]?_i') + #1
# lema('[Ss]ecu_e_ncial(?:es|)_a') + #1
# lema('[Ss]eleccionar_í_a[ns]?_i') + #1
# lema('[Ss]emidestru_i_d[ao]s?_í') + #1
# lema('[Ss]ocorr_í_a[ns]?_i') + #1
# lema('[Ss]oltar_í_a[ns]?_i') + #1
# lema('[Ss]oportar_í_a[ns]?_i') + #1
# lema('[Ss]u_é_teres_e') + #1
# lema('[Ss]ubdivid(?:ir|)_í_a[ns]?_i') + #1
# lema('[Ss]ubir_á_[ns]_a') + #1
# lema('[Ss]ubordinar_í_a[ns]?_i') + #1
# lema('[Ss]ubstitu_i_r(?:l[aeo]s?|se|)_í') + #1
# lema('[Ss]ubstra_í_(?:a[ns]?|d[ao]s?)_i') + #1
# lema('[Ss]ucumb(?:ir|)_í_a[ns]?_i') + #1
# lema('[Ss]urt(?:ir|)_í_a[ns]?_i') + #1
# lema('[Tt]a_m_poco_n') + #1
# lema('[Tt]apar_í_a[ns]?_i') + #1
# lema('[Tt]e_m_plo_n') + #1
# lema('[Tt]e_m_poral_n') + #1
# lema('[Tt]ej_í_a[ns]?_i') + #1
# lema('[Tt]em__porada_n') + #1
# lema('[Tt]em_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_e') + #1
# lema('[Tt]eni_en_do_ne') + #1
# lema('[Tt]estar_í_a[ns]?_i') + #1
# lema('[Tt]iem__po_n') + #1
# lema('[Tt]ocar_í_an_i') + #1
# lema('[Tt]olerar_í_a[ns]?_i') + #1
# lema('[Tt]om_á_r[mts]el[aeo]s?_a') + #1
# lema('[Tt]ra_ns_parente_sn') + #1
# lema('[Tt]ra_ns_portaba_sn') + #1
# lema('[Tt]ra_ns_portado_sn') + #1
# lema('[Tt]ra_ns_portes_sn') + #1
# lema('[Tt]ran_s_parencia_') + #1
# lema('[Tt]ran_s_portador_') + #1
# lema('[Tt]ran_s_portarse_') + #1
# lema('[Tt]ranscender_á_[ns]?_a') + #1
# lema('[Tt]ranscrib(?:ir|)_í_a[ns]?_i') + #1
# lema('[Tt]ranscurrir_á_[ns]?_a') + #1
# lema('[Tt]rasladar_í_a[ns]?_i') + #1
# lema('[Tt]ratar_í_a[ns]?_i') + #1
# lema('[Uu]n_ _papel_') + #1
# lema('[Uu]n_ _periodista_') + #1
# lema('[Vv]engar_í_a[ns]?_i') + #1
# lema('[Vv]ig_ésimo sé_ptima_esimose') + #1
# lema('[Vv]olar_í_a[ns]?_i') + #1
# lema('[Vv]olvi_éndos_e_endoc') + #1
# lema('[Vv]olvi_éndos_e_endoc') + #1
# lema('[ee]_m_pacad[ao]s?_n') + #1
# lema('_marzo__[Mm]arço', pre='acessado em [0-9]+ de ') + #1
# lema('[a]rd_í_an_i') + #1
# lema('[b]ajar_í_a[ns]?_i') + #1
# lema('[c]ern_í__i') + #1
# lema('[c]orr_í_as_i') + #1

lema('[Aa]firmar_í_a[ns]?_i') + #0
lema('[Aa]gotar_í_a[ns]?_i') + #0
lema('[Aa]mabil_í_sim[ao]s?_i') + #0
lema('[Aa]mad_í_sim[ao]s?_i') + #0
lema('\\b(?:[1-9]|[012][0-9]|3[01])_ de_ (?:[Ee]nero|[Ff]ebrero|[Mm]arzo|[Aa]bril|[Mm]ayo|[Jj]unio|[Jj]ulio|[Aa]gosto|[Ss]eptiembre|[Oo]ctubre|[Nn]oviembre|[Dd]iciembre)_') + #7048
lema('_ de _[12][0-9]{3}_', pre='(?:[Ee]nero|[Ff]ebrero|[Mm]arzo|[Aa]bril|[Mm]ayo|[Jj]unio|[Jj]ulio|[Aa]gosto|[Ss]eptiembre|[Oo]ctubre|[Nn]oviembre|[Dd]iciembre)') + 
lema('(?:[Aa]erot|[Cc]rono|[Hh]eli|[Tt]elet|[Tt])ran_s_port(?:a(?:[ns]?|ba[ns]?|bles?|ción|d[ao]s?|dor(?:es|)|ndo|r(?:se|ía[ns]?|))|e[ns]?|istas?)_') + #12
lema('(?:[Cc]on|[Ss](?:ub|))igu_i_entes?_') + #45
lema('(?:[Pp]|[Cc]op)rop__iedad(?:es|)_r') + #24
lema('(?:[Ss]emid|[Ss]ubd|[Hh]iperd|[Dd])esa_rroll_(?:ó|os?|a[nrs]?|ad[ao]s?|ando|ador|adora|adores|arse|aron|ar[ií]a[ns]?|aba[ns]?)_(?:roll|rr?oy|rrol)') + #164
lema('Ad_í_s Abeba_i') + #22
lema('Arbel_á_ez_a') + #94
lema('Azerbaiy_á_n_a') + #42
lema('Berm_ú_dez_u') + #448
lema('C_ú_cuta_u') + #153
lema('Car_ú_pano_u') + #15
lema('D_í_as_i', pre='(?:[uúUÚ]ltimos|Mil|Nueve|Nuestros|Trece|Buenos) ') + #31
lema('E_n_ (?:el|la|los|las)_N') + #15
lema('Emiratos _Á_rabes Unidos_A') + #51
lema('Benalc_á_zar_a') + 
lema('Kirguist_á_n_a') + #28
lema('Logroñ_é_s_e') + #27
lema('Mosc_ú__u') + #77
lema('Pap_ú_a_u', pre='(?:[Dd]e|[Ee]n) ') + #13
lema('Paraguan_á__a') + #14
lema('R_ó_terdam_o', pre='(?:[Dd]e|[Ee]n) ') + #5
lema('Rep_ú_blica Dominicana_u') + #203
lema('Sajcabaj_á__a') + #0
lema('Se_ú_l_u', pre='(?:[Dd]e|[Ee]n) ') + #19
lema('Sud_á_n\]\]_a', pre='\[\[') + #0
lema('T_á_riba_a') + #0
lema('T_ú_nez_u') + #78
lema('Taf_í_ del Valle_i') + #2
lema('Teher_á_n_a', pre='(?:[Dd]e|[Ee]n) ') + #6
lema('Vig_í_a_i', pre='El ') + #20
lema('[12][0-9]{3} _en cine__au cinéma', pre='\[') + #680
lema('[Aa]_ _cabo_', pre='[Ll]lev(?:[oó]|aron|a[ns]?) ') + #42
lema('[Aa]_ _gusto_', pre='(?:[Ee]st[aá]|estaba|sintió|muy|m[aá]s) ') + #0
lema('[Aa]_ _menudo_') + #7
lema('[Aa]_ _partir_') + #47
lema('[Aa]_ _punto_', pre='[Ee]st(?:a(?:[ns]|ba[ns]?|)|uvo)') + #0
lema('[Aa]_m_paro_n') + #1
lema('[Aa]_s_cendencias?_') + #0
lema('[Aa]_ñ_os (?:antes|después)_n') + #9
lema('[Aa]bandonar_í_a[ns]?_i') + #1
lema('[Aa]barcar_í_a[ns]?_i') + #0
lema('[Aa]br(?:ir|)_í_a[ns]?_i') + #4
lema('[Aa]br_í_a[ns]?_i') + #4
lema('[Aa]brir_á_[ns]?_a') + #5
lema('[Aa]bsor_b_(e[rns]?|id[ao]s?)_v') + #35
lema('[Aa]bsorb_í_a[ns]?_i') + #0
lema('[Aa]bstra_í_(?:a[ns]?|d[ao]s?)_i') + #0
lema('[Aa]c__ompañará_c') + #0
lema('[Aa]cad_é_mic(?:as|amente)_e') + #7
lema('[Aa]cceder_á_[ns]?_a') + #3
lema('[Aa]celerar_í_a[ns]?_i') + #0
lema('[Aa]cent_ú_(?:a[ns]?|e[ns]?)_u') + #2
lema('[Aa]ceptar_í_a[ns]?_i') + #0
lema('[Aa]cercar_s_e(?:lo|)_c') + #1
lema('[Aa]cetaldeh_í_d[ao]s?_i') + #9
lema('[Aa]co_g_(?:id[ao]s?|iera[ns]|erá?)_j') + #9
lema('[Aa]coger_á_[ns]?_a') + #2
lema('[Aa]compa_ñ_antes?_n') + #1
lema('[Aa]compañar_í_a[ns]?_i') + #1
lema('[Aa]cr_ó_nimos?_o') + #10
lema('[Aa]credit_á_(?:ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)|rsel[aeo]s?)_a') + #2
lema('[Aa]ct_ú_(?:a[ns]|e[ns]?)_u') + #30
lema('[Aa]cud(?:ir|)_í_a[ns]?_i') + #9
lema('[Aa]cudir_á_[ns]?_a') + #0
lema('[Aa]cusar_í_a[ns]?_i') + #0
lema('[Aa]dmit(?:ir|)_í_a[ns]?_i') + #1
lema('[Aa]dmit_í__i') + #2
lema('[Aa]dmitir_á_[ns]?_a') + #0
lema('[Aa]dole_sc_entes?_[sc]') + #18
lema('[Aa]doptar_í_a[ns]?_i') + #1
lema('[Aa]dquir_ió__(?:io|[oó])') + #25
lema('[Aa]dquir_í_a[ns]?_i') + #0
lema('[Aa]dquirir_á_[ns]?_a') + #3
lema('[Aa]dvers_a_rios?_á') + #11
lema('[Aa]dvi__rti(?:endo|eron|éndole|éndoles|éndose|ó)_e') + #5
lema('[Aa]er__opuertos?_e') + #3
lema('[Aa]er_ó_bic[ao]s?_o') + #5
lema('[Aa]erol_í_neas?_i') + #160
lema('[Aa]fectar_í_a[ns]?_i') + #1
lema('[Aa]g_o_sto_u', pre='(?:[Dd]e|[0-9]+\.?) ') + #18
lema('[Aa]gr_ó_nom[ao]s?_o') + #24
lema('[Aa]gradar_í_a[ns]?_i') + #1
lema('[Aa]gradecim_i_entos?_') + #1
lema('[Aa]jonjol_í__i') + #5
lema('[Aa]justad_í_sim[ao]s?_i') + #1
lema('[Aa]l_ _menos_') + #3
lema('[Aa]l_í_an?_i', pre='[Ss]e ') + #14
lema('[Aa]lcan_c_e[ns]?_z') + #8
lema('[Aa]lcanzar_í_a[ns]?_i') + #1
lema('[Aa]ldeh_í_d[ao]s?_i') + #26
lema('[Aa]leg_ó_ric[ao]s?_o') + #5
lema('[Aa]lfarer_í_as?_i') + #10
lema('[Aa]lgor_í_tmicas?_i') + #3
lema('[Aa]lgori_t_mos?_') + #4
lema('[Aa]lien_í_genas?_i') + #87
lema('[Aa]lm_í_bar(?:es|)_i') + #6
lema('[Aa]lt_í_sim[ao]s?_i') + #2
lema('[Aa]m_é_rica (?:del [Nn]orte|del [Ss]ur|[Cc]entral|[Hh]ispana|[Aa]nglosajona|de Cali)_e') + #121
lema('[Aa]maz_ó_nic(?:as|os?)_o') + #19
lema('[Aa]maz_ó_nica_o', pre='(?:apariencia|especie|[Ss]elva|tribu|Lengua|medicinal|Cuenca|Guayaba|[Rr]egi[oó]n|cultural|dulce..|Colombia..| y) ') + #4
lema('[Aa]mpl_í_sim[ao]s?_i') + #1
lema('[Aa]n_áli_sis_alí') + #9
lema('[Aa]n_ó_nim(?:[ao]s|amente)_o') + #14
lema('[Aa]n_ó_nim[ao]_o', pre='(?:[Ss]ociedad|[Mm]ensaje) ') + #17
lema('[Aa]nal_ó_gic[ao]s?_o') + #19
lema('[Aa]nexar_í_a[ns]?_i') + #0
lema('[Aa]nexion_á_r[mts]el[aeo]s?_a') + #0
lema('[Aa]notar_í_a[ns]?_i') + #6
lema('[Aa]ntag_ó_nic[ao]s?_o') + #22
lema('[Aa]ntagon_i_stas?_í') + #3
lema('[Aa]nti_i_nflamatori[ao]s?_') + #21
lema('[Aa]ntinarc_ó_ticos?_o') + #1
lema('[Aa]ntiqu_í_sim[ao]s?_i') + #2
lema('[Aa]ntropom_ó_rfic[ao]s?_o') + #9
lema('[Aa]p_are_c(?:e(?:[ns]?|r(?:a[ns]?|[áé]|ía[ns]?|))|ieron)_(?:ara|re)') + #29
lema('[Aa]p_é_ndices?_e') + #22
lema('[Aa]p_í_col[ao]s?_i') + #7
lema('[Aa]p_ó_stol (?:San|Andr[eé]s|Juan|Jaime|Pedro|Pablo|Santiago|Mateo|Mat[ií]as|Tom[aá]s|Bartolom[eé])_o') + #21
lema('[Aa]p_ó_stol_o', pre='(?:Andr[eé]s|Juan|Jaime|Pedro|Pablo|Santiago|Mateo|Mat[ií]as|Tom[aá]s|Bartolom[eé]) ') + #154
lema('[Aa]pagar_í_a[ns]?_i') + #0
lema('[Aa]parec_í_a[ns]?_i') + #24
lema('[Aa]parecer_á_[ns]?_a') + #12
lema('[Aa]parecer_í_a[ns]?_i') + #9
lema('[Aa]pocal_i_psis_í') + #17
lema('[Aa]poderar_s_e(?:lo|)_c') + #0
lema('[Aa]poyar_í_a[ns]?_i') + #0
lema('[Aa]prend_í_a[ns]?_i') + #2
lema('[Aa]prender_á_[ns]?_a') + #1
lema('[Aa]pro_b_ad[ao]s?_v') + #36
lema('[Aa]provechar_í_a[ns]?_i') + #0
lema('[Aa]rist_ó_cratas?_o') + #15
lema('[Aa]rque_ó_log[ao]s?_o') + #31
lema('[Aa]rqueol_ó_gic[ao]s?_o') + #126
lema('[Aa]rquer_í_as?_i') + #11
lema('[Aa]rras_ó_ (?:en|con)_o') + #14
lema('[Aa]rt_í_sticamente_i') + #34
lema('[Aa]rtific_i_al(?:es|)_') + #59
lema('[Aa]rtiller_í_as?_i') + #65
lema('[Aa]sar_í_as?_i') + #1
lema('[Aa]sc_ó_rbic[ao]s?_o') + #2
lema('[Aa]scend_í_(?:a[ns]?)_i') + #5
lema('[Aa]scender_á_[ns]?_a') + #0
lema('[Aa]sesinar_í_a[ns]?_i') + #1
lema('[Aa]sis__tió_i') + #8
lema('[Aa]sist(?:ir|)_í_a[ns]?_i') + #13
lema('[Aa]sistir_á_[ns]?_a') + #0
lema('[Aa]sociar_í_a[ns]?_i') + #1
lema('[Aa]sum(?:ir|)_í_a[ns]?_i') + #5
lema('[Aa]sumir_á_[ns]?_a') + #1
lema('[Aa]ten_ú_(?:a[ns]?|e[ns]?)_u') + #4
lema('[Aa]tend_í_(?:a[ns]?|)_i') + #3
lema('[Aa]tender_á_[ns]?_a') + #1
lema('[Aa]terrar_í_a[ns]?_i') + #1
lema('[Aa]tl_é_tic(?:[ao]s|amente)_e') + #6
lema('[Aa]tra_í_d[ao]s?_i') + #24
lema('[Aa]trap_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema('[Aa]tribu_i_d[ao]s?_í') + #65
lema('[Aa]tribu_i_r(?:l[aeo]s?|se|)_í') + #1
lema('[Aa]tribu_í_r[mts]el[aeo]s?_i') + #2
lema('[Aa]u_té_ntic[ao]s?_nte') + #1
lema('[Aa]ut_ó_dromos_o') + #0
lema('[Aa]uto_o_xida(?:ción|ciones|ntes?)_') + #0
lema('[Aa]utob_u_ses_ú') + #2
lema('[Aa]utom_á_tic(?:[ao]s|amente)_a') + #33
lema('[Aa]van_z_(?:ando|ad[ao]s?|[aoó])_s') + #3
lema('[Aa]verg_ü_enza[ns]?_u') + #2
lema('[Aa]yudar_í_a[ns]?_i') + #3
lema('[Aa]ñad_í__i') + #0
lema('[Aa]ñadir_á_[ns]?_a') + #1
lema('[Bb]_ri_tánic[ao]s?_ir') + #0
lema('[Bb]_á_ltic[ao]s_a') + #2
lema('[Bb]_á_ltico(?! S\.)_a') + #4
lema('[Bb]_á_sic(?:as|os?|amente)_a') + #75
lema('[Bb]_ú_squedas?_u') + #147
lema('[Bb]acteriolog_í_as?_i') + #1
lema('[Bb]ailar_í_a[ns]?_i') + #2
lema('[Bb]aj_í_sim[ao]s?_i') + #2
lema('[Bb]astar_í_a[ns]?_i') + #1
lema('[Bb]endec_í_a[ns]?_i') + #0
lema('[Bb]eneficiar_í_an?_i', pre='[Ss]e ') + #4
lema('[Bb]iof_í_sic[ao]s?_i') + #6
lema('[Bb]iomec_á_nic[ao]s?_a') + #7
lema('[Bb]iopol_í_tix[ao]s?_i') + #0
lema('[Bb]ioqu_í_mic[ao]s?_i') + #28
lema('[Bb]iotecnol_ó_gic[ao]s?_o') + #3
lema('[Bb]lanqu_í_sim[ao]s?_i') + #0
lema('[Bb]ol_í_grafos?_i') + #6
lema('[Bb]oleter_í_as?_i') + #6
lema('[Bb]r_ú_julas?_u') + #8
lema('[Bb]rindar_í_a[ns]?_i') + #0
lema('[Bb]uen_í_sim[ao]s?_i') + #4
lema('[Bb]urocr_á_tic[ao]s?_a') + #1
lema('[Bb]uscar_í_a[ns]?_i') + #1
lema('[Bb]ut_í_ric[ao]s?_i') + #3
lema('[Bb]utanodi_ó_lic[ao]s?_o') + #0
lema('[Cc]_iu_dadan[ao]s?_ui') + #4
lema('[Cc]_á_lculo (?:del?|num[eé]rico|mental|según|estructural)_a') + #45
lema('[Cc]_á_lculo_a', pre='(?:[Ee]l|[Uu]n|[Dd]el?|[Aa]l|y)') + #0
lema('[Cc]_á_lid(?:[ao]s|amente)_a') + #5
lema('[Cc]_á_nceres_a') + #12
lema('[Cc]_á_todos?_a') + #4
lema('[Cc]_é_sped_e') + #138
lema('[Cc]_ó_digos_o') + #26
lema('[Cc]_ó_mo_o', pre='¿ *') + #207
lema('[Cc]_ó_mod(?:[ao]s|amente)_o') + #11
lema('[Cc]_ó_moda_o') + #2
lema('[Cc]_ó_nic(?:as|os?)_o') + #0
lema('[Cc]_ó_nyuges?_o') + #20
lema('[Cc]a_cerí_as?_(?:zer[ií]|ceri)') + #44
lema('[Cc]a_m_pos_n') + #17
lema('[Cc]a_y_endo_ll') + #1
lema('[Cc]a_í_a[ns]_i') + #3
lema('[Cc]acer_í_as?_i') + #27
lema('[Cc]ad_á_veres_a') + #10
lema('[Cc]alor_í_as?_i') + #6
lema('[Cc]am_é_lid[ao]s?_e') + #3
lema('[Cc]ambiar_í_a_i', pre='(?:[Nn]o|[Ll][ao]) ') + #1
lema('[Cc]ambiar_í_an_i') + #0
lema('[Cc]ampeon_í_sim[ao]s?_i') + #6
lema('[Cc]anadi_e_nse_é') + #0
lema('[Cc]ancer_í_gen[ao]s?_i') + #3
lema('[Cc]ant_one_s_óne') + #2
lema('[Cc]antar_í_a[ns]?_i') + #8
lema('[Cc]apit_á_n Am[eé]rica_a') + #31
lema('[Cc]ar_í_sim[ao]s?_i') + #1
lema('[Cc]ar_ó_tid[ao]s?_o') + #10
lema('[Cc]aracter_í_stc[ao]s?_i') + #3
lema('[Cc]aracter_í_stic[ao]s?_i') + #185
lema('[Cc]aracteri_z_(?:a[nrs]?|d[ao]s?|[oó])_s') + #2
lema('[Cc]aracterí_s_ticas?_') + #7
lema('[Cc]ardiolog_í_as?_i') + #23
lema('[Cc]ardiopat_í_as?_i') + #11
lema('[Cc]arn_í_vor(os?|as)_i') + #21
lema('[Cc]asar_s_e(?:lo|)_c') + #0
lema('[Cc]at_alogó__ologo') + #3
lema('[Cc]at_á_logo_a', pre='(?:[Ee]l|[Uu]n|[Dd]e) ') + #85
lema('[Cc]at_á_logos_a') + #7
lema('[Cc]atastr_ó_fic(?:[ao]s?|amente)_o') + #3
lema('[Cc]atedr_á_tic[ao]s?_a') + #14
lema('[Cc]ausar_í_a[ns]?_i') + #0
lema('[Cc]e_ntroamé_rica_troam[eé]') + #0
lema('[Cc]ed_í_a[ns]?_i') + #1
lema('[Cc]ent_í_metros?_i') + #9
lema('[Cc]entrar_í_a[ns]?_i') + #0
lema('[Cc]ercan_í_as?_i') + #73
lema('[Cc]et_á_ceos?_a') + #9
lema('[Cc]h_á_rter_a', pre='(?:aerolíneas?|vuelos?|tipos?|modos?)(?: de|) ') + #52
lema('[Cc]ie_m_piés_n') + #5
lema('[Cc]ircu_n_stacias_') + #0
lema('[Cc]ircu_n_stancia(?:l|les|)_') + #0
lema('[Cc]ircun_s_pección_') + #1
lema('[Cc]ircun_s_tancias?_') + #1
lema('[Cc]irug_í_as?_i') + #47
lema('[Cc]iudad__es_d') + #2
lema('[Cc]l_á_sic(?:o|[ao]s|amente)_a') + #289
lema('[Cc]l_í_nic(?:[ao]s|amente)_i') + #20
lema('[Cc]lasificar_í_a[ns]?_i') + #2
lema('[Cc]lorh_í_dric[ao]s?_i') + #4
lema('[Cc]o_m_paras_n') + #2
lema('[Cc]o_m_petencia_n') + #2
lema('[Cc]o_m_port(arse|amiento)_n') + #2
lema('[Cc]o_m_prar_n') + #2
lema('[Cc]o_m_pre_n') + #1
lema('[Cc]o_m_puesto_n') + #0
lema('[Cc]o_m_puso_n') + #0
lema('[Cc]o_nvirtió__virtio') + #0
lema('[Cc]o_o_peraci(?:ón|ones)_') + #12
lema('[Cc]o_o_rdenad[ao]s?_') + #5
lema('[Cc]obrar_í_a[ns]?_i') + #2
lema('[Cc]octeler_í_as?_i') + #0
lema('[Cc]oincidir_á_[ns]?_a') + #0
lema('[Cc]ol_a_boración_o') + #1
lema('[Cc]ol_é_ric[ao]s?_e') + #0
lema('[Cc]om_é_r[mts]el[aeo]s?_e') + #4
lema('[Cc]om_ú_nmente_u') + #119
lema('[Cc]ombat(?:ir|)_í_a[ns]?_i') + #5
lema('[Cc]omenzar_í_a[ns]?_i') + #8
lema('[Cc]ompa_rtió__r?tio', pre='(?:[Qq]ui[ée]n|[Qq]u[ée]|[Dd][óo]nde|[Cc]u[áa]ndo|[Tt]ambién|[Aa]demás|[Ss]e|[Ll][ao]s?|e) ') + #8
lema('[Cc]ompart(?:ir|)_í_a[ns]?_i') + #11
lema('[Cc]ompart_í_a(?:[ns]?|mos)_i') + #10
lema('[Cc]ompartir_á_[ns]?_a') + #1
lema('[Cc]ompet_í_(?:a[ns]?|)_i') + #6
lema('[Cc]ompet_í_a[ns]?_i') + #6
lema('[Cc]ompetic_i_ón_í?') + #1
lema('[Cc]ompetir_á_n?_a') + #5
lema('[Cc]ompetir_í_a[ns]?_i') + #1
lema('[Cc]ompetitiv_id_ad_') + #1
lema('[Cc]ompletar_í_a[ns]?_i') + #2
lema('[Cc]omplic_á_r[mts]el[aeo]s?_a') + #0
lema('[Cc]ompo_s_itor(?:as?|es|)_c') + #1
lema('[Cc]ompon_í_a[ns]?_i') + #9
lema('[Cc]ompondr_á_[ns]?_a') + #1
lema('[Cc]omposi_c_ión_s') + #0
lema('[Cc]omprend_í_a[ns]?_i') + #4
lema('[Cc]omprender_á_[ns]?_a') + #0
lema('[Cc]omunic_á_r[mts]el[aeo]s?_a') + #0
lema('[Cc]on __el_el con ') + #10
lema('[Cc]on_cedié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_sedie') + #1
lema('[Cc]on_s_ecuencias?_c') + #0
lema('[Cc]on_s_iderad[ao]s?_c') + #3
lema('[Cc]on_s_titu(?:ye|y[oó]|ción|ciones|id[ao]s?)_') + #3
lema('[Cc]on_s_tru(?:ir(?:lo|se|á|án|ía|ían|)|cción|cciones)_') + #27
lema('[Cc]on_s_truyeron_') + #2
lema('[Cc]on_strui_d[ao]s?_(?:tru[ií]|struí)') + #80
lema('[Cc]on_strui_d[ao]s?_(?:tru[ií]|struí)') + #80
lema('[Cc]on_struyó__truyo') + #1
lema('[Cc]onced_í_a[ns]?_i') + #1
lema('[Cc]onceder_á_[ns]?_a') + #0
lema('[Cc]onclu_i_(?:r(?:l[aeo]s?|se|)|d[ao]s?)_í') + #38
lema('[Cc]onclu_i_d[ao]s?_í') + #36
lema('[Cc]oncluir_á_[ns]?_a') + #0
lema('[Cc]oncurr(?:ir|)_í_a[ns]?_i') + #0
lema('[Cc]oncurrir_á_[ns]?_a') + #0
lema('[Cc]ondu_jo__cio') + #1
lema('[Cc]onduc_í_a[ns]?_i') + #5
lema('[Cc]onducir_á_[ns]?_a') + #2
lema('[Cc]onf_í_e[ns]_i') + #0
lema('[Cc]onf_í_o_i', pre='(?:[Tt]i|[Vv]os) ') + #0
lema('[Cc]onfia_n_zas?_') + #9
lema('[Cc]onfie_s_a[ns]?_z') + #3
lema('[Cc]onformar_í_a[ns]?_i') + #2
lema('[Cc]ono_c_id[ao]s?_s') + #10
lema('[Cc]onoc_í_a[ns]?_i') + #26
lema('[Cc]onocer_s_e(?:lo|)_c') + #0
lema('[Cc]onocer_á_[ns]?_a') + #8
lema('[Cc]onocer_í_a(?:[ns]?|mos)_i') + #9
lema('[Cc]onocid_í_sim[ao]s?_i') + #1
lema('[Cc]onocim_ie_ntos?_ei') + #1
lema('[Cc]ons_i_guieron_e') + #9
lema('[Cc]ons_iguió__eguio') + #1
lema('[Cc]onsagrar_í_a[ns]?_i') + #3
lema('[Cc]onsecu_e_ncias?_a') + #0
lema('[Cc]onsegu_í_a[ns]?_i') + #20
lema('[Cc]onseguir_á_[ns]?_a') + #4
lema('[Cc]onseguir_í_a[ns]?_i') + #5
lema('[Cc]onsider_á_r[mts]el[aeo]s?_a') + #2
lema('[Cc]onsig_uió__i[oó]') + #12
lema('[Cc]onsigu_ió__o') + #1
lema('[Cc]onsist_í_a[ns]?_i') + #21
lema('[Cc]onsistir_á_[ns]?_a') + #0
lema('[Cc]onst_r_uye[ns]?_') + #0
lema('[Cc]onstituir_á_[ns]?_a') + #0
lema('[Cc]onstru_i_r(?! (?:a paz|unha))_í') + #9
lema('[Cc]onstru_í_as?_i') + #15
lema('[Cc]onstruir_á_[ns]?_a') + #4
lema('[Cc]onsum(?:ir|)_í_a[ns]?_i') + #2
lema('[Cc]ont_á_r[mts]el[aeo]s?_a') + #1
lema('[Cc]ont_ó_ (?:que|como|con)_o') + #43
lema('[Cc]ontadur_í_as?_i') + #7
lema('[Cc]ontar_í_a[ns]?_i') + #6
lema('[Cc]onte_m_poránea_n') + #4
lema('[Cc]onten_í_a[ns]_i') + #3
lema('[Cc]ontend_í_(?:a[ns]?|)_i') + #2
lema('[Cc]ontendr_á_[ns]?_a') + #3
lema('[Cc]onteni_en_do_ne') + #0
lema('[Cc]onti_n_gentes?_') + #13
lema('[Cc]ontin_ú_(?:an|en)_u') + #95
lema('[Cc]ontinuar_í_a[ns]?_i') + #2
lema('[Cc]ontra_í_(?:a[ns]?|d[ao]s?)_i') + #24
lema('[Cc]ontrar_r_estar(?:l[aeo]s?|ía[ns]?|)_') + #7
lema('[Cc]ontrar_r_evoluci(?:ón|onari[ao]s?)_') + #19
lema('[Cc]ontrar_restará__estara') + #0
lema('[Cc]ontribu_i_d[ao]s?_í') + #5
lema('[Cc]ontribu_i_d[ao]s?_í') + #5
lema('[Cc]ontribu_i_r(?:l[aeo]s?|se|)_í') + #1
lema('[Cc]ontribuir_á_[ns]?_a') + #0
lema('[Cc]onv_erti_rían_ierte') + #0
lema('[Cc]onv_i_rti(?:ó|endo|eron)_e') + #49
lema('[Cc]onv_irtié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ertie') + #2
lema('[Cc]onven_c_er(?:se|l[ao]s?|[mt]e|nos|á[ns]?)_s') + #0
lema('[Cc]onvencer_á_[ns]?_a') + #0
lema('[Cc]onvert(?:ir|)_í_a[ns]?_i') + #20
lema('[Cc]onvertir_á_[ns]?_a') + #9
lema('[Cc]onvertir_í_a[ns]?_i') + #15
lema('[Cc]onvi__rtieron_e') + #9
lema('[Cc]onvi_rtié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ertie') + #4
lema('[Cc]onvi_rtió__ertio') + #2
lema('[Cc]onvi_rtió__erto', pre='[Ss]e ') + #3
lema('[Cc]onvir_tió__itio') + #0
lema('[Cc]onvirt_ió__o') + #1
lema('[Cc]onviv_í_a[ns]_i') + #1
lema('[Cc]or_respondí_a_espondi') + #0
lema('[Cc]ore_ó_graf[ao]s?_o') + #22
lema('[Cc]oronar_s_e(?:lo|)_c') + #0
lema('[Cc]orr_í_an_i') + #3
lema('[Cc]orre_spondí_a_pondi') + #0
lema('[Cc]orrer_í_a[ns]?_i') + #4
lema('[Cc]orrespond(?:er|)_í_an?_i') + #13
lema('[Cc]orrespond_í_a[ns]?_i') + #10
lema('[Cc]orresponder_á_[ns]?_a') + #0
lema('[Cc]orresponder_í_a[ns]?_i') + #3
lema('[Cc]r_i_men_') + #0
lema('[Cc]r_á_neos?_a') + #64
lema('[Cc]r_í_menes_i') + #68
lema('[Cc]re_í__i') + #3
lema('[Cc]re_í_a(?:[ns]?|mos)_i') + #56
lema('[Cc]re_í_bles?_i') + #8
lema('[Cc]re_í_d[ao]s?_i') + #14
lema('[Cc]rear_í_a[ns]?_i') + #3
lema('[Cc]recer_á_[ns]?_a') + #0
lema('[Cc]ri_a_turas?_') + #1
lema('[Cc]ron_ó_metros?_o') + #33
lema('[Cc]ronol_ó_gic(?:[ao]s|amente)_o') + #8
lema('[Cc]u[aá]_nd_o_dn') + #5
lema('[Cc]u_m_pla_n') + #2
lema('[Cc]u_m_pliéndose_n') + #0
lema('[Cc]u_á_ntic[ao]s?_a') + #11
lema('[Cc]ua_n_do (?:se|ven?|el|es|eran?|fue|llegan?|hay|el|la|sale|sus?|este)_') + #1
lema('[Cc]uadrag_é_sim[ao]s?_e') + #5
lema('[Cc]ubrir_á_[ns]?_a') + #0
lema('[Cc]ulpar_í_a[ns]?_i') + #1
lema('[Cc]umpl(?:ir|)_í_a[ns]?_i') + #16
lema('[Cc]umpl_í__i') + #1
lema('[Cc]umplir_á_[ns]?_a') + #4
lema('[Cc]ut_á_ne[ao]s?_a') + #23
lema('[Dd]]_ú_os_u') + #0
lema('[Dd]_e_cimocuart[ao]_é') + #35
lema('[Dd]_e_cimoquint[ao]_é') + #38
lema('[Dd]_e_cimosext[ao]_é') + #15
lema('[Dd]_e_cimoséptim[ao]_é') + #3
lema('[Dd]_ecimo_ctav[ao]_écimoo') + #0
lema('[Dd]_á_r[mts]el[aeo]s?_a') + #6
lema('[Dd]_é_biles(?! dignare)_e') + #10
lema('[Dd]_é_bilmente_e') + #3
lema('[Dd]_í_a a d[ií]a_i') + #36
lema('[Dd]_í_gitos?_i') + #79
lema('[Dd]_ó_lar_o', pre='(?:[Ee]l|[Uu]n|[Dd]el|[Aa]l) ') + #45
lema('[Dd]_ó_lares_o', pre='(?:[Ll]os|[Uu]nos|[Ee]n|[Dd]e) ') + #333
lema('[Dd]_ó_nde_o', pre='¿ *') + #1
lema('[Dd]_ú_ctil_u') + #2
lema('[Dd]añar_í_a[ns]?_i') + #0
lema('[Dd]e_ _pronto_') + #5
lema('[Dd]e__l (?:2006|Amparo|Cauca|Club|Commonwealth|Consejo|Ejército|Estado|Norte|Working|archipiélago|año|calentamiento|canal|catálogo|condado|cuento|cuerpo|gobierno|himno|museo|oeste|peón|prestigioso|profesor|punto|siglo|éter)_e') + #1
lema('[Dd]e_cisio_nes_(?:cisió|cici[oó]|si[sc]i[oó])') + #10
lema('[Dd]e_s_c(?:enso|iende[ns]?|end(?:er?|ido)|entrali(?:ce[ns]?|zar|zó|zació))_') + #18
lema('[Dd]e_s_cifrar_') + #1
lema('[Dd]ebat(?:ir|)_í_a[ns]?_i') + #0
lema('[Dd]ebatir_á_[ns]?_a') + #0
lema('[Dd]eber_á_[ns]?_a') + #34
lema('[Dd]eber_í_a(?:[ns]?|mos)_i') + #38
lema('[Dd]ebilitad_í_sim[ao]s?_i') + #0
lema('[Dd]ec_í_a[ns]?_i', pre='(?:[Qq]u[eé]|[Ss]e|[Ll]es?|[Mm]e|[Nn]os|[Ll]o|[Ss]eg[uú]n|[Dd]onde|[Cc]u[aá]l|[Cc][oó]mo|[Ss][oó]lo|[EeÉ]l|[Qq]ui[eé]n) ') + #15
lema('[Dd]ec_í_amos_i') + #5
lema('[Dd]ec_í_r[mts]el[aeo]s?_i') + #4
lema('[Dd]eca_í_do_i') + #6
lema('[Dd]eci__dió_ci') + #2
lema('[Dd]ecid_í__i') + #7
lema('[Dd]ecidir_á_[ns]?_a') + #1
lema('[Dd]ecimos_é_ptim[ao]s?_e') + #24
lema('[Dd]ecimos_é_ptimo_e') + #3
lema('[Dd]eclarar_í_a[ns]?_i') + #0
lema('[Dd]educir_á__a') + #0
lema('[Dd]ef__endió_i') + #2
lema('[Dd]efender_á_[ns]?_a') + #4
lema('[Dd]efin(?:ir|)_í_a[ns]?_i') + #8
lema('[Dd]efinir_á_[ns]?_a') + #2
lema('[Dd]ejar_í_a[ns]?_i') + #12
lema('[Dd]em_ócra_tas?_[oó]cr') + #2
lema('[Dd]ema_s_iados?_c') + #2
lema('[Dd]emandar_í_a[ns]?_i') + #1
lema('[Dd]emost_r_ar(?:le|on|se|)_') + #2
lema('[Dd]enominar_í_a(?:[ns]?|mos)_i') + #1
lema('[Dd]epend_í_a[ns]?_i') + #6
lema('[Dd]epender_á_[ns]?_a') + #0
lema('[Dd]erivar_í_a[ns]?_i') + #1
lema('[Dd]errotar_í_a[ns]?_i') + #0
lema('[Dd]erru_i_d[ao]s?_í') + #5
lema('[Dd]es_ig_nad[ao]s?_gi') + #54
lema('[Dd]es_é_rtic[ao]s?_e') + #6
lema('[Dd]esaf_i_ar_í') + #4
lema('[Dd]esap_are_r(?:e(?:[ns]?|r(?:a[ns]?|[áé]|ía[ns]?|))|ieron)c_(?:ara|re)') + #0
lema('[Dd]esapare_z_ca[ns]?_s') + #2
lema('[Dd]esaparec_í_a[ns]?_i') + #4
lema('[Dd]esaparecer_á_[ns]?_a') + #2
lema('[Dd]esastro_s_[ao]s?_z') + #30
lema('[Dd]escan_s_(?:os?|ar)_z') + #18
lema('[Dd]escend_í_(?:a[ns]?|)_i') + #6
lema('[Dd]escender_á_[ns]?_a') + #3
lema('[Dd]esconf_í_a[na]?_i') + #3
lema('[Dd]escono_c_id[ao]s?_s') + #1
lema('[Dd]escrib(?:ir|)_í_a[ns]?_i') + #5
lema('[Dd]escrib_í__i') + #0
lema('[Dd]escub__rir_i') + #0
lema('[Dd]escub_r_ieron_') + #3
lema('[Dd]escub_r_ir(?:se|)_') + #9
lema('[Dd]escub_ri_mientos?_ir') + #3
lema('[Dd]escubr(?:ir|)_í_a[ns]?_i') + #2
lema('[Dd]escubr_í__i') + #5
lema('[Dd]escubrir_á_[ns]?_a') + #6
lema('[Dd]ese_m_peñarlos_n') + #0
lema('[Dd]ese_m_peño_n') + #1
lema('[Dd]esear_í_a[ns]?_i') + #1
lema('[Dd]eshacer_s_e(?:lo|)_c') + #1
lema('[Dd]esp_i_dió_e') + #2
lema('[Dd]esped_í_a[ns]?_i') + #3
lema('[Dd]esplazar_s_e(?:lo|)_c') + #2
lema('[Dd]espose_í_d[ao]s?_i') + #18
lema('[Dd]esprend_í_a[ns]?_i') + #1
lema('[Dd]esta_ca_d[ao]s?_') + #21
lema('[Dd]estacad_í_sim[ao]s?_i') + #1
lema('[Dd]estinar_í_a[ns]?_i') + #0
lema('[Dd]estitu_i_d[ao]s?_í') + #25
lema('[Dd]estru_i_d[ao]s?_í') + #78
lema('[Dd]estru_i_r(?:l[aeo]s?|se|)_í') + #6
lema('[Dd]estru_í__i') + #1
lema('[Dd]estruir_á_[ns]?_a') + #2
lema('[Dd]esv_á_n_a') + #8
lema('[Dd]esverg_ü_enza[ns]?_u') + #0
lema('[Dd]etendr_á_[ns]?_a') + #1
lema('[Dd]eval_ú_(?:a[ns]?|e[ns]?)_u') + #3
lema('[Dd]evolver_á_[ns]?_a') + #0
lema('[Dd]evorar_í_a[ns]?_i') + #0
lema('[Dd]i_scí_pul[ao]s?_ci') + #0
lema('[Dd]i_sminui_d[ao]s?_minuí') + #2
lema('[Dd]i_á_metros?_a') + #210
lema('[Dd]i_é_ramos_e') + #1
lema('[Dd]i_ó_xidos?_o') + #6
lema('[Dd]iab_ó_lic(?:as|os)_o') + #2
lema('[Dd]iagn_osticó__(?:óstic[oó]|ostico)', pre='[Ss]e(?: me| te| l[aeo]s?|) ') + #6
lema('[Dd]ibujar_í_a[ns]?_i') + #0
lema('[Dd]iecis_é_is_e') + #92
lema('[Dd]iet_é_tic[ao]s?_e') + #3
lema('[Dd]if_í_cil(?:es|mente|)_i') + #143
lema('[Dd]ifer_í_a[ns]?_i') + #0
lema('[Dd]ign_í_sim[ao]s?_i') + #3
lema('[Dd]ij__eron_i') + #10
lema('[Dd]ij_o__ó') + #6
lema('[Dd]ilu_i_d[ao]s?_í') + #9
lema('[Dd]in_á_mic(?:[ao]s|amente)_a') + #9
lema('[Dd]ir_e_ctamente_é') + #2
lema('[Dd]ir_í_amos_i') + #0
lema('[Dd]iri_g_i(?:d[ao]s?|r(?:[tsm]e|á|ía[ns]|l[aeo]s?|))_j') + #26
lema('[Dd]iri_gí_a[ns]?_(?:j[ií]|gi)') + #19
lema('[Dd]irig_id_o por_') + #1
lema('[Dd]irig_í__i') + #2
lema('[Dd]irigir_á_[ns]?_a') + #4
lema('[Dd]is_cí_pul[ao]s?_i') + #2
lema('[Dd]iscurr(?:ir|)_í_a[ns]?_i') + #1
lema('[Dd]iscut(?:ir|)_í_a[ns]?_i') + #3
lema('[Dd]ise_ñ_a(?:d[ao]s?|dor(?:a|es|)|r)_n') + #3
lema('[Dd]isfra_c_es_z') + #0
lema('[Dd]isminu_i_d[ao]s?_í') + #22
lema('[Dd]isminu_i_r(?:l[aeo]s?|se|)_í') + #0
lema('[Dd]isminuir_á_[ns]?_a') + #0
lema('[Dd]isolver_á__a') + #2
lema('[Dd]isparar_í_a[ns]?_i') + #0
lema('[Dd]ispon_í_a[ns]?_i') + #15
lema('[Dd]ispondr_á_[ns]?_a') + #0
lema('[Dd]isputad_í_sim[ao]s?_i') + #0
lema('[Dd]isputar_í_a[ns]?_i') + #9
lema('[Dd]isten_s_ión_c') + #6
lema('[Dd]istingu(?:ir|)_í_a[ns]?_i') + #7
lema('[Dd]istingu_i_d[ao]s?_í') + #1
lema('[Dd]istinguir_á_[ns]?_a') + #0
lema('[Dd]istribu_i_d[ao]s?_í') + #56
lema('[Dd]istribu_i_r(?:l[aeo]s?|se|)_í') + #1
lema('[Dd]istribu_í_a[ns]?_i') + #12
lema('[Dd]istribuir_á_[ns]?_a') + #0
lema('[Dd]isuad(?:ir|)_í_a[ns]?_i') + #0
lema('[Dd]ivi_sio_n_ci[oó]') + #3
lema('[Dd]ividir_á_[ns]?_a') + #1
lema('[Dd]ivorciar_s_e(?:lo|)_c') + #0
lema('[Dd]iál_o_gos?_') + #1
lema('[Dd]onar_í_an_i') + #0
lema('[Dd]r_á_stic(?:[ao]s|amente)_a') + #7
lema('[Dd]ram_á_tic(?:[ao]s|amente)_a') + #2
lema('[Dd]udar_í_a[ns]?_i') + #1
lema('[Dd]ur_an_te_na') + #5
lema('[Dd]ur_í_sim[ao]s?_i') + #3
lema('[Dd]urar_í_a[ns]?_i') + #3
lema('[Ee]__pisodios?_s') + #9
lema('[Ee]_jem_plo_njen') + #1
lema('[Ee]_m_parejado_n') + #0
lema('[Ee]_m_perador_n') + #5
lema('[Ee]_m_pero_n') + #2
lema('[Ee]_m_pieza_n') + #0
lema('[Ee]_m_plear_n') + #1
lema('[Ee]_m_presa_n') + #1
lema('[Ee]_nvolverá_[ns]?_(?:mbolver[aá]|nbolver[aá]|nvolvera)') + #0
lema('[Ee]_s_pectador(?:es|)_x') + #14
lema('[Ee]_s_trech(?:[ao]s?|amente)_x') + #17
lema('[Ee]_x_celencias?_s?') + #0
lema('[Ee]_x_pectativas?_s') + #12
lema('[Ee]char_í_a[ns]?_i') + #1
lema('[Ee]con_ó_mic(?:[ao]s|amente)_o') + #58
lema('[Ee]g_ó_latras?_o') + #0
lema('[Ee]goc_é_ntric[ao]s?_e') + #2
lema('[Ee]j_é_rcitos_e') + #17
lema('[Ee]jerc_í_a[ns]?_i') + #13
lema('[Ee]jercer_á_[ns]?_a') + #0
lema('[Ee]jerci_cio__o', pre='[Ee]l ') + #1
lema('[Ee]l_e_gir(?:se|)_i') + #8
lema('[Ee]l_e_girá[ns]?_i') + #4
lema('[Ee]l_i_minad[ao]s?_') + #3
lema('[Ee]lectrohidr_á_ulic[ao]s?_a') + #0
lema('[Ee]lectromagn_é_tic[ao]s?_e') + #3
lema('[Ee]legir_á_[ns]?_a') + #5
lema('[Ee]levad_í_sim[ao]s?_i') + #0
lema('[Ee]mblem_á_tic(?:as|os?)_a') + #8
lema('[Ee]mit(?:ir|)_í_a[ns]?_i') + #23
lema('[Ee]mit_í_a[ns]?_i') + #21
lema('[Ee]mitir_á_[ns]?_a') + #3
lema('[Ee]mp_i_eza[ns]?_') + #5
lema('[Ee]mp_r_esari(?:os?|al)_') + #2
lema('[Ee]mpatar_í_a[ns]?_i') + #1
lema('[Ee]mpe_z_ar(?:on|)_s') + #1
lema('[Ee]mpe_zó__(?:s[oó]|zo)') + #69
lema('[Ee]mpezar_í_a[ns]?_i') + #2
lema('[Ee]mpie_c_e[ns]?_z') + #9
lema('[Ee]mpie_z_a[ns]?_s') + #2
lema('[Ee]mprend_í_a[ns]?_i') + #0
lema('[Ee]mprender_á_[ns]?_a') + #0
lema('[Ee]mular_í_a[ns]?_i') + #2
lema('[Ee]n don_d_e_') + #2
lema('[Ee]n_é_rgic(?:[ao]s|amente)_e') + #3
lema('[Ee]n_ó_log[ao]s?_o') + #2
lema('[Ee]namorad_í_sim[ao]s?_i') + #1
lema('[Ee]nc_o_ntraba[ns]?_ue') + #31
lema('[Ee]ncargar_í_a[ns]?_i') + #1
lema('[Ee]nco_g_(?:e[nr]?|imiento|í)_j') + #6
lema('[Ee]ncont_r_ar_') + #48
lema('[Ee]ncontrar_í_a(?:[ns]?|mos)_i') + #4
lema('[Ee]ncubr(?:ir|)_í_a[ns]?_i') + #0
lema('[Ee]nfrent_á_r[mts]el[aeo]s?_a') + #0
lema('[Ee]nfrentar_s_e(?:lo|)_c') + #0
lema('[Ee]nfrentar_í_a[ns]?_i') + #7
lema('[Ee]ngre_í_d[ao]s?_i') + #7
lema('[Ee]nlazar_s_e(?:lo|)_c') + #0
lema('[Ee]nojad_í_sim[ao]s?_i') + #0
lema('[Ee]ntalp_í_as?_i') + #8
lema('[Ee]ntend_í_(?:a[ns]?|)_i') + #3
lema('[Ee]ntender_á_[ns]?_a') + #1
lema('[Ee]ntender_í_a(?:[ns]?|mos)_i') + #3
lema('[Ee]nto_n_ces_') + #24
lema('[Ee]ntr_e_ (?:l[ao]s|otros)_é') + #2
lema('[Ee]ntr_e_gad[ao]s?_a') + #8
lema('[Ee]ntr_e_vista(?:s?|d[ao]s?)_') + #7
lema('[Ee]ntrar_í_a[ns]?_i') + #0
lema('[Ee]ntreg_á_r[mts]el[aeo]s?_a') + #6
lema('[Ee]ntregar_í_a[ns]?_i') + #2
lema('[Ee]nv_i_ad[ao]s?_í') + #2
lema('[Ee]nv_í_o_i', pre='(?:[Dd]e|[Ee]l|[Uu]n|[Cc]ada) ') + #9
lema('[Ee]pis_o_dios?_i') + #4
lema('[Ee]pis_ó_dic[ao]s?_o') + #6
lema('[Ee]rr_ó_neamente_o') + #47
lema('[Ee]sc_é_nic[ao]s?_e') + #51
lema('[Ee]scalar_í_a[ns]?_i') + #0
lema('[Ee]scas_í_sim[ao]s?_i') + #0
lema('[Ee]sco_g_(?:e[nr]?|erl[aeo]s?|erá|es|id[aeo]s?|iendo|ieron|imos)_j') + #13
lema('[Ee]sco_j_a[ns]?_g') + #1
lema('[Ee]scoger_á_[ns]?_a') + #1
lema('[Ee]scond_í_a[ns]?_i') + #2
lema('[Ee]scrib(?:ir|)_í_a[ns]?_i') + #14
lema('[Ee]scrib_í_a(?:[ns]?|mos)_i') + #12
lema('[Ee]scribir_á_[ns]?_a') + #0
lema('[Ee]scribir_á_[ns]?_a') + #0
lema('[Ee]sculp(?:ir|)_í_a[ns]?_i') + #1
lema('[Ee]scult_ó_ric[ao]s?_o') + #6
lema('[Ee]spec_í_fic(?:[ao]s|amente)_i') + #93
lema('[Ee]spec_í_fica_i', pre='(?:[Ee]s|[Mm][aá]s) ') + #11
lema('[Ee]spect_á_culos?_a') + #119
lema('[Ee]spont_á_ne(?:[ao]s|amente)_a') + #13
lema('[Ee]spor_á_dic(?:[ao]s|amente)_a') + #8
lema('[Ee]spor_á_dic[ao]_a') + #0
lema('[Ee]spr_í_nters?_i') + #54
lema('[Ee]squ_í__i') + #66
lema('[Ee]st_á_ndares_a') + #56
lema('[Ee]st_é__e', pre='(?:[Ss]e )') + #37
lema('[Ee]st_é_tic(?:[ao]s|amente)_e') + #7
lema('[Ee]st_é_tica_e', pre='(?:[Ll]a|[Uu]na|[Cc]on|[Dd]e|[Ee]n|[Mm]uy|[Ff]unción[Ff]orma|[Uu]nidad|y) ') + #5
lema('[Ee]st_ó_magos?_o') + #60
lema('[Ee]st_ú_pid(?:[ao]s?|amente)_u') + #7
lema('[Ee]stablec(?:er|)_í_a[ns]?_i') + #32
lema('[Ee]stablec_í_(?:a[ns]?|)_i') + #26
lema('[Ee]stablecer_s_e(?:lo|)_c') + #0
lema('[Ee]stablecer_á_[ns]?_a') + #2
lema('[Ee]stanter_í_as?_i') + #2
lema('[Ee]star_í_a(?:[ns]?|mos)_i') + #30
lema('[Ee]statu_i_d[Ao]s?_í') + #2
lema('[Ee]ster_e_otipos?_i') + #2
lema('[Ee]strat_é_gic(?:[ao]s|amente)_e') + #22
lema('[Ee]strat_é_gic[ao]_e') + #16
lema('[Ee]strenar_í_a[ns]?_i') + #6
lema('[Ee]stu_v_(?:[eo]|ieron|iese[ns]?|iera[ns]?)_b') + #31
lema('[Ee]val_ú_(?:a[ns]?|e[ns]?)_u') + #16
lema('[Ee]x_c_elentes?_') + #3
lema('[Ee]x_c_ept(?:o|uar)_') + #10
lema('[Ee]x_clui_d[ao]s?_luí') + #2
lema('[Ee]x_h_aust[ao]s?_') + #4
lema('[Ee]x_á_menes_a') + #17
lema('[Ee]xced_í_a[ns]?_i') + #2
lema('[Ee]xcelent_í_sim[ao]s?_i') + #13
lema('[Ee]xcept_ú_(?:a[ns]?|e[ns]?)_u') + #0
lema('[Ee]xclu_i_d[ao]s?_í') + #182
lema('[Ee]xclu_i_r(?:l[aeo]s?|se|)_í') + #1
lema('[Ee]xi__tos[ao]s?_s') + #51
lema('[Ee]xig_í_a[ns]?_i') + #8
lema('[Ee]xigir_á_[ns]?_a') + #2
lema('[Ee]xist_í_a[ns]?_i') + #54
lema('[Ee]xistir_á_[ns]?_a') + #1
lema('[Ee]xit_o_s(?:[ao]s?|amente)_ó') + #61
lema('[Ee]xitos_í_sim[ao]s?_i') + #0
lema('[Ee]xpand(?:ir|)_í_a[ns]?_i') + #1
lema('[Ee]xpel_í_a[ns]?_i') + #1
lema('[Ee]xpl_í_cit(?:[ao]s|amente)_i') + #31
lema('[Ee]xplicar_í_a[ns]?_i') + #1
lema('[Ee]xpondr_á_[ns]?_a') + #1
lema('[Ee]xt__endió_i') + #10
lema('[Ee]xten_sio_nes_ci[oó]') + #8
lema('[Ee]xtend_í_(?:a[ns]?|)_i') + #6
lema('[Ee]xtender_á_[ns]?_a') + #1
lema('[Ee]xtender_í_a[ns]?_i') + #0
lema('[Ee]xtens_í_sim[ao]s?_i') + #0
lema('[Ee]xtin__tos?_c') + #1
lema('[Ee]xtra_í_(?:a[ns]?|d[ao]s?)_i') + #124
lema('[Ee]xtra_í_d[ao]s?_i') + #123
lema('[Ee]xtra_ñ_[ao]_n') + #2
lema('[Ee]xtrater_r_estres?_') + #0
lema('[Ee]xtru_i_d[ao]s?_í') + #3
lema('[Ff]_r_ustrad[ao]s?_') + #6
lema('[Ff]_u_tbolistas?_ú') + #171
lema('[Ff]_á_cil(?:mente|)_a') + #105
lema('[Ff]_í_sicamente(?! esposta)_i') + #15
lema('[Ff]_ó_lic[ao]s?_o') + #3
lema('[Ff]acilitar_í_a[ns]?_i') + #1
lema('[Ff]allar_í_a[ns]?_i') + #1
lema('[Ff]allecer_á_[ns]?_a') + #0
lema('[Ff]als_í_sim[ao]s?_i') + #0
lema('[Ff]amos_í_sim[ao]s?_i') + #2
lema('[Ff]avorecer_á_[ns]?_a') + #0
lema('[Ff]eligres_í_as?_i') + #10
lema('[Ff]en_ó_menos_o') + #8
lema('[Ff]erreter_í_as?_i') + #19
lema('[Ff]ichar_í_a[ns]?_i') + #2
lema('[Ff]idel_í_sim[ao]s?_i') + #3
lema('[Ff]il_á_ntropos?_a') + #8
lema('[Ff]ilmar_í_a[ns]?_i') + #0
lema('[Ff]ilmograf_í_as?_i') + #115
lema('[Ff]ilud_í_sim[ao]s?_i') + #0
lema('[Ff]in_í_sim[ao]s?_i') + #1
lema('[Ff]inal_í_sim[ao]s?_i') + #7
lema('[Ff]inalizar_í_a[ns]?_i') + #5
lema('[Ff]ing_í_a[ns]?_i') + #0
lema('[Ff]irmar_í_a[ns]?_i') + #3
lema('[Ff]lorecer_á_[ns]?_a') + #1
lema('[Ff]lu_i_d[ao]s?_í') + #33
lema('[Ff]luct_ú_(?:a[ns]?|e[ns]?)_u') + #6
lema('[Ff]olcl_ó_ric[ao]s?_o') + #31
lema('[Ff]ora_j_id[ao]s?_g') + #0
lema('[Ff]ormar_í_a[ns]?_i') + #9
lema('[Ff]ort_í_sim[ao]s?_i') + #0
lema('[Ff]ot_ó_graf[ao]s?_') + #0
lema('[Ff]rigor_í_fic[ao]s?_i') + #12
lema('[Ff]ruter_í_as?_i') + #2
lema('[Ff]u_s_i(?:ón|ones|onó|ona[ns]?)_c') + #6
lema('[Ff]ue_r_zas?_') + #41
lema('[Ff]uer_o_n_ó') + #19
lema('[Ff]unda__d[ao]s?_da') + #7
lema('[Ff]undar_í_a[ns]?_i') + #0
lema('[Ff]utbol_í_stic(?:[ao]s|amente)_i') + #12
lema('[Ff]utbol_í_stic[ao]_i') + #49
lema('[Gg]_é_rmenes_e') + #7
lema('[Gg]anader_í_a_i') + #65
lema('[Gg]anar_í_a[ns]?_i') + #5
lema('[Gg]en_é_ric(?:[ao]s|amente)_e') + #5
lema('[Gg]en_é_tic[ao]s_e') + #3
lema('[Gg]en_é_ticamente(?! modificato)_e') + #4
lema('[Gg]eneral_í_sim[ao]s?_i') + #30
lema('[Gg]enial_í_sim[ao]s?_i') + #0
lema('[Gg]eod_é_sic[ao]s?_e') + #0
lema('[Gg]eogr_á_fic(?:[ao]s|amente)_a') + #25
lema('[Gg]erontolog_í_as?_i') + #1
lema('[Gg]inecolog_í_as?(?! (?:Ospedalieri|e (?:Ostetricia|Obstétrícia)))_i') + #11
lema('[Gg]olear_í_a[ns]?_i') + #0
lema('[Gg]rad_ú_(?:a[ns]|e[ns]?)_u') + #19
lema('[Gg]raduar_s_e(?:lo|)_c') + #1
lema('[Gg]ran_ _partido_') + #1
lema('[Gg]rav_í_sim[ao]s?_i') + #3
lema('[Gg]rupo_s__', pre='[Ll]os ') + #101
lema('[Gg]u_i_ad[ao]s?_í') + #3
lema('[Gg]uap_í_sim[ao]s?_i') + #1
lema('[Gg]uarder_í_as?_i') + #7
lema('[Gg]uitar_r_as?_') + #15
lema('[Gg]ustar_í_a[ns]?_i') + #7
lema('[Hh]_á_bil(?:es|mente)_a') + #9
lema('[Hh]_á_bil_a', pre='(?:[Ee]s|[Ee]ra|[Ff]ue) ') + #0
lema('[Hh]_í_gados?_i') + #13
lema('[Hh]_ú_med[ao]s?_u') + #50
lema('[Hh]a_ll_(?:adas|ados?|ando|arse|éis)_y') + #11
lema('[Hh]ab_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #0
lema('[Hh]ab_é_r[mts]el[aeo]s?_e') + #5
lema('[Hh]ab_í_a(?:n|mos)_i') + #163
lema('[Hh]aber_s_e(?:lo|)_c') + #1
lema('[Hh]abr_í_as?_i') + #22
lema('[Hh]ac_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #2
lema('[Hh]acer_s_e(?:lo|)_c') + #19
lema('[Hh]allar_í_a(?:[ns]?|mos)_i') + #0
lema('[Hh]ect_á_reas?_a') + #69
lema('[Hh]elic_ó_pteros?_o') + #60
lema('[Hh]eredit_a_ri[ao]s?_á') + #16
lema('[Hh]ermos_í_sim[ao]s?_i') + #0
lema('[Hh]eterog_é_ne[ao]s?_e') + #12
lema('[Hh]ialur_ó_nic[ao]s?_o') + #0
lema('[Hh]ic_i_eron_') + #6
lema('[Hh]idr_á_ulic[ao]s?_a') + #17
lema('[Hh]idr_ó_genos?_o') + #28
lema('[Hh]idroel_é_ctric[ao]s?_e') + #19
lema('[Hh]idrogr_á_fic[ao]s?_a') + #23
lema('[Hh]idrograf_í_as?_i') + #79
lema('[Hh]ig_ié_nic[ao]s?_(?:ie|[eé])') + #13
lema('[Hh]iper_ví_nculos?_(?: v[ií]|vi)') + #1
lema('[Hh]ipn_ó_tic[ao]s?_o') + #1
lema('[Hh]ipod_é_rmic[ao]s?_e') + #1
lema('[Hh]ipot_é_tic[ao]s?_e') + #3
lema('[Hh]ispa_noamé_rica_(?:noam|oamé|ñoamé)') + #0
lema('[Hh]istolog_í_as?_i') + #10
lema('[Hh]o_mó_nim[ao]s?_(?:mo|n[oó])') + #90
lema('[Hh]oland_e_s[ae]s_é') + #2
lema('[Hh]ologr_á_fic[ao]s?_a') + #6
lema('[Hh]om_ó_nim[ao]s?_o') + #44
lema('[Hh]onr__os[ao]s?_r') + #3
lema('[Hh]onrar_í_a[ns]?_i') + #3
lema('[Hh]or_ó_scopos?_o') + #3
lema('[Hh]u_i_(?:r(?:l[aeo]s?|se|)|d[ao]s?)_í') + #117
lema('[Hh]u_i_d[ao]s?_í') + #104
lema('[Hh]umor_í_stic(?:[ao]s|amente)_i') + #7
lema('[Hh]umor_í_stic[ao]_i') + #34
lema('[Hh]umor_í_stic[ao]s?_') + #0
lema('[Hh]und(?:ir|)_í_a[ns]?_i') + #0
lema('[Hh]urac_a_nes_á') + #3
lema('[Ii]_m_perceptible_n') + #0
lema('[Ii]_m_perfecto_n') + #0
lema('[Ii]_m_pertinencia_n') + #1
lema('[Ii]_m_plementaron_n') + #0
lema('[Ii]_m_popular_n') + #0
lema('[Ii]_m_portando_n') + #2
lema('[Ii]_m_portantes_n') + #0
lema('[Ii]_m_pulso_n') + #1
lema('[Ii]_mpresió_n_(?:npre[sc]i[oó]|mpreci[oó]|mpresio)') + #14
lema('[Ii]_n_mortal(?:es|idad)_m') + #4
lema('[Ii]deol_ó_gic(?:[ao]s|amente)_o') + #9
lema('[Ii]diom_á_tic[ao]s?_') + #0
lema('[Ii]leg_í_tim(?:as?|os?|amente)_i') + #43
lema('[Ii]lustr_í_sim[ao]s?_i') + #10
lema('[Ii]m_a_gen_á') + #143
lema('[Ii]m_portan_tes?_(?:ortan|porta)') + #15
lema('[Ii]mbu_i_d[Ao]s?_í') + #2
lema('[Ii]mp_idié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_edie') + #0
lema('[Ii]mpedir_á_[ns]?_a') + #0
lema('[Ii]mperar_í_a[ns]?_i') + #1
lema('[Ii]mpl_í_cit(?:[ao]s|amente)_i') + #6
lema('[Ii]mplicar_í_a[ns]?_i') + #0
lema('[Ii]mpondr_á_[ns]?_a') + #0
lema('[Ii]mportant_í_sim[ao]s?_i') + #1
lema('[Ii]mportar_í_a[ns]?_i') + #2
lema('[Ii]mprim(?:ir|)_í_a[ns]?_i') + #0
lema('[Ii]n_clui_d[ao]s?_luí') + #1
lema('[Ii]n_i_cia(?:[rlns]|les|tivas?|lmente|ría[ns]?|ron|ndo|d[ao]s?|ción|ciones|)_') + #127
lema('[Ii]n_j_erencias?_g') + #28
lema('[Ii]n_s_pirado_') + #1
lema('[Ii]n_s_talaci(?:ón|ones)_') + #2
lema('[Ii]n_s_tancias?_') + #2
lema('[Ii]n_s_titu(?:ye|y[oó]|ción|ciones|id[ao]s?)_') + #3
lema('[Ii]n_struccio_nes_s?trucció') + #2
lema('[Ii]nal_á_mbric[ao]s?_a') + #22
lema('[Ii]nclu_i_d[ao]s?_í') + #319
lema('[Ii]nclu_i_r(?:l[aeo]s?|se|)_í') + #5
lema('[Ii]nclu_i_r_í') + #3
lema('[Ii]nclu_i_ría[ns]?_í') + #0
lema('[Ii]nclu_í_a[ns]?_i') + #301
lema('[Ii]ncluir_á_[ns]?_a') + #7
lema('[Ii]ncluir_í_a[ns]?_i') + #4
lema('[Ii]ncon_s_ciencias?_') + #3
lema('[Ii]ncon_s_cientes?_') + #20
lema('[Ii]ncon_sc_ientes?_[sc]') + #32
lema('[Ii]ncorporar_s_e(?:lo|)_c') + #0
lema('[Ii]ncre_í_ble(?:s|mente)_i') + #18
lema('[Ii]ncre_í_blemente_i') + #7
lema('[Ii]nde__pendencia_n') + #1
lema('[Ii]ndepend__encias?_i') + #2
lema('[Ii]ndic_ó_ que_o') + #17
lema('[Ii]ndivid_u_os_') + #1
lema('[Ii]nequ_í_voc(?:[ao]s|amente)_i') + #1
lema('[Ii]nflu_i_dos?_í') + #12
lema('[Ii]nfluir_á_[ns]?_a') + #0
lema('[Ii]nform_á_ticos?(?!\.com)_a') + #15
lema('[Ii]nfrac_c_ión_') + #1
lema('[Ii]ngen_i_erías?_') + #7
lema('[Ii]ngresar_í_a[ns]?_i') + #0
lema('[Ii]nic_i_ativas?_') + #3
lema('[Ii]nmiscu_i_d[ao]s?_í') + #1
lema('[Ii]nmo_v_iliz(?:[oó]|a(?:r?|r(?:l[aeo]s?|nos?)|d[ao]s?|ndo|ción|dor))_b') + #9
lema('[Ii]nscrib(?:ir|)_í_a[ns]?_i') + #0
lema('[Ii]nsin_ú_(?:a[ns]?|e[ns]?)_u') + #8
lema('[Ii]nsist(?:ir|)_í_a[ns]?_i') + #3
lema('[Ii]nspirad_í_sim[ao]s?_i') + #0
lema('[Ii]nspirar_í_a[ns]?_i') + #0
lema('[Ii]nstant_á_ne(?:[ao]s|amente)_a') + #6
lema('[Ii]nstant_á_ne[ao]_a') + #16
lema('[Ii]nstitu_i_d[ao]s?_í') + #21
lema('[Ii]nstru_i_d[ao]s?_í') + #23
lema('[Ii]nt_er_pretad[ao]s?_re') + #15
lema('[Ii]nt_é_rpretes_e', pre='(?:[AaEe]l|[Uu]na?|[Ll][ao]s|[Pp]or|[Vv]ari[ao]s|[Ff]amos[ao]s?|[Aa]rtistas?|[Dd]estacad[ao]s?|[Oo]tr[ao]s?|[Mm]ejor(?:es|)|[Ee]st[ao]s?|[Mm]uch[ao]s?|[Cc]uy[ao]s?|[Aa]lgun[ao]s|[Aa]lgún|[Aa]lguna|[Cc]onocid[ao]s?|[Ss]us?|[0-9]+|[Pp]rimer|[Gg]ran|[Cc]on) ') + #57
lema('[Ii]nte__grad[ao]s?_n') + #0
lema('[Ii]nte_r_pret[oó]_') + #11
lema('[Ii]nte_r_preta[ns]?_') + #4
lema('[Ii]nte_r_pretaba[ns]?_') + #0
lema('[Ii]nte_r_pretaciones_') + #0
lema('[Ii]nte_r_pretación_') + #7
lema('[Ii]nte_r_pretad[ao]s?_') + #30
lema('[Ii]nte_r_pretando_') + #9
lema('[Ii]nte_r_pretar(?:l[ao]s?|se|[aá]|ía[ns]?|ron|)_') + #12
lema('[Ii]nteligent_í_sim[ao]s?_i') + #0
lema('[Ii]nteresar_í_a[ns]?_i') + #1
lema('[Ii]nterp_r_et(?:es?|ad[ao]s?)_') + #6
lema('[Ii]ntervendr_á_[ns]?_a') + #0
lema('[Ii]ntroducir_á_[ns]?_a') + #0
lema('[Ii]ntu_i_d[ao]s?_í') + #0
lema('[Ii]nvad(?:ir|)_í_a[ns]?_i') + #3
lema('[Ii]nven_c_ibles?_s') + #3
lema('[Ii]nvertir_á_[ns]?_a') + #2
lema('[Ii]nvestigaci_ón|investigaciones]]__[óo]n\]\]es') + #0
lema('[Ii]nvolucrar_í_a[ns]?_i') + #1
lema('[Ii]r_ó_nic(?:[ao]s|amente)_o') + #9
lema('[Jj]_o_ven_ó') + #251
lema('[Jj]_ó_venes_o') + #237
lema('[Jj]ap_oné_s_óne') + #1
lema('[Jj]ard_í_n [Bb]otánico_i') + #12
lema('[Jj]esu_í_tic[ao]s?_i') + #19
lema('[Jj]ovenc_í_sim[ao]s?_i') + #2
lema('[Jj]oyer_í_as?_i') + #17
lema('[Jj]uda_í_smo_i') + #98
lema('[Jj]ueg_u_e[ns]?_') + #10
lema('[Jj]ugar_í_a[ns]?_i') + #26
lema('[Jj]ur_í_dic(?:os|amente)_i') + #6
lema('[Jj]ur_í_dicas(?!\.(?:com|unam\.mx))_i') + #14
lema('[Ll]_a_ (?:2a|BBC|Bandera|CIA|Ciudad|Confitería|Copa|Cumbre|Escuela|España|Familia|Fuerza|Isla|MLB|Mancomunidad|Nueva|Parada|Plaza|República|SFP|Sección|Serie|Siderurgia|Sinfónica|Soledad|UEFA|accesibilidad|amplitud|base|bebida|caja|ciudad|compositora|compra|corporación|delincuencia|derecha|derrota|designación|dificultad|discográfica|década|escuela|etiqueta|familia|fecha|formación|fuente|historia|iglesia|imagen|isla|justicia|medicina|más segura|música|normalización|nueva|oposición|organización|otra|pantalla|película|población|poesía|posibilidad|presidenta|primera|producción|promoción|provincia|prueba|psiquiatría|región|reina|revista|secuela|serranía|señorita|situación|sociedad|séptima|virgen|zona|única)_s') + #6
lema('[Ll]_a_s (?:Marquesas|Reducciones|SS|Sombras|\(muchas|arcadas|batallas|características|casas|charofitas|ciudades|colecciones|costas|críticas|dehesas|diferencias|doctrinas|dos puertas|entonces todopoderosa|escenas|especies|espiguillas|esporas|faldas|flores|fronteras|frutas|fuentes|fuerzas|hembras|hojas|indicaciones|inflorescencias|iniciales|inmunoglobulinas|islas|lenguas|lesbianas|leyes|listas|manchas|masas|mayores|mesas|mezquitas|misiones|mulas|negociaciones|normas|novelizaciones|nubes|nuevas|obras|orillas|películas|personas|posesiones|prematuras|prescriptivas|primeras|proximas|proximidades|puntas|raíces|regiones|respuestas|semifinales|sierras|siguientes|tierras|torturas|traducciones|ubicaciones|víctimas|yemas|zonas|órdenes)_') + #15
lema('[Ll]_o_s (?:Agustinos|Caballeros|EE\.UU\.|Llanos|Mártires|Play offs|Reyes|Vertebrados|acompañantes|albores|ascensores|aumentos|años|barrios|bordes|casos|cetáceos|chicos|compañeros|críticos|cupones|cursos|descendientes|dialectos|enviados|episodios|extremos|ganadores|gemelos|grupos|hechiceros|hermanos|hijos|ingenieros|integrantes|intérpretes|investigadores|juegos|lados|lusitanos|machos|memorandos|monos|muchos|muertos|musicales|municipios|negativos|niños|nuevos|ojos|otros|parches|primeros|problemas|programas|pueblos|rebeldes|republicanos|restos|ríos|sacerdotes|seres|siete minutos|siglos|singles|sostenedores|temas|trabajos|trabajadores|tricomas|troncos|viejos)_') + #11
lema('[Ll]_á_piz_a') + #39
lema('[Ll]_í_deres_i') + #172
lema('[Ll]_í_quenes_i') + #8
lema('[Ll]a n_ó_mina(?! (?:di|al|a la|dubia|en|con))_o') + #12
lema('[Ll]a_ _misma_') + #2
lema('[Ll]a_s_ [aá]reas_') + #8
lema('[Ll]a_s_ acciones_') + #13
lema('[Ll]a_s_ actividades_') + #21
lema('[Ll]a_s_ afueras_') + #13
lema('[Ll]a_s_ autoridades_') + #40
lema('[Ll]a_s_ bandas_') + #18
lema('[Ll]a_s_ bases_') + #21
lema('[Ll]a_s_ calles_') + #43
lema('[Ll]a_s_ canciones_') + #40
lema('[Ll]a_s_ caracter[ií]sticas_') + #17
lema('[Ll]a_s_ cercanías_') + #18
lema('[Ll]a_s_ ciencias_') + #13
lema('[Ll]a_s_ ciudades_') + #72
lema('[Ll]a_s_ compañ[ií]as_') + #13
lema('[Ll]a_s_ comunidades_') + #11
lema('[Ll]a_s_ condiciones_') + #18
lema('[Ll]a_s_ costas_') + #15
lema('[Ll]a_s_ cuales_') + #79
lema('[Ll]a_s_ células_') + #17
lema('[Ll]a_s_ diferencias_') + #16
lema('[Ll]a_s_ diferentes_') + #15
lema('[Ll]a_s_ distintas_') + #6
lema('[Ll]a_s_ divisiones_') + #24
lema('[Ll]a_s_ décadas_') + #8
lema('[Ll]a_s_ elecciones_') + #58
lema('[Ll]a_s_ empresas_') + #29
lema('[Ll]a_s_ especies_') + #17
lema('[Ll]a_s_ estaciones_') + #18
lema('[Ll]a_s_ estructuras_') + #7
lema('[Ll]a_s_ familias_') + #20
lema('[Ll]a_s_ fechas_') + #22
lema('[Ll]a_s_ fiestas_') + #28
lema('[Ll]a_s_ figuras_') + #11
lema('[Ll]a_s_ filas_') + #23
lema('[Ll]a_s_ formas_') + #12
lema('[Ll]a_s_ fuerzas_') + #61
lema('[Ll]a_s_ funciones_') + #15
lema('[Ll]a_s_ grandes_') + #44
lema('[Ll]a_s_ ideas_') + #22
lema('[Ll]a_s_ iglesias_') + #16
lema('[Ll]a_s_ im[aá]genes_') + #14
lema('[Ll]a_s_ industrias_') + #10
lema('[Ll]a_s_ inmediaciones_') + #11
lema('[Ll]a_s_ islas_') + #61
lema('[Ll]a_s_ lenguas_') + #9
lema('[Ll]a_s_ letras_') + #14
lema('[Ll]a_s_ leyes_') + #20
lema('[Ll]a_s_ listas_') + #52
lema('[Ll]a_s_ localidades_') + #15
lema('[Ll]a_s_ líneas_') + #24
lema('[Ll]a_s_ manos_') + #17
lema('[Ll]a_s_ mejores_') + #14
lema('[Ll]a_s_ minas_') + #10
lema('[Ll]a_s_ mismas_') + #25
lema('[Ll]a_s_ montañas_') + #12
lema('[Ll]a_s_ mujeres_') + #42
lema('[Ll]a_s_ nuevas_') + #20
lema('[Ll]a_s_ obras_') + #64
lema('[Ll]a_s_ orillas_') + #8
lema('[Ll]a_s_ otras_') + #24
lema('[Ll]a_s_ palabras_') + #27
lema('[Ll]a_s_ partes_') + #19
lema('[Ll]a_s_ pel[ií]culas_') + #21
lema('[Ll]a_s_ personas_') + #26
lema('[Ll]a_s_ plantas_') + #10
lema('[Ll]a_s_ poblaciones_') + #20
lema('[Ll]a_s_ posibilidades_') + #5
lema('[Ll]a_s_ posiciones_') + #16
lema('[Ll]a_s_ primeras_') + #54
lema('[Ll]a_s_ principales_') + #42
lema('[Ll]a_s_ provincias_') + #38
lema('[Ll]a_s_ redes_') + #14
lema('[Ll]a_s_ regiones_') + #32
lema('[Ll]a_s_ relaciones_') + #31
lema('[Ll]a_s_ revistas_') + #11
lema('[Ll]a_s_ ruinas_') + #11
lema('[Ll]a_s_ rutas_') + #8
lema('[Ll]a_s_ semifinales_') + #39
lema('[Ll]a_s_ series_') + #74
lema('[Ll]a_s_ sierras_') + #5
lema('[Ll]a_s_ siguientes_') + #69
lema('[Ll]a_s_ sociedades_') + #5
lema('[Ll]a_s_ temporadas_') + #18
lema('[Ll]a_s_ teor[ií]as_') + #4
lema('[Ll]a_s_ tierras_') + #9
lema('[Ll]a_s_ tropas_') + #19
lema('[Ll]a_s_ unidades_') + #9
lema('[Ll]a_s_ universidades_') + #10
lema('[Ll]a_s_ ventas_') + #4
lema('[Ll]a_s_ vías_') + #16
lema('[Ll]a_s_ últimas_') + #18
lema('[Ll]anzar_í_a[ns]?_i') + #5
lema('[Ll]argu_í_sim[ao]s?_i') + #1
lema('[Ll]as [uú]ltima_s__') + #69
lema('[Ll]eg_í_tim(?:as|os|amente)_i') + #18
lema('[Ll]encer_í_as?_i') + #17
lema('[Ll]exicolog_í_as?_i') + 
lema('[Ll]iger_í_sim[ao]s?_i') + #0
lema('[Ll]inf_á_tic[ao]s?_a') + #6
lema('[Ll]lam_a_d[ao]s?_') + #38
lema('[Ll]lamar_s_e(?:lo|)_c') + #0
lema('[Ll]lamar_í_a(?:[ns]?|mos)_i') + #6
lema('[Ll]legar_í_a[ns]?_i') + #13
lema('[Ll]len_í_sim[ao]s?_i') + #0
lema('[Ll]lev_á_r[mts]el[aeo]s?_a') + #8
lema('[Ll]leva(rá|) a_ _cabo_') + #13
lema('[Ll]levar_í_a[ns]?_i') + #10
lema('[Ll]ocalizar_s_e(?:lo|)_c') + #0
lema('[Ll]ograr_í_a[ns]?_i') + #8
lema('[Ll]uchar_í_a[ns]?_i') + #0
lema('[Mm]_u_sical_ú') + #219
lema('[Mm]_u_sicales_ú') + #15
lema('[Mm]_utua_mente_(?:útual?|utual)') + #27
lema('[Mm]_á_gic(?:[ao]s|amente)_a') + #28
lema('[Mm]_á_nager_a', pre='(?:[Ee]l|[Dd]el?|[Ll]a|[Uu]n|[Ss]u|nuevo|antiguo|anterior|próximo) ') + #732
lema('[Mm]_á_rgenes_a') + #22
lema('[Mm]_á_s (?:accesible|agradable|alegre|amigable|artículo|asistencia|ataque|casilla|célebre|cosa|década|dominante|edificio|ejemplo|emocionante|estable|experiencia|fecha|fiable|fuerte|grande|hilarante|humilde|ilustre|importante|impresionante|minimalista|minutos|muerte|noble|noche|palabra|película|pista|problema|prueba|realista|reciente|resaltante|resistencia|salvaje|sociable|suave|tarde|temporada|vía|victoria|visible|visita|vuelta|vulnerable)s?\\b_a') + #1803
lema('[Mm]_á_s (?:actual|afinidad|calor|espectacular|fértil|gol|letal|posibilidad|principal|real|regular|septentrional|usual)(?:es|)\\b_a') + #136
lema('[Mm]_á_s (?:adelante|atrás|dos)\\b_a') + #152
lema('[Mm]_á_s (?:alt|amarg|amig|citad|competitiv|desconocid|distintiv|envejecid|equilibrad|ergonómic|insegur|lujos|notad|óptim|pequeñ|poblad|prolífic|rocker|select|sosegad|vendid|veteran|vigoros|violent|viv)[ao]s?\\b_a') + #503
lema('[Mm]_á_s (?:cambi|campeonat|dat|equip|fot|minut|reconocimient|refuerz|sencill|tir|trabaj|títul)os?\\b_a') + #137
lema('[Mm]_á_scaras?_a', pre='(?:[Ll]as?|[Uu]nas?|[Ss]us?) ') + #389
lema('[Mm]_ás allá__(?:as all[aá]|ás alla)') + #146
lema('[Mm]_é_dicos_e', pre='(?:[Ll]os|[Ss]us|[Uu]nos) ') + #6
lema('[Mm]_é_todos_e') + #26
lema('[Mm]_éto_dos?_etó') + #3
lema('[Mm]_í_nimamente_i') + #12
lema('[Mm]_ú_ltiple (?:accidente|álbumes|asesinato|cambio|campeón|con|de |instrumentos|interpretación|mediante|ocasiones|por|productores|que|significa|variantes|vol[uú]menes|y )_u') + #3
lema('[Mm]_ú_ltiples?_u', pre='\\b(?:Monitores|en|por|creado|normales|reclutando|[Cc]opias| de|Tiene|esclerosis|[Ee]lectrica) ', xpre=['Pénétrations ']) + #9
lema('[Mm]a_m_posteros_n') + #1
lema('[Mm]a_m_postería_n') + #13
lema('[Mm]a_mposterí_a_nposteri') + #1
lema('[Mm]aci_z_os?_c') + #1
lema('[Mm]acrosc_ó_pic[ao]s?_o') + #4
lema('[Mm]agn_í_fica_i', pre='(?:una (?:banda|vista|forma|defensa natural|escritora)| (?:durante|a) la|de forma|sólida y) ') + #2
lema('[Mm]al_í_sim[ao]s?_i') + #2
lema('[Mm]am_í_fer[ao]s?_i') + #60
lema('[Mm]anten_í_a[ns]?_i') + #14
lema('[Mm]antendr_á_[ns]?_a') + #6
lema('[Mm]antendr_í_a[ns]?_i') + #5
lema('[Mm]archar_í_a[ns]?_i') + #0
lema('[Mm]asoner_í_as?_i') + #29
lema('[Mm]atem_á_tic(?:os|amente)(?!\.unmsm)_a') + #7
lema('[Mm]ayor_í_as?_i') + #216
lema('[Mm]e_n_sajes?_') + #1
lema('[Mm]ec_á_nic(?:[ao]s|amente)_a') + #14
lema('[Mm]ecatr_ó_nicas?_o') + #3
lema('[Mm]edi_a_nte_e') + #5
lema('[Mm]ediod_í_as?_i') + #55
lema('[Mm]edir_á_[ns]?_a') + #2
lema('[Mm]egafon_í_as?_i') + #3
lema('[Mm]elodram_á_tic[ao]s?_a') + #4
lema('[Mm]ensajer_í_as?_i') + #12
lema('[Mm]ercader_í_as?_i') + #9
lema('[Mm]ercanc_í_as?_i') + #71
lema('[Mm]ere_ció__scio') + #0
lema('[Mm]etereol_ó_gic[ao]s?_o') + #1
lema('[Mm]exican_í_sim[ao]s?_i') + #4
lema('[Mm]ie_m_bros?_n') + #5
lema('[Mm]ientra_s__') + #56
lema('[Mm]iner_í_as?_i') + #106
lema('[Mm]inusv_á_lid[ao]s?_a') + #2
lema('[Mm]ism_í_sim[ao]s?_i') + #19
lema('[Mm]o_n_struos?_') + #8
lema('[Mm]o_nstru_o_unstr') + #17
lema('[Mm]oment_á_ne(?:[ao]s|amente)_a') + #6
lema('[Mm]onol_í_tic[ao]s?_i') + #4
lema('[Mm]orir_á_[ns]?_a') + #12
lema('[Mm]orir_í_a[ns]?_i') + #14
lema('[Mm]u__rieron_e') + #5
lema('[Mm]u_n_icipios?__') + #4
lema('[Mm]uch_í_sim[ao]s?_i') + #10
lema('[Mm]ultiprop_ó_sitos?_o') + #4
lema('[Mm]urci_é_lagos?_e') + #40
lema('[Mm]uri_á_tic[ao]s?_a') + #0
lema('[Mm]usic_ó_log[ao]s?_o') + #81
lema('[Mm]usulm_á_n_á') + #6194
lema('[Nn]_á_useas_a') + #182
lema('[Nn]_áu_frag[ao]s?_aú') + #14
lema('[Nn]acional_ de_ Yosemite\]\]_') + #0
lema('[Nn]anotecnolog_í_as?_i') + #6
lema('[Nn]arcotr_á_ficos?_a') + #33
lema('[Nn]ari_c_es_[zs]') + #1
lema('[Nn]ecesitar_í_a(?:[ns]?|mos)_i') + #4
lema('[Nn]ecrol_ó_gic[ao]s?_o') + #16
lema('[Nn]ecrolog_í_as?_i') + #5
lema('[Nn]egoc_i_aci(?:ón|ones)_') + #2
lema('[Nn]eocl_á_sic[ao]s?_a') + #54
lema('[Nn]eum_á_tic[ao]s?_a') + #83
lema('[Nn]eur_á_lgic[ao]s?_a') + #3
lema('[Nn]euroanatom_í_as?_i') + #6
lema('[Nn]europsicolog_í_as?_i') + #5
lema('[Nn]i_ _siquiera_') + #5
lema('[Nn]icarag_ü_enses_u') + #5
lema('[Nn]inf_ó_manas?_o') + #3
lema('[Nn]itr_ó_genos?_o') + #5
lema('[Nn]iv_e_l(?:es|)_é') + #2
lema('[Nn]oqu_eó__io') + #0
lema('[Nn]orirland_é_s_e') + #2
lema('[Nn]orteam_é_rica(?!\]\])_e') + #137
lema('[Nn]otar_í_an_i') + #0
lema('[Nn]ov_í_sim[ao]s?_i') + #9
lema('[Nn]uest_r_o_') + #3
lema('[Nn]um_é_ric(?:[ao]s|amente)_e') + #3
lema('[Oo]_b_t(?:en(?:er|gan?|dr[ií]a[ns]?)|ienen?|uvo)_p') + #5
lema('[Oo]_b_tenido_p') + #0
lema('[Oo]bst_á_culos?_a') + #47
lema('[Oo]bstru_i_d[ao]s?_í') + #2
lema('[Oo]bten(?:dr|)_í_a[ns]?_i') + #14
lema('[Oo]btendr_á_[ns]?_a') + #3
lema('[Oo]btendr_í_a(?:[ns]?|mos)_i') + #5
lema('[Oo]c_éano Í_ndico_(?:eano [iíIÍ]|éano [iIí])') + #29
lema('[Oo]casionar_í_a[ns]?_i') + #0
lema('[Oo]curr(?:ir|)_í_a[ns]?_i') + #6
lema('[Oo]curr_í_a[ns]?_i') + #5
lema('[Oo]currir_á_[ns]?_a') + #5
lema('[Oo]dontol_ó_gic[ao]s?_o') + #5
lema('[Oo]fend_í_a[ns]?_i') + #8
lema('[Oo]frec_í_a[ns]?_i') + #54
lema('[Oo]frecer_á_[ns]?_a') + #4
lema('[Oo]pon_í_a[ns]?_i') + #4
lema('[Oo]ptar_í_a[ns]?_i') + #0
lema('[Oo]r_i_gen_í') + #607
lema('[Oo]r_á_culos?_a') + #15
lema('[Oo]rdenar_í_a[ns]?_i') + #1
lema('[Oo]rg_á_nic(?:[ao]s|amente)_a') + #3
lema('[Oo]rgani_z_ad[ao]s?_s') + #1
lema('[Oo]rganizar_s_e(?:lo|)_c') + #0
lema('[Oo]riginal_í_sim[ao]s?_i') + #1
lema('[Oo]rtop_é_dic[ao]s?_e') + #1
lema('[Oo]torg_á_r[mts]el[aeo]s?_a') + #1
lema('[Oo]torrinolaringolog_í_as?_i') + #5
lema('[Pp]_e_rtenece[nrs]?_a') + #2
lema('[Pp]_ro_gramas?_or') + #2
lema('[Pp]_á_gina (?:[Ww]eb|oficial|del?)_a') + #1219
lema('[Pp]_á_ginas?_a', pre='(?:[Ll]as?)') + #2
lema('[Pp]_á_rrafos?_a') + #37
lema('[Pp]_é_rtigas?_e') + #3
lema('[Pp]_é_sim[ao]s?_e') + #10
lema('[Pp]_í_ldoras?_i') + #10
lema('[Pp]_ó_lvoras?_o') + #27
lema('[Pp]a_í_ses(?! Baixos)_i') + #553
lema('[Pp]ac_í_fic(?:as|os|amente)_i') + #14
lema('[Pp]ac_í_fico_i', pre='([Ee]l|[Dd]el) ') + #253
lema('[Pp]acient_í_sim[ao]s?_i') + #0
lema('[Pp]adec_í_a[ns]?_i') + #14
lema('[Pp]agar_í_a[ns]?_i') + #1
lema('[Pp]aisaj_í_stic(?:[ao]s?|amente)_i') + #9
lema('[Pp]aleogeograf_í_a_i') + #1
lema('[Pp]ar_á_lisis_a') + #16
lema('[Pp]araca_í_das?_i') + #4
lema('[Pp]arad_ó_jic(?:[ao]s|amente)_o') + #6
lema('[Pp]aran_o_ic[ao]s?_ó') + #4
lema('[Pp]arecer_s_e(?:lo|)_c') + #0
lema('[Pp]arecer_á_[ns]?_a') + #0
lema('[Pp]arente_s_cos?_z') + #6
lema('[Pp]arlanch_í_n_i') + #2
lema('[Pp]artic_i_par(?:on|)_') + #12
lema('[Pp]articip_ó_ (?:en|junto|como)_o') + #517
lema('[Pp]articipar_í_a[ns]?_i') + #9
lema('[Pp]as_sio_n_i[oó]', pre='of (?:the |)') + #4
lema('[Pp]as_á_r[mts]el[aeo]s?_a') + #1
lema('[Pp]asant_í_as?_i') + #5
lema('[Pp]asar_í_a[ns]?_i') + #22
lema('[Pp]atol_ó_gic[ao]s?_o') + #6
lema('[Pp]atolog_í_as_i') + #3
lema('[Pp]e_r_manece(?:[nr]|ría[ns]?|)_') + #3
lema('[Pp]e_s_ca[rs]?_z') + #4
lema('[Pp]edir_á_[ns]?_a') + #3
lema('[Pp]elear_s_e_z') + #0
lema('[Pp]elear_í_a[ns]?_i') + #0
lema('[Pp]equeñ_í_sim[ao]s?_i') + #1
lema('[Pp]er__iodista_d') + #2
lema('[Pp]er__iodo_d') + #0
lema('[Pp]er_imetró__(?:ímetr[oó]|imetro)', pre='[Ss]e(?: me| te| l[aeo]s?|) ') + #0
lema('[Pp]ercib(?:ir|)_í_a[ns]?_i') + #1
lema('[Pp]ercl_ó_ric[ao]s?_o') + #1
lema('[Pp]erder_á_[ns]?_a') + #5
lema('[Pp]erdurar_í_a[ns]?_i') + #1
lema('[Pp]eri_ó_dic(?:as|amente)_o', pre='\.edu') + #0
lema('[Pp]eriod_í_stic[ao]s?_i') + #44
lema('[Pp]ermane__ciendo_n') + #15
lema('[Pp]ermanec_í__i') + #0
lema('[Pp]ermanecer_á_[ns]?_a') + #5
lema('[Pp]ermanecer_í_a[ns]?_i') + #6
lema('[Pp]ermit(?:ir|)_í_a[ns]?_i') + #34
lema('[Pp]ermit_í__i') + #4
lema('[Pp]ermitir_á_[ns]?_a') + #9
lema('[Pp]ermitir_í_a[ns]?_i') + #7
lema('[Pp]erseguir_á_[ns]?_a') + #0
lema('[Pp]ersonal_í_sim[ao]s?_i') + #0
lema('[Pp]ersoner_í_as?_i') + #15
lema('[Pp]erten_e_cer(?:á[ns]?|ía[ns]?|)_') + #3
lema('[Pp]ertenecer_á_[ns]?_a') + #0
lema('[Pp]esquer_í_as?_i') + #2
lema('[Pp]ict_ó_ric[ao]s?_o') + #11
lema('[Pp]ing_ü_inos?_u') + #46
lema('[Pp]irater_í_as?_i') + #17
lema('[Pp]luric_é_ntric[ao]s?_e') + #0
lema('[Pp]neumatol_ó_gic[ao]s?_o') + #0
lema('[Pp]nuematolog_í_as?_i') + #0
lema('[Pp]od_í_amos_i') + #2
lema('[Pp]oder_í_o_i') + #27
lema('[Pp]odiatr_í_as?_i') + #0
lema('[Pp]odolog_í_a(?!\.cl)_i') + #1
lema('[Pp]odr_á_[ns]?_a') + #51
lema('[Pp]odr_í_a(?:[ns]?|mos)_i') + #103
lema('[Pp]ol_í_ticas_') + #0
lema('[Pp]ol_í_ticos(?!\.html)_i') + #124
lema('[Pp]olicl_í_nicas?_i') + #19
lema('[Pp]on_é_r[mts]el[aeo]s?_e') + #1
lema('[Pp]ondr_á_n_a') + #0
lema('[Pp]ondr_í_a(?:[ns]?|mos)_i') + #9
lema('[Pp]oner_s_e(?:lo|)_c') + #0
lema('[Pp]opular_í_sim[ao]s?_i') + #0
lema('[Pp]opulari_zó__(?:s[oó]|zo)') + #11
lema('[Pp]opurr_í__i') + #79
lema('[Pp]oqu_í_sim[ao]s?_i') + #0
lema('[Pp]or s_í so_l[ao]s?_(?:i s[oó]|í só)') + #370
lema('[Pp]or_ _ciento_') + #43
lema('[Pp]ort_á_til(?:es|)_a') + #134
lema('[Pp]ortug_ué_s_e') + #6
lema('[Pp]ose_í_a[ns]?_i') + #24
lema('[Pp]ose_í_d[ao]s?_i') + #27
lema('[Pp]oseer_á_[ns]?_a') + #0
lema('[Pp]osi_c_ionada_s') + #1
lema('[Pp]osi_c_ionamiento_s') + #1
lema('[Pp]osicionar_s_e(?:lo|)_c') + #0
lema('[Pp]r_a_cticar(?:se|lo|le|on|an|)_á') + #10
lema('[Pp]r_á_ctic(?:os|amente)_a') + #81
lema('[Pp]r_á_cticas de_a') + #20
lema('[Pp]r_á_cticas_a', pre='(?:[Ll]as|[Uu]nas|[Ss]us) ') + #12
lema('[Pp]r_é_stamo_e') + #216
lema('[Pp]r_ó_xim(?:[ao]s|amente)_o') + #115
lema('[Pp]re_s_enci(?:a[ns]?|[oó]|ar(?:[eé]|[aá][ns]?|ron))_s?c') + #13
lema('[Pp]refi__rieron_e') + #2
lema('[Pp]refi__rió_e') + #1
lema('[Pp]rehisp_á_nic[ao]s?_a') + #23
lema('[Pp]reparar_s_e(?:lo|)_c') + #0
lema('[Pp]resent_á_r[mts]el[aeo]s?_a') + #2
lema('[Pp]residir_á_[ns]?_a') + #0
lema('[Pp]residir_í_a[ns]?_i') + #19
lema('[Pp]restar_í_a[ns]?_i') + #0
lema('[Pp]resum(?:ir|)_í_a[ns]?_i') + #2
lema('[Pp]retend_í_a[ns]?_i') + #11
lema('[Pp]revalecer_á_[ns]?_a') + #0
lema('[Pp]reve_í_a[ns]?_i') + #0
lema('[Pp]ri_me_r[ao]s?_em') + #30
lema('[Pp]ri_n_cipal(?:es|mente|)_') + #43
lema('[Pp]rim_e_r[ao]s?_') + #4
lema('[Pp]rim_e_ras?_a', pre='(?:[Ll]as?|[Ss]us|[Uu]nas?|[Ee]n|[Dd]e|[Pp]or) ') + #3
lema('[Pp]rimar_i_a_', pre='(?:[Ee]scuelas?|formas?|[Ee]nseñanzas?|[Ee]ducación|[Ee]lecciones|[Ee]lección|[Aa]tención|Estudió) ') + #2
lema('[Pp]rimer_í_sim[ao]s?_i') + #5
lema('[Pp]rimi_c_ias?_s') + #0
lema('[Pp]ro_b_ad[ao]s?_v') + #27
lema('[Pp]ro_v_oca[ns]?_b') + #0
lema('[Pp]roceder_á_[ns]?_a') + #0
lema('[Pp]rodu_jo__ci[oó]') + #9
lema('[Pp]roduc(?:ir|)_í_a[ns]?_i') + #11
lema('[Pp]roducir_s_e(?:lo|)_c') + #0
lema('[Pp]roducir_á_[ns]?_a') + #3
lema('[Pp]roducir_í_a[ns]?_i') + #4
lema('[Pp]rofe_s_ional(?:es|)_c') + #16
lema('[Pp]rohib_í_a[ns]?_i') + #10
lema('[Pp]rol_í_fic(?:as|os?)_i') + #5
lema('[Pp]romet_í_(?:a[ns]?|)_i') + #5
lema('[Pp]romov_í_a[ns]?_i') + #1
lema('[Pp]romover_á_[ns]?_a') + #2
lema('[Pp]ropi_ó_nic[ao]s?_o') + #2
lema('[Pp]ropon_í_a[ns]?_i') + #4
lema('[Pp]ropondr_á_[ns]?_a') + #0
lema('[Pp]rot_é_sic[ao]s?_e') + #0
lema('[Pp]rotag_ó_nic[ao]s?_o') + #64
lema('[Pp]rote_g_(?:e[nr]?|emos|erl[aeo]s?|erse|erá[ns]?|ería[ns]?|id[aeo]s?|iendo|iera|ieron|iese|ió)_j') + #11
lema('[Pp]rote_í_nas?_i') + #69
lema('[Pp]roteg_í_a[ns]?_i') + #8
lema('[Pp]roteger_á_[ns]?_a') + #1
lema('[Pp]rove_í_a[ns]?_i') + #1
lema('[Pp]rove_í_d[ao]s?_i') + #6
lema('[Pp]roveer_á_[ns]?_a') + #2
lema('[Pp]roven_í_a[ns]?_i') + #54
lema('[Pp]rovi_sio_(?:nal(?:es|)|nes)_ci[oó]') + #31
lema('[Pp]s_í_quic[ao]s?_i') + #46
lema('[Pp]sicoanal_í_tic[ao]s?_i') + #6
lema('[Pp]sicol_ó_gic[ao]s_o') + #8
lema('[Pp]siqui_á_tric[ao]s?_a') + #19
lema('[Pp]u__dieron_e') + #15
lema('[Pp]ublicar_í_a[ns]?_i') + #1
lema('[Qq]u_eri_endo_ier') + #0
lema('[Qq]u_ie_n_ei') + #4
lema('[Qq]u_í_mic(?:[ao]s|amente)_i') + #18
lema('[Qq]ued_ó_ (?:sólo|sin|descubierto)_o') + #17
lema('[Qq]uedar_s_e(?:lo|)_c') + #1
lema('[Qq]uedar_í_a[ns]?_i') + #14
lema('[Qq]uer_í_amos_i') + #5
lema('[Qq]uer_í_amos_i') + #5
lema('[Qq]uincuag_é_sim[ao]s?_e') + #3
lema('[Qq]uir_ú_rgic[ao]s?_u') + #23
lema('[Qq]uis_o__ó') + #6
lema('[Qq]uiz_á_s_a') + #13
lema('[Rr]_á_pid(?:[ao]s|amente)_a') + #118
lema('[Rr]_é_plica_', pre='(?:[Uu]na|1) ') + #0
lema('[Rr]_í_e[ns]?_i', pre='(?:[Ss]e) ') + #12
lema('[Rr]_í_gida_i', pre='(?:hacer|una|Máscara|persona|cola|está) ') + #4
lema('[Rr]adiofon_í_as?_i') + #6
lema('[Rr]apid_í_sim[ao]s?_i') + #0
lema('[Rr]ar_í_sim[ao]s?_i') + #1
lema('[Rr]e__levantes?_e') + #0
lema('[Rr]e_hu_sa[ns]?_(?:hu|[uú])') + #170
lema('[Rr]e_presá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_gresa') + #0
lema('[Rr]e_s_pectiv[ao]s?_') + #5
lema('[Rr]e_s_ponde[ns]?_') + #2
lema('[Rr]e_s_pondió_') + #0
lema('[Rr]e_í_r_i') + #53
lema('[Rr]e_ú_ne[ns]?_u') + #155
lema('[Rr]e_ú_sa[ns]_u') + #2
lema('[Rr]eabrir_á_[ns]?_a') + #0
lema('[Rr]ealizar_s_e(?:lo|)_c') + #1
lema('[Rr]ealizar_í_a[ns]?_i') + #8
lema('[Rr]eanudar_s_e(?:lo|)_c') + #0
lema('[Rr]eap_are_c(?:e(?:[ns]?|r(?:a[ns]?|[áé]|ía[ns]?|))|ieron)_(?:ara|re)') + #0
lema('[Rr]eaparecer_á_[ns]?_a') + #1
lema('[Rr]earmar_í_a[ns]?_i') + #0
lema('[Rr]eca_í_d[ao]s?_i') + #2
lema('[Rr]ecaudar_í_a[ns]?_i') + #0
lema('[Rr]eci_b_(?:e|ió|[íI]a|ir[eé])_v') + #24
lema('[Rr]eci_b_id[ao]s?_v') + #5
lema('[Rr]eci_bió__(?:vi[oó]|bio)') + #24
lema('[Rr]eci_é_n_e') + #100
lema('[Rr]ecib(?:ir|)_í_a[ns]?_i') + #16
lema('[Rr]ecibir_á_[ns]?_a') + #7
lema('[Rr]ecibir_í_a[ns]?_i') + #2
lema('[Rr]eclu_i_d[ao]s?_í') + #11
lema('[Rr]eco_g_(?:e[nrs]?|erl[aeo]s?|erán|id[ao]s?|iendo|ieron|imiento|ió|í)_j') + #25
lema('[Rr]eco_g_e[ns]?_j') + #17
lema('[Rr]ecog_í_a[ns]?_i') + #10
lema('[Rr]ecoger_á_[ns]?_a') + #1
lema('[Rr]econ_s_truir(?:l[ao]s?|se)_') + #0
lema('[Rr]econciliar_s_e(?:lo|)_c') + #1
lema('[Rr]econoc_í_a[ns]?_i') + #22
lema('[Rr]econocer_á_[ns]?_a') + #0
lema('[Rr]econocid_í_sim[ao]s?_i') + #0
lema('[Rr]econocim_ie_ntos?_ei') + #2
lema('[Rr]econstru_i_d[ao]s?_í') + #13
lema('[Rr]econstru_i_r(?:l[aeo]s?|se|)_í') + #1
lema('[Rr]ecorr_í_a[ns]?_i') + #10
lema('[Rr]ecorrer_á_[ns]?_a') + #0
lema('[Rr]ecuperar_í_a[ns]?_i') + #0
lema('[Rr]ecurr(?:ir|)_í_a[ns]?_i') + #1
lema('[Rr]ecurrir_á_[ns]?_a') + #1
lema('[Rr]edistribu_i_d[ao]s?_í') + #1
lema('[Rr]edu_j_eron_ci') + #6
lema('[Rr]educir_s_e(?:lo|)_c') + #0
lema('[Rr]educir_á_[ns]?_a') + #1
lema('[Rr]eeditar_í_a[ns]?_i') + #0
lema('[Rr]eempla_zó__(?:s[oó]|zo)', pre='(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #26
lema('[Rr]eemplazar_í_a[ns]?_i') + #3
lema('[Rr]eenv_í_a[ns]?_i') + #8
lema('[Rr]ef_e_rencias?_') + #3
lema('[Rr]eferir_s_e(?:lo|)_c') + #0
lema('[Rr]efiner_í_as?_i') + #9
lema('[Rr]eflejar_í_a[ns]?_i') + #0
lema('[Rr]egad_í_os?_i') + #23
lema('[Rr]egir_á_[ns]?_a') + #3
lema('[Rr]egresar_í_a[ns]?_i') + #7
lema('[Rr]ei_m_preso_n') + #2
lema('[Rr]einventar_í_a[ns]?_i') + #0
lema('[Rr]ele_í_d[ao]s?_i') + #0
lema('[Rr]elocalizar_s_e(?:lo|)_c') + #0
lema('[Rr]enombrar_í_a[ns]?_i') + #0
lema('[Rr]epart(?:ir|)_í_a[ns]?_i') + #3
lema('[Rr]epetir_á_[ns]?_a') + #1
lema('[Rr]eposar_í_a[ns]?_i') + #1
lema('[Rr]epresentar_í_a[ns]?_i') + #5
lema('[Rr]equer_í_(?:a[ns]?|)_i') + #7
lema('[Rr]equerir_á_[ns]?_a') + #0
lema('[Rr]esguardar_í_a[ns]?_i') + #0
lema('[Rr]esid(?:ir|)_í_a[ns]?_i') + #12
lema('[Rr]esidir_á_[ns]?_a') + #0
lema('[Rr]esist(?:ir|)_í_a[ns]?_i') + #0
lema('[Rr]esistir_á_[ns]?_a') + #0
lema('[Rr]espetabil_í_sim[ao]s?_i') + #0
lema('[Rr]espond_í_(?:a[ns]?|)_i') + #8
lema('[Rr]esponder_á_[ns]?_a') + #1
lema('[Rr]est_á_r[mts]el[aeo]s?_a') + #0
lema('[Rr]estitu_i_d[ao]s?_í') + #3
lema('[Rr]estitu_i_r(?:l[aeo]s?|se|)_í') + #0
lema('[Rr]esultar_í_a[ns]?_i') + #2
lema('[Rr]etirar_s_e(?:lo|)_c') + #0
lema('[Rr]etirar_í_a[ns]?_i') + #2
lema('[Rr]etra_í_(?:a[ns]?|d[ao]s?)_i') + #19
lema('[Rr]etra_í_d[ao]s?_i') + #19
lema('[Rr]etractar_í_a[ns]?_i') + #0
lema('[Rr]etribu_i_d[ao]s?_í') + #6
lema('[Rr]eun_í_a[ns]?_i') + #39
lema('[Rr]eunir_á_[ns]?_a') + #4
lema('[Rr]evelar_í_a[ns]?_i') + #1
lema('[Rr]eviv(?:ir|)_í_a[ns]?_i') + #1
lema('[Rr]eñid_í_sim[ao]s?_i') + #0
lema('[Rr]iqu_í_sim[ao]s?_i') + #3
lema('[Rr]omp_í_a[ns]?_i') + #1
lema('[Rr]omper_á_[ns]?_a') + #3
lema('[Rr]ud_í_sim[ao]s?_i') + #0
lema('[Ss]_i_do_í') + #3
lema('[Ss]_i_guie(?:ron|ntes?)_e') + #15
lema('[Ss]_o_la(?:s|mente|)_ó') + #110
lema('[Ss]_á_dic(?:[ao]s?|amente)_a') + #3
lema('[Ss]_í_ntesis_i') + #102
lema('[Ss]_ó_tanos_o') + #5
lema('[Ss]_ú_bit(?:[ao]s|amente)_u') + #3
lema('[Ss]_ú_per (?:Vedette|Humor|Pesad[ao]s?)_u') + #36
lema('[Ss]ab_í_amos_i') + #2
lema('[Ss]acrificar_í_a[ns]?_i') + #0
lema('[Ss]aldar_í_a[ns]?_i') + #1
lema('[Ss]aldr_á_[ns]?_a') + #23
lema('[Ss]aldr_í_a[ns]?_i') + #11
lema('[Ss]ali_en_do_ne') + #0
lema('[Ss]at_í_roc[ao]s?_i') + #1
lema('[Ss]e_ri_es?_ir', pre='(?:[Ll]as?|[Dd]e) ') + #2
lema('[Ss]ecu_e_ncia_a') + #1
lema('[Ss]ecu_e_ncias?_a') + #1
lema('[Ss]ecue_s_trad[ao]s?_') + #1
lema('[Ss]egu(?:ir|)_í_a[ns]?_i') + #30
lema('[Ss]egu_í_amos_i') + #0
lema('[Ss]eguir_í_a(?:[ns]?|mos)_i') + #4
lema('[Ss]eguir_í_amos_i') + #0
lema('[Ss]em_á_foros?_a') + #22
lema('[Ss]emiolog_í_as?_i') + #6
lema('[Ss]enadur_í_as?_i') + #3
lema('[Ss]ent_í_amos_i') + #0
lema('[Ss]eparar_í_a[ns]?_i') + #3
lema('[Ss]er_í_amos_i') + #1
lema('[Ss]eren_í_sim[ao]s?_i') + #9
lema('[Ss]erializar_s_e(?:lo|)_c') + #0
lema('[Ss]ervi_c_ios?_s') + #2
lema('[Ss]ervir_á_[ns]?_a') + #7
lema('[Ss]ervir_í_a[ns]?_i') + #6
lema('[Ss]eud_ó_nimos?_o') + #18
lema('[Ss]i_e_mpre_') + #4
lema('[Ss]i_no má_s bien_ no m[aá]') + #4
lema('[Ss]i_s_temas?_') + #12
lema('[Ss]icol_ó_gic[ao]s?_o') + #0
lema('[Ss]ie_m_pre_n') + #2
lema('[Ss]ignificar_í_a[ns]?_i') + #8
lema('[Ss]igu_i_entes?_') + #45
lema('[Ss]iller_í_as?_i') + #28
lema('[Ss]imb_ó_lic(?:[ao]s|amente)_o') + #4
lema('[Ss]imbi_ó_tic[ao]s?_o') + #13
lema('[Ss]impatiqu_í_sim[ao]s?_i') + #0
lema('[Ss]imult_á_neamente_a') + #53
lema('[Ss]in_ó_nimos?_o') + #22
lema('[Ss]intomatolog_í_as?_i') + #0
lema('[Ss]inverg_ü_enzada_u') + #1
lema('[Ss]iqui_á_tric[ao]s?_a') + #0
lema('[Ss]iquiatr_í_as?_i') + #1
lema('[Ss]ismol_ó_gic[ao]s?_o') + #3
lema('[Ss]istem_á_tic(?:[ao]s?|amente)_a') + #5
lema('[Ss]it_ú_(?:a[ns]?|e[ns]?)_u') + #123
lema('[Ss]o_r_prendió_') + #0
lema('[Ss]obre_vi_vientes?_') + #17
lema('[Ss]obresal(?:dr|)_í_a[ns]?_i') + #0
lema('[Ss]obrese_í_d[ao]s?_i') + #7
lema('[Ss]obrevi_vi_do_') + #8
lema('[Ss]obreviv(?:ir|)_í_a[ns]?_i') + #0
lema('[Ss]obrevivir_á_[ns]?_a') + #0
lema('[Ss]of_t_ware_') + #17
lema('[Ss]of_á_s?_a', pre='(?:[Ss]u|[Ee]l|[Dd]el|[Uu]n|[Ll]os|como) ') + #12
lema('[Ss]ol_í_amos_i') + #1
lema('[Ss]omet_é_r[mts]el[aeo]s?_e') + #1
lema('[Ss]omet_í_a[ns]?_i') + #0
lema('[Ss]ometer_á_[ns]?_a') + #1
lema('[Ss]onr_í_e[ns]?_i') + #21
lema('[Ss]onre_í_r_i') + #15
lema('[Ss]orprend_í_a[ns]?_i') + #0
lema('[Ss]u_stitui_d[ao]s?_tituí') + #2
lema('[Ss]ub_í_an_i') + #2
lema('[Ss]ubg_é_neros?_e') + #37
lema('[Ss]uced_í_a[ns]?_i') + #6
lema('[Ss]uceder_á_[ns]?_a') + #2
lema('[Ss]uceder_í_a[ns]?_i') + #2
lema('[Ss]ufr(?:ir|)_í_a[ns]?_i') + #3
lema('[Ss]ufr_í_a[ns]?_i') + #3
lema('[Ss]ufrir_á_[ns]?_a') + #0
lema('[Ss]uger_í_a[ns]?_i') + #0
lema('[Ss]uicid__ó_i') + #7
lema('[Ss]uperh_é_roes?_e', pre='(?:[Uu]n|[Ee]l|[Ll]os| de| y) ') + #11
lema('[Ss]upon_í_a[ns]?_i') + #13
lema('[Ss]upondr_á_[ns]?_a') + #0
lema('[Ss]uponi_en_do_ne') + #0
lema('[Ss]urgir_á_[ns]?_a') + #2
lema('[Ss]urtir_á_[ns]?_a') + #0
lema('[Ss]uspend_í_a[ns]?_i') + #1
lema('[Ss]ust_itui_d[ao]s?_uí') + #1
lema('[Ss]ustitu_i_d[ao]s?_í') + #36
lema('[Ss]ustitu_i_r(?:l[aeo]s?|se|)_í') + #4
lema('[Ss]ustituir_á_[ns]?_a') + #2
lema('[Ss]ustra_í_(?:a[ns]|d[ao]s?)_i') + #2
lema('[Ss]ustra_í_d[ao]s?_i') + #2
lema('[Tt]__igre_r') + #1
lema('[Tt]_e_sis_é') + #124
lema('[Tt]_i_tulad[ao]s?_í') + #111
lema('[Tt]_á_ctil(?:es|)_a') + #23
lema('[Tt]_é_rmic(?:as|os?)_e') + #29
lema('[Tt]_é_rmino_e', pre='[Pp]rimer ') + #10
lema('[Tt]_í_pic(?:[ao]s|amente)_i') + #27
lema('[Tt]_í_teres?_i') + #26
lema('[Tt]_ó_picos?_o') + #12
lema('[Tt]_ó_rax_o') + #17
lema('[Tt]_ó_xic(?:as|os?)_o') + #26
lema('[Tt]ant_í_sim[ao]s?_i') + #0
lema('[Tt]ao_í_s(?:tas?|mo)_i') + #71
lema('[Tt]e_m_prana_n') + #1
lema('[Tt]e_r_minar(?:se|l[ao]s?|ron|ría[ns]?|)_') + #2
lema('[Tt]ec_noló_gic[ao]_(?:nolo|onol[oó])') + #103
lema('[Tt]ect_ó_nic(?:as|os?|amente)_o') + #1
lema('[Tt]el_é_fono_e', pre='(?:[Ee]l|[Ss]u|[Uu]n|como|por) ') + #25
lema('[Tt]el_é_fonos_e') + #25
lema('[Tt]elevi_s_ión_c') + #0
lema('[Tt]elevi_si_ón_') + #2
lema('[Tt]elevis_i_ón_') + #39
lema('[Tt]elevis_i_ón_í') + #0
lema('[Tt]elevisi__ón_s') + #2
lema('[Tt]em_í_a[ns]_i') + #2
lema('[Tt]en_í_amos_i') + #3
lema('[Tt]en_í_an_i') + #79
lema('[Tt]end_í_a[ns]?_i') + #0
lema('[Tt]ende_n_cias?_') + #3
lema('[Tt]endr_á_[ns]_a') + #19
lema('[Tt]endr_í_a[ns]?_i') + #32
lema('[Tt]ent_á_culos?_a') + #13
lema('[Tt]erminar_í_a[ns]?_i') + #15
lema('[Tt]err_e_motos?_o') + #4
lema('[Tt]errest_r_es?_') + #57
lema('[Tt]exte_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema('[Tt]ie_m_po_n') + #10
lema('[Tt]ioci_á_nic[ao]s?_a') + #0
lema('[Tt]itular_í_sim[ao]s?_i') + #0
lema('[Tt]odoter_r_enos?_') + #0
lema('[Tt]omar_í_a[ns]?_i') + #3
lema('[Tt]opolog_í_as?_i') + #14
lema('[Tt]or_á_xoc[ao]s?_a') + #0
lema('[Tt]ra_ns_curr(?:e[ns]?|ió)_sn') + #1
lema('[Tt]ra_ns_porte[ns]_s?n') + #3
lema('[Tt]ra_í_d[ao]s?_i') + #47
lema('[Tt]ra_í_dos?_i') + #24
lema('[Tt]raducir_á_[ns]?_a') + #0
lema('[Tt]raer_á_[ns]?_a') + #1
lema('[Tt]raicionar_í_a[ns]?_i') + #0
lema('[Tt]rampol_í_n_i') + #13
lema('[Tt]ran_s_formar(?:se|)_') + #4
lema('[Tt]ran_s_paren(?:cias?|tes?)_') + #1
lema('[Tt]ran_s_portados_') + #0
lema('[Tt]ran_s_porte_') + #4
lema('[Tt]ranscurr(?:ir|)_í_a[ns]?_i') + #5
lema('[Tt]ransformar_s_e(?:lo|)_c') + #0
lema('[Tt]ransformar_í_a[ns]?_i') + #0
lema('[Tt]ransmit(?:ir|)_í_a[ns]?_i') + #16
lema('[Tt]ransmitir_á_[ns]?_a') + #4
lema('[Tt]ransportar_í_a[ns]?_i') + #2
lema('[Tt]rasladar_s_e(?:lo|)_c') + #1
lema('[Tt]rasmit(?:ir|)_í_a[ns]?_i') + #0
lema('[Tt]rasmitir_á_[ns]?_a') + #0
lema('[Tt]raspi_é_s?_e') + #3
lema('[Tt]raum_á_tic[ao]s?_') + #0
lema('[Tt]raumatolog_í_as?_i') + #3
lema('[Tt]reintai_ú_n_u') + #1
lema('[Tt]reintaid_ó_s_o') + #1
lema('[Tt]reintais_é_is_e') + #1
lema('[Tt]reintaitr_é_s_e') + #0
lema('[Tt]remend_í_sim[ao]s?_i') + #0
lema('[Tt]rig_é_sim[ao]s?_e') + #13
lema('[Tt]ropical_í_sim[ao]s?_i') + #7
lema('[Tt]uber_í_as?_i') + #22
lema('[Uu]gand_é_s_e') + #5
lema('[Uu]ltras_ó_nic[ao]s?_o') + #7
lema('[Uu]n_ _partido_') + #1
lema('[Uu]n_á_nime(?:mente|)_a') + #25
lema('[Uu]ng_ü_entos?_u') + #1
lema('[Uu]nir_s_e(?:lo|)_c') + #0
lema('[Uu]nir_á_[ns]?_a(?!\])') + #11
lema('[Uu]nir_í_a[ns]?_i') + #9
lema('[Uu]sar_í_a[ns]?_i') + #2
lema('[Uu]t_i_li(?:z(?:[ae]n?|[oó])|cen?)_') + #21
lema('[Uu]t_i_lizad[ao]s?_') + #8
lema('[Uu]t_ilizació_n_(?:lizaci[oó]|ilizacio)') + #13
lema('[Uu]til_í_sim[ao]s?_i') + #3
lema('[Uu]tiler_í_as?_i') + #5
lema('[Uu]tilizar_s_e(?:lo|)_c') + #0
lema('[Uu]tilizar_í_a[ns]?_i') + #3
lema('[Vv][eé][aá]se _t_ambi[eé]n_T') + #460
lema('[Vv]_inculó__(?:íncul[oó]|inculo)', pre='[Ss]e(?: me| te| l[aeo]s?|) ') + #2
lema('[Vv]_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #1
lema('[Vv]_í_ctimas?_i', pre='(?:[Ee]s|[Ff]u[ée]|[Ff]ueron|[Ll]as?|[Ss]erá|[Ss]on|[Uu]nas?|[Oo]tras?|[Dd]e|[Ss]u) ') + #157
lema('[Vv]al_ú_(?:a[ns]?|en)_u') + #10
lema('[Vv]aldr_á_[ns]?_a') + #0
lema('[Vv]alios_í_sim[ao]s?_i') + #1
lema('[Vv]e_í_amos_i') + #1
lema('[Vv]eh_í_culos?_i') + #156
lema('[Vv]einti_ú_n_u') + #10
lema('[Vv]eintid_ó_s_o') + #36
lema('[Vv]eintis_é_is_e') + #38
lema('[Vv]eintitr_é_s_e') + #54
lema('[Vv]encer_í_a[ns]?_i') + #10
lema('[Vv]ender_á_[ns]?_a') + #3
lema('[Vv]endr_í_a[ns]?_i') + #6
lema('[Vv]enerad_í_sim[ao]s?_i') + #0
lema('[Vv]engar_s_e(?:lo|)_c') + #0
lema('[Vv]engar_s_e_z') + #0
lema('[Vv]entajos_í_sim[ao]s?_i') + #0
lema('[Vv]er_sió_n_ci[oó]') + #5
lema('[Vv]er_í_amos_i') + #0
lema('[Vv]erg_ü_enzas?_u') + #18
lema('[Vv]estir_á_[ns]?_a') + #6
lema('[Vv]estir_í_a[ns]?_i') + #5
lema('[Vv]ideogr_á_fic[ao]s?_a') + #1
lema('[Vv]illan_í_sim[ao]s?_i') + #0
lema('[Vv]irar_í_a[ns]?_i') + #1
lema('[Vv]iv_í_amos_i') + #0
lema('[Vv]ivir_í_a[ns]?_i') + #1
lema('[Vv]ol_u_men_ú') + #469
lema('[Vv]olv_í_(?:a[ns]?)_i') + #21
lema('[Vv]olver_í_a(?:n|mos|)_i') + #24
lema('[Vv]uelt_a_s?_á') + #0
lema('[Zz]oledr_ó_nic[ao]s?_o') + #1
lema('[p]ertene_nci_as?_c[ií]', pre='(?:[Ll]as?|[Ss]us?|[Dd]e) ') + #117
lema('_Pací_fico_(?:pac[ií]|Paci)', pre='[Oo]c[eé]ano ') + #253
lema('[Ff]i_l_m_', pre='(?:[Dd]el|[Ee]l) ') + #6
lema('[a]_ _sus_') + #4
lema('[c]omprendi_do__[óo]', pre='[Pp]er[ií]odo ') + #3
lema('[d]_í_as_i', pre='(?:[Aa]lgunos|[Bb]uenos|[Ee]scasos|[Ee]stos|[Ll]os|[Nn]uestros|[UÚuú]ltimos|[Uu]nos|[Vv]arios|[Dd]os|[Tt]res|[Cc]uatro|[Cc]inco|[Ss]eis|[Ss]iete|[Oo]cho|[Nn]ueve|[Dd]iez|[0-9]+) ') + #477
lema('[d]e l_ongitud__largària') + #0
lema('[d]eb_í_a(?:s?|mos)_i') + #42
lema('[d]esar_rolló__r?oll?o', pre='[Ss]e(?: me| te| l[aeo]s?|) ') + #83
lema('[d]ivid_id_a_', pre='(?:[Dd]ecisión|[Ss]er|[Ee]star|[Ee]staba|[Ee]st[aá]|estuvo|se encontraba|se encuentra|queda|quedó|quedará|es|fue|llanura|continuó|distancia|Austria|Actualmente|opinión) ') + #22
lema('[e]st_á_(?:[.,;]| (?:el|la|un|una) )_a', pre='donde ') + #1
lema('[f]ranc_é_s[,.]_e') + #23
lema('[f]ranc_é_s_e', pre='[Ii]dioma [Ff]ranc[eé]s\|') + #4
lema('[g]_é_neros?_e', pre='(?:[Ee]l|[Ll]os|[Uu]n|[Uu]nos) ') + #97
lema('[h]ar_á_s_a', pre='(?:[Qq]u[eé]|dinero|te|carrera) ') + #0
lema('[l]e_í_da_i') + #9
lema('[l]e_í_dos_i') + #8
lema('[m]_á_ximas?_a', pre='(?:[Ll]as?|[Uu]nas?) ') + #28
lema('[m]_á_ximos?_a', pre='(?:[Ee]l|[Uu]n|[Ll]os) ') + #22
lema('[m]_í_nimas?_i', pre='(?:[Ll]as?|[Uu]nas?) ') + #8
lema('[m]ir_á_ndol[ae]_a') + #1
lema('[n]_ó_mina_o', pre='(?:[Ss]u|[Ee]n|[Uu]na|misma|primera|en|de) ') + #6
lema('[p]erd_í_a_i') + #7
lema('[p]ondr_á_s?_a') + #7
lema('[q]_ue_ le_') + #1
lema('[s]ab_í_an_i') + #13
lema('[s]ali_o__ó', pre='[Ee]mperador ') + #8
lema('[s]erv_í_a_i') + #31
lema('[t]_é_rmino_e', pre='(?:[Aa]l?|[Dd]el?|[Uu]n|[Ss]u|[Ee]l) ') + #390
lema('[t]_é_rminos_e', pre='[Ll]os ') + #14
lema('[t]rav_é_s_e', pre='(?:[Aa]|[Dd]e) ') + #179
lema('[v]er_á_n_a') + #2
lema('[v]iv(?:ir|)_í_a[ns]?_i') + #57
lema('[Áá]lbum_e_s_(?:ne|)') + #102
lema('\(_álbum de \g<num>_\)_(?P<num>[0-9]{4}) album') + #10
lema('_(discográfica)__\(record label\)') + #107
lema('_A_quel_Á') + #4
lema('_Club de Futbol Igualada__Club de Fútbol Igualada') + #0
lema('_D_inamarca_d', pre='(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or|y) ') + #2
lema('_E_ll[ao]s?_É') + #2
lema('_E_quipos?_É') + #2
lema('_E_spaña_e', pre='(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #64
lema('_E_sta vez_É') + #29
lema('_E_ste (?:último|primer)_É') + #32
lema('_E_sto_É') + #85
lema('_Estados U_nidos_(?:estados [Uu]|Estados u)', pre='(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #334
lema('_F_rancia_f', pre='(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #31
lema('_G_recia_g', pre='(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #5
lema('_Ha_sta ahora_A') + #0
lema('_Hu_esos?_U') + #0
lema('_Hu_ndi(?:d[ao]s?|dimiento)_U') + #2
lema('_I_talia_i', pre='(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #22
lema('_Japó_n_(jap[oó]|Japo)', pre='(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #76
lema('_Latinoamé_rica_[Ll](?:ationoame|atínoame|ationoamé|ationame|atioamé|atinooamé|atínoamé)') + #6
lema('_Murphy Pacific Corporation__Murphy Pacific Corporacion') + #0
lema('_P_araguay_p', pre='(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #9
lema('_R_usia_r', pre='(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #9
lema('_S_uecia_s', pre='(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #7
lema('_U_ruguay_u', pre='(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #15
lema('_V_enezuela_v', pre='(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #49
lema('__a sus?_h') + #5
lema('__acerca(?:r|rse|)_h') + #0
lema('_a_ (?:abrazar|abrir|acceder|aceptar|aclarar|actuar|admitir|adquirir|afectar|ahorrar|ampliar|andar|apalizar|aparecer|aprender|arreglar|asar|ascender|asistir|asumir|atacar|atender|atrapar|aumentar|averiguar|avisar|ayudar|añadir|buscar|caer|cambiar|cancelar|cantar|castigar|cazar|celebrar|cerrar|cobrar|coincidir|combinar|comer|comercializar|cometer|competir|completar|componer|comprar|comprender|conocer|conseguir|considerar|consolar|construir|consumir|convertir|cosechar|crear|cultivar|dar|decir|declarar|definir|dejar|demostrar|denunciar|derramar|desarrollar|desartillar|descender|descubrir|desempeñar|destacar|destruir|detener|devolver|disculpar|disertar|diseñar|disputar|doblar|dominar|efectuar|ejercer|elegir|empezar|emprender|enamorar|encontrar|enfrentar|engrosar|entender|entrar|enviar|esconder|escribir|esperar|estacionar|estar|estudiar|evitar|examinar|existir|experimentar|extraer|extrañar|fabricar|facturar|finalizar|firmar|forjar|formar|formar|ganar|generar|gestar|grabar|haber|hablar|hacer|impartir|implantar|destinar|impulsar|incrementar|informar|inmortalizar|interpretar|investigar|ir|jugar|labrar|levantar|licuar|llegar|llevar|lograr|mantener|marcar|matar|mencionar|morir|necesitar|notar|obtener|ocurrir|ofertar|oficiar|orar|parar|participar|partir|pasar|pesar|pensar|permitir|persistir|poder|poner|practicar|preparar|presentar|producir|promediar|promocionar|proporcionar|protagonizar|publicar|pulsar|quedar|quitar|realizar|recibir|reclamar|recoger|recolectar|reconocer|recopilar|recordar|reeditar|regresar|rellenar|renovar|renunciar|repetir|reprender|respetar|resurgir|retomar|saber|salir|seguir|sobredestacar|solicitar|sufrir|tabajar|tener|tomar|torturar|trabajar|transmitir|trazar|usar|utilizar|vejar|vender|ver|verificar|viajar|visitar|volar)_(?:ha|ah)') + #89
lema('_a_quel_á') + #3
lema('_c_ercan[ao]s?_s') + #0
lema('_consultado el__acessado em') + #25
lema('_d_estacados_D', pre='[Jj]ugadores ') + #1558
lema('_e inglé_s_[ey] ingle', pre='(?:quechua|franc[eé]s|español|coreano|japon[eé]s) ') + #10
lema('_e_spañol_E', pre='ejército ') + 
lema('_e_sta (afición|vez)_é') + #162
lema('_e_ste (?:último|primer)_é') + #192
lema('_e_sto_é') + #233
lema('_e_xternos_E', pre='(?:[Ee]nlaces|[Vv]ínculos) ') + #2146
lema('_encontraba__encuentraba') + #21
lema('_escándalo__escandalo') + #39
lema('_esperando__esparando', pre='[Ee]stán? ') + #0
lema('_febrero__[Ff]evereiro', pre='acessado em [0-9]+ de ') + #0
lema('_ha_ dicho (?: a |el |de |en |que|antes|ser )_ah?') + #3
lema('_ha_sta ahora_a') + #1
lema('_hu_esos?_u') + #2
lema('_hu_ndi(?:d[ao]s?|dimiento)_u') + #2
lema('_increíble__íncreible') + #0
lema('_increíbles__íncreibles') + #1
lema('_noviembre__[Nn]ovembro', pre='acessado em [0-9]+ de ') + #0
lema('_obstáculos__obstaculos') + #26
lema('_sali_an?_(?:Sal[ií]|salí)', pre='[Dd]inast[ií]a ') + #1
lema('_sobre la base de__en base a') + #1093
lema('_v_oleibol_b') + #4
lema('_z_ona_s', pre='(?:[Ll]a|[Uu]na|[Dd]e) ') + #3
lema('_Á_gil(?:es|mente)_A') + #0
lema('_Á_ngel Gim[eé]nez_A') + #14
lema('_Á_rbitros?_A') + #132
lema('_Á_ure[ao]s_A') + #0
lema('_É_l (?:anhela|pued[ae]|gana)_E') + #32
lema('_É_nfasis_E') + #2
lema('_É_tnic(?:[ao]s|amente)_E') + #1
lema('_É_xitos?_E') + #138
lema('_Ó_rbitas?_O', pre='(?:[Ll]as?|[Ss]us?|[Uu]nas?|[Ee]n) ') + #6
lema('_Ú_ltimamente_U') + #9
lema('_Ú_ltimas?_U', pre='(?:[Ll]as?|[Uu]nas?) ') + #129
lema('_Ú_nic(?:[ao]s|amente)_U') + #19
lema('_á_gil(?:es|mente|)_a') + #10
lema('_á_guilas?_a') + #97
lema('_á_ngulos?_a', pre='(?:[Ee][nl]|[Uu]n|[Ll]os|[Uu]nos) ') + #27
lema('_á_reas?_a', pre='(?:[AaEe]l|[Ll]as|[Mm][aá]s|[Uu]nas|[Aa]lgunas|[Dd]el?|[Uu]n|[Cc]ada|[Ss]us|[Oo]tras?|[Dd]os|[Ee]stas?|[Ee]sas?|[Ee]n) ') + #179
lema('_álbu_m(?:es|)_albú') + #101
lema('_álbumes__albums', pre='(?:[Ll]os|[Ss]us)') + #0
lema('_é_l (?:ante|cabe|con|desde|entre|según|sin|tras)\\b_e', pre='[Cc]on ') + #42
lema('_é_nfasis_e') + #11
lema('_é_tnic(?:[ao]s|amente)_e') + #13
lema('_é_xodos?_e') + #7
lema('_í_ntimamente_i') + #11
lema('_ó_mnibus_o', pre='\\b(?:y|[Ee]l|[Uu]n|de|en|trenes|Micro|son|transporte:|llamados|scientiis|formato|tomaran|Empresa|tituló) (?:["\']|\[\[|)') + #47
lema('_ó_pticas_o') + #2
lema('_ó_rdenes_o', pre='(?:[Ll]as|[Uu]nas|[Ss]us|[Dd]ar|[Dd]ando|[Pp]or) ') + #202
lema('_ú_ltima_u', pre='(?:[Aa]|[Cc]omo|[Dd]el|[Ee]st[ao]s?|[Ll]as?|[Pp]or|[Qq]ueda[nsr]?|[Qq]uedó|[Ss]us?|[Uu]na|[Uu]nas|[Yy]) ') + #484
lema('_ú_ltimamente_u') + #25
lema('_ú_ltimas_u', pre='(?:[Ll]as|dos|tres) ') + #83
lema('_ú_nica_u', pre='(?:[Ll]a|[Uu]na|[Ss]u|es|será) ') + #82
lema('_ú_nico_u', pre='(?:[Ee]l|[Uu]n) ') + #111
lema('_ú_nico_u', pre='(?:[Ee]l|[Uu]n)] ') + #0
lema('_ú_nicos_u', pre='(?:[Ss]us|[Ll]os) ') + #17
lema('[Ff]_utbolí_stic(?:[ao]s?|amente)_útbol[ií]') + 
lema('[Dd]_el á_rea_(?:el a|e la [aá])') + 
lema('_el á_rea_(?:el a|la [aá])') + 
lema('[e]n_ _medio_') + 
lema('[Oo]btuv_o__ó') + 
lema('[Ee]stuv_o__ó') + 
lema('[Hh]oland_é_s_e') + 
lema('[Ii]nform_á_tic[ao]s_a') + 
lema('[Vv]ivir_á_[ns]?_a') + #5
lema('_c_heco_C', pre='\\b(?:e[ln]|del|idioma|y) ') + 
lema('[Cc]l_ás_ic[ao]s?_[aá]c') + lema('[Cc]l_á_sica_a', xpos=['(?: do|maior)\\b', '2\.com']) + #293
lema('[Dd]escalific_ó__o') + 
lema('[h]_a_ce_e') + 
lema('[Ll]leg_ó a s_er_(?:o a s|[oó] hac)') + 
lema('[Úú]ltim[ao]_s__', pre='[Ll][ao]s ') + 
lema('[Cc]omisar_í_as?_i', pre='[Ee]n ') + 
lema('_C_olombia_c', pre='(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + 
lema('[Rr]adiolog_í_as?_i') + 
lema('[Ii]nsect_ó_log[ao]s?_o') + 
lema('[Jj]ug_ó_ (?:un|dos|tres|cuatro|diez|cien|mil|unos|varios)_o') + 
lema('[Pp]rot_e_ic[ao]s?_é') + 
lema('[Tt]ransg_é_ner[ao]s?_e') + 
lema('[Dd]esign_ó__o') + 
lema('[Cc]an_c_i(?:ón|ones)_s', xpos=[' barias']) + 
lema('[Gg]r_á_fico_a', xpos=[' Editoriale']) + 
lema('[Dd]isput_ó_ en_o') + 
lema('[Nn]eurofenomenolog_í_as?_i') +
lema('[Ss]obre__nombre_ ') +
lema('[m]_á_s_a', pre='(?:[Nn]o (?:cultivan?)|atendió|da|[Ll]ea|[Pp]ara|produciendo|espec[ií]fic(?:[ao]s?|amente)) ') +
lema('[Uu]n_a_ (?:agencia|aldea|alternativa|amalgama|antigua|banda|barra|bomba|buena|cadena|caja|campaña|capa|carrera|casa|chica|cierta|cita|comedia|compañía|copia|corta|criatura|crítica|cuerda|derrota|distancia|empresa|escena|escuela|escultura|estatua|estrella|estructura|etapa|extensa|extraña|familia|fecha|fiesta|figura|franja|fuerza|guerra|historia|idea|iglesia|intensa|lanza|ligera|lucha|línea|manera|mezcla|misma|niña|nota|novela|nueva|obra|palabra|pareja|pelea|película|pequeña|persona|perspectiva|pieza|pista|placa|planta|plataforma|playa|plaza|política|potencia|profunda|prueba|página|pérdida|rama|raza|referencia|reserva|respuesta|revista|ruta|sala|secuencia|sola|tabla|tasa|temperatura|temporada|tienda|trama|técnica|verdadera|victoria|vida|zona|[eé]poca|[uú]nica)\\b_') + #4462
lema('[Uu]n_a_ (?:alerta|alianza|amiga|armadura|atmósfera|auténtica|avenida|barrera|batalla|bebida|beca|bella|biografía|bola|bolsa|brigada|broma|bóveda|caldera|carga|carretera|caída|ceremonia|cifra|cinta|clara|clínica|cola|colina|comarca|competencia|computadora|conferencia|corona|cubierta|cueva|curva|célula|cúpula|demanda|determinada|diferencia|disputa|dura|década|economía|entrada|ermita|escalera|escritora|esfera|estrategia|estrecha|experiencia|falla|famosa|feria|finca|flota|fotografía|futura|granja|hermana|hija|hora|huelga|inmensa|jugadora|junta|lengua|letra|leyenda|llamada|maestra|mancha|marcha|medalla|medida|mejora|mina|montaña|muestra|ofensiva|oferta|oficina|orquesta|pantalla|parada|parodia|partícula|pelota|piedra|pintura|pistola|postura|presencia|princesa|propuesta|protesta|proteína|provincia|pr[aá]ctica|r[eé]plica|rampa|reforma|regla|revuelta|rica|rueda|rápida|secuela|semana|silla|talla|tarjeta|tecnología|teoría|trampa|trenza|típica|vasta|ventaja|vieja|villa|visita|vista|vivienda|órbita|última)\\b_') + #1657
lema('[Uu]n_a_ (?:lujosa|lámina|lámpara|lápida|maestría|magnífica|maniobra|maqueta|mascota|materia|mayoría|memoria|mesa|meseta|minoría|mirada|molécula|moneda|máscara|máxima|música|norma|novia|olla|onda|palma|parcela|parroquia|partida|patrulla|pausa|pena|perfecta|pierna|pila|pionera|piscina|poca|poderosa|polémica|portada|prenda|presa|previa|proclama|profesora|prostituta|próxima|puesta|racha|rana|recarga|receta|recta|reina|reja|relativa|república|reseña|residencia|resistencia|retrospectiva|rotura|ruptura|ráfaga|saga|salida|sencilla|senda|sentencia|seria|sexta|significativa|suma|superheroína|supuesta|sustancia|sátira|tanda|tela|tendencia|terapia|textura|tormenta|treintena|trompeta|tropa|tía|túnica|vaina|vara|variada|ventana|vuelta|válvula|víctima|ópera)\\b_') + #561
lema('[Uu]n_a_ (?:abogada|academia|aerolínea|alarma|aliada|apariencia|apertura|apuesta|arquitectura|asamblea|asesina|audiencia|aventura|bahía|balada|bandeja|bandera|bestia|biblioteca|bicicleta|botella|búsqueda|cabaña|cabina|cafetería|campeona|capilla|cascada|catarata|categoría|caña|chaqueta|charla|ciencia|cirugía|colonia|columna|completa|comuna|consola|copa|corneta|cota|cuarta|cuenca|cultura|cuota|cápsula|dama|danza|decena|densa|dependencia|destacada|desventaja|dieta|diseñadora|docena|droga|ejecutiva|elevada|embajadora|emboscada|emisora|empleada|encuesta|enfermera|era|escuadra|espada|estética|factoría|falda|falta|farsa|firma|flecha|fractura|fragata|fuga|gata|gigantesca|gorra|grieta|gruesa|hembra|hermosa|hierba|ideología|industria|invitada|jornada|liga|linterna)\\b_') + #558
lema('[Uu]n_a fá_brica_ f[aá]') + #127
lema('[Uu]n_a magní_fica_ magn[ií]') + #127
lema('[Uu]n_a má_quina_ m[aá]') + #127
lema('[Uu]n_a pé_rdida_ p[eé]') + #127
lema('[Uu]n_a ré_plica_ r[eé]') + #127
lema('[Aa]_ _cargo_') + 
lema('[Aa]__ños_ños a') + 
lema('[Cc]__ada_ada c') + 
lema('[Cc]olor___ color', xpos=['\'\'']) + 
lema('[Cc]__omo_omo c') + 
lema('[Cc]__on_on c') + 
lema('[Cc]__uando_uando c') + 
lema('[Dd]__el_el d') + 
lema('[Dd]__esde_esde d') + 
lema('[Dd]__espués_espués d') + 
lema('[Dd]__onde_onde d') + 
lema('[Dd]__urante_urante d') + 
lema('[Dd]e__l_ la e') + 
lema('[Ee]__l_l e') + 
lema('[Ee]n_ _realidad_') + 
lema('[Ee]n_ _serio_') + 
lema('[Ee]n e_l_ año_n') + 
lema('[Ee]__ntre_ntre e') + 
lema('[Ee]__ntre_ntre e') + 
lema('[Ee]__quipo_quipo e') + 
lema('[Ee]__ra_ra e') + 
lema('[Ee]__ste_ste e') + 
lema('[Ff]__ue_ue f') + 
lema('[Ff]__ueron_ueron f') + 
lema('[Hh]__a [a-záéíóúñ]+o_a h') + 
lema('[Ll]__as_as l') + 
lema('[Ll]__o_o l') + 
lema('[Ll]__os_os l') + 
lema('[Ll]o_s_ (?:aires|alrededores|alumnos|antiguos|años|artistas|barrios|bienes|bosques|capítulos|casos|casos|cerros|chicos|ciudadanos|códigos|colores|conceptos|cuales|cuáles|cuartos|datos|derechos|días|dientes|dos|edificios|efectos|ejercicios|elementos|enemigos|equipos|españoles|estándares|estudiantes|eventos|fans|franceses|ganadores|generales|grupos)_') + #600
lema('[Ll]o_s_ (?:habitantes|hechos|hermanos|héroes|hijos|hombres|huevos|indígenas|intereses|jóvenes|juegos|jugadores|líderes|límites|machos|medios|mercados|meses|métodos|miembros|modelos|momentos|motores|municipios|músicos|nazis|niños|niveles|ojos|otros|padres|países|partidos|pasos|períodos|personajes|pobladores|pocos|poderes|precios|premios|primeros|principales|principios|problemas|programas|pueblos|puntos|quales|relatos|resultados|reyes|ríos|sábados|sectores|seis|seres|servicios|siglos|siguientes|símbolos|sistemas|sitios|soldados|sucesos|suelos|territorios|tiempos|trabajos|trenes|tres|últimos|únicos|usuarios|valores|vascos|vecinos|votos)_') + #600
lema('[Ll]o_s_ (?:aborígenes|acontecimientos|actores|actos|acuerdos|admiradores|agentes|albores|alemanes|alimentos|andes|animales|anteriores|árboles|arcos|arqueólogos|arquitectos|arreglos|asuntos|ataques|autores|bancos|baños|beneficios|británicos|buques|cabellos|cambios|campeones|campos|canales|cánones|cargos|carros|centros|cimientos|clubes|colonizadores|concursantes|continentes|continuos|créditos|cronistas|cuadernos|cuadros|cuchillos|cursos|detalles|dibujos|documentos|donativos|ejecutivos|ejemplares|ejes|elfos|empleados|enamorados|encuentros|enérgicos|entes|episodios|escenarios|esclavos|esfuerzos|espectadores|estadounidenses|estilos|exámenes|extranjeros|extremos|factores|fallos|familiares|fanáticos|ferrocarriles|fines|firmantes|fondos|fundadores|gallegos|géneros|gobernadores|gobiernos|guerreros)_') + #230
lema('[Ll]o_s_ (?:hinchas|hindúes|honores|hospitales|huecos|huertos|humanos|húngaros|indios|informes|ingleses|inicios|instrumentos|integrantes|isleños|jardines|jefes|jesuitas|judíos|jueces|juguetes|libros|llamados|lugareños|lugares|máximos|mensajes|miles|militares|monjes|motivos|muros|nombres|números|objetivos|oídos|organismos|órganos|pacientes|pájaros|paquetes|parámetros|participantes|peces|periódicos|pies|pilotos|pioneros|piratas|planes|prisioneros|productos|profesores|propietarios|propios|proyectos|puentes|puestos|radares|rayos|rebeldes|receptores|recursos|referentes|regalos|reinos|religiosos|requerimientos|requisitos|sacerdotes|sacrificios|santos|satélites|secretos|seguidores|segundos|sentidos|sentimientos|señoríos|servidores|sindicatos|síntomas|sobrevivientes|sonidos|sospechábamos|sueños|suministros|tallos|templos|terrenos|testigos|tipos|títulos|túneles|turistas|unos|valles|viajes|vídeos|vientos)_') + #230
lema('[Oo]__tros_tros o') + 
lema('[Pp]__arte_arte p') + 
lema('[Pp]__ero_ero p') + 
lema('[Pp]__or_or p') + 
lema('[Pp]__rimer_rimer p') + 
lema('[Pp]__uede_uede p') + 
lema('[Qq]__ue_ue q') + 
lema('[Ss]__e_e s') + 
lema('[Ss]__er_er s') + 
lema('[Ss]__i_i s') + 
lema('[Ss]__ido_ido s') + 
lema('[Ss]__obre_obre s') + 
lema('[Ss]__on_on s') + 
lema('[Tt]__ambién_ambién t') + 
lema('[Tt]__iene_iene t') + 
lema('[Áá]__lbum_lbum á') + 
lema('_El__La el') + 
lema('[Ii]ndicar_í_a_i', xpre=['Tractatus de astrologia ']) + #4
lema('[Ss]ellar_í_a_i', xpre=['della ']) + #1
lema('(?:[Ss]emi|[Ss]ub|[Hh]iper|[Dd])esarrollar_í_a[ns]?_i') + #1
lema('[Aa]rchivar_í_a[ns]?_i', xpos=[', [1-9][0-9]+']) + #1
lema('[Aa]rd_í_as_i', xpre=['de ']) + #1
lema('[Cc]almar_í_a_i', xpre=['\\ba ']) + #1
lema('[Cc]aminar_í_a_i', xpre=['Hexatoma ']) + #1
lema('[Dd]egenerar_í_a_i', xpre=['Idaea ']) + #1
lema('[Ee]x_ces_iv[ao]s?_', xpre=['Aucula ']) + #1
lema('[Ll]abrar_í_a_i', xpre=['Abraxas ']) + #1
lema('[Mm]orfol_ó_gic(?:[ao]s|amente)_o', xpos=[' e\\b']) + #1
lema('[Oo]sar_í_as?_i', xpos=['\'\'']) + #1
lema('[Pp]illar_í_a_i', xpre=['Cycloclypeus ']) + #1
lema('[Vv]ersar_í_a_i', xpre=['Flagrospira ']) + #1
lema('(?:[Ee]nero|[Ff]ebrero|[Mm]arzo|[Aa]bril|[Mm]ayo|[Jj]unio|[Jj]ulio|[Aa]gosto|[Ss]eptiembre|[Oo]ctubre|[Nn]oviembre|[Dd]iciembre)_ de_ (?:\[\[|)[1-9][0-9][0-9][0-9]_(?:,|)', xpre=['Ediciones del 4 de '], xpos=[' sullo']) + 
lema('Gim_é_nez_e', xpre=['Antônio ']) + #561
lema('Hait_í__i', pre='(?:\||(?:[Dd]e|[Ee]n) )', xpre=['Démocratie ', 'Volleyball '], xpos=[' (?:Sings|and)']) + #103
lema('Jim_é_nez_e', xpre=['Cláudia ']) + #1714
lema('Medell_í_n_i', xpre=['in ', '366272\) ']) + #725
lema('Ocean_í_a_i', pre='(?:[Dd]e|[Ee]n) ', xpos=[' (?:Cruises|Rugby)']) + #7
lema('[Aa]bogac_í_as?_i', xpos=['\.es']) + #6
lema('[Aa]d_h_esivos?_', xpre=['[Cc]aso ']) + #31
lema('[Aa]narqu_í_as?_i', xpre=['amor i ']) + #55
lema('[Aa]nomal_í_as?_i', xpre=['Pichia ']) + #21
lema('[Aa]scen_s_ión_c', xpos=[' (?:Aguilera|[AÁ]lvarez|Alcalá|Andrade|Bonet|De los Santos|Farreras|García|Gómez|Hernández|Lencina|López|Martínez|Negrón|Nicol|Orihuela|Saucedo|Soto|Solórsano|Tepal|Vázquez)']) + #109
lema('[Aa]utom_ó_vil(?:es|)_o', xpos=[' Gesellschaft']) + #298
lema('[Bb]iogeogr_á_fic[ao]s?_a', xpre=['\\bdi ']) + #15
lema('[Bb]istur_í__i', xpre=['\\bO '], xpos=[' - La', ', la']) + #7
lema('[Cc]_ó_ptic[ao]s?_o', xpre=['Ptychotis ']) + #6
lema('[Cc]armes_í__i', xpre=['filla del ']) + #15
lema('[Cc]enar_í_a[ns]?_i', xpre=['(?:[Dd]e|[Ee]n)', '[Ii]slote ']) + #9
lema('[Cc]rec_í__i', xpre=['Enrique ']) + #3
lema('[Cc]ronol_ó_gic[ao]_o', xpre=['Storia '], xpos=[' (?:dei|della|das)']) + #25
lema('[Dd]_í_a_i', pre='(?:[Hh]oy(?: en|)|[Uu]n (?:buen|cierto|duro|gran|largo|nuevo|s[oó]lo)|[Pp]rimer|[Ss]egundo|[Tt]ercer|[Cc]uarto|[Qq]uinto|[Ss]exto|[Ss][eé]ptimo) ', xpos=[' (?:da|e meio)']) + #261
lema('[Dd]ep_ó_sitos?_o', xpre=['(?:[Ii]l|[Ll]a) ', 'Cardili, ', 'sepulcro '], xpos=[' (?:Giordani|da)']) + #383
lema('[Dd]iscogr_á_fic[ao]s?_a', xpre=['della Critica ']) + #434
lema('[Ee]_x_tendid[ao]s?_s?', xpre=['onde ']) + #20
lema('[Ee]nfermer_í_as?_i', xpos=['\.uady']) + #55
lema('[Ee]sf_é_ric[ao]s?_e', xpre=['Vorticella ', 'Lepidocyclina ']) + #21
lema('[Ff]icolog_í_as?_i', xpre=['Brasileira de ']) + #2
lema('[Ff]or_á_ne[ao]s?_a', xpre=['battello ', 'Mythimna ']) + #51
lema('[Ff]re_í_r_i', xpre=['Frey\|']) + #56
lema('[Ff]renes_í__i', xpre=['Coleção '], xpos=[' \(Lisboa', ': história']) + #19
lema('[Gg]e_ó_log[ao]s?_o', xpre=['Professione ']) + #27
lema('[Gg]rad_ú_a_u', xpos=['\'t']) + #19
lema('[Hh]oland_é_s_e', xpre=['permitió que el ']) + #140
lema('[Ii]c_ó_nic[ao]s?_o', xpre=['Glycyrrhiza ', 'Cousinia ', 'Conchologica ', 'Conchologia ']) + #53
lema('[Ii]nfanter_í_as?_i', xpre=['d\''], xpos=[' de marinha']) + #222
lema('[Ii]nic_i_os?_', xpos=[' d[\'’]Avalos', '\'\'\'']) + #37
lema('[Jj]erarqu_í_as?_i', xpos=[' a la Responsabilitat']) + #21
lema('[Ll]_á_mparas?_a', xpre=['[A]\. ', 'Astronesthes ', 'Wishing ']) + #164
lema('[Ll]_á_tigos?_a', xpre=['for ', 'George '], xpos=[' Means']) + #20
lema('[Ll]_é_sbic[ao]s?_e', xpre=['[AI]\. ', 'Aphaenogaster ', 'Isoperla '], xpos=[' e gay']) + #33
lema('[Ll]_ó_gic(?:os|amente)_o', xpos=[' Aristotelis']) + #5
lema('[Ll]_ó_gic[ao]_o', pre='(?:[Ll]a|[Uu]na) ', xpos=[' (?:d[iu]|del)\\b']) + #25
lema('[Ll]exicograf_í_as?_i', xpre=['Lexicologia y '], xpos=[' (?:e os|catalana|catalanes)\\b']) + #14
lema('[Ll]oter_í_as?_i', xpre=['Caixa '], xpos=[' (?:Vella|sem)']) + #106
lema('[Mm]agn_í_fica_i', pre='(?:[Ll]a|[Uu]na|[Dd]e|[Ee]sta|[Ss]u|[Tt]an) ', xpos=[' (?:Cure|ni)\\b']) + #70
lema('[Mm]al_é_vol[ao]s?_e', xpre=['Euphorbia ']) + #7
lema('[Mm]an_í_as?_i', pre='(?:[Ll]as?|[Uu]nas?) ', xpos=['\.com']) + #2
lema('[Mm]ani_á_tic[ao]s?_a', xpre=['[Ii]l ']) + #13
lema('[Mm]ariner_í_as?_i', xpos=[' degli']) + #16
lema('[Mm]iscel_á_ne[ao]s?_a', xpos=[' (?:Antwerpiensia|Barcinonensia|taxinomica)']) + #88
lema('[Mm]o_v_ilidad_b', xpos=[' Bahía']) + #38
lema('[Oo]rfebrer_í_as?_i', xpos=[' i\\b']) + #17
lema('[Pp]_á_jaros?_a', xpos=[' Dunes']) + #135
lema('[Pp]anader_í_as?_i', xpos=['\.blogspot']) + #51
lema('[Pp]arasitolog_í_as?_i', xpre=['\\be ']) + #16
lema('[Pp]atri_ó_tic[ao]s?_o', xpre=['Ação '], xpos=[' di\\b']) + #50
lema('[Pp]edi_á_tric[ao]s?_a', xpos=[' Bambino']) + #22
lema('[Pp]ertenec_í_(?:a[ns]?|)_i', xpre=['(?:[Ll]a|[Dd]e|[Ss]u) ', '(?:[Ll]as|[Ss]us) ']) + #118
lema('[Pp]olicl_í_nicos?_i', xpre=['estación\)\|\'\'\'', 'Viale del ', 'Nápoles\)\|', 'estación\)\|'], xpos=[' \((?:Metro de Nápoles|estación)']) + #19
lema('[Pp]on_í_a[ns]?_i', xpre=['Adiós ']) + #50
lema('[Pp]resb_í_ter[ao]s?_i', xpre=['F\. ']) + #124
lema('[Pp]resid_í_a[ns]?_i', xpre=['fueron ', 'plural \'\'\'']) + #19
lema('[Pp]ris_o_n_i[oó]', pre='[Ii]n ') + #2
lema('[Rr]adiograf_í_as?_i', xpos=[' (?:d´una|di)\\b']) + #21
lema('[Ss]_ó_tano_o', xpre=['\'', 'Zorocrates ', 'Piaggine ']) + #63
lema('[Ss]_ú_per As_u', xpos=[' d’Or']) + #36
lema('[Ss]acrist_í_as?_i', xpos=[' Vecchia']) + #34
lema('[Ss]entir_á_[ns]?_a', xpre=['\\bet ']) + #2
lema('[Ss]ovi_é_tic[ao]s?_e', xpre=['E\. ', 'Saussurea ', 'Euglossa ', 'Unione ']) + #162
lema('[Ss]ulf_ú_ric[ao]s?_u', xpre=['Dipoena ']) + #5
lema('[Ss]upremac_í_as?_i', xpre=['\\be ']) + #35
lema('[Tt]_é_rmica_e', xpre=['Centrale ']) + #29
lema('[Tt]ar_j_etas?_g', xpre=['amb ']) + #5
lema('[Tt]elefon_í_as?_i', xpos=[' Nas']) + #52
lema('[Vv]en_z_(?:a[ns]?|o)_s', xpre=['Sant '], xpos=[' (?:Klicic|Dolonc)']) + #7
lema('[l]e_í_a_i', xpre=['Wo ', 'Doriopsilla ']) + #8
lema('[t]ra_í_an_i', xpos=[' in\\b']) + #4
lema('_Á_rea (?:[Mm]etropolitana|[Cc]hica|Natural|Local|[Cc]onurbada|[Bb]iogeogr[áa]fica|[Rr]ecreativa)\\b_A', xpre=['l\'']) + #484
lema('_Á_rea de\\b_A', xpre=['Council ']) + #484
lema('_Ú_ric(?:as|os?)_U', xpos=[' Schmitdt']) + #4
lema('_é_l (?:anhela|pued[ae]|gana)_e', xpre=['l\'']) + #168
lema('_é_l (?:est(?:ar|)[aá]n?|estaba|estará|estuvo|estar[ií]an?|dijo|dir[aá]|dice|vienen?|fu[ée]|fueron|vendr[aá]n?|tiene|tuvo|ten[ií]a[ns]?|tendrán?|es|era|serán?|fue|hab[ií]a|sabe|sab[ií]a|no le)_e', xpre=['l\'']) + #583
lema('_é_l ha_e', xpre=['(?:ch\'|Af\')']) + #583
lema('_é_l[:]_e', pre='(?:[Aa]|[Dd]e|[Cc]on|[Ee]n|[Pp]or|[Hh]acia) ', xpre=['limita ']) + #1816
lema('_é_l[;]_e', pre='(?:[Aa]|[Dd]e|[Cc]on|[Ee]n|[Pp]or|[Hh]acia) ', xpre=['limita ']) + #1816
lema('_é_pic(?:as|os?)_e', xpre=['Scontro ']) + #12
lema('_é_l[.]_e', pre='(?:[Aa]|[Dd]e|[Cc]on|[Ee]n|[Pp]or|[Hh]acia) ', xpos=['\.\.']) + #275
lema('_é_l[,]_e', pre='(?:[Aa]|[Dd]e|[Cc]on|[Ee]n|[Pp]or|[Hh]acia) ', xpos=[' (?:este|ya|hoy|entonces|abarrotado|en ese|relativamente|ahora|por)']) + #275
lema('_é_xitos?_e', xpos=['\.com']) + #214
lema('[Cc]_ó_digo_o', xpre=['<'], xpos=[' (?:Group|commercial|Manuelino|Afonsino)']) + 
lema('[Ff]_ó_rmulas?_o', pre='(?:[Ll]as?|[Uu]nas?|[Dd]e) ', xpre=['quién '], xpos=[' (?:One|Romani|della)', ]) + #755
lema('_h_oland[eé]s_H', pre='\\b(?:e[ln]|del?|idioma|y) ', xpre=['Diplomado '], xpos=[' (?:[Ee]rrante|[Vv]olador)']) + 
lema('M_é_xico_e', pre='(?:[Dd]e|[Ee]n|[Ss]obre|[Pp]ara|[Pp]or|[Tt]odo) ', xpre=['Chanteur ', 'Audrain ', 'Bassin ', 'Humaines ', 'Histoire ', ], xpos=[' (?:Herpetology|City|Beach)', '[\']s', ]) + #960
lema('[Aa]rt_í_culo_i', xpos=[' (?:mortis|meni)', ]) + #948
lema('[Gg]_é_nero_e', pre='(?:[Ee]l|[Ee]ste|[Un]|[Dd]el?) ', xpre=['[Rr]ío '], xpos=['(?:…|\.com)']) + #848
lema('[Pp]a_í_s_i', pre='(?:[Aa]l|[Cc]ada|[Dd]el|[Ee]l|[Uu]n|[Ss]u|[Mm]i|[Nn]uestro|gran|pequeño|[Ee]ste|[Dd]icho|[Pp]or|[Cc]ualquier) ', xpre=['d\' ', 'd\'D\'Amics ', ], xpos=['\.es', ' (?:dels|Valenci[aàá]|Basc|de les caramelles)', ]) + #808
lema('_ú_ltima_u', pre='[Dd]e ', xpos=[' ratio']) + #677
lema('[Pp]_ú_lico_u', pre='(?:[Aa]cceso|[Aa]cto|[Aa]seo|[Aa]cusador|[Aa]gente|[Aa]lumbrado|[Aa]l|[Aa]lboroto|[Aa]rtículo|[Áá]mbito|[Bb]achillerato|[Bb]alneario|[Bb]astante|[Bb]ien|[Cc]amino|[Cc]argo|[Cc]ar[áa]cter|[Cc][ée]sped|[Cc]olegio|[Cc]omponente|[Cc]oncurso|[Cc]onocimiento|[Cc]ontador|[Cc]on|[Cc]r[ée]dito|[Cc]rematorio|[Cc]ulto|[Dd]ebate|[Dd]el?(?: difícil|)|[Dd]erecho|[Dd]esorden|[Dd]inero|[Dd]ominio|[Dd]éficit|[Ee]dificio|[Ee]l(?: gran|)|[Ee]mpleado|[Ee]ndeudamiento|[Ee]n|[Ee]nte|[Ee]nemigo|[Ee]spacio|[Ee]spejo|[Ee]ste|[Gg]asto|[Ff]in|[Ff]uncionario|[Ii]nterés|[Ii]nstituto|[Ii]nvestigación|[Ll]lamamiento|[Ll]ugar|[Mm]anifiesto|[Mm]ercado|[Mm]inisterio|[Mm]irador|[Mm]ucho|[Nn]otario|[Nn]umeroso|[Oo]brero|[Oo]jo|[Oo]rden|[Oo]rganismo|[Pp]arking|[Pp]arque|[Pp]ersonaje|[Pp]oder|[Pp]resupuesto|[Pp]roblema|[Pp]roceso|[Pp]uesto|[Rr]egistro|[Rr]astro|[Rr]eloj|[Ss]ector|[Ss]ervicio|[Ss]ervidor|[Ss]in|[Ss]u(?: propio|)|[Tt]el[ée]fono|[Tt]ecnológico|[Tt]odo|[Tt]ransporte(?: urbano|)|[Tt]rabajo|[Uu]n|[Uu]so|entre|frontón|hacer?|hará|haría|hecho|hiciera|hicieron|hizo|mayor|más|mismo|nuevo|numeroso|para|tenía) ', xpos=['\.es']) + #669
lema('[Hh]ist_ó_ricos?_o', xpre=['Boletim ', 'romànico ', 'Illimani ', 'Études ', 'medicorum ', 'Estudo ', 'Lesbio ', '[Aa]no ', 'do Patrimonio ', ], xpos=[' (?:Naturalia|do|no|[Aa]sturiensia)\\b', ', biographico', ' et ', ]) + #658
lema('[Dd]emogr_á_fic[ao]s?_a', xpre=['Bilancio ', 'storia ', ]) + #592
lema('(?:[Aa]|[Dd]e)__l (?:equipo|resto|primer|grupo|pueblo|personaje|nombre|[Rr]ey|programa|club|presidente|nuevo|álbum|municipio|planeta|número|estado|centro|trabajo|productor|padre|mundo|lugar|jugador|gobierno|país|margen|juego|incremento|gran|estudio|elenco|desarrollo|cuarto|antiguo|verdadero|usuario|[uú]ltimo|tema|poder|oeste|momento|español|otro|entonces)_ e', xpre=['(?:[Ll]ado|[Cc]ara) ', '\.', ]) + #539
lema('[Ii]m_á_genes_a', xpos=[' Librorum']) + #527
lema('[Bb]ater_í_as?_i', xpre=['[Rr]ainha de ']) + #524
lema('_ha_ (?:jugado|labrado|lanzado|liberado|limitado|llegado|llenado|llevado|logrado|manejado|marcado|mantenido|matado|mejorado|mencionado|modelado|modernizado|mostrado|multiplicado|nacido|obtenido|observado|ocupado|ofrecido|ordenado|participado|peleado|perdido|permanecido|permitido|perseguido|pertenecido|podido|pose[ií]do|presentado|probado|promovido|propagado|prosperado|provocado|publicado|quedado|realizado|recibido|recuperado|regresado|registrado|renunciado|repercutido|replanteado|representado|respondido|restaurado|retenido|retratado|reunido|revelado|revisado|revolucionado|sabido|sacado|señalado|separado|sido|sobrevivido|sostenido|sufrido|sugerido|superado|suspendido|sustituido|tenido|terminado|tocado|tomado|trabajado|tra[ií]do|transcurrido|transformado|trasladado|tratado|ubicado|usado|utilizado|variado|vendido|venido|viajado|visto|vivido|vuelto)_ah?', xpre=['[0-9]', ]) + #501
lema('[Nn]_ú_meros?_u', pre='(?:[Ll]a|[Ee]l|[UuEe]n|[Ll]os|[Uu]nos|[Ss]u|[Ss]in|[Gg]ran|[Cc]iertos?|[Ee]s(?:te|tos|se)) ', xpre=[' il '], xpos=[' (?:Piccoli|indefinito)']) + #520
lema('[Pp]el_í_culas?_i', xpos=['(?:\.disneylatino|\.info|9)']) + #654
lema('[Cc]r_é_dito_e', xpre=['\\bdi ', ], xpos=[' (?:in|Italiano|Artigiano|Valtellinese|Bergamasco|Emiliano|and|per|Varessino|Esattorie)', ]) + lema('[Cc]r_é_ditos_e',xpre=['\\blo ', 'Pizze a '], xpos=[' in\\b', ]) + #311
 
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

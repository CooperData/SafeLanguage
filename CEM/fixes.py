#-*- coding: utf-8  -*-
"""
File containing all standard fixes

"""

## (C) Pywikipedia team, 2008-2013
#
__version__ = '$Id: 7f8e4f43cbc314ed076fc1cd36e81f2a691728c1 $'
#
# Distributed under the terms of the MIT license.
#
import re, string
from subprocess import call
from datetime import date
import urllib
help = u"""
                  * HTML        - Convert HTML tags to wiki syntax, and
                                  fix XHTML.
                                    **) NOTE below
                  * isbn        - Fix badly formatted ISBNs.
                                    **) NOTE below
                  * syntax      - Try to fix bad wiki markup. Do not run
                                  this in automatic mode, as the bot may
                                  make mistakes.
                  * syntax-safe - Like syntax, but less risky, so you can
                                  run this in automatic mode.
                                    **) NOTE below
                  * case-de     - fix upper/lower case errors in German
                  * grammar-de  - fix grammar and typography in German
                  * vonbis      - Ersetze Binde-/Gedankenstrich durch "bis"
                                  in German
                  * music-de    - Links auf Begriffsklärungen in German
                  * datum-de    - specific date formats in German
                  * correct-ar  - Corrections for Arabic Wikipedia and any
                                  Arabic wiki.
                  * yu-tld      - the yu top-level domain is disabled
                  * fckeditor   - Try to convert FCKeditor HTML tags to wiki
                                  syntax.
                                  http://lists.wikimedia.org/pipermail/wikibots-l/2009-February/000290.html

                                    **) NOTE: these fixes are part of the
                                        cosmetic_changes.py. You may use
                                        that script instead.

"""

reg = re.compile(ur'_')
def lemaB(pat, izq, der, mostrar):
    """match patterns"""
    #print "Wrong pattern: %s" % (pat)
    p = reg.split(pat)
    if len (p) < 4:
        print "Wrong pattern: %s" % (pat)
        #raise LemaExc(pat)
    if len (p) == 5:
        fl = ur'(?i)'
    else:
        fl = ur''
    #Contexts
    res = [(fl + izq + p[0] + ur')' + p[3] + 
            ur'(?P<r>' + p[2] + der,
            ur'\g<l>' + p[1] + ur'\g<r>')]
    if mostrar:
        print( res )
    return res

alpha = ur'[-a-zæǣçäëöüãâêàèìòùáéíóúñžŕA-ZÆÇÄËÖÜÃÂÊÀÈÌÒÙÁÉÍÓÚÑŽŔß_/ÐðŜŝĒēŠšÏïÞþÔôÕõŁłŌōŢţςйкŋνĀāŶŷṣṢņŅŪūČčʈƉɖĂăˈṀṁĬĭṂṃŞşŻżĆćĞğıĄąĪīȚțŇňŘřØøĞğΒβŚśŹźŃńÝýḤḥḌḍ]'
noUsado = '_XyZyX'
def lema(pat, pre=ur'', xpre=[], xpos=[], mostrar=False):
    xpres = ur''
    for p in xpre:
        xpres += ur"(?<!"+p+ur")"
    xposs = ur''
    for p in xpos:
        xposs += ur"(?!"+p+ur")"
    return lemaB(pre+pat,xpres+ur'(?<!' + alpha + ur')(?P<l>', ur')(?!' + alpha + ur')'+xposs, mostrar)
def retro(pat):
    p = reg.split(pat)
    if len (p) < 5:
        print "Wrong pattern: %s" % (pat)
    return lema(p[1]+noUsado+'_'+p[3]+'_'+p[4]) + lema(p[0]+p[1]+'_'+p[4]+'_'+p[3]+noUsado) + lema(p[1]+'_'+p[2]+'_'+p[3]+noUsado)
def retroX(pat):
    return lema(pat)

noCorregirEn =  [ ur'(?i)(?:(?:[Ii]magen?|[Ff]ile|[Aa]rchivo):[^\|\]]+(?=[\]\|]))',
                  ur'(?i)(?:(?:https?|mailto|ftp)://[{|}\w“\\@/%.\$\-_¿?&=:;\'\~+*,()#!]+)',
                  ur'(?i)(?:(?<=\[\[):?[-a-z]+:[^\]]+(?=\]\]))',
                  ur'(?i)(?:\[\[ *[Cc]ategor(?:y|ía) *:[^\]]*\]\])',
                  ur'(?i)style *= *\"[^\"]*\"',
                  ur'(?i)(?:[23]|2\.5|2\.75)[G]',
                  ur'(?i)<\!--[\s\S]*?-->', #¿Demasiado lento?
                  ur'(?i)<(?:ref|source|syntaxhighlight|math|code|pre|cite|blockquote|nowiki|timeline|gallery|poem)[^>]*/>', 
                  ur'(?i)<(ref|source|syntaxhighlight|math|code|pre|cite|blockquote|nowiki|timeline|gallery|poem)[^>]*>[\s\S]*?</\1>', 
                  #ur'(?i)<math>[\s\S]*?</math>', 
                  #ur'(?i)<code>[\s\S]*?</code>', 
                  #ur'(?i)<pre>[\s\S]*?</pre>', 
                  #ur'(?i)<cite>[\s\S]*?</cite>', 
                  #ur'(?i)<blockquote>[\s\S]*?</blockquote>', 
                  #ur'(?i)<nowiki>[\s\S]*?</nowiki>', 
                  #ur'(?i)<timeline>[\s\S]*?</timeline>', #OK Ene 06
                  #ur'(?i)<ref .*?>[\s\S]*?</ref>', Esconde demasiado!!
                  #ur'\{\{[^{}]*?\}\}',
                  ur'(?ims)\{\{ *(?:[Vv]ersalita|ca|it|es|fr|en)\b.*?\}\}', #Orden:antes de cita
                  ur'(?ims)\{\{ *(?:BD|[Dd]emografía|[Tt]witter|Categorias taxonomicas etiquetadas|caja de cita|[Ww]ikisource|[Ff]acebook|[Qq]uote|Chess diagram|Diagrama de ajedrez|[Cc]ita|[Bb]otánico|redirige|player2|c?qoute|wide image|audio|AFI|cit[ae] (?:web|libro|book|journal|publicación)|fusionar|gMaps|MySpace|img_panorama_urb|interproyecto|ipr|info|[Ll]ang|[Ll]ang-[a-z]+|nihongo|vocabulario portuñol|wikificar|ordenar|defaultsort|NF|BANDERA VISITA|traducido ref|panorama|commonscat|imagen|PAGENAME|Mapa\.Ciudad\.Tamaño\.2|Wikipedia grabada|quotation|commons|indice|ta|Galería de imágenes|image_skyline|springer|sort|desambiguacion|\#tag:ref|[Ss]fn|Harvnp|SNB 2012-2013 Estado de los Equipos Segunda Fase|Copa America Paraguay 1999|Codificacion caracteres|aut|Imdb|otros usos|refn|wikispecies|l-medlineplus|medlineplus|USS).*?\}\}',
                  ur'(?<=\{\{)[^|{}<>]+?(?=\|)',
                  ur'(?:[Aa]breviatura_zoo|[Aa]rchivo_himno|[Aa]rchivo|[Bb]D|[Bb]andera_[ps][1-9]|[Bb]andera|[Bb]ase|[Bb]otánico|[Cc]amiseta[1-9]?|[Cc]arátula|[Cc]ategoría-Commons|[Cc]over|[Cc]oa_pic|[Dd]ata-sort-value|[Ee]scudo[0-9]*|[Ee]structura[1-3]|[Ff]acebook|e-mail|[Ff]ilename|[Ff]irma|[Ff]oto[0-9]*[abc]?|[Ff]oto[1-9][ab]?|[Hh]imno|[Ii]mage_flag|genus|[Ii]mage_map|mapa_loc|mapa_alternativo_1|[Ii]magen principal[2-9]?|[Ii]magen[0-9]*|[Ii]magen_escudo|nombre_nativo|[Ii]mageninferior|[Ii]magensuperior|[Ii]mage|[Ii]mg1|[Ii]mg_panorama_urb|[Ii]nsignia|[Jj]ugador de fútbol|[Ll]ink|[Ll]ogo|[Mm]apa[0-9]*|[Mm]ultimedia|[Nn]ombre|[Nn]ombre_imagen|[Pp]anorama|[Pp]atrón_cuerpo|image_skyline|[Rr]ange_map|[Ss]ello|[Ss]itio_web|[Ss]onido|[Tt]itulo|[Ww]eb|Website|[Íí]ndice|[Ff]irma|[Cc]allsign)[ \t]*?=[^\n|]*?(?=[\n|])',
                  ur'(?i)\|\s*[- _a-z0-9áéíóúü]*\s*=',
                  ur'«[^»]+»',
                  ur'&[a-zA-Z]+;',
                  ur'^ .*$'
                  #ur'\| *[a-z0-9]* *=',
                  #ur'\{\{[Cc]ita\|.*?\}\}',
                ]

excluir = [
    ur'Selenio 79', #Se se
    ur'Ultracorrección', #Esta agua
    ur'Anexo:Jueces federales de Estados Unidos', #Gonzalez
    ur'Anexo:Miembros de la Academia Brasileña de Ciencias', #Perez
    ur'Parana (Lena)', #Parana
    ur'La leyenda de los hombres más guapos del mundo', #Cansión
    ur'On the Floor', #Lopez
    ur'Reforma Ortográfica de 1911', #:pt
    ur'Albares de la Ribera', #osp
    ur'Copa Desafío Europeo de Rugby 2016-2017', #Caprichos del autor
    ur'Alton Towers', #Galactica, Nemesis
    ur'Anexo:Jueces federales de Estados Unidos', #Gonzalez
    ur'Anexo:Miembros de la Academia Brasileña de Ciencias', #Perez
    ur'Parana (Lena)', #Parana
    ur'Gramática del finés', #Adeisvo
    ur'Gerry Merito', #Merito
    ur'Stars Dance', #Gomez
    ur'Joan Manuel Serrat: Cansiones', #Cansiones
    ur'Joan Manuel Serrat', #cansiones
    ur'Adios (álbum)', #Adios
    ur'Philip K. Dick', # Ciencia Ficción
    ur'Saw VI', #Perez
    ur'Anexo:Músculos del cuerpo humano', #tendon
    ur'Ångström (distribución)', #Boxer
 ur'Luis de Llera Esteban', #Varios
 ur'Anexo:Géneros de astéridas', #Avería Grafia Medica
 ur'Idioma finés', #Adesivo
 ur'Chrysalis (película de 2014)', #Abrira
 ur'Anexo:Plantas de las calles de Rosario, Argentina', #9 de Julio
 ur'Historia del Club Atlético de Madrid', #el Español
 ur'Antonio Piedade da Cruz', #Cruzo
 ur'Luciana by Night', #Gimenez
 ur'Saw IV', #Perez
 ur'Málaga (desambiguación)', #Malaga
 ur'Sístole (figura literaria)', #habia
 ur'Refutación', #y afirmo
 ur'Independiente Santa Fe', #Civico
 ur'Himno nacional de Chile', #{{cita .. {{versalita .. }} dia
 ur'Colibri', #Colibri
 ur'Acuerdo ortográfico de la lengua portuguesa de 1990', # amnistia
 ur'Soy (álbum de Lali Espósito)', #Unico
 ur'Facundo Regalia', #Regalia
 ur'Benegida', #osp
 ur'UD Trucks', #Condor
 ur'Reia (lenguaje de programación)', #Reia
 ur'Dance Again: The Hits', #Lopez
 ur'Dance Again World Tour', #Lopez
 ur'Grupo B', #los grupo B
 ur'Jennifer Lopez: All I Have', #Lopez
 ur'Artur Mas', #Mas
 ur'Idioma mataco', #lo compro
 ur'Antigua Universidad de Perpiñán', #Garcia. Ladron
 ur'Anexo:Pequeños cuadrados latinos y cuasigrupos', # espacios eliminados en líneas que comienzan con espacio
 ur'Conjugación de verbos muiscas', #azoto
 ur'Arquitectura de Barcelona', #Basilica
 ur'Declinación del latín', #consul, :la
 ur'Anexo:Discografía de Jennifer Lopez', #Lopez
 ur'Politico (periódico)', #Politico
 ur'Idioma español en el Perú', #la agua
 ur'Domingo (obispo segobricense)', #Perez
 ur'Jennifer Lopez', #Lopez
 ur'AS Industria Sârmei Câmpia Turzii', #Energia
 ur'Bill Willingham', #Comico
 ur'Ordenación de montes: los alcornocales andaluces', #:es ant
 ur'Anexo:Lemas_nacionales', #varios
 ur'Anexo:Álbumes de Clave', #Totem
 ur'Anexo:Álbumes de De la planta', #Totem
 ur'Goldenwings', #Totem
 ur'Totem (película)', #Totem
 ur'Huancavelica', #Belica
 ur'Firmiliano de Cesarea', #Ibidem
 ur'Filosofía del espacio y el tiempo', #Ibidem
 ur'Grateful Dead', #Garcia
 ur'Campaña de fe', #ibid
 ur'Germán Cueto', #Idem
 ur'Georg Lukács', #Ibidem.
 ur'Shpend Sollaku Noé', #Antologia poetica
 ur'1/2 falta', #Formo
 ur'George Lopez', #Lopez
 ur'Evacuaciones de civiles durante la Operación Atila', #agosto, 5300
 ur'Lorcha', #osp
 ur'Algoritmo de Emparejamiento de Edmonds', #vertices
 ur'Love You Like a Love Song', #Gomez
 ur'Come & Get It (canción de Selena Gomez)', #Gomez
 ur'Patrizia Panico', #Panico
 ur'Ciudad global', #Cebu
 ur'Instituto de Historia Argentina y Americana "Dr. Emilio Ravignani"', #25 de mayo 221
 ur'Joan Cornudella', #biografia (en una cita??)
 ur'Prima della pioggia - Sila in festa', #Oceano
 ur'Oceano (California)', #Oceano
 ur'Revolution (álbum de Tiësto)', #Melodica
 ur'Luis Iberico Núñez', #Iberico
 ur'Márcia Tiburi', #filosofia
 ur'Lubomyr Husar', #husar
 ur'Anexo:Proyectos crowdsourcing', #En inglés
 ur'Giuseppina Alongi', #Biologia Marina Mediterranea
 ur'El Comulgatorio', #compañia
 ur'Black Rock Shooter', #Mato
 ur'Judeoespañol calco', #¿Porque sere
 ur'José de Valdivielso', #Concepcion
 ur'Álvaro Obertos de Valeto', #eclesiasticos,
 ur'Tomás Tamayo de Vargas', #OSP
 ur'Sitio clasificado o inscrito', #novembre
 ur'Rincón (California)', #Rincon
 ur'Rincón (Bonaire)', #Rincon
 ur'Rincon (Georgia)', #Rincon
 ur'Anexo:Planos, líneas y regiones', #Linea
 ur'Alinéa', #linea
 ur'10.000 Days', #Intension
 ur'Gorilla Glass', #Asus
 ur'Verbo copulativo indoeuropeo', #està
 ur'Liston', #liston
 ur'Catalán barcelonés', #dónes
 ur'Monasterio de San Martín de Jubia', #podiamos
 ur'Historia de la bandera de Argentina', #habia
 ur'Iglesia de San Salvador y Santo Domingo de Silos (Córdoba)', #delos
 ur'Concepción de Ataco', #Ataco
 ur'Lenguas cushitas orientales de las tierras altas', #mato
 ur'Tenencia de Puerto Viejo', #es ant.
 ur'Catalanidad de Cristóbal Colón', #es. ant.
 ur'Josè Zatrilla y Vico Dedoni y Manca', #Mexico
 ur'Bernardino Álvarez', #proximo
 ur'Juan Lorenzo Palmireno', #epistolas
 ur'Marquesado de Monte Olivar', #camara
 ur'Gramática del latín', #consules
 ur'Consul (animal)', #Consul
 ur'The Quantum Enigma', #Epica
 ur'Anexo:Calzadas romanas', #Via
 ur"Asa'pili", #gano
 ur'Economía solidaria', #Projecto
 ur'Colera', #Colera
 ur'Incidente de Muhammad al-Durrah', #novembre 2007
 ur'Batalla de Romani', #Romani
 ur'Irma Gramatica', #Gramatica
 ur'Haloalcano', #Espacios
 ur'Gabriel González Videla', #Naci
 ur'Radio Caroline', #Laser
 ur'Anexo:Planeadores', #Condor
 ur'The Human Centipede (First Sequence)', #laser
 ur'Silfio', #laser
 ur'Anexo:Tribus romanas', #Galeria
 ur'Utopia (canción de Within Temptation)', #Utopia
 ur'Mitología finesa', #Agricola
 ur'Ford Laser', #Laser
 ur'Grendel', #Mas
 ur'Anexo:Estrellas con imágenes resueltas', #30 mas
 ur'Bicicletas, Bolos e Outras Alegrias', #Vá
 ur'Anexo:Personajes de Mobile Suit Gundam Wing', #Duo
 ur'Idioma romaní', #Romani
 ur'Pian (enfermedad)', #Pian
 ur'Pendulo Studios, S.L.', #Pendulo
 ur'Alfara de la Baronía', #Baronia
 ur'Idioma chamorro', #adios
 ur'Glosas de Reichenau', #femur
 ur'Anexo:Toponimia de las islas Malvinas', #Galpon
 ur'(2745) San Martin', #Martin
 ur'BMW', #boxer
 ur'Cáncer (constelación)', #Cancer
 ur'Concilios nacionales', #Perez
 ur'Dubái', #Dubai
 ur'Bóxer', #Boxer
 ur'Catalán ribagorzano', #sentia
 ur'Proton-M', #Proton
 ur'Anexo:Publicaciones periódicas francófonas de BD', #fr
 ur'Climax (álbum)', #Climax
 ur'Sustantivos femeninos que empiezan por a- o ha- tónicas', #este águila
 ur'Tandem', #Tandem
 ur'Twin Spica', #Asumi
 ur'Star Wars: Episode V - The Empire Strikes Back', #Leia
 ur'Anexo:Géneros de Scrophulariaceae', #Graderia
 ur'Anexo:Géneros de plantas', #Bahia
 ur'Gramática del esperanto', #via
 ur'Odoardo Spadaro', #Lirico
 ur'Escultura del Renacimiento en Aragón', #Arabe
 ur'Guarda (Portugal)', #fria
 ur'Agustí Pons', #poesia
 ur'Liquido', #liquido
 ur'José María Asensio', #dirijidas
 ur'Toponimia de la Comunidad Valenciana', #Basilica
 ur'Torre Solaria', #arquitectonica
 ur'Anexo:Revistas científicas de química', #farmaco
 ur'Arquitectonica (Miami)', #arquitectonica
 ur'Agrícola (Tácito)', #agrícola o agrícola
 ur'La Santissima Trinità', #teologia
 ur'El Villar (Madrid)', #:es ant
 ur'Talita Fontoura Alves', #:pt
 ur'I\'m Not Missing You', #Pias
 ur'Revival (álbum de Selena Gomez)', #Gomez
 ur'Leonor de Aragón y Foix', #Lo tres
 ur'Pedro I de Castilla', #Apologia
 ur'Festival Internacional de Cine de Venecia de 2014', #Perez
 ur'Rickard Rydell', #Menu
 ur'RML Group', #Menu
 ur'Michel Menu', #Menu
 ur'Alain Menu', #Menu
 ur'Juan Bautista Carrasco', #Geografia
 ur'Francisco Ximénez (monje)', #Metodo
 ur'Yurikuma Arashi', #Reia
 ur'Gaspar Navarro', #dió
 ur'Almeria (Nebraska)', #Almeria
 ur'Almería (desambiguación)', #Almeria
 ur'Almeria (Alabama)', #Almeria
 ur'The Bachelor (temporada 18)', #Alli
 ur'Los desastres de la guerra', #razon, mas
 ur'A.K.A. (álbum)', #Lopez
 ur'Contrafactum', #habra
 ur'Habra', #Habra
 ur'Badiraguato', #dira
 ur'Sexenio de Morella', #estara
 ur'Por medio de la fuerza (Star Trek: La serie original)', #Daras
 ur'Dialectos del euskera', #dira
 ur'Alfonso Bayard', #Dira
 ur'Anexo:Sexta temporada de Face Off', #Daran
 ur'Sofa (guerrero)', #sofas
 ur'Imperio de Malí', #sofas
 ur'Anexo:Vocabulario indoeuropeo (no sustantivos)', #haras
 ur'Vocabulario indoeuropeo (sustantivos)', #haras
 ur'Johannes Althusius', #politica
 ur'Quentin Skinner', #Teoria politica
 ur'Fortaleza de San Juan Bautista', #Bateria
 ur'Anton Francescu Filippini', #Mediterrranea
 ur'Giovanni Gentile', #La Critica
 ur'Bergida', #Belgica
 ur'Selena Gomez', #Gomez
 ur'Expedición Antártica Belga', #Belgica
 ur'Nautica Thorn', #Nautica
 ur'Pierre Boaistuau', #y iquisidor
 ur'Makinavaja (serie de televisión)', # cuidalse
 ur'Olga Dondé', #Dondé
 ur'Chueta', # an
 ur'Busto de San Pedro apóstol (Ayerbe)', # an
 ur'Feria Tabasco', #preferia
 ur'Verbo copulativo indoeuropeo', #estan
 ur'Unico', #Unico
 ur'Estebanillo González', #Gonzalez,
 ur'Elizabeth de Araujo Schwarz', #Taxonomia
 ur'Expedición de Francisco César', #dió
 ur'El padre Horán', #aqui
 ur'Ido', #nacio
 ur'Michael Angelo Batio', #Batio
 ur'Dialectos del catalán', #tenia
 ur'Sylvano Bussotti', #alfabetico
 ur'Silva de Sirenas', #Cancion
 ur'Se canta', #se canto
 ur'Conjugación de verbos auxiliares en catalán', #estan
 ur'Conjugación de verbos regulares en catalán', #perdera
 ur'Anexo:Cronología de la condición femenina', #sera
 ur'José Luis Fontenla', #Antologia
 ur'Libertas quæ sera tamen', #sera
 ur'Juan Francisco de Villava', #devocion...
 ur'Claudio Clemente', #mas, poblacion, ...
 ur'Luciano Urízar', #Refrencia
 ur'Luis Esteso y López de Haro', #dió
 ur'Jaume Casals', #filosofia, apologia
 ur'Víctor Amela', #Antologia
 ur'Premiata Forneria Marconi', #Antologia
 ur'Picap', #Antologia
 ur'Paulo de Carvalho', #Antologia
 ur'Ovidi Montllor', #Antologia
 ur'Maria Teresa Horta', #Antologia
 ur'Maria Marly de Oliveira' #Antologia
 ur'La Trinca', #Antologia
 ur'La muerte (libro)', #Antologia
 ur'Josep Piera', #Antologia
 ur'Jordi Pàmias i Grau', #Antologia
 ur'Joan Fuster', #Antologia
 ur'Jaime Zuzarte Cortesão', #Antologia
 ur'Inês Pedrosa', #Antologia
 ur'Carlos Mendes (cantante)', #Antologia
 ur'Augusto Meyer', #Antologia
 ur'Arnaldo Antunes', #Antologia
 ur'José Cid', #Antologia
 ur'Emilio Coco', #Antologia
 ur'Valter Hugo Mãe', #Antologia poética
 ur'Karen Dejo', #Dejo
 ur'Danza Prima', #Dejo
 ur'Armored Core: For Answer', #Algebra
 ur'(1154) Astronomia', #Astronomia
 ur'Anexo:Fuentes musicales del Renacimiento de España', #Alia
 ur'Dune', #Alia
 ur'Diff', #espaciado
 ur'Maria Corti', #autografo
 ur'Descripción general de África', #descripcion
 ur'Juan José Heydeck', #Serenisima
 ur'Anguta', #Regante serenisimo
 ur'Unión de Bibliófilos Taurinos', #huvo
 ur'Federico Santa María', #Dejo
 ur'Pedro de Portocarrero', #Inquisicion
 ur'Justino Matute y Gaviria', #Inquisicion
 ur'Jerónimo de la Quintana', #Inquisicion
 ur'Libro Verde (Aragón)', #Inquisicion
 ur'Francisco José Orellana', #Inquisicion
 ur'Fernando Niño de Guevara', #Inquisicion
 ur'Francisco de Borja Palomo y Rubio', #Coleccion
 ur'Heero Yuy', #Duo
 ur'Biblioteca de la Academia de Artillería', #es ant.
 ur'Leonés (asturleonés de León y Zamora)', #y iguales
 ur'La Docena', #dejo
 ur'Juan Ponce de León', #y indios
 ur'Francisco Luque Fajardo', #Compañia
 ur'Reflexion', #reflexion
 ur'The Addams Family (serie de 1964)', #Gomez
 ur'OS X', #El capitan
 ur'Avion (Paso de Calais)', #Avion
 ur'The Addams Family (musical)', #Gomez
 ur'Alberto Ginastera', #rustico
 ur'Dialéctica', #Dialectica
 ur'Biblioteca Nacional de la República Argentina', #es
 ur'Juan Rodríguez Cabrillo', #es 
 ur'Español dominicano', #es
 ur'R2*D3', #aqui
 ur'Stripped (canción)', #No esta noche
 ur'Juan Andrés Ricci', #es ant.
 ur'Sebastião da Gama', #Biografia Projecto
 ur'Athanasio de Lobera', #y insigne
 ur'La la la (álbum)', #La la la
 ur'Anexo:Episodios de Gundam Wing', #Duo
 ur'El gran juego de la oca', #Dado a dado
 ur'Anexo:Gentilicios de Estados Unidos', #neoyorkino
 ur'Ngungunhane', #pt
 ur'Diego Muñoz de Saldaña', #comite
 ur'Paris (Arkansas)', #Paris
 ur'Paris (condado de Grant, Wisconsin)', #Paris
 ur'Paris (condado de Kenosha, Wisconsin)', #Paris
 ur'Paris (Idaho)', #Paris
 ur'Paris (Illinois)', #Paris
 ur'Paris (Kentucky)', #Paris
 ur'Paris (Maine)', #Paris
 ur'Paris (Misuri)', #Paris
 ur'Paris (Nueva York)', #Paris
 ur'Paris (Pensilvania)', #Paris
 ur'Paris (Tennessee)', #Paris
 ur'Paris (Texas)', #Paris
 ur'Anexo:Lista de Martínez Compañón', #Reir
 ur'Armonía consonántica', #lo dejo
 ur'Jean Guillou', #organo 
 ur'Reverse Theme Music', # Mas o Mas
 ur'Blasterjaxx', #La musica
 ur'Tomás Carlos Capuz', #redencion
 ur'Anny Cazenave', #Del Rio, Rodriguez
 ur'Paul America', #America
 ur'Tres libros de música en cifra para vihuela', #septimo tono
 ur'Octavio (nombre)', #septima, decima
 ur'Idioma asturleonés', #as
 ur'Diasistema', #ca
 ur'Familia apostólica Orsini', #it
 ur'Anexo:Premiados con la Creu de Sant Jordi', #ca
 ur'Acta de Independencia de Chile', #es ant.
 ur'Francisco Hernández de Toledo', #lat.
 ur'Redecilla del Camino', #es ant.
 ur"Anexo:Scachs d'amor, original y traducido", #es ant
 ur'Historia y teoría de la Arqueología', #espacios en blanco
 ur'Carlos Moesta', #es ant.
 ur'Tercera expansión del Imperio incaico', #es ant.
 ur'Jules Lemaître', #Un salon
 ur'Biblioteca Nacional de Chile', #es ant.
 ur'Fernán González', # et comite
 ur'Guerra de la Independencia de Chile', #i libreria
 ur'Comenio', #didactica
 ur'Fuente Álamo (Albacete)', #Cita
 ur'Historia medieval de España', #es ant
 ur'Jumilla', #es ant
 ur'Bryan Singer', #Galactica
 ur'Pedro de Alvarado', #es ant.
 ur'Apolo', #Delos
 ur'Bartolomé de las Casas', #es ant.
 ur'Alemán de Suiza', #ahi
 ur'Quenya', #vá
 ur'Vislumbres de la India', #lo lleno
 ur'No me pises que llevo chanclas', #las dejo
 ur'Escocés (lengua germánica)', #Reir
 ur'Dune', #Menu
 ur'Organización Mundial de Jóvenes Esperantistas', #organizo
 ur'Albert Pla', #la dejo
 ur'Clemens Brentano', #lo lleno
 ur'Santianes (Ribadesella)', #llovio
 ur'Congreso Internacional de Jóvenes Esperantistas', #esperanto
 ur'Ramona Parra', #Los llamo
 ur'Anexo:Episodios de Shin-chan (1998)', #1a persona
 ur'Las Cabañas de Castilla', #Rodriguez
 ur'Elide Pereira dos Santos', #Farmaceutica
 ur'Valenciano', #huir
 ur'Anexo:Detenidos desaparecidos de Argentina', #Cañon
 ur'Dimensión de un espacio vectorial', #????
 ur'Manuscrito de Old Hall', #Delos
 ur'Eusebio Francisco Kino', #&mdash;también
 ur'Valentín Canalizo', #cita
 ur'Andrea Cagnetti - Akelo', #Mediterraneo
 ur'Túpac Yupanqui', #asta
 ur'Gonzalo Fernández de Oviedo', #Quedo
 ur'Altura (Castellón)', #Mas
 ur'Asturiano (asturleonés de Asturias)', #:as
 ur'Chandler Bing', #Lo dejo
 ur'Judith Butler', #afirmo
 ur'Métrica', #asta
 ur'Cantón Piñas', #mas en zonas altas
 ur'Acuerdo ortográfico de la lengua portuguesa de 1990',
 ur'Álex Ubago', #donde quedo
 ur'Alsineae', #queria
 ur'Franco Venturi', #biografica
 ur'António Hespanha', #projecto
 ur'Giorgio Ceragioli', #tecnologica
 ur'Paolo Ruffini', #tecnologia
 ur'Giuseppe Ciribini', #Tecnologia
 ur'Folco Quilici', #Oceano
 ur'Castellanos de Moriscos', #a traído
 ur'Isidoro de Antillón y Marzo', #es ant.
 ur'Échame sifón', #que gano
 ur'Judaísmo y cristianismo', #Mas en términos
 ur'Anexo:Planos de Madrid', #Catolicos
 ur'Cálculo de la raíz cuadrada', #raiz
 ur'Mar de Bronce', #Jerusalen
 ur'Himno de la Comunidad Valenciana', #envia
 ur'Línea 32 de TMB', #calle Artesania
 ur'Nobleza', #ha demostrar
 ur'Alio (Élide)', #Alio
 ur'Kajam', #Caia
 ur'(952) Caia', #Caia
 ur'Maserati Quattroporte', #Automatica
 ur'Rita de Cássia Leone Figueiredo Ribeiro', #Fisiologia
 ur'Nuestra Señora de Loreto (Algezares)', #:es ant
 ur'Movera', #Movera
 ur'Dialectos calabreses', #linguistica
 ur'Victoria de Mindoro', #Leido
 ur'Fernando de Corradi', #segun
 ur'Biblioteca del Congreso Nacional de Chile', #estranjeras
 ur'Rockland (Maine)', #Dirigo
 ur'Ardia (cortometraje)', #Ardia
 ur'Auto de fe', #es ant.
 ur'Erigio', #Erigio
 ur'Lenguas May-kwomtari', #asi
 ur'Xavier Torres', #:ca
 ur'Latín vulgar', #rustica
 ur'Mas que nada', #Mas
 ur'Rechazo del Paraguay a la Junta de Buenos Aires', #abitantes
 ur'Cantón de Servian', #Servian
 ur'Población de América precolombina', #cronica
 ur'Campo de hielo Patagónico Sur', #recojida
 ur'Lorenzo Sundt', #recojio
 ur'Pulgon (Kirguistán)', #Pulgon
 ur'Fierabrás', #huvo
 ur'Spanish Movie', #Ofendia
 ur'Oraciones explicativas', #Indico
 ur'Albrecht Mayer', #Sinfonia Melodica
 ur'Scott Hall', #Razon
 ur'Catalán septentrional', #facil
 ur'Catalán rosellonés', #facil
 ur'Majorette (automóvil)', #Solido
 ur'Víctor Manuelle', #No Alcanzo
 ur'Valparaiso (Nebraska)', #Valparaiso
 ur'Valparaíso (Indiana)', #Valparaiso
 ur'Valparaiso (Florida)', #Valparaiso
 ur'Valparaíso (desambiguación)', #Valparaiso
 ur'Autocorrección', #todavia
 ur'Idioma lombardo (germánico)', #segun
 ur'Potosi (Wisconsin)', #Potosi
 ur'Potosi (condado de Grant, Wisconsin)', #Potosi
 ur'Potosi (Misuri)', #Potosi
 ur'Rosa \'El Capitan\'', #Capitan
 ur'Erica cinerea', #tereno
 ur'Lenguas Omo-Tana occidentales', #fué
 ur'Miquel Pairolí', #:ca
 ur'Joseba Sarrionandia', #Geografia
 ur'Geografía (Ptolomeo)', #Geografia
 ur'Alegría de Surigao', #Alegria
 ur'Juan de la Concepción', #es ant.
 ur'Fosca', #es ant.
 ur'Bernardo Rico y Ortega', #redencion
 ur'Anselmo Duarte', #Simfonia
 ur'Brujería vasca', #las mas 
 ur'Chinesco', #podia
 ur'Ciudad Universitaria Armando de Salles Oliveira', #psicologia
 ur'Titãs 84 94', #Hereditário
 ur'Titanomaquia (álbum)', #Hereditário
 ur'Manuel José Rubio y Salinas', #es ant.
 ur'Inglés malvinense', #Galpon, Rincon
 ur'Francitan', #pichon
 ur'Anexo:Personajes de Spanish Movie', #ofendia
 ur'Prefijos del español', #temio
 ur'Hari Om Sharan', #Sumiran
 ur'Glosas Silenses', #debiles
 ur'De plata (álbum)', #Sólo él y yo
 ur'Oceano (película de 1971)', #Oceano
 ur'Mary Boquitas (álbum)', #fué
 ur'Antonio Vico Camarero', #Llego
 ur'Proteidae', #proteina
 ur'Gabriel Milito', #Milito
 ur'Jean-Jacques de Boissieu', #Paisage
 ur'Decima Flottiglia MAS', #Decima
 ur'Anexo:Áreas no incorporadas de California', #Asuncion,Cadiz, etc.
 ur'Idioma meryam mir', #Esten
 ur'Pierre el Chantre', #proprietarios
 ur'Guion cinematográfico', #truán
 ur'Marco Cornelio Frontón', #aerea
 ur'Rolando Panerai', #sinfonico
 ur'Cohors I Celtiberorum', #aerea
 ur'Giacomo Puccini', #Sinfonico
 ur'Ceratonia siliqua', #es ant
 ur'Diptongo',
 ur'Antonio de León Pinelo (historiador)', #es ant
 ur'Centurión (Battlestar Galactica)', #Galactica
 ur'Battlestar', #Galactica
 ur'Xenosaga', #Galactica
 ur'Kara Thrace', #Galactica
 ur'Battlestar Galactica (Reimaginada)', #Galactica
 ur'William Adama', #Galactica
 ur'Anexo:Episodios de Battlestar Galactica (2003)', #Galactica
 ur'Habia', #Habia
 ur'José María Encontra', #encontra
 ur'Expedición militar de Alfonso I de Aragón por Andalucía', #depues
 ur'Anexo:Especies de Araneidae (A)', #Aereaxs
 ur'Battlestar Galactica', #Galactica
 ur'Gonçalo Byrne', #fotografia
 ur'Alberto Henschel', #fotografia
 ur'Isla Hayes', #Hayes
 ur'Antonio Folch de Cardona', #mas heroyco
 ur'Premio Iluro de Monografia Histórica', #ca
 ur'Marcos de Guadalajara y Javier', #es ant.
 ur'Mas Torre Amela de Forcall', #mas
 ur'Jacint Segura', #es ant.
 ur'Rapallo', #medico
 ur'Conde', #Comite
 ur'Cosme Bueno', #governadores,
 ur'Motor T-Jet', #linea
 ur'Fiat Linea', #linea
 ur'Anexo:Localidades de Florida', #Valparaiso
 ur'Bajada de línea', #linea
 ur'Real Audiencia de Lima', #govierne
 ur'Rede Integrada de Transporte', #Padron
 ur'Los Reyes del Cuarteto', #Cucuta
 ur'Margarida Ribeiro', #Etnografia
 ur'Historia y desarrollo de las Tecnologías de la Información y la Comunicación',# :pt
 ur'Tereo' #tereno
 ur"Rosa 'El Capitan'", #capitan
 ur'Alexandro Álvarez', #mostro
 ur'Shout Out Louds', #optica
 ur'Regino de Prüm', #danes
 ur'Lluís Calvo', #Lerida
 ur'Roberto Cacciapaglia', #Olimpica
 ur'Lenguas omóticas', #oido
 ur'Lenguas ometo', #oido
 ur'Harri Lorenzi', #morfologia
 ur'Magma (banda)', #Fusion
 ur'Il Sedecia, re di Gerusalemme', #Sinfonia
 ur'Davidis pugna et victoria', #Sinfonia
 ur'Agar et Ismaele esiliati', #Sinfonia
 ur'Phlyctaenodini', #taxonomia
 ur'Live (álbum de Winger)', #Generica
 ur'IV (álbum de Winger)', #Generica
 ur'Thomas Alva Edison', #Milan
 ur'Juan Sobrarias', #sobrarias
 ur'Midway Games', #
 ur'Silhouette Mirage', #Envia
 ur'Burusera', #sera
 ur'Skies of Arcadia', #valua
 ur'Óscar Liera', #tatua
 ur'Pinamonte Bonacolsi', #marcaria
 ur'Anexo:Playas de Canarias', #haria
 ur'Marcaria',
 ur'Haria', #haria
 ur'Berri Txarrak', #haria
 ur'Om (banda)', #donaria
 ur'Juan de Astorga', #edito
 ur'Arcadi Oliveres', #ca
 ur'Idioma irlandés', #frio
 ur'Parque nacional Los Médanos de Coro', #dara
 ur'Dara Shikoh', #dara
 ur'Burhinus bistriatus', #dara
 ur'Murallas de Oporto', #Govierno
 ur'Callejon (banda)', #callejon
 ur'Bula de Lucio III (1182)', #Castellon
 ur'Congreso de Paraguay', #Bóbeda
 ur'Francisco Fernández Buey', #Tranvia
 ur'Cristina Cavalinhos', #Aqui
 ur'Marrón', #Marron
 ur'Jūken Sentai Gekiranger', #Rio
 ur'Caterina Tarongí', #dia
 ur'Alphone Guichenot', #Rio de Janeiro
 ur'Idioma aragonés', 
 ur'Steven Levitsky', #politica
 ur'Política (Aristóteles)', #politica
 ur'Corpus Aristotelicum', #politica
 ur'Carlos Casares Mouriño', #veran
 ur'Antoine Busnoys', #vendra
 ur'Miguel Ortiz Berrocal', #Multiples
 ur'Junjō Romantica', #Egoista
 ur'Fugitiva (novela)', #Legenda
 ur'Anexo:MTV Europe Music Awards 2008', #Legenda
 ur'Polonia en el Festival de la Canción de Eurovisión', #Legenda
 ur'MTV Video Music Awards Japan', #Continue
 ur'Anexo:Baloncestistas del Fútbol Club Barcelona en la Liga ACB', #Nacio
 ur'Segunda expedición de Cevallos a Río Grande', #Rio
 ur'Brigadas Internacionales', #Mas la
 ur'Volvera', #Volvera
 ur'Link (The Legend of Zelda)', #Veran
 ur'Evento divergente', #situe
 ur'Situa', #Situa
 ur'Literatura oral y tradicional en euskera', #puntua
 ur'Bernardo Atxaga', #eu
 ur'Manuel de Escalada y Bustillo', #es ant.
 ur'URL semántica', # variables ''seccion
 ur'Ya comimos', #ladino
 ur'Ciconia ciconia', #&nbsp;asiatica
 ur'Dialecto murciano', #actua''l
 ur'Power Rangers: Wild Force', #Toxica
 ur'Sintaxis latina', #arida
 ur'Banda de La Covatilla', #perdi
 ur'Español cubano', #perdi
 ur'Asedio de Bolduque (1629)', #tenia
 ur'Cariotipo', #,inv
 ur'Insensible (House)', #tenia
 ur'J. M. Asensio', #La Tenia
 ur'Tenia (arquitectura)', #tenia
 ur'Taenia solium', #tenia
 ur'Taenia saginata', #tenia
 ur'Taenia', #tenia
 ur'Piloto (House)', #tenia
 ur'Helanódicas', #tenias
 ur'Echinococcus granulosus', #tenia
 ur'Lorenzo van der Hamen', #es ant.
 ur'Alonso de Espina', #es ant.
 ur'Joaquim Machado de Assis', #Historias
 ur'Hygrocybe conica', #conica
 ur'Silene conica', #conica
 ur'Centrica', #centrica
 ur'La coronación de Popea', #ahi perfida
 ur'French Kiss', #Cardon
 ur'Ilex aquifolium', #cardon
 ur'Validación XML', #<titulo>
 ur'Cortes Portuguesas', #capitulos
 ur'Águas Frias (Chaves)', #pt
 ur'Repostero de camas', #es ant.
 ur'Premio Sent Soví',#ca
 ur'Supermercados Dia', #Dia <----
 ur'La historia esta', #???
 ur'Idioma judeoespañol', #?? <----
 ur'Rio Natsume', #Rio
 ur'Flamengo (Río de Janeiro)', #pt
 ur'Condado de Rio Grande', #Rio
 ur'Anexo:Áreas micropolitanas de Estados Unidos', #Mexico
 ur'RIO (banda)', #Rio
 ur'Cecilia Gonçalves Costa', #biblio <---
 ur'Anexo:Condados de Portugal', #Rio
 ur'Sönke Möhring', #Asi
 ur'Municipio de Rio (condado de Knox, Illinois)', #Rio
 ur'Rio (programa)', #Rio
 ur'Empeine (enfermedad)', #????
 ur'Orontes', #Asi
 ur'Convento de San Francisco (Corrientes)', #es ant.
 ur'Ariella Arida', #Arida
 ur'Catalán de Baleares', #ca
 ur'Oxnard', #El Rio
 ur'El Río (California)', #El Rio
 ur'Manchester (condado de Bennington, Vermont)', #Manchester
 ur'Manchester (condado de Green Lake, Wisconsin)', #Manchester
 ur'Manchester (condado de Jackson, Wisconsin)', #Manchester
 ur'Lenguas atsina-arapaho', #el ha'
 ur'Gabriel de Barletta', #relacion
 ur'Vecino', #es ant.
 ur'Primeros vecinos', #es ant.
 ur'Manuel de Pinazo', #es ant
 ur'Hernán Mejía de Mirabal', #deven
 ur'Hernando de Talavera', #deve
 ur'Anexo:Telenovelas de Brasil', #pt
 ur'Republica (álbum)', #Republica
 ur'República (Transnistria)', #Republica
 ur'Leyenda', #Legenda
 ur'José de Lucas Acevedo', #ha aprender
 ur'Antonio Domínguez Hidalgo', #llego
 ur'Shadow of the Colossus', #Avion
 ur'Divina Comedia', #Ahi
 ur'The Perfect Game', #Maiz
 ur'Parque natural de Urkiola', #lamias
 ur'Número Seis', #Galactica
 ur'Pulsión', #pulsion
 ur'Literatura en sórabo', #sorbio
 ur'Serbia', #sorbio
 ur'Serbios', #sorbio
 ur'Sorabia', #sorbio
 ur'Sorbios', #sorbio
 ur'Ford Nucleon', #Nucleon
 ur'Badoglieide', # it
 ur'Antonio de Lorea', #es ant.
 ur'Aphididae', #Pulgon
 ur'Zucchero Fornaciari', #Incenso
 ur'Justicia (género)', #Emularia
 ur'Yves Balasko', #biblio
 ur'Robert F. Engle', #biblio
 ur'Oskar Lange', #biblio
 ur'Uxío Carré Alvarellos', #Desalento
 ur'Songs in the Key of Life', #Contusion
 ur'Condado de Carbón', #Carbon
 ur'La Xarxa', #Competició
 ur'Río Zambeze', #Caia
 ur'Río Caya', #Caia
 ur'Buzon', #Buzon
 ur'Túnel de Eupalino', #Apostol
 ur'Historia de la bandera de la Argentina', #habia
 ur'Lenguas nilo-saharianas', #élla
 ur'Geografía de Texas', #Capitan
 ur'Albert Martínez', #filip
 ur'Enciclopèdia de Menorca', #Arqueologia
 ur'Idioma ibero', #biblio
 ur'José Luis Maya González', #biblio
 ur'Anexo:Localidades de la merindad de Pamplona', #Alli
 ur'Anexo:Concejos de Navarra', #Alli
 ur'Larráun', #Alli
 ur'Alli', #Alli
 ur'Lyuba Berlin', # y Berlin
 ur'Etnolingüística', # y Berlin
 ur'Combate de Pisco', #???
 ur'Gil Garcés de Azagra', #Sanchez
 ur'João Ubiratan Moreira dos Santos', #biblio
 ur'Paul Scheuring', #Yucatan
 ur'Melrose (álbum)', #Yucatan
 ur'Anexo:Municipios de Minnesota', #Yucatan
 ur'Línea naviera Ward', #Yucatan, Merida
 ur'Municipio de Yucatan (condado de Houston, Minnesota)', #Yucatan
 ur'Gramática del quechua ancashino', # alli
 ur'Cofradía de Jesús Nazareno de Torredonjimeno', #alli
 ur'Anexo:Abreviaturas latinas en bibliografía científica', #la
 ur'Pedro Ocharte', #biblio
 ur'Odium theologicum', #dialogos
 ur'Sequentia', #dialogos
 ur'Pedro de Medina', #biblio
 ur'Historia del libro', #biblio
 ur'Eustaquio Fernández de Navarrete', #biblio
 ur'Natales (Antigua Roma)', #aurea???
 ur'Lamarckia', #aurea
 ur'Alfoz de Palenzuela', #aurea
 ur'Cohors VI Asturum', #aurea
 ur'Cohors III Hispanorum', #aurea
 ur'Legio X Gemina', #aurea
 ur'Cicer arietinum', #em un
 ur'Aragonés medieval', #entro
 ur'Cancionero de Elvas', #lagrimas
 ur'Abierto de la República',#Lagrima
 ur'Enrico Caruso', # lagrima<------
 ur'Paraíso: Canto Trigésimo tercero', #propria
 ur'Anexo:Pueblos de Grado', #Temia
 ur'Temia', #Temia
 ur'Fran Perea', #???
 ur'Celebrity Psychos', #Cadaver
 ur'Apollyon', #Cadaver
 ur'Cadaver (banda)', #cadaver
 ur'Somatic Responses', # Axon
 ur'White Anglo-Saxon Protestant', #axon
 ur'Anexo:Bienes de interés cultural de la provincia de Valencia', #ca
 ur'Alisma plantago-aquatica', # llantén acuatico
 ur'Océano (mitología)', #Accion<-------
 ur'Abba Lerner', #biblio
 ur'Distrito fitogeográfico de la restinga', #biblio
 ur'Anexo:Óperas de Francesco Bianchi', #gascon
 ur'Anexo:Discografía de Dorival Caymmi', #maritimo
 ur'David Prieto Ruiz', #biblio
 ur'Pullip', #Fanatica
 ur'Bilbao', #Béisbol
 ur'OsCommerce', #Fantastico, Ponce de Leon
 ur'Opus clavicembalisticum', # it
 ur'Caterina Valente', #Fantastica
 ur'Anna Oxa', #Fantastica
 ur'Paulo Jovio', #es ant.
 ur'Mercedes Peón', #Etnica
 ur'Idioma talossan', # ch'el <--------
 ur'Señor y Virgen del Milagro', #escencia<--------
 ur'Erevan (banda)', #Erevan
 ur'Thomas Conrad Porter', #Porteria
 ur'Desidae', #porteria
 ur'Anexo:Arañas de Chile', #porteria
 ur'Anexo:Especies de Desidae', #porteria
 ur'Porteria (animal)', #porteria
 ur'Gramática del italiano', #psicologo, <----
 ur'Historia del gato', #murio <-----
 ur'International Launch Services', #Proton
 ur'Acorn Computers', #Proton
 ur'Amelia Luisa Damiani', # biblio
 ur'Catalán pallarés', #ca
 ur'Adrastea (Misia)', #Pario
 ur'Pario', #Pario
 ur'Lito Lapid', #???
 ur'Combate de Cotagaita', #Cita
 ur'Ferrán Sánchez Calavera', #es ant
 ur'Joaquín de Villalba', #biblio
 ur'Cestrum parqui', #Vestia
 ur'Unias', #Unias
 ur'China como superpotencia emergente', #biblio
 ur'Tatsunoko Production', #tento
 ur'Comparación entre el esperanto y el ido', # tento
 ur'Esperanto reformado', #tento
 ur'Matilde Salvador', # tendra
 ur'Iván Tubau', #tendra
 ur'Glan', #Tapon
 ur'Roma criminal (novela)', #Tapon
 ur'Diálogo?', #Desconfia
 ur'Historia del bajo eléctrico', # su Precision
 ur'Athena (misión a Marte)', #Proton
 ur'Sudamericidae', #Sudamerica
 ur'Bharattherium', #Sudamerica
 ur'Sudamerica (animal)', #Sudamerica
 ur'HoverRace', #Eon
 ur'Tagudin', #Salvacion
 ur'Saguday', # Salvacion
 ur'Pachanga Diliman FC', # Salvacion
 ur'Ormoc', #Salvacion, Concepcion
 ur'Luna (municipio de Apayao)', # Salvacion
 ur'Luis Manzano', # Salvacion
 ur'Eddie García', # Salvacion
 ur'Rio Tinto Group', #de Rio
 ur'Transcobalamina', #biblio
 ur'Serenata', #sera
 ur'Hormona luteinizante', #sera
 ur'Conjugación francesa', #sera
 ur'Novallas', #sera
 ur'Ramón Soler', #biblio
 ur'Doctrina de la Iglesia católica', #citas sin comillas
 ur'GoliADs UAO CEU Awards',#i la 
 ur'Hipólito de Este', #minoria
 ur'Silicato (minerales)', #filon??
 ur'Ignacio Gómez',#biblio
 ur'Montia fontana', #comio
 ur'Woe, Is Me', #Corrección manual
 ur'Manuel Germán Ojeda y Muñiz', #es ant
 ur'Rafael Delorme', #biblio
 ur'Juan Ángel Golfarini', #biblio <-----
 ur'José María Quirós', #biblio
 ur'Ubaldo Romero Quiñones', #biblio
 ur'Idioma español en Japón', #???
 ur'Mar Monsoriu Flor', #biblio
 ur'Mansionario', #es ant.
 ur'Historia del idioma asturiano', #ast
 ur'Marquesado de Loja', #canpos
 ur'Leonor de Guevara y Téllez de Castilla', #Ladron
 ur'Agustín Gómez', #es ant.
 ur'José Presas', #es ant
 ur'José Eusebio de Llano Zapata', #biblio <-----
 ur'Amulung', #Jurisdiccion
 ur'Boac', #Boton
 ur'Gobiopterus stellatus', #bombon
 ur'Gnatholepis volcanus', #bombon
 ur'Bombon', #bombon
 ur'Anexo:Discografía de Xuxa', #bombon
 ur'Idioma anglo rom', #perdon
 ur'Perdigó', #Perdigon
 ur'Anexo:Trovadores de Francia en occitano', #Perdigon
 ur'Molinos Río de la Plata', #bellisimo
 ur'Buffalo wings', # bellisimo
 ur'Birreme', #Bebia
 ur'Nitro (banda)', #Batio
 ur'Sacrum palatium',#pedagogia
 ur'Francisco de Toledo Herrera', # es ant.
 ur'Andrés Luis López-Pacheco y Osorio', # es ant.
 ur'El Kaso Urkijo', #???
 ur'Santa Clara (1853)', #es ant.
 ur'Proton Holdings Berhad', #proton
 ur'Manuel Martínez Añíbarro y Rives', #biblio
 ur'Anatheóresis', #biblio
 ur'Florencio Jardiel Dobato', #biblio
 ur'Francisco de Enzinas', #es ant.
 ur'Edward Abramowski', #biblio
 ur'Turcupichun', #biblio
 ur'Lemucaguin', #biblio
 ur'Juan Bautista de Poza', #biblio
 ur'Francisco Botello de Moraes y Vasconcelos', #biblio
 ur'El chitón de las tarabillas', #es ant.
 ur'Batalla de Quiapo', #biblio
 ur'Alberto Boerger', #biblio
 ur'Jardín Botánico de Salazar y Reserva de Flora', #biblio
 ur'Raffaele Ciferri', #biblio
 ur'Romualdo González Fragoso', #biblio
 ur'Sellos y la historia postal de Etiopía', #Avion <-----
 ur'Begonia acida', #acida
 ur'The Delgados', #Peloton
 ur'Gramática del español', #partio
 ur'BBC Micro', #Proton
 ur'Dionisio de Alcedo Herrera', #historico <--------
 ur'Ingelheim am Rhein', #Nasau
 ur'Dinornis', #Movia
 ur'Malolos', #Mojon
 ur'Distrito de Tingo', #Mojon
 ur'Salatzen dut', #Sustraia
 ur'Opacidad', #Mineralogia
 ur'Pomacea', #Republica
 ur'Anexo:Cronología de Dragon Ball', #Marron <-------
 ur'Idioma estonio', # estonio
 ur'Francisque Gay', #fr
 ur'Hispanismo', #es ant.
 ur'Anadolu Efes S.K.', #Jamon
 ur'María Josefa Acevedo de Gómez', #Bibliografía instruccion 
 ur'Jerónimo de Alcalá', #es ant.
 ur'Río Purapel', #se vacia
 ur'Ducado de Vasconia', #????
 ur'Colegio Nacional Rafael Hernández', #Nacio
 ur'Distrito de Mariato', #Quebro
 ur'Gaudeamus igitur', #:faciles, formosae
 ur'Anexo:Películas rodadas en Almería', #????
 ur'Presidium', # presidia
 ur'Antonio de Herrera y Tordesillas', # es ant.
 ur'Anexo:Ciudades de California', # Escalon
 ur'Uniforme escolar', #???
 ur'Energías de Portugal', # ?????
 ur'Fobos-Grunt', #Proton
 ur'Fernando Díaz de Valderrama', # es ant.
 ur'ISO 8601', #Duracion
 ur'Charles Maturin', #Maturin
 ur'Arconte epónimo', #Filon
 ur'Distrito de Camporredondo', #Comia
 ur'Sante Geronimo Caserio', #Caserio
 ur'Americanismo (estudio)', # Bufon
 ur'Artemisia absinthium', #plantas
 ur'Bidón', #bidon
 ur'Bidon', #bidon
 ur'Aburria', #Aburria
 ur'Dublin (Indiana)', #Dublin
 ur"Aziz Ab'Saber", #bibliografía
 ur'Madrigales de Claudio Monteverdi', #it
 ur'Oskar Morgenstern', #econometrica (biblio)
 ur'Clive W. J. Granger', #econometrica (biblio)
 ur'Causalidad de Granger', #econometrica (biblio)
 ur'Katie Melua', #Dramatico
 ur'Anexo:Episodios de Life with Derek', # Adios
 ur'Anexo:Discografía de Sabroso', #se lo mando
 ur'Pastorela', #partia
 ur'Valencia (química)', #valentia
 ur'Valor propedéutico del esperanto', #esperanto
 ur'Anexo:Pokémon', #Uniran
 ur'Sonata Arctica', #unia <--------
 ur'Lenguas asturleonesas', #ast
 ur'Lamium amplexicaule', #lamio
 ur'Historia de Camerún', #camaron
 ur'PCR', #'''C'''ardio
 ur'Lenguas indoeuropeas', #sorbio
 ur'Esperanto', #esperanto
 ur'Crustacea', #exitos
 ur'Andrew Bertie', #Santisima
 ur'William Jones (filólogo)', #mas se
 ur'Unia', #Unia <------
 ur'Theatrum chemicum', #tractatulum propria, suo discipulo
 ur'Tarifa', #Facinas
 ur'Adorno (música)', #biblio
 ur'Júlio Sérgio', #America
 ur'Taeniopterygidae', #Frison
 ur'Microtus', #????
 ur'Lugar designado por el censo', #El Cajon
 ur'Lithops optica', #optica
 ur'Laura Pausini', #Inedito
 ur'Julia Clarete', #biblio
 ur'José Moreno Gans', #ga
 ur'Jordi Sierra i Fabra', #it
 ur'Idioma leonés', #leonés
 ur'Oceano (banda)', #Oceano
 ur'Casimiro Marcó del Pont', #es ant
 ur'José Iglesias de la Casa', #es ant.
 ur'Aziz Ab\'Saber', #Geografia
 ur'Anexo:Glosario de terminología musical', #energico <-----
 ur'Alberto Soriano', # Movia
 ur'Diego de Landa', #es ant
 ur'Orlistat', #Alli
 ur'Occitano limosín', #oc
 ur'Occitano auvernés', #oc
 ur'Municipio Michelena', #conexion94.3fm
 ur'Bartolomé Anento y Peligero', #es ant.
 ur'Anexo:Obispos de Mérida-Badajoz', #Profirio
 ur'Michael Kessler', #Bibliografía
 ur'Zahhak', #Ahi
 ur'Dukla Trencin-Trek', #Merida
 ur'Iglesia de San Clemente (Iran)', #Iran
 ur'Idioma occitano', #oc
 ur'Aquixtla', #quiza
 ur'Riber', #envia
 ur'Cuculliinae', #Jodia
 ur'Calpinae', #Veia
 ur'Anexo:Localidades de California', #nombres en es sin acento
 ur'Anexo:Lista de aves de Sibley-Monroe 7', #aves
 ur'Anexo:Episodios de Split (serie de televisión)', #Jamon
 ur'Función aritmética', #Apostol
 ur'Anexo:Episodios de Ally McBeal', #a ella esta
 ur'Bruno Munari', #it
 ur'Mysterium Cosmographicum', #la
 ur'Metro de Río de Janeiro', #mesquita
 ur'Benimaru Nikaido', #Maxima <------
 ur'Damien: Omen II', #pasarian
 ur'Polònia', #minoria absoluta <----
 ur'Florencio Janer', # es ant
 ur'Eudald Jaumeandreu', # es ant. Diccionario critico
 ur'Provincia de Pomabamba', #???
 ur'Amsterdam (Ohio)', #en Amsterdam
 ur'Amsterdam (Montana)', #en Amsterdam
 ur'Amsterdam (Misuri)', #en Amsterdam
 ur'Gianni Minà', #it
 ur'Vide Cor Meum', #it
 ur'Talpiot', # Asi
 ur'Universidad de Trás-os-Montes e Alto Douro', # pt?
 ur'Miguel Relvas', #mas nunca pariu
 ur'Ariane Luna Peixoto', #pt
 ur'Maria da Conceição Tavares', #pt
 ur'Dante Liano', #
 ur'Dragon Data', #Dragon. Cumana
 ur'Bob Dylan', #interpreto
 ur'Una furtiva lagrima', #lagrima it
 ur'Román Perpiñá Grau', #ca
 ur'Rodrigo Méndez Silva', #es ant
 ur'Cabra (Córdoba)', #Bebio
 ur'Spin (álbum)', #Ayes
 ur'Alonso Núñez de Haro', #es ant
 ur'Caiga quien caiga', #caia quem caia
 ur'El Generico', #Generico
 ur'WrestleMania 29', #Del Rio
 ur'Banda Sonora de Kodai Ōja Kyōryū King', #Paris
 ur'Magic: el encuentro', #Dominaria
 ur'Magic: el encuentro (trama)', #Dominaria
 ur'Anexo:Cronología de la minorización del idioma catalán', #ca
 ur'Ada Wong', #Leon
 ur'Anexo:Condados homónimos de los Estados Unidos', #nombres en es sin acento
 ur'Murillo Fossati', #Cesarian
 ur'Hyundai Coupe', #Tiburon
 ur'Split (serie de televisión)', #Jamon
 ur'Episodios de Split (serie de televisión)', #Jamon
 ur'Zamboanga', #calarian
 ur'Geeta Dutt', #dara
 ur'Survivor Series (2011)', #Del Rio
 ur'Santa Maria (Río Grande del Sur)', #Maria
 ur'America Football Club', #America 
 ur'Distrito de Chucuito', #Aqui
 ur'Partido de los Comunistas Italianos', # sinistra democratica
 ur'SummerSlam (2012)', #Del Río
 ur'Augusto Carlos Teixeira de Aragão', #pt
 ur'Real Sociedad de Fútbol', #Oceano
 ur'Distrito de Potoni', #aqui
 ur'Pecho (tributo)', #historica
 ur'Jerônima Mesquita', #mesquita
 ur'Emigración', #valentia
 ur'Alvise Cadamosto', #it,pt
 ur'Oric Telestrat', #Cumana
 ur'Oric Atmos', #Cumana
 ur'Cumana', #Cumana
 ur'Dos hogares', #romantica
 ur'Villarino de los Aires', #El era
 ur'Anexo:Álbumes de Perro Andaluz', #infundia
 ur'Luana Piovani', #ó
 ur'Muletilla', #ó
 ur'Nicolás Díaz de Benjumea', #ó
 ur'Anexo:Nombres propios y topónimos en idioma quingnam', #ó
 ur'Gaélico escocés',# ó
 ur'Escritura del mapuche',# ó
 ur'Infierno: Canto Cuarto',
 ur'Infierno: Canto Decimoctavo',
 ur'Infierno: Canto Decimocuarto',
 ur'Infierno: Canto Decimoséptimo',
 ur'Infierno: Canto Decimotercero',
 ur'Infierno: Canto Duodécimo',
 ur'Infierno: Canto Décimo',
 ur'Infierno: Canto Octavo',
 ur'Infierno: Canto Primero',
 ur'Infierno: Canto Quinto',
 ur'Infierno: Canto Segundo',
 ur'Infierno: Canto Trigésimo cuarto',
 ur'Infierno: Canto Trigésimo primero',
 ur'Infierno: Canto Vigésimo noveno',
 ur'Infierno: Canto Vigésimo primero',
 ur'Infierno: Canto Vigésimo sexto', 
 ur'Infierno: Canto Vigésimo séptimo',
 ur'Infierno: Canto Vigésimo tercero',
 ur'Infierno: Canto Vigésimo',
 ur'Urracá', #Duraria
 ur'Montaria', #Montaia
 ur'Tales of Vesperia', #Rita Mordio
 ur'José Campero de Sorredevilla' #es ant.
 ur'Sinalefa', #despues la lista se combierte
 ur'Amimitl', #???
 ur'Oliverio Girondo', #Poemas para ser leidos
 ur'Balbino Santos Olivera', #es ant.
 ur'Abd al-Rahman ibn Habid al-Siqlabi', #es ant. <----
 ur'Manuel de Cueto y Ribero', #es ant.
 ur'Familia Agnelli', #Via
 ur'Ricardo Blanco Asenjo',#leido
 ur'Condado de Bergen', #Bogota
 ur'Manila', #Bogota
 ur'Anexo:Localidades de Nueva Jersey', #Bogota
 ur'Bogotá (desambiguación)', #Bogota
 ur'Bogota (Nueva Jersey)', #Bogota
 ur'Ramales de la Victoria', #Pondra
 ur'Comunidades en Saskatchewan', # Valparaiso
 ur'Gaspar Fernández', #es ent.
 ur'Anexo:Designaciones utilizadas en la nomenclatura de los grupos taxonómicos', #bio
 ur'Miguel de Barrios', #???
 ur'Giorgio Manganelli', #De America
 ur'Laurent Ruquier', #fr
 ur'Jules Romains', #fr
 ur'A Horse with No Name', #America
 ur'Llesp (antiguo municipio)', #Iran
 ur'Iglesia de San Martín (Llesp)', #Iran
 ur'Iglesia de San Clemente (Iran) ', #Iran
 ur'Iran (Llesp)', #Iran
 ur'The Metro (canción)', #Berlin <-------
 ur'José María Sánchez Carrión', #antropologia
 ur'Irving Berlin', #Berlin
 ur'Berlin (banda)', #Berlin
 ur'Anexo:Municipios de Pensilvania', #Berlin
 ur'Anexo:Municipios de Illinois', #Berlin, etc.
 ur'Anexo:Municipios de Ohio', # Berlin, Cadiz,...
 ur'Anexo:Municipios de Míchigan', # Berlin, Cadiz,...
 ur'Unicorn Table', #Salia
 ur'Canto ambrosiano', #Lucernaria'' y ''Completaria
 ur'Bruno Nicolai', #it <-------
 ur'Myriad (tipografía)', #humanistica
 ur'Stefano Grondona', #it
 ur'Remo Giazotto', #it
 ur'Pier Vittorio Tondelli', #«Cronologia»,
 ur'Noite Bohemia', #ca <------
 ur'Manuel de Sumaya', #Corrección manual
 ur'La Gossa Sorda', #ca <-------
 ur'Josep Maria Mestres Quadreny', #ca
 ur'Jean-Claude Gérard', #Ensemble Villa Musica
 ur'Sombra perfecta (novela)', #Cenaria
 ur'Más allá de las sombras (novela)', #Cenaria
 ur'El camino de las sombras (novela)', #Cenaria
 ur'El Ángel de la Noche', #Cenaria
 ur'Al filo de las sombras (novela)', #Cenaria
 ur'Leccionario', 
 ur'Cohors XV Voluntariorum', #Auxiliaria
 ur'Juan Ignacio Luca de Tena', #Saldaria, un país imaginario,
 ur'Anselmo Braamcamp Freire', # Armaria portuguesa
 ur'Praia a Mare', #Viscigliosa, Zaparia
 ur'Flora de Asturias', #hispanica o legionensis,
 ur'Ildebrando Pizzetti', # it
 ur'Franco Simone', #compilacion curata
 ur'Walla!', #Walla!pedia
 ur'La Iglesuela del Cid', # de las notarias
 ur'José Luis Pasarín Aristi', #Liberarias
 ur'Danzas vascas', #Laboraria
 ur'Florisando', # es ant.
 ur'The Platinum Collection (álbum de Mina Mazzini)', #it
 ur'Fiordaliso', #Ahi ahi ahi
 ur'Cruz Quebrada - Dafundo', #Caidas
 ur'Latín', #la
 ur'El matadero', # es ant.
 ur'Eliot Paulina Sumner', #avion 
 ur'Oceano da Cruz', #oceano
 ur'Anexo:Submarinos de la Armada de Estados Unidos', #spanglish <---
 ur'Anexo:Canciones de Burnout Revenge y Burnout Legends',#Infusion
 ur'Lino Matías Picado Franco', #es ant.
 ur'Giuseppe D\'Amato', #it
 ur'Bores', #tienpo
 ur'Wellow (Hampshire)', #Canada
 ur'Juan Pérez de Montalbán', #es ant.
 ur'Barriga (Losa)', #es ant.
 ur'Ortografía de Bello', #es ant.
 ur'Marquesado de Gandul', #es ant. por las dudas
 ur'Rafael Farga', #ca
 ur'Rouco (apellido)', #es ant. 
 ur'Alfarería en la provincia de Albacete', #es ant.
 ur'Poemas narrativos de materia carolingia', #es ant.
 ur'Fruela Díaz', #es ant.
 ur'César Bruto',#humor
 ur'Plaza de la Escandalera', #conpre
 ur'Ricardo Castillo', #cienpies
 ur'Aguilar de Campoo', #es ant.
 ur'Anexo:Lugares de la Merindad de Candemuñó', #es ant.
 ur'Campo de Argañán', #es ant.
 ur'Primitiva Iglesia de Santa María de la Mesa', #es ant.
 ur'Lenguas balcorrumanas', #ru
 ur'Médico de familia (serie de televisión)', #ca
 ur'Helena Antipoff', #Psicologia Experimental
 ur'Angiosperm Phylogeny Website', #Plantas
 ur'Anexo:Temporada 2013 del Súper TC 2000', #....svg
 ur'Anexo:David de Donatello al mejor actor protagonista', #it
 ur'Mujer samaritana', #quales
 ur'Concordia de Alcañiz', #quales
 ur'Pablo Ignacio de Dalmases y Ros', #quales
 ur'Hermandad del Nazareno (Córdoba)', #quales
 ur'Real Audiencia de Canarias', #quales
 ur'Bedel', #quales
 ur'Retablo de la capilla del Colegio de San Gregorio', #quales
 ur'Andrés García de Céspedes', #quales
 ur'El Escorial y el Templo de Salomón', #quales
 ur'Fray Miguel López de la Serna', #quales
 ur'Ordenamiento de Montalvo', #quales
 ur'Villacelama', #quales
 ur'Fabián Campagne', #quales
 ur'Historia de Echarri-Aranaz', #quales
 ur'Real Santuario de la Virgen de la Salud', #quales
 ur'Butades', #quales
 ur'Pedro López de Lerena', # quales
 ur'Valdearenas', #quales
 ur'Heinrich Doergangk', #quales
 ur'Cabo de Consolación', #quales
 ur'Harimaguada', #quales
 ur'Capitulaciones de Alfacar', #quales
 ur'Grañén', #quales
 ur'Diego Rosel y Fuenllana', #quales
 ur'Tudela de Duero', #quales
 ur'Fábrica de seda de Vinalesa', #quales
 ur'Pere March', #quales
 ur'Facultad de Derecho (Universidad de Buenos Aires)', #quales <--
 ur'Teulada', #quales
 ur'Mateo Pérez de Alesio', #quales
 ur'Duende', #quales
 ur'Instituto de Biología Subtropical', #Genetica
 ur'Geología de la península ibérica', #Geologia
 ur'Fjölnir', #sv
 ur'Histórica relación del Reyno de Chile', #Histórica relación
 ur'Filipo el Árabe y el Cristianismo', #euriskomena panta: historica, canonica, dogmatica
 ur'Cray Jaguar', #Unicos
 ur'Cray X1 ', #Unicos
 ur'Cray-1', #Unicos
 ur'Últimos momentos de Fernando IV el Emplazado', #no especifica
 ur'Vía Egnatia', #grafica
 ur'Nino Taranto', #grafica
 ur'Enrico Accatino', #grafica
 ur'Dialecto tarentino', #it
 ur'Cristiano nuevo', # d'una minoria
 ur'Annaphila', #Annaphila decia
 ur'Idioma sardo', #sardo
 ur'Vino de la Tierra', #geografica tipica
 ur'Meshchora (región)', #Enciclopedia Geografica
 ur'Copa Mundial de Fútbol de 1986', #futbol
 ur'Dante Pantanelli', #it
 ur'Anexo:Buques de la Armada Soviética', #Delfin
 ur'Anton Johann Krocker', #indigenas
 ur'Alstroemeria ligtu', #Diccionario etimolójico
 ur'Pleurodema thaul', #es ant.
 ur'Giovanni Antonio Scopoli', #indigena
 ur'Agustín Codazzi', #es ant.
 ur'Infierno: Canto Decimocuarto', #e nomina
 ur'Juan José Silvestre Cantó', #de futbol
 ur'Juan José Barcia Goyanes', #i un dia
 ur'Leszek Engelking', #pl
 ur'Carlo Campogalliani', #it
 ur'Anexo:Canciones de Claire Waldoff', #de
 ur'Club Esportiu Europa', #ca
 ur'Escritura española en el siglo XVI', #es ant.
 ur'Idioma francés', #quinze
 ur'Cueva de Oxtotitlán', #Mexico
 ur'Árabe marroquí', # autobus
 ur'Antonio Gandusio', #autobus (corregido)
 ur'Alfred Pasquali', #fr autobus billon  (corregidos)
 ur'Santa Cruz (Río de Janeiro)', #pt
 ur'Maria Cristina Dreher Mansur', #zoologia
 ur'Carolina Martuscelli Bori', #Psicologia
 ur'Anexo:Bibliografía sobre Martín Sarmiento', #Filologia
 ur'Míriam Martinho', #Postumamente
 ur'Ricardo da Costa', #Filosofia
 ur'Joaquina Soares', #Arqueologia
 ur'Lenguas yabutí', #Antropologia
 ur'Rubem Alves', #Teologia de la Esperanza Humana?
 ur'Barbarismo', #aereopuerto
 ur'Catalán nororiental', #ca
 ur'Anexo:Discografía de Floricienta', #encontro <--
 ur'Mozárabe', #te encontro.
 ur'Idioma mozárabe', #de cada dia te encontro. <--
 ur'Energía solar fotovoltaica', # Conto Energia
 ur'Afonso Lopes Vieira', #Desterro Azul
 ur'Sergio Faraco', #ainda que tardia
 ur'Perla Suez', #in America Latina <--
 ur'Escudo portugués', #conto
 ur'Eonaviego', #conto <--
 ur'Belalcázar', #un conto
 ur'Álvaro Cunhal', #um conto
 ur'Conto', #Conto
 ur'Tomares', #es ant.
 ur'Anexo:Bienes de interés cultural de Andrach', #Alqueria
 ur'Álex Gadea', #Alqueria
 ur'Clorinda Matto de Turner', #Humanistica
 ur'Historia del electromagnetismo', #Abria
 ur'Peugeot', #Proxima
 ur'Homeopatía', #Materia médica
 ur'António Calvário', #aqui
 ur'Jon Semadeni', #dramaticas
 ur'Dialecto andaluz', #tranporte
 ur'Hoba Hoba Spirit',#The débil
 ur'Día del Nombre de Castilla', #es ant
 ur'Provincia de Los Santos', #Quebro
 ur'Calliandra spinosa', #botanicas (corregido)
 ur'Domenico Maria Leone Cirillo', #botanicas (corregido)
 ur'Historia de Sacavém', #Serro
 ur'Legión de la Justicia Alfa', #1 Millon
 ur'Idioma ilocano', #kadi no Sabado
 ur'Partido Socialista de Navarra-PSOE', #Alli
 ur'Salvatore Sciarrino', #anonimo it
 ur'Fernando Blumentritt', #anonimo de
 ur'Évariste Lévi-Provençal', #anonimo de
 ur'Johann Friedrich Carl Grimm', #anonimo de
 ur'David Mendes Silva', #Academica
 ur'Walthari', #Monumenta Historica
 ur'Pep Anton Muñoz', #ca
 ur'Ascoli Calcio 1898', #it
 ur'Asesinatos neonazis en Alemania de 2000-2007', # de
 ur'Devaki Pandit', # Subiran
 ur'Asier Illarramendi', #Asi
 ur'Diccionario Etimológico Romance', #ca 
 ur'Organistrum', #de musica
 ur'Jardín Botánico del Mediterráneo', #it
 ur'Dismorphia', #mirandola
 ur'Nambroca', #es ant.
 ur'Bermudo III de León', #es ant.
 ur'Lou Olivier', #it
 ur'Roberto Saviano', #it
 ur'Samuel de Bulgaria', #Servia
 ur'Teodicea', #enlace
 ur'Antoine Gouan',# usus medicos
 ur'Celia Langa', #telefono
 ur'Zayd Abu Zayd', #telefono <--
 ur'Willeke van Ammelrooy', #telefono <--
 ur'Ornella Vanoni', #telefono
 ur'Kerobia', #telefono
 ur'Antonio Meucci', #telefono
 ur'Andrea Camilleri', #telefono
 ur'Ernesto Vaser', #telefono
 ur'Supplì', #telefono
 ur'Gianni Rodari', #Favole al telefono
 ur'Laura Live Gira Mundial 09',#nusica alla (corregido)
 ur'Unicredit', #credito
 ur'FTSE Italia Mid Cap', #credito
 ur'Alfredo Pizzoni', #credito
 ur'Mediobanca', #credito
 ur'Credito Italiano', #credito
 ur'Banca Popolare di Sondrio', #credito
 ur"Banca Popolare dell'Emilia Romagna", #credito
 ur'Banca Carige', # credito
 ur'Anexo:Rangos e insignias de los suboficiales de tierra de la OTAN', #Minimos epilochias
 ur'Anexo:Personas más altas del mundo', #Jarron
 ur'Anexo:Óperas en el Teatro de la Maestranza', #it
 ur'Anexo:Instrumentos Stradivarius', #Unico
 ur'Tre Martelli', #musica
 ur'Origen del topónimo Chile', #es (ant.)
 ur'Survivor (Estados Unidos)', #Tyson Apostol
 ur'Unimarc', #tento
 ur'Somewhere Back In Time World Tour', #Pacifico Yokohama
 ur'Stravaganza', #Servian
 ur'Anexo:Episodios de Malcolm in the middle', #nomina también
 ur'Anexo:Ministros generales de los Hermanos Menores', #nombres
 ur'Simion Bărnuțiu', #ru
 ur'Casa Baratheon', # Balon Greyjoy
 ur'Alfonso Fernández el Niño', #es ant.
 ur'María Elena Galiano', #comun (abrev) <--
 ur'Mário Henrique Simonsen', # pt
 ur'Marlierea', #comun (abrev)
 ur'Marsilio de Padua', #it
 ur'Michel Schooyans', #it
 ur'Anticlericalismo en España', # es ant.
 ur'Anexo:Composiciones de Alessandro Scarlatti', #it
 ur'Carácter (música)', #comodo''''': cómodo.
 ur'Pedro Pablo de Ribera', #it
 ur'Brezzo di Bedero', #it
 ur'Museo de Historia Natural de Florencia', #it
 ur'Mário Guimarães Ferri',#pt
 ur'Machaerantherinae', #en <--
 ur'Anexo:Palabras del idioma inglés provenientes del español', #en
 ur'Leo Jiménez', #Palau de la Musica
 ur'Yucca rostrata', #Mexico en
 ur'María del Socorro González Elizondo', #Mexico en
 ur'Rafael Trevisan', #pt
 ur'António Xavier Pereira Coutinho', #Elementos de botanica
 ur'Fútbol Club Atlético de Sabadell', #ca <--
 ur'Revista médica', #pt
 ur'Partido de los Trabajadores (Brasil)', #pt
 ur'Corona', #corona clinica
 ur'Coronal', #??????
 ur'Miquel Ortega', #Labordeta Clasico,
 ur'José Quezada Macchiavello', #cast. ant.
 ur'Anexo:Glosario de epítetos y nombres botánicos', #especies
 ur'Música clásica', #la musica ‘classica‘
 ur'Augusto Manuel Alves da Veiga', #pt
 ur'Augusto Béguinot', #it
 ur'Gabriela G. Hässel', #comun. <--
 ur'José Luís Morales y Marín', #Corregir a mano
 ur'Luigi Malice', #it Artistico,economia
 ur'Locri (Italia)', #it
 ur'Pez (artista)', #Corregir a mano
 ur'José Jorge Loureiro', #bibliographico, heraldico, numismatico e artistico
 ur'Arpa eólica', #macchina armonica automatica <--
 ur'Howard Benson', #Meson Ray
 ur'Anexo:Caballeros de la Orden del Toisón de Oro', #Unico II
 ur'Vico del Gargano', #dell'artistica
 ur'Virginia Woolf', #Clasica maior,
 ur'Don Quijote de la Mancha', #Fillot de San Martin
 ur'Juicios por delitos de lesa humanidad en Argentina', #Unia
 ur'Norris H. Williams', #Medellin
 ur'Partido Justicialista', #Servini de Cubria (tiene errores)
 ur'Planetario', #Astronomia e Ciencias
 ur'Xabier Lete', #San Martin, azken larrosa
 ur'Palacio de Chiloeches (Espinosa de los Monteros)', #San Martin
 ur'Val Gardena', #San Martin Istitut Ladin
 ur'Asociaciones Italianas en Sudamérica', #in Sud America
 ur'Acta Biologica Venezuelica', #Biologica
 ur'Giovanni Mario Crescimbeni', #it
 ur'Salvatore Contino', 
 ur'Historia de Boca Juniors (fútbol)', #Tomás Movio
 ur'Federazione Italiana di Atletica Leggera', #di Atletica
 ur'Francis Macdonald Cornford', #Microcosmographia Academica
 ur'Clementinae', #diritto canonico
 ur'Clorinda Corradi', #it
 ur'Asociación Europea de Atletismo', #di Atletica
 ur'Alfa Romeo', #Società Anonima
 ur'American Idiot: The Original Broadway Cast Recording (álbum)', #Gerard Canonico
 ur'Anexo:Episodios de Los Simpson', #Cuando criticas
 ur'Anexo:Empresas de ferrocarriles', #Esercizio Ferroviario Turistico
 ur'Anexo:Discografía de Joaquín Sabina', #Pierre Billon
 ur'Anexo:Aves de Bolivia', #Había rubica
 ur'Werner Finck', #Taberna academica
 ur'Westminster Cathedral Choir', #Missa canonica
 ur'Wiehlea', #Senckenbergiana biologica,
 ur'Willa Cather', #Clasica maior,
 ur'William Withering', #Actas da Academica
 ur'Zona Especialmente Protegida de Importancia para el Mediterráneo', #diversità biologica
 ur'Acta societatis scientiarum fennica. Series B. Opera biologica', #Opera biologica
 ur'American Idiot: The Original Broadway Cast Recording (álbum)', #Gerard Canonico,
 ur'Ana Isabel D. Correia', #Portugaliae Acta Biologica
 ur'Anexo:Palmarés de la Juventus de Turín', #Valore Atletico
 ur'Basílica de Santa Maria delle Vigne', #svolgimento artistico
 ur'Casa de Ventimiglia', #Lettere e Filosofia
 ur'Catedral de Santa María de la Asunción de Lucciana', #église de la Canonica
 ur'Claudio Gora', #della clinica
 ur'Clorinda Corradi', #cronologico delle
 ur'Edouard-Jean Gilbert', #fr
 ur'Johan Nicolai Madvig', #Opuscula academica
 ur'José Antonio Conde', #que un Anonimo dirigio
 ur'Enrico Maria Salerno',#Anonimo veneziano
 ur'Ernst Gottlieb Bose',#clinico et forensi
 ur'Lorenzo Lippi (poeta)', #cronologica degli
 ur'Luís Manuel Ferreira Delgado', #Petro Atletico
 ur"Macrino d'Alba", #Artistica Piemontese
 ur'Giovanni Spano', #dal canonico
 ur'Graciano (jurista)', #diritto canonico
 ur'Monumento a la República', #Pietro Canonica
 ur'Nicola Romeo', #Società anonima
 ur'Officine Meccaniche', #Societá Anonima
 ur'Orden Militar de la Stella', #economia pubblica,
 ur'Portugaliae Acta Biologica', #Acta Biologica
 ur'Red ferroviaria de Cerdeña', #Società anonima (contiene errores)
 ur'Rodriguésia – Revista do Jardim Botânico do Rio de Janeiro', # Jardim Botanico
 ur'Rosario Rivellino', # Atletico Puteolana
 ur'Vincenzo Montefusco', #Atletico Puteolana
 ur'William Botting Hemsley', #Biologica Centrali-Americana
 ur'Tim Armstrong', #Head Automatica
 ur'Tulio Lombardo', # economia dalla
 ur'Antonio Lebo Lebo', #Petro Atletico
 ur'Atletico Roma Football Club', #Atletico Roma
 ur'United Nations (banda)', #Head Automatica
 ur'Villa Borghese', #Museo Canonica
 ur'Zé Kalanga',#Petro Atletico
 ur"Canonica d'Adda", # Canonica
 ur'Copa Italia 2010-11', #Atletico Roma
 ur'Decreto de Graciano',#diritto canonico
 ur'La lettera anonima', #lettera anonima
 ur'Rodolia cardinalis',# lotta biologica...
 ur'Santa Cruz de Jerusalén (título cardenalicio)', # Canonico Regolare
 ur'Francesco I de Ventimiglia', #alfabetico della
 ur'Francesco III de Ventimiglia', #Cronologica dei Vicerè
 ur'Gemoterapia', #di Gemmoterapia Clinica,
 ur'Atletica (marca)', #Atletica (tiene errores)
 ur'Historia de Fiat S.p.A.', #Società Anonima
 ur'Jarbas Faustinho Canè', #Atletico Puteolana
 ur'Lega Pro Seconda Divisione', #Atletico Catania
 ur'Pedro de Valencia', #Academica, sive de iudicio
 ur'Amedeo Benedetti', #e la política
 ur'Alife', #it
 ur'Adolfo Muñoz Alonso', #Filosofia di
 ur'Adriano en Siria (Myslivecek)', #Quanto è facil
 ur'1997-2005', #Electrico@hogar.com
 ur'Alba Zaluar', #pt
 ur'Temporada 1986 del Campeonato Mundial de Rally', #Greg Criticos
 ur'European Coordination for Accelerator Research & Development',#di Fisica
 ur'Ultima IX', #los últimos Ultimas.
 ur'Carlo Galli', #della politica.
 ur'Academia Valenciana de la Lengua', # Vicent Gascon
 ur'Comun Nuovo', #it
 ur'James Vandehei', #Politico (periódico)
 ur'Simón de Rojas Clemente y Rubio', #la vid comun
 ur'Josep Maria Flotats', #ja estan
 ur'Kaori Mizuhashi', #Vivio Takamachi 
 ur'Francisco Javier Llorens y Barba', #ca
 ur'Economista', #elho Federal de Economia 
 ur'Caspar Commelijn', #Publicas Plantarum
 ur'Georges Duhamel', # Patagon
 ur'José Pellicer de Ossau Salas y Tovar', #es ant.
 ur'Tipos de entidad empresarial', #Società anonima
 ur'Carlos Castrodeza', #economia della natura
 ur'Debate Bohr-Einstein', #Filosofia della Fisica
 ur'Anekantavada', #ahiṃsā
 ur'Vittorio Bottego', #it
 ur'Baldassarre Boncompagni', #it
 ur'Cobitis', #di Zoologia
 ur'Danilo Zolo', #della teoria democratica
 ur'Gilberto Rodríguez (biólogo)', #pt (tiene errores)
 ur'Die Ärzte', #Debil
 ur'Dino Formaggio', #it
 ur'Etnica (grupo musical)', #Etnica
 ur'Glissando', #it
 ur'Istituto Nazionale di Astrofisica', #di Astrofisica
 ur'Hagure Yūsha no Estetica', #no Estetica
 ur'Latino sine Flexione', #it
 ur'Historia del idioma italiano', #it
 ur'Irene Grandi (álbum)', #it (tiene errores)
 ur'Livorno', #it
 ur'Luigi Buscalioni', #it
 ur'José Torrubia', #cast antiguo
 ur'Andrea Comparetti', #it
 ur'Copa Ibérica de rugby', #pt
 ur'Economía de las organizaciones', # fr
 ur'Francesco II de Ventimiglia', # it
 ur'Giancarlo Fisichella', # Fisico
 ur'Il secondo tragico Fantozzi', #secondo tragico
 ur'Luigi Pareyson', #it (tiene errores)XS
 ur'Mario Donizetti', #it
 ur'Marquesado de Irache', #it
 ur'Simone I de Ventimiglia', #Lettere e Filosofia
 ur'Leyes raciales fascistas', #testo unico
 ur'Anexo:Bibliografía de Italo Mancini', #it
 ur'Amilcare Fantoli', #Società Geografica
 ur'Piergiorgio Odifreddi', #Il matematico, del matematico
 ur'Giuseppe Moscati', #L'anatomia 
 ur'Gianfranco Pasquino', #sviluppo politico
 ur'Mario Perniola', #Estetica news (tiene errores)
 ur'Anexo:Sondeo de las elecciones presidenciales de Estados Unidos de 2012', #Politico (George Washington University)
 ur'Carlo Aymonino', #dell'Istituto técnico
 ur'Economía forestal', #economia della'
 ur'Cocina calabresa', #Traducción incompleta (piatto tipico)
 ur'Giovanni I de Ventimiglia', #Storia Cronológica
 ur'Attilio Celant', #it
 ur'Guerra Civil Española en el País Vasco', #van tomando esta sumando
 ur'Henry Surtees', #tras recorrer esta haciendo un recto
 ur'Dassault Mirage 2000', #Avion de combat
 ur'División de Honor de Rugby 2012-2013', #Unio Esportiva. Ya corregido
 ur'Gina Pane', #un rayon dey soleil
 ur'Estadística multivariante', #se basa en explicar esta recurriendo a otras
 ur'Estatocracia', #nexos muy próximos con esta contrarrestando los cuerpos
 ur'Fernygueira', #Aldea de Melon
 ur'Divini Redemptoris', #Societatis Unio
 ur'Àngels Gonyalons', #Estan Tocant La Nostra Cançó
 ur'Críticas liberales al marxismo', # inversa a esta poniendo de cabeza
 ur'Ninja Gaiden', # Dragon's Claw
 ur'Días extraños', # esta cuando
 ur'True Blood (temporada 2)', # Avion Baker
 ur'Juego de la oca', #Dado a dado
 ur'Mario Vargas Llosa', #peur de l'avion
 ur'Anexo:Falsos amigos',
 ur'Ciudad metropolitana (Italia)', #integrarse a esta conformando
 ur'Club Deportivo Izarra', #en esta compitiendo
 ur'Combate de Concepción', #Concepcion ... .jpg(Corregido)
 ur'Corporación Deportes Quindío', #Dante Pais
 ur'Società Sportiva Calcio Napoli', #Valon(Corregido)
 ur'Sofía Zámolo', #Eximia
 ur'Sol Badguy', #su Dragon Install
 ur'Televiteatros', #Jorge Pais
 ur'Thatcherismo', #Thatcher intentó corregir esta centralizando una
 ur'Cartuja de Ara Christi', # estan en dit testament
 ur'Catedral de León', #Estan escriptas
 ur'Phil Anselmo', #Christ Inversion
 ur'Cayos Miskitos', #Tiburon Rip, Estan Rip
 ur'¡Qué linda es mi familia!', #imagen = Película que linda es mi familia.jpg
 ur'Azalaís de Porcairagues', #aucellet estan mut
 ur'Booker T', #siendo un miembro destacado de esta cambiando a Heel.
 ur'Cabeza Reina', #se puede coger esta cuando
 ur'Campeonato Mundial en Parejas de AAA', #Joe Lider
 ur'Estado Soberano de Cundinamarca', #esta arriba hasta
 ur'Estado Soberano de Boyacá', #esta arriba hasta
 ur'Asunción', #Asuncion montaje.jpg
 ur'Pieza para teclado en fa mayor (Mozart)', #esta viva pieza
 ur'Grup de Folk',
 ur'Cueva de Valporquero',
 ur'The Twilight Saga: Breaking Dawn - Part 1', #Condon
 ur'Anexo:Primera temporada de A.N.T. Farm', #Tacon-City
 ur'Adam Sandler', #Club Baston
 ur'Anexo:MTV Video Music Awards 2001', #Aqui
 ur'Alomorfo', # cancion-es
 ur'Hailee Steinfeld', #Baston
 ur'Liz Vassey', #Lider Pangea
 ur'Demandafolk', #compañia do Ruido
 ur'Daniel Rosten', #Legion
 ur'Cirque du Soleil', #Balcon Vert
 ur'William Jardine', # Le Pichon
 ur'Tormenta de espadas', #Balon
 ur'Anexo:Discografía de Lucia di Lammermoor', #alla it
 ur'Autovía/Autopista del Cantábrico', #Llovio
 ur'Anexo:Divisiones regionales de fútbol en Italia', #Categoria it
 ur'Rodolfo Valentino', #Alla
 ur'San Pío X alla Balduina (título cardenalicio)', #alla
 ur"Sa'ud bin Rashid Al Mu'alla", #alla
 ur'Juan el Apóstol', # Dolio
 ur'Via Embratel', #Via pt
 ur'Anexo:Red de Carreteras de la Comunidad Valenciana', #Via
 ur'Terminal Jardim Ângela', #Via
 ur'Anexo:Puentes romanos', #Via
 ur'Francisco Molinelli', #dió
 ur'Hipótesis de Navier-Bernouilli',#Tensiónes y deformaciónes en materiales elásticos
 ur'Anexo:Discografía de Fall Out Boy', #Policia
 ur'DDCT', #Clutch Transmision
 ur'Ricard Creus', #dónes
 ur'Will Ferrell', #Cimarron Hills
 ur'Baltasar Carlos de Austria', #Castellano antiguo sin cite
 ur'Martín Balza', #Legion D’Honneur, Supervision Organisation
 ur'Segunda campaña al sur de Chile', #Textos antiguos sin cite.
 ur'Anexo:Personajes de Diego Capusotto', #abusos del lenugjes en su lírica
 ur'A1 (Croacia)', #Tifon y Petrol (empresas)
 ur'Anexo:Casos de dopaje en el deporte', #transfusion
 ur'Gérard Courant', #Petite intrusion, 
 ur'Colonias y protectorados de Gran Bretaña', #lease territory
 ur'John T. Reed', #Lease options
 ur'Sayula', #Parian
 ur'Dragon 32/64', #el Dragon
 ur'Fuerzas policiales por país', #Peloton de Gendarmerie
 ur'Anexo:Personajes de Fairy Tail', #Dragon Slayer
 ur'Phoebe Buffay', #Tigh Mega Tampon.
 ur'Cetoacidosis diabética', #anion gap
 ur'Enron', #La Union Bank
 ur'Anexo:Aves de México', #Eupherusa eximia, Habia rubica, Habia fuscicauda
 ur'Lotus Cars', #Proton Holdings Berhad
 ur'Falcon 4.0', #Escuadron111
 ur'Network Q RAC Rally Rally Championship', #Proton Wira
 ur'Club Basquet Inca', #comunicacion@basquetinca.com
 ur'Manga', #de Dragón Ball
 ur'Catete (Río de Janeiro)', #Aterro do
# ur'1985', # Valon Behrami(Corregido)
 ur'Galeon', #Si acento el navegador
 ur'Baltasar Gracián', #castellano antiguo(revisar)
 ur'Verona', #el Liston
 ur'2 de diciembre', #Jarron Collins
 ur'1 de noviembre', # Florent Carton Dancourt
 ur'Varsovia', #Leon Schiller
 ur'Célula (desambiguación)', #de Dragon Ball
 ur'Vergara', #la religion et
 ur'Anillo (matemática)', #Boca Raton,
 ur'Himno nacional de Bolivia', #wastat cojon surañani
 ur'Teoría del Big Bang', #de rayon croissant
 ur'Aeropuerto Intercontinental George Bush', #Baron Aviation Services
 ur'Imperio sasánida', #Partia
 ur'Francis Bacon', #Baron of Verulam,
 ur'Lenguas galoitalianas', #senpro lo balcona, sera
 ur'Juana de Arco', #Ponton de Xantrailles
 ur'Campaña del Loira', #Ponton de Xantrailles
 ur'Historieta en los Estados Unidos', #Mike Baron
 ur'Iannis Xenakis', #Mezcla es-fr
 ur'Olympe de Gouges', #Títulos en francés
 ur'Ajedrez', #Repeticion
 ur'Andorra',
 ur'Argentina',
 ur'República Dominicana', #Juan Dolio
 ur'Islandsflug', #Wet lease
 ur'Marco Aurelio', #Partia
 ur'Enrique Granados', #Subira
 ur'Boeing B-17 Flying Fortress', #Lease
 ur'Rock instrumental', #Batio
 ur'Carl Ludwig Philipp Zeyher', #Unio Itineraria
 ur'Evan Burrows Fontaine', #Comedian
 ur'Transcarga', #Wet Lease
 ur'Provincia de Misiones', #Aburria
 ur'Historia del Real Club Deportivo de La Coruña', #Subias
 ur'Rino Gaetano',
 ur'Anselmo Clavé', #Para ninos
 ur'Coahuayana', #cuagiote de serro
 ur'Zócalo de la ciudad de Puebla', # Parian
 ur'Fortaleza (Ceará)', #Aterro
 ur'Tiro con arco', #Partia
 ur'Ragonvalia', #Aburria
 ur'Anexo:La Academia 2002', #Corazón partio
 ur'Mandarín (cómic)',
 ur'José Antonio Bottiroli', #La ultima curda?
 ur'Hom-Idyomo', #esperantino
 ur'Bauang', #Parian
 ur'S-125 Neva/Pechora', #servias
 ur'Conservación y restauración de metales', #&nbsp; espacio
 ur'Monte Kenia', #Batian
 ur'Juan Galiffi', #lo ultima
 ur'Anexo:La academia 2012',# partío
 ur'República Dominicana', #Dolio
 ur'Fuego Solar', #Ultimo
 ur'Doma clásica', #Ultimo
 ur'Cine de explotación', #Ultimo
 ur'Pupi Avati', #Ultimo
 ur'Helleborus lividus', #Ultimo
 ur'Helleborus foetidus', #Ultimo
 ur'Anexo:Equipos de fútbol por país', #Ahi
 ur'Anexo:Dux de Génova', #Ultimo
 ur'Anexo:Premio Grammy al mejor álbum de banda sonora para película, televisión u otro medio visual', #Ultimo
 ur'Ugo Tognazzi', #Ultimo minuto
 ur'Película de culto', #Ultimo Mondo Cannibale
 ur'Peaches Geldof',#Ultimo
 ur'Bernardo Bertolucci', #Ultimo tango
 ur'Diferencias entre el español y el portugués', #pt
 ur'Italo Calvino', #Último viene il corvo
 ur'155',
 ur'Henry Fonda',#Ultimo atto
 ur'Stan Lee',
 ur'José Cardoso Pires',
 ur'Olentzero',#Soterro
 ur'1766', #Unico Wilhem van Wassenaer
 ur'Osamu Tezuka',#Unico
 ur'Ignacio Ramonet',#Il Pensiero Unico
 ur'2 de noviembre',#Unico Wilhem van Wassenaer
 ur'9 de noviembre',#Unico Wilhem van Wassenaer
 ur'Sisena Estatilio Tauro', #Salio
 ur'Ponce de Minerva', #Salio
 ur'Carande', #Salio
 ur'La melodía de Broadway',#Nacio Herb Brown
 ur'Power Rangers: Mystic Force', #Dimitira
 ur'Reinos de los burgundios', #Salio
 ur'Carlos Vela',#Copa Nacio.
 ur'Vitaliano', #Merecio
 ur'Tin Pan Alley', #Nacio Herb Brown
 ur'Historia de la ciudad de Valencia', #Error en URL.
 ur'Embalse de Riaño', #Salio
 ur'Torre de Don Miguel',#del Salio.
 ur'Formación territorial de España', #Castellano antuguo sin cita
 ur'Siglo de Oro Valenciano', #Cita no identificada
 ur'Anita Page',#Nacio Herb Brown
 ur'Carande', #Salio
 ur'Algemesí', #Unio elongatulus
 ur'Juegos Olímpicos de Río de Janeiro 2016', #Aterro de Flamengo
 ur'Lindsay Lohan', #Alli
 ur'Cantón Atahualpa',#Florecio
 ur'Escuela de Traductores de Toledo', #Salio
 ur'Anexo:Videojuegos para Sega Master System', #Salio
 ur'Adalberón de Eppenstein', #Salio
 ur'Eneida', #Salio
 ur'Anexo:Despoblados de la provincia de León', #Salio
 ur'Pallava', #Partia
 ur'Elota',
 ur'Tu cara me suena (Chile)',
 ur'Colección definitiva',
 ur'Interglossa',
 ur'Quando el Rey Nimrod',
 ur'Sebastián Yepes',
 ur'Alberto Ruiz-Gallardón',
 ur'Juan Cruz Alli',
 ur'Pamplona',
 ur'Pascal (lenguaje de programación)',
 ur"Centre d'Esports Sabadell Futbol Club",
 ur"Ibídem (banda)",
 ur'(75) Eurídice',
 ur'(76) Freya',
 ur'(77) Friga',
 ur'1.fm',
 ur'1244',
 ur'1692',
 ur'1854',
 ur'189 a. C.',
 ur'1948',
 ur'1998',
 ur'22 de junio',
 ur'A.A',
 ur'Acorn Communicator',
 ur'Adolpho Ducke',
 ur'Aeropuerto Coronel Felipe Varela',
 ur'Aeropuerto Internacional General Abelardo L. Rodríguez',
 ur'Aeropuerto Internacional de Cancún',
 ur'Ager (Lérida)',
 ur'Agustina Bessa-Luís',
 ur'Aisle Of Plenty',
 ur'Akcent',
 ur'Albania',
 ur'Albert Om',
 ur'Alfonso III de Portugal',
 ur'Alfonso X de Castilla',
 ur'Alguna pregunta més?',
 ur'Aline Barros',
 ur'Alpha Centauri (álbum)',
 ur'Alveolitis alérgica extrínseca',
 ur'Ambar (Grupo Musical)',
 ur'Amots Dafni',
 ur'Anexo:Abreviaturas latinas',
 ur'Anexo:Acorazados',
 ur'Anexo:Artistas y temas de Italo Disco',
 ur'Anexo:Asteroides (7501)–(7600)',
 ur'Anexo:Atletismo en los Juegos Olímpicos de Atenas 2004 - 400m vallas masculino',
 ur'Anexo:Bibliografía sobre Paulo Orosio',
 ur'Anexo:Bibliografía sobre temas afrobrasileños',
 ur'Anexo:Biblioteca Virtual de Paraguay',
 ur'Anexo:Ciudades de Brasil',
 ur'Anexo:Composiciones de Domenico Cimarosa',
 ur'Anexo:Composiciones de Simon Mayr',
 ur'Anexo:Comunas de Alto Saona',
 ur'Anexo:Cónsules romanos (Alto Imperio)',
 ur'Anexo:Discografía de Egberto Gismonti',
 ur'Anexo:Discografía de Nelly Furtado',
 ur'Anexo:Dux de Venecia',
 ur'Anexo:Escritores de Portugal',
 ur'Anexo:Escuelas de samba de Brasil',
 ur'Anexo:Escuelas de samba',
 ur'Anexo:Especies de Aegiphila',
 ur'Anexo:Especies de Caladenia',
 ur'Anexo:Especies de Inga',
 ur'Anexo:Freguesias de Portugal',
 ur'Anexo:Fuentes musicales del Renacimiento de España',
 ur'Anexo:Grupos de música antigua',
 ur'Anexo:Géneros de Astéridas',
 ur'Anexo:Géneros de rósidas',
 ur'Anexo:Lemas de Estado',
 ur'Anexo:Lista de aves de Sibley-Monroe 18',
 ur'Anexo:Localidades de Italia',
 ur'Anexo:Los lemas de EE.UU.',
 ur'Anexo:MTV Video Music Awards Latinoamérica 2002',
 ur'Anexo:Montañas más altas del mundo',
 ur'Anexo:Municipios de la provincia de Lérida',
 ur'Anexo:Municipios del estado de Goiás por población',
 ur'Anexo:Municipios del estado de Minas Gerais por población',
 ur'Anexo:Municipios del estado de Rio Grande do Sul por población',
 ur'Anexo:Nombres botánicos según la abreviatura del autor',
 ur'Anexo:Nombres botánicos según la abreviatura del autor/G-H-I',
 ur'Anexo:Nombres de ciudades de Europa en diferentes idiomas',
 ur'Anexo:Partidos inscritos en el Registro de Partidos Políticos del Ministerio del Interior de España',
 ur'Anexo:Patrimonio de la Humanidad en España',
 ur'Anexo:Países de África',
 ur'Anexo:Personajes de Héroes',
 ur'Anexo:Personajes de ¡Oye, Arnold!',
 ur'Anexo:Premio Femina',
 ur'Anexo:Promoción de ascenso a Segunda División de España 2003/04',
 ur'Anexo:Series con contenido yuri',
 ur'Anexo:Óperas',
 ur'Angel (King of Fighters)',
 ur'Aniba ferrea',
 ur'Anthocerotales',
 ur'Antoni Mus',
 ur'Antonio Vivaldi',
 ur'Antony Tudor',
 ur'António Luís de Sousa, Marqués de Minas',
 ur'Aparato de Golgi',
 ur'Apis mellifera sicula',
 ur'Apostasia nuda',
 ur'Apostasia wallichii',
 ur'Aragonés del valle de Vió',
 ur'Arisarum simorrhinum',
 ur'Arte de Cataluña',
 ur'Arte',
 ur'Arthur Fallot',
 ur'Arthur Schnitzler',
 ur'Asparagus acutifolius',
 ur'Aulo Cascelio',
 ur'Aurora de Chile',
 ur'Avatar (Ultima)',
 ur'Avatar (desambiguación)',
 ur'Avepoda',
 ur'Balzi Rossi',
 ur'Bandera de Chile',
 ur'Bandera del Perú',
 ur'Barcelona Televisió',
 ur'Barcelona',
 ur'Bartsia',
 ur'Batalla de Dara',
 ur'Batalla de Moquegua',
 ur'Bathory',
 ur'Beato de Liébana',
 ur'Beatriz de Día',
 ur'Bellido Dolfos',
 ur'Benito Arias Montano',
 ur'Bertus Aafjes',
 ur'Bioinformática',
 ur'Biología molecular',
 ur'Bloque Nacionalista Galego',
 ur'Borja Penalba',
 ur'Bryan-Michael Cox',
 ur'Bítem',
 ur'CYP1B1',
 ur'Caesalpinia spinosa',
 ur'Camille Alaphilippe',
 ur'Camisas negras',
 ur'Campeonato Mineiro',
 ur'Candomblé',
 ur'Canto de la Sibila',
 ur'Caproidae',
 ur'Captador de viento',
 ur'Carl Fredrik Fallén',
 ur'Carlos de la Fuente',
 ur'Carmina Burana (cantata)',
 ur'Carnivora',
 ur'Carreteras de Extremadura',
 ur'Carta foral de Vega de Doña Olimpa',
 ur'Casa de Barcelona',
 ur'Casabermeja',
 ur'Casimiro Gómez Ortega',
 ur'Castries (Hérault)',
 ur'Caterina Vertova',
 ur'Catálogo de obras de Cimarosa',
 ur'Cayo César',
 ur'Cayo San Jorge',
 ur'Cedi',
 ur'Charles Gounod',
 ur'Chevron Corporation',
 ur'Cilenos',
 ur'Cilicia',
 ur'Cine de Japón',
 ur'Circus (álbum de Britney Spears)',
 ur'Cistus clusii',
 ur'Claudiano',
 ur'Coccothrinax',
 ur'Codex Las Huelgas',
 ur'Colombia',
 ur'Francisco Mignone',
 ur'Francisco das Chagas Santos',
 ur'Francisco de Contreras',
 ur'Franco Alfano',
 ur'François Rozier',
 ur'Françoiz Breut',
 ur'Freiria',
 ur'Freyja',
 ur'Futbol Club Casa del Benfica',
 ur'Futbol Club Santboià',
 ur'Fíbula prenestina',
 ur'Fútbol',
 ur'Gaston Eugène Marie Bonnier',
 ur'Geometría descriptiva',
 ur'George Wesley Bellows',
 ur'Giacomo Leopardi',
 ur'Giezi',
 ur'Gilbert Bécaud',
 ur'Giordano Bruno',
 ur'Giorgione',
 ur'Giovanni Paisiello',
 ur'Giovanni Sartori',
 ur'Giulio Paoletti',
 ur'Giuseppe Zanardelli',
 ur'Gochu asturcelta',
 ur'Gospel nigeriano',
 ur'Gramática catalana',
 ur'Gramática del húngaro',
 ur'Gramática latina',
 ur'Greci (Italia)',
 ur'Guarani Futebol Clube',
 ur'Guardian (Ultima)',
 ur'Guerra del Pacífico',
 ur'Guerra ruso-turca (1787-1792)',
 ur'Guglielmo Ferrero',
 ur'Guia (Albufeira)',
 ur'Guia',
 ur'Hans Peter Linder',
 ur'Harina',
 ur'Hawala',
 ur'Henry Merritt Paulson Jr.',
 ur'Here Today, Tomorrow, Next Week!',
 ur'Heroes of Might and Magic',
 ur'Heteralocha acutirostris',
 ur'Hilleria',
 ur'Himno Nacional del Perú',
 ur'Himno de San Vicente del Raspeig',
 ur'Historia de Japón',
 ur'Historia de Los Angeles Lakers',
 ur'Historia de los judíos de Salónica',
 ur'Homonimia',
 ur'Hopea',
 ur'Horus',
 ur'Huia',
 ur'Hydrocotyle ranunculoides',
 ur'II Gobierno Constitucional de Portugal',
 ur'Ibagué',
 ur'Idioma gallego',
 ur'Idioma grecocalabrés',
 ur'Idioma tartésico', 
 ur'Idioma valón',
 ur'Idioma véneto',
 ur'Iglesia católica caldea',
 ur'Iglesia evangélica de Marín',
 ur'Il mostro',
 ur'Imitaria',
 ur'Imperio bizantino',
 ur'Incendio de la Iglesia de la Compañía',
 ur'Inmunología de la reproducción',
 ur'Interlingua',
 ur'Invasión luso-brasileña',
 ur'Irias',
 ur'Islandia',
 ur'Islas Cook',
 ur'Isuzu',
 ur'Jack Hawkins',
 ur'Jacques Ozanam',
 ur'Jainal Antel Sali, Jr. ‎',
 ur'Jardín Botánico de Santa Catalina',
 ur'Java Network Launching Protocol',
 ur'Java SE',
 ur'Javi Rodríguez Gonzalvo ‎',
 ur'Jay-Z',
 ur'Joan-Josep Tharrats',
 ur'Joaquim Carbó',
 ur'Joaquim Nabuco',
 ur'Johann Sebastian Bach',
 ur'Jorge Manuel Guerra Tadeu',
 ur'Josep Lobató',
 ur'Josep Maria Andreu',
 ur'Josep Maria Espinàs',
 ur'Josep Maria Llompart de la Peña',
 ur'Joseph Haydn',
 ur'José Antonio Moreno Jurado',
 ur'José Eduardo Agualusa',
 ur'Juan Gerson',
 ur'Juan de Colonia',
 ur'Juan del Camino',
 ur'Juan del Encina',
 ur'Julien Benda',
 ur'Julio César',
 ur'Julio Nieto Bernal',
 ur'Julià Guillamon',
 ur'Kamehameha I',
 ur'Kane',
 ur'Karakuridōji Ultimo',
 ur'Kevin Goldthwaite',
 ur'Kung Fu Panda: Legendary Warriors',
 ur'Kylie Live: X2008',
 ur'LD',
 ur'Laguna Carreras',
 ur'Laguna Las Habras',
 ur'Laticlave',
 ur'Le Tronquay (Eure)',
 ur'Lenguas romances',
 ur'Lenguas ugrofinesas',
 ur'Lepanthes',
 ur'Ley Sálica',
 ur'Leyes de Newton',
 ur'Libro de Mormón',
 ur'Liga Premier de Kuwait',
 ur'Lista de códigos CIE-10',
 ur'Lista de municipios de Barcelona',
 ur'Literatura en catalán',
 ur'Literatura en letón',
 ur'Litteris et artibus',
 ur'Lluís Fullana i Mira',
 ur'Lluís Llach',
 ur'Locuciones latinas',
 ur'Lontra',
 ur'Lord British',
 ur'Lorenzo Pasinelli',
 ur'Los Amigos Invisibles',
 ur'Los caballeros de la cama redonda',
 ur'Low-Life',
 ur'Ludwig Reichenbach',
 ur'Luigi Cremona',
 ur'Lápiz Consciente',
 ur'Léon de Poncins',
 ur'Línea 24 (San Juan)',
 ur'Madredeus',
 ur'Magimaster',
 ur'Mallorquín',
 ur'Manuel Ainaud',
 ur'Manuscrito ilustrado',
 ur'Marco Bellocchio',
 ur'Marcos Antonio Portugal',
 ur'Marcos Pérez Jiménez',
 ur'Marcos el Evangelista',
 ur'Naxos (Sicilia)',
 ur'Nectariniidae',
 ur'Negre Lloma',
 ur'Nighthawks',
 ur'No More Heroes 2: Desperate Struggle',
 ur'Noble camino óctuple',
 ur'Noblejas',
 ur'Norberto Bobbio',
 ur'Normativa oficial del idioma gallego',
 ur'Novallas',
 ur'Nuestra Señora de Lourdes',
 ur'Ojos Negros (canción) ‎',
 ur'Ontinyent Club de Futbol',
 ur'Orden de Malta',
 ur'Organización territorial de Etiopía',
 ur'Original equipment manufacturer',
 ur'Orphénica Lyra',
 ur'Ortega (Tolima)',
 ur'Osea',
 ur'Oswald el conejo afortunado',
 ur'Palma de Mallorca',
 ur'Palíndromo',
 ur'Panceta',
 ur'Papiamento',
 ur'Parietaria judaica',
 ur'Parque nacional Costa Occidental de Isla Mujeres, Punta Cancún y Punta Nizuc',
 ur'Parques y jardines de Menton',
 ur'Pastún',
 ur'Patrick Besson',
 ur'Patrulla ASPA',
 ur'Pau Riba',
 ur'Paul Copin-Albancelli',
 ur'Paul Irwin Forster',
 ur'Paul Klee',
 ur'Pedro Guillermo Ángel Guastavino',
 ur'Pedro Hurtado de la Vera',
 ur'Pedro de Castilla y Molina',
 ur'Pello Salaburu',
 ur'Pendia',
 ur'Peppino De Filippo',
 ur'Perejaume',
 ur'Perm',
 ur'Perusa',
 ur'Perú',
 ur'Peteroa',
 ur'Petra Magoni',
 ur'Pietro Metastasio',
 ur'Pipile cumanensis',
 ur'Pipile pipile',
 ur'Pitrí (hinduismo)',
 ur'Piñeragate',
 ur'Plantilla:Ficha de parque de atracciones',
 ur'Plantilla:Lista de episodios',
 ur'Poesía culta en la literatura medieval española',
 ur'Polícrates de Éfeso',
 ur'Pombal',
 ur'Porcellio',
 ur'Portal lunar',
 ur'Porter Peter Lowry',
 ur'Portoviejo',
 ur'Portuñol riverense',
 ur'Power Rangers: Operation Overdrive',
 ur'Premio Jabuti de Literatura',
 ur'Presidente de Venezuela',
 ur'Pretérito anterior',
 ur'Primera División de México Clausura 2009',
 ur'Proyecto Fenix',
 ur'Proyecto de investigación',
 ur'Publio Cornelio Escipión el Africano',
 ur'Puerto de las Governadas',
 ur'Purépero de Echáiz',
 ur'Quechua costeño',
 ur'Quinta guerra israelita-aramea',
 ur'Ramon Casas',
 ur'Ramón de la Sagra',
 ur'Ratos de Porão',
 ur'Real Sociedad Matemática Española',
 ur'Regimen Sanitatis Salernitanum',
 ur'Renata Tebaldi',
 ur'Reseña histórica de Miraflores (Lima)',
 ur'Rey Sol (álbum)',
 ur'Ricard Pérez Casado',
 ur'Robert Saladrigas',
 ur'Robotech',
 ur'Rococó',
 ur'Roger Garcia Junyent',
 ur'Roman Pais',
 ur'Rongo rongo',
 ur'Rosa',
 ur'Villa Capra',
 ur'Villa Rosaura',
 ur'Vincenzo Bianchini',
 ur'Vincenzo Riccobono',
 ur'Vitovt Putna',
 ur'Wasan',
 ur'Wentworth Miller',
 ur'Whittier (California)',
 ur'Whose Line Is It Anyway?',
 ur'Wisconsin',
 ur'X-men Evolution Rogue',
 ur'Xesús Alonso Montero',
 ur'Xoán Piñeiro Nogueira',
 ur'Xul Solar',
 ur'Zanfona',
 ur'Áhimsa',
 ur'Área Vitivinícola Americana',
 ur'Literatura en euskera',
 ur'Inmigración en Chile',
 ur'César Borgia',
 ur'Mohamed Rouicha',
 ur'Iglesia Arciprestal de Santa María del Salvador (Chinchilla de Montearagón)',
]

def titulo(m):
    txt = m.group('tt')
    return m.group('ii')+txt[0]+txt[1:].lower()+m.group('dd')

##Emacs: '_\(.\)\(.*\)\(.*?\)\(.*\)__\1\2\(.*?\)\4' -> '[\1\1]\2_\3_\4_\5'
##sort  -k1,1 -k3,3nr  -k2,2 -t ';' 
##sort -t "#" -k "2nr"
#lema(ur'[Aa]_rbóre_(?:as|os?)_rbore') + #803 Arborea Puras matas
#lema(ur'[Aa]ll_á__a') + #2447
#lema(ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) [Cc]_ómic_(?![- ](?:Con|[Ss]ans))_omic') + #2527
#lema(ur'_ásper_(?:as|os?)_asper') + lema(ur'_Ásper_(?:as|os?)_Asper') + #530
#lema(ur'_áure_[ao]s?_aure') + lema(ur'_Áure_[ao]s?_Aure') + #1018 Matas
#lema(ur'[Dd]_i_putado_e') + #76 cuidado pt
#lema(ur'[Oo]limp_i_adas_í') + #107 olimpiada/olimpíada
#lema(ur'[Aa]pro_b_ad[ao]s?_v') + #11 cuidado pt
#lema(ur'[Ee]_x_planada_s') + #37 cuidado pt
#lema(ur'[Dd]e_s_velad[ao]s?_') + #70 develar/desvelar
#lema(ur'[Ll]e_o_nes_ó') + #Leonés/2
#lema(ur'gir_á_ndo(?:(?:[mts]e|nos)(?:las|les?|)|l[aeo]s?)_a') + #1 Girandola
#lema(ur'[Ll]eg_í_tim[ao]_i') + #1
#lema(ur'[Ss]imult_á_nea_a') + #simultanear
 #Mason (en)
 #Nipon
 #No existe prión
 #guión o guiones
 #ion o ión
#lema(ur'_Í_ntegr[ao]s? (?:l[ao]s?|el|lo) _I') + #AC integra
#lema(ur'_í_ntegr[ao]_i') + lema(ur'_Í_ntegr[ao]_I') + #integrar
#lema(ur'San Jos_é_(?! (?:Oaks|Earthquakes))_e') + #1
#lema(ur'[Cc]ol_ó_n_o') + #a.c colon
#lema(ur'Cimarr_o_n_ó', pre=ur'[Cc]ondados? de ') + #1
#lema(ur'Megat_ón|Megatones]]__[óo]n\]\]es') + lema(ur'megat_ón|megatones]]__[óo]n\]\]es') + #1
#lema(ur'Prot_ón|Protones]]__[óo]n\]\]es') + lema(ur'prot_ón|protones]]__[óo]n\]\]es') + #1
#lema(ur'Aler_ón|Alerones]]__[óo]n\]\]es') + lema(ur'aler_ón|alerones]]__[óo]n\]\]es') + #1
#lema(ur'Ax_ón|Axones]]__[óo]n\]\]es') + lema(ur'ax_ón|axones]]__[óo]n\]\]es') + #1
#lema(ur'[Bb]al_ó_n(?!\]| Greyjoy)_o') + #1
#lema(ur'Batall_ón|Batallones]]__[óo]n\]\]es') + lema(ur'batall_ón|batallones]]__[óo]n\]\]es') + #1
#lema(ur'Concreci_ón|Concreciones]]__[óo]n\]\]es') + lema(ur'concreci_ón|concreciones]]__[óo]n\]\]es') + #1
#lema(ur'confecci_ón|confeccion\g<x>]]__[óo]n\]\](?P<x>es|ar?)') + #1
#lema(ur'Conjugaci_ón|Conjugaciones]]__[óo]n\]\]es') + lema(ur'conjugaci_ón|conjugaciones]]__[óo]n\]\]es') + #1
#lema(ur'Convulsi_ón|Convulsiones]]__[óo]n\]\]es') + lema(ur'convulsi_ón|convulsiones]]__[óo]n\]\]es') + #1
#lema(ur'Deportaci_ón|Deportaciones]]__[óo]n\]\]es') + lema(ur'deportaci_ón|deportaciones]]__[óo]n\]\]es') + #1
#lema(ur'Depresi_ón|Depresiones]]__[óo]n\]\]es') + lema(ur'depresi_ón|depresiones]]__[óo]n\]\]es') + #1
#lema(ur'Ecorregi_ón|Ecorregiones]]__[óo]n\]\]es') + lema(ur'ecorregi_ón|ecorregiones]]__[óo]n\]\]es') + #1
#lema(ur'embri_ón|embrion\g<x>]]__[óo]n\]\](?P<x>es|ari[ao]s?)') + #1
#lema(ur'Especificaci_ón|Especificaciones]]__[óo]n\]\]es') + lema(ur'especificaci_ón|especificaciones]]__[óo]n\]\]es') + #1
#lema(ur'Exportaci_ón|Exportaciones]]__[óo]n\]\]es') + lema(ur'exportaci_ón|exportaciones]]__[óo]n\]\]es') + #1
#lema(ur'Gasc_ó_n(?!\]| Modernes)_o') + #1
#lema(ur'Hur_o_n_ó', pre=ur'[Cc]ondados? de ') + #1
#lema(ur'Importaci_ón|Importaciones]]__[óo]n\]\]es') + lema(ur'importaci_ón|importaciones]]__[óo]n\]\]es') + #1
#lema(ur'instruccion_es]]__\]\]es') + #1
#lema(ur'Intoxicaci_ón|Intoxicaciones]]__[óo]n\]\]es') + lema(ur'intoxicaci_ón|intoxicaciones]]__[óo]n\]\]es') + #1
#lema(ur'Inundaci_ón|Inundaciones]]__[óo]n\]\]es') + lema(ur'inundaci_ón|inundaciones]]__[óo]n\]\]es') + #1
#lema(ur'[Mm]ascar_ó_n(?!\])_o') + #?????
#lema(ur'Melocot_ón|Melocotones]]__[óo]n\]\]es') + lema(ur'melocot_ón|melocotones]]__[óo]n\]\]es') + lema(ur'melocot_ón|melocoton\g<x>]]__[óo]n\]\](?P<x>es|eros?)') + #1
#lema(ur'Microrregi_ón|Microrregiones]]__[óo]n\]\]es') + lema(ur'microrregi_ón|microrregiones]]__[óo]n\]\]es') + #1
#lema(ur'migraci_ón|migraciones]]__[oó]n\]\]es') + lema(ur'Migraci_ón|Migraciones]]__[oó]n\]\]es') + #1
#lema(ur'Monz_ón|Monzones]]__[óo]n\]\]es') + lema(ur'monz_ón|monzones]]__[óo]n\]\]es') + #1
#lema(ur'Mutaci_ón|Mutaciones]]__[óo]n\]\]es') + lema(ur'mutaci_ón|mutaciones]]__[óo]n\]\]es') + #1
#lema(ur'Preposici_ón|Preposiciones]]__[óo]n\]\]es') + lema(ur'preposici_ón|preposiciones]]__[óo]n\]\]es') + #1
#lema(ur'Privatizaci_ón|Privatizaciones]]__[óo]n\]\]es') + lema(ur'privatizaci_ón|privatizaciones]]__[óo]n\]\]es') + #1
#lema(ur'Procesi_ón|Procesiones]]__[óo]n\]\]es') + lema(ur'procesi_ón|procesiones]]__[óo]n\]\]es') + #1
#lema(ur'Pulm_ón|Pulmones]]__[óo]n\]\]es') + lema(ur'pulm_ón|pulmones]]__[óo]n\]\]es') + #1
#lema(ur'Riñ_ón|Riñones]]__[óo]n\]\]es') + lema(ur'riñ_ón|riñones]]__[óo]n\]\]es') + #1
#lema(ur'Tradici_ón|Tradiciones]]__[óo]n\]\]es') + lema(ur'tradici_ón|tradicion\g<x>]]__[óo]n\]\](?P<x>es|al|ales)') + #1
#lema(ur'Vacaci_ón|Vacaciones]]__[óo]n\]\]es') + lema(ur'vacaci_ón|vacaciones]]__[óo]n\]\]es') + #1
#lema(ur'[Vv]al_ó_n(?!\])_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #1
#lema(ur'Violaci_ón|violaciones]]__[óo]n\]\]es') + lema(ur'violaci_ón|violaciones]]__[óo]n\]\]es') + #1
#lema(ur'[Qq]uin_c_e(?! (?:de Novembro|poemes|generacions))_[sz]') + #fr,ca
#lema(ur'(?:[Ee]l|[Aa]l|[Dd]el) _R_ey \[\[_r') + lema(ur'[Ll]a _R_eina \[\[_r') + #1
#lema(ur'(?:[Ee]l|[Aa]l|[Dd]el) _Prí_ncipe \[\[_(?:pr[ií]|Pri)') + lema(ur'[Ll]a _P_rincesa \[\[_p') + #1
#lema(ur'(?:[Ee]l|[Aa]l|[Dd]el) _E_mperador \[\[_e') + lema(ur'[Ll]a _E_mperatriz \[\[_e') + #1
#lema(ur'(?<!malorum )[Nn]_ó_mina(?! (?:al|el|la|un|dubia|Insecta|nuda|como|también|a))_o') + #1
#retroX(ur'(?: All\'|(?:Aenetus|Aethopyga|Alstonia|Aquilegia|Bleda|Canna|Corymbia|Dicentra|Eucalyptus|Fritillaria|Hyla|Lepanthes|Melaleuca|Maranta|Megalaima|Pleurothallis|Protea|Raulia|Romulea|Scorzonera|Solenopsis|Synopcia|Syncarpha|Talisia|Viola|var\.|[AP]\.)) [Ee]xim_i_a_í') + #1
#lema(ur'[Ss]ub_í_as?_i') + #1
#lema(ur'(?<!Marcel )Pich_ó_n(?!\]| Stevann)_o') + #1
#lema(ur'_c_ual(?:es|)_q') + lema(ur'_C_ual(?:es|)_Q') + #es ant.
#lema(ur'[Dd]emo__str(?:ó|ar|and[ao]s?|ad[ao]s?|ador|aciones|ables?|ativ[ao]s?|ándol[aeo]s?)_n') + #40 demosntración existe pero en deshuso
#lema(ur'[Ll]im_ó_n_o', xpre=[ur'Citrus × ']) + #549
#lema(ur'_D_ebian_d', pre=ur'(?:con|en|para|de) ', xpos=[ur'\.org']) + #1
#lema(ur'Am_á_n_a', pre=ur'(?:[Dd]e|[Ee]n) ') + #Aman (Tolkien)
#lema(ur'[Pp]adr_e_s?_é') + #6 Padrés (apellido)
#lema(ur'[Vv]alent_í_a_i', xpre=[ur'Vibo '], xpos=[ur' Records']) + #20 Valentia
#lema(ur'[Aa]pon_í_a[ns]?_i') + #1
#lema(ur'[Vv]er_s_e_z') + #7
#lema(ur'__a_h', pre=ur'[Ff]u[ée] ') + #Error pero otras correcciones son más probables.
#lema(ur'[Ee]na_j_enad[ao]s?_g') + #10 cas ant.
#lema(ur'[Ee]_n_tendid[ao]s?_s') + #17
#lema(ur'[Ii]nc_ó_mod[ao]s?_o') + #255Corrección manual
#lema(ur'[Pp]ar_í_a[ns]?(?!, Tehuantepec|, Edo\. Sucre)_i') + retroX(ur'[Ee]stados? par_i_as?_í') + #1
#lema(ur'_o__ó', xpre=[ur'\]\]', ur'\''], xpos=[ur' (?:teu|país|ano 2000)', ur'\]\]', ur'[ςйк]']) + #última reforma
#lema(ur'[SS]anta Mar_í_a_i', xpre=[ur'Església de ', ur'Bloomsday ', ur'Les Cantigas de ', ur'ao ', ur'Philippines '], xpos=[ur' (?:alla|dell[ae]|degli|Maddalena|Novella|Maggiore|Antica|del Paradiso|in|Nuova|de Licodia|del Fiore|Besora|Corcó|Merlès|Miralles|d|de Palautordera|Gloriosa dei|sopra|presso|Rossa|Goretti|Madalena|Kalea|Formosa|Assunta|a Colonica|Tiberina|la Major|Paganica|La Palma|Antiqua|- Diocese|e de Santa Simplichi|La Scala|Ammalati|la Stella|Lignano|Feira|Maior|a Chianni|e São|Bambina|Nativitas|Beach|e do|cuneta|Casoria|y Sant Sebastià|Val|Pelindung|a Mare|Capua|foris|Micaela de València|\(Río Grande del Sur\)|la Bruna|y Sao|Forisportam|Annunziata|Domine)']) + #1
#lema(ur'[Pp]i_o_n_ó') + #última reforma
#lema(ur'[Cc]a_m_po_n') + #4
#lema(ur'[Ll]ibrar_í_a[ns]?_i') + #libraría, Librarian
#lema(ur'[Ll]oar_í_a[ns]?_i') + #1
#lema(ur'[Pp]elar_í_a[ns]?_i', xpos=[ur' dari']) + #1
#lema(ur'[Cc]ontinuar_á_[ns]_a') + #1002 continuara
#lema(ur'_hacié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_asi[ée]') + #2
#lema(ur'[Cc]ono_cers_e_scer') + #2
#lema(ur'[Hh]eredit_a_ri[ao]s?_á') + #4 pt
#lema(ur'[Aa]cadem_i_a_í') + #3 pt
#lema(ur'ni_ñ_[ao]s?_n', pre=ur'(?:[Aa]l|[Ee]l|[Ll]as?|[Ll]os|[Mm]is?|[Ss]us?|[Dd]el?|[Pp]ara) ') + #8
#lema(ur'[Nn]ari_z__s', xpre=[ur'Barthélemy ', ur'Dilatator ']) + #1
#lema(ur'Paysand_ú__u', xpos=[ur' Sport']) + #177
#lema(ur'[Aa]fil_i_ad[ao]s? a_') + #
#lema(ur'[Aa]rd_í_an_i', xpre=[ur'Junior ', ], xpos=[ur' (?:Gashi|Aliaj|Rexhepi|Kozniku|Syaf)', ]) + #32
#lema(ur'Mat_ó_n_o', xpre=[ur'L\.\) ', ur'ex ', ur'Lower ', ur'Upper '], xpos=[ur'\]', ur', 1809', ur' (?:BB1200|Mastersound)']) + #67
#lema(ur'[Ss]emi_ó_ticas?_o', xpre=[ur'della ', ur'analisi '], xpos=[ur' (?:letteraria|della)', ]) + #17
#lema(ur'[Ss]orb_í_an?_i', xpre=[ur'[Ll]engua ', ur'televisión ', ur'es ', ur'colmena ', ur'geografía ', ur'etimología '], xpos=[ur'[\]"]', ur' Cultural']) + #61
#lema(ur'[Nn]ari_z__s', xpre=[ur'Compressor ', ur'Barthélemy ', ]) + #10
#lema(ur'[Aa]_demá_s_ dema', xpos=[ur' oijoe', ]) + #8
#lema(ur'[Aa]_demá_s_ dem[aá]') + #1
#lema(ur'Carb_o_n_ó', pre=ur'[Cc]ondados? de ') + #0
#lema(ur'[Tt]estificar_á_[ns]?_a') + #1
#lema(ur'[Dd]eclarar_á_[ns]*_a') + #1
#lema(ur'[Cc]ertificar_á_[ns]*_a') + #1
#lema(ur'[Aa]pestar_á_[ns]?_a') + #4
#lema(ur'[Cc]ontestar_á_[ns]?_a') + #28
#lema(ur'[Dd]etestar_á_[ns]?_a') + #3
#lema(ur'[Ee]ncestar_á_[ns]?_a') + #6
#lema(ur'[Ee]ncuestar_á_[ns]?_a') + #2
#lema(ur'[Mm]anifestar_á_[ns]?_a') + #124
#lema(ur'[Pp]restar_á_[ns]?_a') + #226
#lema(ur'[Pp]resupuestar_á_[ns]?_a') + #1
#lema(ur'[Aa]yudar_á_[ns]?_a') + #1
#lema(ur'[Tt]ratar_á_[ns]?_a') + #1
#lema(ur'Mar_í_a_i', pre=ur'(?:[Dd]e|[Pp]ara|[Cc]on) ', xpre=[ur'Glória ', ur'[Éé] [Dd]ia ', ur'Coração ', ], xpos=[ur' +(?:†|da |Beth[aâ]nia|Stuarda|Shriver|Puig i|Augusta de Barros|Jackson)', ]) + #1447
#lema(ur'_Á_rida_A', xpre=[ur'Pedro ', ur'Persio ', ur'\[\[', ur'\'\'\'\'\''], xpos=[ur' (?:arizonica|blepharophylla|carnosa|coulteri|crispa|mattturneri|parviflora|riparia|turneri)', ur'(?:\]\]|, Wakayama)']) + #59
#lema(ur'[Ii]nc_ó_gnit[ao]s?_o', xpre=[ur'M\. ', ur'L\'', ur'M\. i\. ', ur'Meloidogyne ', ur'Megalaima ', ur'Leucania ', ur'della bella ', ur'Terra ', ur'Australis '], xpos=[ut' - Dossier Rufus']) + #440
#lema(ur'[Ee]nci_en_do_ne') + #53
#lema(ur'[Mm]acer_á_[ns]?_a') + #120
#    lema(ur'[Hh]ist_o_rias?_ó', xpre=[ur'Minha ', ur'Duas ', ur'Ensaios de ', ur'Matéria de ', ur'séculos de ', ur'Séculos de ', ur'Nossa ', ur' da ', ], xpos=[ur' (?:d[ao] |em |[Cc]oncisa da|colonial da|de Portugal|de um|Ilustrada do|e Geografia|curta|Geral e Pátria|e Brasil|Geral da Arte|9\. Revista do|Antiga|Marítima do|de Manaus|Dava um|por Voltaire Schilling|de Alexandre|Incompletas|desse|mais|honlapján)', ur', memórias']) + #1013
#lema(ur'[Ee]sp_e_cies?_é', xpre=[ur'seguintes ', ur'[Nn]ova ', ur'[Nn]ovas ', ur'das '], xpos=[ur' (?:Flora do|ocorrentes|vasculares)']) + #1672
#lema(ur'[Cc]on_s_cien(?:tes?|cias?)_') + #ambas existen 
#lema(ur'_á_nimos?_a', xpos=[ur' et ']) + #1
#lema(ur'_Á_nimos?_A') + #1
#lema(ur'Le_ó_n_o', pre=ur'Ponce [Dd]e ', xpos=[ur' (?:Inlet|Cut|Avenue)', ]) + #2
#lema(ur'[Cc]_ó_roba_o', xpre=[ur'of ', ur'for ', ur'Technology, ', ur'Joseph Marie ', ur'Chrysler ', ], xpos=[ur' (?:Schwaneberg|Durchmusterung|Bay|Reunion|Cinclodes)', ur'(?:\.gob\.ar|\.es)', ]) + #72
#lema(ur'[Cc]ontin_ú_es_u', xpre=[ur'Rivalry ', ur'Chase ', ur'14 ', ur'Quest ', ur'Adventure ', ur'Season ', ur'Legend '], xpos=[ur' (?:from|se|to|preparation)']) + #1
#lema(ur'[Ff]ront_ó_n(?!\])_o', xpos=[ur'Miami Jai Alai ']) + #5
#lema(ur'[Ee]st_a_dios?_á', xpos=[ur' (?:d[oa] |das |Mineirão|Vivaldo|Octávio|Durival|Cícero Pompeu|Magalhaes)', ]) + #1
#lema(ur'Est_a_dios?_á', xpos=[ur' (?:d[ao]s? |no |renovado em|Palestra Itália|de Carnide|da Luz|das Amoreiras|Cidade|Adelino|Municipal de Águeda|Estadual|Trapichão|Municipal de Chaves|Nacional|Municipal Jo[ãa]o|Dr\.|Governador|Vivaldo|D. Al?fonso|Olimpico Jo[ãa]o|Vila|de São|Brinco)', ]) + #542
#lema(ur'[Mm]_á_s el_a') + #1
#lema(ur'[Mm]_á_s a_a', xpos=[ur' (?:diferencia|fin|partir|pesar|poco|última|Alain|ella alaba|Caravana não)']) + #1
#lema(ur'__l[ao]s_el ') + lema(ur'__L[ao]s_El ') + #1
#lema(ur'[Ee]qui_v_alentes?_b') + #0
#lema(ur'[Mm]_á_s l[ao]s?_a', xpre=[ur', '], xpos=[ur' (?:2 pilotos|80 con|acciones|obra|caballería|decisiones|dirección|divisiones|falta|inauguración|carne|patria|pueblos|junta|deserción|lucha|mayoría|oscuridad|posibilidad|recibos|\[\[Real|salvación|señorita|vientos)']) + #553
#lema(ur'[Mm]alcom_í_a[ns]?_i', xpos=[ur'\]']) + #1
#lema(ur'[Hh]ind_ú__u', xpre=[ur'The '], xpos=[ur' (?:Art|Astrology|Charities|College|Electional|Imaginary|[Ll]ore|Nationalism|Troublemaker|University)']) + #1
#lema(ur'_Unión Deportiva Almería__Almería Club de F[úu]tbol', xpos=[ur'\]', ]) + #19
#lema(ur'[Ll]am_í_a[ns]_i', xpre=[ur'[Ll]as ', ur'[Yy] ', ], xpos=[ur'[|,\]]', ]) + #18
#lema(ur'[Vv]ert_í_(?:a[ns]?|)_i', xpre=[ur'Desconciertos ', ur'Sagrario ', ur'Vico ', ur'Virginia ', ur'Granados ', ]) + #6
#lema(ur'[Cc]lavar_í_a_i', xpre=[ur'Pocillopora ', ur'T\. ', ur'Tipula ', ur'and ', ], xpos=[ur' (?:acuta|erinaceus|patouillardii|zollingeri|del?)', ur'\]\]', ]) + #2
#lema(ur'[Ss]infon_í_as?_i', xpre=[ur'Esterházy ', ur'Orkiestra ', ur'Docklands ', ur'Da Casa ', ur'Adickta ', ur'Alpha ', ur'Aspen ', ur'Ballet ', ur'Britten ', ur'Esterhazy ', ur'Hallam ', ur'Jyväskylä ', ur'London ', ur'MSC ', ur'Music ', ur'Northern ', ur'Northwest ', ur'petita ', ur'Portsmouth ', ur'Scottish ', ur'Southbank ', ur'World ', ur'zur ', ], xpos=[ur' (?:d\'(?:amore|un|una)|de la matèria|bellica|Sfera|Piccola|[Cc]oncertante|De Requiem|sobre motius|fantàstica|déposée|brevis|alla|Vivace|Allegro|Antartica|Tellurica|destinului|Domestica|caratteristica|epitalamio|Spagnola|come|per|a violino|Della|Nº 5 Finale|nº 1 d\'Enric|vaga|Sacra, Fantasia, Passacaglia|(?:al|[Dd][aio]|em|in|of|à) )', ur'(?:\'|: (?:Vivace|Allegro))', ]) + #8
#lema(ur'[Ss]ab_í_as?_i', xpre=[ur' es ', ur'leyes ', ur'asamblea ', ur'opiniones ', ur'ideas ', ur' su ', ur' y ', ur'reflexiones ', ur'[Ll]a ', ur'[Ll]as ', ur'[Uu]na ', ur'[Uu]nas ', ur'Mujer ', ur'[Mm]uy ', ur'Ningú ', ur'Pintura '], xpos=[ur' +(?:leyes|hija|decisión|dosificación|disposiciones|imitación|instituciones|y |\(luchador)', ur'[\|\]]']) + #1
#lema(ur'[Ee]_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpos=[ur' the', ]) + #18
#lema(ur'[Cc]od_ó_n_o', xpre=[ur'stop ', ], xpos=[ur' (?:royenii|schenckii|repeat|usage|\(planta)', ur'[\'\]]', ]) + #15
#lema(ur'[Mm]ed_í_a[ns]? m[aá]s_i', xpre=[ur' y ', ur'puntuación ', ur'vida ']) + #1
#lema(ur'[Dd]on_d_e_') + #1
#lema(ur'[Ee]ntrever_á_[ns]?_a') + #11
#lema(ur'[Dd]os_ _mil_', xpre=[ur'Síntesis ']) + #1
#lema(ur'[Tt]res_ _mil_') + #1
#lema(ur'[Cc]uatro_ _mil_') + #1
#lema(ur'[Cc]inco_ _mil_') + #1
#lema(ur'[Ss]eis_ _mil_') + #1
#lema(ur'[Ss]iete_ _mil_') + #1
#lema(ur'[Oo]cho_ _mil_') + #1
#lema(ur'[Nn]ueve_ _mil_') + #1
#lema(ur'[Nn]a_ú_fraga_u', xpos=[ur' (?:frente|la|el|en|tras)']) + #1
#lema(ur'Castell_ó_n_o', xpre=[ur'Jason ', ur'Demacio ', ur'Damm ', ur'Demo ', ur'Demo" ', ur'Fred ', ]) + #39
#lema(ur'[Hh]_í_brida_i', xpre=[ur'carbono ', ur'[Nn]o ' ur'[Ss]e ', ur'morchella ', ur'que ', ], xpos=[ur' +(?:su |en |el |con|Estudio|frecuentemente|fácilmente|libremente|ampliamente|asimismo)', ur' en ', ur'\]', ]) + #14
#lema(ur'[Cc]omisar_í_as?_i') + #1
#lema(ur'[Uu]na_s_ [a-záéíóú]*s_') + #1
#lema(ur'[Bb]alo_m_pié_n') + Hay una marca...
#lema(ur'[Pp]ilotar_í_a[ns]?_i') + #2
#lema(ur'[Pp]ulsi_ó_n(?!\])_o') + #5
#lema(ur'[Ss]er_á_s_a', xpos=[ur' (?:Victoria|i Isern)']) + #1
#lema(ur'[Ss]_o_lo_ó', pre=ur'[Uu]n ') + #88
#lema(ur'[Pp]akistan_í__i', xpre=[ur'Ramchand ', ], xpos=[ur' (?:Music|Ordnance|Nishan-ı|Baby|Gull|women|president|pomade|and )', ]) + #67
#lema(ur'[Rr]ev_és__ez') + #2
#lema(ur'[Ee]r_ó_tic[ao]s?_o', xpre=[ur'[\'\|\[]', ur' of ' ur'Ars ', ur'Viva ', ur'Death ', ur'Classic ', ur'Hotel ', ur'= '], xpos=[ur':? (?:Awards|Lessons|\(canción|veterum)', ur'\'']) + #1
#lema(ur'[Cc]a_í_a_i', xpre=[ur' (?:de|eu) ', ur'(?:ego|Com) ', ur'[Rr]ío ', ur'noite ', ur'principado de ', ], xpos=[ur' (?:Cyrilla|Caecilia|Cecilia|Cirila|Koopman|Cornelia|Van|Coley|de Bragança|Maasakker|e São|\(Mozambique)', ur'(?:\]\]|@)', ]) + #32
#    lema(ur'_Á_sper[ao]s?_A', xpre=[ur' de ', ur'Per ', ur'Cilicia ']) + #1
#    lema(ur'_á_sper[ao]s?_a', xpre=[ur'[CFHIPS]\. ', ur'per ', ur'tollis ', ur'Aeschynomene ', ur'Achyranthes ', ur'Rhinelepis ', ur'Stelis ', ur'Ficus ', ur'[Ss]milax ', ur'Chara ', ur'Mentzelia ', ur'Hydrangea ', ur'Hylomantis ', ur'Pipa ', ur'Crepis ', ur'Inula ', ur'Leucandra ', ur'Smilax ']) + #1
#lema(ur'[Aa]_u_n (?:así)_ú') + #1
#lema(ur'[Aa]l__rededor_ ') + #al rededor existe
#lema(ur'[Aa]ut_é_ntic[ao]s?_e', xpre=[ur'dell\'']) + autentica es válido
#lema(ur'[Ff]_ó_rmic[ao]s?_o', xpre=[ur'Apochinomma', ur'Rino ', ur'Mauro '], xpos=[ur' rufa']) + #1
#lema(ur'[Hh]ac_í_a[ns]? (?:acompañar|actuar|adorar|albergar|alcanzar|aminorar|andar|anunciar|aparecer|aparentar|apodar|aprender|asegurar|atravesar|aumentar|ayudar|bailar|bajar|bañar|caer|cambiar|cantar|circular|coincidir|comenzar|competir|comprar|conseguir|considerar|constar|construir|consultar|consumir|convenir|correr|cortar|creer|cumplir|dar|degollar|delirar|denunciar|depender|desaparecer|descubrir|desprender|disputar|distinguir|dudar|elevar|enfadar|enojar|entender|entrar|entregar|entretener|escuchar|escurrir|esperar|estallar|evitar|expandir|experimentar|extrañar|figurar|firmar|florecer|fotografiar|funcionar|galopar|girar|hacer|hervir|honor|huir|indicar|jugar|llamar|llegar|lucir|maniobrar|marcar|mejorar|mostrar|nacer|notar|obedecer|olvidar|oscilar|parecer|participar|pasar|peligrar|pensar|perder|pisar|plantear|plasmar|practicar|preguntar|presagiar|prever|quemar|rabiar|recordar|recorrer|reforzar|reir|remolcar|repetir|retroceder|reír|rivalizar|salir|saltar|sentir|satisfacer|ser|sobresalir|solucionar|sonar|sondear|soplar|soñar|subir|sufrir|suponer|tambalear|temblar|temer|tener|trabajar|traer|valer|venir|ver|vibrar|volver|vomitar)_i') + #65
#lema(ur'[Hh]ac_í_a[ns]? (?:acabar|abrazar|arribar|asistir|atacar|causar|confiar|conocer|conseguir|consolidar|crear|dar|definir|derrotar|desarrollar|disminuir|dominar|escoger|escribir|establecer|experimentar|facilitar|fusionar|ganar|hacer|interpretar|llegar|lograr|mejorar|mirar|obtener|ofrecer|percibir|permitir|profundizar|proveer|realizar|realzar|requerir|saber|seguir|ser|situar|subrayar|sustituir|proteger|tener|tomar|usar|utilizar|vivir)_i') + #1
#lema(ur'[Hh]edi_ó__o') + #6
#lema(ur'[Mm]_á_s (?:de|finalmente|habitualmente|cariñozamente)_a') + #1
#lema(ur'[Pp]ari_ó__o', xpre=[ur'Mármol ', ], xpos=[ur'\]', ]) + #1
#lema(ur'[Ss]ent_é__e', xpre=[ur'Coração que '], xpos=[ur' x to']) + #1
#lema(ur'_é_l (?:[Ll]os?)_e') + No descomentar
#lema(ur'_é_l [Ll]es?_e') + lema(ur'_É_l [Ll]es?_E') + lema(ur'[Ee]_n_ (?:[Ll]as?)_l') + lema(ur'[Ee]n___ en') + #Descomentar para procesar manualmente la lista _el_l
#lema(ur'[Aa]maz_ó_nica_o', xpre=[ur'\'', ur'[AaBbCcDdEeFfGgLlMmPpRrSsVv]\. ', ur' x ', ur'Acanthops ', ur'Acontista ', ur'Acta ', ur'Aechmea ', ur'Aegiphila ', ur'Algernonia ', ur'Alstroemeria ', ur'Amazona ', ur'Ami ', ur'Amorimia ', ur'Amphisbaena ', ur'Amyris ', ur'Anneslea ', ur'Annona ', ur'Aristolochia ', ur'Arrabidaea ', ur'Bernardia ', ur'Belone ', ur'Biomphalaria ', ur'Blainvillea ', ur'Bletia ', ur'Bolitoglossa ', ur'Bomarea ', ur'Bombacopsis ', ur'Brassavola ', ur'Brassia ', ur'Brocchinia ', ur'Brunfelsia ', ur'Carpotroche ', ur'Cassia ', ur'Cayaponia ', ur'Cyathea ', ur'Chamaedorea ', ur'Chirothecia ', ur'Chondrorhyncha ', ur'Cissampelos ', ur'Cinchonopsis ', ur'Cinchona ', ur'Clowesia ', ur'Clusia ', ur'Cochleanthes ', ur'Couepia ', ur'Cotorrita ', ur'Coryphaeschna ', ur'Crudia ', ur'Cumbia ', ur'Cyathea ', ur'Cynophalla ', ur'Dalbergia ', ur'Dalechampia ', ur'Dekeyseria ', ur'Dicella ', ur'Dicymbe ', ur'Dorstenia ', ur'Eleocharis ', ur'Encyclia ', ur'Epinecrophylla ', ur'Erythrodiplax ', ur'Eschweilera ', ur'Esenbeckia ', ur'Eucharis ', ur'Euglossa ', ur'Euryale ', ur'Exostyles ', ur'Exochogyne ', ur'Fevillea ', ur'Ficus ', ur'Forsteronia ', ur'Fylgia ', ur'Galapagia ', ur'Gaylussacia ', ur'Hetaerina ', ur'Hormetica ', ur'Idiatalphe ', ur'Idiophthalma ', ur'Inga ', ur'Ilisha ', ur'Janusia ', ur'Justicia ', ur'lechera ', ur'Lecointea ', ur'Leiothrix ', ur'Ligeophila ', ur'Loxosceles ', ur'Lucihormetica ', ur'Macfadyena ', ur'Macradenia ', ur'Magnolia ', ur'Malouetia ', ur'Mandevilla ', ur'Manilkara ', ur'Maprounea ', ur'Maranta ', ur'Mascagnia ', ur'Mayna ', ur'Mecistogaster ', ur'Metaleptobasis ', ur'Metilia ', ur'Micropoecilia ', ur'Mirla ', ur'Mormodes ', ur'Nunnezharia ', ur'Nuzonia ', ur'Ocotea ', ur'Octomeria ', ur'Orleanesia ', ur'Ormosia ', ur'Odontadenia ', ur'Pachira ', ur'parda ', ur'Parinari ', ur'Passiflora ', ur'Pellona ', ur'Pentagonia ', ur'Peplonia ', ur'Petrea ', ur'Phragmotheca ', ur'Piptadenia ', ur'Pistia ', ur'Poecilanthe ', ur'Poecilia ', ur'Pomacea ', ur'Poupartia ', ur'Pouteria ', ur'Psammisia ', ur'Psectrogaster ', ur'Pseudorhipsalis ', ur'Pterygota ', ur'Quiina ', ur'Ranitomeya ', ur'Raputia ', ur'Ravenia ', ur'Remijia ', ur'Rhaphiodon ', ur'Rollinia ', ur'Romanita ', ur'Ruyschia ', ur'Rytidostylis ', ur'Sacoglottis ', ur'Sciadotenia ', ur'Securidaca ', ur'seniculus ', ur'Selaginella ', ur'Sigmatostalix ', ur'Siolmatra ', ur'Siparuna ', ur'Sigmatomera ', ur'Sigmatostalix ', ur'Souroubea ', ur'Sparianthis ', ur'Sphaeradenia ', ur'Speocera ', ur'Stagmomantis ', ur'Steindachnerina ', ur'Stilaginella ', ur'Styringomyia ', ur'Stylogyne ', ur'Swartzia ', ur'Tapura ', ur'Terminalia ', ur'Thevetia ', ur'Tipuana ', ur'Tipula ', ur'Touroulia ', ur'Trechalea ', ur'Triolena ', ur'Turbina ', ur'Urania ', ur'Victoria ', ur'Vismia ', ur'Vitis ', ur'Yingaresca ', ur'Zapoteca ', ur'Zomicarpella ', ur'gêral ', ur'haematonota ', ur'haematonota\) ', ur'região ', ur'terra ', ur'var\. ', ]) + #1
#lema(ur'[Ee]sta_b_a[ns]?_v', xpre=[ur'ainda ', ur'primero día ', ur'dicho don Fernando ', ur'la qual ', ur'vila ', ur'não ', ur'Piçarro ',]) + #1
#lema(ur'[Rr]_í_gida_i', xpre=[ur'[AaCcEeJjPp]\: ', ur'Acampe ', ur'Acampe ', ur'Adenogramma ', ur'Aerides ', ur'Agave ', ur'Agrostis ', ur'Alibertia ', ur'Allocasuarina ', ur'Aloe ', ur'Anisantha ', ur'Annona ', ur'Aphelandra ', ur'Arracacia ', ur'Asperula ', ur'Asplundia ', ur'Atrina ', ur'Bartsia ', ur'Betonica ', ur'Caladenia ', ur'Calicotome ', ur'Callostylis ', ur'Calopsis ', ur'Carlina ', ur'Cayaponia ', ur'Cheilanthes ', ur'Chionochloa ', ur'Cleistochloa ', ur'Coccothrinax ', ur'Copernicia ', ur'Coprosma ', ur'Couma ', ur'Cryptandra ', ur'Cryptocarya ', ur'Cryptocarya ', ur'Dactylis ', ur'Desmazeria ', ur'Dichelachne ', ur'Dimorphochloa ', ur'Dioclea ', ur'Dockrillia ', ur'Dryopteris ', ur'Duguetia ', ur'Dysderina ', ur'Ehretia ', ur'Elegia ', ur'Engelhardtia ', ur'Eremogone ', ur'Eriaxis ', ur'Eschscholzia ', ur'Escobaria ', ur'Euphorbia ', ur'Festuca ', ur'Freylinia ', ur'Fuerstia ', ur'Furcraea ', ur'Galenia ', ur'Galeola ', ur'Gaudinia ', ur'Gelasine ', ur'Genea ', ur'Grisebachia ', ur'Guillenia ', ur'Helmiopsis ', ur'Hemigenia ', ur'Hilaria ', ur'Iris ', ur'Jumellea ', ur'Juniperus ', ur'Kaloula ', ur'Licania ', ur'Lomandra ', ur'Mascagnia ', ur'Medicago ', ur'Melaleuca ', ur'Neurolepis ', ur'Nierembergia ', ur'Notholaena ', ur'Oryzopsis ', ur'Ozyptila ', ur'Pallidula, ', ur'Parapiptadenia ', ur'Parasponia ', ur'Parawixia ', ur'Parodia ', ur'Pavetta ', ur'Persoonia ', ur'Phlomis ', ur'Piloblephis ', ur'Pinanga ', ur'Pinus ', ur'Piptadenia ', ur'Piptadenia ', ur'Platyzamia ', ur'Pleuraphis ', ur'Plutarchia ', ur'Polevansia ', ur'Psammotropha ', ur'Pyrrocoma ', ur'Quercus ', ur'Retinispora ', ur'Rodriguezia ', ur'Rupertia ', ur'Salix ', ur'Satureja ', ur'Scolodrys ', ur'Scorzonera ', ur'Senna ', ur'Sesleria ', ur'Setaria ', ur'Smilax ', ur'Solidago ', ur'Sycomorus ', ur'Tabebuia ', ur'Tachigali ', ur'Taralea ', ur'Tephrosia ', ur'Tetramicra ', ur'Trigonachras ', ur'Tunica ', ur'Ulva ', ur'Unonopsis ', ur'Velezia ', ur'Ventricolaria ', ur'Verbena ', ur'Vulpia ', ur'Yuca ', ur'Zamia ', ur'subsp\. ', ur'var ', ur'var\. ', ], xpos=[ur'[\]\']']) + #1
#lema(ur'[Cc]avern_í_colas?_i', xpre=[ur'Aegla ', ur'Aspiduchus ', ur'Damarchus ', ur'Eleutherodactylus ', ur'Episinus ', ur'Euagrus ', ur'Ficus ', ur'Gaucelmus ', ur'Heteropoda ', ur'Hexathele ', ur'Hypericum ', ur'Lathrothele ', ur'Lepthyphantes ', ur'Macrobrachium ', ur'Maloides ', ur'Metopobactrus ', ur'Micrargus ', ur'Oonopoides ', ur'Orsinome ', ur'Porrhomma ', ur'Procambridgea ', ur'Segestria ', ur'Spelungula ', ur'Talanites ', ur'Tetragnatha ', ur'Themacrys ', ur'Tupua ', ur'Turinyphia ', ur'Walckenaeria ', ], xpos=[ur' (?:Records|\+|Recording)', ]) + #120
#lema(ur'Sab_í_an_i', xpre=[ur' a ', ur'B8 ', ur'marcas ', ur'marca ', ur'campeón ', ur'Platillos: ', ur'platillos '], xpos=[ur' (?:Cymbals|\(wrestler|\(luchador|fabrica|y (?:Orion|Promark)|lo incorporó)', ur'[\|\]]']) + #1
# lema(ur'[Bb]arri_ó__o') + #barrio
#lema(ur'[Aa]rquitect_ural_mente_onica') + #5
#lema(ur'[Aa]si_ó__o', xpre=[ur'Phrynosoma '], xpos=[ur' (?:otus|flammeus|stygius)']) + #282
#lema(ur'[Pp]rometi_ó__o') + #elemento
#lema(ur'[Cc]on_ _que_') + "conque existe
#lema(ur'B_á_rbara_a', pre=ur'Santa ', xpos=[ur': ABC-Clio']) + #1
#lema(ur'[Ee]nviar_á__a', xpre=[ur'que ', ur'se le ']) + #1
#lema(ur'[Aa]ccesi_ó_n_o', xpos=[ur'\]', ]) + #11
#lema(ur'[Ll]a_s_ demás_') + #84
#lema(ur'[Ss]_iguie_ntes?_egui', xpre=[ur' (?:as|às) ', ur' e ', ur'Comente o ', ur'O Dia ', ], xpos=[ur' denominações', ]) + #60
#lema(ur'[Ss]ecretar_í_as?_i', xpos=[ur' de Estado da']) + #8
#[(ur' ([a-záéíóúñ][a-záéíóúñ][a-záéíóúñ][a-záéíóúñ]+) \1 ', ur' \1 ')] + #1
#lema(ur'[Aa]plastar_á_[ns]?_a') + #40
#lema(ur'[Dd]eformar_á_[ns]?_a') + #14
#lema(ur'[Dd]isputar_á_[ns]?_a', xpre=[ur' que (?:no|se|le|lo) ', ur'que ', ur'que únicamente ', ur'el de Kentucky ', ur'que Audax ', ur'que el equipo ', ur'el torneo se ', ur'que el equipo [ln]o ', ur'que antes del inicio del Campeonato Nacional se ', ur'que dos concursantes expulsados se ', ur'que el jugador ', ur'que este mismo se ', ur'que Barcelona ', ur'que la final se ', ur'que el club ', ur'que el partido se ', ur'que Cerro Largo FC ', ur'que sólo ', ur'que cada piloto ', ur'que River ', ur'que si se ', ur'que en Estoril se ', ur'que este clásico se ', ur' no se ', ur'que Ignacio ', ur'que el joven futbolista ', ur'que apenas ', ur'que el Campeonato del Mundo se ', ur'que su equipo ', ur'que Pepita ', ur'que el piloto ', ur'que Nueva Zelanda ', ur'que 2 jugadoras rusas ', ur'que dicho equipo ', ur'que otra de las familias nobles ', ur'que la Sub-20 ', ur'que la copa se ', ur'que la selección ', ur'que el set se ', ur'que el cuadro \'Asegurador\' ', ur'que Sunderland ', ur'que Santos no ', ur'que ganara el torneo ', ur'que la carrera se ', ur'que nadie los ', ur'que España ', ur'que el monje ', ur'que cada equipo ', ur'\]\] ', ur'aunque no ', ur'quien ']) + #497
#lema(ur'[Mm]__uy_uy m') + #1
#lema(ur'[Gg]aller_í_as?_i') + #8
#lema(ur'[Hh]u_í_(?:a[ns]?|)_i', xpre=[ur'Datong ', ur'Gyang ', ur'Autónoma ', ur'Etnia ', ur'Jang ', ur'John ', ur'Liu ', ur'aujourd[\'’]', ], xpos=[ur' (?:惠|Pan|mei|Lan|Wen|Wang|Di|Min|Yi|emperador|en\b|de Zhou|\|\|)', ur'(?:\]|, mongoles)', ]) + #1177
#lema(ur'[Mm]or_í_(?:a[ns]?|)_i', xpre=[ur'Bárbara ', ur'Camilo ', ur'Cafe ', ur'Corbera ', ur'Damian ', ur'Flores de ', ur'Gecko ', ur'Kanna ', ur'Kogoro ', ur'Memento ', ur'Menosu no ', ur'Takemoto ', ur'Yoshirō ', ur'artista ', ur'iku ', ], xpos=[ur' (?:es|Takao|no Satori|Ōgai|Alvarado|Parque|Bellavista|no (?:naka|majo|Tonto))\b', ur'(?:#|, en la Moraña)', ]) + #4262
#lema(ur'[Pp]_í_a_i', xpre=[ur'G\. ', ur'Sarah ', ur'Anna ', ur'Distrito de ', ur'Aeródromo de ', ur'Juani De ', ur'Mangora ', ur'Maria ', ur'Noticias ', ur'Porta ', ], xpos=[ur' (?:Hansen|Fai|Records|Toscano|Miranda|fidelis|del Carpine|Tavernelli|Almoina|Carrot)', ur'[ʔ\]]', ]) + #1605
#lema(ur'[Rr]e_í_do_i', xpre=[ur'Zettai '], xpos=[ur' Reiki']) + #16
#lema(ur'[Tt]r_í_a[ns]?_i', xpre=[ur'regna ', ur'Martí ', ur'Casa ', ur'Jordi ', ur'Xavier '], xpos=[ur' (?:nomina|prima|naturae|Tres)']) + #128
#lema(ur'[Cc]_ó_dices?_o', xpre=[ur'\bnel ', ur'Matritensis '], xpos=[ur' (?:Latini|di)\b']) + #291
#lema(ur'[Tt]ravest_í__i') + #Existe travesti también
#lema(ur'[Mm]_ó_dems?_o') + #210 #Módem o Modem
#lema(ur'[Jj]od_í__i', xpos=[ur' Picoult']) + #1
#lema(ur'[Ss]_ú_per_u', xpos=[ur' (?:Cup|Smash|Express|Sherman|ATR|Cub|Dome|Trouper|[Hh]ero|Cabriolet|deformed|Junior|specialists?|Puma|ripam?|Constellation|Adventure|fruit|Frelon|Skyhawk|[Pp]erformance|League|Nintendo|NES|Prestige|hanc|Clasic|Bowl|Leeds|Rugby|Colorado|Yang|Driver|Jounan|Eurobeat|League)\b']) + #38897
#lema(ur'[Ss]on_ó__o', xpre=[ur'chi ', ur'Mi ', ur'\bDe '], xpos=[ur' (?:andati|io|lupi|shinjō|giunta|Radio|pietre|Wake|il|yo|otoko|ki|Rekishi|Chi|Film|miniere)\b']) + #1897
#lema(ur'[Cc]ed_í__i') + #1
#lema(ur'[l]e_í__i', xpre=[ur'tres ', ur'[0-9] ', ur'caro ', ur'cuore ', ur'Zheng ', ur'Lei '], xpos=[ur' (?:quan|Jia|m\'ama|Wulong|Fang)', ur'" antes']) + #338
#lema(ur'[Uu]n_í__i', xpos=[ur'[\'.]']) + #1
#lema(ur'[Cc]orr_í__i', xpre=[ur'Adrienne '], xpos=[ur' English']) + #1
#lema(ur'[Ee]leg_í__i') + #1
#lema(ur'[Ee]scog_í__i') + #1
#lema(ur'[Ee]scrib_í__i') + #1
#lema(ur'[Hh]ar_é__e', xpre=[ur'O[’\']'], xpos=[ur' (?:krishnas?|2007|Kawasaki)']) + #1458
#lema(ur'[Cc]a_í__i', xpre=[ur'\bde ', ur'lexema \'\'', ], xpos=[ur' (?:Li|Shen)\b', ur', Imán']) + #900
#lema(ur'[Rr]ub_í__i') + #1
#lema(ur'[Cc]om_í__i', xpre=[ur'Francesco ']) + #1
#lema(ur'[Bb]arr_í__i', xpre=[ur'"', ur'Pedro ', ], xpos=[ur' (?:en bangor|Griffiths)', ]) + #295
#lema(ur'[Bb]at_í__i', xpre=[ur'\'\'', ], xpos=[ur' = un', ]) + #5
#lema(ur'[Mm]an_í__i', xpre=[ur'\ba ', ur'\ble ', ur'Mounfield\|', ur'Carles ', ur'Península ', ur'Península de ', ur'de Mani\|', ur'profeta\)\|', ur'profeta \[\[', ur'fundada por '], xpos=[ur' (?:fue influenciado|se|Ratnam|Congo|Paudel|Kaul|padme|\]\], (?:líder|fundador)|\(profeta)\b']) + #1
#lema(ur'[Pp]rend_í__i') + #1
#lema(ur'[Pp]resent_í__i') + #1
#lema(ur'[Pp]roced_í__i') + #1
#lema(ur'[Pp]art_í__i', xpre=[ur'AK ' ur'delle ', ur'due ', ur'\bd[ei] '], xpos=[ur' (?:de|du|des|pour|noir|Québécois|patriote|Demokrat|Lepep|Tindakan|Congolais|Démocrate|Démocratique|Radical|chrétien|libéral|communiste|socialiste|Demokrat|radical)\b', ur'\'\' tomada']) + #1154
#lema(ur'[Dd]eb_í__i') + #1
#lema(ur'[Dd]orm_í__i', xpre=[ur'non '], xpos=[ur', mio']) + #36
#lema(ur'[Nn]utr_í__i') + #1
#lema(ur'[Ss]egu_í__i', xpre=[ur'Doris ', ur'Ferrandis ', ur'Mendoza ', ur'ingeniero ', ], xpos=[ur' (?:el Hamra|1005|Monleon)', ]) + #176
#lema(ur'[Ii]nclu_í__i') + #1
#lema(ur'[Ii]nfer_í__i') + #1
#lema(ur'[Ii]nvert_í__i') + #1
#lema(ur'[Tt]it_í__i', xpre=[ur'Adel El '], xpos=[ur' (?:premier|Gantung)']) + #1
#lema(ur'[Nn]o_minó__nimo') + #1
#lema(ur'[Cc]onvert_í__i', xpre=[ur'Ángel ', ur'Hern[aá]n ']) + #1
#lema(ur'[Rr]_é_cord_e', xpre=[ur'(?:HP|TV|on|[Tt]o) ', ur'(?:[Tt]he|and|mix|for|FBI|Red) ', ur'[Bb]oot ', ur'[&X] ', ur'Gramophone ', ur'New ', ur'Montreux ', ur'Dosis ', ur'Midas ', ur'Black ', ur'Cinematic ', ur'Temps ', ur'Express ', ur'Crescendo ', ur'Cutting ', ur'Aces ', ur'Effects ', ur'Zoological ', ur'Victor ', ur'Anatomical ', ur'Gold ', ur'River ', ur'Inch ', ur'Fania ', ur'Congressional ', ur'kickboxing ', ur'Psychological ', ur'Label ', ur'Cumulative ', ur'eXchange ', ur'Fossil ', ur'Whale ', ur'Personal ', ur'Permanent ', ur'vinyl ', ur'fossil ', ur'Daily ', ur'gold ', ur'Alroy\'s ', ur'álbum\)\|', ur'de BD\)\|', ur'Ed\. ', ur'Resource ', ur'Mineralogical ', ur'Architectural ', ur'turons del ', ur'Mercury ', ur'Academy ', ur'Golden ', ur'Skycap ', ur'São Francisco ', ur'Illustrated ', ur'Retailer ', ur'roll ', ur'Rede ', ur'Record\|'], xpos=[ur' (?:i|my|[Oo]f|Club|Master|conversations|holder|Companies|Studios|Producer|o un|chase|Route|Records|Retailer|Online|News|Database|Collection|Office|Transcription|type|Mirror|of|and|[Ll]abel|Collector|One|World|Display|Store|Group|fair|Management|Report|Plant|for|highs|[Hh]igh|Mart|low|Guide|Release|Review|Corporation|Plant|Pool|Jump|[1-4]|de l|\((?:Permite|álbum|journal)|del Saló|Company|Taishou)\b', ur'(?:\'\' en|, Dargaud)']) + #12685
#lema(ur'[Cc]_á_ncer_a', xpre=[ur'\b(?:of|on|Re|CA|in) ', ur'banda\)\|', ur'Blood ', ur'género\)\|', ur'constelación\)\|', ur'canción\)\|', ur'urine ', ur'prevent ', ur'[Tt]o ', ur'Up 2 ', ur'Testicular ', ur'Healing ', ur'Insane ', ur'puesto ', ur'Mask de ', ur'Oro de ', ur'Toll de ', ur'Cloth de ', ur'Sage de ', ur'[Ss]anto de ', ur'también \'\'\'\'\'', ur'Manchester v ', ur'Pancreatic ', ur'Cervical ', ur'[Pp]rostate.', ur'médica ', ur'Teenage ', ur'National ', ur'Καρκίνος; \'\'', ur'with ', ur'Int J ', ur'against ', ur'[Bb]reast ', ur'Face ', ur'stomach[+]', ur'Fields: ', ur'Clinical ',  ur'Chick ', ur'\b(?:for|and|[Tt]he) ', ur'[Ll]ung ', ur'animal\)\|'], xpos=[ur' (?:[0-9\|]+|and|or|cells|Lett|Sci|Pain|stagnalis|with|Commons|Inst|All|Matinero|Vaccine|Friends|productus|Trust|Research|free|dels|incidence|Institute|Man|setosus|Letters|Biotherapy|chemopreventive|Genome|Council|mortality|Center|Research|pagurus|magister|risk|Cell|Care|Centre|Society|Survival|mortality|prevention|\((?:banda|género|canción|porteri|constelación|cells))\b', ur'(?:\.gov|\]\](?:ígen[ao]s?|os[ao]s?)|[+]prostata|\'\' 2003)']) + #3183
#lema(ur'[Ss]al_í__i', xpre=[ur'<\*'], xpos=[ur' Berisha']) + #1
#lema(ur'[Cc]h_á_rter_a', xpre=[ur'carta \(\'\'', ur'Martinair ', ur'Frédéric ', ur'Transport ', ur'Perspectives ', ur'Bay ', ur'People\'s ', ur'Royal ', ur'Media ', ur'Palisades ', ur'Mason ', ur'Air '], xpos=[ur' (?:for|Union|High|Association|schools|Club|Arms|of|One|Hill|Edition|School|Township|Airlines|Communications|Member|League)\b', ur', constitution']) + #1805
#lema(ur'_ó_mnibus_o', xpre=[ur'\b(?:ab|[Ee]x|ut|an|[Ii]n) ', ur'mendis ', ur'vestris ', ur'cum ', ur'alii ', ur'vestris ' ur'lucet ', ur'luceat ', ur'generibus ', ur'cognitus ', ur'Justitia ', ur'mendis ', ur'pro ', ur'[Hh]ipoteca '], xpos=[ur' (?:dórmio|castri|volume|unus|indictam|proculcatisque|ingenti|qui|dictionibus|diebus|corporis|iudicibus|omnia|telephone|requiem|edition|promittat|emendatior|sanctis|scientiis|Gothorum|enucleatis|equis|in|christiani|cum|se manipulis|eorumque|perficiendis)\b', ur'(?:"|” pass|\'\'|, 1999)']) + lema(ur'_Ó_mnibus_O', xpre=[ur'Music '], xpos=[ur' (?:"Gimmick|Heckmotor|Conjuncti|Press|Ubique|Network|Company|compertum)', ur'(?:\'\'|, 2 libros)']) + #970
#lema(ur'[Tt]_á_ndems?_a', xpre=[ur'via ', ur'Peyret ', ur'Quousque ', ur'Ordenadores ', ur'(?:L[ei]|in) ', ur'Radio ', ur'B\.A\.S\.E\. y ', ur'Felix '], xpos=[ur' (?:Computers|Communications|Reaction|venit|ProductionsLinac|Films|Duct|Fund|Architects|Curtius|Calling|abutere|vita|Thrust|Campany|Verlag|[Rr]epeats?|chromosome|Repetition|ad|\(film)\b', ur'\]\] \[\[Architects']) + #439
#lema(ur'[Vv]ol_ó__o', xpre=[ur'\be ', ur'(?:de|al) ', ur'del ', ur'Centro ', ur'Via ', ur'Volo\|', ur'Illinois\)\|', ur'Il breve ', ur'Primo ', ur'Angelo ', ur'[Ll]auren ', ur'como \'\'\'', ur'\ba ', ur'che ', ur'ultimo ', ur'Fabio ', ur'veloce ', ur'Campo ', ur'Sicurezza del ', ur'\b[Ii]l ', ur'cui ', ], xpos=[ur' (?:AZ|Cue|nisi|dal|videre|tra|su|do|di|in|facite|cieco|AZ504|\((?:2007|Illinois))\b', ur'(?:, James|\]\])', ]) + #189
#lema(ur'Mart_í__i', xpos=[ur' (?:ten|Tileno|Noxon|Venturi)']) + #1
#lema(ur'[Pp]achul_í__i') + Pachuli existe
#lema(ur'[Pp]erd_í__i', xpre=[ur'A\. ', ur'Australoheros ', ur'Campamento ', ur'Campo ', ur'Eleanor y ', ], xpos=[ur' (?:la mi rueca|aquest|[Vv]ocê)', ur'\'\'', ]) + #1
#[(ur'\[\[Bah[ií]a\]\]', ur'[[Bahía (Brasil)|Bahía]]')] + #1
#lema(ur'[Mm]an_í_as?_i', xpre=[ur'411', ur'441', ur'Adam ', ur'Amoron\'i ', ur'Dance ', ur'Fighting ', ur'Sonic ', ur'Egg ', ur'Film ', ur'cómic ', ur'Motocross ', ur'Maadanei ', ur'Freestyle ', ur'Guitar ', ur'gee ', ur'Ramones ', ur'Gun ', ur'Mallet ', ur'Décalé ', ur'Cake ', ur'Pipe ', ur'Marble ', ur'Man ', ur'Wedding ', ur'Christmas ', ur'Metal ', ur'Hit ', ur'Minigame ', ur'Motorcycle ', ur'Motown ', ur'Persecution ', ur'Punch ', ur'Ripper ', ur'Talulah ', ur'Vostell\. ', ur'Zykus ', ], xpos=[ur' (?:Simpson|Velichia|Phase|Entertainment|en Marieta|Lispector|Mega|entre otros|y Tematahoa|no gyalu|de (?:Você|kakushidori|explicação)|\((?:álbum|Marieta))', ur'(?:[!]|\.com|\]|\'\'\', también|\'\' \(Barcelona|\., ThisDay|, Shalom|: The)', ]) + #469
#lema(ur'[Tt]em_í__i', xpre=[ur'Oscar ']) + #1
#lema(ur'_É_pic[ao]s?_E', xpre=[ur'Sluijer, ', ur'Delahaye, ', ur'Móvil de ', ur'[Áá]lbum de ', ur'sinfónico, ', ur'\b(?:to|de|[Ee]n|ed) ', ur'con ', ur'tocada por ', ur'Aveo, ', ur'Ars ', ur'Chevrolet Epica\|', ur'Chevrolet ', ur'Ensiferum\]\], \[\[', ur'banda ', ur'Colón\|', ur'Holden ', ur'Primo & ', ur'banda\)\|', ur'della ', ur'álbum\)\|', ], xpos=[ur' (?:Set|& Jägermeister|"Dies|se (?:debe|embarca)|agotó|en (?:reemplazo|The|el)|evolucionó|Darangen|\((?:banda|álbum))', ur'\'+ es']) + lema(ur'_é_pic[ao]s?_e', xpre=[ur'Chevrolet ', ur'Banksia ', ur'Poemata '], xpos=[ur' spagnola', ur'(?:\.nl|\'+:)', ]) + #105
#lema(ur'[Pp]_í_a[ns]_i', xpre=[ur'\bG\. ', ur'\bda ', ur'\b(?:Jiu|fue) ', ur'Alfredo '], xpos=[ur' (?:di|del|due|dell[ae]|tang|Spain|Rosà)\b']) + #454
#lema(ur'[Rr]alent_í__i') + #1
#lema(ur'[Rr]efer_í__i') +  
#lema(ur'[Rr]epet_í__i') + #1
#lema(ur'[Rr]esist_í__i') + #1
#lema(ur'[Ss]ent_í__i') + #1
#lema(ur'cr_í_tico_i', pre=ur'(?:especialmente|golpe|canal|[Tt]eatro|[Pp]unto|periodista|estado|ataque|daño|nivel|físico|periodo|pensamiento|[Ff]ue|[Ee]s|[Ee]ra|[ss]erá|[Ee]l|este|un|del|su|se|prestigioso|famoso|recordado|y) ') + lema(ur'[Cc]r_í_tico e_i', xpre=[ur'apparato '], xpos=[ur' (?:note|cronologico|spirito)']) + lema(ur'[Cc]r_í_tico sobre_i', xpos=[ur' o']) + lema(ur'[Cc]r_í_tico (?:del?|en|influyente|literario|estadounidense|social|literario|teatral|en|con|es|gastronómico|taurino|para|respecto|cinematográfico|musical|y|dijo|ya|haya|ha)_i') + lema(ur'[Cc]r_í_tico al?_i', xpos=' cura di') + lema(ur'[Cc]ritic_ó_ (?:las?|los?|algun[ao]s|el|duramente|fuertemente|ásperamente|públicamente|ácidamente|frecuentemente|sus?|muy|por|que|sino|también)_o') + lema(ur'[Cc]r_í_tic(?:os|amente)_i', xpre=[ur'Basil ', ur'Greg ']) + #1
# lema(ur'[Cc]r_í_tica de_i', xpos=[ur' hecho']) + lema(ur'cr_í_ticas_i', pre=ur'(?:[Ll]as|[Uu]nas) ') + #retro(ur'(?:[Cc]uando|Mao|Artnexus|[Qq]ue|Notte|donde|lo) _[Cc]r_í_tic[ao](?! (?:Casuarinarum|e|storiografica|della|la|abiertamente|Musicale|nunca|al|a|los|individualista anarchica))_i') + #1
#lema(ur'[Aa]sum_í__i', xpre=[ur'\ba ', ur'\b(?:como|Kana) ', ur'\bcon ', ur'\bde ', ur'agrada ', ], xpos=[ur' (?:no|se|y|tiene|asiste|menciona|Miwa|Kana|Nakata)\b', ]) + #132
#lema(ur'[Mm]_óv_il(?:es|)_[oó]b', xpre=[ur'Adria ', ur'Exxon ', ur'ExxonMobil\|', ur'Rally ']) + #1
#lema(ur'[Ss]ub_í__i', xpos=[ur' l\b', ur'ːz', ]) + #39
#lema(ur'[Bb]_ú_nker(?:es|)_u', xpre=[ur'(?:[Tt]he|[Dd]er) ', ur'Shield ', ur'Miller ', ur'Edith ', ur'Michael ', ur'Ellsworth ', ur'Tristan ', ur'Archie ', ur'Alice ', ur'Dennis ', ur'Jon ', ur'Titan ', ur'Ralph ', ur'Nelson ', ur'\bdu ', ur'Jazz ', ur'Dan ', ur'Larry ', ur'Data ', ur'alemán\]\] \'\'', ur'Clive ', ur'Edward ', ur'Frank ', ur'Eddie ', ur'Eng '], xpos=[ur' (?:fue asesinado|Hill|Jenkins|Palace|Roy|Terrillo|buster|Studio|McLaughlin|Bean|Ramo|Gamer|llama|musée|Bean|\(1975)\b', ur'(?:, Oscar|\'s|” Roy)']) + #820 bunker también existe.
#lema(ur'[Vv]est_í__i', xpre=[ur'\bti '], xpos=[ur' la giubba']) + #1
#lema(ur'[M]_á_s y\b_a', xpre=[ur'colección ', ur'Rafael ', ur'Adolf ', ur'Francisco ', ur'Artur ', ur'Glorieta de ', ur'Jeanne ', ur'Conxita ', ur'Manuel ', ], xpos=[ur' (?:al frente|el resto|Sanz|Duran|Noguera|Guindal|Altaya|Zaldúa|Fondevila|Durán|Juan|Ginestà|Baliart|Gil|Jos[eé]|Salvador|Mateu|Rubí|Galmés|Ros|Mas/Auditori|Arcarons|Calderó|remato|Ventura|Mauro)\b', ]) + #954
#lema(ur'[Tt]ransfer_í__i', xpre=[ur'Nakit ']) + #1
# lema(ur'[Rr]eligi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpre=[ur'sur la ', ur'et '], xpos=[ur' (?:zoroastrienne|scandinave|des|romaine|égyptienne|de la science)']) + #1
# lema(ur'Le_ó_n_o', pre=ur'(?:[Ee]n) ', xpre=[ur'Condado '], xpos=[ur' Jones']) + #1
# lema(ur'[Cc]ant_ó_n_o', pre=ur'[Dd]e ', xpre=[ur'[Mm]unicipio ', ur'equipo ', ur'nativos '], xpos=[ur'(?:\]\]|, en|, estado de)']) + #4
# lema(ur'Falc_ó_n_o', pre=ur'(?:[Dd]e|[Ee]n|para|desde) ', xpre=[ur'rival ', ], xpos=[ur' Crest']) + #55
#lema(ur'[Ff]ris_ó_n_o', xpre=[ur' Ed ', ur'Frederik ', ur'Claude ', ur'Bernard ', ur'Casa ', ur'Herman ', ur'Hydroperla\]\] ', ur'Hôtel ', ur'Isoperlinae ', ur'Le ', ur'Lorenzo ', ur'Mauro ', ur'Nino ', ], xpos=[ur' : L\'or', ur'\]\]es', ]) + #11
#[(ur'< *(?P<a>[Bb][Rr]) *>', ur'<br />')] + #1
#lema(ur'(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|dici?embre)_ de_ (?:\[\[|)[1-9][0-9][0-9]+_ del', xpos=[ur' sullo']) +#lema(ur'[Cc]ombusti_ó_n_o', xpre=[ur'Pyrokinesis, ', ur'Diesel ', ur'Second ', ur'Internal ', ur'Autodesk ', ur'Unsteady ', ur'Internacional ', ur'[Cc]oal ', ur'Human ', ur'Inner ', ur'Valve ', ur'Embryo: ', ur'fuel ', ur'plugin ', ur'Spontaneous '], xpos=[ur' (?:& de|as|des|et|of|in|for|and|Technologies|System|de végétaux|en général|improved|Spontaneous|stationary|Science|[Ee]ngines?|[Ee]ngineering|installations|cycle|Chamber|Emissions|products|Deposits|processes|systems|ramjet|2008|2009)\b', ur'" \(2004']) + #1
#lema(ur'[Cc]ombat_í__i') + #1
#lema(ur'[Cc]ompart_í__i') + #1
#lema(ur'[Cc]onclu_í__i') + #1
#lema(ur'[Cc]onoc_í__i') + #1
#lema(ur'[Cc]onsegu_í__i') + #1
#lema(ur'[Cc]ontribu_í__i') + #1
#lema(ur'[Ll]_á_ser(?:es|)_a', xpre=[ur'Manson ', ur'Optic ', ur'dot ', ur'Five ', ur'operating ', ur'[Rr]uby ', ur'Tanto ', ur'Tactical ', ur'Liquid ', ur'Dieter ', ur'Energy ', ur'Dark ', ur'revista \'\'', ur'Vulcan ', ur'Break ', ur'Ax ', ur'Victory ', ur'Living ', ur'Festiva y ', ur'Ford ', ur'RC ', ur'Airborne ', ur'[Ee]lectron ', ur'regreso de ', ur'Clase ', ur'VTech ', ur'disciplina de ', ur'Christine '], xpos=[ur' (?:d|558|Beam|ring|Ranging|Ghost|werden|flip|cannon|battle|TV|scalpel|propulsion|[Ww]eapon|Writing|Research|gyroscope|physics|Blast|Rods?|Warning|Gun|Lipolysis|Harp|Control|Imaging|guide|Performance|que se|16|4\.7|Triangulation|Scanners|stapedotomy|JDAM|Stratos|ranging|Picos|active|Funboat|[Aa]ssisted|Radial|II|Induced|and|disc|Max|Shark|Tanks|Army|Conquest|settler|plasmas?|Fusion|excimer|Surgery|Lock|Compact|EX2|[Tt]ag|Combat|deputy|Innovations|Blaster|desorptio|Squad|50|128|350|treatment|Invasion|with|Disc|Store|Turntable|Airlines|lancers|Interferometer|Mission|Altimeter|Squad|Physics|M[eé]ga ?[Jj]oule|Therapy|Clinic|Guided|Point|Tank|Vidéo Titres|Clay|Image|Retro|\([Vv]ela)', ur'(?:’s Edge|[+\']|, (?:D|Silver|Ultraprisma|Point))\b']) + #1734
#lema(ur'[Nn]ac_í__i'. xpos=[ur' Eldeniz']) + #1
#lema(ur'[Vv]_í_a_i', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpre=[ur'ella estaba ', ur'Dante ', ur'Génova: ', ur'Giovanni '], xpos=[ur' (?:(?:\'\'|)\[\[(?:Alessandro|Accademia|Cola di|Trionfale|Balbo|Santa (?:Brigida|Pudenziana)|Panisperna|Barletta|Crescenzio|Colonna|Ottaviano|Luisa di|Pietro|Andrea|Ulpiano|Sforza|Pompeo|Favència|Lucrezio|Cesi|Cicerone|Vittoria|Leone|del Lavinaio|Giovanni|Nolana|Girolamo|Tanucci|Bernardo|Massagué|Giulini|Meravigli|Rovello|Dante|Salvator|Yolanda)|Acton|Alessandrina|VIII|Apia|Nazionale|Amba|Appia|Arsenale|Augusta|Bellini|Bolognese|Bonazzi|Brigate|Broggi|Buonarroti|C\.|Caecilia|Calabritto|Capitolina|Capo|Capolecase|Cassa|Cassia|Cavour|Conciliazione|Condotti|Conziliazone|Coperta|Crucis|Dalmacia|Dino|Domitia|Donnalbina|Duchessa|Duomo|Egnatia|Emanuele|Emilia|Fani|Fellini|Flaminia|Foria|Forte|Francesco|Francigena|Fèrria|Garibaldi|Ghibellina|Giardini|Giordano|Giorgio|Giovanni|Giovenale|Giulia|Giulio|IV Novembre|Júlia|Laietana|Lata|Latina|Lattea|Lemovicensis|Maggio|Manzoni|Margutta|Marina|Marino, Enrico Reggiani|Mario Fani|Marmorata|Medina|Merulana|Montevecchio|Naquane|Nomenklaturo|Nomentana|Orazio|Orefici|Palestro|Panoramica|Pasquirolo|Petrarca|Piccinni|Piedigrotta|Pignolo|Podiensis|Porta|Portuense|Posillipo|Postumia|Principi|Prè|Rattazzi|Redi|Roma|Salvini|S\. Agostino|SS\. Trinità|Sacra|Sacro Monte|Salaria|Salaria|Salvator|San (?:Biagio|Pietro|Tommaso)|Sant|Sardegna|Stazio|Stresa|Strozzi|Taddeo|Tiburtina|Tiburtina|Toledo|Tolemaide|Tolosana|Traiana|Trajana|Trento|Tuscolana|Ugo Foscolo|Valeria|Veneto|Verdi|Vicaria|Vittorio|XX|[Tt]uronensis|d|de (?:Renai|\'Ginori)|de\' Tornabuoni|degli|dei|del (?:Castello|Corso|Molo|Proconsolo|cibo|peccato|silenzio)|della|di|làctia|morta|per|pi[uù]|poiché|si Santa|veneziana)\b']) + lema(ur'[Vv]_í_as_i', xpre=[ur'Air ', ur'Michel ', ur'longas ', ur'gozosa ', ur'Josefa ', ur'das ', ur'fr ', ur'principais ', ], xpos=[ur' (?:é|Claudia|Paradisi|GZ|dello|Apia|Stradella|Gabelli|\[\[Nino|Emanuele|Teatro Greco|Domini|Persequar|[Dd][ao]|et|Romanas em|Mahou|de Sinalização|Mezzocannone|Porta|Guglielmo|Nazario|Nuova|Gallica|Ulisse|Mazzini|Dunes|San Frediano|Longa|de\'Gori|Vergini|Nazionale|Augusta|Amba|Cavour|priondas|Ratti-Vitali|Fani|a vis|eius|tuas|navegáveis)\b', ur'(?:\]|\'\' \(\[\[1884|\'\' en su)']) + #800
#lema(ur'_[[Parque nacional Waraira Repano|Parque nacional El Ávila]]__\[\[Parque [Nn]acional El Ávila\]\]') + #1
#lema(ur'_[[Parque nacional de Yosemite]]__\[\[(?:Yosemite National Park)\]\]') + #1
#lema(ur'_[[Parque nacional El Cajas]]__\[\[(?:Parque [Nn]acional Cajas)\]\]') + #1
#lema(ur'_[[Parque nacional Sumaco Napo-Galeras]]__\[\[(?:Parque [Nn]acional Sumaco-Napo-Galeras)\]\]') + #1
#lema(ur'_[[Parque nacional Yasuní]]__\[\[(?:Parque nacional Yasuni)\]\]') + #1
#lema(ur'_[[Parque nacional del Gran Cañón]]__\[\[(?:Grand Canyon National Park)\]\]') + #1
#lema(ur'_[[Parque nacional Cañón de los Reyes]]__\[\[(?:Parque [Nn]acional Kings Canyon|Kings Canyon National Park)\]\]') + #1
#lema(ur'_[[Parque nacional de los Arcos]]__\[\[(?:Parque [Nn]acional Arches|Arches National Park)\]\]') + #1
#lema(ur'_[[Parque nacional Archipiélago de Los Roques]]__\[\[(?:Parque [Nn]acional Los Roques)\]\]') + #1
#lema(ur'_[[Parque nacional Enrique Olaya Herrera]]__\[\[(?:Parque [Nn]acional "Enrique Olaya Herrera")\]\]') + #1
#[(ur'\[\[(?:Parque [Nn]acional de Kosciuszko|Parque [Nn]acional Kosciuszko)(?P<a>\]|\|)', ur'[[Parque nacional Kosciuszko\g<a>')] + #1
#[(ur'\[\[(?:Parque [Nn]acional Keoladeo|Parque Nacional de Keoladeo)(?P<a>\]|\|)', ur'[[Parque nacional de Keoladeo\g<a>')] + #1
#[(ur'\[\[(?:Parque [Nn]acional Pilcomayo|Parque [Nn]acional Río Pilcomayo)(?P<a>\]|\|)', ur'[[Parque nacional Río Pilcomayo\g<a>')] + #1
#[(ur'\[\[(?:Parque [Nn]acional de Etosha|Parque Nacional Etosha)(?P<a>\]|\|)', ur'[[Parque nacional Etosha\g<a>')] + #1
#[(ur'\[\[(?:Parque [Nn]acional de Mesa Verde|Parque [Nn]acional Mesa Verde)(?P<a>\]|\|)', ur'[[Parque nacional Mesa Verde\g<a>')] + #1
#[(ur'\[\[(?:Parque [Nn]acional de Redwood|Parque Nacional Redwood)(?P<a>\]|\|)', ur'[[Parque nacional Redwood\g<a>')] + #1
#[(ur'\[\[(?:Parque [Nn]acional de Serengueti|Parque nacional Serengeti|Parque [Nn]acional Serengueti)(?P<a>\]|\|)', ur'[[Parque nacional Serengueti\g<a>')] + #1
#[(ur'\[\[(?:Parque [Nn]acional Henry Pittier)(?P<a>\]|\|)', ur'[[Parque nacional Henri Pittier\g<a>')] + #1
#lema(ur'[Uu]top_í_as?_i', xpre=[ur'\bbis ', ur'dell\’', ur'\b[Aa&] ', ur'\b[Ll]\'', ur'\b(?:[Ii]n|[Tt]o|[Oo]f) ', ur'\b(?:for|the) ', ur'1991: \'\'', ur'[Nn]ew ', ur'and ', ur'form ', ur'Rinne ', ur'invasión hacia ', ur'1951\)\|', ur'Serrat\]\]: \'\'\[\[', ur'revista \'\'', ur'identità e ', ur'Black ', ur'neocon ', ur'Below ', ur'Inverted ', ur'Modern ', ur'grupo ', ur'realistic ', ur'destaca ', ur'[Rr]egency ', ur'Ideology, ', ur'como \'\'', ur'brasileña\)\|', ur'banda\)\|', ur'estudio\)\|', ur'Texas\)\|', ur'Axxis\)\|', ur'título "', ur'Pirate ', ur'Estudios ', ur'ambiguous '], xpos=[ur' (?:in|is|of|or|Records|Sky|lanzaron|possibile|Jovent|and|en Ohio|calcistica|Triumphans|Manabi|Sound|Limited|e disincanto|Planitia|\((?:1951|Texas|estudio|banda|álbum))\b', ur'(?:, (?:Limited|, O)\b|\'\'\')']) + #859
#lema(ur'[Ss]erv_í__i', xpre=[ur'\b[Dd]e ', ur'\bdei ']) + #1
#[(ur'\[\[(?:Tabla [Gg]eneral de la Copa Mundial de Fútbol|Tabla estadística de la Copa Mundial de Fútbol)(?P<a>\]|\|)', ur'[[Anexo:Tabla estadística de la Copa Mundial de Fútbol\g<a>')] + #1
#lema(ur'[Rr]oman_í__i', xpre=[ur'\b(?:ai|de) ', ur'\b(?:dei|que) ', ur'Darlan ', ur'Hugo ', ur'Paulino ', ur'[Ll]udi ', ur'Jacquelin ', ur'Abric ', ur'Papa ', ur'fuerte en ', ur'piezas en ', ur'Imprenditori ', ur'Crescenzi ', ur'Milton ', ur'castelli ', ur'Paesisti ', ur'Pontefici ', ur'Darlan ' ur'populi ', ur'Populi ', ur'equites ', ur'Arnaldo ', ur'Malavasi / ', ur'Francesca ', ur'Felice ', ur'imperatori ', ur'Castelli ', ur'Architettura de ', ur'civis ', ur'[Cc]ives ', ur'populi ', ur'Felice ', ur'italiano\]\], \'\'', ur'[Ii]mperii '], xpos=[ur' (?:e quanti|ite|cree|enriqueció|language|Writers|Pontifices|Pontificis|Pontificies|rapsodia|Ranch|imperatoris|se inspirará)']) + #929
#lema(ur'[A]gr_í_colas?_i', xpre=[ur'juego\)\|', ur'propio ', ur'obra de ', ur'Giulio ', ur'Rodolphus ', ur'Andreas ', ur'Agarista ', ur'Alexander ', ur'Bibliotheca ', ur'Christoph ', ur'Friedrich ', ur'Georg ', ur'Georgius ', ur'Ipsicratea ', ur'Julio ', ur'Julius ', ur'Legione ', ur'Ludwig ', ur'Martin ', ur'Mikael ', ur'Papilio ', ur'Popolare ', ur'Stephan ', ur'Theophilus y ', ur'Stazion[ae] ', ur'Tácito ', ur'\(3212\) ', ur'\|\| ', ur'familia ', ur'ripresa ', ], xpos=[ur' (?:estaba|escribió|Village|Sperimentale|Barbaruccio|nació|co-escribió|Gaetano|Britanniam|de Avignon|en junio|fue|\(juego|también tradujo)', ur'(?:\'s|[\'\]]|: He|, (?:Alexander|Martin|Johann|G|que|Georg\b))', ]) + #6
#[(u'-', u'–')] + %Daña las tablas
#lema(ur'[Zz]ul_ú__u', xpre=[ur'TV2 ', ur'Tambja ', ur'Olios ', ur'Hora ', ur'Stella ', ur'Nota: ', ur'Paulo ', ur'Shaka ', ur'rufoglaucus ', ur'Scherma ', ur'Romeo ', ur'Yankee y ', ur'1922\) ', ur'Compañía ', ur'bakua ', ur'vivo \'\'', ], xpos=[ur' (?:Army|Natiou|Impi|Nation|Dawn|Gems|Time|Cobra|kaNtombhela)', ur'(?:\'\' \((?:álbum|EP)|”|\|\|Zu lu)', ]) + #256
#lema(ur'[Cc]l_í_max_i', xpre=[ur'\bG1 ', ur'\| ', ur'III ', ur'Til ', ur'Eleven ', ur'Tojeiro - ', ur'Project: ', ur'IV ', ur'Mk\.1 ', ur'Halseylec - ', ur'motores ', ur'Anal ', ur'Desire ', ur'Grupo ', ur'John ', ur'locomotora ', ur'Lotus 15 ', ur'Zero ', ur'[Ff]orma ', ur'[Ss]uper ', ur'álbum\)\|', ur'banda\)\|', ur'Games\]\], ', ur'The ', ur'[|"]', ur'M[ií]chigan\)\|', ur'Colorado\)\|', ur'Georgia\)\|', ur'Fighting ', ur'Minnesota\)\|', ur'Kansas\)\|', ur'Coventry '], xpos=[ur' (?:/ Anti-Climax|\((?:banda|impulsó|álbum|ha desarrollado|And|Racing|Colorado|M[ií]chigan|Georgia|Kansas|Minnesota)|Mystery|F2|Blues|Deka|Road|Graphics|Jump|[Gg]roup|Entertainment|Studios|Golden|Heroes|\((?:Kansas|canción|Georgia))', ur'(?:[!<]|\'\'|, \[\[Nebraska)']) + #2058
#lema(ur'[Bb]_ó_xer_o', xpre=[ur'Der ', ur'Thai ', ur'Beautiful ', ur'Ronnie ', ur'R\. ', ur'(?:Tom|USS) ', ur'Live ', ur'Thomas ', ur'por ', ur'Charles ', ur'Blade ', ur'Shadow ', ur'Kick ', ur'disposición ', ur'sistema \'\'', ur'Códice ', ur'[Mm]otor ', ur'boxer\|', ur'Berlinetta ', ur'Nathan ', ur'Barbara ', ur'cilindros ', ur'Alison ', ur'Deutscher ', ur'The ', ur'opuestos \(\'\'', ur'Peugeot ', ur'GTK ', ur'HMS '], xpos=[ur' (?:vs|era una|ganó|MRAV|sobre|briefs|shorts|de usar|Rebellion|\((?:álbum|Protocol|[Mm]arca|brief))\b', ur', Ace']) + #1077
#lema(ur'[Rr]eh_ú_s(a[ns]?)_u') + #1
#lema(ur'[Pp]_ó_ster_o', xpre=[ur'Large ', ur'International ', ur'one ', ur'Film ', ur'Mark ', ur'[Rr]elease ', ur'film festival ', ur'Steven ', ur'[Tt]heatrical ', ur'[Tt]easer ', ur'Meryl ', ur'Metals ', ur'[Oo]riginal ', ur'film ', ], xpos=[ur' (?:[Cc]hild|vailable|release|product|Children|Service)', ]) + #663
#lema(ur'[Cc]ol__aciones_l') + #Existe collación
#lema(ur'_enero de_ (?:\[\[|)[1-9][0-9][0-9]+_gennaio') + #1
#lema(ur'_febrero de_ (?:\[\[|[1-9][0-9][0-9]+)_febbraio') + #1
#lema(ur'_abril de_ (?:\[\[|[1-9][0-9][0-9]+)_aprile', xpre=[ur'’']) + #1
#lema(ur'_mayo de_ (?:\[\[|)[1-9][0-9][0-9]+_maggio', xpos=[ur' \(la historia']) + #1
#lema(ur'_junio de_ (?:\[\[|)[1-9][0-9][0-9]+_giugno') + #1
#lema(ur'_julio de_ (?:\[\[|[1-9][0-9][0-9]+)_luglio') + #1
#lema(ur'_septiembre de_ (?:\[\[|[1-9][0-9][0-9]+)_settembre') + #1
#lema(ur'_octubre de_ (?:\[\[|[1-9][0-9][0-9]+)_ottobre') + #1
#lema(ur'_noviembre de_ (?:\[\[|)[1-9][0-9][0-9]+_novembre', xpre=[ur'(?:du|le) ']) + #1
#lema(ur'[Ff]ranc_é_s+_e', pre=ur'\by ', xpre=[ur'Chalmers ', ur'Archibald ', ur'Charles ', ur'Niewyk ', ur'Wycomb ', ur'Bentivolgio ', ur'Cleveland ', ur'Ejecutiva, ', ur'Wentworth; ', ur'Cueva ', ur'Elsie ', ur'Garth ', ur'Maria ', ur'Samuel ', ur'Baker ', ur'John ', ur'Mary ', ur'Muscinées ', ur'Novio ', ur'[Dd]e ', ur'[Gg]avilán ', ur'amante ', ur'amiga imaginaria ', ur'casadas ', ur'colegio ', ur'confesión ', ur'esposo ', ur'femenino ', ur'herman[ao] ', ur'hijo ', ur'homicidio ', ur'mamá ', ur'marido ', ur'mayor ', ur'muerte ', ur'papá ', ur'poemas ', ], xpos=[ur' (?:G\.|Lockridge|Kroll|A\. Bouffard|Early|Karttunen|Block|Barber|Vaughan|Mundy|and|fueron|Lamont|Griffiths|cámaras|Board|Lucille|estaría|Parker|Bolton|Ford|O’Connor|Wright|Smith|Lincoln|Anne|Hardinge|Steloff|Turner|Dade|Gifford|Farmer|Boscawen|Shea|Gorges|Barton|Beverly|Bratt|Baard|Buss|Brandon|Bean|Worsley|Abington|Walker|Newton|Coles|Osgood|Sargent|Goodrich|Chiapetta|Hunter|Rita|Ribes|Jennings|Mayes|Malone|McDormand|McMahon|Victoria|\'\'Fannie|"Baby|Jarque)', ur'\]\][a-z]', ]) + #89
#lema(ur'_inglé_s_(?:Ingl[eé]|ingle)', pre=ur'\bIdioma ') + #583
#(ur'(?P<ii>[=]+ *)(?P<tt>(?:Edad Media|Edad Moderna|Edad Antigua|Edad Contemporánea))(?P<dd> *[=])', titulo),  
#lema(ur'[Rr]e__valu(?:a|ó|a(?:r|ría[ns]?|ción|ciones|mos|ndo(?:l[aeo]s?|)|d[ao]s?|ron))_e') + Reevaluar existe
#lema(ur'[Rr]e_valú_(a[ns]?|e)_eval[uú]') + Reevaluar existe
#lema(ur'[Hh]isp_á_nic[ao]s?_a', xpre=[ur'[ACDEO]\. ', ur'[Xx×] ', ur'x\'\' ', ur'var\. ', ur'subesp\. \'\' ', ur'subsp ', ur'subsp\. \'\' ', ur'Æra ', ur'Aera ', ur'Abies ', ur'Acta ', ur'Anaecypris ', ur'Adagia ', ur'Adagiae ', ur'Anabasis ', ur'Arenaria ', ur'Berberis ', ur'Capra ', ur'Compendiosa historia ', ur'Cataglyphis ', ur'Cakile ', ur'Carlina ', ur'Coris ', ur'circe ', ur'Claussenia ', ur'Dactylis ', ur'Draba ', ur'Epipactis ', ur'Eratigena ', ur'Fritillaria ', ur'Genista ', ur'Gaudinia ', ur'Gypsophila ', ur'Hemifusulina ', ur'Hispidella ', ur'Hyacinthoides ', ur'Juniperus ', ur'Lacerta ', ur'[Ll]inguarum ', ur'Leptynia ', ur'Leucarum ', ur'Lonicera ', ur'Medievalia ', ur'monarchia ', ur'Ortegia ', ur'Orientalia ', ur'Oenanthe ', ur'Oenanthe\]\] ', ur'Organa ', ur'Pax ', ur'Periballia ', ur'Praehistorica ', ur'Peregrinatio ', ur'Pinus ', ur'Pistorinia ', ur'Podarcis ', ur'[Pp]latanus ', ur'Puccinellia ', ur'[Pp]yrenaica ', ur'Probosca ', ur'religione ', ur'[Ss]alvia ', ur'sigillata ', ur'Sericomyia ', ur'Scorzonera ', ur'Studia ', ur'Tegenaria ', ur'[Vv]accaria ', ur'[Vv]alencia ', ur'Verba ', ur'Vulpia ', ur'VIII ', ur'Continuatio ', ur'et '], xpos=[ur' ad\b', ur'\'\'']) + #1
#lema(ur'[Oo]_b_ras_') + #lema(ur'_ho_ras_o') + lema(ur'_Ho_ras_O') + #lema(ur'[Oo]_t_ras_') + #1
#lema(ur'[Hh]urt_ó__o', pre=ur'\b[Yy] ', xpre=[ur'error ', ur'crédito ', ur'infiltración ', ur'violaciones ', ur'secuestro ', ur'robo ', ], xpos=[ur' agravado']) + #11
#lema(ur'[Cc]ri_ó__o', pre=ur'[Ss]e ') + También existe crio #1835
#lema(ur'[Ee]spec_í_fic[ao]_i', xpre=[ur'(?:[Ss]e|[Nn]o|[Ll]o) ', ur'[Qq]ue ', ur'[Nn]o lo ', ur'sistema ', ur'IEEE 1541 ', ur'también ', ur'donde ', ur'(?:como|cual) '], xpos=[ur' (?:el|la|los|las|también|muchas|como|quien|["“«]?(?:b|del?|[Ll]os|[Ee]l|[Ll]a|una?|a una|qu[ée]|sobre|si|en|un|dos|tres|cuatro|cinco|seis))\b', ur':']) + #1
#lema(ur'[Pp]o_é_tic[ao]s?_e', xpre=[ur'\bdi ', ur'Alstroemeria ', ur'[Aa]rs ', ur'Bibliographia ', ur'Domus ', ur'Insula ', ur'L’Arte ', ur'Musica ', ur'Prova ',ur'Puglia ', ur'Scuola ', ur'Viola ', ur'all\'antropologia ', ur'componimento ', ur'iiO\)\|', ur'dell’arte ', ur'lingua ', ur'nella', ur'vera ', ], xpos=[ur' (?:[de]|di| - All|na|(?:: |)in|artigiana|dedicata|latina|italiana dell|Astronomica|all|di|dell|della|\(álbum|idea Reipublicae|explicationes)\b', ur'\'\'', ]) + #6
#lema(ur'[Ee]rosi_ó_n_o', xpre=[ur'\bon ', ur'Classic ', ur'Aground y ', ur'International ', ur'Island ', ur'Particle ', ur'Metabolic ', ur'Research ', ur'[Ss]oil ', ur'[Tt]he ', ur'l\'', ur'from', ur'using', ur'less ', ur'o \'\'\'', ur'película\)\|', ur'and ', ur'Coastal ', ur'dental ', ur'wave ', ur'wind ', ], xpos=[ur' (?:&|of|or|[io]n|is|at|and|caused|risk|Media|\(película|Research|- Festum)\b', ur'(?:\]\](?:es|ad[ao]s?|antes?)|: las|," "Corrosion|, and|—diagnosis)', ]) + #89
##lema(ur'[Dd]e__ l[ao]s?_l') + #Parece que es aceptado.
#lema(ur'[Tt]ra__splantad[ao]s?_n') + #6 existe transplante
#lema(ur'[Tt]ra__splante[ns]?_n') + #67
#lema(ur'Beltr_á_n_a', xpre=[ur'\bi ', ur'Sant ', ur'Vicenç ', ur'Adolf ', ur'Robert ', ur'Yurizan ', ur'obra de ', ur'Orlando ', ur'azul ', ur'Armando ', ur'Federico ', ur'Miguel ', ur'Termens ', ur'Tony ', ur'Benjamin '], xpos=[ur' Masses']) + #1
#lema(ur'L_o_pez_ó', pre=ur'Santana ') + #1
#lema(ur'Basar_í_an_i') + #0
#lema(ur'[Aa]lg_ún_ (?:[AÁaá](?:rea|guila|lgebra)|ánima|a(?:rma|rca|lma|lza|gua|la|rpa|ve)|ha(?:bla|da|cha|mbre|mpa|rpa))_[uú]na') + #No es error
#lema(ur'[Nn]ing_ún_ (?:[AÁaá](?:rea|guila|lgebra)|ánima|a(?:rma|rca|lma|lza|gua|la|rpa|ve)|ha(?:bla|da|cha|mbre|mpa|rpa))_[uú]na') + #No es error
#lema(ur'[Aa]que_l_ (?:[AÁaá](?:rea|guila|lgebra)|ánima|a(?:rma|rca|lma|lza|gua|la|rpa|ve)|ha(?:bla|da|cha|mbre|mpa|rpa))_lla') + #No es error
#lema(ur'_ha_ contado) + #200 a contado o crédito
#lema(ur'[Cc]o_m_pila(?:d[ao]s?|ciones)_', xpos=[ur' por el orden']) + #existe copilar
#lema(ur'[Cc]onfes_ó__o', xpre=[ur'\b(?:[Uu]n|[Ss]u|[EeÉe]l|[Ee]s|no) ', ur'ateo ', ur'caníbal ', ur'incendiario\]\] ', ur'[Mm]elómano ', ur'simpatizante ', ur'asesino ', ur'pagano ', ur'republicanismo ', ur'hincha ', ur'admirador ', ur'asesino ', ur'seguidor ', ur'anglófilo ', ur'miembro ', ur'convicto ', ur'amor ', ur'Amante ', ur'halló ', ur'delito ', ur'suicida ', ur'homicida ', ur'socialista ', ur'fascista ', ur'\by ', ur'cristiano ', ur'homosexual ', ur'fan ', ur'autor ', ur'objetivo '], xpos=[ur' (?:de|del|hincha|seguidor|fanático|aficionado|ladrón|amante|adicto)\b', ur'\'(?:\'|, confuso)']) + #1
#lema(ur'[Aa]_ _d[oó]nde_', xpos=[ur' marchaba']) + #Adonde existe
#lema(ur'[Aa]ctuar_í_a_i', xpre=[ur' (?:en|de) ', ur' o ', ur'[Cc]iencia ', ur'[Nn]otaria ', ur'justicia ', ur'mecanógrafa, ', ], xpos=[ur'\'', ]) + #5
#lema(ur'[s]ali_o__ó', pre=ur'[Ee]mperador ') + #6

#Prereplacements
fechas = [
lema(ur'_e_nero_E', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_f_ebrero_F', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_m_arzo_M', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_a_bril_A', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_m_ayo_M', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_j_unio_J', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_j_ulio_J', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ', xpos=[ur' (?:César|A\.)']) + #1
lema(ur'_a_gosto_A', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_s_eptiembre_S', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ', xpre=[ur'Liz ']) + #1
lema(ur'_o_ctubre_O', pre=ur'(?:(?:(?<!12 )[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_n_oviembre_N', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_d_iciembre_D', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') +
lema(ur'(?:[Ee]nero|[Ff]ebrero|[Mm]arzo|[Aa]bril|[Mm]ayo|[Jj]unio|[Jj]ulio|[Aa]gosto|[Ss]eptiembre|[Oo]ctubre|[Nn]oviembre|[Dd]iciembre)_ de_ (?:\[\[|)[1-9][0-9][0-9][0-9]_(?:,|)', xpre=[ur'Ediciones del 4 de ', ], xpos=[ur' sullo', ]) + #33918
lema(ur'\b(?:[1-9]|[012][0-9]|3[01])_ de_ (?:[Ee]nero|[Ff]ebrero|[Mm]arzo|[Aa]bril|[Mm]ayo|[Jj]unio|[Jj]ulio|[Aa]gosto|[Ss]eptiembre|[Oo]ctubre|[Nn]oviembre|[Dd]iciembre)_') + #8409
[]][0]

grupoPre = fechas + [
#[(ur'\[\[(?P<a>.+?)\|\g<a>\]\]', ur'[[\g<a>]]')] + #1
lema(ur'[a-záéíóúñü0-9.]+ +[a-záéíóúñü0-9.]*[a-záéíóúñü0-9]_ _[a-záéíóúñü0-9.]+ +[a-záéíóúñü0-9.][a-záéíóúñü0-9]_  +_x') + #1
lema(ur'[a-záéíóúñü0-9.]+ +[a-záéíóúñü0-9.]*[a-záéíóúñü0-9]_ _[a-záéíóúñü0-9.]+ +[a-záéíóúñü0-9.]*[a-záéíóúñü0-9]_  +_x') + #1
lema(ur'[a-záéíóúñü0-9.]*[a-záéíóúñü0-9]_ _[a-záéíóúñü0-9.]+ +[a-záéíóúñü0-9.]+ +[a-záéíóúñü0-9.]*[a-záéíóúñü0-9]_  +_x') + #1
lema(ur'[a-záéíóúñü0-9.]+ +[a-záéíóúñü0-9.]+ +[a-záéíóúñü0-9.]*[a-záéíóúñü0-9]_ _[a-záéíóúñü0-9.]*[a-záéíóúñü0-9]_  +_x') + #1
lema(ur'[a-záéúíóúüñ]*_, _(?!title)[a-záéúíóúüñ]{2}[a-záéúíóúüñ]*_,_x') + #1
lema(ur'[a-záéúíóúüñ]*_, _(?!title)[a-záéúíóúüñ]{2}[a-záéúíóúüñ]*_,_x') + #1
lema(ur'_a  b  c  d  e  f  g  h__a b c d e f g  h') + #1
lema(ur'_Sobre la base de__En base a') + #1
[(ur'((?: [a-záéíóúñ][a-záéíóúñ]+|\]\])[.;])([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+ )', ur'\1 \2')] +    
lema(ur'_ _(?:[A-Z][a-záéíóúñ]*[áéíóúñ][a-záéíóúñ]*|[ÁÉÍÓÚÑ][a-záéíóúñ]+)_', pre=ur'[a-záéúíóúüñA-ZÁÉÚÍÓÚÜÑ][a-záéúíóúüñA-ZÁÉÚÍÓÚÜÑ\]]+[\.;]', xpos=[ur'\.']) + #1

####Apellidos
lema(ur'Fern_á_ndez_a', xpre=[ur'and ', ur'd’Anita ', ur'Ioseph ', ur'J[eé]r[oô]me ',ur'Jean ', ur'Valentim ', ur'Domenique ', ur'Dominique ', ur'Heine ', ur'Mervyn '], xpos=[ur' Islands']) + #1
lema(ur'G_á_lvez_a', xpos=[ur'\.gov']) + #1
lema(ur'Le_ó_n Garc[ií]a_o') + #1
lema(ur'Garc_í_a_i', xpre=[ur'\b[AC]\. ', ur'\bi ', ur'\bto ', ur'1982: ', ur'Heine ', ur'Jerry ', ur'João ', ur'Fabricio ', ur'Souza ', ur'Pinto ', ur'Isaurinha ', ur'los capitanes Bartolome ', ur'Aleixo ', ur'Alexandre ', ur'Lourenço ', ur'Jacy ', ur'Caroline ', ur'Assumpção ', ur'Gertrudes ', ur'Nicole ', ur'Ribeiro ', ur'Alex ', ur'Vila ', ur'Gon[sç]alo ', ur'Stênio ', ur'Ecole de ', ur'Washington\)\|', ur'Salvador\)\|', ur'Escrivà '], xpos=[ur' (?:d|dos|III|i|Grau|Middle|Inyesta|Sarmento|de (?:Resende|Orta|Mello)|en Bassein|en 1556|fils|Fària|\((?:Salvador|Washington)|Publications)\b', ur'\'s']) + #1
lema(ur'G_ó_mez_o', xpre=[ur'[Oo]f ', ur'álbum de ', ur'Francisco ', ur'Dioguo ', ur'Selena ', ur'Thomas ', ur'Michelle ', ur'Scott ', ur'Selena '], xpos=[ur' (?:Gallery|ha obtenido|Addams|recibió 3|\(banda)', ur'(?:\]|\'s)']) + #1
lema(ur'Gal_í_ndez_i') + #1
lema(ur'Gonz_á_lez_a', xpre=[ur'Yann ', ur'Noe ',]) + #1
lema(ur'L_ó_pez_o', xpre=[ur'4657\) ', ur'v\. ', ur'Santana ', ur'Manoel ', ur'Brook Lopez\|', ur'Brook ', ur'Rick ', ur'Olivia ', ur'Bernard ', ur'Colby ', ur'East ', ur'George ', ur'Elysia ', ur'Litoria ', ur'Gerard ', ur'Jennifer ', ur'Lynn '], xpos=[ur' (?:Tonight|Expeditions|Island|dos)', ur'(?:\. Genova|\'s|, Steven)']) + #1
lema(ur'Mart_í_nez_i', xpre=[ur'Guillaume ', ur'Deuce" ', ur'California\)\|', ur'Georgia\)\|', ur'Deuce ', ur'Vicci ', ur'Dean ', ur'Sammy ', ur'Pamela ', ur'Yannick '], xpos=[ur' \((?:California|Georgia)']) + #1
lema(ur'Negr_í_n_i') + #1
lema(ur'Ram_í_rez_i', xpre=[ur'Erika ', ur'Twiggy ']) + #1
lema(ur'S_á_nchez_a', xpre=[ur'[Oo]f ', ur'Nia ', ur'Little ', ur'Temple ', ur'Cole ', ur'Enfants de ', ur'Mike ', ur'Dirty ', ], xpos=[ur' (?:Get High|tradition)', ]) + #1
lema(ur'Su_á_rez_a', xpre=[ur'Jean de ', ur'und ', ur'Jeremy ', ur'R, ', ]) + #1
lema(ur'V_é_lez_e', xpre=[ur'Maria '], xpos=[ur' (?:Mostar|& Dubail)']) + #1
lema(ur'Ter_á_n_a', xpos=[ur' Ikkemen', ur'\'\'']) + #1
lema(ur'_Á_lvarez_A', xpre=[ur'J '], xpos=[ur' Bernardez']) + #1
####Nombres
lema(ur'F_é_lix_e', pre=ur'San ') + #1
lema(ur'Rub_é_n Ram[ií]rez_e') + #1
lema(ur'Andr_é_s (?:Alberto|Álvarez|García|Gómez|González|Jiménez|Martínez|Pérez|Ramírez|Rodríguez|Sánchez|Suárez|Vásquez)_e') + #1
lema(ur'Crist_ó_bal (?:Colón|Álvarez|García|Gómez|González|Jiménez|Martínez|Pérez|Ramírez|Rodríguez|Sánchez|Suárez|Vásquez)_o') + #1
lema(ur'Dar_í_o (?:Alberto|Álvarez|García|Gómez|González|Jiménez|Martínez|Pérez|Ramírez|Rodríguez|Sánchez|Suárez|Vásquez)_i') + #1
lema(ur'Juli_á_n (?:Álvarez|García|Gómez|González|Jiménez|Martínez|Pérez|Ramírez|Rodríguez|Sánchez|Suárez|Vásquez)_a') + #1
lema(ur'Mar_í_a (?:Fernanda|Isabel|Álvarez|García|Gómez|González|Jiménez|Martínez|Pérez|Ramírez|Rodríguez|Sánchez|Suárez|Vásquez)_i') + #1
lema(ur'Mar_í_a Antonia_i', xpos=[ur' Salvà']) + #1
lema(ur'Nicol_á_s_a', pre=ur'San ') + #1
lema(ur'Nicol_á_s (?:Alberto|Álvarez|García|Gómez|González|Jiménez|Martínez|Pérez|Ramírez|Rodríguez|Sánchez|Suárez|Vásquez)_a') + #1
lema(ur'Ram_ó_n (?:Alberto|Álvarez|García|Gómez|González|Jiménez|Martínez|Pérez|Ramírez|Rodríguez|Sánchez|Suárez|Tenias|Vásquez)_o') + #1
lema(ur'Tom_á_s (?:Alberto|Álvarez|Apóstol|García|Gómez|González|Jiménez|Martínez|Pérez|Ramírez|Rodríguez|Sánchez|Suárez|Tenias|Vásquez)_a') + #1
lema(ur'V_í_ctor (?:Alberto|Álvarez|García|Gómez|González|Jiménez|Martínez|Pérez|Ramírez|Rodríguez|Sánchez|Suárez|Vásquez)_i') + #1
lema(ur'Mar_ía J_uana_(?:ia [Jj]|ía j)') + #11
lema(ur'Mart_í_n (?:Alberto|Álvarez|García|Gómez|González|Jiménez|Martínez|Ramírez|Rodríguez|Sánchez|Suárez|Vásquez)_i') + #1
lema(ur'_José_ (?:Alberto|Alejandro|Alfonso|Alfredo|Alonso|Antonio|Batlle|Carlos|Castillo|Clemente|Daniel|Domingo|Eduardo|Emilio|Enrique|Eugenio|Feliciano|Felipe|Fernando|Fernández|Ferrer|Francisco|Gabriel|García|González|Gregorio|Guadalupe|Hernández|Ignacio|Javier|Joaquín|Juan|Julián|Luis|Luís|Manuel|Mari|Maria|Mariano|Martí|Martínez|María|Miguel|Moreno|Mourinho|Ortega|Ortiz|Pablo|Pardo|Pedro|Rafael|Ramón|Reyes|Ricardo|Rivera|Rizal|Roberto|Rodríguez|Santiago|Santos|Silva|Sánchez|Torres|Trinidad|Vicente|Zorrilla|Ángel|de San Mart[ií]n)_(?:jos[eé]|Jose)') + #1
lema(ur'_José_ (?:Abelardo|Acosta|Adolfo|Aguilar|Agustín|Alejo|Amador|Andrés|Benito|Bernardo|Blanco|Cabrera|Castro|Cela|Celestino|Demaría|Díaz|Elías|Eusebio|Faustino|Flores|Félix|Guerra|Gutiérrez|Gálvez|Gómez|Jiménez|Leonardo|León|López|Martín|Matías|Mujica|Muñoz|Mármol|Méndez|Nacho|Navarro|Nicolás|Nieto|Núñez|Ozámiz|Pascual|Pérez|Ramos|Ramírez|Rico|Ruiz|San|Serrano|Simón|Suárez|Tiburcio|Tomás|Toribio|Velásquez|Vázquez|Yves|Álvarez)_(?:jos[eé]|Jose)') + #1
lema(ur'_María_ (?:Gabriela)_(?:mar[ií]a|Maria)') + #1
lema(ur'_José_ del?_(?:jos[eé]|Jose)', pre=ur'San ') + #1
lema(ur'_María_ (?:Morelos?|Gisbert)_(?:mar[ií]a|Maria)', pre=ur'[Jj]os[eé] ', xpos=[ur' (?:Pereira|Neves)']) + #1
lema(ur'_María José__(?:[Mm]ar[ií]a jos[eé]|[Mm]ar[ií]a Jose|mar[ií]a José|Maria José)') + #1
lema(ur'_Simón Bolívar__(?:sim[oó]n [Bb]ol[ií]var|Simon [Bb]ol[ií]var|Simón bol[ií]var|Simón Bolivar)', xpre=[ur'Avenue '], xpos=[ur' (?:Award|Wall|Buckner|and)']) + #1
lema(ur'_Simón Díaz__(?:sim[oó]n [Dd][ií]a[sz]|Simon [Dd][ií]a[sz]|Simón d[ií]a[sz]|Simón Dia[sz]|Simón Días)') + #1

lema(ur'[Nn]eoyor_qu_ino_k') + #21
lema(ur'[Cc]ri_e__é', pre=ur'(?:[Ll]o|[Yy]o) ') + #última reforma
lema(ur'[Cc]ri_a_is_á') + #última reforma
lema(ur'[Cc]ri_e_is_é') + #última reforma
lema(ur'[Ff]i_e__é', pre=ur'(?:[Ll]o|[Yy]o) ') + #última reforma
lema(ur'[Ff]i_a_is_á') + #última reforma
lema(ur'[FF]i_e_is_é') + #última reforma
lema(ur'[Ff]lu_i_s?_í') + #última reforma
lema(ur'[Ff]ri_a_is_á') + #última reforma
lema(ur'[Gg]ui_e__é', pre=ur'(?:[Ll]o|[Yy]o) ') + #última reforma
lema(ur'[Gg]ui_a_is_á') + #última reforma
lema(ur'[Hh]u_i_s?_í', xpre=[ur' de ']) + #última reforma
lema(ur'[Ll]i_e__é', pre=ur'(?:[Ll]o|[Yy]o) ') + #última reforma
lema(ur'[Ll]i_a_is_á') + #última reforma
lema(ur'[Ll]i_e_is_é') + #última reforma
lema(ur'[Pp]i_e__é', pre=ur'(?:[Ll]o|[Yy]o) ') + #última reforma
lema(ur'[Pp]i_a_is_á') + #última reforma
lema(ur'[Pp]i_e_is_é') + #última reforma
lema(ur'[Rr]i_a_is_á') + #última reforma
lema(ur'[Tt]ru_a_n_á') + #última reforma
lema(ur'[Gg]ui_o_n_ó') + #última reforma
lema(ur'[Ii]_o_n_ó', xpre=[ur'Estudios ', ur'\'']) + #última reforma
lema(ur'[Mm]u_o_n_ó') + #última reforma
lema(ur'[Pp]ri_o_n_ó') + #última reforma
lema(ur'[Ss]_o_l(?:os|as?)_ó') + #última reforma
#lema(ur'[Ss]_o_lo_ó', xpos=[ur' (?:tú \(canción|pienso en ti)']) + #última reforma
#lema(ur'[Aa]qu_é_llos_é') + #última reforma
lema(ur'_é_l (?:y|como|a|después|lo|la|con)_e', pre=ur'(?:[Aa]|[Dd]e|[Ee]n) ') + #1
lema(ur'_é_l,_e', pre=ur'(?:[Aa]|[Dd]e|[Cc]on|[Ee]n|[Pp]or|[Hh]acia) ', xpos=[ur' (?:hasta|la, els|así|hoy|en ese|abarrotado|de q|también|entonces|por|ya desaparecido|hoy|relativamente)\b']) + #1
lema(ur'_é_l[.]_e', pre=ur'(?:[Aa]|[Dd]e|[Cc]on|[Ee]n|[Pp]or|[Hh]acia) ', xpos=[ur'\.\.', ]) + #266
lema(ur'_é_l[,]_e', pre=ur'(?:[Aa]|[Dd]e|[Cc]on|[Ee]n|[Pp]or|[Hh]acia) ', xpos=[ur' (?:este|ya|hoy|entonces|abarrotado|en ese|relativamente|ahora|por)', ]) + #261
lema(ur'_é_l[:]_e', pre=ur'(?:[Aa]|[Dd]e|[Cc]on|[Ee]n|[Pp]or|[Hh]acia) ', xpre=[ur'limita ', ]) + #12
lema(ur'_é_l[;]_e', pre=ur'(?:[Aa]|[Dd]e|[Cc]on|[Ee]n|[Pp]or|[Hh]acia) ', xpre=[ur'limita ', ]) + #9
lema(ur'_e_nero_E', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_f_ebrero_F', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_m_arzo_M', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_a_bril_A', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_m_ayo_M', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_j_unio_J', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_j_ulio_J', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ', xpos=[ur' (?:César|A\.)']) + #1
lema(ur'_a_gosto_A', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_s_eptiembre_S', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ', xpre=[ur'Liz ']) + #1
lema(ur'_o_ctubre_O', pre=ur'(?:(?<!12 )(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_n_oviembre_N', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur'_d_iciembre_D', pre=ur'(?:(?:[AaEe]l|lunes|martes|mi[eé]rcoles|vueves|viernes|s[aá]bado|domingo) [0-9]+|[Mm]es) de |[Ee]n ') + #1
lema(ur' *\[\[___ +') + #1
lema(ur' *\[\[[^|\]]*?_|__ +\|') + #1
#lema(ur' *\[\[[^|\]]*?_|__\| +', mostrar=True) + #1
[(u'(?P<l> *\[\[[^|\]]*?)\| +(?P<r>[^ \]])', u'\g<l>|\g<r>'), 
 (ur'(?P<ii>[=]+ *)(?:High [Ss]chool)(?P<dd> *[=])', ur'\g<ii>Escuela secundaria\g<dd>'),  
 (ur'\[\[(?:[Ii]ngl[eé]s \(pueblo\))\|', ur'[[pueblo inglés|'),
 (ur'\[\[(?:[Ii]ngl[eé]s \(idioma\))\|', ur'[[idioma inglés|'),
 (ur'\[\[ *([^\]|]+?) +([]|]+) *', ur'[[\1\2 '),
 (ur'\[\[ +([^\]|]+?)([]|]+)', ur'[[\1\2'),] + 
[]][0]

grupoPost = [#Sólo si hay otros cambios
[(ur'\[\[[Aa]([^\]|]*?)\|([Aa]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'), 
 (ur'\[\[[Bb]([^\]|]*?)\|([Bb]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Cc]([^\]|]*?)\|([Cc]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Dd]([^\]|]*?)\|([Dd]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Ee]([^\]|]*?)\|([Ee]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Ff]([^\]|]*?)\|([Ff]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Gg]([^\]|]*?)\|([Gg]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Hh]([^\]|]*?)\|([Hh]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Ii]([^\]|]*?)\|([Ii]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Jj]([^\]|]*?)\|([Jj]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Kk]([^\]|]*?)\|([Kk]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Ll]([^\]|]*?)\|([Ll]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Mm]([^\]|]*?)\|([Mm]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Nn]([^\]|]*?)\|([Nn]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Ññ]([^\]|]*?)\|([Ññ]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Oo]([^\]|]*?)\|([Oo]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Pp]([^\]|]*?)\|([Pp]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Qq]([^\]|]*?)\|([Qq]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Rr]([^\]|]*?)\|([Rr]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Ss]([^\]|]*?)\|([Ss]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Tt]([^\]|]*?)\|([Tt]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Uu]([^\]|]*?)\|([Uu]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Vv]([^\]|]*?)\|([Vv]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Ww]([^\]|]*?)\|([Ww]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Xx]([^\]|]*?)\|([Xx]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Yy]([^\]|]*?)\|([Yy]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'\[\[[Zz]([^\]|]*?)\|([Zz]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'), 
 (ur'\[\[[Áá]([^\]|]*?)\|([Áá]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'), 
 (ur'\[\[[Éé]([^\]|]*?)\|([Éé]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'), 
 (ur'\[\[[Íí]([^\]|]*?)\|([Íí]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'), 
 (ur'\[\[[Óó]([^\]|]*?)\|([Óó]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'), 
 (ur'\[\[[Úú]([^\]|]*?)\|([Úú]\1)([a-záéíóúñA-ZÁÉÍÓÚÑ]+)\]\]', ur'[[\2]]\3'),
 (ur'(\[\[[^][|]*?\|[^][|]*?)\]\]([a-z]+)', ur'\1\2]]'),
] +
[]][0]

grupo1FormatoLibre = [
[
 (ur'\[\[([Aa])(bstenci)[oó](n)\]\](es|istas?)', ur'[[A\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Aa])(cci)[oó](n)\]\](es|ari[ao]s?)', ur'[[A\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Aa])(dhesi)[oó](n)\]\](es)', ur'[[A\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Aa])(dministraci)[oó](n)\]\](es)', ur'[[A\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Aa])(fici)[oó](n)\]\](es|ad[ao]s?)', ur'[[A\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Aa])(nglosaj)[oó](n)\]\](es|ad[ao]s?)', ur'[[A\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Aa])(glomera)[oó](n)\]\](es)', ur'[[A\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Aa])(lgod)[oó](n)\]\](es|al|ales)', ur'[[A\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Aa])(luvi)[oó](n)\]\](es|al|ales)', ur'[[A\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Aa])(zerbaiy)[aá](n)\]\]([ao]s?)', ur'[[A\2á\3|\1\2a\3\4]]'),
 (ur'\[\[([Bb])(alc)[oó](n)\]\](es|ada)', ur'[[B\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Cc])(ant)[oó](n)\]\](es)', ur'[[C\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Cc])(entroam)[eé](rica)\]\](n[ao]s?)', ur'[[C\2é\3|\1\2e\3\4]]'),
 (ur'\[\[([Cc])(ircunnavegaci)[oó](n)\]\](es|al|ales)', ur'[[C\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Cc])(osmovisi)[oó](n)\]\](es)', ur'[[C\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Dd])(iapas)[oó](n)\]\](es)', ur'[[D\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Dd])(isertaci)[oó](n)\]\](es)', ur'[[D\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Dd])(ocumentaci)[oó](n)\]\](es)', ur'[[D\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Dd])(rag)[oó](n)\]\](es)', ur'[[D\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Ee])(squ)[ií]()\]\](es|ador(?:as?|es|))', ur'[[E\2í\3|\1\2i\3\4]]'),
 (ur'\[\[([Ff])(usi)[oó](n)\]\](es)', ur'[[F\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Hh])(ait)[ií]()\]\](an[ao]s?)', ur'[[H\2í\3|\1\2i\3\4]]'),
 (ur'\[\[([Hh])(ispanoam)[eé](rica)\]\](n[ao]s?)', ur'[[H\2é\3|\1\2e\3\4]]'),
 (ur'\[\[([Ii])(m)[aá](gen)\]\](es)', ur'[[I\2a\3|\1\2á\3\4]]'),
 (ur'\[\[([Ii])(ncrustaci)[oó](n)\]\](es)', ur'[[I\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Ii])(nundaci)[oó](n)\]\](es)', ur'[[I\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Jj])()[oó](ven)\]\](es)', ur'[[J\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Jj])(ap)[oó](n)\]\]([eé]s|es[ae]s?)', ur'[[J\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Jj])(urisdicci)[oó](n)\]\]([eé]s|al|ales)', ur'[[J\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Ll])(at)[ií](n)\]\]([ao]s?|izad[ao]s?)', ur'[[L\2í\3|\1\2i\3\4]]'),
 (ur'\[\[([Ll])(ap)[oó](n)\]\](es|as?)', ur'[[L\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Ll])(atinoam)[eé](rica)\]\](n[ao]s?)', ur'[[L\2é\3|\1\2e\3\4]]'),
 (ur'\[\[([Mm])(esoam)[eé](rica)\]\](n[ao]s?)', ur'[[M\2é\3|\1\2e\3\4]]'),
 (ur'\[\[([Mm])(oj)[oó](n)\]\](es)', ur'[[M\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Mm])(ont)[oó](n)\]\](es)', ur'[[M\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Mm])(usulm)[aá](n)\]\](es)', ur'[[M\2á\3|\1\2a\3\4]]'),
 (ur'\[\[([Nn])(eutr)[oó](n)\]\](es)', ur'[[N\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Nn])(orteam)[eé](rica)\]\](n[ao]s?)', ur'[[N\2é\3|\1\2e\3\4]]'),
 (ur'\[\[([Oo])(scilaci)[oó](n)\]\](es)', ur'[[O\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Pp])(e)[oó](n)\]\](es)', ur'[[P\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Pp])(erd)[oó](n)\]\](es)', ur'[[P\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Pp])(ez)[oó](n)\]\](es)', ur'[[P\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Pp])(oblaci)[oó](n)\]\](es|al|ales)', ur'[[P\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Pp])(ort)[oó](n)\]\](es)', ur'[[P\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Pp])(rofesi)[oó](n)\]\](es|al|ales|istas?|almente)', ur'[[P\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Pp])(rot)[oó](n)\]\](es)', ur'[[P\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Rr])(egi)[oó](n)\]\](es|al|ales)', ur'[[R\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Rr])(evoluci)[oó](n)\]\](es|ari[ao]s?)', ur'[[R\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Rr])(az)[oó](n)\]\](es|ad[ao]s?)', ur'[[R\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Ss])(al)[oó](n)\]\](es)', ur'[[S\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Ss])(axof)[oó](n)\]\](es|istas?)', ur'[[S\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Ss])(ubregi)[oó](n)\]\](es)', ur'[[S\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Ss])(udam)[eé](rica)\]\](n[ao]s?)', ur'[[S\2é\3|\1\2e\3\4]]'),
 (ur'\[\[([Tt])(ibur)[oó](n)\]\](es)', ur'[[T\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Tt])(romb)[oó](n)\]\](es|istas?)', ur'[[T\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Tt])(urr)[oó](n)\]\](es|er[ao]s?)', ur'[[T\2ó\3|\1\2o\3\4]]'),
 (ur'\[\[([Vv])(ol)[uú](men)\]\](es)', ur'[[V\2ú\3|\1\2u\3\4]]'),
] +
[(ur'< */ *(?P<a>[Bb][Rr]) *>', ur'<br />')] + #1
[(ur'(?P<ii>[=]+ *)(?P<tt>(?:Cabezas de Serie|Jugadores Destacados|Rondas Finales|Selección Nacional|Cuadro Inferior|Cuadro Superior|Enlaces Externos|Lista de Canciones))(?P<dd> *[=])', titulo),  
   (ur'(?P<ii>[=]+ *)(?P<tt>(?:Características Técnicas|Centros Comerciales|Centros de Salud|Cine y Televisión|Clasificación General|Como Productor|Cooperación Internacional|Cuadrangular Final|Cuarta Temporada|Disco Dos|Disco Uno|Edición Especial|El Edificio|Especificaciones Técnicas|Exposiciones Individuales|Fiesta Patronal|Formación Académica|Goleadores Históricos|Gran Final|Grupo Norte|Grupo Único|Historia Antigua|Instituciones Educativas|Mecanismo de Acción|Modo Batalla|Obras de Teatro|Otras Actividades|Otras Canciones|Otros Proyectos|Otros Trabajos|Partidos Internacionales|Posiciones en Liga|Premios Individuales|Premios y Distinciones|Primera Generación|Primera Parte|Quinta Temporada|Recepción de La crítica|Origen del Nombre|Referencias Bibliográficas|Segunda Generación|Segunda Parte|Su Obra|Vida Profesional|Álbum de Estudio|Álbumes Recopilatorios))(?P<dd> *[=])', titulo),  
(ur'(?P<ii>[=]+ *)(?P<tt>(?:Campeonatos Nacionales|Dobles Masculino|Fase Final|Fase de Grupos|Individual Masculino|Media Distancia|Premios y Nominaciones|Primera Ronda|Vida Personal))(?P<dd> *[=])', titulo),  
(ur'(?P<ii>[=]+ *)(?P<tt>(?:Banda Sonora|Campeonatos Internacionales|Campeonatos Mundiales|Carrera Profesional|Copa del Mundo|Cuadro Final|Cuartos de Final|Distinciones Individuales|Equipos Participantes|Lista de Episodios|Lista de Temas|Medios de Comunicación|Personajes Principales|Primera Fase|Primeros Años|Segunda Fase|Segunda Ronda|Series de Televisión|Series de Tv|Tabla de Posiciones|Tercer Lugar|Video Musical|Véase También|Álbumes de Estudio))(?P<dd> *[=])', titulo),
(ur'(?P<ii>[=]+ *)(?P<tt>(?:Aerolíneas y Destinos|Artistas Invitados|Carrera Musical|Carrera Política|Ciudades Hermanadas|Ciudades Hermanas|Como Entrenador|Como Jugador|Copas Internacionales|Cuadros Finales|Datos del Club|Dobles Femenino|Dobles Masculinos|Ficha Técnica|Fiestas Patronales|Flora y Fauna|Individuales Masculino|Individuales Masculinos|Información General|Larga Distancia|Listado de Canciones|Lugares de Interés|Medio Ambiente|Miembros Actuales|Notas y Referencias|Orden de Batalla|Organizaciones Multilaterales|Participaciones Internacionales|Personajes Ilustres|Personajes Recurrentes|Personajes Secundarios|Premios Especiales|Primera División|Primera Etapa|Primera Fecha|Primera Temporada|Puntos de Interés|Referencias Externas|Ronda Final|Ronda Preliminar|Récord Europeo|Segunda Fecha|Segunda Temporada|Tabla General|Tercera Fecha|Torneos Nacionales|Videos Musicales|Vídeo Musical|Zona Norte|Zona Residencial|Zona Sur))(?P<dd> *[=])', titulo),
(ur'(?P<ii>[=]+ *)(?P<tt>(?:Actividad Económica|Actividades Políticas|Antiguos Miembros|Ascensos y Descensos|Atractivos Turísticos|Barrios Servidos|Cabeza de Serie|Campeonato Mundial|Campeonato de Pilotos|Carrera Deportiva|Carrera Internacional|Carrera Militar|Clasificación Final|Clubes Afiliados|Composición del Distrito|Consejo de Administración|Cuadro Principal|Cuadro de Honor|Cuerpo Técnico|Cultura Popular|Destinos Internacionales|Destinos Nacionales|Distribución y Hábitat|División Administrativa|División Política|Dobles Femeninos|Ediciones Anteriores|Emisión Internacional|Enlace Externo|Entrenadores Destacados|Estrellas Invitadas|Evolución de la Clasificación|Exposiciones Colectivas|Exposiciones Personales|Finales de División|Formación Actual|Formato del Torneo|Galería de Imágenes|Goles en la Selección|Individual Femenino|Individuales Femenino|Individuales Femeninos|Infancia y Juventud|Junta Directiva|La Batalla|Liga Dominicana|Lista de Campeones|Lugares que Atraviesa|Medallero Total|Medallero por Género|Modos de Juego|Movimientos Divisionales|Máximos Goleadores|Músicos Invitados|Números Retirados|Octavos de Final|Otras Versiones|Otros Personajes|Otros Premios|Parte Alta|Parte Baja|Paso por Carrera Oficial|Poderes y Habilidades|Posiciones Finales|Prehistoria y edad Antigua|Premios Internacionales|Premios Nacionales|Premios y Reconocimientos|Presentación Previa|Programas de Tv|Recursos Naturales|Referencias Culturales|Reseña Histórica|Resultados Electorales|Roles Interpretados|Segunda División|Segunda Etapa|Semifinales de División|Servicios Ferroviarios|Servicios Públicos|Sistema de Competencia|Sitios de Interés|Sitios de Referencia|Tabla Acumulada|Temporada Regular|Tercera Ronda|Tercera Temporada|Territorio y Población|Torneos Internacionales|Trayectoria Política|Trayectoria Profesional|Trayectoria en TV|Ubicación Geográfica|Vialidad y Transporte|Vida Política|Vida Privada|Vida y Carrera|Vida y Obra|Vías de Comunicación|Vídeos Musicales))(?P<dd> *[=])', titulo),
 (ur'(?P<ii>[=]+ *)(?:Best [Aa]lbums)(?P<dd> *[=])', ur'\g<ii>Mejores álbumes\g<dd>'),  
 (ur'(?P<ii>[=]+ *)(?:Bonus [Tt]racks)(?P<dd> *[=])', ur'\g<ii>Pistas adicionales\g<dd>'),  
 (ur'(?P<ii>[=]+ *)(?:Track [Ll]isting)(?P<dd> *[=])', ur'\g<ii>Lista de canciones\g<dd>'),  
 (ur'(?P<ii>[=]+ *)(?:edad [Mm]oderna|Edad moderna)(?P<dd> *[=])', ur'\g<ii>Edad Moderna\g<dd>'),  
 (ur'(?P<ii>[=]+ *)(?:edad [Aa]ntigua|Edad Antigua)(?P<dd> *[=])', ur'\g<ii>Edad Antigua\g<dd>'),  
 (ur'(?P<ii>[=]+ *)(?:edad [Mm]edia|Edad media)(?P<dd> *[=])', ur'\g<ii>Edad Media\g<dd>'),  
 (ur'(?P<ii>[=]+ *)(?:edad [Cc]ontempor[áa]nea|Edad contempor[áa]mea|Edad Contemporanea)(?P<dd> *[=])', ur'\g<ii>Edad Contemporánea\g<dd>'),  
] + #1
#[(ur'¿ *(?:por *qu[eé]|Porqu[eé]|Por que)', ur'¿Por qué')] + #1
[]][0]

grupo1Frec = [#Los que corrijo en cada respaldo
lema(ur'[Ff]_ue__(?:ú[eé]|ué)') + #432
lema(ur'[Aa]_ú_n (?:más|menos|peor|mejor|están?|estaban?|no se|se|queda|hay|m[aá]s)_u') + #413
lema(ur'[Dd]i_o__ó') + #405
lema(ur'[Tt]_ambié_n_(?:ma?bi[eé]|ámbi[eé]|abi[eé]|ambi[eè]|ambí[eéè])') + #345
lema(ur'[Dd]_espué_s_(?:espue|epue|epué)') + #334
lema(ur'_ También__[Tt]ambi[eé]n', pre=ur'[-0-9a-záéúíóúüñA-ZÁÉÚÍÓÚÜÑ\]]+[\.;]') + #316
lema(ur'Jos_é_ (?:Alberto|Álvarez|García|Gómez|González|Jiménez|Martínez|Pérez|Ramírez|Rodríguez|Sánchez|Suárez|Vásquez)_e') + #185
lema(ur'[Vv]i_o_(?!\]\])_ó', xpre=[ur'El hombre que se ', ur'Nadie lo ', ur'[Vv]alle de ', ]) + #152
lema(ur'[Vv]_éase__(?:eas[eé]|eáse)') + #131
lema(ur'[Aa]dem_á_s_a') + #128
lema(ur'[d]em_á_s_a', xpre=[ur' el \'\'', ]) + #98
lema(ur'[Aa]lg_ú_n_u', xpos=[ur' (?:titella|lloc)', ]) + #87
lema(ur'_ Además__[Aa]dem[aá]s', pre=ur'[-0-9a-záéúíóúüñA-ZÁÉÚÍÓÚÜÑ\]]+[\.;]') + #84
lema(ur'[Cc]onstrucci_ó_n_o', xpos=[ur'\]\]es', ]) + #71
lema(ur'_ D_esde_[Dd]', pre=ur'[-0-9a-záéúíóúüñA-ZÁÉÚÍÓÚÜÑ\]]+[\.;]', xpre=[ur'\.\.', ]) + #66
lema(ur'_ Después__[Dd]espu[eé]s', pre=ur'[-0-9a-záéúíóúüñA-ZÁÉÚÍÓÚÜÑ\]]+[\.;]') + #66
lema(ur'[VvLl]_éase t_ambi[eé]n_(?:ea[sc][eé] [Tt]|éace t|eá[sc][eé] [tT])') + #58
lema(ur'_Enlaces externos_ *=_External [Ll]inks', pre=ur'= *') + #56
lema(ur'[Nn]ing_ú_n_u', xpos=[ur' (?:Yoru|poder no por kita|de Barberans)', ]) + #55
lema(ur'[Dd]etr_á_s_a') + #52
lema(ur'[Aa]tr_á_s_a', xpre=[ur'Rogla ', ], xpos=[ur' (?:Abante|d[ae] [Pp]orta)', ]) + #50
lema(ur'[Cc]onstitu_i_d[ao]s?_í') + #49
lema(ur'[Vv]ol_ú_menes_u') + #41
lema(ur'[Cc]onstru_i_d[ao]s?_í') + #38
lema(ur'[Ff]_á_cil_a') + #34
lema(ur'[Tt]odav_í_a_i') + #30
lema(ur'[Ff]_á_cilmente_a') + #29
lema(ur'Referenc_ia_s *=_e', pre=ur'= *') + #22
lema(ur'[Dd]esag_ü_es?_u') + #9
lema(ur'_hus_os? horarios?_(?:huz|[uú][sz])') + #7
lema(ur'[Tt]_ambié_n_ami[eé]', xpre=[ur'Santa Clara, ', ur'también ', ], xpos=[ur' (?:te quieru|i ai|la Virxen)', ur'(?:\||\'\' \(también)', ]) + #6
lema(ur'[Pp]os_ibili_dad(?:es)?_(?:bili|osibil|osibli)') + #3
lema(ur'[Cc]onstitu_i_r(?:l[aeo]s?|se|)_í') + #2
lema(ur'[Cc]onsig_uió__io') + #1
lema(ur'[Cc]onstrucci_o_nes_ó') + #1
#lema(ur'[Pp]_é_rdidas?_[eè]', pre=ur'(?:[Ss]in ) ') + #0
#lema(ur'[Hh]a_ll_a[ns]?_y', pre=ur'(?:se) ') + #1
#lema(ur'[Hh]a_ya__(?:llan?|yan)', pre=ur'(?:que|no) ') + #1
[]][0]

grupo1Mas = [
lema(ur'[Mm]_á_s (?:abajo|abundantes?|acorde|adelante|allá|amable?|amarg[ao]s?|amenazas?|ansiedad|arriba|basuras?|bien|bienes|breves?|brillantes?|cerca|comunes|común|confiables?|conservador(?:[ae]s|)|contenidos?|crucial(?:es|)|daños?|de (?:un[ao]?|dos|tres|diez|cien|mil)|del? [$0-9]+|destacables?|detalles?|dineros?|disparos?|efectos?|efica(?:z|ces)|empleos?|espacios?|frecuentes?|fuertes?|fuerzas?|gente|grandes?|graves?|hacia|hasta|hermos[ao]s?|horribles?|ilustres?importancia|importantes?|influyentes?|informaci(?:ón|ones)|inteligentes?|interesantes?|joven|jóvenes|lejos|lind[ao]s?|mel[oó]dic[ao]s?|memorables?|notables?|o menos|operables?|pero|personajes?|personas?|pobres?|pol[eé]mic[ao]s?|posterior|potentes?|probables?|producción|prominentes?|pronto|protagonismo|puntos?|relevantes?|remedios?|rentables?|resistentes?|saludables?|sensibles?|simples?|semejantes?|sexys?|simples?|sobre|tarde|tempran[ao]s?|territorios?|tiempos?|trascendentes?|usad[ao]s?|veces|velo(?:z|ces)|ventas?|viables?|votos?)\b_a') + #1159
lema(ur'[Mm]_á_s (?:aclamad|activ|adecuad|afectad|agresiv|agud|alejad|alt|anbugu|ampli|anch|angost|antigu|apropiad|asombros|atractiv|asidu|avanzad|baj|barat|bell|bonit|buscad|car|céntric|cercan|certer|chiflad|clar|c[oó]mic|c[oó]mod|complej|complet|complicad|concurrid|conocid|conservad|contaminad|cort|cotizad|creativ|crític|crud|cálid|cómod|delgad|derivad|desapercibid|desarrollad|descargad|destacad|detallad|difundid|distinguid|divertid|ecl[eé]ctic|ecológic|efectiv|elaborad|elevad|emblemátic|enfocad|escuchad|esperad|exclusiv|exitos|extendid|extens|extrañ|famos|fin|fr[ií]|generalizad|grandios|grues|hermos|húmed|inclusiv|influenciad|inmediat|intens|interesad|intern|[ií]ntim|larg|lauread|lejan|lent|liger|lind|limpi|list|llamativ|loc|lluvios|madur|malvad|masculin|met[óo]dic|modern|necesitad|numeros|odiad|ordinari|orientad|oscur|parecid|partid|pausad|pedid|peligros|pequeñ|pesad|poblad|poderos|practicad|preciad|precios|premiad|prestigios|profund|prolongad|pronunciad|próxim|psicodélic|pálid|pulid|pur|querid|r[aá]pid|reconocid|recordad|redond|reducid|relacionad|remot|renombrad|representativ|respetad|ric|rud|rudimentari|sagrad|segur|significativ|sofisticad|solicitad|sólid|sonad|seguid|seri|taquiller|tardí|temid|tont|transitad|transitori|usad|utilizad|valios|valorad|variad|vendid|viej|visitad|vist|viv|votad)[ao]s?_a') + #930
lema(ur'[m]_á_s_a', pre=ur'(?:[Aa]|[Aa]brir|afectar|agrava|[Aa]lgo|[Aa][uú]n|[Aa]preciar|[Cc]on|[Cc]rear|[Cc]uanto|[Dd]a|[Dd]elimitar|desarrolla[nrs]?|diferentes|[Dd]onde|[ee]s|[Ee]sta(?:ba|)|extendiéndose|hacer|[Ii]mpulsar|incrementado|[Mm]is?|mientras|[Mm]uch[ao]s?|[Nn]ada|[Nn]uestros?|ofendía[ns]?|[Pp]oco|proyectar|[Pp]areciéndose|[Pp]or|[Qq]u[eé]|[Ss]er|[Ss]ea|[Ss]iendo|[Ss]ino|[Ss]us?|tanto|tiene[ns]?|[Tt]odavía|[Tt]iempo|[Tt]rayendo|[Uu]n[ao]s?|[Uu]tiliza[ns]?|[Vv]eces|[Vv]er|[Vv]e[sz]) ') + #626
lema(ur'[m]_á_s de_a', xpre=[ur'7', ur'Não de costas ', ], xpos=[ur' (?:Rou|Chemnitz|Cadenet|Moulinas|Mierda|Fontmarie|Partirás|mill|pronto|Fondespierres|Bannière|la Carrasca|Saint|dozientos|pronto el|uma|ella no hay|la (?:Jasse|Cuca)|Méric|Raspall|l)\b', ]) + #348
lema(ur'[m]_á_s_a', pre=ur'(?:[Aa][uú]n|[Aa]lgo|[Aa]lguien|[Aa]lgunos?|[Aa]ños?|[Cc]ientos|[Cc]osas?|[Dd][eé]cadas?|[Dd]esarrollos|[Dd]ías?|[Dd]ur[oó]|[Ee]n|[Hh]oras?|[Mm]es(?:es|)|[Mm]iles|[Mm]illones|[Mm]inutos?|[Mm]uch[ao]s|[Nn]adie|[Nn]unca|[Oo]tr[ao]s?|[Pp]udo|[Ss]egundos?|[Vv]ari[ao]s|[Vv]eces|[Vv]ez|y) ', xpre=[ur'Caralt ', ur'Carreras ', ur'Cerní ', ur'Dijons ', ur'Givanel ', ur'Miguel ', ur'Rajoy ', ur'Zapatero ', ur'd’', ], xpos=[ur' (?:d|Sanz|Deu|Puigsec|Caucas|Crispí|Sauró|Graves|Boronat|Llombart|Altaba|Dorca|le|de (?:las Matas|Boeta|Vilanoveta|la Vila|Figuera|Flors|Fortuny|Bacanizas)|Fumàs|Bort|Films|Rampinyo|Usall|Génégals)\b', ur'[‘\']', ]) + #318
lema(ur'[m]_á_s_a', pre=ur'(?:[Ll]os?|y|[Ss]on) ') + #307
lema(ur'[Mm]_á_s (?:adult|alt|ambicios|básic|característic|clásic|competitiv|deportiv|desead|destructiv|electrónic|exitos|fresc|hablad|longev|lujos|negr|nominad|nuev|poblad|productiv|prolífic|prosper|rar|rocker|sangrient|técnic|vendid|violent)[ao]s?_a') + #231
lema(ur'[m]_á_s_a', pre=ur'[Ll]as? ', xpos=[ur' Cérbero', ]) + #172
lema(ur'[Mm]_á_s (?:abiert|activ|ampli|atractiv|cercan|clar|concrent|concret|confus|correct|dens|direct|e[sx]trech|económic|efectiv|específic|explícit|fidedign|fácil|hermos|h[uú]med|intens|just|larg|lent|minucios|net|ocupad|oportun|ordinari|precis|pront|propi|rápid|seri|sever|silencios|típic|verdader)(?:[ao]s?|amente|)_a') + #166
lema(ur'[Mm]_á_s (?:abrupt|abultad|aceptad|acertad|actualizad|antigu|apegad|apreciad|blanc|carismátic|celebrad|centrad|codiciad|colorid|compact|complet|consolidad|controvertid|costos|criticad|cuidad|distintiv|divers|emotiv|emplead|equipad|espacios|especializad|estrict|estudiad|exact|experimentad|expuest|frecuentad|glorios|icónic|innovador|junt|lógic|marcad|moderad|modest|montaños|negativ|organizad|orgánic|perfect|poderos|positiv|primitiv|propens|práctic|prósper|redondead|refinad|relajad|reproducid|riguros|robust|turístic|unid|vist|vistos|árid|ásper)[ao]s?_a') + #145
lema(ur'[Mm]_á_s que\b_a', xpre=[ur'Archivo ', ur'Carlos ', ], xpos=[ur' (?:nada|otr[ao]s?|tod[ao]s?|en|con|las?|los)', ur' (?:no|Sayago|finquen|doidice|bobo que eu)\b', ]) + #113
lema(ur'[m]_á_s_a', pre=ur'\b[Ee]l ', xpos=[ur' (?:al Montseny|era|Viaplana|Sobirà|Clarà|ha pasado|está|di|de (?:Vila|San|Méric|los Frailes|l|Raspall|la Cuca)|del (?:Quiquet|Canadell)|Borrull|Esquerra|Jordán|Miret|Soler|Bruguera)\b', ur'(?:’am|, el pagès)', ]) + #110
lema(ur'[Mm]_á_s_a', pre=ur'[Qq]ue ', xpos=[ur' (?:fue|i Fontdevila|colaboró|de Barberans)', ]) + #104
lema(ur'[m]_á_s_a', pre=ur'\b[Yy] ', xpre=[ur'Rajoy ', ]) + #98
lema(ur'[Mm]_á_s (?:amable|brutal|com[uú]n|constante|eficiente|esencial|especial|favorable|firme|formal|fácil|general|lineal|notable|particular|peculiar|popular|preponderante|probable|reciente|sexual|terminante|terrible|torpe|veloz)(?:mente|)_a') + #88
lema(ur'[Mm]_á_s (?:ágil|austral|cantidad|convencional|comercial|d[eé]bil|dif[ií]cil|error|fiel|f[aá]cil|funcionalidad|habitual|in[uú]til|meridional|oportunidad|oriental|poder|popular|radical|tradicional)(?:es|)_a') + #72
lema(ur'[m]_á_s_a', pre=ur'[Dd]e ', xpos=[ur' y Partners', ]) + #63
lema(ur'[Mm]_á_s (?:apar|atray|cali|coher|combati|concluy|congru|consist|contund|contund|conveni|convinc|corri|cruji|dec|desobedi|difer|elocu|evid|exig|fehaci|g|independi|inefici|influy|intelig|persist|perteneci|pot|pres|prevaleci|proced|promin|pudi|recurr|resist|rever|sobresali|solv|sorprend|sufici|supl|transpar|urg|vali|vig)entes?_a') + #56
lema(ur'[Mm]_á_s que (?:nada|otr[ao]s?|tod[ao]s?|en|con|las?|los)_a', xpos=[ur'\]', ]) + #37
lema(ur'[Mm]_á_s_a', pre=ur'\bo ', xpos=[ur' (?:Codorniu|Pinc|Dorca|de (?:Vilanova|Vilanoveta|Partirás|Marco)|Duran)', ]) + #28
lema(ur'[Mm]_á_s (?:su número|vidas?|c[aá]maras|ayuda|carros|[ée]xitos?|yardas|tiendo|[Ii]nformaci[oó]n)_a') + #25
lema(ur'[Mm]_á_s_a', pre=ur'[0-9$]+ ', xpre=[ur'actualmente de ', ], xpos=[ur' (?:sin|retorn[oó]|si)\b', ]) + #23
lema(ur'[m]_á_s_a', pre=ur'(?:[Ss]e (?:(?:acentúa|acerca|acoge|adapta|arreglaba|articula|asemeja|atiene|basa|centraba|centra|comenta|compara|concentra|construyese|convertiría|corre|cree|da|describe|describirá|dirige|discute|divide|ejecute|emitiese|emplea|encontraba|encuentra|enfocaba|exhiba|explica|expondrá|extiende|fecunda|habl[ae]|hace|hacía|haga|hallaba|halle|incluía|indica|instala|lleva|mantenía|mantiene|menciona|mezclaba|modifica|muestra|mueve|multiplica|necesita|necesitaría|organizaba|parece|permite|preocupa|presenta|produce|producía|prolonga|provee|publicaría|refiere|reflejaba|remonta|reparte|requerirá|sienta|sentía|tenía|tiene|trabaja|ubica|us[ae]|usará|utilizaba|utiliza|valora|ve|volvía|vuelve)n?)|acumuló|colgaron|consagraron|convirtió|demoró|desarrolló|difundió|dijo|establecieron|estudiaron|exportaron|fijó|hicieron|hizo|necesitó|plantaron|tornaron|vio|volvieron|volvió) ') + #22
lema(ur'[m]_á_s_a', pre=ur'[Nn]o(?: (?:agregar|apoyar|añade|causar|construir|contar|ejercería|encontrar|es|era|haber|huirán?|perder|rodar|ser|son|[Ee]s|ser[aá]|soportar|tienen?|tendrán?|trabajar|usar)|) ') + #21
lema(ur'[Mm]_á_s (?:adecuada|aguda|apropiada|concreta|cómoda|detallada|detenida|exacta|frecuente|fácil|infortunada|marcada|pesada|precisa|profunda|reciente|rápida|seguida|sólida)mente_a') + #15
lema(ur'[m]_á_s y\b_a') + #15
lema(ur'[m]_á_s_a', pre=ur'[Dd]el ', xpos=[ur' (?:d`en|Olmo|Cornell|de (?:l\'Artís|Marianet)|Esquerra)', ]) + #12
lema(ur'[Mm]_á_s (?:ganador|prometedor|tentador)(?:as?|es|)_a') + #11
lema(ur'[m]_á_s_a', pre=ur'[Aa]l ', xpos=[ur' se hace', ]) + #6
lema(ur'[Mm]_á_s ni_a', xpos=[ur' (?:sabes)', ]) + #5
lema(ur'[Mm]_á_s dur[ao]s?_a', xpos=[ur' que marmor', ]) + #4
lema(ur'[Mm]_á_s nunca_a', xpos=[ur' (?:abandones|daja)', ]) + #4
#lema(ur'[m]_á_s_a', pre=ur'[Aa]lgun[ao]s? ', xpos=[ur' no']) + #0
[]][0]

grupo1Esta = [
lema(ur'[Ee]st_á_ (?:proyect|public|radic|realiz|recalc|reclam|recopil|recost|redact|reflej|reforz|refreg|reg|regent|registr|regl|reglament|regul|rehabilit|rein|relacion|relaj|rellen|remarc|remat|remoj|remplaz|report|repres|represent|resguard|residenci|respald|retras|revis|revoc|rod|rode|rotul|sac|salpic|salv|seccion|secuestr|segment|seleccion|sell|sembr|sent|separ|sepult|señaliz|simboliz|sincroniz|situ|sobrecarg|sobregir|solicit|solt|sombre|soport|suaviz|subordin|supedit|superpobl|surc|tachon|tall|tap|tapiz|tas|tech|tematiz|termin|tipific|titul|tom|trab|trabaj|traumatiz|traves|traz|tumb|tutel|ubic|us|utiliz|valor|valu|ved|vigil|vincul|volc)ad[ao]_a') + #441
lema(ur'[Ee]st_á_ (?!cuando)[a-z]+(?:[ae]ndo|[aáeé]ndose(?:las?|les?|los?|))_a', xpre=[ur' (?:en|de) ', ur' a ', ur'por ', ]) + #395
lema(ur'[Ee]st_á_ (?:aboc|abraz|acab|aceler|achat|aclar|acompañ|acondicion|acopl|acost|acostumbr|acot|acredit|adapt|adorn|ados|afect|afili|afin|afinc|agot|agreg|agrup|agujere|ahuec|ajust|ali|aliment|aline|alist|almacen|almorz|aloj|alter|altern|amarr|ambient|amenaz|ameniz|ancl|angusti|anunci|apag|aparc|apart|aplan|aplast|aplic|apoy|aprob|aprovech|ar|arrend|arrop|arrug|asegur|asfalt|asign|asoci|asque|asust|atavi|aterr|aterroriz|atrap|atraves|audit|aument|autoedit|aval|avergonz|ayud|balance|bañ|bas|bloque|borde|calcul|calibr|calific|canaliz|cant)ad[ao]_a') + #312
lema(ur'[Ee]st_á_ (?:escenific|escolt|especializ|especific|esponsoriz|estacion|estandardiz|estim|estipul|estrope|estructur|estudi|estuf|excit|experiment|explic|explot|expres|expuls|extravi|fabric|facult|fascin|fatig|fech|fij|film|finaliz|financi|firm|flanque|flaque|form|formul|fortific|fragment|franque|frustr|fund|fundament|fusion|garantiz|gener|gestion|gobern|grab|gradu|guard|gui|habilit|habit|habl|hal|hechiz|herman|horroriz|hosped|ide|identific|ilumin|impact|implement|implic|imposibilit|impregn|imprim|impuls|imput|inclin|incorpor|indic|individualiz|inerv|infect|infest|influenci|inform|insert|inspir|instal|integr|intencion|intercomunic|interconect|interes|intern|interpret|inund|investig|invit|involucr|jubil|junt|justific|labr|lament|lanz)ad[ao]_a') + #312
lema(ur'[Ee]st_á_n_a', xpos=[ur' en bliau', ]) + #282
lema(ur'[Ee]st_á_ (?:abastec|absorb|aburr|adher|admit|agradec|arrepent|aturd|bendec|ced|ceñ|cog|compart|comprend|comprim|compromet|conceb|conduc|confund|conmov|constitu|constru|conten|convenc|convert|corromp|cos|defin|deprim|destitu|destru|deten|dilu|dirig|disminu|distribu|divid|dol|ejerc|embeb|embellec|enfurec|enloquec|enriquec|erig|escond|esculp|establec|exclu|exhib|flác|fortalec|hund|imbu|imped|inclu|induc|influ|interrump|invert|invest|malher|manten|met|obstru|omit|oscurec|permit|podr|preced|preestablec|prend|presid|produc|prohib|proteg|reclu|reg|repart|resent|restring|reun|revest|segu|sobreentend|somet|sorprend|sosten|subdivid|sumerg|sum|suprim|suspend|tej|tend|traduc|transmit|vend|vest)id[ao]_a', xpre=[ur'quedar ', ur'siendo ', ]) + #278
lema(ur'[Ee]st_á_ (?:casad|capacit|captur|caracteriz|carg|castig|cataliz|catalog|categoriz|cav|centr|cercen|cerr|certific|ciment|cincel|circund|circunval|clarific|clasificad|codific|colaps|colg|colmat|coloc|colore|comand|combin|compens|compil|compinch|complement|complet|comprob|comunic|concentr|concert|condicion|conect|confeccion|confi|configur|confin|confirm|conform|congel|consagr|conserv|consign|consolid|consum|contabiliz|cont|contamin|contempl|contraindic|contrat|control|convoc|coordin|cop|cre|cuarte|cur|curv|custodi|d|dat|debilit|declar|decor|dedic|deflact|delimit|deline|demand|demarc|deposit|derog|desaconsej|desacostumbr|desactiv|desactualiz|desafin|desanim|desarm|desarroll)ad[ao]_a') + #276
lema(ur'[Ee]st_á_ (?:abier|adscri|circunscri|compues|conten|descrip|descri|dispues|disuel|escri|exen|exhaus|expues|hambrien|har|incomple|incorrup|inscri|ocul|opues|predispues|prescri|provis|recubier|reple|resuel|ro|suel|suje|superpues|trascri)t[ao]_a') + #243
lema(ur'[Ee]st_á_ (?:desbloque|descans|desconect|descontinu|descuid|desdobl|desempeñ|desemple|desencant|desfas|deshabilit|deshabit|design|desinteres|desmay|despein|desproporcion|desterr|destin|destroz|desvel|desvi|devalu|devast|dibuj|dict|diseñ|disfraz|disgust|distanci|divorci|dobl|document|domin|dot|edific|edit|ejemplific|elimin|embals|embarc|emocion|emparent|empat|empeñ|emplaz|emple|enamor|encabez|encaden|encaj|encall|encamin|encant|encaprich|encarcel|encarg|encarn|encerr|enclav|encomend|encuadern|encuadr|endeud|energiz|enerv|enfad|enfatiz|enfoc|enfrent|enganch|englob|enlaz|enmarc|enmascar|enoj|enraiz|enred|enroll|enrosc|ensanch|ensangrent|enseñ|enter|enterr|entrelaz|entren|entub|entusiasm|envain|envenen|equip)ad[ao]_a') + #167
lema(ur'[Ee]st_á_ (?:lastim|laure|legisl|legitim|lesion|levant|liber|licenci|lider|limpi|list|llev|localiz|maltrat|manch|mand|manej|maniat|manifest|manipul|manufactur|maquill|mare|matrimoni|mediatiz|mezcl|model|modific|moj|molest|mont|motoriz|multiplic|mutil|nombr|nomin|normaliz|not|obsesion|ocult|oficializ|oper|optimiz|orden|organiz|orient|orl|ornament|pag|paraliz|parcel|patrocin|peg|pein|pele|pen|penaliz|penetr|pens|perne|personaliz|personific|pint|plag|plane|planific|plant|plante|plasm|pleg|pobl|posicion|potenci|predestin|predetermin|prend|prens|prepar|present|preserv|prob|program|promocion|propuls|protagoniz|provoc)ad[ao]_a') + #164
lema(ur'[Ee]st_á_ considerad[ao]_a', xpre=[ur'siendo ', ]) + #128
lema(ur'[Ee]st_á_ (?:list|partid|medid|propues|abandonad|administrad|alargad|autorizad|cruzad|vuelt|destacad|revuelt|llamad|cubiert|armad|parad|maldit|retirad|perdid|quebrad|limitad|conocid|crecid|extint|movid|acogid|unid|agitad|aislad|transformad|animad|arraig|asentad|atestad|atorment|forzad|herid|citad|buscad|complicad|ligad|condenad|marcad|motivad|ocupad|premiad|preocupad|coronad|cortad|cotizad|cuajad|previst|decidid|proporcionad|recogid|recomendad|reconocid|recuperad|reducid|referid|demostrad|denominad|desaparecid|desesperad|despedid|determinad|difundid|repetid|señalad|elaborad|embrujad|encubiert|entregad|envuelt|equilibrad|errad|esperad|expandid|extendid|tirad|aceptad|acusad|alejad|afilad|atribuid)o_a') + #121
lema(ur'[Ee]st_á_ (?:a(?: ?cargo| punto| [0-9,.]+[a-z]*)|arriba|abajo|debajo|dentro|encima|vac[ií][ao]|viv[ao])_a') + #105
lema(ur'[Ee]st_á_ muy_a', xpre=[ur'[Ss]iendo ', ur'incluía ', ur'ser ', ], xpos=[ur' (?:particular|alabada|polémica|pocas|apreciada|notable|dañada|limitada)', ]) + #62
lema(ur'[Ee]st_á_ al_a', xpre=[ur'\b[ay] ', ur'\bde ', ur'Andrea\. ', ur'Hunter ', ur'Tae, ', ur'[Pp]ero ', ur'además, ', ur'adopt[oó] ', ur'c[oó]mo ', ur'cambio ', ur'cayendo ', ur'con ', ur'contra ', ur'contrario, ', ur'convertirse ', ur'corre ', ur'correlaciona ', ur'de que ', ur'deben ', ur'directamente ', ur'directamente ', ur'dándosela ', ur'embargo, ', ur'entendiéndose', ur'entrando ', ur'llegando ', ur'pasando ', ur'pedir ', ur'por ', ur'sobre ', ur'subordinar ', ur'transmite ', ur'traslad[oó] ', ur'ubicada ', ], xpos=[ur' (?:ver|parecer)', ]) + #42
lema(ur'[Ee]st_á_ (?:aquí|allí|allá|acá)_a') + #22
lema(ur'[Ee]st_á_ mal_a', xpre=[ur' de ', ]) + #16
lema(ur'[Ee]st_á_ fuera del?_a', xpre=[ur'a ', ]) + #8
lema(ur'[Ee]st_á_ (?:distra|extra|pose|prove)íd[ao]_a') + #7
lema(ur'[Ee]st_á_ (?:él|ella)_a', xpre=[ur' (?:[Dd]e|[Ee]n) ', ]) + #5
lema(ur'[Ee]st_á_ embarazad[ao]_a', xpre=[ur'estando ', ]) + #5
lema(ur'[Ee]st_á_ pactad[ao]_a', xpos=[ur' solución', ]) + #1
lema(ur'[e]st_á__a', pre=ur'[Nn]o ', xpre=[ur'\b[yo] ', ur'precisamente ', ], xpos=[ur' (?:vez|Corte|noche)', ]) + #167
lema(ur'[e]st_á__a', pre=ur'(?:él|ella) ', xpre=[ur' (?:de|en) ', ur' a ', ur'[Cc]on ', ur'[Pp]ara ', ur'[Ss]egún ', ], xpos=[ur' noticia']) + #24
#lema(ur'[Ee]st_á_ bautizad[ao]_a', xpre=[ur'Siendo ', ]) + #0
[]][0]

grupo1Se = [
lema(ur'[Gg]ui_o__ó', xpos=[ur' mar\b', ]) + #471
lema(ur'[Ll]lev_ó__o', pre=ur'(?:[Ll][ao]s?|[Ee]llo|[Ee]sto|[Ss]e(?: me| te| l[aeo]s?|)) ', xpre=[ur'\b[Mm]e ', ur'amor ', ur'interior ', ur'tengo ', ], xpos=[ur' dentro', ]) + #331
lema(ur'[Jj]ug_ó_ (?:[0-9]+|un[ao]?|un[ao]s|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|varios)_o') + #216
lema(ur'[Jj]ug_ó__o', pre=ur'(?:[Qq]ui[ée]n|[Qq]u[ée]|[Dd][óo]nde|[Cc]u[áa]ndo|[Tt]ambién|[Aa]demás|[Ss]e|[Ll][ao]s?) ', xpos=[ur' de\b']) + #147
lema(ur'[Dd](?:amnific|at|añ|eambul|ebilit|ebit|ebut|ecalcific|ecant|ecapit|ecepcion|eclam|eclin|ecodific|ecor|ecortic|ecret|efec|efoli|eform|efraud|egener|egrad|egust|eific|elat|eleit|elimit|eline|emand|emarc|emor|enomin|enot|ensific|ent|enunci|epar|eport|eposit|eprec|epreci|eriv|erram|errib|erroc|errot|errubi|errumb|esaceler|esacidific|esaconsej|esacopl|esacredit|esactiv|esafi|esagrad|esagravi|esagrup|esahuci|esanim|esaparc|esaplic|esapropi|esaprovech|esarm|esarroll|esarticul|esat|esatanc|esatasc|esatornill|esatranc|esayun|esbanc|esbarat|esbarranc|esbast|esbloque|esboc|esbord|escalcific|escalific|escambi|escans|escar|escarri|escarril|escart|escentr|escifr|esclasific|escoc|escodific|escojon|escoloc|esconect|esconfi|escontrol|esconvoc|escuid|esdas|esdeñ|esdobl|ese|esec|esech|esembarc|esemboc|esempac|esempeñ|esencaden|esenfoc|esenred|esenrosc|esenvain|esert|esertific|esestim|esfalc|esfil|esgaj|esgarr|esgraci|eshidrat|esign|esilusion|esintegr|esinteres|esintoxic|esli|eslind|eslumbr|esmantel|esmarc|esmay|esmemoriar|esmitific|esmont|esmoron|esnuc|esnud|espach|esparasit|espej|espeluc|espen|espendol|esperdici|esplom|espoj|espos|espotric|espreci|espreocup|esprestigi|espunt|esquici|estac|estap|estin|estron|esubic|esvari|esvel|esvi|esvincul|etall|etect|eterior|etermin|eton|evast|evor|iagnostic|iagram|ibuj|ict|ictamin|iezm|iferenci|ificult|ign|ignific|ilat|iligenci|iluvi|iplom|isc|iscrep|iscrimin|isculp|isec|isemin|isert|iseñ|isfrut|isgust|isip|isloc|isoci|ispens|ispers|isput|istanci|istorsion|iversific|ivis|ivorci|obl|octor|ocument|omestic|omicili|omin|on|osific|ot|ren|ud|ulcific|uplic|ur)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #176
lema(ur'[Ee](?:ch|clips|dific|dit|duc|fectu|gres|jecut|jemplific|jercit|labor|lectrific|limin|logi|lucid|man|mancip|mbalsam|mbanc|mbarc|mbarranc|mbauc|mbelec|mbeles|mboc|mbols|mborrach|mborrasc|mbosc|mbroc|mbronc|migr|mocion|mpac|mpan|mpap|mpapuci|mparej|mpat|mpecin|mpeor|mperic|mpeñ|mple|mpuj|mpuñ|mul|najen|namor|namoric|narbol|narc|ncaden|ncaj|ncall|ncamin|ncan|ncant|ncar|ncarcel|ncariñ|ncarn|ncharc|ncomi|ncorv|ncuadr|ncumbr|ndemoni|ndeud|ndos|nemist|nfad|nferm|nfil|nfoc|nfosc|nfrasc|nfrent|nfri|nganch|ngañ|ngendr|nglob|ngrip|njuici|nlist|nmarc|nnoviar|noj|nrabi|nranci|nred|nroc|nrol|nrosc|nsambl|nsanch|nsay|nseñ|nsimism|nsuci|ntabl|nter|ntibi|nton|ntr|ntrañ|ntrechoc|ntren|ntresac|ntrevist|ntronc|nturbi|ntusiasm|numer|nunci|nvenen|nvi|nvici|nvidi|nviud|quilibr|quip|quipar|quivoc|rosion|rradic|ruct|scal|scalofri|scamp|scanci|scane|scap|scaque|scarific|scatim|scenific|scoli|scolt|scori|scuch|scudriñ|sfum|smer|spaci|spant|sparranc|specific|specul|sper|spet|spi|spole|spoli|sput|squi|squiv|stacion|staf|stall|stamp|stanc|statific|stereotip|stim|stimul|stipul|stir|stoque|storb|strangul|stratific|strech|strell|stren|stres|stri|strope|structur|struj|stuc|studi|tiquet|vapor|videnci|vit|voc|volucion|xacerb|xager|xalt|xamin|xcav|xcit|xclam|xcori|xcus|xfoli|xhort|xhum|xili|ximi|xoner|xpatri|xpendi|xperiment|xpi|xpir|xplor|xplot|xpoli|xport|xpres|xpropi|xpuls|xtasi|xtermin|xtravi|xtrañ|yect)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #162
lema(ur'[Ll]lev_ó a c_abo_(?:o a ?c|ó ac)', xpre=[ur'[Hh]oy ', ]) + #160
lema(ur'[Cc](?:abece|able|ablegrafi|aduc|al|alc|alcific|alcografi|alcul|alific|aligrafi|all|alm|alumni|amin|amufl|ancel|anje|ans|ant|ap|apacit|apisc|apitane|apitul|apt|asc|astr|atapult|aus|autiv|av|eb|ej|en|ens|ensur|entr|entuplic|erc|ercen|err|ertific|es|hamusc|hanc|hasc|hate|heque|hirri|hiv|hoc|horre|hurrusc|i|ifr|iment|ircul|isc|it|lam|larific|laudic|lausur|lav|oadyuv|obij|obr|ocin|odici|odific|ofund|olabor|olaps|oleccion|olect|olegi|olision|olm|olore|olumpi|omand|ombin|oment|omerci|omi|omision|ompagin|ompar|ompendi|ompenetr|ompens|ompil|omplement|omplet|omplic|omport|ompr|omprob|omput|omunic|oncentr|oncert|oncienci|oncit|oncret|onculc|oncurs|ondecor|onden|ondicion|ondon|onect|onfeccion|onferenci|onfes|onfi|onfigur|onfin|onfirm|onfisc|onform|onfront|ongel|ongeni|ongraci|onjetur|onjur|onllev|onmemor|onmin|onmocion|onmut|onquist|onsagr|onserv|onsider|onsign|onsolid|onspir|onst|onstat|onstip|onsult|onsum|ontact|ontagi|ontamin|ontempl|ontent|ontest|ontraatac|ontraindic|ontrari|ontrarrest|ontrast|ontrat|ontrol|onvalid|onvers|onvoc|ooper|oordin|op|opi|oquete|oron|orrete|orrobor|ort|ortej|osc|osech|osific|oste|otej|re|ritic|ronometr|rucific|uadriplic|uadruplic|uaj|ualific|uantific|ubic|uchiche|uestion|uid|ulmin|ulp|ultiv|ur|urr|urs|ustodi)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #139
lema(ur'[Cc]onstruy_ó__o', xpos=[ur' sobre Dios']) + #100
lema(ur'[Ii](?:de|dentific|gnor|gual|lumin|lustr|magin|mbric|mit|mpact|mper|mpetr|mplant|mplement|mplic|mplor|mport|mposibilit|mpost|mprec|mpregn|mpresion|mprovis|mpugn|mpuls|mpurific|mput|ncapacit|ncaut|ncendi|ncentiv|ncit|nclin|ncomunic|ncordi|ncrement|ncrep|ncrust|ncub|nculc|ncursion|ndic|ndigest|ndign|ndult|nfect|nfiltr|nfluenci|nform|nfundi|ngeni|nhabilit|nici|njuri|nmigr|nnov|nquiet|nsert|nsinu|nspeccion|nspir|nst|nstal|nstaur|nstrument|nsult|ntegr|ntensific|ntent|ntercal|ntercambi|ntercept|ntercomunic|nterconect|nteres|ntermedi|ntern|nterpel|nterpret|ntitul|ntoxic|ntrinc|nund|nvalid|nvent|nventari|nvit|nvoc|nvolucr|nyect|rradi|rrit)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #90
lema(ur'[Ll]lam_ó__o', pre=ur'(?:[Qq]ui[ée]n|[Qq]u[ée]|[Dd][óo]nde|[Cc]u[áa]ndo|[Tt]ambién|[Aa]demás|[Ss]e|[Ll][ao]s?|e) ', xpre=[ur'"', ur'\'\'', ur'Desde ', ur'Yo ', ur'esto ', ]) + #89
lema(ur'[Aa](?:bandon|banic|barc|barranc|bdic|bjur|bland|boc|bofete|bon|bord|borrasc|bort|boton|brev|brevi|bronc|bult|bund|bus|camp|capar|carici|carre|cat|caudill|ccident|cech|celer|cept|cerc|chac|chic|cidific|clam|clar|climat|comod|compañ|condicion|congoj|consej|copi|copl|corral|cort|cos|costumbr|cot|credit|ctiv|cuci|cultur|cumul|cun|curruc|cus|cuñ|dapt|delant|dentr|dicion|diestr|divin|djudic|djunt|dministr|dmir|dopt|dor|dorn|dos|dueñ|fect|ferr|ficion|fiebr|fili|finc|firm|floj|flor|front|garr|gasaj|genci|git|glutin|gobi|got|graci|grad|grand|grav|gravi|greg|gremi|gri|grup|guant|gusan|hond|horc|horr|huec|hues|huyent|just|justici|lab|lambic|larde|larm|lborot|legr|lej|lert|li|liger|liment|line|list|list|livi|llan|lmacen|loj|lquil|lter|lterc|ltern|lumbr|m|maestr|mamant|mas|mañ|mbicion|mbient|medrent|merit|mnisti|modorr|mold|monest|monton|mosc|motin|mpar|mplific|mput|muebl|ncl|nestesi|nex|nexion|ngusti|nhel|nid|nill|nim|niquil|nonad|nsi|nticip|ntoj|nul|padrin|palanc|parc|pare|part|pasion|pel|penc|piad|piñ|plac|plan|plast|plic|poc|pod|poder|port|postat|poy|preci|premi|pres|prest|presur|prision|propi|provech|proxim|punt|puñal|r|rañ|rbitr|rchiv|rgument|rm|rque|rranc|rras|rrasc|rrastr|rre|rrebat|rreci|rregl|rrejunt|rrellan|rrest|rri|rrib|rrincon|rrodill|rroj|rroll|rruin|rticul|s|salari|salt|se|sedi|segur|semej|sesin|sesor|sest|sever|sfixi|sign|simil|soci|som|sombr|spir|sust|t|tac|taj|tasc|tavi|tent|test|tin|torment|trac|tragant|tranc|trap|tras|trinc|trincher|trofi|tropell|udicion|udit|ugur|ument|usent|uspici|utentic|utentific|utodenomin|utonombr|utoproclam|uxili|val|ventaj|ventur|veri|vi|vis|vist|viv|voc|yud|zot)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #86
lema(ur'[Rr]ecibi_ó__o') + #83
lema(ur'[Ff]inaliz_ó__o') + #77
lema(ur'[Rr](?:abi|adi|adic|adiografi|amific|anci|apt|arific|asc|asguñ|astre|atific|ay|azon|eaccion|eacondicion|eactiv|eafirm|eagrup|eanim|eanud|earm|easign|eaviv|ebaj|eban|ebas|ebautiz|ebel|ebot|ebusc|ecab|ecal|ecalc|ecalific|ecambi|ecaptur|ecaud|ecicl|ecit|eclam|eclut|ecobr|ecolect|ecoloc|ecombin|ecompens|econcili|econquist|econsider|ecopil|ecort|ecre|ecri|ecrimin|ectific|ecul|ecuper|edact|edireccion|ediseñ|edobl|edonde|edund|eduplic|eedific|eedit|eeduc|eelabor|eembarc|eencarn|eentr|eenvi|eestren|eestructur|eferenci|efin|eflej|eflexion|eform|eformul|efrend|efresc|efugi|efund|efut|egal|egañ|egent|egistr|eglament|egrab|egres|egul|ehabilit|ein|einaugur|eincorpor|eingres|einstal|einstaur|eintegr|einterpret|einvent|eiter|eivindic|elacion|elaj|elampague|elat|elev|ellen|emarc|emat|emed|emedi|ememor|emezcl|emodel|emolc|emont|enombr|enov|enunci|eorden|eorient|epar|epas|epatri|epesc|epic|eplante|eplic|eport|epos|epresent|eproch|eprogram|epudi|equis|esabi|esalt|esbal|escat|esec|eserv|eseñ|esfri|esguard|esign|espald|espet|est|estaur|esucit|esult|et|etard|etoc|etom|etorn|etract|etras|etrat|etruc|eubic|eunific|evalid|evel|everenci|evindic|evis|evivific|evoc|evolucion|igi|ob|oci|od|ode|onc|ond|ot|ubric|umi|umore)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #70
lema(ur'[Ss]urgi_ó__o') + #69
lema(ur'[Pp]articip_ó__o', pre=ur'(?:[Qq]ui[ée]n|[Qq]u[ée]|[Dd][óo]nde|[Cc]u[áa]ndo|[Tt]ambién|[Aa]demás|[Ss]e|[Ll][ao]s?|[Nn]o) ') + #68
lema(ur'[Dd]ebut_ó__o') + #62
lema(ur'[Dd]errot_ó__o') + #62
lema(ur'[Pp]erdi_ó__o') + #61
lema(ur'[Ff](?:abric|acilit|actur|acult|aj|all|alsific|alt|antase|ascin|astidi|ech|elicit|eri|estej|estone|ich|igur|ili|ilm|ilosof|iltr|inanci|irm|lame|let|lot|oli|oment|onde|orceje|orj|orm|ormate|ormul|ornic|orr|ortific|otocopi|otografi|racas|raccion|ractur|ragment|recuent|ren|ris|ructific|rustr|ulmin|uncion|und|undament|usil|usion)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #59
lema(ur'[Pp]rovoc_ó__o') + #53
lema(ur'[Cc]omp_itió__(?:eti[oó]|itio)') + #52
lema(ur'[Pp](?:acific|act|agin|ali|anific|ar|arafrase|arodi|arpade|articip|as|ase|atale|ate|atent|atin|atrocin|atrull|aviment|ec|edale|ein|el|ele|ellizc|enc|enetr|ens|ercat|erdon|erdur|eregrin|erfeccion|erfil|erjudic|ermut|ernoct|erpetr|erpetu|ersign|erson|ersonific|erturb|es|esc|etrific|ic|ifi|ill|ilot|inch|int|irar|irate|is|it|ivot|izc|lac|lagi|lanch|lane|lanific|lant|lante|lantific|lasm|lastific|latic|leite|onch|ontific|opul|orfi|ort|os|osesion|osibilit|osicion|ostul|otenci|ractic|reci|recipit|recis|redic|redomin|refabric|refij|regon|regunt|reludi|remi|reocup|repar|resagi|resenci|reserv|resion|rest|restigi|revaric|rim|rincipi|riv|rivilegi|roces|rocesion|rocre|rocur|rofes|rogram|rogres|rolifer|romedi|rometi|romocion|ronostic|ronunci|ropici|ropin|roporcion|ropugn|ropuls|rosific|rosper|rotest|rovoc|royect|ublic|ublicit|uj|uls|untu|urific)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #50
lema(ur'[Vv]olvi_ó__o') + #48
lema(ur'[Pp]rometi_ó__o', xpre=[ur'del \bel ', ur'elemento ', ], xpos=[ur'(?:, (?:[Tt]antalio|[Pp]olonio)| *\||\]\])', ]) + #47
lema(ur'[Tt]raslad_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #46
lema(ur'[Ff]alleci_ó__o') + #45
lema(ur'[Ii]nterpret_ó__o', pre=ur'(?:[Qq]ui[ée]n|[Qq]u[ée]|[Dd][óo]nde|[Cc]u[áa]ndo|[Tt]ambién|[Aa]demás|[Ss]e|[Ll][ao]s?|e) ') + #44
lema(ur'[Ii]naugur_ó__o') + #43
lema(ur'[Ss](?:abore|abote|ac|acarific|aci|ald|alific|almodi|alpic|alt|alte|alud|alv|an|ancion|ane|angr|antific|aponific|aque|ec|ecuenci|ecuestr|ecund|eleccion|ell|ent|entenci|epar|eptuplic|epult|esion|extuplic|eñal|ignific|ilb|ilenci|implific|imul|imultane|indic|iti|oborn|obrepas|ocav|ofistic|ofoc|olap|olidific|olt|olucion|olvent|onde|onsac|opes|opl|oport|orte|oslay|ospech|ubast|uberific|ubestim|ublev|ublim|ubordin|ubray|ubsan|ubsidi|ubstanci|ubtitul|ud|ugestion|uicid|ujet|um|umari|umi|uministr|uper|upervis|uplant|uplic|urc|uscit|ustanci|ustent|usurr)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #41
lema(ur'[Cc]onllev_ó__o') + #39
lema(ur'[Pp]rotagoniz_ó__o') + #38
lema(ur'[Ss]ucedi_ó__o') + #38
lema(ur'[Cc]onvirti_ó__o') + #35
lema(ur'[Ss]igui_ó__o') + #35
lema(ur'[Ll](?:abor|abr|ac|agrime|ament|astim|av|egisl|egitim|enific|entific|esion|ev|evant|evit|ib|iber|ibr|icenci|icit|ider|idi|ignific|ij|imit|impi|iquid|isi|ist|len|lor|o|ogr|ubric|ubrific|uch|uci)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #34
lema(ur'[Rr]euni_ó__o') + #31
lema(ur'[Ee]specializ_ó__o') + #29
lema(ur'[Dd]edic_ó__o', pre=ur'[Ss]e ') + #28
lema(ur'[Mm](?:ac|achac|achuc|adur|agnific|alcri|aleduc|alinterpret|alogr|altrat|anc|and|anduc|anej|anifest|aniobr|anipul|anufactur|aravill|arch|archit|are|argin|arin|arisc|artill|asacr|asc|asific|astic|asturb|at|atricul|atrimoni|e|ecanografi|edic|edit|ejor|el|ene|enospreci|ent|erc|erm|ezcl|igr|ilit|im|in|ini|ir|istific|itific|ixtific|odel|oder|odific|of|oj|olde|olest|olific|omific|ont|ortific|ostr|otiv|ult|ultiplic|urmur|usic|usti|ut|util)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #28
lema(ur'[Tt](?:abic|ach|al|all|ap|api|aquigrafi|ar|arare|ard|artamude|ecnific|elefone|elegrafi|eletransport|elevis|elone|empl|erci|ergivers|ermin|est|estific|estimoni|ibi|ild|ipific|ir|itube|oc|oler|om|onific|op|ore|orn|orpede|ortur|rab|rabaj|rabuc|rafic|raicion|ram|ramit|ransit|ransparent|ransport|ransubstanci|rape|rasform|rasnoch|raspas|rastabill|rastoc|rastorn|rat|rep|ribut|rinc|riplic|risc|ritur|riunf|rompic|ruc|runc|umb|ute)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #27
lema(ur'[Oo](?:bcec|bjet|bnubil|br|bsequi|bserv|bsesion|bstin|bvi|casion|cult|cup|di|fert|fici|fusc|je|lisc|lvid|nde|per|pin|probi|pt|r|rbit|rden|re|rient|rigin|rquest|s|scil|sific|stent|torg|vacion)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #26
lema(ur'[Qq](?:uebr|uebrant|ued|uej|uem|uerell|uintuplic|uit)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #26
lema(ur'[Aa]dapt_ó__o') + #25
lema(ur'[C]uric_ó__o') + #25
lema(ur'[Cc]omenz_ó__o') + #25
lema(ur'[Ll]anz_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #24
lema(ur'[Vv]enci_ó__o') + #24
lema(ur'[Ff]irm_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ', xpre=[ur'Te ', ]) + #23
lema(ur'[Aa]nunci_ó__o', pre=ur'(?:[Ss]e(?: me| te| l[aeo]s?|)|[Qq]ue) ') + #22
lema(ur'[Ff]orm_ó__o', pre=ur'(?:[Qq]ui[ée]n|[Qq]u[ée]|[Dd][óo]nde|[Cc]u[áa]ndo|[Tt]ambién|[Aa]demás|[Ss]e|[Ll][ao]s?|e) ') + #22
lema(ur'[Dd]estac_ó__o') + #21
lema(ur'[Rr]etir_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #20
lema(ur'[Tt]om_ó__o', pre=ur'\b(?:[Ll]a|[Yy]) ', xpre=[ur'Kagura ', ur'Mafuyu ', ur'Shannon ', ur'Terry ', ur'[Mm]e ', ur'tomo ', ], xpos=[ur' (?:[IVXLCDM]+|requerido|segundo|Takahashi|Yamanobe|Inoue|Vran|se ven|logró|tienen|[0-9]+)', ur'(?:, que|: [0-9]+|: [IVXLCDM]+)', ]) + #20
lema(ur'[Aa]pareci_ó__o') + #19
lema(ur'[Ss]ufri_ó__o') + #19
lema(ur'[Ll]ogr_ó__o', pre=ur'(?:[Ll][eo]|[Ss]e(?: me| te| l[aeo]s?|)) ', xpre=[ur'\by ', ]) + #18
lema(ur'[Cc]oloc_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ', xpre=[ur'Yo ', ], xpos=[ur' Films']) + #17
lema(ur'[Ff]ij_ó__o', pre=ur'(?:[Ss]e(?: l[aeo]s?|)|[Ll][aeo]s?) ', xpre=[ur' a ', ur' e[ns] ', ]) + #17
lema(ur'[Ii]ncluy_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)|que) ') + #17
lema(ur'[Oo]curri_ó__o') + #17
lema(ur'[Cc]ubri_ó__o') + #16
lema(ur'[Rr]ecord_ó__o') + #16
lema(ur'[Bb](?:abe|ail|aj|alance|albuce|anc|araj|as|ast|atall|ate|añ|eatific|ec|enefici|es|ifurc|iloc|iografi|isec|lanque|lasfem|loc|loque|oicote|ombarde|onific|orde|orr|osquej|ot|re|rill|rinc|rome|ronce|rot|uce|url)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #15
lema(ur'[Dd]estruy_ó__o') + #15
lema(ur'[Dd]irigi_ó__o') + #15
lema(ur'[Ii]mpidi_ó__o') + #15
lema(ur'[m]arc_ó__o', pre=ur'\b(?:[Ss]e(?: me| te| l[aeo]s?|)|[Ll]os?|y) ', xpos=[ur' de']) + #15
lema(ur'[Pp]ermiti_ó__o') + #15
lema(ur'[Pp]erteneci_ó__o') + #15
lema(ur'[Dd]ebi_ó__o') + #14
lema(ur'[Ii]nvolucr_ó__o', pre=ur'(?:[Ss]e(?: me| te| l[aeo]s?|)|[Qq]ue) ') + #14
lema(ur'[Ss]irvi_ó__o') + #14
lema(ur'[Aa]ñadi_ó__o') + #13
lema(ur'[Dd]escribi_ó__o') + #13
lema(ur'[Ee]xtendi_ó__o') + #13
lema(ur'[Ss]inti_ó__o') + #13
lema(ur'[Uu](?:ltim|nific|nt|s|surp)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #13
lema(ur'[Aa]bri_ó__o') + #12
lema(ur'[Aa]mpli_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ', xpos=[ur' del? ', ]) + #12
lema(ur'[Cc]ambi_ó__o', pre=ur'(?:[Ss]e(?: me| te| l[aeo]s?|)|[Nn]os) ') + #12
lema(ur'[Dd]esv_í_o_i', pre=ur'(?:[AaEe]l|[Uu]n|[Cc]ada|[Ll]igero|[Oo]tro|[Pp]rimer|[Dd]el?|[Mm]ismo) ') + #12
lema(ur'[Gg](?:alardon|angren|asific|ast|ener|ermin|est|estion|ir|lori|lorific|los|ole|olpe|radu|ranje|ratific|rit|uard|uerre|uill|uis|uiñ|ust)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #12
lema(ur'[Pp]obl_ó__o') + #12
lema(ur'[Tt]ransmiti_ó__o') + #12
lema(ur'[Ll]len_ó__o', pre=ur'(?:[Ll][aeo]s?|[Ss]e(?: me| te| l[aeo]s?|)) ', xpre=[ur'\'\'', ur'vacío y ', ], xpos=[ur' y lo vacío']) + #11
lema(ur'[Oo]ficializ_ó__o') + #11
lema(ur'[Rr]ecomend_ó__o') + #11
lema(ur'[Uu]ni_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ', xpos=[ur' (?:Steamship|Flag|Jack)', ]) + #11
lema(ur'[Uu]ni_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ', xpos=[ur' (?:Steamship|Flag|Jack)', ]) + #11
lema(ur'[Cc]elebr_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #10
lema(ur'[Cc]reci_ó__o') + #10
lema(ur'[Dd]espert_ó__o') + #10
lema(ur'[Ee]ntreg_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #10
lema(ur'[Aa]dquiri_ó__o') + #9
lema(ur'[Dd]emostr_ó__o') + #9
lema(ur'[Ee]mpat_ó__o') + #9
lema(ur'[Ee]xigi_ó__o') + #9
lema(ur'[Jj]odi_ó__o') + #9
lema(ur'[Pp]areci_ó__o') + #9
lema(ur'[Pp]as_ó__o', pre=ur'(?:[Tt]odo|[Nn]ada) ', xpos=[ur' se', ]) + #9
lema(ur'[Pp]rotegi_ó__o') + #9
lema(ur'[Rr]egres_ó__o', pre=ur'(?:[Ss]e(?: me| te| l[aeo]s?|)|[Qq]ue) ') + #9
lema(ur'[Rr]equiri_ó__o') + #9
lema(ur'[Rr]ompi_ó__o') + #9
lema(ur'[Ss]ubi_ó__o') + #9
lema(ur'[Aa]not_ó__o', pre=ur'(?:[Ss]e(?: me| te| l[aeo]s?|)|y) ') + #8
lema(ur'[Dd]ecapit_ó__o') + #8
lema(ur'[Dd]efini_ó__o') + #8
lema(ur'[Dd]espleg_ó__o') + #8
lema(ur'[Dd]espleg_ó__o') + #8
lema(ur'[Hh](?:abilit|abit|abl|all|amac|art|asti|el|ered|erman|erni|ibern|inc|ip|ipertrofi|ipotec|ocic|omenaje|onr|osped|osti|ueve|umidific|umill|usme)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #8
lema(ur'[Rr]ecogi_ó__o') + #8
lema(ur'[Uu]tiliz_ó__o', pre=ur'[Ss]e ') + #8
lema(ur'[Aa]prob_ó__o') + #7
lema(ur'[Aa]rrend_ó__o') + #7
lema(ur'[Cc]omprometi_ó__o') + #7
lema(ur'[Cc]umpli_ó__o') + #7
lema(ur'[Ii]ncorpor_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #7
lema(ur'[Mm]inti_ó__o') + #7
lema(ur'[Nn](?:ad|aj|arr|ecesit|egoci|evisc|idific|ombr|omin|oque|ot|otific|umer)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #7
lema(ur'[Oo]freci_ó__o') + #7
lema(ur'[Rr]ecorri_ó__o') + #7
lema(ur'[Vv]isti_ó__o') + #7
lema(ur'[Aa]ctu_ó__o') + #6
lema(ur'[Aa]prendi_ó__o') + #6
lema(ur'[Aa]sent_ó__o') + #6
lema(ur'[Aa]sumi_ó__o') + #6
lema(ur'[Dd]ifundi_ó__o') + #6
lema(ur'[Ee]stableci_ó__o') + #6
lema(ur'[Rr]esidi_ó__o') + #6
lema(ur'[Ss]uspendi_ó__o') + #6
lema(ur'[Vv](?:ac|aci|acil|alid|alor|anaglori|ari|aticin|el|endimi|ener|entisc|erane|erific|ers|ersific|ersion|et|iaj|ici|idri|igil|ilipendi|incul|indic|iol|iolent|ir|ision|isit|islumbr|itrific|ivific|olte|omit|ot|ulner)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #6
lema(ur'[Aa]cogi_ó__o') + #5
lema(ur'[Aa]llan_ó__o', xpre=[ur'me ', ]) + #5
lema(ur'[Cc]aptur_ó__o') + #5
lema(ur'[Cc]ogi_ó__o') + #5
lema(ur'[Cc]ompr_ó__o', pre=ur'(?:[Ll][eo]|[Ss]e(?: me| te| l[aeo]s?|)) ') + #5
lema(ur'[Cc]onsisti_ó__o') + #5
lema(ur'[Dd]esprendi_ó__o') + #5
lema(ur'[Dd]imiti_ó__o') + #5
lema(ur'[Dd]ispar_ó__o', pre=ur'(?:[Ss]e(?: me| te| l[aeo]s?|)|[LlMmTt]e|[Nn]os) ') + #5
lema(ur'[Ee]strell_ó__o', pre=ur'(?:[Ss]e(?: me| te| l[aeo]s?|)|y) ') + #5
lema(ur'[Gg]rab_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #5
lema(ur'[Ii]nterfiri_ó__o') + #5
lema(ur'[Jj](?:act|ade|ipi|iñ|ubil|unt|urament|ustific|ustipreci)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #5
lema(ur'[Pp]ermaneci_ó__o') + #5
lema(ur'[Pp]refiri_ó__o') + #5
lema(ur'[Qq]uit_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ', xpre=[ur'[Yy]o ', ]) + #5
lema(ur'[Rr]econstruy_ó__o') + #5
lema(ur'[Rr]escindi_ó__o') + #5
lema(ur'[Ss]ecuestr_ó__o', pre=ur'\b(?:[Ll]a) ', xpre=[ur'Antiextorsión ', ur'Extorsión ', ], xpos=[ur' (?:de (?:Sol|nativas)|por)\b', ]) + #5
lema(ur'[Ss]ometi_ó__o') + #5
lema(ur'[a]terr_ó__o') + #5
lema(ur'[Aa]dvirti_ó__o') + #4
lema(ur'[Cc]oncedi_ó__o') + #4
lema(ur'[Dd]esapareci_ó__o') + #4
lema(ur'[Dd]esconcert_ó__o', xpos=[ur'\'\'']) + #4
lema(ur'[Dd]evolvi_ó__o') + #4
lema(ur'[Ee]ludi_ó__o') + #4
lema(ur'[Ee]ncontr_ó__o', pre=ur'(?:[Ss]e(?: l[aeo]s?|)|[Ll][aeo]s?|[Dd]onde) ') + #4
lema(ur'[Ee]xisti_ó__o') + #4
lema(ur'[Mm]idi_ó__o') + #4
lema(ur'[Mm]ordi_ó__o') + #4
lema(ur'[Pp]lane_ó__o', pre=ur'(?:[Ss]e(?: me| te| l[aeo]s?|)|[Qq]ue) ') + #4
lema(ur'[Pp]romovi_ó__o') + #4
lema(ur'[Rr]econoci_ó__o') + #4
lema(ur'[Rr]epiti_ó__o') + #4
lema(ur'[Rr]eprob_ó__o') + #4
lema(ur'[Rr]espondi_ó__o') + #4
lema(ur'[Rr]indi_ó__o') + #4
lema(ur'[Ss]olicit_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #4
lema(ur'[Tt]itul_ó__o', pre=ur'(?:[Yy]a|[Ss]e)(?: me| te| l[aeo]s?|) ') + #4
lema(ur'[l]ami_ó__o') + #4
lema(ur'[Aa]basteci_ó__o') + #3
lema(ur'[Aa]cab_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ', xpre=[ur'[Mm]e ', ]) + #3
lema(ur'[Aa]ccedi_ó__o') + #3
lema(ur'[Aa]traves_ó__o') + #3
lema(ur'[Cc]olg_ó__o') + #3
lema(ur'[Cc]ombati_ó__o') + #3
lema(ur'[Cc]omparti_ó__o') + #3
lema(ur'[Dd]efendi_ó__o') + #3
lema(ur'[Dd]esalent_ó__o') + #3
lema(ur'[Dd]escendi_ó__o') + #3
lema(ur'[Dd]espidi_ó__o') + #3
lema(ur'[Dd]evalu_ó__o') + #3
lema(ur'[Dd]evalu_ó__o', pre=ur'[Ss]e ') + #3
lema(ur'[Ee]mprendi_ó__o') + #3
lema(ur'[Ee]nfureci_ó__o') + #3
lema(ur'[Ee]xpandi_ó__o') + #3
lema(ur'[Ee]xtingui_ó__o') + #3
lema(ur'[Ii]mparti_ó__o') + #3
lema(ur'[Pp]adeci_ó__o') + #3
lema(ur'[Pp]ersigui_ó__o') + #3
lema(ur'[Pp]rendi_ó__o') + #3
lema(ur'[Pp]retendi_ó__o') + #3
lema(ur'[Rr]econcomi_ó__o') + #3
lema(ur'[Rr]eforz_ó__o', xpre=[ur'Juan ', ], xpos=[ur' y su', ]) + #3
lema(ur'[Rr]evivi_ó__o') + #3
lema(ur'[Ss]ali_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #3
lema(ur'[Ss]uprimi_ó__o') + #3
lema(ur'[Tt]ranscurri_ó__o') + #3
lema(ur'[Tt]rasmiti_ó__o') + #3
lema(ur'[p]ublic_ó__o', pre=ur'y ', xpre=[ur'alumnos ', ur'cr[íi]tica ', ur'maestros ', ur'oral ', ur'privado ', ], xpos=[ur' (?:en general|presente)', ur'\)', ]) + #3
lema(ur'[Aa]bati_ó__o') + #2
lema(ur'[Aa]bsorbi_ó__o') + #2
lema(ur'[Aa]conteci_ó__o') + #2
lema(ur'[Aa]dmiti_ó__o') + #2
lema(ur'[Aa]marr_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #2
lema(ur'[Aa]plaudi_ó__o') + #2
lema(ur'[Aa]rremeti_ó__o') + #2
lema(ur'[Aa]sesin_ó__o', pre=ur'\b(?:[Ll][eo]as?) ', xpre=[ur'Bitch ', ur'amigo ', ur'corrupto ', ur'psicópata ', ur'violador ', ], xpos=[ur' (?:What|psicópata|serial)', ]) + #2
lema(ur'[Aa]trevi_ó__o') + #2
lema(ur'[Aa]zot_ó__o', pre=ur'(?:[Ss]e(?: me| te| l[aeo]s?|)|[Qq]ue) ') + #2
lema(ur'[Cc]oincidi_ó__o') + #2
lema(ur'[Cc]ompiti_ó__o') + #2
lema(ur'[Cc]onfundi_ó__o') + #2
lema(ur'[Cc]onsumi_ó__o') + #2
lema(ur'[Dd]eneg_ó__o') + #2
lema(ur'[Dd]epar_ó__o') + #2
lema(ur'[Dd]esaloj_ó__o', pre=ur'(?:[Ss]e(?: me| te| l[aeo]s?|)|[Ll][aeo]s?) ') + #2
lema(ur'[Dd]esconoci_ó__o') + #2
lema(ur'[Dd]esisti_ó__o') + #2
lema(ur'[Dd]esminti_ó__o') + #2
lema(ur'[Dd]urmi_ó__o', xpos=[ur' Quadrato', ]) + #2
lema(ur'[Ee]ncerr_ó__o') + #2
lema(ur'[Ee]ncomend_ó__o') + #2
lema(ur'[Ee]nloqueci_ó__o') + #2
lema(ur'[Ee]ntendi_ó__o') + #2
lema(ur'[Ee]valu_ó__o') + #2
lema(ur'[Ff]avoreci_ó__o') + #2
lema(ur'[Ff]ingi_ó__o') + #2
lema(ur'[Ff]undi_ó__o') + #2
lema(ur'[Ii]mprimi_ó__o') + #2
lema(ur'[Ii]ncumpli_ó__o') + #2
lema(ur'[Ii]nsinu_ó__o') + #2
lema(ur'[Ii]nsisti_ó__o') + #2
lema(ur'[Ii]nterrumpi_ó__o') + #2
lema(ur'[Ii]nvadi_ó__o') + #2
lema(ur'[Ii]nvirti_ó__o') + #2
lema(ur'[Ll]ey_ó__o') + #2
lema(ur'[Oo]miti_ó__o') + #2
lema(ur'[Pp]recedi_ó__o') + #2
lema(ur'[Pp]rocedi_ó__o') + #2
lema(ur'[Qq]uem_ó__o', pre=ur'\b(?:[Yy]|[Ss]e) ', xpos=[ur' por mis', ]) + #2
lema(ur'[Rr]eabri_ó__o') + #2
lema(ur'[Rr]eapareci_ó__o') + #2
lema(ur'[Rr]efiri_ó__o') + #2
lema(ur'[Rr]emovi_ó__o') + #2
lema(ur'[Rr]esisti_ó__o') + #2
lema(ur'[Rr]etransmiti_ó__o') + #2
lema(ur'[Rr]event_ó__o') + #2
lema(ur'[Rr]evirti_ó__o') + #2
lema(ur'[Ss]obrevivi_ó__o') + #2
lema(ur'[Ss]ucumbi_ó__o') + #2
lema(ur'[Ss]ugiri_ó__o') + #2
lema(ur'[Tt]emi_ó__o') + #2
lema(ur'[Tt]ransport_ó__o', pre=ur'\b[Ll]o ') + #2
lema(ur'[Vv]erti_ó__o') + #2
lema(ur'[Aa]borreci_ó__o') + #1
lema(ur'[Aa]burri_ó__o') + #1
lema(ur'[Aa]cost_ó__o') + #1
lema(ur'[Aa]cudi_ó__o') + #1
lema(ur'[Aa]dhiri_ó__o') + #1
lema(ur'[Aa]pret_ó__o') + #1
lema(ur'[Bb]lanqueci_ó__o') + #1
lema(ur'[Bb]rind_ó__o', pre=ur'(?:[Ss]e(?: me| te| l[aeo]s?|)|que) ') + #1
lema(ur'[Ca]ambi_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #1
lema(ur'[Cc]edi_ó__o') + #1
lema(ur'[Cc]oescribi_ó__o') + #1
lema(ur'[Cc]ometi_ó__o') + #1
lema(ur'[Cc]onmovi_ó__o') + #1
lema(ur'[Cc]onsinti_ó__o') + #1
lema(ur'[Cc]onstituy_ó__o', pre=ur'[Ss]e ') + #1
lema(ur'[Dd]ebati_ó__o') + #1
lema(ur'[Dd]eprimi_ó__o') + #1
lema(ur'[Dd]erriti_ó__o') + #1
lema(ur'[Dd]esenvolvi_ó__o') + #1
lema(ur'[Dd]esoll_ó__o') + #1
lema(ur'[Dd]esvaneci_ó__o') + #1
lema(ur'[Dd]iscurri_ó__o') + #1
lema(ur'[Dd]iscuti_ó__o') + #1
lema(ur'[Dd]istingui_ó__o') + #1
lema(ur'[Dd]isuadi_ó__o') + #1
lema(ur'[Ee]fectu_ó__o') + #1
lema(ur'[Ee]mparent_ó__o') + #1
lema(ur'[Ee]njuici_ó__o') + #1
lema(ur'[Ee]nnobleci_ó__o') + #1
lema(ur'[Ee]ntrometi_ó__o') + #1
lema(ur'[Ee]nvisti_ó__o') + #1
lema(ur'[Ee]scogi_ó__o') + #1
lema(ur'[Ee]scondi_ó__o') + #1
lema(ur'[Ee]sculpi_ó__o') + #1
lema(ur'[Ee]xcedi_ó__o') + #1
lema(ur'[Ff]inaliz_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #1
lema(ur'[Ii]nscribi_ó__o') + #1
lema(ur'[Ii]ntercedi_ó__o') + #1
lema(ur'[Ii]ntim_ó__o', pre=ur'(?:[Ll][aeo]s?|[Ss]e(?: me| te| l[aeo]s?|)) ') + #1
lema(ur'[Jj]ur_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ', xpos=[ur' padre', ur', Señoría', ]) + #1
lema(ur'[Mm]ereci_ó__o') + #1
lema(ur'[Nn]utri_ó__o') + #1
lema(ur'[Pp]endi_ó__o') + #1
lema(ur'[Pp]ercibi_ó__o') + #1
lema(ur'[Pp]osey_ó__o') + #1
lema(ur'[Pp]rescindi_ó__o') + #1
lema(ur'[Pp]resumi_ó__o') + #1
lema(ur'[Pp]rohibi_ó__o') + #1
lema(ur'[Pp]rovey_ó__o') + #1
lema(ur'[Rr]edimi_ó__o') + #1
lema(ur'[Rr]eescribi_ó__o') + #1
lema(ur'[Rr]emiti_ó__o') + #1
lema(ur'[Rr]enaci_ó__o') + #1
lema(ur'[Rr]eparti_ó__o') + #1
lema(ur'[Rr]esolvi_ó__o') + #1
lema(ur'[Rr]estableci_ó__o') + #1
lema(ur'[Rr]etrocedi_ó__o') + #1
lema(ur'[Rr]evisti_ó__o') + #1
lema(ur'[Rr]evolvi_ó__o') + #1
lema(ur'[Ss]acudi_ó__o') + #1
lema(ur'[Ss]embr_ó__o') + #1
lema(ur'[Ss]ocorri_ó__o') + #1
lema(ur'[Ss]orprendi_ó__o') + #1
lema(ur'[Ss]oterr_ó__o') + #1
lema(ur'[Tt]ransfiri_ó__o') + #1
lema(ur'[Tt]ravisti_ó__o') + #1
# lema(ur'[Aa]bsolvi_ó__o') + #0
# lema(ur'[Aa]caeci_ó__o') + #0
# lema(ur'[Aa]centu_ó__o') + #0
# lema(ur'[Aa]crecent_ó__o') + #0
# lema(ur'[Aa]creci_ó__o') + #0
# lema(ur'[Aa]doleci_ó__o') + #0
# lema(ur'[Aa]dormeci_ó__o') + #0
# lema(ur'[Aa]dscribi_ó__o') + #0
# lema(ur'[Aa]dsorbi_ó__o') + #0
# lema(ur'[Aa]fligi_ó__o') + #0
# lema(ur'[Aa]gradeci_ó__o') + #0
# lema(ur'[Aa]gredi_ó__o') + #0
# lema(ur'[Aa]hij_ó__o') + #0
# lema(ur'[Aa]ludi_ó__o') + #0
# lema(ur'[Aa]maneci_ó__o') + #0
# lema(ur'[Aa]nocheci_ó__o') + #0
# lema(ur'[Aa]ntecedi_ó__o') + #0
# lema(ur'[Aa]pacent_ó__o') + #0
# lema(ur'[Aa]peg_ó__o', pre=ur'[Ss]e ') + #0
# lema(ur'[Aa]percibi_ó__o') + #0
# lema(ur'[Aa]peteci_ó__o') + #0
# lema(ur'[Aa]plic_ó__o', pre=ur'\b(?:[Ll]a|[Yy]) ', xpos=[ur' en usos singulares', ]) + #0
# lema(ur'[Aa]prehendi_ó__o') + #0
# lema(ur'[Aa]rrepinti_ó__o') + #0
# lema(ur'[Aa]serr_ó__o') + #0
# lema(ur'[Aa]sinti_ó__o') + #0
# lema(ur'[Aa]sus_ó__o', pre=ur'(?:[Ss]e(?: me| te| l[aeo]s?|)|[Qq]ue) ') + #0
# lema(ur'[Aa]tardeci_ó__o') + #0
# lema(ur'[Aa]tendi_ó__o') + #0
# lema(ur'[Aa]terriz_ó__o', pre=ur'(?:[Ss]e(?: me| te| l[aeo]s?|)|[Qq]ue) ') + #0
# lema(ur'[Aa]turdi_ó__o') + #0
# lema(ur'[Aa]up_ó__o') + #0
# lema(ur'[Aa]utoabasteci_ó__o') + #0
# lema(ur'[Aa]utodisolvi_ó__o') + #0
# lema(ur'[Aa]vergonz_ó__o') + #0
# lema(ur'[Bb]eld_ó__o') + #0
# lema(ur'[Bb]landi_ó__o') + #0
# lema(ur'[Ca]olabor_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #0
# lema(ur'[Ca]ompr_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #0
# lema(ur'[Cc]arcomi_ó__o') + #0
# lema(ur'[Cc]areci_ó__o') + #0
# lema(ur'[Cc]erni_ó__o') + #0
# lema(ur'[Cc]ircunfiri_ó__o') + #0
# lema(ur'[Cc]ircunscribi_ó__o') + #0
# lema(ur'[Cc]oexisti_ó__o') + #0
# lema(ur'[Cc]omidi_ó__o') + #0
# lema(ur'[Cc]ompadeci_ó__o') + #0
# lema(ur'[Cc]ompareci_ó__o') + #0
# lema(ur'[Cc]ompeli_ó__o') + #0
# lema(ur'[Cc]omplaci_ó__o') + #0
# lema(ur'[Cc]omprendi_ó__o') + #0
# lema(ur'[Cc]oncibi_ó__o') + #0
# lema(ur'[Cc]oncurri_ó__o') + #0
# lema(ur'[Cc]ondescendi_ó__o') + #0
# lema(ur'[Cc]ondoli_ó__o') + #0
# lema(ur'[Cc]onfiri_ó__o') + #0
# lema(ur'[Cc]onsol_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #0
# lema(ur'[Cc]onvaleci_ó__o') + #0
# lema(ur'[Cc]orrespondi_ó__o') + #0
# lema(ur'[Cc]orrigi_ó__o') + #0
# lema(ur'[Cc]orrompi_ó__o') + #0
# lema(ur'[Cc]osi_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #0
# lema(ur'[Cc]ovenci_ó__o') + #0
# lema(ur'[Cc]undi_ó__o') + #0
# lema(ur'[Dd]ecreci_ó__o') + #0
# lema(ur'[Dd]emoli_ó__o') + #0
# lema(ur'[Dd]ependi_ó__o') + #0
# lema(ur'[Dd]erriv_ó__o', xpre=[ur'\bel ', ]) + #0
# lema(ur'[Dd]esabasteci_ó__o') + #0
# lema(ur'[Dd]esacert_ó__o') + #0
# lema(ur'[Dd]esagradeci_ó__o') + #0
# lema(ur'[Dd]esaprob_ó__o') + #0
# lema(ur'[Dd]esatendi_ó__o') + #0
# lema(ur'[Dd]esaterr_ó__o') + #0
# lema(ur'[Dd]escorri_ó__o') + #0
# lema(ur'[Dd]escosi_ó__o') + #0
# lema(ur'[Dd]esentendi_ó__o') + #0
# lema(ur'[Dd]esenterr_ó__o') + #0
# lema(ur'[Dd]esentumeci_ó__o') + #0
# lema(ur'[Dd]esfalleci_ó__o') + #0
# lema(ur'[Dd]esfavoreci_ó__o') + #0
# lema(ur'[Dd]esgobern_ó__o') + #0
# lema(ur'[Dd]esguarneci_ó__o') + #0
# lema(ur'[Dd]eshel_ó__o') + #0
# lema(ur'[Dd]esmembr_ó__o') + #0
# lema(ur'[Dd]esmereci_ó__o') + #0
# lema(ur'[Dd]esmidi_ó__o') + #0
# lema(ur'[Dd]esobedeci_ó__o') + #0
# lema(ur'[Dd]esoy_ó__o') + #0
# lema(ur'[Dd]esposey_ó__o') + #0
# lema(ur'[Dd]esprovey_ó__o') + #0
# lema(ur'[Dd]esteji_ó__o') + #0
# lema(ur'[Dd]esvi_ó__o', pre=ur'[Ss]e ') + #0
# lema(ur'[Dd]esvisti_ó__o') + #0
# lema(ur'[Dd]ifiri_ó__o') + #0
# lema(ur'[Dd]igiri_ó__o') + #0
# lema(ur'[Dd]irimi_ó__o') + #0
# lema(ur'[Dd]isinti_ó__o') + #0
# lema(ur'[Dd]isolvi_ó__o') + #0
# lema(ur'[Dd]istendi_ó__o') + #0
# lema(ur'[Dd]ivirti_ó__o') + #0
# lema(ur'[Ee]mbasteci_ó__o') + #0
# lema(ur'[Ee]mbebeci_ó__o') + #0
# lema(ur'[Ee]mbebi_ó__o') + #0
# lema(ur'[Ee]mbelleci_ó__o') + #0
# lema(ur'[Ee]mbisti_ó__o') + #0
# lema(ur'[Ee]mbraveci_ó__o') + #0
# lema(ur'[Ee]mbruteci_ó__o') + #0
# lema(ur'[Ee]mpalideci_ó__o') + #0
# lema(ur'[Ee]mpedr_ó__o') + #0
# lema(ur'[Ee]mpequeñeci_ó__o') + #0
# lema(ur'[Ee]mplasteci_ó__o') + #0
# lema(ur'[Ee]mpobreci_ó__o') + #0
# lema(ur'[Ee]nalteci_ó__o') + #0
# lema(ur'[Ee]nardeci_ó__o') + #0
# lema(ur'[Ee]ncalleci_ó__o') + #0
# lema(ur'[Ee]ncaneci_ó__o') + #0
# lema(ur'[Ee]ncareci_ó__o') + #0
# lema(ur'[Ee]ncay_ó__o') + #0
# lema(ur'[Ee]ncegueci_ó__o') + #0
# lema(ur'[Ee]ncendi_ó__o') + #0
# lema(ur'[Ee]ncubri_ó__o') + #0
# lema(ur'[Ee]ndureci_ó__o') + #0
# lema(ur'[Ee]nflaqueci_ó__o') + #0
# lema(ur'[Ee]ngrandeci_ó__o') + #0
# lema(ur'[Ee]nmel_ó__o') + #0
# lema(ur'[Ee]nmend_ó__o') + #0
# lema(ur'[Ee]nmoheci_ó__o') + #0
# lema(ur'[Ee]nmudeci_ó__o') + #0
# lema(ur'[Ee]nnegreci_ó__o') + #0
# lema(ur'[Ee]norgulleci_ó__o') + #0
# lema(ur'[Ee]nrareci_ó__o') + #0
# lema(ur'[Ee]nriqueci_ó__o') + #0
# lema(ur'[Ee]nrojeci_ó__o') + #0
# lema(ur'[Ee]nronqueci_ó__o') + #0
# lema(ur'[Ee]nsangrent_ó__o') + #0
# lema(ur'[Ee]nsoberbeci_ó__o') + #0
# lema(ur'[Ee]nsombreci_ó__o') + #0
# lema(ur'[Ee]nsordeci_ó__o') + #0
# lema(ur'[Ee]ntalleci_ó__o') + #0
# lema(ur'[Ee]nterneci_ó__o') + #0
# lema(ur'[Ee]ntonteci_ó__o') + #0
# lema(ur'[Ee]ntorpeci_ó__o') + #0
# lema(ur'[Ee]ntrecerr_ó__o') + #0
# lema(ur'[Ee]ntremeti_ó__o') + #0
# lema(ur'[Ee]ntreteji_ó__o') + #0
# lema(ur'[Ee]ntristeci_ó__o') + #0
# lema(ur'[Ee]ntumeci_ó__o') + #0
# lema(ur'[Ee]nvaneci_ó__o') + #0
# lema(ur'[Ee]nvejeci_ó__o') + #0
# lema(ur'[Ee]nvileci_ó__o') + #0
# lema(ur'[Ee]nvolvi_ó__o') + #0
# lema(ur'[Ee]scarment_ó__o') + #0
# lema(ur'[Ee]scarneci_ó__o') + #0
# lema(ur'[Ee]scindi_ó__o') + #0
# lema(ur'[Ee]sclareci_ó__o') + #0
# lema(ur'[Ee]scupi_ó__o') + #0
# lema(ur'[Ee]sgrimi_ó__o') + #0
# lema(ur'[Ee]splendi_ó__o') + #0
# lema(ur'[Ee]stremeci_ó__o') + #0
# lema(ur'[Ee]xhibi_ó__o') + #0
# lema(ur'[Ee]xpeli_ó__o') + #0
# lema(ur'[Ee]xpidi_ó__o') + #0
# lema(ur'[Ff]eneci_ó__o') + #0
# lema(ur'[Ff]ortaleci_ó__o') + #0
# lema(ur'[Ff]osforeci_ó__o') + #0
# lema(ur'[Ff]osforesci_ó__o') + #0
# lema(ur'[Gg]imi_ó__o') + #0
# lema(ur'[Gg]uareci_ó__o') + #0
# lema(ur'[Gg]uarneci_ó__o') + #0
# lema(ur'[Hh]inchi_ó__o') + #0
# lema(ur'[Hh]irvi_ó__o') + #0
# lema(ur'[Hh]umedeci_ó__o') + #0
# lema(ur'[Hh]undi_ó__o') + #0
# lema(ur'[Ii]mpeli_ó__o') + #0
# lema(ur'[Ii]ncidi_ó__o') + #0
# lema(ur'[Ii]ncurri_ó__o') + #0
# lema(ur'[Ii]nfiri_ó__o') + #0
# lema(ur'[Ii]ngiri_ó__o') + #0
# lema(ur'[Ii]nhibi_ó__o') + #0
# lema(ur'[Ii]njiri_ó__o') + #0
# lema(ur'[Ii]nvisti_ó__o') + #0
# lema(ur'[Ii]rrumpi_ó__o') + #0
# lema(ur'[Jj]jug_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #0
# lema(ur'[Jj]ur_ó__o', pre=ur'[Ss]e(?: me| te| l[ae]s?|los|) ') + #0
# lema(ur'[Ll]anguideci_ó__o') + #0
# lema(ur'[Mm]alcomi_ó__o') + #0
# lema(ur'[Mm]alentendi_ó__o') + #0
# lema(ur'[Mm]alhiri_ó__o') + #0
# lema(ur'[Mm]almeti_ó__o') + #0
# lema(ur'[Mm]alvendi_ó__o') + #0
# lema(ur'[Mm]asacr_ó__o', pre=ur'\b(?:[Ll]a|[Yy]) ') + #0
# lema(ur'[Mm]edi_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ', xpos=[ur' enterraban', ]) + #0
# lema(ur'[Mm]erend_ó__o') + #0
# lema(ur'[Nn]aufrag_ó__o', pre=ur'[Qq]ue ') + #0
# lema(ur'[Oo]bedeci_ó__o') + #0
# lema(ur'[Oo]bscureci_ó__o') + #0
# lema(ur'[Oo]fendi_ó__o') + #0
# lema(ur'[Oo]scureci_ó__o') + #0
# lema(ur'[Oo]xid_ó__o', pre=ur'[Ss]e ') + #0
# lema(ur'[Pp]alideci_ó__o') + #0
# lema(ur'[Pp]erfor_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #0
# lema(ur'[Pp]ersisti_ó__o') + #0
# lema(ur'[Pp]ersuadi_ó__o') + #0
# lema(ur'[Pp]ervirti_ó__o') + #0
# lema(ur'[Pp]ervivi_ó__o') + #0
# lema(ur'[Pp]recavi_ó__o') + #0
# lema(ur'[Pp]reconcibi_ó__o') + #0
# lema(ur'[Pp]redefini_ó__o') + #0
# lema(ur'[Pp]rescribi_ó__o') + #0
# lema(ur'[Pp]resinti_ó__o') + #0
# lema(ur'[Pp]revaleci_ó__o') + #0
# lema(ur'[Pp]ropendi_ó__o') + #0
# lema(ur'[Pp]roscribi_ó__o') + #0
# lema(ur'[Pp]rosigui_ó__o') + #0
# lema(ur'[Rr]eabsorbi_ó__o') + #0
# lema(ur'[Rr]easumi_ó__o') + #0
# lema(ur'[Rr]ebati_ó__o') + #0
# lema(ur'[Rr]eblandeci_ó__o') + #0
# lema(ur'[Rr]ecalent_ó__o') + #0
# lema(ur'[Rr]econvirti_ó__o') + #0
# lema(ur'[Rr]ecosi_ó__o') + #0
# lema(ur'[Rr]ecrudeci_ó__o') + #0
# lema(ur'[Rr]ecubri_ó__o') + #0
# lema(ur'[Rr]ecurri_ó__o') + #0
# lema(ur'[Rr]edefini_ó__o') + #0
# lema(ur'[Rr]edescubri_ó__o') + #0
# lema(ur'[Rr]edirigi_ó__o') + #0
# lema(ur'[Rr]eemprendi_ó__o') + #0
# lema(ur'[Rr]eestableci_ó__o') + #0
# lema(ur'[Rr]eexpidi_ó__o') + #0
# lema(ur'[Rr]eimprimi_ó__o') + #0
# lema(ur'[Rr]eincidi_ó__o') + #0
# lema(ur'[Rr]einvirti_ó__o') + #0
# lema(ur'[Rr]ejuveneci_ó__o') + #0
# lema(ur'[Rr]elami_ó__o') + #0
# lema(ur'[Rr]eley_ó__o') + #0
# lema(ur'[Rr]emeti_ó__o') + #0
# lema(ur'[Rr]emordi_ó__o') + #0
# lema(ur'[Rr]epeli_ó__o') + #0
# lema(ur'[Rr]epens_ó__o') + #0
# lema(ur'[Rr]epercuti_ó__o') + #0
# lema(ur'[Rr]epobl_ó__o') + #0
# lema(ur'[Rr]eprendi_ó__o') + #0
# lema(ur'[Rr]eprimi_ó__o') + #0
# lema(ur'[Rr]equebr_ó__o') + #0
# lema(ur'[Rr]esinti_ó__o') + #0
# lema(ur'[Rr]esplandeci_ó__o') + #0
# lema(ur'[Rr]estringi_ó__o') + #0
# lema(ur'[Rr]esumi_ó__o') + #0
# lema(ur'[Rr]etorci_ó__o') + #0
# lema(ur'[Rr]evendi_ó__o') + #0
# lema(ur'[Rr]everdeci_ó__o') + #0
# lema(ur'[Rr]evolc_ó__o') + #0
# lema(ur'[Rr]obusteci_ó__o') + #0
# lema(ur'[Ss]alpiment_ó__o') + #0
# lema(ur'[Ss]obrecalent_ó__o') + #0
# lema(ur'[Ss]obreentendi_ó__o') + #0
# lema(ur'[Ss]obreexcedi_ó__o') + #0
# lema(ur'[Ss]obrentendi_ó__o') + #0
# lema(ur'[Ss]obresali_ó__o') + #0
# lema(ur'[Ss]obresey_ó__o') + #0
# lema(ur'[Ss]obrexcedi_ó__o') + #0
# lema(ur'[Ss]ubarrend_ó__o') + #0
# lema(ur'[Ss]ubdividi_ó__o') + #0
# lema(ur'[Ss]ubsisti_ó__o') + #0
# lema(ur'[Ss]ubtendi_ó__o') + #0
# lema(ur'[Ss]ubvirti_ó__o') + #0
# lema(ur'[Ss]upli_ó__o') + #0
# lema(ur'[Ss]urti_ó__o') + #0
# lema(ur'[Ss]uscribi_ó__o') + #0
# lema(ur'[Tt]eji_ó__o') + #0
# lema(ur'[Tt]embl_ó__o') + #0
# lema(ur'[Tt]raicion_ó__o', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #0
# lema(ur'[Tt]ranscendi_ó__o') + #0
# lema(ur'[Tt]ranscribi_ó__o') + #0
# lema(ur'[Tt]rascendi_ó__o') + #0
# lema(ur'[Tt]rascurri_ó__o') + #0
# lema(ur'[Tt]rasfiri_ó__o') + #0
# lema(ur'[Uu]rdi_ó__o') + #0
# lema(ur'[Vv]erdeci_ó__o') + #0
# lema(ur'[Xx](?:erografi)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #0
# lema(ur'[Zz](?:af|anj|ap|arp|ozobr|urr)_ó__o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #0
# lema(ur'[Zz]ahiri_ó__o') + #0
[]][0]

grupo1Andos = [
lema(ur'[Mm]altrat_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Cc]onvirti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #69
lema(ur'[d]_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #46
lema(ur'[Hh]aci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #45
lema(ur'[Dd]ej_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #27
lema(ur'[Bb]as_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #23
lema(ur'[Rr]efiri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #20
lema(ur'[Dd]ici_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #18
lema(ur'[Ll]lev_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #18
lema(ur'[Aa]m_á_ndo(?:[mst]e|l[aeo]s|la|nos)(?:[mt]e|l[aeo]s?|nos|)_a', xpre=[ur'\bde ', ur'Pedro ', ]) + #17
lema(ur'[Gg]an_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #16
lema(ur'[Mm]anteni_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #15
lema(ur'[Aa]m_á_ndola_a', xpre=[ur'Pedro ', ], xpos=[ur'\]\]', ]) + #14
lema(ur'[Ll]lam_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #14
lema(ur'[Cc]oloc_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #13
lema(ur'[Pp]resent_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #13
lema(ur'[Rr]etir_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #12
lema(ur'[Dd]isput_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #11
lema(ur'[Ee]nfrent_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #11
lema(ur'[Pp]ermiti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #11
lema(ur'[Pp]osicion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #11
lema(ur'[Qq]ued_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #11
lema(ur'[Ii]ncorpor_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #10
lema(ur'[Mm]at_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #10
lema(ur'[Uu]ni_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #10
lema(ur'[Vv]i_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #10
lema(ur'[Dd]esarroll_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #9
lema(ur'[Dd]estac_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #9
lema(ur'[Uu]bic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #9
lema(ur'[Cc]onsider_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #8
lema(ur'[Gg]radu_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #8
lema(ur'[Hh]abi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #8
lema(ur'[Jj]ug_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #8
lema(ur'[Ll]anz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #8
lema(ur'[Mm]ir_á_ndo(?:[mst]e|las|l[eo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #8
lema(ur'[Vv]olvi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #8
lema(ur'[Cc]alific_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #7
lema(ur'[Cc]oron_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #7
lema(ur'[Dd]irigi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #7
lema(ur'[Ee]xpandi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #7
lema(ur'[Mm]ostr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #7
lema(ur'[Pp]oni_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #7
lema(ur'[Pp]roclam_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #7
lema(ur'[Tt]ransmiti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #7
lema(ur'[Aa]yud_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #6
lema(ur'[Cc]re_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #6
lema(ur'[Ff]orm_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #6
lema(ur'[Ii]ncluy_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #6
lema(ur'[Pp]idi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #6
lema(ur'[Ss]epar_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #6
lema(ur'[Ss]itu_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #6
lema(ur'[Bb]usc_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #5
lema(ur'[Cc]lasific_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #5
lema(ur'[Dd]efini_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #5
lema(ur'[Ee]miti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #5
lema(ur'[Hh]all_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #5
lema(ur'[Ii]nstal_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #5
lema(ur'[Rr]eemplaz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #5
lema(ur'[Aa]cerc_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Aa]ñadi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #4
lema(ur'[Cc]ambi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Cc]edi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #4
lema(ur'[Ee]ncontr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Ee]nfoc_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Ee]ngañ_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Ee]ntreg_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Ee]specializ_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Ee]stableci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #4
lema(ur'[Gg]olpe_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Ii]ntegr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Pp]repar_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Qq]uit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Ss]alv_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Tt]ir_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Tt]ransform_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #4
lema(ur'[Aa]bri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #3
lema(ur'[Aa]dapt_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Aa]sent_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Aa]tribuy_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #3
lema(ur'[Cc]ompar_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Cc]omunic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Cc]onoci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #3
lema(ur'[Cc]onsagr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Cc]onserv_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Cc]onstituy_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #3
lema(ur'[Cc]ort_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Cc]ost_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[D]_á_ndo(?:[mst]e|las?|les?|los|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Dd]edic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Dd]efendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #3
lema(ur'[Dd]enomin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Dd]evolvi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #3
lema(ur'[Ee]scondi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #3
lema(ur'[Ee]xplic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Ee]xtendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #3
lema(ur'[Mm]arc_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Nn]eg_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Nn]ombr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Oo]rganiz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Pp]as_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Pp]rovoc_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Pp]udi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #3
lema(ur'[Rr]educi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #3
lema(ur'[Rr]enombr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Rr]ob_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Tt]om_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Tt]raslad_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Tt]rat_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #3
lema(ur'[Aa]cus_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Aa]firm_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Aa]greg_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Aa]poder_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Aa]puñal_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Aa]rroj_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Bb]es_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Cc]aus_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Cc]omplet_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Cc]ompr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Cc]onform_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Cc]onsolid_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Dd]ispar_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Dd]ividi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #2
lema(ur'[Ee]stren_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Ff]usion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Gg]ener_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Ii]mpidi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #2
lema(ur'[Ii]mponi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #2
lema(ur'[Ll]ogr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Mm]ovi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #2
lema(ur'[Oo]blig_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Oo]bteni_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #2
lema(ur'[Pp]regunt_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Pp]rometi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #2
lema(ur'[Pp]ublic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Qq]uem_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Rr]ecuper_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Rr]egistr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Rr]evel_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Rr]indi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #2
lema(ur'[Rr]ode_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Rr]ompi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #2
lema(ur'[Ss]i_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #2
lema(ur'[Ss]igui_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #2
lema(ur'[Ss]irvi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #2
lema(ur'[Ss]um_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Ss]ustituy_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #2
lema(ur'[Tt]itul_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Tt]oc_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Uu]tiliz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #2
lema(ur'[Vv]ali_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #2
lema(ur'[Aa]bandon_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Aa]delant_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Aa]djudic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Aa]dvirti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Aa]nunci_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Aa]segur_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Aa]tac_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Bb]orr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Cc]as_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Cc]lav_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Cc]omparti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Cc]onfes_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Cc]ont_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Cc]uid_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Dd]errot_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Dd]espidi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Dd]estin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Dd]istribuy_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Ee]quip_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Ee]strell_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Ee]xigi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Ff]elicit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Hh]abl_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Ii]mplic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Ii]nclin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Ii]nscribi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Ll]i_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Mm]and_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Mm]odific_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Mm]olest_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Mm]ordi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Mm]ud_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Oo]di_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Pp]eg_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Pp]riv_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Rr]eport_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Rr]epresent_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Rr]euni_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Ss]alt_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Ss]ell_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Ss]inti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Ss]oterr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Ss]ubi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Tt]eni_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Vv]enci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Vv]eng_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
lema(ur'[Vv]isti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Yy]_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #1
lema(ur'[Aa]plic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #1
# lema(ur'[Aa]bati_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Aa]bofete_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]braz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]broch_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]bsorbi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Aa]cept_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]chac_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]consej_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]corral_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]cos_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]ctiv_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]ctualiz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]cuchill_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]decu_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]derez_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]dministr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]dopt_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]dorn_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]dquiri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Aa]dscribi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Aa]fect_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]feit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]garr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]grad_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]gradeci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Aa]grand_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]grup_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]guard_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]hog_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]isl_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]just_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]lert_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]li_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]line_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]loj_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]lter_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]ludi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Aa]lumbr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]lz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]mbient_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]menaz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]mordaz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]mpli_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]naliz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]nex_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]nim_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]ntecedi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Aa]nticip_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]pil_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]plast_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]plaudi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Aa]port_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]pret_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]provech_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]punt_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]rranc_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]rruin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]rtill_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]scendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Aa]sedi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]sesin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]sest_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]sfalt_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]sign_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]soci_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]t_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]tendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Aa]tropell_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]up_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]vergonz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Aa]vis_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Bb]arri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Bb]añ_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Bb]ombarde_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Bb]orde_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Bb]rind_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Bb]url_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]all_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]amufl_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]ant_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]aptur_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]aracteriz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]atalog_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]ategoriz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]ay_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]az_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]elebr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]erni_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]err_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]hill_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]ircund_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]it_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]lam_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]oci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]ombin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]oment_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]omprimi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]oncedi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]onden_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]ondescendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]onect_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]onfi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]onfiri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]onfirm_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]onllev_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]onmin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]onquist_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]onsigui_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]onsol_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]onsumi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]ontact_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]ontempl_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]ontendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]ontest_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]ontraponi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]onvenci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]oordin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]oquete_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]orrespondi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]orrompi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]oste_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]ri_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]ruz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]ubri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Cc]ulmin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]ulp_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Cc]ultiv_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]ebati_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]ebi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]ebilit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]ecapit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]eclar_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]ecor_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]eform_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]efosforil_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]eponi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]eposit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]eprimi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]erriti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]esacredit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esarm_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esat_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]escalabr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]escalific_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]escendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]escribi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]escubri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]escuid_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esdeñ_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esempeñ_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esencaj_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esentendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]esfigur_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esgarr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]eshaci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]esintegr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]eslig_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esmay_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esmembr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esotorg_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esparaliz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]espert_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esplaz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]espoj_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esposey_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]estaj_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esterr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]estroz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]estruy_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]esvi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]esvincul_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]eteni_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]etermin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]etest_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]evor_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]ifam_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]iferenci_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]isfraz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]isfrut_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]isminuy_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]isolvi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]ispens_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]istendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Dd]on_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_ta') + #0
# lema(ur'[Dd]op_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]ot_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Dd]uplic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]amor_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]ch_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]fectu_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]jerci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ee]lev_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]ligi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ee]limin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]logi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]mbaraz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]mpal_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]mpat_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]mpez_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]mpuj_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]namor_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]ncaj_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]ncarg_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]ncañon_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]ncegueci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ee]ncendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ee]ncerr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]ncomend_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]ncubri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ee]ndos_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]nfrasc_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]nganch_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]ngrandeci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ee]nlaz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]nmarc_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]nred_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]ntendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ee]nterr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]ntren_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]nturbi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]nvi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]quipar_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]rr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]scanci_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]scogi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ee]scuch_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]snif_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]sper_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]spi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]squi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]storb_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]stratific_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]strech_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]structur_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]studi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]vacu_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]vadi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ee]vit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]volucion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]xamin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]xceptu_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]xclam_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]xcluy_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ee]xhort_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]xponi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ee]xpres_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]xpuls_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ee]xtingui_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ff]abric_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ff]acilit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ff]inaliz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ff]ortaleci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ff]ractur_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ff]ragment_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ff]ranque_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ff]ri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ff]rot_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ff]rustr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ff]um_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Gg]arantiz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Gg]ast_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Gg]ole_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Gg]rab_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Gg]rit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Gg]uard_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Gg]uarneci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Gg]ust_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Hh]abit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Hh]aci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Hh]ered_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Hh]inch_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Hh]ipnotiz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Hh]irvi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Hh]ocic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Hh]umill_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Hh]uy_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ii]gnor_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]lumin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]lusion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]mparti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ii]mplant_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]mplement_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]mposibilit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]mpresion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]mprimi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ii]mpuls_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]nactiv_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]ncit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]ncrement_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]ndependiz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]ndic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]nfl_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]nfligi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ii]nform_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]ngiri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ii]nhal_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]nmoviliz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]nsinu_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]nst_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]ntercambi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]nterpret_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]nterrog_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]nterrumpi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ii]ntervini_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ii]ntim_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]ntitul_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]ntroduci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ii]nvent_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]nvestig_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]nvit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ii]nyect_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Jj]al_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Jj]ale_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Jj]ur_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ll]eg_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ll]esion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ll]evant_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ll]ey_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ll]ibert_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ll]ibr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ll]icenci_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ll]ig_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ll]imit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ll]leg_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ll]len_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ll]ocaliz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Mm]achac_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Mm]aldici_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Mm]alentendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Mm]alte_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Mm]anifest_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Mm]arch_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Mm]asacr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Mm]astic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Mm]eci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Mm]eti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Mm]inti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Mm]oderniz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Mm]olde_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Mm]ont_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Mm]util_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Nn]aci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Nn]ecesit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Nn]eutraliz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Nn]omin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Nn]oque_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Nn]ot_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Oo]bsequi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Oo]casion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Oo]cult_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Oo]cup_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Oo]freci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Oo]lvid_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Oo]rbit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Oo]rden_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Oo]rill_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Oo]torg_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Oo]xid_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Oo]y_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Pp]ag_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]arodi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]arti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Pp]ase_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]ate_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]atent_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]el_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_ea') + #0
# lema(ur'[Pp]erdi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Pp]erfeccion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]erfor_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]erjudic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]ersigui_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Pp]ic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]int_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]is_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]ort_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]recedi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Pp]remi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]rendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Pp]reocup_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]residi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Pp]rob_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]roces_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]rocur_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]roduci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Pp]ronunci_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]ropin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Pp]roponi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Pp]rotegi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Pp]uls_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Qq]uebr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Qq]uej_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[RR]eunific_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]adi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]ay_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]ealiz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]eban_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]ebautiz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]ecerc_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]ecibi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]ecit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]eclam_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]econoci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]econstruy_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]ecord_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]ecorri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]ecort_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]ecre_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]ecubri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]edonde_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]efugi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]elat_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]elocaliz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]emat_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]emodel_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]emovi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]emplaz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]epiti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]epitie_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]eprendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]eproch_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]eproduci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]esquebraj_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]est_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]esult_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]etorn_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]evel_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]evirti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]evivi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]i_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Rr]oci_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]og_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]ose_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]ot_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Rr]oz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]ac_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]acraliz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]acrific_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]ali_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]aque_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]eccion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]educi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]indic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]obreentendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]obrentendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]obreponi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]obrevivi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]ofri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]olicit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]ometi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]onri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]opl_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]oport_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]osteni_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]oñ_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]ubordin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]ubstituy_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]ubtendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]uccion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]ucedi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]ucedí_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]ufri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]ugiri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]ujet_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]umi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]uministr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]uperenfri_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]uplant_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Ss]upli_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]uponi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]uprimi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Ss]uspendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Tt]ach_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Tt]eletransport_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Tt]emi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Tt]endi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Tt]ermin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Tt]estific_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Tt]oquete_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Tt]orci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Tt]ortur_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Tt]ransport_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Tt]rascendi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Tt]raspas_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Tt]rasport_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Uu]nific_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Vv]aci_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Vv]apule_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Vv]ari_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Vv]el_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Vv]endi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Vv]erti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
# lema(ur'[Vv]igil_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Vv]incul_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Vv]iol_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Vv]ision_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Vv]isualiz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Vv]omit_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]dentr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]dicion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]horc_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]lcanz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]lej_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]liment_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]not_á_ndola(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]part_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]pod_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]poy_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]proxim_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]rrebat_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]rregl_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]torment_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]traves_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]vent_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Cc]arg_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Cc]entr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Cc]hoc_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Cc]ocin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Cc]ogi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Cc]omi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Cc]omponi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Cc]omprob_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Cc]omprometi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Cc]oncentr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Cc]onduci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Cc]onfi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Cc]onfundi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Cc]onstruy_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Cc]opi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Cc]ur_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Dd]emostr_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Dd]ese_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Dd]ibuj_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Dd]iscuti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Dd]istingui_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Dd]omin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ee]jecut_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ee]lectrocut_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ee]mple_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ee]nsambl_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ee]nseñ_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ee]nter_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ee]strangul_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ee]ximi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Ff]alt_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ff]orz_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Gg]obern_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Hh]iri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Hh]undi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Ii]mport_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ii]ncendi_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ii]nici_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ii]nsert_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ii]nspir_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ii]nsult_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Jj]unt_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ll]iber_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Ll]ider_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Mm]encion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Mm]ezcl_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Oo]bserv_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Pp]ractic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Pp]rest_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Pp]rohibi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Pp]roporcion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Pp]rovey_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Qq]ueri_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Rr]ecrimin_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Rr]egal_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Rr]egres_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Rr]eincorpor_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Rr]elacion_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Rr]emont_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Rr]enov_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Rr]eparti_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Rr]espondi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Rr]ugi_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Ss]uplic_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Tt]ap_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Tt]orn_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Tt]raduci_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Tt]ray_é_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_e') + #0
#lema(ur'[Vv]ol_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
[]][0]

grupo1Musica = [
lema(ur'_álbu_m(?:es|)_albú') + #35
lema(ur'\(_álbum de \g<num>_\)_(?P<num>[0-9]{4}) album') + #9
lema(ur'_á_lbum(?:es|)_a', pre=ur'(?:[Aa]l|[Dd]el?|[Ee]ste|[Ee]stos|[Ee]l|[Ee]n|[Ll]os|[Dd]os|[Tt]res|[Cc]uatro|[Ss]us?|[Pp]rimer|[Ss]egundo|[Tt]ercer|[Cc]uarto|[Qq]uinto|[Ss]exto|[UuÚú]ltimo|[Mm]ejor|[Nn]ing[uú]n|[Nn]uevo|[Mm]ismo) ') + #407
lema(ur'_Á_lbum(?:es|)_A', pre=ur'(?:[Aa]l|[Dd]el?|[Ee]ste|[Ee]stos|[Ee]l|[Ee]n|[Ll]os|[Uu]n|[Dd]os|[Tt]res|[Cc]uatro|[Ss]us?|[Pp]rimer|[Ss]egundo|[Tt]ercer|[UuÚú]ltimo|[Nn]ing[uú]n|[Nn]uevo) ', xpos=[ur' famille', ]) + #50
lema(ur'_á_lbum_a', pre=ur'[Uu]n ', xpos=[ur' che', ]) + #30
lema(ur'[Mm]_ú_sica_u', pre=ur'[Ll]a ', xpre=[ur' e ', ur'Contro ', ur'Euridice, ', ur'Per ', ur'Plau De ', ur'Prima ', ur'Storia de ', ur'per ', ur'sei ', ur'sopra ', ], xpos=[ur' (?:[èe]|dei|ci|provata|Italiana nel|alla|del (?:cuore|violone|mare)|alla|per|degli|antica|nella|intorno|Fiorentina|Notturna|russa|In)\b', ]) + #217
lema(ur'[Mm]_ú_sica_u', pre=ur'\bde ', xpre=[ur'\'', ur'Dialogus ', ur'Escola ', ur'Scriptores ', ur'Tractatus ', ur'ecclesiastici ', ], xpos=[ur' (?:i|da|medii|libri|tratactus|theorica|Elettronica|aurea|Ficta|Tonante|negli)\b', ]) + #182
lema(ur'[Mm]_ú_sicos?_u', xpre=[ur'Adversus ', ur'\b(?:di|[Ii]l) ', ], xpos=[ur' (?:prattico|del secolo|di|portuguezes|ha menester|perfetto)\b', ]) + #150
lema(ur'[Mm]_ú_sica (?:o|y|a|[Aa]c[uú]stica|culta|elaborada|folcl[óo]rica|instrumental|militar|original|orquestal|popular|pagana|profana|sinf[oó]nica|tradicional|regional|religiosa|vocal|[Ee]lectr[óo]nica|[Mm]ec[aá]nica|[Cc]ountry)\b_u') + #142
lema(ur'[Mm]_ú_sica de_u', xpre=[ur'Ars ', ur'della ', ]) + #116
lema(ur'[Mm]_ú_sica en_[uù]', xpre=[ur'Della ', ur'MSC Storia de la ', ur'per ', ], xpos=[ur' (?:nella|Macerata|Mainz|negli)', ]) + #23
lema(ur'[Mm]_ú_sicas?_u', pre=ur'(?:[Ll]as|[Uu]nas?|[Ss]us?|[Dd]ar|[Dd]ando|[Tt]ocando|[Cc]ada|tocaba|cantaba) ') + #13
lema(ur'[Mm]_ú_sica cl[aá]sica_u') + #12
lema(ur'[Mm]_ú_sica del_u', xpre=[ur'Ars ', ], xpos=[ur' (?:XV [Ss]ecolo|cuore|violone|mare|señor Giulio|Signor)', ]) + #11
lema(ur'[Mm]_ú_sica al_u', xpos=[ur' (?:Castell|tempo)', ]) + #2
#lema(ur'[Mm]_ú_sicas_u', pre=ur'(?:[Ll]as|[Uu]nas|[Ss]us) ', xpos=[ur' [Cc]0
#lema(ur'_álbumes__albums', pre=ur'(?:[Ll]os|[Ss]us)') + #0
[]][0]

grupo1 = grupo1FormatoLibre + grupo1Frec + grupo1Mas + grupo1Esta + grupo1Musica + grupo1Andos + grupo1Se + [#Desde 1000
lema(ur'[Tt]_í_tulos?_i', xpre=[ur' [Ss]e ', ur'<', ur'[Qq]ue ', ur'atributo "', ur'class="', ur'inline,splendido ', ], xpos=[ur' (?:Sancti|post praemia|Basilicae|Sanctae|Immaculatae)', ]) + #2000
lema(ur'[Rr]ep_ú_blicas?_u', xpre=[ur'\bse ', ur'Ceska ', ur'Maria ', ur'Summa de ', ur'Trăiască ', ur'Vèneta ', ur'\b(?:Na|De|et) ', ur'\b(?:[Dd]el|the|Res) ', ur'\bA ', ur'\ba I ', ur'della ', ur'i de la ', ur'nella ', ur'siue ', ur'summa ', ], xpos=[ur' (?:Pureza|litteraria|\(álbum|Sovietică|Velha|sang Negros|Moldova|Socialistă|Moldovenească|Cheka|Portuguesa|emendanda|\(banda|noastră|Populară|dominatione|semanalmente|libri|est|e a política|commentationes|e Chantun|Iasorum|Mioritică|Neo |d[io] )', ur'(?:\.com|, Westside|, grabando|\]\]n[ao]s?)', ]) + #1119
[]][0]

grupo2Accion = [
lema(ur'[Ss]elecci_ó_n_o', xpos=[ur' Esportives', ur'\]\]es', ]) + #614
lema(ur'[Cc]lasificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #539
lema(ur'[Pp]oblaci_ó_n_o', xpre=[ur'New ', ur'North ', ur'Old ', ur'South ', ], xpos=[ur' (?:East|West)', ur'\]\](?:es|al|ales)', ]) + #501
lema(ur'[Nn]aci_ó_n_o', xpre=[ur'Mexicana ', ], xpos=[ur' Occitana', ur'(?:\]|\.com)', ]) + #427
lema(ur'[Ee]staci_ó_n_o', xpos=[ur' San Alberto Hurtado.jpg', ur'\]\]es', ]) + #425
lema(ur'[Rr]edirecci_ó_n_o', xpos=[ur'\]\]es', ]) + #300
lema(ur'[Ff]undaci_ó_n_o', xpre=[ur'Fundación en 1987 "', ], xpos=[ur' Paraguaya\'s', ur'(?:[\]@]|2008|\.uocra)', ]) + #282
lema(ur'[Cc]anci_ó_n_o', xpos=[ur'\]\]es', ]) + #216
lema(ur'[Cc]oncepci_ó_n_o', xpre=[ur' (?:of|ng) ', ur'Araneus ', ur'Immaculate ', ur'Sam ', ], xpos=[ur' (?:Gross|\(Texas)', ur'(?:\]|\.cl)', ]) + #191
lema(ur'[Cc]onstituci_ó_n_o', xpre=[ur'da ', ], xpos=[ur' di', ur'\]\]', ]) + #178
lema(ur'[Gg]rabaci_ó_n_o', xpos=[ur'\]\]es', ]) + #175
lema(ur'[Aa]sunci_ó_n_o', xpre=[ur' of ', ur'd\'', ur'near ', ], xpos=[ur' (?:Skyscraper|Golf|Business)', ]) + #172
lema(ur'[Aa]cci_ó_n_o', xpre=[ur'd\'', ], xpos=[ur'\]\]es', ]) + #161
lema(ur'[Cc]ampe_ó_n_o', xpos=[ur'\]\]es', ]) + #159
lema(ur'[Dd]ivisi_ó_n_o', pre=ur'(?:[Uu]na|[Cc]ada|[Ss]u|[Pp]rimera|[Ss]egunda|[Cc]uarta) ', xpos=[ur' [12]\b', ur'\.htm', ]) + #157
lema(ur'[Ee]dici_ó_n(?!\]|\.cl)_o') + #148
lema(ur'[Ii]nformaci_ó_n_o', xpos=[ur'(?: *[@\]]|\.(?:com|es))', ]) + #143
lema(ur'[Cc]oraz_ó_n_o', xpre=[ur'Anya ', ur'D\'', ], xpos=[ur' (?:Productions|Aquino)', ur'(?:\]\][a-z]+|\.(?:pe|cl|com))', ]) + #142
lema(ur'[Cc]omisi_ó_n_o', xpos=[ur'\]\]es', ]) + #137
lema(ur'[Dd]irecci_ó_n_o', xpos=[ur'(?:\]|\.tytres)', ]) + #136
lema(ur'[Rr]inc_ó_n_o', xpre=[ur'Beach ', ur'Bonaire\)\|', ur'California\)\|', ur'Chrysometa ', ur'Georgia\)\|', ur'Indiana\)\|', ur'Real ', ur'Rincon\]\] \(', ur'Vespo ', ur'Vespo\]\] \(', ur'\bs ', ur'cráter\)\|', ], xpos=[ur' (?:to|Valley|Beach|Mix|High|Center|Sapiencia|Point|Hill|Road|i Verdera|\((?:cráter|Georgia|Bonaire|California|Indiana))\b', ur'(?:, Bonaire|\]\]es)', ]) + #133
lema(ur'[Dd]escripci_ó_n_o', xpre=[ur'cousa ', ], xpos=[ur' (?:Graphica|breue|Histórico Geografía|de todas las provincias, reynos)', ur'\]\]es', ]) + #123
lema(ur'[Rr]az_ó_n_o', xpre=[ur'Bernard ', ur'Cynthia V\. ', ur'Meital de ', ], xpos=[ur' (?:and|Copa|de aquellas muchas cabeçuelas)', ur'\]\]es', ]) + #119
lema(ur'[Vv]ersi_ó_n_o', pre=ur'(?:de|[Ll]a|[Uu]na|[Ee]sta|[Ee]sa|[Cc]ada|[Ss]u|[Ee]n|[Pp]rimera|[Ss]egunda|[Tt]ercera|[Cc]uarta|[ÚUúu]ltima|[Nn]ueva|cualquier) ', xpre=[ur'd\'après ', ur'pour ', ur'pour ', ], xpos=[ur' (?:Cue|thebaine|restaurée|en français|française)', ]) + #109
lema(ur'[Ee]ducaci_ó_n_o', xpos=[ur' Salsa', ur'(?:\]|\.go[bv]|\.yucatan|\.es)', ]) + #106
lema(ur'[Aa]sociaci_ó_n_o', xpos=[ur'\]|\.Civil', ]) + #104
lema(ur'[Tt]elevisi_ó_n_o', pre=ur'[Dd]e ', xpos=[ur' (?:City|Without|Heaven)', ]) + #102
lema(ur'[Rr]elaci_ó_n_o', xpos=[ur' del cautiverio i trabajo', ur'\]\]es']) + #95
lema(ur'_Venevisió_n_(venevisi[óo]|Venevisio)', xpre=[ur'\.', ], xpos=[ur'\.', ]) + #93
lema(ur'[Rr]evoluci_ó_n_o', xpre=[ur'Zonda ', ], xpos=[ur'\]\]es', ]) + #89
lema(ur'[Cc]añ_ó_n_o', xpre=[ur'Ipyahe ', ur'[Mm]icropolitana ', ], xpos=[ur' City', ur'\]\]es', ]) + #88
lema(ur'[Ff]ederaci_ó_n_o', xpos=[ur' (?:de l|Galega|d)\b', ur'(?:\]|\.pe)', ]) + #84
lema(ur'[Gg]esti_ó_n_o', xpre=[ur'Assurances ', ur'Contrôle de ', ur'Français de ', ur'Intercommunal de ', ur'Sciences de la ', ur'Societé de ', ur'Socièté de ', ur'Société de ', ur'Suisses de ', ur'Syndicat de ', ur'Système de ', ur'contrôle de ', ur'et ', ur'et de ', ur'européen de ', ur'française de ', ur'mauvaise ', ur'méthodes de ', ur'nouvelle ', ur'pour ', ur'pour la ', ur'structure, ', ur'supérieur de ', ur'École de ', ur'à la ', ur'économie, ', ], xpos=[ur' (?:(?:et|ou) |par|pour|forestière|Privee-SIB|informatisée|publique|Patrimoniale|Animation|Bonfire|stratégique|écologique|du|des|plus|Municipale|Intégrée|de (?:Genève|classe|la qualité|la relation|documents|contenu|l\'ArchiTEcture|l\'Entreprise)|Cinématographique)', ur'(?:[0-9\]]|\.org)', ]) + #83
lema(ur'[Ii]nterpretaci_ó_n_o', xpos=[ur'\]\]es', ]) + #83
lema(ur'[Oo]rganizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #82
lema(ur'[Uu]ni_ó_n (?:Dem[oó]crata|Estepona|Sovi[eé]tica)_o') + #81
lema(ur'[Pp]osici_ó_n_o', xpos=[ur'\]\]es', ]) + #80
lema(ur'[Pp]resentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #79
lema(ur'[Cc]onservaci_ó_n_o', xpos=[ur'\]\](?:es|ista)', ]) + #77
lema(ur'[Cc]reaci_ó_n_o', xpos=[ur'\]\]es', ]) + #76
lema(ur'[Pp]roducci_ó_n_o', xpos=[ur'(?:\]|\.(?:com|gob)|\'s)', ]) + #76
lema(ur'[Aa]vi_ó_n_o', xpre=[ur'CS ', ur'Calais\)\|', ur'Cantón de ', ur'Comme un ', ur'Europe en ', ur'Novi ', ur'Orchestra ', ur'Par ', ur'Paul ', ur'[Cc]antón de ', ur'[Cc]antón de Avion\|', ur'\b[LlDd]\'', ur'cet ', ur'yvate ', ], xpos=[ur' (?:Corporation|Travel|de (?:Transport|minuit|Combat)|Baker|Express|\(Paso|)', ur'(?:, (?:Pas|Grenay)|\]\]es)', ]) + #74
lema(ur'[Cc]olecci_ó_n_o', xpos=[ur'\]\]es', ]) + #72
lema(ur'[Cc]omunicaci_ó_n_o', xpos=[ur'(?:\,umh|\]\]es|\.senado)', ]) + #72
lema(ur'[Pp]asi_ó_n_o', xpre=[ur'E\. ', ur'the ', ], xpos=[ur' (?:for|Wrestling|Dub|ni)\b', ur'\.demotilla', ]) + #72
lema(ur'[Uu]ni_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Ee]st?a) ', xpre=[ur' á ', ur'Auto ', ur'Journal de la ', ur'Ridge ', ur'San Fernando de ', ur'of ', ], xpos=[ur' (?:Camp|Libérale|Académique|College|Women|Insurance|Catholique|anarchiste|County|Nazionale|Bordeaux|Sportive|Testament|Metallic|Anarco-communiste|Athletique|Avenue|Bay|Brazilian|Buildings|Carbide|Castle|Chapel|Church|City|Company|Cycliste|Elementary|Elevated|Evangelischer|Ferry|Fire|Flag|Française|Guilde|High|Hill|Internationale|Jack|League|List|Maçonnique|Mining|Mundial pro|Nationale|Oil|Pacific|Square|Station|Steamship|Stock|Street|Terminal|Theological|Trust|Turnpike|University|Vélocipédique|anarcho|calédonienne|des|fédérale|istorica|nationale|pour|socialiste|storica|de (?:Compositeurs|banques)|(?:of|do) )', ]) + #64
lema(ur'[Aa]dministraci_ó_n_o', xpos=[ur'(?:@|\]\]es)', ]) + #63
lema(ur'[Ii]lustraci_ó_n_o', xpos=[ur'\]\]es', ]) + #61
lema(ur'[Oo]cupaci_ó_n_o', xpos=[ur'\]\]es', ]) + #61
lema(ur'[Gg]eneraci_ó_n_o', xpre=[ur'@1', ], xpos=[ur'(?:\]|\.com)', ]) + #60
lema(ur'[Ss]ecci_ó_n_o', xpos=[ur'[1-9\]]', ]) + #60
lema(ur'[Ee]lecci_ó_n_o', xpos=[ur'\]\]es', ]) + #57
lema(ur'[Ii]_nauguració_n_(?:gnauraci[oó]|naguraci[oó]|nauguracio)', xpos=[ur'\]\]es', ]) + #57
lema(ur'[Rr]egi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na) ', xpos=[ur' (?:de|Mediterraneenne|Centrale|alpine|himalayenne|du |Sud et|Côtier|d\'Ambovombe)', ]) + #55
lema(ur'[Tt]orre_ó_n_o', xpos=[ur'\]\]es', ]) + #55
lema(ur'[Aa]probaci_ó_n_o', xpos=[ur'\]\]es', ]) + #54
lema(ur'[Dd]ivisi_ó_n_o', pre=ur'[Ll]a ', xpos=[ur' (?:[12]|Interrégionale|me perd|navale|en France|of |du |politique|méthodique|Rosemont|One|Two|Three|Théorique|de l’intérieur|des |Skanderbeg, Histoire|Charlemagne|SS Das reich sème|[Oo]ne)\b', ]) + #53
lema(ur'[Tt]radici_ó_n_o', xpos=[ur'\]\](?:al|es)', ]) + #53
lema(ur'[Pp]abell_ó_n_o', xpos=[ur' As', ur'\]\]es', ]) + #51
lema(ur'[Oo]peraci_ó_n_o', xpos=[ur'\]\]es', ]) + #50
lema(ur'[Cc]ati_ó_n_o', xpre=[ur'putative ', ], xpos=[ur' (?:denatonium|exchange|channel|in|of)', ur'\]\]es', ]) + #49
lema(ur'[Ee]xpedici_ó_n_o', xpos=[ur' Antarctic', ur'\]\]es', ]) + #49
lema(ur'[Ii]nvestigaci_ó_n_o', xpos=[ur'\]\]es', ]) + #49
lema(ur'[Ff]unci_ó_n_o', xpos=[ur'\]\]es', ]) + #48
lema(ur'[Kk]ilot_ó_n_o', xpos=[ur'\]\]es', ]) + #48
lema(ur'[Ee]xposici_ó_n_o', xpos=[ur' de la dotrina', ur'\]\]es', ]) + #47
lema(ur'[Ss]ituaci_ó_n_o', xpre=[ur'Q[’\']', ], xpos=[ur' \(Abril de 1864', ur'\]\]es', ]) + #46
lema(ur'[Uu]bicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #46
lema(ur'[Tt]ibur_ó_n_o', xpre=[ur'(?:EA|[Ll]e|of|[Ii]n) ', ur'Arts ', ur'California\)\|', ur'Hyundai ', ], xpos=[ur' (?:Film|Chum|Boulevard|International|Challenger|y Belvedere|Center|Peninsula|\(California)', ur'(?:, \[|\]\]es)', ]) + #45
lema(ur'[Cc]onvulsi_ó_n_o', xpos=[ur' (?:[Tt]herapy|Group)', ur'\]\]es', ]) + #44
lema(ur'[Ii]nstituci_ó_n_o', xpos=[ur'\]\]es', ]) + #44
lema(ur'[Dd]efinici_ó_n_o', xpos=[ur'(?:\]|\.org|\.de)', ]) + #42
lema(ur'[Ff]usi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|de|y) ', xpre=[ur'énergie ', ], xpos=[ur' (?:Ford|Man|de deux|Systems|Rhône)', ur'\]\]es', ]) + #42
lema(ur'[Oo]btenci_ó_n_o', xpos=[ur'\]\]es', ]) + #42
lema(ur'[Rr]egi_ó_n de_o', xpre=[ur'Muscinees de la ', ]) + #42
lema(ur'[Pp]rocesi_ó_n_o', xpos=[ur'\]\](?:es|al|ales)', ]) + #41
lema(ur'[Ee]cuaci_ó_n_o', xpos=[ur'\]\]es', ]) + #40
lema(ur'[Ff]ormaci_ó_n_o', xpos=[ur'\]\]es', ]) + #40
lema(ur'[Pp]rogramaci_ó_n_o', xpos=[ur'\]\]es', ]) + #40
lema(ur'[Dd]istribuci_ó_n_o', xpos=[ur'\]\]es', ]) + #39
lema(ur'[Pp]articipaci_ó_n_o', xpos=[ur' ciutadana', ur'\]\]es', ]) + #39
lema(ur'[Dd]iputaci_ó_n_o', xpos=[ur'\]\]es', ]) + #38
lema(ur'[Dd]rag_ó_n_[oò]', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ', xpre=[ur'Dent ', ur'Europa ', ur'Rêve ', ], xpos=[ur' (?:Cry|Con|Dance|Hunters|Inn|Lancer|Psychic|Caesar|Ranger|School|dans|Festival|Hill|Lore|Fly|Queen|Rouge|Warrior|Boy|TV|City|Tales|Booster|Rock|Comics|Knight|Tour|Hawk|marin|[Bb]oat|Lee|[Bb]all|[Ss]layer|[Qq]uest|[Rr]apide|[Ff]all|[Aa]ge|[Ww]orld|[Gg]ate|Shot|Tail|Khan|Ash|Sound|Force|Mk\.IV|/ Falcon)', ur'(?:\]\]es|\'s)', ]) + #38
lema(ur'[Ee]voluci_ó_n_o', xpos=[ur' e desnreolo', ur'\]\]es', ]) + #38
lema(ur'[Rr]esoluci_ó_n_o', xpos=[ur'\]\]es', ]) + #38
lema(ur'[Aa]viaci_ó_n_o', xpos=[ur'(?:\]\]es|\.mil)', ]) + #37
lema(ur'[Tt]ransmisi_ó_n_o', xpos=[ur' (?:Eléktrika|kon)', ur'\]\]es', ]) + #37
lema(ur'[Cc]uesti_ó_n_o', xpos=[ur'\]\]es', ]) + #36
lema(ur'[Tt]raducci_ó_n_o', xpos=[ur'\]\]es', ]) + #36
lema(ur'[Ii]ntroducci_ó_n_o', xpos=[ur'\]\]es', ]) + #35
lema(ur'[Mm]anifestaci_ó_n_o', xpos=[ur'\]\]es', ]) + #35
lema(ur'[Pp]laneaci_ó_n_o', xpos=[ur'\]\]es', ]) + #35
lema(ur'[Cc]orporaci_ó_n_o', xpos=[ur'\]\]es', ]) + #34
lema(ur'[Oo]pini_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Ee]n|[Dd]e) ') + #34
lema(ur'[Ee]ncarnaci_ó_n_o', xpos=[ur'\]\]es', ]) + #33
lema(ur'[Nn]ataci_ó_n_o', xpos=[ur'\]\]es', ]) + #33
lema(ur'[Cc]olaboraci_ó_n_o', xpos=[ur'\]\]es', ]) + #32
lema(ur'[Ee]misi_ó_n_o', xpos=[ur'\]\]es', ]) + #32
lema(ur'[Ll]ocalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #32
lema(ur'[Rr]enovaci_ó_n_o', xpos=[ur'\]\]es', ]) + #32
lema(ur'[Rr]iñ_ó_n_o', xpos=[ur'\]\]es', ]) + #32
lema(ur'[Pp]ublicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #31
lema(ur'[Cc]onvenci_ó_n_o', xpos=[ur'\]\]es', ]) + #30
lema(ur'[Tt]ax_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ') + #30
lema(ur'[Aa]dhesi_ó_n_o', xpre=[ur'& ', ur'Macrophage ', ur'[Cc]ell ', ur'[Ff]ocal ', ur'[Ii]n ', ], xpos=[ur' (?:and|of|Prevention|molecules)', ur'\]\][a-z]+', ]) + #29
lema(ur'[Aa]parici_ó_n_o', xpos=[ur'\]\]es', ]) + #29
lema(ur'[Cc]onfederaci_ó_n_o', xpos=[ur'\]\]es', ]) + #29
lema(ur'[Ee]lec_cio_nes_(?:i[oó]|cci[oó])') + #29
lema(ur'[Rr]econstrucci_ó_n_o', xpos=[ur'\]\]es', ]) + #29
lema(ur'[Rr]evelaci_ó_n_o', xpos=[ur'\]\]es', ]) + #29
lema(ur'[Rr]estauraci_ó_n_o', xpos=[ur'\]\]es', ]) + #28
lema(ur'[Aa]nimaci_ó_n_o', xpos=[ur'\]\]es', ]) + #27
lema(ur'[Ii]nstrucci_ó_n_o', xpos=[ur' pastoral que el', ur'\]\]es', ]) + #27
lema(ur'[Rr]at_ó_n_o', xpre=[ur'(?:Le|On) ', ur'[Mm]esa ', ur'[RB]oca ', ], xpos=[ur' (?:section|Mesa|Pass|Municipal Airport)', ur'[\'\]]', ]) + #27
lema(ur'[Rr]emodelaci_ó_n_o', xpos=[ur'\]\]es', ]) + #27
lema(ur'[Ss]ubcampe_ó_n_o', xpos=[ur'\]\]es', ]) + #27
lema(ur'[Cc]oalici_ó_n(?![0-9\]])_o') + #26
lema(ur'[Dd]uraci_ó_n_o', xpos=[ur'\]\]es', ]) + #26
lema(ur'[Jj]urisdicci_ó_n_o', xpos=[ur'\]\]es', ]) + #26
lema(ur'[Ll]adr_ó_n_o', xpos=[ur' Peak', ur'\]\]es', ]) + #26
lema(ur'[Pp]risi_ó_n_o', xpre=[ur' In ', ur'Glass ', ], xpos=[ur' (?:ward|blues|Fellowship|Match)', ur'\]\]es', ]) + #26
lema(ur'[Pp]romoci_ó_n_o', xpre=[ur'Ròker ', ], xpos=[ur'\]\]es', ]) + #26
lema(ur'[Rr]edacci_ó_n_o', xpos=[ur'\]\]es', ]) + #26
lema(ur'[Ss]esi_ó_n_o', xpre=[ur'[Ii]n ', ur'jam ', ur'room ', ], xpos=[ur'\]\]es', ]) + #26
lema(ur'[Ss]ucesi_ó_n_o', xpos=[ur'\]\]es', ]) + #26
lema(ur'[Ff]icci_ó_n_o', xpos=[ur'\]\]es', ]) + #25
lema(ur'[Gg]obernaci_ó_n_o', xpos=[ur' de la Generalidad de Cataluna', ur'(?:\]|\.gob)', ]) + #25
lema(ur'[Ii]ntegraci_ó_n_o', xpos=[ur'\]\]es', ]) + #25
lema(ur'[Pp]iñ_ó_n_o', xpre=[ur'Jannis ', ur'Kusnezov ', ur'Led ', ur'Pine ', ur'Ramon ', ], xpos=[ur' (?:Hills|Pine)', ur'\]\]es', ]) + #25
lema(ur'[Pp]roduc_c_i(?:ón|ones)_s?') + #25
lema(ur'[Cc]ertificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #24
lema(ur'[Cc]oncentraci_ó_n_o', xpos=[ur'\]\]es', ]) + #24
lema(ur'[Hh]idroavi_ó_n_o', xpos=[ur'\]\]es', ]) + #24
lema(ur'[Ii]nfecci_ó_n_o', xpos=[ur'\]\]es', ]) + #24
lema(ur'[Ii]nscripci_ó_n_o', xpos=[ur'\]\]es', ]) + #24
lema(ur'[Dd]ifusi_ó_n_o', xpre=[ur'Fonogram ', ], xpos=[ur'\]\]es', ]) + #23
lema(ur'[Ii]nquisici_ó_n_o', xpos=[ur' á ', ur'(?:\]|\.scd|, chronista)', ]) + #23
lema(ur'[Ii]nten_ció_n_si[oó]') + #23
lema(ur'[Ll]esi_ó_n (?:de|en|que)\b_o') + #23
lema(ur'[Oo]ca_sio_nes_(?:ci[oó]|sió)') + #23
lema(ur'[Tt]romb_ó_n_o', xpos=[ur'\]\](?:es|istas?)', ]) + #23
lema(ur'[Aa]ctuaci_ó_n_o', xpos=[ur'\]\]es', ]) + #22
lema(ur'[Bb]alc_ó_n_o', xpre=[ur'(?:[Ll]e|du|au) ', ur'Claudie ', ur'Jill ', ur'M\. ', ur'Michael ', ur'\b(?:por|mon) ', ur'grand ', ur'relais de ', ur'siendo ', ], xpos=[ur' (?:à|sur|Zone|en forêt|renombró)\b', ur'(?:\]\](?:es|ada)|, (?:Sylvie|corridor))', ]) + #22
lema(ur'[Mm]utaci_ó_n_o', xpos=[ur'\]\]es', ]) + #22
lema(ur'[Rr]ecaudaci_ó_n_o', xpos=[ur'\]\]es', ]) + #22
lema(ur'[Vv]ersi_ó_n en_o') + #22
lema(ur'[Ii]nmigraci_ó_n_o', xpos=[ur'\]\]es', ]) + #21
lema(ur'[Vv]ag_ó_n_o', xpos=[ur'\]\]es', ]) + #21
lema(ur'[Ee]recci_ó_n_o', xpos=[ur'\]\]es', ]) + #20
lema(ur'[Pp]ante_ó_n_o', xpos=[ur'\]\]es', ]) + #20
lema(ur'[Pp]ercusi_ó_n_o', xpre=[ur'and ', ], xpos=[ur' [Ss]et', ur'\]\]es', ]) + #20
lema(ur'[Ss]ubregi_ó_n_o', xpre=[ur'Africa ', ur'Papuan ', ], xpos=[ur'\]\]es', ]) + #20
lema(ur'[Vv]isi_ó_n_o', pre=ur'(?:[Uu]na|[Cc]ada|[Ss]u|[Ll]a|[Ee]sta) ', xpos=[ur' (?:City|mystique|érotique|romantique|qu|du|des|Gallery|après)\b', ]) + #20
lema(ur'[Dd]elegaci_ó_n_o', xpos=[ur'\]\]es', ]) + #19
lema(ur'[Ll]iberaci_ó_n_o', xpos=[ur'(?:\]|: Songs)', ]) + #19
lema(ur'[Rr]euni_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Ee]st?a) ', xpre=[ur'Denis de ', ], xpos=[ur' Island', ]) + #19
lema(ur'[Tt]elevisi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Ee]n|[Pp]or|Caracas) ', xpos=[ur' (?:Broadcasts?|Critics?|City|Parts|Preview)', ]) + #19
lema(ur'[Aa]grupaci_ó_n_o', xpos=[ur'\]\]es', ]) + #18
lema(ur'[Aa]tenci_ó_n_o', xpos=[ur'\]\]es', ]) + #18
lema(ur'[Cc]ompetici_ó_n_o', xpos=[ur'\]\]es', ]) + #18
lema(ur'[Dd]enominaci_ó_n_o', xpos=[ur'\]\]es', ]) + #18
lema(ur'[Ii]nundaci_ó_n_o', xpos=[ur'\]\]es', ]) + #18
lema(ur'[Mm]isi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]|[Ee]st?a) ') + #18
lema(ur'[Mm]oj_ó_n_o', xpre=[ur'Benedetto ', ur'Giuseppe ', ], xpos=[ur' Records', ur'\]\]es', ]) + #18
lema(ur'[Pp]articipaci_o_nes_ó') + #18
lema(ur'[Pp]end_ó_n_o', xpre=[ur'Dan y su ', ], xpos=[ur'\]\]es', ]) + #18
lema(ur'[Pp]osesi_ó_n_o', xpos=[ur'\]\]es', ]) + #18
lema(ur'[l]e_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ', xpre=[ur'Juusso ', ]) + #18
lema(ur'[Cc]allej_ó_n_o', xpos=[ur' \(banda', ur'\]\]es', ]) + #17
lema(ur'[Cc]icl_ó_n_o', xpos=[ur'\]\]es', ]) + #17
lema(ur'[Ee]vasi_ó_n_o', xpre=[ur'Bridging ', ur'Cartwheel ', ur'Citro[eë]n ', ur'Disques ', ur'Filter ', ur'Her ', ur'Jailbreak ', ur'Matrix ', ur'Roman de ', ur'Somersault ', ur'[Ll]\'', ur'[Tt]ax ', ur'and ', ur'backflip ', ur'd\'', ur'legged ', ], xpos=[ur' (?:Films|of|par|Clause)', ur'(?:["\]]|, and)', ]) + #17
lema(ur'[Ee]xportaci_ó_n_o', xpos=[ur'\]\]es', ]) + #17
lema(ur'[Ll]egislaci_ó_n_o', xpre=[ur'Nueva Espana\. ', ], xpos=[ur'\]\]es', ]) + #17
lema(ur'[Nn]ominaci_ó_n_o', xpos=[ur' indirècta', ur'\]\]es', ]) + #17
lema(ur'[Ss]anci_ó_n_o', xpos=[ur'\]\]es', ]) + #17
lema(ur'[Ss]oluci_ó_n_o', xpos=[ur'\]\]es', ]) + #17
lema(ur'[Uu]nificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #17
lema(ur'[Cc]aj_ó_n_o', xpos=[ur' (?:Jinbiao|Run|Blvd|[Pp]ass|Summit|Transit|Boulevard|\(California|Valley|Park)', ur'(?:\]|\'\', sin tilde)', ur', (?:California|Fresno)', ]) + #16
lema(ur'[Cc]ivilizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #16
lema(ur'[Cc]omposici_ó_n_o', xpos=[ur'\]\]es', ]) + #16
lema(ur'[Cc]ongesti_ó_n_o', xpre=[ur'Hors ', ur'ease ', ur'of ', ur'the ', ur'traffic ', ur'venous ', ], xpos=[ur' (?:[Aa]voidance|[Hh]andling|[Tt]hreshold|[Pp]ricing|Tax|of|Relief|Window|charges?|window|[Nn]otification|[Mm]itigation|[Ii]nterpretation|[Rr]eduction|[Cc]osts|[Cc]ontrol)', ]) + #16
lema(ur'[Dd]ivisi_ó_n_o', pre=ur'[Tt]ercera ', xpos=[ur'\.cl', ]) + #16
lema(ur'[Ii]nnovaci_ó_n_o', xpos=[ur'\]\]es', ]) + #16
lema(ur'[Pp]atr_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ', xpre=[ur'repiè ', ur'vida ', ], xpos=[ur' (?:de presse|and|Saint|Advisory)', ]) + #16
lema(ur'[Pp]etici_ó_n(?!\]|\.xsd)_o') + #16
lema(ur'[Pp]resi_ó_n_o', xpos=[ur'\]\]es', ]) + #16
lema(ur'[Pp]rotecci_ó_n_o') + #16
lema(ur'[Aa]daptaci_ó_n_o') + #15
lema(ur'[Bb]omb_ó_n_o', xpos=[ur' Evolution', ur'(?:\. Aqua|\]\]es)', ]) + #15
lema(ur'[Cc]elebraci_ó_n_o', xpos=[ur'\]\]es', ]) + #15
lema(ur'[Cc]onexi_ó_n(?!\]|\.com)_o', xpre=[ur'Madonna ', ur'Makarras ', ]) + #15
lema(ur'[Cc]ontinuaci_ó_n_o') + #15
lema(ur'[Dd]e_cisió_n_(?:si[sc]i[oó]|cici[oó])') + #15
lema(ur'[Dd]epresi_ó_n_o', xpos=[ur'\]\]es', ]) + #15
lema(ur'[Oo]posici_ó_n_o', xpos=[ur'\]\]es', ]) + #15
lema(ur'[Pp]rot_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpos=[ur' (?:Block|Prevé|Exora|Satria|en la clase|Synchrotron)', ur' *[1-9][0-9]*', ur'\]\]es', ]) + #15
lema(ur'[Ss]al_ó_n_o', pre=ur'(?:[Ee]l|[Uu]n|[Cc]ada|[Ss]u) ', xpre=[ur'Entr\'acte: ', ], xpos=[ur' (?:Bovy|Indien|International|de (?:Provence|Mai|thé|la (?:Jeune|Correspondance|Société)|l\')|dans |des |d[\'’´]|du |Premium|[Rr][eé]alités?)', ur'(?:\]\]es|\.com)', ]) + #15
lema(ur'[b]al_ó_n_o', xpos=[ur'\]\]es', ]) + #15
lema(ur'[Cc]oncesi_ó_n_o', xpos=[ur'\]\]es', ]) + #14
lema(ur'[Cc]orrupci_ó_n_o', xpos=[ur'\]\]es', ]) + #14
lema(ur'[Ii]nstalaci_ó_n_o', xpos=[ur'\]\]es', ]) + #14
lema(ur'[Ii]ntervenci_ó_n_o', xpre=[ur'Ajoute ', ], xpos=[ur'\]\]es', ]) + #14
lema(ur'[Jj]am_ó_n_o', xpre=[ur'DJ ', ur'Joss ', ur'Kyle ', ur'Nacional ', ur'bruja ', ], xpos=[ur' (?:llega|Alfred|Lucas|Meredith|Gordon)', ur'\]\]es', ]) + #14
lema(ur'[Mm]igraci_ó_n_o', xpos=[ur'\]\]es', ]) + #14
lema(ur'[Nn]utrici_ó_n_o', xpos=[ur'\]\]es', ]) + #14
lema(ur'[Oo]pci_ó_n_o', xpos=[ur'\]\]es', ]) + #14
lema(ur'[Pp]erd_ó_n_o', xpre=[ur'Gerald ', ur'Laurent ', ur'Luana ', ur'S[ae]nt ', ], xpos=[ur'\]\]es', ]) + #14
lema(ur'[Pp]untuaci_ó_n_o', xpos=[ur'\]\]es', ]) + #14
lema(ur'[Rr]eedici_ó_n_o', xpos=[ur'\]\]es', ]) + #14
lema(ur'[Ss]eparaci_ó_n_o', xpos=[ur'\]\]es', ]) + #14
lema(ur'[Tt]ransici_ó_n_o', xpos=[ur'\]\]es', ]) + #14
lema(ur'[Vv]iolaci_ó_n_o', xpos=[ur'\]\]es', ]) + #14
lema(ur'[Dd]estrucci_ó_n_o', xpos=[ur'\]\]es', ]) + #13
lema(ur'[Dd]imisi_ó_n_o', xpos=[ur'\]\]es', ]) + #13
lema(ur'[Ee]valuaci_ó_n_o', xpos=[ur'\]\]es', ]) + #13
lema(ur'[Ee]xtinci_ó_n_o', xpos=[ur'\]\]es', ]) + #13
lema(ur'[Ff]inalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #13
lema(ur'[Hh]abitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #13
lema(ur'[Ll]im_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpre=[ur'Ed\. ', ur'scorzeta ', ]) + #13
lema(ur'[Pp]antal_ó_n_o', xpre=[ur'San ', ur'[Ll]e ', ur'monsieur ', ], xpos=[ur' (?:est|trop|et )', ur'(?:\]\][a-zñ]+|\'])', ]) + #13
lema(ur'[Rr]eacci_ó_n_o', xpos=[ur'\]\]es', ]) + #13
lema(ur'[Rr]eflexi_ó_n_o', xpre=[ur'(?:für|und) ', ur'Eine ', ur'Moment de ', ur'banda\)\|', ur'hermeneutische ', ur'kritischen ', ], xpos=[ur' (?:in|über|und|de[rs]|auf|Exhibition|Masterclass|\(banda)\b', ur', (?:Stargazery|Taste)', ur'\]\]es', ]) + #13
lema(ur'[Ss]alvaci_ó_n_o', xpos=[ur'\]\]es', ]) + #13
lema(ur'[Uu]rbanizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #13
lema(ur'[Aa]fici_ó_n_o', xpos=[ur'\]\](?:es|ad[ao]s?)', ]) + #12
lema(ur'[Aa]lgod_ó_n_o', xpos=[ur' Wine', ur'\]\](?:es|ero)', ]) + #12
lema(ur'[Aa]lucinaci_ó_n_o', xpos=[ur'\]\]es', ]) + #12
lema(ur'[Bb]ot_ó_n_o', xpre=[ur'Joaquín ', ], xpos=[ur'(?:\]|: Houghton)', ]) + #12
lema(ur'[Cc]esi_ó_n_o', xpos=[ur'\]\]es', ]) + #12
lema(ur'[Cc]omparaci_ó_n_o', xpre=[ur'\bE ', ], xpos=[ur'\]\]es', ]) + #12
lema(ur'[Cc]onfesi_ó_n_o', xpre=[ur'A ', ur'Yô ', ], xpos=[ur'\]\]es', ]) + #12
lema(ur'[Cc]oordinaci_ó_n_o', xpos=[ur'\]\]es', ]) + #12
lema(ur'[Cc]oronaci_ó_n_o', xpos=[ur'\]\]es', ]) + #12
lema(ur'[Dd]etenci_ó_n_o', xpos=[ur'\]\]es', ]) + #12
lema(ur'[Dd]imensi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Oo]tra|[Ss]u|[Dd]e|[Ee]st?a|[Tt]ercera|[Cc]uarta) ', xpos=[ur' (?:psychique|Films|Records|Data)', ]) + #12
lema(ur'[Dd]isposici_ó_n_o', xpos=[ur'\]\]es', ]) + #12
lema(ur'[Ee]liminaci_ó_n_o', xpos=[ur'\]\]es', ]) + #12
lema(ur'[Ee]scuadr_ó_n_o', xpos=[ur'[\]0-9]', ]) + #12
lema(ur'[Ee]xtrusi_ó_n_o', xpre=[ur'Screw ', ur'The ', ], xpos=[ur'(?:\]\][a-z]+|: Battlehymns)', ]) + #12
lema(ur'[Oo]raci_ó_n_o', xpos=[ur'\]\]es', ]) + #12
lema(ur'[Pp]elot_ó_n_o', xpre=[ur'Oranje ', ur'Solidaires en ', ur'Tollo ', ur'[Tt]he ', ], xpos=[ur' (?:Association|d\')', ur'\]\][a-zñ]+', ]) + #12
lema(ur'[Pp]royecci_ó_n_o', xpos=[ur'\]\]es', ]) + #12
lema(ur'[Rr]ecopilaci_ó_n_o', xpos=[ur'\]\]es', ]) + #12
lema(ur'[Aa]dmin_istració_n_(?:itraci[oó]|straci[oó]|istrac[ioó])') + #11
lema(ur'[Cc]ombinaci_ó_n_o', xpos=[ur'\]\]es', ]) + #11
lema(ur'[Cc]onsideraci_ó_n_o') + #11
lema(ur'[Cc]onsideraci_ó_n_o', xpos=[ur'\]\]es', ]) + #11
lema(ur'[Cc]onsolaci_ó_n_o', xpos=[ur'\]\]es', ]) + #11
lema(ur'[Dd]edicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #11
lema(ur'[Dd]emostraci_ó_n_o', xpos=[ur'\]\]es', ]) + #11
lema(ur'[Dd]estituci_ó_n_o', xpos=[ur'\]\]es', ]) + #11
lema(ur'[Dd]ocumentaci_ó_n_o', xpre=[ur'Centre International de ', ], xpos=[ur'  e poder', ur'\]\]es', ]) + #11
lema(ur'[Ee]scorpi_ó_n_o', xpre=[ur'Di ', ur'Milo de ', ], xpos=[ur' and', ur'\]\]es', ]) + #11
lema(ur'[Ee]xtensi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #11
lema(ur'[Ff]ermi_ó_n_o', xpos=[ur'\]\]es', ]) + #11
lema(ur'[Ii]ncisi_ó_n_o', xpre=[ur'Second ', ], xpos=[ur'\]\]es', ]) + #11
lema(ur'[Jj]onr_ó_n_o', xpos=[ur'\]\]es', ]) + #11
lema(ur'[Ll]icitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #11
lema(ur'[Mm]edall_ó_n_o', xpos=[ur'\]\]es', ]) + #11
lema(ur'[Pp]e_ó_n_o', xpre=[ur'Carole ', ur'Dictyna ', ur'Domínguez ', ur'Eddie ', ur'Lazy ', ur'Olatz ', ], xpos=[ur' – Batería', ur'\]\]es', ]) + #11
lema(ur'[Pp]lanificaci_ó_n_o', xpos=[ur'(?:\]|\.gob)', ]) + #11
lema(ur'[Pp]recipitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #11
lema(ur'[Rr]ecuperaci_ó_n_o', xpos=[ur'\]\]es', ]) + #11
lema(ur'[Tt]elecomunicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #11
lema(ur'[Aa]dmiraci_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Aa]dvocaci_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Aa]nglosaj_ó_n_o', xpos=[ur'\]\](?:as?|es)', ]) + #10
lema(ur'[Aa]rticulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Cc]amale_ó_n_o', xpos=[ur' Records', ur'\]\]es', ]) + #10
lema(ur'[Cc]amar_ó_n_o', xpre=[ur'J\. ', ur'héros de ', ], xpos=[ur' (?:Marvel|Ochs|Jackson|Silverek)', ur'(?:\]|, la révolution)', ]) + #10
lema(ur'[Cc]ongregaci_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Cc]orrecci_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Dd]emarcaci_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Dd]esambiguaci_ó_n(?!\])_o') + #10
lema(ur'[Dd]esaparici_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Ee]jecuci_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Ee]mbri_ó_n_o', xpos=[ur'\]\](?:es|ari[ao]s?)', ]) + #10
lema(ur'[Ee]rupci_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Ee]scal_ó_n_o', xpre=[ur'California\)\|', ur'Max ', ], xpos=[ur' (?:de Fonton|\(California)', ur'\]\]es', ]) + #10
lema(ur'[Ee]xploraci_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Ee]xten_sió_n_ci[oó]') + #10
lema(ur'[Gg]orri_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Ii]mpresi_ó_n_o', xpos=[ur' de Felipe Mey', ur'\]\]es', ]) + #10
lema(ur'[Mm]edici_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Rr]edenci_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Rr]educci_ó_n_o', xpos=[ur'\.gov', ur'\]\]es', ]) + #10
lema(ur'[Tt]ra_nsliteració_n_sliteraci[oó]') + #10
lema(ur'[Tt]ransformaci_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Tt]ripulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #10
lema(ur'[Aa]ctualizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Bb]uf_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Bb]uz_ó_n_o', xpre=[ur'Bernard ', ur'Beverlee ', ur'Freddy ', ur'du ', ], xpos=[ur'\]\]es', ]) + #9
lema(ur'[Cc]hampiñ_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Cc]intur_ó_n_o', xpre=[ur'Ride ', ], xpos=[ur'\]\]es', ]) + #9
lema(ur'[Cc]onstelaci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Dd]ecisi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #9
lema(ur'[Dd]evoci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Ee]stimaci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Ee]xcepci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Gg]raduaci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Ii]luminaci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Ii]nspiraci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Mm]enci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Nn]avegaci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Nn]otaci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Oo]ca_sió_n_(?:ci[oó]|sio)') + #9
lema(ur'[Oo]casi_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Pp]eregrinaci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Pp]rofesi_ó_n_o', xpos=[ur'\]\](?:es|al|ales|istas?|almente)', ]) + #9
lema(ur'[Pp]urificaci_ó_n_o', xpos=[ur' \(Peñuelas', ur'\]\]es', ]) + #9
lema(ur'[Rr]ecepci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Rr]eglamentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Rr]ehabilitaci_ó_n_o') + #9
lema(ur'[Ss]aj_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[Vv]egetaci_ó_n_o', xpos=[ur'\]\]es', ]) + #9
lema(ur'[b]ill_ó_n_o', xpos=[ur' (?:of)', ur'\]\][a-zñ]+', ]) + #9
lema(ur'[d]ecisi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Pp]or) ') + #9
lema(ur'[Aa]dici_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Aa]doraci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Aa]leaci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Aa]mpliaci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Cc]alificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Cc]ant_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el|[Uu]n|[Cc]ada|[Ss]u) ', xpre=[ur'estatjants ', ], xpos=[ur' (?:Tech|Hall|Ticino)', ]) + #8
lema(ur'[Cc]ircunvoluci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Cc]olonizaci_ó_n_o', xpos=[ur'\.com', ]) + #8
lema(ur'[Cc]onstruc_ció_n_i[oó]', xpos=[ur' dun', ]) + #8
lema(ur'[Cc]onversaci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Cc]ooperaci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Dd]eterminaci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Dd]ivisi_ó_n [Pp]ol[ií]tica_o') + #8
lema(ur'[Ee]xplicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Ee]xplotaci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Ff]og_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Hh]ormig_ó_n_o', xpos=[ur'\]\](?:es|ad[ao]s?)', ]) + #8
lema(ur'[Ii]dentificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Mm]aldici_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Oo]bservaci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Oo]vaci_ó_n(?!\]|\.pe|\.com)_o') + #8
lema(ur'[Pp]acificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Pp]ort_ó_n_o', xpre=[ur'Pamela ', ], xpos=[ur' (?:d[\'’]|Down|Plantation)', ur'\]\]es', ]) + #8
lema(ur'[Pp]reparaci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Pp]reten_sio_nes_(?:sió|ci[oó])') + #8
lema(ur'[Pp]rivatizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Rr]epetici_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Rr]eproducci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Ss]axof_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Ss]educci_ó_n_o', xpos=[ur'\]\]es', ]) + #8
lema(ur'[Tt]elevisi_ó_n (?:por|[Ss]atelital|[Pp][uú]blica)_o') + #8
lema(ur'[Aa]firmaci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Aa]lmid_ó_n_o', xpre=[ur'Rosales ', ], xpos=[ur'\]\]es', ]) + #7
lema(ur'[Aa]nfitri_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Aa]pag_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Cc]irculaci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Cc]ompilaci_ó_n_o', xpos=[ur' curata', ur'\]\]es', ]) + #7
lema(ur'[Cc]onducci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Cc]onfirmaci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Cc]onspiraci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Cc]ontrataci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Dd]isoluci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Ee]laboraci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Ee]spol_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Ff]ortificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Gg]alp_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Ii]ncorporaci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Ii]ndemnizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Ll]ecci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Mm]arat_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ') + #7
lema(ur'[Mm]elocot_ó_n_o', xpos=[ur'\]\](?:es|er[ao]s?)', ]) + #7
lema(ur'[Oo]rientaci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Pp]roclamaci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Rr]ealizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Rr]ecreaci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Ss]uspen_sió_n_ci[oó]') + #7
lema(ur'[Tt]abl_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Tt]ap_ó_n_o', xpre=[ur'Michel ', ur'Serge ', ], xpos=[ur'\]\]es', ]) + #7
lema(ur'[Tt]entaci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Tt]ransmi_sió_n_ci[oó]') + #7
lema(ur'[Vv]otaci_ó_n_o', xpos=[ur'\]\]es', ]) + #7
lema(ur'[Aa]claraci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Aa]ctuaci_o_nes_ó') + #6
lema(ur'[Aa]gregaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Aa]limentaci_ó_n_o', xpos=[ur'(?:\]|\.es)', ]) + #6
lema(ur'[Cc]hicharr_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Cc]ircunvalaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Cc]olch_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Cc]omputaci_ó_n_o', xpos=[ur'(?:\]|\.facyt)', ]) + #6
lema(ur'[Cc]onclusi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #6
lema(ur'[Cc]ondecoraci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Cc]onformaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Cc]ontribuci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Dd]istinci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Dd]onaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Ee]d_i_ciones_') + #6
lema(ur'[Ee]lec_ció_n_i[oó]') + #6
lema(ur'[Ee]levaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Ee]moci_ó_n(?![\]0-9])_o') + #6
lema(ur'[Ee]xaltaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Ee]xcavaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Ee]xplosi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #6
lema(ur'[Ee]xpresi_ó_n_o', pre=ur'(?:[Dd]e|[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ', xpre=[ur'L\'', ], xpos=[ur' t', ur'\.tv', ]) + #6
lema(ur'[Ff]il_ó_n_o', xpre=[ur' du ', ur' i ', ur'Augustin ', ur'L\. ', ur'Larese ', ur'Rick ', ur'Robert ', ur'solenaskitan ', ], xpos=[ur' (?:Kmita|réduit)', ur'\]\]es', ]) + #6
lema(ur'[Ff]undici_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Ii]mitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Ii]mplementaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Ii]mportaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Ii]nvasi_ó_n_o', pre=ur'\b(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|otra|de|[Pp]rimera|[Ss]egunda|[Tt]ercera|[Ss]éptima) ') + #6
lema(ur'[Ii]nversi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Jj]ap_o_nes_ó') + #6
lema(ur'[Jj]uri_sdicció_n_dicci[oó]') + #6
lema(ur'[Mm]ansi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpos=[ur' House', ]) + #6
lema(ur'[Mm]ill_ó_n_o', pre=ur'([Mm]edio|[Uu]n|[Ee]l) ') + #6
lema(ur'[Mm]odificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Nn]umeraci_ó_n_o') + #6
lema(ur'[Nn]umeraci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Pp]remiaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Pp]retensi_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Pp]romulgaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Pp]rostituci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Rr]adiodifusi_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Rr]ecolecci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Rr]eencarnaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Rr]epresi_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Rr]evisi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #6
lema(ur'[Rr]otaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Ss]imulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Tt]if_ó_n_o', xpos=[ur'(?:[1-9\]])', ]) + #6
lema(ur'[Tt]raici_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Tt]ransfiguraci_ó_n_o', xpos=[ur'\]\]es', ]) + #6
lema(ur'[Vv]ersi_o_nes_ó') + #6
lema(ur'[Aa]creditaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Aa]decuaci_ó_n(?!\])_o') + #5
lema(ur'[Aa]dicci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Aa]gresi_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Aa]mputaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Aa]nunciaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Aa]plicaci_ó_n_o', pre=ur'(?:[Dd]e|[Ll]a|[Uu]na) ') + #5
lema(ur'[Bb]eatificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Cc]a_n_ciones_') + #5
lema(ur'[Cc]anci_o_nes_ó') + #5
lema(ur'[Cc]ertifi_cacio_nes_(?:a[cs]i[oó]|casi[oó]|cació)') + #5
lema(ur'[Cc]ircunscripci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Cc]odificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Cc]om__unicaciones_m') + #5
lema(ur'[Cc]ompresi_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Cc]onfiguraci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Cc]onmoci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Cc]onsolidaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Cc]ontaminaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Cc]ontradicci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Cc]orrec_c_iones_') + #5
lema(ur'[Dd]ecepci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Dd]ecoraci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Dd]efunci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Dd]etecci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Ee]corregi_ó_n(?!\])_o') + #5
lema(ur'[Ee]migraci_ó_n_o', xpos=[ur'(?:\.ca|\]\]es)', ]) + #5
lema(ur'[Ee]quipaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Ee]x_h_ibi(?:ó|ciones)_') + #5
lema(ur'[Ff]racci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Gg]laciaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Ii]_o_nes_ó') + #5
lema(ur'[Ii]mprovisaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Ii]n_strucció_n_trucci[oó]', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Ii]nten_cio_nes_si[oó]') + #5
lema(ur'[Ii]ntoxicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Ii]nvitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Jj]arr_ó_n_o', xpre=[ur'& ', ], xpos=[ur' (?:Collins|Vosburg)', ur'\]', ]) + #5
lema(ur'[Ll]egalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Mm]ont_ó_n_o', xpre=[ur'Julie ', ur'Leonard ', ur'de ', ], xpos=[ur' \(Eccles', ur'(?:\]|, (?:Canad[áa]|Gran|Bradley))', ]) + #5
lema(ur'[Mm]otivaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Mm]ultiplicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Mm]unici_ó_n_o', xpos=[ur'(?:\]|\.org)', ]) + #5
lema(ur'[Nn]egociaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Oo]bsesi_ó_n_o', xpre=[ur'l[\'’]', ], xpos=[ur'(?:\])', ]) + #5
lema(ur'[Pp]erdig_ó_n_o', xpre=[ur'Pierre ', ur'Troubadour ', ], xpos=[ur' d', ur'\]\][a-zñ]+', ]) + #5
lema(ur'[Pp]ersecuci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Pp]ez_ó_n_o', xpre=[ur'Andre ', ur'Jean-Baptiste ', ], xpos=[ur'\]\]es', ]) + #5
lema(ur'[Pp]lantaci_ó_n(?!\])_o') + #5
lema(ur'[Pp]ose_sió_n_ci[oó]') + #5
lema(ur'[Pp]ositr_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #5
lema(ur'[Pp]recisi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Cc]on| y| de) ', xpos=[ur' (?:Bass|Weapons)', ]) + #5
lema(ur'[Pp]revenci_ó_n_o') + #5
lema(ur'[Pp]roporci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Rr]ebeli_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Ee]sta|[Ee]sa|[Ee]n) ', xpos=[ur'(?:\]|\.org)', ]) + #5
lema(ur'[Rr]eorganizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Rr]eposici_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Rr]espiraci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Rr]etrotranspos_ó_n_o', xpos=[ur' superfamily', ur'\]\]es', ]) + #5
lema(ur'[Rr]eversi_ó_n_o', xpre=[ur';', ur'Series ', ur'bit ', ], xpos=[ur' to', ur'\]\]es', ]) + #5
lema(ur'[Ss]atisfacci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Ss]elecci_o_nes_ó') + #5
lema(ur'[Tt]ranscripci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Tt]urr_ó_n_o', xpos=[ur' Kofi', ur'\]\]es', ]) + #5
lema(ur'[Uu]tilizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #5
lema(ur'[Aa]cumulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Aa]dmisi_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Aa]dquisici_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Aa]lineaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Aa]lteraci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Aa]lusi_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Aa]luvi_ó_n_o', xpos=[ur'\]\](?:es|al|ales)', ]) + #4
lema(ur'[Aa]notaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Aa]par_i_ciones_a') + #4
lema(ur'[Aa]portaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Aa]tracci_ó_n_o', xpos=[ur'[\]3]', ]) + #4
lema(ur'[Aa]utomoci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Aa]utorizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Cc]apitulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Cc]aracterizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Cc]imarr_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpre=[ur'[Cc]ondado ', ur'[Mm]unicipio ', ], xpos=[ur' (?:Heritage|Cutoff)', ]) + #4
lema(ur'[Cc]o_nmemoració_n_(?:nmemoracio|memoraci[oó])', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Cc]ol__ecciones_l') + #4
lema(ur'[Cc]olocaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Cc]osmovisi_ó_n_o', xpos=[ur' des', ur'\]\]es', ]) + #4
lema(ur'[Cc]ulminaci_ó_n(?!\])_o') + #4
lema(ur'[Dd]egradaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Dd]eliberaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Dd]erivaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Dd]esamortizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Dd]esignaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Dd]etonaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Dd]isertaci_ó_n_o', xpos=[ur' physico', ur'\]\]es', ]) + #4
lema(ur'[Ee]lecci_o_nes_ó') + #4
lema(ur'[Ee]scalaf_ó_n(?!\])_o') + #4
lema(ur'[Ee]staci_o_nes_ó') + #4
lema(ur'[Ee]xpansi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ', xpos=[ur' (?:Opposing|pak)', ]) + #4
lema(ur'[Ee]xposi_ci_ones_(?:|sici|si)') + #4
lema(ur'[Ee]xpropiaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Ff]abricaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Ff]ermentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Ff]ijaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Ff]iliaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Ff]rustraci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Hh]abilitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Hh]omogen_eizació_n_(?:izaci[oó]|eizacio)') + #4
lema(ur'[Ii]mputaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Ii]n_n_ovaciones_') + #4
lema(ur'[Ii]n_s_cripciones_') + #4
lema(ur'[Ii]nclinaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Ii]nflexi_ó_n_o', xpre=[ur'and ', ur'd\'', ], xpos=[ur'\]\]es', ]) + #4
lema(ur'[Ii]nspecci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Ii]ntimidaci_ó_n(?!\])_o') + #4
lema(ur'[Ii]nvestigaci_o_nes_ó') + #4
lema(ur'[Jj]ubilaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Ll]ap_ó_n_o', xpre=[ur'Botaniques de ', ur'Gúdar\+Hazte ', ur'Parlons ', ur'\bDo ', ur'\bun ', ], xpos=[ur'\]\](?:as?|es)', ]) + #4
lema(ur'[Mm]anipulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Mm]edicaci_ó_n(?!\])_o') + #4
lema(ur'[Mm]el_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ', xpre=[ur'Saye ', ur'abbati ', ur'listado ', ur'musicales ', ], xpos=[ur' (?:Music|Kinenbi)', ur', Naver', ]) + #4
lema(ur'[Mm]otorizaci_ó_n(?!\])_o') + #4
lema(ur'[Nn]acionalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Nn]ormalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Oo]bligaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Pp]artici_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Pp]ensi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpre=[ur'Filles de ', ], xpos=[ur' des', ]) + #4
lema(ur'[Pp]ercepci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Pp]erfecci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Pp]orci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Pp]ropagaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Rr]adiaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Rr]eelecci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Rr]eestructuraci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Rr]egi_ó_n_o', pre=ur'(?:[Uu]na|[Cc]ada|[Ss]u) ', xpos=[ur' d\'Ambovombe', ]) + #4
lema(ur'[Rr]egionalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Rr]egulaci_ó_n_o', xpos=[ur'(?:[\]1])', ]) + #4
lema(ur'[Rr]eparaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Rr]estricci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Rr]oset_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Ss]ensaci_ó_n_o') + #4
lema(ur'[Ss]ensaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Ss]ustituci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Tt]ransfusi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #4
lema(ur'[Tt]raslaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Uu]nci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[Vv]entilaci_ó_n_o', xpre=[ur'Sagunto\'\', con libre', ], xpos=[ur'\]\]es', ]) + #4
lema(ur'[Vv]isitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #4
lema(ur'[b]id_ó_n_o', xpre=[ur'Ville ', ur'beau un ', ], xpos=[ur'\]\]es', ]) + #4
lema(ur'[p]ich_ó_n_o', xpos=[ur' quand', ur'\]\]es', ]) + #4
lema(ur'[r]ay_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpre=[ur'd\'', ], xpos=[ur' (?:croissant|de trois)', ]) + #4
lema(ur'[Aa]bdicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Aa]bolici_ó_n_o', xpre=[ur'pola ', ], xpos=[ur'\]\]es', ]) + #3
lema(ur'[Aa]bsorci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Aa]celeraci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Aa]djudicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Aa]gitaci_ó_n(?!\])_o') + #3
lema(ur'[Aa]glomeraci_ó_n_o', xpos=[ur' deu', ur'\]\]es', ]) + #3
lema(ur'[Aa]mbici_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Aa]nticipaci_ó_n(?!\])_o') + #3
lema(ur'[Aa]proximaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Aa]utomatizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Bb]odeg_ó_n(?!\])_o') + #3
lema(ur'[Cc]ampe_o_nes_ó') + #3
lema(ur'[Cc]anel_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Cc]apacitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Cc]ivilizaci_o_nes_ó') + #3
lema(ur'[Cc]oalici_o_nes_ó') + #3
lema(ur'[Cc]occi_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Cc]olec_c_iones_') + #3
lema(ur'[Cc]olisi_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Cc]ombusti_ó_n_o', pre=ur'(?:[Ll]a|[Dd]e) ', xpos=[ur' (?:et|en général)', ]) + #3
lema(ur'[Cc]omercializaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Cc]ompensaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Cc]ompetició_n__m?', xpos=[ur', reglamentacions', ]) + #3
lema(ur'[Cc]ond_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el|[Uu]n|[Cc]ada|[Ss]u) ', xpos=[ur' Clú', ]) + #3
lema(ur'[Cc]ondensaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Cc]ondici_ó_n_o', pre=ur'(?:[Ll]as?|[Uu]nas?|[Ss]us?) ') + #3
lema(ur'[Cc]onsagraci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Cc]onurbaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Cc]onversi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpos=[ur' (?:d|de l\'art|du|des)', ]) + #3
lema(ur'[Dd]ataci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Dd]educci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Dd]eformaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Dd]escalificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Dd]eserci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Dd]esolaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Dd]evastaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Dd]evoluci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Dd]icci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Dd]ilataci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Dd]iscusi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Dd]iversi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #3
lema(ur'[Dd]ominaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ee]dici_o_nes_ó') + #3
lema(ur'[Ee]lectrificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ee]mulaci_ó_n(?!\])_o') + #3
lema(ur'[Ee]ncuadernaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ee]numeraci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ee]quitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ee]rudici_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ee]xcomuni_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ee]xhibici_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ee]xpan_sió_n_ci[oó]') + #3
lema(ur'[Ff]acci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ff]acturaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ff]inanciaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Gg]al_ó_n_o', xpre=[ur'Ezio ', ur'Rémy ', ur'aventurero ', ], xpos=[ur' (?:hapus|lân)', ur'(?:\]|\'\' rebellion)', ]) + #3
lema(ur'[Gg]eolocalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Gg]uarnici_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Hh]ibridaci_ó_n(?!\])_o') + #3
lema(ur'[Ii]ndicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ii]nflaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ii]niciaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ii]nserci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ii]nsurrecci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ii]ntera_c_ciones_') + #3
lema(ur'[Ii]ntersecci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ii]rrigaci_ó_n(?!\])_o') + #3
lema(ur'[Ll]e_o_nes_ó') + #3
lema(ur'[Ll]ocaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Mm]ediaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Mm]ill_o_nes_ó') + #3
lema(ur'[Mm]oci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Mm]odulaci_ó_n(?!\])_o') + #3
lema(ur'[Nn]arraci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Nn]egaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Oo]ptimizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Oo]rdenaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Oo]xidaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Pp]enalizaci_ó_n(?!\])_o') + #3
lema(ur'[Pp]erdici_ó_n_o') + #3
lema(ur'[Pp]ist_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpre=[ur'Sinfonía ', ur'coup ', ], xpos=[ur', Honegger', ]) + #3
lema(ur'[Pp]oblaci_o_nes_ó') + #3
lema(ur'[Pp]reposici_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Pp]resentaci_o_nes_ó') + #3
lema(ur'[Pp]roliferaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Pp]ronunciaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Rr]atificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Rr]efundaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Rr]efutaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Rr]ei__vindicaciones_n') + #3
lema(ur'[Rr]eligi_ó_n [Cc]at[oó]lica_o') + #3
lema(ur'[Ss]alm_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ', xpre=[ur'templo ', ur'áerea ', ], xpos=[ur' (?:Bay|Leap|Chase)', ur' P\.', ]) + #3
lema(ur'[Ss]ecesi_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ss]if_ó_n(?!\])_o') + #3
lema(ur'[Ss]umisi_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Ss]upervisi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Bb]ajo) ', xpre=[ur'sous ', ], xpos=[ur', Tequivo', ur'\]\]es', ]) + #3
lema(ur'[Ss]uspensi_ó_n(?! d[\'’]armes)_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #3
lema(ur'[Tt]amp_ó_n_o', xpre=[ur'Zombie ', ur'[Ll]e ', ur'\bdu ', ], xpos=[ur' Disease', ur'\]\]es', ]) + #3
lema(ur'[Tt]el_ó_n_o', xpre=[ur'Anagyrus ', ur'Ginintuan ', ]) + #3
lema(ur'[Tt]ra_nsliteracio_nes_(?:sliteraci[oó]|nsliteració)') + #3
lema(ur'[Tt]racci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Vv]ariaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Vv]inculaci_ó_n_o', xpos=[ur'\]\]es', ]) + #3
lema(ur'[Vv]iolaci_o_nes_ó') + #3
lema(ur'[Vv]isualizaci_o_nes_ó') + #3
lema(ur'Gab_ó_n_o', pre=ur'(?:[Dd]e|[Ee]n) ', xpos=[ur' [Aa]irlines', ]) + #2
lema(ur'[Aa]bsoluci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Aa]ceptaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Aa]ctivaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Aa]d_aptació_n_pataci[oó]') + #2
lema(ur'[Aa]filiaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Aa]ler_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Aa]lfabetizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Aa]nexi_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Aa]nulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Aa]pelaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Aa]rgumentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Aa]scensi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #2
lema(ur'[Aa]tol_ó_n(?!\])_o') + #2
lema(ur'[Aa]udici_ó_n_o', xpos=[ur' Irritable', ur'\]\]es', ]) + #2
lema(ur'[Aa]utodeterminaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Bb]ot_o_nes_ó') + #2
lema(ur'[Cc]alefacci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Cc]allej_o_nes_ó') + #2
lema(ur'[Cc]alz_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Cc]analizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Cc]ancelaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Cc]anonizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Cc]añ_o_nes_ó') + #2
lema(ur'[Cc]lasificaci_o_nes_ó') + #2
lema(ur'[Cc]o_mposició_n_(?:npo[cs]i[cs]i[oó]|mpoci[cs]i[oó]|mposisi[oó])') + #2
lema(ur'[Cc]ol_o_nes_ó') + #2
lema(ur'[Cc]oloraci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Cc]omplicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Cc]omuni_ó_n_o', xpre=[ur'cathechismo de la ', ], xpos=[ur'(?:\]|\.org)', ]) + #2
lema(ur'[Cc]onciliaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Cc]onfes_io_nes_(?:si[oó]|ió)', xpos=[ur' sacerdotum', ]) + #2
lema(ur'[Cc]onjugaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Cc]ontenci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Cc]onvicci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Cc]oraz_o_nes_ó') + #2
lema(ur'[Cc]uraci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Dd]_o_nes_ó') + #2
lema(ur'[Dd]epredaci_ó_n(?!\])_o') + #2
lema(ur'[Dd]epuraci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Dd]erogaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Dd]esnutrici_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Dd]ivisi_o_nes_ó') + #2
lema(ur'[Dd]ivulgaci_ó_n_o', xpos=[ur'(?:\]\][a-zñ]+|\.famaf)', ]) + #2
lema(ur'[Dd]otaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ee]lectr_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #2
lema(ur'[Ee]mancipaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ee]speci_alizació_n(?!\]\])_(?:alizacio|lizaci[oó])') + #2
lema(ur'[Ee]specificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ee]vangelizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ee]x_cepció_n_epci[oó]') + #2
lema(ur'[Ee]xcreci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ee]xcursi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #2
lema(ur'[Ee]xportaci_o_nes_ó') + #2
lema(ur'[Ee]xtorsi_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ee]xtracci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ff]alsificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ff]iguraci_ó_n(?!\])_o') + #2
lema(ur'[Ff]ilmaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ff]iltraci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ff]loraci_ó_n(?!\])_o') + #2
lema(ur'[Ff]ormaci_o_nes_ó') + #2
lema(ur'[Ff]ragmentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ff]ricci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Gg]estaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Gg]lobalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Gg]rabaci_o_nes_ó') + #2
lema(ur'[Hh]ipertensi_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Hh]umillaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ii]maginaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ii]mplantaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ii]nacci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ii]nstalaci_o_nes_ó') + #2
lema(ur'[Ii]nstituci_o_nes_ó') + #2
lema(ur'[Ii]ntenci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ii]nteracci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ii]ntercesi_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ii]nterconexi_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ii]nterrogaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ii]nterrupci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ii]ntuici_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ii]nva_sio_nes_(?:ci[oó]|sió)') + #2
lema(ur'[Ii]nva_sió_nes_ci[oó]') + #2
lema(ur'[Ii]nvocaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ll]amentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ll]imitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ll]iquidaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ll]ocuci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Mm]alformaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Mm]asterizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Mm]editaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Mm]ejill_ó_n(?!\])_o') + #2
lema(ur'[Mm]odernizaci_ó_n_o', xpos=[ur'(?:\]|\.(?:cl|gob))', ]) + #2
lema(ur'[Mm]orri_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Mm]ovilizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Nn]ivelaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Oo]ca_s_ionando_c') + #2
lema(ur'[Oo]peraci_o_nes_ó') + #2
lema(ur'[Oo]rej_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Pp]erforaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Pp]ersonificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Pp]ostulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Pp]recauci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Pp]revisi_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Pp]roces_io_nes_(?:si[oó]|ió)') + #2
lema(ur'[Pp]roducci_o_nes_ó') + #2
lema(ur'[Pp]rohibici_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Pp]roposici_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Pp]ropulsi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ', xpos=[ur' (?:par |Photonique)', ]) + #2
lema(ur'[Pp]rovisi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #2
lema(ur'[Rr]aci_ó_n_o', xpos=[ur' kaj', ur'(?:\])', ]) + #2
lema(ur'[Rr]eactivaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Rr]eaparici_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Rr]ecesi_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Rr]eclamaci_ó_n(?!\])_o') + #2
lema(ur'[Rr]ecombinaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Rr]econciliaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Rr]ectificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Rr]egresi_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Rr]eimpresi_ó_n_o', xpre=[ur'5th ', ], xpos=[ur'\]\]es', ]) + #2
lema(ur'[Rr]eligi_ó_n_o', pre=ur'(?:[Uu]na|[Cc]ada|[Ss]u) ') + #2
lema(ur'[Rr]emisi_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Rr]emoci_ó_n(?!\])_o') + #2
lema(ur'[Rr]eplicaci_ó_n(?!\])_o') + #2
lema(ur'[Rr]estituci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ss]anaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ss]aturaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ss]ecci_o_nes_ó') + #2
lema(ur'[Ss]edimentaci_ó_n(?!\])_o') + #2
lema(ur'[Ss]egregaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ss]indicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ss]ubdivisi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #2
lema(ur'[Ss]ublevaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ss]ubordinaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ss]ubsecci_ó_n(?!\])_o') + #2
lema(ur'[Ss]uplicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ss]uscripci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Ss]ustentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Tt]elevi_sió_n_cio') + #2
lema(ur'[Tt]ensi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|cierta) ', xpos=[ur' (?:narrative|érotique)', ]) + #2
lema(ur'[Tt]ibur_o_nes_ó') + #2
lema(ur'[Tt]im_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ', xpos=[ur' (?:Screech|David|Menon|of)', ur'\]\]es', ]) + #2
lema(ur'[Tt]inci_ó_n(?!\])_o') + #2
lema(ur'[Tt]ransacci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Tt]ranslocaci_ó_n(?!\])_o') + #2
lema(ur'[Tt]ransportaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Uu]bicaci_o_nes_ó') + #2
lema(ur'[Vv]aloraci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Vv]ibraci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Vv]ocaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[Vv]ocalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #2
lema(ur'[g]asc_ó_n_o', xpre=[ur'Gentilòme ', ur'[Cc]atonet ', ur'[Cc]atonet ritme ', ur'[Ll]e ', ur'dialecte ', ur'gentilòme ', ur'ritme ', ], xpos=[ur' du\b', ur'"', ]) + #2
lema(ur'[t]ac_ó_n_o') + #2
lema(ur'[Aa]berraci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]breviaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]bstenci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]bstracci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]centuaci_ó_n(?!\])_o') + #1
lema(ur'[Aa]ctualizaci_o_nes_ó') + #1
lema(ur'[Aa]cumulaci_o_nes_ó') + #1
lema(ur'[Aa]cusaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]dopci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]fectaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]finaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]gnaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]gresi_o_nes_ó') + #1
lema(ur'[Aa]guij_o_nes_ó') + #1
lema(ur'[Aa]guij_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]locuci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]mputaci_o_nes_ó') + #1
lema(ur'[Aa]ntelaci_ó_n(?!\])_o') + #1
lema(ur'[Aa]prehensi_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]rp_ó_n(?!\])_o') + #1
lema(ur'[Aa]signaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]spiraci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Aa]utenticaci_ó_n(?!\])_o') + #1
lema(ur'[Aa]veriguaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Bb]al_o_nes_ó') + #1
lema(ur'[Bb]endici_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Bb]onificaci_o_nes_ó') + #1
lema(ur'[Bb]uf_o_nes_ó') + #1
lema(ur'[Cc]ant_ó_n_o', pre=ur'[Aa] ', xpre=[ur'franquicia ', ur'interpretar ', ur'permitió ', ], xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]aparaz_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]aptaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]ard_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpos=[ur' Walker', ]) + #1
lema(ur'[Cc]ard_ó_n_o', pre=ur'[Dd]e ', xpre=[ur'Armand ', ], xpos=[ur' Walker', ]) + #1
lema(ur'[Cc]ategorizaci_ó_n(?!\])_o') + #1
lema(ur'[Cc]entralizaci_ó_n(?!\])_o') + #1
lema(ur'[Cc]ertifi_cació_n_(?:a[cs]i[oó]|casi[oó])') + #1
lema(ur'[Cc]intur_o_nes_ó') + #1
lema(ur'[Cc]ircuncisi_ó_n_o', xpos=[ur' on\b', ur'\]\]es', ]) + #1
lema(ur'[Cc]ircunnavegaci_ó_n_o', xpos=[ur'\]\](?:es|al|ales)', ]) + #1
lema(ur'[Cc]oagulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]omisi_o_nes_ó') + #1
lema(ur'[Cc]ompeti_ció_n_tco') + #1
lema(ur'[Cc]omprensi_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]on_strucció_n_truccio') + #1
lema(ur'[Cc]oncatenaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]ondici_o_nes_ó') + #1
lema(ur'[Cc]onjunci_o_nes_ó') + #1
lema(ur'[Cc]onjunci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]onmutaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]onsternaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]onsumaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]ontemplaci_ó_n_o', xpre=[ur'Flor ', ], xpos=[ur'\]\][a-zñ]+', ]) + #1
lema(ur'[Cc]ontestaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]ontracci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]ontraindicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]ontribuci_o_nes_ó') + #1
lema(ur'[Cc]onversaci_o_nes_ó') + #1
lema(ur'[Cc]oproducci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]ord_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #1
lema(ur'[Cc]orrelaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]otizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Cc]reaci_o_nes_ó') + #1
lema(ur'[Dd]efinici_o_nes_ó') + #1
lema(ur'[Dd]eformaci_o_nes_ó') + #1
lema(ur'[Dd]egollaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]egradaci_o_nes_ó') + #1
lema(ur'[Dd]elimitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]emocratizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]emolici_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]emostraci_o_nes_ó') + #1
lema(ur'[Dd]eposici_o_nes_ó') + #1
lema(ur'[Dd]erivaci_o_nes_ó') + #1
lema(ur'[Dd]escentralizaci_ó_n_o', xpos=[ur'(?:\]\][a-zñ]+|\.gov)', ]) + #1
lema(ur'[Dd]escolonizaci_ó_n_o') + #1
lema(ur'[Dd]escomposici_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]esconexi_ó_n(?!\])_o') + #1
lema(ur'[Dd]esesperaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]eshidrataci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]esilusi_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]esintegraci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]esviaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]evaluaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]evastaci_o_nes_ó') + #1
lema(ur'[Dd]ifracci_ó_n(?!\])_o') + #1
lema(ur'[Dd]imensi_o_nes_ó') + #1
lema(ur'[Dd]iputaci_o_nes_ó') + #1
lema(ur'[Dd]irecci_o_nes_ó') + #1
lema(ur'[Dd]iscreci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]iscriminaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]istinci_o_nes_ó') + #1
lema(ur'[Dd]istracci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]iversificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Dd]uplicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ee]_o_nes_ó') + #1
lema(ur'[Ee]dific__aciones_i') + #1
lema(ur'[Ee]fusi_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ee]mis_io_nes_(?:sió|ió)') + #1
lema(ur'[Ee]misi_o_nes_ó') + #1
lema(ur'[Ee]moci_o_nes_ó') + #1
lema(ur'[Ee]ntonaci_ó_n(?!\])_o') + #1
lema(ur'[Ee]ntronizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ee]quivocaci_ó_n(?!\])_o') + #1
lema(ur'[Ee]scisi_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ee]specializaci_ó_n(?!\])_o') + #1
lema(ur'[Ee]speculaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ee]sterilizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ee]vacuaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ee]vacuaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ee]vocaci_ó_n(?!\])_o') + #1
lema(ur'[Ee]xacci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ee]xageraci_ó_n(?!\])_o') + #1
lema(ur'[Ee]xcavaci_o_nes_ó') + #1
lema(ur'[Ee]xclusi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #1
lema(ur'[Ee]xpectaci_ó_n(?!\])_o') + #1
lema(ur'[Ee]xplicaci_o_nes_ó') + #1
lema(ur'[Ee]xplo_sió_n_cio') + #1
lema(ur'[Ee]xposici_o_nes_ó') + #1
lema(ur'[Ee]xpresi_o_nes_ó') + #1
lema(ur'[Ee]xpulsi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpos=[ur' de los Moriscos', ur'\]\]es', ]) + #1
lema(ur'[Ff]acci_o_nes_ó') + #1
lema(ur'[Ff]ald_ó_n(?!\])_o') + #1
lema(ur'[Ff]ascinaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ff]iscalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ff]isi_ó_n_o', xpre=[ur'Celibe ', ], xpos=[ur' boy', ur'\]\]es', ]) + #1
lema(ur'[Ff]luctuaci_ó_n(?!\])_o') + #1
lema(ur'[Ff]onaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ff]orestaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ff]rancmas_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ff]unci_o_nes_ó') + #1
lema(ur'[Ff]undamentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Gg]ale_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #1
lema(ur'[Hh]alc_o_nes_ó') + #1
lema(ur'[Ii]lustrac__iones_c') + #1
lema(ur'[Ii]mplantaci_o_nes_ó') + #1
lema(ur'[Ii]mplicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]mprecisi_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]mpresi_o_nes_ó') + #1
lema(ur'[Ii]nducci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]nervaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]nfiltraci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]nhibici_o_nes_ó') + #1
lema(ur'[Ii]nhibici_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]nicializaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]nmediaci_ó_n_o', xpos=[ur' al Chaco', ur'\]\]es', ]) + #1
lema(ur'[Ii]nmolaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]nstrumentaci_o_nes_ó') + #1
lema(ur'[Ii]ntegraci_o_nes_ó') + #1
lema(ur'[Ii]ntensificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]ntermediaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]nternacionalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]nterrelaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]ntervenci_o_nes_ó') + #1
lema(ur'[Ii]nversi_o_nes_ó') + #1
lema(ur'[Ii]nyecci_o_nes_ó') + #1
lema(ur'[Ii]nyecci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]onizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]rradiaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ii]teraci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Jj]onr_o_nes_ó') + #1
lema(ur'[Jj]ubilaci_o_nes_ó') + #1
lema(ur'[Ll]adr_o_nes_ó') + #1
lema(ur'[Ll]evitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ll]iberalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ll]ist_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el|[Uu]n|[Cc]ada|[Ss]u) ', xpre=[ur'far ', ]) + #1
lema(ur'[Mm]aceraci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Mm]aduraci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Mm]anutenci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Mm]aquetaci_ó_n(?!\])_o') + #1
lema(ur'[Mm]at_o_nes_ó') + #1
lema(ur'[Mm]editaci_o_nes_ó') + #1
lema(ur'[Mm]egat_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpos=[ur' Hit', ]) + #1
lema(ur'[Mm]enci_o_nes_ó') + #1
lema(ur'[Mm]icrorregi_ó_n(?!\])_o') + #1
lema(ur'[Mm]ilitarizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Mm]isti_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Mm]orm_ó_n_o', pre=ur'(?:[Ee]l|[Uu]n|[Cc]ada|[Ss]u) ', xpre=[ur'Yu\'', ]) + #1
lema(ur'[Nn]aci_o_nes_ó') + #1
lema(ur'[Nn]otificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Oo]pini_o_nes_ó') + #1
lema(ur'[Oo]rganizaci_o_nes_ó') + #1
lema(ur'[Oo]rnamentaci_ó_n(?!\])_o') + #1
lema(ur'[Oo]scilaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Oo]stentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Pp]alpitaci_ó_n(?!\])_o') + #1
lema(ur'[Pp]antal_o_nes_ó') + #1
lema(ur'[Pp]atr_o_nes_ó') + #1
lema(ur'[Pp]ercusi_o_nes_ó') + #1
lema(ur'[Pp]eriodizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Pp]ermutaci_o_nes_ó') + #1
lema(ur'[Pp]ersonificaci_o_nes_ó') + #1
lema(ur'[Pp]etici_o_nes_ó') + #1
lema(ur'[Pp]lantaci_o_nes_ó') + #1
lema(ur'[Pp]oci_o_nes_ó') + #1
lema(ur'[Pp]olimerizaci_ó_n(?!\])_o') + #1
lema(ur'[Pp]ose_sio_nes_ci[oó]') + #1
lema(ur'[Pp]redicci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Pp]redicci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Pp]rescripci_ó_n(?!\])_o') + #1
lema(ur'[Pp]reselecci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Pp]revisualizaci_ó_n(?!\])_o') + #1
lema(ur'[Pp]roliferaci_o_nes_ó') + #1
lema(ur'[Pp]rovocaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Pp]udrici_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Pp]unz_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Rr]abi_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Rr]at_o_nes_ó') + #1
lema(ur'[Rr]ecordaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Rr]efacci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Rr]efracci_ó_n(?!\])_o') + #1
lema(ur'[Rr]egeneraci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Rr]egi_o_nes_ó') + #1
lema(ur'[Rr]egularizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Rr]elaci_o_nes_ó') + #1
lema(ur'[Rr]endici_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Rr]engl_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Rr]epercusi_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Rr]epoblaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Rr]eproducci_o_nes_ó') + #1
lema(ur'[Rr]eputaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Rr]estricci_o_nes_ó') + #1
lema(ur'[Rr]euni_o_nes_ó') + #1
lema(ur'[Rr]everberaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Rr]evoluci_o_nes_ó') + #1
lema(ur'[Ss]edici_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ss]esi_o_nes_ó') + #1
lema(ur'[Ss]eñalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ss]oluci_o_nes_ó') + #1
lema(ur'[Ss]ubestaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ss]uperaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ss]uperposici_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ss]uperstici_ó_n(?!\])_o') + #1
lema(ur'[Ss]upresi_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Tt]ap_o_nes_ó') + #1
lema(ur'[Tt]ej_ó_n_o', pre=ur'(?:[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #1
lema(ur'[Tt]ej_ó_n_o', pre=ur'[Ee]l ', xpos=[ur' Ranch', ]) + #1
lema(ur'[Tt]elecomunicaci_o_nes_ó') + #1
lema(ur'[Tt]ensi_o_nes_ó') + #1
lema(ur'[Tt]erminaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Tt]ra_smisió_n_nsmicio') + #1
lema(ur'[Tt]radici_o_nes_ó') + #1
lema(ur'[Tt]ransformaci_o_nes_ó') + #1
lema(ur'[Tt]ransmigraci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Tt]ransportaci_o_nes_ó') + #1
lema(ur'[Tt]áx_ó_n(?!\])_o') + #1
lema(ur'[Vv]acunaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Vv]ag_o_nes_ó') + #1
lema(ur'[Vv]ibraci_o_nes_ó') + #1
lema(ur'[Vv]isualizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[b]ret_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpre=[ur'\bd’', ], xpos=[ur' très', ]) + #1
lema(ur'[m]at_ó_n_o', xpos=[ur' BB1200', ur'\]\]es', ]) + #1
# lema(ur'[Aa]daptaci_o_nes_ó') + #0
# lema(ur'[Cc]onfecci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]isyunci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]nfracci_o_nes_ó') + #0
# lema(ur'[Nn]ominaci_o_nes_ó') + #0
# lema(ur'[Oo]ca_sió_n_ci[oó]') + #0
# lema(ur'[Pp]enetraci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]ecomendaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]epetici_o_nes_ó') + #0
# lema(ur'[Ss]ujeci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Tt]ransmisi_o_nes_ó') + #0
# lema(ur'[Aa]bdicaci_o_nes_ó') + #0
# lema(ur'[Aa]bducci_o_nes_ó') + #0
# lema(ur'[Aa]berraci_o_nes_ó') + #0
# lema(ur'[Aa]blaci_o_nes_ó') + #0
# lema(ur'[Aa]blaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]bluci_o_nes_ó') + #0
# lema(ur'[Aa]bluci_ó_n(?!\])_o') + #0
# lema(ur'[Aa]bolici_o_nes_ó') + #0
# lema(ur'[Aa]bominaci_o_nes_ó') + #0
# lema(ur'[Aa]bominaci_ó_n(?!\])_o') + #0
# lema(ur'[Aa]breviaci_o_nes_ó') + #0
# lema(ur'[Aa]bsoluci_o_nes_ó') + #0
# lema(ur'[Aa]bsorci_o_nes_ó') + #0
# lema(ur'[Aa]bstenci_o_nes_ó') + #0
# lema(ur'[Aa]bstracci_o_nes_ó') + #0
# lema(ur'[Aa]cci_o_nes_ó') + #0
# lema(ur'[Aa]celeraci_o_nes_ó') + #0
# lema(ur'[Aa]centuaci_o_nes_ó') + #0
# lema(ur'[Aa]cepci_o_nes_ó') + #0
# lema(ur'[Aa]cepci_ó_n(?!\])_o') + #0
# lema(ur'[Aa]ceptaci_o_nes_ó') + #0
# lema(ur'[Aa]clamaci_o_nes_ó') + #0
# lema(ur'[Aa]clamaci_ó_n(?!\])_o') + #0
# lema(ur'[Aa]claraci_o_nes_ó') + #0
# lema(ur'[Aa]cotaci_o_nes_ó') + #0
# lema(ur'[Aa]cotaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]creditaci_o_nes_ó') + #0
# lema(ur'[Aa]ctivaci_o_nes_ó') + #0
# lema(ur'[Aa]cusaci_o_nes_ó') + #0
# lema(ur'[Aa]cuñaci_o_nes_ó') + #0
# lema(ur'[Aa]cuñaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]daptaci_o_nes_ó') + #0
# lema(ur'[Aa]decuaci_o_nes_ó') + #0
# lema(ur'[Aa]dhesi_o_nes_ó') + #0
# lema(ur'[Aa]dicci_o_nes_ó') + #0
# lema(ur'[Aa]dici_o_nes_ó') + #0
# lema(ur'[Aa]divinaci_o_nes_ó') + #0
# lema(ur'[Aa]divinaci_ó_n(?!\])_o') + #0
# lema(ur'[Aa]djudicaci_o_nes_ó') + #0
# lema(ur'[Aa]dministraci_o_nes_ó') + #0
# lema(ur'[Aa]dmiraci_o_nes_ó') + #0
# lema(ur'[Aa]dopci_o_nes_ó') + #0
# lema(ur'[Aa]doraci_o_nes_ó') + #0
# lema(ur'[Aa]dquisici_o_nes_ó') + #0
# lema(ur'[Aa]dscripci_o_nes_ó') + #0
# lema(ur'[Aa]dscripci_ó_n(?!\])_o') + #0
# lema(ur'[Aa]dulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]dvocaci_o_nes_ó') + #0
# lema(ur'[Aa]fecci_o_nes_ó') + #0
# lema(ur'[Aa]fecci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]fectaci_o_nes_ó') + #0
# lema(ur'[Aa]fici_o_nes_ó') + #0
# lema(ur'[Aa]filiaci_o_nes_ó') + #0
# lema(ur'[Aa]finaci_o_nes_ó') + #0
# lema(ur'[Aa]firmaci_o_nes_ó') + #0
# lema(ur'[Aa]flicci_o_nes_ó') + #0
# lema(ur'[Aa]floraci_o_nes_ó') + #0
# lema(ur'[Aa]gitaci_o_nes_ó') + #0
# lema(ur'[Aa]glomeraci_o_nes_ó') + #0
# lema(ur'[Aa]glutinaci_o_nes_ó') + #0
# lema(ur'[Aa]glutinaci_ó_n(?!\])_o') + #0
# lema(ur'[Aa]gregaci_o_nes_ó') + #0
# lema(ur'[Aa]grupaci_o_nes_ó') + #0
# lema(ur'[Aa]ireaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]leaci_o_nes_ó') + #0
# lema(ur'[Aa]legaci_o_nes_ó') + #0
# lema(ur'[Aa]legaci_ó_n(?!\])_o') + #0
# lema(ur'[Aa]ler_o_nes_ó') + #0
# lema(ur'[Aa]lfabetizaci_o_nes_ó') + #0
# lema(ur'[Aa]lgod_o_nes_ó') + #0
# lema(ur'[Aa]lienaci_o_nes_ó') + #0
# lema(ur'[Aa]lienaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]limentaci_o_nes_ó') + #0
# lema(ur'[Aa]lineaci_o_nes_ó') + #0
# lema(ur'[Aa]lmid_o_nes_ó') + #0
# lema(ur'[Aa]locuci_o_nes_ó') + #0
# lema(ur'[Aa]lteraci_o_nes_ó') + #0
# lema(ur'[Aa]lternaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]lucinaci_o_nes_ó') + #0
# lema(ur'[Aa]lusi_o_nes_ó') + #0
# lema(ur'[Aa]luvi_o_nes_ó') + #0
# lema(ur'[Aa]mbici_o_nes_ó') + #0
# lema(ur'[Aa]mbientaci_o_nes_ó') + #0
# lema(ur'[Aa]mbientaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]monestaci_o_nes_ó') + #0
# lema(ur'[Aa]monestaci_ó_n(?!\])_o') + #0
# lema(ur'[Aa]mpliaci_o_nes_ó') + #0
# lema(ur'[Aa]mplificaci_o_nes_ó') + #0
# lema(ur'[Aa]mplificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]nfitri_o_nes_ó') + #0
# lema(ur'[Aa]nglosaj_o_nes_ó') + #0
# lema(ur'[Aa]ni_o_nes_ó') + #0
# lema(ur'[Aa]nidaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]nimaci_o_nes_ó') + #0
# lema(ur'[Aa]niquilaci_o_nes_ó') + #0
# lema(ur'[Aa]niquilaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]notaci_o_nes_ó') + #0
# lema(ur'[Aa]ntelaci_o_nes_ó') + #0
# lema(ur'[Aa]nticipaci_o_nes_ó') + #0
# lema(ur'[Aa]nulaci_o_nes_ó') + #0
# lema(ur'[Aa]pag_o_nes_ó') + #0
# lema(ur'[Aa]parici_o_nes_ó') + #0
# lema(ur'[Aa]pelaci_o_nes_ó') + #0
# lema(ur'[Aa]plicaci_o_nes_ó') + #0
# lema(ur'[Aa]portaci_o_nes_ó') + #0
# lema(ur'[Aa]preciaci_o_nes_ó') + #0
# lema(ur'[Aa]preciaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]probaci_o_nes_ó') + #0
# lema(ur'[Aa]propiaci_o_nes_ó') + #0
# lema(ur'[Aa]propiaci_ó_n(?!\])_o') + #0
# lema(ur'[Aa]proximaci_o_nes_ó') + #0
# lema(ur'[Aa]rgumentaci_o_nes_ó') + #0
# lema(ur'[Aa]rp_o_nes_ó') + #0
# lema(ur'[Aa]rticulaci_o_nes_ó') + #0
# lema(ur'[Aa]scensi_o_nes_ó') + #0
# lema(ur'[Aa]serci_o_nes_ó') + #0
# lema(ur'[Aa]serci_ó_n(?!\])_o') + #0
# lema(ur'[Aa]severaci_o_nes_ó') + #0
# lema(ur'[Aa]severaci_ó_n(?!\])_o') + #0
# lema(ur'[Aa]signaci_o_nes_ó') + #0
# lema(ur'[Aa]similaci_o_nes_ó') + #0
# lema(ur'[Aa]similaci_ó_n(?!\])_o') + #0
# lema(ur'[Aa]sociaci_o_nes_ó') + #0
# lema(ur'[Aa]spiraci_o_nes_ó') + #0
# lema(ur'[Aa]tenci_o_nes_ó') + #0
# lema(ur'[Aa]tenuaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]tol_o_nes_ó') + #0
# lema(ur'[Aa]tracci_o_nes_ó') + #0
# lema(ur'[Aa]tribuci_o_nes_ó') + #0
# lema(ur'[Aa]tribuci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]udici_o_nes_ó') + #0
# lema(ur'[Aa]utenticaci_o_nes_ó') + #0
# lema(ur'[Aa]utocami_o_nes_ó') + #0
# lema(ur'[Aa]utocompasi_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]utodestrucci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Aa]utodeterminaci_o_nes_ó') + #0
# lema(ur'[Aa]utomatizaci_o_nes_ó') + #0
# lema(ur'[Aa]utor_regulació_n_egulacio') + #0
# lema(ur'[Aa]utorizaci_o_nes_ó') + #0
# lema(ur'[Aa]utrig_o_nes_ó') + #0
# lema(ur'[Aa]utrig_ó_n(?!\])_o') + #0
# lema(ur'[Aa]veriguaci_o_nes_ó') + #0
# lema(ur'[Aa]vi_o_nes_ó') + #0
# lema(ur'[Aa]x_o_n(?:es|al|ales)_ó') + #0
# lema(ur'[Aa]x_ó_n_o', xpre=[ur'Gen\. ', ur'Short ', ], xpos=[ur' (?:\(?of |compañía|initial|collaterals|guidance|Films|Jump)', ur'[\'\]]', ]) + #0
# lema(ur'[Bb]alc_o_nes_ó') + #0
# lema(ur'[Bb]ar_o_nes_ó') + #0
# lema(ur'[Bb]ar_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]l?) ', xpre=[ur'\bpar ', ur'acuerdo ', ], xpos=[ur' (?:Michele|Reiter|Cohen|Corbin|Wolman|Samedi|Zemo|Gattoni)', ur', el', ]) + #0
# lema(ur'[Bb]ari_o_nes_ó') + #0
# lema(ur'[Bb]ari_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpre=[ur'detrás ', ]) + #0
# lema(ur'[Bb]arrac_o_nes_ó') + #0
# lema(ur'[Bb]arrac_ó_n(?!\])_o') + #0
# lema(ur'[Bb]ast_o_nes_ó') + #0
# lema(ur'[Bb]asti_o_nes_ó') + #0
# lema(ur'[Bb]asti_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #0
# lema(ur'[Bb]atall_o_nes_ó') + #0
# lema(ur'[Bb]eatificaci_o_nes_ó') + #0
# lema(ur'[Bb]endici_o_nes_ó') + #0
# lema(ur'[Bb]id_o_nes_ó') + #0
# lema(ur'[Bb]ifurcaci_o_nes_ó') + #0
# lema(ur'[Bb]ifurcaci_ó_n(?!\])_o') + #0
# lema(ur'[Bb]ill_o_nes_ó') + #0
# lema(ur'[Bb]las_o_nes_ó') + #0
# lema(ur'[Bb]las_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #0
# lema(ur'[Bb]odeg_o_nes_ó') + #0
# lema(ur'[Bb]omb_o_nes_ó') + #0
# lema(ur'[Bb]onificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Bb]oquer_o_nes_ó') + #0
# lema(ur'[Bb]orb_o_nes_ó') + #0
# lema(ur'[Bb]os_o_nes_ó') + #0
# lema(ur'[Bb]os_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #0
# lema(ur'[Bb]ret_o_nes_ó') + #0
# lema(ur'[Bb]uz_o_nes_ó') + #0
# lema(ur'[Cc]aj_o_nes_ó') + #0
# lema(ur'[Cc]alefacci_o_nes_ó') + #0
# lema(ur'[Cc]alibraci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]alificaci_o_nes_ó') + #0
# lema(ur'[Cc]alz_o_nes_ó') + #0
# lema(ur'[Cc]amale_o_nes_ó') + #0
# lema(ur'[Cc]amar_o_nes_ó') + #0
# lema(ur'[Cc]amell_o_nes_ó') + #0
# lema(ur'[Cc]amell_ó_n(?!\])_o') + #0
# lema(ur'[Cc]ami_o_nes_ó') + #0
# lema(ur'[Cc]analizaci_o_nes_ó') + #0
# lema(ur'[Cc]ancelaci_o_nes_ó') + #0
# lema(ur'[Cc]anel_o_nes_ó') + #0
# lema(ur'[Cc]apacitaci_o_nes_ó') + #0
# lema(ur'[Cc]aparaz_o_nes_ó') + #0
# lema(ur'[Cc]aparr_o_nes_ó') + #0
# lema(ur'[Cc]apitalizaci_o_nes_ó') + #0
# lema(ur'[Cc]apitalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]apitulaci_o_nes_ó') + #0
# lema(ur'[Cc]aptaci_o_nes_ó') + #0
# lema(ur'[Cc]aracterizaci_o_nes_ó') + #0
# lema(ur'[Cc]arb_o_nes_ó') + #0
# lema(ur'[Cc]arburaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]ard_o_nes_ó') + #0
# lema(ur'[Cc]art_o_nes_ó') + #0
# lema(ur'[Cc]art_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #0
# lema(ur'[Cc]aset_o_nes_ó') + #0
# lema(ur'[Cc]aset_ó_n(?!\])_o') + #0
# lema(ur'[Cc]ategorizaci_o_nes_ó') + #0
# lema(ur'[Cc]ati_o_nes_ó') + #0
# lema(ur'[Cc]elebraci_o_nes_ó') + #0
# lema(ur'[Cc]entralizaci_o_nes_ó') + #0
# lema(ur'[Cc]enturi_o_nes_ó') + #0
# lema(ur'[Cc]enturi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #0
# lema(ur'[Cc]esi_o_nes_ó') + #0
# lema(ur'[Cc]hampiñ_o_nes_ó') + #0
# lema(ur'[Cc]hicharr_o_nes_ó') + #0
# lema(ur'[Cc]icl_o_nes_ó') + #0
# lema(ur'[Cc]imarr_o_nes_ó') + #0
# lema(ur'[Cc]imentaci_o_nes_ó') + #0
# lema(ur'[Cc]imentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]irculaci_o_nes_ó') + #0
# lema(ur'[Cc]ircunnavegaci_o_nes_ó') + #0
# lema(ur'[Cc]ircunscripci_o_nes_ó') + #0
# lema(ur'[Cc]ircunvalaci_o_nes_ó') + #0
# lema(ur'[Cc]itaci_o_nes_ó') + #0
# lema(ur'[Cc]itaci_ó_n(?!\])_o') + #0
# lema(ur'[Cc]lonaci_o_nes_ó') + #0
# lema(ur'[Cc]lonaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]o_mposicio_nes_(?:npo[cs]i[cs]i[oó]|mpoci[cs]i[oó]|mposisi[oó]|mposició)') + #0
# lema(ur'[Cc]o_operació_n_peracio') + #0
# lema(ur'[Cc]oacci_o_nes_ó') + #0
# lema(ur'[Cc]oacci_ó_n(?!\])_o') + #0
# lema(ur'[Cc]oagulaci_o_nes_ó') + #0
# lema(ur'[Cc]occi_o_nes_ó') + #0
# lema(ur'[Cc]od_o_nes_ó') + #0
# lema(ur'[Cc]odificaci_o_nes_ó') + #0
# lema(ur'[Cc]oj_o_nes_ó') + #0
# lema(ur'[Cc]oj_ó_n(?!\])_o') + #0
# lema(ur'[Cc]olaboraci_o_nes_ó') + #0
# lema(ur'[Cc]olaci_o_nes_ó') + #0
# lema(ur'[Cc]olaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]olch_o_nes_ó') + #0
# lema(ur'[Cc]olecci_o_nes_ó') + #0
# lema(ur'[Cc]olocaci_o_nes_ó') + #0
# lema(ur'[Cc]olonizaci_o_nes_ó') + #0
# lema(ur'[Cc]oloraci_o_nes_ó') + #0
# lema(ur'[Cc]ombinaci_o_nes_ó') + #0
# lema(ur'[Cc]omercializaci_o_nes_ó') + #0
# lema(ur'[Cc]omparaci_o_nes_ó') + #0
# lema(ur'[Cc]ompensaci_o_nes_ó') + #0
# lema(ur'[Cc]ompetic_ió_n_cio') + #0
# lema(ur'[Cc]ompetici_o_nes_ó') + #0
# lema(ur'[Cc]ompilaci_o_nes_ó') + #0
# lema(ur'[Cc]omplicaci_o_nes_ó') + #0
# lema(ur'[Cc]omposici_o_nes_ó') + #0
# lema(ur'[Cc]ompresi_o_nes_ó') + #0
# lema(ur'[Cc]omprobaci_o_nes_ó') + #0
# lema(ur'[Cc]omprobaci_ó_n(?!\])_o') + #0
# lema(ur'[Cc]omputaci_o_nes_ó') + #0
# lema(ur'[Cc]omunicaci_o_nes_ó') + #0
# lema(ur'[Cc]on_struccio_nes_trucció') + #0
# lema(ur'[Cc]oncatenaci_o_nes_ó') + #0
# lema(ur'[Cc]oncentraci_o_nes_ó') + #0
# lema(ur'[Cc]oncepci_o_nes_ó') + #0
# lema(ur'[Cc]oncesi_o_nes_ó') + #0
# lema(ur'[Cc]onciliaci_o_nes_ó') + #0
# lema(ur'[Cc]onclusi_o_nes_ó') + #0
# lema(ur'[Cc]oncreci_o_nes_ó') + #0
# lema(ur'[Cc]oncreci_ó_n(?!\])_o') + #0
# lema(ur'[Cc]ond_o_nes_ó') + #0
# lema(ur'[Cc]ondecoraci_o_nes_ó') + #0
# lema(ur'[Cc]ondeferaci_o_nes_ó') + #0
# lema(ur'[Cc]ondeferaci_ó_n_o') + #0
# lema(ur'[Cc]ondenaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]ondensaci_o_nes_ó') + #0
# lema(ur'[Cc]onducci_o_nes_ó') + #0
# lema(ur'[Cc]onecci_o_nes_ó') + #0
# lema(ur'[Cc]onexi_o_nes_ó') + #0
# lema(ur'[Cc]onfabulaci_o_nes_ó') + #0
# lema(ur'[Cc]onfabulaci_ó_n(?!\])_o') + #0
# lema(ur'[Cc]onfecci_o_nes_ó') + #0
# lema(ur'[Cc]onfecci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]onfederaci_o_nes_ó') + #0
# lema(ur'[Cc]onfiguraci_o_nes_ó') + #0
# lema(ur'[Cc]onfirmaci_o_nes_ó') + #0
# lema(ur'[Cc]onfiscaci_o_nes_ó') + #0
# lema(ur'[Cc]onfiscaci_ó_n(?!\])_o') + #0
# lema(ur'[Cc]onformaci_o_nes_ó') + #0
# lema(ur'[Cc]onfrontaci_o_nes_ó') + #0
# lema(ur'[Cc]onfrontaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]onfusi_o_nes_ó') + #0
# lema(ur'[Cc]onfusi_ó_n_o', pre=ur'(?:[Uu]na|[Cc]ada|[Ss]u) ') + #0
# lema(ur'[Cc]ongelaci_o_nes_ó') + #0
# lema(ur'[Cc]ongelaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]ongregaci_o_nes_ó') + #0
# lema(ur'[Cc]onjugaci_o_nes_ó') + #0
# lema(ur'[Cc]onmemoraci_o_nes_ó') + #0
# lema(ur'[Cc]onmoci_o_nes_ó') + #0
# lema(ur'[Cc]onmutaci_o_nes_ó') + #0
# lema(ur'[Cc]onnotaci_o_nes_ó') + #0
# lema(ur'[Cc]onnotaci_ó_n(?!\])_o') + #0
# lema(ur'[Cc]onsagraci_o_nes_ó') + #0
# lema(ur'[Cc]onsecuci_o_nes_ó') + #0
# lema(ur'[Cc]onsecuci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]onservaci_o_nes_ó') + #0
# lema(ur'[Cc]onsideraci_o_nes_ó') + #0
# lema(ur'[Cc]onsolidaci_o_nes_ó') + #0
# lema(ur'[Cc]onspiraci_o_nes_ó') + #0
# lema(ur'[Cc]onstelaci_o_nes_ó') + #0
# lema(ur'[Cc]onstituci_o_nes_ó') + #0
# lema(ur'[Cc]onsumici_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]ontaminaci_o_nes_ó') + #0
# lema(ur'[Cc]ontemplaci_o_nes_ó') + #0
# lema(ur'[Cc]ontenci_o_nes_ó') + #0
# lema(ur'[Cc]ontestaci_o_nes_ó') + #0
# lema(ur'[Cc]ontinuaci_o_nes_ó') + #0
# lema(ur'[Cc]ontracci_o_nes_ó') + #0
# lema(ur'[Cc]ontradicci_o_nes_ó') + #0
# lema(ur'[Cc]ontraindicaci_o_nes_ó') + #0
# lema(ur'[Cc]ontraposici_o_nes_ó') + #0
# lema(ur'[Cc]ontraposici_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]ontrataci_o_nes_ó') + #0
# lema(ur'[Cc]ontravenci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]ontusi_o_nes_ó') + #0
# lema(ur'[Cc]ontusi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #0
# lema(ur'[Cc]onurbaci_o_nes_ó') + #0
# lema(ur'[Cc]onvecci_o_nes_ó') + #0
# lema(ur'[Cc]onvecci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]onvenci_o_nes_ó') + #0
# lema(ur'[Cc]onversi_o_nes_ó') + #0
# lema(ur'[Cc]onvicci_o_nes_ó') + #0
# lema(ur'[Cc]onvocaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]onvulsi_o_nes_ó') + #0
# lema(ur'[Cc]ooperaci_o_nes_ó') + #0
# lema(ur'[Cc]oordinaci_o_nes_ó') + #0
# lema(ur'[Cc]oproducci_o_nes_ó') + #0
# lema(ur'[Cc]ord_o_nes_ó') + #0
# lema(ur'[Cc]oronaci_o_nes_ó') + #0
# lema(ur'[Cc]orporaci_o_nes_ó') + #0
# lema(ur'[Cc]orrecci_o_nes_ó') + #0
# lema(ur'[Cc]orrelaci_o_nes_ó') + #0
# lema(ur'[Cc]orrupci_o_nes_ó') + #0
# lema(ur'[Cc]otiled_o_nes_ó') + #0
# lema(ur'[Cc]otiled_ó_n(?!\])_o') + #0
# lema(ur'[Cc]otizaci_o_nes_ó') + #0
# lema(ur'[Cc]ristalizaci_o_nes_ó') + #0
# lema(ur'[Cc]ristalizaci_ó_n(?!\])_o') + #0
# lema(ur'[Cc]ristianizaci_o_nes_ó') + #0
# lema(ur'[Cc]ristianizaci_ó_n(?!\])_o') + #0
# lema(ur'[Cc]rucifixi_o_nes_ó') + #0
# lema(ur'[Cc]ualificaci_o_nes_ó') + #0
# lema(ur'[Cc]ualificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]uantificaci_o_nes_ó') + #0
# lema(ur'[Cc]uantificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Cc]uaterni_o_nes_ó') + #0
# lema(ur'[Cc]uaterni_ó_n(?!\])_o') + #0
# lema(ur'[Cc]uesti_o_nes_ó') + #0
# lema(ur'[Cc]ulminaci_o_nes_ó') + #0
# lema(ur'[Cc]uraci_o_nes_ó') + #0
# lema(ur'[Dd]ataci_o_nes_ó') + #0
# lema(ur'[Dd]ecapitaci_o_nes_ó') + #0
# lema(ur'[Dd]ecapitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]ecepci_o_nes_ó') + #0
# lema(ur'[Dd]ecisi_o_nes_ó') + #0
# lema(ur'[Dd]eclaraci_o_nes_ó') + #0
# lema(ur'[Dd]eclinaci_o_nes_ó') + #0
# lema(ur'[Dd]eclinaci_ó_n(?!\])_o') + #0
# lema(ur'[Dd]ecocci_o_nes_ó') + #0
# lema(ur'[Dd]ecodificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]ecoloraci_o_nes_ó') + #0
# lema(ur'[Dd]ecoraci_o_nes_ó') + #0
# lema(ur'[Dd]edicaci_o_nes_ó') + #0
# lema(ur'[Dd]educci_o_nes_ó') + #0
# lema(ur'[Dd]efecci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]eforestaci_o_nes_ó') + #0
# lema(ur'[Dd]eforestaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]efunci_o_nes_ó') + #0
# lema(ur'[Dd]egeneraci_o_nes_ó') + #0
# lema(ur'[Dd]egeneraci_ó_n_o', xpos=[ur' Rock', ur'[\]]', ]) + #0
# lema(ur'[Dd]egustaci_o_nes_ó') + #0
# lema(ur'[Dd]egustaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]elegaci_o_nes_ó') + #0
# lema(ur'[Dd]eliberaci_o_nes_ó') + #0
# lema(ur'[Dd]elimitaci_o_nes_ó') + #0
# lema(ur'[Dd]emarcaci_o_nes_ó') + #0
# lema(ur'[Dd]emocratizaci_o_nes_ó') + #0
# lema(ur'[Dd]emolici_o_nes_ó') + #0
# lema(ur'[Dd]enegaci_o_nes_ó') + #0
# lema(ur'[Dd]enegaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]enominaci_o_nes_ó') + #0
# lema(ur'[Dd]epilaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]eportaci_o_nes_ó') + #0
# lema(ur'[Dd]eportaci_ó_n(?!\])_o') + #0
# lema(ur'[Dd]eposici_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]epravaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]epreciaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]epredaci_o_nes_ó') + #0
# lema(ur'[Dd]epresi_o_nes_ó') + #0
# lema(ur'[Dd]epuraci_o_nes_ó') + #0
# lema(ur'[Dd]erogaci_o_nes_ó') + #0
# lema(ur'[Dd]esambiguaci_o_nes_ó') + #0
# lema(ur'[Dd]esamortizaci_o_nes_ó') + #0
# lema(ur'[Dd]esaparici_o_nes_ó') + #0
# lema(ur'[Dd]esaprobaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]escalificaci_o_nes_ó') + #0
# lema(ur'[Dd]escamaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]escentralizaci_o_nes_ó') + #0
# lema(ur'[Dd]escomposici_o_nes_ó') + #0
# lema(ur'[Dd]escompresi_ó_n_o') + #0
# lema(ur'[Dd]esconexi_o_nes_ó') + #0
# lema(ur'[Dd]escripci_o_nes_ó') + #0
# lema(ur'[Dd]eserci_o_nes_ó') + #0
# lema(ur'[Dd]esesperaci_o_nes_ó') + #0
# lema(ur'[Dd]esfiguraci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]eshidrataci_o_nes_ó') + #0
# lema(ur'[Dd]esignaci_o_nes_ó') + #0
# lema(ur'[Dd]esinfecci_o_nes_ó') + #0
# lema(ur'[Dd]esinfecci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]esinformaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]esintegraci_o_nes_ó') + #0
# lema(ur'[Dd]esintoxicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]esmembraci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]esmoralizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]esnutrici_o_nes_ó') + #0
# lema(ur'[Dd]espoblaci_o_nes_ó') + #0
# lema(ur'[Dd]espoblaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]estilaci_o_nes_ó') + #0
# lema(ur'[Dd]estilaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]estinaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]estituci_o_nes_ó') + #0
# lema(ur'[Dd]estrucci_o_nes_ó') + #0
# lema(ur'[Dd]esuni_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]esviaci_o_nes_ó') + #0
# lema(ur'[Dd]esvinculaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]etecci_o_nes_ó') + #0
# lema(ur'[Dd]etenci_o_nes_ó') + #0
# lema(ur'[Dd]eterminaci_o_nes_ó') + #0
# lema(ur'[Dd]etonaci_o_nes_ó') + #0
# lema(ur'[Dd]evaluaci_o_nes_ó') + #0
# lema(ur'[Dd]evoci_o_nes_ó') + #0
# lema(ur'[Dd]evoluci_o_nes_ó') + #0
# lema(ur'[Dd]iagramaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]iapas_ó_n_o', xpre=[ur'[Ll]e ', ur'[Tt]he ', ur'revue ', ], xpos=[ur' (?:Découverte|Records|[Dd]|\(revista)\b', ur'(?:, Scherzo|’s|\'|\]\])', ]) + #0
# lema(ur'[Dd]icci_o_nes_ó') + #0
# lema(ur'[Dd]ifamaci_o_nes_ó') + #0
# lema(ur'[Dd]ifamaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]iferenciaci_o_nes_ó') + #0
# lema(ur'[Dd]iferenciaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]ifracci_o_nes_ó') + #0
# lema(ur'[Dd]ifusi_o_nes_ó') + #0
# lema(ur'[Dd]igresi_o_nes_ó') + #0
# lema(ur'[Dd]igresi_ó_n(?!\])_o') + #0
# lema(ur'[Dd]ilaci_o_nes_ó') + #0
# lema(ur'[Dd]ilaci_ó_n(?!\])_o') + #0
# lema(ur'[Dd]ilataci_o_nes_ó') + #0
# lema(ur'[Dd]inamizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]iscreci_o_nes_ó') + #0
# lema(ur'[Dd]iscriminaci_o_nes_ó') + #0
# lema(ur'[Dd]iscusi_o_nes_ó') + #0
# lema(ur'[Dd]iseminaci_o_nes_ó') + #0
# lema(ur'[Dd]iseminaci_ó_n(?!\])_o') + #0
# lema(ur'[Dd]isensi_o_nes_ó') + #0
# lema(ur'[Dd]isensi_ó_n(?!\])_o') + #0
# lema(ur'[Dd]isertaci_o_nes_ó') + #0
# lema(ur'[Dd]isfunci_o_nes_ó') + #0
# lema(ur'[Dd]isfunci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]isgregaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]isimulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]isjunci_o_nes_ó') + #0
# lema(ur'[Dd]isjunci_ó_n(?!\])_o') + #0
# lema(ur'[Dd]islocaci_o_nes_ó') + #0
# lema(ur'[Dd]islocaci_ó_n(?!\])_o') + #0
# lema(ur'[Dd]isminuci_o_nes_ó') + #0
# lema(ur'[Dd]isminuci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]isociaci_o_nes_ó') + #0
# lema(ur'[Dd]isociaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]isoluci_o_nes_ó') + #0
# lema(ur'[Dd]ispensaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]ispersion_o_nes_ó') + #0
# lema(ur'[Dd]isposi_ció_n_sio') + #0
# lema(ur'[Dd]isposici_o_nes_ó') + #0
# lema(ur'[Dd]istracci_o_nes_ó') + #0
# lema(ur'[Dd]istribuci_o_nes_ó') + #0
# lema(ur'[Dd]isuasi_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Dd]isyunci_o_nes_ó') + #0
# lema(ur'[Dd]iversi_o_nes_ó') + #0
# lema(ur'[Dd]iversificaci_o_nes_ó') + #0
# lema(ur'[Dd]ivulgaci_o_nes_ó') + #0
# lema(ur'[Dd]ocumentaci_o_nes_ó') + #0
# lema(ur'[Dd]omesticaci_o_nes_ó') + #0
# lema(ur'[Dd]omesticaci_ó_n(?!\])_o') + #0
# lema(ur'[Dd]ominaci_o_nes_ó') + #0
# lema(ur'[Dd]onaci_o_nes_ó') + #0
# lema(ur'[Dd]otaci_o_nes_ó') + #0
# lema(ur'[Dd]r_o_n(?!\])_ó') + #0
# lema(ur'[Dd]r_o_nes_ó') + #0
# lema(ur'[Dd]rag_o_nes_ó') + #0
# lema(ur'[Dd]ramatizaci_o_nes_ó') + #0
# lema(ur'[Dd]uplicaci_o_nes_ó') + #0
# lema(ur'[Dd]uraci_o_nes_ó') + #0
# lema(ur'[Ee]bullici_o_nes_ó') + #0
# lema(ur'[Ee]bullici_ó_n(?!\])_o') + #0
# lema(ur'[Ee]corregi_o_nes_ó') + #0
# lema(ur'[Ee]cuaci_o_nes_ó') + #0
# lema(ur'[Ee]dificaci_o_nes_ó') + #0
# lema(ur'[Ee]dificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]ducaci_o_nes_ó') + #0
# lema(ur'[Ee]jecuci_o_nes_ó') + #0
# lema(ur'[Ee]laboraci_o_nes_ó') + #0
# lema(ur'[Ee]lectr_o_nes_ó') + #0
# lema(ur'[Ee]lectrificaci_o_nes_ó') + #0
# lema(ur'[Ee]levaci_o_nes_ó') + #0
# lema(ur'[Ee]liminaci_o_nes_ó') + #0
# lema(ur'[Ee]longaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]manaci_o_nes_ó') + #0
# lema(ur'[Ee]manaci_ó_n(?!\])_o') + #0
# lema(ur'[Ee]mancipaci_o_nes_ó') + #0
# lema(ur'[Ee]mbarcaci_o_nes_ó') + #0
# lema(ur'[Ee]mbarcaci_ó_n(?!\]|\.gov\.ar)_o') + #0
# lema(ur'[Ee]mbri_o_nes_ó') + #0
# lema(ur'[Ee]migraci_o_nes_ó') + #0
# lema(ur'[Ee]mis_ió_n_sió') + #0
# lema(ur'[Ee]mulaci_o_nes_ó') + #0
# lema(ur'[Ee]mulsi_o_nes_ó') + #0
# lema(ur'[Ee]mulsi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #0
# lema(ur'[Ee]ncarcelaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]ncarnaci_o_nes_ó') + #0
# lema(ur'[Ee]ntonaci_o_nes_ó') + #0
# lema(ur'[Ee]numeraci_o_nes_ó') + #0
# lema(ur'[Ee]nunciaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]quipaci_o_nes_ó') + #0
# lema(ur'[Ee]quitaci_o_nes_ó') + #0
# lema(ur'[Ee]quivocaci_o_nes_ó') + #0
# lema(ur'[Ee]recci_o_nes_ó') + #0
# lema(ur'[Ee]rradicaci_o_nes_ó') + #0
# lema(ur'[Ee]rradicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]rudici_o_nes_ó') + #0
# lema(ur'[Ee]rupci_o_nes_ó') + #0
# lema(ur'[Ee]scal_o_nes_ó') + #0
# lema(ur'[Ee]scalaf_o_nes_ó') + #0
# lema(ur'[Ee]scarificaci_o_nes_ó') + #0
# lema(ur'[Ee]scisi_o_nes_ó') + #0
# lema(ur'[Ee]sclavizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]scolarizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]scorpi_o_nes_ó') + #0
# lema(ur'[Ee]scuadr_o_nes_ó') + #0
# lema(ur'[Ee]specializaci_o_nes_ó') + #0
# lema(ur'[Ee]specificaci_o_nes_ó') + #0
# lema(ur'[Ee]speculaci_o_nes_ó') + #0
# lema(ur'[Ee]spol_o_nes_ó') + #0
# lema(ur'[Ee]stabilizaci_o_nes_ó') + #0
# lema(ur'[Ee]stabilizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]standarizaci_o_nes_ó') + #0
# lema(ur'[Ee]standarizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]sterilizaci_o_nes_ó') + #0
# lema(ur'[Ee]stilizaci_o_nes_ó') + #0
# lema(ur'[Ee]stimaci_o_nes_ó') + #0
# lema(ur'[Ee]stimulaci_o_nes_ó') + #0
# lema(ur'[Ee]stimulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]stipulaci_o_nes_ó') + #0
# lema(ur'[Ee]stipulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]stratificaci_o_nes_ó') + #0
# lema(ur'[Ee]stratificaci_ó_n(?!\])_o') + #0
# lema(ur'[Ee]stribaci_o_nes_ó') + #0
# lema(ur'[Ee]stribaci_ó_n_o', xpre=[ur'En una ', ], xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]structuraci_o_nes_ó') + #0
# lema(ur'[Ee]structuraci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]sturi_o_nes_ó') + #0
# lema(ur'[Ee]sturi_ó_n(?!\])_o') + #0
# lema(ur'[Ee]vacuaci_o_nes_ó') + #0
# lema(ur'[Ee]valuaci_o_nes_ó') + #0
# lema(ur'[Ee]vangelizaci_o_nes_ó') + #0
# lema(ur'[Ee]vaporaci_o_nes_ó') + #0
# lema(ur'[Ee]vaporaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]vocaci_o_nes_ó') + #0
# lema(ur'[Ee]voluci_o_nes_ó') + #0
# lema(ur'[Ee]x_cepcio_nes_epci[oó]') + #0
# lema(ur'[Ee]xaci_o_nes_ó') + #0
# lema(ur'[Ee]xaci_ó_n(?!\])_o') + #0
# lema(ur'[Ee]xageraci_o_nes_ó') + #0
# lema(ur'[Ee]xaltaci_o_nes_ó') + #0
# lema(ur'[Ee]xaptaci_o_nes_ó') + #0
# lema(ur'[Ee]xaptaci_ó_n(?!\])_o') + #0
# lema(ur'[Ee]xcepci_o_nes_ó') + #0
# lema(ur'[Ee]xcitaci_o_nes_ó') + #0
# lema(ur'[Ee]xcitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]xclamaci_o_nes_ó') + #0
# lema(ur'[Ee]xclamaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]xclusi_o_nes_ó') + #0
# lema(ur'[Ee]xcreci_o_nes_ó') + #0
# lema(ur'[Ee]xcursi_o_nes_ó') + #0
# lema(ur'[Ee]xenci_o_nes_ó') + #0
# lema(ur'[Ee]xenci_ó_n(?!\])_o') + #0
# lema(ur'[Ee]xhalaci_o_nes_ó') + #0
# lema(ur'[Ee]xhibici_o_nes_ó') + #0
# lema(ur'[Ee]xpansi_o_nes_ó') + #0
# lema(ur'[Ee]xpectaci_o_nes_ó') + #0
# lema(ur'[Ee]xpectoraci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]xpedici_o_nes_ó') + #0
# lema(ur'[Ee]xperimentaci_o_nes_ó') + #0
# lema(ur'[Ee]xperimentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]xploraci_o_nes_ó') + #0
# lema(ur'[Ee]xplosi_o_nes_ó') + #0
# lema(ur'[Ee]xplotaci_o_nes_ó') + #0
# lema(ur'[Ee]xpoliaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]xponenciaci_o_nes_ó') + #0
# lema(ur'[Ee]xponenciaci_ó_n(?!\])_o') + #0
# lema(ur'[Ee]xpropiaci_o_nes_ó') + #0
# lema(ur'[Ee]xpulsi_o_nes_ó') + #0
# lema(ur'[Ee]xtensi_o_nes_ó') + #0
# lema(ur'[Ee]xtinci_o_nes_ó') + #0
# lema(ur'[Ee]xtinci_o_nes_ó') + #0
# lema(ur'[Ee]xtirpaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]xtorsi_o_nes_ó') + #0
# lema(ur'[Ee]xtracci_o_nes_ó') + #0
# lema(ur'[Ee]xtradici_o_nes_ó') + #0
# lema(ur'[Ee]xtradici_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]xtravasaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ee]xtrusi_o_nes_ó') + #0
# lema(ur'[Ff]abricaci_o_nes_ó') + #0
# lema(ur'[Ff]actorizaci_o_nes_ó') + #0
# lema(ur'[Ff]actorizaci_ó_n(?!\])_o') + #0
# lema(ur'[Ff]acturaci_o_nes_ó') + #0
# lema(ur'[Ff]aj_o_nes_ó') + #0
# lema(ur'[Ff]aj_ó_n(?!\])_o') + #0
# lema(ur'[Ff]ald_o_nes_ó') + #0
# lema(ur'[Ff]alsificaci_o_nes_ó') + #0
# lema(ur'[Ff]ara_o_nes_ó') + #0
# lema(ur'[Ff]arall_o_nes_ó') + #0
# lema(ur'[Ff]arall_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #0
# lema(ur'[Ff]ascinaci_o_nes_ó') + #0
# lema(ur'[Ff]ecundaci_o_nes_ó') + #0
# lema(ur'[Ff]ederaci_o_nes_ó') + #0
# lema(ur'[Ff]elicitaci_o_nes_ó') + #0
# lema(ur'[Ff]elicitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ff]eraci_o_nes_ó') + #0
# lema(ur'[Ff]eraci_ó_n_o') + #0
# lema(ur'[Ff]ermentaci_o_nes_ó') + #0
# lema(ur'[Ff]ermi_o_nes_ó') + #0
# lema(ur'[Ff]ertilizaci_o_nes_ó') + #0
# lema(ur'[Ff]ertilizaci_ó_n(?!\])_o') + #0
# lema(ur'[Ff]icci_o_nes_ó') + #0
# lema(ur'[Ff]iguraci_o_nes_ó') + #0
# lema(ur'[Ff]ijaci_o_nes_ó') + #0
# lema(ur'[Ff]il_o_nes_ó') + #0
# lema(ur'[Ff]iliaci_o_nes_ó') + #0
# lema(ur'[Ff]ilmaci_o_nes_ó') + #0
# lema(ur'[Ff]iltraci_o_nes_ó') + #0
# lema(ur'[Ff]inalizaci_o_nes_ó') + #0
# lema(ur'[Ff]inanciaci_o_nes_ó') + #0
# lema(ur'[Ff]iscalizaci_o_nes_ó') + #0
# lema(ur'[Ff]lor_o_nes_ó') + #0
# lema(ur'[Ff]lor_ó_n(?!\])_o') + #3
# lema(ur'[Ff]loraci_o_nes_ó') + #0
# lema(ur'[Ff]lotaci_o_nes_ó') + #0
# lema(ur'[Ff]lotaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ff]luctuaci_o_nes_ó') + #0
# lema(ur'[Ff]og_o_nes_ó') + #0
# lema(ur'[Ff]ormulaci_o_nes_ó') + #0
# lema(ur'[Ff]ormulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ff]ortificaci_o_nes_ó') + #0
# lema(ur'[Ff]ot_o_nes_ó') + #0
# lema(ur'[Ff]ot_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpre=[ur'oficial ', ], xpos=[ur' Motor', ]) + #0
# lema(ur'[Ff]racci_o_nes_ó') + #0
# lema(ur'[Ff]ragmentaci_o_nes_ó') + #0
# lema(ur'[Ff]rancmas_o_nes_ó') + #0
# lema(ur'[Ff]ricci_o_nes_ó') + #0
# lema(ur'[Ff]ris_o_nes_ó') + #0
# lema(ur'[Ff]ront_o_nes_ó') + #0
# lema(ur'[Ff]ruici_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ff]rustraci_o_nes_ó') + #0
# lema(ur'[Ff]undaci_o_nes_ó') + #0
# lema(ur'[Ff]undici_o_nes_ó') + #0
# lema(ur'[Ff]usi_o_nes_ó') + #0
# lema(ur'[Gg]al_o_nes_ó') + #0
# lema(ur'[Gg]ale_o_nes_ó') + #0
# lema(ur'[Gg]alp_o_nes_ó') + #0
# lema(ur'[Gg]asc_o_nes_ó') + #0
# lema(ur'[Gg]eneraci_o_nes_ó') + #0
# lema(ur'[Gg]eneralizaci_o_nes_ó') + #0
# lema(ur'[Gg]eneralizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Gg]eolocalizaci_o_nes_ó') + #0
# lema(ur'[Gg]erminaci_o_nes_ó') + #0
# lema(ur'[Gg]erminaci_ó_n(?!\])_o') + #0
# lema(ur'[Gg]estaci_o_nes_ó') + #0
# lema(ur'[Gg]esti_o_nes_ó') + #0
# lema(ur'[Gg]laciaci_o_nes_ó') + #0
# lema(ur'[Gg]lobalizaci_o_nes_ó') + #0
# lema(ur'[Gg]lot_o_nes_ó') + #0
# lema(ur'[Gg]obernaci_o_nes_ó') + #0
# lema(ur'[Gg]orri_o_nes_ó') + #0
# lema(ur'[Gg]radaci_o_nes_ó') + #0
# lema(ur'[Gg]radaci_ó_n(?!\])_o') + #0
# lema(ur'[Gg]raduaci_o_nes_ó') + #0
# lema(ur'[Gg]ravitaci_o_nes_ó') + #0
# lema(ur'[Gg]ravitaci_ó_n(?!\])_o') + #0
# lema(ur'[Gg]uarnici_o_nes_ó') + #0
# lema(ur'[Gg]ui_o_nes_ó') + #0
# lema(ur'[Hh]abilitaci_o_nes_ó') + #0
# lema(ur'[Hh]abitaci_o_nes_ó') + #0
# lema(ur'[Hh]adr_o_nes_ó') + #0
# lema(ur'[Hh]adr_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #0
# lema(ur'[Hh]ibernaci_o_nes_ó') + #0
# lema(ur'[Hh]ibernaci_ó_n(?!\])_o') + #0
# lema(ur'[Hh]ibridaci_o_nes_ó') + #0
# lema(ur'[Hh]idroavi_o_nes_ó') + #0
# lema(ur'[Hh]ormig_o_nes_ó') + #0
# lema(ur'[Hh]umillaci_o_nes_ó') + #0
# lema(ur'[Hh]ur_o_nes_ó') + #0
# lema(ur'[Hh]ur_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ', xpos=[ur' (?:University|forman|Band|Potawatomi)', ]) + #0
# lema(ur'[Ii]__dentificaciones_n') + #0
# lema(ur'[Ii]dealizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]dentificaci_o_nes_ó') + #0
# lema(ur'[Ii]gnici_o_nes_ó') + #0
# lema(ur'[Ii]gnici_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]luminaci_o_nes_ó') + #0
# lema(ur'[Ii]lusi_o_nes_ó') + #0
# lema(ur'[Ii]lusi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #0
# lema(ur'[Ii]lustraci_o_nes_ó') + #0
# lema(ur'[Ii]maginaci_o_nes_ó') + #0
# lema(ur'[Ii]mitaci_o_nes_ó') + #0
# lema(ur'[Ii]mperfecci_o_nes_ó') + #0
# lema(ur'[Ii]mperfecci_ó_n(?!\])_o') + #0
# lema(ur'[Ii]mplementaci_o_nes_ó') + #0
# lema(ur'[Ii]mplicaci_o_nes_ó') + #0
# lema(ur'[Ii]mportaci_o_nes_ó') + #0
# lema(ur'[Ii]mposici_o_nes_ó') + #0
# lema(ur'[Ii]mposici_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]mprecisi_o_nes_ó') + #0
# lema(ur'[Ii]mpregnaci_o_nes_ó') + #0
# lema(ur'[Ii]mpregnaci_ó_n(?!\])_o') + #0
# lema(ur'[Ii]mprovisaci_o_nes_ó') + #0
# lema(ur'[Ii]mputaci_o_nes_ó') + #0
# lema(ur'[Ii]nauguraci_o_nes_ó') + #0
# lema(ur'[Ii]ncineraci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]ncisi_o_nes_ó') + #0
# lema(ur'[Ii]nclinaci_o_nes_ó') + #0
# lema(ur'[Ii]nclusi_o_nes_ó') + #0
# lema(ur'[Ii]nclusi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #0
# lema(ur'[Ii]ncomprensi_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]ncorporaci_o_nes_ó') + #0
# lema(ur'[Ii]ncrustaci_o_nes_ó') + #0
# lema(ur'[Ii]ncrustaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]ncubaci_o_nes_ó') + #0
# lema(ur'[Ii]ncubaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]ncursi_o_nes_ó') + #0
# lema(ur'[Ii]ndagaci_o_nes_ó') + #0
# lema(ur'[Ii]ndagaci_ó_n(?!\])_o') + #0
# lema(ur'[Ii]ndemnizaci_o_nes_ó') + #0
# lema(ur'[Ii]ndeterminaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]ndicaci_o_nes_ó') + #0
# lema(ur'[Ii]ndignaci_o_nes_ó') + #0
# lema(ur'[Ii]ndignaci_ó_n_o', xpos=[ur'(?:[\]]|\.org)', ]) + #0
# lema(ur'[Ii]nducci_o_nes_ó') + #0
# lema(ur'[Ii]ndustrializaci_o_nes_ó') + #0
# lema(ur'[Ii]ndustrializaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]nfecci_o_nes_ó') + #0
# lema(ur'[Ii]nfiltraci_o_nes_ó') + #0
# lema(ur'[Ii]nflaci_o_nes_ó') + #0
# lema(ur'[Ii]nflamaci_o_nes_ó') + #0
# lema(ur'[Ii]nflamaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]nflexi_o_nes_ó') + #0
# lema(ur'[Ii]nformaci_o_nes_ó') + #0
# lema(ur'[Ii]nfracci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]nfusi_o_nes_ó') + #0
# lema(ur'[Ii]nfusi_ó_n(?!\]\][a-z]+|)_o') + #0
# lema(ur'[Ii]nhalaci_o_nes_ó') + #0
# lema(ur'[Ii]nhalaci_ó_n(?!\])_o') + #0
# lema(ur'[Ii]nhumaci_o_nes_ó') + #0
# lema(ur'[Ii]nhumaci_ó_n(?!\])_o') + #0
# lema(ur'[Ii]niciaci_o_nes_ó') + #0
# lema(ur'[Ii]nicializaci_o_nes_ó') + #0
# lema(ur'[Ii]nmedaci_o_nes_ó') + #0
# lema(ur'[Ii]nmediaci_o_nes_ó') + #0
# lema(ur'[Ii]nmersi_o_nes_ó') + #0
# lema(ur'[Ii]nmersi_ó_n_o', xpos=[ur' (?:and|of|Corporation)', ur'["\]]', ]) + #0
# lema(ur'[Ii]nmersi_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]nmigraci_o_nes_ó') + #0
# lema(ur'[Ii]nmovilizaci_o_nes_ó') + #0
# lema(ur'[Ii]nnovaci_o_nes_ó') + #0
# lema(ur'[Ii]nscripci_o_nes_ó') + #0
# lema(ur'[Ii]nseminaci_o_nes_ó') + #0
# lema(ur'[Ii]nseminaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]nserci_o_nes_ó') + #0
# lema(ur'[Ii]nsinuaci_o_nes_ó') + #0
# lema(ur'[Ii]nsinuaci_ó_n(?!\])_o') + #0
# lema(ur'[Ii]nsolaci_o_nes_ó') + #0
# lema(ur'[Ii]nsolaci_ó_n(?!\])_o') + #0
# lema(ur'[Ii]nspecci_o_nes_ó') + #0
# lema(ur'[Ii]nspiraci_o_nes_ó') + #0
# lema(ur'[Ii]nstauraci_o_nes_ó') + #0
# lema(ur'[Ii]nstauraci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]nstilaci_o_nes_ó') + #0
# lema(ur'[Ii]nstrucci_o_nes_ó') + #0
# lema(ur'[Ii]nstrumentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]nsubordinaci_o_nes_ó') + #0
# lema(ur'[Ii]nsurrecci_o_nes_ó') + #0
# lema(ur'[Ii]nte_rpretació_n_pretacio') + #0
# lema(ur'[Ii]ntenci_o_nes_ó') + #0
# lema(ur'[Ii]ntensificaci_o_nes_ó') + #0
# lema(ur'[Ii]nteracci_o_nes_ó') + #0
# lema(ur'[Ii]ntercalaci_o_nes_ó') + #0
# lema(ur'[Ii]ntercepci_o_nes_ó') + #0
# lema(ur'[Ii]ntercepci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]nterceptaci_o_nes_ó') + #0
# lema(ur'[Ii]ntercomunicaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]nterconexi_o_nes_ó') + #0
# lema(ur'[Ii]nterdicci_o_nes_ó') + #0
# lema(ur'[Ii]nterdicci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]nterjecci_o_nes_ó') + #0
# lema(ur'[Ii]nterjecci_ó_n(?!\])_o') + #0
# lema(ur'[Ii]ntermediaci_o_nes_ó') + #0
# lema(ur'[Ii]nternacionalizaci_o_nes_ó') + #0
# lema(ur'[Ii]nterocepci_o_nes_ó') + #0
# lema(ur'[Ii]nterocepci_ó_n(?!\])_o') + #0
# lema(ur'[Ii]nterpolaci_o_nes_ó') + #0
# lema(ur'[Ii]nterpolaci_ó_n(?!\])_o') + #0
# lema(ur'[Ii]nterposici_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]nterpretaci_o_nes_ó') + #0
# lema(ur'[Ii]nterrelaci_o_nes_ó') + #0
# lema(ur'[Ii]nterrogaci_o_nes_ó') + #0
# lema(ur'[Ii]nterrupci_o_nes_ó') + #0
# lema(ur'[Ii]ntersecci_o_nes_ó') + #0
# lema(ur'[Ii]ntimaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]ntimidaci_o_nes_ó') + #0
# lema(ur'[Ii]ntoxicaci_o_nes_ó') + #0
# lema(ur'[Ii]ntroducci_o_nes_ó') + #0
# lema(ur'[Ii]ntromisi_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]ntrusi_o_nes_ó') + #0
# lema(ur'[Ii]ntrusi_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Ee]sta|[Ee]sa) ') + #0
# lema(ur'[Ii]ntuici_o_nes_ó') + #0
# lema(ur'[Ii]nundaci_o_nes_ó') + #0
# lema(ur'[Ii]nvenci_o_nes_ó') + #0
# lema(ur'[Ii]nvenci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]nvitaci_o_nes_ó') + #0
# lema(ur'[Ii]nvocaci_o_nes_ó') + #0
# lema(ur'[Ii]onizaci_o_nes_ó') + #0
# lema(ur'[Ii]rradiaci_o_nes_ó') + #0
# lema(ur'[Ii]rrigaci_o_nes_ó') + #0
# lema(ur'[Ii]rritaci_o_nes_ó') + #0
# lema(ur'[Ii]rritaci_ó_n(?!\])_o') + #0
# lema(ur'[Ii]rrupci_o_nes_ó') + #0
# lema(ur'[Ii]rrupci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ii]teraci_o_nes_ó') + #0
# lema(ur'[Jj]ab_o_nes_ó') + #0
# lema(ur'[Jj]am_o_nes_ó') + #0
# lema(ur'[Jj]arr_o_nes_ó') + #0
# lema(ur'[Jj]uguet_o_nes_ó') + #0
# lema(ur'[Jj]uri_sdiccio_nal(?:es|)_dicci[oó]') + #0
# lema(ur'[Jj]urisdicci_o_nes_ó') + #0
# lema(ur'[Jj]ustificaci_o_nes_ó') + #0
# lema(ur'[Jj]ustificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Kk]ilot_o_nes_ó') + #0
# lema(ur'[Ll]amentaci_o_nes_ó') + #0
# lema(ur'[Ll]ap_o_nes_ó') + #0
# lema(ur'[Ll]ecci_o_nes_ó') + #0
# lema(ur'[Ll]egalizaci_o_nes_ó') + #0
# lema(ur'[Ll]egi_o_nes_ó') + #0
# lema(ur'[Ll]egislaci_o_nes_ó') + #0
# lema(ur'[Ll]ept_o_nes_ó') + #0
# lema(ur'[Ll]ept_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #0
# lema(ur'[Ll]esi_o_nes_ó') + #0
# lema(ur'[Ll]et_o_nes_ó') + #0
# lema(ur'[Ll]et_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #0
# lema(ur'[Ll]ibaci_o_nes_ó') + #0
# lema(ur'[Ll]ibaci_ó_n(?!\])_o') + #0
# lema(ur'[Ll]iberaci_o_nes_ó') + #0
# lema(ur'[Ll]iberalizaci_o_nes_ó') + #0
# lema(ur'[Ll]icitaci_o_nes_ó') + #0
# lema(ur'[Ll]icuefacci_o_nes_ó') + #0
# lema(ur'[Ll]icuefacci_ó_n(?!\])_o') + #0
# lema(ur'[Ll]im_o_nes_ó') + #0
# lema(ur'[Ll]imitaci_o_nes_ó') + #0
# lema(ur'[Ll]iquidaci_o_nes_ó') + #0
# lema(ur'[Ll]ist_o_nes_ó') + #0
# lema(ur'[Ll]ocaci_o_nes_ó') + #0
# lema(ur'[Ll]ocalizaci_o_nes_ó') + #0
# lema(ur'[Ll]oci_o_nes_ó') + #0
# lema(ur'[Ll]oci_ó_n(?!\])_o') + #0
# lema(ur'[Ll]ocomoci_o_nes_ó') + #0
# lema(ur'[Ll]ocomoci_ó_n(?!\])_o') + #0
# lema(ur'[Ll]ocuci_o_nes_ó') + #0
# lema(ur'[Ll]uxaci_o_nes_ó') + #0
# lema(ur'[Ll]uxaci_ó_n(?!\])_o') + #0
# lema(ur'[Mm]aduraci_o_nes_ó') + #0
# lema(ur'[Mm]aldici_o_nes_ó') + #0
# lema(ur'[Mm]alformaci_o_nes_ó') + #0
# lema(ur'[Mm]alversaci_o_nes_ó') + #0
# lema(ur'[Mm]alversaci_ó_n(?!\])_o') + #0
# lema(ur'[Mm]anifestaci_o_nes_ó') + #0
# lema(ur'[Mm]anipulaci_o_nes_ó') + #0
# lema(ur'[Mm]ansi_o_nes_ó') + #0
# lema(ur'[Mm]aquetaci_o_nes_ó') + #0
# lema(ur'[Mm]aquinaci_o_nes_ó') + #0
# lema(ur'[Mm]aquinaci_ó_n(?!\])_o') + #0
# lema(ur'[Mm]arat_o_nes_ó') + #0
# lema(ur'[Mm]arginaci_o_nes_ó') + #0
# lema(ur'[Mm]arginaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Mm]arr_o_nes_ó') + #0
# lema(ur'[Mm]as_o_nes_ó') + #0
# lema(ur'[Mm]ascar_o_nes_ó') + #0
# lema(ur'[Mm]asterizaci_o_nes_ó') + #0
# lema(ur'[Mm]asturbaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Mm]aterializaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Mm]atriculaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Mm]ecanizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Mm]ech_o_nes_ó') + #0
# lema(ur'[Mm]edall_o_nes_ó') + #0
# lema(ur'[Mm]ediaci_o_nes_ó') + #0
# lema(ur'[Mm]edicaci_o_nes_ó') + #0
# lema(ur'[Mm]edici_o_nes_ó') + #0
# lema(ur'[Mm]egat_o_nes_ó') + #0
# lema(ur'[Mm]ejill_o_nes_ó') + #0
# lema(ur'[Mm]el_o_nes_ó') + #0
# lema(ur'[Mm]elocot_o_nes_ó') + #0
# lema(ur'[Mm]emorizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Mm]enstruaci_o_nes_ó') + #0
# lema(ur'[Mm]enstruaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Mm]es_o_nes_ó') + #0
# lema(ur'[Mm]esorregi_o_nes_ó') + #0
# lema(ur'[Mm]esorregi_ó_n(?!\])_o') + #0
# lema(ur'[Mm]icroacci_o_nes_ó') + #0
# lema(ur'[Mm]icroacci_ó_n(?!\])_o') + #0
# lema(ur'[Mm]icroficci_o_nes_ó') + #0
# lema(ur'[Mm]icromutaci_o_nes_ó') + #0
# lema(ur'[Mm]icromutaci_ó_n(?!\])_o') + #0
# lema(ur'[Mm]icronaci_o_nes_ó') + #0
# lema(ur'[Mm]icronaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Mm]icroregi_o_nes_ó') + #0
# lema(ur'[Mm]icrorregi_o_nes_ó') + #0
# lema(ur'[Mm]igraci_o_nes_ó') + #0
# lema(ur'[Mm]ineralizaci_o_nes_ó') + #0
# lema(ur'[Mm]isi_o_nes_ó') + #0
# lema(ur'[Mm]oci_o_nes_ó') + #0
# lema(ur'[Mm]oderaci_o_nes_ó') + #0
# lema(ur'[Mm]oderaci_ó_n(?!\])_o') + #0
# lema(ur'[Mm]odernizaci_o_nes_ó') + #0
# lema(ur'[Mm]odificaci_o_nes_ó') + #0
# lema(ur'[Mm]odulaci_o_nes_ó') + #0
# lema(ur'[Mm]oj_o_nes_ó') + #0
# lema(ur'[Mm]onici_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Mm]onocotiled_o_nes_ó') + #0
# lema(ur'[Mm]ont_o_nes_ó') + #0
# lema(ur'[Mm]onz_o_nes_ó') + #0
# lema(ur'[Mm]orm_o_nes_ó') + #0
# lema(ur'[Mm]otivaci_o_nes_ó') + #0
# lema(ur'[Mm]otorizaci_o_nes_ó') + #0
# lema(ur'[Mm]ovilizaci_o_nes_ó') + #0
# lema(ur'[Mm]u_o_nes_ó') + #0
# lema(ur'[Mm]ultiplicaci_o_nes_ó') + #0
# lema(ur'[Mm]unici_o_nes_ó') + #0
# lema(ur'[Mm]usicalizaci_o_nes_ó') + #0
# lema(ur'[Mm]usicalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Mm]utaci_o_nes_ó') + #0
# lema(ur'[Mm]utilaci_o_nes_ó') + #0
# lema(ur'[Mm]utilaci_ó_n(?!\])_o') + #0
# lema(ur'[Nn]acionalizaci_o_nes_ó') + #0
# lema(ur'[Nn]arraci_o_nes_ó') + #0
# lema(ur'[Nn]ataci_o_nes_ó') + #0
# lema(ur'[Nn]aturalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Nn]avegaci_o_nes_ó') + #0
# lema(ur'[Nn]egaci_o_nes_ó') + #0
# lema(ur'[Nn]egociaci_o_nes_ó') + #0
# lema(ur'[Nn]ip_o_nes_ó') + #0
# lema(ur'[Nn]oci_o_nes_ó') + #0
# lema(ur'[Nn]oci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Nn]ocicepci_o_nes_ó') + #0
# lema(ur'[Nn]ocicepci_ó_n(?!\])_o') + #0
# lema(ur'[Nn]ormalizaci_o_nes_ó') + #0
# lema(ur'[Nn]otaci_o_nes_ó') + #0
# lema(ur'[Nn]otificaci_o_nes_ó') + #0
# lema(ur'[Nn]ucle_o_nes_ó') + #0
# lema(ur'[Nn]ucle_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #0
# lema(ur'[Nn]umeraci_o_nes_ó') + #0
# lema(ur'[Nn]utrici_o_nes_ó') + #0
# lema(ur'[Oo]bjecci_o_nes_ó') + #0
# lema(ur'[Oo]bjeci_o_nes_ó') + #0
# lema(ur'[Oo]bjeci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Oo]bligaci_o_nes_ó') + #0
# lema(ur'[Oo]bservaci_o_nes_ó') + #0
# lema(ur'[Oo]bstrucci_o_nes_ó') + #0
# lema(ur'[Oo]bstrucci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Oo]bturaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Oo]casi_o_nes_ó') + #0
# lema(ur'[Oo]clusi_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Oo]cultaci_o_nes_ó') + #0
# lema(ur'[Oo]cultaci_ó_n(?!\])_o') + #0
# lema(ur'[Oo]cupaci_o_nes_ó') + #0
# lema(ur'[Oo]misi_o_nes_ó') + #0
# lema(ur'[Oo]misi_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Oo]ndulaci_o_nes_ó') + #0
# lema(ur'[Oo]ndulaci_ó_n(?!\])_o') + #0
# lema(ur'[Oo]pci_o_nes_ó') + #0
# lema(ur'[Oo]posici_o_nes_ó') + #0
# lema(ur'[Oo]presi_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Oo]ptimizaci_o_nes_ó') + #0
# lema(ur'[Oo]raci_o_nes_ó') + #0
# lema(ur'[Oo]rdenaci_o_nes_ó') + #0
# lema(ur'[Oo]rej_o_nes_ó') + #0
# lema(ur'[Oo]rientaci_o_nes_ó') + #0
# lema(ur'[Oo]rnamentaci_o_nes_ó') + #0
# lema(ur'[Oo]rquestaci_o_nes_ó') + #0
# lema(ur'[Oo]rquestaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Oo]scilaci_o_nes_ó') + #0
# lema(ur'[Oo]vaci_o_nes_ó') + #0
# lema(ur'[Oo]xidaci_o_nes_ó') + #0
# lema(ur'[Pp]abell_o_nes_ó') + #0
# lema(ur'[Pp]acificaci_o_nes_ó') + #0
# lema(ur'[Pp]adr_o_nes_ó') + #0
# lema(ur'[Pp]alpitaci_o_nes_ó') + #0
# lema(ur'[Pp]ante_o_nes_ó') + #0
# lema(ur'[Pp]aralizaci_o_nes_ó') + #0
# lema(ur'[Pp]aralizaci_ó_n(?!\])_o') + #0
# lema(ur'[Pp]arcelaci_o_nes_ó') + #0
# lema(ur'[Pp]artici_o_nes_ó') + #0
# lema(ur'[Pp]asi_o_nes_ó') + #0
# lema(ur'[Pp]avimentaci_o_nes_ó') + #0
# lema(ur'[Pp]avimentaci_ó_n(?!\])_o') + #0
# lema(ur'[Pp]e_o_nes_ó') + #0
# lema(ur'[Pp]eat_o_nes_ó') + #0
# lema(ur'[Pp]eat_ó_n(?!\])_o') + #0
# lema(ur'[Pp]eir_o_nes_ó') + #0
# lema(ur'[Pp]elot_o_nes_ó') + #0
# lema(ur'[Pp]enalizaci_o_nes_ó') + #0
# lema(ur'[Pp]end_o_nes_ó') + #0
# lema(ur'[Pp]enetraci_o_nes_ó') + #0
# lema(ur'[Pp]ensi_o_nes_ó') + #0
# lema(ur'[Pp]ercepci_o_nes_ó') + #0
# lema(ur'[Pp]ercu_sió_n_ci[oó]') + #0
# lema(ur'[Pp]erd_o_nes_ó') + #0
# lema(ur'[Pp]erdig_o_nes_ó') + #0
# lema(ur'[Pp]eregrinaci_o_nes_ó') + #0
# lema(ur'[Pp]erfecci_o_nes_ó') + #0
# lema(ur'[Pp]erforaci_o_nes_ó') + #0
# lema(ur'[Pp]ermutaci_ó_n(?!\])_o') + #0
# lema(ur'[Pp]ersecuci_o_nes_ó') + #0
# lema(ur'[Pp]ersonalizaci_o_nes_ó') + #0
# lema(ur'[Pp]ersonalizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]erturbaci_o_nes_ó') + #0
# lema(ur'[Pp]erturbaci_ó_n(?!\])_o') + #0
# lema(ur'[Pp]erversi_o_nes_ó') + #0
# lema(ur'[Pp]ez_o_nes_ó') + #0
# lema(ur'[Pp]eñ_o_nes_ó') + #0
# lema(ur'[Pp]ich_o_nes_ó') + #0
# lema(ur'[Pp]il_o_nes_ó') + #0
# lema(ur'[Pp]inz_o_nes_ó') + #0
# lema(ur'[Pp]ist_o_nes_ó') + #0
# lema(ur'[Pp]iñ_o_nes_ó') + #0
# lema(ur'[Pp]laneaci_o_nes_ó') + #0
# lema(ur'[Pp]lanificaci_o_nes_ó') + #0
# lema(ur'[Pp]lant_o_nes_ó') + #0
# lema(ur'[Pp]o_sició_n_(?:ci[sc]i[oó]|sisi[oó]n)') + #0
# lema(ur'[Pp]oci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]olarizaci_o_nes_ó') + #0
# lema(ur'[Pp]olarizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]olimerizaci_o_nes_ó') + #0
# lema(ur'[Pp]olinizaci_o_nes_ó') + #0
# lema(ur'[Pp]olinizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]onderaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]ont_o_nes_ó') + #0
# lema(ur'[Pp]ont_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u) ', xpos=[ur' d', ]) + #0
# lema(ur'[Pp]opularizaci_o_nes_ó') + #0
# lema(ur'[Pp]opularizaci_ó_n(?!\])_o') + #0
# lema(ur'[Pp]orci_o_nes_ó') + #0
# lema(ur'[Pp]orr_o_nes_ó') + #0
# lema(ur'[Pp]ort_o_nes_ó') + #0
# lema(ur'[Pp]ortaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]osesi_o_nes_ó') + #0
# lema(ur'[Pp]osici_o_nes_ó') + #0
# lema(ur'[Pp]ositr_o_nes_ó') + #0
# lema(ur'[Pp]ostulaci_o_nes_ó') + #0
# lema(ur'[Pp]recauci_o_nes_ó') + #0
# lema(ur'[Pp]recipitaci_o_nes_ó') + #0
# lema(ur'[Pp]recisi_o_nes_ó') + #0
# lema(ur'[Pp]redicaci_o_nes_ó') + #0
# lema(ur'[Pp]redicaci_ó_n_o', xpos=[ur' de la Ley', ur'\]\]es', ]) + #0
# lema(ur'[Pp]redicci_o_nes_ó') + #0
# lema(ur'[Pp]redilecci_o_nes_ó') + #0
# lema(ur'[Pp]redilecci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]redilecci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]redisposici_o_nes_ó') + #0
# lema(ur'[Pp]redisposici_ó_n(?!\])_o') + #0
# lema(ur'[Pp]reimpresi_o_nes_ó') + #0
# lema(ur'[Pp]reimpresi_ó_n(?!\])_o') + #0
# lema(ur'[Pp]remeditaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]remiaci_o_nes_ó') + #0
# lema(ur'[Pp]remonici_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]reocupaci_o_nes_ó') + #0
# lema(ur'[Pp]reocupaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]reparaci_o_nes_ó') + #0
# lema(ur'[Pp]reposici_o_nes_ó') + #0
# lema(ur'[Pp]rescripci_o_nes_ó') + #0
# lema(ur'[Pp]reselecci_o_nes_ó') + #0
# lema(ur'[Pp]reservaci_o_nes_ó') + #0
# lema(ur'[Pp]reservaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]resi_o_nes_ó') + #0
# lema(ur'[Pp]restaci_o_nes_ó') + #0
# lema(ur'[Pp]restaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]resunci_o_nes_ó') + #0
# lema(ur'[Pp]resunci_ó_n(?!\])_o') + #0
# lema(ur'[Pp]revenci_o_nes_ó') + #0
# lema(ur'[Pp]revisi_o_nes_ó') + #0
# lema(ur'[Pp]revisualizaci_o_nes_ó') + #0
# lema(ur'[Pp]ri_o_nes_ó') + #0
# lema(ur'[Pp]ris_o_n Break_(?:i[oó]|ó)') + #0
# lema(ur'[Pp]risi_o_nes_ó') + #0
# lema(ur'[Pp]rivaci_o_nes_ó') + #0
# lema(ur'[Pp]rivaci_ó_n(?!\])_o') + #0
# lema(ur'[Pp]rivatizaci_o_nes_ó') + #0
# lema(ur'[Pp]roclamaci_o_nes_ó') + #0
# lema(ur'[Pp]rofanaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]rofesi_o_nes_ó') + #0
# lema(ur'[Pp]rofundizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]rogramaci_o_nes_ó') + #0
# lema(ur'[Pp]rogresi_o_nes_ó') + #0
# lema(ur'[Pp]rogresi_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]rohibici_o_nes_ó') + #0
# lema(ur'[Pp]rolongaci_o_nes_ó') + #0
# lema(ur'[Pp]rolongaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]romoci_o_nes_ó') + #0
# lema(ur'[Pp]romulgaci_o_nes_ó') + #0
# lema(ur'[Pp]ronunciaci_o_nes_ó') + #0
# lema(ur'[Pp]ropagaci_o_nes_ó') + #0
# lema(ur'[Pp]ropiocepci_o_nes_ó') + #0
# lema(ur'[Pp]roporci_o_nes_ó') + #0
# lema(ur'[Pp]roposici_o_nes_ó') + #0
# lema(ur'[Pp]ropulsi_o_nes_ó') + #0
# lema(ur'[Pp]roscripci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]rosecuci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]rospecci_o_nes_ó') + #0
# lema(ur'[Pp]rospecci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]rostituci_o_nes_ó') + #0
# lema(ur'[Pp]rot_o_nes_ó') + #0
# lema(ur'[Pp]rotecci_o_nes_ó') + #0
# lema(ur'[Pp]rovi_sió_n_ci[oó]') + #0
# lema(ur'[Pp]rovisi_o_nes_ó') + #0
# lema(ur'[Pp]rovocaci_o_nes_ó') + #0
# lema(ur'[Pp]royecci_o_nes_ó') + #0
# lema(ur'[Pp]ublicaci_o_nes_ó') + #0
# lema(ur'[Pp]ulg_o_nes_ó') + #0
# lema(ur'[Pp]ulg_ó_n_o', xpos=[ur' \(Kirguistán', ur'(?:[\'\]])', ]) + #0
# lema(ur'[Pp]ulm_o_nes_ó') + #0
# lema(ur'[Pp]ulsaci_o_nes_ó') + #0
# lema(ur'[Pp]ulsaci_ó_n(?!\])_o') + #0
# lema(ur'[Pp]ulsi_o_nes_ó') + #0
# lema(ur'[Pp]unci_o_nes_ó') + #0
# lema(ur'[Pp]unci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]unici_o_nes_ó') + #0
# lema(ur'[Pp]unici_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Pp]untuaci_o_nes_ó') + #0
# lema(ur'[Pp]unz_o_nes_ó') + #0
# lema(ur'[Pp]urificaci_o_nes_ó') + #0
# lema(ur'[Pp]utrefacci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]aci_o_nes_ó') + #0
# lema(ur'[Rr]adiaci_o_nes_ó') + #0
# lema(ur'[Rr]ai_o_nes_ó') + #0
# lema(ur'[Rr]amificaci_o_nes_ó') + #0
# lema(ur'[Rr]amificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]atificaci_o_nes_ó') + #0
# lema(ur'[Rr]ay_o_nes_ó') + #0
# lema(ur'[Rr]az_o_nes_ó') + #0
# lema(ur'[Rr]eacci_o_nes_ó') + #0
# lema(ur'[Rr]eactivaci_o_nes_ó') + #0
# lema(ur'[Rr]ealizaci_o_nes_ó') + #0
# lema(ur'[Rr]eanudaci_o_nes_ó') + #0
# lema(ur'[Rr]eanudaci_ó_n(?!\])_o') + #0
# lema(ur'[Rr]eaparici_o_nes_ó') + #0
# lema(ur'[Rr]ebeli_o_nes_ó') + #0
# lema(ur'[Rr]ecapitulaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]ecaptaci_o_nes_ó') + #0
# lema(ur'[Rr]ecaptaci_ó_n(?!\])_o') + #0
# lema(ur'[Rr]ecaudaci_o_nes_ó') + #0
# lema(ur'[Rr]ecepci_o_nes_ó') + #0
# lema(ur'[Rr]ecitaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]eclamaci_o_nes_ó') + #0
# lema(ur'[Rr]eclusi_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]ecolecci_o_nes_ó') + #0
# lema(ur'[Rr]ecolonizaci_ó_n_o') + #0
# lema(ur'[Rr]ecombinaci_o_nes_ó') + #0
# lema(ur'[Rr]ecomendaci_o_nes_ó') + #0
# lema(ur'[Rr]econciliaci_o_nes_ó') + #0
# lema(ur'[Rr]econstituci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]econstrucci_o_nes_ó') + #0
# lema(ur'[Rr]ecopilaci_o_nes_ó') + #0
# lema(ur'[Rr]ecreaci_o_nes_ó') + #0
# lema(ur'[Rr]ectificaci_o_nes_ó') + #0
# lema(ur'[Rr]ecuperaci_o_nes_ó') + #0
# lema(ur'[Rr]edacci_o_nes_ó') + #0
# lema(ur'[Rr]edenci_o_nes_ó') + #0
# lema(ur'[Rr]edirecci_o_nes_ó') + #0
# lema(ur'[Rr]edistribuci_o_nes_ó') + #0
# lema(ur'[Rr]edistribuci_ó_n(?!\])_o') + #0
# lema(ur'[Rr]educci_o_nes_ó') + #0
# lema(ur'[Rr]eedici_o_nes_ó') + #0
# lema(ur'[Rr]eelecci_o_nes_ó') + #0
# lema(ur'[Rr]eencarnaci_o_nes_ó') + #0
# lema(ur'[Rr]eestructuraci_o_nes_ó') + #0
# lema(ur'[Rr]efacci_o_nes_ó') + #0
# lema(ur'[Rr]efinaci_o_nes_ó') + #0
# lema(ur'[Rr]efinaci_ó_n(?!\])_o') + #0
# lema(ur'[Rr]eflexi_o_nes_ó') + #0
# lema(ur'[Rr]eformaci_o_nes_ó') + #0
# lema(ur'[Rr]efracci_o_nes_ó') + #0
# lema(ur'[Rr]efrigeraci_o_nes_ó') + #0
# lema(ur'[Rr]efrigeraci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]efundaci_o_nes_ó') + #0
# lema(ur'[Rr]egeneraci_o_nes_ó') + #0
# lema(ur'[Rr]eglamentaci_o_nes_ó') + #0
# lema(ur'[Rr]egulaci_o_nes_ó') + #0
# lema(ur'[Rr]ehabilitaci_o_nes_ó') + #0
# lema(ur'[Rr]eimpresi_o_nes_ó') + #0
# lema(ur'[Rr]eincorporaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]einfecci_o_nes_ó') + #0
# lema(ur'[Rr]einvenci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]eivindicaci_o_nes_ó') + #0
# lema(ur'[Rr]eivindicaci_ó_n(?!\])_o') + #0
# lema(ur'[Rr]elajaci_o_nes_ó') + #0
# lema(ur'[Rr]elajaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]eligi_o_nes_ó') + #0
# lema(ur'[Rr]emisi_o_nes_ó') + #0
# lema(ur'[Rr]emoci_o_nes_ó') + #0
# lema(ur'[Rr]emodelaci_o_nes_ó') + #0
# lema(ur'[Rr]emuneraci_o_nes_ó') + #0
# lema(ur'[Rr]emuneraci_ó_n(?!\])_o') + #0
# lema(ur'[Rr]endici_o_nes_ó') + #0
# lema(ur'[Rr]engl_o_nes_ó') + #0
# lema(ur'[Rr]enovaci_o_nes_ó') + #0
# lema(ur'[Rr]eorganizaci_o_nes_ó') + #0
# lema(ur'[Rr]eparaci_o_nes_ó') + #0
# lema(ur'[Rr]epartici_o_nes_ó') + #0
# lema(ur'[Rr]epartici_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]epercusi_o_nes_ó') + #0
# lema(ur'[Rr]eplicaci_o_nes_ó') + #0
# lema(ur'[Rr]epoblaci_o_nes_ó') + #0
# lema(ur'[Rr]eposici_o_nes_ó') + #0
# lema(ur'[Rr]epresentaci_o_nes_ó') + #0
# lema(ur'[Rr]epresi_o_nes_ó') + #0
# lema(ur'[Rr]eputaci_o_nes_ó') + #0
# lema(ur'[Rr]esoluci_o_nes_ó') + #0
# lema(ur'[Rr]espiraci_o_nes_ó') + #0
# lema(ur'[Rr]estauraci_o_nes_ó') + #0
# lema(ur'[Rr]estituci_o_nes_ó') + #0
# lema(ur'[Rr]esur_recció_n_o', xpos=[ur' Blv', ur'\]\]es', ]) + #0
# lema(ur'[Rr]esurrecci_o_nes_ó') + #0
# lema(ur'[Rr]etenci_o_nes_ó') + #0
# lema(ur'[Rr]etenci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]etracci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]etransmisi_o_nes_ó') + #0
# lema(ur'[Rr]etransmisi_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]etribuci_o_nes_ó') + #0
# lema(ur'[Rr]etribuci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]etroalimentaci_o_nes_ó') + #0
# lema(ur'[Rr]etroalimentaci_ó_n(?!\])_o') + #0
# lema(ur'[Rr]etrotranspos_o_nes_ó') + #0
# lema(ur'[Rr]eunificaci_o_nes_ó') + #0
# lema(ur'[Rr]eunificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]eutilizaci_o_nes_ó') + #0
# lema(ur'[Rr]eutilizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]evalidaci_o_nes_ó') + #0
# lema(ur'[Rr]evalidaci_ó_n(?!\])_o') + #0
# lema(ur'[Rr]evelaci_o_nes_ó') + #0
# lema(ur'[Rr]eversi_o_nes_ó') + #0
# lema(ur'[Rr]evisi_o_nes_ó') + #0
# lema(ur'[Rr]inc_o_nes_ó') + #0
# lema(ur'[Rr]iñ_o_nes_ó') + #0
# lema(ur'[Rr]omanizaci_o_nes_ó') + #0
# lema(ur'[Rr]omanizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Rr]oset_o_nes_ó') + #0
# lema(ur'[Rr]otaci_o_nes_ó') + #0
# lema(ur'[Ss]aj_o_nes_ó') + #0
# lema(ur'[Ss]al_o_nes_ó') + #0
# lema(ur'[Ss]alaz_o_nes_ó') + #0
# lema(ur'[Ss]alaz_ó_n(?!\])_o') + #0
# lema(ur'[Ss]alm_o_nes_ó') + #0
# lema(ur'[Ss]alvaci_o_nes_ó') + #0
# lema(ur'[Ss]anci_o_nes_ó') + #0
# lema(ur'[Ss]atisfacci_o_nes_ó') + #0
# lema(ur'[Ss]aturaci_o_nes_ó') + #0
# lema(ur'[Ss]axof_o_nes_ó') + #0
# lema(ur'[Ss]ecreci_o_nes_ó') + #0
# lema(ur'[Ss]ecreci_ó_n_o', xpos=[ur'(?:\]|\.com)', ]) + #0
# lema(ur'[Ss]ecuenciaci_o_nes_ó') + #0
# lema(ur'[Ss]ecuenciaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ss]ecularizaci_o_nes_ó') + #0
# lema(ur'[Ss]ecularizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ss]edimentaci_o_nes_ó') + #0
# lema(ur'[Ss]educci_o_nes_ó') + #0
# lema(ur'[Ss]egmentaci_o_nes_ó') + #0
# lema(ur'[Ss]egmentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ss]egregaci_o_nes_ó') + #0
# lema(ur'[Ss]emidesintegraci_o_nes_ó') + #0
# lema(ur'[Ss]emidesintegraci_ó_n(?!\])_o') + #0
# lema(ur'[Ss]emiprotecci_o_nes_ó') + #0
# lema(ur'[Ss]emiprotecci_ó_n(?!\])_o') + #0
# lema(ur'[Ss]ensaci_o_nes_ó') + #0
# lema(ur'[Ss]ensibilizaci_o_nes_ó') + #0
# lema(ur'[Ss]ensibilizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ss]eparaci_o_nes_ó') + #0
# lema(ur'[Ss]erm_o_nes_ó') + #0
# lema(ur'[Ss]erm_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #0
# lema(ur'[Ss]eñalizaci_o_nes_ó') + #0
# lema(ur'[Ss]if_o_nes_ó') + #0
# lema(ur'[Ss]ignificaci_o_nes_ó') + #0
# lema(ur'[Ss]ignificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ss]ill_o_nes_ó') + #0
# lema(ur'[Ss]ill_ó_n_o', xpre=[ur'\'', ur'& ', ur'(?:du|[Ll]e|et) ', ur'Au ', ur'Claude ', ur'Grand ', ur'Jean ', ur'Mon ', ur'Princesse de ', ur'Victor ', ], xpos=[ur' (?:rhodanien|de Talbert|beach|industriel|de Bretagne|Sambre)', ur'\]\]es', ]) + #0
# lema(ur'[Ss]implificaci_o_nes_ó') + #0
# lema(ur'[Ss]implificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ss]imulaci_o_nes_ó') + #0
# lema(ur'[Ss]incronizaci_o_nes_ó') + #0
# lema(ur'[Ss]incronizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ss]ituaci_o_nes_ó') + #0
# lema(ur'[Ss]ituaci_o_nes_ó') + #0
# lema(ur'[Ss]obrealimentaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ss]obregrabaci_o_nes_ó') + #0
# lema(ur'[Ss]obretensi_o_nes_ó') + #0
# lema(ur'[Ss]ocializaci_o_nes_ó') + #0
# lema(ur'[Ss]ocializaci_ó_n(?!\])_o') + #0
# lema(ur'[Ss]olidificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ss]ubcampe_o_nes_ó') + #0
# lema(ur'[Ss]ubdelegaci_o_nes_ó') + #0
# lema(ur'[Ss]ubdelegaci_ó_n(?!\])_o') + #0
# lema(ur'[Ss]ubdivisi_o_nes_ó') + #0
# lema(ur'[Ss]ubestaci_o_nes_ó') + #0
# lema(ur'[Ss]ublevaci_o_nes_ó') + #0
# lema(ur'[Ss]ubordinaci_o_nes_ó') + #0
# lema(ur'[Ss]ubregi_o_nes_ó') + #0
# lema(ur'[Ss]ubsecci_o_nes_ó') + #0
# lema(ur'[Ss]ubstituci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ss]ubvenci_o_nes_ó') + #0
# lema(ur'[Ss]ubvenci_ó_n(?!\])_o') + #0
# lema(ur'[Ss]ucesi_o_nes_ó') + #0
# lema(ur'[Ss]ugesti_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ss]ujeci_o_nes_ó') + #0
# lema(ur'[Ss]uperaci_o_nes_ó') + #0
# lema(ur'[Ss]uperposici_o_nes_ó') + #0
# lema(ur'[Ss]uperproducci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Ss]uperstici_o_nes_ó') + #0
# lema(ur'[Ss]upervisi_o_nes_ó') + #0
# lema(ur'[Ss]uposici_o_nes_ó') + #0
# lema(ur'[Ss]uposici_ó_n(?!\])_o') + #0
# lema(ur'[Ss]uscripci_o_nes_ó') + #0
# lema(ur'[Ss]uspensi_o_nes_ó') + #0
# lema(ur'[Ss]ustentaci_o_nes_ó') + #0
# lema(ur'[Ss]ustituci_o_nes_ó') + #0
# lema(ur'[Ss]ustracci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Tt]abl_o_nes_ó') + #0
# lema(ur'[Tt]ac_o_nes_ó') + #0
# lema(ur'[Tt]al_o_nes_ó') + #0
# lema(ur'[Tt]al_ó_n_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ') + #0
# lema(ur'[Tt]amp_o_nes_ó') + #0
# lema(ur'[Tt]asaci_o_nes_ó') + #0
# lema(ur'[Tt]ax_o_nes_ó') + #0
# lema(ur'[Tt]ej_o_nes_ó') + #0
# lema(ur'[Tt]elevisi_o_nes_ó') + #0
# lema(ur'[Tt]embl_o_nes_ó') + #0
# lema(ur'[Tt]end_o_nes_ó') + #0
# lema(ur'[Tt]end_ó_n_o', xpre=[ur'Achilles\+', ur'Dr ', ], xpos=[ur' (?:hacia|\(receta)', ur'[\'\]]', ]) + #0
# lema(ur'[Tt]entaci_o_nes_ó') + #0
# lema(ur'[Tt]erminaci_o_nes_ó') + #0
# lema(ur'[Tt]eut_o_nes_ó') + #0
# lema(ur'[Tt]eut_ó_n(?!\])_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada) ', xpos=[ur' de Neville', ]) + #0
# lema(ur'[Tt]if_o_nes_ó') + #0
# lema(ur'[Tt]im_o_nes_ó') + #0
# lema(ur'[Tt]inci_o_nes_ó') + #0
# lema(ur'[Tt]itulaci_o_nes_ó') + #0
# lema(ur'[Tt]itulaci_ó_n(?!\])_o') + #0
# lema(ur'[Tt]itulizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Tt]orre_o_nes_ó') + #0
# lema(ur'[Tt]racci_o_nes_ó') + #0
# lema(ur'[Tt]raducci_o_nes_ó') + #0
# lema(ur'[Tt]raici_o_nes_ó') + #0
# lema(ur'[Tt]ramitaci_o_nes_ó') + #0
# lema(ur'[Tt]ramitaci_ó_n(?!\])_o') + #0
# lema(ur'[Tt]ransacci_o_nes_ó') + #0
# lema(ur'[Tt]ranscripci_o_nes_ó') + #0
# lema(ur'[Tt]ransducci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Tt]ransfusi_o_nes_ó') + #0
# lema(ur'[Tt]ransgresi_o_nes_ó') + #0
# lema(ur'[Tt]ransgresi_ó_n(?!\])_o') + #0
# lema(ur'[Tt]ransici_o_nes_ó') + #0
# lema(ur'[Tt]ranslaci_o_nes_ó') + #0
# lema(ur'[Tt]ransliteraci_ó_n(?!\])_o') + #0
# lema(ur'[Tt]ranslocaci_o_nes_ó') + #0
# lema(ur'[Tt]ransposi_ció_n_sicio') + #0
# lema(ur'[Tt]ransposici_o_nes_ó') + #0
# lema(ur'[Tt]ransposici_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Tt]rasformaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Tt]raslaci_o_nes_ó') + #0
# lema(ur'[Tt]rasmisi_ó_n_o', xpos=[ur' (?:kon|Eléktrika)', ur'\]\]es', ]) + #0
# lema(ur'[Tt]repidaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Tt]ribulaci_o_nes_ó') + #0
# lema(ur'[Tt]ribulaci_ó_n(?!\])_o') + #0
# lema(ur'[Tt]ributaci_o_nes_ó') + #0
# lema(ur'[Tt]ributaci_ó_n_o') + #0
# lema(ur'[Tt]rill_o_nes_ó') + #0
# lema(ur'[Tt]rill_ó_n(?!\])_o') + #0
# lema(ur'[Tt]ripulaci_o_nes_ó') + #0
# lema(ur'[Tt]rit_o_nes_ó') + #0
# lema(ur'[Tt]romb_o_nes_ó') + #0
# lema(ur'[Tt]umefacci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Tt]urbaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Tt]urr_o_nes_ó') + #0
# lema(ur'[Tt]áx_o_nes_ó') + #0
# lema(ur'[Uu]ni_o_nes_ó') + #0
# lema(ur'[Uu]ni_ó_n Pac[ií]fico_o', xpre=[ur'Times ', ur'[Ll][’\']', ur'et ', ]) + #0
# lema(ur'[Uu]nificaci_o_nes_ó') + #0
# lema(ur'[Uu]rbanizaci_o_nes_ó') + #0
# lema(ur'[Uu]surpaci_o_nes_ó') + #0
# lema(ur'[Uu]surpaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Uu]tilizaci_o_nes_ó') + #0
# lema(ur'[Vv]acaci_o_nes_ó') + #0
# lema(ur'[Vv]acaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Vv]acilaci_o_nes_ó') + #0
# lema(ur'[Vv]acilaci_ó_n(?!\])_o') + #0
# lema(ur'[Vv]acunaci_o_nes_ó') + #0
# lema(ur'[Vv]al_o_nes_ó') + #0
# lema(ur'[Vv]alidaci_o_nes_ó') + #0
# lema(ur'[Vv]alidaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Vv]aloraci_o_nes_ó') + #0
# lema(ur'[Vv]alorizaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Vv]ar_o_nes_ó') + #0
# lema(ur'[Vv]ar_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #0
# lema(ur'[Vv]ariaci_o_nes_ó') + #0
# lema(ur'[Vv]ectorizaci_o_nes_ó') + #0
# lema(ur'[Vv]ectorizaci_ó_n(?!\])_o') + #0
# lema(ur'[Vv]egetaci_o_nes_ó') + #0
# lema(ur'[Vv]ejaci_o_nes_ó') + #0
# lema(ur'[Vv]ejaci_ó_n(?!\])_o') + #0
# lema(ur'[Vv]eneraci_o_nes_ó') + #0
# lema(ur'[Vv]eneraci_ó_n_o', xpre=[ur'Ian ', ur'Jun ', ur'Luis ', ur'Ofilada ', ur'Ynez ', ], xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Vv]entilaci_o_nes_ó') + #0
# lema(ur'[Vv]erificaci_o_nes_ó') + #0
# lema(ur'[Vv]erificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Vv]ersificaci_ó_n_o', xpos=[ur'\]\]es', ]) + #0
# lema(ur'[Vv]inculaci_o_nes_ó') + #0
# lema(ur'[Vv]isi_o_nes_ó') + #0
# lema(ur'[Vv]ocaci_o_nes_ó') + #0
# lema(ur'[Vv]ocalizaci_o_nes_ó') + #0
# lema(ur'[Vv]otaci_o_nes_ó') + #0
# lema(ur'[p]il_ó_n_o', pre=ur'(?:[Ee]l|[Dd]el?|[Uu]n|[Cc]ada|[Ss]u|[Aa]) ') + #0
[]][0]

grupo2Perfecto = [# Sin excepciones
lema(ur'[Ee]__l_l e') + #1269
lema(ur'[Mm]_á_s (?:accesible|agradable|alegre|amigable|artículo|asistencia|ataque|casilla|célebre|cosa|década|dominante|edificio|ejemplo|emocionante|estable|experiencia|fecha|fiable|fuerte|grande|hilarante|humilde|ilustre|importante|impresionante|minimalista|minutos|muerte|noble|noche|palabra|película|pista|problema|prueba|realista|reciente|resaltante|resistencia|salvaje|sociable|suave|tarde|temporada|vía|victoria|visible|visita|vuelta|vulnerable)s?\b_a') + #594
lema(ur'[Pp]_á_gina (?:[Ww]eb|oficial|del?)_a') + #510
lema(ur'[Uu]n_a_ (?:agencia|aldea|alternativa|amalgama|antigua|banda|barra|bomba|buena|cadena|caja|campaña|capa|carrera|casa|chica|cierta|cita|comedia|compañía|copia|corta|criatura|crítica|cuerda|derrota|distancia|empresa|escena|escuela|escultura|estatua|estrella|estructura|etapa|extensa|extraña|familia|fecha|fiesta|figura|franja|fuerza|guerra|historia|idea|iglesia|intensa|lanza|ligera|lucha|línea|manera|mezcla|misma|niña|nota|novela|nueva|obra|palabra|pareja|pelea|película|pequeña|persona|perspectiva|pieza|pista|placa|planta|plataforma|playa|plaza|política|potencia|profunda|prueba|página|pérdida|rama|raza|referencia|reserva|respuesta|revista|ruta|sala|secuencia|sola|tabla|tasa|temperatura|temporada|tienda|trama|técnica|verdadera|victoria|vida|zona|[eé]poca|[uú]nica)\b_') + #452
lema(ur'_sobre la base de__en base a') + #394
lema(ur'[Ll]__os_os l') + #374
lema(ur'[Dd]__el_el d') + #338
lema(ur'[Pp]a_í_ses(?! Baixos)_i') + #291
lema(ur'[Qq]__ue_ue q') + #278
lema(ur'_e_xternos_E', pre=ur'(?:[Ee]nlaces|[Vv]ínculos) ') + #257
lema(ur'[Mm]usulm_á_n_a', xpre=[ur'monde ', ur'problème ', ur'suis ', ur'Occident '], xpos=[ur'\]\]es']) + #225
lema(ur'[Mm]_á_s (?:alt|amarg|amig|citad|competitiv|desconocid|distintiv|envejecid|equilibrad|ergonómic|insegur|lujos|notad|óptim|pequeñ|poblad|prolífic|rocker|select|sosegad|vendid|veteran|vigoros|violent|viv)[ao]s?\b_a') + #221
lema(ur'[Uu]n_a_ (?:alerta|alianza|amiga|armadura|atmósfera|auténtica|avenida|barrera|batalla|bebida|beca|bella|biografía|bola|bolsa|brigada|broma|bóveda|caldera|carga|carretera|caída|ceremonia|cifra|cinta|clara|clínica|cola|colina|comarca|competencia|computadora|conferencia|corona|cubierta|cueva|curva|célula|cúpula|demanda|determinada|diferencia|disputa|dura|década|economía|entrada|ermita|escalera|escritora|esfera|estrategia|estrecha|experiencia|falla|famosa|feria|finca|flota|fotografía|futura|granja|hermana|hija|hora|huelga|inmensa|jugadora|junta|lengua|letra|leyenda|llamada|maestra|mancha|marcha|medalla|medida|mejora|mina|montaña|muestra|ofensiva|oferta|oficina|orquesta|pantalla|parada|parodia|partícula|pelota|piedra|pintura|pistola|postura|presencia|princesa|propuesta|protesta|proteína|provincia|pr[aá]ctica|r[eé]plica|rampa|reforma|regla|revuelta|rica|rueda|rápida|secuela|semana|silla|talla|tarjeta|tecnología|teoría|trampa|trenza|típica|vasta|ventaja|vieja|villa|visita|vista|vivienda|órbita|última)\b_') + #210
lema(ur'_ú_ltima_u', pre=ur'(?:[Aa]|[Cc]omo|[Dd]el|[Ee]st[ao]s?|[Ll]as?|[Pp]or|[Qq]ueda[nsr]?|[Qq]uedó|[Ss]us?|[Uu]na|[Uu]nas|[Yy]) ') + #195
lema(ur'[Dd]_ó_nde_o', pre=ur'¿ *') + #192
lema(ur'[Ll]__as_as l') + #175
lema(ur'[d]_í_as_i', pre=ur'(?:[Aa]lgunos|[Bb]uenos|[Ee]scasos|[Ee]stos|[Ll]os|[Nn]uestros|[UÚuú]ltimos|[Uu]nos|[Vv]arios|[Dd]os|[Tt]res|[Cc]uatro|[Cc]inco|[Ss]eis|[Ss]iete|[Oo]cho|[Nn]ueve|[Dd]iez|[0-9]+) ') + #175
lema(ur'[Oo]r_i_gen_í') + #168
lema(ur'[Rr]e_hu_sa[ns]?_(?:hu|[uú])') + #154
lema(ur'_Estados U_nidos_(?:estados [Uu]|Estados u)', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #149
lema(ur'_ de _[12][0-9]{3}_', pre=ur'(?:[Ee]nero|[Ff]ebrero|[Mm]arzo|[Aa]bril|[Mm]ayo|[Jj]unio|[Jj]ulio|[Aa]gosto|[Ss]eptiembre|[Oo]ctubre|[Nn]oviembre|[Dd]iciembre)') + #148
lema(ur'[Pp]articip_ó_ (?:en|junto|como)_o') + #145
lema(ur'[Cc]l_á_sic(?:o|[ao]s|amente)_a') + #141
lema(ur'[Ii]nclu_i_d[ao]s?_í') + #138
lema(ur'[t]_é_rmino_e', pre=ur'(?:[Aa]l?|[Dd]el?|[Uu]n|[Ss]u|[Ee]l) ') + #135
lema(ur'[Vv]ol_u_men_ú') + #124
lema(ur'_Pací_fico_(?:pac[ií]|Paci)', pre=ur'[Oo]c[eé]ano ') + #124
lema(ur'[Pp]ol_í_ticos(?!\.html)_i') + #119
lema(ur'[Jj]_ó_venes_o') + #118
lema(ur'[Mm]_á_nager_a', pre=ur'(?:[Ee]l|[Dd]el?|[Ll]a|[Uu]n|[Ss]u|nuevo|antiguo|anterior|próximo) ') + #118
lema(ur'Berm_ú_dez_u') + #113
lema(ur'[Gg]r_á_fico_a', xpos=[ur' Editoriale', ]) + #112
lema(ur'[Nn]orteam_é_rica(?!\]\])_e') + #110
lema(ur'[Cc]l_á_sica_a', xpos=[ur' (?:do|maior)\b', ur'2\.com', ]) + #107
lema(ur'[Ss]__e_e s') + #107
lema(ur'_á_reas?_a', pre=ur'(?:[AaEe]l|[Ll]as|[Mm][aá]s|[Uu]nas|[Aa]lgunas|[Dd]el?|[Uu]n|[Cc]ada|[Ss]us|[Oo]tras?|[Dd]os|[Ee]stas?|[Ee]sas?|[Ee]n) ') + #105
lema(ur'[Ss]istem_á_tic(?:[ao]s?|amente)_a', xpos=[ur' de angiospermas']) + #102
lema(ur'Rep_ú_blica Dominicana_u') + #100
lema(ur'[Ee]xtra_í_(?:a[ns]?|d[ao]s?)_i') + #94
lema(ur'[Ee]xtra_í_d[ao]s?_i') + #94
lema(ur'[Pp]or s_í so_l[ao]s?_(?:i s[oó]|í só)') + #90
lema(ur'[Ll]o_s_ (?:habitantes|hechos|hermanos|héroes|hijos|hombres|huevos|indígenas|intereses|jóvenes|juegos|jugadores|líderes|límites|machos|medios|mercados|meses|métodos|miembros|modelos|momentos|motores|municipios|músicos|nazis|niños|niveles|ojos|otros|padres|países|partidos|pasos|períodos|personajes|pobladores|pocos|poderes|precios|premios|primeros|principales|principios|problemas|programas|pueblos|puntos|quales|relatos|resultados|reyes|ríos|sábados|sectores|seis|seres|servicios|siglos|siguientes|símbolos|sistemas|sitios|soldados|sucesos|suelos|territorios|tiempos|trabajos|trenes|tres|últimos|únicos|usuarios|valores|vascos|vecinos|votos)_') + #86
lema(ur'[Cc]aracter_í_stic[ao]s?_i') + #85
lema(ur'[Mm]_á_scaras?_a', pre=ur'(?:[Ll]as?|[Uu]nas?|[Ss]us?) ') + #84
lema(ur'[Cc]__omo_omo c', xpre=[ur'[Yy]o ']) + #83
lema(ur'_el á_rea_(?:el a|la [aá])') + #83
lema(ur'[Ll]_í_deres_i') + #82
lema(ur'[Mm]_ás allá__(?:as all[aá]|ás alla)') + #82
lema(ur'[Vv][eé][aá]se _t_ambi[eé]n_T') + #82
lema(ur'_É_xitos?_E') + #79
lema(ur'[Mm]ayor_í_as?_i') + #78
lema(ur'[Rr]eci_bió__(?:vi[oó]|bio)') + #78
lema(ur'[Dd]esign_ó__o') + #76
lema(ur'[Ii]n_i_cia(?:[rlns]|les|tivas?|lmente|ría[ns]?|ron|ndo|d[ao]s?|ción|ciones|)_') + #76
lema(ur'_e_ste (?:último|primer)_é') + #76
lema(ur'[Pp]ac_í_fico_i', pre=ur'([Ee]l|[Dd]el) ') + #74
lema(ur'(?:[Ss]emid|[Ss]ubd|[Hh]iperd|[Dd])esa_rroll_(?:ó|os?|a[nrs]?|ad[ao]s?|ando|ador|adora|adores|arse|aron|ar[ií]a[ns]?|aba[ns]?)_(?:roll|rr?oy|rrol)') + #73
lema(ur'_R_usia_r', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #73
lema(ur'[Aa]rqueol_ó_gic[ao]s?_o') + #70
lema(ur'[Ss]_o_la(?:s|mente|)_ó') + #70
lema(ur'[t]rav_é_s_e', pre=ur'(?:[Aa]|[Dd]e) ') + #70
lema(ur'[Ee]spect_á_culos?_a') + #68
lema(ur'[Tt]ec_noló_gic[ao]_(?:nolo|onol[oó])') + #67
lema(ur'_e_sto_é') + #67
lema(ur'[Pp]rot_e_ic[ao]s?_é') + #66
lema(ur'[Ss]it_ú_(?:a[ns]?|e[ns]?)_u') + #66
lema(ur'[Cc]_ó_mo_o', pre=ur'¿ *') + #65
lema(ur'[Ff]__ue_ue f') + #65
lema(ur'[Uu]n_a_ (?:abogada|academia|aerolínea|alarma|aliada|apariencia|apertura|apuesta|arquitectura|asamblea|asesina|audiencia|aventura|bahía|balada|bandeja|bandera|bestia|biblioteca|bicicleta|botella|búsqueda|cabaña|cabina|cafetería|campeona|capilla|cascada|catarata|categoría|caña|chaqueta|charla|ciencia|cirugía|colonia|columna|completa|comuna|consola|copa|corneta|cota|cuarta|cuenca|cultura|cuota|cápsula|dama|danza|decena|densa|dependencia|destacada|desventaja|dieta|diseñadora|docena|droga|ejecutiva|elevada|embajadora|emboscada|emisora|empleada|encuesta|enfermera|era|escuadra|espada|estética|factoría|falda|falta|farsa|firma|flecha|fractura|fragata|fuga|gata|gigantesca|gorra|grieta|gruesa|hembra|hermosa|hierba|ideología|industria|invitada|jornada|liga|linterna)\b_') + #65
lema(ur'[Bb]_ú_squedas?_u') + #64
lema(ur'[Pp]__or_or p') + #63
lema(ur'_ó_rdenes_o', pre=ur'(?:[Ll]as|[Uu]nas|[Ss]us|[Dd]ar|[Dd]ando|[Pp]or) ') + #63
lema(ur'[Aa]p_ó_stol_o', pre=ur'(?:Andr[eé]s|Juan|Jaime|Pedro|Pablo|Santiago|Mateo|Mat[ií]as|Tom[aá]s|Bartolom[eé]) ') + #62
lema(ur'[Hh]ab_í_a(?:n|mos)_i') + #62
lema(ur'[Pp]r_é_stamo_e') + #61
lema(ur'[Rr]e_ú_ne[ns]?_u') + #61
lema(ur'[Dd]if_í_cil(?:es|mente|)_i') + #60
lema(ur'[Ll]o_s_ (?:aires|alrededores|alumnos|antiguos|años|artistas|barrios|bienes|bosques|capítulos|casos|casos|cerros|chicos|ciudadanos|códigos|colores|conceptos|cuales|cuáles|cuartos|datos|derechos|días|dientes|dos|edificios|efectos|ejercicios|elementos|enemigos|equipos|españoles|estándares|estudiantes|eventos|fans|franceses|ganadores|generales|grupos)_') + #60
lema(ur'[Uu]n_a_ (?:lujosa|lámina|lámpara|lápida|maestría|magnífica|maniobra|maqueta|mascota|materia|mayoría|memoria|mesa|meseta|minoría|mirada|molécula|moneda|máscara|máxima|música|norma|novia|olla|onda|palma|parcela|parroquia|partida|patrulla|pausa|pena|perfecta|pierna|pila|pionera|piscina|poca|poderosa|polémica|portada|prenda|presa|previa|proclama|profesora|prostituta|próxima|puesta|racha|rana|recarga|receta|recta|reina|reja|relativa|república|reseña|residencia|resistencia|retrospectiva|rotura|ruptura|ráfaga|saga|salida|sencilla|senda|sentencia|seria|sexta|significativa|suma|superheroína|supuesta|sustancia|sátira|tanda|tela|tendencia|terapia|textura|tormenta|treintena|trompeta|tropa|tía|túnica|vaina|vara|variada|ventana|vuelta|válvula|víctima|ópera)\b_') + #60
lema(ur'Mosc_ú__u') + #59
lema(ur'[Mm]_á_s (?:adelante|atrás|dos)\b_a') + #58
lema(ur'[e]n_ _medio_') + #56
lema(ur'[Ff]ilmograf_í_as?_i') + #55
lema(ur'[Hh]idrograf_í_as?_i') + #55
lema(ur'[Ii]m_a_gen_á') + #55
lema(ur'[Mm]_á_s (?:actual|afinidad|calor|espectacular|fértil|gol|letal|posibilidad|principal|real|regular|septentrional|usual)(?:es|)\b_a') + #55
lema(ur'[Cc]__on_on c') + #54
lema(ur'[Mm]iner_í_as?_i') + #54
lema(ur'[Pp]odr_í_a(?:[ns]?|mos)_i') + #54
lema(ur'_C_olombia_c', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #54
lema(ur'[Hh]u_i_(?:r(?:l[aeo]s?|se|)|d[ao]s?)_í') + #52
lema(ur'[Cc]om_ú_nmente_u') + #51
lema(ur'[Ff]_á_cil(?:mente|)_a') + #51
lema(ur'[Vv]_í_ctimas?_i', pre=ur'(?:[Ee]s|[Ff]u[ée]|[Ff]ueron|[Ll]as?|[Ss]erá|[Ss]on|[Uu]nas?|[Oo]tras?|[Dd]e|[Ss]u) ') + #51
lema(ur'[Hh]u_i_d[ao]s?_í') + #50
lema(ur'[Pp]r_ó_xim(?:[ao]s|amente)_o') + #50
lema(ur'[Tt]_e_sis_é') + #49
lema(ur'[Ee]n e_l_ año_n') + #48
lema(ur'[Ss]_í_ntesis_i') + #48
lema(ur'[Cc]_é_sped_e') + #47
lema(ur'[Vv]eh_í_culos?_i') + #47
lema(ur'_Japó_n_(jap[oó]|Japo)', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #47
lema(ur'[Dd]iecis_é_is_e') + #46
lema(ur'[Jj]_o_ven_ó') + #46
lema(ur'[Aa]m_é_rica (?:del [Nn]orte|del [Ss]ur|[Cc]entral|[Hh]ispana|[Aa]nglosajona|de Cali)_e') + #45
lema(ur'T_ú_nez_u') + #44
lema(ur'[Ee]spec_í_fic(?:[ao]s|amente)_i') + #44
lema(ur'[Aa]rtiller_í_as?_i') + #43
lema(ur'[Rr]_á_pid(?:[ao]s|amente)_a') + #42
lema(ur'[Tt]en_í_an_i') + #42
lema(ur'[Dd]_ó_lares_o', pre=ur'(?:[Ll]os|[Uu]nos|[Ee]n|[Dd]e|[0-9]+|[0-9][0-9.,]+[0-9]) ') + #41
lema(ur'[Ee]xclu_i_d[ao]s?_í') + #41
lema(ur'[Aa]erol_í_neas?_i') + #40
lema(ur'[Bb]_á_sic(?:as|os?|amente)_a') + #40
lema(ur'[Dd]i_á_metros?_a') + #40
lema(ur'[m]_á_s_a', pre=ur'(?:[Nn]o (?:cultivan?)|atendió|da|[Ll]ea|[Pp]ara|produciendo|espec[ií]fic(?:[ao]s?|amente)) ') + #40
lema(ur'_d_estacados_D', pre=ur'[Jj]ugadores ') + #40
lema(ur'[Dd]estru_i_d[ao]s?_í') + #39
lema(ur'[Mm]_á_s (?:cambi|campeonat|dat|equip|fot|minut|reconocimient|refuerz|sencill|tir|trabaj|títul)os?\b_a') + #37
lema(ur'_ú_nico_u', pre=ur'(?:[Ee]l|[Uu]n) ') + #37
lema(ur'C_ú_cuta_u') + #36
lema(ur'Emiratos _Á_rabes Unidos_A') + #36
lema(ur'[Ll]a_s_ grandes_') + #36
lema(ur'[Ll]leg_ó a s_er_(?:o a s|[oó] hac)') + #36
lema(ur'_a_ (?:abrazar|abrir|acceder|aceptar|aclarar|actuar|admitir|adquirir|afectar|ahorrar|ampliar|andar|apalizar|aparecer|aprender|arreglar|asar|ascender|asistir|asumir|atacar|atender|atrapar|aumentar|averiguar|avisar|ayudar|añadir|buscar|caer|cambiar|cancelar|cantar|castigar|cazar|celebrar|cerrar|cobrar|coincidir|combinar|comer|comercializar|cometer|competir|completar|componer|comprar|comprender|conocer|conseguir|considerar|consolar|construir|consumir|convertir|cosechar|crear|cultivar|dar|decir|declarar|definir|dejar|demostrar|denunciar|derramar|desarrollar|desartillar|descender|descubrir|desempeñar|destacar|destruir|detener|devolver|disculpar|disertar|diseñar|disputar|doblar|dominar|efectuar|ejercer|elegir|empezar|emprender|enamorar|encontrar|enfrentar|engrosar|entender|entrar|enviar|esconder|escribir|esperar|estacionar|estar|estudiar|evitar|examinar|existir|experimentar|extraer|extrañar|fabricar|facturar|finalizar|firmar|forjar|formar|formar|ganar|generar|gestar|grabar|haber|hablar|hacer|impartir|implantar|destinar|impulsar|incrementar|informar|inmortalizar|interpretar|investigar|ir|jugar|labrar|levantar|licuar|llegar|llevar|lograr|mantener|marcar|matar|mencionar|morir|necesitar|notar|obtener|ocurrir|ofertar|oficiar|orar|parar|participar|partir|pasar|pesar|pensar|permitir|persistir|poder|poner|practicar|preparar|presentar|producir|promediar|promocionar|proporcionar|protagonizar|publicar|pulsar|quedar|quitar|realizar|recibir|reclamar|recoger|recolectar|reconocer|recopilar|recordar|reeditar|regresar|rellenar|renovar|renunciar|repetir|reprender|respetar|resurgir|retomar|saber|salir|seguir|sobredestacar|solicitar|sufrir|tabajar|tener|tomar|torturar|trabajar|transmitir|trazar|usar|utilizar|vejar|vender|ver|verificar|viajar|visitar|volar)_(?:ha|ah)') + #36
lema(ur'_Ú_ltimas?_U', pre=ur'(?:[Ll]as?|[Uu]nas?) ') + #36
lema(ur'[Gg]rupo_s__', pre=ur'[Ll]os ') + #35
lema(ur'[Mm]_u_sical_ú') + #35
lema(ur'_Á_rbitros?_A') + #35
lema(ur'[Aa]tribu_i_d[ao]s?_í') + #34
lema(ur'[Cc]on_strui_d[ao]s?_(?:tru[ií]|struí)') + #34
lema(ur'[Cc]on_strui_d[ao]s?_(?:tru[ií]|struí)') + #34
lema(ur'[Dd]isput_ó_ en_o') + #34
lema(ur'[Pp]r_á_ctic(?:os|amente)_a') + #34
lema(ur'[Dd]_el á_rea_(?:el a|e la [aá])') + #33
lema(ur'[Hh]elic_ó_pteros?_o') + #33
lema(ur'[Hh]oland_é_s_e') + #33
lema(ur'[p]ertene_nci_as?_c[ií]', pre=ur'(?:[Ll]as?|[Ss]us?|[Dd]e) ') + #33
lema(ur'_á_guilas?_a') + #33
lema(ur'_ú_nica_u', pre=ur'(?:[Ll]a|[Uu]na|[Ss]u|es|será) ') + #33
lema(ur'[Ii]nclu_í_a[ns]?_i') + #32
lema(ur'[g]_é_neros?_e', pre=ur'(?:[Ee]l|[Ll]os|[Uu]n|[Uu]nos) ') + #32
lema(ur'[Aa]lien_í_genas?_i') + #31
lema(ur'[Ee]con_ó_mic(?:[ao]s|amente)_o') + #31
lema(ur'[Ss]__on_on s') + #31
lema(ur'_E_spaña_e', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #31
lema(ur'_E_sto_É') + #31
lema(ur'Azerbaiy_á_n_a') + #30
lema(ur'[Ee]mpe_zó__(?:s[oó]|zo)') + #30
lema(ur'[Tt]ra_í_d[ao]s?_i') + #30
lema(ur'[Cc]irug_í_as?_i') + #29
lema(ur'[Ee]squ_í__i') + #29
lema(ur'[Ff]_utbolí_stic(?:[ao]s?|amente)_útbol[ií]') + #29
lema(ur'_ú_ltimas_u', pre=ur'(?:[Ll]as|dos|tres) ') + #29
lema(ur'[Hh]_ú_med[ao]s?_u') + #28
lema(ur'[Jj]uda_í_smo_i') + #28
lema(ur'[Ll]a_s_ islas_') + #28
lema(ur'[Ll]a_s_ obras_') + #28
lema(ur'[Mm]ediod_í_as?_i') + #28
lema(ur'[Aa]p_é_ndices?_e') + #27
lema(ur'[Cc]an_c_i(?:ón|ones)_s', xpre=[ur'Serrat: ', ur'Cansiones\|'], xpos=[ur' barias', ]) + #27
lema(ur'[Rr]eci_é_n_e') + #27
lema(ur'[v]iv(?:ir|)_í_a[ns]?_i') + #27
lema(ur'_V_enezuela_v', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #27
lema(ur'[Ll]a_s_ elecciones_') + #26
lema(ur'[Ll]o_s_ (?:hinchas|hindúes|honores|hospitales|huecos|huertos|humanos|húngaros|indios|informes|ingleses|inicios|instrumentos|integrantes|isleños|jardines|jefes|jesuitas|judíos|jueces|juguetes|libros|llamados|lugareños|lugares|máximos|mensajes|miles|militares|monjes|motivos|muros|nombres|números|objetivos|oídos|organismos|órganos|pacientes|pájaros|paquetes|parámetros|participantes|peces|periódicos|pies|pilotos|pioneros|piratas|planes|prisioneros|productos|profesores|propietarios|propios|proyectos|puentes|puestos|radares|rayos|rebeldes|receptores|recursos|referentes|regalos|reinos|religiosos|requerimientos|requisitos|sacerdotes|sacrificios|santos|satélites|secretos|seguidores|segundos|sentidos|sentimientos|señoríos|servidores|sindicatos|síntomas|sobrevivientes|sonidos|sospechábamos|sueños|suministros|tallos|templos|terrenos|testigos|tipos|títulos|túneles|turistas|unos|valles|viajes|vídeos|vientos)_') + #26
lema(ur'[d]esar_rolló__r?oll?o', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #26
lema(ur'[Cc]ercan_í_as?_i') + #25
lema(ur'[Dd]istribu_i_d[ao]s?_í') + #25
lema(ur'[m]_á_ximas?_a', pre=ur'(?:[Ll]as?|[Uu]nas?) ') + #25
lema(ur'[Pp]ort_á_til(?:es|)_a') + #24
lema(ur'[Ss]ubg_é_neros?_e') + #24
lema(ur'[Ll]a_s_ ciudades_') + #23
lema(ur'[Pp]_á_rrafos?_a') + #23
lema(ur'[Pp]eriod_í_stic[ao]s?_i') + #23
lema(ur'[Pp]rotag_ó_nic[ao]s?_o') + #23
lema(ur'Kirguist_á_n_a') + #22
lema(ur'[Cc]onclu_i_(?:r(?:l[aeo]s?|se|)|d[ao]s?)_í') + #22
lema(ur'[Ee]__ntre_ntre e') + #22
lema(ur'[Ee]__ntre_ntre e') + #22
lema(ur'[Pp]odr_á_[ns]?_a') + #22
lema(ur'[Ss]__er_er s') + #22
lema(ur'[Ss]obre__nombre_ ') + #22
lema(ur'[Ss]ustitu_i_d[ao]s?_í') + #22
lema(ur'[Cc]onclu_i_d[ao]s?_í') + #21
lema(ur'[Ff]_u_tbolistas?_ú') + #21
lema(ur'[Ff]utbol_í_stic[ao]_i') + #21
lema(ur'[Gg]eneral_í_sim[ao]s?_i') + #21
lema(ur'[Ii]nstru_i_d[ao]s?_í') + #21
lema(ur'[Bb]ioqu_í_mic[ao]s?_i') + #20
lema(ur'[Cc]at_á_logo_a', pre=ur'(?:[Ee]l|[Uu]n|[Dd]e) ') + #20
lema(ur'[Dd]_e_cimocuart[ao]_é') + #20
lema(ur'[Dd]_e_cimoquint[ao]_é') + #20
lema(ur'[Ll]__o_o l') + #20
lema(ur'[Mm]ercanc_í_as?_i') + #20
lema(ur'[Rr]e_í_r_i') + #20
lema(ur'[Tt]_i_tulad[ao]s?_í') + #20
lema(ur'[Aa]__ños_ños a') + #19
lema(ur'[Ff]olcl_ó_ric[ao]s?_o') + #19
lema(ur'[Hh]idrogr_á_fic[ao]s?_a') + #19
lema(ur'[Ll]a_s_ cuales_') + #19
lema(ur'[Ll]a_s_ fuerzas_') + #19
lema(ur'[Ll]a_s_ primeras_') + #19
lema(ur'[Mm]am_í_fer[ao]s?_i') + #19
lema(ur'[Mm]ientra_s__') + #19
lema(ur'[Nn]eocl_á_sic[ao]s?_a') + #19
lema(ur'[Pp]rote_í_nas?_i') + #19
lema(ur'(?:[Pp]|[Cc]op)rop__iedad(?:es|)_r') + #18
lema(ur'[Cc]ie_mpié_s_(?:npi[eé]|mpie)') + #18
lema(ur'[Cc]onv_i_rti(?:ó|endo|eron)_e') + #18
lema(ur'[Ee]j_é_rcitos_e') + #18
lema(ur'[Ll]a_s_ calles_') + #18
lema(ur'[Ll]o_s_ (?:aborígenes|acontecimientos|actores|actos|acuerdos|admiradores|agentes|albores|alemanes|alimentos|andes|animales|anteriores|árboles|arcos|arqueólogos|arquitectos|arreglos|asuntos|ataques|autores|bancos|baños|beneficios|británicos|buques|cabellos|cambios|campeones|campos|canales|cánones|cargos|carros|centros|cimientos|clubes|colonizadores|concursantes|continentes|continuos|créditos|cronistas|cuadernos|cuadros|cuchillos|cursos|detalles|dibujos|documentos|donativos|ejecutivos|ejemplares|ejes|elfos|empleados|enamorados|encuentros|enérgicos|entes|episodios|escenarios|esclavos|esfuerzos|espectadores|estadounidenses|estilos|exámenes|extranjeros|extremos|factores|fallos|familiares|fanáticos|ferrocarriles|fines|firmantes|fondos|fundadores|gallegos|géneros|gobernadores|gobiernos|guerreros)_') + #18
lema(ur'[Mm]_é_todos_e') + #18
lema(ur'_consultado el__acessado em') + #18
lema(ur'[Cc]a_m_pos_n') + #17
lema(ur'[Cc]on_s_tru(?:ir(?:lo|se|á|án|ía|ían|)|cción|cciones)_') + #17
lema(ur'[Cc]r_í_menes_i') + #17
lema(ur'[Dd]ebutar_í_a[ns]?_i') + #17
lema(ur'[Gg]anader_í_a_i') + #17
lema(ur'[Oo]c_éano Í_ndico_(?:eano [iíIÍ]|éano [iIí])') + #17
lema(ur'[Pp]erder_í_a[ns]?_i') + #17
lema(ur'[Pp]ermit(?:ir|)_í_a[ns]?_i') + #17
lema(ur'[Ss]imult_á_neamente_a') + #17
lema(ur'[Tt]ie_m_po_n') + #17
lema(ur'[Tt]ra_í_dos?_i') + #17
lema(ur'[Vv]eintitr_é_s_e') + #17
lema(ur'[Aa]g_o_sto_u', pre=ur'(?:[Dd]e|[0-9]+\.?) ') + #16
lema(ur'[Aa]pro_b_ad[ao]s?_v') + #16
lema(ur'[Cc]ontin_ú_(?:an|en)_u') + #16
lema(ur'[Dd]_í_gitos?_i') + #16
lema(ur'[Dd]ij_o__ó') + #16
lema(ur'[Dd]iri_g_i(?:d[ao]s?|r(?:[tsm]e|á|ía[ns]|l[aeo]s?|))_j') + #16
lema(ur'[Ll]a_s_ relaciones_') + #16
lema(ur'[Mm]_á_gic(?:[ao]s|amente)_a') + #16
lema(ur'[Nn]ecrol_ó_gic[ao]s?_o') + #16
lema(ur'[Pp]ict_ó_ric[ao]s?_o') + #16
lema(ur'[Pp]ing_ü_inos?_u') + #16
lema(ur'[Ss]__obre_obre s') + #16
lema(ur'_F_rancia_f', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #16
lema(ur'_escándalo__escandalo') + #16
lema(ur'Arbel_á_ez_a') + #15
lema(ur'[Cc]onoc_í_a[ns]?_i') + #15
lema(ur'[Cc]ont_ó_ (?:que|como|con)_o') + #15
lema(ur'[Cc]ontra_í_(?:a[ns]?|d[ao]s?)_i') + #15
lema(ur'[Ee]n_ _serio_') + #15
lema(ur'[Ee]xist_í_a[ns]?_i') + #15
lema(ur'[Ii]leg_í_tim(?:as?|os?|amente)_i') + #15
lema(ur'[Ii]ncre_í_ble(?:s|mente)_i') + #15
lema(ur'[Ll]a_s_ personas_') + #15
lema(ur'[Nn]_á_useas_a') + #15
lema(ur'[Pp]__rimer_rimer p') + #15
lema(ur'[Pp]ri_n_cipal(?:es|mente|)_') + #15
lema(ur'[Pp]roven_í_a[ns]?_i') + #15
lema(ur'[Ss]__i_i s') + #15
lema(ur'[Tt]el_é_fonos_e') + #15
lema(ur'_(discográfica)__\(record label\)') + #15
lema(ur'_I_talia_i', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #15
lema(ur'_c_heco_C', pre=ur'\b(?:e[ln]|del|idioma|y) ') + #15
lema(ur'[Aa]_ _partir_') + #14
lema(ur'[Cc]_ó_nyuges?_o') + #14
lema(ur'[Dd]eber_í_a(?:[ns]?|mos)_i') + #14
lema(ur'[Dd]espose_í_d[ao]s?_i') + #14
lema(ur'[Ee]st_á_ndares_a') + #14
lema(ur'[Ee]xpl_í_cit(?:[ao]s|amente)_i') + #14
lema(ur'[Ll]_á_piz_a') + #14
lema(ur'[Ll]a_s_ provincias_') + #14
lema(ur'[Ll]eg_í_tim(?:as|os|amente)_i') + #14
lema(ur'[Nn]eum_á_tic[ao]s?_a') + #14
lema(ur'[Tt]__ambién_ambién t') + #14
lema(ur'[Vv]eintis_é_is_e') + #14
lema(ur'[d]eb_í_a(?:s?|mos)_i') + #14
lema(ur'_ó_mnibus_o', pre=ur'\b(?:y|[Ee]l|[Uu]n|de|en|trenes|Micro|son|transporte:|llamados|scientiis|formato|tomaran|Empresa|tituló) (?:["\']|\[\[|)') + #14
lema(ur'[Aa]ntag_ó_nic[ao]s?_o') + #13
lema(ur'[Cc]_ó_digos_o') + #13
lema(ur'[Cc]h_á_rter_a', pre=ur'(?:aerolíneas?|vuelos?|tipos?|modos?)(?: de|) ') + #13
lema(ur'[Cc]l_í_nic(?:[ao]s|amente)_i') + #13
lema(ur'[Cc]r_á_neos?_a') + #13
lema(ur'[Dd]_í_a a d[ií]a_i') + #13
lema(ur'[Dd]eber_á_[ns]?_a') + #13
lema(ur'[Dd]estitu_i_d[ao]s?_í') + #13
lema(ur'[Dd]iri_gí_a[ns]?_(?:j[ií]|gi)') + #13
lema(ur'[Ee]__ra_ra e') + #13
lema(ur'[Ee]rr_ó_neamente_o') + #13
lema(ur'[Ee]xcelent_í_sim[ao]s?_i') + #13
lema(ur'[Hh]__a [a-záéíóúñ]+o_a h') + #13
lema(ur'[Ll]a_s_ mujeres_') + #13
lema(ur'[Ll]a_s_ series_') + #13
lema(ur'[Ll]a_s_ siguientes_') + #13
lema(ur'[Mm]_ú_ltiples?_u', pre=ur'\b(?:Monitores|en|por|creado|normales|reclutando|[Cc]opias| de|Tiene|esclerosis|[Ee]lectrica) ', xpre=[ur'Pénétrations ', ]) + #13
lema(ur'[Pp]__uede_uede p') + #13
lema(ur'[Rr]eco_g_(?:e[nrs]?|erl[aeo]s?|erán|id[ao]s?|iendo|ieron|imiento|ió|í)_j') + #13
lema(ur'[Rr]egad_í_os?_i') + #13
lema(ur'[Tt]__iene_iene t') + #13
lema(ur'[Tt]_ó_xic(?:as|os?)_o') + #13
lema(ur'[Tt]ransg_é_ner[ao]s?_e') + #13
lema(ur'[Vv]erg_ü_enzas?_u') + #13
lema(ur'[Vv]olver_í_a(?:n|mos|)_i') + #13
lema(ur'Benalc_á_zar_a') + #12
lema(ur'[Aa]_ _cabo_', pre=ur'[Ll]lev(?:[oó]|aron|a[ns]?) ') + #12
lema(ur'[Aa]maz_ó_nic(?:as|os?)_o') + #12
lema(ur'[Aa]rque_ó_log[ao]s?_o') + #12
lema(ur'[Cc]__uando_uando c') + #12
lema(ur'[Cc]ardiolog_í_as?_i') + #12
lema(ur'[Dd]ec_í_a[ns]?_i', pre=ur'(?:[Qq]u[eé]|[Ss]e|[Ll]es?|[Mm]e|[Nn]os|[Ll]o|[Ss]eg[uú]n|[Dd]onde|[Cc]u[aá]l|[Cc][oó]mo|[Ss][oó]lo|[EeÉ]l|[Qq]ui[eé]n) ') + #12
lema(ur'[Ee]nc_o_ntraba[ns]?_ue') + #12
lema(ur'[Ee]stu_v_(?:[eo]|ieron|iese[ns]?|iera[ns]?)_b') + #12
lema(ur'[Gg]eogr_á_fic(?:[ao]s|amente)_a') + #12
lema(ur'[Hh]idr_á_ulic[ao]s?_a') + #12
lema(ur'[Hh]idroel_é_ctric[ao]s?_e') + #12
lema(ur'[Ii]_mpresió_n_(?:npre[sc]i[oó]|mpreci[oó]|mpresio)') + #12
lema(ur'[Ll]a_s_ principales_') + #12
lema(ur'[Mm]antendr_á_[ns]?_a') + #12
lema(ur'[Qq]u_í_mic(?:[ao]s|amente)_i') + #12
lema(ur'[Ss]iller_í_as?_i') + #12
lema(ur'[Ss]in_ó_nimos?_o') + #12
lema(ur'[Tt]endr_í_a[ns]?_i') + #12
lema(ur'[Tt]ransmit(?:ir|)_í_a[ns]?_i') + #12
lema(ur'[s]erv_í_a_i') + #12
lema(ur'_E_ste (?:último|primer)_É') + #12
lema(ur'_e_sta (afición|vez)_é') + #12
lema(ur'[Cc]ron_ó_metros?_o') + #11
lema(ur'[Hh]abr_í_as?_i') + #11
lema(ur'[Ii]nstitu_i_d[ao]s?_í') + #11
lema(ur'[Ii]nte_r_pretad[ao]s?_') + #11
lema(ur'[Ll]a_s_ especies_') + #11
lema(ur'[Ll]a_s_ leyes_') + #11
lema(ur'[Ll]a_s_ listas_') + #11
lema(ur'[Ll]a_s_ palabras_') + #11
lema(ur'[Ll]a_s_ partes_') + #11
lema(ur'[Ll]a_s_ regiones_') + #11
lema(ur'[Mm]edi_a_nte_e') + #11
lema(ur'[Mm]urci_é_lagos?_e') + #11
lema(ur'[Oo]bst_á_culos?_a') + #11
lema(ur'[Pp]_ó_lvoras?_o') + #11
lema(ur'[Pp]ac_í_fic(?:as|os|amente)_i') + #11
lema(ur'[Pp]or_ _ciento_') + #11
lema(ur'[Pp]ro_b_ad[ao]s?_v') + #11
lema(ur'[Ss]_i_guie(?:ron|ntes?)_e') + #11
lema(ur'[Ss]egu(?:ir|)_í_a[ns]?_i') + #11
lema(ur'[Tt]ao_í_s(?:tas?|mo)_i') + #11
lema(ur'_é_tnic(?:[ao]s|amente)_e') + #11
lema(ur'[Cc]arn_í_vor(os?|as)_i') + #10
lema(ur'[Cc]ore_ó_graf[ao]s?_o') + #10
lema(ur'[Cc]re_í_d[ao]s?_i') + #10
lema(ur'[Ee]__pisodios?_s') + #10
lema(ur'[Ee]st_ó_magos?_o') + #10
lema(ur'[Ee]strat_é_gic[ao]_e') + #10
lema(ur'[Hh]idr_ó_genos?_o') + #10
lema(ur'[Hh]o_mó_nim[ao]s?_(?:mo|n[oó])') + #10
lema(ur'[Ii]ncon_sc_ientes?_[sc]') + #10
lema(ur'[Jj]ur_í_dicas(?!\.(?:com|unam\.mx))_i') + #10
lema(ur'[Ll]a_s_ costas_') + #10
lema(ur'[Ll]a_s_ fechas_') + #10
lema(ur'[Ll]a_s_ líneas_') + #10
lema(ur'[Mm]o_nstru_o_unstr') + #10
lema(ur'[Pp]_í_ldoras?_i') + #10
lema(ur'[Pp]u__dieron_e') + #10
lema(ur'[Rr]ecib(?:ir|)_í_a[ns]?_i') + #10
lema(ur'[Rr]eempla_zó__(?:s[oó]|zo)', pre=ur'(?:[Ll]o|[Ss]e(?: me| te| l[aeo]s?|)) ') + #10
lema(ur'[Tt]_í_teres?_i') + #10
lema(ur'[Tt]rig_é_sim[ao]s?_e') + #10
lema(ur'[Uu]n_á_nime(?:mente|)_a') + #10
lema(ur'[f]ranc_é_s[,.]_e') + #10
lema(ur'[t]_é_rminos_e', pre=ur'[Ll]os ') + #10
lema(ur'_ú_nicos_u', pre=ur'(?:[Ss]us|[Ll]os) ') + #10
lema(ur'Ad_í_s Abeba_i') + #9
lema(ur'[Aa]p_ó_stol (?:San|Andr[eé]s|Juan|Jaime|Pedro|Pablo|Santiago|Mateo|Mat[ií]as|Tom[aá]s|Bartolom[eé])_o') + #9
lema(ur'[Aa]utom_á_tic(?:[ao]s|amente)_a') + #9
lema(ur'[Cc]re_í_a(?:[ns]?|mos)_i') + #9
lema(ur'[Cc]u_á_ntic[ao]s?_a') + #9
lema(ur'[Dd]__esde_esde d') + #9
lema(ur'[Ee]star_í_a(?:[ns]?|mos)_i') + #9
lema(ur'[Gg]inecolog_í_as?(?! (?:Ospedalieri|e (?:Ostetricia|Obstétrícia)))_i') + #9
lema(ur'[Hh]_á_bil(?:es|mente)_a') + #9
lema(ur'[Hh]_í_gados?_i') + #9
lema(ur'[Ii]lustr_í_sim[ao]s?_i') + #9
lema(ur'[Ll]a_s_ bases_') + #9
lema(ur'[Ll]a_s_ divisiones_') + #9
lema(ur'[Ll]a_s_ iglesias_') + #9
lema(ur'[Ll]a_s_ poblaciones_') + #9
lema(ur'[Mm]_utua_mente_(?:útual?|utual)') + #9
lema(ur'[Nn]ov_í_sim[ao]s?_i') + #9
lema(ur'[Pp]irater_í_as?_i') + #9
lema(ur'[Pp]opurr_í__i') + #9
lema(ur'[Pp]rehisp_á_nic[ao]s?_a') + #9
lema(ur'[Pp]s_í_quic[ao]s?_i') + #9
lema(ur'[Rr]eco_g_e[ns]?_j') + #9
lema(ur'[Rr]etra_í_(?:a[ns]?|d[ao]s?)_i') + #9
lema(ur'[Rr]etra_í_d[ao]s?_i') + #9
lema(ur'[Rr]eun_í_a[ns]?_i') + #9
lema(ur'[Ss]em_á_foros?_a') + #9
lema(ur'[Ss]i_s_temas?_') + #9
lema(ur'[Ss]onr_í_e[ns]?_i') + #9
lema(ur'[Tt]el_é_fono_e', pre=ur'(?:[Ee]l|[Ss]u|[Uu]n|como|por) ') + #9
lema(ur'[Uu]n_a ré_plica_ r[eé]') + #9
lema(ur'_É_l (?:anhela|pued[ae]|gana)_E') + #9
lema(ur'_ú_ltimamente_u') + #9
lema(ur'(?:[Cc]on|[Ss](?:ub|))igu_i_entes?_') + #8
lema(ur'[Aa]cr_ó_nimos?_o') + #8
lema(ur'[Aa]lfarer_í_as?_i') + #8
lema(ur'[Aa]n_ó_nim(?:[ao]s|amente)_o') + #8
lema(ur'[Aa]parec_í_a[ns]?_i') + #8
lema(ur'[Aa]tra_í_d[ao]s?_i') + #8
lema(ur'[Cc]ad_á_veres_a') + #8
lema(ur'[Cc]atedr_á_tic[ao]s?_a') + #8
lema(ur'[Cc]o_o_peraci(?:ón|ones)_') + #8
lema(ur'[Cc]umpl(?:ir|)_í_a[ns]?_i') + #8
lema(ur'[Dd]__urante_urante d') + #8
lema(ur'[Dd]_e_cimosext[ao]_é') + #8
lema(ur'[Dd]escalific_ó__o') + #8
lema(ur'[Ee]__ste_ste e') + #8
lema(ur'[Ee]mit(?:ir|)_í_a[ns]?_i') + #8
lema(ur'[Ee]ncont_r_ar_') + #8
lema(ur'[Ee]sc_é_nic[ao]s?_e') + #8
lema(ur'[Ee]strat_é_gic(?:[ao]s|amente)_e') + #8
lema(ur'[Ee]xit_o_s(?:[ao]s?|amente)_ó') + #8
lema(ur'[Ff]__ueron_ueron f') + #8
lema(ur'[Ff]_í_sicamente(?! esposta)_i') + #8
lema(ur'[Hh]ect_á_reas?_a') + #8
lema(ur'[Hh]istolog_í_as?_i') + #8
lema(ur'[Ii]nform_á_tic[ao]s_a') + #8
lema(ur'[Ll]a_s_ autoridades_') + #8
lema(ur'[Ll]a_s_ condiciones_') + #8
lema(ur'[Ll]a_s_ estaciones_') + #8
lema(ur'[Ll]a_s_ ideas_') + #8
lema(ur'[Ll]a_s_ letras_') + #8
lema(ur'[Ll]a_s_ semifinales_') + #8
lema(ur'[Ll]a_s_ últimas_') + #8
lema(ur'[Ll]lam_a_d[ao]s?_') + #8
lema(ur'[Mm]asoner_í_as?_i') + #8
lema(ur'[Pp]oder_í_o_i') + #8
lema(ur'[Pp]ose_í_d[ao]s?_i') + #8
lema(ur'[Pp]r_á_cticas_a', pre=ur'(?:[Ll]as|[Uu]nas|[Ss]us) ') + #8
lema(ur'[Pp]ri_me_r[ao]s?_em') + #8
lema(ur'[Ss]eren_í_sim[ao]s?_i') + #8
lema(ur'[Ss]igu_i_entes?_') + #8
lema(ur'[Tt]elevis_i_ón_') + #8
lema(ur'[Tt]endr_á_[ns]_a') + #8
lema(ur'[Uu]n_a má_quina_ m[aá]') + #8
lema(ur'[l]e_í_da_i') + #8
lema(ur'_obstáculos__obstaculos') + #8
lema(ur'Logroñ_é_s_e') + #7
lema(ur'Pap_ú_a_u', pre=ur'(?:[Dd]e|[Ee]n) ') + #7
lema(ur'Se_ú_l_u', pre=ur'(?:[Dd]e|[Ee]n) ') + #7
lema(ur'Vig_í_a_i', pre=ur'El ') + #7
lema(ur'[Aa]br(?:ir|)_í_a[ns]?_i') + #7
lema(ur'[Aa]br_í_a[ns]?_i') + #7
lema(ur'[Aa]ct_ú_(?:a[ns]|e[ns]?)_u') + #7
lema(ur'[Aa]dquir_ió__(?:io|[oó])') + #7
lema(ur'[Aa]n_ó_nim[ao]_o', pre=ur'(?:[Ss]ociedad|[Mm]ensaje) ') + #7
lema(ur'[Aa]p_are_c(?:e(?:[ns]?|r(?:a[ns]?|[áé]|ía[ns]?|))|ieron)_(?:ara|re)') + #7
lema(ur'[Aa]pocal_i_psis_í') + #7
lema(ur'[Aa]rtific_i_al(?:es|)_') + #7
lema(ur'[Cc]_á_lculo (?:del?|num[eé]rico|mental|según|estructural)_a') + #7
lema(ur'[Cc]omp_i_tiera[ns]?_e') + #7
lema(ur'[Cc]ontadur_í_as?_i') + #7
lema(ur'[Cc]ontrar_r_evoluci(?:ón|onari[ao]s?)_') + #7
lema(ur'[Cc]re_í_bles?_i') + #7
lema(ur'[Dd]_é_biles(?! dignare)_e') + #7
lema(ur'[Dd]es_ig_nad[ao]s?_gi') + #7
lema(ur'[Dd]in_á_mic(?:[ao]s|amente)_a') + #7
lema(ur'[Dd]ispon_í_a[ns]?_i') + #7
lema(ur'[Ee]_m_perador_n') + #7
lema(ur'[Ee]_x_pectativas?_s') + #7
lema(ur'[Ee]sco_g_(?:e[nr]?|erl[aeo]s?|erá|es|id[aeo]s?|iendo|ieron|imos)_j') + #7
lema(ur'[Ff]erreter_í_as?_i') + #7
lema(ur'[Ff]lu_i_d[ao]s?_í') + #7
lema(ur'[Ff]ue_r_zas?_') + #7
lema(ur'[Gg]uitar_r_as?_') + #7
lema(ur'[Jj]esu_í_tic[ao]s?_i') + #7
lema(ur'[Jj]ugar_í_a[ns]?_i') + #7
lema(ur'[Ll]_a_s (?:Marquesas|Reducciones|SS|Sombras|\(muchas|arcadas|batallas|características|casas|charofitas|ciudades|colecciones|costas|críticas|dehesas|diferencias|doctrinas|dos puertas|entonces todopoderosa|escenas|especies|espiguillas|esporas|faldas|flores|fronteras|frutas|fuentes|fuerzas|hembras|hojas|indicaciones|inflorescencias|iniciales|inmunoglobulinas|islas|lenguas|lesbianas|leyes|listas|manchas|masas|mayores|mesas|mezquitas|misiones|mulas|negociaciones|normas|novelizaciones|nubes|nuevas|obras|orillas|películas|personas|posesiones|prematuras|prescriptivas|primeras|proximas|proximidades|puntas|raíces|regiones|respuestas|semifinales|sierras|siguientes|tierras|torturas|traducciones|ubicaciones|víctimas|yemas|zonas|órdenes)_') + #7
lema(ur'[Ll]_o_s (?:Agustinos|Caballeros|EE\.UU\.|Llanos|Mártires|Play offs|Reyes|Vertebrados|acompañantes|albores|ascensores|aumentos|años|barrios|bordes|casos|cetáceos|chicos|compañeros|críticos|cupones|cursos|descendientes|dialectos|enviados|episodios|extremos|ganadores|gemelos|grupos|hechiceros|hermanos|hijos|ingenieros|integrantes|intérpretes|investigadores|juegos|lados|lusitanos|machos|memorandos|monos|muchos|muertos|musicales|municipios|negativos|niños|nuevos|ojos|otros|parches|primeros|problemas|programas|pueblos|rebeldes|republicanos|restos|ríos|sacerdotes|seres|siete minutos|siglos|singles|sostenedores|temas|trabajos|trabajadores|tricomas|troncos|viejos)_') + #7
lema(ur'[Ll]a_s_ canciones_') + #7
lema(ur'[Ll]a_s_ inmediaciones_') + #7
lema(ur'[Ll]a_s_ nuevas_') + #7
lema(ur'[Ll]a_s_ otras_') + #7
lema(ur'[Ll]a_s_ posiciones_') + #7
lema(ur'[Ll]a_s_ revistas_') + #7
lema(ur'[Ll]a_s_ temporadas_') + #7
lema(ur'[Ll]a_s_ vías_') + #7
lema(ur'[Ll]leva(rá|) a_ _cabo_') + #7
lema(ur'[Mm]_u_sicales_ú') + #7
lema(ur'[Mm]ec_á_nic(?:[ao]s|amente)_a') + #7
lema(ur'[Mm]ercader_í_as?_i') + #7
lema(ur'[Pp]__arte_arte p') + #7
lema(ur'[Pp]r_á_cticas de_a') + #7
lema(ur'[Pp]retend_í_a[ns]?_i') + #7
lema(ur'[Pp]rovi_sio_(?:nal(?:es|)|nes)_ci[oó]') + #7
lema(ur'[Pp]siqui_á_tric[ao]s?_a') + #7
lema(ur'[Qq]uedar_í_a[ns]?_i') + #7
lema(ur'[Qq]uer_í_amos_i') + #7
lema(ur'[Qq]uer_í_amos_i') + #7
lema(ur'[Qq]uiz_á_s_a') + #7
lema(ur'[Rr]esid(?:ir|)_í_a[ns]?_i') + #7
lema(ur'[Ss]__ido_ido s') + #7
lema(ur'[Ss]aldr_á_[ns]?_a') + #7
lema(ur'[Ss]onre_í_r_i') + #7
lema(ur'[Tt]_í_pic(?:[ao]s|amente)_i') + #7
lema(ur'[Tt]erminar_í_a[ns]?_i') + #7
lema(ur'[Tt]itular_í_a[ns]?_i') + #7
lema(ur'[Tt]uber_í_as?_i') + #7
lema(ur'[Uu]t_ilizació_n_(?:lizaci[oó]|ilizacio)') + #7
lema(ur'[h]_a_ce_e') + #7
lema(ur'[m]_á_ximos?_a', pre=ur'(?:[Ee]l|[Uu]n|[Ll]os) ') + #7
lema(ur'[s]ab_í_an_i') + #7
lema(ur'_U_ruguay_u', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #7
lema(ur'_e_spañol_E', pre=ur'ejército ') + #7
lema(ur'_Á_ngel Gim[eé]nez_A') + #7
lema(ur'_á_gil(?:es|mente|)_a') + #7
lema(ur'[12][0-9]{3} _en cine__au cinéma', pre=ur'\[') + #6
lema(ur'[Aa]_ñ_os (?:antes|después)_n') + #6
lema(ur'[Aa]bsor_b_(e[rns]?|id[ao]s?)_v') + #6
lema(ur'[Bb]r_ú_julas?_u') + #6
lema(ur'[Cc]et_á_ceos?_a') + #6
lema(ur'[Cc]omisar_í_as?_i', pre=ur'[Ee]n ') + #6
lema(ur'[Cc]ongre_s_os?_') + #6
lema(ur'[Cc]onsist_í_a[ns]?_i') + #6
lema(ur'[Cc]onvert(?:ir|)_í_a[ns]?_i') + #6
lema(ur'[Cc]ronol_ó_gic(?:[ao]s|amente)_o') + #6
lema(ur'[Cc]ut_á_ne[ao]s?_a') + #6
lema(ur'[Dd]isminu_i_d[ao]s?_í') + #6
lema(ur'[Ee]mblem_á_tic(?:as|os?)_a') + #6
lema(ur'[Ee]mit_í_a[ns]?_i') + #6
lema(ur'[Ee]n_ _realidad_') + #6
lema(ur'[Ee]st_é__e', pre=ur'(?:[Ss]e )') + #6
lema(ur'[Hh]om_ó_nim[ao]s?_o') + #6
lema(ur'[Ii]ncon_s_cientes?_') + #6
lema(ur'[Ii]nt_é_rpretes_e', pre=ur'(?:[AaEe]l|[Uu]na?|[Ll][ao]s|[Pp]or|[Vv]ari[ao]s|[Ff]amos[ao]s?|[Aa]rtistas?|[Dd]estacad[ao]s?|[Oo]tr[ao]s?|[Mm]ejor(?:es|)|[Ee]st[ao]s?|[Mm]uch[ao]s?|[Cc]uy[ao]s?|[Aa]lgun[ao]s|[Aa]lgún|[Aa]lguna|[Cc]onocid[ao]s?|[Ss]us?|[0-9]+|[Pp]rimer|[Gg]ran|[Cc]on) ') + #6
lema(ur'[Ii]nte_r_pretando_') + #6
lema(ur'[Jj]ap_oné_s_óne') + #6
lema(ur'[Jj]ard_í_n [Bb]otánico_i') + #6
lema(ur'[Ll]a n_ó_mina(?! (?:di|al|a la|dubia|en|con))_o') + #6
lema(ur'[Ll]a_s_ actividades_') + #6
lema(ur'[Ll]a_s_ afueras_') + #6
lema(ur'[Ll]a_s_ empresas_') + #6
lema(ur'[Ll]a_s_ familias_') + #6
lema(ur'[Ll]a_s_ fiestas_') + #6
lema(ur'[Ll]a_s_ lenguas_') + #6
lema(ur'[Ll]a_s_ manos_') + #6
lema(ur'[Ll]a_s_ mismas_') + #6
lema(ur'[Mm]_á_rgenes_a') + #6
lema(ur'[Mm]a_m_postería_n') + #6
lema(ur'[Mm]orir_í_a[ns]?_i') + #6
lema(ur'[Mm]uch_í_sim[ao]s?_i') + #6
lema(ur'[Mm]usic_ó_log[ao]s?_o') + #6
lema(ur'[Nn]arcotr_á_ficos?_a') + #6
lema(ur'[Oo]__tros_tros o') + #6
lema(ur'[Oo]frec_í_a[ns]?_i') + #6
lema(ur'[Pp]asar_í_a[ns]?_i') + #6
lema(ur'[Pp]eluquer_í_as?_i') + #6
lema(ur'[Pp]ose_í_a[ns]?_i') + #6
lema(ur'[Pp]rofe_s_ional(?:es|)_c') + #6
lema(ur'[Rr]adiolog_í_as?_i') + #6
lema(ur'[Rr]eclu_i_d[ao]s?_í') + #6
lema(ur'[Ss]emiolog_í_as?_i') + #6
lema(ur'[Ss]eud_ó_nimos?_o') + #6
lema(ur'[Ss]obrese_í_d[ao]s?_i') + #6
lema(ur'[Ss]of_t_ware_') + #6
lema(ur'[Ss]of_á_s?_a', pre=ur'(?:[Ss]u|[Ee]l|[Dd]el|[Uu]n|[Ll]os|como) ') + #6
lema(ur'[Tt]_á_ctil(?:es|)_a') + #6
lema(ur'[Tt]errest_r_es?_') + #6
lema(ur'[Tt]rampol_í_n_i') + #6
lema(ur'_G_recia_g', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #6
lema(ur'_P_araguay_p', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #6
lema(ur'_encontraba__encuentraba') + #6
lema(ur'_Ú_ltimamente_U') + #6
lema(ur'Car_ú_pano_u') + #5
lema(ur'E_n_ (?:el|la|los|las)_N') + #5
lema(ur'[Aa]dvers_a_rios?_á') + #5
lema(ur'[Aa]gr_ó_nom[ao]s?_o') + #5
lema(ur'[Aa]nal_ó_gic[ao]s?_o') + #5
lema(ur'[Cc]a_cerí_as?_(?:zer[ií]|ceri)') + #5
lema(ur'[Cc]ampeon_í_sim[ao]s?_i') + #5
lema(ur'[Cc]apit_á_n Am[eé]rica_a') + #5
lema(ur'[Cc]onti_n_gentes?_') + #5
lema(ur'[Cc]ontribu_i_d[ao]s?_í') + #5
lema(ur'[Cc]ontribu_i_d[ao]s?_í') + #5
lema(ur'[Cc]onvertir_í_a[ns]?_i') + #5
lema(ur'[Cc]onvi__rtieron_e') + #5
lema(ur'[Dd]_ó_lar_o', pre=ur'(?:[Ee]l|[Uu]n|[Dd]el|[Aa]l) ') + #5
lema(ur'[Dd]escend_í_(?:a[ns]?|)_i') + #5
lema(ur'[Dd]esv_á_n_a') + #5
lema(ur'[Dd]ur_an_te_na') + #5
lema(ur'[Ee]_s_pectador(?:es|)_x') + #5
lema(ur'[Ee]mitir_á_[ns]?_a') + #5
lema(ur'[Ee]mpie_c_e[ns]?_z') + #5
lema(ur'[Ee]nto_n_ces_') + #5
lema(ur'[Ee]spont_á_ne(?:[ao]s|amente)_a') + #5
lema(ur'[Ee]val_ú_(?:a[ns]?|e[ns]?)_u') + #5
lema(ur'[Ff]eligres_í_as?_i') + #5
lema(ur'[Ff]en_ó_menos_o') + #5
lema(ur'[Ff]rigor_í_fic[ao]s?_i') + #5
lema(ur'[Ff]utbol_í_stic(?:[ao]s|amente)_i') + #5
lema(ur'[Gg]ustar_í_a[ns]?_i') + #5
lema(ur'[Hh]ac_é_r[mts]el[aeo]s?_e') + #5
lema(ur'[Hh]acer_s_e(?:lo|)_c') + #5
lema(ur'[Hh]eredit_a_ri[ao]s?_á') + #5
lema(ur'[Ii]mpart(?:ir|)_í_a[ns]?_i') + #5
lema(ur'[Ii]ncre_í_blemente_i') + #5
lema(ur'[Ii]ndic_ó_ que_o') + #5
lema(ur'[Ii]nform_á_ticos?(?!\.com)_a') + #5
lema(ur'[Ii]nstant_á_ne[ao]_a') + #5
lema(ur'[Ii]nte_r_preta[ns]?_') + #5
lema(ur'[Jj]ur_í_dic(?:os|amente)_i') + #5
lema(ur'[Ll]_a_ (?:2a|BBC|Bandera|CIA|Ciudad|Confitería|Copa|Cumbre|Escuela|España|Familia|Fuerza|Isla|MLB|Mancomunidad|Nueva|Parada|Plaza|República|SFP|Sección|Serie|Siderurgia|Sinfónica|Soledad|UEFA|accesibilidad|amplitud|base|bebida|caja|ciudad|compositora|compra|corporación|delincuencia|derecha|derrota|designación|dificultad|discográfica|década|escuela|etiqueta|familia|fecha|formación|fuente|historia|iglesia|imagen|isla|justicia|medicina|más segura|música|normalización|nueva|oposición|organización|otra|pantalla|película|población|poesía|posibilidad|presidenta|primera|producción|promoción|provincia|prueba|psiquiatría|región|reina|revista|secuela|serranía|señorita|situación|sociedad|séptima|virgen|zona|única)_s') + #5
lema(ur'[Ll]a_s_ células_') + #5
lema(ur'[Ll]a_s_ filas_') + #5
lema(ur'[Ll]a_s_ funciones_') + #5
lema(ur'[Ll]a_s_ localidades_') + #5
lema(ur'[Ll]a_s_ plantas_') + #5
lema(ur'[Ll]a_s_ redes_') + #5
lema(ur'[Ll]a_s_ tropas_') + #5
lema(ur'[Ll]a_s_ unidades_') + #5
lema(ur'[Ll]a_s_ universidades_') + #5
lema(ur'[Mm]_é_dicamente_e') + #5
lema(ur'[Nn]ari_c_es_[zs]') + #5
lema(ur'[Oo]bten(?:dr|)_í_a[ns]?_i') + #5
lema(ur'[Oo]btuv_o__ó') + #5
lema(ur'[Oo]r_á_culos?_a') + #5
lema(ur'[Pp]as_sio_n_i[oó]', pre=ur'of (?:the |)') + #5
lema(ur'[Pp]ermane__ciendo_n') + #5
lema(ur'[Pp]ermitir_á_[ns]?_a') + #5
lema(ur'[Pp]ermitir_í_a[ns]?_i') + #5
lema(ur'[Pp]ersoner_í_as?_i') + #5
lema(ur'[Pp]re_s_enci(?:a[ns]?|[oó]|ar(?:[eé]|[aá][ns]?|ron))_s?c') + #5
lema(ur'[Pp]roduc(?:ir|)_í_a[ns]?_i') + #5
lema(ur'[Pp]rote_g_(?:e[nr]?|emos|erl[aeo]s?|erse|erá[ns]?|ería[ns]?|id[aeo]s?|iendo|iera|ieron|iese|ió)_j') + #5
lema(ur'[Pp]rove_í_d[ao]s?_i') + #5
lema(ur'[Pp]sicol_ó_gic[ao]s_o') + #5
lema(ur'[Qq]ued_ó_ (?:sólo|sin|descubierto)_o') + #5
lema(ur'[Rr]ecibir_á_[ns]?_a') + #5
lema(ur'[Rr]econstru_i_d[ao]s?_í') + #5
lema(ur'[Rr]ecorr_í_a[ns]?_i') + #5
lema(ur'[Rr]efiner_í_as?_i') + #5
lema(ur'[Rr]etribu_i_d[ao]s?_í') + #5
lema(ur'[Ss]i_e_mpre_') + #5
lema(ur'[Ss]ie_m_pre_n') + #5
lema(ur'[Ss]obre_vi_vientes?_') + #5
lema(ur'[Ss]uicid__ó_i') + #5
lema(ur'[Uu]n_í_r[mts]el[aeo]s?_i') + #5
lema(ur'[Uu]nir_á_[ns]?_a(?!\])') + #5
lema(ur'[Uu]t_i_lizad[ao]s?_') + #5
lema(ur'[Vv]er_sió_n_ci[oó]') + #5
lema(ur'[m]_í_nimas?_i', pre=ur'(?:[Ll]as?|[Uu]nas?) ') + #5
lema(ur'_e inglé_s_[ey] ingle', pre=ur'(?:quechua|franc[eé]s|español|coreano|japon[eé]s) ') + #5
lema(ur'_ú_nic(?:[ao]s|amente)_u', xpre=[ur'pedes dúo ', ]) + #5
lema(ur'_á_ngulos?_a', pre=ur'(?:[Ee][nl]|[Uu]n|[Ll]os|[Uu]nos) ') + #5
lema(ur'_é_xodos?_e') + #5
lema(ur'_í_ntimamente_i') + #5
lema(ur'D_í_as_i', pre=ur'(?:[uúUÚ]ltimos|Mil|Nueve|Nuestros|Trece|Buenos) ') + #4
lema(ur'Paraguan_á__a') + #4
lema(ur'Teher_á_n_a', pre=ur'(?:[Dd]e|[Ee]n) ') + #4
lema(ur'[Aa]_ _cargo_') + #4
lema(ur'[Aa]cad_é_mic(?:as|amente)_e') + #4
lema(ur'[Aa]dole_sc_entes?_[sc]') + #4
lema(ur'[Aa]greg_á_r[mts]el[aeo]s?_a') + #4
lema(ur'[Aa]l_í_an?_i', pre=ur'[Ss]e ') + #4
lema(ur'[Aa]parecer_á_[ns]?_a') + #4
lema(ur'[Aa]rquer_í_as?_i') + #4
lema(ur'[Aa]sis__tieron_i') + #4
lema(ur'[Aa]sum(?:ir|)_í_a[ns]?_i') + #4
lema(ur'[Cc]_á_lid(?:[ao]s|amente)_a') + #4
lema(ur'[Cc]_ó_mod(?:[ao]s|amente)_o') + #4
lema(ur'[Cc]antar_í_a[ns]?_i') + #4
lema(ur'[Cc]ar_ó_tid[ao]s?_o') + #4
lema(ur'[Cc]at_á_logos_a') + #4
lema(ur'[Cc]ombat(?:ir|)_í_a[ns]?_i') + #4
lema(ur'[Cc]ompet_í_(?:a[ns]?|)_i') + #4
lema(ur'[Cc]ompon_í_a[ns]?_i') + #4
lema(ur'[Cc]u_m_plen_n') + #4
lema(ur'[Dd]__espués_espués d') + #4
lema(ur'[Dd]e__l_ la e') + #4
lema(ur'[Dd]e_cisio_nes_(?:cisió|cici[oó]|si[sc]i[oó])') + #4
lema(ur'[Dd]estru_i_r(?:l[aeo]s?|se|)_í') + #4
lema(ur'[Dd]eval_ú_(?:a[ns]?|e[ns]?)_u') + #4
lema(ur'[Dd]evolv_é_r[mts]el[aeo]s?_e') + #4
lema(ur'[Dd]i_ó_xidos?_o') + #4
lema(ur'[Dd]ise_ñ_a(?:d[ao]s?|dor(?:a|es|)|r)_n') + #4
lema(ur'[Dd]isputar_í_a[ns]?_i') + #4
lema(ur'[Ee]_m_pero_n') + #4
lema(ur'[Ee]_s_trech(?:[ao]s?|amente)_x') + #4
lema(ur'[Ee]l_e_gir(?:se|)_i') + #4
lema(ur'[Ee]ntend_í_(?:a[ns]?|)_i') + #4
lema(ur'[Ee]nv_í_o_i', pre=ur'(?:[Dd]el?|[Ee]l|[Uu]n|[Cc]ada) ') + #4
lema(ur'[Ee]scrib(?:ir|)_í_a[ns]?_i') + #4
lema(ur'[Ee]spr_í_nters?_i') + #4
lema(ur'[Ee]st_é_tic(?:[ao]s|amente)_e') + #4
lema(ur'[Ee]x_á_menes_a') + #4
lema(ur'[Ee]xt__endió_i') + #4
lema(ur'[Ff]il_á_ntropos?_a') + #4
lema(ur'[Ff]luct_ú_(?:a[ns]?|e[ns]?)_u') + #4
lema(ur'[Gg]uarder_í_as?_i') + #4
lema(ur'[Hh]ig_ié_nic[ao]s?_(?:ie|[eé])') + #4
lema(ur'[Ii]deol_ó_gic(?:[ao]s|amente)_o') + #4
lema(ur'[Ii]mpon_í_a[ns]?_i') + #4
lema(ur'[Ii]nal_á_mbric[ao]s?_a') + #4
lema(ur'[Ii]ncon_s_ciencias?_') + #4
lema(ur'[Ii]nflu_i_dos?_í') + #4
lema(ur'[Ii]ngen_i_erías?_') + #4
lema(ur'[Ii]nmo_v_iliz(?:[oó]|a(?:r?|r(?:l[aeo]s?|nos?)|d[ao]s?|ndo|ción|dor))_b') + #4
lema(ur'[Ii]nte_r_pretación_') + #4
lema(ur'[Jj]oyer_í_as?_i') + #4
lema(ur'[Ll]a_s_ ciencias_') + #4
lema(ur'[Ll]a_s_ diferencias_') + #4
lema(ur'[Ll]a_s_ ruinas_') + #4
lema(ur'[Ll]a_s_ tierras_') + #4
lema(ur'[Ll]legar_í_a[ns]?_i') + #4
lema(ur'[Ll]levar_í_a[ns]?_i') + #4
lema(ur'[Mm]_é_dicos_e', pre=ur'(?:[Ll]os|[Ss]us|[Uu]nos) ') + #4
lema(ur'[Mm]anten_í_a[ns]?_i') + #4
lema(ur'[Mm]antendr_í_a[ns]?_i') + #4
lema(ur'[Mm]atem_á_tic(?:os|amente)(?!\.unmsm)_a') + #4
lema(ur'[Mm]ejorar_í_a[ns]?_i') + #4
lema(ur'[Mm]ensajer_í_as?_i') + #4
lema(ur'[Mm]ie_m_bros?_n') + #4
lema(ur'[Mm]ism_í_sim[ao]s?_i') + #4
lema(ur'[Mm]oment_á_ne(?:[ao]s|amente)_a') + #4
lema(ur'[Nn]_áu_frag[ao]s?_aú') + #4
lema(ur'[Nn]anotecnolog_í_as?_i') + #4
lema(ur'[Nn]europsicolog_í_as?_i') + #4
lema(ur'[Oo]currir_á_[ns]?_a') + #4
lema(ur'[Oo]rtop_é_dic[ao]s?_e') + #4
lema(ur'[Pp]__ero_ero p') + #4
lema(ur'[Pp]_é_sim[ao]s?_e') + #4
lema(ur'[Pp]adec_í_a[ns]?_i') + #4
lema(ur'[Pp]aisaj_í_stic(?:[ao]s?|amente)_i') + #4
lema(ur'[Pp]e_s_ca[rs]?_z') + #4
lema(ur'[Pp]opulari_zó__(?:s[oó]|zo)') + #4
lema(ur'[Pp]resentar_í_a[ns]?_i') + #4
lema(ur'[Pp]romov_í_a[ns]?_i') + #4
lema(ur'[Pp]ropon_í_a[ns]?_i') + #4
lema(ur'[Qq]uir_ú_rgic[ao]s?_u') + #4
lema(ur'[Qq]uit_á_r[mts]el[aeo]s?_a') + #4
lema(ur'[Rr]epet_í_a[ns]?_i') + #4
lema(ur'[Ss]upon_í_a[ns]?_i') + #4
lema(ur'[Tt]_é_rmic(?:as|os?)_e') + #4
lema(ur'[Tt]_ó_picos?_o') + #4
lema(ur'[Tt]ardar_í_a[ns]?_i') + #4
lema(ur'[Tt]ect_ó_nic(?:as|os?|amente)_o') + #4
lema(ur'[Tt]err_e_motos?_o') + #4
lema(ur'[Tt]ie_m_pos_n') + #4
lema(ur'[Vv]_inculó__(?:íncul[oó]|inculo)', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #4
lema(ur'[Vv]einti_ú_n_u') + #4
lema(ur'[Vv]eintid_ó_s_o') + #4
lema(ur'[l]e_í_dos_i') + #4
lema(ur'[p]ondr_á_s?_a') + #4
lema(ur'_E_ll[ao]s?_É') + #4
lema(ur'_El__La el') + #4
lema(ur'_é_nfasis_e') + #4
lema(ur'(?:[Aa]erot|[Cc]rono|[Hh]eli|[Tt]elet|[Tt])ran_s_port(?:a(?:[ns]?|ba[ns]?|bles?|ción|d[ao]s?|dor(?:es|)|ndo|r(?:se|ía[ns]?|))|e[ns]?|istas?)_') + #3
lema(ur'R_ó_terdam_o', pre=ur'(?:[Dd]e|[Ee]n) ') + #3
lema(ur'[Aa]cced_í_a[ns]?_i') + #3
lema(ur'[Aa]coger_á_[ns]?_a') + #3
lema(ur'[Aa]daptar_í_a[ns]?_i') + #3
lema(ur'[Aa]dmi_ni_stración_') + #3
lema(ur'[Aa]er__opuertos?_e') + #3
lema(ur'[Aa]l_ _menos_') + #3
lema(ur'[Aa]ldeh_í_d[ao]s?_i') + #3
lema(ur'[Aa]ngiograf_í_as?_i') + #3
lema(ur'[Aa]rras_ó_ (?:en|con)_o') + #3
lema(ur'[Aa]s_c_enso(?:[rs]|res)_') + #3
lema(ur'[Aa]scend_í_(?:a[ns]?)_i') + #3
lema(ur'[Aa]sist(?:ir|)_í_a[ns]?_i') + #3
lema(ur'[Aa]utob_u_ses_ú') + #3
lema(ur'[Bb]_á_ltic[ao]s_a') + #3
lema(ur'[Cc]a_í_a[ns]_i') + #3
lema(ur'[Cc]ardiopat_í_as?_i') + #3
lema(ur'[Cc]ie_m_piés_n') + #3
lema(ur'[Cc]o_m_prar_n') + #3
lema(ur'[Cc]o_o_rdenad[ao]s?_') + #3
lema(ur'[Cc]omenzar_í_a[ns]?_i') + #3
lema(ur'[Cc]ompa_rtió__r?tio', pre=ur'(?:[Qq]ui[ée]n|[Qq]u[ée]|[Dd][óo]nde|[Cc]u[áa]ndo|[Tt]ambién|[Aa]demás|[Ss]e|[Ll][ao]s?|e) ') + #3
lema(ur'[Cc]ompet_í_a[ns]?_i') + #3
lema(ur'[Cc]ono_c_id[ao]s?_s') + #3
lema(ur'[Cc]ons_i_guieron_e') + #3
lema(ur'[Cc]onseguir_í_a[ns]?_i') + #3
lema(ur'[Cc]onstruir_á_[ns]?_a') + #3
lema(ur'[Cc]onte_m_poránea_n') + #3
lema(ur'[Cc]onvertir_á_[ns]?_a') + #3
lema(ur'[Cc]umplir_á_[ns]?_a') + #3
lema(ur'[Dd]e_s_c(?:enso|iende[ns]?|end(?:er?|ido)|entrali(?:ce[ns]?|zar|zó|zació))_') + #3
lema(ur'[Dd]ecid_í__i') + #3
lema(ur'[Dd]ecimos_é_ptim[ao]s?_e') + #3
lema(ur'[Dd]ejar_í_a[ns]?_i') + #3
lema(ur'[Dd]escub_r_ir(?:se|)_') + #3
lema(ur'[Dd]escubr_í__i') + #3
lema(ur'[Dd]iab_ó_lic(?:as|os)_o') + #3
lema(ur'[Dd]ilu_i_d[ao]s?_í') + #3
lema(ur'[Dd]iscurr(?:ir|)_í_a[ns]?_i') + #3
lema(ur'[Dd]isf_r_uta[nrs]?_') + #3
lema(ur'[Dd]r_á_stic(?:[ao]s|amente)_a') + #3
lema(ur'[Ee]jerc_í_a[ns]?_i') + #3
lema(ur'[Ee]l_e_girá[ns]?_i') + #3
lema(ur'[Ee]migrar_í_a[ns]?_i') + #3
lema(ur'[Ee]n_é_rgic(?:[ao]s|amente)_e') + #3
lema(ur'[Ee]nfrentar_í_a[ns]?_i') + #3
lema(ur'[Ee]pis_ó_dic[ao]s?_o') + #3
lema(ur'[Ee]scrib_í_a(?:[ns]?|mos)_i') + #3
lema(ur'[Ee]scult_ó_ric[ao]s?_o') + #3
lema(ur'[Ee]st_é_tica_e', pre=ur'(?:[Ll]a|[Uu]na|[Cc]on|[Dd]e|[Ee]n|[Mm]uy|[Ff]unción[Ff]orma|[Uu]nidad|y) ') + #3
lema(ur'[Ee]studiar_í_a[ns]?_i') + #3
lema(ur'[Ee]x_c_ept(?:o|uar)_') + #3
lema(ur'[Ee]x_h_aust[ao]s?_') + #3
lema(ur'[Ee]xigir_á_[ns]?_a') + #3
lema(ur'[Ee]xten_sio_nes_ci[oó]') + #3
lema(ur'[Ff]idel_í_sim[ao]s?_i') + #3
lema(ur'[Ff]ormar_í_a[ns]?_i') + #3
lema(ur'[Gg]erontolog_í_as?_i') + #3
lema(ur'[Gg]rad_ú_(?:a[ns]|e[ns]?)_u') + #3
lema(ur'[Hh]eterog_é_ne[ao]s?_e') + #3
lema(ur'[Hh]ologr_á_fic[ao]s?_a') + #3
lema(ur'[Hh]undir_á_[ns]?_a') + #3
lema(ur'[Ii]_n_mortal(?:es|idad)_m') + #3
lema(ur'[Ii]mpl_í_cit(?:[ao]s|amente)_i') + #3
lema(ur'[Ii]n_j_erencias?_g') + #3
lema(ur'[Ii]nclu_i_r(?:l[aeo]s?|se|)_í') + #3
lema(ur'[Ii]ncluir_á_[ns]?_a') + #3
lema(ur'[Ii]nstant_á_ne(?:[ao]s|amente)_a') + #3
lema(ur'[Ii]nt_er_pretad[ao]s?_re') + #3
lema(ur'[Ii]nterpretar_í_a[ns]?_i') + #3
lema(ur'[Ii]nvad(?:ir|)_í_a[ns]?_i') + #3
lema(ur'[Ii]r_ó_nic(?:[ao]s|amente)_o') + #3
lema(ur'[Ll]_í_quenes_i') + #3
lema(ur'[Ll]a_s_ bandas_') + #3
lema(ur'[Ll]a_s_ décadas_') + #3
lema(ur'[Ll]a_s_ estructuras_') + #3
lema(ur'[Ll]a_s_ formas_') + #3
lema(ur'[Ll]a_s_ orillas_') + #3
lema(ur'[Ll]a_s_ posibilidades_') + #3
lema(ur'[Ll]anzar_í_a[ns]?_i') + #3
lema(ur'[Ll]encer_í_as?_i') + #3
lema(ur'[M]_ó_naco_o', pre=ur'[Ee]n ') + #3
lema(ur'[Mm]orir_á_[ns]?_a') + #3
lema(ur'[Mm]u__rieron_e') + #3
lema(ur'[Nn]ecrolog_í_as?_i') + #3
lema(ur'[Nn]euroanatom_í_as?_i') + #3
lema(ur'[Nn]i_ _siquiera_') + #3
lema(ur'[Nn]icarag_ü_enses_u') + #3
lema(ur'[Nn]itr_ó_genos?_o') + #3
lema(ur'[Oo]bstru_i_d[ao]s?_í') + #3
lema(ur'[Oo]btendr_á_[ns]?_a') + #3
lema(ur'[Oo]cupar_í_a[ns]?_i') + #3
lema(ur'[Pp]araca_í_das?_i') + #3
lema(ur'[Pp]arad_ó_jic(?:[ao]s|amente)_o') + #3
lema(ur'[Pp]esquer_í_as?_i') + #3
lema(ur'[Pp]od_í_amos_i') + #3
lema(ur'[Pp]rim_e_ras?_a', pre=ur'(?:[Ll]as?|[Ss]us|[Uu]nas?|[Ee]n|[Dd]e|[Pp]or) ') + #3
lema(ur'[Pp]rincipalme_n_te_') + #3
lema(ur'[Pp]roducir_í_a[ns]?_i') + #3
lema(ur'[Pp]rol_í_fic(?:as|os?)_i') + #3
lema(ur'[Qq]u_ie_n_ei') + #3
lema(ur'[Rr]_í_e[ns]?_i', pre=ur'(?:[Ss]e) ') + #3
lema(ur'[Rr]eci_b_id[ao]s?_v') + #3
lema(ur'[Rr]econoc_í_a[ns]?_i') + #3
lema(ur'[Rr]econstitu_i_d[ao]s?_í') + #3
lema(ur'[Rr]espond_í_(?:a[ns]?|)_i') + #3
lema(ur'[Rr]esultar_í_a[ns]?_i') + #3
lema(ur'[Rr]ob_á_r[mts]el[aeo]s?_a') + #3
lema(ur'[Ss]_á_dic(?:[ao]s?|amente)_a') + #3
lema(ur'[Ss]aldr_í_a[ns]?_i') + #3
lema(ur'[Ss]ervir_á_[ns]?_a') + #3
lema(ur'[Ss]ignificar_í_a[ns]?_i') + #3
lema(ur'[Ss]imb_ó_lic(?:[ao]s|amente)_o') + #3
lema(ur'[Ss]imbi_ó_tic[ao]s?_o') + #3
lema(ur'[Ss]uced_í_a[ns]?_i') + #3
lema(ur'[Ss]ufr(?:ir|)_í_a[ns]?_i') + #3
lema(ur'[Ss]ufr_í_a[ns]?_i') + #3
lema(ur'[Ss]uperh_é_roes?_e', pre=ur'(?:[Uu]n|[Ee]l|[Ll]os| de| y) ') + #3
lema(ur'[Ss]ustitu_i_r(?:l[aeo]s?|se|)_í') + #3
lema(ur'[Ss]ustra_í_(?:a[ns]|d[ao]s?)_i') + #3
lema(ur'[Ss]ustra_í_d[ao]s?_i') + #3
lema(ur'[Tt]_ó_rax_o') + #3
lema(ur'[Tt]e_m_porada_n') + #3
lema(ur'[Tt]elevi_si_ón_') + #3
lema(ur'[Tt]ent_á_culos?_a') + #3
lema(ur'[Tt]omar_í_a[ns]?_i') + #3
lema(ur'[Tt]rabajar_í_a[ns]?_i') + #3
lema(ur'[Tt]ran_s_porte_') + #3
lema(ur'[Tt]raumatolog_í_as?_i') + #3
lema(ur'[Tt]ropical_í_sim[ao]s?_i') + #3
lema(ur'[Uu]nir_í_a[ns]?_i') + #3
lema(ur'[Uu]t_i_li(?:z(?:[ae]n?|[oó])|cen?)_') + #3
lema(ur'[Uu]tilizar_í_a[ns]?_i') + #3
lema(ur'[Vv]ender_á_[ns]?_a') + #3
lema(ur'[a]_ _sus_') + #3
lema(ur'[d]ivid_id_a_', pre=ur'(?:[Dd]ecisión|[Ss]er|[Ee]star|[Ee]staba|[Ee]st[aá]|estuvo|se encontraba|se encuentra|queda|quedó|quedará|es|fue|llanura|continuó|distancia|Austria|Actualmente|opinión) ') + #3
lema(ur'[p]erd_í_a_i') + #3
lema(ur'_e_quipos?_é') + #3
lema(ur'_z_ona_s', pre=ur'(?:[Ll]a|[Uu]na|[Dd]e) ') + #3
lema(ur'_Ó_rbitas?_O', pre=ur'(?:[Ll]as?|[Ss]us?|[Uu]nas?|[Ee]n) ') + #3
lema(ur'_é_l (?:ante|cabe|con|desde|entre|según|sin|tras)\b_e', pre=ur'[Cc]on ') + #3
lema(ur'[Aa]brir_á_[ns]?_a') + #2
lema(ur'[Aa]co_g_(?:id[ao]s?|iera[ns]|erá?)_j') + #2
lema(ur'[Aa]cud(?:ir|)_í_a[ns]?_i') + #2
lema(ur'[Aa]cuñar_í_a[ns]?_i') + #2
lema(ur'[Aa]eron_á_uticas_a') + #2
lema(ur'[Aa]frontar_í_a[ns]?_i') + #2
lema(ur'[Aa]gradecim_i_entos?_') + #2
lema(ur'[Aa]lcan_c_e[ns]?_z') + #2
lema(ur'[Aa]lica_í_d[ao]s?_i') + #2
lema(ur'[Aa]notar_í_a[ns]?_i') + #2
lema(ur'[Aa]ntagon_i_stas?_í') + #2
lema(ur'[Aa]nti_i_nflamatori[ao]s?_') + #2
lema(ur'[Aa]parecer_í_a[ns]?_i') + #2
lema(ur'[Aa]s_c_ensor(?:es|)_') + #2
lema(ur'[Aa]ten_ú_(?:a[ns]?|e[ns]?)_u') + #2
lema(ur'[Aa]tl_é_tic(?:[ao]s|amente)_e') + #2
lema(ur'[Aa]trev_í_a[ns]?_i') + #2
lema(ur'[Aa]umentar_í_a[ns]?_i') + #2
lema(ur'[Aa]vanzar_í_a[ns]?_i') + #2
lema(ur'[Aa]ñad(?:ir|)_í_a[ns]?_i') + #2
lema(ur'[Bb]ol_í_grafos?_i') + #2
lema(ur'[Bb]oleter_í_as?_i') + #2
lema(ur'[Bb]uen_í_sim[ao]s?_i') + #2
lema(ur'[Bb]urocr_á_tic[ao]s?_a') + #2
lema(ur'[Cc]__ada_ada c') + #2
lema(ur'[Cc]_iu_dadan[ao]s?_ui') + #2
lema(ur'[Cc]_á_todos?_a') + #2
lema(ur'[Cc]alor_í_as?_i') + #2
lema(ur'[Cc]ar_í_sim[ao]s?_i') + #2
lema(ur'[Cc]ent_í_metros?_i') + #2
lema(ur'[Cc]lasificar_í_a[ns]?_i') + #2
lema(ur'[Cc]lav_á_r[mts]el[aeo]s?_a') + #2
lema(ur'[Cc]o_m_paras_n') + #2
lema(ur'[Cc]obrar_í_a[ns]?_i') + #2
lema(ur'[Cc]oexist(?:ir|)_í_a[ns]?_i') + #2
lema(ur'[Cc]ompart(?:ir|)_í_a[ns]?_i') + #2
lema(ur'[Cc]ompart_í_a(?:[ns]?|mos)_i') + #2
lema(ur'[Cc]omprend_í_a[ns]?_i') + #2
lema(ur'[Cc]onfund(?:ir|)_í_a[ns]?_i') + #2
lema(ur'[Cc]onocer_á_[ns]?_a') + #2
lema(ur'[Cc]onocer_í_a(?:[ns]?|mos)_i') + #2
lema(ur'[Cc]onocid_í_sim[ao]s?_i') + #2
lema(ur'[Cc]onsagrar_í_a[ns]?_i') + #2
lema(ur'[Cc]onseguir_á_[ns]?_a') + #2
lema(ur'[Cc]onsens_ú_(?:a[ns]?|e[ns]?)_u') + #2
lema(ur'[Cc]onstar_í_a[ns]?_i') + #2
lema(ur'[Cc]onsumir_á_[ns]?_a') + #2
lema(ur'[Cc]ontrar_r_estar(?:l[aeo]s?|ía[ns]?|)_') + #2
lema(ur'[Cc]onv_irtié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ertie') + #2
lema(ur'[Cc]onvi_rtié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ertie') + #2
lema(ur'[Cc]re_é_r[mts]el[aeo]s?_e') + #2
lema(ur'[Cc]re_í__i') + #2
lema(ur'[Cc]u_m_pla_n') + #2
lema(ur'[Cc]u_m_plir_n') + #2
lema(ur'[Cc]ulminar_í_a[ns]?_i') + #2
lema(ur'[Dd]_e_cidió_i') + #2
lema(ur'[Dd]_e_cimoséptim[ao]_é') + #2
lema(ur'[Dd]ec_í_r[mts]el[aeo]s?_i') + #2
lema(ur'[Dd]efender_á_[ns]?_a') + #2
lema(ur'[Dd]efin(?:ir|)_í_a[ns]?_i') + #2
lema(ur'[Dd]emostrar_í_a[ns]?_i') + #2
lema(ur'[Dd]epend_í_a[ns]?_i') + #2
lema(ur'[Dd]esaparec_í_a[ns]?_i') + #2
lema(ur'[Dd]esarrollar_í_a[ns]?_i') + #2
lema(ur'[Dd]esconf_í_a[na]?_i') + #2
lema(ur'[Dd]escub_ri_dor(?:[ae]s?|)_ir') + #2
lema(ur'[Dd]escub_ri_mientos?_ir') + #2
lema(ur'[Dd]escubi_e_rt[ao]s?_') + #2
lema(ur'[Dd]escubrir_á_[ns]?_a') + #2
lema(ur'[Dd]ese_m_peño_n') + #2
lema(ur'[Dd]esempeñar_í_a[ns]?_i') + #2
lema(ur'[Dd]esped_í_a[ns]?_i') + #2
lema(ur'[Dd]iagn_osticó__(?:óstic[oó]|ostico)', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #2
lema(ur'[Dd]ifund(?:ir|)_í_a[ns]?_i') + #2
lema(ur'[Dd]ij__eron_i') + #2
lema(ur'[Dd]ilatar_í_a[ns]?_i') + #2
lema(ur'[Dd]irig_í__i') + #2
lema(ur'[Dd]ividi_d_[ao]_', pre=ur'(?:[Ee]st[aá]|[Ff]u[eé]|[Ee]s) ') + #2
lema(ur'[Dd]on_á_r[mts]el[aeo]s?_a') + #2
lema(ur'[Dd]ram_á_tic(?:[ao]s|amente)_a') + #2
lema(ur'[Dd]ur_í_sim[ao]s?_i') + #2
lema(ur'[Ee]__quipo_quipo e') + #2
lema(ur'[Ee]lectromagn_é_tic[ao]s?_e') + #2
lema(ur'[Ee]liminar_í_a[ns]?_i') + #2
lema(ur'[Ee]mp_i_eza[ns]?_') + #2
lema(ur'[Ee]mp_r_esari(?:os?|al)_') + #2
lema(ur'[Ee]mpatar_í_a[ns]?_i') + #2
lema(ur'[Ee]mpezar_í_a[ns]?_i') + #2
lema(ur'[Ee]mular_í_a[ns]?_i') + #2
lema(ur'[Ee]namorar_í_a[ns]?_i', xpre=[ur'm\'']) + #2
lema(ur'[Ee]ncontrar_í_a(?:[ns]?|mos)_i') + #2
lema(ur'[Ee]ntalp_í_as?_i') + #2
lema(ur'[Ee]ntr_e_vista(?:s?|d[ao]s?)_') + #2
lema(ur'[Ee]ntrenar_í_a[ns]?_i') + #2
lema(ur'[Ee]nv_i_ad[ao]s?_í') + #2
lema(ur'[Ee]pis_o_dios?_i') + #2
lema(ur'[Ee]spor_á_dic(?:[ao]s|amente)_a') + #2
lema(ur'[Ee]st_ú_pid(?:[ao]s?|amente)_u') + #2
lema(ur'[Ee]stablec(?:er|)_í_a[ns]?_i') + #2
lema(ur'[Ee]stablec_í_(?:a[ns]?|)_i') + #2
lema(ur'[Ee]stanter_í_as?_i') + #2
lema(ur'[Ee]ster_e_otipos?_i') + #2
lema(ur'[Ee]strenar_í_a[ns]?_i') + #2
lema(ur'[Ee]x_c_elentes?_') + #2
lema(ur'[Ee]x_clui_d[ao]s?_luí') + #2
lema(ur'[Ee]xhib(?:ir|)_í_a[ns]?_i') + #2
lema(ur'[Ee]xi__tos[ao]s?_s') + #2
lema(ur'[Ee]xpon_í_a[ns]?_i') + #2
lema(ur'[Ee]xtend_í_(?:a[ns]?|)_i') + #2
lema(ur'[Ee]xtin__tos?_c') + #2
lema(ur'[Ee]xtra_ñ_[ao]_n') + #2
lema(ur'[Ff]i_l_m_', pre=ur'(?:[Dd]el|[Ee]l) ') + #2
lema(ur'[Ff]inal_í_sim[ao]s?_i') + #2
lema(ur'[Ff]u_s_i(?:ón|ones|onó|ona[ns]?)_c') + #2
lema(ur'[Ff]uncionar_í_an_i') + #2
lema(ur'[Gg]anar_í_a[ns]?_i') + #2
lema(ur'[Gg]en_é_tic[ao]s_e') + #2
lema(ur'[Gg]enerar_í_a[ns]?_i') + #2
lema(ur'[Gg]rabar_í_a[ns]?_i') + #2
lema(ur'[Hh]aci_éndos_e_endoc') + #2
lema(ur'[Hh]aci_éndos_e_endoc') + #2
lema(ur'[Hh]ermos_í_sim[ao]s?_i') + #2
lema(ur'[Hh]ipot_é_tic[ao]s?_e') + #2
lema(ur'[Hh]onrar_í_a[ns]?_i') + #2
lema(ur'[Hh]or_ó_scopos?_o') + #2
lema(ur'[Ii]_m_portando_n') + #2
lema(ur'[Ii]_m_pulsa_n') + #2
lema(ur'[Ii]mbu_i_d[Ao]s?_í') + #2
lema(ur'[Ii]mped_í_r[mts]el[aeo]s?_i') + #2
lema(ur'[Ii]n_clui_d[ao]s?_luí') + #2
lema(ur'[Ii]n_s_talaci(?:ón|ones)_') + #2
lema(ur'[Ii]n_strui_d[ao]s?_truí') + #2
lema(ur'[Ii]nic_i_ativas?_') + #2
lema(ur'[Ii]nsin_ú_(?:a[ns]?|e[ns]?)_u') + #2
lema(ur'[Ii]nte_r_pretar(?:l[ao]s?|se|[aá]|ía[ns]?|ron|)_') + #2
lema(ur'[Ii]nterp_r_et(?:es?|ad[ao]s?)_') + #2
lema(ur'[Ii]ntr_í_nsec(?:[ao]s|amente)_i') + #2
lema(ur'[Ii]nventar_í_a[ns]?_i') + #2
lema(ur'[Jj]er_á_rquic[ao]s?_a') + #2
lema(ur'[Ll]a_s_ acciones_') + #2
lema(ur'[Ll]a_s_ diferentes_') + #2
lema(ur'[Ll]a_s_ figuras_') + #2
lema(ur'[Ll]a_s_ mejores_') + #2
lema(ur'[Ll]a_s_ montañas_') + #2
lema(ur'[Ll]a_s_ rutas_') + #2
lema(ur'[Ll]a_s_ sierras_') + #2
lema(ur'[Ll]anz_á_r[mts]el[aeo]s?_a') + #2
lema(ur'[Ll]exicolog_í_as?_i') + #2
lema(ur'[Ll]inf_á_tic[ao]s?_a') + #2
lema(ur'[Ll]lamar_í_a(?:[ns]?|mos)_i') + #2
lema(ur'[Ll]ograr_í_a[ns]?_i') + #2
lema(ur'[Mm]ostr_á_r[mts]el[aeo]s?_a') + #2
lema(ur'[Mm]ultiprop_ó_sitos?_o') + #2
lema(ur'[Nn]ecesitar_í_a(?:[ns]?|mos)_i') + #2
lema(ur'[Oo]btendr_í_a(?:[ns]?|mos)_i') + #2
lema(ur'[Oo]fend_í_a[ns]?_i') + #2
lema(ur'[Oo]pon_í_a[ns]?_i') + #2
lema(ur'[Oo]ptometr_í_as?_i') + #2
lema(ur'[Oo]rg_á_nic(?:[ao]s|amente)_a') + #2
lema(ur'[Oo]torrinolaringolog_í_as?_i') + #2
lema(ur'[Pp]_ro_gramas?_or') + #2
lema(ur'[Pp]ar_á_lisis_a') + #2
lema(ur'[Pp]aran_o_ic[ao]s?_ó') + #2
lema(ur'[Pp]artic_i_par(?:on|)_') + #2
lema(ur'[Pp]atol_ó_gic[ao]s?_o') + #2
lema(ur'[Pp]e_r_manece(?:[nr]|ría[ns]?|)_') + #2
lema(ur'[Pp]elear_í_a[ns]?_i') + #2
lema(ur'[Pp]erder_á_[ns]?_a') + #2
lema(ur'[Pp]ermanecer_á_[ns]?_a') + #2
lema(ur'[Pp]ermit_í__i') + #2
lema(ur'[Pp]olin_ó_mic[ao]_o') + #2
lema(ur'[Pp]ortug_ué_s_e') + #2
lema(ur'[Pp]resum(?:ir|)_í_a[ns]?_i') + #2
lema(ur'[Pp]rim_e_r[ao]s?_') + #2
lema(ur'[Pp]rohib_í_a[ns]?_i') + #2
lema(ur'[Pp]romet_í_(?:a[ns]?|)_i') + #2
lema(ur'[Pp]romover_á_[ns]?_a') + #2
lema(ur'[Pp]rotagonizar_í_a[ns]?_i') + #2
lema(ur'[Pp]roteg_í_a[ns]?_i') + #2
lema(ur'[Pp]roveer_á_[ns]?_a') + #2
lema(ur'[Qq]ued_á_r[mts]el[aeo]s?_a') + #2
lema(ur'[Rr]e_s_ponde[ns]?_') + #2
lema(ur'[Rr]e_s_pondió_') + #2
lema(ur'[Rr]eca_í_d[ao]s?_i') + #2
lema(ur'[Rr]eci_b_(?:e|ió|[íI]a|ir[eé])_v') + #2
lema(ur'[Rr]eci_b_iendo_v') + #2
lema(ur'[Rr]ecortar_í_a[ns]?_i') + #2
lema(ur'[Rr]edu_j_eron_ci') + #2
lema(ur'[Rr]egrabar_í_a[ns]?_i') + #2
lema(ur'[Rr]emontar_í_a[ns]?_i') + #2
lema(ur'[Rr]epart(?:ir|)_í_a[ns]?_i') + #2
lema(ur'[Rr]estitu_i_d[ao]s?_í') + #2
lema(ur'[Rr]eunir_á_[ns]?_a') + #2
lema(ur'[Rr]omper_á_[ns]?_a') + #2
lema(ur'[Ss]_ú_per (?:Vedette|Humor|Pesad[ao]s?)_u') + #2
lema(ur'[Ss]inverg_ü_enzas?_u') + #2
lema(ur'[Ss]ismol_ó_gic[ao]s?_o') + #2
lema(ur'[Ss]obrevi_vi_do_') + #2
lema(ur'[Ss]u_stitui_d[ao]s?_tituí') + #2
lema(ur'[Ss]uperar_í_a[ns]?_i') + #2
lema(ur'[Tt]_é_rmino_e', pre=ur'[Pp]rimer ') + #2
lema(ur'[Tt]elev_i_sión_') + #2
lema(ur'[Tt]elev_i_sión_e') + #2
lema(ur'[Tt]om_á_r[mts]el[aeo]s?_a') + #2
lema(ur'[Tt]ran_s_formar(?:se|)_') + #2
lema(ur'[Tt]ransitar_í_a[ns]?_i') + #2
lema(ur'[Tt]ransportar_í_a[ns]?_i') + #2
lema(ur'[Uu]bicar_í_a[ns]?_i') + #2
lema(ur'[Uu]ng_ü_entos?_u') + #2
lema(ur'[Uu]til_í_sim[ao]s?_i') + #2
lema(ur'[Vv]encer_í_a[ns]?_i') + #2
lema(ur'[Vv]estir_á_[ns]?_a') + #2
lema(ur'[Vv]ig_ésimo sé_ptima_esimose') + #2
lema(ur'[a]lbergar_í_a[ns]?_i') + #2
lema(ur'[n]_ó_mina_o', pre=ur'(?:[Ss]u|[Ee]n|[Uu]na|misma|primera|en|de) ') + #2
lema(ur'[v]er_á_n_a') + #2
lema(ur'_C_ercan[ao]s?_S') + #2
lema(ur'_E_sta vez_É') + #2
lema(ur'_S_uecia_s', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ') + #2
lema(ur'__a sus?_h') + #2
lema(ur'[Aa]_ _gusto_', pre=ur'(?:[Ee]st[aá]|estaba|sintió|muy|m[aá]s) ') + #1
lema(ur'[Aa]_ _menudo_') + #1
lema(ur'[Aa]bsorb_í_a[ns]?_i') + #1
lema(ur'[Aa]cceder_á_[ns]?_a') + #1
lema(ur'[Aa]cerc_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Aa]cetaldeh_í_d[ao]s?_i') + #1
lema(ur'[Aa]clar_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Aa]compa_ñ_antes?_n') + #1
lema(ur'[Aa]compañar_í_a[ns]?_i') + #1
lema(ur'[Aa]credit_á_(?:ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)|rsel[aeo]s?)_a') + #1
lema(ur'[Aa]credit_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Aa]dministrar_í_a[ns]?_i') + #1
lema(ur'[Aa]dmit(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Aa]dquirir_á_[ns]?_a') + #1
lema(ur'[Aa]er_ó_bic[ao]s?_o') + #1
lema(ur'[Aa]gradar_í_a[ns]?_i') + #1
lema(ur'[Aa]gradec_é_r[mts]el[aeo]s?_e') + #1
lema(ur'[Aa]gregar_í_a[ns]?_i') + #1
lema(ur'[Aa]grupar_í_a[ns]?_i') + #1
lema(ur'[Aa]jonjol_í__i') + #1
lema(ur'[Aa]leg_ó_ric[ao]s?_o') + #1
lema(ur'[Aa]lgori_t_mos?_') + #1
lema(ur'[Aa]lm_í_bar(?:es|)_i') + #1
lema(ur'[Aa]mbientar_í_a[ns]?_i') + #1
lema(ur'[Aa]n_áli_sis_alí') + #1
lema(ur'[Aa]ntinarc_ó_ticos?_o') + #1
lema(ur'[Aa]p_í_col[ao]s?_i') + #1
lema(ur'[Aa]plic_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Aa]portar_í_a[ns]?_i') + #1
lema(ur'[Aa]rregl_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Aa]sociar_í_a[ns]?_i') + #1
lema(ur'[Aa]t_ribui_d[ao]s?_tribuí') + #1
lema(ur'[Aa]tacar_í_a[ns]?_i') + #1
lema(ur'[Aa]tar_í_an_i') + #1
lema(ur'[Aa]tend_í_(?:a[ns]?|)_i') + #1
lema(ur'[Aa]tribu_i_r(?:l[aeo]s?|se|)_í') + #1
lema(ur'[Aa]tribu_í_r[mts]el[aeo]s?_i') + #1
lema(ur'[Bb]_á_ltico(?! S\.)_a') + #1
lema(ur'[Bb]acteriolog_í_as?_i') + #1
lema(ur'[Bb]ailar_í_a[ns]?_i') + #1
lema(ur'[Bb]al_ompié__ónpie') + #1
lema(ur'[Bb]eneficiar_í_an?_i', pre=ur'[Ss]e ') + #1
lema(ur'[Bb]iof_í_sic[ao]s?_i') + #1
lema(ur'[Bb]iomec_á_nic[ao]s?_a') + #1
lema(ur'[Bb]iotecnol_ó_gic[ao]s?_o') + #1
lema(ur'[Bb]ut_í_ric[ao]s?_i') + #1
lema(ur'[Cc]_á_nceres_a') + #1
lema(ur'[Cc]_áno_nes_anó') + #1
lema(ur'[Cc]_ó_moda_o') + #1
lema(ur'[Cc]a_m_panas?_n') + #1
lema(ur'[Cc]ancer_í_gen[ao]s?_i') + #1
lema(ur'[Cc]aracterí_s_ticas?_') + #1
lema(ur'[Cc]at_alogó__ologo') + #1
lema(ur'[Cc]ed_í_a[ns]?_i') + #1
lema(ur'[Cc]elebrar_í_a[ns]?_i') + #1
lema(ur'[Cc]err_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Cc]errar_í_a[ns]?_i') + #1
lema(ur'[Cc]ircular_í_a[ns]?_i') + #1
lema(ur'[Cc]lorh_í_dric[ao]s?_i') + #1
lema(ur'[Cc]o_m_pañía_n') + #1
lema(ur'[Cc]o_m_pendio_n') + #1
lema(ur'[Cc]o_m_pensada_n') + #1
lema(ur'[Cc]o_m_petencia_n') + #1
lema(ur'[Cc]o_m_plejo_n') + #1
lema(ur'[Cc]o_m_port(arse|amiento)_n') + #1
lema(ur'[Cc]o_m_pre_n') + #1
lema(ur'[Cc]o_m_puertas_n') + #1
lema(ur'[Cc]o_nstrui_d[ao]s?_sntruí') + #1
lema(ur'[Cc]ol_a_boró_o') + #1
lema(ur'[Cc]oloc_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Cc]olocar_í_a[ns]?_i') + #1
lema(ur'[Cc]om__pañeros_n') + #1
lema(ur'[Cc]omp_itió__etio') + #1
lema(ur'[Cc]ompar_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Cc]ompetiti__v[ao]s?_t') + #1
lema(ur'[Cc]ompetitiv_id_ad_') + #1
lema(ur'[Cc]ompletar_í_a[ns]?_i') + #1
lema(ur'[Cc]ompondr_á_[ns]?_a') + #1
lema(ur'[Cc]ompromet_í_a[ns]?_i') + #1
lema(ur'[Cc]on_s_titu(?:ye|y[oó]|ción|ciones|id[ao]s?)_') + #1
lema(ur'[Cc]on_s_truyeron_') + #1
lema(ur'[Cc]on_struyó__truyo') + #1
lema(ur'[Cc]oncretar_í_a[ns]?_i') + #1
lema(ur'[Cc]onectar_í_a[ns]?_i') + #1
lema(ur'[Cc]onfes_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Cc]onfundir_á_[ns]?_a') + #1
lema(ur'[Cc]onsegu_í_a[ns]?_i') + #1
lema(ur'[Cc]onservar_í_a[ns]?_i') + #1
lema(ur'[Cc]onsider_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Cc]onsiderar_í_a[ns]?_i') + #1
lema(ur'[Cc]onsigu_ió__o') + #1
lema(ur'[Cc]onstru_i_r(?! (?:a paz|unha))_í') + #1
lema(ur'[Cc]onsum(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Cc]onte_m_poráneo_n') + #1
lema(ur'[Cc]ontemplar_í_a[ns]?_i') + #1
lema(ur'[Cc]onten_í_a[ns]_i') + #1
lema(ur'[Cc]ontendr_á_[ns]?_a') + #1
lema(ur'[Cc]onvi_rtió__tio') + #1
lema(ur'[Cc]onvirt_ió__o') + #1
lema(ur'[Cc]onviv_í_a[ns]_i') + #1
lema(ur'[Cc]onvivir_á_[ns]?_a') + #1
lema(ur'[Cc]oquetear_í_a[ns]?_i') + #1
lema(ur'[Cc]orr_í_an_i') + #1
lema(ur'[Cc]orrespond(?:er|)_í_an?_i') + #1
lema(ur'[Cc]orrespond_í_a[ns]?_i') + #1
lema(ur'[Cc]ortar_í_a[ns]?_i') + #1
lema(ur'[Cc]ri_a_turas?_') + #1
lema(ur'[Cc]ub_r_ir(?:se|)_') + #1
lema(ur'[Cc]umpl_í__i') + #1
lema(ur'[Cc]urar_í_a[ns]?_i') + #1
lema(ur'[Dd]_ecimo_ctav[ao]_écimoo') + #1
lema(ur'[Dd]_é_bilmente_e') + #1
lema(ur'[Dd]_ú_ctil_u') + #1
lema(ur'[Dd]e__cidió_i') + #1
lema(ur'[Dd]e__l (?:2006|Amparo|Cauca|Club|Commonwealth|Consejo|Ejército|Estado|Norte|Working|archipiélago|año|calentamiento|canal|catálogo|condado|cuento|cuerpo|gobierno|himno|museo|oeste|peón|prestigioso|profesor|punto|siglo|éter)_e') + #1
lema(ur'[Dd]eci__dió_ci') + #1
lema(ur'[Dd]eclar_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Dd]econstru_i_d[ao]s?_í') + #1
lema(ur'[Dd]ema_s_iados?_c') + #1
lema(ur'[Dd]emostr_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Dd]enominar_í_a(?:[ns]?|mos)_i') + #1
lema(ur'[Dd]erivar_í_a[ns]?_i') + #1
lema(ur'[Dd]errotar_í_a[ns]?_i') + #1
lema(ur'[Dd]erru_i_d[ao]s?_í') + #1
lema(ur'[Dd]escubr(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Dd]esignar_í_a[ns]?_i') + #1
lema(ur'[Dd]esinter_é_s_e') + #1
lema(ur'[Dd]eslumbrar_í_a[ns]?_i') + #1
lema(ur'[Dd]esplazar_s_e(?:lo|)_c') + #1
lema(ur'[Dd]esprend_í_a[ns]?_i') + #1
lema(ur'[Dd]esta_ca_d[ao]s?_') + #1
lema(ur'[Dd]estitu_i_r(?:l[aeo]s?|se|)_í') + #1
lema(ur'[Dd]etendr_á_[ns]?_a') + #1
lema(ur'[Dd]eterminar_í_a[ns]?_i') + #1
lema(ur'[Dd]i_stribui_d[ao]s?_tribuí') + #1
lema(ur'[Dd]ic_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_e') + #1
lema(ur'[Dd]ici_en_do_ne') + #1
lema(ur'[Dd]ilu_i_r(?:l[aeo]s?|se|)_í') + #1
lema(ur'[Dd]irigir_á_[ns]?_a') + #1
lema(ur'[Dd]is_cí_pul[ao]s?_i') + #1
lema(ur'[Dd]isolver_á__a') + #1
lema(ur'[Dd]istingu(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Dd]istingu_i_d[ao]s?_í') + #1
lema(ur'[Dd]istribu_i_r(?:l[aeo]s?|se|)_í') + #1
lema(ur'[Dd]iál_o_gos?_') + #1
lema(ur'[Dd]ominar_í_a[ns]_i') + #1
lema(ur'[Dd]ominar_í_an_i') + #1
lema(ur'[Dd]otar_í_a[ns]?_i') + #1
lema(ur'[Dd]udar_í_a[ns]?_i') + #1
lema(ur'[Dd]urar_í_a[ns]?_i') + #1
lema(ur'[Ee]_jem_plo_njen') + #1
lema(ur'[Ee]_m_pezó_n') + #1
lema(ur'[Ee]_m_plear_n') + #1
lema(ur'[Ee]_m_presa_n') + #1
lema(ur'[Ee]jecutar_í_a[ns]?_i') + #1
lema(ur'[Ee]jerci_cio__o', pre=ur'[Ee]l ') + #1
lema(ur'[Ee]lectrohidr_á_ulic[ao]s?_a') + #1
lema(ur'[Ee]legir_á_[ns]?_a') + #1
lema(ur'[Ee]mbest_í_a[ns]?_i') + #1
lema(ur'[Ee]mparejar_í_a[ns]?_i') + #1
lema(ur'[Ee]mpe_z_ar(?:on|)_s') + #1
lema(ur'[Ee]n don_d_e_') + #1
lema(ur'[Ee]ncaminar_í_a[ns]?_i') + #1
lema(ur'[Ee]ncend_í_(?:a[ns]?|)_i') + #1
lema(ur'[Ee]nco_g_(?:e[nr]?|imiento|í)_j') + #1
lema(ur'[Ee]nfrent_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Ee]nfurecer_á_[ns]?_a') + #1
lema(ur'[Ee]nojar_í_a[ns]?_i') + #1
lema(ur'[Ee]ntender_í_a(?:[ns]?|mos)_i') + #1
lema(ur'[Ee]nv_iá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ía') + #1
lema(ur'[Ee]scap_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Ee]scond_í_a[ns]?_i') + #1
lema(ur'[Ee]sculp(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Ee]scup(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Ee]sperar_í_a[ns]?_i') + #1
lema(ur'[Ee]stablecer_á_[ns]?_a') + #1
lema(ur'[Ee]x_entá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_senta') + #1
lema(ur'[Ee]xc_é_ntric(?:[ao]s|amente)_e') + #1
lema(ur'[Ee]xced_í_a[ns]?_i') + #1
lema(ur'[Ee]xcept_ú_(?:a[ns]?|e[ns]?)_u') + #1
lema(ur'[Ee]xhibir_á_[ns]?_a') + #1
lema(ur'[Ee]xim_í_as?_i', pre=ur'(?:[Ll]o|[Qq]ue|[Dd]onde) ') + #1
lema(ur'[Ee]xpel_í_a[ns]?_i') + #1
lema(ur'[Ee]xpondr_á_[ns]?_a') + #1
lema(ur'[Ff]_ó_lic[ao]s?_o') + #1
lema(ur'[Ff]acilitar_í_a[ns]?_i') + #1
lema(ur'[Ff]ichar_í_a[ns]?_i') + #1
lema(ur'[Ff]inalizar_í_a[ns]?_i') + #1
lema(ur'[Ff]irmar_í_a[ns]?_i') + #1
lema(ur'[Ff]isiograf_í_a_i') + #1
lema(ur'[Ff]lorecer_á_[ns]?_a') + #1
lema(ur'[Ff]renar_í_a[ns]?_i') + #1
lema(ur'[Ff]ruter_í_as?_i') + #1
lema(ur'[Ff]und(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Ff]unda__d[ao]s?_da') + #1
lema(ur'[Gg]eod_é_sic[ao]s?_e') + #1
lema(ur'[Gg]olp_eá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_éa') + #1
lema(ur'[Gg]ran_ _partido_') + #1
lema(ur'[Gg]u_i_ad[ao]s?_í') + #1
lema(ur'[Hh]a_ll_(?:adas|ados?|ando|arse|éis)_y') + #1
lema(ur'[Hh]eredar_í_a[ns]?_i') + #1
lema(ur'[Hh]iper_ví_nculos?_(?: v[ií]|vi)') + #1
lema(ur'[Hh]ipod_é_rmic[ao]s?_e') + #1
lema(ur'[Hh]umor_í_stic(?:[ao]s|amente)_i') + #1
lema(ur'[Ii]_m_pertinencia_n') + #1
lema(ur'[Ii]_m_portante_n') + #1
lema(ur'[Ii]_m_prácticos_n') + #1
lema(ur'[Ii]_m_pulsaba_n') + #1
lema(ur'[Ii]_m_pulso_n') + #1
lema(ur'[Ii]_ns_pirado_sn') + #1
lema(ur'[Ii]m_portan_tes?_(?:ortan|porta)') + #1
lema(ur'[Ii]mperar_í_a[ns]?_i') + #1
lema(ur'[Ii]n_c_identes?_s') + #1
lema(ur'[Ii]n_s_titu(?:ye|y[oó]|ción|ciones|id[ao]s?)_') + #1
lema(ur'[Ii]nclu_i_rl[aeo]s?_í') + #1
lema(ur'[Ii]ncorporar_í_a[ns]?_i') + #1
lema(ur'[Ii]ncumpl(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Ii]ncur_s_i(?:onar|ón|ones|on[oó]|ona[ns]?)_c') + #1
lema(ur'[Ii]nde__pendencia_n') + #1
lema(ur'[Ii]ndepend__encias?_i') + #1
lema(ur'[Ii]nequ_í_voc(?:[ao]s|amente)_i') + #1
lema(ur'[Ii]ngresar_í_a[ns]?_i') + #1
lema(ur'[Ii]nhib(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Ii]ntegrar_í_a[ns]?_i') + #1
lema(ur'[Ii]ntentar_í_a[ns]?_i') + #1
lema(ur'[Ii]ntercalar_í_a[ns]?_i') + #1
lema(ur'[Ii]nvalidar_í_a[ns]?_i') + #1
lema(ur'[Ii]nvertir_á_[ns]?_a') + #1
lema(ur'[Ii]nvolucrar_í_a[ns]?_i') + #1
lema(ur'[Jj]untar_í_a[ns]?_i') + #1
lema(ur'[K]atmand_ú__u', pre=ur'(?:[Dd]e|[Ee]n) ') + #1
lema(ur'[Ll]a_s_ sociedades_') + #1
lema(ur'[Ll]a_s_ ventas_') + #1
lema(ur'[Ll]avar_í_a[ns]?_i') + #1
lema(ur'[Ll]e_é_r[mts]el[aeo]s?_e') + #1
lema(ur'[Ll]i_m_piamente_n') + #1
lema(ur'[Ll]iberar_í_a[ns]?_i') + #1
lema(ur'[Ll]lam_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Mm]_éto_dos?_etó') + #1
lema(ur'[Mm]_ú_ltiple (?:accidente|álbumes|asesinato|cambio|campeón|con|de |instrumentos|interpretación|mediante|ocasiones|por|productores|que|significa|variantes|vol[uú]menes|y )_u') + #1
lema(ur'[Mm]a_m_posteros_n') + #1
lema(ur'[Mm]a_mposterí_a_nposteri') + #1
lema(ur'[Mm]aci_z_os?_c') + #1
lema(ur'[Mm]agn_í_fica_i', pre=ur'(?:una (?:banda|vista|forma|defensa natural|escritora)| (?:durante|a) la|de forma|sólida y) ') + #1
lema(ur'[Mm]arisquer_í_as?_i') + #1
lema(ur'[Mm]ecatr_ó_nicas?_o') + #1
lema(ur'[Mm]et_é_r[mts]el[aeo]s?_e') + #1
lema(ur'[Mm]etereol_ó_gic[ao]s?_o') + #1
lema(ur'[Mm]irar_í_a[ns]?_i') + #1
lema(ur'[Mm]ostrar_í_a[ns]?_i') + #1
lema(ur'[Mm]ovilizar_í_a[ns]?_i') + #1
lema(ur'[Nn]efr_ó_tic[ao]s?_o') + #1
lema(ur'[Nn]eur_á_lgic[ao]s?_a') + #1
lema(ur'[Nn]eurofenomenolog_í_as?_i') + #1
lema(ur'[Nn]eutralizar_í_a[ns]?_i') + #1
lema(ur'[Nn]inf_ó_manas?_o') + #1
lema(ur'[Nn]ombrar_í_a[ns]?_i') + #1
lema(ur'[Nn]orirland_é_s_e') + #1
lema(ur'[Nn]um_é_ric(?:[ao]s|amente)_e') + #1
lema(ur'[Oo]_b_t(?:en(?:er|gan?|dr[ií]a[ns]?)|ienen?|uvo)_p') + #1
lema(ur'[Oo]bedecer_á_[ns]?_a') + #1
lema(ur'[Oo]bservar_í_a[ns]?_i') + #1
lema(ur'[Oo]clu_i_d[ao]s?_í') + #1
lema(ur'[Oo]dontopediatr_í_as?_i') + #1
lema(ur'[Oo]frecer_á_[ns]?_a') + #1
lema(ur'[Oo]mit(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Oo]rdenar_í_a[ns]?_i') + #1
lema(ur'[Oo]rgani_zacio_nes_sació') + #1
lema(ur'[Pp]_e_rtenece[nrs]?_a') + #1
lema(ur'[Pp]_á_ginas?_a', pre=ur'(?:[Ll]as?)') + #1
lema(ur'[Pp]_é_rtigas?_e') + #1
lema(ur'[Pp]aleogeograf_í_a_i') + #1
lema(ur'[Pp]articipar_í_a[ns]?_i') + #1
lema(ur'[Pp]artir_á_[ns]_a') + #1
lema(ur'[Pp]asant_í_as?_i') + #1
lema(ur'[Pp]atolog_í_as_i') + #1
lema(ur'[Pp]atrocinar_í_a[ns]?_i') + #1
lema(ur'[Pp]ed_í_r[mts]el[aeo]s?_i') + #1
lema(ur'[Pp]edagog_í_as_i') + #1
lema(ur'[Pp]edir_á_[ns]?_a') + #1
lema(ur'[Pp]equeñ_í_sim[ao]s?_i') + #1
lema(ur'[Pp]ercan_c_es?_s') + #1
lema(ur'[Pp]erci_b_id[ao]s?_v') + #1
lema(ur'[Pp]ermit_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #1
lema(ur'[Pp]ermit_í_r[mts]el[aeo]s?_i') + #1
lema(ur'[Pp]erten_e_cer(?:á[ns]?|ía[ns]?|)_') + #1
lema(ur'[Pp]etrograf_í_as?_i') + #1
lema(ur'[Pp]lanear_í_a[ns]?_i') + #1
lema(ur'[Pp]od_ó_log[ao]s?_o') + #1
lema(ur'[Pp]odolog_í_a(?!\.cl)_i') + #1
lema(ur'[Pp]on_é_r[mts]el[aeo]s?_e') + #1
lema(ur'[Pp]orquer_í_as?_i') + #1
lema(ur'[Pp]osi_c_ionada_s') + #1
lema(ur'[Pp]osi_c_ionamiento_s') + #1
lema(ur'[Pp]osi_c_iones_s') + #1
lema(ur'[Pp]osi_ci_ón_sic') + #1
lema(ur'[Pp]r_a_cticar(?:se|lo|le|on|an|)_á') + #1
lema(ur'[Pp]rescribir_á_[ns]?_a') + #1
lema(ur'[Pp]resupon_í_a[ns]?_i') + #1
lema(ur'[Pp]rivar_í_a[ns]?_i') + #1
lema(ur'[Pp]romocionar_í_a[ns]?_i') + #1
lema(ur'[Pp]ropon_é_r[mts]el[aeo]s?_e') + #1
lema(ur'[Pp]roporcionar_í_a[ns]?_i') + #1
lema(ur'[Qq]uitar_í_a[ns]?_i') + #1
lema(ur'[Rr]_í_gida_i', pre=ur'(?:hacer|una|Máscara|persona|cola|está) ') + #1
lema(ur'[Rr]ar_í_sim[ao]s?_i') + #1
lema(ur'[Rr]e_ú_sa[ns]_u') + #1
lema(ur'[Rr]eanudar_í_a[ns]?_i') + #1
lema(ur'[Rr]eclutar_í_a[ns]?_i') + #1
lema(ur'[Rr]ecog_í_a[ns]?_i') + #1
lema(ur'[Rr]econo_z_ca[ns]?_s') + #1
lema(ur'[Rr]econquistar_í_a[ns]?_i') + #1
lema(ur'[Rr]ecordar_í_a[ns]?_i') + #1
lema(ur'[Rr]ecorrer_á_[ns]?_a') + #1
lema(ur'[Rr]edefin(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Rr]edise_ñ_ad[ao]s?_n') + #1
lema(ur'[Rr]educir_á_[ns]?_a') + #1
lema(ur'[Rr]eemplazar_í_a[ns]?_i') + #1
lema(ur'[Rr]eescrib(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Rr]eferir_s_e(?:lo|)_c') + #1
lema(ur'[Rr]egistrar_í_a[ns]?_i') + #1
lema(ur'[Rr]egres_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Rr]elatar_í_a[ns]?_i') + #1
lema(ur'[Rr]emit(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Rr]eparar_í_a[ns]?_i') + #1
lema(ur'[Rr]eposar_í_a[ns]?_i') + #1
lema(ur'[Rr]equer_í_(?:a[ns]?|)_i') + #1
lema(ur'[Rr]escatar_í_a[ns]?_i') + #1
lema(ur'[Rr]esucitar_í_a[ns]?_i') + #1
lema(ur'[Rr]etomar_í_a[ns]?_i') + #1
lema(ur'[Rr]etransmit(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Rr]evel_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Rr]iqu_í_sim[ao]s?_i') + #1
lema(ur'[Rr]odear_í_a[ns]?_i') + #1
lema(ur'[Rr]ondar_í_a[ns]?_i') + #1
lema(ur'[Ss]_ó_tanos_o') + #1
lema(ur'[Ss]_ú_bit(?:[ao]s|amente)_u') + #1
lema(ur'[Ss]ac_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Ss]alt_á_r[mts]el[aeo]s?_a') + #1
lema(ur'[Ss]alvar_í_a[ns]?_i') + #1
lema(ur'[Ss]emidestru_i_d[ao]s?_í') + #1
lema(ur'[Ss]er_í_amos_i') + #1
lema(ur'[Ss]ervi_c_ios?_s') + #1
lema(ur'[Ss]inverg_ü_enzada_u') + #1
lema(ur'[Ss]iquiatr_í_as?_i') + #1
lema(ur'[Ss]obresal(?:dr|)_í_a[ns]?_i') + #1
lema(ur'[Ss]ocorr_í_a[ns]?_i') + #1
lema(ur'[Ss]ol_í_amos_i') + #1
lema(ur'[Ss]oltar_í_a[ns]?_i') + #1
lema(ur'[Ss]olventar_í_a[ns]?_i') + #1
lema(ur'[Ss]oportar_í_a[ns]?_i') + #1
lema(ur'[Ss]u_é_teres_e') + #1
lema(ur'[Ss]ubir_á_[ns]_a') + #1
lema(ur'[Ss]ubordinar_í_a[ns]?_i') + #1
lema(ur'[Ss]ubstitu_i_r(?:l[aeo]s?|se|)_í') + #1
lema(ur'[Ss]urgir_á_[ns]?_a') + #1
lema(ur'[Ss]ustituir_á_[ns]?_a') + #1
lema(ur'[Tt]__igre_r') + #1
lema(ur'[Tt]a_m_poco_n') + #1
lema(ur'[Tt]e_m_plo_n') + #1
lema(ur'[Tt]e_m_poral_n') + #1
lema(ur'[Tt]e_m_prana_n') + #1
lema(ur'[Tt]em__porada_n') + #1
lema(ur'[Tt]em_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_e') + #1
lema(ur'[Tt]en_í_amos_i') + #1
lema(ur'[Tt]eni_en_do_ne') + #1
lema(ur'[Tt]estar_í_a[ns]?_i') + #1
lema(ur'[Tt]ocar_í_an_i') + #1
lema(ur'[Tt]ra_ns_curr(?:e[ns]?|ió)_sn') + #1
lema(ur'[Tt]ra_ns_portado_sn') + #1
lema(ur'[Tt]ran_s_paren(?:cias?|tes?)_') + #1
lema(ur'[Tt]ran_s_parencia_') + #1
lema(ur'[Tt]ranscurr(?:ir|)_í_a[ns]?_i') + #1
lema(ur'[Tt]ranscurrir_á_[ns]?_a') + #1
lema(ur'[Tt]rasladar_í_a[ns]?_i') + #1
lema(ur'[Tt]reintaid_ó_s_o') + #1
lema(ur'[Tt]ro_m_peta_n') + #1
lema(ur'[Uu]gand_é_s_e') + #1
lema(ur'[Uu]ltras_ó_nic[ao]s?_o') + #1
lema(ur'[Uu]sar_í_a[ns]?_i') + #1
lema(ur'[Vv]_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #1
lema(ur'[Vv]al_ú_(?:a[ns]?|en)_u') + #1
lema(ur'[Vv]aldr_á_[ns]?_a') + #1
lema(ur'[Vv]endr_í_a[ns]?_i') + #1
lema(ur'[Vv]ivir_á_[ns]?_a') + #1
lema(ur'[Vv]olvi_éndos_e_endoc') + #1
lema(ur'[Vv]olvi_éndos_e_endoc') + #1
lema(ur'[a]rd_í_an_i') + #1
lema(ur'[c]ern_í__i') + #1
lema(ur'[c]orr_í_as_i') + #1
lema(ur'_A_quel_Á') + #1
lema(ur'_E_quipos?_É') + #1
lema(ur'_Latinoamé_rica_[Ll](?:ationoame|atínoame|ationoamé|ationame|atioamé|atinooamé|atínoamé)') + #1
lema(ur'_a_quel_á') + #1
lema(ur'_hu_esos?_u') + #1
lema(ur'_marzo__[Mm]arço', pre=ur'acessado em [0-9]+ de ') + #1
lema(ur'_É_nfasis_E') + #1
# lema(ur'[A]_r_gentina_t') + #0
# lema(ur'[A]lbergar_í_a[ns]_i') + #0
# lema(ur'[A]rrastrar_í_a[ns]_i') + #0
# lema(ur'[Aa]__compañará_a') + #0
# lema(ur'[Aa]_djudicá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_judica') + #0
# lema(ur'[Aa]_sis_tirá_isi') + #0
# lema(ur'[Aa]batir_á_[ns]?_a') + #0
# lema(ur'[Aa]bjurar_í_a[ns]?_i') + #0
# lema(ur'[Aa]blandar_í_a[ns]?_i') + #0
# lema(ur'[Aa]bofetear_í_a[ns]?_i') + #0
# lema(ur'[Aa]bonar_í_a[ns]?_i') + #0
# lema(ur'[Aa]bordar_í_a[ns]?_i') + #0
# lema(ur'[Aa]bortar_í_a[ns]?_i') + #0
# lema(ur'[Aa]botonar_í_a[ns]?_i') + #0
# lema(ur'[Aa]brevar_í_a[ns]?_i') + #0
# lema(ur'[Aa]bsolver_á_[ns]?_a') + #0
# lema(ur'[Aa]bultar_í_a[ns]?_i') + #0
# lema(ur'[Aa]bundar_í_a[ns]?_i') + #0
# lema(ur'[Aa]burr_í_a[ns]_i') + #0
# lema(ur'[Aa]burrir_á_[ns]?_a') + #0
# lema(ur'[Aa]busar_í_a[ns]?_i') + #0
# lema(ur'[Aa]c_e_ptará_') + #0
# lema(ur'[Aa]campar_í_a[ns]?_i') + #0
# lema(ur'[Aa]carrear_í_a[ns]?_i') + #0
# lema(ur'[Aa]catar_í_a[ns]?_i') + #0
# lema(ur'[Aa]caudillar_í_a[ns]?_i') + #0
# lema(ur'[Aa]ccidentar_í_a[ns]?_i') + #0
# lema(ur'[Aa]cechar_í_a[ns]?_i') + #0
# lema(ur'[Aa]cept_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]cerc_ándos_e_andoc') + #0
# lema(ur'[Aa]cercándo_s_e_c') + #0
# lema(ur'[Aa]cient_í_fic[ao]_i') + #0
# lema(ur'[Aa]clamar_í_a[ns]?_i') + #0
# lema(ur'[Aa]clarar_í_a[ns]?_i') + #0
# lema(ur'[Aa]climatar_í_a[ns]?_i') + #0
# lema(ur'[Aa]co_m_paña_n') + #0
# lema(ur'[Aa]co_m_pañados_n') + #0
# lema(ur'[Aa]co_m_pañamiento_n') + #0
# lema(ur'[Aa]co_m_pañarse_n') + #0
# lema(ur'[Aa]co_ndicioná_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_diciona') + #0
# lema(ur'[Aa]comodar_í_a[ns]?_i') + #0
# lema(ur'[Aa]compa_ñá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_na') + #0
# lema(ur'[Aa]condicionar_í_a[ns]?_i') + #0
# lema(ur'[Aa]congojar_í_a[ns]?_i') + #0
# lema(ur'[Aa]coplar_í_a[ns]?_i') + #0
# lema(ur'[Aa]corralar_í_a[ns]?_i') + #0
# lema(ur'[Aa]cortar_í_a[ns]?_i') + #0
# lema(ur'[Aa]cosar_í_a[ns]?_i') + #0
# lema(ur'[Aa]costumbrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]cotar_í_a[ns]?_i') + #0
# lema(ur'[Aa]creditar_í_a[ns]?_i') + #0
# lema(ur'[Aa]ctivar_í_a[ns]?_i') + #0
# lema(ur'[Aa]cu_sá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_nsa') + #0
# lema(ur'[Aa]culturar_í_a[ns]?_i') + #0
# lema(ur'[Aa]cumular_í_a[ns]?_i') + #0
# lema(ur'[Aa]cunar_í_a[ns]?_i') + #0
# lema(ur'[Aa]cus_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]cusacion__es_p') + #0
# lema(ur'[Aa]d_hiriéndos_e_eriéndoc') + #0
# lema(ur'[Aa]d_quirió__dquirio') + #0
# lema(ur'[Aa]dapt_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]delant_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]delantar_í_a[ns]?_i') + #0
# lema(ur'[Aa]dentrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]dicion_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]dicionar_í_a[ns]?_i') + #0
# lema(ur'[Aa]diestrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]divinar_í_a[ns]?_i') + #0
# lema(ur'[Aa]djudic_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]djuntar_í_a[ns]?_i') + #0
# lema(ur'[Aa]dmirar_í_a[ns]?_i') + #0
# lema(ur'[Aa]dorar_í_a[ns]?_i') + #0
# lema(ur'[Aa]dornar_í_a[ns]?_i') + #0
# lema(ur'[Aa]dosar_í_a[ns]?_i') + #0
# lema(ur'[Aa]dqui_rió__erio') + #0
# lema(ur'[Aa]dscrib(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Aa]dscribir_á_[ns]?_a') + #0
# lema(ur'[Aa]dsorb_í_a[ns]?_i') + #0
# lema(ur'[Aa]dueñar_í_a[ns]?_i') + #0
# lema(ur'[Aa]dvert_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Aa]erotran_s_portadas_') + #0
# lema(ur'[Aa]ferr_ándos_e_andoc') + #0
# lema(ur'[Aa]ferrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]fianzar_í_a[ns]?_i') + #0
# lema(ur'[Aa]ficionar_í_a[ns]?_i') + #0
# lema(ur'[Aa]fiebrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]filiar_í_a[ns]?_i') + #0
# lema(ur'[Aa]flojar_í_a[ns]?_i') + #0
# lema(ur'[Aa]florar_í_a[ns]?_i') + #0
# lema(ur'[Aa]flu_i_d[ao]s?_í') + #0
# lema(ur'[Aa]flu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Aa]garr_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]garrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]gasajar_í_a[ns]?_i') + #0
# lema(ur'[Aa]gitar_í_a[ns]?_i') + #0
# lema(ur'[Aa]glutinar_í_a[ns]?_i') + #0
# lema(ur'[Aa]grandar_í_a[ns]?_i') + #0
# lema(ur'[Aa]gravar_í_a[ns]?_i') + #0
# lema(ur'[Aa]gredecer_á_[ns]?_a') + #0
# lema(ur'[Aa]guantar_í_a[ns]?_i') + #0
# lema(ur'[Aa]gusanar_í_a[ns]?_i') + #0
# lema(ur'[Aa]hondar_í_a[ns]?_i') + #0
# lema(ur'[Aa]horrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]huesar_í_a[ns]?_i') + #0
# lema(ur'[Aa]huyentar_í_a[ns]?_i') + #0
# lema(ur'[Aa]justar_í_a[ns]?_i') + #0
# lema(ur'[Aa]labar_í_a[ns]?_i') + #0
# lema(ur'[Aa]lardear_í_a[ns]?_i') + #0
# lema(ur'[Aa]larmar_í_a[ns]?_i') + #0
# lema(ur'[Aa]lbe_r_gará_') + #0
# lema(ur'[Aa]lborotar_í_a[ns]?_i') + #0
# lema(ur'[Aa]legrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]lej_ándos_e_andoc') + #0
# lema(ur'[Aa]ligerar_í_a[ns]?_i') + #0
# lema(ur'[Aa]limentar_í_an_i') + #0
# lema(ur'[Aa]linear_í_a[ns]?_i') + #0
# lema(ur'[Aa]listar_í_a[ns]?_i') + #0
# lema(ur'[Aa]llanar_í_a[ns]?_i') + #0
# lema(ur'[Aa]lmacenar_í_a[ns]?_i') + #0
# lema(ur'[Aa]lojar_í_a[ns]?_i') + #0
# lema(ur'[Aa]lquilar_í_a[ns]?_i') + #0
# lema(ur'[Aa]lterar_í_a[ns]?_i') + #0
# lema(ur'[Aa]ltoarag_oné_s_óne') + #0
# lema(ur'[Aa]lud(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Aa]ludir_á_[ns]?_a') + #0
# lema(ur'[Aa]lumbrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]m_arrá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_marra') + #0
# lema(ur'[Aa]maestrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]mamantar_í_a[ns]?_i') + #0
# lema(ur'[Aa]marrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]masar_í_a[ns]?_i') + #0
# lema(ur'[Aa]mañar_í_a[ns]?_i') + #0
# lema(ur'[Aa]mbicionar_í_a[ns]?_i') + #0
# lema(ur'[Aa]medrentar_í_a[ns]?_i') + #0
# lema(ur'[Aa]men_a_zará_') + #0
# lema(ur'[Aa]meritar_í_a[ns]?_i') + #0
# lema(ur'[Aa]modorrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]moldar_í_a[ns]?_i') + #0
# lema(ur'[Aa]monestar_í_a[ns]?_i') + #0
# lema(ur'[Aa]montonar_í_a[ns]?_i') + #0
# lema(ur'[Aa]mortig_ü_e[ns]?_u') + #0
# lema(ur'[Aa]motinar_í_a[ns]?_i') + #0
# lema(ur'[Aa]mparar_í_a[ns]?_i') + #0
# lema(ur'[Aa]mputar_í_a[ns]?_i') + #0
# lema(ur'[Aa]mueblar_í_a[ns]?_i') + #0
# lema(ur'[Aa]nclar_í_a[ns]?_i') + #0
# lema(ur'[Aa]nexionar_í_a[ns]?_i') + #0
# lema(ur'[Aa]nhelar_í_a[ns]?_i') + #0
# lema(ur'[Aa]nidar_í_a[ns]?_i') + #0
# lema(ur'[Aa]nillar_í_a[ns]?_i') + #0
# lema(ur'[Aa]niquilar_í_a[ns]?_i') + #0
# lema(ur'[Aa]nonadar_í_a[ns]?_i') + #0
# lema(ur'[Aa]nteced_í_a[ns]?_i') + #0
# lema(ur'[Aa]ntepen_ú_ltim[ao]s?_u') + #0
# lema(ur'[Aa]ntepon_í_a[ns]?_i') + #0
# lema(ur'[Aa]nticipar_í_a[ns]?_i') + #0
# lema(ur'[Aa]ntimon_o_polios_') + #0
# lema(ur'[Aa]ntojar_í_a[ns]?_i') + #0
# lema(ur'[Aa]nu_nciá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_cia') + #0
# lema(ur'[Aa]nul_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]padrinar_í_a[ns]?_i') + #0
# lema(ur'[Aa]par_e_cerá_') + #0
# lema(ur'[Aa]parear_í_a[ns]?_i') + #0
# lema(ur'[Aa]partar_í_a[ns]?_i') + #0
# lema(ur'[Aa]pasionar_í_a[ns]?_i') + #0
# lema(ur'[Aa]pañ_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]pelar_í_a[ns]?_i') + #0
# lema(ur'[Aa]pellidar_í_a[ns]?_i') + #0
# lema(ur'[Aa]percib(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Aa]percibir_á_[ns]?_a') + #0
# lema(ur'[Aa]piadar_í_a[ns]?_i') + #0
# lema(ur'[Aa]piñar_í_a[ns]?_i') + #0
# lema(ur'[Aa]planar_í_a[ns]?_i') + #0
# lema(ur'[Aa]plastar_í_a[ns]?_i') + #0
# lema(ur'[Aa]plaud(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Aa]plaudir_á_[ns]?_a') + #0
# lema(ur'[Aa]podar_í_a[ns]?_i') + #0
# lema(ur'[Aa]postatar_í_a[ns]?_i') + #0
# lema(ur'[Aa]pr_o_vechará_') + #0
# lema(ur'[Aa]pr_oxima_d(?:[ao]s?|amente)_ó') + #0
# lema(ur'[Aa]prendi_en_do_ne') + #0
# lema(ur'[Aa]presar_í_a[ns]?_i') + #0
# lema(ur'[Aa]prestar_í_a[ns]?_i') + #0
# lema(ur'[Aa]presurar_í_a[ns]?_i') + #0
# lema(ur'[Aa]prisionar_í_a[ns]?_i') + #0
# lema(ur'[Aa]probar_í_a[ns]?_i') + #0
# lema(ur'[Aa]provechar_í_a[ns]?_i') + #0
# lema(ur'[Aa]proximar_í_a[ns]?_i') + #0
# lema(ur'[Aa]puntar_í_a[ns]?_i') + #0
# lema(ur'[Aa]purar_í_a[ns]?_i') + #0
# lema(ur'[Aa]puñalar_í_a[ns]?_i') + #0
# lema(ur'[Aa]r_ruinarí_a[ns]?_uinari') + #0
# lema(ur'[Aa]rar_í_a[ns]_i') + #0
# lema(ur'[Aa]rañar_í_a[ns]?_i') + #0
# lema(ur'[Aa]rbitrar_í_an_i') + #0
# lema(ur'[Aa]rgumentar_í_a[ns]?_i') + #0
# lema(ur'[Aa]rquear_í_a[ns]?_i') + #0
# lema(ur'[Aa]rr_ebatá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ébata') + #0
# lema(ur'[Aa]rrasar_í_a[ns]?_i') + #0
# lema(ur'[Aa]rre__pentido_n') + #0
# lema(ur'[Aa]rre__pentí_n') + #0
# lema(ur'[Aa]rre__pintiéndose_n') + #0
# lema(ur'[Aa]rre_pentí__npenti') + #0
# lema(ur'[Aa]rrear_í_a[ns]?_i') + #0
# lema(ur'[Aa]rrebatar_í_a[ns]?_i') + #0
# lema(ur'[Aa]rreglar_í_a[ns]?_i') + #0
# lema(ur'[Aa]rrellanar_í_a[ns]?_i') + #0
# lema(ur'[Aa]rrendar_í_a[ns]?_i') + #0
# lema(ur'[Aa]rrestar_í_a[ns]?_i') + #0
# lema(ur'[Aa]rribar_í_a[ns]?_i') + #0
# lema(ur'[Aa]rrinconar_í_a[ns]?_i') + #0
# lema(ur'[Aa]rrodillar_í_a[ns]?_i') + #0
# lema(ur'[Aa]rrojar_í_a[ns]?_i') + #0
# lema(ur'[Aa]rrollar_í_a[ns]?_i') + #0
# lema(ur'[Aa]rticular_í_a[ns]_i') + #0
# lema(ur'[Aa]saltar_í_a[ns]?_i') + #0
# lema(ur'[Aa]sc_endió__iendio') + #0
# lema(ur'[Aa]scendi_d_o_', pre=ur'[Ss]iendo ') + #0
# lema(ur'[Aa]sear_í_a[ns]?_i') + #0
# lema(ur'[Aa]segur_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]semejar_í_a[ns]?_i') + #0
# lema(ur'[Aa]sent_ándos_e_andoc') + #0
# lema(ur'[Aa]sesorar_í_a[ns]?_i') + #0
# lema(ur'[Aa]sestar_í_a[ns]?_i') + #0
# lema(ur'[Aa]severar_í_a[ns]?_i') + #0
# lema(ur'[Aa]sign_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]signar_í_a[ns]?_i') + #0
# lema(ur'[Aa]similar_í_a[ns]?_i') + #0
# lema(ur'[Aa]somar_í_a[ns]?_i') + #0
# lema(ur'[Aa]sombrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]spirar_í_a[ns]?_i') + #0
# lema(ur'[Aa]sustar_í_a[ns]?_i') + #0
# lema(ur'[Aa]t_ra_vesado_ar') + #0
# lema(ur'[Aa]taj_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]tajar_í_a[ns]?_i') + #0
# lema(ur'[Aa]tener_s_e_z') + #0
# lema(ur'[Aa]tentar_í_a[ns]?_i') + #0
# lema(ur'[Aa]testar_í_a[ns]?_i') + #0
# lema(ur'[Aa]tinar_í_a[ns]?_i') + #0
# lema(ur'[Aa]tormentar_í_a[ns]?_i') + #0
# lema(ur'[Aa]tragant_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]tragantar_í_a[ns]?_i') + #0
# lema(ur'[Aa]trasar_í_a[ns]?_i') + #0
# lema(ur'[Aa]tribu_yé_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_iye') + #0
# lema(ur'[Aa]trincherar_í_a[ns]?_i') + #0
# lema(ur'[Aa]tropellar_í_a[ns]?_i') + #0
# lema(ur'[Aa]turd(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Aa]turdir_á_[ns]?_a') + #0
# lema(ur'[Aa]udi_cio_nes_sió') + #0
# lema(ur'[Aa]udiol_ó_gic[ao]s?_o') + #0
# lema(ur'[Aa]udipr_ó_tesis_o') + #0
# lema(ur'[Aa]uditar_í_a[ns]?_i') + #0
# lema(ur'[Aa]ugurar_í_a[ns]?_i') + #0
# lema(ur'[Aa]ument_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]usentar_í_a[ns]?_i') + #0
# lema(ur'[Aa]ut_on_ómic[ao]s?_') + #0
# lema(ur'[Aa]utenti_cacio_nes_ficació') + #0
# lema(ur'[Aa]utoconstru_i_d[ao]s?_í') + #0
# lema(ur'[Aa]utodenominar_í_a[ns]?_i') + #0
# lema(ur'[Aa]utoexclu_i_d[ao]s?_í') + #0
# lema(ur'[Aa]utofinanci_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Aa]utonombr_ándos_e_andoc') + #0
# lema(ur'[Aa]utonombrar_í_a[ns]?_i') + #0
# lema(ur'[Aa]utoproclamar_í_a[ns]?_i') + #0
# lema(ur'[Aa]utorreclu_i_d[ao]s?_í') + #0
# lema(ur'[Aa]utorreconstru_i_d[ao]s?_í') + #0
# lema(ur'[Aa]uxiliar_í_an_i') + #0
# lema(ur'[Aa]valar_í_a[ns]?_i') + #0
# lema(ur'[Aa]vent_ándos_e_andoc') + #0
# lema(ur'[Aa]venturar_í_a[ns]?_i') + #0
# lema(ur'[Aa]verg_üenc_e[ns]?_uenz') + #0
# lema(ur'[Aa]visar_í_a[ns]?_i') + #0
# lema(ur'[Aa]vistar_í_a[ns]?_i') + #0
# lema(ur'[Aa]vivar_í_a[ns]?_i') + #0
# lema(ur'[Aa]y_udá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_úda') + #0
# lema(ur'[Aa]zotar_í_a[ns]?_i') + #0
# lema(ur'[Aa]ñ_adié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_idie') + #0
# lema(ur'[Aa]ñad_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[B]ajar_í_an_i') + #0
# lema(ur'[B]arr_í_an_i') + #0
# lema(ur'[B]esar_í_a[ns]_i') + #0
# lema(ur'[Bb]abear_í_a[ns]?_i') + #0
# lema(ur'[Bb]aj_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Bb]albucear_í_a[ns]?_i') + #0
# lema(ur'[Bb]arajar_í_a[ns]?_i') + #0
# lema(ur'[Bb]as_ándos_e_adoc') + #0
# lema(ur'[Bb]as_ándos_e_andoc') + #0
# lema(ur'[Bb]atallar_í_a[ns]?_i') + #0
# lema(ur'[Bb]atear_í_a[ns]?_i') + #0
# lema(ur'[Bb]atir_á_[ns]?_a') + #0
# lema(ur'[Bb]autizar_s_e_z') + #0
# lema(ur'[Bb]añar_í_a[ns]?_i') + #0
# lema(ur'[Bb]eb_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Bb]en_e_plácito_') + #0
# lema(ur'[Bb]i_ó_olog[ao]s?_o') + #0
# lema(ur'[Bb]ien_ _parada_') + #0
# lema(ur'[Bb]lanquear_í_a[ns]?_i') + #0
# lema(ur'[Bb]lasfemar_í_a[ns]?_i') + #0
# lema(ur'[Bb]loqu_eá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_éa') + #0
# lema(ur'[Bb]loque_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Bb]loquear_í_a[ns]?_i') + #0
# lema(ur'[Bb]loqué_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Bb]oicotear_í_a[ns]?_i') + #0
# lema(ur'[Bb]ombardear_í_a[ns]?_i') + #0
# lema(ur'[Bb]ordear_í_a[ns]?_i') + #0
# lema(ur'[Bb]orr_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Bb]orrar_í_a[ns]?_i') + #0
# lema(ur'[Bb]osquejar_í_a[ns]?_i') + #0
# lema(ur'[Bb]rear_í_a[ns]?_i') + #0
# lema(ur'[Bb]rillar_í_a[ns]?_i') + #0
# lema(ur'[Bb]rin_dá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ca') + #0
# lema(ur'[Bb]rind_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Bb]romear_í_a[ns]?_i') + #0
# lema(ur'[Bb]roncear_í_a[ns]?_i') + #0
# lema(ur'[Bb]rotar_í_a[ns]?_i') + #0
# lema(ur'[Bb]ucear_í_a[ns]?_i') + #0
# lema(ur'[C]amer_ú_n_u', pre=ur'(?:[Ee]n) ') + #0
# lema(ur'[Cc]_ausá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_uasa') + #0
# lema(ur'[Cc]_onclui_d[ao]s?_ncluí') + #0
# lema(ur'[Cc]_ontá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ónta') + #0
# lema(ur'[Cc]_um_plida_on') + #0
# lema(ur'[Cc]_um_plir_on') + #0
# lema(ur'[Cc]_umplió__onplio') + #0
# lema(ur'[Cc]a_m_pal_n') + #0
# lema(ur'[Cc]a_m_pamento_n') + #0
# lema(ur'[Cc]a_parazo_nes_rapazó') + #0
# lema(ur'[Cc]a_usá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_úsa') + #0
# lema(ur'[Cc]a_yé_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_lle') + #0
# lema(ur'[Cc]abecear_í_a[ns]?_i') + #0
# lema(ur'[Cc]ablear_í_a[ns]?_i') + #0
# lema(ur'[Cc]alar_í_a[ns]?_i') + #0
# lema(ur'[Cc]alcular_í_a[ns]?_i') + #0
# lema(ur'[Cc]alentar_í_a[ns]?_i') + #0
# lema(ur'[Cc]alif_icarí_a[ns]?_cari') + #0
# lema(ur'[Cc]alificar_í_a[ns]?_i') + #0
# lema(ur'[Cc]all_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]allar_í_a[ns]_i') + #0
# lema(ur'[Cc]am__paña_n') + #0
# lema(ur'[Cc]ambi_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]aminar_í_a[ns]_i') + #0
# lema(ur'[Cc]amuflar_í_a[ns]?_i') + #0
# lema(ur'[Cc]anali_c_e[ns]?_[zs]') + #0
# lema(ur'[Cc]anjear_í_a[ns]?_i') + #0
# lema(ur'[Cc]ansar_í_a[ns]?_i') + #0
# lema(ur'[Cc]apacitar_í_a[ns]?_i') + #0
# lema(ur'[Cc]apar_í_a[ns]?_i') + #0
# lema(ur'[Cc]apitanear_í_a[ns]?_i') + #0
# lema(ur'[Cc]apitular_í_a[ns]_i') + #0
# lema(ur'[Cc]aptar_í_a[ns]?_i') + #0
# lema(ur'[Cc]apturar_í_a[ns]?_i') + #0
# lema(ur'[Cc]aracteriz_ándos_e_andoc') + #0
# lema(ur'[Cc]aracterizar_í_a[ns]?_i') + #0
# lema(ur'[Cc]arcom_í_a[ns]?_i') + #0
# lema(ur'[Cc]arg_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]ari_ñ_os(?:[ao]s?|amente)_n') + #0
# lema(ur'[Cc]asar_í_a[ns]_i') + #0
# lema(ur'[Cc]astrar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ategoriz_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]autivar_í_a[ns]?_i') + #0
# lema(ur'[Cc]avar_í_a[ns]_i') + #0
# lema(ur'[Cc]ebar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ejar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ensar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ensurar_í_a[ns]?_i') + #0
# lema(ur'[Cc]entr_ándos_e_andoc') + #0
# lema(ur'[Cc]epill_ándos_e_andoc') + #0
# lema(ur'[Cc]ercenar_í_a[ns]?_i') + #0
# lema(ur'[Cc]esar_í_an_i') + #0
# lema(ur'[Cc]hatear_í_a[ns]?_i') + #0
# lema(ur'[Cc]hequear_í_a[ns]?_i') + #0
# lema(ur'[Cc]hivar_í_a[ns]?_i') + #0
# lema(ur'[Cc]horrear_í_a[ns]?_i') + #0
# lema(ur'[Cc]hup_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]ibercaf_é__e') + #0
# lema(ur'[Cc]ifrar_í_a[ns]?_i') + #0
# lema(ur'[Cc]imentar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ircu_m_polar_n') + #0
# lema(ur'[Cc]ircunscrib(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Cc]ircunscribir_á_[ns]?_a') + #0
# lema(ur'[Cc]itar_í_a[ns]?_i') + #0
# lema(ur'[Cc]l_ás_ic[ao]s?_[aá]c') + #0
# lema(ur'[Cc]lamar_í_a[ns]?_i') + #0
# lema(ur'[Cc]lausur_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]lausurar_í_a[ns]?_i') + #0
# lema(ur'[Cc]lavar_í_an_i') + #0
# lema(ur'[Cc]linicopatol_ó_gic[ao]s?_o') + #0
# lema(ur'[Cc]o_m_paginan_n') + #0
# lema(ur'[Cc]o_m_para_n') + #0
# lema(ur'[Cc]o_m_parten_n') + #0
# lema(ur'[Cc]o_m_partieron_n') + #0
# lema(ur'[Cc]o_m_partir_n') + #0
# lema(ur'[Cc]o_m_partirlos_n') + #0
# lema(ur'[Cc]o_m_partiría_n') + #0
# lema(ur'[Cc]o_m_partía_n') + #0
# lema(ur'[Cc]o_m_patriota_n') + #0
# lema(ur'[Cc]o_m_pañeros_n') + #0
# lema(ur'[Cc]o_m_petencias_n') + #0
# lema(ur'[Cc]o_m_petitivo_n') + #0
# lema(ur'[Cc]o_m_pinche_n') + #0
# lema(ur'[Cc]o_m_plementado_n') + #0
# lema(ur'[Cc]o_m_plementaria_n') + #0
# lema(ur'[Cc]o_m_pletado_n') + #0
# lema(ur'[Cc]o_m_pletamente_n') + #0
# lema(ur'[Cc]o_m_pletando_n') + #0
# lema(ur'[Cc]o_m_ponía_n') + #0
# lema(ur'[Cc]o_m_portaban_n') + #0
# lema(ur'[Cc]o_m_positora_n') + #0
# lema(ur'[Cc]o_m_positores_n') + #0
# lema(ur'[Cc]o_m_prensible_n') + #0
# lema(ur'[Cc]o_m_pro_n') + #0
# lema(ur'[Cc]o_m_prometer_n') + #0
# lema(ur'[Cc]o_m_prometido_n') + #0
# lema(ur'[Cc]o_m_prometió_n') + #0
# lema(ur'[Cc]o_mpartió__npartio') + #0
# lema(ur'[Cc]o_mpañí_a_npañi') + #0
# lema(ur'[Cc]o_mpens_ación_npenz') + #0
# lema(ur'[Cc]o_mprometió__nprometio') + #0
# lema(ur'[Cc]o_nclui_d[ao]s?_lncluí') + #0
# lema(ur'[Cc]o_ns_pirar_sn') + #0
# lema(ur'[Cc]o_nsecue_ncias_secua') + #0
# lema(ur'[Cc]o_ntemporá_nea_mtenpora') + #0
# lema(ur'[Cc]o_nvirtié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_virtie') + #0
# lema(ur'[Cc]oadyuvar_í_a[ns]?_i') + #0
# lema(ur'[Cc]obijar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ocinar_í_a[ns]?_i') + #0
# lema(ur'[Cc]odescub_ri_dor(?:as?|es|)_ir') + #0
# lema(ur'[Cc]oescrib(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Cc]oescribir_á_[ns]?_a') + #0
# lema(ur'[Cc]oexistir_á_[ns]?_a') + #0
# lema(ur'[Cc]ofundar_í_a[ns]?_i') + #0
# lema(ur'[Cc]og_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Cc]oincidi_en_do_ne') + #0
# lema(ur'[Cc]ol_a_boraciones_o') + #0
# lema(ur'[Cc]ol_a_borado_o') + #0
# lema(ur'[Cc]ol_a_boradores_o') + #0
# lema(ur'[Cc]ol_a_boraron_o') + #0
# lema(ur'[Cc]olapsar_í_a[ns]?_i') + #0
# lema(ur'[Cc]oleccionar_í_a[ns]?_i') + #0
# lema(ur'[Cc]olectar_í_a[ns]?_i') + #0
# lema(ur'[Cc]olisionar_í_a[ns]?_i') + #0
# lema(ur'[Cc]olmar_í_a[ns]?_i') + #0
# lema(ur'[Cc]oloc_ándos_e_andoc') + #0
# lema(ur'[Cc]olorear_í_a[ns]?_i') + #0
# lema(ur'[Cc]olu_mpi_ando_npe') + #0
# lema(ur'[Cc]om__partir_n') + #0
# lema(ur'[Cc]om__pletamente_n') + #0
# lema(ur'[Cc]omandar_í_an_i') + #0
# lema(ur'[Cc]ombinar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ome_nzarí_a[ns]?_zari') + #0
# lema(ur'[Cc]omenz_ándos_e_andoc') + #0
# lema(ur'[Cc]omer_s_e_z') + #0
# lema(ur'[Cc]omi_en_do_ne') + #0
# lema(ur'[Cc]omp__itiendo_et') + #0
# lema(ur'[Cc]ompaginar_í_a[ns]?_i') + #0
# lema(ur'[Cc]omparar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ompel_í_a[ns]?_i') + #0
# lema(ur'[Cc]ompenetrar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ompensar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ompeti__ciones_ti') + #0
# lema(ur'[Cc]ompeti__rán_ti') + #0
# lema(ur'[Cc]ompeti_ci_ón_ic') + #0
# lema(ur'[Cc]ompeti_t_iva_v') + #0
# lema(ur'[Cc]ompeti_ti_v[ao]s?_') + #0
# lema(ur'[Cc]ompetici__ones_c') + #0
# lema(ur'[Cc]ompetici__ón_ci') + #0
# lema(ur'[Cc]ompeticio_n_es_') + #0
# lema(ur'[Cc]ompetit_i_vidad_') + #0
# lema(ur'[Cc]ompetiti__vidad_t') + #0
# lema(ur'[Cc]ompetitiv_i_dad_') + #0
# lema(ur'[Cc]ompil_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]ompilar_í_a[ns]?_i') + #0
# lema(ur'[Cc]omplementar_í_an_i') + #0
# lema(ur'[Cc]omportar_í_a[ns]?_i') + #0
# lema(ur'[Cc]omposi_c_iones_s') + #0
# lema(ur'[Cc]ompr_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]omprar_í_a[ns]?_i') + #0
# lema(ur'[Cc]omprim(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Cc]omprob_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]omprobar_í_a[ns]?_i') + #0
# lema(ur'[Cc]omprometiéndo_s_e_c') + #0
# lema(ur'[Cc]omputar_í_a[ns]?_i') + #0
# lema(ur'[Cc]on_s_piración_') + #0
# lema(ur'[Cc]on_stitui_d[ao]s?_tituí') + #0
# lema(ur'[Cc]once_dié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ndie') + #0
# lema(ur'[Cc]oncentrar_í_a[ns]?_i') + #0
# lema(ur'[Cc]oncept_ú_(?:a[ns]?|e[ns]?)_u') + #0
# lema(ur'[Cc]oncitar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onclu_i_rl[ao]s?_í') + #0
# lema(ur'[Cc]onclu_i_rse_í') + #0
# lema(ur'[Cc]oncursar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ondecorar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ondenar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ondescend_í_(?:a[ns]?|)_i') + #0
# lema(ur'[Cc]ondescender_á_[ns]?_a') + #0
# lema(ur'[Cc]ondicionar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ondiment_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]ondonar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onfeccionar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onfer_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Cc]onfi_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]onfigurac_io_nes_ó') + #0
# lema(ur'[Cc]onfigurar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onfinar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onfirmar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onflu_i_d[ao]s?_í') + #0
# lema(ur'[Cc]onflu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Cc]onfrontar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onfund_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Cc]ongelar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onjeturar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onjurar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onllevar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onmemorar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onminar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onmocionar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onmutar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ono__cer(?:[sl]e|)_s') + #0
# lema(ur'[Cc]onoci_d_o_', pre=ur'[Ee]s ') + #0
# lema(ur'[Cc]onquistar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onsegu_i_d[ao]s?_í') + #0
# lema(ur'[Cc]onsent_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Cc]onsi_g_ue[ns]?_q') + #0
# lema(ur'[Cc]onsignar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onsigu_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_e') + #0
# lema(ur'[Cc]onsigui_en_do_ne') + #0
# lema(ur'[Cc]onsolidar_s_e_z') + #0
# lema(ur'[Cc]onspirar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onstatar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onstipar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onsult_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]onsultar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onsumar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ontaminar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onte_m_poráneamente_n') + #0
# lema(ur'[Cc]onte_mporá_nea_npora') + #0
# lema(ur'[Cc]ontender_á_[ns]?_a') + #0
# lema(ur'[Cc]ontrapon_í_a[ns]?_i') + #0
# lema(ur'[Cc]ontrarrestar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ontrastar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ontratar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ontrolar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onvalidar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onver_g_e[ns]?_j') + #0
# lema(ur'[Cc]onversar_í_a[ns]?_i') + #0
# lema(ur'[Cc]onverti_d_o_', pre=ur'(?:[Ff]ue|[Ee]s|[Ss]er) ') + #0
# lema(ur'[Cc]onvirt_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_e') + #0
# lema(ur'[Cc]onvirti_en_do_ne') + #0
# lema(ur'[Cc]onvirti_éndos_e_endoc') + #0
# lema(ur'[Cc]onvirti_éndos_e_endoc') + #0
# lema(ur'[Cc]onvirti_éndos_e_endoc') + #0
# lema(ur'[Cc]onvirti_éndos_e_endoc') + #0
# lema(ur'[Cc]onvirti_ó__oo') + #0
# lema(ur'[Cc]onvirti_ó__rtio') + #0
# lema(ur'[Cc]onvivir_í_a[ns]?_i') + #0
# lema(ur'[Cc]oordinar_í_a[ns]?_i') + #0
# lema(ur'[Cc]opar_í_an_i') + #0
# lema(ur'[Cc]opi_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]opiar_í_a[ns]?_i') + #0
# lema(ur'[Cc]or_respondié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_espondie') + #0
# lema(ur'[Cc]oron_ándos_e_andoc') + #0
# lema(ur'[Cc]oron_ándos_e_andoc') + #0
# lema(ur'[Cc]oronar_í_an_i') + #0
# lema(ur'[Cc]orreg_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Cc]orretear_í_a[ns]?_i') + #0
# lema(ur'[Cc]orroborar_í_a[ns]?_i') + #0
# lema(ur'[Cc]orromp_í_a[ns]?_i') + #0
# lema(ur'[Cc]ort_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]ortejar_í_a[ns]?_i') + #0
# lema(ur'[Cc]osechar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ostear_í_a[ns]?_i') + #0
# lema(ur'[Cc]otejar_í_a[ns]?_i') + #0
# lema(ur'[Cc]rey_éndos_e_endoc') + #0
# lema(ur'[Cc]ronometrar_í_a[ns]?_i') + #0
# lema(ur'[Cc]u_m_plidas_n') + #0
# lema(ur'[Cc]u_m_pliese_n') + #0
# lema(ur'[Cc]u_m_plimiento_n') + #0
# lema(ur'[Cc]u_m_plirse_n') + #0
# lema(ur'[Cc]u_m_plía_n') + #0
# lema(ur'[Cc]uajar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ub__rir_i') + #0
# lema(ur'[Cc]ub_ri_endo_ir') + #0
# lema(ur'[Cc]ub_ri_era[ns]?_ir') + #0
# lema(ur'[Cc]ub_ri_eron_ir') + #0
# lema(ur'[Cc]ubr_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #0
# lema(ur'[Cc]ubri_en_do_ne') + #0
# lema(ur'[Cc]uchichear_í_a[ns]?_i') + #0
# lema(ur'[Cc]uestionar_í_a[ns]?_i') + #0
# lema(ur'[Cc]uidar_í_a[ns]?_i') + #0
# lema(ur'[Cc]umpl_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Cc]und(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Cc]undir_á_[ns]?_a') + #0
# lema(ur'[Cc]ur_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Cc]urrar_í_a[ns]?_i') + #0
# lema(ur'[Cc]ursar_í_a[ns]?_i') + #0
# lema(ur'[Dd]_ecimosé_ptimo_écimose') + #0
# lema(ur'[Dd]_ejá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_éja') + #0
# lema(ur'[Dd]_icié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ecie') + #0
# lema(ur'[Dd]_uodé_cimo_úode') + #0
# lema(ur'[Dd]_é_cimos_e', pre=ur'(?:[Ll]os|[Uu]nos) ') + #0
# lema(ur'[Dd]atar_í_an_i') + #0
# lema(ur'[Dd]e__pendiendo_n') + #0
# lema(ur'[Dd]e_fendió__nfendio') + #0
# lema(ur'[Dd]e_finió__nifinio') + #0
# lema(ur'[Dd]e_s_cifrarlos_') + #0
# lema(ur'[Dd]e_s_cifraron_') + #0
# lema(ur'[Dd]e_s_cifrarás_') + #0
# lema(ur'[Dd]e_spegá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_pega') + #0
# lema(ur'[Dd]eambular_í_a[ns]?_i') + #0
# lema(ur'[Dd]ebilitar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ebitar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ecantar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ecapitar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ecepcionar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ecidi_d_o_', pre=ur'[Hh]a ') + #0
# lema(ur'[Dd]ecidi_éndos_e_endoc') + #0
# lema(ur'[Dd]eclamar_í_a[ns]?_i') + #0
# lema(ur'[Dd]eclinar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ecolor_ándos_e_andoc') + #0
# lema(ur'[Dd]ecorar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ecretar_í_a[ns]?_i') + #0
# lema(ur'[Dd]edic_ándos_e_andoc') + #0
# lema(ur'[Dd]edicar_í_a[ns]?_i') + #0
# lema(ur'[Dd]efen_dió__cdio') + #0
# lema(ur'[Dd]efend_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_e') + #0
# lema(ur'[Dd]efin_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Dd]eformar_í_a[ns]?_i') + #0
# lema(ur'[Dd]efraudar_í_a[ns]?_i') + #0
# lema(ur'[Dd]egradar_í_a[ns]?_i') + #0
# lema(ur'[Dd]egustar_í_a[ns]?_i') + #0
# lema(ur'[Dd]elatar_í_a[ns]?_i') + #0
# lema(ur'[Dd]eleitar_í_a[ns]?_i') + #0
# lema(ur'[Dd]elimitar_í_an_i') + #0
# lema(ur'[Dd]elinear_í_a[ns]?_i') + #0
# lema(ur'[Dd]emorar_í_a[ns]?_i') + #0
# lema(ur'[Dd]emost_ra_ción_ar') + #0
# lema(ur'[Dd]emost_ra_ndo_ar') + #0
# lema(ur'[Dd]enomin_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Dd]enotar_í_a[ns]?_i') + #0
# lema(ur'[Dd]eparar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ependi_en_do_ne') + #0
# lema(ur'[Dd]epondr_á_[ns]?_a') + #0
# lema(ur'[Dd]eportar_í_a[ns]?_i') + #0
# lema(ur'[Dd]epositar_í_an_i') + #0
# lema(ur'[Dd]erramar_í_a[ns]?_i') + #0
# lema(ur'[Dd]erret_í_a[ns]?_i') + #0
# lema(ur'[Dd]erribar_í_a[ns]?_i') + #0
# lema(ur'[Dd]erru_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Dd]es_cribió__rcibio') + #0
# lema(ur'[Dd]es_cribió__ribio') + #0
# lema(ur'[Dd]esacelerar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esaconsejar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esacoplar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esacreditar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esactivar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esaf_í_o__i', pre=ur'(?:[Uu]n|[Ee]l|[Pp]rimer|[Gg]ran) ') + #0
# lema(ur'[Dd]esagradar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esagrupar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esalojar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esangr_ándos_e_andoc') + #0
# lema(ur'[Dd]esanimar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esapare_c_er?_s') + #0
# lema(ur'[Dd]esapare_c_ería_s') + #0
# lema(ur'[Dd]esapare_cerí_a[ns]?_seri') + #0
# lema(ur'[Dd]esaprovechar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esarmar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esarticular_í_a[ns]?_i') + #0
# lema(ur'[Dd]esasign_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Dd]esatar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esatend_í_(?:a[ns]?|)_i') + #0
# lema(ur'[Dd]esatender_á_[ns]?_a') + #0
# lema(ur'[Dd]esatornillar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esayunar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esbaratar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esbastar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esbloquear_í_a[ns]?_i') + #0
# lema(ur'[Dd]esbordar_í_a[ns]?_i') + #0
# lema(ur'[Dd]escalificar_í_a[ns]?_i') + #0
# lema(ur'[Dd]escansar_í_a[ns]?_i') + #0
# lema(ur'[Dd]escarar_í_a[ns]?_i') + #0
# lema(ur'[Dd]escarg_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Dd]escarrilar_í_a[ns]?_i') + #0
# lema(ur'[Dd]escartar_í_a[ns]?_i') + #0
# lema(ur'[Dd]escentrar_í_a[ns]?_i') + #0
# lema(ur'[Dd]escifrar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esco_m_presión_n') + #0
# lema(ur'[Dd]escojonar_í_a[ns]?_i') + #0
# lema(ur'[Dd]escollar_í_a[ns]?_i') + #0
# lema(ur'[Dd]escompon_í_a[ns]?_i') + #0
# lema(ur'[Dd]esconcept_ú_(?:a[ns]?|e[ns]?)_u') + #0
# lema(ur'[Dd]esconcertar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esconectar_í_a[ns]?_i') + #0
# lema(ur'[Dd]escono_c_id[ao]s?_s') + #0
# lema(ur'[Dd]escono_z_cas_s') + #0
# lema(ur'[Dd]escontrolar_í_a[ns]?_i') + #0
# lema(ur'[Dd]escorr_í_a[ns]?_i') + #0
# lema(ur'[Dd]escos_í_a[ns]?_i') + #0
# lema(ur'[Dd]escribir_á_[ns]?_a') + #0
# lema(ur'[Dd]escub__rimientos=_i') + #0
# lema(ur'[Dd]escub__rirla_i') + #0
# lema(ur'[Dd]escub__riría[ns]?_i') + #0
# lema(ur'[Dd]escub_r_iría[ns]?_') + #0
# lema(ur'[Dd]escub_ri_endo_ir') + #0
# lema(ur'[Dd]escub_ri_ó_ir') + #0
# lema(ur'[Dd]escuidar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esdasar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esdeñar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esdoblar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ese_m_peñar_n') + #0
# lema(ur'[Dd]ese_m_peñándose_n') + #0
# lema(ur'[Dd]ese_mpeñá_ndose_npeña') + #0
# lema(ur'[Dd]esechar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esencadenar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esenredar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esentend_í_(?:a[ns]?|)_i') + #0
# lema(ur'[Dd]esentender_á_[ns]?_a') + #0
# lema(ur'[Dd]esenvainar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esenvolver_á_[ns]?_a') + #0
# lema(ur'[Dd]esertar_í_a[ns]_i') + #0
# lema(ur'[Dd]esestimar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esfilar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esfragmentar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esgajar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esgarrar_í_a[ns]?_i') + #0
# lema(ur'[Dd]eshabit_ú_(?:a[ns]?|e[ns]?)_u') + #0
# lema(ur'[Dd]eshac_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Dd]eshidratar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esilu_sio_nes_ció') + #0
# lema(ur'[Dd]esilusionar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esinflar_s_e_z') + #0
# lema(ur'[Dd]esintegrar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esinteresar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esist(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Dd]esistir_á_[ns]?_a') + #0
# lema(ur'[Dd]eslindar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esmantelar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esmayar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esmed_í_a[ns]?_i') + #0
# lema(ur'[Dd]esmontar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esmoronar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esnudar_í_a[ns]?_i') + #0
# lema(ur'[Dd]espachar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esparasitar_í_an_i') + #0
# lema(ur'[Dd]espeg_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Dd]espejar_í_a[ns]?_i') + #0
# lema(ur'[Dd]espenar_í_a[ns]?_i') + #0
# lema(ur'[Dd]espendolar_í_a[ns]?_i') + #0
# lema(ur'[Dd]espla_z_a(?:[rns]?|rse)_s') + #0
# lema(ur'[Dd]esplaz_ándos_e_andoc') + #0
# lema(ur'[Dd]esplazar_í_a[ns]?_i') + #0
# lema(ur'[Dd]espleg_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Dd]esplegar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esplomar_s_e_z') + #0
# lema(ur'[Dd]esplomar_í_a[ns]?_i') + #0
# lema(ur'[Dd]espojar_í_a[ns]?_i') + #0
# lema(ur'[Dd]espos_eyé_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_éye') + #0
# lema(ur'[Dd]esposar_í_a[ns]?_i') + #0
# lema(ur'[Dd]espose_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Dd]espose_í_a[ns]?_i') + #0
# lema(ur'[Dd]esprend_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Dd]espreocupar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esprove_í_d[ao]s?_i') + #0
# lema(ur'[Dd]espuntar_í_a[ns]?_i') + #0
# lema(ur'[Dd]estacándo_s_e_c') + #0
# lema(ur'[Dd]estacándo_s_e_c') + #0
# lema(ur'[Dd]estej_í_a[ns]?_i') + #0
# lema(ur'[Dd]estituí__os_d') + #0
# lema(ur'[Dd]estronar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esva_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Dd]esva_í_d[ao]s?_i') + #0
# lema(ur'[Dd]esvelar_í_a[ns]?_i') + #0
# lema(ur'[Dd]esvest_í_a[ns]?_i') + #0
# lema(ur'[Dd]esvincular_í_a[ns]?_i') + #0
# lema(ur'[Dd]esvirt_ú_(?:a[ns]?|e[ns]?)_u') + #0
# lema(ur'[Dd]esvituar_í_a[ns]?_i') + #0
# lema(ur'[Dd]etallar_í_a[ns]?_i') + #0
# lema(ur'[Dd]etectar_í_a[ns]?_i') + #0
# lema(ur'[Dd]eteriorar_í_a[ns]?_i') + #0
# lema(ur'[Dd]etonar_í_a[ns]?_i') + #0
# lema(ur'[Dd]evastar_í_a[ns]?_i') + #0
# lema(ur'[Dd]evolv_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #0
# lema(ur'[Dd]i_cié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_sie') + #0
# lema(ur'[Dd]i_sfrazars_e_zfrasarz') + #0
# lema(ur'[Dd]i_spará_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_para') + #0
# lema(ur'[Dd]iagnostic_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Dd]iagramar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ictaminar_í_a[ns]?_i') + #0
# lema(ur'[Dd]iezmar_í_a[ns]?_i') + #0
# lema(ur'[Dd]iferenci_ándos_e_adoc') + #0
# lema(ur'[Dd]iferenciar_í_a[ns]?_i') + #0
# lema(ur'[Dd]iferenciándo_s_e_c') + #0
# lema(ur'[Dd]ificultar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ifundir_á_[ns]?_a') + #0
# lema(ur'[Dd]ignar_í_a[ns]?_i') + #0
# lema(ur'[Dd]imit(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Dd]imitir_á_[ns]?_a') + #0
# lema(ur'[Dd]iplomar_í_a[ns]?_i') + #0
# lema(ur'[Dd]irig__en_u') + #0
# lema(ur'[Dd]irig__entes_u') + #0
# lema(ur'[Dd]irig_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_uie') + #0
# lema(ur'[Dd]irig_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Dd]irigi_éndos_e_endoc') + #0
# lema(ur'[Dd]irim(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Dd]irimir_á_[ns]?_a') + #0
# lema(ur'[Dd]iscont_i_nuamente_í') + #0
# lema(ur'[Dd]iscrepar_í_a[ns]?_i') + #0
# lema(ur'[Dd]iscriminar_í_a[ns]?_i') + #0
# lema(ur'[Dd]iscu_sio_nes_ció') + #0
# lema(ur'[Dd]isculpar_í_a[ns]?_i') + #0
# lema(ur'[Dd]iscurrir_á_[ns]?_a') + #0
# lema(ur'[Dd]iscut_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Dd]iscutir_á_[ns]?_a') + #0
# lema(ur'[Dd]isecar_í_a[ns]?_i') + #0
# lema(ur'[Dd]iseminar_í_a[ns]?_i') + #0
# lema(ur'[Dd]isertar_í_a[ns]?_i') + #0
# lema(ur'[Dd]iseñar_í_a[ns]?_i') + #0
# lema(ur'[Dd]isfrazar_s_e_z') + #0
# lema(ur'[Dd]isgustar_í_a[ns]?_i') + #0
# lema(ur'[Dd]isipar_í_a[ns]?_i') + #0
# lema(ur'[Dd]isp_ará_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ra') + #0
# lema(ur'[Dd]ispar_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Dd]ispensar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ispersar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ispersion_e_s_o', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Aa]) ') + #0
# lema(ur'[Dd]isposi__tivos_si') + #0
# lema(ur'[Dd]istend_í_(?:a[ns]?|)_i') + #0
# lema(ur'[Dd]istender_á_[ns]?_a') + #0
# lema(ur'[Dd]isti_nguió__guio') + #0
# lema(ur'[Dd]isting_uió__io') + #0
# lema(ur'[Dd]istorsionar_í_a[ns]?_i') + #0
# lema(ur'[Dd]isuadir_á_[ns]?_a') + #0
# lema(ur'[Dd]ivisar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ivulgar_í_a[ns]?_i') + #0
# lema(ur'[Dd]oblar_í_a[ns]?_i') + #0
# lema(ur'[Dd]octorar_í_a[ns]?_i') + #0
# lema(ur'[Dd]ocumentar_í_an_i') + #0
# lema(ur'[Dd]renar_í_a[ns]?_i') + #0
# lema(ur'[Dd]urmi_en_do_ne') + #0
# lema(ur'[E]tiop_í_a_y') + #0
# lema(ur'[Ee]_cuacio_nes_quació') + #0
# lema(ur'[Ee]_jem_plo_gen') + #0
# lema(ur'[Ee]_m_paque_n') + #0
# lema(ur'[Ee]_m_paquetaba_n') + #0
# lema(ur'[Ee]_m_paquetado_n') + #0
# lema(ur'[Ee]_m_paquetamiento_n') + #0
# lema(ur'[Ee]_m_parejados_n') + #0
# lema(ur'[Ee]_m_parentada_n') + #0
# lema(ur'[Ee]_m_parentados_n') + #0
# lema(ur'[Ee]_m_peoraba_n') + #0
# lema(ur'[Ee]_m_pequeñecida_n') + #0
# lema(ur'[Ee]_m_peradores_n') + #0
# lema(ur'[Ee]_m_piezan_n') + #0
# lema(ur'[Ee]_m_pinada_n') + #0
# lema(ur'[Ee]_m_pinado_n') + #0
# lema(ur'[Ee]_m_plaza_n') + #0
# lema(ur'[Ee]_m_plazado_n') + #0
# lema(ur'[Ee]_m_plearon_n') + #0
# lema(ur'[Ee]_m_polvado_n') + #0
# lema(ur'[Ee]_m_prende_n') + #0
# lema(ur'[Ee]_m_prender_n') + #0
# lema(ur'[Ee]_m_puñadura_n') + #0
# lema(ur'[Ee]_mpez_ando_npes') + #0
# lema(ur'[Ee]_mpez_aron_npes') + #0
# lema(ur'[Ee]_mprenderí_a_nprenderi') + #0
# lema(ur'[Ee]_nmendó__mmendo') + #0
# lema(ur'[Ee]_structurá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_tructura') + #0
# lema(ur'[Ee]ch_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ee]clipsar_í_a[ns]?_i') + #0
# lema(ur'[Ee]closionar_í_a[ns]?_i') + #0
# lema(ur'[Ee]fectu_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ee]flu_i_d[Ao]s?_í') + #0
# lema(ur'[Ee]flu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Ee]gresar_í_a[ns]?_i') + #0
# lema(ur'[Ee]je_m_plares_n') + #0
# lema(ur'[Ee]jec_utá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_tua') + #0
# lema(ur'[Ee]jem__plo_n') + #0
# lema(ur'[Ee]jercitar_í_a[ns]?_i') + #0
# lema(ur'[Ee]laborar_í_a[ns]?_i') + #0
# lema(ur'[Ee]leg_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Ee]legi_d_o_', pre=ur'(?:[Ff]u[eé]|[Ee]s|[Ss]er) ') + #0
# lema(ur'[Ee]levar_í_a[ns]?_i') + #0
# lema(ur'[Ee]lucidar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ludir_á_[ns]?_a') + #0
# lema(ur'[Ee]m__presa_n') + #0
# lema(ur'[Ee]manar_í_a[ns]?_i') + #0
# lema(ur'[Ee]mancipar_í_a[ns]?_i') + #0
# lema(ur'[Ee]mbalsamar_í_a[ns]?_i') + #0
# lema(ur'[Ee]mbeb_í_a[ns]?_i') + #0
# lema(ur'[Ee]mbelesar_í_a[ns]?_i') + #0
# lema(ur'[Ee]mbolsar_í_a[ns]?_i') + #0
# lema(ur'[Ee]mborrachar_í_a[ns]?_i') + #0
# lema(ur'[Ee]mocionar_í_a[ns]?_i') + #0
# lema(ur'[Ee]mpanar_í_a[ns]?_i') + #0
# lema(ur'[Ee]mpapar_í_a[ns]?_i') + #0
# lema(ur'[Ee]mpecinar_í_a[ns]?_i') + #0
# lema(ur'[Ee]mpeorar_í_a[ns]?_i') + #0
# lema(ur'[Ee]mpeñar_í_a[ns]?_i') + #0
# lema(ur'[Ee]mplear_í_a[ns]?_i') + #0
# lema(ur'[Ee]mpujar_í_a[ns]?_i') + #0
# lema(ur'[Ee]mpuñar_í_a[ns]?_i') + #0
# lema(ur'[Ee]n_ _parte_') + #0
# lema(ur'[Ee]n_c_apsulado_p') + #0
# lema(ur'[Ee]n_señá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_zeña') + #0
# lema(ur'[Ee]n_tregá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ trega') + #0
# lema(ur'[Ee]najenar_í_a[ns]?_i') + #0
# lema(ur'[Ee]narbolar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ncabezar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ncadenar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ncajar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ncallar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ncanar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ncarar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ncarcelar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ncariñar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ncarnar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ncasquill_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ee]ncerrar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nciclop_é_dic(?:[ao]s|amente)_e') + #0
# lema(ur'[Ee]nco_ntrándos_e_trándoc') + #0
# lema(ur'[Ee]ncom_endá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_énda') + #0
# lema(ur'[Ee]ncontr_a_ron_á') + #0
# lema(ur'[Ee]ncontr_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ee]ncontr_ándos_e_andoc') + #0
# lema(ur'[Ee]ncontr_ándos_e_andoc') + #0
# lema(ur'[Ee]ncorvar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ncuadrar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ncubi_e_rt[ao]s?_') + #0
# lema(ur'[Ee]ncubrir_á_[ns]?_a') + #0
# lema(ur'[Ee]ncumbrar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ndeudar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ndosar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nemistar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nfadar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nfilar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nfocar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nfrent_ándos_e_andoc') + #0
# lema(ur'[Ee]nfrent_ándos_e_andoc') + #0
# lema(ur'[Ee]nganch_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ee]nganchar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ngañar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ngendrar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nglobar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ngripar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nlazar_s_e_z') + #0
# lema(ur'[Ee]nlazar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nloquecer_á_[ns]?_a') + #0
# lema(ur'[Ee]nredar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nriquecer_á_[ns]?_a') + #0
# lema(ur'[Ee]nrolar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nsamblar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nsanchar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nsayar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nseñar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nsimismar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ntablar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nti_en_do_ne') + #0
# lema(ur'[Ee]ntonar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ntr_egá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ga') + #0
# lema(ur'[Ee]ntrañar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ntremet_í_a[ns]?_i') + #0
# lema(ur'[Ee]ntretej_í_a[ns]?_i') + #0
# lema(ur'[Ee]ntrevistar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ntromet_í_a[ns]?_i') + #0
# lema(ur'[Ee]ntusiasmar_í_a[ns]?_i') + #0
# lema(ur'[Ee]numerar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nv_í_o (?:contra)_i') + #0
# lema(ur'[Ee]nvenenar_í_a[ns]?_i') + #0
# lema(ur'[Ee]nviudar_í_a[ns]?_i') + #0
# lema(ur'[Ee]quilibrar_í_a[ns]?_i') + #0
# lema(ur'[Ee]quipar_í_a[ns]?_i') + #0
# lema(ur'[Ee]quiparar_í_a[ns]?_i') + #0
# lema(ur'[Ee]rgu_i_d[ao]s?_í') + #0
# lema(ur'[Ee]rosionar_í_a[ns]?_i') + #0
# lema(ur'[Ee]ru__pciones_n') + #0
# lema(ur'[Ee]ructar_í_a[ns]?_i') + #0
# lema(ur'[Ee]scabull_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Ee]scampar_í_a[ns]?_i') + #0
# lema(ur'[Ee]scanear_í_a[ns]?_i') + #0
# lema(ur'[Ee]scapar_í_a[ns]?_i') + #0
# lema(ur'[Ee]scaquear_í_a[ns]?_i') + #0
# lema(ur'[Ee]scatimar_í_a[ns]?_i') + #0
# lema(ur'[Ee]scind(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Ee]scindir_á_[ns]?_a') + #0
# lema(ur'[Ee]sco_gerí_a_jeri') + #0
# lema(ur'[Ee]sco_gió__jio') + #0
# lema(ur'[Ee]scog_í_a[ns]?_i') + #0
# lema(ur'[Ee]scoltar_í_a[ns]?_i') + #0
# lema(ur'[Ee]scrib_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Ee]scuchar_í_a[ns]?_i') + #0
# lema(ur'[Ee]scudriñar_í_a[ns]?_i') + #0
# lema(ur'[Ee]sculpir_á_[ns]?_a') + #0
# lema(ur'[Ee]scupir_á_[ns]?_a') + #0
# lema(ur'[Ee]sfumar_í_a[ns]?_i') + #0
# lema(ur'[Ee]sgrim(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Ee]sgrimi_en_do_ne') + #0
# lema(ur'[Ee]sgrimir_á_[ns]?_a') + #0
# lema(ur'[Ee]smerar_í_a[ns]?_i') + #0
# lema(ur'[Ee]spantar_í_a[ns]?_i') + #0
# lema(ur'[Ee]sperar_s_e_z') + #0
# lema(ur'[Ee]spetar_í_a[ns]?_i') + #0
# lema(ur'[Ee]splend_í_a[ns]?_i') + #0
# lema(ur'[Ee]spolear_í_a[ns]?_i') + #0
# lema(ur'[Ee]sputar_í_a[ns]?_i') + #0
# lema(ur'[Ee]squivar_í_a[ns]?_i') + #0
# lema(ur'[Ee]stable_cié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ncie') + #0
# lema(ur'[Ee]stableci_éndos_e_endoc') + #0
# lema(ur'[Ee]stableci_éndos_e_endoc') + #0
# lema(ur'[Ee]stableci_éndos_e_endoc') + #0
# lema(ur'[Ee]stableci_éndos_e_endoc') + #0
# lema(ur'[Ee]stacionar_í_an_i') + #0
# lema(ur'[Ee]stafar_í_a[ns]?_i') + #0
# lema(ur'[Ee]stallar_í_a[ns]?_i') + #0
# lema(ur'[Ee]statu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Ee]stereotipar_í_a[ns]?_i') + #0
# lema(ur'[Ee]stimar_í_a[ns]?_i') + #0
# lema(ur'[Ee]stimular_í_a[ns]?_i') + #0
# lema(ur'[Ee]stipular_í_a[ns]?_i') + #0
# lema(ur'[Ee]stirar_í_a[ns]?_i') + #0
# lema(ur'[Ee]stoquear_í_a[ns]?_i') + #0
# lema(ur'[Ee]storbar_í_a[ns]?_i') + #0
# lema(ur'[Ee]strangular_í_a[ns]?_i') + #0
# lema(ur'[Ee]strechar_í_a[ns]?_i') + #0
# lema(ur'[Ee]strellar_í_a[ns]?_i') + #0
# lema(ur'[Ee]stresar_í_a[ns]?_i') + #0
# lema(ur'[Ee]stropear_í_a[ns]?_i') + #0
# lema(ur'[Ee]structurar_í_a[ns]?_i') + #0
# lema(ur'[Ee]strujar_í_a[ns]?_i') + #0
# lema(ur'[Ee]sturdi_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ee]tiquetar_í_a[ns]?_i') + #0
# lema(ur'[Ee]vad(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Ee]vadir_á_[ns]?_a') + #0
# lema(ur'[Ee]vaporar_í_a[ns]?_i') + #0
# lema(ur'[Ee]volucionar_í_an_i') + #0
# lema(ur'[Ee]x_hortacio_nes_ortació') + #0
# lema(ur'[Ee]xacerbar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xagerar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xaltar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xaminar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xcavar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xcitar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xclamar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xcusar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xhortar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xhumar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xig_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #0
# lema(ur'[Ee]xigi_en_do_ne') + #0
# lema(ur'[Ee]xim_í_an_i') + #0
# lema(ur'[Ee]ximir_á_[ns]?_a') + #0
# lema(ur'[Ee]ximir_í_a[ns]?_i') + #0
# lema(ur'[Ee]xisti_en_do_ne') + #0
# lema(ur'[Ee]xonerar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xpa_nsio_nes_sió') + #0
# lema(ur'[Ee]xpandir_á_[ns]?_a') + #0
# lema(ur'[Ee]xped_í_a[ns]_i') + #0
# lema(ur'[Ee]xpend_í_a[ns]?_i') + #0
# lema(ur'[Ee]xperimentar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xpirar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xplic_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ee]xplicar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xplotar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xportar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xposi_c_ión_s') + #0
# lema(ur'[Ee]xpres_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ee]xpresar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xpulsar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xten_ú_(?:a[ns]?|e[ns]?)_u') + #0
# lema(ur'[Ee]xterminar_í_a[ns]?_i') + #0
# lema(ur'[Ee]xtingu_i_d[ao]s?_í') + #0
# lema(ur'[Ee]xtra_yé_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_je') + #0
# lema(ur'[Ee]xtrajuri_s_diccionales_') + #0
# lema(ur'[Ee]xtrañar_í_a[ns]?_i') + #0
# lema(ur'[Ee]yectar_í_a[ns]?_i') + #0
# lema(ur'[Ff]acilit_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ff]acturar_í_a[ns]?_i') + #0
# lema(ur'[Ff]acultar_í_a[ns]?_i') + #0
# lema(ur'[Ff]ajar_í_a[ns]?_i') + #0
# lema(ur'[Ff]altar_í_a[ns]?_i') + #0
# lema(ur'[Ff]antasear_í_a[ns]?_i') + #0
# lema(ur'[Ff]ascinar_í_a[ns]?_i') + #0
# lema(ur'[Ff]echar_í_a[ns]?_i') + #0
# lema(ur'[Ff]elicitar_í_a[ns]?_i') + #0
# lema(ur'[Ff]estej_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ff]estejar_í_a[ns]?_i') + #0
# lema(ur'[Ff]estonear_í_a[ns]?_i') + #0
# lema(ur'[Ff]igurar_í_a[ns]?_i') + #0
# lema(ur'[Ff]ilmar_s_e_z') + #0
# lema(ur'[Ff]ilosofar_í_a[ns]?_i') + #0
# lema(ur'[Ff]iltr_ándos_e_andoc') + #0
# lema(ur'[Ff]iltrar_í_a[ns]?_i') + #0
# lema(ur'[Ff]lamear_í_a[ns]?_i') + #0
# lema(ur'[Ff]letar_í_a[ns]?_i') + #0
# lema(ur'[Ff]lotar_í_a[ns]?_i') + #0
# lema(ur'[Ff]oll_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ff]omentar_í_a[ns]_i') + #0
# lema(ur'[Ff]ondear_í_a[ns]?_i') + #0
# lema(ur'[Ff]orcejear_í_a[ns]?_i') + #0
# lema(ur'[Ff]orjar_s_e_z') + #0
# lema(ur'[Ff]orjar_í_a[ns]?_i') + #0
# lema(ur'[Ff]orm_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ff]orm_ándos_e_andoc') + #0
# lema(ur'[Ff]ormatear_í_a[ns]?_i') + #0
# lema(ur'[Ff]ormul_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ff]ormular_í_an_i') + #0
# lema(ur'[Ff]orrar_í_a[ns]?_i') + #0
# lema(ur'[Ff]ort_aleciéndos_e_eleciendoc') + #0
# lema(ur'[Ff]ortific_ándos_e_andoc') + #0
# lema(ur'[Ff]ortificar_í_a[ns]?_i') + #0
# lema(ur'[Ff]orz_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ff]racasar_í_a[ns]?_i') + #0
# lema(ur'[Ff]raccionar_í_an_i') + #0
# lema(ur'[Ff]racturar_í_a[ns]?_i') + #0
# lema(ur'[Ff]ragmentar_í_an_i') + #0
# lema(ur'[Ff]recuentar_í_a[ns]?_i') + #0
# lema(ur'[Ff]risar_í_a[ns]?_i') + #0
# lema(ur'[Ff]rustrar_í_a[ns]?_i') + #0
# lema(ur'[Ff]ulminar_í_a[ns]?_i') + #0
# lema(ur'[Ff]undamentar_í_a[ns]?_i') + #0
# lema(ur'[Ff]undir_á_[ns]?_a') + #0
# lema(ur'[Ff]usilar_í_a[ns]?_i') + #0
# lema(ur'[Ff]usion_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Gg]_á_nster_a', pre=ur'(?:[Ee]l|[Uu]n)') + #0
# lema(ur'[Gg]alardonar_í_a[ns]?_i') + #0
# lema(ur'[Gg]angrenar_í_a[ns]?_i') + #0
# lema(ur'[Gg]ast_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Gg]astar_í_a[ns]?_i') + #0
# lema(ur'[Gg]enerac_io_nes_ció') + #0
# lema(ur'[Gg]erminar_í_a[ns]?_i') + #0
# lema(ur'[Gg]eront_ó_log[ao]s?_o') + #0
# lema(ur'[Gg]estar_í_an_i') + #0
# lema(ur'[Gg]irar_í_a[ns]?_i') + #0
# lema(ur'[Gg]loriar_í_a[ns]?_i') + #0
# lema(ur'[Gg]losar_í_a[ns]?_i') + #0
# lema(ur'[Gg]lotolog_í_as?_i') + #0
# lema(ur'[Gg]olp_eá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_a') + #0
# lema(ur'[Gg]olpear_í_a[ns]?_i') + #0
# lema(ur'[Gg]raduar_í_a[ns]?_i') + #0
# lema(ur'[Gg]ran_ _popularidad_') + #0
# lema(ur'[Gg]ranjear_í_a[ns]?_i') + #0
# lema(ur'[Gg]ritar_í_a[ns]?_i') + #0
# lema(ur'[Gg]uard_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Gg]uardar_í_a[ns]?_i') + #0
# lema(ur'[Gg]uerrear_í_a[ns]?_i') + #0
# lema(ur'[Gg]uillar_í_a[ns]?_i') + #0
# lema(ur'[Gg]uisar_í_a[ns]?_i') + #0
# lema(ur'[Gg]uiñar_í_a[ns]?_i') + #0
# lema(ur'[Hh]a_lla_rse_yá') + #0
# lema(ur'[Hh]ab_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Hh]abi_en_do_ne') + #0
# lema(ur'[Hh]abi_éndos_e_endoc') + #0
# lema(ur'[Hh]abilitar_í_a[ns]?_i') + #0
# lema(ur'[Hh]abitar_í_a[ns]_i') + #0
# lema(ur'[Hh]aciéndo_s_e_c') + #0
# lema(ur'[Hh]ala_gá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_nga') + #0
# lema(ur'[Hh]artar_í_a[ns]?_i') + #0
# lema(ur'[Hh]ench_í_a[ns]?_i') + #0
# lema(ur'[Hh]ere_dá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_nda') + #0
# lema(ur'[Hh]ered_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Hh]ermanar_í_a[ns]?_i') + #0
# lema(ur'[Hh]ibernar_í_a[ns]?_i') + #0
# lema(ur'[Hh]inc_há_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ña') + #0
# lema(ur'[Hh]ipar_í_a[ns]?_i') + #0
# lema(ur'[Hh]ir_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #0
# lema(ur'[Hh]omenajear_í_a[ns]?_i') + #0
# lema(ur'[Hh]ospedar_í_an_i') + #0
# lema(ur'[Hh]uevear_í_a[ns]?_i') + #0
# lema(ur'[Hh]umillar_í_a[ns]?_i') + #0
# lema(ur'[Hh]usmear_í_a[ns]?_i') + #0
# lema(ur'[Ii]_gnorá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ngora') + #0
# lema(ur'[Ii]_m_pactaron_n') + #0
# lema(ur'[Ii]_m_pedir_n') + #0
# lema(ur'[Ii]_m_pensable_n') + #0
# lema(ur'[Ii]_m_pensables_n') + #0
# lema(ur'[Ii]_m_pensado_n') + #0
# lema(ur'[Ii]_m_perdibles_n') + #0
# lema(ur'[Ii]_m_perdonable_n') + #0
# lema(ur'[Ii]_m_perfecciones_n') + #0
# lema(ur'[Ii]_m_perfecta_n') + #0
# lema(ur'[Ii]_m_plantándole_n') + #0
# lema(ur'[Ii]_m_plantó_n') + #0
# lema(ur'[Ii]_m_plementado_n') + #0
# lema(ur'[Ii]_m_plicación_n') + #0
# lema(ur'[Ii]_m_plicado_n') + #0
# lema(ur'[Ii]_m_ponen_n') + #0
# lema(ur'[Ii]_m_ponerse_n') + #0
# lema(ur'[Ii]_m_portantemente_n') + #0
# lema(ur'[Ii]_m_portar_n') + #0
# lema(ur'[Ii]_m_posición_n') + #0
# lema(ur'[Ii]_m_precisa_n') + #0
# lema(ur'[Ii]_m_predecible_n') + #0
# lema(ur'[Ii]_m_predecibles_n') + #0
# lema(ur'[Ii]_m_pregna_n') + #0
# lema(ur'[Ii]_m_presa_n') + #0
# lema(ur'[Ii]_m_prescindibles_n') + #0
# lema(ur'[Ii]_m_presionado_n') + #0
# lema(ur'[Ii]_m_productivas_n') + #0
# lema(ur'[Ii]_m_provisada_n') + #0
# lema(ur'[Ii]_m_provisado_n') + #0
# lema(ur'[Ii]_m_provisadores_n') + #0
# lema(ur'[Ii]_m_proviso_n') + #0
# lema(ur'[Ii]_m_prudencias_n') + #0
# lema(ur'[Ii]_m_prudente_n') + #0
# lema(ur'[Ii]_m_puesta_n') + #0
# lema(ur'[Ii]_m_puestas_n') + #0
# lema(ur'[Ii]_m_puestos_n') + #0
# lema(ur'[Ii]_m_pugnadas_n') + #0
# lema(ur'[Ii]_m_pugnado_n') + #0
# lema(ur'[Ii]_m_pugnó_n') + #0
# lema(ur'[Ii]_m_pulsado_n') + #0
# lema(ur'[Ii]_m_punemente_n') + #0
# lema(ur'[Ii]_m_punidad_n') + #0
# lema(ur'[Ii]_m_puntual_n') + #0
# lema(ur'[Ii]_m_puso_n') + #0
# lema(ur'[Ii]_mpacientemente__npacientementa') + #0
# lema(ur'[Ii]_mpereced_ero_nperedec') + #0
# lema(ur'[Ii]_mplí_citamente_npli') + #0
# lema(ur'[Ii]_mponié_ndose_nponie') + #0
# lema(ur'[Ii]_mpres_ionado_nprec') + #0
# lema(ur'[Ii]_mpugnado__npuganado') + #0
# lema(ur'[Ii]_n_morales_m') + #0
# lema(ur'[Ii]_nclui_d[ao]s?_uncluí') + #0
# lema(ur'[Ii]_ncreí_blemente_crei') + #0
# lema(ur'[Ii]_nde_pendizarlo_den') + #0
# lema(ur'[Ii]_ns_piradas_sn') + #0
# lema(ur'[Ii]de_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ii]dear_í_an_i') + #0
# lema(ur'[Ii]gnorar_í_a[ns]?_i') + #0
# lema(ur'[Ii]luminar_í_an_i') + #0
# lema(ur'[Ii]lustr_acio_nes_ció') + #0
# lema(ur'[Ii]lustrar_í_a[ns]?_i') + #0
# lema(ur'[Ii]m__piden_n') + #0
# lema(ur'[Ii]m__plementó_n') + #0
# lema(ur'[Ii]m__ponen_n') + #0
# lema(ur'[Ii]m__portante_n') + #0
# lema(ur'[Ii]m__puesto_n') + #0
# lema(ur'[Ii]m__pulsó_n') + #0
# lema(ur'[Ii]m_portan_te_nporta') + #0
# lema(ur'[Ii]magin_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ii]maginar_í_an_i') + #0
# lema(ur'[Ii]mbu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Ii]mitar_í_an_i') + #0
# lema(ur'[Ii]mpactar_í_a[ns]?_i') + #0
# lema(ur'[Ii]mpartir_á_[ns]?_a') + #0
# lema(ur'[Ii]mpel_í_a[ns]?_i') + #0
# lema(ur'[Ii]mpetrar_í_a[ns]?_i') + #0
# lema(ur'[Ii]mpid_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_e') + #0
# lema(ur'[Ii]mplantar_í_a[ns]?_i') + #0
# lema(ur'[Ii]mplementar_í_an_i') + #0
# lema(ur'[Ii]mplorar_í_a[ns]?_i') + #0
# lema(ur'[Ii]mpon_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Ii]mponi_en_do_ne') + #0
# lema(ur'[Ii]mposi__ción_si') + #0
# lema(ur'[Ii]mposibilitar_í_a[ns]?_i') + #0
# lema(ur'[Ii]mpostar_í_a[ns]?_i') + #0
# lema(ur'[Ii]mpregnar_í_a[ns]?_i') + #0
# lema(ur'[Ii]mpres_io_nes_ó') + #0
# lema(ur'[Ii]mpresionar_í_a[ns]?_i') + #0
# lema(ur'[Ii]mprovisar_í_a[ns]?_i') + #0
# lema(ur'[Ii]mpugnar_í_a[ns]?_i') + #0
# lema(ur'[Ii]mpulsar_í_a[ns]?_i') + #0
# lema(ur'[Ii]mputar_í_a[ns]?_i') + #0
# lema(ur'[Ii]n_dep_endiente_ped') + #0
# lema(ur'[Ii]n_s_peccionar_') + #0
# lema(ur'[Ii]n_s_peccionó_') + #0
# lema(ur'[Ii]n_s_pección_') + #0
# lema(ur'[Ii]n_s_piración_') + #0
# lema(ur'[Ii]n_s_pirada_') + #0
# lema(ur'[Ii]n_s_pirados_') + #0
# lema(ur'[Ii]n_s_piran_') + #0
# lema(ur'[Ii]n_s_piró_') + #0
# lema(ur'[Ii]n_sertá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_certa') + #0
# lema(ur'[Ii]n_stalacio_nes_talació') + #0
# lema(ur'[Ii]n_struccio_nes_trucció') + #0
# lema(ur'[Ii]n_vistié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_sistie') + #0
# lema(ur'[Ii]naugurar_í_a[ns]?_i') + #0
# lema(ur'[Ii]ncapacitar_í_a[ns]?_i') + #0
# lema(ur'[Ii]ncautar_í_a[ns]?_i') + #0
# lema(ur'[Ii]ncentivar_í_a[ns]?_i') + #0
# lema(ur'[Ii]ncid(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Ii]ncidir_á_[ns]?_a') + #0
# lema(ur'[Ii]ncitar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nclinar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nclu_i_rse_í') + #0
# lema(ur'[Ii]nclu_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Ii]nco_m_pleto_n') + #0
# lema(ur'[Ii]ncrepar_í_a[ns]?_i') + #0
# lema(ur'[Ii]ncrustar_í_a[ns]?_i') + #0
# lema(ur'[Ii]ncubar_í_a[ns]?_i') + #0
# lema(ur'[Ii]ncumplir_á_[ns]?_a') + #0
# lema(ur'[Ii]ncurr(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Ii]ncurrir_á_[ns]?_a') + #0
# lema(ur'[Ii]ncursionar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nde_pen_dencia_npe') + #0
# lema(ur'[Ii]nde_pen_diente_npe') + #0
# lema(ur'[Ii]ndic_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ii]ndigestar_í_a[ns]?_i') + #0
# lema(ur'[Ii]ndignar_í_a[ns]?_i') + #0
# lema(ur'[Ii]ndispon_í_a[ns]?_i') + #0
# lema(ur'[Ii]ndultar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nequ_í_voc[ao]_i') + #0
# lema(ur'[Ii]nfectar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nfiltrar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nflig_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Ii]nform_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ii]nfundir_á_[ns]?_a') + #0
# lema(ur'[Ii]nfundir_í_a[ns]?_i') + #0
# lema(ur'[Ii]ngen_ierí_as?_ería') + #0
# lema(ur'[Ii]ngeni_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ii]nhabilitar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nhibir_á_[ns]?_a') + #0
# lema(ur'[Ii]ninterru_m_pidamente_n') + #0
# lema(ur'[Ii]nmigrar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nmiscu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Ii]nmiscuir_s_e(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Ii]nnovar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nquietar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nscri_bié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_e') + #0
# lema(ur'[Ii]nscribir_á_[ns]?_a') + #0
# lema(ur'[Ii]nsert_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ii]nsertar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nsinuar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nsist_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Ii]nsistir_á_[ns]?_a') + #0
# lema(ur'[Ii]nspeccionar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nstal_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ii]nstar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nstaurar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nstru_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Ii]nstrumentar_í_an_i') + #0
# lema(ur'[Ii]nsultar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nsur_reccio_nes_ecció') + #0
# lema(ur'[Ii]nt_entá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_énta') + #0
# lema(ur'[Ii]nte_r_pondrá_n') + #0
# lema(ur'[Ii]nte_r_pretasen_') + #0
# lema(ur'[Ii]nte_r_pretativ[ao]s?_') + #0
# lema(ur'[Ii]nterced_í_a[ns]?_i') + #0
# lema(ur'[Ii]nterceptar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nterconectar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nteres_ándos_e_andoc') + #0
# lema(ur'[Ii]nterjuri_s_diccional_') + #0
# lema(ur'[Ii]nternar_í_an_i') + #0
# lema(ur'[Ii]nterpelar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nterpon_í_a[ns]?_i') + #0
# lema(ur'[Ii]nterru_m_p(?:e[ns]?|iera)_n') + #0
# lema(ur'[Ii]nterrumpir_á_[ns]?_a') + #0
# lema(ur'[Ii]ntimar_í_a[ns]?_i') + #0
# lema(ur'[Ii]ntitular_í_a[ns]?_i') + #0
# lema(ur'[Ii]ntu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Ii]nundar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nva_sio_nes_ció') + #0
# lema(ur'[Ii]nvadir_á_[ns]?_a') + #0
# lema(ur'[Ii]nven_c_ibles?_s') + #0
# lema(ur'[Ii]nvent_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ii]nvest_í_a[ns]_i') + #0
# lema(ur'[Ii]nvestigar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nvitar_í_a[ns]?_i') + #0
# lema(ur'[Ii]nyectar_í_a[ns]?_i') + #0
# lema(ur'[Ii]rritar_í_a[ns]?_i') + #0
# lema(ur'[Ii]rrump(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Ii]rrumpir_á_[ns]?_a') + #0
# lema(ur'[Jj]actar_í_a[ns]?_i') + #0
# lema(ur'[Jj]adear_í_a[ns]?_i') + #0
# lema(ur'[Jj]apon_é_s_pe') + #0
# lema(ur'[Jj]iñar_í_a[ns]?_i') + #0
# lema(ur'[Jj]ubilar_í_an_i') + #0
# lema(ur'[Jj]ug_ándos_e_andoc') + #0
# lema(ur'[Jj]uramentar_í_a[ns]?_i') + #0
# lema(ur'[Jj]urar_í_a[ns]?_i') + #0
# lema(ur'[Jj]ustificar_í_a[ns]?_i') + #0
# lema(ur'[L]e_í_a[ns]_i') + #0
# lema(ur'[L]e_í_da el acta_i') + #0
# lema(ur'[Ll]_egislacio_nes_slegislació') + #0
# lema(ur'[Ll]_lamá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ama') + #0
# lema(ur'[Ll]abrar_í_a[ns]_i') + #0
# lema(ur'[Ll]agrimear_í_a[ns]?_i') + #0
# lema(ur'[Ll]amentar_í_a[ns]_i') + #0
# lema(ur'[Ll]anzar_s_e_z') + #0
# lema(ur'[Ll]astimar_í_a[ns]?_i') + #0
# lema(ur'[Ll]egislar_í_a[ns]?_i') + #0
# lema(ur'[Ll]egitimar_í_an_i') + #0
# lema(ur'[Ll]esionar_í_a[ns]?_i') + #0
# lema(ur'[Ll]evantar_í_a[ns]?_i') + #0
# lema(ur'[Ll]evitar_í_a[ns]?_i') + #0
# lema(ur'[Ll]i_m_pia_n') + #0
# lema(ur'[Ll]i_m_pio_n') + #0
# lema(ur'[Ll]ibar_í_a[ns]?_i') + #0
# lema(ur'[Ll]icitar_í_a[ns]?_i') + #0
# lema(ur'[Ll]iderar_í_a[ns]?_i') + #0
# lema(ur'[Ll]idiar_í_a[ns]?_i') + #0
# lema(ur'[Ll]ig_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ll]ijar_í_a[ns]?_i') + #0
# lema(ur'[Ll]im__piador_n') + #0
# lema(ur'[Ll]imitar_í_a[ns]?_i') + #0
# lema(ur'[Ll]iquidar_í_a[ns]?_i') + #0
# lema(ur'[Ll]istar_í_a[ns]?_i') + #0
# lema(ur'[Ll]leg_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ll]leg_ándos_e_andoc') + #0
# lema(ur'[Ll]lorar_í_a[ns]?_i') + #0
# lema(ur'[Mm]_utipropó_sito_útipropo') + #0
# lema(ur'[Mm]_á_ximamente_a') + #0
# lema(ur'[Mm]a_m_paro_n') + #0
# lema(ur'[Mm]a_m_posterías_n') + #0
# lema(ur'[Mm]adurar_í_a[ns]?_i') + #0
# lema(ur'[Mm]alentend_í_(?:a[ns]?|)_i') + #0
# lema(ur'[Mm]alentender_á_[ns]?_a') + #0
# lema(ur'[Mm]alinterpretar_í_a[ns]?_i') + #0
# lema(ur'[Mm]almet_í_a[ns]?_i') + #0
# lema(ur'[Mm]alograr_í_a[ns]?_i') + #0
# lema(ur'[Mm]altratar_í_a[ns]?_i') + #0
# lema(ur'[Mm]alvend_í_a[ns]?_i') + #0
# lema(ur'[Mm]andar_í_a[ns]_i') + #0
# lema(ur'[Mm]aniobrar_í_a[ns]?_i') + #0
# lema(ur'[Mm]anipular_í_a[ns]?_i') + #0
# lema(ur'[Mm]anteni_en_do_ne') + #0
# lema(ur'[Mm]anufa_c_tura(?:d|d[ao]s?)_') + #0
# lema(ur'[Mm]anufacturar_í_a[ns]?_i') + #0
# lema(ur'[Mm]aquin_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Mm]aravillar_í_a[ns]?_i') + #0
# lema(ur'[Mm]arc_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Mm]architar_í_a[ns]?_i') + #0
# lema(ur'[Mm]arear_í_a[ns]?_i') + #0
# lema(ur'[Mm]arginar_í_a[ns]_i') + #0
# lema(ur'[Mm]arinar_í_a[ns]?_i') + #0
# lema(ur'[Mm]artillar_í_a[ns]?_i') + #0
# lema(ur'[Mm]asacrar_í_a[ns]?_i') + #0
# lema(ur'[Mm]asturbar_í_a[ns]?_i') + #0
# lema(ur'[Mm]ateralizar_í_a[ns]?_i') + #0
# lema(ur'[Mm]atiz_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Mm]atricul_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
# lema(ur'[Mm]atricular_í_a[ns]?_i') + #0
# lema(ur'[Mm]editar_í_a[ns]?_i') + #0
# lema(ur'[Mm]encion_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Mm]encionar_í_a[ns]?_i') + #0
# lema(ur'[Mm]enear_í_a[ns]?_i') + #0
# lema(ur'[Mm]erecer_á_[ns]?_a') + #0
# lema(ur'[Mm]ermar_í_a[ns]?_i') + #0
# lema(ur'[Mm]igrar_í_a[ns]?_i') + #0
# lema(ur'[Mm]ilitar_í_an_i') + #0
# lema(ur'[Mm]imar_í_a[ns]?_i') + #0
# lema(ur'[Mm]ir_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Mm]o_strá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_nstra') + #0
# lema(ur'[Mm]odelar_í_a[ns]?_i') + #0
# lema(ur'[Mm]oderar_í_a[ns]?_i') + #0
# lema(ur'[Mm]ofar_í_a[ns]?_i') + #0
# lema(ur'[Mm]ojar_í_a[ns]?_i') + #0
# lema(ur'[Mm]oldear_í_a[ns]?_i') + #0
# lema(ur'[Mm]olest_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Mm]olestar_í_a[ns]?_i') + #0
# lema(ur'[Mm]oment_á_ne[ao]_a') + #0
# lema(ur'[Mm]ontar_í_a[ns]_i') + #0
# lema(ur'[Mm]os_trá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ntra') + #0
# lema(ur'[Mm]otivar_í_a[ns]?_i') + #0
# lema(ur'[Mm]ovi_éndos_e_endoc') + #0
# lema(ur'[Mm]ovilizar_s_e_z') + #0
# lema(ur'[Mm]ultar_í_a[ns]?_i') + #0
# lema(ur'[Mm]ultilingü_í_stic(?:[ao]s|amente)_i') + #0
# lema(ur'[Mm]ultilingü_í_stic[ao]_i') + #0
# lema(ur'[Mm]urmurar_í_a[ns]?_i') + #0
# lema(ur'[Mm]utar_í_a[ns]?_i') + #0
# lema(ur'[Mm]utilar_í_a[ns]?_i') + #0
# lema(ur'[Mm]utiprop_ó_sito_o') + #0
# lema(ur'[Nn]_o_mbre_p') + #0
# lema(ur'[Nn]adar_í_a[ns]?_i') + #0
# lema(ur'[Nn]arrar_í_a[ns]?_i') + #0
# lema(ur'[Nn]avarroarag_oné_s_óne') + #0
# lema(ur'[Nn]avegar_í_a[ns]?_i') + #0
# lema(ur'[Nn]egar_í_a[ns]?_i') + #0
# lema(ur'[Nn]eole_oné_s_óne') + #0
# lema(ur'[Nn]icarag_üens_es_uenc') + #0
# lema(ur'[Nn]ominar_í_a[ns]?_i') + #0
# lema(ur'[Nn]oquear_í_a[ns]?_i') + #0
# lema(ur'[Nn]otific_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Nn]ov_e_las?_é') + #0
# lema(ur'[Nn]umerar_í_an_i') + #0
# lema(ur'[Nn]utr(?:ir|)_í_an_i') + #0
# lema(ur'[Nn]utrir_á_[ns]?_a') + #0
# lema(ur'[Oo]bjetar_í_a[ns]?_i') + #0
# lema(ur'[Oo]bnubilar_í_a[ns]?_i') + #0
# lema(ur'[Oo]brar_í_a[ns]?_i') + #0
# lema(ur'[Oo]bsequi_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Oo]bserv_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Oo]bsesionar_í_a[ns]?_i') + #0
# lema(ur'[Oo]bstinar_í_a[ns]?_i') + #0
# lema(ur'[Oo]bteni_en_do_ne') + #0
# lema(ur'[Oo]casi_oná_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_na') + #0
# lema(ur'[Oo]clu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Oo]cult_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Oo]cultar_í_a[ns]?_i') + #0
# lema(ur'[Oo]fertar_í_a[ns]?_i') + #0
# lema(ur'[Oo]frec_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #0
# lema(ur'[Oo]frec_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Oo]jear_í_a[ns]?_i') + #0
# lema(ur'[Oo]lvid_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Oo]lvid_ándos_e_andoc') + #0
# lema(ur'[Oo]lvidar_í_a[ns]?_i') + #0
# lema(ur'[Oo]mitir_á_[ns]?_a') + #0
# lema(ur'[Oo]ndear_í_a[ns]?_i') + #0
# lema(ur'[Oo]per_acio_nes_ció') + #0
# lema(ur'[Oo]perar_í_an_i') + #0
# lema(ur'[Oo]pinar_í_a[ns]?_i') + #0
# lema(ur'[Oo]pondr_á_[ns]?_a') + #0
# lema(ur'[Oo]posi_c_ionado_s') + #0
# lema(ur'[Oo]rar_í_a[ns]_i') + #0
# lema(ur'[Oo]rbitar_í_an_i') + #0
# lema(ur'[Oo]rear_í_a[ns]?_i') + #0
# lema(ur'[Oo]rientar_í_a[ns]?_i') + #0
# lema(ur'[Oo]riginar_í_an_i') + #0
# lema(ur'[Oo]rquestar_í_a[ns]?_i') + #0
# lema(ur'[Oo]rtoprot_é_sic[ao]s?_e') + #0
# lema(ur'[Oo]scilar_í_a[ns]?_i') + #0
# lema(ur'[Oo]stentar_í_a[ns]?_i') + #0
# lema(ur'[Oo]vacionar_í_a[ns]?_i') + #0
# lema(ur'[P]artir_í_a[ns]?_i') + #0
# lema(ur'[Pp]_idié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_edie') + #0
# lema(ur'[Pp]actar_í_a[ns]?_i') + #0
# lema(ur'[Pp]ag_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Pp]aginar_í_a[ns]?_i') + #0
# lema(ur'[Pp]alegraf_í_as?_i') + #0
# lema(ur'[Pp]arad_ó_jic[ao]_o') + #0
# lema(ur'[Pp]arafrasear_í_a[ns]?_i') + #0
# lema(ur'[Pp]aram_é_dic[ao]s?_o') + #0
# lema(ur'[Pp]arir_í_a[ns]?_i') + #0
# lema(ur'[Pp]arpadear_í_a[ns]?_i') + #0
# lema(ur'[Pp]artic_iparo_n_paró') + #0
# lema(ur'[Pp]asear_í_a[ns]?_i') + #0
# lema(ur'[Pp]atalear_í_a[ns]?_i') + #0
# lema(ur'[Pp]atear_í_a[ns]?_i') + #0
# lema(ur'[Pp]atentar_í_a[ns]?_i') + #0
# lema(ur'[Pp]atinar_í_a[ns]_i') + #0
# lema(ur'[Pp]atrullar_í_a[ns]?_i') + #0
# lema(ur'[Pp]avimentar_í_a[ns]_i') + #0
# lema(ur'[Pp]edalear_í_a[ns]?_i') + #0
# lema(ur'[Pp]egar_s_e_z') + #0
# lema(ur'[Pp]egar_í_a[ns]?_i') + #0
# lema(ur'[Pp]einar_í_a[ns]?_i') + #0
# lema(ur'[Pp]enetrar_í_a[ns]?_i') + #0
# lema(ur'[Pp]ercatar_í_a[ns]?_i') + #0
# lema(ur'[Pp]ercibir_á_[ns]?_a') + #0
# lema(ur'[Pp]erd_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Pp]erdi_en_do_ne') + #0
# lema(ur'[Pp]erdon_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Pp]erdonar_í_a[ns]?_i') + #0
# lema(ur'[Pp]erecer_á_[ns]?_a') + #0
# lema(ur'[Pp]eregrinar_í_a[ns]?_i') + #0
# lema(ur'[Pp]erfeccionar_í_a[ns]?_i') + #0
# lema(ur'[Pp]erfilar_í_a[ns]?_i') + #0
# lema(ur'[Pp]erforar_í_a[ns]?_i') + #0
# lema(ur'[Pp]eriodontolog_í_as?_i') + #0
# lema(ur'[Pp]ermi_tié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_e') + #0
# lema(ur'[Pp]ermit_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_e') + #0
# lema(ur'[Pp]ermiti_en_do_ne') + #0
# lema(ur'[Pp]ermutar_í_a[ns]?_i') + #0
# lema(ur'[Pp]ernoctar_í_a[ns]?_i') + #0
# lema(ur'[Pp]erpetrar_í_a[ns]?_i') + #0
# lema(ur'[Pp]erpetuar_í_a[ns]?_i') + #0
# lema(ur'[Pp]ersegu_i_d[ao]s?_í') + #0
# lema(ur'[Pp]ersignar_í_a[ns]?_i') + #0
# lema(ur'[Pp]ersigu_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_e') + #0
# lema(ur'[Pp]ersistir_á_[ns]?_a') + #0
# lema(ur'[Pp]ersonar_í_a[ns]?_i') + #0
# lema(ur'[Pp]ersuad(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Pp]ersuadir_á_[ns]?_a') + #0
# lema(ur'[Pp]erturbar_í_a[ns]?_i') + #0
# lema(ur'[Pp]erviv(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Pp]ervivir_á_[ns]?_a') + #0
# lema(ur'[Pp]esar_í_a[ns]?_i') + #0
# lema(ur'[Pp]i_ fiá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_fia') + #0
# lema(ur'[Pp]ic_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Pp]illar_í_a[ns]_i') + #0
# lema(ur'[Pp]inchar_í_a[ns]?_i') + #0
# lema(ur'[Pp]intar_í_a[ns]?_i') + #0
# lema(ur'[Pp]irarse_í_a[ns]?_i') + #0
# lema(ur'[Pp]iratear_í_a[ns]?_i') + #0
# lema(ur'[Pp]isar_í_a[ns]?_i') + #0
# lema(ur'[Pp]ivotar_í_a[ns]?_i') + #0
# lema(ur'[Pp]lanch_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Pp]lanchar_í_a[ns]?_i') + #0
# lema(ur'[Pp]lantar_í_an_i') + #0
# lema(ur'[Pp]lante_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Pp]lantear_í_a[ns]?_i') + #0
# lema(ur'[Pp]lasmar_í_a[ns]?_i') + #0
# lema(ur'[Pp]leitear_í_a[ns]?_i') + #0
# lema(ur'[Pp]od_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Pp]odolog_í_as_i') + #0
# lema(ur'[Pp]olin_ó_mic(?:[ao]s|amente)_o') + #0
# lema(ur'[Pp]onchar_í_a[ns]?_i') + #0
# lema(ur'[Pp]oner_s_e_z') + #0
# lema(ur'[Pp]ortar_í_an_i') + #0
# lema(ur'[Pp]osar_í_a[ns]?_i') + #0
# lema(ur'[Pp]osesionar_í_an_i') + #0
# lema(ur'[Pp]osi_c_ionarse_s') + #0
# lema(ur'[Pp]osi_c_iono_s') + #0
# lema(ur'[Pp]osi_c_ionándose_s') + #0
# lema(ur'[Pp]osi_cioná_ndose_siona') + #0
# lema(ur'[Pp]osibil_itá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ta') + #0
# lema(ur'[Pp]osibili_tarí_a[ns]?_ari') + #0
# lema(ur'[Pp]osicionar_í_a[ns]?_i') + #0
# lema(ur'[Pp]ospon_í_a[ns]?_i') + #0
# lema(ur'[Pp]ostul_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Pp]ostular_í_a[ns]?_i') + #0
# lema(ur'[Pp]r_esentándos_e_sentandoc') + #0
# lema(ur'[Pp]r_á_ctica_a', pre=ur'[Mm]edicina +') + #0
# lema(ur'[Pp]recav_í_a[ns]?_i') + #0
# lema(ur'[Pp]recipitar_í_a[ns]?_i') + #0
# lema(ur'[Pp]recisar_í_a[ns]?_i') + #0
# lema(ur'[Pp]reconceb_í_a[ns]?_i') + #0
# lema(ur'[Pp]reconstru_i_d[ao]s?_í') + #0
# lema(ur'[Pp]redefin(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Pp]redefinir_á_[ns]?_a') + #0
# lema(ur'[Pp]redic_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Pp]redispon_í_a[ns]?_i') + #0
# lema(ur'[Pp]redominar_í_a[ns]?_i') + #0
# lema(ur'[Pp]refi__rieran_e') + #0
# lema(ur'[Pp]refi_rie_ndo_eri') + #0
# lema(ur'[Pp]refi_rié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_erie') + #0
# lema(ur'[Pp]refier__en_i') + #0
# lema(ur'[Pp]refijar_í_a[ns]?_i') + #0
# lema(ur'[Pp]regonar_í_a[ns]?_i') + #0
# lema(ur'[Pp]regun_tá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ata') + #0
# lema(ur'[Pp]regunt_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Pp]reguntar_í_a[ns]?_i') + #0
# lema(ur'[Pp]reocupar_í_a[ns]?_i') + #0
# lema(ur'[Pp]repar_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Pp]repar_ándos_e_andoc') + #0
# lema(ur'[Pp]reparar_í_a[ns]?_i') + #0
# lema(ur'[Pp]rescind(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Pp]rescindir_á_[ns]?_a') + #0
# lema(ur'[Pp]rescrib(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Pp]resent_ándos_e_andoc') + #0
# lema(ur'[Pp]resent_ándos_e_andoc') + #0
# lema(ur'[Pp]reservar_í_a[ns]?_i') + #0
# lema(ur'[Pp]resionar_í_a[ns]?_i') + #0
# lema(ur'[Pp]rest_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Pp]resum_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Pp]resumir_á_[ns]?_a') + #0
# lema(ur'[Pp]rimar_í_an_i') + #0
# lema(ur'[Pp]rin_c_ipal_p') + #0
# lema(ur'[Pp]rin_ci_pio_') + #0
# lema(ur'[Pp]rinci__pal_n') + #0
# lema(ur'[Pp]ro_v_ocad[ao]s?_b') + #0
# lema(ur'[Pp]ro_v_ocarl[aeo]s?_b') + #0
# lema(ur'[Pp]ro_v_ocará[ns]?_b') + #0
# lema(ur'[Pp]ro_v_ocativ[ao]s?_b') + #0
# lema(ur'[Pp]rocesar_í_a[ns]?_i') + #0
# lema(ur'[Pp]rocesionar_í_an_i') + #0
# lema(ur'[Pp]rocrear_í_a[ns]?_i') + #0
# lema(ur'[Pp]rocurar_í_a[ns]?_i') + #0
# lema(ur'[Pp]rofesar_í_a[ns]?_i') + #0
# lema(ur'[Pp]rogresar_í_a[ns]?_i') + #0
# lema(ur'[Pp]roh_ibié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íbie') + #0
# lema(ur'[Pp]rohib_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Pp]roliferar_í_a[ns]?_i') + #0
# lema(ur'[Pp]romo_cioná_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_rciona') + #0
# lema(ur'[Pp]ronunci_ándos_e_andoc') + #0
# lema(ur'[Pp]ronunci_ándos_e_andoc') + #0
# lema(ur'[Pp]ropend_í_a[ns]?_i') + #0
# lema(ur'[Pp]ropiciar_í_a[ns]?_i') + #0
# lema(ur'[Pp]ropinar_í_a[ns]?_i') + #0
# lema(ur'[Pp]roponi_en_do_ne') + #0
# lema(ur'[Pp]ropugnar_í_a[ns]?_i') + #0
# lema(ur'[Pp]ropulsar_í_a[ns]?_i') + #0
# lema(ur'[Pp]roscrib(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Pp]roscribir_á_[ns]?_a') + #0
# lema(ur'[Pp]rosegu_i_d[ao]s?_í') + #0
# lema(ur'[Pp]rosperar_í_a[ns]?_i') + #0
# lema(ur'[Pp]rostitu_i_d[ao]s?_í') + #0
# lema(ur'[Pp]rostitu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Pp]rot_ég_el[aeo]s?_ej') + #0
# lema(ur'[Pp]rote_gers_e_jerc') + #0
# lema(ur'[Pp]rote_gió__jio') + #0
# lema(ur'[Pp]rotestar_í_a[ns]?_i') + #0
# lema(ur'[Pp]rove_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Pp]ublicitar_í_an_i') + #0
# lema(ur'[Pp]ujar_í_a[ns]?_i') + #0
# lema(ur'[Pp]ulir_í_a[ns]?_i') + #0
# lema(ur'[Pp]ulsar_í_a[ns]?_i') + #0
# lema(ur'[Pp]untuar_í_a[ns]?_i') + #0
# lema(ur'[Qq]_u_edan(?:do|)_') + #0
# lema(ur'[Qq]u_ie_nes_ei') + #0
# lema(ur'[Qq]uebrantar_í_a[ns]?_i') + #0
# lema(ur'[Qq]uebrar_í_a[ns]?_i') + #0
# lema(ur'[Qq]ued_ándos_e_andoc') + #0
# lema(ur'[Qq]uejar_í_a[ns]?_i') + #0
# lema(ur'[Qq]uemar_í_a[ns]?_i') + #0
# lema(ur'[Qq]uer_íai_s_iaí') + #0
# lema(ur'[Qq]uerellar_í_a[ns]?_i') + #0
# lema(ur'[Qq]ui_tá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_a') + #0
# lema(ur'[Qq]ui_tá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_nta') + #0
# lema(ur'[Qq]uin_c_ena(?! ao)_[sz]') + #0
# lema(ur'[Rr]_obá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_eoba') + #0
# lema(ur'[Rr]adicándo_s_e_c') + #0
# lema(ur'[Rr]aptar_í_a[ns]?_i') + #0
# lema(ur'[Rr]asguñar_í_a[ns]?_i') + #0
# lema(ur'[Rr]astrear_í_a[ns]?_i') + #0
# lema(ur'[Rr]ay_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Rr]ayar_í_a[ns]?_i') + #0
# lema(ur'[Rr]azonar_í_a[ns]?_i') + #0
# lema(ur'[Rr]e_construi_d[ao]s?_nconstruí') + #0
# lema(ur'[Rr]eabr(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Rr]eabsorb_í_a[ns]?_i') + #0
# lema(ur'[Rr]eaccionar_í_an_i') + #0
# lema(ur'[Rr]eacondicionar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eactivar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eafirm_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Rr]eafirmar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eagrupar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ealiz_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Rr]eanimar_í_a[ns]?_i') + #0
# lema(ur'[Rr]easign_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Rr]easignar_í_a[ns]?_i') + #0
# lema(ur'[Rr]easum(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Rr]easumir_á_[ns]?_a') + #0
# lema(ur'[Rr]eavivar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ebajar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ebanar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ebasar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ebat(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Rr]ebatir_á_[ns]?_a') + #0
# lema(ur'[Rr]ebelar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ebotar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ebusc_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Rr]ec_ordá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_órda') + #0
# lema(ur'[Rr]ecabar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ecalar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ecapturar_í_a[ns]?_i') + #0
# lema(ur'[Rr]echazar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eciclar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ecitar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eclamar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eclu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Rr]eco_gió__jio') + #0
# lema(ur'[Rr]eco_gí_a_ji') + #0
# lema(ur'[Rr]eco_nstitui_d[ao]s?_stituí') + #0
# lema(ur'[Rr]ecobrar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ecolectar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ecombinar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ecomend_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Rr]ecomendar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ecomi_en_do_ne') + #0
# lema(ur'[Rr]ecompensar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ecompon_í_a[ns]?_i') + #0
# lema(ur'[Rr]econ_strui_d[ao]s?_truí') + #0
# lema(ur'[Rr]econ_struyó__truyo') + #0
# lema(ur'[Rr]econcom_í_a[ns]?_i') + #0
# lema(ur'[Rr]econoc_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Rr]econsiderar_í_a[ns]?_i') + #0
# lema(ur'[Rr]econst_itui_d[ao]s?_uí') + #0
# lema(ur'[Rr]econst_r_uye[ns]?_') + #0
# lema(ur'[Rr]econstitu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Rr]ecopilar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ecord_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Rr]ecorr_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Rr]ecos_í_a[ns]?_i') + #0
# lema(ur'[Rr]ecrear_í_a[ns]?_i') + #0
# lema(ur'[Rr]ecrimin_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Rr]ecriminar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ecub__rimientos?_i') + #0
# lema(ur'[Rr]ecub_r_ir(?:se|)_') + #0
# lema(ur'[Rr]ecub_ri_mientos?_ir') + #0
# lema(ur'[Rr]ecubi_e_rt[ao]s?_') + #0
# lema(ur'[Rr]ecubr(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Rr]ecubrir_á_[ns]?_a') + #0
# lema(ur'[Rr]ecular_í_a[ns]?_i') + #0
# lema(ur'[Rr]edefinir_á_[ns]?_a') + #0
# lema(ur'[Rr]edescubi_e_rt[ao]s?_') + #0
# lema(ur'[Rr]edescubr(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Rr]edescubrir_á_[ns]?_a') + #0
# lema(ur'[Rr]edim(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Rr]edimir_á_[ns]?_a') + #0
# lema(ur'[Rr]edireccionar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ediseñar_í_a[ns]?_i') + #0
# lema(ur'[Rr]edistribu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Rr]edit_ú_(?:a[ns]?|e[ns]?)_u') + #0
# lema(ur'[Rr]edoblar_í_a[ns]?_i') + #0
# lema(ur'[Rr]edondear_í_a[ns]?_i') + #0
# lema(ur'[Rr]educ_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_cie') + #0
# lema(ur'[Rr]edundar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eel_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Rr]eelaborar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eemprend_í_a[ns]?_i') + #0
# lema(ur'[Rr]eencarnar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eentrar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eescribir_á_[ns]?_a') + #0
# lema(ur'[Rr]eestrenar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eestructurar_í_a[ns]?_i') + #0
# lema(ur'[Rr]efer_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Rr]eferir_s_e_z') + #0
# lema(ur'[Rr]efiri_éndos_e_endoc') + #0
# lema(ur'[Rr]eflexionar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eflu_i_d[ao]s?_í') + #0
# lema(ur'[Rr]eflu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Rr]eformar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eformular_í_a[ns]?_i') + #0
# lema(ur'[Rr]eforzar_í_a[ns]?_i') + #0
# lema(ur'[Rr]efresquer_í_as?_i') + #0
# lema(ur'[Rr]efutar_í_a[ns]?_i') + #0
# lema(ur'[Rr]egal_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Rr]egalar_í_a[ns]?_i') + #0
# lema(ur'[Rr]egañar_í_a[ns]?_i') + #0
# lema(ur'[Rr]egentar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eglamentar_í_an_i') + #0
# lema(ur'[Rr]egular_í_a[ns]_i') + #0
# lema(ur'[Rr]ehabilitar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ei_m_plantes_n') + #0
# lema(ur'[Rr]eimprim(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Rr]eimprimir_á_[ns]?_a') + #0
# lema(ur'[Rr]einar_í_a[ns]?_i') + #0
# lema(ur'[Rr]einaugurar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eincid(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Rr]eincidir_á_[ns]?_a') + #0
# lema(ur'[Rr]eincorporar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eingresar_í_a[ns]?_i') + #0
# lema(ur'[Rr]einiciar_í_a[ns]?_i') + #0
# lema(ur'[Rr]einstalar_í_a[ns]?_i') + #0
# lema(ur'[Rr]einstaurar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eintegrar_í_a[ns]?_i') + #0
# lema(ur'[Rr]einterpretar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eiterar_í_a[ns]?_i') + #0
# lema(ur'[Rr]elacionar_í_a[ns]?_i') + #0
# lema(ur'[Rr]elajar_í_a[ns]?_i') + #0
# lema(ur'[Rr]elam_í_a[ns]?_i') + #0
# lema(ur'[Rr]elampaguear_í_a[ns]?_i') + #0
# lema(ur'[Rr]ele_í_a[ns]?_i') + #0
# lema(ur'[Rr]elevar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ellenar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ematar_í_a[ns]?_i') + #0
# lema(ur'[Rr]emedar_í_a[ns]?_i') + #0
# lema(ur'[Rr]ememorar_í_a[ns]?_i') + #0
# lema(ur'[Rr]emet_í_a[ns]?_i') + #0
# lema(ur'[Rr]emezclar_í_a[ns]?_i') + #0
# lema(ur'[Rr]emitir_á_[ns]?_a') + #0
# lema(ur'[Rr]emodelar_í_a[ns]?_i') + #0
# lema(ur'[Rr]end_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Rr]endir_s_e_z') + #0
# lema(ur'[Rr]enov_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Rr]eordenar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eorganizar_s_e_z') + #0
# lema(ur'[Rr]eorientar_í_a[ns]?_i') + #0
# lema(ur'[Rr]epagar_í_a[ns]?_i') + #0
# lema(ur'[Rr]epartir_á_[ns]?_a') + #0
# lema(ur'[Rr]epasar_í_a[ns]?_i') + #0
# lema(ur'[Rr]epatriar_í_a[ns]?_i') + #0
# lema(ur'[Rr]epel_í_a[ns]?_i') + #0
# lema(ur'[Rr]epercut(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Rr]epercutir_á_[ns]?_a') + #0
# lema(ur'[Rr]eplante_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Rr]eplantear_í_a[ns]?_i') + #0
# lema(ur'[Rr]epon_í_a[ns]?_i') + #0
# lema(ur'[Rr]eportar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eposi_c_ionar_s') + #0
# lema(ur'[Rr]eprend_í_a[ns]?_i') + #0
# lema(ur'[Rr]eprim(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Rr]eprimir_á_[ns]?_a') + #0
# lema(ur'[Rr]eproch_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Rr]eprochar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eprogramar_í_a[ns]?_i') + #0
# lema(ur'[Rr]equetele_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Rr]equisar_í_a[ns]?_i') + #0
# lema(ur'[Rr]esaltar_í_a[ns]?_i') + #0
# lema(ur'[Rr]esbalar_í_a[ns]?_i') + #0
# lema(ur'[Rr]escindir_á_[ns]?_a') + #0
# lema(ur'[Rr]eservar_í_a[ns]?_i') + #0
# lema(ur'[Rr]eseñar_í_a[ns]?_i') + #0
# lema(ur'[Rr]esignar_í_a[ns]?_i') + #0
# lema(ur'[Rr]esist_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Rr]espetar_í_a[ns]?_i') + #0
# lema(ur'[Rr]espo_ndié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_die') + #0
# lema(ur'[Rr]espond_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Rr]estar_í_a[ns]?_i') + #0
# lema(ur'[Rr]estaurar_í_a[ns]?_i') + #0
# lema(ur'[Rr]esumi_en_do_ne') + #0
# lema(ur'[Rr]esumir_á_[ns]?_a') + #0
# lema(ur'[Rr]etardar_í_a[ns]?_i') + #0
# lema(ur'[Rr]etransmitir_á_[ns]?_a') + #0
# lema(ur'[Rr]etrasar_í_a[ns]?_i') + #0
# lema(ur'[Rr]etratar_í_a[ns]?_i') + #0
# lema(ur'[Rr]etribu_i_r(?:l[aeo]s?|se|)_í') + #0
# lema(ur'[Rr]etroced_í_a[ns]?_i') + #0
# lema(ur'[Rr]etrotra_í_(?:a[ns]?|d[ao]s?)_i') + #0
# lema(ur'[Rr]euni_en_do_ne') + #0
# lema(ur'[Rr]evalidar_í_a[ns]?_i') + #0
# lema(ur'[Rr]evelar_í_a[ns]?_i') + #0
# lema(ur'[Rr]evend_í_a[ns]?_i') + #0
# lema(ur'[Rr]evert_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Rr]everter_á_[ns]_a') + #0
# lema(ur'[Rr]evest_í_a[ns]?_i') + #0
# lema(ur'[Rr]evi_s_ar_z') + #0
# lema(ur'[Rr]evisar_í_a[ns]?_i') + #0
# lema(ur'[Rr]evivir_á_[ns]?_a') + #0
# lema(ur'[Rr]evolucionar_í_an_i') + #0
# lema(ur'[Rr]obar_í_a[ns]?_i') + #0
# lema(ur'[Rr]umorear_í_a[ns]?_i') + #0
# lema(ur'[Ss]ab_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Ss]aborear_í_a[ns]?_i') + #0
# lema(ur'[Ss]abotear_í_a[ns]?_i') + #0
# lema(ur'[Ss]acud(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Ss]acudir_á_[ns]?_a') + #0
# lema(ur'[Ss]aldar_í_a[ns]?_i') + #0
# lema(ur'[Ss]altar_í_a[ns]?_i') + #0
# lema(ur'[Ss]altear_í_a[ns]?_i') + #0
# lema(ur'[Ss]aludar_í_a[ns]?_i') + #0
# lema(ur'[Ss]anar_í_a[ns]_i') + #0
# lema(ur'[Ss]ancionar_í_a[ns]?_i') + #0
# lema(ur'[Ss]anear_í_a[ns]?_i') + #0
# lema(ur'[Ss]angrar_í_a[ns]?_i') + #0
# lema(ur'[Ss]aquear_í_a[ns]?_i') + #0
# lema(ur'[Ss]ecu_e_nciación_a') + #0
# lema(ur'[Ss]ecuestrar_í_a[ns]?_i') + #0
# lema(ur'[Ss]ecundar_í_an_i') + #0
# lema(ur'[Ss]elecc_io_nes_ció') + #0
# lema(ur'[Ss]emidisminu_i_d[ao]s?_í') + #0
# lema(ur'[Ss]eptuag_ésimo sé_ptimo_esimose') + #0
# lema(ur'[Ss]epultar_í_a[ns]?_i') + #0
# lema(ur'[Ss]erv_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Ss]esionar_í_a[ns]?_i') + #0
# lema(ur'[Ss]eñalar_í_a[ns]?_i') + #0
# lema(ur'[Ss]i_m_plicidad_n') + #0
# lema(ur'[Ss]i_mpatí_a_npati') + #0
# lema(ur'[Ss]ig_uié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_ie') + #0
# lema(ur'[Ss]igu_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_e') + #0
# lema(ur'[Ss]igui_en_do_ne') + #0
# lema(ur'[Ss]il_bá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_va') + #0
# lema(ur'[Ss]ilbar_í_a[ns]?_i') + #0
# lema(ur'[Ss]imular_í_a[ns]?_i') + #0
# lema(ur'[Ss]imultanear_í_a[ns]?_i') + #0
# lema(ur'[Ss]in_ _pagar_') + #0
# lema(ur'[Ss]ina__psis_n') + #0
# lema(ur'[Ss]ir_vien_do_ivine') + #0
# lema(ur'[Ss]irvi_en_do_ne') + #0
# lema(ur'[Ss]it_uá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_úa') + #0
# lema(ur'[Ss]obornar_í_a[ns]?_i') + #0
# lema(ur'[Ss]obreco_g_(?:e|edor|edoras)_j') + #0
# lema(ur'[Ss]obreco_g_e[ns]?_j') + #0
# lema(ur'[Ss]obreentend_í_(?:a[ns]?|)_i') + #0
# lema(ur'[Ss]obreentender_á_[ns]?_a') + #0
# lema(ur'[Ss]obreexced_í_a[ns]?_i') + #0
# lema(ur'[Ss]obrentend_í_(?:a[ns]?|)_i') + #0
# lema(ur'[Ss]obrentender_á_[ns]?_a') + #0
# lema(ur'[Ss]obrepasar_í_a[ns]?_i') + #0
# lema(ur'[Ss]obrepon_í_a[ns]?_i') + #0
# lema(ur'[Ss]obresaldr_á_[ns]?_a') + #0
# lema(ur'[Ss]obrese_í_a[ns]?_i') + #0
# lema(ur'[Ss]obrexced_í_a[ns]?_i') + #0
# lema(ur'[Ss]ocavar_í_a[ns]?_i') + #0
# lema(ur'[Ss]olapar_í_a[ns]?_i') + #0
# lema(ur'[Ss]olicit_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Ss]olicitar_í_a[ns]?_i') + #0
# lema(ur'[Ss]oluci_ón polí_tica_onpoli') + #0
# lema(ur'[Ss]olucionar_í_a[ns]?_i') + #0
# lema(ur'[Ss]omet_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #0
# lema(ur'[Ss]ondear_í_a[ns]?_i') + #0
# lema(ur'[Ss]onre_í_a[ns]?_i') + #0
# lema(ur'[Ss]opesar_í_a[ns]?_i') + #0
# lema(ur'[Ss]oplar_í_a[ns]?_i') + #0
# lema(ur'[Ss]ort_eá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_éa') + #0
# lema(ur'[Ss]ortear_í_a[ns]?_i') + #0
# lema(ur'[Ss]oslayar_í_a[ns]?_i') + #0
# lema(ur'[Ss]ospechar_í_a[ns]?_i') + #0
# lema(ur'[Ss]u_stitui_d[ao]s?_btituí') + #0
# lema(ur'[Ss]ub_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Ss]ubastar_í_a[ns]?_i') + #0
# lema(ur'[Ss]ubdividir_á_[ns]?_a') + #0
# lema(ur'[Ss]ubestimar_í_a[ns]?_i') + #0
# lema(ur'[Ss]ubir_í_a[ns]?_i', pre=ur'May ') + #0
# lema(ur'[Ss]ublevar_í_a[ns]?_i') + #0
# lema(ur'[Ss]ublimar_í_a[ns]?_i') + #0
# lema(ur'[Ss]ubrayar_í_a[ns]?_i') + #0
# lema(ur'[Ss]ubsanar_í_a[ns]?_i') + #0
# lema(ur'[Ss]ubsistir_á_[ns]?_a') + #0
# lema(ur'[Ss]ubtend_í_(?:a[ns]?|)_i') + #0
# lema(ur'[Ss]ubtender_á_[ns]?_a') + #0
# lema(ur'[Ss]ubtitular_í_a[ns]?_i') + #0
# lema(ur'[Ss]uc_edié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_idie') + #0
# lema(ur'[Ss]ucumbir_á_[ns]?_a') + #0
# lema(ur'[Ss]ugestionar_í_a[ns]?_i') + #0
# lema(ur'[Ss]ugi_rié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_erie') + #0
# lema(ur'[Ss]uicid_ándos_e_andoc') + #0
# lema(ur'[Ss]uicidar_í_an_i') + #0
# lema(ur'[Ss]ujetar_í_a[ns]?_i') + #0
# lema(ur'[Ss]umir_í_a[ns]?_i') + #0
# lema(ur'[Ss]uperflu_i_dos?_í') + #0
# lema(ur'[Ss]uperpon_í_a[ns]?_i') + #0
# lema(ur'[Ss]upervisar_í_a[ns]?_i') + #0
# lema(ur'[Ss]upl(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Ss]uplantar_í_a[ns]?_i') + #0
# lema(ur'[Ss]uplir_á_[ns]?_a') + #0
# lema(ur'[Ss]uprim(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Ss]uprimir_á_[ns]?_a') + #0
# lema(ur'[Ss]uscitar_í_a[ns]?_i') + #0
# lema(ur'[Ss]uscrib(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Ss]uscribir_á_[ns]?_a') + #0
# lema(ur'[Ss]uspensión_ _para_') + #0
# lema(ur'[Ss]ustentar_í_a[ns]?_i') + #0
# lema(ur'[Ss]usurrar_í_a[ns]?_i') + #0
# lema(ur'[Tt]achar_í_a[ns]?_i') + #0
# lema(ur'[Tt]alar_í_a[ns]_i') + #0
# lema(ur'[Tt]allar_í_a[ns]?_i') + #0
# lema(ur'[Tt]ambién_ _parece_') + #0
# lema(ur'[Tt]ambién_ _permiten_') + #0
# lema(ur'[Tt]ap_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Tt]arar_í_an_i') + #0
# lema(ur'[Tt]ararear_í_a[ns]?_i') + #0
# lema(ur'[Tt]artamudear_í_a[ns]?_i') + #0
# lema(ur'[Tt]e_m_peratura_n') + #0
# lema(ur'[Tt]e_m_poradas_n') + #0
# lema(ur'[Tt]e_rminarí_a[ns]?_minari') + #0
# lema(ur'[Tt]ect_ónica_mente_onicá') + #0
# lema(ur'[Tt]ele_v_isión_b') + #0
# lema(ur'[Tt]elefan_á_tic[ao]s?_a') + #0
# lema(ur'[Tt]elefonear_í_a[ns]?_i') + #0
# lema(ur'[Tt]elenov_e_la_é') + #0
# lema(ur'[Tt]eletra_ns_portando_sn') + #0
# lema(ur'[Tt]eletra_ns_portó_sn') + #0
# lema(ur'[Tt]eletran_s_portación_') + #0
# lema(ur'[Tt]eletran_s_portador_') + #0
# lema(ur'[Tt]eletran_s_portan_') + #0
# lema(ur'[Tt]eletran_s_portarse_') + #0
# lema(ur'[Tt]eletran_s_porte_') + #0
# lema(ur'[Tt]eletransportar_í_a[ns]?_i') + #0
# lema(ur'[Tt]elevisar_í_a[ns]?_i') + #0
# lema(ur'[Tt]elonear_í_a[ns]?_i') + #0
# lema(ur'[Tt]emblar_í_a[ns]?_i') + #0
# lema(ur'[Tt]emplar_í_an_i') + #0
# lema(ur'[Tt]en_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Tt]ender_á_[ns]_a') + #0
# lema(ur'[Tt]ergiversar_í_a[ns]?_i') + #0
# lema(ur'[Tt]ermin_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Tt]eñ_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Tt]ildar_í_a[ns]?_i') + #0
# lema(ur'[Tt]itubear_í_a[ns]?_i') + #0
# lema(ur'[Tt]op_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Tt]opar_í_an_i') + #0
# lema(ur'[Tt]or_cié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_sie') + #0
# lema(ur'[Tt]orear_í_a[ns]?_i') + #0
# lema(ur'[Tt]ornar_í_a[ns]_i') + #0
# lema(ur'[Tt]orpedear_í_a[ns]?_i') + #0
# lema(ur'[Tt]orturar_í_a[ns]?_i') + #0
# lema(ur'[Tt]ra_m_polín_n') + #0
# lema(ur'[Tt]ra_mpolí_n_npoli') + #0
# lema(ur'[Tt]ra_ns_parentes_sn') + #0
# lema(ur'[Tt]ra_ns_porta_sn') + #0
# lema(ur'[Tt]ra_ns_portadas_sn') + #0
# lema(ur'[Tt]ra_ns_portadores_sn') + #0
# lema(ur'[Tt]ra_ns_portados_sn') + #0
# lema(ur'[Tt]ra_ns_portar_sn') + #0
# lema(ur'[Tt]ra_ns_portarlo_sn') + #0
# lema(ur'[Tt]ra_ns_portaron_sn') + #0
# lema(ur'[Tt]ra_ns_portistas_sn') + #0
# lema(ur'[Tt]ra_spasá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_pasa') + #0
# lema(ur'[Tt]ra_splantá_r[mts]el[aeo]s?_nspanta') + #0
# lema(ur'[Tt]ra_sportan__nportas') + #0
# lema(ur'[Tt]rabaj_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Tt]rabar_í_a[ns]_i') + #0
# lema(ur'[Tt]rad_uccio_nes_icció') + #0
# lema(ur'[Tt]raduc_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Tt]rag_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Tt]ramar_í_a[ns]?_i') + #0
# lema(ur'[Tt]ramitar_í_a[ns]?_i') + #0
# lema(ur'[Tt]ran_s_parente_') + #0
# lema(ur'[Tt]ran_s_parentemente_') + #0
# lema(ur'[Tt]ran_s_porta_') + #0
# lema(ur'[Tt]ran_s_portaba_') + #0
# lema(ur'[Tt]ran_s_portaban_') + #0
# lema(ur'[Tt]ran_s_portables_') + #0
# lema(ur'[Tt]ran_s_portación_') + #0
# lema(ur'[Tt]ran_s_portadas_') + #0
# lema(ur'[Tt]ran_s_portado_') + #0
# lema(ur'[Tt]ran_s_portadores_') + #0
# lema(ur'[Tt]ran_s_portan_') + #0
# lema(ur'[Tt]ran_s_portando_') + #0
# lema(ur'[Tt]ran_s_portar_') + #0
# lema(ur'[Tt]ran_s_portaría_') + #0
# lema(ur'[Tt]ran_s_portista_') + #0
# lema(ur'[Tt]ran_s_posición_') + #0
# lema(ur'[Tt]ran_scurrien_do_currine') + #0
# lema(ur'[Tt]ran_sfirié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_firie') + #0
# lema(ur'[Tt]ran_sformacio_nes_formació') + #0
# lema(ur'[Tt]ran_sp_ortes_ps') + #0
# lema(ur'[Tt]ran_spo_rte_p') + #0
# lema(ur'[Tt]ran_spor_tes_pos') + #0
# lema(ur'[Tt]ranscend_í_(?:a[ns]?|)_i') + #0
# lema(ur'[Tt]ranscribir_á_[ns]?_a') + #0
# lema(ur'[Tt]ransform_ándos_e_andoc') + #0
# lema(ur'[Tt]ransform_ándos_e_andoc') + #0
# lema(ur'[Tt]ransmit_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Tt]ransparentar_í_a[ns]?_i') + #0
# lema(ur'[Tt]ranspon_í_a[ns]?_i') + #0
# lema(ur'[Tt]rapear_í_a[ns]?_i') + #0
# lema(ur'[Tt]ras_por_tar_npos') + #0
# lema(ur'[Tt]rascend_í_(?:a[ns]?|)_i') + #0
# lema(ur'[Tt]rascend_í_a[ns]?_i') + #0
# lema(ur'[Tt]rascender_á_[ns]?_a') + #0
# lema(ur'[Tt]rascurr(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Tt]rascurrir_á_[ns]?_a') + #0
# lema(ur'[Tt]rasformar_í_a[ns]?_i') + #0
# lema(ur'[Tt]raslad_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Tt]rasladándo_s_e_c') + #0
# lema(ur'[Tt]rasnochar_í_a[ns]?_i') + #0
# lema(ur'[Tt]raspasar_í_a[ns]?_i') + #0
# lema(ur'[Tt]raspon_í_a[ns]?_i') + #0
# lema(ur'[Tt]rastabillar_í_a[ns]?_i') + #0
# lema(ur'[Tt]rastocar_í_a[ns]?_i') + #0
# lema(ur'[Tt]rastornar_í_a[ns]?_i') + #0
# lema(ur'[Tt]ravest_í_a[ns]?_i') + #0
# lema(ur'[Tt]repar_í_a[ns]?_i') + #0
# lema(ur'[Tt]ributar_í_an_i') + #0
# lema(ur'[Tt]riturar_í_a[ns]?_i') + #0
# lema(ur'[Tt]riunfar_í_a[ns]?_i') + #0
# lema(ur'[Tt]umbar_í_a[ns]?_i') + #0
# lema(ur'[Tt]utear_í_a[ns]?_i') + #0
# lema(ur'[Uu]fanarse_í_a[ns]?_i') + #0
# lema(ur'[Uu]ltimar_í_a[ns]?_i') + #0
# lema(ur'[Uu]n_ _parque_') + #0
# lema(ur'[Uu]n_ _pequeño_') + #0
# lema(ur'[Uu]n_ _pingüino_') + #0
# lema(ur'[Uu]n_ _pistolero_') + #0
# lema(ur'[Uu]n_ _principio_') + #0
# lema(ur'[Uu]n_ _puesto_') + #0
# lema(ur'[Uu]n_ pró_logo_pro') + #0
# lema(ur'[Uu]nificar_í_a[ns]?_i') + #0
# lema(ur'[Uu]ntar_í_a[ns]?_i') + #0
# lema(ur'[Uu]rd(?:ir|)_í_a[ns]?_i') + #0
# lema(ur'[Uu]rdir_á_[ns]?_a') + #0
# lema(ur'[Uu]surpar_í_a[ns]?_i') + #0
# lema(ur'[Uu]tilizar_s_e_z') + #0
# lema(ur'[V]ivir_í_as?_i') + #0
# lema(ur'[Vv]aciar_í_a[ns]?_i') + #0
# lema(ur'[Vv]acilar_í_a[ns]?_i') + #0
# lema(ur'[Vv]alidar_í_a[ns]?_i') + #0
# lema(ur'[Vv]alor_á_r[mts]el[aeo]s?_a') + #0
# lema(ur'[Vv]alorar_í_a[ns]?_i') + #0
# lema(ur'[Vv]aquer_í_as?_i') + #0
# lema(ur'[Vv]ariar_í_a[ns]?_i') + #0
# lema(ur'[Vv]aticinar_í_a[ns]?_i') + #0
# lema(ur'[Vv]end_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Vv]enerar_í_a[ns]?_i') + #0
# lema(ur'[Vv]engar_í_a[ns]?_i') + #0
# lema(ur'[Vv]eranear_í_a[ns]?_i') + #0
# lema(ur'[Vv]ersar_í_a[ns]_i') + #0
# lema(ur'[Vv]ersionar_í_a[ns]?_i') + #0
# lema(ur'[Vv]erter_á_[ns]?_a') + #0
# lema(ur'[Vv]est_í_r[mts]el[aeo]s?_i') + #0
# lema(ur'[Vv]etar_í_a[ns]?_i') + #0
# lema(ur'[Vv]i_en_do_ne') + #0
# lema(ur'[Vv]igilar_í_a[ns]?_i') + #0
# lema(ur'[Vv]igésima_ sé_ptima_se') + #0
# lema(ur'[Vv]igésimo_ sé_ptim[ao]s?_se') + #0
# lema(ur'[Vv]incular_í_a[ns]?_i') + #0
# lema(ur'[Vv]iolentar_í_a[ns]?_i') + #0
# lema(ur'[Vv]isionar_í_an_i') + #0
# lema(ur'[Vv]isitar_í_a[ns]?_i') + #0
# lema(ur'[Vv]islumbrar_í_a[ns]?_i') + #0
# lema(ur'[Vv]oltear_í_a[ns]?_i') + #0
# lema(ur'[Vv]olv_é_r[mts]el[aeo]s?_e') + #0
# lema(ur'[Vv]omitar_í_a[ns]?_i') + #0
# lema(ur'[Vv]otar_í_a[ns]?_i') + #0
# lema(ur'[Vv]ulnerar_í_an_i') + #0
# lema(ur'[Y]aund_é__e') + #0
# lema(ur'[Yy]uxtapon_í_a[ns]?_i') + #0
# lema(ur'[Zz]afar_í_a[ns]?_i') + #0
# lema(ur'[Zz]anjar_í_a[ns]?_i') + #0
# lema(ur'[Zz]arpar_í_a[ns]?_i') + #0
# lema(ur'[Zz]ozobrar_í_a[ns]?_i') + #0
# lema(ur'[Zz]urrar_í_a[ns]?_i') + #0
# lema(ur'[a]ll_á__a', pre=ur'(?:[Ee]stando|[Ee]speraba|[Ll]egaron) ') + #0
# lema(ur'[a]m_á_ndola_a') + #0
# lema(ur'[a]rrastrar_í_a[ns]?_i') + #0
# lema(ur'[b]esar_í_a[ns]?_i') + #0
# lema(ur'[c]avar_í_a_i') + #0
# lema(ur'[c]omisionar_í_an_i') + #0
# lema(ur'[eHh]aciéndo_s_e_c') + #0
# lema(ur'[f]a_s_cina_') + #0
# lema(ur'[r]everter_á__a') + #0
# lema(ur'[s]_o_lido_ó', pre=ur'[Hh]a ') + #0
# lema(ur'[t]ender_á_ a_a') + #0
# lema(ur'__Acerca(?:r|rse|)_H') + #0
# lema(ur'_acostumbrando__aconstumbrando', pre=ur'[Ee]stán? ') + #0
# lema(ur'_adentrando__adrentrando', pre=ur'[Ee]stán? ') + #0
# lema(ur'_alejando__lejando', pre=ur'[Ee]stán? ') + #0
# lema(ur'_asechando__hasechando', pre=ur'[Ee]stán? ') + #0
# lema(ur'_baldí_os?_valdi') + #0
# lema(ur'_columpiando__colunpeando', pre=ur'[Ee]stán? ') + #0
# lema(ur'_construi_d[Ao]s?_onstruí') + #0
# lema(ur'_contraatacando__contratacando', pre=ur'[Ee]stán? ') + #0
# lema(ur'_diciembre__[Dd]ezembro', pre=ur'acessado em [0-9]+ de ') + #0
# lema(ur'_echarí_a[ns]?_hechari') + #0
# lema(ur'_empezando__empesando', pre=ur'[Ee]stán? ') + #0
# lema(ur'_enero__[Jj]aneiro', pre=ur'acessado em [0-9]+ de ') + #0
# lema(ur'_evaluando__valutando de', pre=ur'[Ee]stán? ') + #0
# lema(ur'_fingiendo__fingiando', pre=ur'[Ee]stán? ') + #0
# lema(ur'_h_aciéndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_') + #0
# lema(ur'_ha_sta ahora_a') + #0
# lema(ur'_hu_ndi(?:d[ao]s?|dimiento)_u') + #0
# lema(ur'_julio__[Jj]ulho', pre=ur'acessado em [0-9]+ de ') + #0
# lema(ur'_junio__[Jj]uin', pre=ur'acessado em [0-9]+ de ') + #0
# lema(ur'_mayo__[Mm]aio', pre=ur'acessado em [0-9]+ de ') + #0
# lema(ur'_octubre__[Oo]utubro', pre=ur'acessado em [0-9]+ de ') + #0
# lema(ur'_preparando__prparando', pre=ur'[Ee]stán? ') + #0
# lema(ur'_septiembre__[Ss]etembro', pre=ur'acessado em [0-9]+ de ') + #0
# lema(ur'_siempre__cienpre') + #0
# lema(ur'_vigilando__vijilando', pre=ur'[Ee]stán? ') + #0
# lema(ur'_vié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_bie') + #0
# lema(ur'_volviendo viable__viabilizando', pre=ur'[Ee]stán? ') + #0
# lema(ur'_Í_ntegramente_I') + #0
# lema(ur'_í_r[mts]el[aeo]s?_i') + #0
#lema(ur'Sajcabaj_á__a') + #0
#lema(ur'Sud_á_n\]\]_a', pre=ur'\[\[') + #0
#lema(ur'T_á_riba_a') + #0
#lema(ur'Taf_í_ del Valle_i') + #0
#lema(ur'[Aa]_ _punto_', pre=ur'[Ee]st(?:a(?:[ns]|ba[ns]?|)|uvo)') + #0
#lema(ur'[Aa]_m_parar_n') + #0
#lema(ur'[Aa]_m_paro_n') + #0
#lema(ur'[Aa]_s_cendencias?_') + #0
#lema(ur'[Aa]bandonar_í_a[ns]?_i') + #0
#lema(ur'[Aa]barcar_í_a[ns]?_i') + #0
#lema(ur'[Aa]bstra_í_(?:a[ns]?|d[ao]s?)_i') + #0
#lema(ur'[Aa]c__ompañará_c') + #0
#lema(ur'[Aa]cab_a_rá_') + #0
#lema(ur'[Aa]celerar_í_a[ns]?_i') + #0
#lema(ur'[Aa]cent_ú_(?:a[ns]?|e[ns]?)_u') + #0
#lema(ur'[Aa]ceptar_í_a[ns]?_i') + #0
#lema(ur'[Aa]cercar_s_e(?:lo|)_c') + #0
#lema(ur'[Aa]consejar_í_a[ns]?_i') + #0
#lema(ur'[Aa]copl_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Aa]cudir_á_[ns]?_a') + #0
#lema(ur'[Aa]cusar_í_a[ns]?_i') + #0
#lema(ur'[Aa]dmit_í__i') + #0
#lema(ur'[Aa]dmitir_á_[ns]?_a') + #0
#lema(ur'[Aa]doptar_í_a[ns]?_i') + #0
#lema(ur'[Aa]dquir_í_a[ns]?_i') + #0
#lema(ur'[Aa]dvi__rti(?:endo|eron|éndole|éndoles|éndose|ó)_e') + #0
#lema(ur'[Aa]fectar_í_a[ns]?_i') + #0
#lema(ur'[Aa]firmar_í_a[ns]?_i') + #0
#lema(ur'[Aa]gotar_í_a[ns]?_i') + #0
#lema(ur'[Aa]griar_í_a[ns]?_i') + #0
#lema(ur'[Aa]justad_í_sim[ao]s?_i') + #0
#lema(ur'[Aa]lcanzar_í_a[ns]?_i') + #0
#lema(ur'[Aa]lejar_í_a[ns]?_i') + #0
#lema(ur'[Aa]lertar_í_a[ns]?_i') + #0
#lema(ur'[Aa]lgor_í_tmicas?_i') + #0
#lema(ur'[Aa]liar_s_e_z') + #0
#lema(ur'[Aa]lt_í_sim[ao]s?_i') + #0
#lema(ur'[Aa]mabil_í_sim[ao]s?_i') + #0
#lema(ur'[Aa]mad_í_sim[ao]s?_i') + #0
#lema(ur'[Aa]maz_ó_nica_o', pre=ur'(?:apariencia|especie|[Ss]elva|tribu|Lengua|medicinal|Cuenca|Guayaba|[Rr]egi[oó]n|cultural|dulce..|Colombia..| y) ') + #0
#lema(ur'[Aa]mpl_í_sim[ao]s?_i') + #0
#lema(ur'[Aa]nexar_í_a[ns]?_i') + #0
#lema(ur'[Aa]nexion_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Aa]ntiqu_í_sim[ao]s?_i') + #0
#lema(ur'[Aa]ntropom_ó_rfic[ao]s?_o') + #0
#lema(ur'[Aa]pagar_í_a[ns]?_i') + #0
#lema(ur'[Aa]pare_z_ca[ns]?_s') + #0
#lema(ur'[Aa]parec_é_r[mts]el[aeo]s?_e') + #0
#lema(ur'[Aa]poderar_s_e(?:lo|)_c') + #0
#lema(ur'[Aa]poderar_í_a[ns]?_i') + #0
#lema(ur'[Aa]poyar_í_a[ns]?_i') + #0
#lema(ur'[Aa]prehend_í_a[ns]?_i') + #0
#lema(ur'[Aa]prend_í_a[ns]?_i') + #0
#lema(ur'[Aa]prender_á_[ns]?_a') + #0
#lema(ur'[Aa]rist_ó_cratas?_o') + #0
#lema(ur'[Aa]rrebat_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Aa]rremet_í_a[ns]?_i') + #0
#lema(ur'[Aa]rruinar_í_a[ns]?_i') + #0
#lema(ur'[Aa]rt_í_sticamente_i') + #0
#lema(ur'[Aa]sar_í_as?_i') + #0
#lema(ur'[Aa]sc_ó_rbic[ao]s?_o') + #0
#lema(ur'[Aa]scender_á_[ns]?_a') + #0
#lema(ur'[Aa]segurar_í_a[ns]?_i') + #0
#lema(ur'[Aa]sesinar_í_a[ns]?_i') + #0
#lema(ur'[Aa]sis__tió_i') + #0
#lema(ur'[Aa]sistir_á_[ns]?_a') + #0
#lema(ur'[Aa]sumir_á_[ns]?_a') + #0
#lema(ur'[Aa]tender_á_[ns]?_a') + #0
#lema(ur'[Aa]terrar_í_a[ns]?_i') + #0
#lema(ur'[Aa]trap_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Aa]u_té_ntic[ao]s?_nte') + #0
#lema(ur'[Aa]udicionar_í_a[ns]?_i') + #0
#lema(ur'[Aa]ut_ó_dromos_o') + #0
#lema(ur'[Aa]uto_o_xida(?:ción|ciones|ntes?)_') + #0
#lema(ur'[Aa]van_z_(?:ando|ad[ao]s?|[aoó])_s') + #0
#lema(ur'[Aa]verg_ü_enza[ns]?_u') + #0
#lema(ur'[Aa]yudar_í_a[ns]?_i') + #0
#lema(ur'[Aa]ñad_í__i') + #0
#lema(ur'[Aa]ñadir_á_[ns]?_a') + #0
#lema(ur'[Bb]_ri_tánic[ao]s?_ir') + #0
#lema(ur'[Bb]aj_í_sim[ao]s?_i') + #0
#lema(ur'[Bb]astar_í_a[ns]?_i') + #0
#lema(ur'[Bb]endec_í_a[ns]?_i') + #0
#lema(ur'[Bb]ibliograf_í_as_i') + #0
#lema(ur'[Bb]iopol_í_tix[ao]s?_i') + #0
#lema(ur'[Bb]lanqu_í_sim[ao]s?_i') + #0
#lema(ur'[Bb]rindar_í_a[ns]?_i') + #0
#lema(ur'[Bb]urlar_í_a[ns]?_i') + #0
#lema(ur'[Bb]uscar_í_a[ns]?_i') + #0
#lema(ur'[Bb]utanodi_ó_lic[ao]s?_o') + #0
#lema(ur'[Cc]_á_lculo_a', pre=ur'(?:[Ee]l|[Uu]n|[Dd]el?|[Aa]l|y)') + #0
#lema(ur'[Cc]_ó_nic(?:as|os?)_o') + #0
#lema(ur'[Cc]a_y_endo_ll') + #0
#lema(ur'[Cc]a_é_r[mts]el[aeo]s?_e') + #0
#lema(ur'[Cc]acer_í_as?_i') + #0
#lema(ur'[Cc]almar_í_a[ns]_i') + #0
#lema(ur'[Cc]am_é_lid[ao]s?_e') + #0
#lema(ur'[Cc]ambiar_í_a_i', pre=ur'(?:[Nn]o|[Ll][ao]) ') + #0
#lema(ur'[Cc]ambiar_í_an_i') + #0
#lema(ur'[Cc]anadi_e_nse_é') + #0
#lema(ur'[Cc]ant_one_s_óne') + #0
#lema(ur'[Cc]aracter_í_stc[ao]s?_i') + #0
#lema(ur'[Cc]aracteri_z_(?:a[nrs]?|d[ao]s?|[oó])_s') + #0
#lema(ur'[Cc]asar_s_e(?:lo|)_c') + #0
#lema(ur'[Cc]atapultar_í_a[ns]?_i') + #0
#lema(ur'[Cc]atastr_ó_fic(?:[ao]s?|amente)_o') + #0
#lema(ur'[Cc]ausar_í_a[ns]?_i') + #0
#lema(ur'[Cc]e_ntroamé_rica_troam[eé]') + #0
#lema(ur'[Cc]entrar_í_a[ns]?_i') + #0
#lema(ur'[Cc]hurrasquer_í_as?_i') + #0
#lema(ur'[Cc]ircu_n_stacias_') + #0
#lema(ur'[Cc]ircu_n_stancia(?:l|les|)_') + #0
#lema(ur'[Cc]ircun_s_pección_') + #0
#lema(ur'[Cc]ircun_s_tancias?_') + #0
#lema(ur'[Cc]iudad__es_d') + #0
#lema(ur'[Cc]o_m_parte_n') + #0
#lema(ur'[Cc]o_m_patriotas_n') + #0
#lema(ur'[Cc]o_m_positor_n') + #0
#lema(ur'[Cc]o_m_puesta_n') + #0
#lema(ur'[Cc]o_m_puesto_n') + #0
#lema(ur'[Cc]o_m_puso_n') + #0
#lema(ur'[Cc]o_nvirtió__virtio') + #0
#lema(ur'[Cc]octeler_í_as?_i') + #0
#lema(ur'[Cc]oincidir_á_[ns]?_a') + #0
#lema(ur'[Cc]ol_a_boración_o') + #0
#lema(ur'[Cc]ol_a_borador_o') + #0
#lema(ur'[Cc]ol_é_ric[ao]s?_e') + #0
#lema(ur'[Cc]olaborar_í_a[ns]?_i') + #0
#lema(ur'[Cc]olor___ color', xpos=[ur'\'\'']) + #0
#lema(ur'[Cc]om_é_r[mts]el[aeo]s?_e') + #0
#lema(ur'[Cc]ombatir_á_[ns]?_a') + #0
#lema(ur'[Cc]oment_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Cc]ompartir_á_[ns]?_a') + #0
#lema(ur'[Cc]ompeti_ci_ones_') + #0
#lema(ur'[Cc]ompeti_ci_ón_') + #0
#lema(ur'[Cc]ompetic_i_ón_í?') + #0
#lema(ur'[Cc]ompeticio_ne_s_en') + #0
#lema(ur'[Cc]ompetir_á_n?_a') + #0
#lema(ur'[Cc]ompetir_í_a[ns]?_i') + #0
#lema(ur'[Cc]omplic_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Cc]ompo_s_itor(?:as?|es|)_c') + #0
#lema(ur'[Cc]omposi_c_ión_s') + #0
#lema(ur'[Cc]omprender_á_[ns]?_a') + #0
#lema(ur'[Cc]omunic_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Cc]on __el_el con ') + #0
#lema(ur'[Cc]on_cedié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_sedie') + #0
#lema(ur'[Cc]on_s_ecuencias?_c') + #0
#lema(ur'[Cc]on_s_iderad[ao]s?_c') + #0
#lema(ur'[Cc]onceb_í_a[ns]?_i') + #0
#lema(ur'[Cc]onced_é_r[mts]el[aeo]s?_e') + #0
#lema(ur'[Cc]onced_í_a[ns]?_i') + #0
#lema(ur'[Cc]onceder_á_[ns]?_a') + #0
#lema(ur'[Cc]oncluir_á_[ns]?_a') + #0
#lema(ur'[Cc]oncurr(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Cc]oncurrir_á_[ns]?_a') + #0
#lema(ur'[Cc]ondu_jo__cio') + #0
#lema(ur'[Cc]onduc_í_a[ns]?_i') + #0
#lema(ur'[Cc]onducir_á_[ns]?_a') + #0
#lema(ur'[Cc]onf_í_e[ns]_i') + #0
#lema(ur'[Cc]onf_í_o_i', pre=ur'(?:[Tt]i|[Vv]os) ') + #0
#lema(ur'[Cc]onfia_n_zas?_') + #0
#lema(ur'[Cc]onfie_s_a[ns]?_z') + #0
#lema(ur'[Cc]onformar_í_a[ns]?_i') + #0
#lema(ur'[Cc]onocer_s_e(?:lo|)_c') + #0
#lema(ur'[Cc]onoci_éndos_e_endoc') + #0
#lema(ur'[Cc]onocim_ie_ntos?_ei') + #0
#lema(ur'[Cc]ons_iguió__eguio') + #0
#lema(ur'[Cc]ons_titui_d[ao]s?_ituí') + #0
#lema(ur'[Cc]onsecu_e_ncias?_a') + #0
#lema(ur'[Cc]onsig_uió__i[oó]') + #0
#lema(ur'[Cc]onsistir_á_[ns]?_a') + #0
#lema(ur'[Cc]onsolidar_í_a[ns]?_i') + #0
#lema(ur'[Cc]onst_itui_d[ao]s?_rituí') + #0
#lema(ur'[Cc]onst_itui_d[ao]s?_uí') + #0
#lema(ur'[Cc]onst_r_uye[ns]?_') + #0
#lema(ur'[Cc]onstituir_á_[ns]?_a') + #0
#lema(ur'[Cc]onstru_í_as?_i') + #0
#lema(ur'[Cc]ont_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Cc]ontactar_í_a[ns]?_i') + #0
#lema(ur'[Cc]ontar_í_a[ns]?_i') + #0
#lema(ur'[Cc]ontend_í_(?:a[ns]?|)_i') + #0
#lema(ur'[Cc]onteni_en_do_ne') + #0
#lema(ur'[Cc]ontestar_í_a[ns]?_i') + #0
#lema(ur'[Cc]ontinuar_í_a[ns]?_i') + #0
#lema(ur'[Cc]ontrar_restará__estara') + #0
#lema(ur'[Cc]ontribu_i_r(?:l[aeo]s?|se|)_í') + #0
#lema(ur'[Cc]ontribuir_á_[ns]?_a') + #0
#lema(ur'[Cc]onv_erti_rían_ierte') + #0
#lema(ur'[Cc]onven_c_er(?:se|l[ao]s?|[mt]e|nos|á[ns]?)_s') + #0
#lema(ur'[Cc]onvencer_á_[ns]?_a') + #0
#lema(ur'[Cc]onvi_r_tieron_') + #0
#lema(ur'[Cc]onvi_rtió__ertio') + #0
#lema(ur'[Cc]onvi_rtió__erto', pre=ur'[Ss]e ') + #0
#lema(ur'[Cc]onvir_tió__itio') + #0
#lema(ur'[Cc]onvirti_éndos_e_endoc') + #0
#lema(ur'[Cc]ooperar_í_a[ns]?_i') + #0
#lema(ur'[Cc]or_respondí_a_espondi') + #0
#lema(ur'[Cc]oronar_s_e(?:lo|)_c') + #0
#lema(ur'[Cc]orre_spondí_a_pondi') + #0
#lema(ur'[Cc]orrer_í_a[ns]?_i') + #0
#lema(ur'[Cc]orresponder_á_[ns]?_a') + #0
#lema(ur'[Cc]orresponder_í_a[ns]?_i') + #0
#lema(ur'[Cc]r_i_men_') + #0
#lema(ur'[Cc]rear_í_a[ns]?_i') + #0
#lema(ur'[Cc]recer_á_[ns]?_a') + #0
#lema(ur'[Cc]u[aá]_nd_o_dn') + #0
#lema(ur'[Cc]u_m_pliéndose_n') + #0
#lema(ur'[Cc]ua_d_rad[ao]s?_') + #0
#lema(ur'[Cc]ua_n_do (?:se|ven?|el|es|eran?|fue|llegan?|hay|el|la|sale|sus?|este)_') + #0
#lema(ur'[Cc]uadrag_é_sim[ao]s?_e') + #0
#lema(ur'[Cc]ubi_e_rt[ao]s?_') + #0
#lema(ur'[Cc]ubrir_á_[ns]?_a') + #0
#lema(ur'[Cc]ulpar_í_a[ns]?_i') + #0
#lema(ur'[Cc]ultivar_í_a[ns]?_i') + #0
#lema(ur'[Dd]]_ú_os_u') + #0
#lema(ur'[Dd]__onde_onde d') + #0
#lema(ur'[Dd]_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Dd]añar_í_a[ns]?_i') + #0
#lema(ur'[Dd]e_ _pronto_') + #0
#lema(ur'[Dd]e_s_cifrar_') + #0
#lema(ur'[Dd]ebat(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Dd]ebatir_á_[ns]?_a') + #0
#lema(ur'[Dd]ebilitad_í_sim[ao]s?_i') + #0
#lema(ur'[Dd]ec_í_amos_i') + #0
#lema(ur'[Dd]eca_í_do_i') + #0
#lema(ur'[Dd]ecidir_á_[ns]?_a') + #0
#lema(ur'[Dd]ecimos_é_ptimo_e') + #0
#lema(ur'[Dd]eclarar_í_a[ns]?_i') + #0
#lema(ur'[Dd]edic_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Dd]educir_á__a') + #0
#lema(ur'[Dd]ef__endió_i') + #0
#lema(ur'[Dd]efinir_á_[ns]?_a') + #0
#lema(ur'[Dd]egenerar_í_a[ns]_i') + #0
#lema(ur'[Dd]ej_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Dd]em_ócra_tas?_[oó]cr') + #0
#lema(ur'[Dd]emandar_í_a[ns]?_i') + #0
#lema(ur'[Dd]emost_r_ar(?:le|on|se|)_') + #0
#lema(ur'[Dd]enominar_í_a[ns]?_i') + #0
#lema(ur'[Dd]epender_á_[ns]?_a') + #0
#lema(ur'[Dd]errumbar_í_a[ns]?_i') + #0
#lema(ur'[Dd]es_é_rtic[ao]s?_e') + #0
#lema(ur'[Dd]esaf_i_ar_í') + #0
#lema(ur'[Dd]esap_are_r(?:e(?:[ns]?|r(?:a[ns]?|[áé]|ía[ns]?|))|ieron)c_(?:ara|re)') + #0
#lema(ur'[Dd]esapare_z_ca[ns]?_s') + #0
#lema(ur'[Dd]esaparecer_á_[ns]?_a') + #0
#lema(ur'[Dd]esaperci_b_id[ao]s?_v') + #0
#lema(ur'[Dd]esastro_s_[ao]s?_z') + #0
#lema(ur'[Dd]escan_s_(?:os?|ar)_z') + #0
#lema(ur'[Dd]escender_á_[ns]?_a') + #0
#lema(ur'[Dd]escrib(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Dd]escrib_í__i') + #0
#lema(ur'[Dd]escub__rir_i') + #0
#lema(ur'[Dd]escub_r_ieron_') + #0
#lema(ur'[Dd]escub_ri_eron_ir') + #0
#lema(ur'[Dd]escub_ri_r_ir') + #0
#lema(ur'[Dd]ese_m_peñarlos_n') + #0
#lema(ur'[Dd]esear_í_a[ns]?_i') + #0
#lema(ur'[Dd]eshacer_s_e(?:lo|)_c') + #0
#lema(ur'[Dd]esp_i_dió_e') + #0
#lema(ur'[Dd]estacad_í_sim[ao]s?_i') + #0
#lema(ur'[Dd]estapar_í_a[ns]?_i') + #0
#lema(ur'[Dd]estinar_í_a[ns]?_i') + #0
#lema(ur'[Dd]estru_í__i') + #0
#lema(ur'[Dd]estruir_á_[ns]?_a') + #0
#lema(ur'[Dd]esverg_ü_enza[ns]?_u') + #0
#lema(ur'[Dd]evolver_á_[ns]?_a') + #0
#lema(ur'[Dd]evorar_í_a[ns]?_i') + #0
#lema(ur'[Dd]i_scí_pul[ao]s?_ci') + #0
#lema(ur'[Dd]i_sminui_d[ao]s?_minuí') + #0
#lema(ur'[Dd]i_é_ramos_e') + #0
#lema(ur'[Dd]ibujar_í_a[ns]?_i') + #0
#lema(ur'[Dd]iet_é_tic[ao]s?_e') + #0
#lema(ur'[Dd]ifer_í_a[ns]?_i') + #0
#lema(ur'[Dd]ign_í_sim[ao]s?_i') + #0
#lema(ur'[Dd]ir_e_ctamente_é') + #0
#lema(ur'[Dd]ir_í_amos_i') + #0
#lema(ur'[Dd]irig_id_o por_') + #0
#lema(ur'[Dd]iscut(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Dd]isfra_c_es_z') + #0
#lema(ur'[Dd]isfrutar_í_a[ns]?_i') + #0
#lema(ur'[Dd]isminu_i_r(?:l[aeo]s?|se|)_í') + #0
#lema(ur'[Dd]isminuir_á_[ns]?_a') + #0
#lema(ur'[Dd]isparar_í_a[ns]?_i') + #0
#lema(ur'[Dd]ispondr_á_[ns]?_a') + #0
#lema(ur'[Dd]isputad_í_sim[ao]s?_i') + #0
#lema(ur'[Dd]isten_s_ión_c') + #0
#lema(ur'[Dd]istinguir_á_[ns]?_a') + #0
#lema(ur'[Dd]istribu_í_a[ns]?_i') + #0
#lema(ur'[Dd]istribuir_á_[ns]?_a') + #0
#lema(ur'[Dd]isuad(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Dd]ivi_sio_n_ci[oó]') + #0
#lema(ur'[Dd]ividir_á_[ns]?_a') + #0
#lema(ur'[Dd]ividir_í_a[ns]?_i') + #0
#lema(ur'[Dd]ivorciar_s_e(?:lo|)_c') + #0
#lema(ur'[Dd]onar_í_an_i') + #0
#lema(ur'[Ee]_m_parejado_n') + #0
#lema(ur'[Ee]_m_parentado_n') + #0
#lema(ur'[Ee]_m_pieza_n') + #0
#lema(ur'[Ee]_nvolverá_[ns]?_(?:mbolver[aá]|nbolver[aá]|nvolvera)') + #0
#lema(ur'[Ee]_s_culturas?_') + #0
#lema(ur'[Ee]_x_celencias?_s?') + #0
#lema(ur'[Ee]char_í_a[ns]?_i') + #0
#lema(ur'[Ee]conom_é_tric(?:as|os?)_e') + #0
#lema(ur'[Ee]fectuar_í_a[ns]?_i') + #0
#lema(ur'[Ee]fica_c_es_s') + #0
#lema(ur'[Ee]fica_z__s') + #0
#lema(ur'[Ee]g_ó_latras?_o') + #0
#lema(ur'[Ee]goc_é_ntric[ao]s?_e') + #0
#lema(ur'[Ee]jercer_á_[ns]?_a') + #0
#lema(ur'[Ee]l_i_minad[ao]s?_') + #0
#lema(ur'[Ee]levad_í_sim[ao]s?_i') + #0
#lema(ur'[Ee]lud(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Ee]m_blemá_tic[ao]s?_plem[aá]') + #0
#lema(ur'[Ee]mpe_zarí_a[ns]?_sari') + #0
#lema(ur'[Ee]mpie_z_a[ns]?_s') + #0
#lema(ur'[Ee]mprend_í_a[ns]?_i') + #0
#lema(ur'[Ee]mprender_á_[ns]?_a') + #0
#lema(ur'[Ee]n_ó_log[ao]s?_o') + #0
#lema(ur'[Ee]namorad_í_sim[ao]s?_i') + #0
#lema(ur'[Ee]ncantar_í_a[ns]?_i') + #0
#lema(ur'[Ee]ncargar_í_a[ns]?_i') + #0
#lema(ur'[Ee]ncender_á_[ns]?_a') + #0
#lema(ur'[Ee]ncubr(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Ee]nfrentar_s_e(?:lo|)_c') + #0
#lema(ur'[Ee]ngre_í_d[ao]s?_i') + #0
#lema(ur'[Ee]nlazar_s_e(?:lo|)_c') + #0
#lema(ur'[Ee]nlistar_í_a[ns]?_i') + #0
#lema(ur'[Ee]nojad_í_sim[ao]s?_i') + #0
#lema(ur'[Ee]nseñ_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Ee]ntender_á_[ns]?_a') + #0
#lema(ur'[Ee]ntr_e_ (?:l[ao]s|otros)_é') + #0
#lema(ur'[Ee]ntr_e_gad[ao]s?_a') + #0
#lema(ur'[Ee]ntrar_í_a[ns]?_i') + #0
#lema(ur'[Ee]ntreg_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Ee]ntregar_í_a[ns]?_i') + #0
#lema(ur'[Ee]nvi_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Ee]scalar_í_a[ns]?_i') + #0
#lema(ur'[Ee]scas_í_sim[ao]s?_i') + #0
#lema(ur'[Ee]sco_j_a[ns]?_g') + #0
#lema(ur'[Ee]scoger_á_[ns]?_a') + #0
#lema(ur'[Ee]scribir_á_[ns]?_a') + #0
#lema(ur'[Ee]scribir_á_[ns]?_a') + #0
#lema(ur'[Ee]spec_í_fica_i', pre=ur'(?:[Ee]s|[Mm][aá]s) ') + #0
#lema(ur'[Ee]specular_í_a[ns]?_i') + #0
#lema(ur'[Ee]spor_á_dic[ao]_a') + #0
#lema(ur'[Ee]st_á dividid_a_a divid') + #0
#lema(ur'[Ee]stablecer_s_e(?:lo|)_c') + #0
#lema(ur'[Ee]statu_i_d[Ao]s?_í') + #0
#lema(ur'[Ee]stuv_o__ó') + #0
#lema(ur'[Ee]timol_ó_gic(?:[ao]s|amente)_o') + #0
#lema(ur'[Ee]vitar_í_a[ns]?_i') + #0
#lema(ur'[Ee]xclu_i_r(?:l[aeo]s?|se|)_í') + #0
#lema(ur'[Ee]xig_í_a[ns]?_i') + #0
#lema(ur'[Ee]xig_í_r[mts]el[aeo]s?_i') + #0
#lema(ur'[Ee]xistir_á_[ns]?_a') + #0
#lema(ur'[Ee]xitos_í_sim[ao]s?_i') + #0
#lema(ur'[Ee]xpand(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Ee]xplorar_í_a[ns]?_i') + #0
#lema(ur'[Ee]xtender_á_[ns]?_a') + #0
#lema(ur'[Ee]xtender_í_a[ns]?_i') + #0
#lema(ur'[Ee]xtens_í_sim[ao]s?_i') + #0
#lema(ur'[Ee]xtra_ñ_(?:[ao]s|amente)_n') + #0
#lema(ur'[Ee]xtrater_r_estres?_') + #0
#lema(ur'[Ee]xtru_i_d[ao]s?_í') + #0
#lema(ur'[Ff]_r_ustrad[ao]s?_') + #0
#lema(ur'[Ff]allar_í_a[ns]?_i') + #0
#lema(ur'[Ff]allecer_á_[ns]?_a') + #0
#lema(ur'[Ff]als_í_sim[ao]s?_i') + #0
#lema(ur'[Ff]amos_í_sim[ao]s?_i') + #0
#lema(ur'[Ff]avorecer_á_[ns]?_a') + #0
#lema(ur'[Ff]ijar_í_a[ns]?_i') + #0
#lema(ur'[Ff]ilmar_í_a[ns]?_i') + #0
#lema(ur'[Ff]ilud_í_sim[ao]s?_i') + #0
#lema(ur'[Ff]in_í_sim[ao]s?_i') + #0
#lema(ur'[Ff]ing_í_a[ns]?_i') + #0
#lema(ur'[Ff]lu_i_r(?:l[aeo]s?|se|)_í') + #0
#lema(ur'[Ff]ora_j_id[ao]s?_g') + #0
#lema(ur'[Ff]ort_í_sim[ao]s?_i') + #0
#lema(ur'[Ff]ot_ó_graf[ao]s?_') + #0
#lema(ur'[Ff]uer_o_n_ó') + #0
#lema(ur'[Ff]undar_í_a[ns]?_i') + #0
#lema(ur'[Ff]usionar_í_a[ns]?_i') + #0
#lema(ur'[Gg]_é_rmenes_e') + #0
#lema(ur'[Gg]an_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Gg]en_é_ric(?:[ao]s|amente)_e') + #0
#lema(ur'[Gg]en_é_ticamente(?! modificato)_e') + #0
#lema(ur'[Gg]enial_í_sim[ao]s?_i') + #0
#lema(ur'[Gg]erontolog_í_as?_i') + #0
#lema(ur'[Gg]olear_í_a[ns]?_i') + #0
#lema(ur'[Gg]raduar_s_e(?:lo|)_c') + #0
#lema(ur'[Gg]rav_í_sim[ao]s?_i') + #0
#lema(ur'[Gg]uap_í_sim[ao]s?_i') + #0
#lema(ur'[Hh]_á_bil_a', pre=ur'(?:[Ee]s|[Ee]ra|[Ff]ue) ') + #0
#lema(ur'[Hh]ab_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #0
#lema(ur'[Hh]aber_s_e(?:lo|)_c') + #0
#lema(ur'[Hh]ablar_í_a[ns]?_i') + #0
#lema(ur'[Hh]ac_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #0
#lema(ur'[Hh]allar_í_a(?:[ns]?|mos)_i') + #0
#lema(ur'[Hh]ialur_ó_nic[ao]s?_o') + #0
#lema(ur'[Hh]ic_i_eron_') + #0
#lema(ur'[Hh]ipn_ó_tic[ao]s?_o') + #0
#lema(ur'[Hh]ispa_noamé_rica_(?:noam|oamé|ñoamé)') + #0
#lema(ur'[Hh]oland_e_s[ae]s_é') + #0
#lema(ur'[Hh]onr__os[ao]s?_r') + #0
#lema(ur'[Hh]umor_í_stic[ao]_i') + #0
#lema(ur'[Hh]umor_í_stic[ao]s?_') + #0
#lema(ur'[Hh]und(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Hh]urac_a_nes_á') + #0
#lema(ur'[Ii]_m_pacto_n') + #0
#lema(ur'[Ii]_m_perceptible_n') + #0
#lema(ur'[Ii]_m_perfecto_n') + #0
#lema(ur'[Ii]_m_plantación_n') + #0
#lema(ur'[Ii]_m_plementaron_n') + #0
#lema(ur'[Ii]_m_plica_n') + #0
#lema(ur'[Ii]_m_popular_n') + #0
#lema(ur'[Ii]_m_popularidad_n') + #0
#lema(ur'[Ii]_m_portantes_n') + #0
#lema(ur'[Ii]_m_prescindible_n') + #0
#lema(ur'[Ii]_m_previsto_n') + #0
#lema(ur'[Ii]_m_pulsó_n') + #0
#lema(ur'[Ii]_nclui_d[ao]s?_cluí') + #0
#lema(ur'[Ii]diom_á_tic[ao]s?_') + #0
#lema(ur'[Ii]gualar_í_a[ns]?_i') + #0
#lema(ur'[Ii]mp_idié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_edie') + #0
#lema(ur'[Ii]mpedir_á_[ns]?_a') + #0
#lema(ur'[Ii]mplicar_í_a[ns]?_i') + #0
#lema(ur'[Ii]mpondr_á_[ns]?_a') + #0
#lema(ur'[Ii]mportant_í_sim[ao]s?_i') + #0
#lema(ur'[Ii]mportar_í_a[ns]?_i') + #0
#lema(ur'[Ii]mprim(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Ii]mprimir_á_[ns]?_a') + #0
#lema(ur'[Ii]n_s_pector_') + #0
#lema(ur'[Ii]n_s_pirado_') + #0
#lema(ur'[Ii]n_s_tancias?_') + #0
#lema(ur'[Ii]n_struccio_nes_s?trucció') + #0
#lema(ur'[Ii]ncendiar_í_an_i') + #0
#lema(ur'[Ii]nclu_i_r_í') + #0
#lema(ur'[Ii]nclu_i_ría[ns]?_í') + #0
#lema(ur'[Ii]nclu_irá_[ns]?_íra') + #0
#lema(ur'[Ii]nclu_irí_a[ns]?_íri') + #0
#lema(ur'[Ii]ncluir_í_a[ns]?_i') + #0
#lema(ur'[Ii]ncorporar_s_e(?:lo|)_c') + #0
#lema(ur'[Ii]ncrementar_í_a[ns]?_i') + #0
#lema(ur'[Ii]ndicar_í_a[ns]_i') + #0
#lema(ur'[Ii]ndivid_u_os_') + #0
#lema(ur'[Ii]nflu_i_r(?:l[aeo]s?|se|)_í') + #0
#lema(ur'[Ii]nfluir_á_[ns]?_a') + #0
#lema(ur'[Ii]nfrac_c_ión_') + #0
#lema(ur'[Ii]nmiscu_i_d[ao]s?_í') + #0
#lema(ur'[Ii]nscrib(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Ii]nsect_ó_log[ao]s?_o') + #0
#lema(ur'[Ii]nsinu_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Ii]nsist(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Ii]nspirad_í_sim[ao]s?_i') + #0
#lema(ur'[Ii]nspirar_í_a[ns]?_i') + #0
#lema(ur'[Ii]nstalar_í_a[ns]?_i') + #0
#lema(ur'[Ii]nstitu_i_r(?:l[aeo]s?|se|)_í') + #0
#lema(ur'[Ii]nte__grad[ao]s?_n') + #0
#lema(ur'[Ii]nte_r_pret[oó]_') + #0
#lema(ur'[Ii]nte_r_pretaba[ns]?_') + #0
#lema(ur'[Ii]nte_r_pretaciones_') + #0
#lema(ur'[Ii]nteligent_í_sim[ao]s?_i') + #0
#lema(ur'[Ii]nteresar_í_a[ns]?_i') + #0
#lema(ur'[Ii]nterrump(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Ii]ntervendr_á_[ns]?_a') + #0
#lema(ur'[Ii]ntroducir_á_[ns]?_a') + #0
#lema(ur'[Ii]ntu_i_d[ao]s?_í') + #0
#lema(ur'[Ii]nvestigaci_ón|investigaciones]]__[óo]n\]\]es') + #0
#lema(ur'[Jj]ovenc_í_sim[ao]s?_i') + #0
#lema(ur'[Jj]ueg_u_e[ns]?_') + #0
#lema(ur'[Jj]ug_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Ll]a_ _misma_') + #0
#lema(ur'[Ll]a_s_ [aá]reas_') + #0
#lema(ur'[Ll]a_s_ caracter[ií]sticas_') + #0
#lema(ur'[Ll]a_s_ cercanías_') + #0
#lema(ur'[Ll]a_s_ compañ[ií]as_') + #0
#lema(ur'[Ll]a_s_ comunidades_') + #0
#lema(ur'[Ll]a_s_ distintas_') + #0
#lema(ur'[Ll]a_s_ im[aá]genes_') + #0
#lema(ur'[Ll]a_s_ industrias_') + #0
#lema(ur'[Ll]a_s_ minas_') + #0
#lema(ur'[Ll]a_s_ pel[ií]culas_') + #0
#lema(ur'[Ll]a_s_ teor[ií]as_') + #0
#lema(ur'[Ll]am_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_bie') + #0
#lema(ur'[Ll]argu_í_sim[ao]s?_i') + #0
#lema(ur'[Ll]as [uú]ltima_s__') + #0
#lema(ur'[Ll]evar_í_a[ns]?_i') + #0
#lema(ur'[Ll]iger_í_sim[ao]s?_i') + #0
#lema(ur'[Ll]lamar_s_e(?:lo|)_c') + #0
#lema(ur'[Ll]len_í_sim[ao]s?_i') + #0
#lema(ur'[Ll]lenar_í_a[ns]?_i') + #0
#lema(ur'[Ll]lev_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Ll]ocalizar_s_e(?:lo|)_c') + #0
#lema(ur'[Ll]ogar_í_tmic[ao]s?_i') + #0
#lema(ur'[Ll]uchar_í_a[ns]?_i') + #0
#lema(ur'[Mm]_í_nimamente_i') + #0
#lema(ur'[Mm]a_m_posteados_n') + #0
#lema(ur'[Mm]acrosc_ó_pic[ao]s?_o') + #0
#lema(ur'[Mm]al_í_sim[ao]s?_i') + #0
#lema(ur'[Mm]and_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Mm]anejar_í_a[ns]?_i') + #0
#lema(ur'[Mm]anten_é_r[mts]el[aeo]s?_e') + #0
#lema(ur'[Mm]archar_í_a[ns]?_i') + #0
#lema(ur'[Mm]e_n_sajes?_') + #0
#lema(ur'[Mm]edir_á_[ns]?_a') + #0
#lema(ur'[Mm]egafon_í_as?_i') + #0
#lema(ur'[Mm]elodram_á_tic[ao]s?_a') + #0
#lema(ur'[Mm]ere_ció__scio') + #0
#lema(ur'[Mm]exican_í_sim[ao]s?_i') + #0
#lema(ur'[Mm]ezclar_í_a[ns]?_i') + #0
#lema(ur'[Mm]inusv_á_lid[ao]s?_a') + #0
#lema(ur'[Mm]o_n_struos?_') + #0
#lema(ur'[Mm]onol_í_tic[ao]s?_i') + #0
#lema(ur'[Mm]u_n_icipios?__') + #0
#lema(ur'[Mm]uri_á_tic[ao]s?_a') + #0
#lema(ur'[Nn]acional_ de_ Yosemite\]\]_') + #0
#lema(ur'[Nn]eg_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Nn]egoc_i_aci(?:ón|ones)_') + #0
#lema(ur'[Nn]iv_e_l(?:es|)_é') + #0
#lema(ur'[Nn]oqu_eó__io') + #0
#lema(ur'[Nn]otar_í_an_i') + #0
#lema(ur'[Nn]uest_r_o_') + #0
#lema(ur'[Oo]_b_tenido_p') + #0
#lema(ur'[Oo]bstru_i_r(?:l[aeo]s?|se|)_í') + #0
#lema(ur'[Oo]casionar_í_a[ns]?_i') + #0
#lema(ur'[Oo]curr(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Oo]curr_í_a[ns]?_i') + #0
#lema(ur'[Oo]dontol_ó_gic[ao]s?_o') + #0
#lema(ur'[Oo]ptar_í_a[ns]?_i') + #0
#lema(ur'[Oo]rgani_z_ad[ao]s?_s') + #0
#lema(ur'[Oo]rganizar_s_e(?:lo|)_c') + #0
#lema(ur'[Oo]riginal_í_sim[ao]s?_i') + #0
#lema(ur'[Oo]torg_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Pp]acient_í_sim[ao]s?_i') + #0
#lema(ur'[Pp]agar_í_a[ns]?_i') + #0
#lema(ur'[Pp]arecer_s_e(?:lo|)_c') + #0
#lema(ur'[Pp]arecer_á_[ns]?_a') + #0
#lema(ur'[Pp]arente_s_cos?_z') + #0
#lema(ur'[Pp]arlanch_í_n_i') + #0
#lema(ur'[Pp]as_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Pp]elear_s_e_z') + #0
#lema(ur'[Pp]ens_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Pp]er__iodista_d') + #0
#lema(ur'[Pp]er__iodo_d') + #0
#lema(ur'[Pp]er_imetró__(?:ímetr[oó]|imetro)', pre=ur'[Ss]e(?: me| te| l[aeo]s?|) ') + #0
#lema(ur'[Pp]ercib(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Pp]ercl_ó_ric[ao]s?_o') + #0
#lema(ur'[Pp]erdurar_í_a[ns]?_i') + #0
#lema(ur'[Pp]eri_ó_dic(?:as|amente)_o', pre=ur'\.edu') + #0
#lema(ur'[Pp]ermanec_í__i') + #0
#lema(ur'[Pp]ermanecer_í_a[ns]?_i') + #0
#lema(ur'[Pp]erseguir_á_[ns]?_a') + #0
#lema(ur'[Pp]ersist(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Pp]ersonal_í_sim[ao]s?_i') + #0
#lema(ur'[Pp]erten_ecerí_a_ceri') + #0
#lema(ur'[Pp]ertenecer_á_[ns]?_a') + #0
#lema(ur'[Pp]itar_í_a[ns]?_i') + #0
#lema(ur'[Pp]luric_é_ntric[ao]s?_e') + #0
#lema(ur'[Pp]neumatol_ó_gic[ao]s?_o') + #0
#lema(ur'[Pp]nuematolog_í_as?_i') + #0
#lema(ur'[Pp]odiatr_í_as?_i') + #0
#lema(ur'[Pp]ol_í_ticas_') + #0
#lema(ur'[Pp]olicl_í_nicas?_i') + #0
#lema(ur'[Pp]ondr_á_n_a') + #0
#lema(ur'[Pp]ondr_í_a(?:[ns]?|mos)_i') + #0
#lema(ur'[Pp]oner_s_e(?:lo|)_c') + #0
#lema(ur'[Pp]oni_en_do_ne') + #0
#lema(ur'[Pp]opular_í_sim[ao]s?_i') + #0
#lema(ur'[Pp]oqu_í_sim[ao]s?_i') + #0
#lema(ur'[Pp]oseer_á_[ns]?_a') + #0
#lema(ur'[Pp]osi__ción_si') + #0
#lema(ur'[Pp]osi_c_ionado_s') + #0
#lema(ur'[Pp]osi_c_ionó_s') + #0
#lema(ur'[Pp]osicionar_s_e(?:lo|)_c') + #0
#lema(ur'[Pp]reced_í_a[ns]?_i') + #0
#lema(ur'[Pp]refi__riendo_e') + #0
#lema(ur'[Pp]refi__rieron_e') + #0
#lema(ur'[Pp]refi__rió_e') + #0
#lema(ur'[Pp]rend_í_a[ns]?_i') + #0
#lema(ur'[Pp]reparar_s_e(?:lo|)_c') + #0
#lema(ur'[Pp]resent_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Pp]residir_á_[ns]?_a') + #0
#lema(ur'[Pp]residir_í_a[ns]?_i') + #0
#lema(ur'[Pp]restar_í_a[ns]?_i') + #0
#lema(ur'[Pp]revalecer_á_[ns]?_a') + #0
#lema(ur'[Pp]reve_í_a[ns]?_i') + #0
#lema(ur'[Pp]rimar_i_a_', pre=ur'(?:[Ee]scuelas?|formas?|[Ee]nseñanzas?|[Ee]ducación|[Ee]lecciones|[Ee]lección|[Aa]tención|Estudió) ') + #0
#lema(ur'[Pp]rimer_í_sim[ao]s?_i') + #0
#lema(ur'[Pp]rimi_c_ias?_s') + #0
#lema(ur'[Pp]ro_v_oca[ns]?_b') + #0
#lema(ur'[Pp]ro_v_ocando_b') + #0
#lema(ur'[Pp]ro_v_ocar_b') + #0
#lema(ur'[Pp]roceder_á_[ns]?_a') + #0
#lema(ur'[Pp]roclamar_í_a[ns]?_i') + #0
#lema(ur'[Pp]rodu_jo__ci[oó]') + #0
#lema(ur'[Pp]roducir_s_e(?:lo|)_c') + #0
#lema(ur'[Pp]roducir_á_[ns]?_a') + #0
#lema(ur'[Pp]rogramar_í_a[ns]?_i') + #0
#lema(ur'[Pp]romet_ié_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_íe') + #0
#lema(ur'[Pp]ropi_ó_nic[ao]s?_o') + #0
#lema(ur'[Pp]ropondr_á_[ns]?_a') + #0
#lema(ur'[Pp]rot_é_sic[ao]s?_e') + #0
#lema(ur'[Pp]roteger_á_[ns]?_a') + #0
#lema(ur'[Pp]rove_í_a[ns]?_i') + #0
#lema(ur'[Pp]royectar_í_a[ns]?_i') + #0
#lema(ur'[Pp]sicoanal_í_tic[ao]s?_i') + #0
#lema(ur'[Pp]ublicar_í_a[ns]?_i') + #0
#lema(ur'[Qq]u_eri_endo_ier') + #0
#lema(ur'[Qq]uedar_s_e(?:lo|)_c') + #0
#lema(ur'[Qq]uin_c_e(?:nal|nalmente)_[sz]') + #0
#lema(ur'[Qq]uincuag_é_sim[ao]s?_e') + #0
#lema(ur'[Qq]uis_o__ó') + #0
#lema(ur'[Rr]_é_plica_', pre=ur'(?:[Uu]na|1) ') + #0
#lema(ur'[Rr]adiofon_í_as?_i') + #0
#lema(ur'[Rr]apid_í_sim[ao]s?_i') + #0
#lema(ur'[Rr]e__levantes?_e') + #0
#lema(ur'[Rr]e_presá_ndo(?:(?:[mts]e|nos|se)(?:l[aeo]s?|)|l[aeo]s?)_gresa') + #0
#lema(ur'[Rr]e_s_pectiv[ao]s?_') + #0
#lema(ur'[Rr]eabrir_á_[ns]?_a') + #0
#lema(ur'[Rr]ealizar_s_e(?:lo|)_c') + #0
#lema(ur'[Rr]ealizar_í_a[ns]?_i') + #0
#lema(ur'[Rr]eanudar_s_e(?:lo|)_c') + #0
#lema(ur'[Rr]eap_are_c(?:e(?:[ns]?|r(?:a[ns]?|[áé]|ía[ns]?|))|ieron)_(?:ara|re)') + #0
#lema(ur'[Rr]eaparecer_á_[ns]?_a') + #0
#lema(ur'[Rr]earmar_í_a[ns]?_i') + #0
#lema(ur'[Rr]ecaudar_í_a[ns]?_i') + #0
#lema(ur'[Rr]ecibir_í_a[ns]?_i') + #0
#lema(ur'[Rr]ecoger_á_[ns]?_a') + #0
#lema(ur'[Rr]econ_s_truir(?:l[ao]s?|se)_') + #0
#lema(ur'[Rr]econciliar_s_e(?:lo|)_c') + #0
#lema(ur'[Rr]econocer_á_[ns]?_a') + #0
#lema(ur'[Rr]econocid_í_sim[ao]s?_i') + #0
#lema(ur'[Rr]econocim_ie_ntos?_ei') + #0
#lema(ur'[Rr]econstru_i_r(?:l[aeo]s?|se|)_í') + #0
#lema(ur'[Rr]econv_i_rtió_e') + #0
#lema(ur'[Rr]ecuperar_í_a[ns]?_i') + #0
#lema(ur'[Rr]ecurr(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Rr]ecurrir_á_[ns]?_a') + #0
#lema(ur'[Rr]edactar_í_a[ns]?_i') + #0
#lema(ur'[Rr]edistribu_i_d[ao]s?_í') + #0
#lema(ur'[Rr]educir_s_e(?:lo|)_c') + #0
#lema(ur'[Rr]eeditar_í_a[ns]?_i') + #0
#lema(ur'[Rr]eenv_í_a[ns]?_i') + #0
#lema(ur'[Rr]ef_e_rencias?_') + #0
#lema(ur'[Rr]eflejar_í_a[ns]?_i') + #0
#lema(ur'[Rr]efundar_í_a[ns]?_i') + #0
#lema(ur'[Rr]egir_á_[ns]?_a') + #0
#lema(ur'[Rr]egresar_í_a[ns]?_i') + #0
#lema(ur'[Rr]ei_m_preso_n') + #0
#lema(ur'[Rr]einventar_í_a[ns]?_i') + #0
#lema(ur'[Rr]ele_í_d[ao]s?_i') + #0
#lema(ur'[Rr]elocalizar_s_e(?:lo|)_c') + #0
#lema(ur'[Rr]enombrar_í_a[ns]?_i') + #0
#lema(ur'[Rr]enovar_í_a[ns]?_i') + #0
#lema(ur'[Rr]epetir_á_[ns]?_a') + #0
#lema(ur'[Rr]epresentar_í_a[ns]?_i') + #0
#lema(ur'[Rr]equerir_á_[ns]?_a') + #0
#lema(ur'[Rr]escind(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Rr]esguardar_í_a[ns]?_i') + #0
#lema(ur'[Rr]esidir_á_[ns]?_a') + #0
#lema(ur'[Rr]esist(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Rr]esistir_á_[ns]?_a') + #0
#lema(ur'[Rr]espaldar_í_a[ns]?_i') + #0
#lema(ur'[Rr]espetabil_í_sim[ao]s?_i') + #0
#lema(ur'[Rr]esponder_á_[ns]?_a') + #0
#lema(ur'[Rr]est_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Rr]estitu_i_r(?:l[aeo]s?|se|)_í') + #0
#lema(ur'[Rr]esum(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Rr]etir_á_r[mts]el[aeo]s?_a') + #0
#lema(ur'[Rr]etirar_s_e(?:lo|)_c') + #0
#lema(ur'[Rr]etirar_í_a[ns]?_i') + #0
#lema(ur'[Rr]etornar_í_a[ns]?_i') + #0
#lema(ur'[Rr]etractar_í_a[ns]?_i') + #0
#lema(ur'[Rr]eviv(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Rr]eñid_í_sim[ao]s?_i') + #0
#lema(ur'[Rr]omp_í_a[ns]?_i') + #0
#lema(ur'[Rr]ud_í_sim[ao]s?_i') + #0
#lema(ur'[Ss]_i_do_í') + #0
#lema(ur'[Ss]ab_í_amos_i') + #0
#lema(ur'[Ss]acrificar_í_a[ns]?_i') + #0
#lema(ur'[Ss]ali_en_do_ne') + #0
#lema(ur'[Ss]at_í_roc[ao]s?_i') + #0
#lema(ur'[Ss]e_ri_es?_ir', pre=ur'(?:[Ll]as?|[Dd]e) ') + #0
#lema(ur'[Ss]ecu_e_ncia_a') + #0
#lema(ur'[Ss]ecu_e_ncial(?:es|)_a') + #0
#lema(ur'[Ss]ecu_e_ncias?_a') + #0
#lema(ur'[Ss]ecue_s_trad[ao]s?_') + #0
#lema(ur'[Ss]egu_í_amos_i') + #0
#lema(ur'[Ss]eguir_í_a(?:[ns]?|mos)_i') + #0
#lema(ur'[Ss]eguir_í_amos_i') + #0
#lema(ur'[Ss]eleccionar_í_a[ns]?_i') + #0
#lema(ur'[Ss]ellar_í_a[ns]_i') + #0
#lema(ur'[Ss]emiderru_i_d[ao]s?_í') + #0
#lema(ur'[Ss]enadur_í_as?_i') + #0
#lema(ur'[Ss]ent_í_amos_i') + #0
#lema(ur'[Ss]eparar_í_a[ns]?_i') + #0
#lema(ur'[Ss]erializar_s_e(?:lo|)_c') + #0
#lema(ur'[Ss]ervir_í_a[ns]?_i') + #0
#lema(ur'[Ss]i_no má_s bien_ no m[aá]') + #0
#lema(ur'[Ss]icol_ó_gic[ao]s?_o') + #0
#lema(ur'[Ss]impatiqu_í_sim[ao]s?_i') + #0
#lema(ur'[Ss]intomatolog_í_as?_i') + #0
#lema(ur'[Ss]iqui_á_tric[ao]s?_a') + #0
#lema(ur'[Ss]o_r_prendió_') + #0
#lema(ur'[Ss]obreviv(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Ss]obrevivir_á_[ns]?_a') + #0
#lema(ur'[Ss]omet_é_r[mts]el[aeo]s?_e') + #0
#lema(ur'[Ss]omet_í_a[ns]?_i') + #0
#lema(ur'[Ss]ometer_á_[ns]?_a') + #0
#lema(ur'[Ss]orprend_í_a[ns]?_i') + #0
#lema(ur'[Ss]ub_í_an_i') + #0
#lema(ur'[Ss]ubdivid(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Ss]ubsist(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Ss]ubstra_í_(?:a[ns]?|d[ao]s?)_i') + #0
#lema(ur'[Ss]uceder_á_[ns]?_a') + #0
#lema(ur'[Ss]uceder_í_a[ns]?_i') + #0
#lema(ur'[Ss]ucumb(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Ss]ufrir_á_[ns]?_a') + #0
#lema(ur'[Ss]uger_í_a[ns]?_i') + #0
#lema(ur'[Ss]upondr_á_[ns]?_a') + #0
#lema(ur'[Ss]uponi_en_do_ne') + #0
#lema(ur'[Ss]urt(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Ss]urtir_á_[ns]?_a') + #0
#lema(ur'[Ss]uspend_í_a[ns]?_i') + #0
#lema(ur'[Ss]ust_itui_d[ao]s?_uí') + #0
#lema(ur'[Tt]ant_í_sim[ao]s?_i') + #0
#lema(ur'[Tt]apar_í_a[ns]?_i') + #0
#lema(ur'[Tt]e_r_minar(?:se|l[ao]s?|ron|ría[ns]?|)_') + #0
#lema(ur'[Tt]ej_í_a[ns]?_i') + #0
#lema(ur'[Tt]elevi_s_ión_c') + #0
#lema(ur'[Tt]elevis_i_ón_í') + #0
#lema(ur'[Tt]elevisi__ón_s') + #0
#lema(ur'[Tt]em_í_a[ns]_i') + #0
#lema(ur'[Tt]end_í_a[ns]?_i') + #0
#lema(ur'[Tt]ende_n_cias?_') + #0
#lema(ur'[Tt]exte_á_ndo(?:[mst]e|l[aeo]s?|nos)(?:[mt]e|l[aeo]s?|nos|)_a') + #0
#lema(ur'[Tt]iem__po_n') + #0
#lema(ur'[Tt]ioci_á_nic[ao]s?_a') + #0
#lema(ur'[Tt]itular_í_sim[ao]s?_i') + #0
#lema(ur'[Tt]odoter_r_enos?_') + #0
#lema(ur'[Tt]olerar_í_a[ns]?_i') + #0
#lema(ur'[Tt]opolog_í_as?_i') + #0
#lema(ur'[Tt]or_á_xoc[ao]s?_a') + #0
#lema(ur'[Tt]ra_ns_parente_sn') + #0
#lema(ur'[Tt]ra_ns_portaba_sn') + #0
#lema(ur'[Tt]ra_ns_porte[ns]_s?n') + #0
#lema(ur'[Tt]ra_ns_portes_sn') + #0
#lema(ur'[Tt]raducir_á_[ns]?_a') + #0
#lema(ur'[Tt]raer_á_[ns]?_a') + #0
#lema(ur'[Tt]raicionar_í_a[ns]?_i') + #0
#lema(ur'[Tt]ran_s_portador_') + #0
#lema(ur'[Tt]ran_s_portados_') + #0
#lema(ur'[Tt]ran_s_portarse_') + #0
#lema(ur'[Tt]ranscender_á_[ns]?_a') + #0
#lema(ur'[Tt]ranscrib(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Tt]ransformar_s_e(?:lo|)_c') + #0
#lema(ur'[Tt]ransformar_í_a[ns]?_i') + #0
#lema(ur'[Tt]ransmitir_á_[ns]?_a') + #0
#lema(ur'[Tt]rasladar_s_e(?:lo|)_c') + #0
#lema(ur'[Tt]rasmit(?:ir|)_í_a[ns]?_i') + #0
#lema(ur'[Tt]rasmitir_á_[ns]?_a') + #0
#lema(ur'[Tt]raspi_é_s?_e') + #0
#lema(ur'[Tt]ratar_í_a[ns]?_i') + #0
#lema(ur'[Tt]raum_á_tic[ao]s?_') + #0
#lema(ur'[Tt]raumat_ó_log[ao]s?_o') + #0
#lema(ur'[Tt]reintai_ú_n_u') + #0
#lema(ur'[Tt]reintais_é_is_e') + #0
#lema(ur'[Tt]reintaitr_é_s_e') + #0
#lema(ur'[Tt]remend_í_sim[ao]s?_i') + #0
#lema(ur'[Uu]n_ _papel_') + #0
#lema(ur'[Uu]n_ _partido_') + #0
#lema(ur'[Uu]n_ _periodista_') + #0
#lema(ur'[Uu]n_a fá_brica_ f[aá]') + #0
#lema(ur'[Uu]n_a magní_fica_ magn[ií]') + #0
#lema(ur'[Uu]n_a pé_rdida_ p[eé]') + #0
#lema(ur'[Uu]nir_s_e(?:lo|)_c') + #0
#lema(ur'[Uu]tiler_í_as?_i') + #0
#lema(ur'[Uu]tilizar_s_e(?:lo|)_c') + #0
#lema(ur'[Vv]alios_í_sim[ao]s?_i') + #0
#lema(ur'[Vv]e_í_amos_i') + #0
#lema(ur'[Vv]enerad_í_sim[ao]s?_i') + #0
#lema(ur'[Vv]engar_s_e(?:lo|)_c') + #0
#lema(ur'[Vv]engar_s_e_z') + #0
#lema(ur'[Vv]entajos_í_sim[ao]s?_i') + #0
#lema(ur'[Vv]er_í_amos_i') + #0
#lema(ur'[Vv]estir_í_a[ns]?_i') + #0
#lema(ur'[Vv]iajar_í_a[ns]?_i') + #0
#lema(ur'[Vv]ideogr_á_fic[ao]s?_a') + #0
#lema(ur'[Vv]illan_í_sim[ao]s?_i') + #0
#lema(ur'[Vv]irar_í_a[ns]?_i') + #0
#lema(ur'[Vv]iv_í_amos_i') + #0
#lema(ur'[Vv]ivir_í_a[ns]?_i') + #0
#lema(ur'[Vv]olar_í_a[ns]?_i') + #0
#lema(ur'[Vv]olv_í_(?:a[ns]?)_i') + #0
#lema(ur'[Vv]uelt_a_s?_á') + #0
#lema(ur'[Zz]oledr_ó_nic[ao]s?_o') + #0
#lema(ur'[b]ajar_í_a[ns]?_i') + #0
#lema(ur'[c]omprendi_do__[óo]', pre=ur'[Pp]er[ií]odo ') + #0
#lema(ur'[d]e l_ongitud__largària') + #0
#lema(ur'[e]st_á_(?:[.,;]| (?:el|la|un|una) )_a', pre=ur'donde ') + #0
#lema(ur'[ee]_m_pacad[ao]s?_n') + #0
#lema(ur'[f]ranc_é_s_e', pre=ur'[Ii]dioma [Ff]ranc[eé]s\|') + #0
#lema(ur'[h]ar_á_s_a', pre=ur'(?:[Qq]u[eé]|dinero|te|carrera) ') + #0
#lema(ur'[l]ic_ú_an_u') + #0
#lema(ur'[m]ir_á_ndol[ae]_a') + #0
#lema(ur'[q]_ue_ le_') + #0
#lema(ur'[t]en_ido__dio', pre=ur'[Hh]a(?:n?|bían?|ber) ') + #0
#lema(ur'[Áá]__lbum_lbum á') + #0
#lema(ur'[Áá]lbum_e_s_(?:ne|)') + #0
#lema(ur'[Úú]ltim[ao]_s__', pre=ur'[Ll][ao]s ') + #0
#lema(ur'_Club de Futbol Igualada__Club de Fútbol Igualada') + #0
#lema(ur'_D_inamarca_d', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or|y) ') + #0
#lema(ur'_Ha_sta ahora_A') + #0
#lema(ur'_Hu_esos?_U') + #0
#lema(ur'_Hu_ndi(?:d[ao]s?|dimiento)_U') + #0
#lema(ur'_Murphy Pacific Corporation__Murphy Pacific Corporacion') + #0
#lema(ur'__acerca(?:r|rse|)_h') + #0
#lema(ur'_c_ercan[ao]s?_s') + #0
#lema(ur'_esperando__esparando', pre=ur'[Ee]stán? ') + #0
#lema(ur'_febrero__[Ff]evereiro', pre=ur'acessado em [0-9]+ de ') + #0
#lema(ur'_ha_ dicho (?: a |el |de |en |que|antes|ser )_ah?') + #0
#lema(ur'_increíble__íncreible') + #0
#lema(ur'_increíbles__íncreibles') + #0
#lema(ur'_noviembre__[Nn]ovembro', pre=ur'acessado em [0-9]+ de ') + #0
#lema(ur'_sali_an?_(?:Sal[ií]|salí)', pre=ur'[Dd]inast[ií]a ') + #0
#lema(ur'_v_oleibol_b') + #0
#lema(ur'_Á_gil(?:es|mente)_A') + #0
#lema(ur'_Á_ure[ao]s_A') + #0
#lema(ur'_É_tnic(?:[ao]s|amente)_E') + #0
#lema(ur'_ó_pticas_o') + #0
[]][0]

grupo2 = grupo2Perfecto + grupo2Accion + [# 500-999
lema(ur'_Latinoamé_rica_(?:Latinoame|latinoam[eé])', xpos=[ur' e tutti', ur'\]\][a-z]*', ]) + #951
lema(ur'[Ff]_ú_tbol_u', pre=ur'[Dd]e ', xpre=[ur'Associació Catalana ', ur'Burjassot Club ', ur'Club Escola ', ur'Escola ', ur'Estadi Municipal ', ur'Federació ', ur'Federació Andorrana ', ur'Federació [Cc]atalana ', ur'Lliga Nacional ', ur'Mafumet Club ', ur'Nou camp ', ur'Ontinyent Club ', ur'Palamós Club ', ur'Pego Club ', ur'Segona Catalana ', ur'Selecció catalana ', ur'Tercera Catalana ', ur'Vilobí Club ', ur'[Cc]amp ', ur'anys ', ur'equip ', ], xpos=[ur' (?:Amposta|Mollet|Juventut|Os |do |Gavà|Badalona|Balaguer|Pobla|Club Martinenc|Valls|Club Andorra|Indoor|Sudanell|Lloret|de Logroño|Santa Eulàlia|Organyà|Reus|Vilanova|Factory|Femení|Suiço|Jovent|Atlètic)', ]) + #798
lema(ur'[Pp]el_í_culas?_i', xpos=[ur'(?:\.disneylatino|\.info|9)', ]) + #783
lema(ur'[Aa]s_í__i', xpre=[ur'Emmanuel ', ur'K’', ur'Ta\'', ur'[Ii]dioma ', ur'\ben ', ur'al-Fak\'', ], xpos=[ur' (?:(?:sen|TV) |Rahamim|language|dizen|Gonia|Deobriga|Klyáchkinoy|Cohen|Gilboa|Domb|Ses|Taulava|Ganga|Pudjiastuti|Golboa|Doğan|Klyachinoy|Al Shuraim|Yarba|Vassihon|Kehra)', ur'(?:\]|\.nic|[0-9ˈ"\']|\.C3)', ]) + #738
lema(ur'_ E_st(?:e|á[ns]?|[ao]s?)_[Ee]', pre=ur'[-0-9a-záéúíóúüñA-ZÁÉÚÍÓÚÜÑ\]]+[\.;]') + #642
lema(ur'[Pp]a_í_s_i', pre=ur'(?:[Aa]l|[Cc]ada|[Dd]el|[Ee]l|[Uu]n|[Ss]u|[Mm]i|[Nn]uestro|gran|pequeño|[Ee]ste|[Dd]icho|[Pp]or|[Cc]ualquier) ', xpre=[ur'd\' ', ur'd\'D\'Amics ', ], xpos=[ur' (?:dels|Valenci[aàá]|Basc|de les caramelles)', ur'\.es', ]) + #626
lema(ur'M_é_xico_e', pre=ur'(?:[Dd]e|[Ee]n|[Ss]obre|[Pp]ara|[Pp]or|[Tt]odo) ', xpre=[ur'Audrain ', ur'Bassin ', ur'Chanteur ', ur'Histoire ', ur'Humaines ', ], xpos=[ur' (?:Herpetology|City|Beach)', ur'[\']s', ]) + #609
lema(ur'[Dd]emogr_á_fic[ao]s?_a', xpre=[ur'Bilancio ', ur'storia ', ]) + #594
lema(ur'_ú_ltimos?_u', pre=ur'(?:[Ss]us?|[Ee]l|[Ll]os?|[Aa]l?|[Ee]n|[Dd]el?|[Uu]n(?:os|)|[Ee]st(?:e|os?)|[Éé]ste|[Ee]s(?:e|os?)|[Pp]or|[Cc]omo|[Cc]uyos?|[Yy]|[Mm]is?|terminó|terminando|terminar|quedar|quedando|dos) ', xpos=[ur' (?:battito|fine)', ]) + #587
lema(ur'[Aa]rt_í_culo_i', xpos=[ur' (?:mortis|meni)', ]) + #572
lema(ur'[Cc]ap_í_tulos?_i', xpre=[ur' in ', ], xpos=[ur' et', ]) + #556
lema(ur'Jim_é_nez_e', xpre=[ur'Cláudia ', ]) + #516
lema(ur'[Hh]ist_ó_ricos?_o', xpre=[ur'Boletim ', ur'Estudo ', ur'Illimani ', ur'Lesbio ', ur'[Aa]no ', ur'do Patrimonio ', ur'medicorum ', ur'romànico ', ur'Études ', ], xpos=[ur' (?:Naturalia|do|no|[Aa]sturiensia)\b', ur' et ', ur', biographico', ]) + #514
[]][0]

grupo3 = [# 250-499
lema(ur'[Tt]en_í_as?_i', xpre=[ur'Estas ', ur'Mario ', ur'Ram[oó]n ', ur'[Ee]l ', ur'[Ll]as ', ur'\ba ', ur'\bcon ', ur'\bde ', ur'curar la ', ur'entre ', ur'excepto ', ur'llamado ', ], xpos=[ur' (?:\((?:adulta|arquitectura)|E\. granulosus|o lombriz|de la que|saginata|del (?:hombre|\[\[perro|rumiante)|dues cases|del (?:pez|género)|raor|els|[Mm]ortal)', ur'(?:[\'\|\]]|, amiba)', ]) + #794
lema(ur'[Nn]_ú_mero (?:de|uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|veinte|[1-9][0-9]*)_u', xpre=[ur'(?:[Ii]l|um) ', ur'Anno III – ', ur'Cabine ', ur'Canzone ', ur'Magazine, ', ur'Resolução ', ur'Sunyer\. ', ur'Turisme\'\'\. ', ur'anno 1897 ', ur'anno 8. ', ur'anno I, ', ur'anno II, ', ur'anno III, ', ur'anno IV, ', ur'archi ', ur'grande ', ur'humanitat\. ', ur'notte ', ur'pericolo ', ur'pubblicazione ', ur'scudetto ', ur'stesso ', ur'tram ', ], xpos=[ur' (?:apeles|d[ai] )', ]) + #465
lema(ur'[Aa]uton_ó_mic[ao]s?_o', xpos=[ur'[0-9]', ]) + #441
lema(ur'[Ff]_ú_tbol_u', pre=ur'(?:[Aa]l|[Ee]l|[Uu]n|[Dd]el) ', xpre=[ur'Cap ', ur'Estadi ', ur'Història crítica ', ur'lusionistes ', ], xpos=[ur' (?:Gavà|Català|Martinenc|modest|Reus|Vilanova i|Igualada|Balaguer|D\'Ordino|Nou|Club Santboià)', ur'ʹnyy̆', ]) + #412
lema(ur'[Ee]j_é_rcito_e', pre=ur'(?:[Aa]l|[Ee]l|[Dd]el|[Uu]n|[Ss]u) ') + #395
lema(ur'(?:[Aa]|[Dd]e)__l (?:[Rr]ey|[uú]ltimo|antiguo|centro|club|cuarto|desarrollo|elenco|entonces|equipo|español|estado|estudio|g[ée]nero|gobierno|gran|grupo|incremento|juego|jugador|lugar|margen|momento|mundo|municipio|nombre|nuevo|número|oeste|otro|padre|país|personaje|planeta|poder|presidente|primer|productor|programa|pueblo|resto|tema|trabajo|usuario|verdadero|álbum)_ e', xpre=[ur'intentos y ', ur'(?:[Ll]ado|[Cc]ara) ', ur'\.', ]) + #363
lema(ur'Medell_í_n_i', xpre=[ur'366272\) ', ur'in ', ]) + #338
lema(ur'B_é_lgica_e', xpre=[ur' (?:du|el) ', ur' (?:du|el) \'\'', ur'1884\)\|', ur'1884\)\|\'\'', ur'Botanica ', ur'Florula ', ur'Fort ', ur'Galia ', ur'Gallia ', ur'Janseniana ', ur'Linneana ', ur'María ', ur'Neurologica ', ur'Nova ', ur'Psychiatrica ', ur'RV ', ur'RV \'\'', ur'S\.Y\. ', ur'Scripta Bot\. ', ur'Scripta botanica ', ur'The ', ur'[Ll]a ', ur'[ae]l ', ur'\(1052\) ', ur'de la ', ur'del ', ur'del \'\'', ur'el "', ur'expédition "', ur'género\)\|', ur'llamándolo \'\'', ur'navío ', ur'navío "', ur'nombre de \'\'', ur'velero ', ], xpos=[ur' (?:Nova|prima|secunda|de Nassau|antarctica|Diary|FC|Edegem|Universe|Prima|Secunda|Historiae|Nostri|Flemish|Wallonian|Edegem|Select|Albums|Top|\(género)', ]) + #336
lema(ur'[Hh]ist_ó_ric(?:as?|amente)_o', xpre=[ur' e[nt] ', ur'Acta ', ur'Augustiniana ', ur'Bibliotheca ', ur'Commentatio ', ur'De ', ur'De arte ', ur'Dissertatio ', ur'Epitome ', ur'Exquisitio ', ur'Flora ', ur'Folia Linguistica ', ur'Folia Lingüística ', ur'Fragmenta ', ur'Geographia ', ur'Geographica ', ur'Germaniae ', ur'Germanica ', ur'Germaniæ ', ur'Militaria & ', ur'Miscellanea ', ur'Monumenta ', ur'Opera ', ur'Recerca ', ur'Relatio ', ur'Romaniae ', ur'Studia ', ur'Studia ', ur'Synopsis ', ur'panta: ', ], xpos=[ur' (?:Minutes|facultate|Constantiniana|Bohemica|da|del Rei|e [Gg]eneal[oó]gicas|Hungariam|Asturiensia|Didactica|Foundation|Russiae|Lwów|et)\b', ur'(?:\] project|\.(?:ejercito|unam)|\'\')', ]) + #333
lema(ur'[Pp]eri_ó_dic[ao]_o', xpre=[ur'Christiana ', ur'Il sistema ', ur'Publicatio ', ], xpos=[ur' (?:della|dell|evangeliorum|Constantiniana|internazionale|national|\(sic|di )', ur'\.cnt', ]) + #316
lema(ur'[s]er_á__a', xpre=[ur'(?:da|ne|où|\'a) ', ur'Ades ', ur'Alla ', ur'Aussi ', ur'Bona ', ur'Buona ', ur'Caledanapis ', ur'Campanile ', ur'Domenica ', ur'Elle ', ur'L\'ultima ', ur'La ', ur'Pissarrachampsa ', ur'Prima ', ur'Quando viene ', ur'Quando viene la ', ur'Quella ', ur'Questa ', ur'Stampa ', ur'Verso ', ur'Viene ', ur'[\' ](?:[Ff]a|[Ii]l|[Dd][ei]|[Cc]e|[Nn]a|[Ll]a) ', ur'[Qq]ue ', ur'[Qq]ui ', ur'[Ss]abato ', ur'[Ss]er[aá] ', ur'[Ss]er[aá], ', ur'[Tt]out ', ur'[Tt]oyota ', ur'[Uu]na ', ur'[Uu]na ', ur'c\'', ur'che ', ur'come ', ur'culotte ', ur'dell\'ultima ', ur'della ', ur'devoir ', ur'domenica ', ur'dur ', ur'esce la ', ur'grande ', ur'idioma ', ur'ieri ', ur'mezza ', ur'n\'ata ', ur'nella ', ur'nous ', ur'quel ', ur'quella ', ur'questa ', ur'stessa ', ur'subito ', ur'vie ', ], xpos=[ur' (?:a [cz]ena|admis|assimilée|aussi|calme|como antes: MPB anos|complet|del grande|di|définitivement|démocratique|reprise|dépassé|désormais|en retard|facilement|fait|fiesolana|fuku|gentile|impitoyable|jamais|l\'aurore|le mois|liberté|longue|l´alba|mon|notre|pas|plus|pour|quando|tamen|toujours|tournée|une|unité|à )', ur', (?:ser[aá]|aussi|amen)', ]) + #315
lema(ur'[Ee]conom_í_as?_i', xpre=[ur'Facultade de ', ur'Història, ', ur'Instituições de ', ur'Nodal ', ur'Outra ', ur'Parlem de ', ur'Pensiero – ', ur'Societat i ', ur'Societat, ', ur'UOL ', ur'[Ll][`’\']', ur'[Uu]ma ', ur'[dl]\'', ur'\b(?:e[dm]|na) ', ur'\b[Aa] ', ur'\bd[ai] ', ur'\be ', ur'\by \'\'', ur'dell\'', ur'il Magnifico: politica, ', ur'llamado \'\'', ur'nostra ', ur'nuova ', ], xpos=[ur' (?:non|Fechada|rustica per|d[aio]|dell|Internazionale|canaglia|Brasileira|pubblica|mundial em|Política do|Solidária|\(editorial|e (?:sviluppo|[Ss]ociedade|società|[Tt]eologia|[Pp]olítica|[Gg]estão|Storia|Retórica|Finanze)|i|popular e solidária|- Itália marca)\b', ur'(?:[]0-9]+|, (?:cultura i|planejamento|producció|Internazionale|Management|Administração)|\.(?:gob|uady)|: O novo)\b', ]) + #313
lema(ur'Bogot_á__a', xpre=[ur'12325\) ', ur'Illinois\)\|', ur'Labama ', ur'Royal ', ur'Tennessee\)\|', ur'[Ff]rom ', ur'\b(?:in|of) ', ur'\bthe ', ur'd[\'’]Or de ', ], xpos=[ur'\.gov\.co|: From|[\'’]s| (?:[Ii]n|Film|Beer|Wildlife|[Pp]roject|Laser|\((?:Tennessee|Illinois)|Telephone)', ]) + #307
lema(ur'M_á_laga_a', xpre=[ur'Gustave ', ur'[Mm]unicipio de ', ur'\b(?:í|a) ', ur'\bin ', ], xpos=[ur' (?:Auditorium|Airport)', ur'\.es', ]) + #286
lema(ur'[Pp]ol_í_tica_i', xpre=[ur'Carità ', ur'Commentatio ', ur'Comunicacao & ', ur'Exercitatio ', ur'Lege ', ur'Palingenesi ', ur'Principia ', ur'Renovacio ', ur'Scienza ', ur'Societá italiana de Filosofia ', ur'Studia ', ur'Vita ', ur'Zero ', ur'[Rr]egio ', ur'[Ss]cienza & ', ur'\b(?:d[ai]|De) ', ur'\b[Aaei] ', ur'\be la ', ur'\buma ', ur'\by \'\'', ur'alla ', ur'capitale ', ur'concepire la ', ur'dalla mafia ', ur'dell[\'’][Ee]conomia ', ur'dell[ae] ', ur'della filosofia ', ur'democrazia ', ur'di Economia ', ur'di [Ee]conomía ', ur'di economia ', ur'di teoria ', ur'distinzione ', ur'e Cultura ', ur'eclesiastica: ', ur'elettorale ', ur'et ', ur'giurisdizione ', ur'il Magnifico: ', ur'in "Filosofia ', ur'legittimazione ', ur'libertate ', ur'nella ', ur'nuova ', ur'partecipazione ', ur'passione ', ur'rappresentanza ', ur'riflessione ', ur'scienza ', ur'sulla ', ur'trias ', ur'vita ', ur'vita la ', ], xpos=[ur' (?:del diritto|Educacional No|del novecento|autoritară|sapientia|nazionale|hermetica|mineaza|ostile|estera|xxi|contro|Oeconomica|sotterranea|Methodicae|and|nell|[Ee] (?:morte|cultura|nuove|verità|utopia|letteratura|dissimulazione|la|[Hh]istoria)|italiana di|seu|Logica|perduta|ecclesiatica|Hermetica|e |(?:ed|in) |come|razzista|occidentale|internazionale|d[aio] |dell|della|al tempo|del (?:Regno|corpo)|tedesca|de Acalmação)', ur'(?:, (?:mafia e giustizia|Corsica)|: Logica e Metodo|\.Ambiental)', ]) + #286
lema(ur'[Ee]stad_í_sticas_i', xpre=[ur'CD ', ], xpos=[ur'(?:\.sport)', ]) + #272
lema(ur'[Hh]ab_í_a_i', xpos=[ur' (?:atrimaxillaris|rubra|rubica|fuscicauda|cristata|copetona|ceniza|gutteralis|Carinegra|de garganta|que chusar|gutturalis|\[\[Rosa|sombría|gorjirroja|coronirroja|carinegra)', ur'(?:\]\]|\'\')', ]) + #266
lema(ur'[Bb]_é_isbol_e', xpre=[ur'Camp de ', ur'Politics, ', ur'française de ', ], xpos=[ur' (?:Elkartea|i Softbol|Viladecans|i Sofbol)', ur'(?:\.com|\]\]istas?)', ]) + #261
lema(ur'[Mm]en_ú__u', xpre=[ur'\'s ', ur'Alain ', ur'Beatmac ', ur'Bernadette ', ur'Bernard ', ur'British ', ur'CD ', ur'CSS3', ur'Charles ', ur'Cheat ', ur'Clothilde ', ur'Conde ', ur'Expanded ', ur'François ', ur'Home ', ur'Ithaa ', ur'Jan ', ur'Jean-Christophe ', ur'Koi ', ur'Load ', ur'Love ', ur'Main ', ur'Me ', ur'Memphis ', ur'Michel ', ur'Millionaire ', ur'Operation ', ur'Paris: ', ur'Philippe ', ur'Pierre ', ur'Player ', ur'Rudi ', ur'S\. ', ur'Services ', ur'Short ', ur'Special ', ur'Start ', ur'Sunday ', ur'Sunday ', ur'Teni ', ur'Video ', ur'Word ', ur'[Aa]dministration ', ur'[Gg]eneral ', ur'[Tt]he ', ur'[・]', ur'\ba ', ur'attribute ', ur'het ', ur'main ', ur'pie ', ur'pineau ', ur'value ', ], xpos=[ur' (?:à|items|W9|du |wa Tips|Planner|Cookbook|Music|automatically|Screen|programming|Degustació|of|and|for|bétail|[Bb]ar|[Dd]efinition|idéal|Yves|Steam|y (?:Command|Back)|de (?:Ménil|dimanche|repas)|loops|Theme|Engineer|Engineering|Select|Items|navigation|editor|von|Có|\(Melee|& Autopsy)', ur'(?:\.(?:xml|asp|[Aa]pplet|com)|\|, (?:Scheduler|en|\(1984|M\.|Michel)|\'\'\', \(1987|\]\], 1984)', ]) + #258
lema(ur'_Perú__(?:per[uú]|Peru)', pre=ur'(?:[Aa]|[AaEe]l|[Aa]nte|[Dd]el?|[Ee]n|[Pp]ara|[Pp]or|[Ss]omos) ', xpre=[ur'Reynos ', ur'[Mm]icropolitana ', ur'[Mm]unicipio ', ], xpos=[ur' \((?:condado|Iowa)', ur'(?:\.com|[0-9]+)', ]) + #255
lema(ur'[Ss]_é_ptim[ao]s?_e', xpre=[ur'Anne ', ur'Dissertation ', ur'Drepanosticta ', ur'Et ', ur'Franca ', ur'Legio ', ur'Limnoria ', ur'Macromia ', ur'Triacanthagyna ', ur'vicesima ', ], xpos=[ur' (?:Vector|Gemina|saeculo|Basiano|Severo|Arts|editio|ab )', ur'\.cl', ]) + #254
lema(ur'M_ú_nich_u', pre=ur'(?:[Dd]e|[Ee]n) ', xpre=[ur'Biennale ', ur'Français ', ur'Souvenirs ', ur'accord ', ], xpos=[ur' (?:[Mm]achine|My|Kurt)', ]) + #253
lema(ur'[Cc]at_ó_lic[ao]s?_o', xpre=[ur'Escola ', ur'Missão ', ur'Rei ', ur'Universidade ', ur'dos Siriacos ', ], xpos=[ur'\.edu', ur'do\b', ]) + #251
lema(ur'[Dd]ej_ó__o', xpre=[ur' (?:un|[tm]e|al|lo|yo) ', ur' [&] ', ur'"lo ', ur'#Los ', ur'(?:[Ee]l|Un|[TM]e|Al|Lo) ', ur'Ahí le ', ur'Ahí les ', ur'Aquí ', ur'Aquí les ', ur'Ben ', ur'Chullén ', ur'Juan ', ur'Karen ', ur'Les ', ur'Lozada ', ur'No la ', ur'Os ', ur'Si ', ur'Si alguna vez ', ur'Yo ', ur'Yo nunca ', ur'[Ss]u ', ur'aplicó ', ur'con ', ur'conducto ', ur'cuando ', ur'ese ', ur'esta noche ', ur'herencia que le ', ur'irme ', ur'linquo\'\' \'', ur'ningún ', ur'o no ', ur'o no la ', ur'qu-o\'\' \'', ur'si no ', ur'tus manos ', ur'un cierto ', ur'visigodos ', ], xpos=[ur' (?:charapa|aquí|alemán|que|todo|a |CNN|botá|heredad|Bendezú|ar |The|Dance|el (?:Art|amor|cargo|festival|resto)|entre vosotros|En Libertad|la (?:selección|ventana|mejor compañía|Sonora)|[Dd]e (?:Pensar|salir)|o no|[Tt]u (?:sombra|corazón)|su hogar|[Mm]i (?:estela|corazón|Huella|estatua|dedo)|Amber|Libre|Madrid|Sparavalo|eso para Mortifera|Fayemi|prendida mi|un apellido|una familia|como herederos|curial|rastro tras|piedra sobre|por razones|[Cc]onstancia|nuestra|y me)', ur'(?:[\'\]]|, Juan|" \(1 sg)', ]) + #389
[]][0]

grupo4 = [# 100-249
lema(ur'_Á_msterdam_A', pre=ur'(?:[Dd]e|[Ee]n) ', xpre=[ur'[Mm]icropolitana ', ur'[Mm]unicipio ', ], xpos=[ur' (?:Midkap|Zuidoost|Pride)', ur' Street', ur' Vallon', ]) + #245
lema(ur'[Dd]iscograf_í_as?_i', xpre=[ur'Uma ', ], xpos=[ur' (?:brasileira|Illustrata)', ]) + #241
lema(ur'[Pp]olic_í_as?_i', xpre=[ur'\bda ', ur'bon ', ur'deputado ', ], xpos=[ur' (?:de la Generalitat|armat|in)\b', ur'(?:\.gov|[\]])', ]) + #235
lema(ur'_Á_frica_[Aaá]', pre=ur'(?:[Dd]e|[Ee]n|[Aa]l?|y) ', xpos=[ur' (?:Korps|Sports|House|Data|One|Race|Star|Magic|desde o )', ]) + #234
lema(ur'[Ee]stad_í_stic(?:a|os?|amente)_i', xpos=[ur'(?:\.(?:ad|net))', ]) + #234
lema(ur'[Aa]qu_í__i', xpre=[ur'Ara i ', ur'Chegar ', ur'Eis ', ur'Ele Está ', ur'Esteve ', ur'Estou ', ur'Ficar Por ', ur'Isto ', ur'Keith ', ur'Político ', ur'Senta ', ur'Ter ', ur'Vem ', ur'Voc[eê] Está ', ur'[Dd]\'', ur'[Ff]ique ', ur'[Vv]eja ', ur'[Éé] ', ur'foram ', ur'jogam ', ur'pouco ', ur'prá ', ur'se Faz, ', ur'soc ', ], xpos=[ur' (?:Huec[oó]|Tão|Portugal|Chegamos|comiença|lladas|yaze|fasemos|restringido à|[Nn][aã]o|Há|D\'El|s\'Acaba|se Faz|Tá|Ness|iace|de Novo|jaz|Strange|Without|havia|[áeé] |na |tudo|tem |entre nós|Estou|começa|o R[íi]o|a (?:palavra|emoção))', ur'(?:[\|\)\']|, (?:ali|Buytrago|Mato Grosso se vê))', ]) + #232
lema(ur'M_á_nchester_a', pre=ur'(?:[Dd]e|[Ee]n) ', xpre=[ur'Clay ', ur'[Cc]ondado ', ur'[Mm]unicipio ', ur'[Rr]esidiendo ', ur'electoral ', ], xpos=[ur' (?:Square|City|Academy|United|Central|Apollo|University|Magic|terrier)', ]) + #227
lema(ur'_é_l (?:est(?:ar|)[aá]n?|estaba|estará|estuvo|estar[ií]an?|dijo|dir[aá]|dice|vienen?|fu[ée]|fueron|vendr[aá]n?|tiene|tuvo|ten[ií]a[ns]?|tendrán?|es|era|serán?|fue|hab[ií]a|sabe|sab[ií]a|no le)_e', xpre=[ur'l\'', ]) + #222
lema(ur'Crist_ó_bal_o', pre=ur'San ', xpre=[ur' [Tt]o ', ur' ng ', ur'[Ff]rom ', ], xpos=[ur' (?:Thrush|Starling|Mockingbird|Melidectes|Leaf)', ur'(?:\.jpg|, Columbus)', ]) + #218
lema(ur'[Mm]_ás tarde__(?:as tardes?|ás tardes)', xpre=[ur'[Nn]o habrá ', ur'vivió ', ]) + #218
lema(ur'[Mm]editerr_á_ne[ao]s?_a', xpre=[ur' (?:dil|nel|dal) ', ur' e ', ur' il ', ur'\'', ur'Accademia ', ur'Acetabularia ', ur'Actinia ', ur'Aegiphila ', ur'Alus ', ur'Anoplolepis ', ur'Antedon ', ur'Aria ', ur'Arundo ', ur'Ascidia ', ur'Associazione ', ur'Associazione ', ur'Astacilla ', ur'Atropa ', ur'Bacino ', ur'Biscutella ', ur'Biserrula ', ur'Borsa ', ur'Brevundimonas ', ur'Brotera ', ur'Bursa ', ur'Calea ', ur'Camerata ', ur'Cappella ', ur'Capsella ', ur'Carex ', ur'Chelidonura ', ur'Città del ', ur'Cladonia ', ur'Comatula ', ur'Cooperazione ', ur'Corsari del ', ur'Corynactis ', ur'Cypridina ', ur'Cystoseira ', ur'Cystoseira ', ur'Cystosera ', ur'Da Bahia ', ur'Dacia ', ur'Dal ', ur'Decaisnella ', ur'Diospyros ', ur'Dipoena ', ur'Echi del ', ur'Editoriale del ', ur'Elytrigia ', ur'Enoplognatha ', ur'Erica ', ur'Ersilia ', ur'Eucera ', ur'Ferriera ', ur'Festuca ', ur'Flammulina ', ur'Flora ', ur'Geranium subsección ', ur'Giochi del ', ur'Globorotalia ', ur'Gnathostomula ', ur'Grande ', ur'Gypsocallis ', ur'Hermione ', ur'Itinera ', ur'Janusia ', ur'L\'[Aa]ncora del ', ur'Leptomysis ', ur'Lyra del ', ur'Malthonica ', ur'Malva ', ur'Marinomonas ', ur'Multimediale del ', ur'Musica ', ur'Musicale ', ur'Mycosphaerella ', ur'Myristica ', ur'Okenia ', ur'Orchis ', ur'Organizzatore Giochi del ', ur'Osyris ', ur'Paesaggio ', ur'Parachiridotea ', ur'Periandra ', ur'Periandra ', ur'Phycologia ', ur'Phytopathologia ', ur'Procrassula ', ur'Pseudomonas ', ur'Pseudorca ', ur'Raynaudetia ', ur'Sanguisorba ', ur'Scabiosa ', ur'Setaphis ', ur'Società Aerea ', ur'Spermophorides ', ur'Spirulina ', ur'Stachys ', ur'Stenosoma ', ur'Stipa ', ur'Studi ', ur'Studia ', ur'Tipula ', ur'Tipula ', ur'Upogebia ', ur'Uropoda ', ur'Vedetta ', ur'Vegetazione ', ur'Voci del ', ur'Xerula ', ur'Zostera ', ur'[ABP]\. ', ur'[Cc]ostiero ', ur'[CfST]\. ', ur'[Mm]acchia ', ur'[Nn]obiltà ', ur'[Ss]ocietà ', ur'[Tt]arantola ', ur'argo ', ur'capitale fenicia del ', ur'centro on-line ', ur'civiltà ', ur'collinetta ', ur'd[\'’][Aa]rt del ', ur'dell[\'’]area ', ur'di poesia ', ur'e del ', ur'e fauna del ', ur'foina ', ur'identità ', ur'impero ', ur'internazionale ', ur'la canción "', ur'mare ', ur'mari ', ur'nell\'area ', ur'officinalis ', ur'portuali del ', ur'sciafila del ', ur'storia del ', ur'subsp\. ', ur'sul ', ur'ungarica ', ur'var\. ', ur'vegetazione ', ur'vegetazione marina bentonica fotofila del ', ur'vie del ', ], xpos=[ur' (?:nella|nei|Editions|viventibus|ricerche|Imperia|Antico|del Limbara|per la Cultura|Sarcuto|\((?:2003|película)|fitosociologico|Studios|centrale|centro-occidentale)', ur'(?:", in|" de Regio|: (?:[Ss]erie|vegetazione|Da))', ]) + #218
lema(ur'C_á_diz_a', xpre=[ur'Amoco ', ur'John ', ur'Ohio\)\|', ur'Roberto ', ur'[Mm]unicipio de ', ur'\b(?:at|of) ', ur'von ', ], xpos=[ur' (?:& Hedges|\((?:California|Ohio)|Bay|Island|Geneviève)', ]) + #216
lema(ur'_ha_ (?:jugado|labrado|lanzado|liberado|limitado|llegado|llenado|llevado|logrado|manejado|marcado|mantenido|matado|mejorado|mencionado|modelado|modernizado|mostrado|multiplicado|nacido|obtenido|observado|ocupado|ofrecido|ordenado|participado|peleado|perdido|permanecido|permitido|pertenecido|podido|pose[ií]do|presentado|probado|promovido|propagado|prosperado|provocado|publicado|quedado|realizado|recibido|recuperado|regresado|registrado|renunciado|repercutido|replanteado|representado|respondido|restaurado|retenido|retratado|reunido|revelado|revisado|revolucionado|sabido|sacado|salido|señalado|separado|sido|sobrevivido|sostenido|sufrido|sugerido|superado|suspendido|sustituido|tenido|terminado|tocado|tomado|trabajado|tra[ií]do|transcurrido|transformado|trasladado|tratado|ubicado|usado|utilizado|variado|vendido|venido|viajado|visto|vivido|vuelto)_ah?', xpre=[ur'[0-9]', ]) + #216
lema(ur'_ha_ perseguido_a', xpre=[ur'eufórico ', ]) + #1
lema(ur'Hungr_í_a_i', xpos=[ur', M\.', ]) + #214
lema(ur'[Jj]ud_í_[ao]s?_i', xpre=[ur'A ', ur'Als ', ur'Kentucky\)\|', ], xpos=[ur' \(Kentucky', ]) + #211
lema(ur'[Bb]ater_í_as?_i', xpre=[ur'[Rr]ainha de ', ]) + #210
lema(ur'_é_l se_e', xpre=[ur'Har\'', ur'Yisra’', ur'l\'', ]) + #201
lema(ur'Gim_é_nez_e', xpre=[ur'Antônio ', ]) + #192
lema(ur'[Nn]_ú_meros?_u', pre=ur'(?:[Ll]a|[Ee]l|[UuEe]n|[Ll]os|[Uu]nos|[Ss]u|[Ss]in|[Gg]ran|[Cc]iertos?|[Ee]s(?:te|tos|se)) ', xpre=[ur' il ', ], xpos=[ur' (?:Piccoli|indefinito)', ]) + #192
lema(ur'[Tt]ipograf_í_as?_i', xpre=[ur'Antica ', ur'Milán ', ur'Regia ', ur'Verona, ', ], xpos=[ur' (?:L|do|F\. Grossi|E\. Voghera|dei|Atlântida|Editrice|Rattero|Cipriani, Pescia|Governativa|Pontificia nell|Lo Statuto|Chirio e Mina|M\. Ricci|R\. Istituto|Paccasassi|Savini|Porta|Thurst|Bonazzi|A\.Tomatis|\'Giolitti|classica|Successori|editrice|Luigi Niccolai|dei|dell|della|delle|provinciale|Lineagrafica|Traversa|dellAquila|Bertelli|Guasti|Centrală|Cartea|Macarello|G\. B\. Messaggi|Francesco|Beneditina|seminario|Benedettina|Cardoni|Osservatore|[Nn]azionale|del Reale|Carmignani|del (?:Seminario|Comune)|Giuseppe|Emiliana|Torinese|italo-orientale|Laurenziana|Poliglotta|di|Pioda)\b', ur'\.cl', ]) + #192
lema(ur'[Gg]_é_nero_e', pre=ur'(?:[Ee]l|[Ee]ste|[Un]|[Dd]el?) ', xpre=[ur'[Rr]ío ', ], xpos=[ur'(?:…|\.com)', ]) + #187
lema(ur'[Cc]_ó_digo_o', xpre=[ur'<', ], xpos=[ur' (?:Group|commercial|Manuelino|Afonsino)', ]) + #183
lema(ur'[Dd]iscogr_á_fic[ao]s?_a', xpre=[ur'della Critica ', ]) + #183
lema(ur'[Ee]sp_í_ritus?_i', xpre=[ur'\bdo ', ur'Dark ', ur'Jett C\. ', ur'Nadia ', ur'Sancti ', ], xpos=[ur' (?:vite|da )', ]) + #179
lema(ur'[Kk]il_ó_metros?_o') + #179
lema(ur'Valpara_í_so_i', xpre=[ur'College\|', ur'DTP ', ur'Florida\)\|', ur'Indiana\)\|', ur'Porter en ', ur'Valley ', ur'Vickers ', ur'college = ', ur'etre a ', ur'à ', ], xpos=[ur' (?:Artizan|School|High|Region|athletic|Crusaders|College|Male|Crusaders|Muntanya|Platja|University|\((?:in spanish|Indiana|Florida|Nebraska))', ur'(?:, ?(?:\[\[|)(?:IN|décembre|Indiana|Florida|Nebraska)|[\]\}])', ]) + #177
lema(ur'_é_xitos?_e', xpos=[ur'\.com', ]) + #170
lema(ur'L_í_bano_i', xpre=[ur'\bdal ', ur'\bin ', ur'Andrew ', ur'Bilbao ', ur'Giulio ', ur'Il cedro del ', ur'Medaglia [Cc]ommemorativa ONU ', ], xpos=[ur' Noruega', ]) + #170
lema(ur'[Cc]ronolog_í_as?_i', xpre=[ur'\b[ei] ', ur'Barça del canvi\. Una ', ur'amb la ', ur'd’una ', ur'per a una ', ur'su una ', ur'sulla ', ], xpos=[ur' (?:Ornitologica|Histórica|dei|dell|: les causes|[Cc]ronografia e [Cc]alendario|de Tyrteu|e (?:documentaçom|fortuna)|Prototipi|d\'|d[io] )', ur', [Cc]ronografia e [Cc]alendario', ]) + #167
lema(ur'[Ss]eg_ú_n_u', xpre=[ur'Mabel ', ], xpos=[ur' (?:Owobowale|James|Adeniyi|Lazkano|Adefila|Atere|Amoo|Odegbani|Odegbami|Oluwaniyi|Olumodeji|Michael|Toriola)', ]) + #167
lema(ur'[Pp]resent_ó__o', xpre=[ur'(?:[Mm]e|[Ll]e|[Ll]o|[Tt]e|Vi|Ti|[Oo]s|[Yy]o) ', ur'[Cc][oó]mo ', ur'[Ll]es ', ]) + #165
lema(ur'[Aa]ut_ó_nom[ao]s?_o', xpre=[ur'1465\) ', ur'Comunicació de la Universidad ', ur'Komando ', ur'Regiöes ', ur'Universitat ', ur'[Rr]egiao ', ur'[Rr]egioes ', ur'[Rr]egione ', ur'comune ', ur'teritoriala ', ], xpos=[ur' (?:dei|Volturno|Caccia|carri|delle|Zacatensis|di|recibió|orbita)\b', ur'\]', ]) + #162
lema(ur'[Aa]ll_í__i', xpre=[ur'& ', ur'Bamidele ', ur'Cruz ', ur'Dele ', ur'Jermaine ', ur'Jiménez ', ur'Pier\'', ur'Pier’', ur'Terrence ', ur'Tom y ', ur'Ubbas ', ur'Waheed ', ur'Yusuf ', ur'et ', ur'ki ', ur'þa ', ], xpos=[ur' (?:[0-9]+|y Tom|Forsythe|Ramachari|Sims|Mauzey|Jonathan|fue|Ewichkeit|Kinzel|Abdullahi|Web|Simpson|Nimaiya|Arjuna|[Ll]ettori|Butterman|qarwasha|Mustapha|huomini|Thanda|Biggs|Truch|N\'Dri|Häjänen|Mtinge|Mia|os |gara|Bhandari|kawananchikpaq|Monti|willacuynin|\(novia)', ur'(?:\]|"\'* Bhandari|\'s)', ]) + #160
lema(ur'Tucum_á_n_a', xpre=[ur'Ayres y ', ur'[0-9]', ur'and ', ], xpos=[ur' (?:und|Lawn|Pygmy-owl|Parrot)', ]) + #159
lema(ur'[Aa]lem_á_n_a', xpre=[ur'Allan ', ur'Antonio ', ur'Roberto ', ur'Selva ', ur'[Dl][\'’]', ], xpos=[ur' (?:Cardona|Grup)', ur'\]\]es', ]) + #158
lema(ur'[Cc]a_í_d[ao]s?_i', xpre=[ur'Naga ', ]) + #158
lema(ur'[Ee]lectr_ó_nic[ao]s?_o', xpre=[ur' (?:to|of) ', ur' de \'\'', ur'Ethnic ', ur'Intreprinderea ', ur'Jay ', ur'New ', ur'Palaeontologia ', ur'Project\|', ur'Veronica ', ur'[Aa][Rr][Ss] ', ], xpos=[ur' (?:[1-9]|Mix|[Bb]y|World|Project|Classica|Version|remixe)', ur'(?:\.es|\'s)', ]) + #158
lema(ur'[Pp]odr?_í_a[ns]?_i', xpos=[ur' Acabar o Mundo', ]) + #158
lema(ur'[Ss]u[dr]am_é_rica_e', xpre=[ur'[Ff]rom ', ur'animal\)\|', ], xpos=[ur' (?:Oggi|\((?:género|animal)|ameghinoi)', ur'\]\][a-zñ]+', ]) + #152
lema(ur'Turqu_í_a_i', xpos=[ur' e Síria', ]) + #151
lema(ur'[Jj]apon_é_s_e', xpre=[ur'dos ', ], xpos=[ur'(?:\]\][a-zñ]+|\.cl)', ]) + #150
lema(ur'[Cc]r_é_ditos_e', xpre=[ur'Pizze a ', ur'\blo ', ], xpos=[ur' in\b', ]) + #147
lema(ur'M_é_rida_e', xpre=[ur'Bahr[ae]in[- ]', ur'Joker ', ur'Lampre–', ur'Reyna ', ur'Trencin ', ur'Trenčín ', ur'[Jj]uan ', ur'[Pp]rincesa ', ur'bicicletas ', ur'con ', ur'el \'\'', ur'escocesa ', ur'from ', ur'of ', ur'the Cordillera de ', ], xpos=[ur' (?:Maxillaria|Sunangel|Cycling|Biking|inicia|una nueva|va con|matar|incapaz|Roman|Ladies|Island|Europe|solicita|aprende|Small-eared)', ur', personaje', ]) + #147
lema(ur'Almer_í_a_i', xpre=[ur' di ', ur'5879\) ', ur'Nebraska\)\|', ], xpos=[ur' (?:Star|Lykes|Teatre|Basin|province|\((?:Alabama|Nebraska|Urban))', ]) + #142
lema(ur'[Ii]m_á_genes_a', xpos=[ur' Librorum', ]) + #140
lema(ur'[Oo]l_í_mpico_i', xpre=[ur'Palasport ', ur'Palau ', ur'Profilo ', ur'Stadio ', ], xpos=[ur' (?:di|Nazionale)', ur'\.es', ]) + #140
lema(ur'[Ss]_á_bados?_a', xpre=[ur'Laugh ', ]) + #139
lema(ur'[Ff]otograf_í_an?_i', xpre=[ur' (?:[Dd][ai]) ', ur' e ', ur' i la ', ur'Curs de ', ur'Fragmenta ', ur'I ', ur'Lleida de ', ur'Nuova ', ur'Português de ', ur'Prêmio Nacional de ', ur'da Terra: ', ur'della ', ur'nuova ', ur'ricerche ', ], xpos=[ur' (?:e (?:non|a Agricultura)|Aéreas do|Oltre|[Nn]o |[Dd]i |pittorica|commentata|dell|a Catalunya|\(música|na )', ur'(?:\]\][a-zñ]+|" \(Jobim|\.Islamoriente)', ]) + #138
lema(ur'[Dd]_é_cadas?_e', xpre=[ur'Orbe ', ], xpos=[ur' (?:da|de Orbe Novo)', ur'\'', ]) + #137
lema(ur'T_á_chira_a', xpos=[ur' (?:Emerald|Antpitta)', ]) + #137
lema(ur'Andr_é_s_e', pre=ur'San ', xpre=[ur'\bof ', ur'Fort ', ]) + #134
lema(ur'[Ll]ibrer_í_as?_i', xpre=[ur'Istituto Propaganda ', ur'U[Tt][Ee][Tt] ', ], xpos=[ur' (?:Universitària|Piani|Aeronautica\. Milano|d[\'’]|[Mm]usicale|Cattolica|Serret|Piccolomini|del Mercurio|Milanese|Antiquaria|Gregoriana estense|Internazionale|Scientifica|dello|del Excelentissimo|Croce|Tres i Quatre|Miguel-Creus|[Ee]ditrice|dell|Ed\.)', ]) + #130
lema(ur'[Cc]om_ú_n_u', xpre=[ur'D\'Mente ', ur'\bdi ', ], xpos=[ur' (?:Nuovo|françois)', ur'\. Inst']) + #125
lema(ur'[Dd]ep_ó_sitos?_o', xpre=[ur'(?:[Ii]l|[Ll]a) ', ur'Cardili, ', ur'sepulcro ', ], xpos=[ur' (?:Giordani|da)', ]) + #124
lema(ur'[Rr]a_í_z_i', xpre=[ur'\b[dn]a ', ur'Playsson ', ur'in una ', ur'minha ', ur'músico\)\|', ], xpos=[ur' (?:Records|Music|Tape|madrugada|de Orvalho|Afectuosa|d[aio]|\((?:músico|60))\b', ]) + #124
lema(ur'[Ss]eñor_í_[ao]s?_i', xpre=[ur'Nobiliario de los reinos y ', ]) + #122
lema(ur'[Aa]n_á_lisis_a', xpre=[ur'Pattern ', ], xpos=[ur'[0-9]', ]) + #117
lema(ur'Am_é_rica_e', pre=ur'[Dd]e ', xpre=[ur'[Mm]unicipio ', ur'electoral ', ur'álbum ', ], xpos=[ur' (?:Online|Jackson|One|West|East)', ur'[\'’´]s', ]) + #115
lema(ur'Yucat_á_n_a', xpre=[ur' (?:in|au|of|du) ', ur', & ', ur'Celebrity Mole: ', ur'Chichen Itza, ', ur'Colonial ', ur'Municipio de ', ur'Northern ', ur'Northwest ', ur'[Tt]he ', ur'and ', ur'from ', ], xpos=[ur' (?:peninsula|portal|and|Salamander|Flycatcher|before|pendant|World|Peninsula|[Kk]illifish|Adventure|Township|Jay|Bill|Poorwill|Nightjar|[Vv]ireo)', ur'(?:\.(?:svg|gob)|, & the|[’\']s)', ]) + #115
lema(ur'Potos_í__i', xpre=[ur'Misuri\)\|', ur'Wisconsin\)\|', ur'[Mm]unicipio de ', ur'from San Luis ', ], xpos=[ur' (?:Township|Mountain|Décembre|\(Wisconsin|\(condado|\(Misuri|\(Texas)', ur'(?:\]|, le temps)', ]) + #114
lema(ur'_é_pocas?_e', xpre=[ur' (?:di|ed|in) ', ur' din ', ur'2\.a ', ur'[Aa]ll[\'’]', ur'[Ll]\'', ur'[dl][\'´]', ur'dall[\'’]', ur'nell\'', ur'un\'', ], xpos=[ur' di', ]) + #113
lema(ur'[Ff]_ú_tbol Sala_u') + #113
lema(ur'[Dd]elf_í_n_i', xpre=[ur'Colecciâon Ancora y ', ur'L-29 ', ur'Rietumu-', ur'montti\'\' ', ], xpos=[ur' (?:Vigil|visszanézett|Clutch|Sarl|S\.A\.R\.L)', ur'(?:\]\][a-z]+|\.quishpe)', ]) + #111
lema(ur'Par_í_s_i', pre=ur'[Ee]n ', xpre=[ur'semanal ', ], xpos=[ur' (?:Hill|Review|Parade|Photo|Conservatoire|et al)', ur'\.fr', ]) + #110
lema(ur'[Pp]rop__i[ao]s?_r', xpre=[ur'\b[Èè] ', ur'(?:in|ad|ac) ', ur'Rus ', ur'Albionella ', ur'Cryptantha ', ur'Dubiaranea ', ur'Hogna ', ur'Hogna ', ur'Lithuania ', ur'Lituania ', ur'Meioneta ', ur'Nomina ', ur'Officia ', ur'Rus\' ', ur'T\. ', ur'Tasiocera ', ur'Tous ', ur'Vita ', ur'[Ll][aá]mina ', ur'[Mm]otu ', ur'[Mm]otus ', ur'\be ', ur'calcáreo ', ur'dal ', ur'ecclesia ', ur'ecclessia ', ur'ha una ', ur'hepatica ', ur'hepática ', ur'industria ', ur'iure ', ur'l\'oggetto', ur'manu ', ur'moto ', ur'per ', ur'sei ', ur'spargimento del ', ], xpos=[ur' (?:Tu|orbati|come|Cures|Fiorentina|Sanctorum|SummorumPontificum|come|danno|nombre|albergo|motu|palazzo|vita|giornalismo|teatro, sì|persona|passato|Ecclesia|y Vigarolo|vocat|vigore|pluribus|male|l\')', ur'\]', ]) + #110
lema(ur'Mal_í__i', pre=ur'(?:[Dd]e|[Ee]n) ', xpre=[ur'Culture ', ], xpos=[ur' (?:Ajún|Lo[šs]inj|Ston|Ždrelac|Pek|Shpati|Brezovec|Bukovec|Chekon|Kichmái|Vuković|Tabor|Utrish|Raznokol|Obljaj|Komor|Kozinac|Gradac)', ]) + #107
lema(ur'[Aa]lcald_í_as?_i', xpos=[ur' del Concello', ur'\.santiagoyzaraiche', ]) + #105
lema(ur'Berl_í_n_i', pre=ur'[Dd]e ', xpre=[ur'Philharmonie ', ur'Contrats ', ur'Cour ', ur'Française ', ur'Gemäldegalerie ', ur'Homme ', ur'La Dame ', ur'Mon enfant ', ur'Universitat ', ur'[Mm]icropolitana ', ur'[Mm]unicipio ', ur'canción ', ur'chute ', ur'commune ', ur'cumpleaños ', ur'démons ', ur'mur ', ur'obra ', ur'près ', ur'secrètes ', ], xpos=[ur' (?:Silaen|pour|et|Classics|Dahlem|\([Cc]ondado|Air|Zoologischer)', ur'\.de', ]) + #105
lema(ur'[Aa]h_í__i', xpre=[ur'\b(?:ke|di|nā) ', ur'(?:Lē|Pe)[´\'ʻ]', ur'Elton ', ur'religioso, ', ], xpos=[ur' (?:[\']|che|lasso|poke|Evran|Nazaret|Acre|Ka|dispietata)', ur'(?:\'ezer|quanto|, (?:amors|dispietata)|[\|\'\]]|!(?: Amors|!\'))', ]) + #102
lema(ur'[Rr]_é_gimen_e', xpre=[ur'Ecclesiae ', ur'[Dd]osage ', ur'quo ', ], xpos=[ur' (?:[Ss]anitatis|optimum|Almeriae)', ur', and', ]) + #102
lema(ur'N_á_poles_a', xpre=[ur'secondo, ', ], xpos=[ur', Liguori Editore', ]) + #101
[]][0]

grupo5 = [# 50-99
lema(ur'[Cc]ar_á_tulas?_a', xpre=[ur'[Ss] e', ], xpos=[ur'\.net', ]) + #98
lema(ur'[Ll]_á_grimas?_a', xpre=[ur' e ', ur'[Ff]urtiva ', ], xpos=[ur' Dolly', ]) + #98
lema(ur'[Rr]a_í_ces_i', xpre=[ur'and Musica ', ]) + #98
lema(ur'[Ss]er_á_n_a', xpre=[ur'Deadlands ', ur'Sanjay ', ur'llamada \'\'', ]) + #97
lema(ur'[Dd]_é_ficits?_e', xpre=[ur'Attention: ', ur'Democratic ', ur'Trade ', ur'[Aa]ttention[+ ]', ur'[Bb]udget ', ur'[Tt]he ', ur'\b(?:et|to) ', ur'et non ', ur'polar ', ur'pollination ', ur'this ', ur'totum ', ur'water ', ], xpos=[ur' (?:in|of|angles?|needs|Reduction|Hyperactivity|de Atencao|Review|Tuscana et)\b', ]) + #96
lema(ur'[Rr]_á_pid[ao]_a', xpre=[ur'Euophrys ', ur'Qual ', ur'Roman ', ur'Treno ', ur'plej ', ], xpos=[ur' (?:Trains|carriera|Rock|delle)', ]) + #96
lema(ur'[Dd]iagn_ó_sticos?_o', xpos=[ur' da\b', ]) + #93
lema(ur'Taip_é_i_e', pre=ur'(?:[Dd]e|[Ee]n) ', xpos=[ur' (?:City|Fine)', ]) + #92
lema(ur'[Cc]ient_í_fic(?:as|os?|amente)_i', xpre=[ur'trabalhos ', ], xpos=[ur' (?:classe|da)\b', ]) + #91
lema(ur'Taiw_á_n_a', pre=ur'(?:[Dd]e|[Ee]n) ', xpre=[ur'Pont ', ], xpos=[ur' (?:Taoyuan International|zhi)', ]) + #89
lema(ur'[Pp]_ú_blic(?:os|amente)_u', xpos=[ur' hostes', ur'\'', ]) + #88
lema(ur'[Ff]_ó_rmulas?_o', pre=ur'(?:[Ll]as?|[Uu]nas?|[Dd]e) ', xpre=[ur'quién ', ], xpos=[ur' (?:One|Romani|della)', ]) + #87
lema(ur'[Tt]ecnolog_í_as?_i', xpre=[ur' [aei&] ', ur' in ', ur'Català de ', ur'Ciência e ', ur'do Comércio de ', ur'Contemporâneo de ', ur'Faculdade de ', ur'Fòrum Nord de la ', ur'Investigação para ', ur'Mauá de ', ur'Mediterrani de la ', ur'Mix ', ur'Museu de Ciencia y ', ur'Transferência de ', ur'd[ae]lla ', ur'd[ai] ', ur'e Alta ', ur'e la ', ur'e raciocínio', ur'em ', ur'i la ', ur'importação de ', ur'outras ', ], xpos=[ur' (?:na|ao|em|d[ao]|dei|dell|della|pelo|\(UNIFOR|restauro conservazione|y Ciências|nella|para produzir|Avanzata|educacional: política, histórias|de Informação|del design|de (?:produção|Sementes)|e (?:Ensino|[Gg]overnabilidade|Sociedade|[Gg]estão|Inovação|Políticas|materiali|o homen)|i (?:Cultura|educació))', ur', comunicazione', ur'\. Atti del convegno', ]) + #87
lema(ur'_Á_rea (?:[Mm]etropolitana|[Cc]hica|Natural|Local|[Cc]onurbada|[Bb]iogeogr[áa]fica|[Rr]ecreativa)\b_A', xpre=[ur'l\'', ]) + #86
lema(ur'[Hh]urac_á_n_a', xpos=[ur' (?:Studio|Dive)', ur'\]', ]) + #85
lema(ur'[Vv]_í_nculos?_i', xpre=[ur'[Ss]e ', ], xpos=[ur' Caritatis', ]) + #82
lema(ur'[Dd]_í_a_i', pre=ur'(?:[Hh]oy(?: en|)|[Uu]n (?:buen|cierto|duro|gran|largo|nuevo|s[oó]lo)|[Pp]rimer|[Ss]egundo|[Tt]ercer|[Cc]uarto|[Qq]uinto|[Ss]exto|[Ss][eé]ptimo) ', xpos=[ur' (?:da|e meio)', ]) + #80
lema(ur'[Aa]rqueolog_í_as?_i', xpre=[ur' [ei] ', ur'Congresso de ', ur'Consell de ', ur'Història Antiga y ', ur'Museu Nacional de ', ur'Museu de ', ur'Museude ', ur'Português de ', ur'[LlDd][`’´\']', ur'[Pp]ortuguesa de ', ur'\bda ', ur'd ́', ], xpos=[ur' (?:[Ee]m|da|i|d\'una|es lestiu|de la Generalitat|de Rescat|de Piaçagüera|de Puigcerdà|del paisatge|funerària|I (?:documentació|Universitat)|& Indústria|medieval a Catalunya|medievais|industrial\. Actes|Pré-Histórica|e Etnologia)\b', ur', Arte e História', ]) + #79
lema(ur'[Hh]_é_roes?_e', pre=ur'(?:[Uu]n|[Ee]l|[Ll]os|[Dd]e|en) ', xpos=[ur' [Oo]f', ]) + #78
lema(ur'[Aa]tl_á_nticos?_a', xpre=[ur'369-Vela ', ur'Balco ', ur'Espaço ', ur'Grande ', ur'Passei ', ur'Passeio ', ur'Pavilhao ', ur'l[\'’]', ur'vapor \'', ], xpos=[ur' (?:ao |in |Sul)', ur'\.gov\.co', ]) + #75
lema(ur'[Aa]z_ú_car(?:es|)_u', xpre=[ur' at ', ], xpos=[ur'\]\]ad[ao]s?', ]) + #75
lema(ur'_ha_ (?:dado|debilitado|debutado|deca[ií]do|declarado|decrecido|decretado|dedicado|defendido|dejado|demostrado|denominado|denunciado|derivado|derrotado|desaparecido|desarrollado|descansado|des?cendido|deseado|desclasificado|deseado|desempeñado|desconectado|desfilado|desmentido|desovado|desperdiciado|despertado|despreciado|destacado|detectado|destinado|destruido|detenido|dibujado|dictado|diri[gj]ido|discriminado|disminuido|disputado|distribuido|diversificado|domesticado|dominado|drenado|durado)_ah?', xpre=[ur'[0-9]', ]) + #75
lema(ur'_Á_rea de\b_A', xpre=[ur'Council ', ]) + #74
lema(ur'_C_(hina)_c', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ', xpos=[ur' poblana', ur'\.(?:org|com)', ]) + #73
lema(ur'[Aa]uditor_í_as?_i', xpre=[ur' of ', ]) + #71
lema(ur'[Aa]uditor_í_as?_i', xpre=[ur' of ', ur'en el ', ]) + #71
lema(ur'_é_l (?:anhela|pued[ae]|gana)_e', xpre=[ur'l\'', ]) + #70
lema(ur'_A_rgentina_a', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ', xpre=[ur'\]', ur'\b[Ll]a ', ]) + #69
lema(ur'[Gg]r_á_fica_a', xpre=[ur'Edizioni ', ur'Nova Tecnica ', ur'Torino ', ur'[Nn]os ', ur'[Oo]pera ', ur'\b(?:di|[Ss]e) ', ur'\be ', ur'alla ', ur'della ', ur'estudio ', ur'per la ', ur'que mejor ', ], xpos=[ur' (?:a cura|una? |l[ao]s? |e Editora|European|Gazeta|i disseny|contro|e[ln] )', ]) + #69
lema(ur'_Japó_n_(?:Japo|jap[oó])', pre=ur'(?:[Aa]l?|[Dd]el?|[Pp]ara|[Ee][nl]|[Hh]acia|[Yy]|[Cc]on) ', xpos=[ur' y China desde el anno', ]) + #69
lema(ur'[Aa]utom_ó_vil(?:es|)_o', xpos=[ur' Gesellschaft', ]) + #68
lema(ur'l_í_mites?_i', pre=ur'(?:[Aa]l|[Dd]el|[Ee]l|[Ll]os) ', xpre=[ur'Mondi ', ur'signore ', ]) + #67
lema(ur'[Ss]ant_í_sim[ao]s?_i', xpos=[ur' Anunziata', ]) + #67
lema(ur'[Ss]_í_ndromes?_i', xpre=[ur'Ltd ', ur'Tunnel ', ], xpos=[ur' (?:da|di|florais|Association|lunare)\b', ur'(?:\+|’, ‘Wait)', ]) + #67
lema(ur'Bol_í_var_i', pre=ur'(?:Ciudad|[Ee]stado|[Dd]e|[Ee]n|Edo\.) ', xpre=[ur'Avenue Simon ', ur'Estación ', ur'Marin ', ur'[Cc]ondado ', ur'[Mm]unicipio ', ur'[Pp]enínsula ', ], xpos=[ur' (?:Trask|Award|à Castro)', ur', Australia', ]) + #66
lema(ur'[Hh]ac_í_a[ns]?_i', pre=ur'(?<!\])(?:[Ss]e|[Ll][aeo]s?|[Nn]os|[Mm]e|[Ee]so) ', xpre=[ur'por ', ur'reyno ', ]) + #66
lema(ur'[Ss]_ó_lid[ao]_o', xpre=[ur'Aceria ', ur'Admete ', ur'Alveolina ', ur'Antimima ', ur'Ardisia ', ur'Barteria ', ur'Blowiella ', ur'Borckhausenia ', ur'Bulla ', ur'Capnites ', ur'Capnoides ', ur'Caryophyllia\) ', ur'Corydalis ', ur'Cymbaloporetta ', ur'Davallia ', ur'Dioryche ', ur'Dos ', ur'Eragrostis ', ur'Euphaedra ', ur'Euphaedrana\) ', ur'Euthyonacta ', ur'Fargesia ', ur'Fumaria ', ur'Fusulina ', ur'Gari ', ur'Hastula ', ur'Leptoseris ', ur'Marginulina ', ur'Marginulinita ', ur'Neocyrena ', ur'Nodosarella ', ur'Nososticta ', ur'Pateoris ', ur'Phallomedusa ', ur'Pistolochia ', ur'Planorbulinella ', ur'Planorbulinoides ', ur'Polymesoda ', ur'Porites ', ur'Pseudotristix ', ur'Quinqueloculina ', ur'Ruschia ', ur'Semele ', ur'Single ', ur'Sphera ', ur'Spiroplectina ', ur'Sybra ', ur'[Hh]a ', ur'[Hh]an ', ur'\b[AC]\. ', ur'bat likido ', ur'nisi duos ', ur'septem ', ur'var\. ', ], xpos=[ur' (?:intra solidum|quam)', ur'\'', ]) + #66
lema(ur'[Cc]ad_á_ver_a', xpre=[ur'(?:and| ac) ', ur'Abra ', ur'Polkadot ', ur'[Tt]he ', ur'male ', ur'petit ', ur'tanquam ', ], xpos=[ur' (?:lover|[Ii]n|Productions|decomposition|barroc|\(banda|\(videojuego)', ur'\]', ]) + #65
lema(ur'[Cc]_á_mara_a', pre=ur'(?:[Dd]e|[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Oo]tra) ', xpre=[ur'Sierra ', ], xpos=[ur' (?:Degli|real del prinçipe|de su Magestad)', ]) + #65
lema(ur'[Pp]_ú_blicas_u', xpre=[ur'Divers[õő]es ', ur'T[uú] ', ur'[Qq]ue ', ], xpos=[ur' (?:federais|e Proteção)', ]) + #64
lema(ur'[Qq]uer_í_a[ns]?_i', xpre=[ur'Eu ', ur'Homem que ', ], xpos=[ur' (?:Te Amar|Ventura|dizer|ouvir)', ur'\'', ]) + #64
lema(ur'(?:[Aa]|[Dd]e) _é_l (?:y|como|a|después|la|lo|con)_e', xpos=[ur' Avenue', ]) + #63
lema(ur'[Ff]iscal_í_as?_i', xpos=[ur'\.(?:com|go[bv])', ]) + #63
lema(ur'[Tt]_í_pic[ao]_i', xpre=[ur'Capocollo ', ur'Crycosaura ', ur'Grana ', ur'L\. ', ur'Schwibbogen ', ur'Upogebia ', ur'[Gg]eografica ', ur'[Ii]ndicazione ', ur'terra ', ], xpos=[ur' (?:Sondor|Borgo)', ]) + #63
lema(ur'[Hh]_é_roes? del?_e', xpre=[ur'Als', ur'Sonic ', ], xpos=[ur'Reborn ', ]) + #62
lema(ur'[Ii]nterpret_ó_ (?:el|las?|los|a|por|sus?)_o', xpre=[ur'[Yy]o ', ]) + #62
lema(ur'_ha_ (?:fallecido|favorecido|formado|funcionado|fundado|fusionado|generado|grabado|habido|habilitado|hablado|hecho|implementado|identificado|ido|igualado|impregnado|implementado|impulsado|incendiado|incluido|incrementado|indicado|inducido|informado|ingresado|iniciado|inspirado|instalado|intentado|interesado|interpretado|investigado)_ah?', xpre=[ur'[0-9]', ]) + #61
lema(ur'[Hh]abr_á_[ns]?_a', xpre=[ur'\b(?:de|[Ee]l|[Ll]a) ', ur'Doctor ', ur'Las ', ur'Pearl ', ur'Pieris ', ], xpos=[ur' (?:Nuñez|Bongaon|Romain)', ur'[\'\]]', ]) + #61
lema(ur'[Ss]ovi_é_tic[ao]s?_e', xpre=[ur'E\. ', ur'Euglossa ', ur'Saussurea ', ur'Unione ', ]) + #61
lema(ur'Hait_í__i', pre=ur'(?:\||(?:[Dd]e|[Ee]n) )', xpre=[ur'Démocratie ', ur'Volleyball ', ], xpos=[ur' (?:Sings|and)', ]) + #60
lema(ur'[Ff]_á_brica_a', pre=ur'(?:[Ll]a|[Uu]na?|nueva|antigua) ', xpre=[ur'[Qq]u[eé] ', ur'[Qq]ui[eé]n ', ur'[Ss]e ', ]) + #59
lema(ur'_á_rbol(?:es|)_a', pre=ur'(?:[Ee]l|[Ll]os|[Uu]n|[Uu]nos|[Ee]ste[Ee]stos|[Cc]on|[Dd]e) ', xpos=[ur' que produze', ]) + #58
lema(ur'[Ll]_í_quidos?_i', xpre=[ur'\bnel ', ur'iusto ', ur'phosphoro ', ]) + #58
lema(ur'[Zz]oolog_í_as?_i', xpre=[ur' (?:di|in) ', ur' e ', ur'Arquivos de ', ur'Avulsos de ', ur'Boletim de ', ur'Botanica ', ur'Brasileir[ao] de ', ur'Centrali-Americana, ', ur'Goeldiana ', ur'Iheringia \(', ur'Museu Nacional Rio de Janeiro ', ur'Museu de ', ur'Noções de ', ur'Sér\. ', ur'Série ', ur'avulsos de ', ur'do Departamento de ', ur'séries ', ], xpos=[ur' (?:e a|do |krótko|degli|post |kansalaisille|medicinalis|Baetica|fantástica do|Neocaledonica|i ecologia|Adriatica, ossia|specialis)', ur', Lisboa', ]) + #58
lema(ur'_á_lgebras?_a', xpre=[ur'Clifford ', ur'Combinatory ', ur'Commutative ', ur'Die ', ur'Lie ', ur'Moody ', ur'Riemann-Roch ', ur'Undergraduate ', ur'Vertex ', ur'Virasoro ', ur'Witt ', ur'[Aa]ssociative ', ur'[Bb]oolean ', ur'[Cc]omputer ', ur'[DdLl][’\']', ur'[Hh]omological ', ur'[Hh]ypercomplex ', ur'[Ll]inear ', ur'[Mm]atrix ', ur'[Rr]eal ', ur'\b(?:of|to|[ai]n|as) ', ur'\bs ', ur'about ', ur'and ', ur'differential ', ur'group ', ur'maior, ', ur'operator ', ur'particles, ', ur'relational ', ur'the ', ], xpos=[ur' (?:graded|for|from|and|of|em|et)\b', ur'(?:\]|, geometry)', ]) + #57
lema(ur'[Aa]c_ú_stic[ao]s?_u', xpre=[ur'Ars ', ur'Versione ', ur'dell\'', ], xpos=[ur' for', ur'\'\'', ]) + #56
lema(ur'Afganist_á_n_a', xpre=[ur'Azadi ', ur'L\'', ]) + #56
lema(ur'Lan_ú_s_u', xpos=[ur'\.com', ]) + #55
lema(ur'[Mm]atem_á_tic[ao]_a', xpre=[ur'Analisi ', ur'Composito ', ur'Incontri con la ', ur'L’officina ', ur'Unione ', ur'\bdi ', ur'\be ', ur'\bin ', ur'\btra ', ur'analisi ', ur'and: ', ur'della ', ur'esposizione ', ur'ricerca ', ur'speculativo ', ur'viaggio con la ', ], xpos=[ur' (?:dell|italiana|Applicata|nella|la Realta|e (?:a|di|la sua|Cultura) |a scuola|napoletano|nella|oggi|di)\b', ur'(?:[+]|", A: Roero|: (?:I Numeri|La Geometr[ií]a)|\. (?:Scandicci|6 volumetti)|\'\' \(Burali)', ]) + #55
lema(ur'[Ee]con_ó_mico_o', xpre=[ur'Barometro ', ur'stato ', ur'sviluppo ', ], xpos=[ur' (?:Brasileiro|della|in|di|e (?:downturn LGD|nel))', ]) + #54
lema(ur'[Ii]nform_á_tica_a', xpre=[ur'Acta ', ur'Athenas ', ur'Contabilitate si ', ur'Sociaal-Wetenschappelijke ', ur'Wiskunde & ', ], xpos=[ur' (?:i |Particolare|Corporation|per )', ur' e (?:Diritto|internet per)', ]) + #54
lema(ur'_ha_ (?:ca[ií]do|calculado|calificado|cambiado|cantado|capacitado|capturado|caracteri[sz]ado|cargado|casado|catalogado|catapultado|categorizado|catequizado|causado|cedido|celebrado|cerrado|clasificado|cobrado|coincidido|colaborado|colgado|colocado|colonizado|combatido|comentado|cometido|comenzado|compaginado|compartido|compensado|competido|complacido|comprobado|comunicado|concedido|condenado|conducido|confesado|confiado|confirmado|conformando|confundido|congelado|congregado|conquistado|consagrado|conseguido|conservado|considerado|consolidado|consumido|contactado|contestado|continuado|contribu[ií]do|convenido|convertido|convocado|cooperado|copiado|coreografiado|coronado|corregido|correspondido|cortado|cosechado|cotizado|creado|crecido|cre[ií]do|cruzado|cumplido|cursado)_ah?', xpre=[ur'[0-9]', ]) + #53
lema(ur'[Mm]ar_í_tim(?:as|os?)_i', xpre=[ur'Museu ', ]) + #53
lema(ur'[Pp]aleontolog_í_as?_i', xpre=[ur' da ', ur' e ', ur'Brasileir[ao] de ', ur'Català de ', ur'Institut de ', ur'Trabalho de ', ur'di ', ur'i la ', ], xpos=[ur' (?:em |Electronica|Africana|Lombarda|E Stratigrafia|i Evolució\')', ]) + #53
lema(ur'[Hh]onor_í_fic[ao]s?_i', xpre=[ur'T\. ', ur'Tipula ', ur'[Ss]e ', ]) + #51
lema(ur'[Gg]astronom_í_as?_i', xpre=[ur'\be ', ur'Art i ', ], xpos=[ur' Elkartea', ]) + #50
lema(ur'_h_oland[eé]s_H', pre=ur'\b(?:e[ln]|del?|idioma|y) ', xpre=[ur'Diplomado ', ], xpos=[ur' (?:[Ee]rrante|[Vv]olador)', ]) + #50
lema(ur'[Ii]nfanter_í_as?_i', xpre=[ur'd\'', ], xpos=[ur' de marinha', ]) + #50
lema(ur'[Pp]_á_jaros?_a', xpos=[ur' Dunes', ]) + #50
lema(ur'[Pp]rime_r_[ao]s?_', xpre=[ur'Discovery ']) + #65
[]][0]

grupo6 = [# 25-49
lema(ur'[Cc]_í_rculos?_i', pre=ur'(?:[Dd]el|[Ee]l|[Ll]os|[Uu]n|[Uu]nos|[Aa]lgunos) ', xpos=[ur' sportivo', ]) + #49
lema(ur'_Á_cid[ao]s?_A', xpre=[ur'Monte ', ur'Probierstein de ', ur'\bdi ', ur'sine ', ], xpos=[ur' (?:220|Mc|pyro-tartarico pars I|remix|Clhoe)\b', ]) + #48
lema(ur'_Á_rboles_A', xpre=[ur'[0-9]', ], xpos=[ur' \(Colorado', ur'\]', ]) + #47
lema(ur'[Ii]deolog_í_as?_i', xpre=[ur' i ', ur'L\' ', ur'Primário e ', ur'[Pp]assione e ', ur'com a ', ur'dell[\'’]', ur'di Nuraghe. Simbolismo e ', ur'edició, ', ur'id "', ur'scienze e ', ], xpos=[ur' (?:garaikide|della|nell|dominante na|i (?:cultura|il\.lustrada|la)|e (?:politica|[Pp]rática)|(?:d[ao]|in|ou) )', ur'\'\', cortometraje', ]) + #47
lema(ur'[Mm]ec_á_nic[ao]_a', xpre=[ur' é ', ur'scienza ', ], xpos=[ur' Records', ]) + #47
lema(ur'[Ff]otograf_í_as_i', xpre=[ur'Mostra de ', ur'Três ', ur'[nd]ella ', ], xpos=[ur' (?:e Músicas|com|pittorica|commentata|e non|[Dd][io] |[dn]a )', ]) + #46
lema(ur'[Mm]_á_gico_a', xpre=[ur'Il carillon ', ur'Il momento ', ur'Il totem ', ur'L\'anello ', ur'L\'astro ', ur'Occhio ', ur'Tocco ', ur'Tripp ', ur'Veicolo ', ur'[Mm]ondo ', ur'[Tt]reno ', ur'amico ', ur'antro ', ur'cerchio ', ur'corno ', ur'flauto ', ur'regno ', ur'storia del Pifferaio ', ur'uccello ', ], xpos=[ur' (?:di|eroe|Lilo|Vento|Bonding|connubio|Veneto|Antico Oriente|e altri)', ]) + #46
lema(ur'[Aa]ct_ú_a_u', xpos=[ur' (?:Sports|Pool|Golf|Ice|[Ss]occer|Tennis)', ]) + #44
lema(ur'[Aa]rt_í_culos_i', xpre=[ur'XXXIX ', ]) + #44
lema(ur'[Aa]utor_í_as?_i', xpre=[ur'1985, ', ur'[dl][’\']', ur'd\'Autor 2014 - ', ur'disputam ', ur'sua ', ], xpos=[ur' e produção', ]) + #44
lema(ur'est_á_ bajo_a', xpre=[ur'[Aa] ', ]) + #44
lema(ur'[Jj]ur_í_dic[ao]_i', xpre=[ur'[Oo]pera ', ur'esperienza ', ]) + #44
lema(ur'[Aa]natom_í_as?_i', xpre=[ur' d[ai] ', ur' e ', ur'[Cc]orporis ', ur'[Hh]umani ', ur'd[’\']', ur'das plantas ', ur'dell\'', ur'pela ', ], xpos=[ur' (?:auri|Hvmani|Mundini|de raízes|Patológica e Medicina|patologica di|Plantarum|Vegetal\. Viçosa|[Cc]omparata|[Uu]mana|comparada (?:das|do)|corporis|foliar|generalis|hummingbird|microscopica corporis|partium|pharmaceutica|półprawd|sistematica|uteri|Vitrioli|d[aio] |dos|del (?:Vitrioli|somni|[Cc]avallo)|comparada da|e (?:fisiologia|[Mm]orfologia|ontogenia|relações|sistematica)|de (?:la relativitat|uma|espécies)|d[’\']un)', ]) + #44
lema(ur'Ben_í_n_i', pre=ur'(?:[Dd]e|[Ee]n) ', xpre=[ur'Dame ', ur'et ', ], xpos=[ur' (?:City|Golf|jusqu)', ]) + #43
lema(ur'Berl_í_n_i', pre=ur'(?:[Ee]n|y|o) ', xpos=[ur' (?:Dahlem|Air)', ur'\.de', ]) + #43
lema(ur'[Ff]_é_rtil(?:es|)_e', xpre=[ur'J\. ', ur'Reprod ', ur'Terres ', ur'[Yy]eux ', ur'plu ', ur'vallées ', ], xpos=[ur' (?:Grass|Steril|Women|SteriI)', ur'\. Steril', ]) + #43
lema(ur'Han_ó_i_o', pre=ur'(?:[Dd]e|[Ee]n) ', xpos=[ur' (?:Rocks|Jane|Securities|Road)', ]) + #43
lema(ur'[Oo]_í_dos?_i', xpos=[ur' \(Metro', ]) + #43
lema(ur'[Pp]_ó_stum[ao]_o', xpre=[ur'Apologo ', ur'Atilio ', ur'Cephaloleia ', ur'Lucio ', ur'Poenio ', ur'Vibio ', ur'pubblicato ', ], xpos=[ur' (?:dello|Megelo|se suicidó|Dardano)', ]) + #43
lema(ur'[Cc]_iu_dad(?:es|)_ui', xpre=[ur'Fabrice ', ], xpos=[ur' de hacerle', ]) + #42
lema(ur'[Dd]ecidi_ó_(?! Saxa)_o', xpre=[ur'un ', ]) + #42
lema(ur'_ha_ (?:absorbido|acabado|aceptado|acercado|acertado|acordado|acosado|acostado|actuado|actualizado|acogido|acompañado|acreditado|adoptado|acudido|acumulado|acusado|adaptado|adjudicado|adquirido|afectado|afiliado|afirmado|agotado|agredido|albergado|alcanzado|alternado|amado|ampliado|anotado|anunciado|aparecido|aplicado|aportado|apostado|apoyado|aprendido|argumentado|armado|atrapado|arrojado|ascendido|asegurado|asesinado|asistido|atendido|atormentado|atra[ií]do|at(?:ar|ra)vesado|atribuido|aumentado|ayudado)_ah?', xpre=[ur'[0-9]', ]) + #42
lema(ur'[Ll]_á_mparas?_a', xpre=[ur'Astronesthes ', ur'Wishing ', ur'[A]\. ', ]) + #42
lema(ur'[Mm]_á_xim[ao]s?_a', pre=ur'(?:[Ee]l|[Ll][ao]s?|[Ss]u|[Uu]na?|[Pp]unto) ', xpos=[ur' (?:debutó|anteriores)', ]) + #42
lema(ur'[Oo]rg_á_nic[ao]_a', xpre=[ur'Lei ', ur'Modulatio ', ur'e materia ', ur'pianificazione ', ur'sostanza ', ]) + #42
lema(ur'[Tt]endr_á__a', xpre=[ur'Barcelona ', ur'Golfo ', ur'[Ii]sla ', ur'de ', ], xpos=[ur' Risant', ur'\]\]', ]) + #42
lema(ur'[Aa]si_á_tic(?:as|os?)_a', xpre=[ur'ad Plantas ', ]) + #41
lema(ur'[Pp]rop_ó_sitos?_o', xpre=[ur'fermo ', ], xpos=[ur' (?:dell|di|pellimur)', ]) + #41
lema(ur'L_é_rida_e', xpre=[ur' i ', ], xpos=[ur' ostroma', ]) + #39
lema(ur'[Aa]_ _pesar_', xpos=[ur' (?:do|de você)\b', ur'\'\'', ]) + #38
lema(ur'[Aa]utonom_í_as?_i', xpre=[ur'Euskal ', ur'[DdLl][’\']', ur'\b[aei] ', ur'per \'', ], xpos=[ur' (?:and|e (?:solidarietà|socialismo)|i (?:Benestar|centralisme)|Integrale|Operaia|possible|galega)', ur'(?:\.­htm|: Post-Political)', ]) + #38
lema(ur'[Cc]aser_í_o_i', xpre=[ur'Alberto ', ur'Carlos ', ur'Ger[óo]nimo ', ur'Jesús ', ur'Jorge ', ur'Mathías ', ur'Nick ', ur'Sante ', ur'Ulderino ', ur'a ', ur'italiano ', ], xpos=[ur' (?:vivió|acuchilló|describiría|fue)', ur'[]|\']', ]) + #38
lema(ur'[Tt]ur_í_stico_i', xpre=[ur'Consorzio ', ur'Guida ', ur'Porto ', ur'Società Incremento ', ], xpos=[ur' (?:ufficiale|della|Cinque|Acores)', ]) + #38
lema(ur'[Ff]_á_brica_a', pre=ur'[Dd]e ', xpos=[ur' (?:Mvndi|[Mm]undi|Machinarum)', ]) + #37
lema(ur'[Pp]roh_í_be[ns]?_i', xpos=[ur' el Emmo', ]) + #37
lema(ur'[Aa]rtesan_í_as?_i', xpre=[ur'Asociació ', ur'l[\'’]', ], xpos=[ur'(?:, (?:Alcantara|Almansa|Via|C/)|: Art )', ]) + #35
lema(ur'[Aa]_ travé_s_trav[eé]', xpos=[ur' (?:da|dos?|editora|de um)\b', ]) + #35
lema(ur'[Cc]r_é_dito_e', xpre=[ur'\bdi ', ], xpos=[ur' (?:in|Italiano|Artigiano|Valtellinese|Bergamasco|Emiliano|and|per|Varessino|Esattorie)', ]) + #35
lema(ur'[Ee]star_á_[ns]?_a', xpre=[ur'Xiphias ', ], xpos=[ur' Ferragut', ]) + #35
lema(ur'[Pp]ur_í_sim[ao]s?_i', xpre=[ur'Cesar ', ur'Mission La ', ], xpos=[ur' Mission', ]) + #35
lema(ur'[Pp]roblem_á_tic[ao]s?_a', xpre=[ur'Cypraea ', ur'Jivaromyia ', ur'Leedsia ', ur'Lygrommatoides ', ur'Marginulina ', ur'Mordellina ', ur'Propercarina ', ur'Purcelliana ', ur'R\. Brickellia ', ur'Rhophodon ', ur'Thopeutica ', ], xpos=[ur' traducerii', ur'\'', ]) + #34
lema(ur'[s]er_á__a', pre=ur'(?:[Qq]ui[ée]n|[Qq]u[ée]|[Dd][óo]nde|[Cc]u[áa]ndo|[Tt]ambién|[Aa]demás|[Ss]e|[Ll]os?) ', xpre=[ur'de ', ], xpos=[ur' (?:Marz|[Ss]era)', ur', sera', ]) + #34
lema(ur'[Aa]ut_ó_dromo_o', xpre=[ur'dell\'', ur'spider ', ], xpos=[ur' (?:di|Nazionale|Internazionale|Enzo e Dino Ferrari|de (?:Portimao|Umbria))', ]) + #33
lema(ur'[Ee]limin_ó__o', xpre=[ur'[Yy]o ', ur'[Yy]o los ', ]) + #33
lema(ur'[Ee]vang_é_lica_e', xpre=[ur'Dubia ', ur'Chiesa ', ur'Demonstratio ', ur'Harmonia ', ur'Iosephina ', ur'Lux ', ur'Perfectione ', ur'Praeparatio ', ur'Preparatio ', ur'Studia ', ur'praedicatione ', ], xpos=[ur' (?:Beati|Praeparatione|libertate|et|e Documentazione|a Georgio)', ]) + #33
lema(ur'[Hh]oland_é_s_e', xpre=[ur'permitió que el ', ]) + #32
lema(ur'[Ll]oter_í_as?_i', xpre=[ur'Caixa ', ], xpos=[ur' (?:Vella|sem)', ]) + #32
lema(ur'[Rr]e_í_r(?:se|)_i', xpos=[ur'\'', ]) + #32
lema(ur'[Tt]ur_í_stica_i', xpre=[ur'accoglienza ', ur'Consociazione ', ur'Promozione ', ], xpos=[ur' (?:della|del Tigullio)', ]) + #32
lema(ur'[Aa]post_ó_lico_o', xpre=[ur'Missionario ', ur'Nunzio ', ur'Palazzo ', ur'Pellegrino ', ur'amministratore ', ur'ex ', ], xpos=[ur' (?:[Mm]uneri|Seggio|di Bologna|San Michele)', ]) + #31
lema(ur'[Cc]_á_maras_a', xpre=[ur' as ', ]) + #31
lema(ur'[Dd]ir_á_[ns]?_a', xpre=[ur' (?:on|El|ne) ', ur' nun ', ur'Elle le ', ur'Ledisi, ', ur'Oya ', ur'Plaza ', ur'Qui ', ur'Tal\'', ur'aipatzekoak ', ur'arindu ', ur'errian ', ur'kontuak ', ur'matxinatu ', ur'ne le ', ur'qui la ', ur'vous ', ], xpos=[ur' (?:cristau|inoiz|Hitzak|Lehaskir|Paes|miraballesen|egiazko|besteak|notre|pezetan|ito|Yulianti|Sugandi|Alexanian|Stevsson|Oyelade|Kelekian|Noubar|Sarkissian|Airways|de lui)', ur'(?:[\'\)]|, (?:huato|"muchos|che))', ]) + #31
lema(ur'[Pp]atri_ó_tic[ao]s?_o', xpre=[ur'Ação ', ], xpos=[ur' di\b', ]) + #31
lema(ur'_Á_reas?_A', pre=ur'[Dd]e ', xpre=[ur'María ', ur'Punta ', ur'[Ee]stación ', ur'[Ii]nsua ', ur'[Ii]sla ', ur'[Pp]arroquia ', ur'[Pp]laya ', ur'praia ', ]) + #30
lema(ur'_e_ll[ao]s?_é', xpos=[ur' llos ', ]) + #30
lema(ur'[Ff]_é_mur_e', xpre=[ur'Abogado de ', ur'Bonita ', ur'Freddie ', ur'Neandertal \[\[', ur'Rural \(', ur'\.\.\. ', ur'\b[Tt]he ', ur'\bof ', ur'left ', ur'super ', ], xpos=[ur' (?:and)', ur'\+head', ]) + #30
lema(ur'[Aa]sesor_í_as?_i', xpre=[ur'polaco: \'\'', ]) + #29
lema(ur'[Aa]yud_ó__o', xpre=[ur'(?:[Yy]o|[Tt]e) ', ur'Nunca ', ur'Vengo y ', ], xpos=[ur' (?:a (?:porque|papá a|mi madre|Fabri|verte|mamá a|limpiar la|un extranjero|armar los|la gente|mi señor|las libreras)|porque|Gutiérrez)', ur', javier', ]) + #29
lema(ur'_Á_reas?_A', pre=ur'(?:[AaEe]l|[Ll]as?|[Uu]nas|[Dd]el|[Uu]n|[Cc]ada|[Ss]us|[Oo]tras?) ', xpos=[ur' (?:Council|Mix|Sacra)', ]) + #29
lema(ur'_B_rasil_b', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ', xpre=[ur'viene ', ], xpos=[ur' natal', ]) + #29
lema(ur'[Dd]ar_á_[ns]_a', xpre=[ur' (?:de|et|[Nn]e) ', ur'André ', ur'Barb\' ', ur'Bayt ', ur'Beit ', ur'Charles ', ur'Dee ', ur'Denk ', ur'Glaub\' ', ur'José ', ur'Navarro ', ur'[Nn]ichts ', ], xpos=[ur' (?:dice|Bina|Norris|Little|Holt|Morrison|V\.|Maisutā|hindert|erinnert|Publishing)', ur'(?:[\)\]]|, (?:al|Clémansin|dass|gavilán|presidente|che))', ]) + #29
lema(ur'[Ii]rland_é_s_e', xpos=[ur'\]\][a-z]+', ]) + #29
lema(ur'[Aa]nal_í_tica_i', xpre=[ur'della psicologia ', ur'di [Pp]sicologia ', ur'e geometrica ', ur'relazione ', ur'terapia ', ], xpos=[ur' (?:d|do|ed|ragionata|Priora)\b', ur'(?:\.com|: Reflexão)', ]) + #28
lema(ur'[Dd]isc_í_pul[ao]s?_i', xpre=[ur'[Ss]uo ', ], xpos=[ur' (?:eique|perusinos|fidelissime)', ]) + #28
lema(ur'[Gg]r_á_fic(?:[ao]s|amente)_a', xpre=[ur'Comunicacio ', ur'Nos ', ur'escribe o ', ur'escribe o ', ], xpos=[ur' (?:del Parteolla|Five)', ]) + #28
lema(ur'[Ss]erv_í_an_i', xpre=[ur'Cristian ', ur'Guillermo ', ur'Nadia ', ur'Yasmine ', ur'de ', ur'hermanos ', ], xpos=[ur' (?:verbi|Giosa|\'\'\')', ur'\]\]', ]) + #28
lema(ur'[Dd]i_á_logo_a', pre=ur'(?:[Ee]l|[Uu]n|[Ss]u) ', xpos=[ur' (?:di|scientifico)', ]) + #27
lema(ur'[Tt]_á_ndems?_a', pre=ur'\b(?:[Ee]l|[Uu]n|del|en|tipo|con|haciendo|formando|formó|equipos|Velocidad|legendario|gran|cabinas|club|[Bb]uses|ajedrez) (?:\[\[||)', xpre=[ur'Tm para ', ], xpos=[ur' (?:Fundazioa|open|Computers)', ]) + #27
lema(ur'[Ee]nfermer_í_as?_i', xpos=[ur'\.uady', ]) + #26
lema(ur'[Ff]_í_sic[ao]s_i', xpre=[ur'difetto ', ], xpos=[ur' (?:i politica|e matematica|riduzione)', ur'(?:\.ru|\.png|" e "Del)', ]) + #26
lema(ur'[Ll]og_í_sticas?_i', xpre=[ur'Cecchi ', ur'Fruit ', ur'Rad ', ur'Varig ', ], xpos=[ur' até', ]) + #26
lema(ur'[Tt]ra__stornos?_n', xpos=[ur' mentais', ]) + #26
lema(ur'[Ss]_ó_rdida_o', xpre=[ur'Achillea ', ur'Aegiphila ', ur'Agave ', ur'Anemone ', ur'Apatura ', ur'Ardisia ', ur'Argia ', ur'Atriplex ', ur'Ballota ', ur'Bartlettina ', ur'Basselinia ', ur'Bodilopsis ', ur'Bolbophyllaria ', ur'Callicarpa ', ur'Calyptranthes ', ur'Carex ', ur'Centaurea ', ur'Centemopsis ', ur'Cercomela ', ur'Chamaesaracha ', ur'Chitoria ', ur'Chloroclystis ', ur'Coryogalops ', ur'Coryogalops ', ur'Diclidia ', ur'Dyckia ', ur'Edithcolea ', ur'Eria ', ur'Erioptera ', ur'Eulophia ', ur'Eumyias ', ur'Gochnatia ', ur'Hymenandra ', ur'Indigofera ', ur'Iris ', ur'Isoperla ', ur'Jungia ', ur'Larnax ', ur'Monoxia ', ur'Muscicapa ', ur'Nectandra ', ur'Nectandra ', ur'Nemosia ', ur'Neobartlettia ', ur'Odostomia ', ur'Orobanche ', ur'Palmorchis ', ur'Paracaesio ', ur'Physalis ', ur'Pinarochroa ', ur'Pitcairnia ', ur'Pitta ', ur'Pleurothallis ', ur'Pluchea ', ur'Podagricomela ', ur'Pomacea ', ur'Pomacea\) ', ur'Pseudoraphis ', ur'Psychotria ', ur'Pteronia ', ur'Roentgenia ', ur'Salvia ', ur'Sansevieria ', ur'Saussurea ', ur'Schinia ', ur'Scytodes ', ur'Smilisca ', ur'Specklinia ', ur'Stigmatopteris ', ur'Thlypopsis ', ur'Tillandsia ', ur'[ABPEMNDTCls]\. ', ur'lavat ', ur'molinae ', ur'obscura ', ur'sordida ', ur'subsp\. ', ur'var\. ', ], xpos=[ur' struma', ]) + #26
lema(ur'_á_cid(?:as|os?)_a', xpre=[ur'\bdi ', ur'l[’\']', ], xpos=[ur' pyro-tartarico pars I', ]) + #25
lema(ur'[Ff]en_ó_meno_o', xpre=[ur'NIFO‑', ur'\bO ', ur'\b[Ii]l ', ur'come ', ur'comesviluppo del ', ur'sviluppo del ', ], xpos=[ur' (?:di|Esperanto|paranormale|radiante cerebropsichico|sociale)\b', ur'\.com', ]) + #25
lema(ur'[Mm]iscel_á_ne[ao]s?_a', xpos=[ur' (?:Antwerpiensia|Barcinonensia|taxinomica)', ]) + #25
lema(ur'[Pp]ertenec_í_(?:a[ns]?|)_i', xpre=[ur'(?:[Ll]as|[Ss]us) ', ur'(?:[Ll]a|[Dd]e|[Ss]u) ', ]) + #25
[]][0]

grupo7 = [# 1-24
lema(ur'[Ee]sp_e_cies?_a', xpos=[ur' sus']) + #16
lema(ur'[Aa]rchidi_ó_cesis_o', xpos=[ur' (?:Turritanus|Praetoriensis|Bisuntinis|Limanus)', ]) + #24
lema(ur'[Cc]l_í_max_i', pre=ur'(?:[Ee]l|[Uu]n|de|en|su) ', xpre=[ur'Situación ', ur'[Mm]unicipio ', ur'anual ', ur'cartucho ', ur'fama ', ur'residiendo ', ]) + #24
lema(ur'[Cc]_ó_nclaves?_o', xpre=[ur'Caribbean ', ur'Magic, ', ur'Papal ', ur'Piano ', ur'Tenor ', ur'The ', ur'Triennial ', ur'[Ii][ls] ', ur'des ', ur'papal ', ur's ', ], xpos=[ur' (?:of|visentibus|& Earshot)', ]) + #24
lema(ur'[Gg]al_á_ctic[ao]s?_a', xpre=[ur' (?:la|of) ', ur'2004\)\|', ur'Agua \(', ur'Aria ', ur'Battlestar ', ur'Battlestar "', ur'Battlestar\]\] ', ur'Ephemeroptera ', ur'Galactica\|', ur'Hyde ', ur'Imperium ', ur'Invaders ', ur'Pirámide \(', ur'Saddlesore ', ur'Saddlessore ', ur'Sadlessore ', ur'Shadow ', ur'\ba ', ur'como ', ur'marca ', ], xpos=[ur' (?:e[ns] |Donut|Discovers|Plants|Myosotis|Tornado|Tsunami|Crunch|Magnum|reúne|Year|Inflation|Scales|Superstring|1980|\((?:voz|nave))', ur'(?:\)\||\'\'|: The|, [Aa]stronave)', ]) + #24
lema(ur'[Pp]resb_í_ter[ao]s?_i', xpre=[ur'F\. ', ]) + #24
lema(ur'[Dd]ur_ó_ (?:m[aá]s |[0-9+]+)_o', xpre=[ur'[Dd]isco ', ur'[Rr]ock ', ur'caparazón ', ur'de a ', ur'de un ', ur'golpeó ', ur'metal ', ]) + #23
lema(ur'[Ff]an_á_tic[ao]s?_a', xpre=[ur'1589\) ', ur'Il ', ], xpos=[ur' (?:se designó|orbita|Films|per|\(Club)', ur'\]', ]) + #23
lema(ur'[Gg]arant_í_as?_i', xpre=[ur' e ', ur' em ', ur'Banco ', ]) + #23
lema(ur'[Mm]atem_á_ticas_a', xpre=[ur' d[ae]s ', ur'es\.ciencia\.', ], xpos=[ur'\.(?:unmsm|uady)', ]) + #23
lema(ur'[Pp]arec_í_a[ns]?_i', xpos=[ur' Não', ]) + #23
lema(ur'[Aa]lfab_é_tic(?:[ao]s?|amente)_e', xpre=[ur'Sull\'', ]) + #22
lema(ur'[Ee]vang_é_lic(?:as|os?)_e', xpre=[ur'Cantore ', ur'Si ', ur'movimento ', ]) + #22
lema(ur'[Ii]n_é_dit[ao]s_e', xpre=[ur'corrispondenza ', ur'tum ', ]) + #22
lema(ur'[Pp]orter_í_as?_i', xpre=[ur'Diari de la ', ur'OJ ', ], xpos=[ur' (?:albopunctata|escapulada està)', ]) + #22
lema(ur'[Vv]olver_á_[ns]?_a', xpre=[ur'Gilberto ', ], xpos=[ur'\]', ]) + #22
lema(ur'[Zz]ool_ó_gicos?_o', xpre=[ur' e ', ur'Monitore ', ], xpos=[ur' (?:dell|La Specola|di )', ]) + #22
lema(ur'[Aa]cad_é_mico_e', xpre=[ur'Concerto ', ur'Iure ', ur'Mauri ', ur'[Aa]nno ', ur'horto ', ], xpos=[ur' (?:dell|Viseu|Hauniensi|FC|Do)', ]) + #21
lema(ur'[Aa]cu_á_tic[ao]s?_a', xpre=[ur'f\. ', ], xpos=[ur' Milan', ]) + #21
lema(ur'[Aa]scen_s_ión_c', xpos=[ur' (?:Aguilera|[AÁ]lvarez|Alcalá|Andrade|Bonet|De los Santos|Farreras|García|Gómez|Hernández|Lencina|López|Martínez|Negrón|Nicol|Orihuela|Saucedo|Soto|Solórsano|Tepal|Vázquez)', ]) + #21
lema(ur'[Cc]l_í_nico(?! (?:di))_i', xpre=[ur'Nico ', ur'lavoro ', ]) + #21
lema(ur'[Dd]ram_á_tic[ao]_a', xpre=[ur'Encyclopedia ', ur'Encyclopædia ', ur'Lento e ', ur'Ouverture ', ur'favola ', ur'mezzosoprano ', ], xpos=[ur'Cascais ', ]) + #21
lema(ur'[Ee]_n_ (?:el|l[ao]s?|una?|unos?|varios|algun[ao]s?)_m', xpos=[ur' papel de \'\'Brunilda', ]) + #21
lema(ur'[Ee]tnograf_í_as?_i', xpre=[ur' e ', ur'd[\'’]', ur'falações de variantes ', ], xpos=[ur' (?:[Pp]ortuguesa|religiosa e psicanálise|brasileira|e Folclore|del tarantismo pugliese|do )', ]) + #21
lema(ur'_é_l van?_e', xpos=[ur' (?:escometre|parir|Helsing|dame)', ur'\.ran', ]) + #21
lema(ur'est_á_ muert[ao]_a', xpre=[ur'[Dd]e ', ]) + #21
lema(ur'[Rr]om_á_ntico_a', xpre=[ur' e ', ur' rom ', ur'Concerto ', ur'Essere ', ur'Operachi ', ur'[Mm]elodramma ', ur'[Qq]uartetto ', ur'[Tt]rio ', ur'amore ', ur'bacio ', ur'belcanto ', ], xpos=[ur' (?:blues|Rock|Bosanova|e mistico)', ]) + #21
lema(ur'[Tt]ra_í_as?_i', xpre=[ur'Is ', ], xpos=[ur' del Gofio', ]) + #21
lema(ur'[Ff]isiolog_í_as?_i', xpre=[ur'\b[ei] ', ], xpos=[ur' (?:umana|vegetale|comparate|dell|dos|aeroespacial : conhecimentos)', ur', taxonomia, ecologia e gen[eé]tica', ]) + #20
lema(ur'G_é_nova_e', pre=ur'(?:[Dd]e|[Ee]n|para|desde) ', xpre=[ur'Camogli ', ur'Pallavicino ', ], xpos=[ur', Nicholas', ]) + #20
lema(ur'Ir_á_n_a', pre=ur'(?:[Dd]e|[Ee]n) ', xpre=[ur'Francaises ', ur'Française ', ur'Pasquier ', ur'Recherche ', ur'Recherches ', ur'San Clemente ', ur'historiques ', ur'peinture ', ], xpos=[ur' (?:Air|Aseman|Chamber|Telecommunications|et)', ]) + #20
lema(ur'[Tt]e_ó_ric[ao]_o', xpre=[ur'Sulla ', ur'dal fisico ', ur'modello ', ], xpos=[ur' (?:dell|degli|fino|- pratica|e pratico)', ur', dall', ]) + #20
lema(ur'[Vv]_á_lvulas?_a', xpre=[ur'Elaver ', ], xpos=[ur' venae', ]) + #20
lema(ur'Am_é_rica_e', pre=ur'[Ll]a ', xpre=[ur'Faremo ', ], xpos=[ur' (?:Cantat|3|Online|do|RJ|East|West|on|Actors|Society)', ur'[\'’´]s', ]) + #19
lema(ur'[Cc]_á_psulas?_a', xpre=[ur'Capsula\|', ur'City ', ur'Italdesign ', ur'Ogasawarana ', ur'Romeo ', ur'Stelis ', ur'Zelotes ', ur'\b[O]\. ', ur'polilla\)\|', ], xpos=[ur' (?:articularis|subflava|sparganii|algae|oblonga|alaeta|lameda|\(polilla)', ]) + #19
lema(ur'[Ee]_x_clusiv[ao]s?_s', xpre=[ur'Toscana ', ], xpos=[ur' XII', ]) + #19
lema(ur'[Hh]_í_brid(?:as|os?)_i', xpos=[ur' di ', ]) + #19
lema(ur'[Pp]roced_í_a[ns]?_i', xpre=[ur'ELSEVIER ', ur'Elsevier ', ur'Platform\. ', ], xpos=[ur' Economics', ]) + #19
lema(ur'[Rr]eh_é_n_e', xpos=[ur'\]\][a-zñ]+', ]) + #19
lema(ur'[Aa]s_c_enso_', xpre=[ur'García ', ur'González ', ur'Jacobo ', ur'real ', ], xpos=[ur' Ampim', ]) + #18
lema(ur'[Aa]utom_á_tica_a', xpre=[ur'Elaborazione ', ur'Quattroporte ', ur'[Hh]ead ', ur'[Ii]nformazione ', ], xpos=[ur' [0-9]+', ]) + #18
lema(ur'[Bb]_é_same_e', xpos=[ur'\.fm', ]) + #18
lema(ur'[Cc]onf_í_a[ns]?_i', xpre=[ur'DTU ', ur'\be ', ur'proceedings‚ ', ], xpos=[ur' em ', ]) + #18
lema(ur'[Dd]ar_á_ (?:marcha|origen|inicio|declaración|monedas|acceso|como|fuego|una?|en|de|el|las?|los|a)_a', xpre=[ur'\ba ', ur'\bde ', ur'CL y ', ur'Chahar ', ur'Olu ', ]) + #18
lema(ur'[Dd]efend_í_(?:a[ns]?|)_i', xpre=[ur'Italo ', ur'Marino ', ur'Rafael ', ur'Rodrigo ', ur'Tonioli ', ], xpos=[ur' Asturies', ur'\]', ]) + #18
lema(ur'[Dd]uod_é_cim[ao]s?_e', xpre=[ur'primo ', ur'Paraphlebia ', ur'dell[\' ]', ur'in ', ], xpos=[ur' (?:novarum|reformata|impressao)', ]) + #18
lema(ur'[Ee]go_í_stas?_i', xpre=[ur'Junai ', ur'Junjou ', ur'Lamborghini ', ur'lamborgini ', ur'sporco ', ], xpos=[ur' Feat', ]) + #18
lema(ur'[Ff]ant_á_stic[ao]s_a', xpre=[ur'mighhola mis ', ]) + #18
lema(ur'[Ff]armac_é_utic[ao]s?_e', xpre=[ur'Palestra ', ur'Tribuna ', ur'di Botanica ', ], xpos=[ur' (?:di |e tossicologica)', ]) + #18
lema(ur'[Ff]_é_nix_e', pre=ur'(?:[Aa]ve|[Aa]tl[eé]tico) ', xpos=[ur' Pictures', ]) + #18
lema(ur'[Ii]n_é_dita_e', xpre=[ur'Carmina ', ur'Lettera ', ur'Opera ', ur'Pelecopsis ', ur'Problemata ', ur'Vallesia ', ur'[Ss]acra ', ur'adhuc ', ur'corrispondenza ', ur'lettera ', ur'maximum ', ur'quam ', ur'ricerca sociologica ', ur'tum ', ], xpos=[ur' (?:di |a cura di|e due|grammatica|Discorso|Editores)', ]) + #18
lema(ur'[Pp]l_á_stica_a', xpre=[ur'Bianco ', ur'Nero ', ur'Rosso ', ur'[Dd]i ', ur'[Vv]is ', ur'litúrgia ', ur'uomo ', ], xpos=[ur' Narboria', ]) + #18
lema(ur'[Ss]eguir_á_[ns]?_a', xpre=[ur'Luis ', ]) + #18
lema(ur'[Ss]int_é_tic[ao]s?_e', xpre=[ur'ammoniaca ', ur'grass ', ], xpos=[ur' di', ]) + #18
lema(ur'[Ss]u_é_ter_e', xpre=[ur'Murray ', ur'banda\)\|', ur'escrito como ', ], xpos=[ur' (?:5|Book)', ]) + #18
lema(ur'[Aa]_ _veces_', xpre=[ur'Teena ', ]) + #17
lema(ur'ha_ll_(?:ar|es)_y', xpos=[ur' buddy', ]) + #17
lema(ur'[Mm]inor_í_as?_i', xpre=[ur'Fusulina ', ], xpos=[ur' [Aa]bsoluta', ]) + #17
lema(ur'[Uu]nd_é_cim[ao]s?_e', xpre=[ur'L\'', ur'dell\'', ], xpos=[ur' (?:novarum|Xou)', ur', nel', ]) + #17
lema(ur'[Aa]narqu_í_as?_i', xpre=[ur'amor i ', ]) + #16
lema(ur'[Bb]iol_ó_gic(?:[ao]s|amente)_o', xpre=[ur' e ', ur'Ciências ', ur'Ciências Medicas e ', ur'Sitientibus serie Ciencias ', ]) + #16
lema(ur'[Cc]at_á_strofes?_a', xpre=[ur' e ', ur'della ', ], xpos=[ur' da', ]) + #16
lema(ur'[Cc]onc_é_ntric[ao]s?_e', xpre=[ur'Daldinia ', ur'Dosinia ', ur'Halomitra ', ur'Helminthopsis ', ur'Lepidocyclina ', ur'Mississippina ', ur'Neoregelia ', ur'Phyllolepis ', ur'Quercus ', ur'Stomatorbina ', ur'[Pp]\. ', ur'var\. ', ], xpos=[ur', Montalbruto', ]) + #16
lema(ur'[Ee]s__encia(?! Banda Show)_c', xpre=[ur'\]', ]) + #16
lema(ur'Erev_á_n_a', xpre=[ur'Ararat ', ur'Banants ', ur'Pyunik ', ur'Spartak ', ur'd\'', ur'und ', ], xpos=[ur' (?:on|Ilesere|Olympic)', ]) + #16
lema(ur'fantas_í_as?_i', pre=ur'(?:[Dd]e|[Ll]as|[Ee]n|[Ee]stas?|[Tt]ienen|sus?|y) ', xpre=[ur'Scherzi ', ]) + #16
lema(ur'[Ii]c_ó_nic[ao]s?_o', xpre=[ur'Conchologia ', ur'Conchologica ', ur'Cousinia ', ur'Glycyrrhiza ', ]) + #16
lema(ur'[Pp]erif_é_ric[ao]s?_e', xpre=[ur'troppo ', ]) + #16
lema(ur'[Tt]aiwan_é_s_e', xpos=[ur'\]\](?:as?|es)', ]) + #16
lema(ur'[Dd]escubr_ió__(?:io|ío)', xpre=[ur'quando ', ], xpos=[ur' no anno', ]) + #15
lema(ur'[Jj]ard_í_n_i', pre=ur'[Uu]n ', xpre=[ur'[Dd]ans ', ur'avait ', ur'd\'', ], xpos=[ur' (?:qui|pour|Royale?|En Méditerranée|en désordre|[Bb]otanique|secret|sauvage|mouillé|à |sans |sur |du |au |de (?:Passacailles|Ville|l\'État)|d[\'’])', ]) + #15
lema(ur'[Mm]edi_á_tic[ao]s?_a', xpre=[ur'non ', ur'democrazia ', ]) + #15
lema(ur'[Pp]art_í_culas?_i', xpre=[ur'historiae ', ur'novem ', ], xpos=[ur' (?:prima|secunda)', ]) + #15
lema(ur'[Pp]sic_ó_log[ao]s?_o', xpos=[ur' del carattere', ]) + #15
lema(ur'[Pp]siquiatr_í_as?_i', xpre=[ur' e ', ur' em ', ur'A ', ur'Brasileira de ', ur'antropològica existencial de la ', ur'questões de ', ], xpos=[ur' (?:fonamental|e psicanálise| (?:do|em) )', ur'\.com', ]) + #15
lema(ur'[Rr]ob_ó_tic[ao]s?_o', xpre=[ur'Toccata ', ], xpos=[ur' (?:\(juego|earthensis)', ur': Cybernation', ]) + #15
lema(ur'[Rr]ob_ó_tic[ao]s?_o', xpre=[ur'Toccata ', ], xpos=[ur' (?:\(juego|earthensis)', ur': Cybernation', ]) + #15
lema(ur'_A_lemania_a', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ', xpre=[ur'\]', ]) + #14
lema(ur'Bak_ú__u', pre=ur'(?:[Dd]e|[Ee]n) ', xpre=[ur'acompañado ', ], xpos=[ur' Crystal', ]) + #14
lema(ur'[Bb]eb_í_a[ns]?_i', xpre=[ur'Sent ', ], xpos=[ur' Emilia', ]) + #14
lema(ur'est_á__a', pre=ur'(?:Él|[ÉE]lla) ', xpos=[ur' comunidad', ]) + #14
lema(ur'[Ff]armacolog_í_as?_i', xpre=[ur'Català de ', ], xpos=[ur' e Terapia', ]) + #14
lema(ur'_ha_ (?:editado|eliminado|embarcado|empezado|encajado|encontrado|enfocado|enfrentado|enseñado|entendido|entrado|enviado|enviudado|esculpido|especializado|especulado|estudiado|evolucionado|expandido|experimentado|expresado)_ah?', xpre=[ur'[0-9]', ]) + #14
lema(ur'Pakist_á_n_a', pre=ur'(?:[Dd]e|[Ee]n) ', xpos=[ur' International', ]) + #14
lema(ur'[Pp]_á_lid[ao]s?_a', xpos=[ur' Fonk', ]) + #14
lema(ur'[Pp]eri_ó_dicos_o', xpre=[ur'dos ', ]) + #14
lema(ur'_últ_im[ao]s?_[uú]tl') + #14
lema(ur'Z_ú_rich_u', pre=ur'(?:[Ee]n|y|o) ', xpos=[ur' (?:Zentralbibliothek|Afore)', ]) + #14
lema(ur'[Aa]p_ó_stoles_o', xpos=[ur', Michael', ur'\.gov', ]) + #13
lema(ur'Belmop_á_n_a', xpre=[ur'FC ', ], xpos=[ur' (?:Hospital|Public|United|Blaze|Museum|Bandits)', ]) + #13
lema(ur'[Cc]_á_lida_a', xpre=[ur'Acraea ', ur'Aegilops ', ur'Anthia ', ur'Antiblemma ', ur'Aquae ', ur'Argia ', ur'Drummondita ', ur'Euphrasia ', ur'Globigerinella ', ur'Hyles ', ur'Indervalle - ', ur'Megachile ', ur'Microcyba ', ur'Thalpochares ', ], xpos=[ur' (?:fornax|nit)', ]) + #13
lema(ur'[Cc]ronol_ó_gic[ao]_o', xpre=[ur'Storia ', ], xpos=[ur' (?:dei|della|das)', ]) + #13
lema(ur'[Dd]ur_ó_ (?:una?|dos|tres|diez|cien|mil)_o', xpre=[ur'Seguimiento ', ur'molde ', ur'muy ', ]) + #13
lema(ur'[Gg]eomorfolog_í_a_i', xpos=[ur' da', ]) + #13
lema(ur'[Pp]edagog_í_a_i', xpre=[ur'Facultat de ', ur'Premi Rosa Sensat de ', ur'Secció de ', ur'\b[Aei] ', ur'\bd[ai] ', ur'\bin ', ur'della ', ur'dir ', ur'do Curso de ', ], xpos=[ur' (?:sociale|d[aio]|dels|Dell|anb|amb|a Catalunya|sexuala|spagnola|: diálogo e conflito|Revuo|del segle|que ens)', ]) + #13
lema(ur'[Pp]on_í_a[ns]?_i', xpre=[ur'Adiós ', ]) + #13
lema(ur'[Ss]upremac_í_as?_i', xpre=[ur'\be ', ]) + #13
lema(ur'[Tt]_ú_neles_u', xpos=[ur'\.info', ]) + #13
lema(ur'[Uu]n_í_a[ns]_i', xpre=[ur'[Dd][’\']', ], xpos=[ur'\]\]', ]) + #13
lema(ur'[Aa]rmer_í_as?_i', xpre=[ur' in ', ur'Byzantine ', ur'Dianthus ', ur'Glomérulo de ', ur'HMS ', ur'L\'', ur'Limonium, ', ur'Silene ', ur'antica ', ur'presencia de la ', ], xpos=[ur' (?:alboi|alliacea|alliana|allioides|alpina|arcuata|arenaria|australis|baetica|beirana|berlengensis|bigerrensis|bupleuroides|bourgaei|bubanii|caballeroi|capitella|cariensis|carratracensis|castellana|castroviejoi|ciliata|caespitosa|colorata|cantabrica|cephalotes|Confessionis|daveaui|de (?:convenientia|ivstificatione|la Borrida|roca|[Ss]egovia)|del Rey Don|denticulata|depilata|dianthoides|duriaei|duriensis|e profezia|elongata|eriophylla|euscadiensis|expansa|filicaulis|fasciculata|gaditana|genesiana|girardii|hirta|hispalensis|humilis|juncea|juniperifolia|lacaitae|lanceobracteata|langei|leucantha|leucocephala|linkiana|littoralis|longiaristata|losae|macrophylla|maderensis|maritima|maritime|matritensis|miscella|montana|muelleri|nebrodensis|pinifolia|plantaginea|platyphyla|pubescens|purpurea|pseudarmeria|pseudoarmeria|pubigera|pubinervis|pungens|Reale|rigida|rivasmartinezii|rumelica|sampaioi|sabulosa|sardoa|scorzonerifolia|segoviensis|seticeps|sicorisiensis|splendens|stenophylla|sulcitana|trachyphyla|trachyphylla|transmontana|trigoloides|undulata|velutina|vestita|villosa|vulgaris|welwitschii|Eskola|rhodopaea|var|x )', ur'(?:[|:\'\]]|\.gob|, (?:césped|Limonium))', ]) + #12
lema(ur'[Ee]ntomolog_í_as?_i', xpre=[ur' (?:et|di) ', ur'[Bb]rasileira de ', ur'sull\'', ], xpos=[ur' (?:African|agraria e biologia applicata|[Ss]ystematica|Parisiensis|applicata|generale|[Cc]arniolica|nella|Americana|Experimentalis|de Mocambique)', ur'\.?\'', ]) + #12
lema(ur'[Ee]p_í_tetos?_i', xpos=[ur' (?:Botánicos|Melesigenes)', ]) + #12
lema(ur'[Ee]xc_é_ntric[ao]_e', xpre=[ur'Acacia ', ur'Bulolia ', ur'Compsodrillia ', ur'Dentalina ', ur'Eoophyla ', ur'Hallo ', ur'Kefersteinia ', ur'Pleurothallis ', ur'Stachybotryna ', ]) + #12
lema(ur'le_í_a[ns]?_i', xpre=[ur'2 ', ], xpos=[ur' sawola', ]) + #12
lema(ur'[Mm]agn_í_fica_i', pre=ur'(?:[Ll]a|[Uu]na|[Dd]e|[Ee]sta|[Ss]u|[Tt]an) ', xpos=[ur' (?:Cure|ni)\b', ]) + #12
lema(ur'[Mm]arcar_í_a[ns]?_i', xpre=[ur'Julio ', ur'Protección ', ], xpos=[ur' (?:Julio|sopra)', ur'\]', ]) + #12
lema(ur'[Pp]arasitolog_í_as?_i', xpre=[ur'\be ', ]) + #12
lema(ur'sent_í_a_i', xpre=[ur'Egun ', ]) + #12
lema(ur'[Ss]inton_í_as?_i', xpre=[ur'Cicurina ', ]) + #12
lema(ur'[Tt]elefon_í_as?_i', xpos=[ur' Nas', ]) + #12
lema(ur'[Tt]_é_rmica_e', xpre=[ur'Centrale ', ]) + #12
lema(ur'[Tt]r_á_gica_a', xpre=[ur' e ', ur'Alba ', ur'Ballata ', ur'Caccia ', ur'Musa ', ], xpos=[ur' (?:notte|dei|poveste|I-VII)', ]) + #12
lema(ur'_ú_ltima_u', pre=ur'[Dd]e ', xpos=[ur' ratio', ]) + #12
lema(ur'[Aa]utom_á_tico_a', xpre=[ur'Moschetto ', ]) + #11
lema(ur'[Bb]iogeogr_á_fic[ao]s?_a', xpre=[ur'\bdi ', ]) + #11
lema(ur'[Bb]ot_á_nicos_a', xpre=[ur'Termos ', ], xpos=[ur' (?:e Estaçao|mais|Regiae|della|intrapreso|in|[Mm]alacitana|do)', ur', in Il', ]) + #11
lema(ur'[Ee]s__encia(?:l|les|lmente)_c', xpre=[ur'\]', ], xpos=[ur' Indígena', ]) + #11
lema(ur'[Ff]el_i_(?:z|ces)_í', xpre=[ur'San ', ]) + #11
lema(ur'[Mm]and_í_bula_i', xpre=[ur'Euphitrea ', ur'uma ', ], xpos=[ur' superiore', ur'\]\][a-z]+', ]) + #11
lema(ur'[Mm]etaf_í_sic[ao]s?_i', xpre=[ur' d[ai] ', ur'Giornale de ', ur'della ', ur'di una ', ur'scuola ', ur'suono ', ], xpos=[ur' (?:[Aa]perta|classica|das|di )', ur'\'\' di', ]) + #11
lema(ur'[Pp]anader_í_as?_i', xpos=[ur'\.blogspot', ]) + #11
lema(ur'[Pp]en_ú_ltim[ao]s?_u', xpos=[ur' (?:Online|calatorie)', ]) + #11
lema(ur'[Pp]erd_í_a[ns]?_i', xpre=[ur'Alejandro ', ur'Roberto ', ]) + #11
lema(ur'[Pp]ol_í_ticamente_i', xpre=[ur'Partito ', ], xpos=[ur' (?:scorretto|incorreto da)', ]) + #11
lema(ur'[Ss]epar_ó__o', xpre=[ur'(?:[Mm]e|[Uu]n|[Yy]o) ', ], xpos=[ur' tus', ]) + #11
lema(ur'[Aa]nomal_í_as?_i', xpre=[ur'Pichia ', ]) + #10
lema(ur'[Cc]_á_scaras?_a', xpos=[ur' Sagrado', ]) + #10
lema(ur'[Ee]stad_í_as?_i', xpos=[ur' y Telquinis', ]) + #10
lema(ur'_é_l ha_e', xpre=[ur'(?:ch\'|Af\')', ]) + #10
lema(ur'[Hh]ip_ó_tesis_o', xpre=[ur'gap ', ]) + #10
lema(ur'[Hh]uman_í_stic[ao]s?_i', xpre=[ur'Bibliotheca ', ur'Scripta ', ur'Universitas ', ur'et ', ], xpos=[ur' Lovaniensia', ]) + #10
lema(ur'[Mm]ov_í_a_i', xpre=[ur'C\. ', ur'[Pp]ía ', ], xpos=[ur' (?:ingens|BM2)', ur'\]', ]) + #10
lema(ur'[Mm]o_v_ilidad_b', xpos=[ur' Bahía', ]) + #10
lema(ur'[Nn]um_é_ric[ao]_e', xpre=[ur'T\. ', ], xpos=[ur' delle', ur', T\. y', ]) + #10
lema(ur'[Ss]imetr_í_as?_i', xpos=[ur' (?:dei|das?)\b', ]) + #10
lema(ur'[Ss]upers_ó_nic[ao]s?_o', xpos=[ur'\.net', ]) + #10
lema(ur'_Á_rid(?:as|os?)_A', xpre=[ur' of ', ], xpos=[ur' movie', ]) + #9
lema(ur'_a_ ser_(?:ha|ah)', xpre=[ur'\$', ]) + #9
lema(ur'[Bb]enem_é_rit[ao]s?_e', xpos=[ur' Associazione', ]) + #9
lema(ur'[Cc]riminolog_í_as?_i', xpre=[ur'derecho\.', ], xpos=[ur' (?:femminile|e direito)', ]) + #9
lema(ur'[Ee]mbriolog_í_as?_i', xpos=[ur' di\b', ]) + #9
lema(ur'[Ee]_x_tendid[ao]s?_s?', xpre=[ur'onde ', ]) + #9
lema(ur'[Hh]_á_bitat_a', pre=ur'(?:[Ee]l|[Ss]u|[Uu]n|[Ee]s) ', xpos=[ur' (?:collectif|magdalénien)', ]) + #9
lema(ur'[Ll]a_s_ versiones_', xpos=[ur' ufficiale', ]) + #9
lema(ur'[Pp]end_í_a[ns]?_i', xpre=[ur' (?:de|en) ', ], xpos=[ur'(?:[|\]])', ]) + #9
lema(ur'[Pp]er_í_metros?_i', xpre=[ur'[Ss]e ', ur'\be ', ]) + #9
lema(ur'[Pp]olit_é_cnicas?_e', xpre=[ur'Escola ', ur'Scuola ', ur'Università ', ], xpos=[ur' (?:de Catalunya|)', ]) + #9
lema(ur'[Pp]sic_ó_patas?_o', xpos=[ur' (?:e Profilaxia|Mora ao)', ]) + #9
lema(ur'[Ss]acrist_í_as?_i', xpos=[ur' Vecchia', ]) + #9
lema(ur'[Tt]err_í_colas?_i', xpre=[ur'A\. ', ur'Aysenoides ', ur'Camponotus ', ur'Cylindera ', ur'Cyrtauchenius ', ur'Microtus \(', ur'Moggridgea ', ur'Otira ', ur'Paecilomyces ', ur'Solenopsis ', ur'Spironema ', ur'Trochosa ', ur'Tropiphorus ', ], xpos=[ur' atapuerquensis', ur'[)\]]', ]) + #9
lema(ur'[Tt]r_á_gic(?:[ao]s|amente)_a', xpre=[ur' e ', ]) + #9
lema(ur'[Aa]d_h_esivos?_', xpre=[ur'[Cc]aso ', ]) + #8
lema(ur'[Aa]u_n_que_', xpre=[ur'Roger ', ]) + #8
lema(ur'Am_é_rica_e', pre=ur'Sud ', xpre=[ur'für ', ], xpos=[ur' Bank', ]) + #8
lema(ur'[Cc]oreograf_í_as?_i', xpre=[ur'\bi ', ur'com ', ]) + #8
lema(ur'[Cc]orr_í_a_i', xpre=[ur'Fenge ', ur'Odontoptilum ', ur'de ', ur'o Amazonas ', ], xpos=[ur' da', ]) + #8
lema(ur'[Cc]osm_é_tic(?:as|os?)_e', xpre=[ur'Benefit ', ur'Natura ', ], xpos=[ur'\.name', ]) + #8
lema(ur'[Dd]esaf_í_o de_i', xpre=[ur'O ', ], xpos=[ur' Criar', ]) + #8
lema(ur'[Ee]sf_é_ric[ao]s?_e', xpre=[ur'Lepidocyclina ', ur'Vorticella ', ]) + #8
lema(ur'[Ee]str_é_s_e', xpos=[ur'(?:\]\]or|\'\'s)', ]) + #8
lema(ur'[Ff]isiol_ó_gic[ao]s?_o', xpre=[ur' e ', ]) + #8
lema(ur'[Ff]itogeograf_í_a_i', xpre=[ur' e ', ], xpos=[ur' (?:no|do|e Genetica)', ]) + #8
lema(ur'[l]e_í_a_i', xpre=[ur'Doriopsilla ', ur'Wo ', ]) + #8
lema(ur'Matur_í_n_i', pre=ur'(?:[Dd]e|[Ee]n) ', xpos=[ur' llega', ]) + #8
lema(ur'[Mm]icr_ó_fonos?_o', xpos=[ur' (?:è|d)', ]) + #8
lema(ur'[Pp]edag_ó_gica_o', xpre=[ur'L\'Opera ', ], xpos=[ur'\.edu', ]) + #8
lema(ur'[Pp]_ó_stum[ao]s_o', xpre=[ur'Atilio ', ur'Vibio ', ur'op\. ', ], xpos=[ur' Dardano', ]) + #8
lema(ur'[Pp]resid_í_a[ns]?_i', xpre=[ur'fueron ', ur'plural \'\'\'', ]) + #8
lema(ur'[Rr]adiograf_í_as?_i', xpos=[ur' (?:d´una|di)\b', ]) + #8
lema(ur'[Ss]imb_ó_lica_o', xpre=[ur'Fiamma ', ur'Natura ', ur'Tarocchi via ', ur'Vita ', ur'città ', ], xpos=[ur' in', ]) + #8
lema(ur'[Ss]ubstitu_i_d[ao]s?_í', xpre=[ur'Coroa ', ur'foi ', ur'sendo ', ur'tendo sido ', ], xpos=[ur' por um', ]) + #8
lema(ur'Sud_á_n_a', pre=ur'(?:[Dd]e|[Ee]n) ', xpos=[ur' (?:Airways|Foundation)', ]) + #8
lema(ur'[Tt]em_í_a_i', xpre=[ur'C\. ', ur'Crypsirina ', ur'Quesería ', ], xpos=[ur'["\]]', ]) + #8
lema(ur'[Tt]ornar_í_a_i', xpre=[ur'Larva ', ur'Mauro ', ], xpos=[ur'\]\]', ]) + #8
lema(ur'[Aa]cert_ó_(?! dos)_o', xpre=[ur'Bo ', ]) + #7
lema(ur'[Aa]strof_í_sicas?_i', xpre=[ur' di ', ], xpos=[ur' (?:Spaziale|d\'oggi)', ]) + #7
lema(ur'_á_cida_a', xpre=[ur'Aglaia ', ur'Ambelania ', ur'Asclepia ', ur'Asclepias ', ur'Averrhoa ', ur'Begonia ', ur'Berberis ', ur'Cerasus ', ur'Cicca ', ur'Citrus ', ur'Eulychnia ', ur'Fucsina ', ur'Hymenocardia ', ur'Hypertelis ', ur'Lannea ', ur'Leptomeria ', ur'Meriania ', ur'P\. ', ur'Prunus ', ur'Sonneratia ', ur'Spiloxene ', ur'Spondias ', ur'Tapirira ', ur'Uncaria ', ur'Willughbeia ', ur'ssp\. ', ur'subsp\. ', ur'subsp\. \'\'', ur'var\. ', ], xpos=[ur'\'', ]) + #7
lema(ur'_á_ure(?:as|os?)_a', xpre=[ur'\'', ur'Miliario ', ur'Ortoedro ', ur'Pisces ', ur'Trifolio ', ur'mille ', ur'trifolio ', ur'villa ', ], xpos=[ur' cornu', ]) + #7
lema(ur'[Bb]iom_é_dicas?_e', xpre=[ur'Recerca ', ur'Storia ', ]) + #7
lema(ur'[Cc]_é_ntric[ao]s?_e', xpre=[ur'por ', ], xpos=[ur' Energía', ur'[\|\]]', ]) + #7
lema(ur'[Dd]emocr_á_tic(?:[ao]s|amente)_a', xpos=[ur' Avançadas', ]) + #7
lema(ur'[Dd]ial_é_ctic[ao]s?_e', xpre=[ur'\'', ur'Institutiones ', ur'Partitio ', ur'canities ', ur'inventione ', ur'sive ', ], xpos=[ur' (?:Eristica|Resolutio|erroribus|libri|[1-9]|\(polilla)', ur'(?:\]|, (?:Logica sive|Rhetorica))', ]) + #7
lema(ur'[Ee]nv_í_a[ns]_i', xpos=[ur'(?:=|\'m)', ]) + #7
lema(ur'[Ff]r_á_gil_a', xpos=[ur' (?:X|things|Heart|Records|[Dd]iscos)', ]) + #7
lema(ur'[Gg]en_é_rica_e', xpre=[ur'Floralis ', ], xpos=[ur' (?:e specifica|Hepaticarum)', ]) + #7
lema(ur'[Gg]en_é_tico_e', xpre=[ur'Pomodoro ', ]) + #7
lema(ur'[Hh]abr_í_an_i', xpre=[ur'Ain ', ]) + #7
lema(ur'[Ll]_ó_gic[ao]_o', pre=ur'(?:[Ll]a|[Uu]na) ', xpos=[ur' (?:d[iu]|del)\b', ]) + #7
lema(ur'[Pp]edi_á_tric[ao]s?_a', xpos=[ur' Bambino', ]) + #7
lema(ur'[Ss]imb_ó_lico(?!e o imaxinario)_o', xpre=[ur'Mondo ', ur'suo uso ', ]) + #7
lema(ur'[Aa]erodin_á_mic[ao]s?_a', xpre=[ur'600 Y ', ur'Regia ', ur'Servizio ', ur'di ', ], xpos=[ur' (?:Spider|Torino)', ur' \.difesa', ]) + #6
lema(ur'[Bb]ell_í_sim[ao]s?_i', xpre=[ur'Frank ', ]) + #6
lema(ur'[Bb]iogeograf_í_a_i', xpre=[ur'Nuova ', ur'e ', ], xpos=[ur' (?:della|e conservação|d\’un|de parlamentaris|de Magalhães)', ]) + #6
lema(ur'[Cc]_á_lculos_a', xpos=[ur' accuratissimos', ]) + #6
lema(ur'[Cc]ent_í_grados?_i', xpre=[ur'Graus ', ]) + #6
lema(ur'[Cc]ompa_ñ_er[ao]s?_n', xpre=[ur'The ', ], xpos=[ur'\'\'', ]) + #6
lema(ur'[Cc]ono_z_c(?:a[ns]?|amos|o)_s', xpre=[ur'Brincar ', ur'Non ', ur'[TtVvLl]i ', ur'che ', ur'cuide ', ur'non lo ', ]) + #6
lema(ur'[Cc]orrer_á_[ns]?_a', xpre=[ur'Azalia ', ur'Camila ', ur'Luigi ', ur'son ', ]) + #6
lema(ur'[Dd]esaf_í_a[ns]?_i', xpos=[ur' o nosso', ]) + #6
lema(ur'[Ee]nerg_í_as_i', xpre=[ur'Acciona ', ur'Amorim ', ur'Amorim ', ur'CS ', ur'CS ', ur'Direcção Geral de ', ur'EDP ', ur'Engenharia de ', ur'Galp ', ur'Iberdrola ', ur'Kerava ', ur'L[\'’]', ur'Manaus ', ur'Mello ', ur'Quale ', ur'Som ', ur'Tractebel ', ur'Tractebel ', ur'\be ', ur'as ', ur'da Mesa ', ur'essa ', ], xpos=[ur' (?:a um|Fălticeni|della|Târgu|Circular Sport Clube|Lignitul|Ploiești|Productions|Elétrica|y Flacăra|d[ao]|Trustul|de (?:la Generalitat|Portugal)|e (?:Trabalho|Serviços|Servizi))\b', ]) + #6
lema(ur'est_á_ detrás_a', xpre=[ur'[Ee]stando ', ]) + #6
lema(ur'est_a_dios?_á', xpre=[ur' (?:em|do|no) ', ur'novos ', ], xpos=[ur' (?:do |no |renovado em|Palestra Itália|de Carnide|da Luz|das Amoreiras|Cidade|Adelino)', ]) + #6
lema(ur'[Gg]eof_í_sicas?_i', xpre=[ur'Nazionale ', ur'di ', ], xpos=[ur' e Vulcanologia' ur'\.cl', ]) + #6
lema(ur'[Gg]e_ó_log[ao]s?_o', xpre=[ur'Professione ', ]) + #6
lema(ur'[Gg]rad_ú_a_u', xpos=[ur'\'t', ]) + #6
lema(ur'[h]ar_á_n_a', xpos=[ur' (?:bat|hua|Al-Awamid|no |\'*\(valle)', ur'\'', ]) + #6
lema(ur'[Hh]u_b_o_v', xpos=[ur'\]\]', ]) + #6
lema(ur'[Ii]mpl_í_cit[ao]_i', xpre=[ur'Limnophila ', ur'Phyllophaga ', ur'[LP]\. ', ur'[Ll]\'', ur'testo ', ], xpos=[ur' nel', ]) + #6
lema(ur'[Ll]ic_ú_(?:a|as?|e[ns]?)_u', xpre=[ur'grupo ', ur'perlatum ', ], xpos=[ur' Labaudt', ]) + #6
lema(ur'[Mm]orfol_ó_gic[ao]s?_o', xpre=[ur'Diversidade ', ], xpos=[ur' e formas', ]) + #6
lema(ur'Om_á_n_a', pre=ur'(?:[Dd]e|[Ee]n) ', xpos=[ur' Air', ]) + #6
lema(ur'[Oo]rfebrer_í_as?_i', xpos=[ur' i\b', ]) + #6
lema(ur'part_í_a[ns]?_i', xpre=[ur'Ispanskaja ', ur'Txakurraren ', ur'bactriana y ', ], xpos=[ur'[\|\]]', ]) + #6
lema(ur'[Pp]artir_á__a', xpre=[ur'(?:tu|[Oo]n) ', ]) + #6
lema(ur'[Pp]olicl_í_nicos?_i', xpre=[ur'Nápoles\)\|', ur'Viale del ', ur'estación\)\|', ur'estación\)\|\'\'\'', ], xpos=[ur' \((?:Metro de Nápoles|estación)', ]) + #6
lema(ur'[Pp]rol_í_fica_i', xpre=[ur'Derbesia ', ur'Echeveria ', ur'Epicauta ', ur'Fragaria ', ur'Lycosa ', ur'Mimosa ', ur'Ophiocordyceps ', ur'Ottoia ', ur'Pardosa ', ur'Pachyphloia ', ur'Poeciliopsis ', ur'[EOP]\. ', ]) + #6
lema(ur'[Tt]ard_í_(?:[ao]s|amente)_i', xpre=[ur'Direitos ', ]) + #6
lema(ur'[Tt]at_ú_(?:a[ns]?|e[ns]?)_u', xpre=[ur'Baby ', ]) + #6
lema(ur'[Tt]e_ó_ric(?:[ao]s|amente)_o', xpre=[ur'Sulla ', ]) + #6
lema(ur'Viv_í_as?_i', xpre=[ur' de ', ]) + #6
lema(ur'[Vv]encer_á_[ns]?_a', xpos=[ur' e vinha', ]) + #6
lema(ur'[Aa]cabar_í_a[ns]?_i', xpos=[ur' splendens', ur'[\]\']', ]) + #5
lema(ur'[Aa]ctuar_í_a[ns]_i') + #5
lema(ur'[Aa]gron_ó_mic[ao]s?_o', xpre=[ur'Acta ', ], xpos=[ur'(?: +(?:per|coloniale|[Aa]cademiae))', ]) + #5
lema(ur'[Aa]rd_í_a_i', xpre=[ur'Sindie ', ], xpos=[ur' (?:Napoli|\(cortometraje)', ur'\]', ]) + #5
lema(ur'[Aa]utob_ú_s_u', pre=ur'(?:[Ee]l|[Uu]n|[Ee]n) ', xpos=[ur' tutto', ]) + #5
lema(ur'[Cc]enar_í_a[ns]?_i', xpre=[ur'(?:[Dd]e|[Ee]n)', ur'[Ii]slote ', ]) + #5
lema(ur'[Cc]_í_tric[ao]s?_i', xpre=[ur'Cancro ', ur'Eotaria ', ur'\b[E]\. ', ur'das plantas ', ]) + #5
lema(ur'[Cc]riminal_í_stica_i', xpos=[ur'\.(?:com|net)', ]) + #5
lema(ur'[Dd]r_á_stic[ao]_a', xpre=[ur'Anisomeria ', ur'Euphorbia ', ur'Millettia ', ur'Wilbrandia ', ]) + #5
lema(ur'[Ff]enomenolog_í_as?_i', xpre=[ur'Estudi sobre la ', ur'Oltre la ', ur'[Uu]ma ', ur'\bi la ', ], xpos=[ur' (?:da|moral de la modernitat|del linguaggio|della|dell|nella|a (?:Sartre|prova)|feministado|spiritului)\b', ]) + #5
lema(ur'[Ff]or_á_ne[ao]s?_a', xpre=[ur'Mythimna ', ur'battello ', ]) + #5
lema(ur'[Gg]en_é_rico_e', xpre=[ur' ', ur'E', ur'l', ]) + #5
lema(ur'[Gg]ob_i_erno_', pre=ur'(?:[Ee]l|[Uu]n|[Dd]el?) ', xpre=[ur'Via ', ]) + #5
lema(ur'[Ii]n_ú_tiles_u', xpre=[ur'Bouches ', ur'Sourires ', ur'choses ', ur'plantes ', ur'risques ', ur'seraient ', ]) + #5
lema(ur'[Jj]erarqu_í_as?_i', xpos=[ur' a la Responsabilitat', ]) + #5
lema(ur'[Ll]_é_sbic[ao]s?_e', xpre=[ur'Aphaenogaster ', ur'Isoperla ', ur'[AI]\. ', ], xpos=[ur' e gay', ]) + #5
lema(ur'[Mm]an_í_as? de_i', xpre=[ur'[Ll]a (?:[Ll]as|[Uu]na) ', ur'[Uu]nas ', ], xpos=[ur' (?:Você|de [Vv]ocê|kakushidori|explicação)', ]) + #5
lema(ur'[Nn]obil_í_sim[ao]s?_i', xpos=[ur' Cæsares', ]) + #5
lema(ur'Ocean_í_a_i', pre=ur'(?:[Dd]e|[Ee]n) ', xpos=[ur' (?:Cruises|Rugby)', ]) + #5
lema(ur'[Pp]unt_ú_(?:a[ns]?|e[ns]?)_u', xpre=[ur'eta ', ]) + #5
lema(ur'[Qq]uerr_á_[ns]?_a', xpre=[ur'en la ', ]) + #5
lema(ur'Sal_í_an_i', xpos=[ur', Bhat', ]) + #5
lema(ur'Uzbekist_á_n_a', pre=ur'(?:[Dd]e|[Ee]n) ', xpos=[ur' (?:Airways|Temir)', ]) + #5
lema(ur'[Vv]endr_á_[ns]?_a', xpre=[ur'Paul ', ]) + #5
lema(ur'[Aa]punt_ó__o', pre=ur'(?:[Ll]e|[Mm]e|[Nn]os) ', xpre=[ur'Yo ', ]) + #4
lema(ur'[Dd]ermatolog_í_as?_i', xpos=[ur' (?:e venereologia|Ospedale)', ]) + #4
lema(ur'[Ff]r_á_gil(?:es|mente)_a', xpre=[ur'Moisson ', ur'[&] ', ur'choses ', ur'conquérants ', ]) + #4
lema(ur'H_á_bil_a', xpre=[ur'Adil ', ur'Dr ', ur'Dr\. ', ], xpos=[ur' (?:Heidelberg|Dr\.|Ahmadov)', ur', (?:eraikan|Halle)', ur'\.', ]) + #4
lema(ur'[Ii]r_ó_nic[ao]_o', xpre=[ur'La ', ]) + #4
lema(ur'[Ll]acrim_ó_gen[ao]s?_o', xpos=[ur'" Bubaseta', ]) + #4
lema(ur'[Ll]_á_tigos?_a', xpre=[ur'George ', ur'for ', ], xpos=[ur' Means', ]) + #4
lema(ur'[Ll]avander_í_as?_i', xpos=[ur'\'\' regia', ]) + #4
lema(ur'[Ll]_ó_gic(?:os|amente)_o', xpos=[ur' Aristotelis', ]) + #4
lema(ur'[Mm]alet_í_n_i', xpre=[ur'Alexander ', ur'Alexandr ', ur'Pavel ', ur'Slavko ', ]) + #4
lema(ur'[Mm]et_í_a[ns]?_i', xpre=[ur';', ur'Lotoala ', ur'\bde ', ur'en que ', ur'muestra el ', ur'mágico \(', ], xpos=[ur' (?:Lotoala|Interactive|Iparis|Industry)', ]) + #4
lema(ur'[Mm]ineralog_í_as?_i', xpre=[ur'di ', ur'e ', ], xpos=[ur' Cornubiensis', ]) + #4
lema(ur'_N_oruega_n', pre=ur'(?:[Aa]|[Aa]nte|[Dd]e|[Ee]n|[Pp]ara|[Pp]or) ', xpre=[ur'Serie [A-C] ', ]) + #4
lema(ur'[Oo]ftalmolog_í_as?_i', xpre=[ur'Brasileiros de ', ur'd[’\']', ]) + #4
lema(ur'[Pp]sicopedagog_í_as?_i', xpos=[ur' em ', ur'\.com', ]) + #4
lema(ur'[Rr]om_á_ntic[ao]s_a', xpos=[ur' di ', ]) + #4
lema(ur'[Ss]i_g_ue[ns]?_q', xpre=[ur'[Ee]l ', ], xpos=[ur' Rodríguez', ]) + #4
lema(ur'[Tt]ar_j_etas?_g', xpre=[ur'amb ', ]) + #4
lema(ur'[Cc]armes_í__i', xpre=[ur'filla del ', ]) + #3
lema(ur'[Cc]asar_í_a_i', xpre=[ur'Pseudopoda ', ]) + #3
lema(ur'[Cc]os_í_a[ns]?_i', xpre=[ur'Carlota '], xpos=[ur'\]', ]) + #3
lema(ur'[Cc]rec_í__i', xpre=[ur'Enrique ', ]) + #3
lema(ur'[Dd]iat_ó_nic[ao]s?_o', xpre=[ur'Philaethria ', ur'il periodo ', ]) + #3
lema(ur'[Ee]mblem_á_tica_a', xpre=[ur'Ars ', ], xpos=[ur' (?:in|Online)\b', ]) + #3
lema(ur'[Ee]_n_ cada_m', xpre=[ur'uma gota de sangue ', ], xpos=[ur' (?:rosto|esquina um)', ]) + #3
lema(ur'[Ee]scenograf_í_as?_i', xpre=[ur'[DdLl]\'', ]) + #3
lema(ur'_é_pic(?:as|os?)_e', xpre=[ur'Scontro ', ]) + #3
lema(ur'[Ff]re_í_r_i', xpre=[ur'Frey\|', ]) + #3
lema(ur'[Gg]ra_c_ias?_s', xpos=[ur' \(Grupo', ur'\]', ]) + #3
lema(ur'[Mm]ariner_í_as?_i', xpos=[ur' degli', ]) + #3
lema(ur'[Mm]ontar_í_a_i', xpos=[ur'\]\]', ]) + #3
lema(ur'[Nn]omb_r_es?_', xpre=[ur'Nakera ', ], xpos=[ur'\'', ]) + #3
lema(ur'[Rr]egular_í_a_i', xpre=[ur' et ', ], xpos=[ur' magistri', ur'\]\]', ]) + #3
lema(ur'[s]abr_á_[ns]?_a', xpre=[ur'eddar ', ], xpos=[ur' y ', ur'[\]\']', ]) + #3
lema(ur'[Ss]i_en_do_ne', xpre=[ur'Andre ', ur'Sinedo\|', ]) + #3
lema(ur'[Aa]bogac_í_as?_i', xpos=[ur'\.es', ]) + #2
lema(ur'[Aa]ll_á_ por_a', xpre=[ur'Tethe\'', ]) + #2
lema(ur'[Aa]lquer_í_as_i', xpre=[ur'sive ', ]) + #2
lema(ur'barr_í_a[ns]?_i', xpre=[ur'etxe ', ur'orbel ', ur'toño ', ], xpos=[ur'\]', ]) + #2
lema(ur'[Bb]ot_á_nicas(?! (?:institutiones|no Ceara|in ))_a', xpre=[ur'ad excursiones ', ur'lectiones ', ]) + #2
lema(ur'[Cc]_á_lido_a', xpre=[ur'Marquilles y ', ], xpos=[ur' innato', ]) + #2
lema(ur'[Cc]ompeti_ti_vidad_', xpos=[ur'"', ]) + #2
lema(ur'[Cc]_ó_ptic[ao]s?_o', xpre=[ur'Ptychotis ', ]) + #2
lema(ur'[Dd]ecid(?:ir|)_í_a[ns]?_i', xpre=[ur'Caleta ', ]) + #2
lema(ur'[Dd]epon_í_a[ns]?_i', xpre=[ur' de ', ur'vertedero ', ]) + #2
lema(ur'[D]eb_í_as?_i', xpre=[ur'Christian ', ur'L\. ', ur'Mercedes ', ur'Miranda ', ur'Vetsch / ', ]) + #2
lema(ur'[Ee]l_igió__egio', xpre=[ur'San ', ur'[Ee]s ', ur'[Ff]u[eé] ', ur'[Ss]er ', ], xpos=[ur' (?:funebre|del sueño)', ur'[\]\|]', ]) + #2
lema(ur'[Ee]n_é_rgica_e', xpos=[ur' (?:Ego|Motor|decisione)', ur', con', ]) + #2
lema(ur'[Ee]st_é_tico_e', xpre=[ur'Cl[íi]nica ', ur'Dizionario ', ], xpos=[ur' (?:di|e psicologico)', ]) + #2
lema(ur'[Ff]a_s_cin(?:ante|ación|ad[ao]s|ó|an?|antes?|aba[ns]?|ación)_', xpre=[ur'Adriana ', ur'de ', ], xpos=[ur' Cane', ur'\]', ]) + #2
lema(ur'[Ff]_ú_tbol_u', pre=ur'(?:Millonarios|Bogotá) ') + #2
lema(ur'[Ii]deol_ó_gic[ao]_o', xpre=[ur'galassia ', ], xpos=[ur' della', ]) + #2
lema(ur'[Ii]ndicar_í_a_i', xpre=[ur'Tractatus de astrologia ', ]) + #2
lema(ur'[Mm]al_é_vol[ao]s?_e', xpre=[ur'Euphorbia ', ]) + #2
lema(ur'[Mm]an_í_as?_i', pre=ur'(?:[Ll]as?|[Uu]nas?) ', xpos=[ur'\.com', ]) + #2
lema(ur'[Mm]atar_í_a[ns]?_i', xpos=[ur'\]', ]) + #2
lema(ur'[Mm]ear_í_a[ns]?_i', xpre=[ur'Lucas, ', ]) + #2
lema(ur'[Mm]e_z_cl(?:a(?:s|r|d[ao]s?)|[éoó])_s', xpos=[ur'["\.,]', ]) + #2
lema(ur'[Mm]over_á_[ns]?_a', xpre=[ur'Peñaflor, ', ur'Vivero y ', ur'\bde ', ur'\| ', ], xpos=[ur' S\.L', ur'(?:[\'\]\|]|, (?:\+Bytes|Peñaflor|Moyuela))', ]) + #2
lema(ur'[Pp]eque_ñ_[ao]s? (?:formato|gran|países|[Ss]uite|Democracias|Italia|Jerusalen|Larousse|Maravilla|Mundo|Odessa|Polonia|Reyes|Veneta)_n', xpos=[ur' de Marcos', ]) + #2
lema(ur'[Ss]ab_á_tic[ao]s?_a', xpos=[ur'\.com', ]) + #2
lema(ur'(?:[Ss]emi|[Ss]ub|[Hh]iper|[Dd])esarrollar_í_a[ns]?_i') + #2
lema(ur'[Ss]ent_í_a[ns]_i', xpos=[ur' impel•lida', ]) + #2
lema(ur'[Ss]entir_á_[ns]?_a', xpre=[ur'\bet ', ]) + #2
lema(ur'[t]ra_í_an_i', xpos=[ur' in\b', ]) + #2
lema(ur'_Ú_ric(?:as|os?)_U', xpos=[ur' Schmitdt', ]) + #2
lema(ur'[Aa]mar_í_a[ns]?_i', xpre=[ur'Mohamad ', ur'denominadas ', ur'incluido ', ]) + #1
lema(ur'[Aa]nal_í_tic(?:as|os?)_i', xpre=[ur'ed ', ]) + #1
lema(ur'[Aa]t_ó_nit[ao]s?_o', xpre=[ur'[Ee]l ', ur'cenobitismo ', ]) + #1
lema(ur'[Bb]a_il_es?_li', xpos=[ur' (?:Peyton|Mangroe|Swart)', ur'’ Mangroe', ]) + #1
lema(ur'[Bb]erlin_é_s_e', xpre=[ur'Berlinesa\|', ur'Berlinesas\|', ur'dos ', ur'dos \'', ]) + #1
lema(ur'[Bb]istur_í__i', xpre=[ur'\bO ', ], xpos=[ur' - La', ur', la', ]) + #1
lema(ur'[Cc]aer_á_[ns]?_a', xpre=[ur' (?:of|be) ', ur'Camila ', ur'Cerrig y ', ur'Denk ', ], xpos=[ur' O\'Shaughneey', ur'\'', ]) + #1
lema(ur'[Cc]aminar_í_a_i', xpre=[ur'Hexatoma ', ]) + #1
lema(ur'[Dd]egenerar_í_a_i', xpre=[ur'Idaea ', ]) + #1
lema(ur'_É_pic(?:as|os)_E', xpre=[ur'Colón\|', ur'[y&] ', ]) + #1
lema(ur'fantas_í_as?_i', pre=ur'[Uu]nas? ', xpre=[ur'[Qq]uasi ', ]) + #1
lema(ur'[Gg]rand_í_sim[ao]s?_i', xpre=[ur'ymagen de ', ]) + #1
lema(ur'_ha_ (?:bajado|batallado|bebido|beneficiado|borrado|brillado|brindado|buscado)_ah?', xpre=[ur'[0-9]', ]) + #1
lema(ur'_ha_ dicho_ah?', pre=ur'(?:[Ll]es?|[Éé]l|[Ss]e(?: me| te| l[aeo]s?|)) ', xpre=[ur' con ', ]) + #1
lema(ur'[Hh]abit_ú_(?:a[ns]?|e[ns]?)_u', xpre=[ur'[Uu]n ', ur's\'', ]) + #1
lema(ur'[Hh]erb_á_ce(?:as|os?)_a', xpre=[ur'algodoeiros ', ]) + #1
lema(ur'[Ll]aborar_í_a[ns]?_i', xpre=[ur'inurri ', ]) + #1
lema(ur'[Ll]ucir_á_[ns]?_a', xpos=[ur' Yariff', ]) + #1
lema(ur'[Mm]ani_á_tic[ao]s?_a', xpre=[ur'[Ii]l ', ]) + #1
lema(ur'[Mm]oment_o_s?_ó', xpos=[ur' que todos', ]) + #1
lema(ur'[Mm]udar_í_a[ns]?_i', xpos=[ur' Nada Em', ur'\]', ]) + #1
lema(ur'Nas_á_u_a', xpre=[ur'Guillermo ', ur'Kuresa ', ur'Mikaele ', ], xpos=[ur' Street', ]) + #1
lema(ur'[Nn]acer_á_[ns]?_a', xpre=[ur'Benkhelifa ', ], xpos=[ur' Boukamoum', ]) + #1
lema(ur'[Nn]_í_tid(?:as|os?|amente)_i', xpos=[ur' [Nn]ulo', ]) + #1
lema(ur'[Pp]aisa_j_es?_g', xpos=[ur' de l´apparence', ur'\'', ]) + #1
lema(ur'[Pp]_ó_stumamente_o', xpre=[ur' ', ur'H', ur'a', ur'a', ur'e', ur'e', ur'g', ur'i', ur'm', ur'n', ur'o', ]) + #1
lema(ur'[Pp]_ú_lico_u', pre=ur'(?:[Aa]cceso|[Aa]cto|[Aa]seo|[Aa]cusador|[Aa]gente|[Aa]lumbrado|[Aa]l|[Aa]lboroto|[Aa]rtículo|[Áá]mbito|[Bb]achillerato|[Bb]alneario|[Bb]astante|[Bb]ien|[Cc]amino|[Cc]argo|[Cc]ar[áa]cter|[Cc][ée]sped|[Cc]olegio|[Cc]omponente|[Cc]oncurso|[Cc]onocimiento|[Cc]ontador|[Cc]on|[Cc]r[ée]dito|[Cc]rematorio|[Cc]ulto|[Dd]ebate|[Dd]el?(?: difícil|)|[Dd]erecho|[Dd]esorden|[Dd]inero|[Dd]ominio|[Dd]éficit|[Ee]dificio|[Ee]l(?: gran|)|[Ee]mpleado|[Ee]ndeudamiento|[Ee]n|[Ee]nte|[Ee]nemigo|[Ee]spacio|[Ee]spejo|[Ee]ste|[Gg]asto|[Ff]in|[Ff]uncionario|[Ii]nterés|[Ii]nstituto|[Ii]nvestigación|[Ll]lamamiento|[Ll]ugar|[Mm]anifiesto|[Mm]ercado|[Mm]inisterio|[Mm]irador|[Mm]ucho|[Nn]otario|[Nn]umeroso|[Oo]brero|[Oo]jo|[Oo]rden|[Oo]rganismo|[Pp]arking|[Pp]arque|[Pp]ersonaje|[Pp]oder|[Pp]resupuesto|[Pp]roblema|[Pp]roceso|[Pp]uesto|[Rr]egistro|[Rr]astro|[Rr]eloj|[Ss]ector|[Ss]ervicio|[Ss]ervidor|[Ss]in|[Ss]u(?: propio|)|[Tt]el[ée]fono|[Tt]ecnológico|[Tt]odo|[Tt]ransporte(?: urbano|)|[Tt]rabajo|[Uu]n|[Uu]so|entre|frontón|hacer?|hará|haría|hecho|hiciera|hicieron|hizo|mayor|más|mismo|nuevo|numeroso|para|tenía) ', xpos=[ur'\.es', ]) + #1
lema(ur'Reverter_á__a', xpre=[ur'Nicola ', ], xpos=[ur' della', ]) + #1
lema(ur'[Rr]eval_ú_(?:a[ns]?|e[ns]?)_u', xpos=[ur' currency', ]) + #1
lema(ur'[Rr]evert_í_(?:a[ns]?|)_i', xpre=[ur'Posse ', ur'missa ', ]) + #1
lema(ur'[Ss]ellar_í_a_i', xpre=[ur'della ', ]) + #1
lema(ur'[Ss]obrar_í_a[ns]?_i', xpre=[ur' de ', ur'Juan ', ]) + #1
lema(ur'[Ss]_ó_rdido_o', xpre=[ur'sentier ', ]) + #1
lema(ur'[Ss]um_á_r[mts]el[aeo]s?_a', xpos=[ur' la conquista de los Creek', ]) + #1
lema(ur'[Ss]umir_á_[ns]?_a', xpre=[ur'Mihara ', ], xpos=[ur', Tequivo', ]) + #1
lema(ur'[Uu]n_á_nimes_a', xpos=[ur' [Pp]ro [Dd]eo', ]) + #1
lema(ur'[Vv]en_z_(?:a[ns]?|o)_s', xpre=[ur'Sant ', ], xpos=[ur' (?:Klicic|Dolonc)', ]) + #1
 []][0]

grupo11 = [#Sin ocurrencias 2015/09 
# lema(ur'Arrastrar_í_a_i', xpre=[ur'Guerola ', ]) + #0
# lema(ur'Ben_í_n\]\]_i', xpre=[ur'(?:[Dd]e|[Ee]n) ', ur'Aero ', ur'Air ', ur'Airways ', ur'Dag ', ur'Joey ', ur'Morice ', ], xpos=[ur'\'s', ]) + #0
# lema(ur'Besar_í_a_i', xpre=[ur'Raj ', ]) + #0
# lema(ur'Dem_á_s_a', pre=ur'[Ll][ao]s ', xpre=[ur' el \'\'', ]) + #0
# lema(ur'Perd_í_a_i', xpre=[ur'Alejandro ', ]) + #0
# lema(ur'[Aa]_dquirió__quirio', xpre=[ur' en ', ]) + #0
# lema(ur'[Aa]burr_í_a_i', xpre=[ur'carunculada, ', ur'[Pp]ava ', ], xpos=[ur' (?:cujubi|común|cumanensis|jacutinga|[Aa]burri|pipile|jacutinga)', ur'[\]\']', ]) + #0
# lema(ur'[Aa]burrir_í_a[ns]?_i', xpos=[ur' cumanensis', ]) + #0
# lema(ur'[Aa]lent_ó__o', xpre=[ur'\bel ', ur'\bdo ', ur'Casale ', ur'Valle ', ur'[Rr][ií]o ', ], xpos=[ur' (?:da |de Dano|Salvatore|\(Campania)', ur'(?:\]|, 2011)', ]) + #0
# lema(ur'[Aa]lternar_í_an[ns]?_i', xpos=[ur'\]\]', ]) + #0
# lema(ur'[Aa]nimar_í_a[ns]?_i', xpre=[ur'of ', ], xpos=[ur'\'', ]) + #0
# lema(ur'[Aa]ntip_á_tic[ao]s?_a', xpre=[ur'sta ', ]) + #0
# lema(ur'[Aa]nular_í_a[ns]?_i', xpre=[ur'[Bb]lanco ', ], xpos=[ur'\]\]', ]) + #0
# lema(ur'[Aa]rchivar_í_a[ns]?_i', xpos=[ur', [1-9][0-9]+']) + #0
# lema(ur'[Aa]rd_í_as_i', xpre=[ur'de ']) + #0
# lema(ur'[Aa]rdi_ó__o', xpre=[ur'Guzmán y ', ur'Ventura ', ]) + #0
# lema(ur'[Aa]rmar_í_a[ns]?_i', xpos=[ur'\]', ]) + #0
# lema(ur'[Aa]rticular_í_a_i', xpos=[ur'\]\]', ]) + #0
# lema(ur'[Aa]sar_í_an_i', xpre=[ur'Albert ', ur'Frank ', ]) + #0
# lema(ur'[Cc]alent_ó__o', xpre=[ur'llamada \'\''], xpos=[ur'\]', ]) + #0
# lema(ur'[Cc]allar_í_a_i', xpre=[ur'Amazonepeira ', ], xpos=[ur'\'', ]) + #0
# lema(ur'[Cc]almar_í_a_i', xpre=[ur'\ba ']) + #0
# lema(ur'[Cc]an_ó_nic(?:[ao]s|amente)_o', xpre=[ur'Epistulas ', ], xpos=[ur' vocant', ]) + #0
# lema(ur'[Cc]ancelar_í_a[ns]?_i', xpre=[ur'hacia ', ]) + #0
# lema(ur'[Cc]eg_ó__o', xpre=[ur'Cal ', ur'mur ', ur'Mateus ', ur' d[eo] ', ur' [eé] '], xpos=[ur' (?:da|Rabequista)\b']) + 32
# lema(ur'[Cc]ern_í_a[ns]?_i', xpos=[ur' ad ', ]) + #0
# lema(ur'[Cc]erner_á_[ns]?_a', xpos=[ur' de Zalima', ]) + #0
# lema(ur'[Cc]itol_ó_gic[ao]s?_o', xpos=[ur'\.org', ]) + #0
# lema(ur'[Cc]lar_í_sim[ao]s?_i', xpos=[ur'\'', ]) + #0
# lema(ur'[Cc]olar_í_a[ns]?_i', xpos=[ur' acuminata', ]) + #0
# lema(ur'[Cc]omentar_í_a[ns]_i', xpre=[ur'Frases ', ]) + #0
# lema(ur'[Cc]omentar_í_a_i', xpre=[ur'Cerynea ', ur'Hippocratis, ', ], xpos=[ur' in', ur' juris', ]) + #0
# lema(ur'[Cc]omet_í_a[ns]?_i', xpos=[ur'\'', ]) + #0
# lema(ur'[Cc]onsol_ó__o', xpre=[ur'Vincenzo ', ur'Gina ', ur'Bartolo ', ur'Federico ', ur'Precisam de ', ur'Margherita ', ], xpos=[ur' (?:\||seguirá)']) + 35
# lema(ur'[Cc]ontendi_ó__o', xpre=[ur'su ', ]) + #0
# lema(ur'[Cc]ontentar_í_a[ns]?_i', xpre=[ur'Cerynea ', ]) + #0
# lema(ur'[Cc]onv_irtió__ertio', xpre=[ur'[Ee]s ', ur'[Ff]ue ', ur'[Ss]er ', ]) + #0
# lema(ur'[Cc]onviv_í_a_i', xpos=[ur' [Ll]iteraria', ur'\'', ]) + #0
# lema(ur'[Cc]orri_ó__o', xpre=[ur'del ', ]) + #0
# lema(ur'[Cc]osm_é_tica_e', xpre=[ur'Ardisia ', ur'Misa ', ], xpos=[ur' Moderna - Prodotti', ]) + #0
# lema(ur'[Cc]riminal_í_stic(?:as|os?)_i', xpos=[ur'\.unne', ]) + #0
# lema(ur'[Dd]escubri_ó__o', xpre=[ur'quando ', ]) + #0
# lema(ur'[Dd]esertar_í_a_i', xpos=[ur'\]\]', ]) + #0
# lema(ur'[Dd]ictar_í_a[ns]?_i', xpre=[ur'Corgatha ', ]) + #0
# lema(ur'[Dd]irig_ió__o', xpre=[ur'Carmen ', ur'estado : ', ], xpos=[ur' por', ur'[\'”]', ]) + #0
# lema(ur'[Dd]isect_ó__o', xpos=[ur'\'', ]) + #0
# lema(ur'[Ee]conom_é_trica_e', xpos=[ur'(?:[\]\']|, Econometric|, Vol|, Review)', ur' 50/1', ]) + #0
# lema(ur'[Ee]ditar_í_a[ns]?_i', xpre=[ur'Nota ', ]) + #0
# lema(ur'[Ee]mp_í_ric[ao]s?_i', xpre=[ur'Psychologia ', ur'di vista ', ], xpos=[ur'\'', ]) + #0
# lema(ur'[Ee]n_é_rgico_e', xpre=[ur'Allegro ', ur'Sempre ', ur'ma ', ], xpos=[ur'\'', ]) + #0
# lema(ur'[Ee]nfermar_í_a[ns]?_i', xpos=[ur'\'', ]) + #0
# lema(ur'[Ee]nterr_ó__o', xpre=[ur'O ', ur'[Ll][\'’]', ], xpos=[ur' d[ao]', ]) + #0
# lema(ur'[Ee]st_á_ regenerad[ao]_a', xpos=[ur' veneración', ]) + #0
# lema(ur'[Ee]stampar_í_a[ns]?_i', xpre=[ur'Na ', ]) + #0
# lema(ur'[Ee]vadi_ó__o', xpre=[ur'Néstor ', ]) + #0
# lema(ur'[Ee]x_ces_iv[ao]s?_', xpre=[ur'Aucula ']) + #0
# lema(ur'[Ff]ant_á_stic[ao]_a', xpre=[ur'e del ', ur' e ', ur'Ceropegia ', ur'Divertimento ', ur'Egostico ', ur'Fantasia & ', ur'J\.P\. ', ur'Liparis ', ur'Loxia ', ur'MSC ', ur'Neocteniza ', ur'Pleurothallis ', ur'Polonica ', ur'Ranitomeya ', ur'Sei ', ur'Terra ', ], xpos=[ur' (?:8|3|12|mondo|nella|Club)', ur'["\']', ]) + #0
# lema(ur'[Ff]icolog_í_as?_i', xpre=[ur'Brasileira de ']) + #0
# lema(ur'[Ff]inanciar_í_a[ns]?_i', xpre=[ur'organizaciones ', ]) + #0
# lema(ur'[Ff]omentar_í_a_i', xpre=[ur'Ungulina ', ]) + #0
# lema(ur'[Ff]renes_í__i', xpre=[ur'Coleção '], xpos=[ur' \(Lisboa', ur': história']) + #0
# lema(ur'[Gg]em_í_a[ns]?_i', xpos=[ur' Jasani', ]) + #0
# lema(ur'[Gg]eriatr_í_as?_i', xpos=[ur' e Gerontologia', ]) + #0
# lema(ur'[Gg]estionar_í_a[ns]?_i', xpre=[ur'entidades ', ]) + #0
# lema(ur'[Hh]a_ll_ada_y', xpre=[ur'Tras la ', ], xpos=[ur' Asturias', ]) + #0
# lema(ur'[Hh]abitar_í_a_i', xpos=[ur'\]\]', ]) + #0
# lema(ur'[Hh]ero_í_smos?_i', xpre=[ur' do ', ur'\'', ], xpos=[ur' e lealdade', ]) + #0
# lema(ur'[Hh]err_ó__o', xpre=[ur'Marcelle ', ur'Mike ', ], xpos=[ur'\'', ]) + #0
# lema(ur'[Hh]iri_ó__o', xpos=[ur'\]', ]) + #0
# lema(ur'[Ii]_m_perial_n', xpos=[ur' sedendo', ]) + #0
# lema(ur'[Ii]_m_presas_n', xpre=[ur'domínios de ', ]) + #0
# lema(ur'[Ii]ncens_ó__o', xpos=[ur' e discordia', ]) + 5
# lema(ur'[Ii]nformar_í_a[ns]?_i', xpos=[ur' Digital', ur'\.com', ]) + #0
# lema(ur'[Ii]nfund_í_a[ns]?_i', xpos=[ur'\'', ]) + #0
# lema(ur'[Ii]nic_i_os?_', xpos=[ur' d[\'’]Avalos', ur'\'\'\'']) + #0
# lema(ur'[Ii]niciar_í_a[ns]?_i', xpre=[ur'sus ', ]) + #0
# lema(ur'[Jj]od_í_a[ns]?_i', xpos=[ur'\]', ]) + #0
# lema(ur'[Jj]ubilar_í_as?_i', xpre=[ur'Loheria ', ], xpos=[ur'[\'\]]', ]) + #0
# lema(ur'[Ll]_ó_gicas_o', xpre=[ur' ', ur'c', ur'm', ur'u', ]) + #0
# lema(ur'[Ll]abrar_í_a_i', xpre=[ur'Abraxas ']) + #0
# lema(ur'[Ll]amentar_í_a_i', xpre=[ur'T\. ', ur'Tipula ', ]) + #0
# lema(ur'[Ll]e_y_endas?_g', xpre=[ur'"', ur'\'\'', ur'A ', ur'Fuente ', ur'Nova ', ur'Oxford: ', ur'Paleosepharia ', ur'Pendragon ', ur'Siri ', ur'Sistema ', ur'latín \'\'', ur'nume de ', ur'Áurea ', ur'Česká ', ], xpos=[ur' (?:minor|Editore|Cinta|Ular|Chernigov|sanctorum|Sundel|áurea|jazz|Wormnet|[Aa]urea|Prima|Secunda|Maior|Trium|del pianista sull\'|Sanctorum|para Viola|\(Legenda|Srl Cartografia|eps\.|, 2001|2001|om )', ur'\]', ]) + #0
# lema(ur'[Ll]eer_á_[ns]?_a', xpos=[ur'\]', ]) + #0
# lema(ur'[Ll]exicograf_í_as?_i', xpre=[ur'Lexicologia y '], xpos=[ur' (?:e os|catalana|catalanes)\b']) + #0
# lema(ur'[Mm]andar_í_a_i', xpre=[ur'Tako ', ]) + #0
# lema(ur'[Mm]arginar_í_a_i', xpos=[ur' (?:del Mundo Gráfico|angustifolia|ensifolia|incana|polypodioides|\(protista)', ur'(?:\]\]|\'\')', ]) + #0
# lema(ur'[Mm]inar_í_a[ns]?_i', xpos=[ur'\]\]', ]) + #0
# lema(ur'[Mm]oli_ó__o', xpos=[ur'\]\]', ]) + #0
# lema(ur'[Mm]orfol_ó_gic(?:[ao]s|amente)_o', xpos=[ur' e\b']) + #0
# lema(ur'[Nn]ombór_ó__o', xpre=[ur'[Tt]e ', ]) + #0
# lema(ur'[Oo]sar_í_an_i', xpre=[ur'[Ee]l ', ]) + #0
# lema(ur'[Oo]sar_í_as?_i', xpos=[ur'\'\'']) + #0
# lema(ur'[Pp]arar_í_a[ns]?_i', xpre=[ur'T\. ', ur'Tipula ', ]) + #0
# lema(ur'[Pp]atinar_í_a_i', xpre=[ur'Stelis ', ]) + #0
# lema(ur'[Pp]avimentar_í_a_i', xpre=[ur'Revolución ', ur'[Ff]orma ', ]) + #0
# lema(ur'[Pp]ed_í_a[ns]?_i', xpre=[ur'Cilicia ', ur'Soft ', ur'Arteria ', ur'Elísia ', ur'Gens ', ur'[0-9]', ur'[Ll]ex ', ur'arteria ', ur'placa ', ur'posteriores y ', ur'ta ', ], xpos=[ur' tou', ur'(?:\'|\]\])', ]) + #0
# lema(ur'[Pp]erd_í__i', xpre=[ur'A\. ', ur'Australoheros ', ur'Campamento ', ur'Campo ', ur'Eleanor y ', ], xpos=[ur' (?:la mi rueca|aquest|[Vv]ocê)', ur'\'\'', ]) + #0
# lema(ur'[Pp]ereci_ó__o', xpre=[ur'Lodovico ', ]) + #0
# lema(ur'[Pp]illar_í_a_i', xpre=[ur'Cycloclypeus ']) + #0
# lema(ur'[Pp]rend_é_r[mts]el[aeo]s?_e', xpre=[ur'come ', ]) + #0
# lema(ur'[Pp]ris_o_n_i[oó]', pre=ur'[Ii]n ') + #0
# lema(ur'[Pp]rofiri_ó__o', xpos=[ur'\'', ]) + #0
# lema(ur'[Pp]ul_í_a[ns]?_i', xpre=[ur'Gottfried ', ]) + #0
# lema(ur'[Pp]uli_ó__o', xpos=[ur' Elio', ]) + #0
# lema(ur'[Pp]ulir_á_[ns]?_a', xpre=[ur'\* ', ]) + #0
# lema(ur'[Q]uebr_ó__o', xpre=[ur'\bde ', ur'\* '], xpos=[ur' y Arenas', ur'[,\'\]]', ]) + #0
# lema(ur'[Rr]efinar_í_a[ns]?_i', xpos=[ur' (?:do|União|de Paulínia|Petrobras)', ]) + #0
# lema(ur'[Rr]efrendar_í_a[ns]?_i', xpre=[ur' no ', ]) + #0
# lema(ur'[Rr]emend_ó__o', xpre=[ur' i ', ]) + #0
# lema(ur'[Rr]etar_í_a[ns]?_i', xpos=[ur'\]\]', ]) + #0
# lema(ur'[Ss]_e_ están?_é', xpos=[ur' aficionado']) + #0
# lema(ur'[Ss]_ó_tano_o', xpre=[ur'\'', ur'Zorocrates ', ur'Piaggine ']) + #0
# lema(ur'[Ss]_ú_per As_u', xpos=[ur' d’Or']) + #0
# lema(ur'[Ss]acar_í_a[ns]?_i', xpos=[ur'\]', ]) + #0
# lema(ur'[Ss]anar_í_a_i', xpre=[ur'de ', ]) + #0
# lema(ur'[Ss]erv_í_as_i', xpre=[ur'Katepanikion ', ur'expansiones ', ur'murallas ', ]) + #0
# lema(ur'[Ss]imult_á_neo_a', xpos=[ur'\'', ]) + #0
# lema(ur'[Ss]olemn_í_sim[ao]s?_i', xpos=[ur' fiesta del Santissimo', ]) + #0
# lema(ur'[Ss]onar_í_a[ns]?_i', xpos=[ur' Festival', ]) + #0
# lema(ur'[Ss]ulf_ú_ric[ao]s?_u', xpre=[ur'Dipoena ']) + #0
# lema(ur'[Ss]um_í_a[ns]?_i', xpre=[ur'Henri ', ur'\* ', ]) + #0
# lema(ur'[Ss]uministrar_í_a[ns]?_i', xpre=[ur'Bolivia les ', ]) + #0
# lema(ur'[Ss]ustra_í_a_i', xpos=[ur'(?:\]\]|\')', ]) + #0
# lema(ur'[Tt]_ó_xica_o', xpre=[ur'Amanita ', ur'con ', ur'ser ', ], xpos=[ur' (?:y un|y Jindrax|a General)', ur'\'\'\'', ]) + #0
# lema(ur'[Tt]ect_ó_nica_o', xpos=[ur'\.es', ]) + #0
# lema(ur'[Tt]end_í__i', xpre=[ur' el ', ur'[Rr]ío ', ]) + #0
# lema(ur'[Tt]endi_ó__o', xpre=[ur'El ', ]) + #0
# lema(ur'[Tt]er_r_enos?_', xpre=[ur'Pica ', ur'[Mm]unicipio de ', ], xpos=[ur' (?:y Blanda|era descendiente)', ur'\'', ]) + #0
# lema(ur'[Tt]osi_ó__o', xpre=[ur'Paolo ', ], xpos=[ur' (?:Kato|Martinengo|\|apellido)', ]) + #0
# lema(ur'[Tt]rabar_í_a_i', xpre=[ur'Bocca ', ur'Massa ', ]) + #0
# lema(ur'[Uu]n_í_a_i', xpre=[ur'a la ', ur'Azoty ', ur'Miguel ', ur'padre ', ur'jaettuja ', ur'gira de ', ur'Krestanska ', ur'abandonando la ', ], xpos=[ur'(?:\]\]|\.es|\'\')', ur' (?:Raciborz|lubelska|Janikowo|Realnej|Racibórz|troista|polsko|Tarnów|Chorzów|Chrześcijańsko|Demokratyczna|Wolnośći|\(Sindicato|\(Nueva|Wolności|Pracy|Polityki)', ]) + #0
# lema(ur'[Vv]end_í_a[ns]?_i', xpre=[ur'Small ', ur'\bthe ', ur'\bof ', ur'[P]. ', ur'Plentusia ', ur'Wendos\|', ur'SS ', ur'\'\'', ], xpos=[ur'\[', ur' (?:Period|Animals)']) + #0
# lema(ur'[Vv]ers_á_til(?:es)_a', xpre=[ur'and ', ]) + #0
# lema(ur'[Vv]ersar_í_a_i', xpre=[ur'Flagrospira ']) + #0
# lema(ur'[Vv]iolar_í_a[ns]?_i', xpre=[ur'Hesperis ', ]) + #0
# lema(ur'[d]ominar_í_a_i', xpre=[ur' a ', ur'de ', ], xpos=[ur' a qui', ur'\]\]', ]) + #0
# lema(ur'[s]ubir_á__a', xpos=[ur' et', ]) + #0
# lema(ur'_a_ños?_A', pre=ur'(?:[Pp]rimer(?:os|)|[Ss]egundo|[Tt]ercer) ', xpos=[ur' (?:Nuevo|Polar|Santo)']) + #381
# lema(ur'_c_omunicación_C', pre=ur'de ', xpre=[ur'Red Privada ', ur'Servicios ', ur'Paraguaya ', ur'Federal de Servicios ', ur'Municipal ', ur'[Mm]inistr[oa] ', ur'Secretaría ', ur'Director ', ur'Departamento ', ur'Facultad ', ur'Comunidad ', ur'estudios ', ur'Gabinete ', ur'Quintanarroense ', ur'Premio ', ur'Comisión ', ur'Bolivariano ', ur'[Mm]inisterio ', ur'[Mm]inistro ', ur'Asturias ']) + #4348
# lema(ur'_d_estinos?_D', pre=ur'[Yy] ', xpre=[ur'Dúos ']) + #1
# lema(ur'_e_studio_E', pre=ur'de ', xpre=[ur'Parques ', ur'Casa ', ur'Instituto '], xpos=[ur' (?:y Seguimiento|de Lenguas|del Régimen|Interactivo)']) + #1708
# lema(ur'_Á_gil_A', xpre=[ur'L\'', ur'St ', ur'presentando a ', ur'graminicidas ', ], xpos=[ur' (?:Syed|Mammadov|Naguib|Nabiyev|Etemadi)', ]) + #0
# lema(ur'_Ó_pticas?_O', xpre=[ur'[Ff]estival ', ur'\bda ', ur'[Pp]ars ', ], xpos=[ur' (?:Gand[ií]a|[Pp]romota|[Ff]estival||atapuerquensis)', ur'(?:\'|\.info)', ]) + #0
# lema(ur'_á_urea_a', xpre=[ur' et ', ur'Atteva ', ur'Aciphylla ', ur'Agave ', ur'Aglossorrhyncha ', ur'Aldina ', ur'Alstroemeria ', ur'Amarylis ', ur'Amaryllis ', ur'Amia ', ur'Aquilegia ', ur'Aratinga ', ur'Areca ', ur'Athamanta ', ur'Babiana ', ur'Barbacenia ', ur'Bartonia ', ur'Berberis ', ur'Betula ', ur'Bidens ', ur'Bifrenaria ', ur'Bignonia ', ur'Blakistonia ', ur'Broughtonia ', ur'Brugmansia ', ur'Buxus ', ur'Calamagrostis ', ur'Calpurnia ', ur'Campomanesia ', ur'Capnoides ', ur'Carex ', ur'Cattleya ', ur'Cavacoa ', ur'Chamomilla ', ur'Chrysopteris ', ur'Chuquiraga ', ur'Chysis ', ur'Clidemia ', ur'Corbularia ', ur'Coreopsis ', ur'Corydalis ', ur'Crepis ', ur'Croaspila ', ur'Crocosmia ', ur'Cyclopia ', ur'Cyrtanthera ', ur'Daemonorops ', ur'Dalea ', ur'Daphne ', ur'Dasistoma ', ur'Datura ', ur'Daubenya ', ur'Deyeuxia ', ur'Dioclea ', ur'Diplommatina ', ur'Diuris ', ur'Draba ', ur'Dyckia ', ur'Echinopsis ', ur'Emblemata ', ur'Eulalia ', ur'Expositio ', ur'Ficus ', ur'Fragaria ', ur'Fragmenta ', ur'Frailea ', ur'Fumaria ', ur'Gaya ', ur'Gentianella ', ur'Gloriosa ', ur'Greenovia ', ur'Grevillea ', ur'Hebenstretia ', ur'Heliconia ', ur'Heritiera ', ur'Hieronymiella ', ur'Hymenaea ', ur'Hymenorebutia ', ur'Iris ', ur'Ixia ', ur'Justicia ', ur'Lachnaea ', ur'Laelia ', ur'Lalage ', ur'Lamarckia ', ur'Leandra ', ur'Leavenworthia ', ur'Legenda ', ur'Lepanthes ', ur'Lesquerella ', ur'Lindmania ', ur'Litoria ', ur'Lobivia ', ur'Lophiola ', ur'Loxosceles ', ur'Lycoris ', ur'Lycosa ', ur'Mendoncia ', ur'Millettia ', ur'Mormodes ', ur'Musschia ', ur'Myrmechis ', ur'Myrrhis ', ur'Navia ', ur'Neckeria ', ur'Nectandra ', ur'Nerine ', ur'Neskiza ', ur'Odoptera ', ur'Oeceoclades ', ur'Opuntia ', ur'Opuscula ', ur'Pachira ', ur'Pachycephala ', ur'Packera ', ur'Pallenis ', ur'Pamphilia ', ur'Panorpa ', ur'Paradrymonia ', ur'Pentachaeta ', ur'Pentachaeta ', ur'Ph\. ', ur'Phaeolepiota ', ur'Phlomis ', ur'Phyllostachys ', ur'Phyllostachys\' ', ur'Pimpinella ', ur'Piriqueta ', ur'Pleopeltis ', ur'Podalyria ', ur'Populus ', ur'Potentilla ', ur'Protea ', ur'Pseudolobivia ', ur'Quadrula ', ur'Rapanea ', ur'Ruizia ', ur'Russula ', ur'Sanchezia ', ur'Saxifraga ', ur'Scandix ', ur'Scaphyglottis ', ur'Selenia ', ur'Sinoarundinaria ', ur'Solenopsis ', ur'Sophora ', ur'Spathoglottis ', ur'Stylosanthes ', ur'Syncarpha ', ur'Tabebuia ', ur'Tabebuia ', ur'Tecoma ', ur'Thelypodiopsis ', ur'Thuja ', ur'Thymophylla ', ur'Todaroa ', ur'Trichocline ', ur'Tristachya ', ur'Tritonia ', ur'Utricularia ', ur'Verticordia ', ur'Villa ', ur'Viola ', ur'Virgilia ', ur'Xanthomyrtus ', ur'Zizia ', ur'[ABCDEfFGLMQSTZ]\. ', ur'abeillei ', ur'aurea ', ur'bulla ', ur'cult\. ', ur'justicia ', ur'latino, ', ur'mea ', ur'rubra\]\]\'\' ', ur'subsp\. ', ur'var\. ', ], xpos=[ur' (?:mediocritas|donavit)', ur'[\'\]]', ]) + #0
# lema(ur'arar_í_a_i', xpre=[ur'Grewia ', ], xpos=[ur'\.bih', ]) + #0
# lema(ur'capitular_í_a_i', xpos=[ur'\'', ]) + #0
# lema(ur'clavar_í_as_i', xpre=[ur'a las ', ur'para ', ]) + #0
# lema(ur'deb_í_a[ns]?_i', xpre=[ur'L\. ', ], xpos=[ur' installer', ur'(?:[\]\']|\.org)', ]) + #0
# lema(ur'fa_s_cino_', xpos=[ur' Cane', ]) + #0
# lema(ur'partir_í_a[ns]?_i', xpre=[ur'Phocides ', ]) + #0
# lema(ur'secessione\. ', pre=ur'[Dd]i_á_logos_a', xpre=[ur'Lancia ', ur'educaçao: ', ur'el ', ur'secessione. Un ', ], xpos=[ur' (?:del bienaue|between)', ur'\]', ]) + #0
# lema(ur'talar_í_a_i', xpos=[ur'\]\]', ]) + #0
  []][0]

### Por revisar, han fallado receintemente.
congelador = [
lema(ur'[Aa]divin_ó__o', xpre=[ur'caso ', ur'enano ', ur'(?:ser|del) ', ur'\b([AaEe]l|es|un) '], xpos=[ur'\)']) + #1
lema(ur'[Dd]esterr_ó__o', xpre=[ur'Florianópolis\|', ur'\bO ', ur'\bd[eo] ', ], xpos=[ur' (?:do|RC|\(Santa)', ur'(?:: Edições|\]\]|\')', ]) + #32
lema(ur'[Ss]err_ó__o', xpos=[ur' (?:do|Ventoso)\b', ur'(?:\]\]|, Zifronte)', ]) + #23
lema(ur'_Centroamé_rica_[Cc]entroame', xpos=[ur'\]\]n[ao]s?', ]) + #55
lema(ur'_C_hile_c', pre=ur'[Dd]e ', xpre=[ur'deshidratadoras ', ur'capa ', ur'cultivo '], xpos=[ur' (?:rojo|colorado|en polvo|y cenizas|jalapeño|poblano)']) + #1
lema(ur'[Ff]und_ó__o', xpre=[ur'Passo ', ur'\b(?:[AaEe]l|[Uu]n) ', ur'del '], xpos=[ur' legal', ur'(?:\]\]|\|)']) + #1
lema(ur'_p_olaco_P', pre=ur'ejército ') + #2
lema(ur'_p_rimer ejército_P', pre=ur'(?:(?:[Ee]l|[Uu]n|del) |\[\[|\|)') + #3
lema(ur'_r_uso_R', pre=ur'ejército ') + #8
lema(ur'_s_egundo ejército_S', pre=ur'(?:(?:[Ee]l|[Uu]n|del) |\[\[|\|)') + #3
lema(ur'_t_ercer ejército_T', pre=ur'(?:(?:[Ee]l|[Uu]n|del) |\[\[|\|)') + #4
lema(ur'_i_nternacional(?:es|)_I', pre=ur'[Cc]ampeonatos? ') + #613
lema(ur'_m_inistro_M', pre=ur'[Pp]rimer ') + lema(ur'_p_rimer (?:ministro)_P', pre=ur'(?:(?:[Ee]l|[Uu]n|al|del|siendo|cuarto|electo) |\||\[\[|[\|\'])') + #1364
lema(ur'_m_undial(?:es|)_M', pre=ur'[Cc]ampeonatos? ') + #1
lema(ur'_a_cumulad[ao]s?_A', pre=ur'(?:[Gg]eneral(?:es|)) ') + #1
lema(ur'_a_lternativos?_A', pre=ur'(?:[Mm]edios?) ') + #1
lema(ur'_b_anda_B', pre=ur'(?:[Mm]ejor|[Pp]eor) ') + #1
lema(ur'_c_lasificación_C', pre=ur'(?:[Gg]eneral de) ') + #1
lema(ur'_c_lasificatori[ao]s?_C', pre=ur'(?:[Rr]onda) ') + #1
lema(ur'_c_ocientes?_C', pre=ur'(?:[Gg]eneral de) ') + #1
lema(ur'_c_ompetencia_C', pre=ur'(?:[Gg]eneral de) ') + #1
lema(ur'_d_isciplinas_D', pre=ur'[Pp]or ') + #281
lema(ur'_d_ram[áa]tic[ao]s?_D', pre=ur'[Ss]erie ') + #1
lema(ur'_e_liminatori[ao]s?_E', pre=ur'(?:[Rr]ondas?|[Tt]orneos?|[Pp]artidos?) ') + #1008
lema(ur'_e_pisodios_E', pre=ur'de ') + #1008
lema(ur'_f_auna_F', pre=ur'[Nn]acional de ') + #1
lema(ur'_f_emenin[ao]_F', pre=ur'(?:[Nn]acional) ') + #1
lema(ur'_f_emeninos_F', pre=ur'(?:[Ii]ndividuales|[Dd]obles) ') + #363
lema(ur'_f_inales_F', pre=ur'[Rr]ondas ') + #1806
lema(ur'_g_eneral_G', pre=ur'(?:[Tt]abla|[Cc]lasificación) ') + #1
lema(ur'_i_ndividuales_I', pre=ur'[Dd]istinciones ') + #364
lema(ur'_i_nferior_I', pre=ur'[Cc]uadro ') + #2970
lema(ur'_i_ntern[ao]s?_I', pre=ur'[Cc]omunicación ') + #1
lema(ur'_l_ugar_L', pre=ur'(?:[Pp]rimer|[Ss]egundo|[Tt]ercer|[Cc]uarto|[Qq]uinto|[Ss]exto|[Ss]éptimo|[Oo]ctavo|[Nn]oveno|[Dd]écimo) ') + lema(ur'_p_rimer (?:lugar)_P', pre=ur'(?:(?:[Ee]l|[Uu]n|al|del|siendo|nombrado) |\[\[|\|) ') + #1364
lema(ur'_m_asculin[ao]_M', pre=ur'(?:[Nn]acional) ') + #1261
lema(ur'_m_asculinos_M', pre=ur'(?:[Ii]ndividuales|[Dd]obles) ') + #1261
lema(ur'_m_usical(?:es|)_M', pre=ur'[Vv][íi]deos? ') + #1164
lema(ur'_n_acional(?:es|)_N', pre=ur'(?:[Pp]arques?|[Rr]onda) ', xpre=[ur'Ley de ', ur'estación\)\|', ur'Radio ', ur'Leguminosas del ', ur'\bdo ', ur'Red de ', ur'Aeropuerto ', ur'Autónomo ', ur'[Ss]istema de ', ur'[Aa]dministración de ', ur'[Ss]ervicio de ', ], xpos=[ur' (?:Andinos-Patagónicos|\(estación)', ur'\'\'\' hará']) + lema(ur'_n_acional(?:es|)_N', pre=ur'(?:[Rr]eservas?|[Ss]elecci(?:ón|ones)) ') + lema(ur'_n_atural(?:es|)_N', pre=ur'(?:[Pa]arques?|[Nn]acional(?:es|)(?: y|)|[AÁaá]reas?) ') + lema(ur'_p_arque (?:nacional|natural)_P', pre=ur'(?:(?:[Ee]l|[Dd]el|[Uu]n) |\[\[|[|\'])') + lema(ur'_s_elección nacional_S', pre=ur'(?:(?:[Ll]a|[Uu]na) |\[\[)') + lema(ur'_r_eserva nacional_R', pre=ur'(?:(?:[Ll]a|[Uu]na) |\[\[)') + #30125
lema(ur'_n_ominaciones_N', pre=ur'[Pp]remios y ') + #726
lema(ur'_o_ficial_O', pre=ur'(?:[Pp][aá]gina|[Ww]eb) ') + #14456
lema(ur'_p_articipantes_P', pre=ur'[Ee]quipos ') + #578
lema(ur'_p_eriodismo_P', pre=ur'y ') + #1
lema(ur'_p_ersonal(?:es|)_P', pre=ur'[Ww]eb ') + #578
lema(ur'_p_osiciones_P', pre=ur'de ') + #495
lema(ur'_p_rincipales_P', pre=ur'[Pp]ersonajes ') + #544
lema(ur'_p_rofesional_P', pre=ur'[Cc]arrera ') + #389
lema(ur'_p_rotegidas?_P', pre=ur'[Nn]atural(?:es|) ') + #1
lema(ur'_r_eferencias?_R', pre=ur'(?:[Ee]xternos y) ') + #1
lema(ur'_r_onda_R', pre=ur'(?:[Pp]rimera|[Ss]egunda|[Tt]ercera|[Cc]uarta|[Úú]ltima) ') + #33695
lema(ur'_s_ocial_S', pre=ur'[Cc]omunicación ') + #1686
lema(ur'_s_onora_S', pre=ur'[Bb]anda ') + #1686
lema(ur'_s_uperior_S', pre=ur'[Cc]uadro ') + #3197
lema(ur'_t_emas_T', pre=ur'(?:[Ll]istas?|[Ll]istados?) de ') + #587
lema(ur'_w_eb_W', pre=ur'(?:[Pp][aá]gina|[Ss]itio|[Pp]ortal) ') + #5102
lema(ur'[Aa]_m_parados?_n') + #1
lema(ur'_a_cumulad[ao]s?_A', pre=ur'(?:[Gg]eneral(?:es|)) ') + #1
lema(ur'_a_lternativos?_A', pre=ur'(?:[Mm]edios?) ') + #1
lema(ur'_b_anda_B', pre=ur'(?:[Mm]ejor|[Pp]eor) ') + #1
lema(ur'_c_lasificación_C', pre=ur'(?:[Gg]eneral de) ') + #1
lema(ur'_c_lasificatori[ao]s?_C', pre=ur'(?:[Rr]onda) ') + #1
lema(ur'_c_ocientes?_C', pre=ur'(?:[Gg]eneral de) ') + #1
lema(ur'_c_ompetencia_C', pre=ur'(?:[Gg]eneral de) ') + #1
lema(ur'_d_isciplinas_D', pre=ur'[Pp]or ') + #281
lema(ur'_d_ram[áa]tic[ao]s?_D', pre=ur'[Ss]erie ') + #1
lema(ur'_e_liminatori[ao]s?_E', pre=ur'(?:[Rr]ondas?|[Tt]orneos?|[Pp]artidos?) ') + #1008
lema(ur'_e_pisodios_E', pre=ur'de ') + #1008
lema(ur'_f_auna_F', pre=ur'[Nn]acional de ') + #1
lema(ur'_f_emenin[ao]_F', pre=ur'(?:[Nn]acional) ') + #1
lema(ur'_f_emeninos_F', pre=ur'(?:[Ii]ndividuales|[Dd]obles) ') + #363
lema(ur'_f_inales_F', pre=ur'[Rr]ondas ') + #1806
lema(ur'_g_eneral_G', pre=ur'(?:[Tt]abla|[Cc]lasificación) ') + #1
lema(ur'_i_ndividuales_I', pre=ur'[Dd]istinciones ') + #364
lema(ur'_i_nferior_I', pre=ur'[Cc]uadro ') + #2970
lema(ur'_i_ntern[ao]s?_I', pre=ur'[Cc]omunicación ') + #1
lema(ur'_l_ugar_L', pre=ur'(?:[Pp]rimer|[Ss]egundo|[Tt]ercer|[Cc]uarto|[Qq]uinto|[Ss]exto|[Ss]éptimo|[Oo]ctavo|[Nn]oveno|[Dd]écimo) ') + lema(ur'_p_rimer (?:lugar)_P', pre=ur'(?:(?:[Ee]l|[Uu]n|al|del|siendo|nombrado) |\[\[|\|) ') + #1364
lema(ur'_m_asculin[ao]_M', pre=ur'(?:[Nn]acional) ') + #1261
lema(ur'_m_asculinos_M', pre=ur'(?:[Ii]ndividuales|[Dd]obles) ') + #1261
lema(ur'_m_usical(?:es|)_M', pre=ur'[Vv][íi]deos? ') + #1164
lema(ur'_n_acional(?:es|)_N', pre=ur'(?:[Pp]arques?|[Rr]onda) ', xpre=[ur'Ley de ', ur'estación\)\|', ur'Radio ', ur'Leguminosas del ', ur'\bdo ', ur'Red de ', ur'Aeropuerto ', ur'Autónomo ', ur'[Ss]istema de ', ur'[Aa]dministración de ', ur'[Ss]ervicio de ', ], xpos=[ur' (?:Andinos-Patagónicos|\(estación)', ur'\'\'\' hará']) + lema(ur'_n_acional(?:es|)_N', pre=ur'(?:[Rr]eservas?|[Ss]elecci(?:ón|ones)) ') + lema(ur'_n_atural(?:es|)_N', pre=ur'(?:[Pa]arques?|[Nn]acional(?:es|)(?: y|)|[AÁaá]reas?) ') + lema(ur'_p_arque (?:nacional|natural)_P', pre=ur'(?:(?:[Ee]l|[Dd]el|[Uu]n) |\[\[|[|\'])') + lema(ur'_s_elección nacional_S', pre=ur'(?:(?:[Ll]a|[Uu]na) |\[\[)') + lema(ur'_r_eserva nacional_R', pre=ur'(?:(?:[Ll]a|[Uu]na) |\[\[)') + #30125
lema(ur'_n_ominaciones_N', pre=ur'[Pp]remios y ') + #726
lema(ur'_o_ficial_O', pre=ur'(?:[Pp][aá]gina|[Ww]eb) ') + #14456
lema(ur'_p_articipantes_P', pre=ur'[Ee]quipos ') + #578
lema(ur'_p_eriodismo_P', pre=ur'y ') + #1
lema(ur'_p_ersonal(?:es|)_P', pre=ur'[Ww]eb ') + #578
lema(ur'_p_osiciones_P', pre=ur'de ') + #495
lema(ur'_p_rincipales_P', pre=ur'[Pp]ersonajes ') + #544
lema(ur'_p_rofesional_P', pre=ur'[Cc]arrera ') + #389
lema(ur'_p_rotegidas?_P', pre=ur'[Nn]atural(?:es|) ') + #1
lema(ur'_r_eferencias?_R', pre=ur'(?:[Ee]xternos y) ') + #1
lema(ur'_r_onda_R', pre=ur'(?:[Pp]rimera|[Ss]egunda|[Tt]ercera|[Cc]uarta|[Úú]ltima) ') + #33695
lema(ur'_s_ocial_S', pre=ur'[Cc]omunicación ') + #1686
lema(ur'_s_onora_S', pre=ur'[Bb]anda ') + #1686
lema(ur'_s_uperior_S', pre=ur'[Cc]uadro ') + #3197
lema(ur'_t_emas_T', pre=ur'(?:[Ll]istas?|[Ll]istados?) de ') + #587
lema(ur'_w_eb_W', pre=ur'(?:[Pp][aá]gina|[Ss]itio|[Pp]ortal) ') + #5102
lema(ur'[Cc]eb_ú__u', xpre=[ur'\b(?:to|of) ', ur'Casino, ', ur'City\]\], ', ur'City\|', ur'Davao y '], xpos=[ur' (?:Pacific|City|International|Flowerpecker)', ur', Filipinas']) + #1
lema(ur'[Hh]_á_mster_a', xpre=[ur'Bounty ', ur'Original ', ur'impossible ', ur'The ', ur'Pamela '], xpos=[ur' (?:Mix|Mirror|Applet|Corporation|Software|Productions)', ur'\'s']) + #211
lema(ur'[Aa]ndalus_í__i', xpre=[ur'poeti ', ur'[Aa]l[- ]\'\'', ur'[Aa]l[- ]\'', ur'[Aa]l[- ]'], xpos=[ur' (?:Arabic|Mix)']) + #1
lema(ur'_Á_rabes?_A', xpre=[ur'\b(?:al|et) ', ur'[DdLl][’\']', ur'Danse ', ur'[LlDd]es ', ur'Culturel ', ur'\b(?:Art|ami|les) ', ur'Grammaire ', ur'source ', ur'Roman ', ur'Cinéma ', ur'Miguel de ', ur'Etudes ', ur'Chrestomatie ', ur'[Rr]évolutions ', ur'Français - ', ur'Auteurs ', ur'renouveau ', ur'Académie ', ur'Ouvrages ', ur'Dialectologie ', ur'Medicine ', ur'Monde ', ur'Musique ', ur'raids ', ur'Raison ', ur'Téléphone ', ur'Clase \'\'', ur'clase ', ur'[Cc]onquête '], xpos=[ur' (?:[0-9]+|à|et|of|au|avant|Bank|Bédouins|Associés|Syrienne|scenitae|Press|Presse|néonazi|medievale|assis|en Syrie|chrétiens)\b', ur', genèse']) + lema(ur'_á_rabes?_a', xpre=[ur'\b(?:et|en) ', ur'\be un ', ur'Danse ', ur'[Cc]ulture ', ur'Apocalypse ', ur'Baath ', ur'Caprice ', ur'Cavaliers ', ur'Cheval ', ur'Chrestomathie ', ur'Dialectologie ', ur'Famille ', ur'Fiancée ', ur'Fête ', ur'Grammaire ', ur'Littérature ', ur'Manuscrits ', ur'Mariage ', ur'Mots ', ur'Musique ', ur'Passions ', ur'Quartier ', ur'Relation ', ur'Scopitones ', ur'Téléphone ', ur'[DdLl][’\']', ur'[Ll]angues ', ur'[Ll]angue ', ur'[Mm]onde ', ur'[Mm]usique\.', ur'[Rr]évolution ', ur'[Rr]évolutions ', ur'[Tt]exte ', ur'[Tt]extes ', ur'[dl]es ', ur'chef ', ur'chevaux ', ur'colline ', ur'conquête ', ur'conte ', ur'des origines ', ur'dialectologie ', ur'dictionnaires ', ur'droit ', ur'et 100% ', ur'gaullisme ', ur'grammaticale ', ur'l\'expansion ', ur'littérature ', ur'livre ', ur'malheur ', ur'math[eé]matiques ', ur'medicine ', ur'mond ', ur'national ', ur'nationalisme ', ur'parentés ', ur'parler ', ur'pays ', ur'peinture ', ur'persans, ', ur'politique ', ur'populaires ', ur'poète ', ur'primavere ', ur'scholiastes ', ur'source ', ur'source ', ur'théâtre ', ur'écrivains ', ], xpos=[ur' (?:et|du|au|dans|aux|par|actuels|parlé|scenitae|se défiant|contemporaine|sahraouie|néonazi|medievale|en Numidie|dans)\b', ur', genèse', ]) + #600

lema(ur'Dub_á_i_a', xpre=[ur'\b(?:in|of) ', ur'\band ', ur'(?:Art|Bur) ', ur'Airport ', ur'Al-Ahli ', ur'Burj ', ur'Cavalli ', ur'Center ', ur'College ', ur'Dive ', ur'Downtown ', ur'Dusit ', ur'Fairmont ', ur'Musical Festival ', ur'My ', ur'Nick ', ur'Noor ', ur'Palm ', ur'Pilani - ', ur'Prix ', ur'Report: ', ur'Sama ', ur'School, ', ur'Sevens ', ur'Ski ', ur'SkyDive ', ur'Tower & Hotel ', ur'Towers ', ur'University, ', ur'University[ #]', ur'Versace ', ur'[Xx]angainés a ', ur'chronique ', ], xpos=[ur' (?:and|Civil|Group|Design|Cares|Silicon|Islamic|Waterfront|Cargo|BFF|Eye|Land|Heritage|Wheel|Recycling|Excel|Club|Mirage|American|College|Rally|Football|Festival|Motor|Taxi|Electricity|MotorShow|Air ?Show|Palace|Health|One|TV|Properties|Financial|Community|Sound|Tennis|Ports|Rail|Internet|Studio|Summer|Shopping|Sevens|Humanitarian|International|Sports|Tour|Autodrome|Holding|Mall|Duty|Desert|Creek|Towers|Pearl|Classic|Marina|Academic|Knowledge|Healthcare|Investments|Media|World|City|Enterprise|Bank|\(yate)', ur'92', ]) + #1337
lema(ur'[Gg]ur_ú__u', xpre=[ur'\bA ', ur'\bof', ur'Blue ', ur'Game ', ur'Guru ', ur'Jandiala ', ur'Kang ', ur'Loop ', ur'Love ', ur'Metal ', ur'PC ', ur'Pavarn ', ur'Shanti ', ur'Shree ', ur'Skanda ', ur'Sree ', ur'Swami ', ur'The ', ur'Tien\'s ', ur'Time ', ur'Voodo ', ur'Wahe ', ur'rapero\)\|', ur'tare ', ur'the ', ], xpos=[ur' (?:And|\(?:Pathik|Meditation|Nanak|Josh|rapero|Ram|Guru|of|Publishing)\b', ]) + #1042
lema(ur'[Bb]iograf_í_as?_i', xpre=[ur'\bcom ', ur'\bda ', ur'\bo ', ur'Basaglia\. Una ', ur'Studi su ', ur'Uma Princesa\'\', ', ur'Un ', ur'[Uu]ma ', ur'l[\'’]arte. La ', ur'malagasy ', ur'nova ', ur'pela ', ur'per a una ', ur'tenen ', ], xpos=[ur' (?:il·lustrada|universale|spirituale|del gerarca|Maçônicas|Jacka|tra|per|su|da|na|essencial|Não|[Pp]ubblicata|política d\'un|do|di|des|della|de (?:um |Francesc|Magalhães|Fabrizio|polítics|Madre Vitória|David Miranda e IPDA|universal compendiada|Renata Tarragó Fàbregas: Guitarrista, professora|Josep Iglésies|parlamentaris)|del (?:mestre|silenzio|metge|silenci)|[ei] |pagana come|ufficiale|musicale|Petra|Ritrovata|no sítio|d[’\'](?:un|Assumpta)|intellettuale|degli|velikogo|non autorizzata|sitgetana|no Brasil)', ur'(?:\.(?:bcn|BCN|com|bon)|, obres|\] a )', ]) + #929
lema(ur'[Ee]nerg_í_a_i', xpre=[ur'\b(?:di|ed) ', ur'\be ', ur'(?:RKK|EDP|NPO) ', ur'Ansaldo ', ur'Bizkaia ', ur'Carangola empresa ', ur'Comissão Nacional de ', ur'Corporation ', ur'Direcção Geral de ', ur'E ', ur'Elettra ', ur'Galp ', ur'Iberdrola ', ur'Mello ', ur'Polska ', ur'RSC ', ur'Rovinari\|', ur'Som ', ur'[dl]\'', ur'cohete ', ur'nombre a \'\'\'', ur'nossa ', ], xpos=[ur' (?:Siciliana|Limited|Areena|Rovinari|Vladivostok|Trento|elettrica|Pandurii|Câmpia-Turzii|Nucleare| \(industria|e (?:Trustul|Manifatturiero|l|Trabalho|della|Circular))\b', ur'(?:\.ru|\'+ \(1957)', ]) + #444
lema(ur'[Pp]en_í_nsulas?_i', xpre=[ur'\b(?:in|on|Au|na) ', ur'\b[Aaes] ', ur'"', ur'(?:Pan|din) ', ur'Acadian ', ur'Adelaide ', ur'Alaska ', ur'Almanor ', ur'Antarctic ', ur'Arabic ', ur'Arauco ', ur'Ardisia ', ur'Ards ', ur'Athos ', ur'Avalon ', ur'Azuero ', ur'Baja ', ur'Balboa ', ur'Baldwin ', ur'Balkan ', ur'Banks ', ur'Banks ', ur'Barcelona ', ur'Beach ', ur'Beach\)\|', ur'Bear ', ur'Beara ', ur'Bellarine ', ur'Berwick, ', ur'Bolivar ', ur'Bolívar ', ur'Boothia ', ur'Boothia ', ur'Borden ', ur'Breakfree ', ur'Brodeur ', ur'Bruce ', ur'Brunswick ', ur'Burin ', ur'Burrup ', ur'California ', ur'Cape ', ur'Cherbourg ', ur'Cobourg ', ur'Cornish ', ur'Coromandel ', ur'Crimean ', ur'Dampier ', ur'Delmarva ', ur'Dingle ', ur'Eyre ', ur'Fairpoint ', ur'Federacão ', ur'Festival ', ur'Fleurieu ', ur'Florida ', ur'Forgotten ', ur'Foxe ', ur'Freetown ', ur'Gansevoort ', ur'Gargano ', ur'Gasp[eé] ', ur'Gazelle ', ur'Goathorn ', ur'Gower ', ur'Greene ', ur'Greenwich ', ur'Group ', ur'Guajíra ', ur'Hellfire ', ur'Hispanic ', ur'Huon ', ur'Hæmo ', ur'Indian ', ur'Inishowen ', ur'Iveragh ', ur'Izu ', ur'Jason ', ur'Kaikoura ', ur'Kenai ', ur'Kent ', ur'Keweenaw ', ur'Kii ', ur'Kitsap ', ur'Kola ', ur'Korean ', ur'Kowloon ', ur'Kunisaki ', ur'Kurnell ', ur'Labrador ', ur'Laurens ', ur'Leizhou ', ur'Leschenault ', ur'Lichenes ', ur'Lleyn ', ur'Llŷn ', ur'Malay ', ur'Malayan ', ur'Mani ', ur'Marina ', ur'Marmaris ', ur'Mascareen ', ur'Masoala ', ur'Melville ', ur'Monterey ', ur'Mornington ', ur'Muria ', ur'Neck ', ur'Northern ', ur'Noto ', ur'Núñez ', ur'Ohio\)\|', ur'Olympic ', ur'Orote ', ur'Osa ', ur'Oshima ', ur'Otago ', ur'Pablo ', ur'Paraguan[aá] ', ur'Pinellas ', ur'Potter ', ur'Range ', ur'Reyes ', ur'Rockaway ', ur'Royal ', ur'Saanich ', ur'Samana ', ur'Scandinavian ', ur'Scotia ', ur'Seward ', ur'Sharqi ', ur'Siamese ', ur'Sibley ', ur'Simpson ', ur'Sinai ', ur'Sinaitic ', ur'Skagi ', ur'South ', ur'Southeast ', ur'Stricken', ur'Tabarin ', ur'Tail ', ur'Tasman ', ur'Tautuku ', ur'Thatcher ', ur'The ', ur'Tiburon ', ur'Tilliria ', ur'Trinity ', ur'Tróia ', ur'Ungava ', ur'Upper ', ur'Uvaria ', ur'Vald[eé]s ', ur'Verdes ', ur'Virginia ', ur'Warm ', ur'West ', ur'Western ', ur'Wild ', ur'Willaumez ', ur'Yampi ', ur'York ', ur'Yorke ', ur'Yucat[aá]n ', ur'[Aa]rabian ', ur'[Ii]berian ', ur'[Mm]unicipio de ', ur'[Ss]panish ', ur'[Uu]ltimate ', ur'and ', ur'entire ', ur'prairie ', ur'the ', ur'whole ', ], xpos=[ur' (?:of|Fine|Rugby|Business|Tower|Players|Borough|Town|Logging|Antarctica|Cafe|Pulse|Hispano-Lusitana|Corridor|Banjo|Skating|Soccer|Airways|Films|State|Medical|Hotel|no Shura|Library|Pharmaceuticals|Racquet|Catholic|Talent|Foundation|Boys|Power|College|\((?:Ohio|Long)|Township|Frog|de Yucatan en el Archivo General)\b', ur'\'\'"', ]) + #313
lema(ur'[s]_á_ndwich(?:es|)_a', xpre=[ur'Années ', ur'Breakfast ', ur'Club ', ur'Cream ', ur'Crisp ', ur'Deli ', ur'Earl de ', ur'Rail ', ur'Reuben ', ur'Scam ', ur'[Cc]heese ', ur'[Tt]ea ', ur'barbecue ', ur'bean ', ur'beef ', ur'dip ', ur'film ', ur'jelly ', ur'mein ', ur'nice ', ur'tenderloin ', ur'weck ', ]) + #308
lema(ur'[Bb]ant_ú__u', xpre=[ur'Jah ', ur'Moses ', ], xpos=[ur' (?:FC|Welfare|United|bakua|Land|Languages|Holomisa|and)\b', ]) + #254
lema(ur'[Mm]onograf_í_as?_i', xpre=[ur'Uma voz de muda espera: ', ur'prima ', ], xpos=[ur' (?:d[ai]|sui|Ladis|miasteczka|insulei|del (?:bombice|Genere?)|de especialização)\b', ur'(?:\.com|\. Ed Fundació|, dissertacoes)', ]) + #254
lema(ur'[Tt]alism_á_n_a', xpre=[ur'The ', ur'película\)\|', ], xpos=[ur' (?:recibió|Seal|Energy|Cage|\(película)', ]) + #219
lema(ur'[Rr]ab_í__i', xpre=[ur'Abi o ', ur'Isaac ', ], xpos=[ur' (?:I|Venkatesan|Akiva)\b', ur'(?:[‘\'](?:I|II|[- ]?[au]l-[Aa]ww?al|~en))', ]) + #204
lema(ur'[Tt]ab_ú__u', xpre=[ur'\be ', ur'Ete ', ur'Jonathan ', ur'und ', ], xpos=[ur' (?:chilla|search|Recordings)', ur'\]\]iza', ]) + #158
lema(ur'[Nn]azar_í__i', xpre=[ur'Amin ', ur'Esmail ', ur'Henrietta ', ]) + #103
lema(ur'[Nn]eg_ó__o', xpre=[ur'Abed ', ur'Loïc ', ur'Nogo\|', ur'burek ', ], xpos=[ur' (?:u|drugdje|da|ja|lani|véio|četri|je|moralna|fogo)\b', ur'” Haedo', ]) + #67
lema(ur'[Cc]_ó_ndor_o', xpre=[ur'\b(?:il|[Oo]f) ', ur'200\]\] \'\'', ur'AS-C03 ', ur'Airlines\|', ur'Black ', ur'Contrary ', ur'Curtiss ', ur'Dittmar ', ur'Flugdienst\|', ur'Giant ', ur'Hurakan ', ur'Il ', ur'JLT ', ur'Lana ', ur'Operação ', ur'Peace ', ur'Pristimantis ', ur'Pulo ', ur'Schleicher ', ur'Screaming ', ur'Twin ', ur'Wright ', ur'[Tt]he ', ur'chárter ', ur'con ', ur'der Legion', ur'journal\)\|', ur'mástiles "', ur'the ', ur'ópera\)\|', ], xpos=[ur' (?:10|of|du|Club|Films|Ferries|fue|ordenó|Hamburg|desarrollaron|Attack|Syndikat|Saito|Rapide|Golden|Flugdienst|Airlines|\((?:journal|ópera)|Golden|Crux|Games)\b', ur'(?:\'|" –|\. vol|\'s|1|, (?:S\.|Inc))', ]) + #46
lema(ur'[Aa]utobiograf_í_as?_i', xpre=[ur'\be ', ur'Pietro\. ', ur'[Ll][’\']', ur'[Uu]ma ', ur'[Uu]n[’\']', ur'anarchico\. ', ur'come ', ur'nossa ', ], xpos=[ur' (?:di|in|d\'un|della|con illustrazioni|con l|Precoce|de Déu|del blu di|disfarçada|do |homossexual|não|lui|i ficció)\b', ur'(?:\. Kindler|: a luta)', ]) + #40
lema(ur'[Mm]_é_dicas_e', xpre=[ur'Citrus ', ur'Ciências ', ur'Facolta ', ur'Responsabilidade ', ur'[Ss]ciencias ', ur'cryptogamicarum ', ur'di Antropologia ', ], xpos=[ur' ex', ur', Chirurgicas', ]) + #37
lema(ur'_ó_ptica_o', xpre=[ur'L\. ', ur'Lithops ', ur'Typhedanus ', ur'camera ', ur'illusione ', ], xpos=[ur' onde', ]) + #16
lema(ur'_acadé_mica_(?:Acad[eé]|acade)', pre=ur'[Ff]ormaci[oó]n ') + #1
lema(ur'[Cc]iencia _f_icci[oó]n_F') + #1
lema(ur'_e_spañol_E', pre=ur'\b(?:e[ln]|del?|idioma|y) ', xpre=[ur'llega ', ur'[Ee]scritor ', ur'destacando ', ur'TLN ', ur'ATSDR ', ur'Alemán ', ur'inferiores ', ur'jugador ', ur'Certificado ', ur'curso ', ur'clases ', ur'materia ', ur'Verbal en el ', ur'Estilística del ', ur'Torre ', ur'Diploma ', ur'Diplomas ', ur'Departamento ', ur'estudios ', ur'Sección ', ur'Discovery ', ur'Proveniente ', ur'Escritores ', ur'Málaga Cine ', ur'[Pp]rofesor ', ur'[Pp]rofesores ', ur'Chicago ', ur'Club ', ur'Graña, ', ur'graduarse ', ur'Pop ', ur'CNN ', ur'People '], xpos=[ur' (?:y Athletic|como|de Madrid|sobre Schopenhauer|lo contrató|Urgente|Actual|de (?:Afuera|Talca))', ur', Matemáticas']) + #1

#lema(ur'[Cc]ontinu_ó_ (?:en|con)_o', xpre=[ur'modo ', ur'cambio ', ur'movimiento ', ur'\bes ', ur'medio ']) + #1
# lema(ur'_t_elevisión_T', pre=ur'(?:[Cc]adena|[Ss]erie) de ', xpre=[ur'Yaracuyana ', ur'Tovareña ', ur'Venezolana ', ur'Nacional ']) + #7506
# lema(ur'_v_ideo_V', pre=ur'(?:[Mm]ejor|y) ', xpos=[ur' (?:Gaudio|Pop|Image|Voladero)']) + #587
# lema(ur'_c_anciones_C', pre=ur'de ', xpre=[ur'creador ', ur'Colección ', ur'Libro '], xpos=[ur' (?:Secretas|Regionales|Nativas|de Navidad)']) + #2714
# lema(ur'_f_ase_F', pre=ur'(?:[Pp]rimera|[Ss]egunda|[Tt]ercera|[Uu]ltima|[Cc]uarta|[Qq]uinta|[Ss]exta|[Ss]éptima) ', xpre=[ur'Equipos ']) + #3241
# lema(ur'_f_inal_F', pre=ur'(?:[Cc]uadro|de|[Ff]ase|[Rr]onda) ', xpos=[ur' (?:Audition|\'*Fantasy|Cut|Resolution)']) + #16612
# lema(ur'_g_rupos_G', pre=ur'de ', xpos=[ur' Étnicos']) + #3894
# lema(ur'_o_riginal_O', pre=ur'[Ss]onora ', xpos=[ur' do\b']) + #1
# lema(ur'_s_erie_S', pre=ur'(?:de|una|[Mm]ejor) ', xpre=[ur'[0-9] ', ur'Brasileño '], xpos=[ur' Mundial']) + #3634
  []][0]

####
nuevos = [
[(ur'(?P<f>\[|\|)(?P<a>Campeonato de Wimbledon|Torneo de Roland Garros) (?P<b>[12][0-9][0-9][0-9]) Individuales Masculinos(?P<e>\}|\]|\|)', ur'\g<f>Anexo:\g<a> \g<b> (individual masculino)\g<e>')] + #1
[(ur'(?P<f>\[|\|)(?P<a>Campeonato de Wimbledon|Torneo de Roland Garros) (?P<b>[12][0-9][0-9][0-9]) Individuales Femeninos(?P<e>\}|\]|\|)', ur'\g<f>Anexo:\g<a> \g<b> (individual femenino)\g<e>')] + #1
[(ur'(?P<f>\[|\|)(?P<a>Campeonato de Wimbledon|Torneo de Roland Garros) (?P<b>[12][0-9][0-9][0-9]) Dobles Masculinos(?P<e>\}|\]|\|)', ur'\g<f>Anexo:\g<a> \g<b> (dobles masculino)\g<e>')] + #1
[(ur'(?P<f>\[|\|)(?P<a>Campeonato de Wimbledon|Torneo de Roland Garros) (?P<b>[12][0-9][0-9][0-9]) Dobles Femeninos(?P<e>\}|\]|\|)', ur'\g<f>Anexo:\g<a> \g<b> (dobles femenino)\g<e>')] + #1
[(ur'\((?P<a>[12][0-9][0-9][0-9]) film\)', ur'(película de \g<a>)')] + #1
[(ur'\((?P<a>[12][0-9][0-9][0-9]) [Bb]engal[ií] film\)', ur'(película bengalí de \g<a>)')] + #1
[(ur'\([Bb]engal[ií] film\)', ur'(película bengalí)')] + #1
[(ur'\([Tt][Vv] series\)', ur'(serie de televisión)')] + #1
[(ur'\([Bb]oxer\)', ur'(boxeador)')] + #1
[(ur'\([Ww]restler\)', ur'(luchador)')] + #1
[(ur'\((?:Banda [Ss]onora|banda Sonora)\)', ur'(banda sonora)')] + #1
[(ur'\[\[(?:Parque [Nn]acional [Mm]arítimo-[Tt]errestre del Archipi[eé]lago de Cabrera|Parque nacional del Archipiélago de Cabrera|Parque [Nn]acional del Archipi[eé]lago de Cabrera)(?P<a>\]|\|)', ur'[[Parque nacional marítimo-terrestre del Archipiélago de Cabrera\g<a>')] + #1
[(ur'\b(?P<a>[Tt]ermin)o(?P<b> [0-9]+)', ur'\g<a>ó\g<b>')] +

lema(ur'[Bb]engal_í__i', xpre=[ur'\bin ', ur'the ', ur'and ', ur'Uca ', ur'nuit ', ur'Jolly ', ur'Indigenous ', ur'Renault\]\] ', ur'Renault '], xpos=[ur' (?:in|and|Night|Album|English|[Cc]inema|[Rr]ock|[Ff]olk|[Bb]eat|[Ff]ilms?|[Mm]ovies?|title|[Ss]ongs?|webzine|Lyrics|Liberation|[Ll]anguage|Bantam|Bauls|Alphabet|Songs|[Aa]mbassador|Tiger)']) + #132
lema(ur'[Hh]i_c_ieron_z', xpos=[ur' los capitanes']) + #30
lema(ur'[Hh]i_z_o_s', xpre=[ur'quispe tito ', ur'\| '], xpos=[ur' Hyakuga', ur'\)']) + #13
lema(ur'[Ll]_í_mites?_i', pre=ur'(?:[Ss]in(?: m[aá]s|)|[Hh]ay|[Cc]on|[Cc]omo|[Dd]el?|[Ee]ntre|[Tt]odo|[Ss]us?|[Ee]l|[Uu]n|[Uu]nos|al?|y|[Ee]st?e|[Ee]stos|[Ff]ija|[Dd]etermina|tiempo) ', xpre=[ur'questão ', ur'Froid ', ur'Mondi ', ur'signore ', ], xpos=[ur' Produções', ur', d\'échang']) + #201
lema(ur'[Ll]_í_mites_i', pre=ur'[Ll]os ') + #60
lema(ur'[Mm]_é_ritos?_e', xpre=[ur'\b(?:[Yy]a|di|et|do|il|in) ', ur'Marquesado de ', ur'Marqu[eé]s de ', ur'Libens ', ur'Nilo ', ur'Ufficiale al ', ur'San Fernando del ', ur'libens ', ur'Bene ', ur'aedem ', ur'quas ', ur'Ordine al ', ], xpos=[ur' (?:dei|della|hec|dell|per|ad|di|et|[Mm][ei]litensi|Sportivo|Culturale|dedicata|tali|beneficia quae|legionemque|rabirrubio|del lavoro|civile)\b']) + #216
lema(ur'[Pp]aran_á__a', xpre=[ur'[Hf]\. ', ur'Le Rio ', ur'the ', ur'1779\) ', ur'Burón y ', ur'[Vv]iaducto de ', ur'Ji ', ur'Upper ', ur'Lower ', ur'Aegla ', ur'Acontia ', ur'Acanthogonatus ', ur'Alagoasa ', ur'Acanthogonatus ', ur'Losdolobus ', ur'Losdolobus ', ur'Hernandarias ', ur'Hemigrammus ', ur'Lena\)\|', ur'Baxada del ', ur'Hololena ', ur'Lamina ', ur'Misagria ', ur'Tarache ', ur'Cryptachaea '], xpos=[ur' (?:[Rr]iver|Ports|Post|Kalender|\(Lena)', ur'´i']) + #511
lema(ur'[Pp]oes_í_as?_i', xpre=[ur'\b[AaàePi]\. ', ur'\b[AaàePi] ', ur'\b(?:[Dd][ai]|na) ', ur'C\'è ', ur'\be la ', ur'946\) ', ur'Roma, ', ur'Iniciació a la ', ur'Prémio de ', ur'Foscari ', ur'Versions de ', ur'Igualda de ', ur'Falar de ', ur'Bown’s ', ur'Prémio de ', ur'Premi de ', ur'Noptile de ', ur'Jaume de ', ur'Rainha Sofia de ', ur'originale volgare ', ur'jovem ', ur'Prémio Internacional de ', ur'Premi Crítica Serra d\'Or de ', ur'do Bem-Te-Vi: ', ur'Premi Martí Dot de ', ur'Quaderns de ', ur'As 7 ', ur'Bon dia, ', ur'món de ', ur'Concert de ', ur'[Nn]ova ', ur'collecção de ', ur'cicle de ', ur'[Dd]ella ', ur'teva ', ur'Encontro maior: ', ur'Ciència, fe, ', ur'd[\'’]abril de ', ur'València de ', ur'aplech de ', ur'della epica ', ur'\be de ', ur'amb la ', ur'Introducció a la ', ur'Outras ', ur'Sulla ', ur'Jornal de ', ur'Natura, ', ur'Elogi de la ', ur'Quart en ', ur'nella ', ur'vera ', ur'Premis Octubre de ', ur'Pedaliodes ', ur'Pronophila ', ur'Premi de ', ur'celobert. Antologia de ', ur'[Mm]elhores ', ur'[Rr]evista \'\'', ur'Jabuti de ', ur'perfetta ', ur'Futura: ', ur'MSC ', ur'na ', ur'mig editorial de ', ur'minha alma: '], xpos=[ur' (?:[di]|in|di|per|do|des|nell|nel|dins|dels|\'90|[Aa]cadèmica|[Pp]erifèrica|come|napoletana|al Carrer|dialettale|sarda e|satirica in|sempre|scritta|experimental en terres|[Nn]ova|en valencià|insular del segle|catalana del segle|lirica ed|numa|jove|sonora|kaierak|Mienia|No Condado|Escolhidas|contemporània|Completa \(1940|espanhola|eletronica|popolare|originale|Etna-Taormina|ed|comprometida com|spagnola|galega|banatua|bromélias|en acció|egípcia antiga|neoclàssica|[Ss]enza|noranta|xinesa|a quel|argentina e brasileira|e (?:storia|[Pp]rosa|sentimento|Composição|Crônica|retorica)|de (?:les|la Mediterrània|Marian Aguiló)|Espanhola)\b', ur'(?:: a paixão|\'+ y \'+Teatre|\.(?:cl|cat)|, (?:realisme, història|estética e política)|\'\', Antonio|[:,] \[\[(?:Paolo|contos|Enrico|Alessandro|Maria Luisa Spazani|Antonella))']) + #523
lema(ur'_alemá_n_(?:Alem[aá]|alema)', pre=ur'\b(?:idioma) ') + #444
lema(ur'_alemá_n_(?:Alem[aá]|alema)', pre=ur'\b(?:e[nl]|del?|y) ', xpre=[ur'por ', ur'Baile ', ur'Mina ', ur'Pozo ', ur'llamado ', ur'reales ', ur'entrega ', ur'hombres ', ur'presidencia ', ur'especialización ', ur'huyeran, ', ur'revolución ', ur'gobierno ', ur'[Mm]aestra ', ur'viuda ', ur'privado ', ur'catedrático ', ur'taller ', ur'Instituto ', ur'Magnani ', ur'Velasco ', ur'clases en Griego ', ur'estudió Inglés, Francés ', ur'Natural ', ur'Derecho\]\] ', ur'Internacional ', ur'Colegio Francés ', ur'Viganego ', ur'Sánchez ', ur'Sadoc ', ur'Farrill ', ur'Filosofía ', ur'Latín ', ur'Juan ', ur'Profesora ', ur'Profesor ', ur'Profesores ', ur'Sanscrito ', ur'alemán y ', ur'Espuny y ', ur'Aberardo ', ur'Cursos ', ur'Básico ', ur'Avanzado ', ur'Conrado ', ur'Diego ', ur'Hermann ', ur'Silvia ', ur'Velasco\]\] ', ur'Nicol[aá]s ', ur'Garnier ', ur'Valdez ', ur'Monterrey ', ur'Zorida ', ur'Programa ', ur'Diplomado ', ur'Didáctica ', ur'Columna ', ur'Huerta ', ur'Valdés ', ur'Schultz, ', ur'Henry ', ur'Herm[aá]n ', ur'Química ', ur'Español, ', ur'Departamento ', ur'Pedagogías ', ur'Estudios ', ur'Sanabria ', ur'ojos ', ur'Ortega ', ur'Sayula '], xpos=[ur' Transatlántico', ur'(?:"|\'\')']) + #444
lema(ur'_francé_s_(?:Franc[eé]|france)', pre=ur'\b(?:e[ln]|del?|idioma) ', xpre=[ur'José ', ur'Guerra ', ur'maestra ', ur'Docencia ', ur'Diplomado ']) + #1
lema(ur'_japoné_s_(?:Japon[eé]|japone)', pre=ur'\b(?:idioma|e[nl]|del?|y) ', xpre=[ur'Diplomado ']) + #1
lema(ur'_i_taliano_I', pre=ur'\b(?:idioma|e[nl]|del?|e) ', xpre=[ur'clases ', ur'Club ', ur'Francés e ', ur'Alemán y ']) + #1
lema(ur'_c_oreano_C', pre=ur'\b(?:idioma|e[nl]|del?|e) ') + #1
lema(ur'_inglé_s_(?:Ingl[eé]|ingle)', pre=ur'\b(?:e[ln]|del?|e) ', xpre=[ur'Diccionario ', ur'Gestión ', ur'Preescolar ', ur'en Francés ', ur'Nivel ', ur'Docencia ', ur'[Dd]epartamento ', ur'B\.A\. ', ur'Juan ', ur'Pedagogía ', ur'bilingüe ', ur'[Cc]lase ', ur'[Cc]lases ', ur'[Cc]ursos ', ur'[Cc]arreras ', ur'aparte ', ur'titula ', ur'[Pp]rofesores ', ur'[Pp]rofesor ', ur'Diplomado ', ur'Programa ', ur'[Ee]nseñanza ', ur'graduó ', ur'especializada ', ur'\bla ', ur'Mesa del ', ur'Piedra ', ur'Castellano ', ur'Castillo ', ur'orales ', ur'Maestra ', ur'[Pp]rogramas ', ur'Teacher ', ur'interrelacionados ', ur'Punta ', ur'Playa ', ur'Pico ', ur'Instituto ', ur'Física Nuclear ', ur'grado ', ur'profesor\]\]a ', ur'[Pp]rofesor ', ur'[Pp]rofesora ', ur'Profesorado ', ur'Maestría ', ur'Japón\]\] ', ur'Bogotá\)\|', ur'Playa ', ], xpos=[ur' (?:\(idiomas)', ur'\'\'']) + lema(ur'[Ii]ngl_é_s(?:\]\]|[,.]| \(pueblo)_e', xpre=[ur'Zach ', ur'Chris ', ur'Clube ', ur'cintura e ', ur'David ', ur'Nelson ', ur'J\. ', ur'Joe ', ur'Joe Ingles\|', ur'ojos e ', ur'las ', ur'sus ', ], xpos=[ur'[a-z]+', ur' (?:cuello|axilas|\(Bogotá)']) + #583
lema(ur'_c_heco_C', pre=ur'\bde ', xpos=[ur' (?:a|Pérez)\b']) + #1
lema(ur'_ó_rbitas?_o', pre=ur'(?:[Ll]as?|[Ss]us?|[Uu]nas?|[Ee]n) ', xpre=[ur'que ']) + #1
lema(ur'_é_tnic[ao]_e', xpre=[ur'rapporto ', ur'composizione ', ur'Dalmazia ', ], xpos=[ur' e resistenza', ur'\'', ]) + #1
lema(ur'_ejé_rcito_Ej[eé]', pre=ur'(?:[Aa]l|[Ee]l|[Dd]el|[Uu]n|[Ss]u) (?:[Pp]rimer|[Ss]egundo|[Tt]ercer|[Cc]uarto|[Qq]uinto|[Ss]exto|[Ss]éptimo|[Oo]ctavo|[Nn]oveno|[Dd]écimo|[0-9]+º) ', xpos=[ur' (?:Panzer|Francés)']) + #1
lema(ur'[l]_í_der_i', pre=ur'(?:[Ee]l|[Ll]a|[Uu]na?|[Ee]s|[Ff]u[ée]|[Ss]u) ', xpre=[ur'd´']) + #1
lema(ur'[Tt]ermin_ó_ [a-zñ]+[aeáé]ndo(?:(?:[mts]e|nos)(?:l[aeo]s?|)|l[aeo]s?|)_o', xpre=[ur'primer ']) + #1
lema(ur'[Rr]_í_gid(?:as|os?|amente)_i', xpos=[ur' e [Cc]erimonale']) + #1
lema(ur'[Qq]u_í_mic[ao]_i', xpre=[ur'Uniao ', ur'Estudo '], xpos=[ur'cNova', ur'\.uady']) + #1
lema(ur'[Pp]sicol_ó_gic[ao]_o', xpre=[ur'e ', ur'primo ', ], xpos=[ur' ed', ]) + #1
lema(ur'[Pp]ol_í_tico_i', xpre=[ur'\be ', ur'\b[Ii]l ', ur'de \'\'', ur'ordinamento ', ur'periódico\)\|', ur'regime ', ur'come paradigma ', ur'categorie del ', ur'pensamento ', ur'regolarità del ciclo ', ur'Aspetti del realismo ', ur'Niente Asilo ', ur'The ', ur'canterò ', ur'il ', ur'significato ', ur'scritto ', ur'Niente Asilo ', ur'The ', ur'il ', ur'scritto ', ur'uomo ', ], xpos=[ur' (?:Centrale|dalla|delle|dei|di|\(periódico)\b', ur'\.(?:com| Diplomazia)']) + #1
lema(ur'[Mm]_é_todo_e', xpre=[ur'\be ', ur'\b(?:di|[Ii]l) ', ur'Cirilo y ', ur'struktura ', ur'Introduzione al ', ur'genesi del ', ur'[Ss]ul ', ], xpos=[ur' (?:mui|facile|naturale|galileiano|ipocondriaco|konparatzailea|[Cc]lassico|exposita|refrigerandi|Telecomunicacoes|storico|anal[ií]tico, filosofico e fisiologico|e tavole|per|di )', ur', Fonti', ]) + #109
lema(ur'[Ll]ogr_ó_ +(?:el|la|los|las|un|una|unos|unas|dos|tres|cuatro|cinco)_o', xpre=[ur'(?:[Uu]n|[Ss]u|[Ll][eo]|[Ss]e) ', ur'mayor ', ur'[Ee]ste ', ur'[Ss]e (?:me|te|l[aeo]) ', ur'[Ss]e l[aeo]s ']) + #1
lema(ur'[Ii]nt_é_rprete_e', pre=ur'(?:[Ll]a|[Ee]l|[Uu]na?|como) ', xpre=[ur'no '], xpos=[ur' (?:como|siente|\'\'a capella|el|[ay] )']) + #1
lema(ur'[Ff]_á_ciles_a', xpre=[ur'T\. ', ur'Tugulusaurus ', ur'[Pp]ièces ', ], xpos=[ur' (?:à|pour|et)', ]) + #1
lema(ur'[Dd]ic_i_embre_', xpre=[ur'Dodici ', ur'\bdi ']) + #1
lema(ur'[Dd]iab_ó_lico_o', xpre=[ur'[Ii]l ', ur'Scherzo ', ur'Megachile ']) + lema(ur'[Dd]iab_ó_lica_o', xpre=[ur'[BILRT]\. ', ur'Synaphea ', ur'Deamia ', ur'probatio ', ur'Notosacantha ', ur'Isachne ', ur'Trappola ', ur'Rhagodista ', ur'Notosacantha ', ur'Ligariella ', ur'Ficus ', ur'Barbucca ', ur'Charidotis ', ur'Sasa ', ur'Megachile ', ur'Idolum ', ur'Idolomantis ', ur'Deinopis ', ur'Synagoga ', ur'Tipula ', ur'Laminaria ', ur'Vanilla ', ur'Trappola ', ur'Trilacuna ', ]) + #51
lema(ur'[Dd]_ú_o_u', pre=ur'(?:[Aa]|[AaEe]l|[Dd]el?|[Ss]u|[EeUu]n|exitoso|como|dicho|es|este|famoso|formando|formato|formó|hacer?|haciendo|hermoso|hizo|hop|mejor|nuevo|otro|popular|por|primer|proyecto|siniestro|tiene|[uú]nico|versión|y) ', xpre=[ur'\bby ', ur'Benedictus ', ur'ayuda ', ur'After '], xpos=[ur' (?:[Oo]r|Music|Damsel|I Lombardi|Lon|Maxwell|de Gatti|Inattendu)\b']) + #1
lema(ur'[Dd]_í_a_i', pre=ur'\b(?:[Dd][ií]a a|[Cc]ada|[Dd]el?|en|[AaEe]l|[UÚuú]ltimo|[Mm]ismo|[Aa]lg[uú]n|[Pp]or|[Ee]se|[Nn]uevo) ', xpre=[ur'nit ', ur'Nosso de ', ur'Contessa ', ur'Festa ', ur'Manual ', ur'Ous ', ur'Plaza ', ur'Sermão ', ur'dies de ', ur'Tol dia todos ', ur'cami de la consciencia en el ', ur'començar el ', ur'd’un ', ur'nombre ', ur'nombres ', ur'nou, ', ur'pa de ', ur'per commemorar ', ur'sexonosso de ', ur'terra de ', ur'tot ', ], xpos=[ur' (?:6 d’abril|Mais|Jack|d[io] |de les|e Síria|Vira|i de |revolt|que en Cecili|qualsevol|més|de (?:solidão|Pasqua|l\'ós|l[\'’]eclipsi)|d\'enganyar|d\'Andalusia|melhor|Kossoi|dels|del senyor|en ke|d[\'’]estiu)', ur'(?:\'\' de la emisora catalana|, calendari)', ]) + #1
lema(ur'[Dd]_í_a_i', pre=ur'[Uu]n ', xpre=[ur'menys ', ur'Deixar-te ', ur'd’', ur'i ', ], xpos=[ur' (?:de la vida d\'un|no sé com|al mercat|Qualsevol|que els|d’estiu)', ur'\. Mirall']) + #1
lema(ur'[d]_í_as_i', xpre=[ur'primeiros ', ur'Tem ', ur'O respirar dos ', ur'Certos ', ur'\b[Oo]s ', ur'Há ', ur'nossos '], xpos=[ur' (?:a dia, calendari|de hoje|que en Gluck va arribar)', ur'\.com']) + #1200
lema(ur'[Dd]_é_bil_e', xpre=[ur'Guardian ', ur'as '], xpos=[ur' Estar', ]) + #41
lema(ur'[Cc]apit_á_n_a', pre=ur'(?:[Ee]l|[Uu]n|[Dd]el?|[Cc]omo) ', xpre=[ur'OS X ', ur'OS X\]\] "', ur'10.11 \(', ur'OS X\]\] ', ur'\]\] \(', ur'The ', ], xpos=[ur' (?:Theatre|Theater|generale|10\.11)', ]) + #1
lema(ur'[Pp]erpet_ú_(?:an|e[ns]?)_u', xpre=[ur'Rote ']) + #1
lema(ur'[Rr]esult_ó__o', xpre=[ur'(?:[UuEe]n|[Ee]l) ']) + #29
lema(ur'[Dd]_é_cim(?:as?|o)_e', xpre=[ur'\ba ', ur'\b(?:di|[Ii]l) ', ur'Azzano ', ur'Leone ', ur'Maioris ', ur'Molly ', ur'Leon ', ur'legio ', ur'quarta ', ur'Nona\'\', y ', ur'parakosvensis ', ur'Pio ', ur'Toccata ', ur'[Dd][ae]lla ', ur'[Ee]ditio ', ur'alla ', ur'by ', ur'hermana ', ur'julii ', ur'nella ', ur'secolo ', ur'virgula\'\', \'\'', ur'tertia ', ], xpos=[ur' (?:ac|ex|et|in|anno|kalendas|bolgia|puntata|stagione|dissertatio|le prime|Incontro|Proto|Tutori|Schmidt|Moore|gemina|Junio|Magno|Giunio|nel|nono|Plotio|Albino|Ebucio|Tertia|flottiglia|DLC|MAS|vittima|novarum|legio|legione|legionibus|calendas|Valerio|Veturio|\[pars|Mas|Flottiglia|Meridio|dixere|revisione|Dall\'Arsina|Bettini)\b', ur', ove']) + #235
lema(ur'[Ll]_é_mur_e', xpre=[ur'Ruffed ', ur'término \'\'', ur'[Gg]énero \'\'', ur'[Gg]énero \'\'\[\[', ur'[Gg]énero\]\] \'\'', ur'The ', ur'latín \'\'', ur'catta\|', ur'Pristimantis '], xpos=[ur' (?:See|Do|News|Ultra|Center|Conservation|Street|Species|catta|Input)', ur'\] BBC']) + #337
lema(ur'[Vv]_é_rtices?_e', xpre=[ur'\b(?:[Ii]n|Il|of) ', ur'São Paulo: ', ur'Its '], xpos=[ur' (?:del Pci|of|usque)']) + #148
lema(ur'[Aa]rt_í_stic[ao]s_i', xpre=[ur'Produçoes ', ur'storico ']) + lema(ur'[Aa]rt_í_stic[ao]_i', xpre=[ur'\be ', ur'non solo ', ur'Umane, Liceo ', ur'Guida ', ur'letteratura ', ur'creatività ', ur'storico ', ur'storia ', ur'[Ff]onderia ', ur'[Ff]ormazione ', ur'[Aa]ssociazione ', ur'[Ee]sposizione ',ur'[Pp]iù ', ur'[Cc]ircolo ', ur'[Ss]tanilimiento ', ur'sull\''], xpos=[ur' (?:statale|Editrice|e (?:ambientale|demoantropologico)|editrice|a Mantova|architettonica|ticinese|di|futuribile|cremonese)\b']) + #1
lema(ur'[Cc]_ó_mplices?_o', xpre=[ur'[LlSs]es ', ur'[Ll]e ', ur'Dii ', ur'Soleil '], xpos=[ur' (?:muta|Ou)', ur'\'']) + #1
lema(ur'[mm]_á_quinas?_a', pre=ur'(?:[Ll]as?|[Uu]nas?|[Cc]ada|[Ss]us?|[Ee]stas?|[Aa]) ', xpos=[ur' da ']) + #1
lema(ur'Copiap_ó__o', xpre=[ur'Volcano ', ]) + #1
lema(ur'Llovi_ó__o', xpre=[ur'de ', ], xpos=[ur' (?:\(Lloviu|•)', ur'\]', ]) + #13
lema(ur'[Aa]_demá_s_ dem[aá]', xpos=[ur' (?:adolescentes|autoridades|aspectos|bandas|cosas|esclavos|estudiantes|espíritus|gente|generales|jugadores|municipios|organizaciones|partes|plataformas|personas|personalidades|países)']) + #1
lema(ur'[Aa]boli_ó__o', xpre=[ur'Rosalía ', ]) + #1
lema(ur'[Aa]cad_é_micos_e', xpre=[ur'Artes ', ur'Congressos ']) + #1
lema(ur'[Aa]cord_ó__o', xpre=[ur' [nd]o ', ur' el ', ur'Novo ', ur'm\'', ], xpos=[ur' (?:e vejo|[Oo]rtográfico|de (?:Paz|Argel)|com)', ]) + #4
lema(ur'[Aa]dopt_ó__o', xpos=[ur' la postura']) + #18
lema(ur'[Aa]eron_á_utica_a', xpre=[ur'Sociedade ', ur'maggiore ', ur'militare ', ur'Nazionale ', ur'Autoritatea ', ur'Brasileira de ', ur'Gira Globo ', ur'R\. ', ur'dell[’\']', ur'Alenia ', ur'Regia '], xpos=[ur' (?:SMA|[Mm]ilitare|Nazionale|Torino|Umbra|Macchi|Nakajima|Cobelligerante|Regală|Romana|Română|Aichi|Ansaldo|de São Paulo|Sicula|per|Imperialis)', ur'\. Milano']) + #1
lema(ur'[Aa]lcanz_ó__o', xpre=[ur'[Tt]e ', ], xpos=[ur' a verte', ]) + #25
lema(ur'[Aa]li_ó__o', xpre=[ur' in ', ur'Jorge ', ur'Nur ', ur'cum ', ur'otras ', ], xpos=[ur' (?:Albino|\(Albino|Élide|y ens|[Mm]odo|cibo|ergo|[Ii]tinere|nomine|fue|se|i)\b', ur'\]', ]) + #3
lema(ur'[Aa]ntig_ü_edad(?:es|)_u', xpre=[ur'Ibèrica de la '], xpos=[ur' deste', ur', calidad, i\b']) + #1
lema(ur'[Aa]post_ó__o', xpre=[ur'Evarcha ', ], xpos=[ur' Gazella', ]) + #1
lema(ur'[Aa]r_á_cnid[oa]s?_a', xpre=[ur'ooteca ']) + #1
lema(ur'[Aa]scendi_ó__o', xpre=[ur'[Ss]iendo ', ]) + #2
lema(ur'[Aa]stron_á_uticas?_a', xpre=[ur'in "', ur'Encyclopedia ']) + #1
lema(ur'[Aa]tl_é_tic[ao]_e', xpre=[ur'Clube ', ur'Viva l\'', ur'Associazione '], xpos=[ur'\]\]', ur' (?:Clube|\([Mm]arca|Tucumán|Leggera|Portici|Informáticos|Puteolana|Paranaense)']) + #1
lema(ur'[Aa]vent_ó__o', xpos=[ur' Aretino', ]) + #1
lema(ur'[Bb]_ó_ric[ao]s?_o', xpre=[ur'Zamora ', ur'Diego ', ur'Toichoa ', ur'Terencio ']) + #1
lema(ur'[Bb]ailar_í_n_i', xpos=[ur'\]\](?:es|a)']) + #1
lema(ur'[Bb]ati_ó__o', xpre=[ur'Angelo ', ur'Pizze a ', ], xpos=[ur' (?:Barnabás|di 1Bassieré)', ]) + #2
lema(ur'[Bb]ebi_ó__o', xpre=[ur'Cayo ', ur'Lucio ', ur'Marco ', ur'Mario ', ], xpos=[ur' (?:T[aá]nfilo|Macro)', ]) + #7
lema(ur'[Bb]iogr_á_fic[ao]s?_a', xpre=[ur' e ', ur'Scheda ', ur'[Ss]aggio ', ur'Archivio ', ur'percorso ', ur'studio ', ur'Storico ', ur'Schizzo ', ur'Dizionario[- ]'], xpos=[ur' (?:universale|degli|Treccani|e concettuale|Parmigiani|di|Universale)']) + #1
lema(ur'[Bb]iol_ó_gic[ao]_o', xpre=[ur'agricoltura ', ur'Lotta ', ur'testamento ', ur'Senckenbergiana ', ur'Seckenbergiana ', ur'Acta ', ur'Symposia ', ur'Carolinae - ', ur'Carolinae -- ', ur'[Oo]pera '], xpos=[ur', Geographica', ur' (?:Benrodis|[Ff]ennica|[Hh]ungarica|Paranaense|sui|della|nel|e integrata|vegetale|applicata|et )']) + #1
lema(ur'[Cc]_á_tedras?_a', xpre=[ur'Publicacions de la ', ur'[Ee]x ']) + #1
lema(ur'[Cc]_ú_spides?_u', xpre=[ur' a '], xpos=[ur' (?:tetigisse|Awards)']) + #1
lema(ur'[Cc]af_é__e', pre=ur'(?:[Ee]l|[Uu]n|[Cc]olor|[Dd]e) ', xpos=[ur' (?:romantic|dels)']) + #1
lema(ur'[Cc]af_é_s_e', xpre=[ur'Two '], xpos=[ur' (?:do|of|and)']) + #1
lema(ur'[Cc]l_í_nica_i', xpre=[ur'Schola ', ur'della ', ur'Esempio '], xpos=[ur' (?:di|delle?|e (?:Terapia|di|giuridica)|de l\'Aliança|di |Chimica|Serres|outcome|groazei|Medical|Chirurgica|Est[ée]tico)\b']) + #1
lema(ur'[Cc]ompa_ñí_as?_(?:n[ií]|ñi)', xpre=[ur' i ', ur'exercita la '], xpos=[ur' (?:do|Națională|de Iesu)']) + #1
lema(ur'[Cc]onoci_ó__o', xpre=[ur'[Ee]s ', ]) + #4
lema(ur'[Cc]onsigui_ó__o', xpos=[ur' dificultar i ', ]) + #4
lema(ur'[Cc]rey_ó__o', xpre=[ur'Ignacio ', ]) + #1
lema(ur'[Cc]ruz_ó__o', xpre=[ur'\*\* ', ur'\b(?:me|[Yy]o) ', ur'Mayas ']) + #1
lema(ur'[Dd]iat_ó_nic[ao]s?_o', xpre=[ur'Philaethria '], xpos=[ur' genere']) + #1
lema(ur'[Dd]id_á_ctic[ao]s?_a', xpre=[ur'Historica ', ur'Methodus '], xpos=[ur' Omnia']) + #1
lema(ur'[Dd]ividi_ó__o', xpre=[ur'[Ee]s ', ur'[Ee]st[aá] ', ur'[Ff]u[eé] ', ]) + #1
lema(ur'[Dd]oli_ó__o', xpre=[ur'Juan ', ur'un ', ], xpos=[ur'\]\]', ]) + #2
lema(ur'[Dd]ond_e__é', xpre=[ur'Villar ', ur'Rafael ', ur'Manuel ', ur'Salvador ', ur'Emilio ', ur'Pedro ', ur'Elda  ', ur'Fundación '], xpos=[ur' Matute', ur'[\]]']) + #1
lema(ur'[Dd]orm_í_a[ns]?_i', xpre=[ur'notte, Cassio ']) + #1
lema(ur'[Ee]_x_tranjer[ao]s?_s', xpre=[ur'Inglesa y ']) + #1
lema(ur'[Ee]jerci_ó__o', xpre=[ur'[Ee]l ', ]) + #1
lema(ur'[Ee]miti_ó__o', xpos=[ur' Mayo', ]) + #6
lema(ur'[Ee]nd_é_mic[ao]s?_e', xpos=[ur' di']) + #1
lema(ur'[Ee]nvi_ó__o', xpre=[ur'(?:[Ee]l|[Uu]n|[Dd]e) ', ur'[Cc]ada ', ], xpos=[ur' (?:cada)', ]) + #7
lema(ur'[Ee]rr_ó_ne[ao]s?_o', xpre=[ur'Cordulegaster ']) + #1
lema(ur'[Ee]sc_á_ndalos?_a', xpre=[ur'Pubblicista de ']) + #1
lema(ur'[Ee]sco_cé_s_(?:s[eé]|ce)', xpos=[ur'\]']) + #1
lema(ur'[Ee]scribi_ó__o', xpos=[ur' de sus andanças', ]) + #5
lema(ur'[Ee]strenar_á__a', pre=ur'(?:[Ss]e )', xpre=[ur'que esta ', ur'que ']) + #1
lema(ur'[Ee]ucar_í_stic[ao]s?_i', xpos=[ur' nazionale']) + #1
lema(ur'[Ee]ucarist_í_as?_i', xpre=[ur' a ', ur'[Ll][\'’]']) + #1
lema(ur'[f]antas_í_as?_i', pre=ur'(?:[Ll]as?|[Uu]nas?|[Dd]e|[Cc]ada|[Ss]u) ', xpre=[ur'regne de la ', ur'Enciclopèdia ', ur'Quando ', ur'[Qq]uasi ', ur'Scherzi '], xpos=[ur' (?:Barrino|inacabable d)\b', ur': (?:enquesta|ballava)']) + #1
lema(ur'[Ff]ilm_ó__o', xpos=[ur' (?:[Ii]magen|López)']) + #3
lema(ur'[Ff]loreci_ó__o', xpos=[ur' Varela', ]) + #1
lema(ur'[Ff]onolog_í_as?_i', xpre=[ur'\be ', ur'di ', ur'Hizkuntzen ', ur'Euskal '], xpos=[ur' (?:della|e Gramática|Hitzez|e prosódia)']) + #1
lema(ur'[Ff]otogr_á_fic[ao]s?_a', xpre=[ur'Informazione ', ur'percorso ', ur'immagine ', ur'Mostra ', ur'atlante '], xpos=[ur' con testi']) + #1
lema(ur'[Gg]eneal_ó_gic[ao]s?_o', xpre=[ur'\be ', ur'\b(?:et|re) '], xpos=[ur' delle']) + #1
lema(ur'[Gg]eogr_á_fic[ao]_a', xpre=[ur'Congresso ', ur'[Ss]ociet[áà] ', ur'[Ss]toria ', ur'Frazione ', ur'di una carta ', ur'[Ii]ndicazione ', ur'Istituto '], xpos=[ur', (?:edizione|statistico|nazionale|militare)', ur' (?:dell|Militare|ed|di|das|del mondo|Mondiale|Universale)']) + #1
lema(ur'[Gg]eol_ó_gic[ao]s?_o', xpre=[ur' e ', ur' et ', ur'Scripta ', ur'Shakspeareana ', ur'Ufficio ', ur'Studia ', ur'Società ', ur'Carolinae - ', ur'Carolinae: '], xpos=[ur', Palaeontologica et', ur' (?:Sinica|Lilloana|Acta)']) + #1
lema(ur'[Gg]obern_ó__o', xpre=[ur'(?:[Ee]l|[Uu]n|[Dd]e) ', ur'V[ií]a del ', ur'[Dd]el ', ur'[Dd]o ', ], xpos=[ur'(?: de Galicia)', ]) + #6
lema(ur'[Hh]er_o_ic[ao]s?_ó', xpre=[ur' e ', ur'Tempos ']) + #1
lema(ur'[Hh]erb_á_cea_a', xpre=[ur'Aloe ', ur'Amorpha ', ur'Artemisia ', ur'Ageratina ', ur'[BCEHMSV]\. ', ur'Buddleja ', ur'Begonia ', ur'Capparis ', ur'Cattleya ', ur'Clidemia ', ur'Calycera ', ur'Cicindela ', ur'Calanthe ', ur'Chrysomela ', ur'Chrysolina ', ur'Cornus ', ur'Careya ', ur'var\. ', ur'Eugenia ', ur'Erica ', ur'Epitenodera ', ur'Epipactis ', ur'Erythrina ', ur'Eulophia ', ur'Euphorbia ', ur'Eurydema ', ur'Geophila ', ur'Grewia ', ur'Haworthia ', ur'Histiopteris ', ur'Jatropha ', ur'Memphis ', ur'Nemexia ', ur'Oldenburgia ', ur'Pteromonnina ', ur'Pavetta ', ur'Sybra ', ur'sicula ', ur'salicis-', ur'Sida ', ur'Salvia ', ur'Salicornia ', ur'Sambucus ', ur'Smilax ', ur'Sesbania ', ur'Salix ', ur'Solandra ', ur'Tetradenia ', ur'Tibouchina ', ur'Tetraneuris ', ur'Tetragonia ', ur'Vinca ', ur'Xerothamnella ', ur'Zornia '], xpos=[ur'\'']) + #1
lema(ur'[Hh]u_é_rfan[ao]s?_e', xpre=[ur'Christian ', ur'Camilo '], xpos=[ur' \(Colorado']) + #1
lema(ur'[Ii]_mbé_cil(?:es|)_(?:nb[eé]|mbe)', xpre=[ur'No ', ur'Vile ', ur'Rotten '], xpos=[ur'\.com']) + #1
lema(ur'[Ii]d_é_ntic[ao]s?_e', xpre=[ur'L\'']) + #1
lema(ur'[Ii]n_ú_til(?:mente|)_u', xpre=[ur'L\'espera ']) + #1
lema(ur'[Ii]nt_é_rpretes_e', pre=ur'(?:[Ll]as|[Ll]os|[Ee]s) ', xpos=[ur' (?:como|siente|\'\'a capella|el|[ay] )']) + #1
lema(ur'[Ii]nter_é_s_e', xpos=[ur'\]']) + #1
lema(ur'[Ii]sl_á_mic[ao]s?_a', xpre=[ur'Leptanilla ', ur'diritto ', ur'espansione ']) + #1
lema(ur'[Jj]am_á_s_a', xpre=[ur'Abel ']) + #1
lema(ur'[Jj]ard_í_n_i', pre=ur'(?:[Dd]el|[Ee]l|[Ss]u|[Tt]u|para|dicho) ', xpos=[ur' (?:pour|des|du |En Méditerranée|de Passacailles|[Bb]otanique|séculaire|d[\'’])', ]) + #25
lema(ur'[Ll]lovi_ó__o', xpre=[ur'\ba ', ur'Estación de ', ur'Llovio\|', ur'Túnel de ', ur'\ben ',ur'\['], xpos=[ur' • Ribadesella']) + #13
lema(ur'[Ll]ogr_ó_ +(?:[a-z]+[aei]r|[0-9]+)(?:se|)\b_o', xpre=[ur'grande ', ur'gran ', ur'[Cc][oó]mo ', ur'mayor ', ur'destacado ', ur'notable ', ur'[Uu]n ']) + #1
lema(ur'[Mm]_é_dico_e', pre=ur'(?:[Aa]l|[Ee]l|[Ss]u|[Uu]n|como) ', xpos=[ur' in ']) + #1
lema(ur'[Mm]_ó_vil(?:es|)_o', xpre=[ur'and '], xpos=[ur'@ccess', ur' (?:Tours|Air|Acces)']) + #1
lema(ur'[Mm]elanc_ó_lic[ao]s?_o', xpos=[ur' – Allegro']) + #1
lema(ur'[Mm]eti_ó__o', xpre=[ur' tri ', ], xpos=[ur' (?:Rufo|Marulo|Marullus|Fufecio)', ]) + #2
lema(ur'[Mm]icrobiolog_í_as?_i', xpos=[ur' (?:Ambiental|e Parasitologia|- Manual de Aulas Práticas)']) + #1
lema(ur'[Mm]icrosc_ó_pic[ao]s?_o', xpre=[ur'Ascodesmis ', ur'Lemna ', ur'Orthocosta '], xpos=[ur' (?:di|corporis|ron)\b']) + #1
lema(ur'[Mm]itolog_í_as?_i', xpre=[ur'sulla ', ur'Herriko ', ur'Relats de '], xpos=[ur' (?:locale|grega|vedica|comparata)']) + #1
lema(ur'[Mm]ovi_ó__o', xpre=[ur'Gonzalo ', ur'Simone ', ur'Tomás ', ]) + #1
lema(ur'[Mm]uri_ó__o', xpre=[ur' de ', ur'Enric ', ur'John ', ur'Francisco ', ur'Jordi ', ]) + #8
lema(ur'[Nn]_á_ufrag(as|os?)_a', xpre=[ur'[Qq]ue ', ur'Denboraren ']) + #1
lema(ur'[Nn]_í_tric[ao]s?_i', xpre=[ur'l’acido ']) + #1
lema(ur'[Bb]aron_í_as?_i', xpre=[ur'\| Alfara de la ', ur'[Ss]ossio ', ur'Tòfona de la '], xpos=[ur'\]', ur' (?:di|\(Anacardiaceae|Bassa)\b']) + #8
lema(ur'[Bb]rujer_í_as?_i', xpre=[ur'canción de ', ur'regresó a ', ur'miembro de ', ur'banda\)\|'], xpos=[ur' \(banda']) + #8
lema(ur'[Cc]aballer_í_as?_i', xpre=[ur'fragmento de \'\'Flor de ']) + #32
lema(ur'[Cc]apitan_í_as?_i', xpre=[ur'\b[dn]a '], xpos=[ur' (?:dos|d|de São)\b']) + #8
lema(ur'[Cc]elos_í_as?_i', xpre=[ur'\[', ur'Iresine '], xpos=[ur' (?:argentea|monsoniae|paniculata)']) + #8
lema(ur'[Cc]inematograf_í_as?_i', xpre=[ur'\b[Dd]i ', ur'Coralta ']) + #8
lema(ur'[Cc]iudadan_í_as?_i', xpre=[ur'Breviari de ', ur'Nova ']) + #32
lema(ur'[Cc]onsultor_í_as?_i', xpre=[ur'Scot '], xpos=[ur' (?:em|e educação)']) + #8
lema(ur'[Cc]ortes_í_as?_i', xpre=[ur'Godoy y ', ur'\bi ']) + #8
lema(ur'[Dd]emograf_í_as?_i', xpre=[ur'alla ']) + #8
lema(ur'[Dd]ir_í_a[ns]?_i', xpre=[ur'Eu '], xpos=[ur' y los', ur'(?:\'\'|\]\])']) + #32
lema(ur'[Ee]timolog_í_as?_i', xpos=[ur' (?:African|da Palavra)', ur'\.dechile']) + #16
lema(ur'[Ff]ilolog_í_as?_i', xpre=[ur'\be ', ur'Interuniversitari de ', ur'Portuguesa de ', ur'Departament de ', ur'sigle de ', ur'Seminari de ', ur'Quaderns de ', ur'Grande Antologia ', ur'Anuari de ', ur'alla '], xpos=[ur' (?:da|eta|catalana i|de la Universitat|e (?:storia|cr[ií]tica|modernità|letteratura)|Anglesa)\b']) + #32
lema(ur'[Gg]raf_í_as?_i', xpos=[ur' (?:parishii|foi|de l\'Occitan)', ur'\'\'']) + #8
lema(ur'[Hh]abr_í_a[ns]?_i', xpre=[ur'Ain ']) + #32
lema(ur'[Hh]egemon_í_as?_i', xpre=[ur'\b[Aa] '], xpos=[ur' e terror']) + #16
lema(ur'[Ii]ron_í_as?_i', xpre=[ur'\bè ']) + #8
lema(ur'[Ll]itograf_í_as?_i', xpos=[ur' (?:i|de Agustin Peiró)\b']) + #16
lema(ur'[Mm]_í_as_i', xpos=[ur'\]\]']) + #1000
lema(ur'[Mm]as_í_as?_i', xpre=[ur'Alessandro ', ur'Aïllada ', ur'Gioia ', ur'Lisandro '], xpos=[ur' (?:Muju|d\'en|dels|One|Cal)\b', ur'\'\', Escuela']) + #16
lema(ur'[Mm]eteorolog_í_as?_i', xpre=[ur'\bdi ', ur'Nova ', ur'della '], xpos=[ur' (?:e Recursos|Aetnea)']) + #8
lema(ur'[Mm]etodolog_í_as?_i', xpre=[ur'\be '], xpos=[ur', métodos e técnicas', ur' (?:aplicadas desde a|e didattica|da|de (?:Disseny|l\'istòria)|para quantificação|Interativa)']) + #16
lema(ur'[Nn]eumon_í_as?_i', xpos=[ur' in']) + #8
lema(ur'[Pp]od_í_a[ns]?_i', xpre=[ur'Ninguém ', ur'Não '], xpos=[ur' [Aa]cabar o [Mm]undo']) + #32
lema(ur'[Pp]ornograf_í_as?_i', xpos=[ur' i vestits']) + #8
lema(ur'[Pp]rofec_í_as?_i', xpre=[ur'\b[Aa] ', ur'\bda '], xpos=[ur' e memória']) + #32
lema(ur'[Rr]egal_í_as?_i', xpre=[ur'Peaches en ', ur'[IiJj]ura ', ur'Facu ', ur'Facundo ', ur'\bin ', ur'sive ', ur'Danzai no '], xpos=[ur' (?:Bay|building|acad[ée]micas|dicuntur|insignia)\b', ur'(?:: (?:insignia of|The)|\'\'|\]\]|\])']) + #8
lema(ur'[Rr]oc_í_a[ns]?_i', xpos=[ur' Gracie']) + #8
lema(ur'[Ss]abidur_í_as?_i', xpos=[ur' patrona de la']) + #32
lema(ur'[Ss]angr_í_as?_i', xpre=[ur'Sweet ']) + #8
lema(ur'[Ss]equ_í_as?_i', xpos=[ur' (?:de Sollana|Mare)']) + #32
lema(ur'[Ss]impat_í_as?_i', xpre=[ur'\bas ', ur'Cidade']) + #8
lema(ur'[Ss]ol_í_a[ns]?_i', xpre=[ur'\by ', ur'biella que ', ur'antigua ', ur'Patricia '], xpos=[ur' (?:\(en el|deriva)', ur'\'\'\' es']) + #32
lema(ur'[Tt]rilog_í_as?_i', xpre=[ur'izeneko ', ur'itsasoa '], xpos=[ur' (?:delle|romana|cunoaşterii|culturii|cosmologică|Belgrădeană|della|di)\b', ur', Libellula']) + #32
lema(ur'[Vv]ig_í_as?_i', xpre=[ur'Brasil\)\|'], xpos=[ur' (?:da|\(Brasil)\b']) + #8
#lema(ur'[Aa]ntropolog_í_as?_i', xpre=[ur'[Ddl][´’\']', ur' [àae] ', ur' (?:e[dm]|in|as|[dn][ai]) ', ur'dal sito ', ur'festa\. ', ur'estudo de ', ur'Avançats en ', ur'Ensaios de ', ur'Boletim de ', ur'Equatorial de ', ur'Piazza\. ', ur'Sociologia i ', ur'Estudos de ', ur'brasileir[ao]s de ', ur'Brasileira de '], xpos=[ur' (?:nel|das?|dell|[Dd]ell[ao]|n[ao] |del (?:cervello|pastore|Conflicte Urbà)|called|brasileiras de|Cristã|medica\. Saperi|i Etnografía|Indígena(?:: Uma| - Uma)|Aplicada ao|Mèdica|brasileira|poética das|hermenêutica|social\. Zahar|de (?:la religió\'|la vida quotidiana)|e (?:altri|diretito|Etnologia|Educação|Mondo|Historia|storia|Indigenismo na)|\(São)', ur', (?:histórias)']) + #0
lema(ur'[Nn]aci_ó__o', xpre=[ur'Copa ', ur'El ', ], xpos=[ur' (?:y Criao|Herb)', ]) + #8
lema(ur'[Oo]blig_ó__o', xpre=[ur'\by ', ur'\bte ']) + #1
lema(ur'[Oo]r_í_genes_i', xpos=[ur' \& Associates']) + #1
lema(ur'[Oo]rganiz_ó__o', xpre=[ur'Junulara ', ur'Naturista ']) + #10
lema(ur'[Pp]_á_ramos?_a', xpre=[ur'\bin ', ur'\bo ', ur'Adriana ', ur'[Nn]os ', ur'Santi ', ur'the '], xpos=[ur' (?:dharmáh|dharmaḥ|nunca)']) + #1
lema(ur'[Pp]_é_ndulos?_e', xpos=[ur', Doubtful', ur' (?:Studios|lanzó)']) + #1
lema(ur'[Pp]_ú_blica_u', pre=ur'(?:Notar[ií]a|[Tt]elevisi[oó]n|[Pp]olítica) ', xpos=[ur' un']) + #1
lema(ur'[Pp]_ú_lpitos?_u', xpos=[ur'\'', ur' (?:de chocolate|di |tehuelche|\(Orful)', ur', Nartece']) + #1
lema(ur'[Pp]_ú_trid[ao]s?_u', xpre=[ur'Cyclocephala ', ]) + #1
lema(ur'[Pp]aleontol_ó_gic[ao]s?_o', xpre=[ur'Societa '], xpos=[ur' e Geol[oó]gico']) + #1
lema(ur'[Pp]arti_ó__o', xpre=[ur'[Cc]orazón ', ]) + #3
lema(ur'[Pp]aup_é_rrim[ao]s?_e', xpre=[ur'magistrorum ']) + #1
lema(ur'[Pp]ediatr_í_as?_i', xpre=[ur'della ', ur'\bdi ', ur'Symposia – '], xpos=[ur' d’Urgenza']) + #1
lema(ur'[Pp]idi_ó__o', xpre=[ur'del ', ur'(?:Lo|El) ']) + #3
lema(ur'[Pp]in_z_as?_s', xpos=[ur'["\']', ur' Attack']) + #1
lema(ur'[Pp]ir_á_mides?_i', xpos=[ur' di ']) + #1
lema(ur'[Pp]neum_á_tic[ao]s?_a', xpre=[ur'\[\[', ur'seu ', ur'Battello ', ur'Antlia ', ur'Martello ']) + #1
lema(ur'[Pp]odr?_í_amos_i', xpre=[ur'nom ']) + #1
lema(ur'[Pp]ol_é_mic[ao]s?_e', xpre=[ur'di una '], xpos=[ur' (?:in|tra)\b']) + #1
lema(ur'[Pp]r_í_ncipes?_i', pre=ur'(?:[AaEe]l|[Ll]os|[Uu]n|[Uu]nos) ', xpre=[ur' di '], xpos=[ur' metaphysique']) + #1
lema(ur'[Pp]ro_y_ectos?_j', xpre=[ur'\bin ', ur'\bcom '], xpos=[ur' (?:971|Francesinha|e edifícios|do|Eficiência|impossível|Vercial)\b']) + #154
lema(ur'[Pp]rogn_ó_stic[ao]s?_o', xpre=[ur'Hippocratis ', ur'\bet ', ur'Lunario Y '], xpos=[ur'\'']) + #1
lema(ur'[Pp]ublic_ó_ (?:el|las?|los|una?)_o', xpre=[ur'\bal ']) + #1
lema(ur'[Rr]_í_os?_i', pre=ur'(?:[Ll]os|[Uu]nos|[Vv]arios) ', xpos=[ur' Carcedo']) + #1
lema(ur'[Rr]_í_tmic[ao]s?_i', xpre=[ur'Allegro ', ur'ben ']) + #1
lema(ur'[Rr]_ú_stic[ao]s?_u', xpre=[ur'\bo ', ur'Via ', ur'Nicotiana ', ur'Catonis ', ur'Villa ', ur'Columbella ', ur'alla ', ur'\b(?:[Rr]e|di) ', ur'Emberiza ', ur'Capitalis ', ur'Antonio ', ur'Éditions ', ur'[Hh]irundo '], xpos=[ur'[\]\']', ur' (?:di|degli|Carpio|Xalostoc|nelle|de (?:Filippo|Narbona)|UIR|per|\(revista)\b']) + #1
lema(ur'[Rr]e_í_a[ns]?_i', xpre=[ur'programación\)\|', ur'Kiyoku ', ur'wa '], xpos=[ur'[\'\]?]', ur' (?:\(lenguaje|Hiruda|Barbut)']) + #1
lema(ur'[Rr]ealiz_ó__o', xpos=[ur' mis']) + #31
lema(ur'[Rr]ev_ó_lver_o', pre='(?:[Ee]l|[Uu]n|[Cc]on) ', xpos=[ur' Golden']) + #1
lema(ur'[Rr]id_í_cul[ao]s?_i', xpre=[ur'\bet ', ur'Aristolochia ']) + #1
lema(ur'[Rr]omer_í_as?_i', xpos=[ur' \(género', ur'[\]\']']) + #1
lema(ur'[Ss]_á_tiras?_a', xpre=[ur'della ']) + #1
lema(ur'[Ss]_ó_lid[ao]s_o', xpre=[ur'Rocka ', ur'duos ', ur'septem ', ], xpos=[ur' mulier', ur'\.es']) + #43
lema(ur'[Ss]abr_í_a[ns]?_i', xpos=[ur' Dahane']) + #1
lema(ur'[Ss]at_é_lites?_e', xpre=[ur'Sirus '], xpos=[ur' Awards']) + #1
lema(ur'[Ss]er_í_an_i', xpre=[ur'Metazygia ']) + #1
lema(ur'[Ss]imp_á_tic[ao]s?_a', xpre=[ur'sunnambola / '], xpos=[ur' [Mm]ascalzone']) + #1
lema(ur'[Ss]in_ _embargo_', xpos=[ur'\.mx']) + #1
lema(ur'[Ss]orbi_ó__o', xpre=[ur' [yo] ', ur' el ', ur'Alfabeto ', ur'Colegio ', ur'Seminario ', ur'[Aa]lto ', ur'[Bb]ajo ', ur'[Ii]dioma ', ur'[Pp]eriódico ', ur'[Pp]ueblo ', ur'\|', ur'civil ', ur'del ', ur'derecho ', ur'elemento ', ur'en ', ur'espíritu ', ur'fiesta ', ur'hablaba ', ur'himno ', ur'nacional ', ur'pasado ', ur'pueblito ', ur'territorio ', ], xpos=[ur' (?:Zarow|que|[Aa]lto|[Bb]ajo|en )', ur'[\]|]', ]) + #2
lema(ur'[Tt]_í_[ao]s?_i', pre=ur'(?:[Ee]l|[Ll]as?|[Ll]os|[Uu]na?|[Uu]n[ao]s|[Ss]us?|y|[Cc]on|[Uu]na?|[Dd]os|[Tt]res|[Cc]uatro) ', xpre=['testament de ', ur'Mia '], xpos=[ur' por']) + #1
lema(ur'[Tt]ecnol_ó_gic[ao]s?_o', xpos=[ur'umanesimo ']) + #1
lema(ur'[Tt]el_é_grafos?_e', xpre=[ur'Il '], xpos=[ur' and']) + #1
lema(ur'[Tt]ent_ó__o', xpre=[ur'Bannou ', ur'Matsui ', ], xpos=[ur' (?:I|\(Febrero)', ur'(?:\)|\'\')', ]) + #1
lema(ur'[Tt]opogr_á_fic[ao]s?_a', xpos=[ur' e geometica']) + #1
lema(ur'[Tt]r_á_nsito_a', xpre=[ur'Cappella del '], xpos=[ur' "Frankie']) + #1
lema(ur'[Tt]r_á_queas?_a', xpos=[ur'\]']) + #1
lema(ur'[Tt]raves_í_as?_i', xpre=[ur'millor ']) + #1
lema(ur'[Vv]e_z__s', pre=ur'(?:[Uu]na|[Ee]sta|[Ee]sa|[Cc]ada|[Ss]ola|[Ee]n|[Pp]or) ', xpos=[ur' blanquecino']) + #De
lema(ur'[Vv]ig_é_sim[ao]s?_e', xpre=[ur'alla '], xpos=[ur' libertatis']) + #1
lema(ur'[Vv]ivi_ó__o', xpre=[ur'Marco ', ur'Subaru '], xpos=[ur' (?:Pacioco|Sedan)']) + #6
lema(ur'[Zz]apater_í_as?_i', xpos=[ur' hirsuta']) + #1
lema(ur'[e]ligi_ó__o', xpre=[ur'ANCONA, ', ur'Juan ', ur'Gabriel ', ur'[Ss]an ', ur'\['], xpos=[ur' (?:R\.|Bravo|Juárez|Restifo|Anzola|Flores|[Aa]yala|Lozada|Calderón|Ancona|Alzuru|Cedeño|Mendoza|Victoria|Esquivel|y Juan|renuncia|no acepta)', ]) + #31
lema(ur'[e]rigi_ó__o', xpre=[ur'Erigyius ', ], xpos=[ur' mató', ur'\]', ]) + #1
lema(ur'_V_oleibol_B', xpos=[ur' Taldea']) + #1
lema(ur'_h_asta (?:el|ahora)_', xpre=[ur'Compluto, ']) + #1
lema(ur'_hu_yen?_u', xpos=[ur'Aoi no ']) + #1
lema(ur'_Á_rbol_A', xpos=[ur' Malacca']) + #191
lema(ur'_Í_dolos?_I', xpos=[ur' (?:infranto|folk|speculi|della)', ]) + #1
lema(ur'_Ó_xidos?_O', xpre=[ur'director: ', ]) + #1
lema(ur'_á_rbitros?_a', xpre=[ur'L\'']) + #1
lema(ur'_í_dolos?_i', xpre=[ur'[Ll]\'', ur'nia kar ', ur'nia grand '], xpos=[ur' ji']) + #1
lema(ur'_ó_rganos?_o', xpre=[ur'\bDe ', ur'\bin ', ur'per ', ur'[DdLl][\'’]']) + #1
lema(ur'_ó_xidos?_o', xpre=[ur'[Ss]e ']) + #1
lema(ur'q_ue__', pre=ur'(?:[Pp]or|[Pp]ara|[Pp]ero) ', xpos=[ur'[<]', ur' є']) + #1
lema(ur'[Ll]a primer_a__', xpos=[ur' (?:ministro|miembro)']) + #1
lema(ur'[Pp]_ú_rpuras?_u', xpre=[ur'(?:M\.|R,) ', ur'\'\'De ', ur'thrombocytopenic ', ur'Orchis ', ur'Henoch-Schonlein ', ur'erythrostomus, ',], xpos=[ur' (?:scorbutica|[Tt]rombocitopenia|patula|venosa)', ur'\.micolegio', ]) + #1
lema(ur'[Rr]_é_plicas_', xpre=[ur'prop ', ur'the ', ur'Master ', ur'\'\''], xpos=[ur' (?:in|look|of|that|917)']) + #1
lema(ur'[Cc]r_í_a[ns]?_i', xpos=[ur' a universidade', ur'\.org']) + #1
lema(ur'[Mm]agn_é_tic[ao]s?_e', xpos=[ur' vulnerum']) + #1
lema(ur'[Tt]ransform_ó__o', xpos=[ur' (?:em)\b']) + #1
lema(ur'[Ee]ntre__ver_ ', xpre=[ur'escoger ']) + #1
lema(ur'[Rr]adiof_ó_nic[ao]s?_o', xpre=[ur'Unione '], xpos=[ur' che']) + #1
lema(ur'[Dd]efensor_í_as?_i', xpre=[ur'patria ', ur'Ep[ií]stola ']) + #1
lema(ur'[Dd]ivi_di_d[ao]s_', xpre=[ur'Denise ']) + #1
lema(ur'[v]er_í_a[ns]?_i', xpre=[ur'Vería, '], xpos=[ur' (?:\(género|Stadium|Football|FC|F\. C\.)', ur'(?:\]|, Veria)']) + #247
lema(ur'[Ee]scuder_í_as?_i', xpos=[ur' d\'Scalextric']) + #165
lema(ur'[Ff]actor_í_as?_i', xpos=[ur' (?:Escènica|d[’\'](?:Arquitectura|Arts))', ]) + #139
lema(ur'[Mm]aestr_í_as?_i', xpos=[ur' di ']) + #109
lema(ur'[Aa]ver_í_a[ns]?_i', xpre=[ur'Ionel ']) + #60
lema(ur'[Pp]refer_í_a[ns]?_i', xpre=[ur' de '], xpos=[ur' (?:==|de)']) + #39
lema(ur'[Cc]afeter_í_as?_i', xpre=[ur'The ', ur'Nightmare ', ], xpos=[ur' (?:in|of|workers|Ladies|Table|Riot|food|roenbergensis|\(protista)', ur'\]', ]) + #34
lema(ur'[Cc]ubr_í_a[ns]?_i', xpre=[ur'Nicolás ', ur' de ']) + #34
lema(ur'[Gg]rader_í_as?_i', xpos=[ur' (?:speciosa|scabra|subintegra|fruticosa|linearifolia)', ur'[\]\']']) + #33
lema(ur'[Ee]str_í_as?_i', xpos=[ur'\]']) + #29
lema(ur'_han_ (?:adquirido|agregado|anunciado|asociado|bautizado|cambiado|cerrado|creado|dado|debutado|dicho|disputado|entrometido|esperado|estado|expandido|ganado|implementado|jugado|labrado|lanzado|liberado|limitado|llegado|llenado|llevado|logrado|maldecido|manejado|manifestado|mantenido|marcado|matado|mejorado|mencionado|metido|modelado|modernizado|mostrado|multiplicado|nacido|observado|obtenido|ocupado|ofrecido|ordenado|participado|pasado|peleado|perdido|permanecido|permitido|perseguido|pertenecido|podido|portado|pose[ií]do|presentado|probado|promovido|propagado|prosperado|provocado|publicado|puesto|quedado|realizado|recibido|recuperado|regalado|registrado|regresado|renunciado|repercutido|replanteado|representado|respondido|restaurado|retenido|retratado|reunido|revelado|revisado|revolucionado|sabido|sacado|salido|seguido|sentido|separado|servido|señalado|sido|sobrevivido|sostenido|sufrido|sugerido|superado|suspendido|sustituido|tenido|terminado|tocado|tomado|tra[ií]do|trabajado|transcurrido|transformado|trasladado|tratado|ubicado|usado|utilizado|variado|vendido|venido|vestido|viajado|visto|vivido|vuelto)_an', xpre=[ur'[0-9]', ur'[XJ]in\'', ]) + #49
lema(ur'[Oo]nom_á_stic[ao]s?_a', xpre=[ur'Egyptian ', ur'Giorno '], xpos=[ur' della']) + #1
lema(ur'[Cc]icl_í_stic[ao]s?_i', xpre=[ur'Settimana ', ur'Prova ', ur'[Gg]iro ', ur'[Ss]ettiman ', ur'[Ff]ederazione ', ur'[Ss]ocieta ', ur'[Gg]ara ', ur'[Aa]ssociazione ',]) + #1
lema(ur'[Nn]eurol_ó_gic[ao]s?_o', xpos=[ur' (?:Belgica|Scandinavica)']) + #1
lema(ur'[Ff]ilogen_é_tic[ao]s?_e', xpre=[ur'approccio '], xpos=[ur'\.org']) + #1
lema(ur'[Aa]er_ó_dromos?_o', xpre=[ur'Associazione '], xpos=[ur'\.cl']) + #87
lema(ur'[Aa]n_á_log[ao]s?_a', xpre=[ur'[Ee]merita ' ur'Jacobaea ', ur'Emerita ', ur'Hippa ', ur'Cydista ', ur'analoga ', ur'Meliphaga ', ur'Puncturella ', ur'P\. ']) + #69
lema(ur'[Aa]p_í_colas?_i', xpre=[ur'Neocypholaelaps ', ur'Candida ']) + #6
lema(ur'[Aa]rchipi_é_lagos?_e', xpos=[ur'[Tt]he ', ur' Press']) + #99
lema(ur'[Aa]rquitect_ó_nic[ao]s?_o', xpre=[ur'= ', ur'Principia ', ur'arquitectos ', ur'Studio ', ur'Associates, ', ur'Miami\)\|', ], xpos=[ur' (?:ganó|\(estudio|\(Miami)', ur'\]\]']) + #65
lema(ur'[Aa]str_ó_nom[ao]s?_o', xpos=[ur'\.org', ]) + #52
lema(ur'[Aa]tm_ó_sferas?_o', xpre=[ur'\bda ', ur'nell\'\[\['], xpos=[ur' (?:Mažeikiai|da|e di)\b']) + #100
lema(ur'[Aa]tmosf_é_ric[ao]s?_e', xpre=[ur'Elettricità Terrestre ']) + #16
lema(ur'[Bb]_é_lic[ao]s?_e', xpre=[ur'Archaeologia '], xpos=[ur' \(Croacia', ur'(?:\]\]|, (?:Leccino|Lepenica))']) + #35
lema(ur'[Bb]_ú_lgar[ao]s?_u', xpos=[ur' Esperanto']) + #96
#lema(ur'[Bb]as_í_lica_i', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u) ', xpos=[ur' (?:dello|dei|di|San Paolo)\b']) + #1
lema(ur'[Bb]as_í_licas?_i', xpre=[ur'[MDb]\. ', ur'y la \'\'', ur'vena ', ur'della ', ur'\b(?:di|in) ', ur'\be ', ur'Paul’s ', ur'cum ', ur'latín\]\] \'\'', ur'cuius ', ur'alla ', ur'parochialis ', ur'Reale ', ur'Caudisona ', ur'Frauenkirchen ', ur'Gavelinopsis ', ur'Villa ', ur'Münster ', ur'Constantinian ', ur'[Mm]inor ', ur'Mission ', ur'dell’Arca en la ', ur'Myiothlypis ', ur'Acentroptera ', ur'Bamba ', ur'Taal ', ur'Orchis ', ur'Artemisia ', ur'Roman \[\[', ur'\'s ', ur'Treu ', ur'St. Joseph ', ur'Aquileia ', ur'Ducula ', ur'nella ', ur'the ', ur'Cathedral '], xpos=[ur' (?:[Dd]i|of|in|and|dei|degli|dell|dello|Concattedrale|[Ss]ntuario (?:di|del Gesù)|maior|Minor|Nova|Constantini|Cai|Giulia|Iulia|Maxentii|Benedettina|palladiana|established|dello|de (?:Santa Maria degli|la Madonna)|del (?:Crocifisso|Sacré|Sacro)|novarum|Iunii|Fausti|[Ss]otterranea|[Mm]inore|civile|Press|Opera|Cistern|Julia|Sports|[Cc]attedrale|San Paolo|Sanctae|Ulpia|Aemilia|Paulii|Papale di|thermarum|trium|della|Martyrum|superiore|minor|Chymica)\b', ur'(?:, Cignano|\]\]l|"\))']) + #853
lema(ur'[Cc]_é_lulas?_e', xpos=[ur'(?:\]\]r|\'\')', ]) + #114
lema(ur'[Cc]_ú_pulas?_u', xpre=[ur'Hipanto ']) + #101
lema(ur'[Cc]l_é_rig[ao]s?_e', xpre=[ur'André ']) + #61
lema(ur'[Cc]lim_á_tic[ao]s?_a', xpre=[ur'Fascia ', ur'Atlante ', ]) + #79
lema(ur'[Ee]_ó_lic[ao]s?_o', xpre=[ur'\bed '], xpos=[ur' Baia']) + #33
lema(ur'[Ee]clesi_á_stic[ao]s?_a', xpre=[ur'Annales ', ur'auctores ', ur'Convitto ', ], xpos=[ur' de Catalunya']) + #195
lema(ur'[Ee]f_í_mer[ao]s?_i', xpre=[ur'Kostas '], xpos=[ur'\.com']) + #26
lema(ur'[Ee]l_í_ptic[ao]s?_i', xpre=[ur'Tagetes ', ur'Argia ', ur'Rogerella ']) + #24
lema(ur'[Ee]nerg_é_tic[ao]s?_e', xpre=[ur'Companhia '], xpos=[ur' UPME']) + #72
lema(ur'[Ff]_á_rmacos?_a', xpre=[ur'Il '], xpos=[ur'(?:\]\]lógic[ao]s?|\'\' o)']) + #29
lema(ur'[Ff]il_ó_sof[ao]s?_o', xpre=[ur'\bdi un ', ur'\bse ', ur'[Pp]rincipessa ', ur'finta ', ur'antro del ', ur'\b[Ii]l '], xpos=[ur' (?:sobre|mondain|dell|della|peripatetico)\b', ur'\.org']) + #1
lema(ur'[Ff]ilos_ó_fic[ao]s?_o', xpre=[ur'Counseling ', ur'Grande Antologia ', ur'testo ', ur'pensiero ', ur'identità ', ur'universitarios ni ', ur'Circolo ', ur'morale ', ur'storia '], xpos=[ur' (?:di|dei|e (?:scientifico|coscienza|fisiologico)|sul|Attuale)\b']) + #60
lema(ur'[Gg]e_ó_graf[ao]s?_o', xpos=[ur' (?:[Bb]awarskiego|tedesco)']) + #32
lema(ur'[Hh]_á_bitos?_a', xpre=[ur'Cauallero del ', ur'[Dd][oó]nde ', ur'qu[ei] ', ]) + #223
lema(ur'[Hh]_é_lices?_e', xpre=[ur'género\)\|', ur'Pontia ', ur'latín\]\] \'\'', ur'f\. \'\'', ur'transmembrane ', ], xpos=[ur' (?:formosensis|latimera|tientsinensis|tridens|sans|Commonly|granulata|Patino|Gaudichaudi|\(género)', ur'\.net']) + #42
lema(ur'[Hh]_ú_ngar[ao]s?_u', xpre=[ur'Romanza '], xpos=[ur' (?:Vivo|Esperanto)\b']) + #119
lema(ur'[Hh]ero_í_nas?_i', xpre=[ur'género\)\|'], xpos=[ur' (?:isonycterina|\(género)', ur'(?:\.d\b|\'\' \(Director)']) + #190
lema(ur'[Ll]im_í_trofes?_i', xpre=[ur'zone ']) + #56
lema(ur'[Mm]_í_tic[ao]s?_i', xpre=[ur'Terra ', ur'clopotele, ', ur'Sicilia '], xpos=[ur' (?:Filipescu|Pisa)']) + #69
lema(ur'[Mm]and_í_bulas?_i', xpre=[ur'uma ', ur'Euphitrea '], xpos=[ur'\]\]res']) + #33
lema(ur'[Mm]eteorol_ó_gic[ao]s?_o', xpre=[ur'Società ', ur'Societas ', ur'Meteorología \(', ur'Servizio ', ], xpos=[ur'\'\'']) + #59
lema(ur'[Mm]ol_é_culas?_e', xpre=[ur'Truncatellina '], xpos=[ur'(?:\]\]r(?:es|)|\.cl)', ]) + #58
lema(ur'[Nn]umism_á_tic[ao]s?_a', xpre=[ur'Antiqua ', ur'della ', ur'Bibliotheca ', ur'\bdi '], xpos=[ur' (?:e antichità|- Descrizione)']) + #24
lema(ur'[Pp]_á_nicos?_a', xpre=[ur'\bdi ', ur'Sami ', ur'Timor ', ur'Dario ', ur'Giovanni ', ur'Patrizia ', ur'Panico\|', ur'Giuseppe '], xpos=[ur' (?:O|Ia[ck]ovou|Chrysanthou|urvilleani|Orphanides|Pirata|Na)\b', ur'(?:\'s|! La creazione)']) + #113
    lema(ur'[Pp]_á_rroc[ao]s?_a', xpre=[ur'dell\'ex '], xpos=[ur' (?:i|di|in)\b']) + #103
lema(ur'[Pp]anor_á_mic[ao]s?_a', xpos=[ur' (?:di|della)\b']) + #318
lema(ur'[Pp]ar_á_metros?_a', xpre=[ur'int ', ], xpos=[ur', (?:n|Roma)\b']) + #58
lema(ur'[Pp]ara_í_sos?_i', xpre=[ur'\bof ', ur'Sebastiao ', ur'Hai un ', ]) + #579
lema(ur'[Pp]l_á_sticos?_a', xpre=[ur'\'\'', ur'E\.N\.'], xpos=[ur' servicio']) + #48
lema(ur'[Pp]r_é_stamos?_e', xpre=[ur'(?:[sS]i|[Nn]o|[Ll]e) ', ur'que '], xpos=[ur' (?:que passan|servicio|aquí)']) + #293
lema(ur'[Pp]r_ó_logos?_o', xpre=[ur'omnes ', ur'Silvio '], xpos=[ur' (?:ed|a Ritorno|e quattro)\b', ur': Il\b']) + #221
lema(ur'[Pp]rimog_é_nit[ao]s?_e', xpre=[ur'Trichilia '], xpos=[ur' vita']) + #34
lema(ur'[Rr]_ú_nic[ao]s?_u', xpre=[ur'dell\'alfabeto ', ur'Monumenta ', ur'Alboreda '], xpos=[ur'\]']) + #10
lema(ur'[Ss]_í_smic[ao]s?_i', xpre=[ur'Rischio ']) + #40
lema(ur'[Tt]_á_ctic[ao]s?_a', xpre=[ur'\[\['], xpos=[ur' (?:di|Imperialis)']) + #100
lema(ur'[Tt]e_ó_log[ao]s?_o', xpre=[ur'Jana '], xpos=[ur' (?:- Predicatore|cattolico|del (?:Popolo|purgatorio\. Fedeltà))']) + #27
lema(ur'[Tt]op_ó_nimos?_o', xpre=[ur'Bels ']) + #55
lema(ur'[Uu]rban_í_stic[ao]s?_i', xpre=[ur'\be ', ur'l[\'’]', ur'dell\'', ur'\bdi ', ur'storia '], xpos=[ur'(?:"|, architettonica)', ur' e (?:archeologia|architettura)']) + #48
lema(ur'[Vv]_í_speras?_i', xpre=[ur'Lucifer: ']) + #95
lema(ur'[Vv]est_í_bul[ao]s?_i', xpos=[ur' emotional']) + #31
lema(ur'[Dd]istra_í_d(?:[ao]s?|amente)a_i', xpos=[ur'\.org', ]) + #1
lema(ur'[Aa]ntr_ó_pic[ao]s?_o', xpre=[ur'influsso ']) + #1
lema(ur'Boyac_á__a', xpre=[ur'\bof ']) + #1
lema(ur'_É_tic[ao]s?_E', xpre=[ur'Popolare '], xpos=[ur' (?:della|e Vita)', ur'(?:; con una|e analisi)']) + lema(ur'_é_tic[ao]s?_e', xpre=[ur'\bed ']) + #1
lema(ur'[Ee]pidemiolog_í_as?_i', xpos=[ur'i Demografía']) + #1
lema(ur'[Cc]_á_liz_a', xpre=[ur'Poyal ']) + #34
lema(ur'[Hh]_ú_sar(?:es|)_u', xpre=[ur'D\. ', ur'occitano\]\] \'\'\'', ur'OV ', ur'ihr ', ur'treue ', ur'treuer ', ur'Goethes ', ur'Schwarze ', ur'Marija ', ur'Lubomyr ', ur'Liviu ', ur'fesche ', ur'Radovan ', ur'Dieter ', ur'Al ', ur'rock ', ur'cómic\)\|', ur'Comics\)\|', ur'schwarze ', ur'Chilena '], xpos=[ur' (?:Opera|\((?:cómic|Marvel Comics))', ur'(?:\]\]|, Starbolt)']) + #75
lema(ur'[Nn]_á_car_a', xpre=[ur'Leslie ', ur'Eloino ', ur'Bertino ', ur'Noel A ', ur'Percival ', ur'Manilyn ', ur'Doleschallia ', ur'Vizconde de ', ur'Esteban '], xpos=[ur' de Tupot']) + #24
lema(ur'[Nn]_é_ctar_e', xpre=[ur'Arula\'\', \'\'', ur'of '], xpos=[ur' (?:feeding|Variations|receivers|robbery|sources|ecology|production)']) + #167
lema(ur'[Ss]_í_mil(?:es|)_i', xpre=[ur'alii '], xpos=[ur' (?:rodhes|est)']) + #54
lema(ur'[Tt]r_é_bol(?:es|)_e', xpos=[ur' Clan']) + #125
lema(ur'[Tt]r_í_ceps_i', xpre=[ur'Hydnora ', ur'Juncus ', ur'subsp\. ', ur'Hydnora ', ur'filosofía \'\'', ur'Cousinia '], xpos=[ur' (?:brachii|extensor|surae)']) + #47
lema(ur'[Ii]ran_í_(?:es|)_i', xpre=[ur'Honey ', ur'Boman ', ur'Natasha ', ur'Ardeshir '], xpos=[ur' (?:Rael|Sharif)', ur', Shahrukh']) + #1
lema(ur'[Ii]raqu_í_(?:es|)_i', xpos=[ur' Oil', ur'\. Jinete']) + #1
lema(ur'[Jj]abal_í__i', xpre=[ur'\bAl ', ur'Roberto ', ur'Jabali\|']) + #1
lema(ur'[Mm]anat_í_(?:es|)_i', xpos=[ur'\.pr']) + #1
lema(ur'[Mm]aniqu_í__i', xpre=[ur'río ', ur'Alto ', ur'Pizza o ']) + #1
lema(ur'[Mm]arroqu_í__i', xpre=[ur'María ']) + #1
lema(ur'[Rr]earregl_ó__o', xpre=[ur'[Cc]on ', ur'(?:[Uu]n|[Ee]l) ']) + #1
lema(ur'[Ss]efard_í__i', xpre=[ur'Bustan '], xpos=[ur' Kultturist']) + #1
lema(ur'[Jj]ud_a_ic[ao]s?_á', xpre=[ur'Civilização ']) + #1
lema(ur'[Ii]nform_ó__o', xpre=[ur'\b[Yy]o ', ur'\bo "'], xpos=[ur' (?:que (?:no estaré|si usted))']) + #1
lema(ur'[Cc]ong_é_nit[ao]s?_e', xpre=[ur'Litoria ']) + #1
lema(ur'[Pp]rincip_i_os?_', xpos=[ur' defeso']) + #1
lema(ur'[Gg]eobot_á_nic[ao]s?_a', xpre=[ur'Phytotaxonomica ', ur'Folia ', ur'Series A, Taxonomica, ']) + #1
lema(ur'[Cc]_ó_smic[ao]s?_o', xpre=[ur'mistero '], xpos=[ur' (?:do|Artists)\b']) + #1
lema(ur'¿[Pp]or_ qué__(?:qu[eé]| [Qq]ue)', xpos=[ur' decide establecer']) + #1
# lema(ur'[Pp]r_á_ctic[ao]_a', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Dd]e) ', xpre=[ur'nadie ', ur'aun ', ur'se ']) + #1
lema(ur'[Pp]r_á_ctica_a', pre=ur'(?:[Aa]|[Ee]n|[Dd]e|[Uu]na?|[Pp]ara) la ', xpos=[ur' (?:iudiciaria|della)']) + #1
lema(ur'[Rr]_é_cords?_e', pre=ur'(?:[Ll]os|[Uu]nos|[Ee]l|[Uu]n|[Ss]us?|nuevos?|anterior(?:es|)|otros?) ', xpos=[ur' (?:i|o un Recordset|Week|Store|Manager|Plant|Academy|[Rr]eport)\b']) + #1
lema(ur'[Rr]_é_cords? (?:del?|que|Guiness|absoluto|[Mm]undial|[Oo]l[ií]mpico)_e', xpre=[ur'(?:[Ee]l|[Uu]n|[Ss]u) ', ur'\b[KM] ', ur'Bros\. ', ur'ABC ', ur'Active ', ur'Jazzman ', ur'Atlantic ', ur'Colpix ', ur'Gigolo ', ur'Dekathlon ', ur'Wondaland ', ur'URL ', ur'Fear ', ur'Virgin ', ur'Columbia ', ur'Radish ', ur'Daily ', ur'Selectric ', ur'Doorn ', ur'Invasion ', ur'Flicker ', ur'Capitol ', ur'House ', ur'Repsychled ', ur'Counterfeit ', ur'Tower ', ur'Blind ', ur'RCA ', ur'Earache ', ur'Cleopatra ', ur'Hollywood ', ur'MODE ', ur'Nine ', ur'Elígeme ', ur'Pulse ', ur'London ', ur'Jive ', ur'Ultra ', ur'Reprise ', ur'Napalm ', ur'Stiff ', ur'nuevo ', ur'anterior ', ur'otro ', ur'speed ', ur'Rede ', ur'Cinematic ', ur'World ', ur'Boot ', ], xpos=[ur' (?:l|France|Saló|Comunicações|València)\b']) + #1
lema(ur'[Hh]echi_c_er[ao]s?_z', xpre=[ur'bruxa y '], xpos=[ur' Band']) + #1
lema(ur'[Cc]_á_ncer_a', pre=ur'(?:[Ee]l|[Uu]n|al|del?|por|tenía|tiene|tuvo) (?:\[\[|)', xpos=[ur' (?:and|Therapy|pagurus|Council|Bats|Research|Immunology)\b']) + #1
lema(ur'[Cc]_á_ncer(?:\]\]|) (?:del?|en)_a', xpre=[ur'(?:[Ee]l|[Uu]n|al|de) \[\[', ur'(?:[Ee]l|[Uu]n|al|de) ', ur'(?:del|por) \[\[', ur'(?:del|por) ', ur'Gastric ', ur'Dinah '], xpos=[ur' (?:la MEN|inglés)']) + #1
lema(ur'[Pp]r_ó_statas?_o', xpre=[ur'Eumorphia ', ur'Pernettya ', ur'var\. '],) + #1
lema(ur'_s_edes? de_c', xpre=[ur'(?:[EeÉé]l|lo|un) ', ur'\bo ', ur'del ', ur'Villota ', ur'no la ', ur'que ']) + #1
lema(ur'[Tt]oponom_á_stic[ao]s?_a', xpos=[ur', Relazioni']) + #1
lema(ur'[Bb]_e_mol_é', xpre=[ur'Nocturne en Mi '], xpos=[ur' (?:Mineur|Majeur)']) + #1
lema(ur'[Oo]x_í_genos?_i', xpos=[ur'\.bo']) + #1
lema(ur'[Nn]_ó_dulos?_o', xpos=[ur'\.org']) + #1
lema(ur'[Ll]_i_quen_í', xpre=[ur'Lira de ', ur'Siphula \('], xpos=[ur'\]\]es']) + #1
lema(ur'[Cc]entr_í_fug[ao]s?_i', xpre=[ur'[Ss]e ']) + #1
lema(ur'[Ll]at_í_n_i', pre=ur'(?:[Ee]n|[Ee]l|[Dd]el) ', xpos=[ur' (?:house|amour|Beat|jazz|lover|New|Award|Horror|American|Cinema|Alternative|Tracks|Grammy|script|Songs|Pop|Regional Mexican)']) + #1
lema(ur'[Nn]av_í_os?_i', xpre=[ur'\bdo ', ur'Francisco ', ur'Malo i ', ur'Malo ', ur'Melara '], xpos=[ur' (?:da|e Mariana)\b', ur'[\'\]]']) + #1
lema(ur'[Aa]lmac_é_n_e', xpos=[ur'\]\]es']) + #1
lema(ur'[Ii]ncluy_ó__o', xpre=[ur'[Yy]o ']) + #1
lema(ur'[Aa]not_ó__o', xpre=[ur'\bde \[\[', ur'\bde '], xpos=[ur' (?:\(Col|para que)', ur'\'\'']) + #1
lema(ur'[Tt]r_í_os?_i', pre=ur'(?:[Uu]n|[Dd]os|[Tt]res|[Ee]l|[Ll]os|[Aa]l|[Dd]el) (?:\'+|"|\[\[|)', xpos=[ur' (?:Tournament|amb)']) + #1
lema(ur'[a]tac_ó__o', xpre=[ur'[Yy]o ', ur'\b[Yy] '], xpos=[ur' (?:tiene origen|sobre el río|o Acajutla|significa|pertenecía|perteneció|solicitaron|espinoso|con besos)']) + #1
lema(ur'[m]at_ó__o', xpre=[ur'\b(?:[Ll][eo]|[Ee]l|lu|[Tt]e|[Mm]e|d[eo]) ', ur'horco ', ur'Eugenia ', ur'[Yy]o no ', ur'Esta noche ', ur'pasado y ', ur'Myrcianthes ', ur'\bdel '], xpos=[ur' (?:real|y vuelvo|y aparece|negro|de risa|al hombre|el toro|la idea|que fura|albar|de agua|yo|o no|pollero|para hacerla|gente|hoy|Fortunato|Ikaalisissa|dentro|rendidos)\b', ur'(?:\]\]s|")']) + #1
lema(ur'[Ee]ncarg_ó_ una?_o', xpre=[ur'\bsu ']) + #1
lema(ur'[Dd]istri__tos?_c', xpre=[ur'\b(?:do|no) ']) + #1
lema(ur'[Mm]_u_tu[ao]s?_ú', xpre=[ur'Cable ', ur'Caja ', ur'Agrupació '], xpos=[ur' (?:Escolar|del C|Madrileña|de Granollers|com|General|Universal|Obreros|de Pa)\b']) + #1
lema(ur'_í_ndole_i', xpre=[ur'Dell\'']) + #1
lema(ur'_Í_ndole_I', xpos=[ur' Metabolism']) + #1
lema(ur'[Vv]iol_ó__o', xpre=[ur'Sergio ', ur'[Ss]i no ', ur'[ns]i ']) + #1
lema(ur'[Hh]om_ó_log[ao]s?_o', xpre=[ur'coordina y ', ur'[Qq]ue ', ur'\b(?:[Ss]e|[Nn]o|[Ll][ao]) ', ur'[Ll][ao]s '], xpos=[ur' norma']) + #1
lema(ur'[Ll]_l_amad[ao]s?_', xpos=[ur' Award']) + #1
lema(ur'[Mm]_é_dica_e', xpre=[ur'\b(?:se|et) ', ur'physico ', ur'Questio ', ur'politice ', ur'Citrus ', ur'John ', ur'Excerpta ', ur'Eduardo ', ur'Scuola ', ur'[Aa]rs ', ur'Clio ', ur'Tesis ', ur'Micaria ', ur'Praecepta ', ur'[Mm]ateria ', ur'Mariana Practica ', ur'dottrina ', ur'\be ', ur'Tipula ', ur'\b[Rr]e ', ur'T\. '], xpos=[ur' (?:nell|[Cc]ompleta|Inauguralis|Italo-Argentina|et|nel|facultate|libri|sistens|e dell)\b', ur', Battat']) + #1
lema(ur'[Ee]st_á_[ns]?_à', xpre=[ur'Mercè '], xpos=[ur' (?:fent|al exconvento|em|triomfant|amb|gotjant|ben|per|si bull|envoltada|llenot|enamorat|oberta|el nostre|es Canal|blau|pioc|a|perduda|constituït|clar|mort|relacionada formalement|en (?:dit|crisi|consonància|son|xinès)|ensorrant|malalt|assegurada|mai|embelt|“marginat|damunt|que bossa|sol)\b']) + #1
lema(ur'[Mm]ar_í_tima_i', xpre=[ur'Nicea ', ur'Sueda ', ur'latín\]\] \'\'', ur'\b[ABL]\. ', ur'subsp\. ', ur'ssp\. ', ur'var\. ', ur'var\. \'\'', ur'Prunus\]\] ', ur'912 ', ur'912\) ', ur'Anurida ', ur'Ruppia ', ur'Muilla ', ur'Matricaria ', ur'Diospyros ', ur'Puccinellia ', ur'Armeria ', ur'Missao de Biologia ', ur'Stachys ', ur'Dipsastraea ', ur'Draba ', ur'Drimia ', ur'Glyce ', ur'Scabiosa ', ur'Alnus ', ur'Cleome ', ur'Cicindela ', ur'Lavatera ', ur'[Ss]partina ', ur'Alnus ', ur'Linaria ', ur'Armenia ', ur'lobularia ', ur'Lasaia ', ur'Salsola ', ur'Chenopodina ', ur'Cryptantha ', ur'Octadenia ', ur'Gnaphosa ', ur'Ipomoea ', ur'Silene ', ur'Urginea ', ur'Artemisia ', ur'Abronia ', ur'Anthemis ', ur'Senckenbergiana ', ur'Armeria', ur'Festuca ', ur'pars ', ur'[Ll]oca ', ur'Glaucoides ', ur'Geositta ', ur'Chromodoris ', ur'ditione ', ur'maritima ', ur'Calendula ', ur'Kakile ', ur'Eurybia ', ur'Mertensia ', ur'Calidris ', ur'Strumpfia ', ur'Carex ', ur'Glaux ', ur'Crucianella ', ur'Mammillaria ', ur'[Ss]uaeda ', ur'Suriana ', ur'Hypselodoris ', ur'Suaeda ', ur'Statice ', ur'\b[Oo]ra ', ur'Batis ', ur'Cakile ', ur'Malcolmia ', ur'Remirea ', ur'Crambe ', ur'Lysimachia ', ur'Urginea ', ur'Vignea ', ur'vulgaris ', ur'Strumpfia ', ur'Jacobaea ', ur'Koniga ', ur'Clypeola ', ur'Prunus ', ur'Lobularia ', ur'Plantago ', ur'Caesarea ', ur'Pinus ', ur'[Rr]uppia ', ur'Thermotoga '], xpos=[ur' (?:in|Centrum|reveal|din|Italorum|omnis|uocauit|crudelissime|\(costera|tiene un \[\[periodo)\b', ur'\'\'']) + #1
lema(ur'[Dd]emocr_á_tic[ao]_a', xpre=[ur'dittatore ', ur'Organizzazione ', ur'Editrice ', ur'Convergència ', ur'della teoria ', ur'Esquerra ', ur'istituita la ', ur'Partito Socialista ', ur'Partito ', ur'Sinistra ', ur'Liberalis ', ur'do Movimento '], xpos=[ur' (?:di|in|per|pra|Cinque|Svizzero|Nazionale|Repubblicana|della)\b']) + #1
lema(ur'_t_v_T', pre=ur'de ', xpos=[ur' Azteca']) + #7506
lema(ur'[Mm]_é_danos?_e', xpos=[ur' Alt']) + #1
lema(ur'[Uu]top_í_as?_i', pre=ur'(?:[Ll]as?|[Uu]nas?) ', xpre=[ur'd\'']) + #1
lema(ur'C_anadá__ánada', xpre=[ur'William ', ur'cónsul ']) + #1
lema(ur'[Aa]rt_í_fices?_i', xpre=[ur'Dark ', ur'and ', ur'd[’\']'], xpos=[ur' (?:et|and)']) + #1
lema(ur'[Dd]i_ó_cesis_o', xpre=[ur'in '], xpos=[ur' (?:Hispaniourum|Hispaniarum)']) + #1
lema(ur'[Pp]_í_car[ao]s?_i', xpre=[ur'se '], xpos=[ur' Press']) + #1
lema(ur'[Dd]ar_s_e(?:lo|)_c', xpre=[ur'Benito ']) + #1
lema(ur'[Vv]endi_ó__o', xpos=[ur' y shopkick', ]) + #1
lema(ur'[Ss]obre_ _todo_', xpre=[ur'(?:[Ee]l|[Ss]u|[Uu]n|de) ', ur'\[']) + #1
lema(ur'[H]ispanoam_é_rica_e', xpos=[ur'\]\]n[ao]s?']) + #1
lema(ur'[Pp]ol_íti_c[ao]s?_[ií]t', xpos=[ur'\'']) + #1
lema(ur'[Aa]compañ_ó__o', xpre=[ur'[Tt]e ']) + #1
lema(ur'_ó_ptim[ao]s?_o', xpre=[ur'Ogasawarana '], xpos=[ur' (?:rerum|iure|politia|genere|et)']) + #1
lema(ur'[Aa]gronom_í_as?_i', xpre=[ur'\bdi ', ur'Escola Superior de '], xpos=[ur' \(Puerto Bertoni']) + #1
lema(ur'[Oo]_í_r_i', xpre=[ur'an '], xpos=[ur'(?:\'\'|")', ur' (?:misa los vaqueiros|é librar|y ayudar á misa|misa y dar cebada|17 años|con)']) + #1
lema(ur'[Mm]_í_nimos?_i', xpre=[ur'Canzoniere ', ur'at ', ]) + #2
lema(ur'[Bb]_í_blic[ao]s?_i', xpre=[ur'Napoli, Centro ', ur'Rivista ', ur'Guida ', ur'Biblicum: ', ur'Re ', ur'Incunabula ', ur'possibile itinerario ', ur'interpretazione ', ur'Ichthyologia ', ur'Studia  ', ur'Guida ', ur'Lux ', ur'\bof ', ur'=', ur'l\'opera ', ur'Encyclopedia ', ur'Encyclopaedia '], xpos=[ur' (?:et|alla|negli|della|Britannica|Sacra Vulgatae)', ur'(?:, Vol|: G)\b']) + #132
lema(ur'[Dd]em_ó_cratas?_o', xpre=[ur'EC ', ur'Clube Democrata\|', ur'Aliança Social ', ur'Acção Social ', ur'Clube\|', ur'Clube '], xpos=[ur' (?:FC|EC|Sete|Clube|Cristão|de Governador|Autoritários|Brasileira|\(GV|Futebol|Governador)', ]) + #395
lema(ur'[Ff]r_í_[ao]s_i', xpre=[ur'\bå ', ur'\'É ', ur'\bAs ', ur'\b[Dd]en ', ur'numa ', ur'Janeth ', ur'Janeth Frias ', ur'Octavio ', ur'em águas ', ur'manhanas ', ur'das Aguas ', ur'Araneus ', ur'Nicolau de ', ur'Magdalena de ', ur'Mário ', ur'Oct[aá]vio ', ur'Pés ', ur'boias ', ur'em ', ur'Águas ', ], xpos=[ur' (?:[Kk]onsterna|de Oliveira|Filho|församlingens|Martins|boias|Forcada|\(\[\[Octavio)', ]) + #213
lema(ur'[Ii]b_é_ric[ao]s?_e', xpre=[ur'[ACDHMNR]\. ', ur'cf\. \'\'', ur'var\. ', ur'Federacão ', ur'Luis Iberico\|', ur'[Aa]t Centro ', ur'Aphaenogaster ', ur'Heliswiss ', ur'Nobilis ', ur'Aristolochia ', ur'Euphorbia ', ur'Filosofía ', ur'reunía con ', ur'Quercus ', ur'Trichouropoda ', ur'Contestania ', ur'ciutadella ', ur'Stone ', ur'Belt ', ur'orbicularis ', ur'sylvestris ', ur'Eremostachys ', ur'Enrique ', ur'Berberis ', ur'Luis ', ur'Penisola ', ur'collection ', ur'Penisola ', ur'Gagea ', ur'Chorispora ', ur'Onobrychis ', ur'year ', ur'Nansenia ', ur'Orobanche ', ur'Sintula ', ur'Festuca ', ur'Cataglyphis ', ur'Roncocreagris ', ur'Rhagonycha ', ur'Passio ', ur'Lallemantia ', ur'Neoraja ', ur'Minniza ', ur'Meles ', ur'Iris ', ur'Isatis ', ur'Musica ', ur'Calcitrapa ', ur'Dactylorhiza ', ur'Amphicoma ', ur'Altica ', ur'mellifera ', ur'Meles ', ur'Hippocrepis ', ur'Helicella ', ur'Gypsophila ', ur'Gnaphosa ', ur'Phoenix ', ur'Phyllotreta ', ur'Civilização ', ur'União ', ur'Publishing ', ur'Centaurea ', ur'Epaenesis ', ur'Mycologica ', ur'Mespilus ', ur'Flora ', ur'Tempo ', ur'hiedra ', ur'Religio ', ur'Salsola ', ur'Hedera ', ur'Rana ', ur'itinere ', ur'Cicindela ', ur'Trofeu ', ur'Stipa ', ur'Harlequin ', ur'Concha ', ur'subsp\. ', ur'Magnificentia ', ur'Vox ', ur'mamífero\)\|', ur'Devotio ', ur'Fl\. ', ur'Flora ', ur'Puccinellia ', ], xpos=[ur' (?:ha|do|hahni|e celtico|\((?:mamífero|1942))\b', ur'\'\'']) + #454
lema(ur'[Ff]ilosof_í_as?_i', xpre=[ur'per la ', ur'è la ', ur'\b[ài] ', ur'(?:què|sua) ', ur'\'\'De ', ur'alla ', ur'in \'\'Diccionario de ', ur'morale ', ur'Muratori ', ur'Internazionale de ', ur'Anuario ', ur'Síntese - Revista de ', ur'Scienza, cultura, ', ur'quaderns de ', ur'Quaderns de ', ur'Natura, poesia, ', ur'chimica, ', ur'Revista catalana de ', ur'Societá italiana de ', ur'Pensiero – ', ur'senza ', ur'in "', ur'e la ', ur' [ae] ', ur'Uma ', ur'conceito de ', ur'Facultat de ', ur'Estudos de ', ur'Societat Catalana de ', ur'inurri ', ur'd\'una ', ur'Epistéme: ', ur'Introducció a la ', ur'Faculdade de ', ur'i mites de ', ur'sulla ', ur'nella ', ur'Faculdade Nacional de ', ur' (?:in|da|na|em|di) ', ur'[Dd]ella ', ur'A '], xpos=[ur' (?:d|dos|in|della|degl|cinza|come|contemporanea del Novecento|contemporanea\. Il|pensiero|Regular|del (?:plat|Dret|limite come|judaisme)|Unicase|contemporânea|civile|platònica|De L\'edadt|Moderna e Contemporânea|Criacionista|alabari|delle?|[Dd][aio]|dei|nell|Política do|avui|Frankliliana|politica di|de (?:Catalunya|l\'educació|Kant dos-cents)|no Ceará|e (?:identità|Teologia|fede|patriota|morale|Religione|naturale|politica|Ciencia|pedagogia|pedagogía|filosofia|scienze|Abath|Ciências?|naturale|Metafísica|crítica|storiografia|Quercus|Educação|storia|storia)|i (?:pràctica|cattolica|Lletres|teologia)|a (?:polifonia|Catalunya|la presó))\b', ur'(?:@|\.org|: a polifonia|, (?:[1-9][0-9]+|scienza|Letras e Ciências|teologia, storia)|\. Universidade|: para o\b)']) + #305
lema(ur'[Cc]r_í_tica_i', pre=ur'(?:[Ll]a|[Uu]na|[Ss]u|[Oo]tra|[Dd]ura|[Hh]istoria) ', xpre=[ur'\be ', ur'\bin ', ur'Per ', ur'bien '], xpos=[ur' (?:della?|[Oo]perativa)']) + lema(ur'[Cc]r_í_tica (?:por no descubrirse|positiva|negativa|literaria|discogr[aá]fica)\b_i', xpre=[ur'\bno ', ur'donde ', ur'que ', ur'quien ', ur'pero ']) + #1
lema(ur'[Cc]r_í_ticas_i', xpre=[ur'[Qq]ue ', ur'[Cc]uando ', ur'chronologicas e '], xpos=[ur' tu propia']) + #1
lema(ur'[Gg]an_ó__o', xpre=[ur'G\. ', ur'Calle ', ur'Tara ', ur'Gordon ', ur'Graham ', ur'John ', ur'Maersk ', ur'Zinho ', ur'[Qq]ué ', ur'Nada ', ur'Yo\) ', ur'\b(?:[Yy]o|[Tt]e|[Mm]e) '], xpos=[ur' (?:di|degli|Burbridge|gol|[Yy]o|o me|porque me|Grills|Dunn|porque me)\b', ur'(?:, (?:gana|soy)|’\) o)']) + #657
lema(ur'[Gg]uaran_í__i', xpre=[ur'\* ', ur'\bO ', ur'\bdo ', ur'origem \[\[', ur'Diapoma ', ur'Bothriurus ', ur'Clube Guarani\|', ur'Clube\|', ur'VBTP-MR ', ur'Clube ', ur'Hyphessobrycon ', ], xpos=[ur' (?:EC|FC|Book|Futebol|Award|Sarandi|Esporte|Juazeiro|no coração|de (?:Goiás|Campinas))', ]) + #306
lema(ur'_Amé_rica_(?:am[eé]|Ame)', pre=ur'(?:[Ee]n|[Ee]l|[Aa]unque|[Aa]tl[ée]tico|[Aa]venidas?|[Cc]apit[aá]n|[Cc]entro|[Cc]lub|[Cc]ontinente|[Cc]opa|[Cc]uando|[Ee]l|[Ee]ditorial|[Nn]orte|[Nn]ueva|[Nn]uestra|[Ss]u[dr]|[Tt]oda|a|del|abreviado|con|considerando|descubrir|descubre|descubrió|descubrieron|desde|entonces|entre|hacia|incluso|ni|nombres?|nuestra|o|palabras?|para|por|resultando|siendo|sobre|tanto|que|visitar|y) ', xpre=[ur'Mature en ', ur'citta del ', ], xpos=[ur' (?:TV|Next|huishoudende|SOAP|Coming|Labor|Television|Online|do|RJ|West|East|Bank)', ur'(?:[\'’]s|\'?: The|\.com)', ]) + #168
lema(ur'_Latinoamé_rica_(?:latino ?[Aa]m[eé]|Latino [Aa]m[eé]|Latinoame)') + #1
lema(ur'[Dd]_ú_plex_u', xpre=[ur'tractatus ', ur'Zelotes ', ur'Pakeha ', ur'Shadowy ', ur'TGV ', ur'rubiginosa\'\' \'', ur'argentea ', ur'Coregonus ', ur'Diploplecta ', ur'Japonicum ', ur'Sciaphila ', ur'Pleurothallis ', ur'Vasseuromys ', ur'[Ff]ull ', ur'[Hh]alf ', ur'[Tt]he ', ur'acies ', ], xpos=[ur' (?:acies|Planet|longa|Spacing|hinc|ordo)', ]) + #153
lema(ur'[Mm]elod_í_as?_i', xpre=[ur'C\'è una ', ur'Três ', ur'sulla ', ur'estudio “', ur'\bM\. ', ur'Luiz ', ur'Chorale ', ur'Melospiza ', ur'Stardust ', ur'álbum\)\|', ], xpos=[ur' (?:Tecna|Musik|e Letra|\(álbum)', ur'\'\' \(Diana', ]) + #142
lema(ur'[Bb]_ú_hos?_u', xpre=[ur'Gary ', ur'se al ', ur'Partita de ', ], xpos=[ur' (?:Jolson|Rep)\b', ]) + #113
lema(ur'[Ll]_á_tex_a', xpos=[ur' (?:particle|Hearts|Records|Hindustan|Cult|Diamond|Condoms)', ]) + #112
lema(ur'[Dd]inast_í_as?_i', xpre=[ur'\ba ', ur'della ', ur'di una ', ur'duas ', ur'per una ', ], xpos=[ur' (?:Crew)', ]) + #104
lema(ur'[Gg]_ó_tic[ao]s?_o', xpre=[ur'Don ', ur'sulla Linea ', ur'nell\'aula ', ur'Quaderno ', ur'Missa ', ur'lex ', ], xpos=[ur' usque', ]) + #85
lema(ur'[Cc]_ó_nsul_o', xpre=[ur'Deputy ', ur'AS-65 ', ur'\* ', ur'\b(?:le|as|du) ', ur'first ', ur'Airspeed ', ur'American ', ur'africano de ', ur'nombre \'\'', ur'second ', ur'météo ', ur'río ', ur'Baillie y del ', ur'Embassy ', ur'Acting ', ur'Canopy ', ur'McKinley y ', ur'Dutch ', ur'Ford ', ur'Honorary ', ur'Portuguese ', ur'Premier ', ur'Roman ', ur'[Tt]he ', ur'Alabama\)\|', ur'animal\)\|', ur'cigarrillos\)\|', ur'praetor\'\', \'\'', ur'suffectus ', ], xpos=[ur' (?:in|at|of|IV|venit|[Oo]rdinan?rius|[Oo]rdianrius|[Ss]uffectus|exercitus|designatus|für|junior|suffectuss|General(?:, Consulate|, Embassy| for| and| of)\b|Gallecie|electra|excellens|panariste|fabius|general in|jussit|Capri|tertium|de France|Gen to|[Ss]uffectus|and|fieri|for|General of|franchissant|IV|\((?:animal|cigarrillos|Alabama))\b', ur'(?:@|, Censor, Aedilis|\'\'\' es|\) Smith|\]\] suffectus)', ]) + #1
lema(ur'[Cc]_ó_nsules_o', xpos=[ur' (?:ne|ordinarii|suffecti)\b']) + #182
lema(ur'[Gg]aler_í_as?_i', xpre=[ur' da ', ur'A ', ur'A Cidade, ', ur'Arte ', ur'Duza ', ur'Estación ', ur'Estación Galeria\|', ur'Falerna\]\], \[\[', ur'Fosso ', ur'Gomez ', ur'Museu ', ur'Robinson ', ur'Perez ', ur'Ponte ', ur'Shopping ', ur'Tapeçaria, ', ur'Tribu ', ur'Valeria ', ur'\bdi ', ur'\bfue ', ur'anys de ', ur'das ', ur'das Galerias, ', ur'e Pintura, ', ur'tribu ', ur'tribu \'\'\[\[', ], xpos=[ur' (?:d\'ombres|Carles Taché|nationale|Muro|Spazio|Octagon|Kramy|Joan Prats|Maeght|Fernando Santos|Toni Tàpies|Senda|Maeght|delle|Kombëtare|Sztuki|Kaufhof|Arte Algarve|Romigioli|[Aa]m|de Campions|des|dell|Adelphi|Jacques|Lydia|Iynedjian|Latzer|Suzanne|regia|ebrenca|Chissano|Algarve|Valid|Divulgação|Diário|oberta|Salduba|Mar, Barcelona|El Carme|Terraferma|Augusta, Barcelona|Bertran, Barcelona|Sant Jordi|Anquins|Dário|era|logró|Mokotów|Medicci\.com|Angels|Athenea|Només|Pátio|Fraîch|Uffizi|Biographica|Copiola|Lucilla|Faustina|Valeria|Lamelli|Fundana|Comunale|Lucila|Toni Tàpies|Joan Prats|dos |de (?:Março|Catalans|imagens|retrats|personatges|Metges|La Ligne|Artâ|de Março|Arte do)|degli|dels|[Dd][\'´’] ?(?:[Aa]rt|[Aa]rco|[Aa]rte)|na|d[aiou])\b', ur'(?:[\'\|]|\.com|\]\])', ]) + #102
lema(ur'[Dd]ivid_í_a[ns]?_i', xpre=[ur'[Ee]s ', ur'[Ee]st[aá] ', ur'[Ff]u[eé] ', ur'pois ', ], xpos=[ur' Production', ]) + #5
lema(ur'[Aa]stron_ó_mic[ao]s?_o', xpre=[ur'\'', ur'annulo ', ur'osservatorio ', ur'Praedictio ', ur'Dissertatio ', ur'Hypoaspis ', ur'Osservativa ', ur'Acta ', ur'Manuscripta ', ur'[Oo]sservatorio ', ur'[Dd]e ', ur'[aá]lbum\)\|', ur'disputatio ', ur'exercitatio ', ], xpos=[ur' (?:minora|sine|di|et|e Orto|Betelgeuse|Cortina|\([áa]lbum)\b', ]) + #1
lema(ur'_Ó_mnibus_O', pre=ur'\b(?:y|[Ee]l|[Uu]n|de|en|trenes|Micro|son|transporte:|llamados|formato|tomaran|Empresa|tituló) (?:["\']|\[\[|)', xpos=[ur' (?:Records|Press)']) + #141
lema(ur'[Bb]_ó_vedas?_o', xpre=[ur'Mery ', ur'Apolinario ', ur'Juan ', ], xpos=[ur' Temiño', ur'(?:\]\]d[ao]s?|, \[\[Baamonde)', ]) + #91
lema(ur'[Ll]_á_pidas?_a', xpos=[ur' (?:las|a)\b', ur'\]\]ri[ao]s?']) + #69
lema(ur'[Pp]aradis_í_ac[ao]s?_i', xpre=[ur'X\. ', ur'Sobralia ' ur'pneumatologia ', ur'Cipurao ', ur'Sobralia ', ur'[Mm]usa ', ur'Xyris ', ur'[Mm]usa [x×] ', ]) + #68
lema(ur'[Vv]olc_á_nic[ao]s?_a', xpre=[ur'Viola ', ur'Draba ', ur'Anticlea ', ur'Arrhenophanes ', ur'Bocona ', ur'Liparis ', ur'Malvasia ', ur'Nolana ', ur'Persoonia ', ur'Pozoa ', ur'R\. ', ur'Rapanea ', ur'Triplarina ', ]) + #24
lema(ur'[Cc]arpinter_í_as?_i', xpre=[ur'California\)\|', ur'at ', ], xpos=[ur' (?:offshore|Tar|\(California|Valley|State)', ur', California', ]) + #12
lema(ur'[Cc]arrocer_í_as?_i', xpre=[ur'Comércio de ', ], xpos=[ur' e Ônibus', ]) + #12
lema(ur'[Aa]sisti_ó__o', xpre=[ur'Ynna ', ], xpos=[ur' III', ]) + #9
lema(ur'[Cc]om_í_a[ns]?_i', xpre=[ur'Laiza ', ur'mulher que ', ], xpos=[ur'\]\]', ]) + #8
lema(ur'Brun_é_i_e', xpre=[ur' (?:of|in) ', ur'from ', ur'The ', ur'Shah ', ur'Sungai ', ur'Independent Borneo – ', ur'DBP:', ur'Empayar ', ur'Melayu ', ur'Daerah ', ur'Televisyen ', ur'Teluk ', ur'Concert ', ur'Diraja ', ur'Malaysia, ', ur'Muzium ', ur'Populaire de ', ur'Mahkota ', ur'Royal ', ur'Saru ', ur'School ', ur'Sungei ', ur'for ', ], xpos=[ur' (?:DPMM|Moden|Gallery|Super|Amateur|Yang|Times|Town|History|Shell|Museum|Rock|Investment|Project|Princess|Business|Beauty|People|Premier|Darussalam|- List)', ur': The']) + #431
lema(ur'Canad_á_ *,_a', xpre=[ur'Health ', ur'Martin ', ur'Aircraft ', ur'Roe ', ur'Siddeley ', ur'Havilland ', ur'Avro ', ur'Western ', ur'UK, ', ur'Development ', ur'Skate ', ur'Exposing ', ur'Bell ', ur'Primus ', ur'Rommel ', ur'Par[ck]s ', ur'Music ', ur'Hello! ', ur'\bO ', ur'\b(?:[Oo]f|[Dd]u|[Tt]o|[Ii]n) ', ur'\bfor ', ur'in Toronto, ', ur'Statistics ', ur'Team ', ur'Blame ', ur'Resources ', ur'Child ', ur'Don Mills Ontario ', ur'Education ', ur'Arctic ', ur'Indiangrass - ', ur'Intuit ' ur'Statistics ', ur'Marport ', ur'Environment ', ur'Agriculture ', ur'Air ', ur'Bechtel ', ur'Intuit ', ur'Horizon ', ur'Press ', ur'Woolworth ', ur'Shell ', ur'BP ', ur'against ', ur'Transport ', ], xpos=[ur' (?:we|UK|Geoffrey|Golf|Inc\.|EL Nicholls|Museum|architects|Journal|and|Latin America|Russia|Bibliothèque|Hochelaga|ISL-1129|7E-2008)']) + #1453
lema(ur'Canad_á__a', pre=ur'\b(?:[Dd]e|[Ee]n|y) ', xpre=[ur'W\. ', ur'Education ', ur'Statistics ', ur'Dominion ', ur'[Mm]unicipio ', ur'[Rr]ivière ', ], xpos=[ur' (?:Fed|EIC|Basketball|Dept|Packers|Bread|Water|State|Soccer|Dry)', ur'(?:\.[Cc]om|\'s|,)', ]) + #70
lema(ur'Dom_í_nguez_i', xpre=[ur'P ', ur'R\.; ', ur'P\. ', ur'Eléonore ', ur'd\'Oscar ', ur'Patrice Dominguez\|', ur'Patrice ', ur'Patrick ', ], xpos=[ur' Hills', ]) + #1105
lema(ur'Hern_á_ndez_a', xpre=[ur'\bby ', ur'over ', ur'Ferreyra ', ur'Feuntes ', ur'Patrick ', ur'Joe ', ur'Cole ', ur'Laurie ', ur'Jason ', ur'Gérard '], xpos=[ur' (?:High|Satyricon|es actualmente)', ur', Kelly']) + #1
lema(ur'M_é_ndez_e') + #1
lema(ur'P_á_ez_a') + #1
lema(ur'Rold_á_n_a') + #1
lema(ur'Jerusal_é_n_e', xpre=[ur'frayre a ', ur'Hapoel ']) + #139 
lema(ur'Ju_á_rez_a', xpre=[ur'the Sierra de ', ur'\bof ', ], xpos=[ur' (?:do|et|City|Fuel|Murders|Elementary|Távora|Hidden|\((?:Texas|canción)|Community)\b', ur'\]', ]) + #412
lema(ur'Mart_í_n_i', pre=ur'San ', xpre=[ur'\bof ', ur'the ', ur'Ameskoako ', ur'and ', ur'2745\) '], xpos=[ur' (?:Came|[Ii]n|et|Txiki|Station|\(California)', ur'\'s', ur', California', ]) + #569
lema(ur'Mazatl_á_n_a', xpos=[ur' Times', ur': Sea', ]) + #28
lema(ur'Tur_í_n_i', xpre=[ur'Gentilhombre '], xpos=[ur' Ferroviaire']) + #28
lema(ur'Mil_á_n_a', pre=ur'(?:[Dd]e|[Ee]n) ', xpre=[ur'amor ', ur'nombre ', ur'político ', ur'muerte ', ur'marcha ', ur'favor ', ur'africain ', ur'esposa ', ur'Maître ', ur'Africain ', ur'Dame ', ur'politiques ', ur'aldea ', ur'amante ', ur'padre ', ur'favor ', ur'Passage ', ur'Internazionale ', ur'Bâton de Jean ', ur'Pico ', ur'personas residiendo ', ur'Princesse ', ur'Jefa ', ur'Naturale ', ur'Scala ', ur'Valentine ', ur'[Mm]unicipio ', ur'l\'Etat ', ], xpos=[ur' (?:\(fue mucho|Trenc|Gurovic|oeste|Football|Piqué|Stojadinović|Ivelic|Vidmar|Knížák|Ciganović|Lalkovič|Janković|Studios|Kadlec|Kosovac|Bandić|Gorkić|Bisevac|Turkovic|[Dd]i|Kundera|Melvin|Begović)', ]) + #261
lema(ur'Neuqu_é_n_e', xpre=[ur'7'], xpos=[ur' Trabvun']) + #1
lema(ur'Guzm_á_n_a', xpre=[ur'Roderici de '], xpos=[ur' audience']) + #1
lema(ur'P_é_rez_e', xpre=[ur'E\. ', ur'Of ', ur'née ', ur'Ellen ', ur'Vivancos ', ur'Rosie ', ur'Abe ', ur'Maurice ', ur'Moshe ', ur'Erickson y ', ur'Vincent ', ur'Lindsey ', ur'Guillo '], xpos=[ur' (?:Hilton|National|Companc Family|Family|Elementary|–se refiere)']) + #1
lema(ur'Guti_é_rrez_e', xpre=[ur'Rocky '], xpos=[ur' as\b']) + #1
lema(ur'M_á_rquez_a', xpre=[ur'Texas\)\|'], xpos=[ur' \(Texas']) + #1
lema(ur'Panam_á__a', pre=ur'(?:[Dd]e|[Ee]n) ', xpre=[ur'(?:[Dd]u|[Ll]e) [Cc]anal ', ur'histoire ', ur'Congrès ', ur'histoire ' ur'personaje de ', ur'Pionnier ', ur'[Ii]nterocéanique ', ur'[Ii]sthme ', ur'[Ii]sthmes ', ], xpos=[ur' (?:\([Cc]ondado|Talents|Papers|Smith|Railroad|Music|Hat|City)', ur'\.svg']) + #100
lema(ur'Rodr_í_guez_i', xpre=[ur'and ', ur'Claudinei ', ur'Jayson ', ur'Benjamin ', ur'Robert ', ur'Michelle '], xpos=[ur'(?:, G\.|, Carvallaro|\|2012)', ur' (?:Buron|International)']) + #1
lema(ur'Taip_é_i_e', pre=ur'(?:[Dd]e|[Ee]n) ', xpos=[ur' City']) + #169
lema(ur'V_á_squez_a', xpre=[ur'Junior ', ur'Jhonen ', ur'and Mario ']) + #1
lema(ur'[Aa]_é_re[ao]s?_e', xpre=[ur'L\'', ur'vascello ', ur'Societá ', ur'illeggibili\'\' - ', ur'Divisione ', ur'Chaetomorpha ', ur'Macchina ', ur'Forca ', ur'tabula ', ur'tabu\[la ', ur'tabul\(a\) ', ur'Allagrapha ', ur'Atitara ', ur'Babilonia ', ur'Brigata ', ur'Compagnia ', ur'Corpo ', ur'Dicladispa ', ur'Excoecaria ', ur'Navigazione ', ur'Noctua ', ur'Peperomia ', ur'Quercus ', ur'Salvia ', ur'Società ', ur'Società Incremento Tur[ií]stico ', ur'Svenska ', ur'Temnoscheila ', ur'[AT]\. ', ur'[Ll]inhas ', ur'architettura ', ur'dall\'', ur'navigazione ', ur'var\. ', ur'vulcanetto ', ], xpos=[ur' (?:di |in |quae|dell|Teseo|magnifica|Carabinieri|Negrot|del Decennale)', ur'(?:\. Conoscere|\'\' Urquhart)', ]) + #430
lema(ur'[Aa]bad_í_as?_i', xpre=[ur'\bA\. ', ur'\bna ', ur'Guy ', ur'Francolí: ', ur'Bock ', ur'C\. ', ur'Capella de la ', ur'Editor ', ur'Escolania de la ', ur'Herney ', ur'Lourdes ', ur'Maria ', ur'Natale ', ur'[DdLl][´’\']', ], xpos=[ur' (?:dos|de (?:Nossa|Mont?serrat|Goiás))', ]) + #115
lema(ur'[Aa]burr_í__i', xpre=[ur'Aburria ', ]) + #4
lema(ur'[Aa]di_ó_s_o', xpre=[ur'Vaarwel, ', ur'nombre de \'\''], xpos=[ur' (?:alligator|\|\|)', ur'\'+ (?:es|fue)\b']) + #1
lema(ur'[Aa]gon_í_as?_i', xpre=[ur'\b(?:da|by) ', ur'Dolce ', ur'Theresa ', ur'Crisi e ', ur'l\''], xpos=[ur' (?:de (?:Llum|l\'home)|dels|Records|la dels)', ur'(?:\'\' en catalán|<br/>Deathstrike|, 2004)']) + #1
lema(ur'[a]gr_í_colas?_i', xpre=[ur'[AHOo]\. ', ur'calcaratus ', ur'ricerca ', ur'thraso ', ur'Coccospora ', ur'Gecarcinus ', ur'Heliophanus ', ur'Ochlodes ', ur'Acrocephalus ']) + #1
lema(ur'[Aa]legor_í_as?_i', xpre=[ur' da ', ur' e ', ], xpos=[ur' (?:da |Moral|al Paraná|Polski)', ur', Warszaw', ]) + #31
lema(ur'[Aa]legr_í_as?_i', xpre=[ur'Un ', ur'Ter ', ur'Muita ', ur'Paguristes ', ur'Lautaro ', ur'So ', ur'Eqüestre ', ur'Chã de ', ur'minha ', ur'Epipactis.. ', ur' da ', ur' [eé] ', ur'[Ll][’\']', ur'Provavelmente ', ur'Alegria, ', ur'Cartola\)\|', ur'Ousadia & ', ur'Outras ', ur'A '], xpos=[ur' (?:i|Productions|do|Ao|de viure|de Viver|e Ternura|Cristā|É Viver|minha|que passa|\(canção)\b', ur'(?:[\'´]s|, Alegria|’s)']) + #1
lema(ur'[Aa]mar_á__a', pre=ur'(?:[MmTt]e|[Nn]os) ', xpre=[ur'dejar que ', ur'Si ella ']) + #1
lema(ur'[Aa]nt_á_rtic[ao]s?_a', xpre=[ur'Nothofagus ', ur'Dicksonia ', ur'Ginkgoites ', ur'Vesperal ']) + #1
lema(ur'[Aa]ntolog_í_as?_i', xpre=[ur'\be ', ur'\bna ', ur'\be vividos - ', ur'inquietants\. ', ur'Cançó. ', ur'vacants\. ', ur'Un\'', ur'L\'', ur'etsiko\. ', ur'cançó\. ', ur'Pierwsza ', ur'Palavras: ', ur'rua\. ', ur'Possibles, II \(', ur'Possibles, I \(', ur'Crew - ', ur'Nova ', ur'il\'', ur'II - ', ur'Ionios ', ur'Grande ', ur'Petita ', ur'Nuova ', ur'uma ', ur'celobert\. ', ur'literaturaren ', ur'Gacitúa ', ur'adversos: ', ur'Poesiaren ', ur'Klasikoen ', ur'adolescência: ', ur'beltzaren ', ur'continu : una ', ur'd[\'’]', ur'perduto\. ', ur'ride ', ], xpos=[ur' (?:até|sonora della|Poetica 1971-1998|[Pp]oètica|[Pp]oética(?:\'\'\. Belo| - selecção|\'\' - Porto|\'\' \(1962|\'\' \[\[1963|\'\' - Editora do|\'\' \(nova)|\'\', Barcelona, Edicions|\+ 3 inediti|dos|nos|Musicale|italiana per|della|degli|de (?:Trovadores|II Poetas do|Pedro Velho|joves|literatures|poetów|poemes|la poesía alemanya|10 anys|poemas dos|poetica dedicata|poesia universitária|poesia do século|Contos|poetes|Cants|l[\'’])|d[aio]|d\'un|del grande|dalle|dei|dos|bat|dels|\(Recopilatorio|general de la poesia catalana\'\', Edicions|74-99|comentada de literatura brasileira|i collecció|post-junghiana|kabaretu|Contemporânea|luso-brasileira|poezji|poeziei|poetek|polskiej|Poética|internazionale|storico|pessoal|privata|opowiadań|bachiczna|Pessoal|Festivalului|scritti|Catalana|del nou|de (?:la nova|poesía portuguesa erótica e|poetica dedicata|Poetas Brasileiros)|e storia|\'\'Een)', ]) + #297
lema(ur'[Aa]polog_í_as?_i', xpre=[ur'[Ll]\'', ur'Zweyte ', ur'regibus ', ur'romani ', ], xpos=[ur' (?:dels|and|[Aa]dversus|contra Arianos|de Adeserenda|de tribus locis quos|del tomo|dell|della|dictorum|chirurgica|doctae|e Cidadania|fratrum|i vindicació|satisfacció|Sichardi|sobre la cabeza|Socratis|oder|monasticae|per|(?:in|ad|di|by|of) |[Pp]ro (?:Fide|Galeno|Iudaeis|Marcel|Philippo|Renato|Galileo, mathematico|[Vv]ita))', ur'[\'\]]']) + #87
lema(ur'[Aa]rm_ó_nicas?_o', xpre=[ur'Cassa ', ur'Dwarkin ', ur'Guida ', ur'Stagione ', ur'Tromba ', ur'dell\' arte ', ur'staffetta ', ur'un\'', ], xpos=[ur' (?:Institutione|costruzione|exultatio|Sinfonie|Blues|& Seraphim)', ]) + #18
lema(ur'[Aa]rmon_í_as?_i', xpre=[ur'Gruppo ', ur'\be ', ur'\bdi ', ur'[LlDd][´’\']', ur'MSC \'\'', ur'Logia ', ur'MSC ', ur'Recondita ', ur'dell[´’\']', ur'dell[´’\'] ', ur'ed ', ur'bon ', ur'principessa ', ], xpos=[ur' (?:dell|Beyondormason|d’Italia|dulcissime|Egara|F\.C\.|Favellare|Justin|per|sacra di|Somers|Valahă|Vivente)\b', ur'(?:\.info|1019fm)']) + #133
lema(ur'[Aa]rtr_ó_pod[ao]s?_o', xpre=[ur'los ', ]) + #17
lema(ur'[Aa]si_á_tica_a', xpre=[ur'[ABCeGHhLMOPRrSTZ]\. ', ur'formas \'\'', ur'subespecie \'\'', ur'Hoplolabis ', ur'Anthopleura ', ur'Austrolimnophila ', ur'Anoxia ', ur'Isoetes ', ur'Solpugella ', ur' var\. \'\'', ur'Achillea ', ur'Acrolepia ', ur'Actaea ', ur'Adlumia ', ur'Agrimonia ', ur'Amelanchier ', ur'Amphipoea ', ur'Andrena ', ur'Annona ', ur'Antiphylla ', ur'Barringtonia ', ur'Bevanda ', ur'Bryolichenologica ', ur'Buddleja ', ur'Bulbine ', ur'Centella ', ur'Centrolepis ', ur'Cetonia ', ur'Channa ', ur'Cholera ', ur'Chrysochloris ', ur'Chrysocloris ', ur'Cicindela ', ur'Colubrina ', ur'Colubrina\]\] ', ur'Coscinida ', ur'Crantzia ', ur'Cuviera ', ur'Cymodocea ', ur'Cyprianthe ', ur'Digitivalva ', ur'Dysdera ', ur'Encyclopaedia ', ur'Eomerope ', ur'Eremogone ', ur'Epigaea ', ur'Euphydryas ', ur'Fagus ', ur'Galenia ', ur'Garnotia ', ur'Gmelina ', ur'Golshanichthys ', ur'Grewia ', ur'Hanabusaya ', ur'Hemicordulia ', ur'Hoplolabis ' ur'Hepatica ', ur'Hersilia ', ur'Hilaira ', ur'Hitobia ', ur'Hydrocotyle ', ur'Ischnura ', ur'Isoperla ', ur'Itineria ', ur'Keumkangsania ', ur'Laetesia ', ur'Lechytia ', ur'Lycosa ', ur'Macaroeris ', ur'Malus ', ur'Mammea ', ur'Malouetia ', ur'Manotes ', ur'Megachile ', ur'Megalaima ', ur'Melanophthalma ', ur'Mentha ', ur'Monolepis ', ur'Monsonia ', ur'Morisonia ', ur'Musée ', ur'Nectarinia ', ur'Oparba ', ur'Ornitrophe ', ur'Osmunda ', ur'Parasteatoda ', ur'Padus ', ur'Parasyrisca ', ur'Perdicula ', ur'Plantago ', ur'Prunella ', ur'Pseudiosma ', ur'Rana ', ur'Rivetina ', ur'Sakaina ', ur'Saxifraga ', ur'Scyloxes ', ur'Sida ', ur'Setaria ', ur'Sillago ', ur'Spirochaeta ', ur'Striga ', ur'Symphyandra ', ur'Tarenna ', ur'Teilhardina ', ur'Tetracera ', ur'Toddalia ', ur'Torenia ', ur'Triglochin ', ur'Vallisneria ', ur'Zala ', ur'Zenaida ', ur'Zostera ', ur'asiatica ', ur'europaea ', ur'società ', ur'ssp\. ', ur'ssp\. \'\'', ur'subsp\. ', ur'var\'\'\'\. \'\'\'\'\'', ur'var\. ', ], xpos=[ur', vol\. 6', ur' (?:Film Mediale|Barringtonia|equitatu)', ]) + #19
lema(ur'[Aa]stronom_í_as?_i', xpre=[ur'\be ', ur'(?:De|di) ', ur'[DdLl][’\']', ur'Mathematici de ', ur'1154\) ', ur'llibre de la ', ur'rotunda\|', ur'sua ', ur'Prodromus ', ur'dell\'', ur'della ', ], xpos=[ur' (?:alla|lunaris|[Nn]ova|e Ciencias|del rei|des|Esperanto-Klubo|reformata|2014 \[Gratis)', ur'(?:\.net|, Geofísica e Ciências|[0-9])']) + #88
lema(ur'[Aa]t_ó_mic[ao]s?_o', xpre=[ur'\be ', ur'Fizica ', ur'Desyello ', ur'Zanzara ', ur'formica ', ur'rubammo la bomba ', ur'vis ', ], xpos=[ur' (?:e altri|and|cinese|Patibulo)', ur'\]', ]) + #22
lema(ur'[Aa]ut_ó_cton[ao]s?_o', xpos=[ur' per', ]) + #28
lema(ur'[Aa]ut_ó_grafos?_o', xpre=[ur'dell[\'’]', ur'di un ', ]) + #39
lema(ur'[Bb]_í_ceps_i', xpre=[ur'N\. ', ur'Math\. ', ur'Paikiniana ', ur'Pelecopsis ', ur'[Bb]rachii ', ur'Pseudanabaena ', ur'Pseuderanthemum ', ur'Athyreus ', ur'Acianthera ', ur'Neoathyreus ', ur'Eupatorium ', ur'Mathesis ', ur'Tiso '], xpos=[ur' (?:slicer|femoris|Brachii)']) + #101
lema(ur'[Bb]ah_í_as?_i', xpre=[ur'M\.', ur'\bà ', ur'\b(?:[Dd]a|of|na|in|EC) ', ur'Reece ', ur'candomblé de ', ur'Xisto ', ur'Grass\. ', ur'Mesosemia ', ur'Bradypus torquatus \(', ur'Clube ', ur'Diamantina, ', ur'Henrique from ', ur'Meca de ', ur'Metazygia ', ur'Vitória ', ur'Taça Estado de ', ur'Mucugê, ', ur'Neoregelia ', ur'Palais de la ', ur'Southern ', ur'Una, ', ur'da Catarina, Jeremoabo, ', ur'da Jacobina, ', ur'floresta urbano, Salvador, ', ur'from ', ur'no Município de Conde, ', ur'no Parque Metropolitano de Pituaçu, Salvador, ', ur'1995 - ', ur'Clube Bahia\|', ur'no munícipio de Alagoinhas, ', ur'southern ', ur'Produções '], xpos=[ur' (?:in|dos|Plant|Railway|Mouhtassine|Mix|Championship|ambrosioides|bint|Basket|de (?:Todos os|Feira|outrora)|\(1865|Commitee)\b', ur'(?:\]\]|\'|, (?:Imagens|Boa)|: (?:informações|Imprensa))', ]) + #147
lema(ur'[Bb]amb_ú__u', xpre=[ur'Green ', ur'Pristimantis ', ur'balam '], xpos=[ur'\'']) + #1
lema(ur'[Bb]ibliograf_í_a_i', xpre=[ur'\b[ei] ', ur'\bdi ', ur'\be la ', ur'Català de ', ur'in \'\'', ur'de la Llengua ', ur'Txillardegiren ', ur'Ensaios de ', ur'Indro Montanelli\. ', ur'locale, ', ur'Pequena ', ur'Seminari de ', ur'assaig de ', ur'della ', ur'di una ', ur'omosessuale\. ', ur'per \'', ur'uma ', ur'universala ', ], xpos=[ur' (?:dell|analitica ragionata|Botânica|militare|de la Llengua|de fra|botanica ossia|botanica della|de Botânica|de botanica 3|catalana cap a|\|Vlahov|critica \(1916-1963|su|i discografía|intellettuale|Medical de Catalunya|interdisciplinària|ragionata|bàsica|sullo|intellettuale|Literatury|italiana degli|cronologica della|Naukowa|Maria da Penha|d[ai]|dell[ae]|degli|e Informazione|verghiana|storico)\b', ]) + #106
lema(ur'[Bb]iling_ü_e_u', xpre=[ur'revue ', ur'Edition ' ur'Anthologie ', ur'édition '], xpos=[ur' in\b']) + #46
lema(ur'[Bb]iolog_í_as?_i', xpre=[ur'\bi ', ur'\b[Dd][aei] ', ur'obsevaçaões de campo sobre la ', ur'obsevaçaões de laboratorio sobre la ', ur'per la ', ur'Senckenbergiana ', ur'Estação de ', ur'Copernici ', ur'Naukowego ', ur'Médio - ', ur'ensino de ', ur'Mecànica estadística y ', ur'Brasileira de ', ur'Encontro de ', ur'subspecies\. ', ur'\b(?:du|em) ', ur'Nordestina de ', ur'do Instituto de ', ur'mensile '], xpos=[ur'(?:\.org|\.unipi|\.edu|, (?:phytologia|Departamento de Botânica)|: an|\')', ur' (?:e|of|da|in|do|em|dei|cent\.|centrali|kaj|reprodutiva e interações|II: podręcznik|Gabonica|kl\.1|Rovid|Animal e Vegetal|Generalis|Mello|[Ff]loral e|an|ecologia|Centrali|fiorale|Plantarum|applicata|[Dd]efinition|Nomenklaturo|Centrali-Americana|delle|vegetale|floral da|ambientale|\((?:Bratislava|\[\[Lahore)|e (?:taxonom[ií]a|antropologia|medicina|morfologia))\b']) + #554
lema(ur'[Bb]orb_ó_nic[ao]s?_o', xpre=[ur'Euphorbia ', ur'Agelena ', ur'Watsonia ', ur'Parnara ', ur'Pamphila ', ur'Hesperia ', ur'Borbo ', ur'borbonica ', ur'Gazella ', ur'Hirundo ', ur'Phedina ', ur'Uniola ', ur'[Pb]\. ', ]) + #124
lema(ur'[Bb]rit_á_nic[ao]s?_a', xpre=[ur'B\. ', ur'Androsace ', ur'Britannia ', ur'Flora ', ur'Encyclopædia ']) + #268
lema(ur'[Cc]_á_rcel(?:es|)_a', xpre=[ur'Fran ', ur'Guillaume ', ur'[Cc]alle '], xpos=[ur' delle']) + #1
lema(ur'[Cc]_í_vic[ao]s?_i', xpre=[ur'Dictyna ', ur'Galleria ', ur'Doroteo ', ur'Senso ', ur'Arena ', ur'[Mm]useum ', ur'Pinacoteca ', ur'Lista ', ur'Museo ', ur'e Humanismo '], xpos=[ur' (?:d\'|[Mm]useo|Orto|Istituto|uniti|Storico|di|Raccolta|Planetario)\b', ur', Bologna']) + #793
lema(ur'[Cc]_ó_leras?_o', xpre=[ur'\bdal ', ur'\bRem ', ur'[Ii]l ', ur'Mendiri y ', ur'Quirze de ', ur'Quirico de ', ur'Estación de ', ur'Colera\|', ur'Boned ', ur'\| \[\[', ur'\| '], xpos=[ur' (?:Jiménez|Morbo|[Mm]orbus|· \'\'\'Portbou)', ur'(?:\]\](?:,| y) \[\[Portbou|\]\] cercano)', ]) + #168
lema(ur'[Cc]_ó_mic(?:as?|o)_o', xpre=[ur'\b(?:de|at) ', ur'Absurda ', ur'Theatro ', ur'ricreatione ', ur'Discoides ', ur'Scena ', ur'Stelis ', ur'di un ', ur'nasce un ', ur'Il Poeta '], xpos=[ur' (?:Valkyrie|caduto|spettacolo|Comics)\b', ur'(?:[0-9:\]\']|\.jp)']) + #1
lema(ur'[Cc]_ó_mics?_o', pre=ur'\b(?:[Uu]n|[Ee]l|[Ll]os|de|en) ', xpos=[ur' (?:Relief|books?|Earth|News|Bulletin|[Cc]on|Vine|Book|Strip|Buyer|Code)', ur'\.com']) + #384
lema(ur'[Cc]anciller_í_as?_i', xpre=[ur'documents de la '], xpos=[ur'\.go[bv]']) + #16
lema(ur'[Cc]arn_í_vora_i', xpre=[ur'[Oo]rden ', ur'Orden: ', ur'Orden \'\'', ur'Category:', ur'Order ', ur'\[', ur'Anexo:', ur'Union: ', ur'edición de ', ur'Orden '], xpos=[ur' (?:==|Dracunivora)', ur' and', ur'(?:: Canidae|\'\'\'\|y \[\[Miacoidea|, (?:Fissipedia|Ursidae))']) + #1
lema(ur'[Cc]artograf_í_as?_i', xpre=[ur'és la '], xpos=[ur' (?:da|dell|fitoclimatica dell|medievale|de Barcelona, del segle)\b', ur'\]\]da']) + #16
lema(ur'[Cc]ategor_í_as?_i', xpre=[ur'et ', ur'it:', ur'Plantilla:', ur'[Pp]rima ', ur'demais ', ur'[Ss]econda ', ur'[Tt]erza ', ur'nella ', ur'per la ', ], xpos=[ur' (?:del Championat|Inovação|y Perihermeneias|Prima|Canção)', ]) + #520
lema(ur'[Cc]er_á_mic[ao]s?_a', xpre=[ur'della ', ur'Società ', ur'\'Arte '], xpos=[ur' (?:Flaminia|Pagnossin|Panaria|egizia)']) + #483
lema(ur'[Cc]inematogr_á_fic[ao]s?_a', xpre=[ur'[\'’]Arte ', ur'\b[Dd]i ', ur'Coralta ', ur'Clesi ', ur'Clodio ', ur'Compagnia ', ur'Corriere ', ur'Generale ', ur'Intercontinentale ', ur'Italonegglio ', ur'City\|', ur'Laurentiis ', ur'Melampo ', ur'Noleggio ', ur'Ponti\]\] ', ur'Tiger ', ur'Unione ', ur'Unione ', ur'Vides ', ur'Vita ', ur'di Critica ', ur'recitazione ', ur'scena ', ], xpos=[ur' (?:di |Titanus Produzione|Roma|Associati|con Citto|Internazionale|Associata|\(ita)', ]) + #34
lema(ur'[Cc]olibr_í__i', xpre=[ur'[Ll]e ', ur'EC 120 ', ur'Publishers ', ur'Lisboa, ', ur'EC120 ', ur'Edições ', ur'Elettronica ', ur'Lisboa: ', ], xpos=[ur' (?:delphinae|thalassinus|coruscans|serrirostris)', ur'(?:\.cult|\]\]\'\')']) + #262
lema(ur'[Cc]omit_é_s?_e', xpre=[ur'suum ', ur'Petty ', ur'Carlo ', ur'illorum ', ur'Poncius ', ur'illo ', ur'illustrissimo ', ur'Petro ', ur'System ', ur'maior inter '], xpos=[ur' (?:de (?:Acção|Patronage)|a Lamberg|cyanotus|iniuste|Hohenburc|Dei|civitatis|domesticorum|rei|limitis|Musco|Raimundus|Dre|Carolo|Auriliacensis|Maritime|Eberhardo|Nunu|Carpensi|filius|Guttier|Gundissalbo|Garsia|Assur|Lope|Permanent|\[\[Sagittarii|Alsatienses|de Ottingen|et|in)\b', ur'\'']) + #1
lema(ur'[Cc]ompañ_í_as?_i', xpos=[ur' (?:Franco-Română|Brasileira)', ur'\.com']) + #256
lema(ur'[Cc]ontempor_á_ne[ao]s?_a', xpre=[ur'\bil ', ur'\'Italia ', ur'Spagna ', ur'spagnola ', ur'racconto ', ur'età ', ur'di Arte ', ur'd\' Arte ', ur'[Dd]isegno ', ur'Ponte ', ur'Spagna ', ur'Ebraica ', ur'Orchestra ', ur'nella cultura ', ur'centre de arte ', ur'sociale ', ur'letteratura italiana ', ur'Letteratura italiana ', ur'letteratura ', ur'e politico italiano ', ur'dell\'epica ', ur'Internazionale Musica ', ur'\be arte ', ur'realtà ', ur'[Ss]pagnolo ', ur'in \'\'Italia ', ur'basca ', ur'ecuadoriana ', ur'messicana ', ur'Collezione Teatro italiano ', ur'Il ', ur'all\'epoca ', ur'città ', ur'l[\'’]architettura ', ur'seus ', ur'etá ', ur'di poesia europea ', ur'della poesia argentina ', ur'Fenice ', ur'Gioiello Italiano ', ur'Ars ', ur'di Musica ', ur'[dl][´’\'][Aa]rte ', ur' e ', ur'voce ', ur'musicale ', ur'Storia ', ur'e filosofia ', ur'da poesia moderna ', ur'dell\'ideologia ', ur'nell\'arte '], xpos=[ur' di ', ur'(?:, recensioni|\. Tesi)']) + #410
lema(ur'[Cc]r_á_ter_a', xpre=[ur'\ba ', ur'The ', ur'Barringer ', ur'Eagle ', ur'Roden ', ur'Turbinaria ', ur'Punchbowl ', ur'Meteor ', ur'Talebheim ', ur'Meteorite ', ur'Molten ', ur'Sedan ', ur'Pico ', ur'Pit ', ur'Gas ', ur'Face ', ur'Corvus y ', ur'Impact ', ur'\bof ', ur'Impact ', ur'constelación\)\|', ur'Sunset ', ur'Nesta '], xpos=[ur' (?:of|in|and|Crawl|Observation|Lakes|structure|Lake|Festival|\(constelación|lake)\b']) + #687
lema(ur'[Cc]r_ó_nicas?_o', xpre=[ur'les ', ur'[Tt]he ', ur'Nova ', ur'Imperiale ', ur'conocido: \'\'', ur'Nuova ', ur'vitta ', ur'[0-9]'], xpos=[ur' (?:d|d[io]|Alberici|Imperiale|del muy esclarecido|Xeral|moravurilor|cercetărilor|Hugonis|Bălenilor|Universale|Română|Hungarorum|ante aduentum|de (?:Vent-li-Bufa|Wallia)|Actitatorum|Slavorum|unui|Adefonsi|Funk|troiana|geral)\b', ur'(?:\.cl|\'\' con la)']) + #536
lema(ur'[Dd]_ó_cil_o', xpos=[ur' by\b', ]) + #6
lema(ur'[Dd]esaf_í_os_i', xpre=[ur'\b[Ee] ', ur'\bdos ', ur'novos ', ur'sete ', ], xpos=[ur' (?:para um|para a conservação|para Conservação|brasileiros|e (?:perspectivas|falácias)|d[ao] |de uma|dos)', ]) + #12
lema(ur'[Dd]iplom_á_tic[ao]s?_a', xpre=[ur'\b(?:re|il) ', ur'\bres ', ur'storico ', ur'Corpo ', ], xpos=[ur' (?:di|nunc)\b']) + #192
lema(ur'[Dd]istra_í_(?:a[ns]?|d[ao]s?)_i', xpos=[ur'\.(?:com|org)', ]) + #9
lema(ur'[Dd]om_é_stic(?:as|os?)_e', xpre=[ur'Anthony ', ur'Vincenzo ', ur'Enzo ', ur'[Ii]l ', ur'[Ss]e '], xpos=[ur' (?:Kabregu|las plantas)']) + #1
lema(ur'[Dd]om_é_stica_e', xpre=[ur'\[\[', ur'\bet ', ur'que ', ur'\b(?:hac|est) ', ur'\b[Ss]e ', ur'[IMNPsT]\. ', ur'\b[Ll]as ', ur'Brueelia ', ur'canaria ', ur'Catappa ', ur'Violenza ', ur'Channel ', ur'Cariniana ', ur'Curcuma ', ur'Cormus ', ur'Eugenia ', ur'Ilex ', ur'Iris ', ur'Jambosa ', ur'Kua ', ur'livia ', ur'Musca ', ur'Malus ', ur'Monodelphis ', ur'moschata ', ur'Nandina ', ur'Prunus ', ur'Pyrus ', ur'striata ', ur'scrofa ', ur'[Ss]orbus ', ur'Sus ', ur'Spermophora ', ur'Tegenaria ', ur'Thermobia '], xpos=[ur' (?:las|algun[ao]s|×|var)\b', ur'(?:\'|, or)']) + #1
lema(ur'[Ee]col_ó_gic[ao]s?_o', xpre=[ur'Estação ', ur'Acta ', ur'Amblyothele ', ur'Estaçao ', ur'rivoluzione ', ], xpos=[ur' (?:do |Micologico Abruzzese|Gazeta de Alagoas|svizra|contro|e (?:democrazia|consumo))', ]) + #25
lema(ur'[Ee]colog_í_as?_i', xpre=[ur'[Ll]\'', ur'\b[ei] ', ur'\b(?:ed|em) ', ur'Sociedade Portuguesa de ', ur'obsevaçaões de campo sobre la biologia ', ur'Odum\. \'\'', ur'Globo ', ur'obsevaçaões de laboratorio sobre la biologia ', ur'Congresso de ', ur'Congresso Internacional de ',], xpos=[ur' (?:d[ao]|della|Aquática|del paesaggio|a fumetti|e (?:genética|Aplicação|controle|Libertà|Flora|distribuzione|conservação)|Vegetal: integrando ecossistema)\b', ur', História']) + #16
lema(ur'[Ee]l_é_ctric(?:[ao]s|amente)_e', xpre=[ur'Machina ', ur'Carnivale ', ]) + lema(ur'[Ee]l_é_ctric[ao]_e', xpre=[ur'[LM]\. ', ur'Litoria ', ur'Stadionul ', ur'Myrmarachne ', ], xpos=[ur' (?:Salsa|Banat|Dobrogea|Dharma|Timişoara)', ]) + #226
lema(ur'[Ee]m_é_rit[ao]s?_e', xpre=[ur'entre \[\[', ur'de ', ur'con ', ur'Asturica y ', ur'Caesaraugustam ', ur'Augusta ', ], xpos=[ur' (?:[1-9][0-9]*|sp|ya que|Football|Caesarea|Asturicam|Augusta|Caesaraugustam|analoga)\b', ur'(?:\'\'|\]\]\'\'|\]\])', ]) + #2
lema(ur'[Aa]mnist_í_as?_i', xpre=[ur'Art ', ur'L\'', ur'Premi ', ], xpos=[ur' (?:77|i Estatut|Internacional Catalunya|que trata de Spagna|Giustizia|Togliatti|e la|ot )', ur'(?:\]|, Estatut|\.net)', ]) + #38
lema(ur'[Ee]con_ó_mica_o', pre=ur'\b(?:y|más|Antropolog[ií]a|Ciudad|[Cc]omisi[oó]n|[Cc]ompensacion|[Cc]onferencia|[Cc]omunidad|[Cc]ooperaci[óo]n|[Dd]epresi[oó]n|[Gg]uerra|[Vv]ida|[Pp]articipaci[oó]n|[Dd]euda|fuente|[Bb]iblioteca|[Oo]pción|[Aa]portación|[Aa]ctividad|[Hh]istoria|[Cc]lase|[Cc]ultura|[Cc]risis|[Cc]iencia|[Mm]undial|[Pp]olitica,?|[Rr]ecesión|[Rr]egi[oó]n|[Ss]ituaci[oó]n|zona) ', xpre=[ur' di ', ur'nuova ', ], xpos=[ur' (?:tra)\b']) + #25
lema(ur'[Ee]ntr_ó_ (?:al?|en)_o', xpos=[ur' (?:el gran buit|otro mundo)', ]) + #92
lema(ur'[Ee]nv_í_a_i', xpre=[ur'Shimano ', ], xpos=[ur' (?:220|garciai|\'m)', ur'(?:\]|\'m)', ]) + #29
lema(ur'[Ee]p_í_stolas?_i', xpre=[ur'\'\'', ur'\bin ', ur'per ', ur'cum ', ur'Poet\. 50; ', ur'apostoli ', ur'suum ', ur'seu ', ur'Pauli ', ur'Romani \.\.\. ', ur'Rajum\.\.\. ', ur'Plantarum ', ur'Theatri ', ur'Remensem ', ur'Mertensium ', ur'plantarum ', ], xpos=[ur' (?:ad|et|às|em|di|Pelagianorum|quare|Pauli|Mathildis|Sancti|Clementi|Cuthberti|Pio|Julii|de (?:nihilo et|Symphysia|secretis)|Petri|partic)\b', ]) + #197
lema(ur'[Ee]sp_í_as?_i', xpre=[ur'espía\'\' \'', ], xpos=[ur' català', ur'\'\' \'espía']) + #64
lema(ur'[Ee]t_í_lic[ao]s?_i', xpre=[ur'Pscirco ', ]) + #3
lema(ur'[Ff]_é_rre[ao]s?_e', xpre=[ur'Banksia ', ur'Mesua ', ur'Clathria ', ur'Caesalpinia ', ur'manus ', ]) + #216
lema(ur'[Ff]_í_sic[ao]_i', xpre=[ur'difetto ', ur'chimica - ', ur'dal ', ur'dell\'universo ', ur'della ', ur'di ', ur'di una ', ur'e ', ], xpos=[ur' (?:\.ru|d\'|e (?:di|matematica)dei|riduzione|della|Appula|Storico|bestiale|e matematica|i politica)', ur'(?:\.(?:unmsm|uh|ru|unam)|, storico|: Celebrazione|" e)', ]) + #167
lema(ur'[Ff]_ó_sil(?:es|)_o', xpos=[ur'\]\](?:ífero|izad[ao]s?)']) + #44
lema(ur'[Ff]_ú_nebres?_u', xpre=[ur'\b(?:di|et) ', ur'\[\[', ur'banda\)\|', ur'Orasion ', ur'Vincetoxicum ', ur'Letto ', ur'Rex ', ur'Car ', ur'Pompe ', ur'Concerto ', ur'Marcia ', ur'M[ae]rche ', ur'Elegio ', ur'[Ee]logio '], xpos=[ur' (?:in|di|per|sur)\b']) + #81
lema(ur'[Ff]_út_bol_u', xpre=[ur'fútbol, ', ]) + #5
lema(ur'[Ff]at_í_dic[ao]s?_i', xpre=[ur'T\. ', ur'Cicindela ', ur'Agrotis ', ur'Tipula ']) + #3
lema(ur'[Ff]on_é_tic[ao]s?_e', xpre=[ur'\be ', ], xpos=[ur', lessico', ur' e fonologia']) + #16
lema(ur'[Ff]orm_ó__o', xpre=[ur'[@"\']', ur'@ ', ur'Brian ', ur'Exedol ', ur'Exedore ', ur'Exodol ', ur'riacho ', ur'Ivar '], xpos=[ur' parte de esto!', ]) + #786
lema(ur'[Ff]r_á_gil_a', xpos=[ur' (?:Records|X syndrome|things|Heart)', ]) + #5
lema(ur'[Ff]r_í_an_i', xpre=[ur'Terra ', ur'\be '], xpos=[ur' en São']) + #32
lema(ur'[f]ranc_é_s(?!\]\][a-z])+_e', pre=ur'\by ', xpos=[ur' Macdonald']) + #7
lema(ur'[Gg]enealog_í_as?_i', xpre=[ur'\be ', ur'das ', ur'Treball social: una ', ur'Internacionale de ', ur'Societat Catalana de ', ], xpos=[ur' (?:ampliata|regum|de um|e Estratégias|dos|delle|deorum|libellus|teologica dell|i)\b', ur'\'\', \'\'genos']) + #293
lema(ur'[Gg]eograf_í_as?_i', xpre=[ur'\b(?:na|di|em|da) ', ur'\b[Aaei] ', ur'Gazte ', ur'Euskal ', ur'Simpósio de ', ur'Brasileiro de ', ur'Quaderns de ', ur'Ensaio de ', ur'Ensaios de ', ur'História e ', ur'Professores de ', ur'Quaderns de', ur'Revista Catalana de ', ur'Sociedade de ', ur'Societat Catalana de ', ur'do Departamento de ', ur'per la ', ], xpos=[ur' (?:eta|o mundo|- o mundo|Conceitos|şi|nova|brasileira|powszechna|e (?:[Cc]ronologias|Estratégias|política: território|storia)|Histórica dos|espiritual de Catalunya|[Cc]omarcal de Catalunya|[Gg]eneral de Catalunya|das|[di]|nelle|e Estatística|humana i|cioè|critica\. \'\'Revista Geografica|Humana\'\'\. Rio de Janeiro: Livraria)', ur'(?:[,\.] ?(?:caratteri|cartografia|Història|czyli|teoria e realidade)|: (?:conceitos|Ita-z)|%)', ]) + #108
lema(ur'[Gg]eolog_í_as?_i', xpre=[ur'\b[Ee] ', ur'dogmaticae: ', ur'escola de ', ur'parola ', ur'Geologia\. '], xpos=[ur' (?:e Geodesia|petrografia e Mineralogia|Tecnica & Ambientale)', ur'\'\', \'\'espeleologia']) + #8
lema(ur'[Gg]eom_é_tric[ao]s?_e', xpre=[ur'\be ', ur'\bet ', ur'Analysis ', ur'Dubia ', ur'Opera ', ur'Transformatione ', ur'Planisphærio ', ur'Problemata ', ur'Synopsis ', ur'descriptio ', ur'secondo ', ], xpos=[ur' (?:et|quam|demonstrata|practica|de quadratura|secondo|[Dd]edicata)', ]) + #35
lema(ur'[Gg]eometr_í_as?_i', xpre=[ur'\bdi ', ur'Dalla ', ur'fratrum de ', ur'Arithmetica, ', ur'\be ', ], xpos=[ur' (?:do|de solidi|del (?:Compasso|disordine)|plana i àlgebra|intuitiva, per|magna in|Proportioni|diferencial i|speculativa|e la|indivisibilibus)\b', ur'\. Firenze']) + #142
lema(ur'[Gg]r_á_cil_a', xpos=[ur' cactus', ]) + #7
lema(ur'[Gg]ram_á_tic[ao]s?_a', xpre=[ur'Jorgelina ', ur'Emma ', ur'Irma '], xpos=[ur' (?:Ades|cathalana|occitana|de la lengua latina: parte|e pragmalingüistica|limbii)', ur'(?:\]\](?:l|les)|\'\'\' es una)', ]) + #155
lema(ur'[Hh]_á_bil_a', xpre=[ur'Dr\. '], xpos=[ur' Khorakiwala', ur'\.']) + #39
lema(ur'[Hh]ar_í_a[ns]?_i', xpre=[ur'Ipuinen ', ur'montando ', ur'Berita '], xpos=[ur' (?:Penang|Nacional|[Mm]etro|Analisa|Global|Nayla|Waspada)', ur'\]']) + #1
lema(ur'[Hh]er_á_ldic[ao]s?_a', xpre=[ur'P\. ', ur'Bitis ', ur'Redvcida A Las Leyes ', ur'arminjoniana\) ', ur'Aysha ', ur'Pterodroma '], xpos=[ur'\.org']) + #167
lema(ur'[Hh]istoriograf_í_as?_i', xpre=[ur'\bda '], xpos=[ur' (?:i|catalana als)\b', ur', llegenda']) + #8
lema(ur'[Ii]conograf_í_as?_i', xpre=[ur'l\'', ur'\be ', ur'\b(?:ed|di) '], xpos=[ur' (?:storica|dos|e arte|de les)']) + #16
lema(ur'[Ii]nd_í_genas?_i', xpre=[ur'R\. ', ur'Rhabdomastix ', ur'septentrionalis ', ur'Walterius ', ur'Canzone ', ur'Velapertina ', ur'Terra ', ur'sueciæ ', ur'noctua ', ur'Anorthodes ', ], xpos=[ur'\.Bioetica\.org', ur' (?:Hallerianas|et|Cum|do|secundum)\b']) + #215
lema(ur'[Ii]ngenier_í_as?_i', xpos=[ur' (?:Gestionale|Cartogràfica)', ur'\.(?:unam|industrial)', ]) + #189
lema(ur'[Ii]srael_í__i', xpre=[ur'D\'', ur'\bof ', ur'Calisto ', ur'Eitam ', ur'Isaac ', ur'Jordanian–', ur'Raphael '], xpos=[ur' (?:& oKsher Restaurants|Soldiers|Trance||deputy|Army|Tanks|settler|Leadership|Sources|Conquest|Songbook|coast|politician|settlements|Krav|finding|Kitchen|Weapons|Lirah|Conflict|Singles|Theatre|rapper|Music|Educational|Food|Quartet|Knesset|Basketball|Air|Defense|Nuclear|Shekel|Cowboy|Hebrew|financial|insurer|university|insurer|Novelist|Space|Premier|Court|Trial|Police|Shot|Case|Cabinet)', ur', Raphael']) + #874
lema(ur'[Kk]uwait_í__i', xpre=[ur'[Aa]l '], xpos=[ur' (?:journalist|Premier)']) + #1
lema(ur'[Ll]_í_neas?_i', xpre=[ur'\ba ', ur'\bdi ', ur'\'', ur'F\. ', ur'B\. linea ', ur'Buccinulum ', ur'Buccinulum linea ', ur'Clubiona ', ur'Cobitis ', ur'Fiat ', ur'Fiat Linea\|', ur'Grande Punto y ', ur'Papilio ', ur'Phintella ', ur'Prima ', ur'Systolocranius ', ur'[BC]\. ', ur'[Dd]ella ', ur'php\?', ur'prima ', ur'sine ', ur'sulla ', ], xpos=[ur' (?:Input|dialogico|Veneta|della|non|Jireček|del fuoco|[Dd]i |spezzata|rovente|Pelle|nigra|estense|Rossa|alba|fusca|nigra|sinuum)', ur'(?:=|[0-9][0-9])', ]) + #20
lema(ur'[Ll]_í_ric[ao]s?_i', xpre=[ur'dell\'Ópera ', ur'% ', ur'Visione ', ur'Città ', ur'Mistral\'\'/ \'\'', ur'nella ', ur'familia \'\'', ur'[Cc]lase \'\'', ur'Clase ', ur'MSC \'\'', ur'MSC ', ur'della ', ur'Shotta\]\], ', ur'Agony\]\], \[\[', ur'tenore ', ur'Accademia ', ur'astrazione ', ur'tra Opera ', ur'dramma ', ur'scena ', ur'Commedia ', ur'Concerto ', ur'melodramma ', ur'Suite ', ur'Fondazione ', ur'della musica ', ur'Lado ', ur'carriera ', ur'dell\'opera ', ur'firmamento '], xpos=[ur' (?:ed|in|di|lui|leggero|Sperimentale|spinto|nelle|Analas|- tradicijsko|Alfieriana|aragonese|Internazionale|Lado B|\(MSC)\b']) + #369
lema(ur'[Ll]a_s_ dos_', xpre=[ur'tres y ', ur'Y con ', ur'documentales de '], xpos=[ur' (?:dos|en|produce|modifica|y la cuatro)\b', ur'\'', ]) + #1
lema(ur'[Ll]e_í_(?:a[ns]|d(?:as|o))_i', xpre=[ur'\b(?:es|in|di|de) ', ur'\bcon ', ur'Doriopsilla ', ur'Linda ', ur'Mostra de ', ur'Pujol ', ur'[Pp]rincesa '], xpos=[ur' (?:de los|1697|Organa|sawola|Yusheng|Lei|[Tt]ai|Zhenchung|Márquez|Buglass|\((?:1897|arc))', ur'(?:["\]]|, *Shangtun)']) + #257
lema(ur'[Ll]ing_üí_stic[ao]s?_(?:u[ií]|üi)', xpre=[ur'\be ', ur'\b(?:et|di) ', ur'Ars ', ur'alla ', ur'modalidadez ', ur'Espaços ', ur'altra ', ur'Caffè ', ur'Sociedat de ', ur'Associação Portuguesa de ', ur'di politica ', ur'Historiographica ', ur'maturità ', ur'Monumenta ', ur'profilo ', ur'análise ', ur'Atlante ', ur'Storico ', ur'Brasileira de ', ur'Folia ', ur'Diversidade ', ur'Evolução ', ur'Historiographia ', ur'Filologia e ', ur'Società ', ur'promozione del patrimonio ', ur'Studia ', ur'[Ff]ilologia e ', ur'[Ss]toria ', ur'estudos ', ur'estudos ', ur'situação ', ur'situação ', ], xpos=[ur' (?:si|dell|Hafniensia|nella|dalla|Academiae|effettuata|indígena e educação|Românica|Italiana Fuori|moderna e il|occitanas|romanica|Baltica|diatopica de l\'|e (?:filologia|scienze|ideoloxía)\b)', ]) + #310
lema(ur'[Ll]leg_ó__o', xpre=[ur'\b(?:[Ss]i|[Ll]e) ', ur'Ángel ', ur'[Hh]uy que ', ur'[Ss]i (?:lo|te|[Yy]o) ', ], xpos=[ur' (?:[Tt]arde|A La Disco)']) + #93
lema(ur'[M]et_á_lic(?:as|os?)_a', xpos=[ur'(?:\.com|\[\[)']) + #1
lema(ur'[M]et_á_lica_a', xpos=[ur' Zine']) + #130
lema(ur'[Mm]_á_rmol(?:es|)_a', xpre=[ur'Joan ', ur'Sagastume ', ur'Guilbert del '], xpos=[ur' de Dodson', ur'\]\]er[ao]s?']) + #220
lema(ur'[Mm]_á_rtir(?:es|)_a', xpre=[ur'\b(?:ad|di) ', ur'blissful ', ur'je moray ', ur'1582\) ', ur'dessos gloriosos '], xpos=[ur' (?:da|Cypress)\b', ur'(?:\.gov|\]\]io)']) + #1
lema(ur'[Mm]_á_stil_a', xpos=[ur', (?:Chema|Al-Son)']) + #50
lema(ur'[Mm]_é_tric[ao]s?_e', xpre=[ur'\b(?:ad|di) ', ur'Ars ', ur'appendice '], xpos=[ur' (?:spagnola|siculo|Sancti|ad|e (?:poesia|il))']) + #1
lema(ur'[Mm]_í_stic[ao]s?_i', xpre=[ur'\be ', ur'alla ', ur'Predicatore - ', ur'\bdi ', ur'e la '], xpos=[ur' (?:omaggio|ultranaţionalismului|di|Maxima|Power)\b']) + #1
lema(ur'[Mm]_ú_ltiples_u', xpre=[ur' et ', ur'faces ', ur'About ', ur'and ', ur'talents ', ], xpos=[ur' (?:Myelom|arcades|façons|accords|auteurs|by|concessions|effets|expéditions|flashes|Hwanguks|infinis|[Oo]f|parsemés|pattes|Pigmentsarkom|pour|punt|sont|splendeurs|statuts|tours|travées|subcomplexes|submissions|visages|et )', ur'(?:, SE|\.es)\b', ]) + #178
lema(ur'[Mm]a_í_z_i', xpre=[ur'\be ', ur'Extremera ', ur'Alejandro ', ur'Antton ', ur'Fran ', ur'Ramón ', ur'Rementeria ', ur'mays\]\] \(', ], xpos=[ur' (?:Mier|II)', ]) + #206
lema(ur'[Mm]agn_í_fic(?:as|os?)_i', xpre=[ur'\b[Dd]on ', ur'\b[Ii]l ', ur'Il falso ', ur'Walter ', ur'Guglielmo '], xpos=[ur' (?:cornuto|Arts|theatro|Studios)', ur'(?:, Salves|\')']) + #1
lema(ur'[Mm]aor_í_(?:es|)_i', xpre=[ur'[Tt]he ', ur'Blacks ', ur'Kaupapa ', ur'Does ', ur'\bof '], xpos=[ur' (?:converts|Tattoo|Myths|Lore|village|Songs|Venture|tattooing|tatu|or Less)', ur'\'']) + #160
lema(ur'[Mm]e_z_cla_s', xpre=[ur'"', ], xpos=[ur' (?:de noms|or Less)', ]) + #12
lema(ur'[Mm]el_ó_dic[ao]s?_o', xpre=[ur'Hohner ', ur'álbum\)\|' ], xpos=[ur'"', ur' (?:for|Records|napoletana|Cega|\(álbum)']) + #66
lema(ur'[Mm]elancol_í_as?_i', xpre=[ur'\b[Aa] ', ur'pàgina de '], xpos=[ur', a revolução']) + #8
lema(ur'[Mm]itol_ó_gic[ao]s?_o', xpre=[ur'linguaggio '], xpos=[ur' per']) + #38
lema(ur'[Mm]orfolog_í_as?_i', xpre=[ur'\be ', ur'Euskal ', ur'des de la ', ur'do Século XXI: ', ur'livro ', ], xpos=[ur' (?:e (?:distribuição|di|reprodução|formas|anatomia|taxonomia|ecologia)\b|della|polínica de (?:algumas|espécies)|aplicada à|do\b|das|dos|de (?:plântulasfrutos e sementes)|externa e|floral e|biologica vegetale|verbale|Histórica do|E Na|/ Mythologiques)', ur'(?:, (?:riproduzione|sintassi))', ]) + #47
lema(ur'[Mm]ov_í_(?:a[ns])_i', xpre=[ur'Augusto ', ur'Guillermo ']) + #2
lema(ur'[Nn]_á_utic[ao]s?_a', xpre=[ur'[Ii]n ', ur'Chromia y ', ur'De re ', ur'MS ', ur'empresa\)\|', ur'lingua ', ur'at ', ur'Clube ', ur'Circolo ', ur'Sci ', ur'Eumig ', ur'Neoscona ', ur'Perodua ', ur'barbatus ', ur'Neoscona ', ur'Pyxis ', ur'MS Nautica\|'], xpos=[ur' (?:a su|Cervia|Malibu Triathlon|Thorn|Stage|Theater|Neptunia|Posillipo|della|\(empresa|en Cleveland|Sabazia|& David Jones|d[ai] )', ur'(?:\'|, (?:Guess|Paula|John Varvatos))']) + #205
lema(ur'[Nn]_ó_rdic[ao]s?_o', xpre=[ur'Aula ', ur'banda\)\|', ur'aerolínea\)\|', ur'Funga ', ur'Chrysso ', ur'Flora ', ur'Lillian '], xpos=[ur' (?:Arrows|\((?:banda|aerolínea))']) + #69
lema(ur'[Nn]_ú_cleos?_u', xpre=[ur'Il '], xpos=[ur' (?:di|Speculativo|interdisciplinar|Armato)\b', ur'\[\[cápside']) + #313
lema(ur'[Oo]c_é_anos?_e', xpre=[ur'\bao ', ur'\bO ', ur'\b(?:d[ae]ll|nell)[\'’]', ur'1971: \'\'', ur'XVI\'\'\. \'\'', ur'Lisboa: \'\'Revista ', ur'Rossi\]\]: \'\'', ur'[Aa]ll[\'’]', ur'S\.', ur'Xavier y ', ur'imperium ', ur'compañero ', ur'Serata ', ur'Leone y ', ur'[Mm]ar ', ur'Mare ', ur'Sugeytas no ', ur'Tapp ', ur'sull\'', ], xpos=[ur' (?:di|Mare|da|ao|propriora|Andrade|[Mm]osby|Elkann|prese|Grupo|Nox|mare|Atlântico|MAEVA|\((?:California|banda)|County|Net|\(39|\(83)\b', ur'(?:, Palmers|\])', ]) + #235
lema(ur'[Oo]rtograf_í_as?_i', xpre=[ur'[dl]\'', ur'd\' '], xpos=[ur' de la Llengua']) + #8
lema(ur'[Pp]_ó_mez_o', xpos=[ur' Di\b', ur', Roncagliolo', ]) + #7
lema(ur'[Pp]_ó_rticos?_o', xpre=[ur'\ba ', ur'\bin ', ur'(?:[Tt]he|and) ', ur'Stamperia del ', ], xpos=[ur' (?:e San|of|on|di|della|Quartet|del Pavaglione|Books)']) + #153
lema(ur'[Pp]_ú_gil_u', xpre=[ur'[ACI"]\. ', ur'Chelanops ', ur'Athleticatemnus ', ur'Arctosa ', ur'Ideoblothrus ', ur'Paguristes ', ur'Anyphaena '], xpos=[ur'\'\'\', de']) + #36
lema(ur'[Pp]atolog_í_a_i', xpre=[ur'\bd[ai] ', ur'Revisão Anual de ', ], xpos=[ur' (?:[Vv]egetale|e crimes|del pancreas in)\b', ]) + #32
lema(ur'[Pp]ol_í_gonos?_i', xpre=[ur'Edizioni del '], xpos=[ur' (?:Febo|Manoppello)', ur'\'', ]) + #5
lema(ur'[Pp]ortugu_é_s_e', xpre=[ur'\b[Ee]m ', ur'lingoajem ', ur'Associacio ', ur'Clube ', ur'Gladys ', ], xpos=[ur' (?:da|Water|Acevedo)\b', ur'\]\][ae]s', ]) + #169
lema(ur'[Pp]otos_í__i', xpre=[ur'Zorocrates ', ur'Gnaphosa ', ur'Misuri\)\|'], xpos=[ur' \(Misuri', ur'\]\]n[ao]s?']) + #1
lema(ur'[Pp]r_ó_cer(?:es|)_o', xpre=[ur'L\: ', ur'rex ', ur'Recognoverunt ', ur'Lamprochernes ', ur'Diplocephalus ', ur'Carbonell ', ur'Megascolia ']) + #53
lema(ur'[Qq]ued_ó__o', xpre=[ur'(?:[Yy]o|[Mm]e|[Ll]o|[Ee]m|[Dd]o) ', ur'bisbiseo, ', ur'muy ', ur'Azul ', ur'cómo ante el público ', ur'Ahora ', ur'eu acá ', ur'Gómez ', ur'Picón ', ur'[Dd]onde ', ], xpos=[ur' (?:estido|co\'ele)', ]) + #83
lema(ur'[Rr]_í_o_i', pre=ur'(?:[Ee]l|[Dd]e|del|al|[Uu]n) ', xpre=[ur'\baan ', ur'Alberto ', ur'Alessandro ', ur'Antonius ', ur'Avinguda ', ur'Bacino ', ur'Botanique ', ur'Chemin ', ur'Complexo do Alemão ', ur'Câmara Municipal ', ur'Desportivo ', ur'Desporto ', ur'Diário ', ur'Ercole ', ur'Estadual ', ur'Eug[éê]nia ', ur'Eulália ', ur'Henrique ', ur'Herdade ', ur'Homme ', ur'Igreja Matriz ', ur'Memória ', ur'Microrregião ', ur'Museu Nacional ', ur'Museu Oceanografico ', ur'Palácio ', ur'Paul ', ur'Prato ', ur'RPM ', ur'Região ', ur'Singing ', ur'São Francisco ', ur'São José ', ur'São Pedro ', ur'Torneo ', ur'[Cc]ondado ', ur'amiga ', ur'concelho ', ur'do Brasil ', ur'fundação ', ur'fundação de ', ur'homme ', ur'jaune ', ur'mines ', ur'mines de ', ur'provinces ', ur'voz ', ], xpos=[ur' (?:Quente|Claro FC|Tinto|Vermelho|Ave Futebol|Branch|Convention|de Contas|nell|delle|das|do|di|dei|Maior|Metro|Branco|Gran do Nord|[Gg]rande (?:[Dd]o|Railroad|Valley|Story|Botanic|City)|Preto da|Livre|de Moinhos|de Janeiro à|Tinto (?:Group|Copper|Alcan|Energy|Diamonds|Iron|Coal|Plc|a la nit|Sports|di|nell\'Elba|Preto|Grande Western))\b', ur', Grecia', ]) + #1948
lema(ur'[Rr]efer_í_(?:a[ns]?|)_i', xpos=[ur'\bel ', ur'del ', ]) + #26
lema(ur'[Rr]endir_á_[ns]?_a', xpos=[ur' coi', ]) + #5
lema(ur'[Rr]esolv_í__i', xpre=[ur'gradus ', ]) + #1
lema(ur'[Rr]etom_ó__o', xpre=[ur'[AaEe]l ']) + #1
lema(ur'[Rr]om_á_nic[ao]s?_a', xpre=[ur'Italia ', ur'Architettura ', ur'Septaglomospiranella ', ur'Trichouropoda ', ur'Pittura ', ur'ottoniana e ', ur'Voz ', ], xpos=[ur' (?:archaico|dos)', ur'\.com']) + #143
lema(ur'[Ss]_í_lex_i', xpre=[ur'\bà ', ur'\bdu ', ur'SS-N-14 ', ur'néolithiques de ', ur'éclats de ', ur'Indiana\)\|'], xpos=[ur' (?:\(Indiana|and)', ur'\'S']) + #336
lema(ur'[Ss]_í_mbolos?_i', xpre=[ur'Torino ', ur'jubilea '], xpos=[ur' (?:[Vv]alore|di)\b', ur', valore', ur'\]\]gía']) + #260
lema(ur'[Ss]ab_í_as? (?:que|lo)_i', xpre=[ur'l\'home ', ur'\bla ', ur'palabra más ', ur'mujeres ', ur'mujer ', ur'disciplina ', ur'\by ', ur'muy '], xpos=[ur' Demais']) + #1
lema(ur'[Ss]ab_í_as?_i', pre=ur'(?:[EeÉé]l|[Ee]lla|[Ll]o|[Ss]i|[Nn]o|[Nn]adie|[Qq]u[ée]|[Qq]ui[ée]n|[Yy]a|[Ss]e(?: me| te| l[aeo]s?|)) ', xpos=[ur' (?:não|Javanês|de Cor)']) + #1
lema(ur'[Ss]and_í_as?_i', xpre=[ur'The ', ur'por ', ur'George ', ur'Unida de las ', ur'llamada ', ur'Nacional ', ur'Nacionales ', ur'[Dd]el ', ur'de ', ur'sandios” o “', ur'de Sandia\|', ur'sandía, ', ur'Perú\)\|', ur'Provincia de ', ur'Acacio ', ur'Eduardo ', ur'Familia '], xpos=[ur' (?:\(\(Perú|View|High|Perú|Pueblo|National|Laboratories|Labs|Casino)', ur'(?:\]\]|\.gov|, Puno)']) + #8
lema(ur'[Ss]angu_í_ne[ao]s?_i', xpre=[ur'\'\'', ur'[BbCcFfGgHhLlNnRrSs]\. ', ur'var\. ', ur'Yamina\) ', ur' × ', ur'Stelis ', ur'Madrella ', ur'Thordisa ', ur'Hetaerina ', ur'Etlingera ', ur'Sanguirana ', ur'Anemone ', ur'Amelanchier ', ur'Amyema ', ur'Argemone ', ur'Baccaurea ', ur'Baccharis ', ur'Begonia ', ur'Bematistes ', ur'Berberis ', ur'Bertolonia ', ur'Botryonopa ', ur'Bletia ', ur'Broughtonia ', ur'Brugmansia ', ur'Buprestis ', ur'Cacatua ', ur'Caladenia ', ur'Calandrinia ', ur'Calobotrya ', ur'Canna ', ur'Canavalia ', ur'Caraguata ', ur'Catagramma ', ur'Catasetum ', ur'Celaenorrhinus ', ur'Centaurea ', ur'Cephaloleia ', ur'Chidlowia ', ur'Corinna ', ur'Coreosma ', ur'Cornus ', ur'Cousinia ', ur'Crataegus ', ur'Crematogaster ', ur'Cycloneda ', ur'Datura ', ur'Delesseria ', ur'Diplura ', ur'Digitaria ', ur'Disa ', ur'Drimia ', ur'Dussia ', ur'Echinacea ', ur'Eremostachys ', ur'Eria ', ur'Euglena ', ur'Euphorbia ', ur'Fernandezia ', ur'Formica ', ur'Galerella ', ur'Gasteracantha ', ur'Guzmania ', ur'Haemodoryida ', ur'Heuchera ', ur'Himatione ', ur'Holmskioldia ', ur'Hyobanche ', ur'Hypsosinga ', ur'Indigofera ', ur'Iris ', ur'Lactuca', ur'Lantana ', ur'Leandra ', ur'Lebistina ', ur'Lepanthes ', ur'Libellula ', ur'Lycoris ', ur'Linyphia ', ur'Macrophora ', ur'Macrosamanea ', ur'Maurandya ', ur'Maxillaria ', ur'Melithaea ', ur'Mirabilis ', ur'Musa ', ur'Nepenthes ', ur'Neuropeltis ', ur'Nycerella ', ur'Olea ', ur'Orchestina ', ur'Orobanche ', ur'Oreorchis ', ur'Pachycondyla ', ur'Paratropis ', ur'Passiflora ', ur'Phytolacca ', ur'Pinus ', ur'Platypoecilus ', ur'Portulaca ', ur'Potentilla ', ur'Pritzelia ', ur'Pterostylis ', ur'Pyrus ', ur'Rana ', ur'Rebutia ', ur'Restrepia ', ur'Rhodopechys ', ur'Rottboellia ', ur'Ruellia ', ur'Russula ', ur'Salix ', ur'Sanguirana', ur'Sarcodes ', ur'Sarcophyte ', ur'Schinia ', ur'Stromanthe ', ur'Swida ', ur'Tabebuia ', ur'Tacsonia ', ur'Thecanthes ', ur'Thelepogon ', ur'Thelycrania ',ur'Thonningia ', ur'Tituboea ', ur'Trianthema ', ur'Trigonuropoda ', ur'Tricholochmaea ', ur'Tritonia', ur'Vandellia ', ur'Uroactinia ', ur'Xanthopachys ', ur'Xyris ', ur'Weigela ', ur'Zeugophora ', ur'subsp\. ', ur'camara ', ur'maculatus ', ur'vitzthumiconsanguinea ', ur'[Vv]irga ', ]) + #1
lema(ur'[Ss]egu_í_a[ns]?_i', xpre=[ur'por ', ur'Genesis ']) + #176
lema(ur'[Ss]elec_c_ionad[ao]s?_', xpos=[ur' na\b']) + #13
lema(ur'[Ss]inf_ó_nic[ao]s?_o', xpre=[ur'Pezzo ', ur'Ciaccona ', ur'Rappresentazione ', ur'Trinita ', ur'Intermezzo ', ur'Associazione ', ur'[Oo]rchestra ', ur'Suite ', ur'\|', ], xpos=[ur' (?:per|della|e Coro|(?:di|of) )', ]) + #53
lema(ur'[Ss]oberan_í_as?_i', xpos=[ur' (?:i|do|das|del reyno|e Cultura)\b', ]) + #38
lema(ur'[Ss]ociolog_í_as?_i', xpre=[ur'\b(?:em|na|di) ', ur'Systema de ', ur'Català de ', ur'espaço: textos de ', ur'\bi '], xpos=[ur' (?:da|della|e Comunicaçao)\b']) + #8
lema(ur'[Ss]omal_í__i', xpre=[ur'Hamzeh '], xpos=[ur' (?:Man|Piracy|Pigeon|Queen|King|Nationalism|Airlines|Supper)']) + #1
lema(ur'[Ss]orb_í_an_i', xpos=[ur' Cultural', ur'"\. El']) + #3
lema(ur'[Ss]ubterr_á_ne[ao]s?_a', xpre=[ur'[AP]\. ', ur'\ba ', ur'\b(?:en|de) ', ur'Aphaenogaster ', ur'Ficus ', ur'Rieti ', ur'Etlingera ', ur'Walckenaeria ', ur'Acalypha ', ur'Vicia ', ur'horrea ', ur'Microcreagrina ', ur'Agrotis ', ur'Thermotoga ', ur'Physica ', ur'Adesmia ', ur'Linyphia ', ur'Phanetta ', ur'Newberrya ', ur'Voandzeia ', ], xpos=[ur' (?:films|\(cómic|Americal|do)\b', ur'\'\', álbum']) + #1
lema(ur'[T]ard_í_[ao]_i', xpre=[ur'Vinicius ', ur'Alex ', ur'Chris ', ur'Jackie ', ur'Joseph ', ur'Loaiza ', ur'Rojas ', ur'Sandro ', ], xpos=[ur' y Guzm[áa]n', ]) + #12
lema(ur'[Tt]_é_cnica (?:de|que)_e', xpos=[ur' Engenharia']) + lema(ur'[Tt]_é_cnicas? de_e', xpos=[ur' de coleta e herborizacao']) + lema(ur'[Tt]_é_cnic(?:[ao]s|amente)_e', xpre=[ur' e ']) + lema(ur'[Tt]_é_cnico_e', xpre=[ur'Istituto ', ur'Boletim ', ur'Stabilimento ', ur'Studio ', ur'Superiore '], xpos=[ur' (?:d\'Artiglieria|Industriale|superiore|dell|di )', ur'@', ]) + lema(ur'[Tt]_é_cnica_e', pre=ur'(?:[Ll]a|[Uu]na|[Cc]ada|[Ss]u|[Ee]sta|y) ', xpre=[ur' i de ', ur'Scuola ', ], xpos=[ur' (?:edilizia|dell|di )', ]) + #63
lema(ur'[Tt]_í_mid(?:[ao]s?|amente)_i', xpre=[ur'T\. ', ur'Alstroemeria ', ur'Benoitia ', ur'labbro ', ur'Ebrechtella ', ur'Benoitia ', ur'Dibolia ', ur'Carex ', ur'Gentiana ', ur'Actinia ', ur'mais ', ur'Il ', ur'Zephyranthes ', ur'Triglochinura ', ur'Megachile ', ur'Troppo ']) + #51
lema(ur'[Tt]_ú_nicas?_u', xpre=[ur'\bsa ', ur'lenguas ', ur'idioma ', ur'Thrinax ', ur'Pablo ',ur'longa ', ], xpos=[ur' (?:Resorts|muscularis|language|\(Misisipi|\(MS)', ur'(?:\]|, Greenville|, Mississippi)', ]) + #170
lema(ur'[Tt]al_ _vez_', xpre=[ur'Um Dia… ', ur'Amanhã '], xpos=[ur' (?:não|[Ss]eja|Depois)']) + #1
lema(ur'[Tt]axon_ó_mic[ao]s?_o', xpre=[ur'Estudo ', ur'Plantilla:Categorias ', ur'Revisão ', ur'Series A, '], xpos=[ur' (?:da|[Dd]ipterorum)\b']) + #1
lema(ur'[Tt]axonom_í_as?_i', xpre=[ur'\b(?:na|da) ', ur'\b[àe] ', ur'Laboratório ', ur'Laboratório de ', ur'Bibliografía de botanica 3, ', ur'Biología e ', ur'Botânica IV - ', ur'Botânica V - ', ur'Morfologia e ', ur'Sul-Americanos\. ', ur'sobre a ', ur'sul-americanos \(Coleoptera\)\. ', ], xpos=[ur' (?:e (?:Evolução|aspectos|[Dd]istribuição|Morfologia|filogenia|revisão|Anatomia das)|de angiospermae|mascherina|d[ao]s? )', ur', (?:morfologia e distribuição|distribuição|ecologia e gen[eé]tica)', ]) + #51
lema(ur'[Tt]elef_ó_nic[ao]s?_o', xpre=[ur'L\'Esercizio ', ur'L\'elenco', ], xpos=[ur'\.net', ur' (?:USA|Data|Networks|di|ROMANIA|farà)\b', ]) + #67
lema(ur'[Tt]em_á_tic[ao]s?_a', xpre=[ur'Tartini ', ur'Platti – Catalogo ', ur'l\'opera con catalogo ', ur'Parco '], xpos=[ur' (?:dell[ae]|Nazionale)', ]) + #64
lema(ur'[Tt]eolog_í_as?_i', xpre=[ur'\b(?:em|di|da) ', ur'\b[aeéi] ', ur'\be la ', ur'Doutrina Católica - ', ur'Facultat de ', ur'Història de la ', ur'Institut de ', ur'Libertação, ', ur'Pietro: ', ur'Revista catalana de ', ur'Uma ', ur'della ', ], xpos=[ur' (?:lucana|Práticas|Razionale|Politica dell|avui|ecofeminista|actual|Morale|[Ff]ondamentale|com|d[ai]|pol[ií]tica (?:pastorale|per|di|e dissimulazione)|della|delle|e (?:Liberazione|spiritualità)|por la Insigne Vniversidad|i|na)\b', ur'(?:\.com|, storia)', ]) + #132
lema(ur'[Tt]eor_í_as?_i', pre=ur'(?:[Ee]stas?|[Ll]as?|[Oo]tras?|[Uu]nas?|[Ee]n|[Dd]iversas) ', xpos=[ur' (?:politica di|scientifica|ideologica della|Senyal|e (?:Crítica|i suoi)|della|degli|dei|de la Probabilitat|del sacro|di )', ur'\.com', ]) + #98
lema(ur'[Tt]ermin_ó_ (?:sus?|por|con|en|el|después|empatad[ao]|eliminad[ao]|primer[ao]|segund[ao]|tercer[ao]|cuart[ao]|quint[ao])_o', xpre=[ur'dando ', ur'nuevo ', ], xpos=[ur' el']) + #115
lema(ur'[Tt]opograf_í_as?_i', xpre=[ur'\ba ', ur'\bdi ', ur'sulla ', ], xpos=[ur' (?:e geografia|d[io]|dei|Savini|Firenze|dels)', ur'\]', ]) + #6
lema(ur'[Tt]os_í_a[ns]?_i', xpre=[ur'Santa ', ], xpos=[ur' (?:Altman|Malamud|apenas tenía)', ur'(?:\]| \|\|)', ]) + #3
lema(ur'[Tt]r_á_ficos?_a', xpre=[ur'No '], xpos=[ur' transatlântico']) + #1
lema(ur'[Tt]r_á_gico_a', xpre=[ur'Incantessimo ', ur'pensiero ', ur'Idillio ', ur'Incantesimo ', ur'[Mm]elodramma ', ur'e del ', ur'fine ', ur'secondo ', ], xpos=[ur' (?:ritorno|amore|e improvvisatore|Garrick|convegno|del mondo|francese)', ]) + #13
lema(ur'[Tt]r_á_mites?_a', xpre=[ur'que ', ur'Il ', ur'marchio ', ur'[Ss]e ']) + #1
lema(ur'[Tt]ranv_í_a_i', xpos=[ur' Blau', ur'(?:\]|\.(?:org|2011))', ]) + #29
lema(ur'[Uu]tili_c_en?_z', xpre=[ur'Can '], xpos=[ur' (?:the|loss-less)']) + #1
lema(ur'[Vv]_a_[ns]?_á', xpre=[ur'marit ', ur'Não ', ur'Eu '], xpos=[ur'[<]', ur' (?:jól|Cavar|[Tt]udo|de (?:bike|Metrô)|Sim\'bora|Movimiento|Se Perder)', ur', mas Volte']) + #62
lema(ur'[Vv]ac_í_[ao]s?_i', xpre=[ur'Absolut ', ur'Natividad ', ], xpos=[ur' (?:el|l[ao]s?|y Neill|Isáurico)', ]) + #183
lema(ur'[Vv]al_í_a[ns]?_i', xpre=[ur'Três Escultores de '], xpos=[ur'\]', ur' (?:se|Barak|&|Garz[oó]n|Merino)\b']) + #8
lema(ur'[Vv]e_í_a[ns]?_i', xpre=[ur'\b[Nn]a '], xpos=[ur' (?:vostra|poética|em)']) + #32
lema(ur'[Vv]ern_á_cul[ao]s?_a', xpre=[ur'Legio '], xpos=[ur'\]\]r\b']) + #1
lema(ur'[Vv]est_í_a[ns]?_i', xpos=[ur' (?:la giubba|lycioides|foetida|gotov)', ur'(?:\]\]|\'\'\'\'\' es)', ]) + #18
lema(ur'[Vv]olc_á_n_a', xpre=[ur'être un ', ur'pequeño de ', ur'planes de ', ur'Viola ', ur'Mangora ', ur'Anyphaenoides ', ur'Lygromma ', ur' (?:du|[Ll]e) '], xpos=[ur' (?:d\'|du|de nous|Mines|Club|Entertainment|Studios)\b', ur'(?:\]\]es)']) + #1
lema(ur'[d]e_ _l[ao]s_', xpre=[ur' (?:en|de) ', ur' a ', ur'calandarios '], xpos=[ur'[\]\|\']', ur' (?:\)|Santos|Alas|Eljas|Reyes|[BW]\.)']) + #10
lema(ur'[f]r_í_[ao]_i', xpre=[ur'\bdo ', ur'Theridion ', ur'Acrobasis ', ur'Andrena ', ur'Herpyllus ', ur'Noite ', ur'P\. ', ur'Poecilia ', ur'Priapichthys ', ur'Pseudopoecilia ', ur'aquela ', ur'\b[Dd]u ', ], xpos=[ur' konsterna', ur'5']) + #191
lema(ur'[m]et_á_lic[ao]s?_a', xpre=[ur'T\. ', ur'Fanzine ', ur'Chamaedorea ', ur'Mnesarete '], xpos=[ur' zine', ur'\.com']) + #1
lema(ur'[t]ard_í_[ao]_i', xpre=[ur'Director ', ur'Neil ', ur'\*', ur'do amor ', ], xpos=[ur' de Rio Grande do Sul', ]) + #27
lema(ur'[v]iv_í_a[ns]?_i', xpre=[ur'\b[Dd]i '], xpos=[ur' es el']) + #1
lema(ur'_Z_onas_S', xpre=[ur'Jeff ', ]) + #2
lema(ur'_z_onas_s', xpre=[ur'Fuxidos de ', ], xpos=[ur' Veris']) + #5
lema(ur'_Á_guilas?_A', xpre=[ur'Penna ', ur'Dell\' ', ur'[LlSs]\'', ur'School Nido de ', ur'Jeff ']) + #1
lema(ur'_Á_lgebras?_A', xpre=[ur' (?:of|to|[ai]n|on) ', ur'# ', ur'\'', ur'Double ', ur'[Aa]bstract ', ur'Abstrakt ', ur'[Cc]ommutative ', ur'about ', ur'Applicable ', ur'Applied ', ur'Banach ', ur'[Bb]asic ', ur'Beitraege ', ur'Boolean ', ur'Categorical ', ur'class ', ur'Clifford ', ur'College ', ur'Comm\. ', ur'Computer ', ur'Differential ', ur'Fashion ', ur'Local ', ur'Geometric ', ur'Heisenberg ', ur'Homological ', ur'Image ', ur'Jahre ', ur'Liber ', ur'Lie ', ur'Linear ', ur'Logical ', ur'[Mm]atrix ', ur'[Mm]odern ', ur'Moderne ', ur'Multilinear ', ur'Neumann ', ur'Nichtkommutative ', ur'Noncommutative ', ur'Operator ', ur'ROSE ', ur'Relational ', ur'Tensor ', ur'Term ', ur'Try ', ur'Visualizing ', ur'Your ', ur'[Aa]ssociative ', ur'[Bb]efore ', ur'[Hh]ypercomplex ', ur'[Rr]eal ', ur'[Uu]niversal ', ur'[fz][uü]r ', ur'absoluten ', ur'and ', ], xpos=[ur' (?:is|der|and|Suicide|for|\(cantante|of)\b', ur'(?:["\]]|, (?:rings|with|and|quantum|Geometry))', ]) + #1
lema(ur'[Mm]uft_í_s?_i', xpre=[ur'Aamir ', ur'des ', ur'Mehbooba ', ur'Mumtaz ', ur'Mohammed ', ur'A\. ', ur'Al '], xpos=[ur' Mohammad']) + #186
lema(ur'_C_hile_c', pre=ur'(?:[Aa]|[Aa]nte|[Ee]n|[Pp]ara|[Pp]or) ') + #1
lema(ur'[Vv]_í_a de_i', xpre=[ur'Uma '], xpos=[ur' les']) + #1
lema(ur'[Vv]_í_as de_i') + #1
lema(ur'[Ee]scond_é_rsel[ao]s?_e') + #1
lema(ur'[Ee]nterar_í_a[ns]?_i') + #1
lema(ur'[d]ar_í_a[ns]?_i') + #1
lema(ur'[Dd]iver_sió_n_(?:ci[oó]|sió)') + #1
lema(ur'[Ii]r_í_a[ns]? (?:a|de)\b_i') + #1
lema(ur'[Ee]ntreten_í_a[ns]?_i') + #1
lema(ur'_S_ur ?[Aa]m[eé]rica_s') + #1
lema(ur'_C_entro ?[Aa]m[eé]rica_c') + #1
lema(ur'[Pp]rov_e_nientes?_i') + #1
lema(ur'[Cc]l_ú_ster_u', pre=ur'(?:[Ee]l|[Uu]n) ') + #1
lema(ur'[Cc]onquistar_á_[ns]?_a', xpre=[ur'Johnny ', ur'que ', ur'\bl[ae] ']) + #1
lema(ur'[Tt]iran_í_as?_i', xpos=[ur' visului']) + #1
lema(ur'_Castejó_n_(?:castej[oó]|Castejo)') + #1
lema(ur'[Ee]nc_é_falos?_e') + #1
lema(ur'[Pp]re_c_isamente_s') + #1
lema(ur'[Ee]spadach_í_n_i') + #1
lema(ur'[Cc]r_í_ticos? de_i') + #1
lema(ur'[Pp]ornogr_á_fic[ao]s?_a') + #1
lema(ur'[Aa]__ l[ao]s_l') + #1
lema(ur'[Ee]n_ _una?_') + #1
lema(ur'[Pp]roteger_í_a[ns]?_i') + #1
lema(ur'[Jj]ugar_á_[ns]_a', xpre=[ur'que ambos ']) + #1
lema(ur'[Jj]ugar_á__a', pre=ur'\b[Ss]e ') + #1
lema(ur'[Oo]per_ó__o', xpre=[ur'\bv ', ur'[Yy]o ', ur'y lo ', ur'delle ', ur'mejor me '], xpos=[ur' omnia']) + #1
lema(ur'[Pp]repar_ó__o', xpre=[ur'\b(?:[Mm]e|[Yy]o|[Ll]o|de) '], xpos=[ur' (?:la adecuada|muy bien|el (?:t[eé]|arroz)|arroz|te para|una (?:fiambrera|super)|muy poco|estas gilipolleces)']) + #1
lema(ur'[Vv]isit_ó__o', xpos=[ur' (?:Mi Región|Mi Naturaleza|Mi Historia)']) + #1
lema(ur'[Cc]re_ó_ (?:una?|el|la)_o') + #1
lema(ur'[Vv]aci_ó_ (?:una?|el|la)_o') + #1
lema(ur'[Pp]ag_ó_ (?:una?|el|la)_o') + #1
lema(ur'(?<= )(?:[1-9]|[1-3][0-9])_ _de(?= )_', xpre=[ur'[Vv]id ']) + #657
lema(ur'[Cc]o_nvirtió__(?:m[bv]irti[oó]|nbirti[oó]|onvirtió)_') + #1
lema(ur'[Cc]onfi_ó__o') + #1
lema(ur'_á_mbitos?_a') + #1
lema(ur'_Á_mbitos?_A') + #1
lema(ur'_É_l (?:aceptó|actuó|afirmó|anunció|apareció|aprendió|argumentó|asistió|ayudó|buscó|cambió|cantó|comentó|comenzó|compitió|concluyó|conoció|consiguió|continuó|creció|creó|debutó|decidió|declaró|dejó|demostró|desafió|desarrolló|descubrió|dirigió|diseñó|eligió|empezó|encontró|entró|envió|equipó|escogió|escribió|estableció|estrenó|estudió|explicó|falleció|firmó|formó|fundó|ganó|grabó|inició|intentó|interpretó|jugó|llamó|llegó|llevó|logró|luchó|mató|mencionó|murió|nació|negó|notó|ofreció|participó|pasó|pensó|perteneció|pidió|presentó|proyectó|publicó|realizó|recibió|regresó|respondió|rondó|salió|siguió|sirvió|sugirió|terminó|tomó|trabajó|trió|usó|utilizó|vivió)_E') + #780
lema(ur'_é_l (?:aceptó|actuó|afirmó|anunció|apareció|aprendió|argumentó|asistió|ayudó|buscó|cambió|cantó|comentó|comenzó|compitió|concluyó|conoció|consiguió|continuó|creció|creó|debutó|decidió|declaró|dejó|demostró|desafió|desarrolló|descubrió|dirigió|diseñó|eligió|empezó|encontró|entró|envió|equipó|escogió|escribió|estableció|estrenó|estudió|explicó|falleció|firmó|formó|fundó|ganó|grabó|inició|intentó|interpretó|jugó|llamó|llegó|llevó|logró|luchó|mató|mencionó|murió|nació|negó|notó|ofreció|participó|pasó|pensó|perteneció|pidió|presentó|proyectó|publicó|realizó|recibió|regresó|respondió|rondó|salió|siguió|sirvió|sugirió|terminó|tomó|trabajó|trió|usó|utilizó|vivió)_e') + #780
lema(ur'_É_l (?:acompañó|administró|adoptó|agregó|alcanzó|alegó|anotó|arbitró|asedió|atendió|audicionó|añadió|bombardeó|caló|causó|cayó|centró|citó|compartió|comparó|completó|compró|concursó|confirmó|conquistó|consideró|contribuyó|contó|coreografió|corrió|creyó|criticó|dedicó|denominó|denunció|derrotó|desapareció|describió|desempeñó|dimitió|elogió|emigró|encargó|enseñó|esperó|experimentó|expresó|forró|frió|habló|ideó|impactó|impartió|impulsó|incendió|informó|ingresó|insistió|inspiró|inventó|lanzó|libró|mandó|marcó|mostró|nombró|observó|organizó|perdió|permaneció|prefirió|pregó|premió|preparó|prometió|promovió|quedó|rechazó|reclutó|recomendó|reemplazó|registró|removió|renunció|representó|resaltó|respetó|restó|retomó|retornó|rompió|señaló|sintió|sitió|sobrevivió|subió|sucedió|sufrió|tituló|tocó|torneó|traspasó|trató|vendió|viajó|visitó|volvió)_E') + #246
lema(ur'_é_l (?:acompañó|administró|adoptó|agregó|alcanzó|alegó|anotó|arbitró|asedió|atendió|audicionó|añadió|bombardeó|caló|causó|cayó|centró|citó|compartió|comparó|completó|compró|concursó|confirmó|conquistó|consideró|contribuyó|contó|coreografió|corrió|creyó|criticó|dedicó|denominó|denunció|derrotó|desapareció|describió|desempeñó|dimitió|elogió|emigró|encargó|enseñó|esperó|experimentó|expresó|forró|frió|habló|ideó|impactó|impartió|impulsó|incendió|informó|ingresó|insistió|inspiró|inventó|lanzó|libró|mandó|marcó|mostró|nombró|observó|organizó|perdió|permaneció|prefirió|pregó|premió|preparó|prometió|promovió|quedó|rechazó|reclutó|recomendó|reemplazó|registró|removió|renunció|representó|resaltó|respetó|restó|retomó|retornó|rompió|señaló|sintió|sitió|sobrevivió|subió|sucedió|sufrió|tituló|tocó|torneó|traspasó|trató|vendió|viajó|visitó|volvió)_e') + #246
lema(ur'[Cc]lasific_ó_ (?:al|en)_o') + #1
lema(ur'[Cc]elebr_ó_ (?:al|en)_o') + #1
lema(ur'[Rr]adi_ó_log[oa]s?_o') + #1
lema(ur'[Pp]rocuradur_í_as?_i') + #1
lema(ur'[Cc]lausur_ó__o') + #1
lema(ur'[Gg]eneral_me_nte_em') + #1
lema(ur'_ú_nico [a-zñáéíóú]+_', xpre=[ur'[Ll]\'', ur'in un ', ur'in ', ur'Partito ', ur'quasi '], xpos=[ur' (?:motus|expressarum|concorrente|Amore|mercato|arbëreshë|posto|suo|la quantità|gli|norme|manuale|prima|de Espana|leggi|tra|di|nome|biblioteche|in|funivia|di|suo|della|queda|leggi|per)']) + #1
lema(ur'[Mm]arc_ó_ (?:en|un|dos|tres|la|l[ao]s)_o', xpre=[ur'como ']) + #1
lema(ur'[Ee]_spe_cies?_(?:pe|sp)') + #1
#lema(ur'___') + #1
#lema(ur'___') + #1
#lema(ur'___') + #1
#lema(ur'___') + #1
#lema(ur'___') + #1
#lema(ur'___') + #1
#lema(ur'___') + #1
#lema(ur'___') + #deleitó 

lema(ur'[Aa]_ _los_', xpre=[ur'Arnaldo ', ur'Arronte ', ur'Peiro ', ur' et '], xpos=[ur' (?:Ahmed|más tarde|Indios|passados)', ur'(?:\]|\.e-monsite)']) + #50
lema(ur'[Aa]__l_ la e', xpre=[ur'[Ll]a '], xpos=[ur' la']) + #1
lema(ur'[Aa]_l_ (?:[AÁaá](?:rea|guila|lgebra)|ánima|a(?:rma|rca|lma|lza|gua|la|rpa|ve)|ha(?:bla|da|cha|mbre|mpa|rpa))_ (?:el|la)', xpos=[ur' [Mm][aá]ter']) + #1
lema(ur'[Aa]firm_ó__o', xpre=[ur'\bdi ', ur'afirmar y ', ur'\[', ur'\b(?:[Nn]o|[SsNn]i|[YyLl]o|me) '], xpos=[ur' (?:oc|hoy|No|que en este punto|lo que|toda la|un contenido|l\'esperança|un judaísmo)', ur', pues']) + #1
lema(ur'[Cc]ancel_ó__o', xpre=[ur'João ', 'Cancelo\|'], xpos=[ur'\]\]']) + #1
lema(ur'[Dd]__e_e d', xpos=[ur' (?:Quervain|Waite|Murise|Beer|Toro|Broglie|Gaulle|Morgan|Arteaga)']) + #1
lema(ur'[Dd]e_l_ (?:[AÁaá](?:rea|guila|lgebra)|ánima|a(?:rma|rca|lma|lza|gua|la|rpa|ve)|ha(?:bla|da|cha|mbre|mpa|rpa))_ la', xpos=[ur' [Mm][aá]ter']) + #1
lema(ur'[Ee]__n_n e', xpos=[ur' año', ur'\.']) + #1
lema(ur'[Ee]__s_s e', xpre=[ur'[Ll]o que ', ur'[\]\.]'], xpos=[ur' (?:eterno|el solar)']) + #1
lema(ur'[Ee]n_ _la_', xpos=[ur' (?:eglesia|lengua castellana)']) + #1
lema(ur'[Ee]st?_a_ (?:[AÁaá](?:rea|guila|lgebra)|ánima|a(?:rma|rca|lma|lza|gua|la|rpa|ve)|ha(?:da|cha|mbre|mpa|rpa))_e', xpre=[ur'del '], xpos=[ur' [Mm][aá]ter']) + #1
lema(ur'[Ff]_á_bricas? de_a', xpre=[ur'\b[Ss]e ']) + #1
lema(ur'[Ff]em_e_nin[ao]s?_i', xpre=[ur'[Mfs]\. ', ur'\bdo ', ur'prisão política ', ur'do sexo ', ur'condiçao ', ur'Sul-Americano ', ur'Identidade ', ur'Pachycephala ', ur'Miomantis ', ur'Basquete ', ur'Speocera ', ur'Zanomys ', ur'progresso ', ur'Histórias ', ur'Urethra ', ur'Profissionalização ', ur'sexualidade ', ur'Revelação ', ur'Diospyros ', ur'stephaniae ', ur'revista \'\'Alma ', ur'da escrita ', ur'Paranaense '], xpos=[ur' (?:dos|na|Masculino, uma)\b']) + #1
lema(ur'[Ll]__a_a l', xpre=[ur'dzim ', ur'tra ', ur'"', ur'[OoUu]h ', ur'Limbo ', ur'[Ll]a ', ur'lae ', ur'Sha '], xpos=[ur'[)\'\]"]', ur' (?:la|aku|jump|m )']) + #1
lema(ur'[Pp]__ara_ara p', xpos=[ur'[|\]\']']) + #1
lema(ur'[Pp]sicolog_í_as?_i', xpre=[ur'Ensaios de ', ur'em Psicopedagogia, ', ur'Viver ', ur'Um curso moderno de ', ur'\bna ', ur'\bem ', ur'\bd[ai] ', ur'\b[àae] ', ur'della ', ur'alla ', ur'Grau de ', ur'Estudiants ', ur'Sociedade ', ur'Facultat de ', ur'Paulista de '], xpos=[ur'(?:\.(?:unmsm|pt)|: (?:ciência|Reflexão)|, arte e política)', ur' (?:i|dels|geral|pune|USP|alla|da|dal|dels|dell[ae]?|em|do|de les|per|no Brasil|a (?:Granollers|Catalunya)|e (?:na|sociedade|limiti|ambiente|logica|educaçao|storia|Ciência)|del (?:llenguatge|pensament|ritratto)|Educacão|Psicoterapia Psichiatria)\b']) + #32
lema(ur'[Rr]eprogramaci_ó_n_o', xpos=[ur'\]\]es', ]) + #1
lema(ur'[Ss]__u_u s', xpre=[ur'[Ss]u '], xpos=[ur' su']) + #1
lema(ur'[Tt]_ó_tems?_o', xpre=[ur'\'\'', ur'Galería ', ur'multimedia ', ur'Evil ', ur'Dark ', ur'Tour ', ur'Poste ', ur'Jungle ', ur'Twisted ', ur'Magical ', ur'(?:[Dd]ie|his|des|Oma|[Tt]he|[Ll]es|HMS) ', ur'París, ', ur'grupo ', ur'Living ', ur'titulado ', ur'Risk ', ur'Mountain ', ur'Zapotec ', ur'Wolf ', ur'\bU ', ur'\b(?:di|de|en|[Ll]e|[Ii]l) ', ur'mejoras a ', ur'revista\)\|', ur'revista\)\|', ur'Faun\)\|', ur'película\)\|', ur'banda\)\|', ur'software\)\|', ], xpos=[ur' (?:[12] con|III|d|[Pp]oles?|Spell|Store|Lake|urbain|cómics|and|et|to|on|el [Cc][oó]mix|la revista|monumento ao|de la Bande|Wines|del Tambo|Power|Mole|Park|Games|Ocean|Press|Records|y (?:Nautilus|MPlayer|\'\'Descarga|\[\[Puma)|\((?:revista|Wines|software|desambiguación|banda|película|álbum))\b', ur'(?:: The|"|, (?:and|con|Eye|el C[oó]mix|Germans|la revista|Psiglo|Editorial)|\. L)', ]) + #344
lema(ur'[Uu]__na_na u', xpre=[ur'cada ']) + #1
lema(ur'[Uu]n__ (?:[AÁaá](?:rea|guila|lgebra)|ánima|a(?:rma|rca|lma|lza|gua|la|rpa|ve)|ha(?:da|cha|mbre|mpa|rpa))_a', xpos=[ur' [Mm][aá]ter']) + #1
lema(ur'[Uu]n_a fó_rmula_ f[oó]', xpos=[ur' (?:1|[Uu]no|compitiendo)\b', ]) + #127
lema(ur'[Uu]n_a ví_a_(?: v[ií]|a vi)', xpos=[ur' [Cc]rucis', ]) + #127
lema(ur'[Uu]n_a ó_pera_ [oó]', xpre=[ur'd[\'’]', ur'\bda ']) + #127
lema(ur'[Uu]n_a_ (?:primera|segunda|tercera)_', xpos=[ur' base', ]) + #110
lema(ur'[Uu]n_a_ bella_', xpre=[ur'per ', ]) + #10
lema(ur'[Uu]n_a_ camisa_', xpos=[ur' (?:roja|vieja)', ]) + #10
lema(ur'[Uu]n_a_ cara_', xpos=[ur' (?:o cruz|a cara)', ]) + #10
lema(ur'[Uu]n_a_ carta_', xpre=[ur'd\'']) + #10
lema(ur'[Uu]n_a_ cuenta_', xpos=[ur' (?:revoluciones|chistes|cuentos)', ]) + #10
lema(ur'[Uu]n_a_ guitarra_', xpre=[ur'reclutaron a '], xpos=[ur' (?:con el|\(Mantas|de \[\[Valdeganga)', ]) + #10
lema(ur'[Uu]n_a_ ida_', xpos=[ur' (?:y vuelta)', ]) + #10
lema(ur'[Uu]n_a_ lanza_', xpos=[ur' (?:agua|granadas|dardos|misiles|pelotas|petardos|cohetes|dardos|discos)', ]) + #10
lema(ur'[Uu]n_a_ larga_', xpos=[ur' (?:duración)', ]) + #10
lema(ur'[Uu]n_a_ mala_', xpos=[ur' (?:sangre)', ]) + #10
lema(ur'[Uu]n_a_ meta_', xpos=[ur' (?:análisis|estudio|sistema)', ]) + #10
lema(ur'[Uu]n_a_ puerta_', xpos=[ur' (?:a puerta)', ]) + #10
lema(ur'[Uu]n_a_ punta_', xpos=[ur' (?:izquierdo|derecho|pie|neto)', ]) + #10
lema(ur'[Uu]n_a_ pura_', xpos=[ur' (?:sangre|raza)', ]) + #10
lema(ur'[Uu]n_a_ toma_', xpos=[ur' y (?:daca|dame)', ]) + #10
lema(ur'[Vv]iaj_ó__o', xpre=[ur'[Yy]o '], xpos=[ur' (?:en tu|con mamá|al país)', ur'\.com']) + #1
lema(ur'[y]___ y', xpre=[ur'\]', ur'[Ll]a ', ur'\|\| ', ur'como ', ur'Eosina ', ur'Bay ', ur'Mboi[’\']', ur'= x ', ur'kurupa\'', ur'cromosoma ', ur'núcleo ', ur'R4', ur'w̃, ', ur'W e ', ur'½', ur'X o '], xpos=[ur'[=}\'\]|]', ur' (?:[:BbZzWwXxKk]|iv|ll|el aumento|mitocondrial|luego|el ADN|magia|[0-9])']) + #1
lema(ur'\b[Dd]e_ _[0-9][0-9.,]+_', xpre=[ur'[#]']) + #1
lema(ur'_El_ (?:[AÁaá](?:rea|guila|lgebra)|ánima|a(?:rma|rca|lma|lza|gua|la|rpa|ve)|ha(?:bla|da|cha|mbre|mpa|rpa))_La', xpos=[ur' (?:en gesto|[Mm][aá]ter)', ur'\'\'']) + #1
lema(ur'_L_a_Un [Ll]', xpos=[ur' (?:b[eé]mol|natural)', ur'3']) + #5
lema(ur'__la_un ', xpre=[ur'será ', ur'sería ',], xpos=[ur' (?:bemol|natural)\b', ur'(?:3|, el inicio)']) + #90
lema(ur'_e_ (?!i[ivx]|ius|imn|indios|indica|induce|ist|hiérvelo|hide|hip|high|hippies|hippy|hie|hits)h?[ií][a-záéíóúñ]+_y', xpre=[ur'>='], xpos=[ur' (?:Meteo|installer|interceptèrent|installa|ii\)|(?:ia|in) )']) + #1
lema(ur'_el_ (?:[AÁaá](?:rea|guila|lgebra)|ánima|a(?:rma|rca|lma|lza|gua|la|rpa|ve)|ha(?:bla|da|cha|mbre|mpa|rpa))_la', xpre=[ur'dióle '], xpos=[ur' [Mm][aá]ter', ur'\'\'"']) + #1
lema(ur'_el__la el' , xpre=[ur'cerul ', ur'un ']) + #1
lema(ur'_É_l (?:est(?:ar|)[aá]n?|estará|estuvo|estaban|estar[ií]an?|vienen?|fu[ée]|fueron|vendr[aá]n?|tiene|tuvo|tendrán?|es|era|serán?|fue|ha|hab[ií]a|sabe|sab[ií]a)_E', xpre=[ur'(?:ch\'|Af\')', ur'Gnet ', ur'H\''], xpos=[ur' (?:agua|esos)']) + #630
lema(ur'_É_xodos?_E', xpre=[ur'\|', ur'Trofeo del '], xpos=[ur' Salmus', ur', Excess']) + #1
lema(ur'_Ó_rdenes_O', pre=ur'(?:[Ll]as|[Uu]nas|[Ss]us) ', xpos=[ur' (?:[Mm]ilitares|[Rr]eligiosas|[Cc]iviles|[Dd]inásticas|[yi] [Dd]ecretos)']) + #1
lema(ur'_Ó_rganos?_O', xpre=[ur'\b(?:De|il) ', ur'Grand\'', ur'[DdLl][’\']', ur'Lowrey ', ur' in ', ur'per ', ur'Tetl '], xpos=[ur' (?:dei|che|para que puedam)', ur', resumido en doze']) + #1
lema(ur'_Ú_nico_U', xpre=[ur'= ', ur'[«"]', ur'\b(?:o[fr]|il) ', ur'\by ', ur'\'\' - ', ur'Amore ', ur'Girone ', ur'Hermanos ', ur'Physis ', ur'Senso ', ur'de temas ', ur'il Catalogo ', ], xpos=[ur' (?:suo|Uomo|Properties|Maho|reemplaza|Ambientale|Microfon|delle|e la|Special|Wilhem|Wilhelm|van|Glorie|National|in )', ur'(?:[\|:]|\]\]|, por)', ]) + #56
lema(ur'_é_l ante\b_e', pre=ur'[Cc]on ', xpos=[ur' último', ur' penúltimo']) + #1
lema(ur'_é_l contra\b_e', pre=ur'[Cc]on ', xpos=[ur'-(?:insulto|tenor|almirante)']) + #1
lema(ur'_é_l en\b_e', pre=ur'[Cc]on ', xpos=[ur' ese']) + #1
lema(ur'_é_l para\b_e', pre=ur'[Cc]on ', xpos=[ur' entonces', ur'-médico']) + #1
lema(ur'_í_ndices?_i', xpre=[ur'\bet ', ur'LVA ', ur'local ', ur'duplici ', ur'dell\'', ], xpos=[ur' (?:copiosissimo|locupletissimo|contenu|ad)', ur'[\'"]', ]) + lema(ur'_Í_ndices?_I', xpre=[ur' et ', ur'Double ', ur'Price ', ur'Bond ', ur'Capability ', ur'Cum', ur'[Ll]\'', ur'reagent ', ], xpos=[ur' (?:d|e sviluppo|dos|istorico|de las Glorias|Analítico dell|Virgen|generale|capitum|Nominum|rerum|copiosissimo|and|Excerptarum|nominum|seminum|botanici|et|on|ad|of|to|ac)\b', ur'”\.']) + #10
[]][0]


################# + #0

retros = [
[]][0]

reforma2010 = [
[]][0]

contenido = ""
nombreRef = dict()
alpha = ur'-_a-zA-ZáéíóúñàèìòùüâçÁÉÍÓÚÑÀÈÌÒÙÜÂÇØø0-9'
refR = re.compile((
    ur'(?:[Hh]arv|[Hh]arvn[bp]|[Hh]arvsp|[Hh]arvtxt|[Ss]fnp|[Cc]ita Harvard|[Cc]ita DRAE|[Vv]ersalita|[Bb]iblia) *\| *([' + alpha + ur'\'’,.]*?)[| }]'
    ur'|\{\{([Yy]outube|[Pp]oblación)\|'
    ur'|.*?(?:last|apellidos?|author|autor) *= *([' + alpha + ur'\'’,.]{3,}?(?: [' + alpha + ur'\'’]{2,})?)[,.:;| }]'
    ur'|.*?(?:nombre|first) *= *([' + alpha + ur'\'’,.]{3,}?(?: [' + alpha + ur'\'’]{2,})?)[,.:;| }]'
    ur'|.*https?://(?:www[0-9]*\.)?([-_a-zA-Z.0-9]+?)(?:\.(?:com|org|net|al|ar|at|au|be|bh|bo|br|bz|ca|ch|cl|cn|co|cr|cu|cz|de|dk|do|ec|ee|es|eu|fi|fr|gt|hn|ht|hu|is|it|il|in|jp|kr|lt|lv|mx|ni|nl|no|nz|pa|pe|pl|pr|pt|py|ro|ru|se|su|sv|tm|tn|tr|tv|tw|uk|us|uy|va|ve|cat|go[bv]|gouv|gub|edu|mil|blogspot|wordpress|info))*[:/ \]<]'
    ur'|.*?(?:title|título) *= *[«"“”´\']*([' + alpha + ur'\'’]{3,}?(?: [' + alpha + ur'\'’]{2,}?)?)[^' + alpha + ur'\'’]'
    ur'|.*?(?:obra|publicación|revista) *= *[«"“”´\']*([' + alpha + ur'\'’]{3,}?(?: [' + alpha + ur'\'’]{2,}?)?)\b'
    ur'|\[\[ *# *([^|]*?) *\|'
    ur'| *\[\[(?::(?:[a-z]+:)+)?([-a-zA-ZáéíóúñàèìòùüâçÁÉÍÓÚÑÀÈÌÒÙÜÂÇ\'’0-9]+?(?:[ _][-a-zA-ZáéíóúñàèìòùüâçÁÉÍÓÚÑÀÈÌÒÙÜÂÇ\'’0-9]{2,})?)[_,. \]\|#]'
    ur'| *\[\[[^\]]*?([-a-zA-ZáéíóúñàèìòùüâçÁÉÍÓÚÑÀÈÌÒÙÜÂÇ\'’0-9]{4,}?)[_,. \]\|#]'
    ur'|^[«"“”´\' [(]*(?:[A-Z][.,] *)+([' + alpha + ur'\'’]{2,}(?: [' + alpha + ur']{2,})?)[«"“”´\' .,:]'
    ur'|^[«"“”´\' [(]*([' + alpha + ur'\'’]{2,}(?: [' + alpha + ur']{2,})?)[«"“”´\' .,;:<]'))
#pagR = re.compile(ur'.*|páginas=[-0-9]+')
urls = dict()

#Referencias dobles
def reset_file(cont):
  global contenido, nombreRef, urls
  contenido = cont
  nombreRef = dict()
  if len(urls)>1000:
      urls = dict()
  
def escogerNombre(tuplas):
    if tuplas:
        for i in range(len(tuplas[0])):
            for tupla in reversed(tuplas):
                if len(tupla[i])>0:
                    return tupla[i]+"_"
    return ur'ref_duplicada_'

def ref_dup(m):
  #print("ref_dup")
  global contenido, nombreRef, refR
  ref = escogerNombre(refR.findall(m.group(1)))
  if ref in nombreRef:
      valor = nombreRef[ref]
  else:
      valor = 1
  while contenido.find(ref+str(valor))>=0:
      valor += 1
  refn = ref+str(valor)
  nombreRef[ref] = valor + 1
  return ur'<ref name="'+refn+ur'">'+m.group(1)+m.group(2)+ur'<ref name="'+refn+ur'"/>'

def checkURL(url):
    global urls
    if url in urls:
        return urls[url]
#    print(url)
    if call(['wget', '-q', '--tries=1', '--spider', url]):
        urls[url] = False
        print (url+ur' No')
        return False
    else:
        urls[url] = True
        print (url+ur' OK')
        return True

meses = {ur'1':ur'enero', ur'2':ur'febrero', ur'3':ur'marzo', ur'4':ur'abril', ur'5':ur'mayo' , ur'6':ur'junio' , ur'7':ur'julio' , ur'8':ur'agosto' , ur'9':ur'septiembre' , ur'10':ur'octubre' , ur'11':ur'noviembre' , ur'12':ur'diciembre', ur'January':ur'enero', ur'February':ur'febrero', ur'March':ur'marzo', ur'April':ur'abril', ur'May':ur'mayo' , ur'June':ur'junio' , ur'July':ur'julio' , ur'August':ur'agosto' , ur'September':ur'septiembre' , ur'October':ur'octubre' , ur'November':ur'noviembre' , ur'December':ur'diciembre'}
def hoy(*any):
    fec = date.today()
    return ur'{} de {} de {}'.format(fec.day, meses[str(fec.month)], fec.year)

def formatoFecha(m):
    try:
        return (m.group('pre')
            +ur'{} de {} de {}'
            .format(int(m.group('d')), meses[m.group('m')], int(m.group('y')))
            +m.group('pos'))
    except:
        print(ur'#{#fec:'+m.group('url')+ur'#|#'+m.group('fec')+ur'#}#')
        return (m.group('pre')
            +ur'#{#fec:'+m.group('url')+ur'#|#'+m.group('fec')+ur'#}#'
            +m.group('pos'))

def activeURL(m):
    url = m.group(1)
    if "books.google" in url:
        return ur'' if m.lastindex==1 else ur'|fechaacceso='+m.group(2)
    if checkURL(url):
        return ur'|fechaacceso='+hoy()
    else:
        return ur'' if m.lastindex==1 else ur'|fechaacceso='+m.group(2)

def desporciento(m):
    pagina = m.group(2)
    try:
        print(m.group(2))
        pagina = urllib.unquote(re.sub('_', ' ', str(pagina))).decode('utf8')
        print(pagina)
    except:
        pass
    return m.group(1)+pagina+m.group(3)
    

def pisoAEspacio(m):
    pagina = m.group(2)
    try:
        print(m.group(2))
        pagina = urllib.unquote(re.sub('_', ' ', str(pagina))).decode('utf8')
        print(pagina)
    except:
        pass
    if len(m.groups())>2:
        return ur'[[:'+m.group(1)+ur':'+pagina+ur'|'+ m.group(3)+ur']]'
    else:
        label = re.sub(ur'#.*', ur'', pagina)
    return ur'<ref>[[:'+m.group(1)+ur':'+pagina+ur'|'+label+ur']] {{'+m.group(1)+ur'}}</ref>'


# def inactiveURL(m):
#     url = m.group(1)
#     if "books.google" in url:
#         return ur''
#     if checkURL(url):
#         return ur''
#     else:
#         return ur'{{Enlace roto|'+url+ur'}}'

citaWeb = [            (ur'(?ms)(<ref[^>]*?>)\s*\[\s*https?://web\.archive\.org/web/(https?://[^\\ \]]*) ([^\]]*)\](</ref>)', ur'\1{{cita web |url=\2|título=\3|urlarchivo=http://web.archive.org/web/\2|fechaarchivo=#{#fec#}#}}\4'),
            (ur'(?ms)(<ref[^>]*?>)\s*(https?://web\.archive\.org/web/(https?://[^<]*?))(</ref>)', ur'\1{{cita web |url=\3|título=\3|urlarchivo=\2 |fechaarchivo=#{#fec#}#}}\4'),
            (ur'(?ms)(<ref[^ >]*?>)\s*\[\s*(http[s]?:[^\\ \]]*) ([^\]]*?)\s*\((?:en )?(alemán|catalán|español|francés|griego|inglés|italiano|japonés|neerlandés|polaco|portugués|rumano|ruso|sueco|turco)\)\.?\](</ref>)', ur'\1{{cita web |url=\2|título=\3|idioma=\4}}\5'),
            (ur'(?ms)(<ref[^>]*?>)\s*\[\s*(http[s]?:[^\\ \]]*) ([^\]]*?)\.?\s*\]\s*\((?:en )?(alemán|catalán|español|francés|griego|inglés|italiano|japonés|neerlandés|polaco|portugués|rumano|ruso|sueco|turco)\)\.?(</ref>)', ur'\1{{cita web |url=\2|título=\3|idioma=\4}}\5'),
            (ur'(?ms)(<ref[^>]*?>)\s*\[\s*(http[s]?:[^\\ \]<]*) ([^\]<]*)\s*\]\s*(</ref>)', ur'\1{{cita web |url=\2|título=\3}}\4'),
             #título maquillado libro google
            (ur'(?ms)(<ref[^>]*?>)\s*\[\s*(http[s]?://)(books\.google\.[-.a-zA-Z0-9]+)([^\\ \]]+?)\s*\]\s*(</ref>)',  ur'\1{{cita web |url=\2\3\4|título=Libro en \3<!-- título generado-->}}\5'),
             #título maquillado 
            (ur'(?ms)(<ref[^>]*?>)\s*\[\s*(http[s]?://)([-.a-zA-Z0-9]+)([^\\ \]]+?)\s*\]\s*(</ref>)',  ur'\1{{cita web |url=\2\3\4|título=Página en \3<!-- título generado-->}}\5'),
             #título=url
            (ur'(?ms)(<ref[^>]*?>)\s*(http[s]?:[^\\\s<]+?)\s*(</ref>)',  ur'\1{{cita web |url=\2|título=\2}}\3'),
            (ur'(?ms)(<ref[^>]*?>)\s*\[\s*(http[s]?:[^\\ \]]+?)\s*\]\s*(</ref>)',  ur'\1{{cita web |url=\2|título=\2}}\3'),
            (ur'([<]ref name="[^"]*?" *)[>][<]/ref[>]', ur'\1/>'),
] + fechas

enlacesInternos = [
 (ur'\[\[ *[Aa]([^\]|]*?) *\| *([Aa]\1) *\]\]', ur'[[\2]]'), 
 (ur'\[\[ *[Bb]([^\]|]*?) *\| *([Bb]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Cc]([^\]|]*?) *\| *([Cc]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Dd]([^\]|]*?) *\| *([Dd]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Ee]([^\]|]*?) *\| *([Ee]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Ff]([^\]|]*?) *\| *([Ff]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Gg]([^\]|]*?) *\| *([Gg]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Hh]([^\]|]*?) *\| *([Hh]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Ii]([^\]|]*?) *\| *([Ii]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Jj]([^\]|]*?) *\| *([Jj]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Kk]([^\]|]*?) *\| *([Kk]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Ll]([^\]|]*?) *\| *([Ll]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Mm]([^\]|]*?) *\| *([Mm]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Nn]([^\]|]*?) *\| *([Nn]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Ññ]([^\]|]*?) *\| *([Ññ]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Oo]([^\]|]*?) *\| *([Oo]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Pp]([^\]|]*?) *\| *([Pp]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Qq]([^\]|]*?) *\| *([Qq]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Rr]([^\]|]*?) *\| *([Rr]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Ss]([^\]|]*?) *\| *([Ss]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Tt]([^\]|]*?) *\| *([Tt]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Uu]([^\]|]*?) *\| *([Uu]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Vv]([^\]|]*?) *\| *([Vv]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Ww]([^\]|]*?) *\| *([Ww]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Xx]([^\]|]*?) *\| *([Xx]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Yy]([^\]|]*?) *\| *([Yy]\1) *\]\]', ur'[[\2]]'),
 (ur'\[\[ *[Zz]([^\]|]*?) *\| *([Zz]\1) *\]\]', ur'[[\2]]'), 
 (ur'\[\[ *[Áá]([^\]|]*?) *\| *([Áá]\1) *\]\]', ur'[[\2]]'), 
 (ur'\[\[ *[Éé]([^\]|]*?) *\| *([Éé]\1) *\]\]', ur'[[\2]]'), 
 (ur'\[\[ *[Íí]([^\]|]*?) *\| *([Íí]\1) *\]\]', ur'[[\2]]'), 
 (ur'\[\[ *[Óó]([^\]|]*?) *\| *([Óó]\1) *\]\]', ur'[[\2]]'), 
 (ur'\[\[ *[Úú]([^\]|]*?) *\| *([Úú]\1) *\]\]', ur'[[\2]]'),
] 

fixes = {
    'superfamila': {
        'regex': True,
        'saves': [],
        'msg': {
               'de':u'Bot: Korrigiere Wiki-Syntax',
               'en':u'Bot: Fixing wiki syntax',
               'es':u'Correcciones menores : [[WP:CEM]].',
              },
        'prereplacements': [],
        'postreplacements': [],
        'replacements': [
            lema(ur'[Ee](?:\.|llen)_ Pe_rez_ +Pé') + []][0],

        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre',
                'ref',
                'source',
                'syntaxhighlight',
                'code',
                'cite',
                'blockquote',
                'nowiki',
                'timeline'
            ],
            'text-contains': [
                ur'#REDIRECCIÓN',
                ur'#REDIRECT',
                ur'#Redirección',
                ur'#Redireccion',
                ur'#Redirect',
                ur'#redirección',
                ur'#redireccion',
                ur'#redirect',
            ],
        }
    },

    'referencias': {
        'regex': True,
        'recursive': True,
        'saves': [
            #Ref. externa con corchetes no balanceados 
            ur'\[\[(?:[Aa]rchivo|[Ff]ile|[Ii]magen|[Ii]image|[Mm]edi[ao]):[^]]*?\[.*?\]\]\]',
        ],
        'msg': {
               'en':u'Bot: References and links',
               'es':u'Referencias y enlaces.',
              },
        'prereplacements': [
            (ur'([<]ref +name *= *)([- _a-zA-Z0-9áéíóúñÁÉÍÓÚÑ]+?) +(group *=.*?)(/?[>])', ur'\1"\2" \3\4'),

            (ur'([<]ref +name *= *)[“”´\']*([^"/<>]+?)[“”´\']*( */?[>])', ur'\1"\2"\3'),

            (ur'([<]ref +name *= *)"[“”´\']+((?:[^"/<>]|/[^>])+?)[“”´\']+"( */?[>])', ur'\1"\2"\3'),
            (ur'([<]ref +group *= *)([- _a-zA-Z0-9áéíóúñÁÉÍÓÚÑ]+?) +(name *=.*?)(/?[>])', ur'\1"\2" \3\4'),
            (ur'([<]ref +group *= *)[“”´\']+((?:[^"/<>]|/[^>])+?)[“”´\']+ +(name *=.*?)(/?[>])', ur'\1"\2" \3\4'),
            (ur'([<]ref [^>]*?group *= *)((?:[^"/<>]|/[^>])+?) *(name *= *.*?/?[>])', ur'\1"\2" \3'),
            (ur'([<]ref [^>]*?group *= *)((?:[^"/<>]|/[^>])+?)( */?[>])', ur'\1"\2"\3'),
            (ur'([<]ref [^>]*?group *= *)"[“”´\']+([^"<>]+?)[“”´\']+" *(name *= *.*?/?[>])', ur'\1"\2" \3'),
            (ur'([<]ref [^>]*?group *= *)"[“”´\']+([^"<>]+?)[“”´\']+"( */?[>])', ur'\1"\2"\3'),
            (ur'([<]ref [^>]*?name *= *)((?:[^"/<>]|/[^>])+?)( */?[>])', ur'\1"\2"\3'),
            (ur'([<]ref [^>]*?name *= *)((?:[^"/<>]|/[^>])+?)( */?[>])', ur'\1"\2"\3'),
            (ur'([<]ref [^>]*?name *= *)"[“”´\']+([^"<>]+?)[“”´\']+"( */?[>])', ur'\1"\2"\3'),
        ],
        'postreplacements': 
        grupoPost + citaWeb + [
#             (ur'(?ms)#{#fec:([^#|]*?)#\|#([^#]*?)#}#', activeURL),
#             (ur'(?ms)#{#fec:(.*?)#}#', activeURL),
# #            (ur'(?ms)#{#roto:(.*?)#}#', inactiveURL),
#             (ur'(?ms)#{#roto:(.*?)#}#', ur''),
            (ur'(?ms)#{#fec#}#', hoy),
            (ur'(?ms)[<]ref +(name="[^"]*?" *)[>]([^<]*?[<]/ref[>])(.*?)([<]ref +\1[>])\2', ur'<ref \1>\2\3<ref \1/>'),
            (ur'([<]ref name="[^"]*?" *)[>][<]/ref[>]', ur'\1/>'),
            (ur'\[\[:(?:m:w:)?es:', ur'[['),

        ],
        'replacements': [
#           (ur'(?ms)(?P<pre><ref[^>]*>[^<]*?\|\s*url *= *(?P<url>http[s]?:[^\\\s|<]*?)\s*)\|\s*(?:fechaacceso|accessdate) *= *(?P<fec>(?P<y>[0-9]{4})-(?P<m>[0-9]{1,2})-(?P<d>[0-9]{1,2}))(?P<pos>[^<]*</ref>)', formatoFecha),
#           (ur'(?ms)(?P<pre><ref[^>]*>[^<]*?\|\s*url *= *(?P<url>http[s]?:[^\\\s|<]*?)\s*)\|\s*(?:fechaacceso|accessdate) *= *(?P<fec>(?P<y>[0-9]{4})/(?P<m>[0-9]{1,2})/(?P<d>[0-9]{1,2}))(?P<pos>[^<]*</ref>)', formatoFecha),
#           (ur'(?ms)(?P<pre><ref[^>]*>[^<]*?\|\s*url *= *(?P<url>http[s]?:[^\\\s|<]*?)\s*)\|\s*(?:fechaacceso|accessdate) *= *(?P<fec>(?P<d>[0-9]{1,2})/(?P<m>[0-9]{1,2})/(?P<y>[0-9]{4}))(?P<pos>[^<]*</ref>)', formatoFecha),
#           (ur'(?ms)(?P<pre><ref[^>]*>[^<]*?\|\s*url *= *(?P<url>http[s]?:[^\\\s|<]*?)\s*)\|\s*(?:fechaacceso|accessdate) *= *(?P<fec>(?P<d>[0-9]{1,2}) (?P<m>January|February|March|April|May|June|July|August|September|October|November|December) (?P<y>[0-9]{4}))(?P<pos>[^<]*</ref>)', formatoFecha),

            #Referencias internas
            (ur'\[\s*(?:https?:)?//((?!test)[-a-z]+)\.wikipedia\.org/wiki/((?!\?oldid|(?:[Uu]suario|[Ee]special|Wikipedia)(?::|%3A))[^][ |]+) *\| *([^][]+)\]', pisoAEspacio),
            (ur'\[\s*(?:https?:)?//((?!test)[-a-z]+)\.wikipedia\.org/wiki/((?!\?oldid|(?:[Uu]suario|[Ee]special|[Ss]pecial|[Ww]ikipedia)(?::|%3A))[^][ |]+) +([^][]+)\]', pisoAEspacio),
           # (ur'\[\s*(?:https?:)?//((?!test)[-a-z]+)\.wikipedia\.org/wiki/((?!\?oldid|(?:[Uu]suario|[Ee]special|[Ss]pecial|[Ww]ikipedia)(?::|%3A))[^][ |]+)\]', pisoAEspacio), No está listo
            (ur'(\[\[:[-a-z]+:)([^]|]*%[0-9a-fA-F]{2}[^]|]*)(\|[^]\|]+\]\])', desporciento),
            (ur'\[(\[\[[^]]+\]\])\]', ur'\1'),
            #Nombre de referencia con solo comilla a izquierda o a derecha
            (ur'([<]ref +name *= *)["][“”´\']*([^"/<>]+?)[“”´\']*( */?[>])', ur'\1"\2"\3'),
            (ur'([<]ref +name *= *)[“”´\']*([^"/<>]+?)[“”´\']*["]( */?[>])', ur'\1"\2"\3'),
            
            #Ref. externa con corchetes no balanceados 
            (ur'\[\[+ *(https?://[^][]*?) *\]+', ur'[\1]'),
            (ur'\[+ *(https?://[^][]*?) *\]\]+', ur'[\1]'),

            #Marca br
            (ur'< */ *(?P<a>[Bb][Rr]) *>', ur'<br />'),
            (ur'<br +clear *= *"?(?:all|both)"? */?>', ur'{{clear}}'),
            (ur'<br +(?:clear|align) *= *"?(left|right)"?\s*/?>', ur'{{clear|\1}}'),
            (ur'<br +style *= *"?clear *: *both *?;? *"?\s*/?>', ur'{{clear}}'),
            (ur'<br +style *= *"?clear *: *(left|right) *?;? *"?\s*/?>', ur'{{clear|\1}}'),

            #Referencias duplicadas, una de ellas con nombre
            (ur'(?ms)[<]ref (name="[^"]*?" *)[>]([^<]*?[<]/ref[>])(.*?)([<]ref[>])\2', ur'<ref \1>\2\3<ref \1/>'),
            (ur'(?ms)[<]ref[>]([^<]*?[<]/ref[>])(.*?)([<]ref name="[^"]*?" *)[>]\1', ur'\3/>\2\3>\1'),

            #Nuevas etiquetas para referencias duplicadas.
            (ur'(?ms)<ref>([^<]+</ref>)(.*?)<ref>\1', ref_dup, True),
        ] + [
            (ur'\[\[ *(.*?) *\| *\1 *\]\]', ur'[[\1]]'),
        ] + enlacesInternos +
        [[]][0],

        'exceptions': {
            'inside-tags': [
                'nowiki',
#                'comment',
                'math',
                'pre',
                'source',
                'syntaxhighlight',
                'code',
                'cite',
                'blockquote',
                'nowiki',
                'timeline'
            ],
            'text-contains': [
                ur'#REDIRECCIÓN',
                ur'#REDIRECT',
                ur'#Redireccion',
                ur'#Redirección',
                ur'#Redirect',
                ur'#redireccion',
                ur'#redirección',
                ur'#redirect',
                ur'<ref>"ibid"</ref>',
                ur'<ref>Ibid.</ref>',
                ur'<ref>Ibid</ref>',
                ur'<ref>Ibíd.</ref>',
                ur'<ref>Ibíd</ref>',
                ur'<ref>Ibídem.</ref>', 
                ur'<ref>Ibídem</ref>',
                ur'<ref>Idem.</ref>',
                ur'<ref>Idem</ref>',
                ur'<ref>Obra citada</ref>',
                ur'<ref>Op. cit.</ref>',
                ur'<ref>Sic</ref>',
                ur'<ref>\'\'Ibid.\'\'</ref>',
                ur'<ref>\'\'Ibid\'\'.</ref>', 
                ur'<ref>\'\'Ibid\'\'</ref>',
                ur'<ref>\'\'Ibidem\'\'.</ref>',
                ur'<ref>\'\'Ibidem\'\'</ref>',
                ur'<ref>\'\'Ibíd.\'\'</ref>',
                ur'<ref>\'\'Ibídem\'\'</ref>',
                ur'<ref>\'\'Idem.\'\'</ref>',
                ur'<ref>\'\'Idem\'\'.</ref>',
                ur'<ref>\'\'ibídem\'\'</ref>',
                ur'<ref>ibid.</ref>',
                ur'<ref>ibid</ref>',
                ur'<ref>ibíd</ref>',
                ur'<ref>ibídem</ref>',
                ur'<ref>idem.</ref>',
                ur'<ref>idem</ref>',
                ur'<ref>op. cit.</ref>',
                ur'<ref>sic</ref>',
                ur'<ref>Íbid.</ref>',
                ur'<ref>Íbid</ref>',
                ur'<ref>Íbidem</ref>',
                ur'<ref>íbid</ref>',
            ],
        }
    },

    'err-es': {
        'regex': True,
        'saves': noCorregirEn,
        'msg': {
               'de':u'Bot: Korrigiere Wiki-Syntax',
               'en':u'Bot: Fixing wiki syntax',
               'es':u'Pequeñas correcciones [[WP:CEM]].',
              },
        'prereplacements': grupoPre + [[(ur'\[\[ *([^]|]+?) *\| *\1 *\]\]', ur'[[\1]]')]][0],
        'postreplacements': grupoPre + grupoPost + [[(ur'\[\[ *([^]|]+?) *\| *\1 *\]\]', ur'[[\1]]')]][0],
        'replacements': 
        #  grupo1 + 
        # grupo2 + 
        # grupo3 + 
        # grupo4 + 
        # grupo5 + 
        # grupo6 + 
        # grupo7 + 
        #nuevos +
        #congelador +
        [[]][0],

        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre',
                'ref',
                'source',
                'syntaxhighlight',
                'code',
                'cite',
                'blockquote',
                'nowiki',
                'timeline'
            ],
            'text-contains': [
                ur'#REDIRECCIÓN',
                ur'#REDIRECT',
                ur'#Redirección',
                ur'#Redireccion',
                ur'#Redirect',
                ur'#redirección',
                ur'#redireccion',
                ur'#redirect',
            ],
        }
    },
    'ones-es': {
        'regex': True,
        'saves': noCorregirEn,
        'msg': {
               'de':u'Bot: Korrigiere Wiki-Syntax',
               'en':u'Bot: Fixing wiki syntax',
               'es':u'Pequeñas correcciones [[WP:CEM]].',
              },
        'prereplacements': grupoPre,
        'postreplacements': grupoPre + grupoPost ,
        'replacements': enlacesInternos + 
        grupo1 + 
        grupo2 + 
        grupo3 + 
        grupo4 + 
        grupo5 + 
        grupo6 + 
        grupo7 + 
        nuevos +
        #congelador +
        [(ur'\[\[ *([^]|]+?) *\| *\1 *\]\]', ur'[[\1]]')] + 
        [[]][0],

        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre',
                'ref',
                'source',
                'syntaxhighlight',
                'code',
                'cite',
                'blockquote',
                'nowiki',
                'timeline'
            ],
            'text-contains': [
                ur'#REDIRECCIÓN',
                ur'#REDIRECT',
                ur'#Redirección',
                ur'#Redireccion',
                ur'#Redirect',
                ur'#redirección',
                ur'#redireccion',
                ur'#redirect',
            ],
        }
    },
    'safe-es': {
        'regex': True,
        'saves': noCorregirEn,
        'msg': {
               'es':u'Pequeñas correcciones: [[WP:CEM]].',
              },
        'prereplacements': grupoPre,
        'postreplacements': grupoPre + grupoPost + enlacesInternos + 
        grupo1 + 
        grupo2 + 
        grupo3 + 
        grupo4 + 
        grupo5 + 
        grupo6 + 
        grupo7 + 
        nuevos,
        'replacements': enlacesInternos + 
        grupo1Frec +
        grupo1Mas +
        grupo2Perfecto +
        [(ur'\[\[ *([^]|]+?) *\| *\1 *\]\]', ur'[[\1]]')] + 
        [[]][0],

        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre',
                'ref',
                'source',
                'syntaxhighlight',
                'code',
                'cite',
                'blockquote',
                'nowiki',
                'timeline'
            ],
            'text-contains': [
                ur'#REDIRECCIÓN',
                ur'#REDIRECT',
                ur'#Redirección',
                ur'#Redireccion',
                ur'#Redirect',
                ur'#redirección',
                ur'#redireccion',
                ur'#redirect',
            ],
        }
    },
    # These replacements will convert HTML to wiki syntax where possible, and
    # make remaining tags XHTML compliant.
    'HTML': {
        'regex': True,
        'msg': {
            'ar':u'روبوت: تحويل/تصليح HTML',
            'be':u'Бот: карэкцыя HTML',
            'be-x-old':u'Бот: карэкцыя HTML',
            'cs':u'převod/oprava HTML',
            'en':u'Robot: Converting/fixing HTML',
            'eo':u'Bot: koredtado de HTMLa teksto',
            'fa':u'ربات:تبدیل/تصحیح کدهای اچ‌تی‌ام‌ال',
            'de':u'Bot: konvertiere/korrigiere HTML',
            'fr':u'Robot: convertit/fixe HTML',
            'he':u'בוט: ממיר/מתקן HTML',
            'ja':u'ロボットによる: HTML転換',
            'ksh':u'Bot: vun HTML en Wikikood wandelle',
            'ia':u'Robot: conversion/reparation de HTML',
            'lt':u'robotas: konvertuojamas/taisomas HTML',
            'nl':u'Bot: conversie/reparatie HTML',
            'pl':u'Robot konwertuje/naprawia HTML',
            'pt':u'Bot: Corrigindo HTML',
            'ru':u'Бот: коррекция HTML',
            'sr':u'Бот: Поправка HTML-а',
            'sv':u'Bot: Konverterar/korrigerar HTML',
            'uk':u'Бот: корекцiя HTML',
            'zh':u'機器人: 轉換HTML',
        },
        'replacements': [
            # Everything case-insensitive (?i)
            # Keep in mind that MediaWiki automatically converts <br> to <br />
            # when rendering pages, so you might comment the next two lines out
            # to save some time/edits.
            #(r'(?i)<br>',                      r'<br />'),
            # linebreak with attributes
            #(r'(?i)<br ([^>/]+?)>',            r'<br \1 />'),
            (r'(?i)<b>(.*?)</b>',              r"'''\1'''"),
            (r'(?i)<strong>(.*?)</strong>',    r"'''\1'''"),
            (r'(?i)<i>(.*?)</i>',              r"''\1''"),
            (r'(?i)<em>(.*?)</em>',            r"''\1''"),
            # horizontal line without attributes in a single line
            (r'(?i)([\r\n])<hr[ /]*>([\r\n])', r'\1----\2'),
            # horizontal line without attributes with more text in the same line
            #(r'(?i) +<hr[ /]*> +',             r'\r\n----\r\n'),
            # horizontal line with attributes; can't be done with wiki syntax
            # so we only make it XHTML compliant
            (r'(?i)<hr ([^>/]+?)>',            r'<hr \1 />'),
            # a header where only spaces are in the same line
            (r'(?i)([\r\n]) *<h1> *([^<]+?) *</h1> *([\r\n])',  r"\1= \2 =\3"),
            (r'(?i)([\r\n]) *<h2> *([^<]+?) *</h2> *([\r\n])',  r"\1== \2 ==\3"),
            (r'(?i)([\r\n]) *<h3> *([^<]+?) *</h3> *([\r\n])',  r"\1=== \2 ===\3"),
            (r'(?i)([\r\n]) *<h4> *([^<]+?) *</h4> *([\r\n])',  r"\1==== \2 ====\3"),
            (r'(?i)([\r\n]) *<h5> *([^<]+?) *</h5> *([\r\n])',  r"\1===== \2 =====\3"),
            (r'(?i)([\r\n]) *<h6> *([^<]+?) *</h6> *([\r\n])',  r"\1====== \2 ======\3"),
            # TODO: maybe we can make the bot replace <p> tags with \r\n's.
        ]
        ,
        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre'
            ],
        }
    },

    # Grammar fixes for German language
    # Do NOT run this automatically!
    'grammar-de': {
        'regex': True,
        'msg': {
            'de':u'Bot: korrigiere Grammatik',
        },
        'replacements': [
            #(u'([Ss]owohl) ([^,\.]+?), als auch',                                                            r'\1 \2 als auch'),
            #(u'([Ww]eder) ([^,\.]+?), noch', r'\1 \2 noch'),
            #
            # Vorsicht bei Substantiven, z. B. 3-Jähriger!
            (u'(\d+)(minütig|stündig|tägig|wöchig|jährig|minütlich|stündlich|täglich|wöchentlich|jährlich|fach|mal|malig|köpfig|teilig|gliedrig|geteilt|elementig|dimensional|bändig|eckig|farbig|stimmig)', r'\1-\2'),
            # zusammengesetztes Wort, Bindestrich wird durchgeschleift
            (u'(?<!\w)(\d+|\d+[\.,]\d+)(\$|€|DM|£|¥|mg|g|kg|ml|cl|l|t|ms|min|µm|mm|cm|dm|m|km|ha|°C|kB|MB|GB|TB|W|kW|MW|GW|PS|Nm|eV|kcal|mA|mV|kV|Ω|Hz|kHz|MHz|GHz|mol|Pa|Bq|Sv|mSv)([²³]?-[\w\[])',           r'\1-\2\3'),
            # Größenangabe ohne Leerzeichen vor Einheit
            # weggelassen wegen vieler falsch Positiver: s, A, V, C, S, J, %
            (u'(?<!\w)(\d+|\d+[\.,]\d+)(\$|€|DM|£|¥|mg|g|kg|ml|cl|l|t|ms|min|µm|mm|cm|dm|m|km|ha|°C|kB|MB|GB|TB|W|kW|MW|GW|PS|Nm|eV|kcal|mA|mV|kV|Ω|Hz|kHz|MHz|GHz|mol|Pa|Bq|Sv|mSv)(?=\W|²|³|$)',          r'\1 \2'),
            # Temperaturangabe mit falsch gesetztem Leerzeichen
            (u'(?<!\w)(\d+|\d+[\.,]\d+)° C(?=\W|²|³|$)',          ur'\1 °C'),
            # Kein Leerzeichen nach Komma
            (u'([a-zäöüß](\]\])?,)((\[\[)?[a-zäöüA-ZÄÖÜ])',                                                                          r'\1 \3'),
            # Leerzeichen und Komma vertauscht
            (u'([a-zäöüß](\]\])?) ,((\[\[)?[a-zäöüA-ZÄÖÜ])',                                                                          r'\1, \3'),
            # Plenks (d. h. Leerzeichen auch vor dem Komma/Punkt/Ausrufezeichen/Fragezeichen)
            # Achtung bei Französisch: http://de.wikipedia.org/wiki/Plenk#Sonderfall_Franz.C3.B6sisch
            # Leerzeichen vor Doppelpunkt/Semikolon kann korrekt sein, nach irgendeiner Norm für Zitationen.
            (u'([a-zäöüß](\]\])?) ([,\.!\?]) ((\[\[)?[a-zäöüA-ZÄÖÜ])',                                                                          r'\1\3 \4'),
            #(u'([a-z]\.)([A-Z])',                                                                             r'\1 \2'),
        ],
        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre',           # because of code examples
                'source',        # because of code examples
                'startspace',    # because of code examples
                'hyperlink',     # e.g. commas in URLs
                'gallery',       # because of filenames
                'timeline',
            ],
            'text-contains': [
                r'sic!',
                r'20min.ch',     # Schweizer News-Seite
            ],
            'inside': [
                r'<code>.*</code>', # because of code examples
                r'{{[Zz]itat\|.*?}}',
                ur'{{§\|.*?}}',  # Gesetzesparagraph
                ur'§ ?\d+[a-z]',  # Gesetzesparagraph
                r'Ju 52/1m', # Flugzeugbezeichnung
                r'Ju 52/3m', # Flugzeugbezeichnung
                r'AH-1W',    # Hubschrauberbezeichnung
                r'ZPG-3W',   # Luftschiffbezeichnung
                r'8mm',      # Filmtitel
                r'802.11g',  # WLAN-Standard
                r'DOS/4GW',  # Software
                r'ntfs-3g',  # Dateisystem-Treiber
                r'/\w(,\w)*/',     # Laut-Aufzählung in der Linguistik
                r'[xyz](,[xyz])+', # Variablen in der Mathematik (unklar, ob Leerzeichen hier Pflicht sind)
                r'(?m)^;(.*?)$', # Definitionslisten, dort gibt es oft absichtlich Leerzeichen vor Doppelpunkten
                r'\d+h( |&nbsp;)\d+m', # Schreibweise für Zeiten, vor allem in Film-Infoboxen. Nicht korrekt, aber dafür schön kurz.
                r'(?i)\[\[(Bild|Image|Media):.+?\|', # Dateinamen auslassen
                r'{{bgc\|.*?}}',  # Hintergrundfarbe
                r'<sup>\d+m</sup>',                   # bei chemischen Formeln
                r'\([A-Z][A-Za-z]*(,[A-Z][A-Za-z]*(<sup>.*?</sup>|<sub>.*?</sub>|))+\)' # chemische Formel, z. B. AuPb(Pb,Sb,Bi)Te. Hier sollen keine Leerzeichen hinter die Kommata.
            ],
            'title': [
                r'Arsen',  # chemische Formel
            ],
        }
    },

    # Do NOT run this automatically!
    # Recommendation: First run syntax-safe automatically, afterwards
    # run syntax manually, carefully checking that you're not breaking
    # anything.
    'syntax': {
        'regex': True,
        'msg': {
            'ar':u'بوت: تصليح تهيئة الويكي',
            'be':u'Бот: Карэкцыя вiкi-сiнтаксiсу',
            'be-x-old':u'Бот выпраўляе вiкi-сынтаксiс',
            'cs':u'Oprava wikisyntaxe',
            'de':u'Bot: Korrigiere Wiki-Syntax',
            'en':u'Robot: Fixing wiki syntax',
            'eo':u'Bot: Korektado de vikia sintakso',
            'fa':u'ربات:تصحیح قالب ویکی‌نویسی',
            'fr':u'Bot: Corrige wiki-syntaxe',
            'he':u'בוט: מתקן תחביר ויקי',
            'ia':u'Robot: Reparation de syntaxe wiki',
            'ja':u'ロボットによる: wiki構文修正',
            'lt':u'robotas: Taisoma wiki sintaksė',
            'nl':u'Bot: reparatie wikisyntaxis',
            'pl':u'Robot poprawia wiki-składnię',
            'pt':u'Bot: Corrigindo sintaxe wiki',
            'ru':u'Бот: Коррекция вики синтаксиса',
            'sr':u'Бот: Поправка вики синтаксе',
            'uk':u'Бот: Корекцiя вiкi-синтаксису',
            'zh':u'機器人: 修正wiki語法',
        },
        'replacements': [
            # external link in double brackets
            (r'\[\[(?P<url>https?://[^\]]+?)\]\]',   r'[\g<url>]'),
            # external link starting with double bracket
            (r'\[\[(?P<url>https?://.+?)\]',   r'[\g<url>]'),
            # external link with forgotten closing bracket
            #(r'\[(?P<url>https?://[^\]\s]+)\r\n',  r'[\g<url>]\r\n'),
            # external link ending with double bracket.
            # do not change weblinks that contain wiki links inside
            # inside the description
            (r'\[(?P<url>https?://[^\[\]]+?)\]\](?!\])',   r'[\g<url>]'),
            # external link and description separated by a dash.
            # ATTENTION: while this is a mistake in most cases, there are some
            # valid URLs that contain dashes!
            (r'\[(?P<url>https?://[^\|\]\s]+?) *\| *(?P<label>[^\|\]]+?)\]', r'[\g<url> \g<label>]'),
            # wiki link closed by single bracket.
            # ATTENTION: There are some false positives, for example
            # Brainfuck code examples or MS-DOS parameter instructions.
            # There are also sometimes better ways to fix it than
            # just putting an additional ] after the link.
            (r'\[\[([^\[\]]+?)\](?!\])',  r'[[\1]]'),
            # wiki link opened by single bracket.
            # ATTENTION: same as above.
            (r'(?<!\[)\[([^\[\]]+?)\]\](?!\])',  r'[[\1]]'),
            # template closed by single bracket
            # ATTENTION: There are some false positives, especially in
            # mathematical context or program code.
            (r'{{([^{}]+?)}(?!})',       r'{{\1}}'),
        ],
        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre',
                'source',        # because of code examples
                'startspace',    # because of code examples
            ],
            'text-contains': [
                r'http://.*?object=tx\|',               # regular dash in URL
                r'http://.*?allmusic\.com',             # regular dash in URL
                r'http://.*?allmovie\.com',             # regular dash in URL
                r'http://physics.nist.gov/',            # regular dash in URL
                r'http://www.forum-seniorenarbeit.de/', # regular dash in URL
                r'http://kuenstlerdatenbank.ifa.de/',   # regular dash in URL
                r'&object=med',                         # regular dash in URL
                r'\[CDATA\['                            # lots of brackets
            ],
        }
    },

    # The same as syntax, but restricted to replacements that should
    # be safe to run automatically.
    'syntax-safe': {
        'regex': True,
        'msg': {
            'ar':u'بوت: تصليح تهيئة الويكي',
            'be':u'Бот: Карэкцыя вiкi-сiнтаксiсу',
            'be-x-old':u'Бот выпраўляе вiкi-сынтаксiс',
            'cs':u'Oprava wikisyntaxe',
            'de':u'Bot: Korrigiere Wiki-Syntax',
            'en':u'Robot: Fixing wiki syntax',
            'eo':u'Bot: Korektado de vikia sintakso',
            'fa':u'ربات:تصحیح قالب ویکی‌نویسی',
            'fr':u'Bot: Corrige wiki-syntaxe',
            'he':u'בוט: מתקן תחביר ויקי',
            'ia':u'Robot: Reparation de syntaxe wiki',
            'ja':u'ロボットによる: wiki構文修正',
            'lt':u'robotas: Taisoma wiki sintaksė',
            'nl':u'Bot: reparatie wikisyntaxis',
            'pl':u'Robot poprawia wiki-składnię',
            'pt':u'Bot: Corrigindo sintaxe wiki',
            'ru':u'Бот: Коррекция вики синтаксиса',
            'sr':u'Бот: Поправка вики синтаксе',
            'uk':u'Бот: Корекцiя вiкi-синтаксису',
            'zh':u'機器人: 修正wiki語法',
        },
        'replacements': [
            # external link in double brackets
            (r'\[\[(?P<url>https?://[^\]]+?)\]\]',   r'[\g<url>]'),
            # external link starting with double bracket
            (r'\[\[(?P<url>https?://.+?)\]',   r'[\g<url>]'),
            # external link with forgotten closing bracket
            #(r'\[(?P<url>https?://[^\]\s]+)\r\n',   r'[\g<url>]\r\n'),
            # external link and description separated by a dash, with
            # whitespace in front of the dash, so that it is clear that
            # the dash is not a legitimate part of the URL.
            (r'\[(?P<url>https?://[^\|\] \r\n]+?) +\| *(?P<label>[^\|\]]+?)\]', r'[\g<url> \g<label>]'),
            # dash in external link, where the correct end of the URL can
            # be detected from the file extension. It is very unlikely that
            # this will cause mistakes.
            (r'\[(?P<url>https?://[^\|\] ]+?(\.pdf|\.html|\.htm|\.php|\.asp|\.aspx|\.jsp)) *\| *(?P<label>[^\|\]]+?)\]', r'[\g<url> \g<label>]'),
        ],
        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre',
                'source',        # because of code examples
                'startspace',    # because of code examples
            ],
        }
    },

    'case-de': { # German upper / lower case issues
        'regex': True,
        'msg': {
            'de':u'Bot: Korrigiere Groß-/Kleinschreibung',
        },
        'replacements': [
            (r'\batlantische(r|n|) Ozean', r'Atlantische\1 Ozean'),
            (r'\bdeutsche(r|n|) Bundestag\b', r'Deutsche\1 Bundestag'),
            (r'\bdeutschen Bundestags\b', r'Deutschen Bundestags'), # Aufpassen, z. B. 'deutsche Bundestagswahl'
            (r'\bdeutsche(r|n|) Reich\b', r'Deutsche\1 Reich'),
            (r'\bdeutschen Reichs\b', r'Deutschen Reichs'), # Aufpassen, z. B. 'deutsche Reichsgrenzen'
            (r'\bdritte(n|) Welt(?!krieg)', r'Dritte\1 Welt'),
            (r'\bdreißigjährige(r|n|) Krieg', r'Dreißigjährige\1 Krieg'),
            (r'\beuropäische(n|) Gemeinschaft', r'Europäische\1 Gemeinschaft'),
            (r'\beuropäische(n|) Kommission', r'Europäische\1 Kommission'),
            (r'\beuropäische(n|) Parlament', r'Europäische\1 Parlament'),
            (r'\beuropäische(n|) Union', r'Europäische\1 Union'),
            (r'\berste(r|n|) Weltkrieg', r'Erste\1 Weltkrieg'),
            (r'\bkalte(r|n|) Krieg', r'Kalte\1 Krieg'),
            (r'\bpazifische(r|n|) Ozean', r'Pazifische\1 Ozean'),
            (r'Tag der deutschen Einheit', r'Tag der Deutschen Einheit'),
            (r'\bzweite(r|n|) Weltkrieg', r'Zweite\1 Weltkrieg'),
        ],
        'exceptions': {
            'inside-tags': [
                'nowiki',
                'comment',
                'math',
                'pre',
            ],
            'text-contains': [
                r'sic!',
            ],
        }
    },

    'vonbis': {
        'regex': True,
        'msg': {
            'de':u'Bot: Ersetze Binde-/Gedankenstrich durch "bis"',
        },
        'replacements': [
            # Bindestrich, Gedankenstrich, Geviertstrich
            (u'(von \d{3,4}) *(-|&ndash;|–|&mdash;|—) *(\d{3,4})', r'\1 bis \3'),
        ],
    },

    # some disambiguation stuff for de:
    # python replace.py -fix:music-de -subcat:Album
    'music-de': {
        'regex': False,
        'msg': {
            'de':u'Bot: korrigiere Links auf Begriffsklärungen',
        },
        'replacements': [
            (u'[[CD]]', u'[[Audio-CD|CD]]'),
            (u'[[LP]]', u'[[Langspielplatte|LP]]'),
            (u'[[EP]]', u'[[Extended Play|EP]]'),
            (u'[[MC]]', u'[[Musikkassette|MC]]'),
            (u'[[Single]]', u'[[Single (Musik)|Single]]'),
        ],
        'exceptions': {
            'inside-tags': [
                'hyperlink',
            ]
        }
    },

    # format of dates of birth and death, for de:
    # python replace.py -fix:datum-de -ref:Vorlage:Personendaten
    'datum-de': {
        'regex': True,
        'msg': {
            'de': u'Bot: Korrigiere Datumsformat',
        },
        'replacements': [
            # space after birth sign w/ year
            #(u'\(\*(\d{3,4})', u'(* \\1'),
            ## space after death sign w/ year
            #(u'†(\d{3,4})', u'† \\1'),
            #(u'&dagger;(\d{3,4})', u'† \\1'),
            ## space after birth sign w/ linked date
            #(u'\(\*\[\[(\d)', u'(* [[\\1'),
            ## space after death sign w/ linked date
            #(u'†\[\[(\d)', u'† [[\\1'),
            #(u'&dagger;\[\[(\d)', u'† [[\\1'),
            (u'\[\[(\d+\. (?:Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)) (\d{1,4})\]\]', u'[[\\1]] [[\\2]]'),
            # Keine führende Null beim Datum (ersteinmal nur bei denen, bei denen auch ein Leerzeichen fehlt)
            (u'0(\d+)\.(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)', r'\1. \2'),
            # Kein Leerzeichen zwischen Tag und Monat
            (u'(\d+)\.(Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)', r'\1. \2'),
            # Kein Punkt vorm Jahr
            (u'(\d+)\. (Januar|Februar|März|April|Mai|Juni|Juli|August|September|Oktober|November|Dezember)\.(\d{1,4})', r'\1. \2 \3'),
        ],
        'exceptions': {
            'inside': [
                r'\[\[20. Juli 1944\]\]', # Hitler-Attentat
                r'\[\[17. Juni 1953\]\]', # Ost-Berliner Volksaufstand
                r'\[\[1. April 2000\]\]', # Film
                r'\[\[11. September 2001\]\]', # Anschläge in den USA
                r'\[\[7. Juli 2005\]\]',  # Terroranschläge in Spanien
            ],
        }
    },

    'isbn': {
        'regex': True,
        'msg': 'isbn-formatting', # use i18n translations
        'replacements': [
            # colon
            (r'ISBN: (\d+)', r'ISBN \1'),
            # superfluous word "number"
            (r'ISBN( number| no\.?| No\.?|-Nummer|-Nr\.):? (\d+)', r'ISBN \2'),
            # Space, minus, dot,  hypen, en dash, em dash, etc. instead of
            # hyphen-minus as separator, or spaces between digits and separators.
            # Note that these regular expressions also match valid ISBNs, but
            # these won't be changed.
            (ur'ISBN (978|979) *[\- −\.‐-―] *(\d+) *[\- −\.‐-―] *(\d+) *[\- −\.‐-―] *(\d+) *[\- −\.‐-―] *(\d)(?!\d)', r'ISBN \1-\2-\3-\4-\5'), # ISBN-13
            (ur'ISBN (\d+) *[\- −\.‐-―] *(\d+) *[\- −\.‐-―] *(\d+) *[\- −\.‐-―] *(\d|X|x)(?!\d)', r'ISBN \1-\2-\3-\4'), # ISBN-10
            # missing space before ISBN-10 or before ISBN-13,
            # or non-breaking space.
            (r'ISBN(|&nbsp;| )((\d(-?)){12}\d|(\d(-?)){9}[\dXx])', r'ISBN \2'),
        ],
        'exceptions': {
            'inside-tags': [
                'comment',
                'hyperlink',
            ],
            'inside': [
                r'ISBN (\d(-?)){12}\d',    # matches valid ISBN-13s
                r'ISBN (\d(-?)){9}[\dXx]', # matches valid ISBN-10s
            ],
        }
    },

    #Corrections for Arabic Wikipedia and any Arabic wiki.
    #python replace.py -fix:correct-ar -start:! -always

    'correct-ar': {
        'regex': True,
        'msg': {
            'ar':u'تدقيق إملائي',
        },
        'replacements': [
            #(u' ,', u' ،'), #FIXME: Do not replace comma in non-Arabic text, interwiki, image links or <math> syntax.
            (ur'\bإمرأة\b', u'امرأة'),
            (ur'\bالى\b', ur'إلى'),
            (ur'\bإسم\b', u'اسم'),
            (ur'\bالأن\b', u'الآن'),
            (ur'\bالة\b', u'آلة'),
            (ur'\bفى\b', u'في'),
            (ur'\bإبن\b', u'ابن'),
            (ur'\bإبنة\b', u'ابنة'),
            (ur'\bإقتصاد\b', u'اقتصاد'),
            (ur'\bإجتماع\b', u'اجتماع'),
            (ur'\bانجيل\b', u'إنجيل'),
            (ur'\bاجماع\b', u'إجماع'),
            (ur'\bاكتوبر\b', u'أكتوبر'),
            (ur'\bإستخراج\b', u'استخراج'),
            (ur'\bإستعمال\b', u'استعمال'),
            (ur'\bإستبدال\b', u'استبدال'),
            (ur'\bإشتراك\b', u'اشتراك'),
            (ur'\bإستعادة\b', u'استعادة'),
            (ur'\bإستقلال\b', u'استقلال'),
            (ur'\bإنتقال\b', u'انتقال'),
            (ur'\bإتحاد\b', u'اتحاد'),
            (ur'\bاملاء\b', u'إملاء'),
            (ur'\bإستخدام\b', u'استخدام'),
            (ur'\bأحدى\b', u'إحدى'),
            (ur'\bلاكن\b', u'لكن'),
            (ur'\bإثنان\b', u'اثنان'),
            (ur'\bإحتياط\b', u'احتياط'),
            (ur'\bإقتباس\b', u'اقتباس'),
            (ur'\bادارة\b', u'إدارة'),
            (ur'\bابناء\b', u'أبناء'),
            (ur'\bالانصار\b', u'الأنصار'),
            (ur'\bاشارة\b', u'إشارة'),
            (ur'\bإقرأ\b', u'اقرأ'),
            (ur'\bإمتياز\b', u'امتياز'),
            (ur'\bارق\b', u'أرق'),
            (ur'\bاللة\b', u'الله'),
            (ur'\bإختبار\b', u'اختبار'),
            (ur'==[ ]?روابط خارجية[ ]?==', u'== وصلات خارجية =='),
            (ur'\bارسال\b', u'إرسال'),
            (ur'\bإتصالات\b', u'اتصالات'),
            (ur'\bابو\b', u'أبو'),
            (ur'\bابا\b', u'أبا'),
            (ur'\bاخو\b', u'أخو'),
            (ur'\bاخا\b', u'أخا'),
            (ur'\bاخي\b', u'أخي'),
            (ur'\bاحد\b', u'أحد'),
            (ur'\bاربعاء\b', u'أربعاء'),
            (ur'\bاول\b', u'أول'),
            (ur'\b(ال|)اهم\b', ur'\1أهم'),
            (ur'\b(ال|)اثقل\b', ur'\1أثقل'),
            (ur'\b(ال|)امجد\b', ur'\1أمجد'),
            (ur'\b(ال|)اوسط\b', ur'\1أوسط'),
            (ur'\b(ال|)اشقر\b', ur'\1أشقر'),
            (ur'\b(ال|)انور\b', ur'\1أنور'),
            (ur'\b(ال|)اصعب\b', ur'\1أصعب'),
            (ur'\b(ال|)اسهل\b', ur'\1أسهل'),
            (ur'\b(ال|)اجمل\b', ur'\1أجمل'),
            (ur'\b(ال|)اقبح\b', ur'\1أقبح'),
            (ur'\b(ال|)اطول\b', ur'\1أطول'),
            (ur'\b(ال|)اقصر\b', ur'\1أقصر'),
            (ur'\b(ال|)اسمن\b', ur'\1أسمن'),
            (ur'\b(ال|)اذكى\b', ur'\1أذكى'),
            (ur'\b(ال|)اكثر\b', ur'\1أكثر'),
            (ur'\b(ال|)افضل\b', ur'\1أفضل'),
            (ur'\b(ال|)اكبر\b', ur'\1أكبر'),
            (ur'\b(ال|)اشهر\b', ur'\1أشهر'),
            (ur'\b(ال|)ابطأ\b', ur'\1أبطأ'),
            (ur'\b(ال|)اماني\b', ur'\1أماني'),
            (ur'\b(ال|)احلام\b', ur'\1أحلام'),
            (ur'\b(ال|)اسماء\b', ur'\1أسماء'),
            (ur'\b(ال|)اسامة\b', ur'\1أسامة'),
            (ur'\bابراهيم\b', u'إبراهيم'),
            (ur'\bاسماعيل\b', u'إسماعيل'),
            (ur'\bايوب\b', u'أيوب'),
            (ur'\bايمن\b', u'أيمن'),
            (ur'\bاوزبكستان\b', u'أوزبكستان'),
            (ur'\bاذربيجان\b', u'أذربيجان'),
            (ur'\bافغانستان\b', u'أفغانستان'),
            (ur'\bانجلترا\b', u'إنجلترا'),
            (ur'\bايطاليا\b', u'إيطاليا'),
            (ur'\bاوربا\b', u'أوروبا'),
            (ur'\bأوربا\b', u'أوروبا'),
            (ur'\bاوغندة\b', u'أوغندة'),
            (ur'\b(ال|)ا(لماني|فريقي|سترالي)(ا|ة|تان|ان|ين|ي|ون|و|ات|)\b', ur'\1أ\2\3'),
            (ur'\b(ال|)ا(وروب|مريك)(ا|ي|ية|يتان|يان|يين|يي|يون|يو|يات|)\b', ur'\1أ\2\3'),
            (ur'\b(ال|)ا(ردن|رجنتين|وغند|سبان|وكران|فغان)(ي|ية|يتان|يان|يين|يي|يون|يو|يات|)\b', ur'\1أ\2\3'),
            (ur'\b(ال|)ا(سرائيل|يران|مارات|نكليز|نجليز)(ي|ية|يتان|يان|يين|يي|يون|يو|يات|)\b', ur'\1إ\2\3'),
            (ur'\b(ال|)(ا|أ)(رثوذكس|رثوذوكس)(ي|ية|يتان|يان|يين|يي|يون|يو|يات|)\b', ur'\1أرثوذكس\4'),
            (ur'\bإست(عمل|خدم|مر|مد|مال|عاض|قام|حال|جاب|قال|زاد|عان|طال)(ت|ا|وا|)\b', ur'است\1\2'),
            (ur'\bإست(حال|قال|طال|زاد|عان|قام|راح|جاب|عاض|مال)ة\b', ur'است\1ة'),
        ],
        'exceptions': {
            'inside-tags': [
                'interwiki',
                'math',
                'ref',
            ],
        }
    },
    'specialpages': {
        'regex': False,
        'msg': {
            'en': u'Robot: Fixing special page capitalisation',
            'fa':u'ربات: تصحیح بزرگی و کوچکی حروف صفحه‌های ویژه',
        },
        'replacements': [
            (u'Special:Allpages',        u'Special:AllPages'),
            (u'Special:Blockip',         u'Special:BlockIP'),
            (u'Special:Blankpage',       u'Special:BlankPage'),
            (u'Special:Filepath',        u'Special:FilePath'),
            (u'Special:Globalusers',     u'Special:GlobalUsers'),
            (u'Special:Imagelist',       u'Special:ImageList'),
            (u'Special:Ipblocklist',     u'Special:IPBlockList'),
            (u'Special:Listgrouprights', u'Special:ListGroupRights'),
            (u'Special:Listusers',       u'Special:ListUsers'),
            (u'Special:Newimages',       u'Special:NewImages'),
            (u'Special:Prefixindex',     u'Special:PrefixIndex'),
            (u'Special:Protectedpages',  u'Special:ProtectedPages'),
            (u'Special:Recentchanges',   u'Special:RecentChanges'),
            (u'Special:Specialpages',    u'Special:SpecialPages'),
            (u'Special:Unlockdb',        u'Special:UnlockDB'),
            (u'Special:Userlogin',       u'Special:UserLogin'),
            (u'Special:Userlogout',      u'Special:UserLogout'),
            (u'Special:Whatlinkshere',   u'Special:WhatLinksHere'),
        ],
    },
    # yu top-level domain was disabled in 2010,
    # see http://lists.wikimedia.org/pipermail/wikibots-l/2009-February/000290.html
    # The following are domains that are often-used.
    'yu-tld': {
        'regex': False,
        'nocase': True,
        'msg': {
            'de': u'Bot: Ersetze Links auf .yu-Domains',
            'en': u'Robot: Replacing links to .yu domains',
            'fa': u'ربات: جایگزینی پیوندها به دامنه‌ها با پسوند yu',
            'fr': u'Robot: Correction des liens pointant vers le domaine .yu, qui expire en 2009',
            'ksh': u'Bot: de ahle .yu-Domains loufe us, dröm ußjetuusch',
         },
         'replacements': [
            (u'www.budva.cg.yu',             u'www.budva.rs'),
            (u'spc.org.yu',                  u'spc.rs'),
            (u'www.oks.org.yu',              u'www.oks.org.rs'),
            (u'www.kikinda.org.yu',          u'www.kikinda.rs'),
            (u'www.ds.org.yu',               u'www.ds.org.rs'),
            (u'www.nbs.yu',                  u'www.nbs.rs'),
            (u'www.serbia.sr.gov.yu',        u'www.srbija.gov.rs'),
            (u'eunet.yu',                    u'eunet.rs'),
            (u'www.zastava-arms.co.yu',      u'www.zastava-arms.co.rs'),
            (u'www.airportnis.co.yu',        u'www.airportnis.rs'),
            # (u'www.danas.co.yu',             u'www.danas.rs'), # Archive links don't seem to work
            (u'www.belex.co.yu',             u'www.belex.rs'),
            (u'beograd.org.yu',              u'beograd.rs'),
            (u'www.vlada.cg.yu',             u'www.vlada.me'),
            (u'webrzs.statserb.sr.gov.yu',   u'webrzs.stat.gov.rs'),
            (u'www.statserb.sr.gov.yu',      u'webrzs.stat.gov.rs'),
            (u'www.rastko.org.yu',           u'www.rastko.org.rs'),
            (u'www.reprezentacija.co.yu',    u'www.reprezentacija.rs'),
            (u'www.blic.co.yu',              u'www.blic.co.rs'),
            (u'www.beograd.org.yu',          u'www.beograd.org.rs'),
            (u'arhiva.glas-javnosti.co.yu',  u'arhiva.glas-javnosti.rs'),
            (u'www.srpsko-nasledje.co.yu',   u'www.srpsko-nasledje.co.rs'),
            (u'www.dnevnik.co.yu',           u'www.dnevnik.rs'),
            (u'www.srbija.sr.gov.yu',        u'www.srbija.gov.rs'),
            (u'www.kurir-info.co.yu/Arhiva', u'arhiva.kurir-info.rs/Arhiva'),
            (u'www.kurir-info.co.yu/arhiva', u'arhiva.kurir-info.rs/arhiva'),
            (u'www.kurir-info.co.yu',        u'www.kurir-info.rs'),
            (u'arhiva.kurir-info.co.yu',     u'arhiva.kurir-info.rs'),
            (u'www.prvaliga.co.yu',          u'www.prvaliga.rs'),
            (u'www.mitropolija.cg.yu',       u'www.mitropolija.me'),
            (u'www.spc.yu/sr',               u'www.spc.rs/sr'),
            (u'www.sk.co.yu',                u'www.sk.co.rs'),
            (u'www.ekoforum.org.yu',         u'www.ekoforum.org'),
            (u'www.svevlad.org.yu',          u'www.svevlad.org.rs'),
            (u'www.posta.co.yu',             u'www.posta.rs'),
            (u'www.glas-javnosti.co.yu',     u'www.glas-javnosti.rs'),
            (u'www.fscg.cg.yu',              u'www.fscg.co.me'),
            (u'ww1.rts.co.yu/euro',          u'ww1.rts.co.rs/euro'),
            (u'www.rtv.co.yu',               u'www.rtv.rs'),
            (u'www.politika.co.yu',          u'www.politika.rs'),
            (u'www.mfa.gov.yu',              u'www.mfa.gov.rs'),
            (u'www.drzavnauprava.sr.gov.yu', u'www.drzavnauprava.gov.rs'),
        ],
    },
    # These replacements will convert HTML tag from FCK-editor to wiki syntax.
    #
    'fckeditor': {
        'regex': True,
        'msg': {
            'en': u'Robot: Fixing rich-editor html',
            'fa': u'ربات: تصحیح اچ‌تی‌ام‌ال ویرایشگر پیشرفته',
         },
         'replacements': [
            # replace <br> with a new line
            (r'(?i)<br>',                      r'\n'),
            # replace &nbsp; with a space
            (r'(?i)&nbsp;',                      r' '),
        ],
    },
}

#
# Load the user fixes file.

import config

try:
    execfile(config.datafilepath(config.base_dir, "user-fixes.py"))
except IOError:
    pass

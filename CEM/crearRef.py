#-*- coding: utf-8  -*-
import re, string
import fileinput, codecs, sys

#Reconocimiento de referencias.
apeNomFecTitR = re.compile(ur'(?P<ape>[^,]+), (?P<nom>[^(]+?) \((?P<fec>[0-9]+)\):? (?:"|\'\')(?P<tit>.+?)(?:"|\'\')')
volR = re.compile(ur' vol\. ([-0-9]+)[,.]')
numR = re.compile(ur' no\. ([-0-9]+)[,.]')
ppR = re.compile(ur' pp\. ([-0-9]+)[,.]')
edR = re.compile(ur' ed\. by ([^,.]+)[,.]')
inR = re.compile(ur' In (?:"|\'\')([^\'"]+)(?:"|\'\')')
def crearRef(ref):
    apeNomFecTitL = apeNomFecTitR.findall(ref)
    volL = volR.findall(ref)
    numL = numR.findall(ref)
    ppL = ppR.findall(ref)
    edL = edR.findall(ref)
    inL = inR.findall(ref)
    apeV = nomV = fecV = titV = volV = numV = ppV = otrosV = inV = ur''
    if apeNomFecTitL:
        apeV = apeNomFecTitL[0][0]
        nomV = apeNomFecTitL[0][1]
        fecV = apeNomFecTitL[0][2]
        titV = apeNomFecTitL[0][3]
    if volL:
        volV = volL[0]
    if numL:
        numV = numL[0]
    if ppL:
        ppV = ppL[0]
    if edL:
        otrosV = ur'|nombre-editor='+edL[0]
    if inL:
        inV = inL[0]
    
#    cita = ur'cita publicación |apellidos={ape} |nombre={nom} |enlaceautor= |año={fec} |título={tit} |publicación={in_} |volumen={vol} |número={num} |páginas={pp} |ubicación= |editorial= |issn= |url= |fechaacceso= {otros}'
    return ur'{{cita publicación |apellidos='+apeV+ur' |nombre='+nomV+ur' |enlaceautor= |año='+fecV+ur' |título='+titV+ur' |publicación='+inV+ur' |volumen='+volV+ur' |número='+numV+ur' |páginas='+ppV+ur' |ubicación= |editorial= |issn= |url= |fechaacceso= '+otrosV+ur'}}'

UTF8Reader = codecs.getreader('utf8')
sys.stdin = UTF8Reader(sys.stdin)

lineaR = re.compile(ur'#? *\*(.*)')
def leer():
    for line in fileinput.input():
        res = lineaR.findall(line)
        if res:
            print line
            print crearRef(res[0])
#Pruebas
# * Barbeau, Marius (1950) ''Totem Poles.'' 2 vols. (Anthropology Series 30, National Museum of Canada Bulletin 119.) Ottawa: National Museum of Canada.
# * Garfield, Viola E. (1939) "Tsimshian Clan and Society." ''University of Washington Publications in Anthropology,'' vol. 7, no. 3, pp. 167-340.
# *Beynon, William (1992) "The Feast of Nisyaganaat, Chief of the Gitsiis." In ''Na Amwaaltga Tsmsiyeen: The Tsimshian, Trade, and the Northwest Coast Economy,'' ed. by [[Susan Marsden]], pp. 45-54. (Suwilaay\'msga Na Ga'niiyatgm, Teachings of Our Grandfathers, vol. 1.) Prince Rupert, B.C.: First Nations Advisory Council of School District #52.
# *Helin, Calvin (2006) ''Dances with Dependency: Indigenous Success through Self-Reliance.'' Vancouver: Orca Spirit Publishing and Communications.

# * [[Jorge Basadre|Basadre Grohmann, Jorge]]: ''Historia de la República del Perú (1822 - 1933)'', Tomo 10, pp. 264-265; y Tomo 17, pp. 56-57. Editada por la Empresa Editora El Comercio S. A. Lima, 2005. ISBN 9972-205-72-X (V.10) / ISBN 9972-205-79-7 (V.17) 
# * Sobrevilla, David (1982): ''Las ideas en el Perú contemporáneo''. Tomo XI de la “Historia del Perú” (Procesos e Instituciones), pp. 152-153. Cuarta  Edición. Lima, Editorial Mejía Baca. ISBN 84-499-1616-X
# * [[Alberto Tauro del Pino|Tauro del Pino, Alberto]] (2001): ''Enciclopedia Ilustrada del Perú''. Tercera Edición. Tomo 17. VAC/ZUZ. Lima, PEISA. ISBN 9972-40-166-9
# * Varios autores (2000): ''Grandes Forjadores del Perú''. Artículo: <small>VILLARREAL, Federico.</small> Lima, Lexus Editores. ISBN 9972-625-50-8

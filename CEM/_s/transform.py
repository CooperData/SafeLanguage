#!/home/ascander/py3/Python-3.3.1/python
# -*- coding: utf-8  -*-
import sys, getopt
import re
import excluidos

regexp = re.compile('[^a-zA-ZáéíóúñüàèìòùÁÉÍÓÚÑÜÀÈÌÒÙ]*([a-zA-ZáéíóúñüàèìòùÁÉÍÓÚÑÜÀÈÌÒÙ]+)')
regURL = re.compile('https?:[\w\d*#@!%+()~/\-\?;,&=:_.]+(?:(?=[{|}\]|\s<>]|&gt;)|$)')
numbExp = re.compile('^[0-9]+$')
regtitle = re.compile('^.*<title>(.*)</title>.*$')

nombres = set([

 'Argentina',
 'Atlas',
 'BAFTA',
 'Belice',
 'Bezier',
 'Blender', 
 'Boeing',
 'Bolivia',
 'Brasil'
 'Canadá',
 'Cannes',
 'Caracas',
 'Chile',
 'Colombia',
 'Cristianismo',
 'Disney',
 'Ecuador',
 'Emmy',
 'España',
 'Euskera',
 'Excel',
 'FIFA',
 'Facebook',
 'Firefox',
 'FreeBSD',
 'Gmail',
 'Google',
 'Grammy',
 'Guatemala',
 'Guyana',
 'HTML',
 'HTTP',
 'HTTPS',
 'Honduras',
 'IRIX',
 'Inca',
 'Internet',
 'Java',
 'John',
 'Joomla!',
 'LaTeX',
 'Lasseter',
 'Linux', 
 'LucasFilm',
 'MadiaWiki',
 'Madrid',
 'Maya',
 'Moodle',
 'MySQL',
 'México',
 'Nicaragua',
 'Oscar',
 'Panamá',
 'Paraguay'
 'Perú',
 'Pixar',
 'PostgreSQL',
 'SCORM',
 'Solaris', 
 'Sutherland',
 'TeX',
 'Tony',
 'Twitter',
 'UEFA',
 'URL',
 'Unicode',
 'Unix',
 'Uruguay',
 'Venezuela',
 'Wiki',
 'Wikipedia', 
 'Wiktionary',
 'Windows', 
 'XAMPP',
 'XML',
 'Hispanoamérica',

])

auxiliares =  [
  'a', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', 
  'durante', 'en', 'entre', 'hacia', 'hasta', 'mediante', 'para', 
  'por', 'según', 'sin', 'so', 'tras', 'versus', 'vía', #sobres
  'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'al', 'del',
  'yo', 'mi', 'mis', 'conmigo', 'tu', 'tus', 'ti', 'contigo', 'vos', 'él', 
  'ella', 'ello', 'sí', 'consigo', 'nosotros', 'nosotras', 
  'ustedes', 'vosotros', 'vosotras', 'ellos', 'ellas', 'me', 
  'nos', 'te', 'os', 'se', 'lo', 'la', 'le', 'se', 'los', 'las', 
  'les', 'me', 'nos', 'mío', 'mía', 'míos', 'mías', 'tuyo', 'tuya', 
  'tuyos', 'tuyas', 'suyo', 'suya', 'suyos', 'suyas', 
  'nuestro', 'nuestra', 'nuestros', 'nuestras', 
  'vuestro', 'vuestra', 'vuestros', 'vuestras', 
  'este', 'esta', 'esto', 'estos', 'estas', 
  'ese', 'esa', 'eso', 'esos', 'esas', 'algo', 
  'ningún', 'ninguno', 'ninguna', 'nada', 'ningunos', 'ningunas', 
  'poco', 'poca', 'pocos', 'pocas', 
  'escaso', 'escasa', 'escasos', 'ascasas', 
  'mucho', 'mucha', 'muchos', 'muchas', 
  'demasiado', 'demasiada', 'demasiados', 'demasiadas', 
  'todo', 'toda', 'todos', 'todas', 'varios', 'varias', 
  'otro', 'otra', 'otros', 'otras', 'mismo', 'misma', 'mismos', 'mismas', 
  'tan', 'tanto', 'tanta', 'tantos', 'tantas', 
  'alguien', 'nadie', 'cualquier', 'cualquiera', 'cualesquiera', 
  'quienquiera', 'quienesquiera', 'demás', 
  'y', 'e', 'ni', 'pero', 'sino', 'conque', 'luego', 'tan',
  'así', 'por', 'etc', 'o', 'u', 'tal', 'tales', 'que', 'pero',
  'sin', 'embargo', 'con', 'pesar', 'no', 'obstante', 'más', 'menos',
  'excepto', 'salvo', 'sino', 'antes', 'bien',
  'como', 'por', 'fin', 'pese', 'si', 'cuando', 'también', 'debido', 
  'entonces', 'donde', 'qué', 'porque', 'porqué', 'muy', 'mientras',
  'cómo', 'aún', 'aun', 'dos', 'tres', 'cuatro', 'cinco', 'seis',
  'siete', 'ocho', 'nueve', 'diez', 'pues',
 'mas',
 'mí',
 'tú',
 'ahí',
 'allá',
 'quién',
 'subgénero',
 'sánscrito',
 'permanencia',
 'alba',
 'ira',
 'realismo',
 'dureza',
 'madurez',
 'socialismo',
 'caos',
 'alfa',
 'homosexualidad',
 'arqueología',
 'patrocinio',
 'aislamiento',
 'gamma',
 'soledad',
 'canonización',
 'ábside',
 'esclavitud',
 'amplitud',
 'postgrado',
 'rotor',
 'movilidad',
 'acompañamiento',
 'dieciocho',
 'multimedia',
 'escasez',
 'budismo',
 'excelencia',
 'terrorismo',
 'constancia',

]

#Palabras escritas correctamente sin plural.
adv_mente = [
 'académicamente',
 'alfabéticamente',
 'anónimamente',
 'artísticamente',
 'automáticamente',
 'biológicamente',
 'básicamente',
 'canónicamente',
 'cariñosamente',
 'científicamente',
 'clínicamente',
 'comúnmente',
 'cronológicamente',
 'críticamente',
 'cómodamente',
 'democráticamente',
 'difícilmente',
 'dinámicamente',
 'dramáticamente',
 'drásticamente',
 'débilmente',
 'económicamente',
 'electrónicamente',
 'eléctricamente',
 'enciclopédicamente',
 'enérgicamente',
 'erróneamente',
 'específicamente',
 'espontáneamente',
 'esporádicamente',
 'estadísticamente',
 'estratégicamente',
 'estéticamente',
 'etimológicamente',
 'explícitamente',
 'extrañamente',
 'futbolísticamente',
 'fácilmente',
 'físicamente',
 'genéricamente',
 'genéticamente',
 'geográficamente',
 'gráficamente',
 'históricamente',
 'hábilmente',
 'ideológicamente',
 'implícitamente',
 'increíblemente',
 'inequívocamente',
 'instantáneamente',
 'intrínsecamente',
 'inútilmente',
 'irónicamente',
 'jurídicamente',
 'legítimamente',
 'lingüísticamente',
 'lógicamente',
 'matemáticamente',
 'mecánicamente',
 'momentáneamente',
 'morfológicamente',
 'mágicamente',
 'médicamente',
 'mínimamente',
 'numéricamente',
 'pacíficamente',
 'paradójicamente',
 'periódicamente',
 'polinómicamente',
 'políticamente',
 'prácticamente',
 'próximamente',
 'psicológicamente',
 'póstumamente',
 'públicamente',
 'químicamente',
 'rápidamente',
 'simbólicamente',
 'simultáneamente',
 'sistemáticamente',
 'súbitamente',
 'tardíamente',
 'tecnológicamente',
 'teóricamente',
 'trágicamente',
 'técnicamente',
 'típicamente',
 'unánimemente',
 'étnicamente',
 'íntegramente',
 'íntimamente',
 'últimamente',
 'únicamente',
# 'sólamente',

 'abaxialmente',
 'abiertamente',
 'abruptamente',
 'absolutamente',
 'abundantemente',
 'accidentalmente',
 'activamente',
 'actualmente',
 'adaxialmente',
 'adecuadamente',
 'adicionalmente',
 'administrativamente',
 'afortunadamente',
 'aleatoriamente',
 'alegremente',
 'altamente',
 'alternativamente',
 'amablemente',
 'ampliamente',
 'anchamente',
 'angostamente',
 'anteriormente',
 'antiguamente',
 'anualmente',
 'aparentemente',
 'apicalmente',
 'apresuradamente',
 'apropiadamente',
 'aproximadamente',
 'arbitrariamente',
 'ardientemente',
 'artificialmente',
 'asexualmente',
 'asiduamente',
 'atentamente',
 'basalmente',
 'brevemente',
 'brillantemente',
 'bruscamente',
 'brutalmente',
 'casualmente',
 'cercanamente',
 'ciertamente',
 'clandestinamente',
 'claramente',
 'colectivamente',
 'coloquialmente',
 'comercialmente',
 'comparativamente',
 'completamente',
 'computacionalmente',
 'concretamente',
 'conjuntamente',
 'conscientemente',
 'consecuentemente',
 'consecutivamente',
 'considerablemente',
 'consistentemente',
 'constantemente',
 'constitucionalmente',
 'continuamente',
 'contrariamente',
 'convencionalmente',
 'convenientemente',
 'correctamente',
 'cortamente',
 'cruelmente',
 'cuidadosamente',
 'culturalmente',
 'curiosamente',
 'debidamente',
 'decididamente',
 'decisivamente',
 'definitivamente',
 'deliberadamente',
 'demente',
 'densamente',
 'deportivamente',
 'desafortunadamente',
 'desesperadamente',
 'desgraciadamente',
 'despectivamente',
 'detalladamente',
 'detenidamente',
 'diariamente',
 'digitalmente',
 'directamente',
 'discretamente',
 'doblemente',
 'dorsalmente',
 'duramente',
 'efectivamente',
 'eficazmente',
 'eficientemente',
 'eminentemente',
 'emocionalmente',
 'enormemente',
 'enteramente',
 'equivocadamente',
 'escasamente',
 'esencialmente',
 'especialmente',
 'espiritualmente',
 'estacionalmente',
 'estrechamente',
 'estrictamente',
 'estructuralmente',
 'eternamente',
 'eventualmente',
 'evidentemente',
 'exactamente',
 'excepcionalmente',
 'excesivamente',
 'exclusivamente',
 'exitosamente',
 'experimentalmente',
 'exponencialmente',
 'expresamente',
 'extensamente',
 'extensivamente',
 'exteriormente',
 'externamente',
 'extraordinariamente',
 'extremadamente',
 'falsamente',
 'fatalmente',
 'favorablemente',
 'felizmente',
 'ferozmente',
 'fielmente',
 'finalmente',
 'finamente',
 'financieramente',
 'firmemente',
 'formalmente',
 'forzosamente',
 'francamente',
 'frecuentemente',
 'frontalmente',
 'fuertemente',
 'funcionalmente',
 'fundamentalmente',
 'generalmente',
 'generosamente',
 'genuinamente',
 'globalmente',
 'gradualmente',
 'grandemente',
 'gratuitamente',
 'gravemente',
 'habitualmente',
 'horizontalmente',
 'idealmente',
 'igualmente',
 'ilegalmente',
 'inadvertidamente',
 'incansablemente',
 'incondicionalmente',
 'inconscientemente',
 'incorrectamente',
 'indebidamente',
 'indefinidamente',
 'independientemente',
 'indirectamente',
 'indistintamente',
 'individualmente',
 'indudablemente',
 'industrialmente',
 'inesperadamente',
 'inevitablemente',
 'inexplicablemente',
 'infinitamente',
 'informalmente',
 'infructuosamente',
 'inherentemente',
 'inicialmente',
 'ininterrumpidamente',
 'injustamente',
 'inmediatamente',
 'inmensamente',
 'innecesariamente',
 'intencionadamente',
 'intencionalmente',
 'intensamente',
 'interinamente',
 'interiormente',
 'internacionalmente',
 'internamente',
 'inusualmente',
 'invariablemente',
 'involuntariamente',
 'irregularmente',
 'irremediablemente',
 'judicialmente',
 'justamente',
 'lamentablemente',
 'largamente',
 'lateralmente',
 'legalmente',
 'lentamente',
 'levemente',
 'libremente',
 'ligeramente',
 'linealmente',
 'literalmente',
 'localmente',
 'locamente',
 'longitudinalmente',
 'magistralmente',
 'manualmente',
 'marcadamente',
 'masivamente',
 'mayoritariamente',
 'mayormente',
 'medianamente',
 'mensualmente',
 'mentalmente',
 'meramente',
 'milagrosamente',
 'militarmente',
 'minuciosamente',
 'misteriosamente',
 'moderadamente',
 'moralmente',
 'mortalmente',
 'mundialmente',
 'musicalmente',
 'mutuamente',
 'nacionalmente',
 'naturalmente',
 'necesariamente',
 'negativamente',
 'netamente',
 'nominalmente',
 'normalmente',
 'notablemente',
 'notoriamente',
 'nuevamente',
 'objetivamente',
 'obligatoriamente',
 'obviamente',
 'ocasionalmente',
 'ocultamente',
 'oficialmente',
 'opcionalmente',
 'oportunamente',
 'oralmente',
 'originalmente',
 'originariamente',
 'ostensiblemente',
 'paralelamente',
 'parcialmente',
 'particularmente',
 'paulatinamente',
 'peligrosamente',
 'perdidamente',
 'perfectamente',
 'permanentemente',
 'perpendicularmente',
 'personalmente',
 'plenamente',
 'pobremente',
 'poderosamente',
 'popularmente',
 'posiblemente',
 'positivamente',
 'posteriormente',
 'potencialmente',
 'precipitadamente',
 'precisamente',
 'predominantemente',
 'preferentemente',
 'preferiblemente',
 'prematuramente',
 'presumiblemente',
 'presuntamente',
 'previamente',
 'primariamente',
 'primeramente',
 'primordialmente',
 'principalmente',
 'probablemente',
 'profesionalmente',
 'profundamente',
 'profusamente',
 'progresivamente',
 'prontamente',
 'propiamente',
 'proporcionalmente',
 'provisionalmente',
 'puntualmente',
 'puramente',
 'racionalmente',
 'radicalmente',
 'raramente',
 'razonablemente',
 'realmente',
 'recientemente',
 'regularmente',
 'reiteradamente',
 'relativamente',
 'remotamente',
 'repentinamente',
 'repetidamente',
 'respectivamente',
 'ricamente',
 'rigurosamente',
 'rotundamente',
 'satisfactoriamente',
 'secretamente',
 'seguidamente',
 'seguramente',
 'selectivamente',
 'semanalmente',
 'sencillamente',
 'sensiblemente',
 'sentimentalmente',
 'separadamente',
 'seriamente',
 'severamente',
 'sexualmente',
 'significativamente',
 'simplemente',
 'sinceramente',
 'singularmente',
 'socialmente',
 'solamente',
 'solemnemente',
 'sorprendentemente',
 'sorpresivamente',
 'suavemente',
 'subsecuentemente',
 'sucesivamente',
 'suficientemente',
 'sumamente',
 'superficialmente',
 'supuestamente',
 'sustancialmente',
 'sutilmente',
 'temporalmente',
 'tempranamente',
 'tentativamente',
 'terriblemente',
 'territorialmente',
 'textualmente',
 'totalmente',
 'tradicionalmente',
 'tranquilamente',
 'transversalmente',
 'tremendamente',
 'tristemente',
 'uniformemente',
 'unilateralmente',
 'universalmente',
 'urgentemente',
 'usualmente',
 'vagamente',
 'valientemente',
 'velozmente',
 'verbalmente',
 'verdaderamente',
 'verticalmente',
 'violentamente',
 'virtualmente',
 'visiblemente',
 'visualmente',
 'voluntariamente',
 'vulgarmente',

]
verificadas = adv_mente + [
 'a',
 'aceptable',
 'acercamiento',
 'adelante',
 'además',
 'ahora',
 'ajedrez',
 'algorítmica',
 'altura',
 'ambiente',
 'and',
 'análisis',
 'aparte',
 'aprendizaje',
 'artificial',
 'auge',
 'auto',
 'autonomía',
 'aviso',
 'b',
 'bioinformática',
 'biología',
 'bits',
 'bucle',
 'búsqueda',
 'c',
 'cabo',
 'cada',
 'casi',
 'celular',
 'cerebro',
 'china',
 'cibernética',
 'ciudad',
 'complejidad',
 'completitud',
 'completitud',
 'computabilidad',
 'consecuencia',
 'consenso',
 'contexto',
 'controlarse',
 'correspondencia',
 'cota',
 'crecimiento',
 'crédito',
 'cuerpo',
 'cuándo',
 'cómputo',
 'd',
 'decidible',
 'dentro',
 'do',
 'dolor',
 'durable',
 'débil',
 'e',
 'economía',
 'eficacia',
 'eficiencia',
 'eficiente',
 'energía',
 'entendimiento',
 'equivalencia',
 'escritura',
 'etcétera',
 'etiología',
 'existencia',
 'experiencia',
 'exponencial',
 'exterior',
 'f',
 'feedback',
 'flexible',
 'for',
 'formal',
 'fraude',
 'frente',
 'fuerza',
 'funcionamiento',
 'física',
 'g',
 'gama',
 'gran',
 'h',
 'hambre',
 'hard',
 'hardware',
 'hoy',
 'i',
 'importancia',
 'independiente',
 'individuo',
 'ineficiente',
 'inferencia',
 'ingeniería',
 'ingenio',
 'inherente',
 'insensible',
 'instante',
 'integridad',
 'interlocutor',
 'invariante',
 'j',
 'k',
 'l',
 'labor',
 'lejos',
 'lengua',
 'longitud',
 'loop',
 'm',
 'management',
 'matemático',
 'materia',
 'mayor',
 'mayoría',
 'medicina',
 'mejor',
 'menudo',
 'miedo',
 'milicia',
 'misil',
 'modo',
 'multi',
 'mundo',
 'n',
 'norteamericano',
 'o',
 'p',
 'papel',
 'peso',
 'polinomial',
 'polinomio',
 'polisemia',
 'portaaviones',
 'primo',
 'primordial',
 'priori',
 'probable',
 'process',
 'profundidad',
 'psicología',
 'psicopatología',
 'psiquiátrico',
 'pérdida',
 'q',
 'quizás',
 'r',
 'racional',
 'realidad',
 'reconocimiento',
 'refuerzo',
 'regularse',
 'rendimiento',
 'robótica',
 'rutina',
 's',
 'seguridad',
 'semisupervisado',
 'sentido',
 'siempre',
 'sintaxis',
 'siquiera',
 'sociedad',
 'sociología',
 'subconjunto',
 'suficiente',
 'sufrimiento',
 'sumo',
 'superado',
 'surgimiento',
 'síntesis',
 'sólo',
 't',
 'taxonomía',
 'teoría',
 'test',
 'teórico',
 'torno',
 'totalidad',
 'través',
 'u',
 'v',
 'variedad',
 'vida',
 'vocabulario',
 'w',
 'x',
 'y',
 'ya',
 'z',
 'phishing',
 'spoofing',
 'enero',
 'febrero',
 'marzo',
 'abril',
 'mayo',
 'junio',
 'julio',
 'agosto',
 'septiembre',
 'octubre',
 'noviembre',
 'diciembre',
 'lunes',
 'martes',
 'miércoles',
 'jueves',
 'viernes',
 'jamás',
 'virus',
 'hipótesis',
 'rascacielos',
'después',
'fútbol',
'aunque',
'sur',
'norte',
'aquí',
'incluso',
'genus',
'gracias',
'oeste',
'nunca',
'amor',
'allí',
'gente',
'respecto',
'aire',
 'todavía',
 'baloncesto',
 'status',
 'pronto',
 'crisis',
 'detrás',
 'noreste',
 'suroeste',
 'latín',
 'encima',
 'diócesis',
 'abajo',
 'apenas',
 'website',
 'óblast',
 'doce',
 'atrás',
 'URL',
 'alias',
 'mexicas',
 'debajo',
 'salud',
 'noroeste',
 'rugby',
 'violencia',
 'elenco',
 'pobreza',
 'sureste',
 'fe',
 'bordo',
 'mantenimiento',
 'treinta',
 'ciclismo',
 'béisbol',
 'tesis',
 'eslogan',
 'fauna',
 'calor',
 'cincuenta',
 'tenis',
 'hockey',
 'confianza',
 'capita',
 'cuarenta',
 'quince',
 'balonmano',
 'beta',
 'sudeste',
 'cien',
 'aviación',
 'voleibol',
 'sesenta',
 'trece',
 'periodismo',
 'setenta',
 'semi',
 'atletismo',
 'ochenta',
 'delta',
 'endemismo',
 'nordeste',
 'dosis',
 'cumpleaños',
 'levantamiento',
 'automovilismo',
 'minería',
 'odio',
 'sudoeste',
 'alpha',
 'noventa',
 'jpeg',
 'vigor',
 'énfasis',
 'envergadura',
 'abundancia',
 'supervivencia',
 'waterpolo',
 'limpieza',
 'boxeo',
 'prevención',
 'adolescencia',
 'obtención',
 'bienestar',
 'catolicismo',

]

#Principalmente etiquetas de plantillas y palabras en otros idiomas
ignorar = [
 'antselecciones',
 'aaa',
 'abs',
 'ac',
 'action',
 'ad',
 'af',
 'align',
 'all',
 'alliance',
 'amp',
 'an',
 'anatomy',
 'anyo',
 'ar',
 'arial',
 'array',
 'art',
 'article',
 'articles',
 'arxiv',
 'as',
 'asp',
 'aspx',
 'at',
 'authority',
 'az',
 'añoacceso',
 'background',
 'bbc',
 'bgcolor',
 'big',
 'bit',
 'black',
 'blues',
 'books',
 'border',
 'br',
 'by',
 'ca',
 'caption',
 'cat',
 'cd',
 'cdot',
 'cedff',
 'cellpadding',
 'cellspacing',
 'center',
 'cgi',
 'cia',
 'cit',
 'cl',
 'clade',
 'clarin',
 'class',
 'classification',
 'cm',
 'co',
 'code',
 'collapse',
 'colspan',
 'com',
 'comment',
 'commons',
 'commonscat',
 'content',
 'coord',
 'copyleft',
 'country',
 'cr',
 'cu',
 'cytology',
 'dan',
 'days',
 'db',
 'deg',
 'der',
 'des',
 'descriptions',
 'distribution',
 'div',
 'doc',
 'docs',
 'doi',
 'dq',
 'ds',
 'du',
 'ed',
 'eds',
 'edu',
 'eee',
 'efefef',
 'ejem',
 'elmundo',
 'elpais',
 'elpepiint',
 'else',
 'em',
 'end',
 'enlaceautor',
 'est',
 'et',
 'eu',
 'ex',
 'ey',
 'factbook',
 'false',
 'families',
 'family',
 'fechaacceso',
 'fechaaceso',
 'ffffff',
 'fi',
 'first',
 'flowering',
 'font',
 'format',
 'fr',
 'frac',
 'frac',
 'from',
 'ft',
 'gallery',
 'gc',
 'gif',
 'go',
 'gob',
 'gov',
 'gr',
 'grass',
 'group',
 'grp',
 'gt',
 'hab',
 'harvnp',
 'hdr',
 'height',
 'hi',
 'high',
 'history',
 'hl',
 'htm',
 'html',
 'http',
 'https',
 'id',
 'ido',
 'if',
 'ij',
 'illustrations',
 'image',
 'images',
 'imf',
 'in',
 'including',
 'indec',
 'index',
 'indol',
 'ine',
 'info',
 'infobae',
 'int',
 'intkey',
 'is',
 'isbn',
 'it',
 'jpg',
 'kew',
 'km',
 'label',
 'lanacion',
 'lang',
 'last',
 'lavender',
 'left',
 'library',
 'lightgreen',
 'line',
 'link',
 'listaref',
 'lng',
 'low',
 'lt',
 'lucida',
 'margin',
 'math',
 'mathbf',
 'mathit',
 'max',
 'mecon',
 'min',
 'mm',
 'mobot',
 'model',
 'morphology',
 'ms',
 'msnm',
 'mx',
 'na',
 'name',
 'nbsp',
 'net',
 'new',
 'news',
 'newsid',
 'nom',
 'nowiki',
 'ns',
 'nuevaweb',
 'of',
 'ogg',
 'on',
 'onepage',
 'oni',
 'online',
 'op',
 'or',
 'orange',
 'orders',
 'org',
 'orthographic',
 'padding',
 'page',
 'parentid',
 'pathogens',
 'pdf',
 'pe',
 'per',
 'pg',
 'php',
 'physiology',
 'phytochemistry',
 'pi',
 'pl',
 'plainlinks',
 'plants',
 'pmid',
 'png',
 'pp',
 'pr',
 'pt',
 'pubs',
 'px',
 'pág',
 'qc',
 'quad',
 'quot',
 'rae',
 'ranks',
 're',
 'record',
 'ref',
 'references',
 'reg',
 'regnum',
 'result',
 'retrieval',
 'ria',
 'right',
 'rock',
 'rowspan',
 'sa',
 'safe',
 'san',
 'sangrado',
 'sans',
 'science',
 'scsm',
 'search',
 'server',
 'sha',
 'shift',
 'shift',
 'shtml',
 'site',
 'size',
 'small',
 'solid',
 'sort',
 'source',
 'sp',
 'space',
 'span',
 'spanish',
 'ssd',
 'statistics',
 'stm',
 'structure',
 'style',
 'sub',
 'sup',
 'sup',
 'svg',
 'sy',
 'synonyms',
 'td',
 'text',
 'th',
 'the',
 'thumb',
 'till',
 'time',
 'timestamp',
 'title',
 'to',
 'top',
 'tt',
 'type',
 'uk',
 'undp',
 'url',
 'username',
 'valign',
 'var',
 'view',
 'vol',
 'von',
 'watch',
 'web',
 'weo',
 'weodata',
 'weorept',
 'wg',
 'white',
 'width',
 'wikcionario',
 'wikispecies',
 'wikitable',
 'wikitext',
 'with',
 'world',
 'www',
 'xls',
 'year',
 'contributor',
 'begin',
 'yellow',
 'ch',
 'fontsize',
 'wikiquote',
 'jsp',
 'mu',
 'minor',
 'mathbb',
 'arms',
 'sqrt',
 'precip',
 'págs',
 'ei',
 'ois',
 'publisher',
 'bin',
 'und',
 'ff',
 'publications',
 'be',
 'none',
 'human',
 'have',
 'man',
 'pungens',
 'pts',
 'provinces',
 'preview',
 'docman',
 'dll',
 'disk',
 'formatnum',
 'google',
 'rk',
 'vec',
 'mbox',
 'loc',
 'he',
 'kg',
 'display',
 'nobel',
 'nih',
 'book',
 'information',
 'home', 
 'imdb',
 'evolution',
 'clear',
 'bottom',
 'ct',
 'urlarchivo',
 'cfm',
 'thumbnail',
 'map',
 'tufts',
 'fechaarchivo',
 'float',
 'single',
 'may',
 'col',
 'times',
 'youtube',
 'pub',
 'tr',
 'that',
 'oi',
 'ru',
 'pre',
 'hopper',
 'nlm',
 'nature',
 'ne',
 'au',
 'pages',
 'autogenerated',
 'larger',
 'frontcover',
 'cs',
 'espana',
 'redirect',
 'full',
 'up',
 'sig',
 'nu',
 'mathrm',
 'st',
 'not',
 'pag',
 'pls',
 'once',
 'prizes',
 'over',
 'story',
 'nowrap',
 'music',
 'count',
 'column',
 'symbol',
 'default',
 'scielo',
 'della',
 'nm',
 'catholic',
 'coor',
 'file',
 'files',
 'laureates',
 'cervantesvirtual',
 'ffdead',
 'work',
 'sortable',
 'li',
 'pos',
 'nat',
 'cod',
 'sep',
 'ago',
 'nov',
 'efcfff',
 'oct',
 'pattern',
 'wikt',
 'dic',
 'ene',
 'selb',
 'longd',
 'latd',
 'latm',
 'longm',
 'cp',
 'num',
 'lats',
 'longs',
 'adm',
 'length',
 'ip',
 'pop',
 'about',
 'version',
 'printsec',
 'lpg',
 'ec',
 'post',
 'physics',
 'cc',
 'nobelprize',
 'iba',
 'revision',
 'alt',
 'insee',
 'xml',
 'score',
 'subdivision',
 'team',
 'classis',
 'noinclude',
 'latitude',
 'longitude',
 'seed',
 'mini',
 'maxi',
 'jun',
 'communes',
 'arrondissement',
 'département',
 'maire',
 'mandat',
 'nomcommune',
 'recensement',
 'abr',
 'wikiproyecto',
 'intercomm',
 'jul',
 'moy',
 'sansdoublescomptes',
 'rp',
 'theme',
 'navigation',
 'typeprod',
 'nivgeo',
 'codgeo',
 'episodionumero',
 'nomhab',
 'gray',
 'without',
 'diacritics',
 'lat',
 'research',
 'collection',
 'city',
 'region',
 'insects',
 'met',
 'mar',
 'player',
 'dms',
 'gnis',
 'másrazas',
 'maps',
 'vs',
 'dts',
 'us',
 'sports',
 'yes',
 'shorts',
 'was',
 'partidosinternacionales',
 'results',
 'ratings',
 'details',
 'charts',
 'socks',
 'credits',
 'has',
 'players',
 'res',
 'awards',
 'lyrics',
 'teams',
 'das',
 'subclassis',
 'biblios',
 'this',
 'his',
 'spiders',
 'nytimes',
 'ots',
 'discogs',
 'its',
 'fs',
 'organismnames',
 'itunes',
 'singles',
 'colcomments',
 'tvbythenumbers',
 'lbs',
 'otrosusos',
 'fans',
 'stripes',
 'arts',
 'dans',
 'reviews',
 'wordpress',
 'press',
 'gcis',
 'stars',
 'cities',
 'apps',
 'nts',
 'olympics',
 'matches',
 'years',
 'campus',
 'cdsads',
 'highways',
 'emporis',
 'songs',
 'whiteflies',
 'photos',
 'athletes',
 'perepis',
 'ekspres',
 'stories',
 'sites',
 'uploads',
 'releases',
 'census',
 'games',
 'movies',
 'features',
 'toccolours',
 'documents',
 'trans',
 'artists',
 'rs',
 'pdfs',
 'names',
 'prosportstransactions',
 'sets',
 'members',
 'products',
 'ss',
 'business',
 'caps',
 'footnotes',
 'contribs',
 'plus',
 'events',
 'points',
 'cms',
 'pibmunicipios',
 'ps',
 'bonus',
 'comics',
 'bot',
 'canton',
 'feb',
 'région',
 'hectares',
 'guion',
 'oldid',
 'season',
 'check',
 'writer',
 'ra',
 'user',
 'ja',
 'jp',
 'tv',
 'nombrecompleto',
 'prev',
 'allmusic',
 'option',
 'flag',
 'er',
 'nl',
 'lon',
 'punk',
 'gouv',
 'abc',
 'service',
 'range',
 'list',
 'landmark',
 'month',
 'goleslocal',
 'you',
 'añodebut',
 'reference',
 'minibandera',
 'middle',
 'ciudaddenacimiento',
 'paisdenacimiento',
 'clubdebut',
 'tam',
 'value',
 'il',
 'chan',
 'golesvisita',
 'elections',
 'round',
 'wikificar',
 'silver',
 'blue',
 'gold',
 'includeonly',
 'cup',
 'monobook',
 'inline',
 'sections',
 'fechanac',
 'sel',
 'sh',
 'lugarnac',
 'query',
 'artist',
 'votre',
 'resultats',
 'interieur',
 'eeeeee',
 'tl',
 'weight',
 'uy',
 'am',
 'accessdate',
 'infobox',
 'people',
 'ge',
 'block',
 'nd',
 'talk',
 'disc',
 'review',
 'report',
 'rsssf',
 'start',
 'gules',
 'rightarm',
 'leftarm',
 'serv',
 'cfcfff',
 'moi',
 'urb',
 'system',
 'dia',
 'ign',
 'locator',
 'scope',
 'iban',
 'imageninferior',
 'my',
 'subsp',
 'll',
 'tour',
 'dfffdf',
 'true',
 'zh',
 'iucnredlist',
 'table',
 'help',
 'billboard',
 'rgb',
 'añoretiro',
 'magazine',
 'off',
 'mp',
 'ie',
 'bio',
 'task',
 'one',
 'set',
 'img',
 'limit',
 'national',
 'ma',
 'aa',
 'lugarmuerte',
 'face',
 'wikimedia',
 'mark',
 'ul',
 'sv',
 'dc',
 'pro',
 'chart',
 'location',
 'author',
 'ddffdd',
 'cap',
 'mode',
 'rio',
 'boe',
 'terra',
 'rd',
 'ecemaml',
 'position',
 'ka',
 'die',
 'main',
 'draft',
 'myspace',
 'part',
 'precipitation',
 'nba',
 'vi',
 'ng',
 'anti',
 'marksize',
 'items',
 'available',
 'external',
 'jn',
 'vk',
 'euskomedia',
 'acordió',
 'anará',
 'apresentará',
 'aprimorá',
 'apsará',
 'aserrá',
 'asuatará',
 'colorá',
 'diff',
 'fechadenacimiento',
 'refe',
 'uefa',
 'fifa',
 'fechamuerte',
 'icon',
 'euskera',
 'ifeq',
 'paíslocal',
 'paísvisita',
 'pa',
 'lightsteelblue',
 'trad',
 'fechafallecimiento',
 'ciudadfallecimiento',
 'paisfallecimiento',
 'tpl',
 'ga',
 'fb',
 'out',
 'hop',
 'hr',
 'fff',
 'im',
 'ppp',
 'cover',
 'clubretiro',
 'iucn',
 'wa',
 'both',
 'tab',
 'free',
 'wp',
 'pid',
 'find',
 'non',
 'release',
 'feature',
 'teau',
 'issn',
 'um',
 'dx',
 'dir',
 'expr',
 'song',
 'ep',
 'edit',
 'bl',
 'ffdddd',
 'sec',
 'theplantlist',
 'autovia',
 'english',
 'espanol',
 'wikipedia',
 'ordo',
 'nihongo',
 'mg',
 'urlcapítulo',
 'boxstyle',
 'fa',
 'sat',
 'which',
 'reverse',
 'course',
 'universe',
 'phylum',
 'status',
 'superordo',
 'subordo',
 'subphylum',
 'debut',
 'cápita',
 'convert',
 'infraordo',
 'abbr',
 'diversity',
 'lk',
 'sqkm',
 'sqmi',
 'opc',
 'december',
 'núm',
 'medal',
 'freshwater',
 'nbay',
 'istat',
 'aut',
 'divisio',
 'jazz',
 'krai',
 'body',
 'collapsible',
 'ndash',
 'collapsed',
 'ccffcc',
 'oclc',
 'green',
 'unranked',
 'piedefoto',
 'jct',
 'ayudantedirección',
 'rev',
 'veinte',
 'their',
 'row',
 'dist',
 'journal',
 'pob',
 'signal',
 'feat',
 'traffic',
 'quote',
 'highlighting',
 'für',
 'estadisticavalor',
 'estadisticaetiqueta',
 'sincat',
 'writing',
 'concelho',
 'fossil',
 'sortname',
 'bibcode',
 'variant',
 'unsortable',
 'volume',
 'tc',
 'rating',
 'goal',
 'seg',
 'mater',
 'pointer',
 'singlechart',
 'lightblue',
 'newspaper',
 'relac',
 'flagicon',
 'language',
 'but',
 'were',
 'faff',
 'ncia',
 'two',
 'tre',
 'resumenprofano',
 'fuenteprofano',
 'freguesiasdeportugal',
 'fechaprofano',
 'subregnum',
 'into',
 'dddddd',
 'añosactivo',
 'place',
 'company',
 'other',
 'official',
 'quotes',
 'also',
 'aux',
 'who',
 'borough',
 'will',
 'track',
 'after',
 'station',
 'ant',
 'máter',
 'can',
 'zoo',
 'long',
 'ta',
 'qui',
 'life',
 'band',
 'almamáter',
 'more',
 'play',
 'lightgrey',
 'dei',
 'pictogram',
 'generated',
 'issue',
 'pm',
 'had',
 'guide',
 'ffff',
 'aprox',
 'ededed',
 'her',
 'pour',
 'izq',
 'sag',
 'dell',
 'pen',
 'college',
 'canvas',
 'sinreferencias',
 'fran',
 'pink',
 'ko',
 'catalogación',
 'only',
 'grey',
 'blockquote',
 'heavy',
 'aise',
 'between',
 'ffcccc',
 'pk',
 'bold',
 'back',
 'ur',
 'live',
 'thedraftreview',
 'protein',
 'reality',
 'through',
 'ffdf',
 'fechadefallecimiento',
 'sun',
 'assessors',
 'been',
 'ou',
 'subspecies',
 'fishes',
 'infraclassis',
 'estatus',
 'cannes',
 'described',
 'filmaffinity',
 'basketball',
 'emmy',
 'comune',
 'pieimagen',
 'grammy',
 'tony',
 'superfamila',
 'population',
 'nombreanterior',
 'á',
 'relative',
 'fishbase',
 'spider',
 'twitter',
 'tamañoimagen',
 'number',
 'lugardefallecimiento',
 'sfn',
 'hip',
 'repeat',
 'harvnb',
 'ffffbf',
 'railwaystation',
 'like',
 'rn',
 'scroll',
 'they',
 'ffcfcf',
 'dfdfdf',
 'card',
 'under',
 'star',
 'death',
 'tag',
 'videoclip',
 'terr',
 'than',
 'mdash',
 'annotated',
 'state',
 'ibn',
 'ftp',
 'vel',
 'rain',
 'aw',
 'sous',
 'pmc',
 'tes',
 'during',
 'house',
 'smaller',
 'scale',
 'zu',
 'ro',
 'love',
 'zur',
 'delle',
 'catalog',
 'ki',
 'game',
 'major',
 'sq',
 'football',
 'humidity',
 'profile',
 'ia',
 'category',
 'selectall',
 'colname',
 'colcategory',
 'colauthority',
 'ballet',
 'dens',
 'khaki',
 'power',
 'copyedit',
 'nia',
 'ers',
 'voivodato',
 'mit',
 'western',
 'nrhp',
 'study',
 'anno',
 'folk',
 'ek',
 'coordinates',
 'hp',
 'ao',
 'we',
 'iptv',
 'tel',
 'next',
 'based',
 'three',
 'aus',
 'ccccff',
 'most',
 'ji',
 'leader',
 'rally',
 'wrestling',
 'ffe',
 'legend',
 'zip',
 'vols',
 'ibge',
 'land',
 'water',
 'blank',
 'dem',
 'í',
 'ring',
 'hardcore',
 'analysis',
 'episode',
 'geoftp',
 'movie',
 'when',
 'war',
 'featuring',
 'cum',
 'downloaded',
 'acessodata',
 'lugardenacimiento',
 'chasis',
 'would',
 'ais',
 'harv',
 'abitanti',
 'dictionary',
 'airport',
 'ce',
 'there',
 'upright',
 'sitioweb',
 'av',
 'your',
 'evi',
 'bg',
 'early',
 'citation',
 'dels',
 'century',
 'box',
 'hit',
 'ri',
 'day',
 'yel',
 'indie',
 'roll',
 'latin',
 'feudo',
 'avec',
 'match',
 'cccccc',
 'age',
 'ville',
 'bis',
 'prefisso',
 'degli',
 'rugbybox',
 'mountain',
 'frazioni',
 'franquismo',
 'acres',
 'description',
 'against',
 'field',
 'key',
 'auf',
 'bfefff',
 'soul',
 'urltrad',
 'vre',
 'sum',
 'side',
 'interview',
 'mesacceso',
 'large',
 'made',
 'vlasenko',
 'dfd',
 'ico',
 'published',
 'fan',
 'best',
 'tracks',
 'she',
 'southern',
 'australis',
 'fish',
 'assist',
 'dead',
 'harvsp',
 'cfc',
 'piedemapa',
 'contrarreloj',
 'med',
 'vice',
 'hall',
 'such',
 'adj',
 'known',
 'nen',
 'archiveurl',
 'rebounds',
 'ii',
 'now',
 'log',
 'coat',
 'ffcc',
 'medaille',
 'notasalpie',
 'before',
 'role',
 'week',
 'archivedate',
 'bei',
 'mix',
 'among',
 'see',
 'squet',
 'iii',
 'gl',
 'cv',
 'public',
 'head',
 'circa',
 'ccc',
 'second',
 'waterbody',
 'cfffcf',
 'superclassis',
 'database',
 'then',
 'ray',
 'many',
 'retrieved',
 'present',
 'og',
 'party',
 'four',
 'coach',
 'mo',
 'cropped',
 'government',
 'lb',
 'ci',
 'desc',
 'where',
 'remake',
 'listref',
 'political',
 'ab',
 'pc',
 'baa',
 'rpm',
 'als',
 'gra',
 'fdd',
 'theta',
 'rank',
 'drop',
 'eastern',
 'md',
 'cle',
 'qu',
 'authorlink',
 'north',
 'pog',
 'equipoactual',
 'nationale',
 'añosprof',
 'since',
 'lee',
 'them',
 'equiposprof',
 'roster',
 'plantillapais',
 'way',
 'photo',
 'hits',
 'ind',
 'ej',
 'skyblue',
 'sitiodeciclismo',
 'change',
 'any',
 'him',
 'tablapartidos',
 'ln',
 'marketing',
 'fechainicia',
 'well',
 'what',
 'attendance',
 'vulgaris',
 'industry',
 'autopromoción',
 'men',
 'occidentalis',
 'culture',
 'late',
 'headline',
 'development',
 'darkgray',
 'ai',
 'section',
 'arcade',
 'performance',
 'air',
 'plainrowheaders',
 'homepage',
 'deadurl',
 'clip',
 'encyclopedia',
 'our',
 'reggae',
 'referee',
 'esp',
 'agency',
 'using',
 'network',
 'away',
 'anotadorvisita',
 'anotadorlocal',
 'income',
 'accessed',
 'posiólok',
 'siteweb',
 'xx',
 'playoffs',
 'production',
 'entry',
 'glspp',
 'unit',
 'cfffff',
 'agglomération',
 'partial',
 'studies',
 'rt',
 'rg',
 'cell',
 'plant',
 'break',
 'paisgol',
 'funk',
 'casting',
 'found',
 'tempo',
 'double',
 'ccf',
 'upon',
 'around',
 'records',
 'bgcolour',
 'birds',
 'biography',
 'listing',
 'night',
 'moz',
 'these',
 'run',
 'associated',
 'nac',
 'origin',
 'sul',
 'nh',
 'superfamilia',
 'superfamilias',
 'nz',
 'tz',
 'cz',
 'ez',
 'dz',
 'lz',
 'rz',
 'oz',
 'iz',
 'sz',
 'mz',
 'jz',
 'bz',
 'pz',
 'uz',
 'kz',
 'yz',
 'hz',
 'vz',
 'xz',
 'gz',
 'zz',
 'fz',
 'qz',
 'wz',
 'chez',
 'absolute',
 'acute',
 'admin',
 'abstract',
 'act',
 'airdate',
 'army',
 'amg',
 'aerial',
 'association',
 'alive',
 'amateurteams',
 'authors',
 'autres',
 'adjacent',
 'attacks',
 'always',
 'annual',
 'añoestadisticas',
 'applications',
 'année',
 'assessment',
 'añosamateur',
 'acts',
 'announces',
 'artistid',
 'adult',
 'average',
 'añodebutjug',
 'añoretirojug',
 'almost',
 'ambient',
 'aspects',
 'ascii',
 'added',
 'autre',
 'affaire',
 'administration',
 'alltimes',
 'addition',
 'aequo',
 'address',
 'activities',
 'activation',
 'animation',
 'aculturación',
 'apple',
 'although',
 'ball',
 'being',
 'beat',
 'brown',
 'boy',
 'bass',
 'building',
 'bmatrix',
 'bull',
 'because',
 'basketballbox',
 'birth',
 'boldsymbol',
 'bordered',
 'baseball',
 'became',
 'baby',
 'bridge',
 'biology',
 'binding',
 'battle',
 'botanique',
 'brain',
 'born',
 'beaux',
 'blood',
 'buffer',
 'behavior',
 'become',
 'behind',
 'belly',
 'better',
 'bird',
 'brevis',
 'begins',
 'began',
 'built',
 'bad',
 'blason',
 'brief',
 'board',
 'below',
 'bronze',
 'bomb',
 'balls',
 'blanc',
 'biological',
 'boxes',
 'boys',
 'boot',
 'becomes',
 'beach',
 'believe',
 'brought',
 'basket',
 'basis',
 'basic',
 'binary',
 'beyond',
 'bars',
 'beginning',
 'bank',
 'bands',
 'brother',
 'banner',
 'billion',
 'broadcast',
 'bill',
 'biondich',
 'bearing',
 'boat',
 'build',
 'barset',
 'down',
 'cos',
 'citarequerida',
 'dewiki',
 'cellpading',
 'current',
 'density',
 'could',
 'due',
 'called',
 'complex',
 'characters',
 'disease',
 'covers',
 'common',
 'did',
 'domain',
 'different',
 'dec',
 'children',
 'chapter',
 'compter',
 'coauthors',
 'does',
 'climate',
 'deux',
 'design',
 'countries',
 'cabaret',
 'camp',
 'district',
 'crop',
 'changes',
 'community',
 'checklist',
 'call',
 'close',
 'church',
 'channel',
 'core',
 'contribution',
 'concert',
 'computer',
 'callsign',
 'doom',
 'console',
 'character',
 'darkblue',
 'cqranking',
 'conf',
 'dinosaur',
 'circle',
 'diesel',
 'coverage',
 'def',
 'child',
 'court',
 'coast',
 'detail',
 'charter',
 'construction',
 'crossover',
 'crash',
 'dream',
 'dog',
 'catalina',
 'caribe',
 'career',
 'cquote',
 'darkgrey',
 'crew',
 'choke',
 'discovery',
 'circ',
 'dinosaurs',
 'cycle',
 'dello',
 'colour',
 'clasification',
 'cinerea',
 'contre',
 'codes',
 'crack',
 'deutschen',
 'det',
 'cols',
 'concept',
 'dmoz',
 'came',
 'door',
 'comme',
 'chief',
 'conservation',
 'durch',
 'care',
 'drive',
 'clinical',
 'captain',
 'dinger',
 'conference',
 'drug',
 'dependent',
 'delete',
 'diagram',
 'critical',
 'download',
 'depuis',
 'dateformat',
 'daimy',
 'caloresp',
 'cen',
 'deep',
 'demographics',
 'cornflowerblue',
 'discolor',
 'dai',
 'created',
 'classical',
 'downarrow',
 'county',
 'centered',
 'diferenciable',
 'decrease',
 'drum',
 'direction',
 'document',
 'contemporary ',
 'direct',
 'carbon',
 'conditions',
 'chemical',
 'died',
 'chance ',
 'coming',
 'divcolend',
 'coupé',
 'commentary',
 'certain',
 'cool',
 'considered ',
 'distance',
 'crowned',
 'drag',
 'chromosome',
 'drawing',
 'commercial',
 'comparison',
 'certifications',
 'divisions',
 'conflict ',
 'campaign',
 'champ',
 'containing',
 'comments',
 'composition',
 'controlled',
 'discussion',
 'definition',
 'clubdebutjug',
 'clubretirojug',
 'disorder',
 'developed',
 'catfishes',
 'damage',
 'consul',
 'condita',
 'constant',
 'deluxe',
 'crimson',
 'códigopostal',
 'click',
 'correct',
 'claims',
 'cameos',
 'corps',
 'carry',
 'decoration',
 'copy',
 'confirmed',
 'chemistry',
 'commune',
 'collected',
 'dubium',
 'discovered',
 'discography',
 'classic',
 'custom',
 'comparative',
 'citocromo',
 'carrier',
 'divisional',
 'deutsche',
 'clock',
 'drugs',
 'contact',
 'dollar',
 'documentary',
 'degree',
 'continued',
 'cette',
 'descripcion',
 'curul',
 'context',
 'create',
 'command',
 'choose',
 'compilation',
 'castle',
 'caused',
 'changed',
 'drums',
 'daughter',
 'cold',
 'ranking',
 'edition',
 'rap',
 'remix',
 'miniaturadeimagen',
 'wikisource',
 'some',
 'náhuatl',
 'futbol',
 'used',
 'histoire',
 'scriptstyle',
 'inch',
 'géographique',
 'manager',
 'nombredenacimiento',
 'timeline',
 'tamañodelaimagen',
 'front',
 'rho',
 'province',
 'medium',
 'mathcal',
 'widht',
 'wiktionary',
 'janvier',
 'windowtext',
 'vie',
 'squad',
 'pags',
 'subcampeonato',
 'snow',
 'light',
 'folklore',
 'theory',
 'lieu',
 'established',
 'river',
 'enwiki',
 'spin',
 'increment',
 'rigth',
 'historical',
 'sign',
 'justify',
 'languages',
 'television',
 'textoimagen',
 'frame',
 'underground',
 'motorcycle',
 'point',
 'function',
 'school',
 'satelital',
 'make',
 'thrash',
 'identification',
 'jockey',
 'international',
 'return',
 'systematics',
 'suplex',
 'open',
 'nigra',
 'mangaka',
 'form',
 'same',
 'oise',
 'gene',
 'rangle',
 'get',
 'stage',
 'here',
 'limegreen',
 'uruguay',
 'evidence',
 'modern',
 'how',
 'thriller',
 'über',
 'es',
 'while',
 'very',
 'order',
 'short',
 'know',
 'strong',
 'vnormal',
 'orig',
 'eta',
 'remixes',
 'trailer',
 'reapertura',
 'topofi',
 'mod',
 'soundtrack',
 'officinalis',
 'slam',
 'matrix',
 'zum',
 'ninja',
 'million',
 'foundation',
 'staff',
 'just',
 'wave',
 'south',
 'good',
 'tree',
 'event',
 'orientation',
 'nach',
 'letter',
 'still',
 'sapiens',
 'publication',
 'pretemporada',
 'take',
 'elevation',
 'unicode',
 'tomato',
 'leg',
 'varphi',
 'orientalis',
 'utc',
 'overline',
 'sir',
 'rayon',
 'grunge',
 'project',
 'timezone',
 'situ',
 'town',
 'systems',
 'own',
 'related',
 'later',
 'transparent',
 'portrait',
 'share',
 'metric',
 'road',
 'ping',
 'little',
 'women',
 'prod',
 'girl',
 'ok',
 'near',
 'vcrucero',
 'temps',
 'great',
 'fechatermina',
 'vnexceder',
 'perrow',
 'future',
 'says',
 'hindi',
 'editors',
 'hex',
 'vpérdida',
 'grandesvictorias',
 'seal',
 'mer',
 'skyline',
 'never',
 'law',
 'example',
 'support',
 'epsilon',
 'heart',
 'named',
 'japonica',
 'gays',
 'said',
 'special',
 'host',
 'sex',
 'self',
 'young',
 'prize',
 'treatment',
 'male',
 'living',
 'rightarrow',
 'swing',
 'much',
 'obrasdestacadas',
 'sequence',
 'opening',
 'fire',
 'hemiptera',
 'vigueur',
 'food',
 'won',
 'term',
 'kick',
 'edited',
 'each',
 'military',
 'phylogeny',
 'pole',
 'making',
 'pers',
 'nes',
 'shock',
 'should',
 'purple',
 'homme',
 'subcontinente',
 'romaji',
 'half',
 'introduction',
 'relationships',
 'hobbit',
 'effects',
 'say',
 'phylogenetic',
 'growth',
 'extrasolares',
 'och',
 'five',
 'temp',
 'effect',
 'standard',
 'mexica',
 'grand',
 'familytree',
 'office',
 'stop',
 'rue',
 'vmcontrol',
 'vitro',
 'sound',
 'pecíolo',
 'vom',
 'urban',
 'ever',
 'released',
 'gridcolor',
 'even',
 'hot',
 'must',
 'forall',
 'reflist',
 'stic',
 'olympic',
 'translation',
 'those',
 'techno',
 'sciences',
 'employees',
 'refs',
 'pmatrix',
 'groups',
 'several',
 'level',
 'program',
 'mid',
 'fierro',
 'past',
 'tamil',
 'period',
 'vita',
 'far',
 'syndrome',
 'third',
 'nororiental',
 'increase',
 'ttingen',
 'literature',
 'ichi',
 'juntoa',
 'focus',
 'train',
 'sample',
 'religion',
 'given',
 'west',
 'relief',
 'exjugador',
 'shogunato',
 'ich',
 'shoulder',
 'ppen',
 'premier',
 'transfermarkt',
 'widths',
 'motion',
 'include',
 'singer',
 'voice',
 'mac',
 'energy',
 'vous',
 'mais',
 'maritima',
 'until',
 'prettytable',
 'heights',
 'intro',
 'instrumentalista',
 'imagesize',
 'influidopor',
 'holotipo',
 'following',
 'female',
 'works',
 'question',
 'patron',
 'gets',
 'want',
 'taxonomic',
 'engine',
 'various',
 'patients',
 'paper',
 'memory',
 'health',
 'tablabonita',
 'seen',
 'mort',
 'island',
 'otroresultado',
 'nchengladbach',
 'grandiflora',
 'endisputa',
 'rad',
 'fm',
 'vulgare',
 'scientific',
 'ran',
 'word',
 'wordmark',
 'sunt',
 'port',
 'emol',
 'got',
 'navy',
 'pieescudo',
 'survey',
 'whiteborder',
 'isle',
 'speed',
 'primerministro',
 'person',
 'woman',
 'mia',
 'possible',
 'guerre',
 'oder',
 'genre',
 'latifolia',
 'quo',
 'gi',
 'former',
 'wide',
 'om',
 'influenza',
 'trend',
 'force',
 'oil',
 'split',
 'operating',
 'ldots',
 'lim',
 'fun',
 'mir',
 'éditions',
 'transepto',
 'shot',
 'mellifera',
 'heel',
 'esq',
 'lemonchiffon',
 'rhythm',
 'polis',
 'wins',
 'switch',
 'wild',
 'planet',
 'ship',
 'northern',
 'naturelle',
 'mov',
 'mayoria',
 'formation',
 'technology',
 'pushpin',
 'think',
 'sitcom',
 'hand',
 'takes',
 'língua',
 'episodes',
 'soccerway',
 'numbers',
 'links',
 'sativa',
 'général',
 'union',
 'fact',
 'written',
 'radius',
 'encurso',
 'includes',
 'others',
 'ending',
 'tennis',
 'often',
 'neogótico',
 'killed',
 'fall',
 'race',
 'lost',
 'fareast',
 'seléucida',
 'today',
 'fig',
 'tests',
 'langle',
 'humilis',
 'polluelos',
 'palustris',
 'important',
 'layer',
 'fricativa',
 'pack',
 'sylvestris',
 'extrasolar',
 'relanzamiento',
 'premiere',
 'tank',
 'states',
 'sectio',
 'rate',
 'secret',
 'park',
 'king',
 'glam',
 'forces',
 'shield',
 'minus',
 'nomen',
 'habitacionales',
 'maculata',
 'imagemap',
 'fitogeográfico',
 'taxonomy',
 'nicht',
 'goes',
 'types',
 'movement',
 'gubernatura',
 'niger',
 'specific',
 'street',
 'ph',
 'textcolor',
 'postscript',
 'flight',
 'imagem',
 'geomorfología',
 'rect',
 'mara',
 'wikiespecies',
 'implications',
 'royal',
 'framework',
 'spec',
 'operatorname',
 'sont',
 'museum',
 'rankings',
 'problem',
 'hash',
 'nigsberg',
 'mathfrak',
 'partidobk',
 'void',
 'signs',
 'historique',
 'musician',
 'reggaeton',
 'member',
 'earth',
 'zombies',
 'why',
 'strike',
 'rights',
 'ránking',
 'positions',
 'lingua',
 'held',
 'obrasdestacadas',
 'otroresultado',
 'strada',
 'autostrada',
 'cdbpasada',
 'passado'
]

correcciones = {}#excluidos.correcciones


ambiguas = [
 'sedió',
 'pedió',
 'haberon',
]

reglas = {}
valores = set()
funciones2 = {}
funciones3 = {}
funciones4 = {}


def regOnes(t, v):
  w=v.replace('ón', 'ones')
  reglas[w] = [v, t]
funciones2['pOnes'] = regOnes

def regCes(t, v):
  raiz = v[0:len(v)-1]
  reglas[raiz+'ces'] = [v, t]
funciones2['pCes'] = regCes

def regEs(t, v):
  reglas[v+'es'] = [v, t]
funciones2['pEs'] = regEs

def regA(t, v):
  reglas[v+'es'] = [v, t]
  reglas[v+'a'] = [v, t]
  reglas[v+'as'] = [v, t]
funciones2['pA'] = regA

def regAs(t, v):
  raiz = v[0:len(v)-1]
  reglas[raiz+'a'] = [v, t]
  reglas[raiz+'as'] = [v, t]
  reglas[raiz+'os'] = [v, t]
  #print(raiz+'--as')
funciones2['pAs'] = regAs

def regS(t, v):
  reglas[v+'s'] = [v, t]
#  print(c+'--'+w)
funciones2['pS'] = regS

def regCambiar(t, v):
  raiz = v[0:len(v)-2]
#  raiz = v.replace('ar','')
  par = [v, t]
#  print(raiz+'--ado')
  reglas[raiz+'a'      ] = par
  reglas[raiz+'ó'      ] = par
  reglas[raiz+'aron'   ] = par
  reglas[raiz+'ada'    ] = par
  reglas[raiz+'ado'    ] = par
  reglas[raiz+'adas'   ] = par
  reglas[raiz+'ados'   ] = par
  reglas[raiz+'an'     ] = par
  reglas[raiz+'ando'   ] = par
  reglas[raiz+'aremos' ] = par
  reglas[raiz+'aría'   ] = par
  reglas[raiz+'arías'  ] = par
  reglas[raiz+'arían ' ] = par
  reglas[raiz+'e'      ] = par
  reglas[raiz+'en'     ] = par
  reglas[raiz+'ará'    ] = par
  reglas[raiz+'arán'   ] = par
  reglas[raiz+'arás'   ] = par
funciones2['iCambiar'] = regCambiar


def regPartir(t, v):
  raiz = v[0:len(v)-2]
#  raiz = v.replace('ir','')
  par = [v, t]
  reglas[raiz+'iendo'] = par
#  print(raiz+'--ido')
  reglas[raiz+'a'     ] = par
  reglas[raiz+'irá'   ] = par
  reglas[raiz+'irán'   ] = par
  reglas[raiz+'irás'   ] = par
  reglas[raiz+'iría'  ] = par
  reglas[raiz+'irías' ] = par
  reglas[raiz+'irían' ] = par
  reglas[raiz+'an'  ] = par
  reglas[raiz+'as'  ] = par
  reglas[raiz+'e'   ] = par
  reglas[raiz+'en'  ] = par
  reglas[raiz+'ida' ] = par
  reglas[raiz+'idas'] = par
  reglas[raiz+'ido' ] = par
  reglas[raiz+'idos'] = par
  reglas[raiz+'imos'] = par
  reglas[raiz+'í'   ] = par
  reglas[raiz+'ía'  ] = par
  reglas[raiz+'ían' ] = par
  reglas[raiz+'ías' ] = par
  reglas[raiz+'ió'  ] = par
  reglas[raiz+'ieron'  ] = par
  reglas[raiz+'iera'  ] = par
  reglas[raiz+'ieran'  ] = par
  reglas[raiz+'ieras'  ] = par
funciones2['iPartir'] = regPartir

def regAmar(t, v):
  raiz = v[0:len(v)-2]
  #raiz = v.replace('ar','')
  par = [v, t]
  #print(raiz+'--ado')
  reglas[raiz+'a'    ] = par
  reglas[raiz+'aba'  ] = par
  reglas[raiz+'aban' ] = par
  reglas[raiz+'abas' ] = par
  reglas[raiz+'ada'  ] = par
  reglas[raiz+'adas' ] = par
  reglas[raiz+'ado'  ] = par
  reglas[raiz+'ados' ] = par
  reglas[raiz+'ara'  ] = par
  reglas[raiz+'aran' ] = par
  reglas[raiz+'aras' ] = par
  reglas[raiz+'an'   ] = par
  reglas[raiz+'ando' ] = par
  reglas[raiz+'ará'  ] = par
  reglas[raiz+'arán' ] = par
  reglas[raiz+'arás' ] = par
  reglas[raiz+'aría' ] = par
  reglas[raiz+'arían'  ] = par
  reglas[raiz+'arías'  ] = par
  reglas[raiz+'aron' ] = par
  reglas[raiz+'as'   ] = par
  reglas[raiz+'e'    ] = par
  reglas[raiz+'en'   ] = par
  reglas[raiz+'es'   ] = par
  reglas[raiz+'o'    ] = par
  reglas[raiz+'á'    ] = par
  reglas[raiz+'ó'    ] = par
  reglas[raiz+'aron'    ] = par
funciones2['iAmar'] = regAmar

def regVaciar(t, v):
  raiz = v[0:len(v)-3]
  #raiz = v.replace('iar','')
  par = [v, t]
  #print(raiz+'--iado')
  reglas[raiz+'iaba'  ] = par
  reglas[raiz+'iaban' ] = par
  reglas[raiz+'iabas' ] = par
  reglas[raiz+'iada'  ] = par
  reglas[raiz+'iadas' ] = par
  reglas[raiz+'iado'  ] = par
  reglas[raiz+'iados' ] = par
  reglas[raiz+'iando' ] = par
  reglas[raiz+'iara'  ] = par
  reglas[raiz+'iaran' ] = par
  reglas[raiz+'iaras' ] = par
  reglas[raiz+'iaría' ] = par
  reglas[raiz+'iarías' ] = par
  reglas[raiz+'iarían' ] = par
  reglas[raiz+'iaron' ] = par
  reglas[raiz+'iará'  ] = par
  reglas[raiz+'ié'    ] = par
  reglas[raiz+'ió'    ] = par
  reglas[raiz+'iaron' ] = par
  reglas[raiz+'ía'    ] = par
  reglas[raiz+'ían'   ] = par
  reglas[raiz+'ías'   ] = par
  reglas[raiz+'íe'    ] = par
  reglas[raiz+'íen'   ] = par
  reglas[raiz+'íes'   ] = par
  reglas[raiz+'ío'    ] = par
funciones2['iVaciar'] = regVaciar

def regSeguir(t, v):
  raiz = v[0:len(v)-5]
  #raiz = v.replace('eguir','')
  par = [v, t]
  #print(raiz+'--eguido')
  reglas[raiz+'eguida'   ] = par
  reglas[raiz+'eguidas'  ] = par
  reglas[raiz+'eguido'   ] = par
  reglas[raiz+'eguidos'  ] = par
  reglas[raiz+'eguí'     ] = par
  reglas[raiz+'eguirá'   ] = par
  reglas[raiz+'eguirás'  ] = par
  reglas[raiz+'eguirán'  ] = par
  reglas[raiz+'eguía'    ] = par
  reglas[raiz+'eguían'   ] = par
  reglas[raiz+'eguías'   ] = par
  reglas[raiz+'iga'      ] = par
  reglas[raiz+'igan'     ] = par
  reglas[raiz+'igas'     ] = par
  reglas[raiz+'igo'      ] = par
  reglas[raiz+'igue'     ] = par
  reglas[raiz+'iguen'    ] = par
  reglas[raiz+'igues'    ] = par
  reglas[raiz+'iguiendo' ] = par
  reglas[raiz+'iguiera'  ] = par
  reglas[raiz+'iguieran' ] = par
  reglas[raiz+'iguieras' ] = par
  reglas[raiz+'iguieron' ] = par
  reglas[raiz+'iguiese'  ] = par
  reglas[raiz+'iguiesen' ] = par
  reglas[raiz+'iguieses' ] = par
  reglas[raiz+'iguió'    ] = par
  reglas[raiz+'iguieron'    ] = par
funciones2['iSeguir'] = regSeguir

def regCoger(t, v):
  raiz = v[0:len(v)-3]
  #raiz = v.replace('ger','')
  par = [v, t]
  #print(raiz+'--guido')
  reglas[raiz+'ge'     ] = par
  reglas[raiz+'gen'    ] = par
  reglas[raiz+'gería'  ] = par
  reglas[raiz+'gerían' ] = par
  reglas[raiz+'gerías' ] = par
  reglas[raiz+'ges'    ] = par
  reglas[raiz+'gerá'   ] = par
  reglas[raiz+'gerán'  ] = par
  reglas[raiz+'gerás'  ] = par
  reglas[raiz+'giera'  ] = par
  reglas[raiz+'gieran' ] = par
  reglas[raiz+'gieras' ] = par
  reglas[raiz+'gieron' ] = par
  reglas[raiz+'giesen' ] = par
  reglas[raiz+'gió'    ] = par
  reglas[raiz+'gieron' ] = par
  reglas[raiz+'guida'  ] = par
  reglas[raiz+'guidas' ] = par
  reglas[raiz+'guido'  ] = par
  reglas[raiz+'guidos' ] = par
  reglas[raiz+'gí'     ] = par
  reglas[raiz+'ja'     ] = par
  reglas[raiz+'jan'    ] = par
  reglas[raiz+'jas'    ] = par
  reglas[raiz+'jo'     ] = par
funciones2['iCoger'] = regCoger

def regConducir(t, v):
  raiz = v[0:len(v)-3]
  #raiz = v.replace('cir','')
  par = [v, t]
  #print(raiz+'--cido')
  reglas[raiz+'ce'     ] = par
  reglas[raiz+'cen'    ] = par
  reglas[raiz+'ces'    ] = par
  reglas[raiz+'cida'   ] = par
  reglas[raiz+'cidas'  ] = par
  reglas[raiz+'cido'   ] = par
  reglas[raiz+'cidos'  ] = par
  reglas[raiz+'ciendo' ] = par
  reglas[raiz+'cirá'   ] = par
  reglas[raiz+'cirás'  ] = par
  reglas[raiz+'cirán'  ] = par
  reglas[raiz+'ciré'   ] = par
  reglas[raiz+'cía'    ] = par
  reglas[raiz+'cían'   ] = par
  reglas[raiz+'cías'   ] = par
  reglas[raiz+'ciría'    ] = par
  reglas[raiz+'cirías'   ] = par
  reglas[raiz+'cirían'   ] = par
  reglas[raiz+'je'     ] = par
  reglas[raiz+'jera'   ] = par
  reglas[raiz+'jeran'  ] = par
  reglas[raiz+'jeras'  ] = par
  reglas[raiz+'jeron'  ] = par
  reglas[raiz+'jese'   ] = par
  reglas[raiz+'jesen'  ] = par
  reglas[raiz+'jeses'  ] = par
  reglas[raiz+'jo'     ] = par
  reglas[raiz+'jeron'  ] = par
  reglas[raiz+'zca'    ] = par
  reglas[raiz+'zcan'   ] = par
  reglas[raiz+'zcas'   ] = par
  reglas[raiz+'zco'    ] = par
funciones2['iConducir'] = regConducir

def regTemer(t, v):
  raiz = v[0:len(v)-2]
  #raiz = v.replace('ar','')
  par = [v, t]
  #print(raiz+'--ido')
  reglas[raiz+'o'    ] = par
  reglas[raiz+'es'   ] = par
  reglas[raiz+'e'    ] = par
  reglas[raiz+'en'   ] = par
  reglas[raiz+'ía'   ] = par
  reglas[raiz+'ían'  ] = par
  reglas[raiz+'ías'  ] = par
  reglas[raiz+'ería'  ] = par
  reglas[raiz+'erían'  ] = par
  reglas[raiz+'erías'  ] = par
  reglas[raiz+'erá'  ] = par
  reglas[raiz+'erán' ] = par
  reglas[raiz+'erás' ] = par
  reglas[raiz+'ido'  ] = par
  reglas[raiz+'ida'  ] = par
  reglas[raiz+'idos' ] = par
  reglas[raiz+'idas' ] = par
  reglas[raiz+'iendo'] = par
  reglas[raiz+'í'    ] = par
  reglas[raiz+'ió'   ] = par
  reglas[raiz+'ieron'] = par
  reglas[raiz+'iste' ] = par
  reglas[raiz+'a'    ] = par
  reglas[raiz+'as'    ] = par
  reglas[raiz+'an'    ] = par
funciones2['iTemer'] = regTemer

def regHuir(t, v):
  raiz = v[0:len(v)-2]
  par = [v, t]
  #print(raiz+'--ido')
  reglas[raiz+'yendo'    ] = par
  reglas[raiz+'ido'  ] = par
  reglas[raiz+'ida' ] = par
  reglas[raiz+'idos' ] = par
  reglas[raiz+'idas'  ] = par
  reglas[raiz+'yo' ] = par
  reglas[raiz+'yes'  ] = par
  reglas[raiz+'ye' ] = par
  reglas[raiz+'yen' ] = par
  reglas[raiz+'i'   ] = par
  reglas[raiz+'í' ] = par
  reglas[raiz+'ía' ] = par
  reglas[raiz+'ías' ] = par
  reglas[raiz+'ían' ] = par
  reglas[raiz+'yó'  ] = par
  reglas[raiz+'yeron' ] = par
  reglas[raiz+'ya'   ] = par
  reglas[raiz+'yas'    ] = par
  reglas[raiz+'yan'   ] = par
  reglas[raiz+'iré'   ] = par
  reglas[raiz+'irá'    ] = par
  reglas[raiz+'iría'    ] = par
  reglas[raiz+'irías'   ] = par
  reglas[raiz+'irían'   ] = par
  reglas[raiz+'irán'    ] = par
  reglas[raiz+'irás'    ] = par
  reglas[raiz+'imos'    ] = par
funciones2['iHuir'] = regHuir

def regAgradecer(t, v):
  raiz = v[0:len(v)-3]
  #raiz = v.replace('ar','')
  par = [v, t]
  #print(raiz+'--cido')
  reglas[raiz+'ciendo'  ] = par
  reglas[raiz+'cieron'  ] = par
  reglas[raiz+'cido'    ] = par
  reglas[raiz+'cida'    ] = par
  reglas[raiz+'cidos'   ] = par
  reglas[raiz+'cidas'   ] = par
  reglas[raiz+'ce'      ] = par
  reglas[raiz+'cen'     ] = par
  reglas[raiz+'zco'     ] = par
  reglas[raiz+'zca'     ] = par
  reglas[raiz+'zcas'    ] = par
  reglas[raiz+'zcan'    ] = par
  reglas[raiz+'cí'      ] = par
  reglas[raiz+'cía'      ] = par
  reglas[raiz+'cían'      ] = par
  reglas[raiz+'cías'      ] = par
  reglas[raiz+'cería'   ] = par
  reglas[raiz+'cerías'  ] = par
  reglas[raiz+'cerían'  ] = par
  reglas[raiz+'ció'     ] = par
  reglas[raiz+'cieron'  ] = par
  reglas[raiz+'ciera'  ] = par
  reglas[raiz+'cieran'  ] = par
  reglas[raiz+'cieras'  ] = par
  reglas[raiz+'ceré'    ] = par
  reglas[raiz+'cerás'   ] = par
  reglas[raiz+'cerá'    ] = par
  reglas[raiz+'cerán'   ] = par
funciones2['iAgradecer'] = regAgradecer

def regTraer(t, v):
  raiz = v[0:len(v)-2]
  #raiz = v.replace('er','')
  par = [v, t]
  #print(raiz+'--jo')
  reglas[raiz+'e'    ] = par
  reglas[raiz+'jo'   ] = par
  reglas[raiz+'jeron'] = par
  reglas[raiz+'jiste'] = par
  reglas[raiz+'ída'  ] = par
  reglas[raiz+'ídas' ] = par
  reglas[raiz+'ído'  ] = par
  reglas[raiz+'ídos' ] = par
  reglas[raiz+'emos' ] = par
  reglas[raiz+'ía'   ] = par
  reglas[raiz+'ías'  ] = par
  reglas[raiz+'ían'  ] = par
  reglas[raiz+'ería' ] = par
  reglas[raiz+'erías'] = par
  reglas[raiz+'erían'] = par
  reglas[raiz+'en'   ] = par
  reglas[raiz+'yendo'] = par
  reglas[raiz+'erá'  ] = par
  reglas[raiz+'erán' ] = par
  reglas[raiz+'erás' ] = par
  reglas[raiz+'es'   ] = par
  reglas[raiz+'e'    ] = par
  reglas[raiz+'en'   ] = par
  reglas[raiz+'iga'  ] = par
  reglas[raiz+'jo'   ] = par
funciones2['iTraer'] = regTraer

def regCazar(t, v):
  raiz = v[0:len(v)-3]#.encode('utf-8')
#  raiz = v.replace('zar','')
  par = [v, t]
  #print(raiz+"ce")
  reglas[raiz+'ce'   ] = par
  reglas[raiz+'cen'  ] = par
  reglas[raiz+'ces'  ] = par
  reglas[raiz+'za'   ] = par
  reglas[raiz+'zaba' ] = par
  reglas[raiz+'zaban'] = par
  reglas[raiz+'zabas'] = par
  reglas[raiz+'zada' ] = par
  reglas[raiz+'zadas'] = par
  reglas[raiz+'zado' ] = par
  reglas[raiz+'zados'] = par
  reglas[raiz+'zamos'] = par
  reglas[raiz+'zan'  ] = par
  reglas[raiz+'zando'] = par
  reglas[raiz+'zará' ] = par
  reglas[raiz+'zarán'] = par
  reglas[raiz+'zarás'] = par
  reglas[raiz+'zaría' ] = par
  reglas[raiz+'zarías'] = par
  reglas[raiz+'zarían'] = par
  reglas[raiz+'zas'  ] = par
  reglas[raiz+'zon'  ] = par
  reglas[raiz+'zó'   ] = par
  reglas[raiz+'zaron'] = par
funciones2['iCazar'] = regCazar

def regAdecuar(t, v): #Sin diferencia con amar en los casos incluidos aquí
  raiz = v[0:len(v)-2]
#  raiz = v.replace('ar','')
  par = [v, t]
#  print(raiz+'--ado')
  reglas[raiz+'a'   ] = par
  reglas[raiz+'aba' ] = par
  reglas[raiz+'aban'] = par
  reglas[raiz+'abas'] = par
  reglas[raiz+'ada' ] = par
  reglas[raiz+'adas'] = par
  reglas[raiz+'ado' ] = par
  reglas[raiz+'ados'] = par
  reglas[raiz+'amos'] = par
  reglas[raiz+'an'  ] = par
  reglas[raiz+'ando'] = par
  reglas[raiz+'ará' ] = par
  reglas[raiz+'arán'] = par
  reglas[raiz+'arás'] = par
  reglas[raiz+'aría' ] = par
  reglas[raiz+'arías'] = par
  reglas[raiz+'arían'] = par
  reglas[raiz+'as'  ] = par
  reglas[raiz+'e'   ] = par
  reglas[raiz+'en'  ] = par
  reglas[raiz+'es'  ] = par
  reglas[raiz+'o'   ] = par
  reglas[raiz+'ó'   ] = par
funciones2['iAdecuar'] = regAdecuar

def regLlegar(t, v):
  raiz = v[0:len(v)-2]
#  raiz = v.replace('ar','')
  par = [v, t]
#  print(raiz+'--ado')
  reglas[raiz+'a'   ] = par
  reglas[raiz+'aba' ] = par
  reglas[raiz+'aban'] = par
  reglas[raiz+'abas'] = par
  reglas[raiz+'ada' ] = par
  reglas[raiz+'adas'] = par
  reglas[raiz+'ado' ] = par
  reglas[raiz+'ados'] = par
  reglas[raiz+'amos'] = par
  reglas[raiz+'an'  ] = par
  reglas[raiz+'ando'] = par
  reglas[raiz+'ará' ] = par
  reglas[raiz+'arán'] = par
  reglas[raiz+'arás'] = par
  reglas[raiz+'aría' ] = par
  reglas[raiz+'arías'] = par
  reglas[raiz+'arían'] = par
  reglas[raiz+'as'  ] = par
  reglas[raiz+'ue'  ] = par
  reglas[raiz+'uen' ] = par
  reglas[raiz+'ues' ] = par
  reglas[raiz+'ó'   ] = par
  reglas[raiz+'aron'   ] = par
funciones2['iLlegar'] = regLlegar

def regDesapegarse(t, v):
  raiz = v[0:len(v)-4]
#  raiz = v.replace('arse','')
  par = [v, t]
#  print(raiz+'--ado')
  reglas[raiz+'a'   ] = par
  reglas[raiz+'aba' ] = par
  reglas[raiz+'aban'] = par
  reglas[raiz+'abas'] = par
  reglas[raiz+'ada' ] = par
  reglas[raiz+'adas'] = par
  reglas[raiz+'ado' ] = par
  reglas[raiz+'ados'] = par
  reglas[raiz+'amos'] = par
  reglas[raiz+'an'  ] = par
  reglas[raiz+'ando'] = par
  reglas[raiz+'ará' ] = par
  reglas[raiz+'arán'] = par
  reglas[raiz+'arás'] = par
  reglas[raiz+'aría' ] = par
  reglas[raiz+'arías'] = par
  reglas[raiz+'arían'] = par
  reglas[raiz+'as'  ] = par
  reglas[raiz+'ue'  ] = par
  reglas[raiz+'uen' ] = par
  reglas[raiz+'ues' ] = par
  reglas[raiz+'ó'   ] = par
  reglas[raiz+'aron'   ] = par
funciones2['iDesapegarse'] = regDesapegarse

def regSacar(t, v):
  raiz = v[0:len(v)-3]
#  raiz = v.replace('car','')
  par = [v, t]
  #print(raiz+'--cado')
  reglas[raiz+'ca'   ] = par
  reglas[raiz+'caba' ] = par
  reglas[raiz+'caban'] = par
  reglas[raiz+'cabas'] = par
  reglas[raiz+'cada' ] = par
  reglas[raiz+'cadas'] = par
  reglas[raiz+'cado' ] = par
  reglas[raiz+'caron' ] = par
  reglas[raiz+'cados'] = par
  reglas[raiz+'camos'] = par
  reglas[raiz+'can'  ] = par
  reglas[raiz+'cando'] = par
  reglas[raiz+'cará' ] = par
  reglas[raiz+'carán'] = par
  reglas[raiz+'carás'] = par
  reglas[raiz+'caría' ] = par
  reglas[raiz+'carías'] = par
  reglas[raiz+'carían'] = par
  reglas[raiz+'cas'  ] = par
  reglas[raiz+'có'   ] = par
  reglas[raiz+'caron'   ] = par
  reglas[raiz+'que'  ] = par
  reglas[raiz+'quen' ] = par
  reglas[raiz+'ques' ] = par
funciones2['iSacar'] = regSacar

def regSacarse(t, v):
  raiz = v[0:len(v)-5]
#  raiz = v.replace('carse','')
  par = [v, t]
#  print(raiz+'--ado')
  reglas[raiz+'ca'   ] = par
  reglas[raiz+'caba' ] = par
  reglas[raiz+'caban'] = par
  reglas[raiz+'cabas'] = par
  reglas[raiz+'cada' ] = par
  reglas[raiz+'cadas'] = par
  reglas[raiz+'cado' ] = par
  reglas[raiz+'cados'] = par
  reglas[raiz+'camos'] = par
  reglas[raiz+'can'  ] = par
  reglas[raiz+'cando'] = par
  reglas[raiz+'cará' ] = par
  reglas[raiz+'carás' ] = par
  reglas[raiz+'carán' ] = par
  reglas[raiz+'caría' ] = par
  reglas[raiz+'carías'] = par
  reglas[raiz+'carían'] = par
  reglas[raiz+'cas'  ] = par
  reglas[raiz+'có'   ] = par
  reglas[raiz+'caron'] = par
  reglas[raiz+'que'  ] = par
  reglas[raiz+'quen' ] = par
  reglas[raiz+'ques' ] = par
funciones2['iSacarse'] = regSacarse
 
def regReponer(t, v):
  raiz = v[0:len(v)-4]
#  raiz = v.replace('oner','')
  par = [v, t]
#  print(raiz+'--uesto')
  reglas[raiz+'oniendo'   ] = par
  reglas[raiz+'ongo'   ] = par
  reglas[raiz+'onga'   ] = par
  reglas[raiz+'ongan'   ] = par
  reglas[raiz+'ongas'   ] = par
  reglas[raiz+'ones' ] = par
  reglas[raiz+'one'] = par
  reglas[raiz+'onen'] = par
  reglas[raiz+'uesto' ] = par
  reglas[raiz+'uesta' ] = par
  reglas[raiz+'uestos' ] = par
  reglas[raiz+'uestas' ] = par
  reglas[raiz+'use'] = par
  reglas[raiz+'uso'] = par
  reglas[raiz+'usieron'] = par
  reglas[raiz+'ondré' ] = par
  reglas[raiz+'ondrá' ] = par
  reglas[raiz+'ondrán' ] = par
  reglas[raiz+'ondrás' ] = par
  reglas[raiz+'onía' ] = par
  reglas[raiz+'onían' ] = par
  reglas[raiz+'onías' ] = par
  reglas[raiz+'ondría' ] = par
  reglas[raiz+'ondrían' ] = par
  reglas[raiz+'ondrías' ] = par
funciones2['iReponer'] = regReponer
 
def regContar(t, v, s1):
  raiz = v[0:len(v)-2]
#  raiz = v.replace('ar','')
  raiz2 = s1[0:len(s1)-1]
#  raiz2 = s1.replace('o','')
  par = [v, t]
  #print(raiz+'--ado')
  #print(raiz2+'--a')
  reglas[raiz+'aba' ] = par
  reglas[raiz+'aban'] = par
  reglas[raiz+'abas'] = par
  reglas[raiz+'ada' ] = par
  reglas[raiz+'adas'] = par
  reglas[raiz+'ado' ] = par
  reglas[raiz+'ados'] = par
  reglas[raiz+'amos'] = par
  reglas[raiz+'ando'] = par
  reglas[raiz+'ará' ] = par
  reglas[raiz+'arán' ] = par
  reglas[raiz+'arás' ] = par
  reglas[raiz+'aría' ] = par
  reglas[raiz+'arías'] = par
  reglas[raiz+'arían'] = par
  reglas[raiz+'ó'   ] = par
  reglas[raiz+'aron'   ] = par
  reglas[raiz2+'a'  ] = par
  reglas[raiz2+'an' ] = par
  reglas[raiz2+'as' ] = par
  reglas[raiz2+'e'  ] = par
  reglas[raiz2+'en' ] = par
  reglas[raiz2+'es' ] = par
  reglas[raiz2+'o'  ] = par
funciones3['iContar'] = regContar

def regPedir(t, v, s1):
  raiz = v[0:len(v)-2]
#  raiz = v.replace('ar','')
  raiz2 = s1[0:len(s1)-5]
#  raiz2 = s1.replace('o','')
  par = [v, t]
  #print(raiz+'--ido')
  #print(raiz2+'--iendo')
  reglas[raiz+'ido'    ] = par
  reglas[raiz+'ida'    ] = par
  reglas[raiz+'idos'   ] = par
  reglas[raiz+'idas'   ] = par
  reglas[raiz+'í'      ] = par
  reglas[raiz+'imos'   ] = par
  reglas[raiz+'ía'     ] = par
  reglas[raiz+'ían'    ] = par
  reglas[raiz+'ías'    ] = par
  reglas[raiz+'iría'   ] = par
  reglas[raiz+'irías'  ] = par
  reglas[raiz+'irían'  ] = par
  reglas[raiz+'iré'    ] = par
  reglas[raiz+'irás'   ] = par
  reglas[raiz+'irá'    ] = par
  reglas[raiz+'irán'   ] = par
  reglas[raiz2+'o'     ] = par
  reglas[raiz2+'es'    ] = par
  reglas[raiz2+'e'     ] = par
  reglas[raiz2+'en'    ] = par
  reglas[raiz2+'a'     ] = par
  reglas[raiz2+'as'    ] = par
  reglas[raiz2+'an'    ] = par
  reglas[raiz2+'ió'    ] = par
  reglas[raiz2+'ieron' ] = par
  reglas[raiz2+'iera'  ] = par
  reglas[raiz2+'ieran' ] = par
  reglas[raiz2+'ieras' ] = par
  reglas[raiz2+'iese'  ] = par
  reglas[raiz2+'iesen' ] = par
  reglas[raiz2+'ieses' ] = par
  reglas[raiz2+'iere'  ] = par
  reglas[raiz2+'ieren' ] = par
  reglas[raiz2+'ieres' ] = par
funciones3['iPedir'] = regPedir

def regAcertar(t, v, s1):
  raiz = v[0:len(v)-2]
#  raiz = v.replace('ar','')
  raiz2 = s1[0:len(v)-1]
#  raiz2 = s1.replace('o','')
  par = [v, t]
  #print(raiz+'--ado')
  #print(raiz2+'--a')
  reglas[raiz+'aba'   ] = par
  reglas[raiz+'aban'  ] = par
  reglas[raiz+'abas'  ] = par
  reglas[raiz+'ó'     ] = par
  reglas[raiz+'aron'  ] = par
  reglas[raiz+'ará'   ] = par
  reglas[raiz+'arán'  ] = par
  reglas[raiz+'arás'  ] = par
  reglas[raiz+'aría'  ] = par
  reglas[raiz+'arían' ] = par
  reglas[raiz+'arías' ] = par
  reglas[raiz+'ado'   ] = par
  reglas[raiz+'ados'  ] = par
  reglas[raiz+'ada'   ] = par
  reglas[raiz+'adas'  ] = par
  reglas[raiz+'ando'  ] = par
  reglas[raiz2+'o'    ] = par
  reglas[raiz2+'as'   ] = par
  reglas[raiz2+'a'    ] = par
  reglas[raiz2+'an'   ] = par
  reglas[raiz2+'e'    ] = par
  reglas[raiz2+'es'   ] = par
  reglas[raiz2+'en'   ] = par
funciones3['iAcertar'] = regAcertar

def regEntender(t, v, s1):
  raiz = v[0:len(v)-2]
#  raiz = v.replace('ar','')
  raiz2 = s1[0:len(v)-1]
#  raiz2 = s1.replace('o','')
  par = [v, t]
#  print(raiz+'--iendo')
#  print(raiz2+'--o')
  reglas[raiz+'emos' ] = par
  reglas[raiz+'ido'] = par
  reglas[raiz+'ida'] = par
  reglas[raiz+'idos' ] = par
  reglas[raiz+'idas'] = par
  reglas[raiz+'iendo' ] = par
  reglas[raiz+'ía'] = par
  reglas[raiz+'ió'] = par
  reglas[raiz+'ieron'] = par
  reglas[raiz+'ías'] = par
  reglas[raiz+'ían'] = par
  reglas[raiz+'erá'  ] = par
  reglas[raiz+'erán' ] = par
  reglas[raiz+'erás' ] = par
  reglas[raiz+'ería'  ] = par
  reglas[raiz+'erías' ] = par
  reglas[raiz+'erían' ] = par
  reglas[raiz2+'o'  ] = par
  reglas[raiz2+'es' ] = par
  reglas[raiz2+'e' ] = par
  reglas[raiz2+'en' ] = par
  reglas[raiz2+'a' ] = par
  reglas[raiz2+'as'  ] = par
  reglas[raiz2+'an'  ] = par
funciones3['iEntender'] = regEntender

def regMover(t, v, s1):
  raiz = v[0:len(v)-2]
#  raiz = v.replace('er','')
  raiz2 = s1[0:len(v)-1]
#  raiz2 = s1.replace('o','')
  par = [v, t]
#  print(raiz+'--iendo')
#  print(raiz2+'--o')
  reglas[raiz+'emos' ] = par
  reglas[raiz+'ido'] = par
  reglas[raiz+'ida'] = par
  reglas[raiz+'idos' ] = par
  reglas[raiz+'idas'] = par
  reglas[raiz+'iendo' ] = par
  reglas[raiz+'ía'] = par
  reglas[raiz+'ió'] = par
  reglas[raiz+'ieron'] = par
  reglas[raiz+'ías'] = par
  reglas[raiz+'ían'] = par
  reglas[raiz+'erá'  ] = par
  reglas[raiz+'erán' ] = par
  reglas[raiz+'erás' ] = par
  reglas[raiz+'ería'  ] = par
  reglas[raiz+'erías' ] = par
  reglas[raiz+'erían' ] = par
  reglas[raiz2+'o'  ] = par
  reglas[raiz2+'es' ] = par
  reglas[raiz2+'e' ] = par
  reglas[raiz2+'en' ] = par
  reglas[raiz2+'a' ] = par
  reglas[raiz2+'as'  ] = par
  reglas[raiz2+'an'  ] = par
funciones3['iMover'] = regMover

def regSentir(t, v, s1, s2):
  raiz = v[0:len(v)-2]
  raiz2 = s1[0:len(s1)-4]
  raiz3 = s2[0:len(s2)-1]
  #print(raiz+'--ido')
  #print(raiz2+'--endo')
  #print(raiz3+'--o')
#  raiz = v.replace('ir','')
  par = [v, t]
  reglas[raiz2+'endo'] = par
  reglas[raiz2+'ó'    ] = par
  reglas[raiz2+'eron' ] = par
  reglas[raiz2+'era'  ] = par
  reglas[raiz2+'eras' ] = par
  reglas[raiz2+'eran' ] = par
  reglas[raiz2+'ese'  ] = par
  reglas[raiz2+'esen' ] = par
  reglas[raiz2+'eses' ] = par
  reglas[raiz2+'ere'  ] = par
  reglas[raiz2+'eres' ] = par
  reglas[raiz2+'eren' ] = par
  reglas[raiz3+'a'    ] = par
  reglas[raiz3+'as'   ] = par
  reglas[raiz3+'an'   ] = par
  reglas[raiz3+'o'    ] = par
  reglas[raiz3+'e'    ] = par
  reglas[raiz3+'es'   ] = par
  reglas[raiz3+'en'   ] = par
  reglas[raiz+'id'    ] = par
  reglas[raiz+'irá'   ] = par
  reglas[raiz+'irán'  ] = par
  reglas[raiz+'irás'  ] = par
  reglas[raiz+'an'    ] = par
  reglas[raiz+'as'    ] = par
  reglas[raiz+'ida'   ] = par
  reglas[raiz+'idas'  ] = par
  reglas[raiz+'ido'   ] = par
  reglas[raiz+'idos'  ] = par
  reglas[raiz+'imos'  ] = par
  reglas[raiz+'ía'    ] = par
  reglas[raiz+'ían'   ] = par
  reglas[raiz+'ías'   ] = par
  reglas[raiz+'iría'  ] = par
  reglas[raiz+'irían' ] = par
  reglas[raiz+'irías' ] = par
funciones4['iSentir'] = regSentir

def reg(t, v, *ks):
  if t in funciones2:
    funciones2[t](t,v)
  elif t in funciones3:
    funciones3[t](t,v, ks[0])
    ks = ks[1:len(ks)]
  elif t in funciones4:
    funciones4[t](t,v, ks[0], ks[1])
    ks = ks[2:len(ks)]
  valores.add(v)
  par = [v, t]
  for k in ks:
    reglas[k] = par


reg( '', 'alguno', 'algún', 'alguna', 'algunas', 'algunos' )
reg( '', 'almacén', 'almacenes' )
reg( '', 'ambos', 'ambas' )
reg( '', 'andén', 'andenes' )
reg( '', 'anfitrión', 'anfitriona', 'anfitrionas', 'anfitriones' )
reg( '', 'anglosajón', 'anglosajona', 'anglosajonas', 'anglosajones' )
reg( '', 'aquel', 'aquella', 'aquello', 'aquellos', 'aquellas' )
reg( '', 'aragonés', 'aragonesa', 'aragoneses', 'aragonesas' )
reg( '', 'autobús', 'autobuses' )
reg( '', 'bailarín', 'bailarina', 'bailarinas', 'bailarines' )
reg( '', 'campeón', 'campeona', 'campeónas', 'campeones' )
reg( '', 'capitán', 'capitanes' )
reg( '', 'carácter', 'caracteres' )
reg( '', 'catalán', 'catalana', 'catalanes', 'catalanas' )
reg( '', 'clon', 'clones' )
reg( '', 'cluster', 'clusters' )
reg( '', 'comodín', 'comodines' )
reg( '', 'computadora', 'computadoras', 'computadores', 'computador' )
reg( '', 'común', 'comunes' )
reg( '', 'crimen', 'crímenes' )
reg( '', 'cánon', 'cánones' )
reg( '', 'danés', 'danesa', 'daneses', 'danesas' )
reg( '', 'don', 'doña', 'doñas' )
reg( '', 'duque', 'duques', 'duquesa', 'duquesas' )
reg( '', 'emoticón', 'emoticones' )
reg( '', 'escocés', 'escocesa', 'escoceses', 'escocesas' )
reg( '', 'español', 'española', 'españolas', 'españoles' )
reg( '', 'francés', 'franceses', 'francesa', 'francesas' )
reg( '', 'holandés', 'holandesa', 'holandeses', 'holandesas' )
reg( '', 'huracán', 'huracanes' )
reg( '', 'imagen', 'imágenes' )
reg( '', 'inglés', 'inglesa', 'inglesas', 'ingleses' )
reg( '', 'irlandés', 'irlandesa', 'irlandeses', 'irlandesas' )
reg( '', 'japonés', 'japonesa', 'japonesas', 'japoneses' )
reg( '', 'jardín', 'jardines' )
reg( '', 'joven', 'jóvenes' )
reg( '', 'lingüística', 'lingüístico', 'lingüísticas', 'lingüísticos' )
reg( '', 'margen', 'márgenes' )
reg( '', 'marqués', 'marquesa', 'marqueses', 'marquesas' )
reg( '', 'matemáticas', 'matemáticos' )
reg( '', 'musulmán', 'musulmana', 'musulmanes', 'musulmanas' )
reg( '', 'musulmán', 'musulmanes' )
reg( '', 'neerlandés', 'neerlandesa', 'neerlandeses', 'neerlandesaa' )
reg( '', 'objetivo', 'objetivos', 'objetiva' )
reg( '', 'orden', 'órdenes' )
reg( '', 'portugués', 'portuguesa', 'portugueses', 'portuguesas' )
reg( '', 'razón', 'razones')
reg( '', 'reciénte', 'recién' )
reg( '', 'régimen', 'regímenes' )
reg( '', 'sendos', 'sendas' )
reg( '', 'sultán', 'sultánnes', 'sultána', 'sultánas' )
reg( '', 'violín', 'violines' )
reg( '', 'volcán', 'volcanes' )
reg( '', 'volumen', 'volúmenes' )
reg( '', 'vídeo', 'video' , 'videos' )
reg( 'As', 'regulador' )
reg( 'iAbolir', 'abolir', 'abolió', 'abolieron' )
reg( 'iAbolir', 'agredir', 'agredió', 'agredieron' )
reg( 'iAcertar', 'acertar', 'acierto' )
reg( 'iAcertar', 'acrecentar', 'acreciento' )
reg( 'iAcertar', 'alentar', 'aliento' )
reg( 'iAcertar', 'apacentar', 'apaciento' )
reg( 'iAcertar', 'apretar', 'aprieto' )
reg( 'iAcertar', 'arrendar', 'arriendo' )
reg( 'iAcertar', 'asentar', 'asiento', 'asentarse' )
reg( 'iAcertar', 'aserrar', 'asierro' )
reg( 'iAcertar', 'aterrar', 'atierro' )
reg( 'iAcertar', 'atestar', 'atiesto' )
reg( 'iAcertar', 'atravesar', 'atravieso' )
reg( 'iAcertar', 'aventar', 'aviento' )
reg( 'iAcertar', 'beldar', 'bieldo' )
reg( 'iAcertar', 'calentar', 'caliento' )
reg( 'iAcertar', 'cerrar', 'cierro', 'cerrarse' )
reg( 'iAcertar', 'cimentar', 'cimiento' )
reg( 'iAcertar', 'concertar', 'consierto' )
reg( 'iAcertar', 'confesar', 'confieso' )
reg( 'iAcertar', 'dentar', 'diento' )
reg( 'iAcertar', 'desacertar', 'desacierto' )
reg( 'iAcertar', 'desalentar', 'desaliento' )
reg( 'iAcertar', 'desaterrar', 'desatierro' )
reg( 'iAcertar', 'desconcertar', 'desconcierto' )
reg( 'iAcertar', 'desenterrar', 'desntierro' )
reg( 'iAcertar', 'desgobernar', 'desgobierno' )
reg( 'iAcertar', 'deshelar', 'deshielo' )
reg( 'iAcertar', 'desmembrar', 'desmiembro' )
reg( 'iAcertar', 'despertar', 'despierto' )
reg( 'iAcertar', 'desterrar', 'destierro' )
reg( 'iAcertar', 'emparentar', 'empariento' )
reg( 'iAcertar', 'empedrar', 'empiedro' )
reg( 'iAcertar', 'encerrar', 'encierro' )
reg( 'iAcertar', 'encomendar', 'encomiendo' )
reg( 'iAcertar', 'enmelar', 'enmielo' )
reg( 'iAcertar', 'enmendar', 'enmiendo' )
reg( 'iAcertar', 'ensangrentar', 'ensangriento' )
reg( 'iAcertar', 'enterrar', 'entierro' )
reg( 'iAcertar', 'entrecerrar', 'entrecierro' )
reg( 'iAcertar', 'escarmentar', 'escarmiento' )
reg( 'iAcertar', 'gobernar', 'gobierno' )
reg( 'iAcertar', 'helar', 'hielo' )
reg( 'iAcertar', 'herrar', 'hierro' )
reg( 'iAcertar', 'incensar', 'incienso' )
reg( 'iAcertar', 'invernar', 'envierno' )
reg( 'iAcertar', 'manifestar', 'manifiesto', 'manifestarse' )
reg( 'iAcertar', 'melar', 'mielo' )
reg( 'iAcertar', 'mentar', 'miento' )
reg( 'iAcertar', 'merendar', 'meriendo' )
reg( 'iAcertar', 'nevar', 'nievo' )
reg( 'iAcertar', 'pensar', 'pienso', 'pensarse', 'pensamos' )
reg( 'iAcertar', 'quebrar', 'quiebro' )
reg( 'iAcertar', 'recalentar', 'recaliento' )
reg( 'iAcertar', 'recomendar', 'recomiendo' )
reg( 'iAcertar', 'remendar', 'remiendo' )
reg( 'iAcertar', 'repensar', 'repienso' )
reg( 'iAcertar', 'requebrar', 'requiebro' )
reg( 'iAcertar', 'reventar', 'reviento' )
reg( 'iAcertar', 'salpimentar', 'salpimiento' )
reg( 'iAcertar', 'sembrar', 'siembro' )
reg( 'iAcertar', 'sentar', 'siento', 'sentarse' )
reg( 'iAcertar', 'serrar', 'sierro' )
reg( 'iAcertar', 'sobrecalentar', 'sobrecaliento', 'sobrecalentarse' )
reg( 'iAcertar', 'soterrar', 'sotierro' )
reg( 'iAcertar', 'subarrendar', 'subarriendo' )
reg( 'iAcertar', 'temblar', 'tiemblo' )
reg( 'iAcertar', 'tentar', 'tiento' )
reg( 'iActuar', 'acentuar', 'acentuó', 'acentuará', 'acentuarán', 'acentuarás', 'acentuaron' )
reg( 'iActuar', 'actuar', 'actuó', 'actúan', 'actúa', 'actúe', 'actuará', 'actuarán', 'actuarás', 'actuaría', 'actuarían', 'actuarías', 'actuaron', 'actuando' )
reg( 'iActuar', 'consensuar', 'consensuó' )
reg( 'iActuar', 'continuar', 'continúa', 'continúan', 'continuaba', 'continúe', 'continuó', 'continuará', 'continuarán', 'continuarás', 'continuaría', 'continuarían', 'continuarías', 'continuaron' )
reg( 'iActuar', 'descontinuar', 'descontinuó' )
reg( 'iActuar', 'devaluar', 'devaluó' )
reg( 'iActuar', 'efectuar', 'efectúa', 'efectúan', 'efectuarse' )
reg( 'iActuar', 'evaluar', 'evaluó', 'evalúa', 'evaluará', 'evaluarán', 'evaluarás' )
reg( 'iActuar', 'fluctuar', 'fluctuará', 'fluctuarán', 'fluctuarás', 'fluctuó' )
reg( 'iActuar', 'interactuar', 'interactúa', 'interactúan' )
reg( 'iActuar', 'situar', 'situarse', 'situado', 'situada', 'situados', 'situadas', 'sitúa', 'sitúan', 'situó', 'situará', 'situarán', 'situarás', 'situaría', 'situarían', 'situarías', 'situaron' )
reg( 'iActuar', 'tatuar', 'tatuó' )
reg( 'iAdecuar', 'adecuar' )
reg( 'iAdecuar', 'anticuar', 'anticuarse' )
reg( 'iAdecuar', 'apropincuar', 'apropincuarse' )
reg( 'iAdecuar', 'evacuar', 'evacuaron' )
reg( 'iAdecuar', 'menstruar' )
reg( 'iAdquirir', 'adquirir', 'adquiere', 'adquirimos', 'adquirido', 'adquirida', 'adquiridos', 'adquirias', 'adquirieran', 'adquirieron', 'adquirió', 'adquirirá', 'adquirirán', 'adquirirás', 'adquiría', 'adquirían', 'adquirías', 'adquiriría', 'adquirirían', 'adquirirías' )
reg( 'iAgradecer', 'abastecer' )
reg( 'iAgradecer', 'aborrecer' )
reg( 'iAgradecer', 'acaecer' )
reg( 'iAgradecer', 'acontecer' )
reg( 'iAgradecer', 'acrecer' )
reg( 'iAgradecer', 'adolecer' )
reg( 'iAgradecer', 'adormecer' )
reg( 'iAgradecer', 'agradecer' )
reg( 'iAgradecer', 'amanecer' )
reg( 'iAgradecer', 'anochecer' )
reg( 'iAgradecer', 'aparecer', 'aparecieron', 'apareciera', 'aparecieran', 'aparecieras' )
reg( 'iAgradecer', 'apetecer' )
reg( 'iAgradecer', 'atardecer' )
reg( 'iAgradecer', 'autoabastecer', 'autoabastecerse' )
reg( 'iAgradecer', 'blanquecer' )
reg( 'iAgradecer', 'carecer' )
reg( 'iAgradecer', 'compadecer' )
reg( 'iAgradecer', 'comparecer' )
reg( 'iAgradecer', 'conocer', 'conocemos', 'conocía', 'conocías', 'conocían', 'conocerse', 'conocimos' )
reg( 'iAgradecer', 'convalecer' )
reg( 'iAgradecer', 'crecer' )
reg( 'iAgradecer', 'decrecer' )
reg( 'iAgradecer', 'desabastecer' )
reg( 'iAgradecer', 'desagradecer' )
reg( 'iAgradecer', 'desaparecer', 'desapareciera', 'desparecieron' )
reg( 'iAgradecer', 'desconocer', 'desconocía', 'desconocías', 'desconocían' )
reg( 'iAgradecer', 'desentumecer' )
reg( 'iAgradecer', 'desfallecer' )
reg( 'iAgradecer', 'desfavorecer' )
reg( 'iAgradecer', 'desguarnecer' )
reg( 'iAgradecer', 'desmerecer' )
reg( 'iAgradecer', 'desobedecer' )
reg( 'iAgradecer', 'desvanecer' )
reg( 'iAgradecer', 'embastecer' )
reg( 'iAgradecer', 'embebecer' )
reg( 'iAgradecer', 'embellecer' )
reg( 'iAgradecer', 'embravecer' )
reg( 'iAgradecer', 'embrutecer' )
reg( 'iAgradecer', 'empalidecer' )
reg( 'iAgradecer', 'empequeñecer' )
reg( 'iAgradecer', 'emplastecer' )
reg( 'iAgradecer', 'empobrecer' )
reg( 'iAgradecer', 'enaltecer' )
reg( 'iAgradecer', 'enardecer' )
reg( 'iAgradecer', 'encallecer' )
reg( 'iAgradecer', 'encanecer' )
reg( 'iAgradecer', 'encarecer' )
reg( 'iAgradecer', 'enceguecer' )
reg( 'iAgradecer', 'endurecer' )
reg( 'iAgradecer', 'enflaquecer' )
reg( 'iAgradecer', 'enfurecer' )
reg( 'iAgradecer', 'engrandecer' )
reg( 'iAgradecer', 'enloquecer' )
reg( 'iAgradecer', 'enmohecer' )
reg( 'iAgradecer', 'enmudecer' )
reg( 'iAgradecer', 'ennegrecer' )
reg( 'iAgradecer', 'ennoblecer' )
reg( 'iAgradecer', 'enorgullecer' )
reg( 'iAgradecer', 'enrarecer' )
reg( 'iAgradecer', 'enriquecer' )
reg( 'iAgradecer', 'enrojecer' )
reg( 'iAgradecer', 'enronquecer' )
reg( 'iAgradecer', 'ensoberbecer' )
reg( 'iAgradecer', 'ensombrecer' )
reg( 'iAgradecer', 'ensordecer' )
reg( 'iAgradecer', 'entallecer' )
reg( 'iAgradecer', 'enternecer' )
reg( 'iAgradecer', 'entontecer' )
reg( 'iAgradecer', 'entorpecer' )
reg( 'iAgradecer', 'entristecer' )
reg( 'iAgradecer', 'entumecer' )
reg( 'iAgradecer', 'envanecer' )
reg( 'iAgradecer', 'envejecer' )
reg( 'iAgradecer', 'envilecer' )
reg( 'iAgradecer', 'escarnecer' )
reg( 'iAgradecer', 'esclarecer' )
reg( 'iAgradecer', 'establecer', 'establecerse' )
reg( 'iAgradecer', 'estremecer' )
reg( 'iAgradecer', 'fallecer' )
reg( 'iAgradecer', 'favorecer', 'favoreciera', 'favorecía' )
reg( 'iAgradecer', 'fenecer' )
reg( 'iAgradecer', 'florecer' )
reg( 'iAgradecer', 'fortalecer' )
reg( 'iAgradecer', 'fosforecer' )
reg( 'iAgradecer', 'fosforescer' )
reg( 'iAgradecer', 'guarecer' )
reg( 'iAgradecer', 'guarnecer' )
reg( 'iAgradecer', 'humedecer' )
reg( 'iAgradecer', 'languidecer' )
reg( 'iAgradecer', 'merecer' )
reg( 'iAgradecer', 'nacer', 'nacemos', 'nacimos' )
reg( 'iAgradecer', 'obedecer' )
reg( 'iAgradecer', 'obscurecer' )
reg( 'iAgradecer', 'ofrecer' )
reg( 'iAgradecer', 'oscurecer' )
reg( 'iAgradecer', 'pacer' )
reg( 'iAgradecer', 'padecer' )
reg( 'iAgradecer', 'palidecer' )
reg( 'iAgradecer', 'parecer', 'parecerse' )
reg( 'iAgradecer', 'perecer' )
reg( 'iAgradecer', 'permanecer' )
reg( 'iAgradecer', 'pertenecer' )
reg( 'iAgradecer', 'prevalecer' )
reg( 'iAgradecer', 'reaparecer' )
reg( 'iAgradecer', 'reblandecer' )
reg( 'iAgradecer', 'reconocer', 'reconocemos', 'reconocerse' )
reg( 'iAgradecer', 'recrudecer' )
reg( 'iAgradecer', 'reestablecer' )
reg( 'iAgradecer', 'rejuvenecer' )
reg( 'iAgradecer', 'renacer' )
reg( 'iAgradecer', 'resplandecer' )
reg( 'iAgradecer', 'restablecer' )
reg( 'iAgradecer', 'reverdecer' )
reg( 'iAgradecer', 'robustecer' )
reg( 'iAgradecer', 'verdecer' )
reg( 'iAislar', 'aislar', 'aisló', 'aislaron' )
reg( 'iAmar', 'abandonar' )
reg( 'iAmar', 'abjurar' )
reg( 'iAmar', 'ablandar' )
reg( 'iAmar', 'abofetear' )
reg( 'iAmar', 'abonar' )
reg( 'iAmar', 'abordar' )
reg( 'iAmar', 'abortar' )
reg( 'iAmar', 'abotonar' )
reg( 'iAmar', 'abrevar' )
reg( 'iAmar', 'abultar' )
reg( 'iAmar', 'abundar' )
reg( 'iAmar', 'abusar' )
reg( 'iAmar', 'acabar' )
reg( 'iAmar', 'acampar' )
reg( 'iAmar', 'acaparar' )
reg( 'iAmar', 'acarrear' )
reg( 'iAmar', 'acatar' )
reg( 'iAmar', 'acaudillar' )
reg( 'iAmar', 'accidentar' )
reg( 'iAmar', 'acechar' )
reg( 'iAmar', 'acelerar' )
reg( 'iAmar', 'aceptar', 'aceptarla' )
reg( 'iAmar', 'aclamar' )
reg( 'iAmar', 'aclarar', 'aclarás' )
reg( 'iAmar', 'aclimatar' )
reg( 'iAmar', 'acomodar' )
reg( 'iAmar', 'acompañar' )
reg( 'iAmar', 'acondicionar' )
reg( 'iAmar', 'acongojar' )
reg( 'iAmar', 'aconsejar' )
reg( 'iAmar', 'acoplar' )
reg( 'iAmar', 'acorralar' )
reg( 'iAmar', 'acortar' )
reg( 'iAmar', 'acosar' )
reg( 'iAmar', 'acostumbrar' )
reg( 'iAmar', 'acotar' )
reg( 'iAmar', 'acreditar' )
reg( 'iAmar', 'activar' )
reg( 'iAmar', 'aculturar' )
reg( 'iAmar', 'acumular', 'acumularse' )
reg( 'iAmar', 'acunar' )
reg( 'iAmar', 'acusar' )
reg( 'iAmar', 'acuñar', 'acuñó' )
reg( 'iAmar', 'adaptar', 'adaptarla', 'adaptarse' )
reg( 'iAmar', 'adelantar' )
reg( 'iAmar', 'adentrar', 'adentrarse' )
reg( 'iAmar', 'adicionar' )
reg( 'iAmar', 'adiestrar' )
reg( 'iAmar', 'adivinar' )
reg( 'iAmar', 'adjuntar' )
reg( 'iAmar', 'administrar', 'administrarlos' )
reg( 'iAmar', 'admirar' )
reg( 'iAmar', 'adoptar' )
reg( 'iAmar', 'adorar' )
reg( 'iAmar', 'adornar', 'adornarse' )
reg( 'iAmar', 'adosar' )
reg( 'iAmar', 'adueñar', 'adueñarse' )
reg( 'iAmar', 'afectar', 'afectarán' )
reg( 'iAmar', 'aferrar' )
reg( 'iAmar', 'aficionar' )
reg( 'iAmar', 'afiebrar', 'afiebrarse' )
reg( 'iAmar', 'afiliar' )
reg( 'iAmar', 'afirmar', 'afirmarse' )
reg( 'iAmar', 'aflojar' )
reg( 'iAmar', 'aflorar' )
reg( 'iAmar', 'afrontar' )
reg( 'iAmar', 'agarrar', 'agarrás' )
reg( 'iAmar', 'agasajar' )
reg( 'iAmar', 'agitar' )
reg( 'iAmar', 'aglutinar' )
reg( 'iAmar', 'agotar' )
reg( 'iAmar', 'agradar' )
reg( 'iAmar', 'agrandar' )
reg( 'iAmar', 'agravar' )
reg( 'iAmar', 'agriar' )
reg( 'iAmar', 'agrupar', 'agruparse' )
reg( 'iAmar', 'aguantar' )
reg( 'iAmar', 'agusanar', 'agusanarse' )
reg( 'iAmar', 'ahondar' )
reg( 'iAmar', 'ahorrar', 'ahorrás' )
reg( 'iAmar', 'ahuesar', 'ahuesarse' )
reg( 'iAmar', 'ahuyentar' )
reg( 'iAmar', 'ajustar', 'ajustarla', 'ajustarse' )
reg( 'iAmar', 'alabar' )
reg( 'iAmar', 'alardear')
reg( 'iAmar', 'alarmar' )
reg( 'iAmar', 'alborotar' )
reg( 'iAmar', 'alegrar' )
reg( 'iAmar', 'alejar', 'alejarse' )
reg( 'iAmar', 'alertar' )
reg( 'iAmar', 'aligerar' )
reg( 'iAmar', 'alimentar', 'alimentarse' )
reg( 'iAmar', 'alinear', 'alinearlos' )
reg( 'iAmar', 'alistar', 'alistarse' )
reg( 'iAmar', 'allanar' )
reg( 'iAmar', 'almacenar', 'almacenarlos' )
reg( 'iAmar', 'alojar' )
reg( 'iAmar', 'alquilar' )
reg( 'iAmar', 'alterar' )
reg( 'iAmar', 'alternar' )
reg( 'iAmar', 'alumbrar' )
reg( 'iAmar', 'amaestrar' )
reg( 'iAmar', 'amamantar' )
reg( 'iAmar', 'amar' )
reg( 'iAmar', 'amarrar' )
reg( 'iAmar', 'amasar' )
reg( 'iAmar', 'amañar' )
reg( 'iAmar', 'ambicionar' )
reg( 'iAmar', 'ambientar' )
reg( 'iAmar', 'amedrentar' )
reg( 'iAmar', 'ameritar' )
reg( 'iAmar', 'amodorrar' )
reg( 'iAmar', 'amoldar' )
reg( 'iAmar', 'amonestar' )
reg( 'iAmar', 'amontonar' )
reg( 'iAmar', 'amotinar' )
reg( 'iAmar', 'amparar' )
reg( 'iAmar', 'amputar' )
reg( 'iAmar', 'amueblar' )
reg( 'iAmar', 'anclar' )
reg( 'iAmar', 'anexar' )
reg( 'iAmar', 'anexionar' )
reg( 'iAmar', 'anhelar' )
reg( 'iAmar', 'anidar', 'anidarse' )
reg( 'iAmar', 'anillar' )
reg( 'iAmar', 'animar' )
reg( 'iAmar', 'aniquilar' )
reg( 'iAmar', 'anonadar' )
reg( 'iAmar', 'anotar' )
reg( 'iAmar', 'anticipar', 'anticiparse' )
reg( 'iAmar', 'antojar', 'antojarse' )
reg( 'iAmar', 'anular' )
reg( 'iAmar', 'apadrinar' )
reg( 'iAmar', 'aparear', 'aparearse' )
reg( 'iAmar', 'apartar', 'apartarse' )
reg( 'iAmar', 'apasionar' )
reg( 'iAmar', 'apelar' )
reg( 'iAmar', 'apellidar' )
reg( 'iAmar', 'apiadar' )
reg( 'iAmar', 'apiñar' )
reg( 'iAmar', 'aplanar' )
reg( 'iAmar', 'aplastar' )
reg( 'iAmar', 'apodar' )
reg( 'iAmar', 'apoderar', 'apoderarse' )
reg( 'iAmar', 'aportar' )
reg( 'iAmar', 'apostatar' )
reg( 'iAmar', 'apoyar', 'apoyarse' )
reg( 'iAmar', 'apresar' )
reg( 'iAmar', 'aprestar' )
reg( 'iAmar', 'apresurar' )
reg( 'iAmar', 'aprisionar' )
reg( 'iAmar', 'aprovechar', 'aprovecharse' )
reg( 'iAmar', 'aproximar', 'aproximarse' )
reg( 'iAmar', 'apuntar' )
reg( 'iAmar', 'apuñalar' )
reg( 'iAmar', 'arar' )
reg( 'iAmar', 'arañar' )
reg( 'iAmar', 'arbitrar' )
reg( 'iAmar', 'archivar' )
reg( 'iAmar', 'argumentar' )
reg( 'iAmar', 'armar' )
reg( 'iAmar', 'arquear' )
reg( 'iAmar', 'arrasar' )
reg( 'iAmar', 'arrastrar', 'arrastrarla', 'arrástrelo' )
reg( 'iAmar', 'arrear' )
reg( 'iAmar', 'arrebatar' )
reg( 'iAmar', 'arreglar' )
reg( 'iAmar', 'arrejuntar', 'arrejuntarse' )
reg( 'iAmar', 'arrellanar', 'arrellanarse' )
reg( 'iAmar', 'arrestar' )
reg( 'iAmar', 'arribar' )
reg( 'iAmar', 'arrinconar' )
reg( 'iAmar', 'arrodillar' )
reg( 'iAmar', 'arrojar' )
reg( 'iAmar', 'arrollar' )
reg( 'iAmar', 'arruinar' )
reg( 'iAmar', 'articular' )
reg( 'iAmar', 'asaltar' )
reg( 'iAmar', 'asar' )
reg( 'iAmar', 'asear' )
reg( 'iAmar', 'asegurar', 'asegurarse', 'asegúrese' )
reg( 'iAmar', 'asemejar', 'asemejen' )
reg( 'iAmar', 'asesinar' )
reg( 'iAmar', 'asesorar' )
reg( 'iAmar', 'asestar' )
reg( 'iAmar', 'aseverar' )
reg( 'iAmar', 'asignar', 'asignarle' )
reg( 'iAmar', 'asimilar' )
reg( 'iAmar', 'asomar' )
reg( 'iAmar', 'asombrar' )
reg( 'iAmar', 'aspirar' )
reg( 'iAmar', 'asustar')
reg( 'iAmar', 'atajar' )
reg( 'iAmar', 'atar' )
reg( 'iAmar', 'atentar')
reg( 'iAmar', 'atestar' )
reg( 'iAmar', 'atinar' )
reg( 'iAmar', 'atormentar' )
reg( 'iAmar', 'atragantar', 'atragantarse' )
reg( 'iAmar', 'atrapar' )
reg( 'iAmar', 'atrasar' )
reg( 'iAmar', 'atrincherar' )
reg( 'iAmar', 'atropellar' )
reg( 'iAmar', 'audicionar' )
reg( 'iAmar', 'auditar', 'auditada' )
reg( 'iAmar', 'augurar' )
reg( 'iAmar', 'aumentar' )
reg( 'iAmar', 'ausentar', 'ausentarse' )
reg( 'iAmar', 'autodenominar' )
reg( 'iAmar', 'autonombrar' )
reg( 'iAmar', 'autoproclamar' )
reg( 'iAmar', 'auxiliar' )
reg( 'iAmar', 'avalar' )
reg( 'iAmar', 'aventajar' )
reg( 'iAmar', 'aventurar' )
reg( 'iAmar', 'avisar' )
reg( 'iAmar', 'avistar' )
reg( 'iAmar', 'avivar' )
reg( 'iAmar', 'ayudar', 'ayudarles', 'ayudarle', 'ayudarán' )
reg( 'iAmar', 'azotar' )
reg( 'iAmar', 'babear' )
reg( 'iAmar', 'bailar' )
reg( 'iAmar', 'bajar' )
reg( 'iAmar', 'balancear' )
reg( 'iAmar', 'balbucear' )
reg( 'iAmar', 'barajar' )
reg( 'iAmar', 'basar', 'basarse', 'basándose' )
reg( 'iAmar', 'bastar' )
reg( 'iAmar', 'batallar' )
reg( 'iAmar', 'batear' )
reg( 'iAmar', 'bañar', 'bañarse' )
reg( 'iAmar', 'besar' )
reg( 'iAmar', 'blanquear' )
reg( 'iAmar', 'blasfemar' )
reg( 'iAmar', 'bloquear', 'bloquearse' )
reg( 'iAmar', 'boicotear' )
reg( 'iAmar', 'bombardear' )
reg( 'iAmar', 'bordear' )
reg( 'iAmar', 'borrar', 'borrarlo', 'borrarla' )
reg( 'iAmar', 'bosquejar', 'bosquejando' )
reg( 'iAmar', 'botar' )
reg( 'iAmar', 'brear' )
reg( 'iAmar', 'brillar' )
reg( 'iAmar', 'brindar')
reg( 'iAmar', 'bromear' )
reg( 'iAmar', 'broncear' )
reg( 'iAmar', 'brotar' )
reg( 'iAmar', 'bucear' )
reg( 'iAmar', 'burlar', 'burlarse' )
reg( 'iAmar', 'cabecear' )
reg( 'iAmar', 'cablear', 'cablearlos' )
reg( 'iAmar', 'calar' )
reg( 'iAmar', 'calcular', 'calcularla', 'calcularse' )
reg( 'iAmar', 'callar' )
reg( 'iAmar', 'calmar' )
reg( 'iAmar', 'caminar' )
reg( 'iAmar', 'camuflar' )
reg( 'iAmar', 'cancelar' )
reg( 'iAmar', 'canjear' )
reg( 'iAmar', 'cansar' )
reg( 'iAmar', 'cantar' )
reg( 'iAmar', 'capacitar' )
reg( 'iAmar', 'capar' )
reg( 'iAmar', 'capitanear' )
reg( 'iAmar', 'capitular' )
reg( 'iAmar', 'captar' )
reg( 'iAmar', 'capturar' )
reg( 'iAmar', 'casar', 'casarse' )
reg( 'iAmar', 'castrar' )
reg( 'iAmar', 'catapultar' )
reg( 'iAmar', 'causar')
reg( 'iAmar', 'cautivar' )
reg( 'iAmar', 'cavar' )
reg( 'iAmar', 'cebar' )
reg( 'iAmar', 'cejar' )
reg( 'iAmar', 'celebrar', 'celebrarse' )
reg( 'iAmar', 'cenar' )
reg( 'iAmar', 'censar' )
reg( 'iAmar', 'censurar' )
reg( 'iAmar', 'centrar', 'centraremos', 'centrarse' )
reg( 'iAmar', 'cercenar' )
reg( 'iAmar', 'cesar' )
reg( 'iAmar', 'chatear' )
reg( 'iAmar', 'chequear' )
reg( 'iAmar', 'chivar', 'chivarse' )
reg( 'iAmar', 'chorrear' )
reg( 'iAmar', 'cifrar')
reg( 'iAmar', 'cimentar' )
reg( 'iAmar', 'circular' )
reg( 'iAmar', 'citar', 'citando', 'citarse' )
reg( 'iAmar', 'clamar' )
reg( 'iAmar', 'clausurar' )
reg( 'iAmar', 'clavar' )
reg( 'iAmar', 'coadyuvar' )
reg( 'iAmar', 'cobijar' )
reg( 'iAmar', 'cobrar' )
reg( 'iAmar', 'cocinar' )
reg( 'iAmar', 'cofundar' )
reg( 'iAmar', 'colaborar', 'colaboran' )
reg( 'iAmar', 'colapsar' )
reg( 'iAmar', 'coleccionar' )
reg( 'iAmar', 'colectar' )
reg( 'iAmar', 'colisionar' )
reg( 'iAmar', 'colmar' )
reg( 'iAmar', 'colorear' )
reg( 'iAmar', 'comandar' )
reg( 'iAmar', 'combinar', 'combinarse' )
reg( 'iAmar', 'comentar' )
reg( 'iAmar', 'comisionar' )
reg( 'iAmar', 'compaginar' )
reg( 'iAmar', 'comparar', 'comparándola', 'compararse' )
reg( 'iAmar', 'compenetrar', 'compenetrarse' )
reg( 'iAmar', 'compensar' )
reg( 'iAmar', 'compilar' )
reg( 'iAmar', 'complementar', 'complementaria' )
reg( 'iAmar', 'completar', 'completarán', 'completarse' )
reg( 'iAmar', 'comportar', 'comportarse' )
reg( 'iAmar', 'comprar' )
reg( 'iAmar', 'comprobar', 'comprobarse' )
reg( 'iAmar', 'computar' )
reg( 'iAmar', 'concentrar', 'concentraremos', 'concentrarse' )
reg( 'iAmar', 'concitar' )
reg( 'iAmar', 'concretar', 'concretarse' )
reg( 'iAmar', 'concursar' )
reg( 'iAmar', 'condecorar' )
reg( 'iAmar', 'condenar' )
reg( 'iAmar', 'condicionar', 'condicionarán' )
reg( 'iAmar', 'condonar' )
reg( 'iAmar', 'conectar', 'conéctese', 'conectarse' )
reg( 'iAmar', 'confeccionar' )
reg( 'iAmar', 'configurar', 'configurarse', 'configurarlo' )
reg( 'iAmar', 'confinar' )
reg( 'iAmar', 'confirmar' )
reg( 'iAmar', 'conformar', 'conformarse' )
reg( 'iAmar', 'confrontar' )
reg( 'iAmar', 'congelar' )
reg( 'iAmar', 'conjeturar' )
reg( 'iAmar', 'conjurar' )
reg( 'iAmar', 'conllevar' )
reg( 'iAmar', 'conmemorar' )
reg( 'iAmar', 'conminar' )
reg( 'iAmar', 'conmocionar' )
reg( 'iAmar', 'conmutar' )
reg( 'iAmar', 'conquistar' )
reg( 'iAmar', 'consagrar', 'consagrarse' )
reg( 'iAmar', 'conservar' )
reg( 'iAmar', 'considerar', 'consideremos', 'considerarse' )
reg( 'iAmar', 'consignar' )
reg( 'iAmar', 'consolidar', 'consolidarse' )
reg( 'iAmar', 'conspirar' )
reg( 'iAmar', 'constar' )
reg( 'iAmar', 'constatar' )
reg( 'iAmar', 'constipar', 'constiparse' )
reg( 'iAmar', 'consultar', 'consultarse' )
reg( 'iAmar', 'consumar' )
reg( 'iAmar', 'contactar' )
reg( 'iAmar', 'contaminar' )
reg( 'iAmar', 'contemplar', 'contemplarse' )
reg( 'iAmar', 'contentar' )
reg( 'iAmar', 'contestar' )
reg( 'iAmar', 'contrarrestar', 'contrarrestó' )
reg( 'iAmar', 'contrastar' )
reg( 'iAmar', 'contratar' )
reg( 'iAmar', 'controlar' )
reg( 'iAmar', 'convalidar' )
reg( 'iAmar', 'conversar' )
reg( 'iAmar', 'cooperar' )
reg( 'iAmar', 'coordinar', 'coordinarse' )
reg( 'iAmar', 'copar' )
reg( 'iAmar', 'coquetear' )
reg( 'iAmar', 'coronar', 'coronarse' )
reg( 'iAmar', 'corretear' )
reg( 'iAmar', 'corroborar', 'corroboradas' )
reg( 'iAmar', 'cortar' )
reg( 'iAmar', 'cortejar' )
reg( 'iAmar', 'cosechar' )
reg( 'iAmar', 'costear' )
reg( 'iAmar', 'cotejar' )
reg( 'iAmar', 'crear', 'crearemos', 'crearlo', 'crearse', 'crearlos', 'creamos' )
reg( 'iAmar', 'cronometrar' )
reg( 'iAmar', 'cuajar' )
reg( 'iAmar', 'cuchichear' )
reg( 'iAmar', 'cuestionar' )
reg( 'iAmar', 'cuidar' )
reg( 'iAmar', 'culminar' )
reg( 'iAmar', 'culpar', 'culparse' )
reg( 'iAmar', 'cultivar' )
reg( 'iAmar', 'curar' )
reg( 'iAmar', 'currar' )
reg( 'iAmar', 'cursar' )
reg( 'iAmar', 'datar' )
reg( 'iAmar', 'dañar' )
reg( 'iAmar', 'deambular' )
reg( 'iAmar', 'debilitar' )
reg( 'iAmar', 'debitar' )
reg( 'iAmar', 'debutar' )
reg( 'iAmar', 'decantar' )
reg( 'iAmar', 'decapitar' )
reg( 'iAmar', 'decepcionar' )
reg( 'iAmar', 'declamar' )
reg( 'iAmar', 'declarar', 'declaramos', 'declararse' )
reg( 'iAmar', 'declinar' )
reg( 'iAmar', 'decorar' )
reg( 'iAmar', 'decretar' )
reg( 'iAmar', 'deformar' )
reg( 'iAmar', 'defraudar' )
reg( 'iAmar', 'degenerar' )
reg( 'iAmar', 'degradar' )
reg( 'iAmar', 'degustar' )
reg( 'iAmar', 'dejar', 'dejarlos', 'dejarse' )
reg( 'iAmar', 'delatar' )
reg( 'iAmar', 'deleitar' )
reg( 'iAmar', 'delimitar' )
reg( 'iAmar', 'delinear' )
reg( 'iAmar', 'demandar' )
reg( 'iAmar', 'demorar' )
reg( 'iAmar', 'denominar', 'denominarse' )
reg( 'iAmar', 'denotar' )
reg( 'iAmar', 'deparar' )
reg( 'iAmar', 'deportar' )
reg( 'iAmar', 'depositar' )
reg( 'iAmar', 'derivar', 'deriva' )
reg( 'iAmar', 'derramar' )
reg( 'iAmar', 'derribar' )
reg( 'iAmar', 'derrotar' )
reg( 'iAmar', 'derrumbar' )
reg( 'iAmar', 'desacelerar' )
reg( 'iAmar', 'desaconsejar' )
reg( 'iAmar', 'desacoplar' )
reg( 'iAmar', 'desacreditar' )
reg( 'iAmar', 'desactivar', 'desactive' )
reg( 'iAmar', 'desagradar' )
reg( 'iAmar', 'desagrupar', 'desagruparlos' )
reg( 'iAmar', 'desalojar' )
reg( 'iAmar', 'desanimar' )
reg( 'iAmar', 'desaprovechar' )
reg( 'iAmar', 'desarmar' )
reg( 'iAmar', 'desarrollar', 'desarrollamos', 'desarrollarse' )
reg( 'iAmar', 'desarticular' )
reg( 'iAmar', 'desatar' )
reg( 'iAmar', 'desatornillar' )
reg( 'iAmar', 'desayunar' )
reg( 'iAmar', 'desbaratar' )
reg( 'iAmar', 'desbastar' )
reg( 'iAmar', 'desbloquear' )
reg( 'iAmar', 'desbordar' )
reg( 'iAmar', 'descansar' )
reg( 'iAmar', 'descarar', 'descararse' )
reg( 'iAmar', 'descarrilar' )
reg( 'iAmar', 'descartar' )
reg( 'iAmar', 'descentrar' )
reg( 'iAmar', 'descifrar')
reg( 'iAmar', 'descojonar', 'descojonarse' )
reg( 'iAmar', 'desconectar' )
reg( 'iAmar', 'descontrolar', 'descontrolarse' )
reg( 'iAmar', 'descuidar' )
reg( 'iAmar', 'desdasar', 'desdasarse' )
reg( 'iAmar', 'desdeñar' )
reg( 'iAmar', 'desdoblar' )
reg( 'iAmar', 'desear' )
reg( 'iAmar', 'desechar' )
reg( 'iAmar', 'desempeñar', 'desempeñarse' )
reg( 'iAmar', 'desencadenar' )
reg( 'iAmar', 'desenredar' )
reg( 'iAmar', 'desenvainar' )
reg( 'iAmar', 'desertar' )
reg( 'iAmar', 'desestimar' )
reg( 'iAmar', 'desfilar' )
reg( 'iAmar', 'desgajar' )
reg( 'iAmar', 'desgarrar' )
reg( 'iAmar', 'deshidratar' )
reg( 'iAmar', 'designar' )
reg( 'iAmar', 'desilusionar' )
reg( 'iAmar', 'desintegrar' )
reg( 'iAmar', 'desinteresar', 'desinteresarse' )
reg( 'iAmar', 'deslindar' )
reg( 'iAmar', 'deslumbrar' )
reg( 'iAmar', 'desmantelar' )
reg( 'iAmar', 'desmayar' )
reg( 'iAmar', 'desmontar' )
reg( 'iAmar', 'desmoronar' )
reg( 'iAmar', 'desnudar' )
reg( 'iAmar', 'despachar' )
reg( 'iAmar', 'desparasitar' )
reg( 'iAmar', 'despejar' )
reg( 'iAmar', 'despenar' )
reg( 'iAmar', 'despendolar', 'despendolarse' )
reg( 'iAmar', 'desplomar' )
reg( 'iAmar', 'despojar' )
reg( 'iAmar', 'desposar' )
reg( 'iAmar', 'despreocupar', 'despreocuparse' )
reg( 'iAmar', 'despuntar' )
reg( 'iAmar', 'destapar' )
reg( 'iAmar', 'destinar' )
reg( 'iAmar', 'destronar' )
reg( 'iAmar', 'desvelar' )
reg( 'iAmar', 'desvelar', 'desveló' )
reg( 'iAmar', 'desvincular' )
reg( 'iAmar', 'detallar' )
reg( 'iAmar', 'detectar' )
reg( 'iAmar', 'deteriorar' )
reg( 'iAmar', 'determinar', 'determinarse' )
reg( 'iAmar', 'detonar' )
reg( 'iAmar', 'devastar' )
reg( 'iAmar', 'devorar' )
reg( 'iAmar', 'diagramar' )
reg( 'iAmar', 'dibujar' )
reg( 'iAmar', 'dictaminar' )
reg( 'iAmar', 'dictar' )
reg( 'iAmar', 'diezmar' )
reg( 'iAmar', 'dificultar' )
reg( 'iAmar', 'dignar', 'dignarse' )
reg( 'iAmar', 'dilatar' )
reg( 'iAmar', 'diplomar' )
reg( 'iAmar', 'discrepar' )
reg( 'iAmar', 'discriminar' )
reg( 'iAmar', 'disculpar' )
reg( 'iAmar', 'diseminar' )
reg( 'iAmar', 'disertar' )
reg( 'iAmar', 'diseñar', 'diseñarlo' )
reg( 'iAmar', 'disfrutar' )
reg( 'iAmar', 'disgustar' )
reg( 'iAmar', 'disipar' )
reg( 'iAmar', 'disparar' )
reg( 'iAmar', 'dispensar' )
reg( 'iAmar', 'dispersar' )
reg( 'iAmar', 'disputar', 'disputarse' )
reg( 'iAmar', 'distorsionar', 'distorsionarla' )
reg( 'iAmar', 'divisar' )
reg( 'iAmar', 'doblar' )
reg( 'iAmar', 'doctorar' )
reg( 'iAmar', 'documentar' )
reg( 'iAmar', 'dominar' )
reg( 'iAmar', 'donar' )
reg( 'iAmar', 'dotar' )
reg( 'iAmar', 'drenar' )
reg( 'iAmar', 'dudar' )
reg( 'iAmar', 'durar' )
reg( 'iAmar', 'echar' )
reg( 'iAmar', 'eclipsar' )
reg( 'iAmar', 'editar', 'editarlos', 'editarse' )
reg( 'iAmar', 'efectuar' )
reg( 'iAmar', 'egresar' )
reg( 'iAmar', 'ejecutar', 'ejecutarse' )
reg( 'iAmar', 'ejercitar' )
reg( 'iAmar', 'elaborar')
reg( 'iAmar', 'elevar', 'elevarse' )
reg( 'iAmar', 'eliminar', 'eliminarlo' )
reg( 'iAmar', 'elucidar' )
reg( 'iAmar', 'emanar' )
reg( 'iAmar', 'emancipar' )
reg( 'iAmar', 'embalsamar' )
reg( 'iAmar', 'embelesar' )
reg( 'iAmar', 'embolsar' )
reg( 'iAmar', 'emborrachar' )
reg( 'iAmar', 'emigrar' )
reg( 'iAmar', 'emocionar' )
reg( 'iAmar', 'empanar' )
reg( 'iAmar', 'empapar' )
reg( 'iAmar', 'emparejar' )
reg( 'iAmar', 'empatar' )
reg( 'iAmar', 'empecinar', 'empecinarse' )
reg( 'iAmar', 'empeorar' )
reg( 'iAmar', 'empeñar' )
reg( 'iAmar', 'emplear', 'emplearse' )
reg( 'iAmar', 'empujar' )
reg( 'iAmar', 'empuñar' )
reg( 'iAmar', 'emular' )
reg( 'iAmar', 'enajenar' )
reg( 'iAmar', 'enamorar', 'enamorarse' )
reg( 'iAmar', 'enarbolar' )
reg( 'iAmar', 'encadenar' )
reg( 'iAmar', 'encajar', 'encajarlos' )
reg( 'iAmar', 'encallar' )
reg( 'iAmar', 'encaminar' )
reg( 'iAmar', 'encanar', 'encanarse' )
reg( 'iAmar', 'encantar' )
reg( 'iAmar', 'encarar' )
reg( 'iAmar', 'encarcelar' )
reg( 'iAmar', 'encariñar', 'encariñarse' )
reg( 'iAmar', 'encarnar' )
reg( 'iAmar', 'encorvar' )
reg( 'iAmar', 'encuadrar' )
reg( 'iAmar', 'encumbrar' )
reg( 'iAmar', 'endeudar', 'endeudarse' )
reg( 'iAmar', 'endosar' )
reg( 'iAmar', 'enemistar' )
reg( 'iAmar', 'enfadar' )
reg( 'iAmar', 'enfermar' )
reg( 'iAmar', 'enfilar' )
reg( 'iAmar', 'enfrentar', 'enfrentarse' )
reg( 'iAmar', 'enganchar' )
reg( 'iAmar', 'engañar', 'engañen' )
reg( 'iAmar', 'engendrar' )
reg( 'iAmar', 'englobar' )
reg( 'iAmar', 'engripar', 'engriparse' )
reg( 'iAmar', 'enlistar' )
reg( 'iAmar', 'enojar' )
reg( 'iAmar', 'enredar' )
reg( 'iAmar', 'enrolar' )
reg( 'iAmar', 'ensamblar', 'ensamblado' )
reg( 'iAmar', 'ensanchar' )
reg( 'iAmar', 'ensayar' )
reg( 'iAmar', 'enseñar', 'enseña' )
reg( 'iAmar', 'ensimismar', 'ensimismarse' )
reg( 'iAmar', 'entablar' )
reg( 'iAmar', 'enterar', 'enterarse' )
reg( 'iAmar', 'entonar' )
reg( 'iAmar', 'entrar' )
reg( 'iAmar', 'entrañar')
reg( 'iAmar', 'entrenar', 'entrenarse' )
reg( 'iAmar', 'entrevistar', 'entrevistarse' )
reg( 'iAmar', 'entusiasmar' )
reg( 'iAmar', 'enumerar', 'enumeran', 'enumera' )
reg( 'iAmar', 'envenenar' )
reg( 'iAmar', 'enviudar' )
reg( 'iAmar', 'equilibrar' )
reg( 'iAmar', 'equipar' )
reg( 'iAmar', 'equiparar' )
reg( 'iAmar', 'erosionar' )
reg( 'iAmar', 'eructar' )
reg( 'iAmar', 'escalar' )
reg( 'iAmar', 'escampar' )
reg( 'iAmar', 'escanear', 'escanearse', 'escanee' )
reg( 'iAmar', 'escapar', 'escaparse' )
reg( 'iAmar', 'escaquear', 'escaquearse' )
reg( 'iAmar', 'escatimar' )
reg( 'iAmar', 'escoltar' )
reg( 'iAmar', 'escuchar', 'escucharse' )
reg( 'iAmar', 'escudriñar' )
reg( 'iAmar', 'esfumar' )
reg( 'iAmar', 'esmerar', 'esmerarse' )
reg( 'iAmar', 'espantar' )
reg( 'iAmar', 'especular' )
reg( 'iAmar', 'esperar', 'esperarse' )
reg( 'iAmar', 'espetar' )
reg( 'iAmar', 'espolear' )
reg( 'iAmar', 'esputar' )
reg( 'iAmar', 'esquivar' )
reg( 'iAmar', 'estacionar' )
reg( 'iAmar', 'estafar' )
reg( 'iAmar', 'estallar' )
reg( 'iAmar', 'estampar' )
reg( 'iAmar', 'estereotipar' )
reg( 'iAmar', 'estimar' )
reg( 'iAmar', 'estimular' )
reg( 'iAmar', 'estipular' )
reg( 'iAmar', 'estirar', 'estirarse', 'estirarla', 'estirarlo', 'estirándolo' )
reg( 'iAmar', 'estoquear' )
reg( 'iAmar', 'estorbar' )
reg( 'iAmar', 'estrangular' )
reg( 'iAmar', 'estrechar' )
reg( 'iAmar', 'estrellar', 'estrellarse' )
reg( 'iAmar', 'estrenar', 'estrenarse' )
reg( 'iAmar', 'estresar' )
reg( 'iAmar', 'estropear' )
reg( 'iAmar', 'estructurar' )
reg( 'iAmar', 'estrujar' )
reg( 'iAmar', 'etiquetar' )
reg( 'iAmar', 'evaporar' )
reg( 'iAmar', 'evitar', 'evitarla', 'evitarse' )
reg( 'iAmar', 'evolucionar' )
reg( 'iAmar', 'exacerbar' )
reg( 'iAmar', 'exagerar' )
reg( 'iAmar', 'exaltar' )
reg( 'iAmar', 'examinar' )
reg( 'iAmar', 'excavar' )
reg( 'iAmar', 'excitar' )
reg( 'iAmar', 'exclamar' )
reg( 'iAmar', 'excusar' )
reg( 'iAmar', 'exhortar' )
reg( 'iAmar', 'exhumar' )
reg( 'iAmar', 'exonerar' )
reg( 'iAmar', 'experimentar' )
reg( 'iAmar', 'expirar' )
reg( 'iAmar', 'explorar' )
reg( 'iAmar', 'explotar' )
reg( 'iAmar', 'exportar', 'exportarla' )
reg( 'iAmar', 'expresar', 'expresarse' )
reg( 'iAmar', 'expulsar' )
reg( 'iAmar', 'exterminar' )
reg( 'iAmar', 'extrañar' )
reg( 'iAmar', 'eyectar' )
reg( 'iAmar', 'facilitar', 'facilitarle' )
reg( 'iAmar', 'facturar' )
reg( 'iAmar', 'facultar' )
reg( 'iAmar', 'fajar' )
reg( 'iAmar', 'fallar' )
reg( 'iAmar', 'faltar' )
reg( 'iAmar', 'fantasear' )
reg( 'iAmar', 'fascinar' )
reg( 'iAmar', 'fechar' )
reg( 'iAmar', 'felicitar' )
reg( 'iAmar', 'festejar' )
reg( 'iAmar', 'festonear' )
reg( 'iAmar', 'fichar' )
reg( 'iAmar', 'figurar' )
reg( 'iAmar', 'fijar', 'fijarse' )
reg( 'iAmar', 'filmar' )
reg( 'iAmar', 'filosofar' )
reg( 'iAmar', 'filtrar' )
reg( 'iAmar', 'firmar' )
reg( 'iAmar', 'flamear' )
reg( 'iAmar', 'fletar' )
reg( 'iAmar', 'flotar' )
reg( 'iAmar', 'fomentar' )
reg( 'iAmar', 'fondear' )
reg( 'iAmar', 'forcejear' )
reg( 'iAmar', 'forjar' )
reg( 'iAmar', 'formar', 'formarse' )
reg( 'iAmar', 'formatear' )
reg( 'iAmar', 'formular' )
reg( 'iAmar', 'forrar' )
reg( 'iAmar', 'fracasar' )
reg( 'iAmar', 'fraccionar' )
reg( 'iAmar', 'fracturar' )
reg( 'iAmar', 'fragmentar' )
reg( 'iAmar', 'frecuentar' )
reg( 'iAmar', 'frenar' )
reg( 'iAmar', 'frisar' )
reg( 'iAmar', 'frustrar' )
reg( 'iAmar', 'fulminar' )
reg( 'iAmar', 'funcionar' )
reg( 'iAmar', 'fundamentar' )
reg( 'iAmar', 'fundar', 'fundarse')
reg( 'iAmar', 'fusilar' )
reg( 'iAmar', 'fusionar', 'fusionarse' )
reg( 'iAmar', 'galardonar' )
reg( 'iAmar', 'ganar', 'ganarse' )
reg( 'iAmar', 'gangrenar', 'gangrenarse' )
reg( 'iAmar', 'gastar' )
reg( 'iAmar', 'generar' )
reg( 'iAmar', 'germinar' )
reg( 'iAmar', 'gestar' )
reg( 'iAmar', 'gestionar' )
reg( 'iAmar', 'girar', 'girarlo', 'girándolo', 'girarla' )
reg( 'iAmar', 'gloriar' )
reg( 'iAmar', 'glosar' )
reg( 'iAmar', 'golear' )
reg( 'iAmar', 'golpear' )
reg( 'iAmar', 'grabar' )
reg( 'iAmar', 'graduar', 'graduarse' )
reg( 'iAmar', 'granjear' )
reg( 'iAmar', 'gritar' )
reg( 'iAmar', 'guardar', 'guardarlo', 'guardarán' )
reg( 'iAmar', 'guerrear' )
reg( 'iAmar', 'guillar', 'guillarse' )
reg( 'iAmar', 'guisar' )
reg( 'iAmar', 'guiñar' )
reg( 'iAmar', 'gustar' )
reg( 'iAmar', 'habilitar' )
reg( 'iAmar', 'habitar' )
reg( 'iAmar', 'hablar', 'hablarse' )
reg( 'iAmar', 'hallar', 'hallarse' )
reg( 'iAmar', 'hartar' )
reg( 'iAmar', 'heredar', 'heredarse' )
reg( 'iAmar', 'hermanar' )
reg( 'iAmar', 'hibernar' )
reg( 'iAmar', 'hipar' )
reg( 'iAmar', 'homenajear' )
reg( 'iAmar', 'honrar' )
reg( 'iAmar', 'hospedar' )
reg( 'iAmar', 'huevear' )
reg( 'iAmar', 'humillar' )
reg( 'iAmar', 'husmear' )
reg( 'iAmar', 'idear' )
reg( 'iAmar', 'ignorar' )
reg( 'iAmar', 'igualar' )
reg( 'iAmar', 'iluminar' )
reg( 'iAmar', 'ilustrar' )
reg( 'iAmar', 'imaginar' )
reg( 'iAmar', 'imitar' )
reg( 'iAmar', 'impactar', 'impacten')
reg( 'iAmar', 'imperar' )
reg( 'iAmar', 'impetrar' )
reg( 'iAmar', 'implantar' )
reg( 'iAmar', 'implementar', 'implementarla', 'implementarán' )
reg( 'iAmar', 'implorar' )
reg( 'iAmar', 'importar' )
reg( 'iAmar', 'imposibilitar' )
reg( 'iAmar', 'impostar' )
reg( 'iAmar', 'impregnar' )
reg( 'iAmar', 'impresionar' )
reg( 'iAmar', 'improvisar' )
reg( 'iAmar', 'impugnar' )
reg( 'iAmar', 'impulsar')
reg( 'iAmar', 'imputar' )
reg( 'iAmar', 'inaugurar' )
reg( 'iAmar', 'incapacitar')
reg( 'iAmar', 'incautar' )
reg( 'iAmar', 'incentivar' )
reg( 'iAmar', 'incitar' )
reg( 'iAmar', 'inclinar', 'inclinándolo' )
reg( 'iAmar', 'incorporar', 'incorporarse' )
reg( 'iAmar', 'incrementar', 'incrementarse' )
reg( 'iAmar', 'increpar' )
reg( 'iAmar', 'incrustar' )
reg( 'iAmar', 'incubar' )
reg( 'iAmar', 'incursionar' )
reg( 'iAmar', 'indigestar', 'indigestarse' )
reg( 'iAmar', 'indignar' )
reg( 'iAmar', 'indultar' )
reg( 'iAmar', 'infectar', 'infectarse')
reg( 'iAmar', 'infiltrar', 'infiltrarse' )
reg( 'iAmar', 'informar' )
reg( 'iAmar', 'ingresar' )
reg( 'iAmar', 'inhabilitar' )
reg( 'iAmar', 'inmigrar' )
reg( 'iAmar', 'innovar' )
reg( 'iAmar', 'inquietar' )
reg( 'iAmar', 'insertar' )
reg( 'iAmar', 'insinuar' )
reg( 'iAmar', 'inspeccionar' )
reg( 'iAmar', 'inspirar' )
reg( 'iAmar', 'instalar', 'instalarla', 'instalarlo', 'instalarse' )
reg( 'iAmar', 'instar' )
reg( 'iAmar', 'instaurar' )
reg( 'iAmar', 'instrumentar' )
reg( 'iAmar', 'insultar' )
reg( 'iAmar', 'integrar', 'integrarse' )
reg( 'iAmar', 'intentar', 'intentásemos' )
reg( 'iAmar', 'intercalar' )
reg( 'iAmar', 'interceptar' )
reg( 'iAmar', 'interconectar' )
reg( 'iAmar', 'interesar', 'interesarse' )
reg( 'iAmar', 'internar', 'internarse' )
reg( 'iAmar', 'interpelar' )
reg( 'iAmar', 'interpretar', 'interpretarlos', 'interpretarse' )
reg( 'iAmar', 'intimar' )
reg( 'iAmar', 'intitular' )
reg( 'iAmar', 'inundar' )
reg( 'iAmar', 'invalidar' )
reg( 'iAmar', 'inventar' )
reg( 'iAmar', 'invitar' )
reg( 'iAmar', 'involucrar', 'involucrarse' )
reg( 'iAmar', 'inyectar', 'inyectarla' )
reg( 'iAmar', 'irritar' )
reg( 'iAmar', 'jactar', 'jactarse' )
reg( 'iAmar', 'jadear' )
reg( 'iAmar', 'jiñar' )
reg( 'iAmar', 'jubilar' )
reg( 'iAmar', 'juntar', 'juntarse' )
reg( 'iAmar', 'juramentar' )
reg( 'iAmar', 'jurar' )
reg( 'iAmar', 'laborar' )
reg( 'iAmar', 'labrar' )
reg( 'iAmar', 'lagrimear' )
reg( 'iAmar', 'lamentar' )
reg( 'iAmar', 'lastimar' )
reg( 'iAmar', 'lavar' )
reg( 'iAmar', 'legislar' )
reg( 'iAmar', 'legitimar' )
reg( 'iAmar', 'lesionar' )
reg( 'iAmar', 'levantar', 'levantarse' )
reg( 'iAmar', 'levar' )
reg( 'iAmar', 'levitar' )
reg( 'iAmar', 'libar' )
reg( 'iAmar', 'liberar', 'liberarse' )
reg( 'iAmar', 'librar', 'librarse' )
reg( 'iAmar', 'licitar' )
reg( 'iAmar', 'liderar' )
reg( 'iAmar', 'lijar' )
reg( 'iAmar', 'limitar', 'limitarse' )
reg( 'iAmar', 'liquidar' )
reg( 'iAmar', 'listar', 'listarlos' )
reg( 'iAmar', 'llamar', 'llamaremos', 'llamarse' )
reg( 'iAmar', 'llenar' )
reg( 'iAmar', 'llevar', 'llevarse', 'llevamos' )
reg( 'iAmar', 'llorar' )
reg( 'iAmar', 'loar' )
reg( 'iAmar', 'lograr', 'logramos', 'lograrse', 'lograrlo' )
reg( 'iAmar', 'luchar' )
reg( 'iAmar', 'madurar' )
reg( 'iAmar', 'malinterpretar' )
reg( 'iAmar', 'malograr' )
reg( 'iAmar', 'maltratar' )
reg( 'iAmar', 'mandar' )
reg( 'iAmar', 'manejar', 'manejarla' )
reg( 'iAmar', 'maniobrar' )
reg( 'iAmar', 'manipular' )
reg( 'iAmar', 'manufacturar' )
reg( 'iAmar', 'maravillar' )
reg( 'iAmar', 'marchar', 'marcharse' )
reg( 'iAmar', 'marchitar' )
reg( 'iAmar', 'marear' )
reg( 'iAmar', 'marginar' )
reg( 'iAmar', 'marinar' )
reg( 'iAmar', 'martillar' )
reg( 'iAmar', 'masacrar' )
reg( 'iAmar', 'masturbar' )
reg( 'iAmar', 'matar' )
reg( 'iAmar', 'matricular' )
reg( 'iAmar', 'mear' )
reg( 'iAmar', 'meditar' )
reg( 'iAmar', 'mejorar', 'mejorarlo' )
reg( 'iAmar', 'mencionar', 'mencionarse' )
reg( 'iAmar', 'menear' )
reg( 'iAmar', 'mermar' )
reg( 'iAmar', 'mezclar', 'mezclarse' )
reg( 'iAmar', 'migrar' )
reg( 'iAmar', 'militar' )
reg( 'iAmar', 'mimar' )
reg( 'iAmar', 'minar' )
reg( 'iAmar', 'mirar' )
reg( 'iAmar', 'modelar' )
reg( 'iAmar', 'moderar' )
reg( 'iAmar', 'mofar', 'mofarse' )
reg( 'iAmar', 'mojar' )
reg( 'iAmar', 'moldear' )
reg( 'iAmar', 'molestar' )
reg( 'iAmar', 'montar' )
reg( 'iAmar', 'motivar' )
reg( 'iAmar', 'mudar', 'mudarse' )
reg( 'iAmar', 'multar' )
reg( 'iAmar', 'murmurar' )
reg( 'iAmar', 'mutar' )
reg( 'iAmar', 'mutilar' )
reg( 'iAmar', 'nadar' )
reg( 'iAmar', 'najar', 'najarse' )
reg( 'iAmar', 'narrar' )
reg( 'iAmar', 'necesitar', 'necesitamos' )
reg( 'iAmar', 'nombrar' )
reg( 'iAmar', 'nominar' )
reg( 'iAmar', 'noquear' )
reg( 'iAmar', 'notar', 'nótese', 'notarse' )
reg( 'iAmar', 'numerar' )
reg( 'iAmar', 'objetar' )
reg( 'iAmar', 'obnubilar' )
reg( 'iAmar', 'obrar' )
reg( 'iAmar', 'observar', 'observarse' )
reg( 'iAmar', 'obsesionar' )
reg( 'iAmar', 'obstinar', 'obstinarse' )
reg( 'iAmar', 'ocasionar' )
reg( 'iAmar', 'ocultar', 'ocultos', 'ocultarse' )
reg( 'iAmar', 'ocupar', 'ocuparemos', 'ocuparse' )
reg( 'iAmar', 'ofertar' )
reg( 'iAmar', 'ojear' )
reg( 'iAmar', 'olvidar', 'olvidarse' )
reg( 'iAmar', 'ondear' )
reg( 'iAmar', 'operar' )
reg( 'iAmar', 'opinar' )
reg( 'iAmar', 'optar' )
reg( 'iAmar', 'orar' )
reg( 'iAmar', 'orbitar' )
reg( 'iAmar', 'ordenar', 'ordenarse' )
reg( 'iAmar', 'orear' )
reg( 'iAmar', 'orientar', 'orientarse' )
reg( 'iAmar', 'originar')
reg( 'iAmar', 'orquestar' )
reg( 'iAmar', 'osar' )
reg( 'iAmar', 'oscilar' )
reg( 'iAmar', 'ostentar' )
reg( 'iAmar', 'ovacionar' )
reg( 'iAmar', 'pactar' )
reg( 'iAmar', 'paginar', 'pagina' )
reg( 'iAmar', 'parafrasear' )
reg( 'iAmar', 'parar' )
reg( 'iAmar', 'parpadear' )
reg( 'iAmar', 'participar' )
reg( 'iAmar', 'pasar', 'pasarlo', 'pasarle', 'pasarse' )
reg( 'iAmar', 'pasear' )
reg( 'iAmar', 'patalear' )
reg( 'iAmar', 'patear' )
reg( 'iAmar', 'patentar' )
reg( 'iAmar', 'patinar' )
reg( 'iAmar', 'patrocinar' )
reg( 'iAmar', 'patrullar' )
reg( 'iAmar', 'pavimentar' )
reg( 'iAmar', 'pedalear' )
reg( 'iAmar', 'peinar' )
reg( 'iAmar', 'pelar' )
reg( 'iAmar', 'pelear' )
reg( 'iAmar', 'penetrar' )
reg( 'iAmar', 'percatar', 'percatarse' )
reg( 'iAmar', 'perdonar' )
reg( 'iAmar', 'perdurar' )
reg( 'iAmar', 'peregrinar' )
reg( 'iAmar', 'perfeccionar' )
reg( 'iAmar', 'perfilar' )
reg( 'iAmar', 'perforar' )
reg( 'iAmar', 'permutar' )
reg( 'iAmar', 'pernoctar' )
reg( 'iAmar', 'perpetrar' )
reg( 'iAmar', 'perpetuar' )
reg( 'iAmar', 'persignar' )
reg( 'iAmar', 'personar', 'personarse' )
reg( 'iAmar', 'perturbar' )
reg( 'iAmar', 'pesar' )
reg( 'iAmar', 'pillar' )
reg( 'iAmar', 'pilotar' )
reg( 'iAmar', 'pinchar' )
reg( 'iAmar', 'pintar' )
reg( 'iAmar', 'pirarse' )
reg( 'iAmar', 'piratear' )
reg( 'iAmar', 'pisar' )
reg( 'iAmar', 'pitar' )
reg( 'iAmar', 'pivotar' )
reg( 'iAmar', 'planchar' )
reg( 'iAmar', 'planear' )
reg( 'iAmar', 'plantar' )
reg( 'iAmar', 'plantear', 'plantearse' )
reg( 'iAmar', 'plasmar' )
reg( 'iAmar', 'pleitear' )
reg( 'iAmar', 'ponchar' )
reg( 'iAmar', 'popular' )
reg( 'iAmar', 'portar' )
reg( 'iAmar', 'posar' )
reg( 'iAmar', 'posesionar' )
reg( 'iAmar', 'posibilitar' )
reg( 'iAmar', 'posicionar', 'posicionarse' )
reg( 'iAmar', 'postular', 'postularse' )
reg( 'iAmar', 'precipitar' )
reg( 'iAmar', 'precisar' )
reg( 'iAmar', 'predominar' )
reg( 'iAmar', 'prefijar', 'prefijada' )
reg( 'iAmar', 'pregonar' )
reg( 'iAmar', 'preguntar', 'preguntarse' )
reg( 'iAmar', 'preocupar', 'preocuparse' )
reg( 'iAmar', 'preparar', 'prepararse' )
reg( 'iAmar', 'presentar', 'presentarlo', 'presentarse' )
reg( 'iAmar', 'preservar' )
reg( 'iAmar', 'presionar' )
reg( 'iAmar', 'prestar' )
reg( 'iAmar', 'primar' )
reg( 'iAmar', 'privar' )
reg( 'iAmar', 'procesar' )
reg( 'iAmar', 'procesionar' )
reg( 'iAmar', 'proclamar', 'proclamarse' )
reg( 'iAmar', 'procrear' )
reg( 'iAmar', 'procurar' )
reg( 'iAmar', 'profesar' )
reg( 'iAmar', 'programar' )
reg( 'iAmar', 'progresar' )
reg( 'iAmar', 'proliferar' )
reg( 'iAmar', 'promocionar' )
reg( 'iAmar', 'propinar' )
reg( 'iAmar', 'proporcionar' )
reg( 'iAmar', 'propugnar' )
reg( 'iAmar', 'propulsar' )
reg( 'iAmar', 'prosperar' )
reg( 'iAmar', 'protestar' )
reg( 'iAmar', 'proyectar' )
reg( 'iAmar', 'publicitar' )
reg( 'iAmar', 'pujar')
reg( 'iAmar', 'pulsar' )
reg( 'iAmar', 'puntuar' )
reg( 'iAmar', 'quebrantar' )
reg( 'iAmar', 'quedar', 'quedaron', 'quedará', 'quedarás', 'quedarán', 'quedarse' )
reg( 'iAmar', 'quejar', 'quejarse' )
reg( 'iAmar', 'quemar' )
reg( 'iAmar', 'querellar', 'querellarse' )
reg( 'iAmar', 'quitar', 'quitarse' )
reg( 'iAmar', 'raptar' )
reg( 'iAmar', 'rasguñar' )
reg( 'iAmar', 'rastrear' )
reg( 'iAmar', 'rayar' )
reg( 'iAmar', 'razonar' )
reg( 'iAmar', 'reaccionar' )
reg( 'iAmar', 'reacondicionar' )
reg( 'iAmar', 'reactivar' )
reg( 'iAmar', 'reafirmar' )
reg( 'iAmar', 'reagrupar' )
reg( 'iAmar', 'reanimar' )
reg( 'iAmar', 'reanudar' )
reg( 'iAmar', 'rearmar' )
reg( 'iAmar', 'reasignar' )
reg( 'iAmar', 'reavivar' )
reg( 'iAmar', 'rebajar' )
reg( 'iAmar', 'rebanar' )
reg( 'iAmar', 'rebasar' )
reg( 'iAmar', 'rebelar', 'rebelarse' )
reg( 'iAmar', 'rebotar' )
reg( 'iAmar', 'recabar' )
reg( 'iAmar', 'recalar' )
reg( 'iAmar', 'recapturar' )
reg( 'iAmar', 'recaudar' )
reg( 'iAmar', 'reciclar' )
reg( 'iAmar', 'recitar', 'recite' )
reg( 'iAmar', 'reclamar' )
reg( 'iAmar', 'reclutar' )
reg( 'iAmar', 'recobrar' )
reg( 'iAmar', 'recolectar' )
reg( 'iAmar', 'recombinar' )
reg( 'iAmar', 'recompensar' )
reg( 'iAmar', 'reconquistar' )
reg( 'iAmar', 'reconsiderar' )
reg( 'iAmar', 'recopilar' )
reg( 'iAmar', 'recortar' )
reg( 'iAmar', 'recrear' )
reg( 'iAmar', 'recriminar' )
reg( 'iAmar', 'recular' )
reg( 'iAmar', 'recuperar', 'recuperarse' )
reg( 'iAmar', 'redactar' )
reg( 'iAmar', 'redireccionar' )
reg( 'iAmar', 'rediseñar' )
reg( 'iAmar', 'redoblar' )
reg( 'iAmar', 'redondear' )
reg( 'iAmar', 'redundar' )
reg( 'iAmar', 'reeditar' )
reg( 'iAmar', 'reelaborar' )
reg( 'iAmar', 'reencarnar' )
reg( 'iAmar', 'reentrar' )
reg( 'iAmar', 'reestrenar' )
reg( 'iAmar', 'reestructurar' )
reg( 'iAmar', 'refinar' )
reg( 'iAmar', 'reflejar', 'refleje', 'reflejándolo' )
reg( 'iAmar', 'reflexionar' )
reg( 'iAmar', 'reformar' )
reg( 'iAmar', 'reformular' )
reg( 'iAmar', 'refrendar' )
reg( 'iAmar', 'refundar' )
reg( 'iAmar', 'refutar' )
reg( 'iAmar', 'regalar' )
reg( 'iAmar', 'regañar' )
reg( 'iAmar', 'regentar' )
reg( 'iAmar', 'registrar', 'registrarse' )
reg( 'iAmar', 'reglamentar' )
reg( 'iAmar', 'regrabar' )
reg( 'iAmar', 'regresar', 'regresaremos', 'regresarán' )
reg( 'iAmar', 'regular' )
reg( 'iAmar', 'rehabilitar' )
reg( 'iAmar', 'reinar' )
reg( 'iAmar', 'reinaugurar' )
reg( 'iAmar', 'reincorporar' )
reg( 'iAmar', 'reingresar' )
reg( 'iAmar', 'reinstalar' )
reg( 'iAmar', 'reinstaurar' )
reg( 'iAmar', 'reintegrar' )
reg( 'iAmar', 'reinterpretar' )
reg( 'iAmar', 'reinventar' )
reg( 'iAmar', 'reiterar' )
reg( 'iAmar', 'relacionar', 'relacionarse' )
reg( 'iAmar', 'relajar' )
reg( 'iAmar', 'relampaguear' )
reg( 'iAmar', 'relatar' )
reg( 'iAmar', 'relevar' )
reg( 'iAmar', 'rellenar' )
reg( 'iAmar', 'rematar' )
reg( 'iAmar', 'remedar' )
reg( 'iAmar', 'rememorar' )
reg( 'iAmar', 'remezclar' )
reg( 'iAmar', 'remodelar' )
reg( 'iAmar', 'remontar', 'remontarse' )
reg( 'iAmar', 'renombrar' )
reg( 'iAmar', 'renovar' )
reg( 'iAmar', 'reordenar' )
reg( 'iAmar', 'reorientar' )
reg( 'iAmar', 'reparar' )
reg( 'iAmar', 'repasar' )
reg( 'iAmar', 'repatriar' )
reg( 'iAmar', 'replantear' )
reg( 'iAmar', 'reportar' )
reg( 'iAmar', 'reposar' )
reg( 'iAmar', 'representar', 'representarla', 'representarse' )
reg( 'iAmar', 'reprochar' )
reg( 'iAmar', 'reprogramar' )
reg( 'iAmar', 'requisar' )
reg( 'iAmar', 'resaltar' )
reg( 'iAmar', 'resbalar' )
reg( 'iAmar', 'rescatar' )
reg( 'iAmar', 'reservar' )
reg( 'iAmar', 'reseñar' )
reg( 'iAmar', 'resguardar')
reg( 'iAmar', 'resignar', 'resignarse' )
reg( 'iAmar', 'respaldar' )
reg( 'iAmar', 'respetar' )
reg( 'iAmar', 'restar' )
reg( 'iAmar', 'restaurar' )
reg( 'iAmar', 'resucitar' )
reg( 'iAmar', 'resultar' )
reg( 'iAmar', 'retar' )
reg( 'iAmar', 'retardar' )
reg( 'iAmar', 'retirar', 'retirarse' )
reg( 'iAmar', 'retomar' )
reg( 'iAmar', 'retornar' )
reg( 'iAmar', 'retractar' )
reg( 'iAmar', 'retrasar' )
reg( 'iAmar', 'retratar' )
reg( 'iAmar', 'revalidar' )
reg( 'iAmar', 'revelar' )
reg( 'iAmar', 'revisar' )
reg( 'iAmar', 'revolucionar' )
reg( 'iAmar', 'robar' )
reg( 'iAmar', 'rodear', 'rodeamos' )
reg( 'iAmar', 'rondar' )
reg( 'iAmar', 'rotar' )
reg( 'iAmar', 'rumorear' )
reg( 'iAmar', 'saborear' )
reg( 'iAmar', 'sabotear' )
reg( 'iAmar', 'saldar' )
reg( 'iAmar', 'saltar' )
reg( 'iAmar', 'saltear' )
reg( 'iAmar', 'saludar' )
reg( 'iAmar', 'salvar', 'salvarse' )
reg( 'iAmar', 'sanar' )
reg( 'iAmar', 'sancionar' )
reg( 'iAmar', 'sanear' )
reg( 'iAmar', 'sangrar' )
reg( 'iAmar', 'saquear' )
reg( 'iAmar', 'secuestrar' )
reg( 'iAmar', 'secundar' )
reg( 'iAmar', 'seleccionar', 'seleccionamos', 'seleccionarlas', 'seleccionarlo', 'selecciónela', 'selecciónelos', 'selecciónelo', 'seleccionarlos' )
reg( 'iAmar', 'sellar' )
reg( 'iAmar', 'separar', 'separados', 'separadas', 'separarse' )
reg( 'iAmar', 'sepultar' )
reg( 'iAmar', 'sesionar' )
reg( 'iAmar', 'señalar', 'señalarse' )
reg( 'iAmar', 'silbar' )
reg( 'iAmar', 'simular', 'simularlos', 'simularla' )
reg( 'iAmar', 'simultanear' )
reg( 'iAmar', 'sobornar' )
reg( 'iAmar', 'sobrepasar')
reg( 'iAmar', 'socavar' )
reg( 'iAmar', 'solapar' )
reg( 'iAmar', 'solicitar' )
reg( 'iAmar', 'soltar', 'soltarlo' )
reg( 'iAmar', 'solucionar' )
reg( 'iAmar', 'solventar' )
reg( 'iAmar', 'sondear' )
reg( 'iAmar', 'sopesar' )
reg( 'iAmar', 'soplar' )
reg( 'iAmar', 'soportar' )
reg( 'iAmar', 'sortear' )
reg( 'iAmar', 'soslayar' )
reg( 'iAmar', 'sospechar' )
reg( 'iAmar', 'subastar' )
reg( 'iAmar', 'subestimar' )
reg( 'iAmar', 'sublevar' )
reg( 'iAmar', 'sublimar' )
reg( 'iAmar', 'subordinar' )
reg( 'iAmar', 'subrayar', 'subrayándolas' )
reg( 'iAmar', 'subsanar', 'subsanarse' )
reg( 'iAmar', 'subtitular' )
reg( 'iAmar', 'sudar' )
reg( 'iAmar', 'sugestionar' )
reg( 'iAmar', 'suicidar', 'suicidarse' )
reg( 'iAmar', 'sujetar' )
reg( 'iAmar', 'sumar', 'sumarse' )
reg( 'iAmar', 'suministrar' )
reg( 'iAmar', 'superar' )
reg( 'iAmar', 'supervisar' )
reg( 'iAmar', 'suplantar' )
reg( 'iAmar', 'suscitar' )
reg( 'iAmar', 'sustentar' )
reg( 'iAmar', 'susurrar' )
reg( 'iAmar', 'tachar' )
reg( 'iAmar', 'talar' )
reg( 'iAmar', 'tallar' )
reg( 'iAmar', 'tapar' )
reg( 'iAmar', 'tarar' )
reg( 'iAmar', 'tararear' )
reg( 'iAmar', 'tardar' )
reg( 'iAmar', 'tartamudear' )
reg( 'iAmar', 'telefonear' )
reg( 'iAmar', 'teletransportar' )
reg( 'iAmar', 'televisar' )
reg( 'iAmar', 'telonear' )
reg( 'iAmar', 'templar' )
reg( 'iAmar', 'tergiversar' )
reg( 'iAmar', 'terminar' )
reg( 'iAmar', 'testar' )
reg( 'iAmar', 'tildar', 'tildándolo' )
reg( 'iAmar', 'tirar' )
reg( 'iAmar', 'titubear' )
reg( 'iAmar', 'titular', 'titulares' )
reg( 'iAmar', 'tolerar' )
reg( 'iAmar', 'tomar', 'tomarla', 'tomarse' )
reg( 'iAmar', 'topar', 'toparse' )
reg( 'iAmar', 'torear' )
reg( 'iAmar', 'tornar' )
reg( 'iAmar', 'torpedear' )
reg( 'iAmar', 'torturar' )
reg( 'iAmar', 'trabajar', 'trabajaremos' )
reg( 'iAmar', 'trabar' )
reg( 'iAmar', 'traicionar' )
reg( 'iAmar', 'tramar' )
reg( 'iAmar', 'tramitar' )
reg( 'iAmar', 'transformar', 'transformarse' )
reg( 'iAmar', 'transitar' )
reg( 'iAmar', 'transparentar' )
reg( 'iAmar', 'transportar' )
reg( 'iAmar', 'trapear' )
reg( 'iAmar', 'trasformar' )
reg( 'iAmar', 'trasladar', 'trasladarse' )
reg( 'iAmar', 'trasnochar' )
reg( 'iAmar', 'traspasar' )
reg( 'iAmar', 'trastabillar' )
reg( 'iAmar', 'trastocar' )
reg( 'iAmar', 'trastornar' )
reg( 'iAmar', 'tratar', 'tratarse' )
reg( 'iAmar', 'trepar' )
reg( 'iAmar', 'tributar' )
reg( 'iAmar', 'triturar' )
reg( 'iAmar', 'triunfar' )
reg( 'iAmar', 'tumbar' )
reg( 'iAmar', 'tutear' )
reg( 'iAmar', 'ufanarse' )
reg( 'iAmar', 'ultimar' )
reg( 'iAmar', 'untar' )
reg( 'iAmar', 'usar', 'usaremos', 'usarse', '', 'usarlo', 'usamos' )
reg( 'iAmar', 'usurpar' )
reg( 'iAmar', 'vacilar' )
reg( 'iAmar', 'validar' )
reg( 'iAmar', 'valorar')
reg( 'iAmar', 'vaticinar' )
reg( 'iAmar', 'velar' )
reg( 'iAmar', 'venerar' )
reg( 'iAmar', 'veranear' )
reg( 'iAmar', 'versar' )
reg( 'iAmar', 'versionar' )
reg( 'iAmar', 'vetar' )
reg( 'iAmar', 'viajar' )
reg( 'iAmar', 'vigilar' )
reg( 'iAmar', 'vincular', 'vinculamos' )
reg( 'iAmar', 'violar' )
reg( 'iAmar', 'violentar' )
reg( 'iAmar', 'virar' )
reg( 'iAmar', 'visionar' )
reg( 'iAmar', 'visitar', 'visitarse' )
reg( 'iAmar', 'vislumbrar' )
reg( 'iAmar', 'voltear' )
reg( 'iAmar', 'vomitar' )
reg( 'iAmar', 'votar' )
reg( 'iAmar', 'vulnerar' )
reg( 'iAmar', 'zafar' )
reg( 'iAmar', 'zanjar' )
reg( 'iAmar', 'zapar' )
reg( 'iAmar', 'zarpar' )
reg( 'iAmar', 'zozobrar' )
reg( 'iAmar', 'zurrar' )
reg( 'iAndar', 'andar', 'andará', 'andarán', 'andarás', 'anduvieron' )
reg( 'iArguir', 'argüir', 'arguyó', 'arguyeron' )
reg( 'iAullar', 'aupar', 'aupó' )
reg( 'iAullar', 'rehusar', 'rehusó', 'rehusaron' )
reg( 'iAvergonzar', 'avergonzar', 'avergonzó' )
reg( 'iCaber' 'caber', 'cabía', 'cabían', 'cabías' )
reg( 'iCaer', 'caer', 'caído', 'caída', 'caídos', 'caídas', 'cayó', 'cae', 'caerá', 'caerán', 'caerás', 'caerse', 'caía', 'caían', 'caías', 'cayeron' )
reg( 'iCaer', 'decaer', 'decayó', 'decaerá', 'decaerán', 'decaerás', 'decayeron' )
reg( 'iCaer', 'recaer', 'recayó', 'recaerá', 'recaerán', 'recaerás', 'recaía', 'recaían', 'recaías', 'recayeron' )
reg( 'iCambiar', 'abreviar' )
reg( 'iCambiar', 'acariciar' )
reg( 'iCambiar', 'acopiar' )
reg( 'iCambiar', 'acuciar' )
reg( 'iCambiar', 'agenciar' )
reg( 'iCambiar', 'agobiar' )
reg( 'iCambiar', 'agraciar' )
reg( 'iCambiar', 'agraviar' )
reg( 'iCambiar', 'agremiar' )
reg( 'iCambiar', 'ajusticiar' )
reg( 'iCambiar', 'aliviar' )
reg( 'iCambiar', 'anestesiar' )
reg( 'iCambiar', 'angustiar' )
reg( 'iCambiar', 'anunciar' )
reg( 'iCambiar', 'apreciar', 'apreciarse' )
reg( 'iCambiar', 'apremiar' )
reg( 'iCambiar', 'apropiar', 'apropiarse' )
reg( 'iCambiar', 'arreciar' )
reg( 'iCambiar', 'asalariar' )
reg( 'iCambiar', 'asediar' )
reg( 'iCambiar', 'asfixiar' )
reg( 'iCambiar', 'asociar', 'asociarse' )
reg( 'iCambiar', 'atrofiar' )
reg( 'iCambiar', 'auspiciar' )
reg( 'iCambiar', 'beneficiar', 'beneficiarse' )
reg( 'iCambiar', 'calumniar' )
reg( 'iCambiar', 'cambiar', 'cámbieles', 'cambiándole', 'cambiarle', 'cambiarse' )
reg( 'iCambiar', 'codiciar' )
reg( 'iCambiar', 'colegiar' )
reg( 'iCambiar', 'columpiar' )
reg( 'iCambiar', 'comerciar' )
reg( 'iCambiar', 'compendiar' )
reg( 'iCambiar', 'concienciar' )
reg( 'iCambiar', 'conferenciar' )
reg( 'iCambiar', 'congeniar' )
reg( 'iCambiar', 'congraciar' )
reg( 'iCambiar', 'contagiar', 'contagiarlos' )
reg( 'iCambiar', 'copiar', 'copiarlo' )
reg( 'iCambiar', 'custodiar' )
reg( 'iCambiar', 'defoliar' )
reg( 'iCambiar', 'denunciar' )
reg( 'iCambiar', 'depreciar' )
reg( 'iCambiar', 'derrubiar' )
reg( 'iCambiar', 'desagraviar' )
reg( 'iCambiar', 'desahuciar' )
reg( 'iCambiar', 'desapropiar' )
reg( 'iCambiar', 'descambiar' )
reg( 'iCambiar', 'desgraciar' )
reg( 'iCambiar', 'desperdiciar' )
reg( 'iCambiar', 'despreciar' )
reg( 'iCambiar', 'desprestigiar' )
reg( 'iCambiar', 'desquiciar' )
reg( 'iCambiar', 'diferenciar', 'diferenciarse' )
reg( 'iCambiar', 'diligenciar' )
reg( 'iCambiar', 'diluviar' )
reg( 'iCambiar', 'disociar' )
reg( 'iCambiar', 'distanciar', 'distanciarse' )
reg( 'iCambiar', 'divorciar', 'divorciaron', 'divorciarse' )
reg( 'iCambiar', 'domiciliar' )
reg( 'iCambiar', 'elogiar' )
reg( 'iCambiar', 'empapuciar' )
reg( 'iCambiar', 'encomiar' )
reg( 'iCambiar', 'endemoniar' )
reg( 'iCambiar', 'enjuiciar' )
reg( 'iCambiar', 'ennoviarse' )
reg( 'iCambiar', 'enrabiar' )
reg( 'iCambiar', 'enranciar' )
reg( 'iCambiar', 'ensuciar' )
reg( 'iCambiar', 'entibiar' )
reg( 'iCambiar', 'enturbiar' )
reg( 'iCambiar', 'enunciar' )
reg( 'iCambiar', 'enviciar' )
reg( 'iCambiar', 'envidiar' )
reg( 'iCambiar', 'escanciar' )
reg( 'iCambiar', 'escoliar' )
reg( 'iCambiar', 'escoriar' )
reg( 'iCambiar', 'espaciar' )
reg( 'iCambiar', 'espoliar' )
reg( 'iCambiar', 'estudiar', 'estudiaron' )
reg( 'iCambiar', 'evidenciar' )
reg( 'iCambiar', 'excoriar' )
reg( 'iCambiar', 'exfoliar' )
reg( 'iCambiar', 'exiliar', 'exiliarse' )
reg( 'iCambiar', 'expoliar' )
reg( 'iCambiar', 'expropiar' )
reg( 'iCambiar', 'fastidiar' )
reg( 'iCambiar', 'feriar' )
reg( 'iCambiar', 'filiar' )
reg( 'iCambiar', 'financiar' )
reg( 'iCambiar', 'foliar' )
reg( 'iCambiar', 'fotocopiar' )
reg( 'iCambiar', 'herniar' )
reg( 'iCambiar', 'hipertrofiar' )
reg( 'iCambiar', 'hostiar' )
reg( 'iCambiar', 'incendiar' )
reg( 'iCambiar', 'incordiar' )
reg( 'iCambiar', 'influenciar' )
reg( 'iCambiar', 'ingeniar' )
reg( 'iCambiar', 'iniciar', 'inició', 'iniciarse', 'iniciaron' )
reg( 'iCambiar', 'injuriar' )
reg( 'iCambiar', 'intercambiar' )
reg( 'iCambiar', 'intermediar' )
reg( 'iCambiar', 'irradiar' )
reg( 'iCambiar', 'jipiar' )
reg( 'iCambiar', 'justipreciar' )
reg( 'iCambiar', 'licenciar', 'licenciarse' )
reg( 'iCambiar', 'lidiar' )
reg( 'iCambiar', 'limpiar' )
reg( 'iCambiar', 'lisiar' )
reg( 'iCambiar', 'matrimoniar' )
reg( 'iCambiar', 'mediar' )
reg( 'iCambiar', 'menospreciar' )
reg( 'iCambiar', 'miniar' )
reg( 'iCambiar', 'mustiar' )
reg( 'iCambiar', 'negociar' )
reg( 'iCambiar', 'obsequiar' )
reg( 'iCambiar', 'obviar' )
reg( 'iCambiar', 'odiar' )
reg( 'iCambiar', 'oficiar' )
reg( 'iCambiar', 'oprobiar' )
reg( 'iCambiar', 'paliar' )
reg( 'iCambiar', 'parodiar' )
reg( 'iCambiar', 'pifiar' )
reg( 'iCambiar', 'plagiar' )
reg( 'iCambiar', 'potenciar' )
reg( 'iCambiar', 'preciar' )
reg( 'iCambiar', 'preludiar' )
reg( 'iCambiar', 'premiar' )
reg( 'iCambiar', 'presagiar' )
reg( 'iCambiar', 'presenciar' )
reg( 'iCambiar', 'prestigiar' )
reg( 'iCambiar', 'principiar' )
reg( 'iCambiar', 'privilegiar' )
reg( 'iCambiar', 'promediar' )
reg( 'iCambiar', 'pronunciar', 'pronunciarse' )
reg( 'iCambiar', 'propiciar' )
reg( 'iCambiar', 'rabiar' )
reg( 'iCambiar', 'radiar' )
reg( 'iCambiar', 'ranciar' )
reg( 'iCambiar', 'recambiar' )
reg( 'iCambiar', 'reconciliar', 'reconciliarse' )
reg( 'iCambiar', 'referenciar', 'referenciarlo' )
reg( 'iCambiar', 'refugiar', 'refugiarse' )
reg( 'iCambiar', 'reiniciar' )
reg( 'iCambiar', 'remediar' )
reg( 'iCambiar', 'renunciar' )
reg( 'iCambiar', 'repudiar' )
reg( 'iCambiar', 'resabiar' )
reg( 'iCambiar', 'reverenciar' )
reg( 'iCambiar', 'rumiar' )
reg( 'iCambiar', 'saciar' )
reg( 'iCambiar', 'salmodiar' )
reg( 'iCambiar', 'secuenciar' )
reg( 'iCambiar', 'sentenciar' )
reg( 'iCambiar', 'seriar' )
reg( 'iCambiar', 'silenciar' )
reg( 'iCambiar', 'sitiar' )
reg( 'iCambiar', 'subsidiar' )
reg( 'iCambiar', 'substanciar' )
reg( 'iCambiar', 'sustanciar' )
reg( 'iCambiar', 'tapiar' )
reg( 'iCambiar', 'terciar' )
reg( 'iCambiar', 'testimoniar' )
reg( 'iCambiar', 'tibiar' )
reg( 'iCambiar', 'transubstanciar' )
reg( 'iCambiar', 'vanagloriarse' )
reg( 'iCambiar', 'vendimiar' )
reg( 'iCambiar', 'viciar' )
reg( 'iCambiar', 'vilipendiar' )
reg( 'iCazar', 'abalanzar', 'abalanzarse' )
reg( 'iCazar', 'abonanzar' )
reg( 'iCazar', 'abrazar' )
reg( 'iCazar', 'acorazar' )
reg( 'iCazar', 'actualizar' )
reg( 'iCazar', 'acuatizar' )
reg( 'iCazar', 'adelgazar' )
reg( 'iCazar', 'aderezar' )
reg( 'iCazar', 'adverbializar' )
reg( 'iCazar', 'afianzar' )
reg( 'iCazar', 'africanizar' )
reg( 'iCazar', 'agilizar' )
reg( 'iCazar', 'agonizar' )
reg( 'iCazar', 'agudizar' )
reg( 'iCazar', 'aguzar' )
reg( 'iCazar', 'alborozar' )
reg( 'iCazar', 'alcalinizar' )
reg( 'iCazar', 'alcanzar' )
reg( 'iCazar', 'alcoholizar' )
reg( 'iCazar', 'alfabetizar' )
reg( 'iCazar', 'alunizar' )
reg( 'iCazar', 'aluzar' )
reg( 'iCazar', 'alzar', 'alzarse' )
reg( 'iCazar', 'amarizar' )
reg( 'iCazar', 'amenazar' )
reg( 'iCazar', 'amenizar' )
reg( 'iCazar', 'americanizar' )
reg( 'iCazar', 'amerizar' )
reg( 'iCazar', 'amordazar' )
reg( 'iCazar', 'amortizar' )
reg( 'iCazar', 'amostazar' )
reg( 'iCazar', 'analizar' )
reg( 'iCazar', 'anatematizar' )
reg( 'iCazar', 'animalizar' )
reg( 'iCazar', 'apelmazar' )
reg( 'iCazar', 'aplazar' )
reg( 'iCazar', 'arabizar' )
reg( 'iCazar', 'armonizar' )
reg( 'iCazar', 'aromatizar' )
reg( 'iCazar', 'atemorizar' )
reg( 'iCazar', 'atenazar' )
reg( 'iCazar', 'aterrizar' )
reg( 'iCazar', 'aterrorizar' )
reg( 'iCazar', 'atezar' )
reg( 'iCazar', 'atizar' )
reg( 'iCazar', 'atomizar' )
reg( 'iCazar', 'automatizar' )
reg( 'iCazar', 'autorizar' )
reg( 'iCazar', 'avanzar' )
reg( 'iCazar', 'avezar' )
reg( 'iCazar', 'azuzar' )
reg( 'iCazar', 'barnizar' )
reg( 'iCazar', 'bautizar' )
reg( 'iCazar', 'bostezar' )
reg( 'iCazar', 'burocratizar' )
reg( 'iCazar', 'calzar' )
reg( 'iCazar', 'canalizar' )
reg( 'iCazar', 'canonizar' )
reg( 'iCazar', 'capitalizar' )
reg( 'iCazar', 'caracterizar' )
reg( 'iCazar', 'caramelizar' )
reg( 'iCazar', 'carbonizar' )
reg( 'iCazar', 'caricaturizar' )
reg( 'iCazar', 'castellanizar' )
reg( 'iCazar', 'catalanizar', 'catalanizó' )
reg( 'iCazar', 'catalizar' )
reg( 'iCazar', 'categorizar', 'categorízame' )
reg( 'iCazar', 'cauterizar' )
reg( 'iCazar', 'cazar' )
reg( 'iCazar', 'centralizar' )
reg( 'iCazar', 'chapuzar' )
reg( 'iCazar', 'cicatrizar' )
reg( 'iCazar', 'civilizar' )
reg( 'iCazar', 'climatizar' )
reg( 'iCazar', 'colonizar', 'colonizaron' )
reg( 'iCazar', 'comercializar' )
reg( 'iCazar', 'compatibilizar' )
reg( 'iCazar', 'computadorizar' )
reg( 'iCazar', 'computarizar' )
reg( 'iCazar', 'computerizar' )
reg( 'iCazar', 'conceptualizar' )
reg( 'iCazar', 'concretizar' )
reg( 'iCazar', 'confraternizar' )
reg( 'iCazar', 'contabilizar' )
reg( 'iCazar', 'contemporizar' )
reg( 'iCazar', 'coprotagonizar' )
reg( 'iCazar', 'cotizar' )
reg( 'iCazar', 'criogenizar' )
reg( 'iCazar', 'cristalizar' )
reg( 'iCazar', 'cristianizar' )
reg( 'iCazar', 'cruzar', 'cruzaron', 'cruzarse' )
reg( 'iCazar', 'culpabilizar' )
reg( 'iCazar', 'culturizar' )
reg( 'iCazar', 'danzar' )
reg( 'iCazar', 'democratizar' )
reg( 'iCazar', 'derechizar' )
reg( 'iCazar', 'desacralizar' )
reg( 'iCazar', 'desalinizar' )
reg( 'iCazar', 'desamortizar' )
reg( 'iCazar', 'desarmonizar' )
reg( 'iCazar', 'desautorizar' )
reg( 'iCazar', 'desbrozar' )
reg( 'iCazar', 'descabezar' )
reg( 'iCazar', 'descalzar' )
reg( 'iCazar', 'descapitalizar' )
reg( 'iCazar', 'descarozar' )
reg( 'iCazar', 'descentralizar' )
reg( 'iCazar', 'descontextualizar' )
reg( 'iCazar', 'descortezar' )
reg( 'iCazar', 'descruzar' )
reg( 'iCazar', 'descuartizar' )
reg( 'iCazar', 'desdramatizar' )
reg( 'iCazar', 'desembarazar' )
reg( 'iCazar', 'desentronizar' )
reg( 'iCazar', 'desertizar' )
reg( 'iCazar', 'desesperanzar' )
reg( 'iCazar', 'desestabilizar' )
reg( 'iCazar', 'desguazar' )
reg( 'iCazar', 'deshumanizar' )
reg( 'iCazar', 'desindustrializar' )
reg( 'iCazar', 'deslizar' )
reg( 'iCazar', 'desmenuzar' )
reg( 'iCazar', 'desmilitarizar' )
reg( 'iCazar', 'desmineralizarse' )
reg( 'iCazar', 'desmonetizar' )
reg( 'iCazar', 'desmoralizar' )
reg( 'iCazar', 'desmovilizar', 'desmovilizó' )
reg( 'iCazar', 'desnaturalizar' )
reg( 'iCazar', 'desodorizar' )
reg( 'iCazar', 'desorganizar' )
reg( 'iCazar', 'despedazar' )
reg( 'iCazar', 'despenalizar' )
reg( 'iCazar', 'desperezarse' )
reg( 'iCazar', 'despersonalizar' )
reg( 'iCazar', 'despiezar' )
reg( 'iCazar', 'desplazar', 'desplazarlo', 'desplazarse', 'desplácese' )
reg( 'iCazar', 'despotizar' )
reg( 'iCazar', 'desratizar' )
reg( 'iCazar', 'desrizar' )
reg( 'iCazar', 'destrenzar' )
reg( 'iCazar', 'destrozar' )
reg( 'iCazar', 'desvalorizar' )
reg( 'iCazar', 'digitalizar' )
reg( 'iCazar', 'dinamizar' )
reg( 'iCazar', 'disfrazar' )
reg( 'iCazar', 'divinizar' )
reg( 'iCazar', 'dogmatizar' )
reg( 'iCazar', 'dramatizar' )
reg( 'iCazar', 'economizar' )
reg( 'iCazar', 'ecualizar' )
reg( 'iCazar', 'ejemplarizar' )
reg( 'iCazar', 'electrizar' )
reg( 'iCazar', 'embarazar' )
reg( 'iCazar', 'embozar' )
reg( 'iCazar', 'empapuzar' )
reg( 'iCazar', 'emplazar' )
reg( 'iCazar', 'encabezar' )
reg( 'iCazar', 'encarnizar' )
reg( 'iCazar', 'encauzar' )
reg( 'iCazar', 'encolerizar' )
reg( 'iCazar', 'enderezar' )
reg( 'iCazar', 'endulzar' )
reg( 'iCazar', 'enfatizar' )
reg( 'iCazar', 'enfervorizar' )
reg( 'iCazar', 'engarzar' )
reg( 'iCazar', 'enjaezar' )
reg( 'iCazar', 'enlazar', 'enlazarlas', 'enlazarlos', 'enlazarla', 'enlazándola', 'enlazaran', 'enlazara' )
reg( 'iCazar', 'enlodazar' )
reg( 'iCazar', 'ensalzar' )
reg( 'iCazar', 'entrecruzar' )
reg( 'iCazar', 'entrelazar' )
reg( 'iCazar', 'entronizar' )
reg( 'iCazar', 'enzarzar' )
reg( 'iCazar', 'erizar' )
reg( 'iCazar', 'erotizar' )
reg( 'iCazar', 'esbozar' )
reg( 'iCazar', 'escandalizar' )
reg( 'iCazar', 'esclavizar' )
reg( 'iCazar', 'escolarizar' )
reg( 'iCazar', 'españolizar' )
reg( 'iCazar', 'especializar' )
reg( 'iCazar', 'esperanzar' )
reg( 'iCazar', 'espiritualizar' )
reg( 'iCazar', 'esponsorizar' )
reg( 'iCazar', 'esquematizar' )
reg( 'iCazar', 'estabilizar' )
reg( 'iCazar', 'estandarizar' )
reg( 'iCazar', 'estatalizar' )
reg( 'iCazar', 'estelarizar' )
reg( 'iCazar', 'esterilizar' )
reg( 'iCazar', 'estigmatizar' )
reg( 'iCazar', 'estilizar' )
reg( 'iCazar', 'eternizar' )
reg( 'iCazar', 'evangelizar' )
reg( 'iCazar', 'exorcizar' )
reg( 'iCazar', 'exteriorizar' )
reg( 'iCazar', 'familiarizar', 'familiarizarse' )
reg( 'iCazar', 'fecundizar' )
reg( 'iCazar', 'fertilizar' )
reg( 'iCazar', 'finalizar' )
reg( 'iCazar', 'fiscalizar' )
reg( 'iCazar', 'flexibilizar' )
reg( 'iCazar', 'focalizar' )
reg( 'iCazar', 'formalizar' )
reg( 'iCazar', 'fosilizarse' )
reg( 'iCazar', 'fraternizar' )
reg( 'iCazar', 'frezar' )
reg( 'iCazar', 'galvanizar' )
reg( 'iCazar', 'garantizar' )
reg( 'iCazar', 'generalizar', 'generalizarse' )
reg( 'iCazar', 'germanizar' )
reg( 'iCazar', 'globalizar' )
reg( 'iCazar', 'gozar' )
reg( 'iCazar', 'granizar' )
reg( 'iCazar', 'hechizar' )
reg( 'iCazar', 'helenizar' )
reg( 'iCazar', 'hidrolizar' )
reg( 'iCazar', 'higienizar' )
reg( 'iCazar', 'hipnotizar' )
reg( 'iCazar', 'hispanizar' )
reg( 'iCazar', 'horrorizar' )
reg( 'iCazar', 'hospitalizar' )
reg( 'iCazar', 'hostilizar' )
reg( 'iCazar', 'hozar' )
reg( 'iCazar', 'humanizar' )
reg( 'iCazar', 'idealizar' )
reg( 'iCazar', 'idiotizar' )
reg( 'iCazar', 'ilegalizar' )
reg( 'iCazar', 'ilegitimizar' )
reg( 'iCazar', 'impermeabilizar' )
reg( 'iCazar', 'indemnizar' )
reg( 'iCazar', 'independizar', 'independizarse' )
reg( 'iCazar', 'individualizar' )
reg( 'iCazar', 'indizar' )
reg( 'iCazar', 'industrializar' )
reg( 'iCazar', 'infantilizar' )
reg( 'iCazar', 'informatizar' )
reg( 'iCazar', 'inicializar' )
reg( 'iCazar', 'inmortalizar' )
reg( 'iCazar', 'inmovilizar' )
reg( 'iCazar', 'inmunizar' )
reg( 'iCazar', 'insensibilizar' )
reg( 'iCazar', 'insonorizar' )
reg( 'iCazar', 'institucionalizar' )
reg( 'iCazar', 'instrumentalizar' )
reg( 'iCazar', 'intelectualizar' )
reg( 'iCazar', 'interiorizar' )
reg( 'iCazar', 'internacionalizar' )
reg( 'iCazar', 'intranquilizar' )
reg( 'iCazar', 'inutilizar', 'utilizarse' )
reg( 'iCazar', 'ionizar' )
reg( 'iCazar', 'ironizar' )
reg( 'iCazar', 'islamizar' )
reg( 'iCazar', 'izar' )
reg( 'iCazar', 'jerarquizar' )
reg( 'iCazar', 'labializar' )
reg( 'iCazar', 'laicizar' )
reg( 'iCazar', 'lanzar', 'lanzarse' )
reg( 'iCazar', 'lateralizar' )
reg( 'iCazar', 'latinizar' )
reg( 'iCazar', 'lazar' )
reg( 'iCazar', 'legalizar' )
reg( 'iCazar', 'lexicalizar' )
reg( 'iCazar', 'liberalizar' )
reg( 'iCazar', 'liofilizar' )
reg( 'iCazar', 'localizar', 'localizarlos')
reg( 'iCazar', 'macizar' )
reg( 'iCazar', 'magnetizar' )
reg( 'iCazar', 'maquinizar' )
reg( 'iCazar', 'martirizar' )
reg( 'iCazar', 'materializar' )
reg( 'iCazar', 'matizar' )
reg( 'iCazar', 'maximizar' )
reg( 'iCazar', 'mecanizar' )
reg( 'iCazar', 'mediatizar' )
reg( 'iCazar', 'memorizar' )
reg( 'iCazar', 'mentalizar' )
reg( 'iCazar', 'metabolizar' )
reg( 'iCazar', 'metalizar' )
reg( 'iCazar', 'meteorizar' )
reg( 'iCazar', 'mexicanizar' )
reg( 'iCazar', 'militarizar' )
reg( 'iCazar', 'mimetizar' )
reg( 'iCazar', 'mineralizar' )
reg( 'iCazar', 'miniaturizar' )
reg( 'iCazar', 'minimizar' )
reg( 'iCazar', 'modernizar' )
reg( 'iCazar', 'monetizar' )
reg( 'iCazar', 'monitorizar' )
reg( 'iCazar', 'monopolizar' )
reg( 'iCazar', 'moralizar' )
reg( 'iCazar', 'motorizar' )
reg( 'iCazar', 'movilizar' )
reg( 'iCazar', 'municipalizar' )
reg( 'iCazar', 'musicalizar' )
reg( 'iCazar', 'nacionalizar' )
reg( 'iCazar', 'narcotizar' )
reg( 'iCazar', 'nasalizar' )
reg( 'iCazar', 'naturalizar' )
reg( 'iCazar', 'nebulizar' )
reg( 'iCazar', 'neutralizar' )
reg( 'iCazar', 'nominalizar' )
reg( 'iCazar', 'normalizar' )
reg( 'iCazar', 'nuclearizar' )
reg( 'iCazar', 'obstaculizar' )
reg( 'iCazar', 'occidentalizar' )
reg( 'iCazar', 'oficializar' )
reg( 'iCazar', 'optimizar' )
reg( 'iCazar', 'organizar' )
reg( 'iCazar', 'orientalizar' )
reg( 'iCazar', 'orzar' )
reg( 'iCazar', 'paganizar' )
reg( 'iCazar', 'palatalizar' )
reg( 'iCazar', 'parabolizar' )
reg( 'iCazar', 'paralizar' )
reg( 'iCazar', 'particularizar' )
reg( 'iCazar', 'pasterizar' )
reg( 'iCazar', 'pasteurizar' )
reg( 'iCazar', 'patentizar' )
reg( 'iCazar', 'pauperizar' )
reg( 'iCazar', 'penalizar' )
reg( 'iCazar', 'perennizar' )
reg( 'iCazar', 'permeabilizar' )
reg( 'iCazar', 'personalizar' )
reg( 'iCazar', 'pinzar' )
reg( 'iCazar', 'pluralizar' )
reg( 'iCazar', 'poetizar' )
reg( 'iCazar', 'polarizar' )
reg( 'iCazar', 'polemizar' )
reg( 'iCazar', 'polinizar' )
reg( 'iCazar', 'politizar' )
reg( 'iCazar', 'popularizar' )
reg( 'iCazar', 'pormenorizar' )
reg( 'iCazar', 'potabilizar' )
reg( 'iCazar', 'preconizar' )
reg( 'iCazar', 'presurizar' )
reg( 'iCazar', 'previsualizar' )
reg( 'iCazar', 'priorizar' )
reg( 'iCazar', 'privatizar' )
reg( 'iCazar', 'profesionalizar' )
reg( 'iCazar', 'profetizar' )
reg( 'iCazar', 'profundizar' )
reg( 'iCazar', 'protagonizar' )
reg( 'iCazar', 'psicoanalizar' )
reg( 'iCazar', 'pulverizar' )
reg( 'iCazar', 'puntualizar' )
reg( 'iCazar', 'punzar' )
reg( 'iCazar', 'racionalizar' )
reg( 'iCazar', 'radicalizar' )
reg( 'iCazar', 'ralentizar' )
reg( 'iCazar', 'realizar', 'realizarse', 'realizarlo', 'realizaran', 'realizaron' )
reg( 'iCazar', 'realzar' )
reg( 'iCazar', 'rebautizar' )
reg( 'iCazar', 'rebozar' )
reg( 'iCazar', 'rechazar', 'rechazar' )
reg( 'iCazar', 'reemplazar' )
reg( 'iCazar', 'regularizar' )
reg( 'iCazar', 'reinicializar' )
reg( 'iCazar', 'relanzar' )
reg( 'iCazar', 'relativizar' )
reg( 'iCazar', 'remasterizar', 'remasterizó' )
reg( 'iCazar', 'remozar' )
reg( 'iCazar', 'remplazar' )
reg( 'iCazar', 'renderizar')
reg( 'iCazar', 'rentabilizar' )
reg( 'iCazar', 'reorganizar', 'organizarse' )
reg( 'iCazar', 'repentizar' )
reg( 'iCazar', 'reprivatizar' )
reg( 'iCazar', 'responsabilizar' )
reg( 'iCazar', 'retozar' )
reg( 'iCazar', 'reutilizar' )
reg( 'iCazar', 'revalorizar' )
reg( 'iCazar', 'revitalizar' )
reg( 'iCazar', 'rezar' )
reg( 'iCazar', 'ridiculizar' )
reg( 'iCazar', 'rivalizar' )
reg( 'iCazar', 'rizar' )
reg( 'iCazar', 'robotizar' )
reg( 'iCazar', 'romanizar' )
reg( 'iCazar', 'ronzar' )
reg( 'iCazar', 'rozar' )
reg( 'iCazar', 'ruborizar' )
reg( 'iCazar', 'sacralizar' )
reg( 'iCazar', 'satirizar' )
reg( 'iCazar', 'secularizar' )
reg( 'iCazar', 'sensibilizar' )
reg( 'iCazar', 'señalizar' )
reg( 'iCazar', 'simbolizar' )
reg( 'iCazar', 'simpatizar' )
reg( 'iCazar', 'sincronizar' )
reg( 'iCazar', 'singularizar' )
reg( 'iCazar', 'sinterizar' )
reg( 'iCazar', 'sintetizar' )
reg( 'iCazar', 'sintonizar' )
reg( 'iCazar', 'sistematizar' )
reg( 'iCazar', 'sobrealzar' )
reg( 'iCazar', 'socializar' )
reg( 'iCazar', 'sodomizar' )
reg( 'iCazar', 'solazar' )
reg( 'iCazar', 'solemnizar' )
reg( 'iCazar', 'solidarizar' )
reg( 'iCazar', 'sollozar' )
reg( 'iCazar', 'somatizar' )
reg( 'iCazar', 'sonorizar' )
reg( 'iCazar', 'sponsorizar' )
reg( 'iCazar', 'suavizar' )
reg( 'iCazar', 'sutilizar' )
reg( 'iCazar', 'tamizar' )
reg( 'iCazar', 'tapizar' )
reg( 'iCazar', 'teatralizar' )
reg( 'iCazar', 'temporalizar' )
reg( 'iCazar', 'teorizar' )
reg( 'iCazar', 'tiranizar' )
reg( 'iCazar', 'totalizar' )
reg( 'iCazar', 'tranquilizar' )
reg( 'iCazar', 'traumatizar' )
reg( 'iCazar', 'trazar' )
reg( 'iCazar', 'trenzar' )
reg( 'iCazar', 'trivializar' )
reg( 'iCazar', 'uniformizar' )
reg( 'iCazar', 'universalizar' )
reg( 'iCazar', 'uperizar' )
reg( 'iCazar', 'urbanizar' )
reg( 'iCazar', 'utilizar', 'utilizaremos', 'utilizarlas', 'utilizarán', 'utilizarlos' )
reg( 'iCazar', 'valorizar' )
reg( 'iCazar', 'vampirizar' )
reg( 'iCazar', 'vandalizar' )
reg( 'iCazar', 'vaporizar', 'vectorizarlo' )
reg( 'iCazar', 'vehiculizar' )
reg( 'iCazar', 'velarizar' )
reg( 'iCazar', 'verbalizar' )
reg( 'iCazar', 'vigorizar' )
reg( 'iCazar', 'visibilizar' )
reg( 'iCazar', 'visualizar' )
reg( 'iCazar', 'vitalizar' )
reg( 'iCazar', 'vocalizar' )
reg( 'iCazar', 'volatilizar' )
reg( 'iCazar', 'vulcanizar' )
reg( 'iCazar', 'vulgarizar' )
reg( 'iCoger', 'absterger' )
reg( 'iCoger', 'acoger', 'acogía', 'acogían', 'acogías' )
reg( 'iCoger', 'asperger' )
reg( 'iCoger', 'coger', 'cogerse' )
reg( 'iCoger', 'converger' )
reg( 'iCoger', 'desproteger', 'desprotegerse' )
reg( 'iCoger', 'emerger', 'emergía', 'emergían', 'emergías' )
reg( 'iCoger', 'encoger', 'encogerse' )
reg( 'iCoger', 'escoger', 'escogía', 'escogían', 'escogías' )
reg( 'iCoger', 'proteger', 'protegerse' )
reg( 'iCoger', 'recoger', 'recogerse', 'recogerlo', 'recogía', 'recogían', 'recogías' )
reg( 'iCoger', 'sobrecoger', 'sobrecogerse' )
reg( 'iCohibir', 'prohibir', 'prohíbe', 'prohíben', 'prohíbes', 'prohibía', 'prohibían', 'prohibió', 'prohibirá', 'prohibirán', 'prohibirás', 'prohibieron' )
reg( 'iConducir', 'aducir')
reg( 'iConducir', 'conducir')
reg( 'iConducir', 'coproducir' )
reg( 'iConducir', 'deducir', 'deducirse', 'deducimos')
reg( 'iConducir', 'inducir')
reg( 'iConducir', 'introducir', 'introducirse', 'introducimos' )
reg( 'iConducir', 'producir', 'produciría', 'producirse' )
reg( 'iConducir', 'reconducir')
reg( 'iConducir', 'reducir', 'reducirse' )
reg( 'iConducir', 'reintroducir', 'reintrodujeron' )
reg( 'iConducir', 'reproducir', 'reproducirse', 'reproducimos', 'reprodujimos')
reg( 'iConducir', 'seducir')
reg( 'iConducir', 'traducir', 'traducirse' )
reg( 'iContar', 'acordar', 'acuerdo', 'acordaron' )
reg( 'iContar', 'acostar', 'acuesto', 'acostarse' )
reg( 'iContar', 'afollar', 'afuello', 'afollarse' )
reg( 'iContar', 'aforar', 'afuero' )
reg( 'iContar', 'amoblar', 'amueblo' )
reg( 'iContar', 'amolar', 'amuelo' )
reg( 'iContar', 'apostar', 'apuesto' )
reg( 'iContar', 'aprobar', 'apruebo' )
reg( 'iContar', 'asolar', 'asuelo' )
reg( 'iContar', 'asonar', 'asueno' )
reg( 'iContar', 'atronar', 'atrueno' )
reg( 'iContar', 'colar', 'cuelo' )
reg( 'iContar', 'comprobar', 'compruebo' )
reg( 'iContar', 'concordar', 'concuerdo' )
reg( 'iContar', 'consolar', 'consuelo' )
reg( 'iContar', 'contar', 'cuento' )
reg( 'iContar', 'costar', 'cuesto' )
reg( 'iContar', 'demostrar', 'demuestro', 'demostraron', 'demostraría', 'demostrarse' )
reg( 'iContar', 'denostar', 'denuesto' )
reg( 'iContar', 'desacordar', 'desacuerdo' )
reg( 'iContar', 'desaforar', 'desafuero' )
reg( 'iContar', 'desaprobar', 'desapruebo' )
reg( 'iContar', 'descollar', 'descuello' )
reg( 'iContar', 'desconsolar', 'desconsuelo' )
reg( 'iContar', 'descontar', 'descuento' )
reg( 'iContar', 'descornar', 'descuerno' )
reg( 'iContar', 'desencontrar', 'desencuentro', 'desencontrarse' )
reg( 'iContar', 'desolar', 'desuelo' )
reg( 'iContar', 'desollar', 'desuello' )
reg( 'iContar', 'desollar', 'desuello', 'desolló' )
reg( 'iContar', 'despoblar', 'despueblo' )
reg( 'iContar', 'discordar', 'discuerdo' )
reg( 'iContar', 'disonar', 'disueno' )
reg( 'iContar', 'encontrar', 'encuentro', 'encontrarlos', 'encontrarse', 'encontraría', 'encontrarían', 'encontraron' )
reg( 'iContar', 'engrosar', 'engrueso' )
reg( 'iContar', 'escornar', 'escuerno' )
reg( 'iContar', 'hollar', 'huello' )
reg( 'iContar', 'mancornar', 'mancuerno' )
reg( 'iContar', 'mostrar', 'muestro', 'mostrarse' )
reg( 'iContar', 'poblar', 'pueblo' )
reg( 'iContar', 'probar', 'pruebo', 'probaron', 'probarse' )
reg( 'iContar', 'recontar', 'recuento' )
reg( 'iContar', 'recordar', 'recuerdo' )
reg( 'iContar', 'recostar', 'recuesto' )
reg( 'iContar', 'reencontrar', 'reencuentro', 'reencontrarse' )
reg( 'iContar', 'renovar', 'renuevo' )
reg( 'iContar', 'repoblar', 'repueblo' )
reg( 'iContar', 'reprobar', 'repruebo' )
reg( 'iContar', 'resollar', 'resuello' )
reg( 'iContar', 'resonar', 'resueno' )
reg( 'iContar', 'rodar', 'ruedo' )
reg( 'iContar', 'sobrevolar', 'sebrevuelo' )
reg( 'iContar', 'solar', 'suelo' )
reg( 'iContar', 'soldar', 'sueldo' )
reg( 'iContar', 'soltar', 'suelto' )
reg( 'iContar', 'sonar', 'sueno' )
reg( 'iContar', 'soñar', 'sueño' )
reg( 'iContar', 'superpoblar', 'superpeublo' )
reg( 'iContar', 'tostar', 'tuesto' )
reg( 'iContar', 'tronar', 'trueno' )
reg( 'iContar', 'volar', 'vuelo' )
reg( 'iDar', 'dar', 'da', 'daba', 'daban', 'dabas', 'darle', 'darse', 'damos', 'dando', 'darles', 'dará', 'darán', 'darás', 'dio', 'dé', 'den', 'diera', 'dieran', 'dieras', 'daría', 'darían', 'darías', 'dimos', 'dándole' )
reg( 'iDecir', 'bendecir', 'bendecirá', 'bendecirán', 'bendecirás' )
reg( 'iDecir', 'decir', 'dice', 'dicen', 'decirse', 'dio', 'dieron', 'di', 'dijo', 'decía', 'decían', 'dirá', 'dirán', 'dirás', 'diciendo', 'diría', 'dirían', 'dirías', 'dijeron', 'decimos', 'dijimos' )
reg( 'iDegollar', 'degollar', 'degolló', 'degollaron' )
reg( 'iDesapegarse', 'aborregarse' )
reg( 'iDesapegarse', 'abotagarse' )
reg( 'iDesapegarse', 'agringarse' )
reg( 'iDesapegarse', 'arrepanchigarse' )
reg( 'iDesapegarse', 'coligarse' )
reg( 'iDesapegarse', 'desapegarse' )
reg( 'iDesapegarse', 'despechugarse' )
reg( 'iDesapegarse', 'desporrondingarse' )
reg( 'iDesapegarse', 'encenagarse' )
reg( 'iDesapegarse', 'endomingarse' )
reg( 'iDesapegarse', 'fugarse' )
reg( 'iDesapegarse', 'repanchigarse' )
reg( 'iDesapegarse', 'repantigarse' )
reg( 'iDistinguir', 'distinguir', 'distingue', 'distinguen', 'distinguió', 'distinguirá', 'distinguirán', 'distinguirás', 'distinguieron', 'distinguirse', 'distinguía', 'distinguían', 'distinguías', 'distinguimos' )
reg( 'iDistinguir', 'extinguir', 'extinguieron', 'extinga', 'extinguen', 'extinguió', 'extinguirá', 'extinguirán', 'extinguirás' )
reg( 'iDormir', 'dormir', 'durmió', 'dormirá', 'dormirán', 'dormirás', 'durmieron', 'dormía', 'dormían', 'dormías', 'dormimos' )
reg( 'iDormir', 'morir', 'morimos', 'murió', 'muere', 'mueren', 'murieron', 'morirá', 'morirán', 'morirás', 'muriera', 'murieran', 'murieras', 'moriría', 'morirían', 'morirías', 'moría', 'morían', 'morías' )
reg( 'iElegir', 'corregir', 'corrija', 'corrigió', 'corregirá', 'corregirán', 'corregirás', 'corrigieron' )
reg( 'iElegir', 'elegir', 'elegido', 'elegida', 'elige', 'eligen', 'elegidos', 'elegidas', 'elija', 'electo', 'eligió', 'elegirá', 'elegirán', 'elegirás', 'eligieron', 'elegiría', 'elegirían', 'elegirías', 'elegimos' )
reg( 'iElegir', 'reelegir', 'reeligió' )
reg( 'iElegir', 'regir', 'rigió', 'regirá', 'regirán', 'regirás', 'rigieron', 'regía', 'regían', 'regías' )
reg( 'iEntender', 'ascender', 'asciendo' )
reg( 'iEntender', 'atender', 'atiendo' )
reg( 'iEntender', 'cerner', 'cierno' )
reg( 'iEntender', 'condescender', 'condesciendo' )
reg( 'iEntender', 'contender', 'contiendo' )
reg( 'iEntender', 'defender', 'defiendo', 'defenderse' )
reg( 'iEntender', 'desatender', 'desatiendo' )
reg( 'iEntender', 'descender', 'desciendo' )
reg( 'iEntender', 'desentender', 'desentiendo', 'desentendió', 'desentenderse' )
reg( 'iEntender', 'distender', 'distiendo' )
reg( 'iEntender', 'encender', 'enciendo' )
reg( 'iEntender', 'entender', 'entiendo', 'entienda', 'entenderse' )
reg( 'iEntender', 'extender', 'extiendo', 'extiende', 'extenderse' )
reg( 'iEntender', 'heder', 'hiedo' )
reg( 'iEntender', 'hender', 'hiendo' )
reg( 'iEntender', 'malentender', 'malentiendo' )
reg( 'iEntender', 'perder', 'pierdo', 'perdiéndose', 'perdiera', 'perdieran', 'perdieras', 'perderse', 'perdimos' )
reg( 'iEntender', 'reverter', 'revierto' )
reg( 'iEntender', 'sobreentender', 'sobreentiendo' )
reg( 'iEntender', 'sobrentender', 'sobrentiendo' )
reg( 'iEntender', 'subtender', 'subtiendo' )
reg( 'iEntender', 'tender', 'tiendo', 'tienden' )
reg( 'iEntender', 'transcender', 'transciendo' )
reg( 'iEntender', 'trascender', 'trasciendo' )
reg( 'iEntender', 'verter', 'vierto' )
reg( 'iErrar', 'errar', 'erró' )
reg( 'iEs' 'dios', 'diosa', 'doisas', 'doises' )
reg( 'iEscocer', 'cocer', 'coció' )
reg( 'iEscocer', 'escocer', 'escoció' )
reg( 'iEscocer', 'recocer', 'recoció' )
reg( 'iEscocer', 'retorcer', 'retorció' )
reg( 'iEscocer', 'torcer', 'torció', 'torcieron' )
reg( 'iEstar', 'estar', 'estando', 'estaba', 'estaban', 'está', 'estén', 'estará', 'estarán', 'estarás', 'estoy', 'están', 'estás', 'esté', 'estaría', 'estarían', 'estarías', 'estuvo', 'estamos', 'estuvieron', 'estuviera', 'estuvieran', 'estuvieras', 'estuvimos' )
reg( 'iForzar', 'esforzar', 'esforzó', 'esforzará', 'esforzarán', 'esforzarás', 'esforzaron', 'esforzarse' )
reg( 'iForzar', 'forzar', 'forzó', 'forzará', 'forzarán', 'forzarás', 'forzaron' )
reg( 'iForzar', 'reforzar', 'reforzaba', 'reforzó', 'reforzará', 'reforzarán', 'reforzarás', 'reforzaron' )
reg( 'iFruncir', 'esparcir', 'esparció', 'esparcieron' )
reg( 'iFruncir', 'fruncir', 'frunció' )
reg( 'iHaber', 'haber', 'ha', 'haberse', 'habiendo', 'habría', 'habrá', 'habrán', 'habrás', 'había', 'habían', 'han', 'haya', 'hayan', 'hay', 'hubo', 'hemos', 'hubiesen', 'hubiera', 'haría', 'hará', 'harán', 'harás', 'habrían', 'habido', 'hubieron', 'hubiese' )
reg( 'iHacer', 'deshacer', 'deshace', 'deshará', 'desharán', 'desharás', 'deshicieron', 'deshacerse' )
reg( 'iHacer', 'hacer', 'hacerse', 'hace', 'hacen', 'hacerlo', 'haciendo', 'haga', 'hagan', 'hacerla', 'haremos', 'haciéndolas', 'haciéndolos', 'hacía', 'hacían', 'hizo', 'hicieron', 'hará', 'harán', 'harás', 'hiciera', 'hicieran', 'hicieras', 'hicimos' )
reg( 'iHacer', 'satisfacer', 'satisfizo', 'satisfará', 'satisfacía', 'satisfacían', 'satisfacías', 'satisficieron' )
reg( 'iHuir', 'afluir' )
reg( 'iHuir', 'atribuir', 'atribuirse' )
reg( 'iHuir', 'concluir' )
reg( 'iHuir', 'confluir' )
reg( 'iHuir', 'constituir', 'constituirse' )
reg( 'iHuir', 'construir', 'construirlo', 'construirse' )
reg( 'iHuir', 'contribuir' )
reg( 'iHuir', 'derruir' )
reg( 'iHuir', 'destituir' )
reg( 'iHuir', 'destruir' )
reg( 'iHuir', 'desvaír' )
reg( 'iHuir', 'diluir' )
reg( 'iHuir', 'disminuir' )
reg( 'iHuir', 'distribuir' )
reg( 'iHuir', 'efluir' )
reg( 'iHuir', 'estatuir' )
reg( 'iHuir', 'excluir' )
reg( 'iHuir', 'fluir' )
reg( 'iHuir', 'gruir' )
reg( 'iHuir', 'huir' )
reg( 'iHuir', 'imbuir' )
reg( 'iHuir', 'incluir', 'incluirse', 'incluiremos' )
reg( 'iHuir', 'influir' )
reg( 'iHuir', 'inmiscuirse' )
reg( 'iHuir', 'instituir' )
reg( 'iHuir', 'instruir' )
reg( 'iHuir', 'intuir' )
reg( 'iHuir', 'obstruir' )
reg( 'iHuir', 'ocluir' )
reg( 'iHuir', 'prostituir' )
reg( 'iHuir', 'recluir' )
reg( 'iHuir', 'reconstituir' )
reg( 'iHuir', 'reconstruir' )
reg( 'iHuir', 'redistribuir' )
reg( 'iHuir', 'refluir' )
reg( 'iHuir', 'restituir' )
reg( 'iHuir', 'retribuir' )
reg( 'iHuir', 'substituir' )
reg( 'iHuir', 'sustituir', 'sustituirla' )
reg( 'iIr', 'ir', 'va', 'vas', 'van', 'irá', 'irán', 'irás', 'vamos', 'vaya', 'voy', 'ido', 'ida', 'idas', 'idos', 'irse', 'iría', 'irían', 'irías', 'fuimos' )
reg( 'iJugar', 'jugar', 'juega', 'juegan', 'jugaban', 'jugaba', 'jugado', 'jugada', 'jugados', 'jugadas', 'jugó', 'jugará', 'jugarán', 'jugarás', 'jugando', 'jugarse', 'jugaría', 'jugarían', 'jugarías', 'jugaron' )
reg( 'iLeer', 'creer', 'creemos', 'creía', 'creías', 'creían', 'creyó', 'creerá', 'creerán', 'creerás', 'creyeron' )
reg( 'iLeer', 'desposeer', 'desposeyó' )
reg( 'iLeer', 'leer', 'leen', 'leyendo', 'leído', 'leerá', 'leerán', 'leerás', 'leerse', 'leía', 'leían', 'leías', 'leyó', 'leyeron' )
reg( 'iLeer', 'poseer', 'posea', 'posee', 'posean', 'poseen', 'poseyó', 'poseía', 'poseías', 'poseían', 'poseerá', 'poseerán', 'poseerás', 'poseyeron' )
reg( 'iLeer', 'proveer', 'provee', 'proveen', 'proveyó', 'proveerá', 'proveerán', 'proveerás', 'proveía', 'proveían', 'proveías', 'proveyeron' )
reg( 'iLeer', 'sobreseer', 'sobreseyó' )
reg( 'iLlegar', 'abogar' )
reg( 'iLlegar', 'abrigar' )
reg( 'iLlegar', 'abrogar' )
reg( 'iLlegar', 'agregar' )
reg( 'iLlegar', 'ahogar' )
reg( 'iLlegar', 'alargar' )
reg( 'iLlegar', 'albergar' )
reg( 'iLlegar', 'alegar' )
reg( 'iLlegar', 'aletargar' )
reg( 'iLlegar', 'allegar' )
reg( 'iLlegar', 'amagar' )
reg( 'iLlegar', 'amargar' )
reg( 'iLlegar', 'amigar' )
reg( 'iLlegar', 'apagar', 'apagarlas' )
reg( 'iLlegar', 'apechugar' )
reg( 'iLlegar', 'apegarse' )
reg( 'iLlegar', 'arengar' )
reg( 'iLlegar', 'arraigar' )
reg( 'iLlegar', 'arremangar' )
reg( 'iLlegar', 'arriesgar' )
reg( 'iLlegar', 'arrogar' )
reg( 'iLlegar', 'arrugar' )
reg( 'iLlegar', 'atosigar' )
reg( 'iLlegar', 'azogar' )
reg( 'iLlegar', 'bogar' )
reg( 'iLlegar', 'bregar' )
reg( 'iLlegar', 'cabalgar' )
reg( 'iLlegar', 'cagar' )
reg( 'iLlegar', 'cargar', 'cargarlas' )
reg( 'iLlegar', 'castigar' )
reg( 'iLlegar', 'catalogar' )
reg( 'iLlegar', 'centrifugar' )
reg( 'iLlegar', 'changar' )
reg( 'iLlegar', 'chingar' )
reg( 'iLlegar', 'circunnavegar' )
reg( 'iLlegar', 'coaligar' )
reg( 'iLlegar', 'comulgar' )
reg( 'iLlegar', 'congregar' )
reg( 'iLlegar', 'conjugar' )
reg( 'iLlegar', 'delegar' )
reg( 'iLlegar', 'derogar' )
reg( 'iLlegar', 'derrengar' )
reg( 'iLlegar', 'desabrigar' )
reg( 'iLlegar', 'desahogar' )
reg( 'iLlegar', 'desarraigar' )
reg( 'iLlegar', 'descabalgar' )
reg( 'iLlegar', 'descargar' )
reg( 'iLlegar', 'descuajaringar' )
reg( 'iLlegar', 'descuajeringar' )
reg( 'iLlegar', 'desembargar' )
reg( 'iLlegar', 'desembragar' )
reg( 'iLlegar', 'desfogar' )
reg( 'iLlegar', 'desguañangar' )
reg( 'iLlegar', 'desligar' )
reg( 'iLlegar', 'desmigar' )
reg( 'iLlegar', 'desnarigar' )
reg( 'iLlegar', 'despegar' )
reg( 'iLlegar', 'desperdigar' )
reg( 'iLlegar', 'desvirgar' )
reg( 'iLlegar', 'devengar' )
reg( 'iLlegar', 'dialogar' )
reg( 'iLlegar', 'diptongar' )
reg( 'iLlegar', 'disgregar' )
reg( 'iLlegar', 'divagar' )
reg( 'iLlegar', 'divulgar' )
reg( 'iLlegar', 'doblegar' )
reg( 'iLlegar', 'dragar' )
reg( 'iLlegar', 'drogar' )
reg( 'iLlegar', 'embargar' )
reg( 'iLlegar', 'embragar' )
reg( 'iLlegar', 'embriagar' )
reg( 'iLlegar', 'empalagar' )
reg( 'iLlegar', 'encabalgar' )
reg( 'iLlegar', 'encargar', 'encargarse' )
reg( 'iLlegar', 'endilgar' )
reg( 'iLlegar', 'endrogarse' )
reg( 'iLlegar', 'enfangar' )
reg( 'iLlegar', 'enjalbegar' )
reg( 'iLlegar', 'enjuagar' )
reg( 'iLlegar', 'enjugar' )
reg( 'iLlegar', 'entregar', 'entregarse' )
reg( 'iLlegar', 'erogar' )
reg( 'iLlegar', 'espigar' )
reg( 'iLlegar', 'espulgar' )
reg( 'iLlegar', 'estomagar' )
reg( 'iLlegar', 'estragar' )
reg( 'iLlegar', 'excomulgar' )
reg( 'iLlegar', 'expurgar' )
reg( 'iLlegar', 'fatigar' )
reg( 'iLlegar', 'fisgar' )
reg( 'iLlegar', 'fumigar' )
reg( 'iLlegar', 'fustigar' )
reg( 'iLlegar', 'halagar' )
reg( 'iLlegar', 'homologar' )
reg( 'iLlegar', 'hostigar' )
reg( 'iLlegar', 'hurgar' )
reg( 'iLlegar', 'indagar' )
reg( 'iLlegar', 'instigar' )
reg( 'iLlegar', 'interrogar' )
reg( 'iLlegar', 'intrigar' )
reg( 'iLlegar', 'investigar' )
reg( 'iLlegar', 'irrigar' )
reg( 'iLlegar', 'irrogar' )
reg( 'iLlegar', 'jalbegar' )
reg( 'iLlegar', 'jeringar' )
reg( 'iLlegar', 'juzgar' )
reg( 'iLlegar', 'largar' )
reg( 'iLlegar', 'legar' )
reg( 'iLlegar', 'ligar' )
reg( 'iLlegar', 'litigar' )
reg( 'iLlegar', 'llegar', 'llegaron' )
reg( 'iLlegar', 'madrugar' )
reg( 'iLlegar', 'mangar' )
reg( 'iLlegar', 'mendigar' )
reg( 'iLlegar', 'merengar' )
reg( 'iLlegar', 'migar' )
reg( 'iLlegar', 'mitigar' )
reg( 'iLlegar', 'monologar' )
reg( 'iLlegar', 'monoptongar' )
reg( 'iLlegar', 'naufragar' )
reg( 'iLlegar', 'navegar' )
reg( 'iLlegar', 'obligar' )
reg( 'iLlegar', 'otorgar' )
reg( 'iLlegar', 'pagar' )
reg( 'iLlegar', 'pegar', 'pegarlo' )
reg( 'iLlegar', 'pingar' )
reg( 'iLlegar', 'plagar' )
reg( 'iLlegar', 'postergar' )
reg( 'iLlegar', 'prejuzgar' )
reg( 'iLlegar', 'pringar' )
reg( 'iLlegar', 'prodigar' )
reg( 'iLlegar', 'prologar' )
reg( 'iLlegar', 'prolongar' )
reg( 'iLlegar', 'promulgar' )
reg( 'iLlegar', 'propagar' )
reg( 'iLlegar', 'prorrogar' )
reg( 'iLlegar', 'purgar' )
reg( 'iLlegar', 'rasgar' )
reg( 'iLlegar', 'recargar' )
reg( 'iLlegar', 'rehogar' )
reg( 'iLlegar', 'relegar' )
reg( 'iLlegar', 'remangar' )
reg( 'iLlegar', 'respingar' )
reg( 'iLlegar', 'rezagar' )
reg( 'iLlegar', 'rezongar' )
reg( 'iLlegar', 'segregar' )
reg( 'iLlegar', 'sesgar' )
reg( 'iLlegar', 'sobrecargar' )
reg( 'iLlegar', 'sojuzgar' )
reg( 'iLlegar', 'subdelegar' )
reg( 'iLlegar', 'subrogar' )
reg( 'iLlegar', 'subyugar' )
reg( 'iLlegar', 'sufragar' )
reg( 'iLlegar', 'tangar' )
reg( 'iLlegar', 'tragar' )
reg( 'iLlegar', 'vagar' )
reg( 'iLlegar', 'vengar', 'vengarse' )
reg( 'iLucir', 'lucir', 'lució', 'lucirá', 'lucirán', 'lucirás', 'lucieron' )
reg( 'iMecer', 'convencer', 'convenció', 'convencerá', 'convencerán', 'convencerás', 'convencieron' )
reg( 'iMecer', 'ejercer', 'ejerció', 'ejercerá', 'ejercerán', 'ejercerás', 'ejercieron', 'ejercía', 'ejercían', 'ejercías', 'ejercería', 'ejercerían', 'ejercerías', 'ejerce' )
reg( 'iMecer', 'vencer', 'venció', 'vencerá', 'vencerán', 'vencerás', 'vencieron', 'vencía', 'vencían', 'vencías', 'vencería', 'vencerían', 'vencerías' )
reg( 'iMenguar', 'apaciguar', 'apaciguó' )
reg( 'iMenguar', 'atestiguar', 'atestigua', 'atestiguas', 'atestiguan', 'atestiguó', 'atestiguaron' )
reg( 'iMenguar', 'averiguar', 'averigua', 'averiguó' )
reg( 'iMenguar', 'fraguar', 'fraguó', 'fraguaron' )
reg( 'iMenguar', 'menguar', 'menguó' )
reg( 'iMover', 'absolver', 'absuelvo', 'absuelto' )
reg( 'iMover', 'autodisolver', 'autodisuelvo', 'autodisuelto' )
reg( 'iMover', 'condoler', 'conduelo', 'condolerse' )
reg( 'iMover', 'conmover', 'conmuevo' )
reg( 'iMover', 'demoler', 'demuelo' )
reg( 'iMover', 'desenvolver', 'desenvuelvo', 'desenvuelto', 'desenvolverse' )
reg( 'iMover', 'devolver', 'devuelvo', 'devuelto' )
reg( 'iMover', 'disolver', 'disuelvo', 'disuelto', 'disolverse' )
reg( 'iMover', 'doler', 'duelo' )
reg( 'iMover', 'envolver', 'envuelvo', 'envuelto' )
reg( 'iMover', 'llover', 'lluevo' )
reg( 'iMover', 'moler', 'muelo' )
reg( 'iMover', 'morder', 'muerdo' )
reg( 'iMover', 'mover', 'muedo', 'moviéndose', 'moverlos', 'moverla', 'moverse', 'mueve' )
reg( 'iMover', 'promover', 'promuevo' )
reg( 'iMover', 'remorder', 'remuevo' )
reg( 'iMover', 'remover', 'remuevo' )
reg( 'iMover', 'resolver', 'resuelvo', 'resolverlo', 'resolverlos', 'resolverse' )
reg( 'iMover', 'revolver', 'resuelvo' )
reg( 'iMover', 'volver', 'vuelvo', 'volvieron', 'volviera', 'volvieran', 'volvieras', 'volverse', 'volvimos' )
reg( 'iNegar', 'anegar', 'anegó' )
reg( 'iNegar', 'cegar', 'cegó', 'cegaron' )
reg( 'iNegar', 'denegar', 'denegó', 'denegaron' )
reg( 'iNegar', 'desplegar', 'desplegó', 'desplegará', 'desplegarán', 'desplegarás', 'desplegaron' )
reg( 'iNegar', 'desplegar', 'despliega', 'despliegan', 'despliegue' )
reg( 'iNegar', 'negar', 'negó', 'negará', 'negarán', 'negarás', 'negarse', 'negaron' )
reg( 'iNegar', 'plegar', 'plegó', 'plegaron' )
reg( 'iNegar', 'renegar', 'renegó', 'renegaron' )
reg( 'iNegar', 'replegar', 'replegó', 'replegarse', 'replegaron' )
reg( 'iOir', 'oir', 'oyó', 'oía', 'oían', 'oías', 'oyeron' )
reg( 'iPartir', 'abatir' )
reg( 'iPartir', 'abrir', 'abro', 'abrirse' )
reg( 'iPartir', 'aburrir', 'aburrió' )
reg( 'iPartir', 'acudir' )
reg( 'iPartir', 'admitir', 'admitieron' )
reg( 'iPartir', 'adscribir' )
reg( 'iPartir', 'aludir' )
reg( 'iPartir', 'apercibir' )
reg( 'iPartir', 'aplaudir' )
reg( 'iPartir', 'asistir' )
reg( 'iPartir', 'asumir' )
reg( 'iPartir', 'aturdir' )
reg( 'iPartir', 'añadir', 'añadirlas', 'añadirle', 'añadirse', 'añadirlo' )
reg( 'iPartir', 'batir' )
reg( 'iPartir', 'circunscribir' )
reg( 'iPartir', 'coescribir' )
reg( 'iPartir', 'coexistir' )
reg( 'iPartir', 'coincidir', 'coincidieron' )
reg( 'iPartir', 'combatir' )
reg( 'iPartir', 'compartir' )
reg( 'iPartir', 'concurrir' )
reg( 'iPartir', 'confundir', 'confundido', 'confundirse' )
reg( 'iPartir', 'consistir' )
reg( 'iPartir', 'consumir' )
reg( 'iPartir', 'convivir' )
reg( 'iPartir', 'cubrir', 'cubierto', 'cubiertos', 'cubierta', 'cubiertas', 'cubrirse' )
reg( 'iPartir', 'cumplir', 'cumplirse' )
reg( 'iPartir', 'cundir' )
reg( 'iPartir', 'debatir' )
reg( 'iPartir', 'decidir', 'decidieron', 'decidirse' )
reg( 'iPartir', 'definir', 'definirse', 'definiremos', 'definieron' )
reg( 'iPartir', 'describir', 'describirlo', 'descrita', 'descritas', 'descrito', 'descritos', 'describirse' )
reg( 'iPartir', 'descubrir', 'descubierto', 'descubiertos', 'descubierta', 'descubiertas', 'descubrirse' )
reg( 'iPartir', 'desistir' )
reg( 'iPartir', 'difundir' )
reg( 'iPartir', 'dimitir' )
reg( 'iPartir', 'dirimir' )
reg( 'iPartir', 'discurrir' )
reg( 'iPartir', 'discutir', 'discutieron' )
reg( 'iPartir', 'disuadir' )
reg( 'iPartir', 'dividir', 'divididas', 'dividirse' )
reg( 'iPartir', 'eludir' )
reg( 'iPartir', 'emitir', 'emitirse' )
reg( 'iPartir', 'encubrir' )
reg( 'iPartir', 'escindir' )
reg( 'iPartir', 'escribir', 'escribiera', 'escrita', 'escrito', 'escritas', 'escritos', 'escribirse' )
reg( 'iPartir', 'esculpir' )
reg( 'iPartir', 'escupir' )
reg( 'iPartir', 'esgrimir' )
reg( 'iPartir', 'evadir' )
reg( 'iPartir', 'exhibir' )
reg( 'iPartir', 'eximir' )
reg( 'iPartir', 'existir' )
reg( 'iPartir', 'expandir', 'expandirse' )
reg( 'iPartir', 'fundir' )
reg( 'iPartir', 'hundir', 'hundió', 'hundirse' )
reg( 'iPartir', 'impartir' )
reg( 'iPartir', 'imprimir', 'imprimirlo', 'imprimirlas' )
reg( 'iPartir', 'incidir' )
reg( 'iPartir', 'incumplir' )
reg( 'iPartir', 'incurrir' )
reg( 'iPartir', 'infundir' )
reg( 'iPartir', 'inhibir' )
reg( 'iPartir', 'inscribir', 'inscrita', 'inscrito', 'inscritas', 'inscritos', 'inscribirse' )
reg( 'iPartir', 'insistir' )
reg( 'iPartir', 'interrumpir', 'interrumpirse' )
reg( 'iPartir', 'invadir' )
reg( 'iPartir', 'irrumpir' )
reg( 'iPartir', 'nutrir' )
reg( 'iPartir', 'ocurrir' )
reg( 'iPartir', 'omitir', 'omitirse' )
reg( 'iPartir', 'parir' )
reg( 'iPartir', 'partir' )
reg( 'iPartir', 'percibir' )
reg( 'iPartir', 'permitir', 'permitirle', 'permitirán', 'permitieron', 'permitiera', 'permitieran', 'permitieras', 'permitirse' )
reg( 'iPartir', 'persistir' )
reg( 'iPartir', 'persuadir' )
reg( 'iPartir', 'pervivir' )
reg( 'iPartir', 'predefinir', 'predefinida' )
reg( 'iPartir', 'prescindir' )
reg( 'iPartir', 'prescribir' )
reg( 'iPartir', 'presidir' )
reg( 'iPartir', 'presumir' )
reg( 'iPartir', 'proscribir' )
reg( 'iPartir', 'pulir' )
reg( 'iPartir', 'reabrir' )
reg( 'iPartir', 'reasumir' )
reg( 'iPartir', 'rebatir' )
reg( 'iPartir', 'recibir' )
reg( 'iPartir', 'recubrir' )
reg( 'iPartir', 'recurrir' )
reg( 'iPartir', 'redefinir' )
reg( 'iPartir', 'redescubrir' )
reg( 'iPartir', 'redimir' )
reg( 'iPartir', 'reescribir' )
reg( 'iPartir', 'reimprimir' )
reg( 'iPartir', 'reincidir' )
reg( 'iPartir', 'remitir' )
reg( 'iPartir', 'repartir' )
reg( 'iPartir', 'repercutir' )
reg( 'iPartir', 'reprimir' )
reg( 'iPartir', 'rescindir' )
reg( 'iPartir', 'residir' )
reg( 'iPartir', 'resistir' )
reg( 'iPartir', 'resumir' )
reg( 'iPartir', 'retransmitir' )
reg( 'iPartir', 'revivir' )
reg( 'iPartir', 'sacudir' )
reg( 'iPartir', 'sobrevivir', 'sobrevinieron' )
reg( 'iPartir', 'subdividir' )
reg( 'iPartir', 'subir', 'subirla', 'subiéndolo', 'subirse' )
reg( 'iPartir', 'subsistir' )
reg( 'iPartir', 'sucumbir' )
reg( 'iPartir', 'sufrir' )
reg( 'iPartir', 'sumir' )
reg( 'iPartir', 'suplir' )
reg( 'iPartir', 'suprimir' )
reg( 'iPartir', 'surtir' )
reg( 'iPartir', 'suscribir', 'suscribieron' )
reg( 'iPartir', 'transcribir' )
reg( 'iPartir', 'transcurrir' )
reg( 'iPartir', 'transmitir', 'transmitirse' )
reg( 'iPartir', 'trascurrir' )
reg( 'iPartir', 'trasmitir' )
reg( 'iPartir', 'unir', 'unirse' )
reg( 'iPartir', 'urdir' )
reg( 'iPartir', 'vivir' )
reg( 'iPedir', 'acomedir', 'acomidiendo', 'acomedirse' )
reg( 'iPedir', 'comedir', 'comidiendo', 'comedirse' )
reg( 'iPedir', 'competir', 'compitiendo' )
reg( 'iPedir', 'concebir', 'concibiendo')
reg( 'iPedir', 'derretir', 'derritiendo' )
reg( 'iPedir', 'desmedir', 'desmidiendo', 'desmedirse' )
reg( 'iPedir', 'despedir', 'despidiendo', 'despedirse' )
reg( 'iPedir', 'desvestir', 'desvistiendo' )
reg( 'iPedir', 'embestir', 'embistiendo' )
reg( 'iPedir', 'expedir', 'expidiendo' )
reg( 'iPedir', 'gemir', 'gimiendo' )
reg( 'iPedir', 'henchir', 'hinchiendo' )
reg( 'iPedir', 'impedir', 'impidiendo')
reg( 'iPedir', 'investir', 'invistiendo' )
reg( 'iPedir', 'medir', 'midiendo', 'medirse' )
reg( 'iPedir', 'pedir', 'pidiendo' )
reg( 'iPedir', 'preconcebir', 'preconcibiendo' )
reg( 'iPedir', 'rendir', 'rindiendo', 'rendirse' )
reg( 'iPedir', 'repetir', 'repitiendo', 'repetirse' )
reg( 'iPedir', 'revestir', 'revistiendo' )
reg( 'iPedir', 'servir', 'sirviendo', 'servirle', 'servirse' )
reg( 'iPedir', 'travestir', 'travistiendo' )
reg( 'iPedir', 'vestir', 'vistiendo', 'vestirse' )
reg( 'iPlacer', 'complacer', 'complació' )
reg( 'iPlacer', 'placer', 'plació' )
reg( 'iPoder', 'poder', 'pudo', 'podía', 'podemos', 'podrá', 'podrán', 'podrás', 'podría', 'podrían', 'pude', 'pudiera', 'pudieran', 'pudiese', 'pueda', 'puedan', 'puedas', 'puede', 'pueden', 'puedes', 'pudiendo', 'podido', 'podríamos', 'pudieron', 'podían', 'podía', 'puedo', 'poderse' )
reg( 'iPoner', 'poner', 'pone', 'pones', 'ponen', 'poniendo', 'puesta', 'poniéndolas', 'puso', 'pondrá', 'pondrán', 'pondrás', 'pusieron', 'pusiera', 'pusieran', 'pusieras', 'ponía', 'ponían', 'ponías', 'pondría', 'pondrían', 'pondrías', 'pusimos', 'ponerse' )
reg( 'iPredecir', 'contradecir', 'contradecía', 'contradecían', 'contradecías', 'contradice', 'contradices', 'contradicen', 'contradijeron' )
reg( 'iPredecir', 'predecir', 'predijo', 'predijeron' )
reg( 'iPrevenir' 'devenir', 'devendrá', 'devendrán', 'devendrás', 'devinieron' )
reg( 'iPrevenir', 'convenir', 'conviene', 'convendrá', 'convendrán', 'convendrás', 'convinieron', 'convenía', 'convenían', 'convenías' )
reg( 'iPrevenir', 'intervenir', 'intervienen', 'interviniendo', 'intervenidos', 'intervengan', 'intervendrá', 'intervendrán', 'intervendrás', 'intervinieron', 'intervenía', 'intervenían', 'intervenías', 'intervendría', 'intervendrían', 'intervendrías', 'intervino' )
reg( 'iPrevenir', 'prevenir', 'previno', 'prevendrá', 'prevendrán', 'prevendrás', 'previnieron' )
reg( 'iPrevenir', 'provenir', 'provendrá', 'provendrás', 'provendrán', 'proviene', 'provienen', 'provino', 'provinieron', 'provenía', 'provenían', 'provenías', 'provendría', 'provendrían', 'provendrías' )
reg( 'iPrever', 'prever', 'previó', 'preveía', 'preveían', 'preveías', 'previeron' )
reg( 'iQuerer', 'querer', 'quería', 'querían', 'querías', 'quiera', 'quieran', 'quiere', 'quieres', 'quieren', 'queremos', 'queriendo', 'querida', 'queridas', 'querido', 'queridos', 'querrá', 'querrán', 'querrás', 'quisieron', 'quiero', 'quiso', 'quisiera', 'quisieran', 'quisieras', 'querría', 'querrían', 'querrías', 'quisimos' )
reg( 'iRehacer', 'rehacer', 'rehicieron' )
reg( 'iReir', 'freír', 'frió' )
reg( 'iReir', 'reír', 'rió', 'rieron', 'reía', 'reían', 'reías' )
reg( 'iReir', 'sonreír', 'sonrió' )
reg( 'iReponer', 'anteponer' )
reg( 'iReponer', 'aponer' )
reg( 'iReponer', 'componer' )
reg( 'iReponer', 'contraponer' )
reg( 'iReponer', 'deponer' )
reg( 'iReponer', 'descomponer' )
reg( 'iReponer', 'disponer' )
reg( 'iReponer', 'exponer' )
reg( 'iReponer', 'imponer', 'imponerse' )
reg( 'iReponer', 'indisponer' )
reg( 'iReponer', 'interponer' )
reg( 'iReponer', 'oponer', 'oponerse' )
reg( 'iReponer', 'posponer' )
reg( 'iReponer', 'predisponer' )
reg( 'iReponer', 'presuponer' )
reg( 'iReponer', 'proponer', 'propusieron', 'propusimos' )
reg( 'iReponer', 'recomponer' )
reg( 'iReponer', 'reponer' )
reg( 'iReponer', 'sobreponer' )
reg( 'iReponer', 'superponer' )
reg( 'iReponer', 'suponer', 'supongamos' )
reg( 'iReponer', 'transponer' )
reg( 'iReponer', 'trasponer' )
reg( 'iReponer', 'yuxtaponer' )
reg( 'iResolver', 'resolver', 'resolvió' )
reg( 'iRetener', 'abstener', 'abstendrá', 'abstendrán', 'abstendrás', 'abstuvieron', 'abstenerse' )
reg( 'iRetener', 'contener', 'contenía', 'contenías', 'contenían', 'contiene', 'contienen', 'contengan', 'contenga', 'contendrá', 'contendrán', 'contendrás', 'contuvieron' )
reg( 'iRetener', 'detener', 'detenerse', 'detiene', 'deteniéndose', 'detendrá', 'detendrán', 'detendrás', 'detuvieron', 'detenía', 'detenían', 'detenías', 'detuvimos', 'detenido', 'detenida', 'detenidos', 'detenidas', 'detuvo' )
reg( 'iRetener', 'mantener', 'mantenga', 'mantendrá', 'mantendrán', 'mantendrás', 'mantengan', 'mantenían', 'mantuvo', 'mantiene', 'mantienen', 'mantienes', 'mantuvieron', 'manteniendo', 'mantuviera', 'mantuvieran', 'mantuvieras', 'mantenerse', 'mantenía', 'mantenían', 'mantenías', 'mantendría', 'mantendrían', 'mantendrías', 'mantuvimos' )
reg( 'iRetener', 'obtener', 'obtiene', 'obtienen', 'obtenido', 'obtenidos', 'obtenida', 'obtenidas', 'obtenerse', 'obtuvo', 'obteniendo', 'obtendrá', 'obtendrán', 'obtendrás', 'obtuvieron', 'obtuviera', 'obtuvieran', 'obtuvieras', 'obtenía', 'obtenían', 'obtenías', 'obtendría', 'obtendrían', 'obtendrías', 'contendría', 'contendrían', 'contendrías', 'obtuvimos' )
reg( 'iRetener', 'retener', 'retendrá', 'retendrán', 'retendrás', 'retuvieron', 'retenía', 'retenían', 'retenías' )
reg( 'iRetener', 'sostener', 'sostiene', 'sostendrá', 'sostendrán', 'sostendrás', 'sostuvieron', 'sostenerse', 'sostenía', 'sostenían', 'sostenías' )
reg( 'iReunir', 'reunir', 'reunirse', 'reunió', 'reunirá', 'reunirán', 'reunirás', 'reunieron', 'reúne', 'reúnes', 'reúnen', 'reúna', 'reúnas', 'reúnan', 'reunía', 'reunían', 'reunías', 'reuniría', 'reunirían', 'reunirías', 'reunimos' )
reg( 'iReñir', 'ceñir', 'ciñó' )
reg( 'iReñir', 'teñir', 'tiñó', 'tiñeron' )
reg( 'iRogar', 'colgar', 'colgó', 'colgará', 'colgarán', 'colgarás', 'colgaron' )
reg( 'iRogar', 'descolgar', 'descolgó' )
reg( 'iRogar', 'rogar', 'rogó', 'rogaron' )
reg( 'iRugir', 'codirigir', 'codirigió' )
reg( 'iRugir', 'convergir', 'convergen' )
reg( 'iRugir', 'dirigir', 'dirigió', 'dirige', 'dirigen', 'dirigirá', 'dirigirán', 'dirigirás', 'dirigieron', 'dirigirse', 'dirigía', 'dirigían', 'dirigías', 'dirigiría', 'dirigirían', 'dirigirías', 'dirigimos' )
reg( 'iRugir', 'divergir', 'diverge', 'divergen', 'divergido', 'divergieron', 'divergió' )
reg( 'iRugir', 'erigir', 'erigirá', 'erigirán', 'erigirás', 'erigía', 'erigían', 'erigías', 'erigió', 'erigieron' )
reg( 'iRugir', 'exigir', 'exigen', 'exigió', 'exigirá', 'exigirán', 'exigirás', 'exigieron', 'exigió', 'exigía', 'exigían', 'exigías', 'exigimos' )
reg( 'iRugir', 'fingir', 'fingió', 'fingirá', 'fingirán', 'fingirás', 'fingieron' )
reg( 'iRugir', 'fungir', 'fungirá', 'fungirán', 'fungirás', 'fungieron', 'fungía', 'fungían', 'fungías' )
reg( 'iRugir', 'fungir', 'fungió', 'fungirá', 'fungirán', 'fungirás' )
reg( 'iRugir', 'infligir', 'infligió', 'infligieron' )
reg( 'iRugir', 'infringir', 'infringieron' )
reg( 'iRugir', 'redirigir', 'redirigirlos', 'redirigió', 'redirigirá', 'redirigirán', 'redirigirás' )
reg( 'iRugir', 'restringir', 'restringe', 'restringen', 'restringes', 'restringirá', 'restringirán', 'restringirás', 'restringieron', 'restringió', 'restringía', 'restringían', 'restringías' )
reg( 'iRugir', 'resurgir', 'resurgió', 'resurgirá', 'resurgirán', 'resurgirás', 'resurgieron' )
reg( 'iRugir', 'sumergir', 'sumergió', 'sumergirá', 'sumergirán', 'sumergirás', 'sumergieron', 'sumergirse' )
reg( 'iRugir', 'surgir', 'surge', 'surgen', 'surgieron', 'surgirían', 'surgió', 'surgido', 'surgirá', 'surgirán', 'surgirás', 'surgiría', 'surgirían', 'surgirías', 'surgía', 'surgían', 'surgías' )
reg( 'iRugir', 'ungir', 'ungió' )
reg( 'iRugir', 'urgir', 'urgió', 'urgieron' )
reg( 'iSaber', 'saber', 'sé', 'sabe', 'sabía', 'sabían', 'sabías', 'saben', 'sabemos', 'sepamos', 'sepa', 'sabrá', 'sabrán', 'sabrás', 'supieron', 'supiera', 'supieran', 'supieras', 'saberse', 'sabría', 'sabrían', 'sabrías', 'supimos', 'supo' )
reg( 'iSacar', 'abanicar' )
reg( 'iSacar', 'abarcar' )
reg( 'iSacar', 'abarrancar' )
reg( 'iSacar', 'abdicar' )
reg( 'iSacar', 'abocar' )
reg( 'iSacar', 'abroncar' )
reg( 'iSacar', 'acercar', 'acercarlo', 'acercarla', 'acercarse' )
reg( 'iSacar', 'achacar' )
reg( 'iSacar', 'achicar' )
reg( 'iSacar', 'acidificar' )
reg( 'iSacar', 'adjudicar' )
reg( 'iSacar', 'afincar' )
reg( 'iSacar', 'ahorcar' )
reg( 'iSacar', 'ahuecar' )
reg( 'iSacar', 'alambicar' )
reg( 'iSacar', 'altercar' )
reg( 'iSacar', 'amplificar' )
reg( 'iSacar', 'apalancar' )
reg( 'iSacar', 'aparcar' )
reg( 'iSacar', 'apencar' )
reg( 'iSacar', 'aplacar' )
reg( 'iSacar', 'aplicar', 'aplicarle', 'aplicarse', 'aplicarlas', 'aplicarles', 'aplicarlo', 'aplicándoles', 'aplíquele' )
reg( 'iSacar', 'apocar' )
reg( 'iSacar', 'arrancar' )
reg( 'iSacar', 'arrascar' )
reg( 'iSacar', 'atacar', 'atacarla' )
reg( 'iSacar', 'atascar' )
reg( 'iSacar', 'atracar' )
reg( 'iSacar', 'atrancar' )
reg( 'iSacar', 'atrincar' )
reg( 'iSacar', 'autenticar' )
reg( 'iSacar', 'autentificar' )
reg( 'iSacar', 'avocar' )
reg( 'iSacar', 'bancar' )
reg( 'iSacar', 'beatificar' )
reg( 'iSacar', 'becar' )
reg( 'iSacar', 'bisecar' )
reg( 'iSacar', 'blocar' )
reg( 'iSacar', 'bonificar' )
reg( 'iSacar', 'brincar' )
reg( 'iSacar', 'buscar', 'buscándolo', 'buscarse' )
reg( 'iSacar', 'caducar' )
reg( 'iSacar', 'calcar' )
reg( 'iSacar', 'calcificar' )
reg( 'iSacar', 'calificar' )
reg( 'iSacar', 'capiscar' )
reg( 'iSacar', 'cascar' )
reg( 'iSacar', 'centuplicar' )
reg( 'iSacar', 'cercar' )
reg( 'iSacar', 'certificar' )
reg( 'iSacar', 'chamuscar' )
reg( 'iSacar', 'chancar' )
reg( 'iSacar', 'chascar' )
reg( 'iSacar', 'chocar' )
reg( 'iSacar', 'churruscar' )
reg( 'iSacar', 'ciscar' )
reg( 'iSacar', 'clarificar' )
reg( 'iSacar', 'clasificar', 'clasificaron', 'clasificarse' )
reg( 'iSacar', 'claudicar' )
reg( 'iSacar', 'codificar', 'codificante' )
reg( 'iSacar', 'colocar', 'colocarlas', 'colocarlo', 'colóquelo', 'colocarse' )
reg( 'iSacar', 'complicar' )
reg( 'iSacar', 'comunicar', 'comunicarse' )
reg( 'iSacar', 'conculcar' )
reg( 'iSacar', 'confiscar' )
reg( 'iSacar', 'contraatacar' )
reg( 'iSacar', 'contraindicar' )
reg( 'iSacar', 'convocar' )
reg( 'iSacar', 'cosificar' )
reg( 'iSacar', 'criticar' )
reg( 'iSacar', 'crucificar' )
reg( 'iSacar', 'cuadriplicar' )
reg( 'iSacar', 'cuadruplicar' )
reg( 'iSacar', 'cualificar' )
reg( 'iSacar', 'cuantificar' )
reg( 'iSacar', 'cubicar' )
reg( 'iSacar', 'damnificar' )
reg( 'iSacar', 'decalcificar' )
reg( 'iSacar', 'decodificar' )
reg( 'iSacar', 'decorticar' )
reg( 'iSacar', 'dedicar', 'dedicarse' )
reg( 'iSacar', 'defecar' )
reg( 'iSacar', 'deificar' )
reg( 'iSacar', 'demarcar' )
reg( 'iSacar', 'densificar' )
reg( 'iSacar', 'deprecar' )
reg( 'iSacar', 'derrocar' )
reg( 'iSacar', 'desacidificar' )
reg( 'iSacar', 'desaparcar' )
reg( 'iSacar', 'desaplicar' )
reg( 'iSacar', 'desatancar' )
reg( 'iSacar', 'desatascar' )
reg( 'iSacar', 'desatrancar' )
reg( 'iSacar', 'desbancar' )
reg( 'iSacar', 'desbarrancar' )
reg( 'iSacar', 'desbocar' )
reg( 'iSacar', 'descalcificar' )
reg( 'iSacar', 'descalificar' )
reg( 'iSacar', 'desclasificar' )
reg( 'iSacar', 'descodificar' )
reg( 'iSacar', 'descolocar' )
reg( 'iSacar', 'desconvocar' )
reg( 'iSacar', 'desecar' )
reg( 'iSacar', 'desembarcar' )
reg( 'iSacar', 'desembocar' )
reg( 'iSacar', 'desempacar', 'desempáquela' )
reg( 'iSacar', 'desenfocar' )
reg( 'iSacar', 'desenroscar' )
reg( 'iSacar', 'desertificar' )
reg( 'iSacar', 'desfalcar' )
reg( 'iSacar', 'desintoxicar' )
reg( 'iSacar', 'desmarcar' )
reg( 'iSacar', 'desmitificar' )
reg( 'iSacar', 'desnucar' )
reg( 'iSacar', 'despelucar' )
reg( 'iSacar', 'despotricar' )
reg( 'iSacar', 'destacar', 'destacarse' )
reg( 'iSacar', 'desubicar' )
reg( 'iSacar', 'diagnosticar' )
reg( 'iSacar', 'dignificar' )
reg( 'iSacar', 'discar' )
reg( 'iSacar', 'disecar' )
reg( 'iSacar', 'dislocar' )
reg( 'iSacar', 'diversificar' )
reg( 'iSacar', 'domesticar' )
reg( 'iSacar', 'dosificar' )
reg( 'iSacar', 'dulcificar' )
reg( 'iSacar', 'duplicar', 'duplicarlos' )
reg( 'iSacar', 'edificar' )
reg( 'iSacar', 'educar' )
reg( 'iSacar', 'ejemplificar' )
reg( 'iSacar', 'electrificar' )
reg( 'iSacar', 'embarcar', 'embarcarse' )
reg( 'iSacar', 'embarrancar' )
reg( 'iSacar', 'embaucar' )
reg( 'iSacar', 'embelecar' )
reg( 'iSacar', 'embocar' )
reg( 'iSacar', 'emboscar' )
reg( 'iSacar', 'embrocar' )
reg( 'iSacar', 'empacar' )
reg( 'iSacar', 'enarcar' )
reg( 'iSacar', 'encharcar' )
reg( 'iSacar', 'enfocar', 'enfocarse' )
reg( 'iSacar', 'enfoscar' )
reg( 'iSacar', 'enmarcar' )
reg( 'iSacar', 'enrocar' )
reg( 'iSacar', 'enroscar' )
reg( 'iSacar', 'entrechocar' )
reg( 'iSacar', 'entresacar' )
reg( 'iSacar', 'entroncar' )
reg( 'iSacar', 'equivocar' )
reg( 'iSacar', 'erradicar' )
reg( 'iSacar', 'escarificar' )
reg( 'iSacar', 'escenificar' )
reg( 'iSacar', 'especificar' )
reg( 'iSacar', 'estancar' )
reg( 'iSacar', 'estatificar' )
reg( 'iSacar', 'estratificar' )
reg( 'iSacar', 'estucar' )
reg( 'iSacar', 'evocar' )
reg( 'iSacar', 'explicar', 'explicarse' )
reg( 'iSacar', 'fabricar', 'fabricarse' )
reg( 'iSacar', 'falsificar' )
reg( 'iSacar', 'fornicar' )
reg( 'iSacar', 'fortificar' )
reg( 'iSacar', 'fructificar' )
reg( 'iSacar', 'gasificar' )
reg( 'iSacar', 'glorificar' )
reg( 'iSacar', 'gratificar' )
reg( 'iSacar', 'hamacar' )
reg( 'iSacar', 'hincar' )
reg( 'iSacar', 'hipotecar' )
reg( 'iSacar', 'hocicar' )
reg( 'iSacar', 'humidificar' )
reg( 'iSacar', 'identificar', 'identificarlo' )
reg( 'iSacar', 'imbricar' )
reg( 'iSacar', 'implicar', 'implicara', 'implicaría' )
reg( 'iSacar', 'imprecar' )
reg( 'iSacar', 'impurificar' )
reg( 'iSacar', 'incomunicar' )
reg( 'iSacar', 'inculcar' )
reg( 'iSacar', 'indicar', 'indicarles', 'indicándole', 'indicaría' )
reg( 'iSacar', 'intensificar' )
reg( 'iSacar', 'intercomunicar' )
reg( 'iSacar', 'intoxicar' )
reg( 'iSacar', 'intrincar' )
reg( 'iSacar', 'invocar' )
reg( 'iSacar', 'justificar' )
reg( 'iSacar', 'lacar' )
reg( 'iSacar', 'lenificar' )
reg( 'iSacar', 'lentificar' )
reg( 'iSacar', 'lignificar' )
reg( 'iSacar', 'lubricar' )
reg( 'iSacar', 'lubrificar' )
reg( 'iSacar', 'machacar' )
reg( 'iSacar', 'machucar' )
reg( 'iSacar', 'magnificar' )
reg( 'iSacar', 'maleducar' )
reg( 'iSacar', 'mancar' )
reg( 'iSacar', 'manducar' )
reg( 'iSacar', 'marcar' )
reg( 'iSacar', 'mariscar' )
reg( 'iSacar', 'mascar' )
reg( 'iSacar', 'masificar' )
reg( 'iSacar', 'masticar' )
reg( 'iSacar', 'medicar' )
reg( 'iSacar', 'mercar' )
reg( 'iSacar', 'mistificar' )
reg( 'iSacar', 'mitificar' )
reg( 'iSacar', 'mixtificar' )
reg( 'iSacar', 'modificar', 'modificarla', 'modificarse' )
reg( 'iSacar', 'molificar' )
reg( 'iSacar', 'momificar' )
reg( 'iSacar', 'mortificar' )
reg( 'iSacar', 'multiplicar' )
reg( 'iSacar', 'musicar' )
reg( 'iSacar', 'neviscar' )
reg( 'iSacar', 'nidificar' )
reg( 'iSacar', 'notificar' )
reg( 'iSacar', 'obcecar' )
reg( 'iSacar', 'ofuscar' )
reg( 'iSacar', 'oliscar' )
reg( 'iSacar', 'opacar' )
reg( 'iSacar', 'pacificar' )
reg( 'iSacar', 'panificar' )
reg( 'iSacar', 'pecar' )
reg( 'iSacar', 'pellizcar' )
reg( 'iSacar', 'pencar' )
reg( 'iSacar', 'perjudicar' )
reg( 'iSacar', 'personificar' )
reg( 'iSacar', 'pescar' )
reg( 'iSacar', 'petrificar' )
reg( 'iSacar', 'picar' )
reg( 'iSacar', 'pizcar' )
reg( 'iSacar', 'placar' )
reg( 'iSacar', 'planificar' )
reg( 'iSacar', 'plantificar' )
reg( 'iSacar', 'plastificar' )
reg( 'iSacar', 'platicar' )
reg( 'iSacar', 'pontificar' )
reg( 'iSacar', 'practicar' )
reg( 'iSacar', 'predicar' )
reg( 'iSacar', 'prefabricar' )
reg( 'iSacar', 'prevaricar' )
reg( 'iSacar', 'pronosticar' )
reg( 'iSacar', 'prosificar' )
reg( 'iSacar', 'provocar', 'provocaría' )
reg( 'iSacar', 'publicar', 'publicaron', 'publicara', 'publicarse' )
reg( 'iSacar', 'purificar' )
reg( 'iSacar', 'quintuplicar' )
reg( 'iSacar', 'radicar', 'radicarse' )
reg( 'iSacar', 'rarificar' )
reg( 'iSacar', 'rascar' )
reg( 'iSacar', 'ratificar' )
reg( 'iSacar', 'rebuscar' )
reg( 'iSacar', 'recalcar' )
reg( 'iSacar', 'recalificar' )
reg( 'iSacar', 'reclasificar', 'reclasificó' )
reg( 'iSacar', 'recolocar' )
reg( 'iSacar', 'rectificar' )
reg( 'iSacar', 'reduplicar' )
reg( 'iSacar', 'reedificar' )
reg( 'iSacar', 'reeducar' )
reg( 'iSacar', 'reembarcar' )
reg( 'iSacar', 'refrescar' )
reg( 'iSacar', 'reivindicar' )
reg( 'iSacar', 'remarcar' )
reg( 'iSacar', 'remolcar' )
reg( 'iSacar', 'repescar' )
reg( 'iSacar', 'repicar' )
reg( 'iSacar', 'replicar' )
reg( 'iSacar', 'resecar' )
reg( 'iSacar', 'retocar' )
reg( 'iSacar', 'retrucar' )
reg( 'iSacar', 'reubicar', 'reubicarlo' )
reg( 'iSacar', 'reunificar' )
reg( 'iSacar', 'revindicar' )
reg( 'iSacar', 'revivificar' )
reg( 'iSacar', 'revocar' )
reg( 'iSacar', 'roncar' )
reg( 'iSacar', 'rubricar' )
reg( 'iSacar', 'sacar' )
reg( 'iSacar', 'sacarificar' )
reg( 'iSacar', 'sacrificar' )
reg( 'iSacar', 'salificar' )
reg( 'iSacar', 'salpicar' )
reg( 'iSacar', 'santificar' )
reg( 'iSacar', 'saponificar' )
reg( 'iSacar', 'secar' )
reg( 'iSacar', 'septuplicar' )
reg( 'iSacar', 'sextuplicar' )
reg( 'iSacar', 'significar', 'significaría' )
reg( 'iSacar', 'simplificar' )
reg( 'iSacar', 'sindicar' )
reg( 'iSacar', 'sofisticar' )
reg( 'iSacar', 'sofocar' )
reg( 'iSacar', 'solidificar' )
reg( 'iSacar', 'sonsacar' )
reg( 'iSacar', 'suplicar' )
reg( 'iSacar', 'surcar' )
reg( 'iSacar', 'tabicar' )
reg( 'iSacar', 'tecnificar' )
reg( 'iSacar', 'testificar' )
reg( 'iSacar', 'tipificar' )
reg( 'iSacar', 'tocar' )
reg( 'iSacar', 'tonificar' )
reg( 'iSacar', 'trabucar' )
reg( 'iSacar', 'traficar' )
reg( 'iSacar', 'trincar' )
reg( 'iSacar', 'triplicar' )
reg( 'iSacar', 'triscar' )
reg( 'iSacar', 'trompicar' )
reg( 'iSacar', 'trucar' )
reg( 'iSacar', 'truncar' )
reg( 'iSacar', 'ubicar', 'ubicado', 'ubicarla', 'ubique', 'ubicarse', 'ubicarlos' )
reg( 'iSacar', 'unificar' )
reg( 'iSacar', 'vacar' )
reg( 'iSacar', 'ventiscar' )
reg( 'iSacar', 'verificar' )
reg( 'iSacar', 'versificar' )
reg( 'iSacar', 'vindicar' )
reg( 'iSacar', 'vitrificar' )
reg( 'iSacar', 'vivificar' )
reg( 'iSacarse', 'aborrascarse' )
reg( 'iSacarse', 'acurrucarse' )
reg( 'iSacarse', 'amoscarse' )
reg( 'iSacarse', 'bifurcarse' )
reg( 'iSacarse', 'bilocarse' )
reg( 'iSacarse', 'coscarse' )
reg( 'iSacarse', 'descocarse' )
reg( 'iSacarse', 'embancarse' )
reg( 'iSacarse', 'emborrascarse' )
reg( 'iSacarse', 'embroncarse' )
reg( 'iSacarse', 'empacarse' )
reg( 'iSacarse', 'empericarse' )
reg( 'iSacarse', 'enamoricarse' )
reg( 'iSacarse', 'enfrascarse' )
reg( 'iSacarse', 'esparrancarse' )
reg( 'iSacarse', 'identificarse', 'identificándose' )
reg( 'iSacarse', 'macarse' )
reg( 'iSacarse', 'osificarse' )
reg( 'iSacarse', 'ramificarse' )
reg( 'iSacarse', 'suberificarse' )
reg( 'iSalir', 'salir', 'salgo', 'saldré', 'saldrá', 'saldrás', 'saldrán', 'salió', 'salieron', 'sale', 'salen', 'sales', 'saliera', 'salieran', 'salieras', 'salirse', 'salía', 'salían', 'salías', 'saldría', 'saldrían', 'saldrías', 'salimos', 'saliendo' )
reg( 'iSalir', 'sobresalir', 'sobresalió', 'sobresalieron', 'sobresalía', 'sobresalían', 'sobresalías' )
reg( 'iSeguir', 'conseguir', 'conseguirse', 'conseguiría', 'conseguirían', 'conseguirías', 'consigue', 'conseguirlo', 'conseguimos' )
reg( 'iSeguir', 'perseguir', 'persigue', 'perseguimos' )
reg( 'iSeguir', 'proseguir' )
reg( 'iSeguir', 'seguir', 'seguiría', 'seguirán' )
reg( 'iSeguir', 'subseguir' )
reg( 'iSentir', 'adherir', 'adhiriendo', 'adhiero', 'adherirse' )
reg( 'iSentir', 'advertir', 'advirtiendo', 'advierto' )
reg( 'iSentir', 'arrepentir', 'arrepintiendo', 'arrepiento', 'arrepentirse' )
reg( 'iSentir', 'asentir', 'asintiendo', 'asiento' )
reg( 'iSentir', 'circunferir', 'circunfiriendo', 'circunfiero' )
reg( 'iSentir', 'conferir', 'confiriendo', 'confiero' )
reg( 'iSentir', 'consentir', 'consintiendo', 'consiento' )
reg( 'iSentir', 'convertir', 'convirtiendo', 'convierto', 'convertirse', 'convertirla', 'convertiría', 'convertirías', 'convertirían', 'convirtieron', 'convirtiéndose', 'conviertieron' )
reg( 'iSentir', 'desmentir', 'desmintiendo', 'desmiento' )
reg( 'iSentir', 'diferir', 'difiriendo', 'difiero' )
reg( 'iSentir', 'digerir', 'digiriendo', 'digiero' )
reg( 'iSentir', 'disentir', 'disintiendo', 'disiento' )
reg( 'iSentir', 'divertir', 'divirtiendo', 'divierto', 'divertirse' )
reg( 'iSentir', 'herir', 'hiriendo', 'hiero' )
reg( 'iSentir', 'hervir', 'hirviendo', 'hiervo' )
reg( 'iSentir', 'inferir', 'infiriendo', 'infiero' )
reg( 'iSentir', 'ingerir', 'ingiriendo', 'ingiero' )
reg( 'iSentir', 'injerir', 'injiriendo', 'injiero', 'injerirse' )
reg( 'iSentir', 'interferir', 'interfiriendo', 'interfiero' )
reg( 'iSentir', 'invertir', 'invirtiendo', 'invierto' )
reg( 'iSentir', 'malherir', 'malhiriendo', 'malhiero' )
reg( 'iSentir', 'mentir', 'mintiendo', 'miento' )
reg( 'iSentir', 'pervertir', 'pervirtiendo', 'pervierto' )
reg( 'iSentir', 'preferir', 'prefiriendo', 'prefiero' )
reg( 'iSentir', 'presentir', 'presintiendo', 'presiento' )
reg( 'iSentir', 'proferir', 'profiriendo', 'profiero' )
reg( 'iSentir', 'reconvertir', 'reconvirtiendo', 'reconvierto' )
reg( 'iSentir', 'referir', 'refiriendo', 'refiero', 'referirse', 'referiremos', 'referirnos' )
reg( 'iSentir', 'reinvertir', 'reinvirtiendo', 'reinvierto' )
reg( 'iSentir', 'requerir', 'requiriendo', 'requiero' )
reg( 'iSentir', 'resentir', 'resintiendo', 'resiento', 'resentirse' )
reg( 'iSentir', 'revertir', 'revirtiendo', 'revierto' )
reg( 'iSentir', 'sentir', 'sintiendo', 'siento', 'sentirse' )
reg( 'iSentir', 'subvertir', 'subvirtiendo', 'subvierto' )
reg( 'iSentir', 'sugerir', 'sugiriendo', 'sugiero' )
reg( 'iSentir', 'transferir', 'transfiriendo', 'transfiero' )
reg( 'iSentir', 'trasferir', 'trasfiriendo', 'trasfiero' )
reg( 'iSentir', 'zaherir', 'zahiriendo', 'zahiero' )
reg( 'iSer', 'ser', 'soy', 'eres', 'es', 'siendo', 'fue', 'fuera', 'fueran', 'fuese', 'fueron', 'sea', 'sean', 'seas', 'seres', 'serlo', 'sería', 'serían', 'serías', 'sido', 'somos', 'son', 'será', 'serán', 'serás', 'era', 'eran' )
reg( 'iSoler', 'soler', 'suelo', 'sueles', 'suele', 'solemos', 'suelen', 'solía', 'solían', 'solías', 'suela', 'suelas', 'suelan', 'soliendo' )
reg( 'iTañer', 'atañer', 'atañe' )
reg( 'iTemer', 'absorber' )
reg( 'iTemer', 'acceder', 'accederse' )
reg( 'iTemer', 'acometer' )
reg( 'iTemer', 'adsorber' )
reg( 'iTemer', 'anteceder' )
reg( 'iTemer', 'aprehender' )
reg( 'iTemer', 'aprender', 'aprenderemos', 'aprendiese', 'aprendimos' )
reg( 'iTemer', 'arder' )
reg( 'iTemer', 'arremeter' )
reg( 'iTemer', 'atrever', 'atreverse' )
reg( 'iTemer', 'barrer' )
reg( 'iTemer', 'beber' )
reg( 'iTemer', 'carcomer' )
reg( 'iTemer', 'ceder' )
reg( 'iTemer', 'comer', 'comerse' )
reg( 'iTemer', 'cometer' )
reg( 'iTemer', 'compeler' )
reg( 'iTemer', 'competer' )
reg( 'iTemer', 'comprender' )
reg( 'iTemer', 'comprometer', 'comprometerse' )
reg( 'iTemer', 'conceder' )
reg( 'iTemer', 'correr', 'corrimos' )
reg( 'iTemer', 'corresponder' )
reg( 'iTemer', 'corromper' )
reg( 'iTemer', 'coser' )
reg( 'iTemer', 'deber', 'debía', 'debería', 'debemos', 'debe', 'deben', 'deberse' 'debiera' 'debieran' 'debieras', 'deberse' )
reg( 'iTemer', 'depender' )
reg( 'iTemer', 'descorrer' )
reg( 'iTemer', 'descoser' )
reg( 'iTemer', 'desprender', 'desprenderse' )
reg( 'iTemer', 'destejer' )
reg( 'iTemer', 'embeber' )
reg( 'iTemer', 'emprender' )
reg( 'iTemer', 'entremeter' )
reg( 'iTemer', 'entretejer' )
reg( 'iTemer', 'entrometer' )
reg( 'iTemer', 'esconder', 'esconderse' )
reg( 'iTemer', 'esplender' )
reg( 'iTemer', 'exceder' )
reg( 'iTemer', 'expeler' )
reg( 'iTemer', 'expender' )
reg( 'iTemer', 'impeler' )
reg( 'iTemer', 'interceder' )
reg( 'iTemer', 'joder' )
reg( 'iTemer', 'lamer' )
reg( 'iTemer', 'malcomer' )
reg( 'iTemer', 'malmeter' )
reg( 'iTemer', 'malvender' )
reg( 'iTemer', 'meter', 'meterse' )
reg( 'iTemer', 'ofender' )
reg( 'iTemer', 'pender' )
reg( 'iTemer', 'precaver' )
reg( 'iTemer', 'preceder' )
reg( 'iTemer', 'prender' )
reg( 'iTemer', 'pretender' )
reg( 'iTemer', 'proceder' )
reg( 'iTemer', 'prometer' )
reg( 'iTemer', 'propender' )
reg( 'iTemer', 'reabsorber' )
reg( 'iTemer', 'reconcomer', 'reconcomerse' )
reg( 'iTemer', 'recorrer', 'recorrimos' )
reg( 'iTemer', 'recoser' )
reg( 'iTemer', 'reemprender' )
reg( 'iTemer', 'relamer' )
reg( 'iTemer', 'remeter' )
reg( 'iTemer', 'repeler' )
reg( 'iTemer', 'reprender' )
reg( 'iTemer', 'responder', 'responda', 'responde', 'responden', 'responderlo' )
reg( 'iTemer', 'retroceder' )
reg( 'iTemer', 'revender' )
reg( 'iTemer', 'romper', 'romperse' )
reg( 'iTemer', 'sobreexceder' )
reg( 'iTemer', 'sobrexceder' )
reg( 'iTemer', 'socorrer' )
reg( 'iTemer', 'someter', 'someterse' )
reg( 'iTemer', 'sorber' )
reg( 'iTemer', 'sorprender' )
reg( 'iTemer', 'suceder' )
reg( 'iTemer', 'suspender' )
reg( 'iTemer', 'tejer' )
reg( 'iTemer', 'temer' )
reg( 'iTemer', 'toser' )
reg( 'iTemer', 'vender', 'venderse' )
reg( 'iTener', 'tener', 'tendrá', 'tendrás', 'tendrán', 'tenga', 'tengo', 'tendremos', 'tengan', 'tiene', 'tienen', 'tienes', 'tuvo', 'tenemos', 'tenía', 'tendría', 'teniendo', 'tenido', 'tenidos', 'tenida', 'tenidas', 'tenían', 'tenerlo', 'tuvieron', 'tuviera', 'tuvieran', 'tuvieras', 'tenerse', 'tuvimos', 'tenia' )
reg( 'iTraer', 'abstraer' )
reg( 'iTraer', 'atraer', 'atraído' )
reg( 'iTraer', 'contraer', 'contraen' )
reg( 'iTraer', 'distraer' )
reg( 'iTraer', 'extraer' )
reg( 'iTraer', 'maltraer' )
reg( 'iTraer', 'retraer' )
reg( 'iTraer', 'retrotraer' )
reg( 'iTraer', 'substraer' )
reg( 'iTraer', 'sustraer' )
reg( 'iTraer', 'traer' )
reg( 'iTropezar', 'comenzar', 'comenzó', 'comienzan', 'comienza', 'comienzo', 'comenzando', 'comenzaron', 'comenzará', 'comenzarás', 'comenzarán', 'comenzado' )
reg( 'iTropezar', 'empezar', 'empieza', 'empiezan', 'empezado', 'empezó', 'empezaron', 'empezará', 'empezarán', 'empezarás' )
reg( 'iTropezar', 'recomenzar', 'recomenzó' )
reg( 'iTropezar', 'tropezar', 'tropezó', 'tropezaron' )
reg( 'iVaciar', 'aliar', 'aliarse' )
reg( 'iVaciar', 'amnistiar' )
reg( 'iVaciar', 'ampliar', 'ampliarlo' )
reg( 'iVaciar', 'ansiar' )
reg( 'iVaciar', 'arriar' )
reg( 'iVaciar', 'ataviar' )
reg( 'iVaciar', 'averiar' )
reg( 'iVaciar', 'aviar' )
reg( 'iVaciar', 'biografiar' )
reg( 'iVaciar', 'cablegrafiar' )
reg( 'iVaciar', 'calcografiar' )
reg( 'iVaciar', 'caligrafiar' )
reg( 'iVaciar', 'cartografiar', 'cartografió' )
reg( 'iVaciar', 'chirriar' )
reg( 'iVaciar', 'ciar' )
reg( 'iVaciar', 'confiar' )
reg( 'iVaciar', 'contrariar' )
reg( 'iVaciar', 'coreografiar' )
reg( 'iVaciar', 'criar' )
reg( 'iVaciar', 'desafiar' )
reg( 'iVaciar', 'descarriar' )
reg( 'iVaciar', 'desconfiar' )
reg( 'iVaciar', 'desliar', 'deslizarse' )
reg( 'iVaciar', 'desvariar' )
reg( 'iVaciar', 'desviar', 'desviarse' )
reg( 'iVaciar', 'enfriar' )
reg( 'iVaciar', 'enviar', 'enviarse', 'enviarles', 'enviarle' )
reg( 'iVaciar', 'escalofriar' )
reg( 'iVaciar', 'espiar' )
reg( 'iVaciar', 'esquiar' )
reg( 'iVaciar', 'estriar' )
reg( 'iVaciar', 'expatriar' )
reg( 'iVaciar', 'expiar' )
reg( 'iVaciar', 'extasiar' )
reg( 'iVaciar', 'extraviar' )
reg( 'iVaciar', 'fiar' )
reg( 'iVaciar', 'fotografiar' )
reg( 'iVaciar', 'guiar' )
reg( 'iVaciar', 'hastiar' )
reg( 'iVaciar', 'inventariar' )
reg( 'iVaciar', 'liar' )
reg( 'iVaciar', 'malcriar' )
reg( 'iVaciar', 'mecanografiar' )
reg( 'iVaciar', 'piar' )
reg( 'iVaciar', 'porfiar' )
reg( 'iVaciar', 'radiografiar' )
reg( 'iVaciar', 'recriar' )
reg( 'iVaciar', 'reenviar' )
reg( 'iVaciar', 'resfriar' )
reg( 'iVaciar', 'rociar' )
reg( 'iVaciar', 'sumariar' )
reg( 'iVaciar', 'taquigrafiar' )
reg( 'iVaciar', 'telegrafiar' )
reg( 'iVaciar', 'vaciar', 'vació' )
reg( 'iVaciar', 'variar' )
reg( 'iVaciar', 'vidriar' )
reg( 'iVaciar', 'xerografiar' )
reg( 'iValer', 'equivaler', 'equivale', 'equivalía', 'equivalían', 'equivalías', 'equivaldría', 'equivaldrían', 'equivaldrías' )
reg( 'iValer', 'valer', 'vale', 'valen', 'valdrá', 'valdrán', 'valdrás', 'valieron', 'valió', 'valía', 'valían', 'valías', 'valdría', 'valdrían', 'valdrías' )
reg( 'iVenir', 'venir', 'ven', 'vienen', 'viene', 'venía', 'venías', 'venían', 'vendrá', 'vendrán', 'vendrás', 'vinieron', 'vendría', 'vendrían', 'vendrías', 'venimos', 'vinimos' )
reg( 'iVer', 'ver', 'vea', 'veo', 've', 'ved', 'vio', 'veamos', 'veremos', 'verse', 'verá', 'verán', 'verás', 'viera', 'vista', 'vistos', 'vistas', 'visto', 'vemos', 'vería', 'verían', 'verías', 'véase', 'vió', 'vieron', 'veía', 'veían', 'veías', 'viendo' )
reg( 'iVolcar', 'trocar', 'trocó' )
reg( 'iVolcar', 'volcar', 'volcó', 'volcará', 'volcarán', 'volcarás', 'volcaron' )
reg( 'iYacer', 'subyacer', 'subyació' )
reg( 'iYacer', 'yacer', 'yació', 'yacía', 'yacían', 'yacías' )
reg( 'pA', 'abrumador' )
reg( 'pA', 'acreedor')
reg( 'pA', 'administrador' )
reg( 'pA', 'alemán', 'alemana', 'alemanas', 'alemanes' )
reg( 'pA', 'animador')
reg( 'pA', 'anotador' )
reg( 'pA', 'anterior' )
reg( 'pA', 'asesor' )
reg( 'pA', 'autor' )
reg( 'pA', 'biomarcador' )
reg( 'pA', 'cazador' )
reg( 'pA', 'colector' )
reg( 'pA', 'comparador' )
reg( 'pA', 'competidor' )
reg( 'pA', 'compilador' )
reg( 'pA', 'compositor' )
reg( 'pA', 'conductor' )
reg( 'pA', 'conector' )
reg( 'pA', 'conquistador' )
reg( 'pA', 'constructor' )
reg( 'pA', 'consumidor' )
reg( 'pA', 'controlador' )
reg( 'pA', 'coordinador' )
reg( 'pA', 'coronel' )
reg( 'pA', 'corredor' )
reg( 'pA', 'defensor' )
reg( 'pA', 'delimitador' )
reg( 'pA', 'depredador' )
reg( 'pA', 'desarrollador' )
reg( 'pA', 'descubridor' )
reg( 'pA', 'detector')
reg( 'pA', 'dictador' )
reg( 'pA', 'dios' )
reg( 'pA', 'director' )
reg( 'pA', 'diseñador' )
reg( 'pA', 'distribuidor' )
reg( 'pA', 'doctor' )
reg( 'pA', 'editor' )
reg( 'pA', 'educador' )
reg( 'pA', 'embajador' )
reg( 'pA', 'empleador' )
reg( 'pA', 'enriquecedor' )
reg( 'pA', 'entrenador' )
reg( 'pA', 'escritor' )
reg( 'pA', 'escultor' )
reg( 'pA', 'espectador' )
reg( 'pA', 'estabilizador' )
reg( 'pA', 'explorador' )
reg( 'pA', 'fundador' )
reg( 'pA', 'ganador' )
reg( 'pA', 'gestor' )
reg( 'pA', 'gobernador' )
reg( 'pA', 'goleador' )
reg( 'pA', 'historiador' )
reg( 'pA', 'hospedador' )
reg( 'pA', 'identificador' )
reg( 'pA', 'ilustrador' )
reg( 'pA', 'imitador' )
reg( 'pA', 'impulsor' )
reg( 'pA', 'indicador' )
reg( 'pA', 'interceptor' )
reg( 'pA', 'intermediador' )
reg( 'pA', 'invasor' )
reg( 'pA', 'inversor')
reg( 'pA', 'investigador' )
reg( 'pA', 'lanzador' )
reg( 'pA', 'lector' )
reg( 'pA', 'localizador' )
reg( 'pA', 'locutor' )
reg( 'pA', 'luchador' )
reg( 'pA', 'marcador' )
reg( 'pA', 'materno' )
reg( 'pA', 'narrador' )
reg( 'pA', 'navegador' )
reg( 'pA', 'operador' )
reg( 'pA', 'opositor' )
reg( 'pA', 'pastor' )
reg( 'pA', 'pescador' )
reg( 'pA', 'portador' )
reg( 'pA', 'predador' )
reg( 'pA', 'predecesor' )
reg( 'pA', 'presentador' )
reg( 'pA', 'procesador' )
reg( 'pA', 'productor' )
reg( 'pA', 'profesor' )
reg( 'pA', 'progenitor' )
reg( 'pA', 'programador' )
reg( 'pA', 'prometedor' )
reg( 'pA', 'promotor' )
reg( 'pA', 'protector')
reg( 'pA', 'realizador' )
reg( 'pA', 'receptor' )
reg( 'pA', 'rector' )
reg( 'pA', 'reductor' )
reg( 'pA', 'revisor' )
reg( 'pA', 'roedor' )
reg( 'pA', 'selector' )
reg( 'pA', 'senador' )
reg( 'pA', 'servidor' )
reg( 'pA', 'señor' )
reg( 'pA', 'suscriptor' )
reg( 'pA', 'tirador' )
reg( 'pA', 'trabajador')
reg( 'pA', 'traductor' )
reg( 'pA', 'transportador' )
reg( 'pA', 'trazador')
reg( 'pA', 'vencedor' )
reg( 'pAe', 'certero')
reg( 'pAs ', 'comprendido')
reg( 'pAs', 'abierto' )
reg( 'pAs', 'abrahámico' )
reg( 'pAs', 'abrupto' )
reg( 'pAs', 'absoluto' )
reg( 'pAs', 'abstracto' )
reg( 'pAs', 'abuelo' )
reg( 'pAs', 'académico' )
reg( 'pAs', 'acoplado' )
reg( 'pAs', 'acostumbrado' )
reg( 'pAs', 'acrobático' )
reg( 'pAs', 'acrílico' )
reg( 'pAs', 'acuático' )
reg( 'pAs', 'acérrimo' )
reg( 'pAs', 'acústico' )
reg( 'pAs', 'adaptativo' )
reg( 'pAs', 'adecuado' )
reg( 'pAs', 'adivino' )
reg( 'pAs', 'adjunto')
reg( 'pAs', 'administrativo' )
reg( 'pAs', 'adulto' )
reg( 'pAs', 'aerodinámico' )
reg( 'pAs', 'aeronáutico' )
reg( 'pAs', 'aeróbico' )
reg( 'pAs', 'afortunado' )
reg( 'pAs', 'africano' )
reg( 'pAs', 'afroamericano' )
reg( 'pAs', 'afroasiático' )
reg( 'pAs', 'agudo' )
reg( 'pAs', 'aislado' )
reg( 'pAs', 'ajeno')
reg( 'pAs', 'alcohólico' )
reg( 'pAs', 'aleatorio' )
reg( 'pAs', 'alegórico' )
reg( 'pAs', 'alejado')
reg( 'pAs', 'algebraico' )
reg( 'pAs', 'alguno', 'algún' )
reg( 'pAs', 'alocado' )
reg( 'pAs', 'alojado')
reg( 'pAs', 'alopátrico' )
reg( 'pAs', 'alpino' )
reg( 'pAs', 'altaico' )
reg( 'pAs', 'alternativo' )
reg( 'pAs', 'alterno' )
reg( 'pAs', 'altimétrico' )
reg( 'pAs', 'alto', 'altísimo', 'altísima', 'altísimos', 'altísimas' )
reg( 'pAs', 'alélico' )
reg( 'pAs', 'alérgico' )
reg( 'pAs', 'amarillo' )
reg( 'pAs', 'amazónico' )
reg( 'pAs', 'ambiguo' )
reg( 'pAs', 'americano' )
reg( 'pAs', 'amerindio' )
reg( 'pAs', 'amistoso' )
reg( 'pAs', 'amplio', 'amplísimo', 'amplísima', 'amplísimos', 'amplísimas' )
reg( 'pAs', 'analítico' )
reg( 'pAs', 'analógico' )
reg( 'pAs', 'anatómico' )
reg( 'pAs', 'ancho' )
reg( 'pAs', 'anfibio' )
reg( 'pAs', 'anidado' )
reg( 'pAs', 'anotado' )
reg( 'pAs', 'antagónico' )
reg( 'pAs', 'antepasado' )
reg( 'pAs', 'antiguo', 'antiquísimo', 'antiquísima', 'antiquísimos', 'antiquísimas' )
reg( 'pAs', 'antológico' )
reg( 'pAs', 'antropológico' )
reg( 'pAs', 'antropomórfico' )
reg( 'pAs', 'antártico' )
reg( 'pAs', 'análogo' )
reg( 'pAs', 'anónimo' )
reg( 'pAs', 'apomíctico' )
reg( 'pAs', 'apostólico' )
reg( 'pAs', 'apropiado' )
reg( 'pAs', 'arcaico' )
reg( 'pAs', 'arenoso' )
reg( 'pAs', 'argentino' )
reg( 'pAs', 'aristocrático' )
reg( 'pAs', 'aristotélico' )
reg( 'pAs', 'aritmético' )
reg( 'pAs', 'armónico' )
reg( 'pAs', 'aromático' )
reg( 'pAs', 'arqueológico' )
reg( 'pAs', 'arquitecto' )
reg( 'pAs', 'arquitectónico' )
reg( 'pAs', 'artesano' )
reg( 'pAs', 'artístico' )
reg( 'pAs', 'arácnido' )
reg( 'pAs', 'asesino' )
reg( 'pAs', 'asimétrico' )
reg( 'pAs', 'asiático' )
reg( 'pAs', 'asociado' )
reg( 'pAs', 'asombroso' )
reg( 'pAs', 'astillero' )
reg( 'pAs', 'astrológico' )
reg( 'pAs', 'astronómico' )
reg( 'pAs', 'astrónomo' )
reg( 'pAs', 'astuto' )
reg( 'pAs', 'asíncrono' )
reg( 'pAs', 'atlántico' )
reg( 'pAs', 'atlético' )
reg( 'pAs', 'atmosférico' )
reg( 'pAs', 'atractivo' )
reg( 'pAs', 'atípico' )
reg( 'pAs', 'atómico' )
reg( 'pAs', 'australiano' )
reg( 'pAs', 'austriaco' )
reg( 'pAs', 'austroasiático' )
reg( 'pAs', 'austríaco' )
reg( 'pAs', 'autobiográfico' )
reg( 'pAs', 'autogénico' )
reg( 'pAs', 'automovilístico' )
reg( 'pAs', 'automático' )
reg( 'pAs', 'autonómico' )
reg( 'pAs', 'auténtico')
reg( 'pAs', 'autóctono' )
reg( 'pAs', 'autónomo' )
reg( 'pAs', 'azteco' )
reg( 'pAs', 'aéreo' )
reg( 'pAs', 'bacteriano' )
reg( 'pAs', 'bajo', 'bajísimo', 'bajísima', 'bajísimos', 'bajísimas' )
reg( 'pAs', 'balcánico' )
reg( 'pAs', 'barroco' )
reg( 'pAs', 'basáltico' )
reg( 'pAs', 'bayesiano' )
reg( 'pAs', 'bello', 'bellísimo', 'bellísima', 'bellísimos', 'bellísimas' )
reg( 'pAs', 'beneficioso' )
reg( 'pAs', 'benéfico' )
reg( 'pAs', 'bibliográfico' )
reg( 'pAs', 'bibliotecario' )
reg( 'pAs', 'biogeográfico' )
reg( 'pAs', 'biográfico' )
reg( 'pAs', 'biológico' )
reg( 'pAs', 'biomédico' )
reg( 'pAs', 'biométrico' )
reg( 'pAs', 'bioquímico' )
reg( 'pAs', 'biselado' )
reg( 'pAs', 'bisiesto' )
reg( 'pAs', 'bizantino' )
reg( 'pAs', 'biólogo' )
reg( 'pAs', 'blanco' )
reg( 'pAs', 'boliviano' )
reg( 'pAs', 'booleano' )
reg( 'pAs', 'borbónico' )
reg( 'pAs', 'botánico' )
reg( 'pAs', 'brasileño' )
reg( 'pAs', 'británico' )
reg( 'pAs', 'brujo' )
reg( 'pAs', 'brusco' )
reg( 'pAs', 'bruto' )
reg( 'pAs', 'bueno', 'buen' )
reg( 'pAs', 'burocrático' )
reg( 'pAs', 'báltico' )
reg( 'pAs', 'básico' )
reg( 'pAs', 'bélico' )
reg( 'pAs', 'bíblico' )
reg( 'pAs', 'búlgaro' )
reg( 'pAs', 'caballeresco' )
reg( 'pAs', 'cableado' )
reg( 'pAs', 'caligráfico' )
reg( 'pAs', 'campesino' )
reg( 'pAs', 'candidato' )
reg( 'pAs', 'canónico' )
reg( 'pAs', 'caracteristico' )
reg( 'pAs', 'característico' )
reg( 'pAs', 'cardiaco' )
reg( 'pAs', 'cardíaco' )
reg( 'pAs', 'cartográfico' )
reg( 'pAs', 'castaño' )
reg( 'pAs', 'castellano' )
reg( 'pAs', 'catalítico' )
reg( 'pAs', 'catastrófico' )
reg( 'pAs', 'catedrático' )
reg( 'pAs', 'católico' )
reg( 'pAs', 'caucásico' )
reg( 'pAs', 'caótico' )
reg( 'pAs', 'centésimo' )
reg( 'pAs', 'cercano' )
reg( 'pAs', 'cerdo' )
reg( 'pAs', 'cerámico' )
reg( 'pAs', 'checo' )
reg( 'pAs', 'chichimeco' )
reg( 'pAs', 'chico' )
reg( 'pAs', 'chileno' )
reg( 'pAs', 'chino' )
reg( 'pAs', 'chádico' )
reg( 'pAs', 'ciego' )
reg( 'pAs', 'científico' )
reg( 'pAs', 'cierto' )
reg( 'pAs', 'ciervo' )
reg( 'pAs', 'cilíndrico' )
reg( 'pAs', 'cinegético' )
reg( 'pAs', 'cinematográfico' )
reg( 'pAs', 'cinemático' )
reg( 'pAs', 'cirujano' )
reg( 'pAs', 'ciudadano' )
reg( 'pAs', 'claro' )
reg( 'pAs', 'climatológico' )
reg( 'pAs', 'climático' )
reg( 'pAs', 'clásico' )
reg( 'pAs', 'clínico' )
reg( 'pAs', 'cognitivo' )
reg( 'pAs', 'colectivo' )
reg( 'pAs', 'coleóptero' )
reg( 'pAs', 'colombiano' )
reg( 'pAs', 'combinatorio' )
reg( 'pAs', 'comisario' )
reg( 'pAs', 'compacto')
reg( 'pAs', 'comparativo' )
reg( 'pAs', 'compañero' )
reg( 'pAs', 'competitivo' )
reg( 'pAs', 'complejo' )
reg( 'pAs', 'complementario' )
reg( 'pAs', 'completo' )
reg( 'pAs', 'comprometido' )
reg( 'pAs', 'compuesto' )
reg( 'pAs', 'conciliado' )
reg( 'pAs', 'concreto' )
reg( 'pAs', 'concéntrico' )
reg( 'pAs', 'conjunto' )
reg( 'pAs', 'conocido' )
reg( 'pAs', 'consecutivo' )
reg( 'pAs', 'consejero' )
reg( 'pAs', 'conservador' )
reg( 'pAs', 'conspicuo' )
reg( 'pAs', 'contemporáneo' )
reg( 'pAs', 'contenido' )
reg( 'pAs', 'continuo' )
reg( 'pAs', 'contradictorio' )
reg( 'pAs', 'contrario' )
reg( 'pAs', 'controvertido' )
reg( 'pAs', 'cooperativo' )
reg( 'pAs', 'cordado' )
reg( 'pAs', 'coreano' )
reg( 'pAs', 'corporativo')
reg( 'pAs', 'correcto' )
reg( 'pAs', 'corto' )
reg( 'pAs', 'cosaco' )
reg( 'pAs', 'cosmológico' )
reg( 'pAs', 'costero' )
reg( 'pAs', 'costoso' )
reg( 'pAs', 'cotidiano' )
reg( 'pAs', 'creativo' )
reg( 'pAs', 'criptográfico' )
reg( 'pAs', 'cristiano' )
reg( 'pAs', 'cromosómico' )
reg( 'pAs', 'cromático' )
reg( 'pAs', 'cronológico' )
reg( 'pAs', 'críptico' )
reg( 'pAs', 'crítico')
reg( 'pAs', 'crónico' )
reg( 'pAs', 'cuadrado' )
reg( 'pAs', 'cuadrático' )
reg( 'pAs', 'cuanto' )
reg( 'pAs', 'cuarto' )
reg( 'pAs', 'cubano' )
reg( 'pAs', 'cuidadoso')
reg( 'pAs', 'curioso' )
reg( 'pAs', 'cursivo' )
reg( 'pAs', 'curvado', 'curvo', 'curvos' )
reg( 'pAs', 'cuyo' )
reg( 'pAs', 'cuántico' )
reg( 'pAs', 'cálido' )
reg( 'pAs', 'cámbrico' )
reg( 'pAs', 'céltico' )
reg( 'pAs', 'céntrico' )
reg( 'pAs', 'cíclico' )
reg( 'pAs', 'cívico' )
reg( 'pAs', 'cómico' )
reg( 'pAs', 'cónico' )
reg( 'pAs', 'cósmico' )
reg( 'pAs', 'cúbico' )
reg( 'pAs', 'dado' )
reg( 'pAs', 'decano' )
reg( 'pAs', 'declarativo' )
reg( 'pAs', 'deductivo' )
reg( 'pAs', 'defensivo' )
reg( 'pAs', 'definitivo' )
reg( 'pAs', 'delantero' )
reg( 'pAs', 'deletéreo' )
reg( 'pAs', 'delgado' )
reg( 'pAs', 'democrático' )
reg( 'pAs', 'demográfico' )
reg( 'pAs', 'demonio' )
reg( 'pAs', 'demoníaco' )
reg( 'pAs', 'dendrítico' )
reg( 'pAs', 'deportivo' )
reg( 'pAs', 'derecho' )
reg( 'pAs', 'desacoplado' )
reg( 'pAs', 'desactualizado')
reg( 'pAs', 'desapercibido' )
reg( 'pAs', 'descriptivo' )
reg( 'pAs', 'destructivo')
reg( 'pAs', 'desventajoso' )
reg( 'pAs', 'desértico' )
reg( 'pAs', 'detallado' )
reg( 'pAs', 'diagnóstico' )
reg( 'pAs', 'diario' )
reg( 'pAs', 'diatómico' )
reg( 'pAs', 'dicho' )
reg( 'pAs', 'didáctico' )
reg( 'pAs', 'diferido' )
reg( 'pAs', 'difuso' )
reg( 'pAs', 'dinámico' )
reg( 'pAs', 'dinástico' )
reg( 'pAs', 'diplomático' )
reg( 'pAs', 'diputado' )
reg( 'pAs', 'directivo' )
reg( 'pAs', 'directo' )
reg( 'pAs', 'dirigido' )
reg( 'pAs', 'disciplinario' )
reg( 'pAs', 'discografico' )
reg( 'pAs', 'discográfico' )
reg( 'pAs', 'diseminado' )
reg( 'pAs', 'distinto' )
reg( 'pAs', 'diverso' )
reg( 'pAs', 'divino' )
reg( 'pAs', 'documentado' )
reg( 'pAs', 'dogmático' )
reg( 'pAs', 'dominicano' )
reg( 'pAs', 'doméstico' )
reg( 'pAs', 'dorado' )
reg( 'pAs', 'dramaturgo' )
reg( 'pAs', 'dramático' )
reg( 'pAs', 'drástico' )
reg( 'pAs', 'dueño' )
reg( 'pAs', 'duro' )
reg( 'pAs', 'dístico' )
reg( 'pAs', 'dórico' )
reg( 'pAs', 'eclesiástico' )
reg( 'pAs', 'ecológico' )
reg( 'pAs', 'económico')
reg( 'pAs', 'ecuatoriano' )
reg( 'pAs', 'educativo' )
reg( 'pAs', 'efectivo' )
reg( 'pAs', 'egipcio' )
reg( 'pAs', 'ejecutivo' )
reg( 'pAs', 'electo' )
reg( 'pAs', 'electromagnético' )
reg( 'pAs', 'electrónico' )
reg( 'pAs', 'elegido' )
reg( 'pAs', 'elevado' )
reg( 'pAs', 'elástico' )
reg( 'pAs', 'eléctrico' )
reg( 'pAs', 'elíptico' )
reg( 'pAs', 'emblemático' )
reg( 'pAs', 'embrionario' )
reg( 'pAs', 'embriólogo' )
reg( 'pAs', 'emotivo' )
reg( 'pAs', 'empresario' )
reg( 'pAs', 'empírico' )
reg( 'pAs', 'encadenado' )
reg( 'pAs', 'enciclopédico' )
reg( 'pAs', 'encuestado' )
reg( 'pAs', 'encíclico' )
reg( 'pAs', 'endorreico' )
reg( 'pAs', 'endosimbiótico' )
reg( 'pAs', 'endémico' )
reg( 'pAs', 'enemigo' )
reg( 'pAs', 'energético' )
reg( 'pAs', 'enfermizo' )
reg( 'pAs', 'enigmático' )
reg( 'pAs', 'entero' )
reg( 'pAs', 'enzimático' )
reg( 'pAs', 'enérgico' )
reg( 'pAs', 'epidérmico' )
reg( 'pAs', 'epigenético' )
reg( 'pAs', 'epigámico' )
reg( 'pAs', 'epiléptico' )
reg( 'pAs', 'epistemológico' )
reg( 'pAs', 'epónimo' )
reg( 'pAs', 'equivocado' )
reg( 'pAs', 'erróneo' )
reg( 'pAs', 'erótico' )
reg( 'pAs', 'escaso' )
reg( 'pAs', 'escultórico' )
reg( 'pAs', 'escénico' )
reg( 'pAs', 'esférico' )
reg( 'pAs', 'esotérico' )
reg( 'pAs', 'espectroscópico' )
reg( 'pAs', 'específico' )
reg( 'pAs', 'espontáneo' )
reg( 'pAs', 'esporádico' )
reg( 'pAs', 'esposo' )
reg( 'pAs', 'esquelético' )
reg( 'pAs', 'esquemático' )
reg( 'pAs', 'estadístico' )
reg( 'pAs', 'estilístico' )
reg( 'pAs', 'estocástico' )
reg( 'pAs', 'estratégico' )
reg( 'pAs', 'estrecho' )
reg( 'pAs', 'estromatolito' )
reg( 'pAs', 'estructurado' )
reg( 'pAs', 'estudioso' )
reg( 'pAs', 'estático' )
reg( 'pAs', 'estético' )
reg( 'pAs', 'etimológico' )
reg( 'pAs', 'etnográfico' )
reg( 'pAs', 'etrusco' )
reg( 'pAs', 'eucariótico' )
reg( 'pAs', 'europeo' )
reg( 'pAs', 'evangélico' )
reg( 'pAs', 'evolutivo' )
reg( 'pAs', 'exacto' )
reg( 'pAs', 'examinado' )
reg( 'pAs', 'exclusivo' )
reg( 'pAs', 'excéntrico' )
reg( 'pAs', 'exhaustivo' )
reg( 'pAs', 'exitoso' )
reg( 'pAs', 'experto' )
reg( 'pAs', 'explicativo' )
reg( 'pAs', 'explícito' )
reg( 'pAs', 'expuesto' )
reg( 'pAs', 'extenso' )
reg( 'pAs', 'externo' )
reg( 'pAs', 'extinguido' )
reg( 'pAs', 'extinto' )
reg( 'pAs', 'extranjero' )
reg( 'pAs', 'extraordinario' )
reg( 'pAs', 'extrapolado' )
reg( 'pAs', 'extraño' )
reg( 'pAs', 'extremo' )
reg( 'pAs', 'exótico' )
reg( 'pAs', 'eólico' )
reg( 'pAs', 'facultativo' )
reg( 'pAs', 'fallido' )
reg( 'pAs', 'fallo' )
reg( 'pAs', 'falso' )
reg( 'pAs', 'famoso', 'famosísimo', 'famosísima', 'famosísimos', 'famosísimas' )
reg( 'pAs', 'fantástico' )
reg( 'pAs', 'fanático' )
reg( 'pAs', 'farmacológico' )
reg( 'pAs', 'farmacéutico' )
reg( 'pAs', 'favorito' )
reg( 'pAs', 'femenino' )
reg( 'pAs', 'fenotípico' )
reg( 'pAs', 'ferroviario' )
reg( 'pAs', 'festivo' )
reg( 'pAs', 'ficticio' )
reg( 'pAs', 'fijo' )
reg( 'pAs', 'filantrópico' )
reg( 'pAs', 'filatélico' )
reg( 'pAs', 'filogenético' )
reg( 'pAs', 'filosófico' )
reg( 'pAs', 'filósofo' )
reg( 'pAs', 'financiero' )
reg( 'pAs', 'finito' )
reg( 'pAs', 'fino', 'finísimo', 'finísima', 'finísimos', 'finísimas' )
reg( 'pAs', 'fisiográfico' )
reg( 'pAs', 'fisiológico' )
reg( 'pAs', 'flamenco' )
reg( 'pAs', 'folclórico' )
reg( 'pAs', 'folklórico' )
reg( 'pAs', 'fonológico' )
reg( 'pAs', 'fonético' )
reg( 'pAs', 'foraminífero' )
reg( 'pAs', 'forzos' )
reg( 'pAs', 'fotoautótrofo' )
reg( 'pAs', 'fotográfico' )
reg( 'pAs', 'fotosintético' )
reg( 'pAs', 'fotovoltaico' )
reg( 'pAs', 'fotógrafo' )
reg( 'pAs', 'franco' )
reg( 'pAs', 'francófono' )
reg( 'pAs', 'fresco' )
reg( 'pAs', 'freático' )
reg( 'pAs', 'fructífero' )
reg( 'pAs', 'frío' )
reg( 'pAs', 'funcionario' )
reg( 'pAs', 'futbolístico' )
reg( 'pAs', 'futuro' )
reg( 'pAs', 'férreo' )
reg( 'pAs', 'fílmico' )
reg( 'pAs', 'físico' )
reg( 'pAs', 'gallego' )
reg( 'pAs', 'galáctico' )
reg( 'pAs', 'gasterópodo' )
reg( 'pAs', 'gastronómico' )
reg( 'pAs', 'gemelo' )
reg( 'pAs', 'genealógico' )
reg( 'pAs', 'genotípico' )
reg( 'pAs', 'genérico' )
reg( 'pAs', 'genético' )
reg( 'pAs', 'genómico' )
reg( 'pAs', 'geodésico' )
reg( 'pAs', 'geográfico' )
reg( 'pAs', 'geológico' )
reg( 'pAs', 'geomorfológico' )
reg( 'pAs', 'geométrico' )
reg( 'pAs', 'geoquímico' )
reg( 'pAs', 'germánico' )
reg( 'pAs', 'geólogo' )
reg( 'pAs', 'gigantesco' )
reg( 'pAs', 'gnóstico' )
reg( 'pAs', 'golfo' )
reg( 'pAs', 'gramático' )
reg( 'pAs', 'granítico' )
reg( 'pAs', 'gratuito' )
reg( 'pAs', 'griego' )
reg( 'pAs', 'grotesco' )
reg( 'pAs', 'grueso' )
reg( 'pAs', 'gráfico' )
reg( 'pAs', 'guerrero' )
reg( 'pAs', 'guerrillero' )
reg( 'pAs', 'gástrico' )
reg( 'pAs', 'génico' )
reg( 'pAs', 'gótico' )
reg( 'pAs', 'hebreo' )
reg( 'pAs', 'hecho' )
reg( 'pAs', 'helenístico' )
reg( 'pAs', 'hematológico' )
reg( 'pAs', 'hepático' )
reg( 'pAs', 'herbáceo' )
reg( 'pAs', 'heredero' )
reg( 'pAs', 'hereditario' )
reg( 'pAs', 'hermano' )
reg( 'pAs', 'hermoso' )
reg( 'pAs', 'heroico' )
reg( 'pAs', 'heráldico' )
reg( 'pAs', 'herético' )
reg( 'pAs', 'heterocigótico' )
reg( 'pAs', 'heurístico' )
reg( 'pAs', 'hidroeléctrico' )
reg( 'pAs', 'hidrográfico' )
reg( 'pAs', 'hidrológico' )
reg( 'pAs', 'hidráulico' )
reg( 'pAs', 'higiénico' )
reg( 'pAs', 'hijo' )
reg( 'pAs', 'hiperbólico' )
reg( 'pAs', 'hipotético' )
reg( 'pAs', 'hispano' )
reg( 'pAs', 'hispánico' )
reg( 'pAs', 'historico' )
reg( 'pAs', 'historiográfico' )
reg( 'pAs', 'histórico' )
reg( 'pAs', 'holístico' )
reg( 'pAs', 'homeótico' )
reg( 'pAs', 'homínido' )
reg( 'pAs', 'homólogo' )
reg( 'pAs', 'homónimo' )
reg( 'pAs', 'honorífico' )
reg( 'pAs', 'horario' )
reg( 'pAs', 'hueco' )
reg( 'pAs', 'humano' )
reg( 'pAs', 'humanístico' )
reg( 'pAs', 'humorístico' )
reg( 'pAs', 'híbrido' )
reg( 'pAs', 'hídrico' )
reg( 'pAs', 'húmedo' )
reg( 'pAs', 'húngaro' )
reg( 'pAs', 'ibérico' )
reg( 'pAs', 'iconográfico' )
reg( 'pAs', 'ideológico' )
reg( 'pAs', 'idiomático' )
reg( 'pAs', 'idéntico' )
reg( 'pAs', 'idóneo' )
reg( 'pAs', 'ilegítimo' )
reg( 'pAs', 'ilimitado' )
reg( 'pAs', 'impuesto' )
reg( 'pAs', 'inacabado')
reg( 'pAs', 'inactivo' )
reg( 'pAs', 'inalámbrico' )
reg( 'pAs', 'incaico' )
reg( 'pAs', 'incierto' )
reg( 'pAs', 'inclusivo' )
reg( 'pAs', 'incompleto' )
reg( 'pAs', 'incorrecto' )
reg( 'pAs', 'incómodo' )
reg( 'pAs', 'indefinido' )
reg( 'pAs', 'indicativo' )
reg( 'pAs', 'indiscriminado' )
reg( 'pAs', 'indoeuropeo' )
reg( 'pAs', 'inductivo' )
reg( 'pAs', 'inesperado' )
reg( 'pAs', 'informático')
reg( 'pAs', 'infundado' )
reg( 'pAs', 'ingeniero' )
reg( 'pAs', 'ingenioso' )
reg( 'pAs', 'inmediato' )
reg( 'pAs', 'inmunológico' )
reg( 'pAs', 'innecesario' )
reg( 'pAs', 'inofensivo' )
reg( 'pAs', 'inorgánico' )
reg( 'pAs', 'inspirado' )
reg( 'pAs', 'instantáneo' )
reg( 'pAs', 'intacto' )
reg( 'pAs', 'intenso' )
reg( 'pAs', 'interactivo' )
reg( 'pAs', 'intercalado' )
reg( 'pAs', 'interespecífico' )
reg( 'pAs', 'interino' )
reg( 'pAs', 'interlingüístico' )
reg( 'pAs', 'intermedio' )
reg( 'pAs', 'interno' )
reg( 'pAs', 'interrelacionado' )
reg( 'pAs', 'intraespecífico' )
reg( 'pAs', 'introductorio' )
reg( 'pAs', 'intrínseco' )
reg( 'pAs', 'intuitivo' )
reg( 'pAs', 'inverso' )
reg( 'pAs', 'invitado' )
reg( 'pAs', 'inédito' )
reg( 'pAs', 'irónico' )
reg( 'pAs', 'isleño' )
reg( 'pAs', 'islámico' )
reg( 'pAs', 'isótopo' )
reg( 'pAs', 'italiano' )
reg( 'pAs', 'itálico' )
reg( 'pAs', 'izquierdo' )
reg( 'pAs', 'iónico' )
reg( 'pAs', 'jerárquico' )
reg( 'pAs', 'jesuítico' )
reg( 'pAs', 'judío' )
reg( 'pAs', 'junto' )
reg( 'pAs', 'jurídico' )
reg( 'pAs', 'justo' )
reg( 'pAs', 'jónico' )
reg( 'pAs', 'laico' )
reg( 'pAs', 'lamarckiano' )
reg( 'pAs', 'lanceolado' )
reg( 'pAs', 'largo', 'larguísimo', 'larguísima', 'larguísimos', 'larguísimas' )
reg( 'pAs', 'latino' )
reg( 'pAs', 'latinoamericano' )
reg( 'pAs', 'legendario' )
reg( 'pAs', 'legislativo' )
reg( 'pAs', 'legítimo' )
reg( 'pAs', 'lento' )
reg( 'pAs', 'lesbiano' )
reg( 'pAs', 'leñoso' )
reg( 'pAs', 'libreto' )
reg( 'pAs', 'ligero' )
reg( 'pAs', 'limpio' )
reg( 'pAs', 'lipídico' )
reg( 'pAs', 'liso' )
reg( 'pAs', 'listo' )
reg( 'pAs', 'literario' )
reg( 'pAs', 'litúrgico' )
reg( 'pAs', 'lobo' )
reg( 'pAs', 'loco' )
reg( 'pAs', 'logarítmico' )
reg( 'pAs', 'logístico' )
reg( 'pAs', 'lucrativo')
reg( 'pAs', 'lésbico' )
reg( 'pAs', 'léxico' )
reg( 'pAs', 'lípido' )
reg( 'pAs', 'lírico' )
reg( 'pAs', 'lítico' )
reg( 'pAs', 'lógico' )
reg( 'pAs', 'lúdico' )
reg( 'pAs', 'macizo' )
reg( 'pAs', 'macroeconómico' )
reg( 'pAs', 'macroevolutivo' )
reg( 'pAs', 'macroscópico' )
reg( 'pAs', 'maestro' )
reg( 'pAs', 'magnético' )
reg( 'pAs', 'magnífico')
reg( 'pAs', 'mago' )
reg( 'pAs', 'malicioso')
reg( 'pAs', 'malo' )
reg( 'pAs', 'marino' )
reg( 'pAs', 'marítimo' )
reg( 'pAs', 'masculino' )
reg( 'pAs', 'masivo' )
reg( 'pAs', 'masónico' )
reg( 'pAs', 'matematico' )
reg( 'pAs', 'materno' )
reg( 'pAs', 'maximo' )
reg( 'pAs', 'mecánico' )
reg( 'pAs', 'mediano' )
reg( 'pAs', 'mediático' )
reg( 'pAs', 'megalítico' )
reg( 'pAs', 'meiótico' )
reg( 'pAs', 'melancólico' )
reg( 'pAs', 'melánico' )
reg( 'pAs', 'melódico' )
reg( 'pAs', 'mendeliano' )
reg( 'pAs', 'mercenario' )
reg( 'pAs', 'mesopotámico' )
reg( 'pAs', 'metabólico' )
reg( 'pAs', 'metafísico' )
reg( 'pAs', 'metafórico' )
reg( 'pAs', 'metalúrgico' )
reg( 'pAs', 'metamórfico' )
reg( 'pAs', 'meteorológico' )
reg( 'pAs', 'metodológico' )
reg( 'pAs', 'metropolitano' )
reg( 'pAs', 'metálico' )
reg( 'pAs', 'mexicano' )
reg( 'pAs', 'microbiano' )
reg( 'pAs', 'microevolutivo' )
reg( 'pAs', 'microscópico' )
reg( 'pAs', 'migratorio' )
reg( 'pAs', 'minero' )
reg( 'pAs', 'minucioso')
reg( 'pAs', 'misceláneo' )
reg( 'pAs', 'misionero' )
reg( 'pAs', 'misterioso' )
reg( 'pAs', 'mitológico' )
reg( 'pAs', 'mixto' )
reg( 'pAs', 'modelado' )
reg( 'pAs', 'moderado' )
reg( 'pAs', 'moderno' )
reg( 'pAs', 'mono' )
reg( 'pAs', 'monoico' )
reg( 'pAs', 'montañoso' )
reg( 'pAs', 'monárquico' )
reg( 'pAs', 'monástico' )
reg( 'pAs', 'morfológico' )
reg( 'pAs', 'morisco' )
reg( 'pAs', 'mucho', 'muchísimo', 'muchísima', 'muchísimos', 'muchísimas' )
reg( 'pAs', 'muerto' )
reg( 'pAs', 'muñeco' )
reg( 'pAs', 'mágico' )
reg( 'pAs', 'máximo' )
reg( 'pAs', 'médico' )
reg( 'pAs', 'métrico' )
reg( 'pAs', 'mínimo' )
reg( 'pAs', 'místico' )
reg( 'pAs', 'mítico' )
reg( 'pAs', 'músico' )
reg( 'pAs', 'napoleónico' )
reg( 'pAs', 'narrado' )
reg( 'pAs', 'nativo' )
reg( 'pAs', 'necesario' )
reg( 'pAs', 'negativo' )
reg( 'pAs', 'negociado' )
reg( 'pAs', 'negro' )
reg( 'pAs', 'neoclásico' )
reg( 'pAs', 'neolítico' )
reg( 'pAs', 'nervioso' )
reg( 'pAs', 'neumático' )
reg( 'pAs', 'neurológico' )
reg( 'pAs', 'neutro' )
reg( 'pAs', 'nieto' )
reg( 'pAs', 'niño' )
reg( 'pAs', 'nocturno' )
reg( 'pAs', 'norteamericano' )
reg( 'pAs', 'noruego' )
reg( 'pAs', 'noveno' )
reg( 'pAs', 'novio' )
reg( 'pAs', 'nucleótido' )
reg( 'pAs', 'nuevo' )
reg( 'pAs', 'numeroso', 'numerosísimo', 'numerosísima', 'numerosísimos', 'numerosísimas' )
reg( 'pAs', 'numérico' )
reg( 'pAs', 'náutico' )
reg( 'pAs', 'nórdico' )
reg( 'pAs', 'obrero' )
reg( 'pAs', 'occitano' )
reg( 'pAs', 'oceánico' )
reg( 'pAs', 'octavo' )
reg( 'pAs', 'ofensivo' )
reg( 'pAs', 'olmeco' )
reg( 'pAs', 'olímpico' )
reg( 'pAs', 'onírico' )
reg( 'pAs', 'operativo')
reg( 'pAs', 'operístico' )
reg( 'pAs', 'opuesta' )
reg( 'pAs', 'organoléptico' )
reg( 'pAs', 'orgánico' )
reg( 'pAs', 'orientado' )
reg( 'pAs', 'originario' )
reg( 'pAs', 'orográfico' )
reg( 'pAs', 'ortodoxo' )
reg( 'pAs', 'ortográfico' )
reg( 'pAs', 'oscuro' )
reg( 'pAs', 'otomano' )
reg( 'pAs', 'ovíparo' )
reg( 'pAs', 'pacífico' )
reg( 'pAs', 'paisajístico' )
reg( 'pAs', 'paleohispánico' )
reg( 'pAs', 'paleolítico' )
reg( 'pAs', 'paleontológico' )
reg( 'pAs', 'panorámico' )
reg( 'pAs', 'parabólico' )
reg( 'pAs', 'paraguayo' )
reg( 'pAs', 'paralelo' )
reg( 'pAs', 'parlamentario' )
reg( 'pAs', 'partidario' )
reg( 'pAs', 'patagónico' )
reg( 'pAs', 'patológico' )
reg( 'pAs', 'patriótico' )
reg( 'pAs', 'patrono' )
reg( 'pAs', 'pedagógico' )
reg( 'pAs', 'peligroso' )
reg( 'pAs', 'penúltimo' )
reg( 'pAs', 'peptídico' )
reg( 'pAs', 'pequeñ' )
reg( 'pAs', 'pequeño' )
reg( 'pAs', 'peregrino' )
reg( 'pAs', 'perfecto' )
reg( 'pAs', 'periférico' )
reg( 'pAs', 'periodístico' )
reg( 'pAs', 'periódico' )
reg( 'pAs', 'perseguido')
reg( 'pAs', 'peruano' )
reg( 'pAs', 'pictórico' )
reg( 'pAs', 'pintoresco' )
reg( 'pAs', 'pionero' )
reg( 'pAs', 'pirenaico' )
reg( 'pAs', 'plasmático' )
reg( 'pAs', 'pleno' )
reg( 'pAs', 'plutónico' )
reg( 'pAs', 'plástico' )
reg( 'pAs', 'poderoso' )
reg( 'pAs', 'poetico' )
reg( 'pAs', 'polaco' )
reg( 'pAs', 'policiaco' )
reg( 'pAs', 'policíaco' )
reg( 'pAs', 'polifónico' )
reg( 'pAs', 'polimórfico')
reg( 'pAs', 'polinómico' )
reg( 'pAs', 'pollo' )
reg( 'pAs', 'polémico' )
reg( 'pAs', 'político' )
reg( 'pAs', 'pornográfico' )
reg( 'pAs', 'positivo' )
reg( 'pAs', 'poético' )
reg( 'pAs', 'pragmático' )
reg( 'pAs', 'precioso' )
reg( 'pAs', 'preciso' )
reg( 'pAs', 'predeterminado' )
reg( 'pAs', 'preestablecido' )
reg( 'pAs', 'prehispánico' )
reg( 'pAs', 'prehistórico' )
reg( 'pAs', 'preincaico' )
reg( 'pAs', 'preocupado')
reg( 'pAs', 'presentador' )
reg( 'pAs', 'preso' )
reg( 'pAs', 'prestigioso' )
reg( 'pAs', 'previo' )
reg( 'pAs', 'previsto' )
reg( 'pAs', 'primario' )
reg( 'pAs', 'primero', 'primer' )
reg( 'pAs', 'primigenio' )
reg( 'pAs', 'primitivo' )
reg( 'pAs', 'primo' )
reg( 'pAs', 'prisionero' )
reg( 'pAs', 'privado' )
reg( 'pAs', 'probabilístico' )
reg( 'pAs', 'problemático' )
reg( 'pAs', 'producido' )
reg( 'pAs', 'productivo' )
reg( 'pAs', 'productore' )
reg( 'pAs', 'profundo' )
reg( 'pAs', 'profético' )
reg( 'pAs', 'programático' )
reg( 'pAs', 'progresivo' )
reg( 'pAs', 'prohibido' )
reg( 'pAs', 'propietario' )
reg( 'pAs', 'propio' )
reg( 'pAs', 'protegido' )
reg( 'pAs', 'proteico' )
reg( 'pAs', 'provisto' )
reg( 'pAs', 'proximo' )
reg( 'pAs', 'práctico' )
reg( 'pAs', 'próximo' )
reg( 'pAs', 'pseudocientífico' )
reg( 'pAs', 'psicoanalítico' )
reg( 'pAs', 'psicodélico' )
reg( 'pAs', 'psicológico' )
reg( 'pAs', 'psicotrópico' )
reg( 'pAs', 'psiquiátrico' )
reg( 'pAs', 'psíquico' )
reg( 'pAs', 'publicitario' )
reg( 'pAs', 'pulmonado' )
reg( 'pAs', 'punteado' )
reg( 'pAs', 'puntuado' )
reg( 'pAs', 'puro' )
reg( 'pAs', 'pálido' )
reg( 'pAs', 'pélvico' )
reg( 'pAs', 'público' )
reg( 'pAs', 'púnico' )
reg( 'pAs', 'quinto' )
reg( 'pAs', 'quirúrgico' )
reg( 'pAs', 'químico' )
reg( 'pAs', 'radiofónico' )
reg( 'pAs', 'rapero' )
reg( 'pAs', 'raro' )
reg( 'pAs', 'recogido' )
reg( 'pAs', 'recopilatorio' )
reg( 'pAs', 'recto' )
reg( 'pAs', 'recíproco' )
reg( 'pAs', 'redondeado' )
reg( 'pAs', 'reescrito')
reg( 'pAs', 'relativo' )
reg( 'pAs', 'religioso' )
reg( 'pAs', 'remoto' )
reg( 'pAs', 'renombrado')
reg( 'pAs', 'repetido' )
reg( 'pAs', 'repetitivo' )
reg( 'pAs', 'representativo' )
reg( 'pAs', 'reproductivo' )
reg( 'pAs', 'republicano' )
reg( 'pAs', 'reservado')
reg( 'pAs', 'respectivo' )
reg( 'pAs', 'restringido' )
reg( 'pAs', 'retórico' )
reg( 'pAs', 'reumatológico' )
reg( 'pAs', 'revolucionario' )
reg( 'pAs', 'revuelto' )
reg( 'pAs', 'rico' )
reg( 'pAs', 'riguroso' )
reg( 'pAs', 'robertsoniano' )
reg( 'pAs', 'robusto' )
reg( 'pAs', 'robótico' )
reg( 'pAs', 'rocoso' )
reg( 'pAs', 'rojizo' )
reg( 'pAs', 'rojo' )
reg( 'pAs', 'romano' )
reg( 'pAs', 'románico' )
reg( 'pAs', 'romántico' )
reg( 'pAs', 'rumano' )
reg( 'pAs', 'ruso' )
reg( 'pAs', 'rápido' )
reg( 'pAs', 'rígido' )
reg( 'pAs', 'río' )
reg( 'pAs', 'rítmico' )
reg( 'pAs', 'rúnico' )
reg( 'pAs', 'rústico' )
reg( 'pAs', 'sabio' )
reg( 'pAs', 'sagrado' )
reg( 'pAs', 'salomónico' )
reg( 'pAs', 'sanitario' )
reg( 'pAs', 'satírico' )
reg( 'pAs', 'secreto' )
reg( 'pAs', 'secundario' )
reg( 'pAs', 'segundo' )
reg( 'pAs', 'seguro')
reg( 'pAs', 'selectivo' )
reg( 'pAs', 'selenográfico' )
reg( 'pAs', 'selvático' )
reg( 'pAs', 'semiautomático' )
reg( 'pAs', 'semántico' )
reg( 'pAs', 'semítico' )
reg( 'pAs', 'sencillo' )
reg( 'pAs', 'serbio' )
reg( 'pAs', 'serio')
reg( 'pAs', 'servidor')
reg( 'pAs', 'severo' )
reg( 'pAs', 'sexto' )
reg( 'pAs', 'siderúrgico' )
reg( 'pAs', 'significativo' )
reg( 'pAs', 'simbiogenético' )
reg( 'pAs', 'simbiótico' )
reg( 'pAs', 'simbólico' )
reg( 'pAs', 'simpático' )
reg( 'pAs', 'simultáneo' )
reg( 'pAs', 'simétrico' )
reg( 'pAs', 'sinfónico' )
reg( 'pAs', 'sintáctico' )
reg( 'pAs', 'sintético' )
reg( 'pAs', 'sináptico' )
reg( 'pAs', 'sinítico' )
reg( 'pAs', 'sistemático' )
reg( 'pAs', 'sistémico' )
reg( 'pAs', 'soberano' )
reg( 'pAs', 'sobrino' )
reg( 'pAs', 'socio' )
reg( 'pAs', 'socioeconómico' )
reg( 'pAs', 'sociológico' )
reg( 'pAs', 'solitario' )
reg( 'pAs', 'solo' )
reg( 'pAs', 'sometido' )
reg( 'pAs', 'somático' )
reg( 'pAs', 'sonoro' )
reg( 'pAs', 'sospechoso')
reg( 'pAs', 'sostenido' )
reg( 'pAs', 'soviético' )
reg( 'pAs', 'subacuático' )
reg( 'pAs', 'subantártico' )
reg( 'pAs', 'subatómico' )
reg( 'pAs', 'subsimbólico' )
reg( 'pAs', 'subterráneo' )
reg( 'pAs', 'sucesivo' )
reg( 'pAs', 'sueco' )
reg( 'pAs', 'suizo' )
reg( 'pAs', 'sujeto' )
reg( 'pAs', 'suministrado' )
reg( 'pAs', 'supersónico' )
reg( 'pAs', 'supervisor' )
reg( 'pAs', 'séptimo' )
reg( 'pAs', 'síncrono' )
reg( 'pAs', 'sísmico' )
reg( 'pAs', 'sólido' )
reg( 'pAs', 'tardío' )
reg( 'pAs', 'taxonómico' )
reg( 'pAs', 'tecnico' )
reg( 'pAs', 'tecnológico' )
reg( 'pAs', 'tectónico' )
reg( 'pAs', 'telefónico' )
reg( 'pAs', 'telegráfico' )
reg( 'pAs', 'telescópico' )
reg( 'pAs', 'televisivo' )
reg( 'pAs', 'temprano' )
reg( 'pAs', 'temático' )
reg( 'pAs', 'teológico' )
reg( 'pAs', 'terapéutico' )
reg( 'pAs', 'tercero', 'tercer' )
reg( 'pAs', 'termodinámico' )
reg( 'pAs', 'termoeléctrico' )
reg( 'pAs', 'termoiónico' )
reg( 'pAs', 'teórico' )
reg( 'pAs', 'tipográfico' )
reg( 'pAs', 'tlaxcalteco' )
reg( 'pAs', 'tolerado' )
reg( 'pAs', 'tolteco' )
reg( 'pAs', 'topográfico' )
reg( 'pAs', 'topológico' )
reg( 'pAs', 'toponímico' )
reg( 'pAs', 'torácico' )
reg( 'pAs', 'tosco' )
reg( 'pAs', 'transgénico' )
reg( 'pAs', 'trasero' )
reg( 'pAs', 'traumático' )
reg( 'pAs', 'trigonométrico' )
reg( 'pAs', 'troyano')
reg( 'pAs', 'trágico' )
reg( 'pAs', 'turco' )
reg( 'pAs', 'turístico' )
reg( 'pAs', 'táctico' )
reg( 'pAs', 'técnico' )
reg( 'pAs', 'térmico' )
reg( 'pAs', 'tío' )
reg( 'pAs', 'típico' )
reg( 'pAs', 'tónico' )
reg( 'pAs', 'tóxico' )
reg( 'pAs', 'túrquico' )
reg( 'pAs', 'ucraniano' )
reg( 'pAs', 'unitario' )
reg( 'pAs', 'universitario' )
reg( 'pAs', 'uno' )
reg( 'pAs', 'urbano' )
reg( 'pAs', 'urbanístico' )
reg( 'pAs', 'uruguayo' )
reg( 'pAs', 'urálico' )
reg( 'pAs', 'utilitario' )
reg( 'pAs', 'utópico' )
reg( 'pAs', 'vacío' )
reg( 'pAs', 'valioso', 'valiosísimo', 'valiosísima', 'valiosísimos', 'valiosísimas' )
reg( 'pAs', 'vampiro' )
reg( 'pAs', 'vampírico' )
reg( 'pAs', 'vandálico' )
reg( 'pAs', 'variado' )
reg( 'pAs', 'vasco' )
reg( 'pAs', 'vascófono' )
reg( 'pAs', 'vecino' )
reg( 'pAs', 'venezolano' )
reg( 'pAs', 'verdadero' )
reg( 'pAs', 'veterano' )
reg( 'pAs', 'viajero' )
reg( 'pAs', 'vicario' )
reg( 'pAs', 'viejo')
reg( 'pAs', 'vigoroso' )
reg( 'pAs', 'vikingo' )
reg( 'pAs', 'villano' )
reg( 'pAs', 'viudo' )
reg( 'pAs', 'vivo' )
reg( 'pAs', 'volcánico' )
reg( 'pAs', 'voluminoso')
reg( 'pAs', 'vírico' )
reg( 'pAs', 'zacateco' )
reg( 'pAs', 'zapoteco' )
reg( 'pAs', 'ácido' )
reg( 'pAs', 'ártico' )
reg( 'pAs', 'élfico' )
reg( 'pAs', 'épico' )
reg( 'pAs', 'éste' )
reg( 'pAs', 'ético' )
reg( 'pAs', 'étnico' )
reg( 'pAs', 'íntimo' )
reg( 'pAs', 'óptico' )
reg( 'pAs', 'óptimo' )
reg( 'pAs', 'último' )
reg( 'pAs', 'único' )
reg( 'pCes', 'acidez' )
reg( 'pCes', 'alférez' )
reg( 'pCes', 'altavoz' )
reg( 'pCes', 'andaluz' )
reg( 'pCes', 'aprendiz' )
reg( 'pCes', 'arroz' )
reg( 'pCes', 'audaz' )
reg( 'pCes', 'automotriz' )
reg( 'pCes', 'capaz')
reg( 'pCes', 'cicatriz' )
reg( 'pCes', 'cruz' )
reg( 'pCes', 'cáliz' )
reg( 'pCes', 'disfraz' )
reg( 'pCes', 'eficaz' )
reg( 'pCes', 'emperatriz' )
reg( 'pCes', 'estupidez' )
reg( 'pCes', 'faz' )
reg( 'pCes', 'feliz' )
reg( 'pCes', 'feroz' )
reg( 'pCes', 'fluidez' )
reg( 'pCes', 'fugaz' )
reg( 'pCes', 'haz' )
reg( 'pCes', 'incapaz' )
reg( 'pCes', 'infeliz' )
reg( 'pCes', 'interfaz' )
reg( 'pCes', 'juez' )
reg( 'pCes', 'liquidez' )
reg( 'pCes', 'luz' )
reg( 'pCes', 'lápiz' )
reg( 'pCes', 'matiz' )
reg( 'pCes', 'matriz' )
reg( 'pCes', 'maíz' )
reg( 'pCes', 'motriz' )
reg( 'pCes', 'nariz' )
reg( 'pCes', 'niñez' )
reg( 'pCes', 'nuez' )
reg( 'pCes', 'paz' )
reg( 'pCes', 'perdiz' )
reg( 'pCes', 'pez' )
reg( 'pCes', 'portavoz' )
reg( 'pCes', 'precoz' )
reg( 'pCes', 'rapidez' )
reg( 'pCes', 'raíz' )
reg( 'pCes', 'rigidez' )
reg( 'pCes', 'sencillez' )
reg( 'pCes', 'solidez' )
reg( 'pCes', 'tapiz' )
reg( 'pCes', 'tenaz' )
reg( 'pCes', 'validez' )
reg( 'pCes', 'vejez' )
reg( 'pCes', 'veloz' )
reg( 'pCes', 'vez' )
reg( 'pCes', 'voz' )
reg( 'pE', 'programador' )
reg( 'pEs', 'abdominal' )
reg( 'pEs', 'aborígen' )
reg( 'pEs', 'accesibilidad' )
reg( 'pEs', 'actitud' )
reg( 'pEs', 'actividad' )
reg( 'pEs', 'actor', 'actriz', 'actrices' )
reg( 'pEs', 'actual')
reg( 'pEs', 'actualidad' )
reg( 'pEs', 'adicional' )
reg( 'pEs', 'afinidad' )
reg( 'pEs', 'agilidad' )
reg( 'pEs', 'agresividad' )
reg( 'pEs', 'agricultor' )
reg( 'pEs', 'alcohol' )
reg( 'pEs', 'alrededor' )
reg( 'pEs', 'altar' )
reg( 'pEs', 'altitud' )
reg( 'pEs', 'ambiental' )
reg( 'pEs', 'ambigüedad' )
reg( 'pEs', 'amistad' )
reg( 'pEs', 'amor' )
reg( 'pEs', 'ancestral' )
reg( 'pEs', 'angular' )
reg( 'pEs', 'animal' )
reg( 'pEs', 'ansiedad' )
reg( 'pEs', 'anterior' )
reg( 'pEs', 'anterioridad' )
reg( 'pEs', 'antigüedad' )
reg( 'pEs', 'anual' )
reg( 'pEs', 'artificial' )
reg( 'pEs', 'asexual' )
reg( 'pEs', 'atrocidad' )
reg( 'pEs', 'audiovisual' )
reg( 'pEs', 'austeridad' )
reg( 'pEs', 'autenticidad' )
reg( 'pEs', 'automóvil' )
reg( 'pEs', 'autor' )
reg( 'pEs', 'autoridad' )
reg( 'pEs', 'auxiliar' )
reg( 'pEs', 'axial' )
reg( 'pEs', 'azul' )
reg( 'pEs', 'bar' )
reg( 'pEs', 'bicolor' )
reg( 'pEs', 'bien')
reg( 'pEs', 'binomial' )
reg( 'pEs', 'biodiversidad' )
reg( 'pEs', 'bisel', 'biseles' )
reg( 'pEs', 'bondad' )
reg( 'pEs', 'branquial' )
reg( 'pEs', 'bus', 'buses')
reg( 'pEs', 'cadáver' )
reg( 'pEs', 'calidad' )
reg( 'pEs', 'canal' )
reg( 'pEs', 'canciller' )
reg( 'pEs', 'cantidad' )
reg( 'pEs', 'capacidad' )
reg( 'pEs', 'capital' )
reg( 'pEs', 'cardenal' )
reg( 'pEs', 'caridad' )
reg( 'pEs', 'cartel' )
reg( 'pEs', 'casualidad' )
reg( 'pEs', 'catastral' )
reg( 'pEs', 'caudal' )
reg( 'pEs', 'cautividad' )
reg( 'pEs', 'cavidad' )
reg( 'pEs', 'cavidad' )
reg( 'pEs', 'celebridad' )
reg( 'pEs', 'celebridad' )
reg( 'pEs', 'celular' )
reg( 'pEs', 'central' )
reg( 'pEs', 'cereal' )
reg( 'pEs', 'cerebral' )
reg( 'pEs', 'ceremonial' )
reg( 'pEs', 'certamen', 'certámenes' )
reg( 'pEs', 'cibercriminal')
reg( 'pEs', 'ciudad' )
reg( 'pEs', 'civil' )
reg( 'pEs', 'clan' )
reg( 'pEs', 'clandestinidad' )
reg( 'pEs', 'claridad' )
reg( 'pEs', 'club' )
reg( 'pEs', 'coautor' )
reg( 'pEs', 'coctel' )
reg( 'pEs', 'colaborador' )
reg( 'pEs', 'colectividad' )
reg( 'pEs', 'colisión')
reg( 'pEs', 'colonial' )
reg( 'pEs', 'coloquial' )
reg( 'pEs', 'color' )
reg( 'pEs', 'comercial' )
reg( 'pEs', 'comodidad' )
reg( 'pEs', 'compatibilidad' )
reg( 'pEs', 'competitividad' )
reg( 'pEs', 'complicidad' )
reg( 'pEs', 'compositor' )
reg( 'pEs', 'computacional' )
reg( 'pEs', 'comunidad' )
reg( 'pEs', 'concejal' )
reg( 'pEs', 'conceptual' )
reg( 'pEs', 'conductividad' )
reg( 'pEs', 'conectividad' )
reg( 'pEs', 'conformidad' )
reg( 'pEs', 'conservador' )
reg( 'pEs', 'constitucional' )
reg( 'pEs', 'contabilidad' )
reg( 'pEs', 'continental' )
reg( 'pEs', 'continuidad' )
reg( 'pEs', 'control' )
reg( 'pEs', 'convencional')
reg( 'pEs', 'coral' )
reg( 'pEs', 'corporal' )
reg( 'pEs', 'creador' )
reg( 'pEs', 'creatividad' )
reg( 'pEs', 'credencial' )
reg( 'pEs', 'credibilidad' )
reg( 'pEs', 'criminal' )
reg( 'pEs', 'cristal' )
reg( 'pEs', 'crueldad' )
reg( 'pEs', 'cráter' )
reg( 'pEs', 'crímen' )
reg( 'pEs', 'cual' )
reg( 'pEs', 'cualidad' )
reg( 'pEs', 'cuartel' )
reg( 'pEs', 'culpabilidad' )
reg( 'pEs', 'cultural' )
reg( 'pEs', 'curiosidad' )
reg( 'pEs', 'curiosidad' )
reg( 'pEs', 'cuál' )
reg( 'pEs', 'cáncer' )
reg( 'pEs', 'cárcel' )
reg( 'pEs', 'cóndor' )
reg( 'pEs', 'cónsul' )
reg( 'pEs', 'debilidad' )
reg( 'pEs', 'debilidad' )
reg( 'pEs', 'decimal' )
reg( 'pEs', 'deidad' )
reg( 'pEs', 'deidad' )
reg( 'pEs', 'densidad' )
reg( 'pEs', 'departamental' )
reg( 'pEs', 'desigualdad' )
reg( 'pEs', 'destructor' )
reg( 'pEs', 'dificultad' )
reg( 'pEs', 'difícil' )
reg( 'pEs', 'digital' )
reg( 'pEs', 'dignidad' )
reg( 'pEs', 'discapacidad' )
reg( 'pEs', 'disciplinar' )
reg( 'pEs', 'discontinuidad' )
reg( 'pEs', 'disponibilidad' )
reg( 'pEs', 'diversidad' )
reg( 'pEs', 'divinidad' )
reg( 'pEs', 'divinidad' )
reg( 'pEs', 'doctoral' )
reg( 'pEs', 'documental' )
reg( 'pEs', 'dorsal' )
reg( 'pEs', 'dualidad' )
reg( 'pEs', 'débil' )
reg( 'pEs', 'dólar')
reg( 'pEs', 'edad' )
reg( 'pEs', 'editorial' )
reg( 'pEs', 'efectividad' )
reg( 'pEs', 'ejemplar' )
reg( 'pEs', 'elasticidad' )
reg( 'pEs', 'electoral' )
reg( 'pEs', 'electricidad' )
reg( 'pEs', 'emocional' )
reg( 'pEs', 'emperador' )
reg( 'pEs', 'empresarial')
reg( 'pEs', 'enfermedad' )
reg( 'pEs', 'entidad' )
reg( 'pEs', 'episcopal' )
reg( 'pEs', 'equidad' )
reg( 'pEs', 'error' )
reg( 'pEs', 'escalar' )
reg( 'pEs', 'escolar' )
reg( 'pEs', 'escritor' )
reg( 'pEs', 'esencial' )
reg( 'pEs', 'eslabon' )
reg( 'pEs', 'espacial' )
reg( 'pEs', 'especial' )
reg( 'pEs', 'especialidad' )
reg( 'pEs', 'espectador' )
reg( 'pEs', 'espectral' )
reg( 'pEs', 'especímen' )
reg( 'pEs', 'espiral' )
reg( 'pEs', 'espiritual' )
reg( 'pEs', 'espiritualidad' )
reg( 'pEs', 'esquí', 'esquís' )
reg( 'pEs', 'estabilidad' )
reg( 'pEs', 'estatal' )
reg( 'pEs', 'estructural' )
reg( 'pEs', 'estudiantil' )
reg( 'pEs', 'estándar' )
reg( 'pEs', 'estéril' )
reg( 'pEs', 'eternidad' )
reg( 'pEs', 'excentricidad' )
reg( 'pEs', 'excepcional' )
reg( 'pEs', 'exclusividad' )
reg( 'pEs', 'experimental' )
reg( 'pEs', 'exterior' )
reg( 'pEs', 'extremidad' )
reg( 'pEs', 'facilidad' )
reg( 'pEs', 'factor')
reg( 'pEs', 'facultad' )
reg( 'pEs', 'falsedad' )
reg( 'pEs', 'familiar' )
reg( 'pEs', 'favor' )
reg( 'pEs', 'fecundidad' )
reg( 'pEs', 'federal' )
reg( 'pEs', 'felicidad' )
reg( 'pEs', 'ferrocarril' )
reg( 'pEs', 'fertilidad' )
reg( 'pEs', 'festival' )
reg( 'pEs', 'festividad' )
reg( 'pEs', 'fiabilidad' )
reg( 'pEs', 'fidelidad' )
reg( 'pEs', 'fiel' )
reg( 'pEs', 'filial' )
reg( 'pEs', 'fin' )
reg( 'pEs', 'final' )
reg( 'pEs', 'finalidad' )
reg( 'pEs', 'fiscal' )
reg( 'pEs', 'flexibilidad' )
reg( 'pEs', 'flor' )
reg( 'pEs', 'fluvial' )
reg( 'pEs', 'forestal' )
reg( 'pEs', 'formal' )
reg( 'pEs', 'fraternidad' )
reg( 'pEs', 'frontal' )
reg( 'pEs', 'funcional' )
reg( 'pEs', 'funcionalidad' )
reg( 'pEs', 'fundador' )
reg( 'pEs', 'fundamental' )
reg( 'pEs', 'funeral' )
reg( 'pEs', 'fusil' )
reg( 'pEs', 'fácil' )
reg( 'pEs', 'fértil' )
reg( 'pEs', 'fósil' )
reg( 'pEs', 'ganador' )
reg( 'pEs', 'gas' )
reg( 'pEs', 'gen' )
reg( 'pEs', 'general' )
reg( 'pEs', 'generosidad' )
reg( 'pEs', 'glaciar' )
reg( 'pEs', 'global' )
reg( 'pEs', 'gol' )
reg( 'pEs', 'gradual' )
reg( 'pEs', 'gravedad' )
reg( 'pEs', 'gris' )
reg( 'pEs', 'gubernamental')
reg( 'pEs', 'habilidad' )
reg( 'pEs', 'habitual' )
reg( 'pEs', 'hacedor' )
reg( 'pEs', 'hermandad' )
reg( 'pEs', 'historiador' )
reg( 'pEs', 'historial' )
reg( 'pEs', 'hogar' )
reg( 'pEs', 'homosexual' )
reg( 'pEs', 'honestidad' )
reg( 'pEs', 'honor' )
reg( 'pEs', 'horizontal' )
reg( 'pEs', 'horror' )
reg( 'pEs', 'hospital' )
reg( 'pEs', 'hostilidad' )
reg( 'pEs', 'hostilidad' )
reg( 'pEs', 'hotel' )
reg( 'pEs', 'humanidad' )
reg( 'pEs', 'humedad' )
reg( 'pEs', 'humildad' )
reg( 'pEs', 'humor' )
reg( 'pEs', 'ideal' )
reg( 'pEs', 'identidad' )
reg( 'pEs', 'igual')
reg( 'pEs', 'igualdad' )
reg( 'pEs', 'ilegal' )
reg( 'pEs', 'impar' )
reg( 'pEs', 'imperial' )
reg( 'pEs', 'imposibilidad' )
reg( 'pEs', 'inactividad' )
reg( 'pEs', 'inaugural' )
reg( 'pEs', 'incapacidad' )
reg( 'pEs', 'incremental')
reg( 'pEs', 'individual' )
reg( 'pEs', 'industrial' )
reg( 'pEs', 'inestabilidad' )
reg( 'pEs', 'infantil' )
reg( 'pEs', 'inferior' )
reg( 'pEs', 'inferioridad' )
reg( 'pEs', 'infidelidad' )
reg( 'pEs', 'infinidad' )
reg( 'pEs', 'informal' )
reg( 'pEs', 'inicial' )
reg( 'pEs', 'inmortalidad' )
reg( 'pEs', 'inmunidad' )
reg( 'pEs', 'innovación')
reg( 'pEs', 'inseguridad' )
reg( 'pEs', 'institucional' )
reg( 'pEs', 'instrumental' )
reg( 'pEs', 'integral' )
reg( 'pEs', 'intelectual' )
reg( 'pEs', 'intensidad' )
reg( 'pEs', 'intercensal' )
reg( 'pEs', 'interestatal' )
reg( 'pEs', 'interior' )
reg( 'pEs', 'internacional' )
reg( 'pEs', 'interés' )
reg( 'pEs', 'intimidad' )
reg( 'pEs', 'inusual' )
reg( 'pEs', 'invasor' )
reg( 'pEs', 'investigador' )
reg( 'pEs', 'irregular' )
reg( 'pEs', 'irregularidad' )
reg( 'pEs', 'israelí' )
reg( 'pEs', 'iteración' )
reg( 'pEs', 'judicial' )
reg( 'pEs', 'jugabilidad' )
reg( 'pEs', 'jugador' )
reg( 'pEs', 'juvenil' )
reg( 'pEs', 'juventud' )
reg( 'pEs', 'laboral' )
reg( 'pEs', 'lateral' )
reg( 'pEs', 'latitud' )
reg( 'pEs', 'leal' )
reg( 'pEs', 'lealtad' )
reg( 'pEs', 'legal' )
reg( 'pEs', 'legalidad' )
reg( 'pEs', 'legitimidad' )
reg( 'pEs', 'ley')
reg( 'pEs', 'liberal' )
reg( 'pEs', 'libertad' )
reg( 'pEs', 'lineal' )
reg( 'pEs', 'literal' )
reg( 'pEs', 'litoral' )
reg( 'pEs', 'local' )
reg( 'pEs', 'localidad' )
reg( 'pEs', 'longevidad' )
reg( 'pEs', 'lugar')
reg( 'pEs', 'luminosidad' )
reg( 'pEs', 'lunar' )
reg( 'pEs', 'lápic' )
reg( 'pEs', 'líder' )
reg( 'pEs', 'magnitud' )
reg( 'pEs', 'mal' )
reg( 'pEs', 'maldad' )
reg( 'pEs', 'mancomunidad' )
reg( 'pEs', 'manual' )
reg( 'pEs', 'mar' )
reg( 'pEs', 'marcial' )
reg( 'pEs', 'mariscal' )
reg( 'pEs', 'material' )
reg( 'pEs', 'maternidad' )
reg( 'pEs', 'mayor' )
reg( 'pEs', 'medicinal' )
reg( 'pEs', 'medieval' )
reg( 'pEs', 'menor' )
reg( 'pEs', 'mensual')
reg( 'pEs', 'mental' )
reg( 'pEs', 'mentalidad' )
reg( 'pEs', 'meridional' )
reg( 'pEs', 'mes')
reg( 'pEs', 'metal' )
reg( 'pEs', 'metalicidad' )
reg( 'pEs', 'miel' )
reg( 'pEs', 'mil' )
reg( 'pEs', 'militar' )
reg( 'pEs', 'mineral' )
reg( 'pEs', 'misil' )
reg( 'pEs', 'mitad' )
reg( 'pEs', 'modalidad' )
reg( 'pEs', 'modernidad' )
reg( 'pEs', 'molecular' )
reg( 'pEs', 'monumental' )
reg( 'pEs', 'moral' )
reg( 'pEs', 'moralidad' )
reg( 'pEs', 'mortal' )
reg( 'pEs', 'mortalidad' )
reg( 'pEs', 'motor' )
reg( 'pEs', 'mujer' )
reg( 'pEs', 'multicelular' )
reg( 'pEs', 'multijugador' )
reg( 'pEs', 'multitud' )
reg( 'pEs', 'mundial' )
reg( 'pEs', 'municipal' )
reg( 'pEs', 'municipalidad' )
reg( 'pEs', 'mural' )
reg( 'pEs', 'musical' )
reg( 'pEs', 'mármol' )
reg( 'pEs', 'mártir' )
reg( 'pEs', 'mísil' )
reg( 'pEs', 'móvil' )
reg( 'pEs', 'nacional')
reg( 'pEs', 'nacionalidad' )
reg( 'pEs', 'natal' )
reg( 'pEs', 'natalidad' )
reg( 'pEs', 'natural', 'naturales' )
reg( 'pEs', 'naval' )
reg( 'pEs', 'navidad' )
reg( 'pEs', 'necesidad' )
reg( 'pEs', 'neuronal' )
reg( 'pEs', 'neutral' )
reg( 'pEs', 'neutralidad' )
reg( 'pEs', 'neutron' )
reg( 'pEs', 'nivel' )
reg( 'pEs', 'normal' )
reg( 'pEs', 'normalidad' )
reg( 'pEs', 'notoriedad' )
reg( 'pEs', 'novedad' )
reg( 'pEs', 'novel' )
reg( 'pEs', 'nuclear' )
reg( 'pEs', 'obesidad' )
reg( 'pEs', 'objetividad' )
reg( 'pEs', 'occidental' )
reg( 'pEs', 'oficial')
reg( 'pEs', 'oficialidad' )
reg( 'pEs', 'olor' )
reg( 'pEs', 'opcional' )
reg( 'pEs', 'oportunidad' )
reg( 'pEs', 'oral' )
reg( 'pEs', 'orbital' )
reg( 'pEs', 'ordenador' )
reg( 'pEs', 'oriental' )
reg( 'pEs', 'original' )
reg( 'pEs', 'originalidad' )
reg( 'pEs', 'oscuridad' )
reg( 'pEs', 'pan' )
reg( 'pEs', 'papel' )
reg( 'pEs', 'par' )
reg( 'pEs', 'parcial' )
reg( 'pEs', 'pared' )
reg( 'pEs', 'paridad' )
reg( 'pEs', 'parroquial' )
reg( 'pEs', 'particular' )
reg( 'pEs', 'particularidad' )
reg( 'pEs', 'particularidad' )
reg( 'pEs', 'paternidad' )
reg( 'pEs', 'patronal' )
reg( 'pEs', 'país' )
reg( 'pEs', 'peculiar' )
reg( 'pEs', 'peculiaridad' )
reg( 'pEs', 'peculiaridad' )
reg( 'pEs', 'penal' )
reg( 'pEs', 'peor' )
reg( 'pEs', 'perfil' )
reg( 'pEs', 'periodicidad' )
reg( 'pEs', 'perjudicial' )
reg( 'pEs', 'personal', 'personalísimo', 'personalísima', 'personalísimos', 'personalísimas' )
reg( 'pEs', 'personalidad' )
reg( 'pEs', 'piedad' )
reg( 'pEs', 'piel' )
reg( 'pEs', 'pilar' )
reg( 'pEs', 'pincel' )
reg( 'pEs', 'pintor' )
reg( 'pEs', 'plan')
reg( 'pEs', 'plantel' )
reg( 'pEs', 'poblacional' )
reg( 'pEs', 'poblador' )
reg( 'pEs', 'poder' )
reg( 'pEs', 'policial' )
reg( 'pEs', 'poligonal')
reg( 'pEs', 'popular' )
reg( 'pEs', 'popularidad' )
reg( 'pEs', 'portal' )
reg( 'pEs', 'portátil')
reg( 'pEs', 'posibilidad' )
reg( 'pEs', 'postal' )
reg( 'pEs', 'posterior' )
reg( 'pEs', 'posterioridad' )
reg( 'pEs', 'potencial' )
reg( 'pEs', 'preliminar' )
reg( 'pEs', 'prenatal' )
reg( 'pEs', 'presencial' )
reg( 'pEs', 'presidencial' )
reg( 'pEs', 'principal' )
reg( 'pEs', 'prioridad' )
reg( 'pEs', 'privacidad' )
reg( 'pEs', 'probabilidad' )
reg( 'pEs', 'productividad' )
reg( 'pEs', 'productor' )
reg( 'pEs', 'profesional' )
reg( 'pEs', 'profundidad' )
reg( 'pEs', 'promocional' )
reg( 'pEs', 'propiedad' )
reg( 'pEs', 'prosperidad' )
reg( 'pEs', 'provincial' )
reg( 'pEs', 'provisional' )
reg( 'pEs', 'proximidad' )
reg( 'pEs', 'proyectil' )
reg( 'pEs', 'pseudogen' )
reg( 'pEs', 'publicidad' )
reg( 'pEs', 'píxel' )
reg( 'pEs', 'quien' )
reg( 'pEs', 'radar' )
reg( 'pEs', 'radial' )
reg( 'pEs', 'radical' )
reg( 'pEs', 'ramal' )
reg( 'pEs', 'reactor' )
reg( 'pEs', 'real' )
reg( 'pEs', 'realidad' )
reg( 'pEs', 'receptor' )
reg( 'pEs', 'rectangular' )
reg( 'pEs', 'red' )
reg( 'pEs', 'regional' )
reg( 'pEs', 'regular' )
reg( 'pEs', 'regularidad' )
reg( 'pEs', 'relatividad' )
reg( 'pEs', 'religiosidad' )
reg( 'pEs', 'reloj' )
reg( 'pEs', 'rentabilidad' )
reg( 'pEs', 'reptil' )
reg( 'pEs', 'residencial' )
reg( 'pEs', 'responsabilidad' )
reg( 'pEs', 'rey' )
reg( 'pEs', 'ritual' )
reg( 'pEs', 'rival' )
reg( 'pEs', 'rivalidad' )
reg( 'pEs', 'rol' )
reg( 'pEs', 'rumor' )
reg( 'pEs', 'rural' )
reg( 'pEs', 'sabor' )
reg( 'pEs', 'sal' )
reg( 'pEs', 'salinidad' )
reg( 'pEs', 'sanidad' )
reg( 'pEs', 'santidad' )
reg( 'pEs', 'sector')
reg( 'pEs', 'secuencial' )
reg( 'pEs', 'secular' )
reg( 'pEs', 'semanal')
reg( 'pEs', 'semiestéril' )
reg( 'pEs', 'semifinal' )
reg( 'pEs', 'sensibilidad' )
reg( 'pEs', 'sensor' )
reg( 'pEs', 'septentrional' )
reg( 'pEs', 'serial' )
reg( 'pEs', 'seriedad' )
reg( 'pEs', 'severidad' )
reg( 'pEs', 'sexual' )
reg( 'pEs', 'sexualidad' )
reg( 'pEs', 'señal' )
reg( 'pEs', 'similar' )
reg( 'pEs', 'similitud' )
reg( 'pEs', 'simple' )
reg( 'pEs', 'simplicidad' )
reg( 'pEs', 'singular' )
reg( 'pEs', 'singularidad' )
reg( 'pEs', 'sismicidad' )
reg( 'pEs', 'sobrenatural' )
reg( 'pEs', 'social' )
reg( 'pEs', 'sociedad' )
reg( 'pEs', 'sol' )
reg( 'pEs', 'solar' )
reg( 'pEs', 'solicitud' )
reg( 'pEs', 'solidaridad' )
reg( 'pEs', 'sostenibilidad' )
reg( 'pEs', 'subeditor' )
reg( 'pEs', 'subnacional' )
reg( 'pEs', 'subtropical' )
reg( 'pEs', 'sucesor' )
reg( 'pEs', 'superficial' )
reg( 'pEs', 'superior' )
reg( 'pEs', 'superioridad' )
reg( 'pEs', 'sustancial' )
reg( 'pEs', 'sutil' )
reg( 'pEs', 'símil' )
reg( 'pEs', 'taller' )
reg( 'pEs', 'tambor' )
reg( 'pEs', 'teatral' )
reg( 'pEs', 'temor' )
reg( 'pEs', 'temporal' )
reg( 'pEs', 'tenor' )
reg( 'pEs', 'terminal' )
reg( 'pEs', 'territorial' )
reg( 'pEs', 'terror' )
reg( 'pEs', 'textil' )
reg( 'pEs', 'textual' )
reg( 'pEs', 'titularidad' )
reg( 'pEs', 'tonalidad' )
reg( 'pEs', 'tonalidad' )
reg( 'pEs', 'total' )
reg( 'pEs', 'toxicidad' )
reg( 'pEs', 'trabajador' )
reg( 'pEs', 'tradicional' )
reg( 'pEs', 'tranquilidad' )
reg( 'pEs', 'transicional' )
reg( 'pEs', 'transversal' )
reg( 'pEs', 'tren' )
reg( 'pEs', 'tribunal' )
reg( 'pEs', 'tridimensional' )
reg( 'pEs', 'tropical' )
reg( 'pEs', 'túnel' )
reg( 'pEs', 'umbral' )
reg( 'pEs', 'unanimidad' )
reg( 'pEs', 'unicelular' )
reg( 'pEs', 'unidad' )
reg( 'pEs', 'uniformidad' )
reg( 'pEs', 'universal' )
reg( 'pEs', 'universidad' )
reg( 'pEs', 'utilidad' )
reg( 'pEs', 'valor' )
reg( 'pEs', 'vanidad' )
reg( 'pEs', 'vapor' )
reg( 'pEs', 'variabilidad' )
reg( 'pEs', 'variacion' )
reg( 'pEs', 'variedad' )
reg( 'pEs', 'vascular' )
reg( 'pEs', 'vecindad' )
reg( 'pEs', 'vector' )
reg( 'pEs', 'vectorial' )
reg( 'pEs', 'vegetal' )
reg( 'pEs', 'velocidad' )
reg( 'pEs', 'veracidad' )
reg( 'pEs', 'verdad' )
reg( 'pEs', 'verificabilidad' )
reg( 'pEs', 'versatilidad' )
reg( 'pEs', 'versátil' )
reg( 'pEs', 'vertical' )
reg( 'pEs', 'vestigial' )
reg( 'pEs', 'viabilidad' )
reg( 'pEs', 'virrey' )
reg( 'pEs', 'virtual' )
reg( 'pEs', 'virtud' )
reg( 'pEs', 'visibilidad' )
reg( 'pEs', 'visual' )
reg( 'pEs', 'vital' )
reg( 'pEs', 'vitalidad' )
reg( 'pEs', 'vocal' )
reg( 'pEs', 'voluntad' )
reg( 'pEs', 'vulnerabilidad' )
reg( 'pEs', 'ágil' )
reg( 'pEs', 'álbum' )
reg( 'pEs', 'ángel' )
reg( 'pEs', 'árbol' )
reg( 'pEs', 'útil' )
reg( 'pOnes',  'adaptación', 'adaptaciones' )
reg( 'pOnes',  'adivinación', 'adivinaciones' )
reg( 'pOnes',  'aseveración', 'aseveraciones' )
reg( 'pOnes',  'automatización', 'automatizaciones' )
reg( 'pOnes',  'caracterización', 'caracterizaciones' )
reg( 'pOnes',  'computación', 'computaciones' )
reg( 'pOnes',  'cuantificación', 'cuantificaciones' )
reg( 'pOnes',  'delimitación', 'delimitaciones' )
reg( 'pOnes',  'distinción', 'distinciones' )
reg( 'pOnes',  'evolución', 'evoluciones' )
reg( 'pOnes',  'inducción', 'inducciones' )
reg( 'pOnes',  'interocepción', 'interocepciones' )
reg( 'pOnes',  'nocicepción', 'nocicepciones' )
reg( 'pOnes',  'opinión', 'opiniones' )
reg( 'pOnes',  'optimización', 'optimizaciones' )
reg( 'pOnes',  'planificación', 'planificaciones' )
reg( 'pOnes',  'propiocepción', 'propiocepciones' )
reg( 'pOnes',  'reestructuración', 'reestructuraciones' )
reg( 'pOnes',  'retroalimentación', 'retroalimentaciones' )
reg( 'pOnes',  'situación', 'situaciones' )
reg( 'pOnes', 'abdicación' )
reg( 'pOnes', 'aberración' )
reg( 'pOnes', 'ablación' )
reg( 'pOnes', 'ablución', 'abluciones' )
reg( 'pOnes', 'abolición' )
reg( 'pOnes', 'abominación' )
reg( 'pOnes', 'abreviación' )
reg( 'pOnes', 'absolución' )
reg( 'pOnes', 'absorción' )
reg( 'pOnes', 'abstención', 'abstenciones' )
reg( 'pOnes', 'abstracción', 'abstracciones' )
reg( 'pOnes', 'acción' )
reg( 'pOnes', 'aceleración', 'aceleraciones' )
reg( 'pOnes', 'acentuación' )
reg( 'pOnes', 'acepción' )
reg( 'pOnes', 'aceptación' )
reg( 'pOnes', 'aclamación', 'aclamaciones' )
reg( 'pOnes', 'aclaración', 'aclaraciones' )
reg( 'pOnes', 'acotación', 'acotaciones' )
reg( 'pOnes', 'acreditación' )
reg( 'pOnes', 'activación' )
reg( 'pOnes', 'actuación' )
reg( 'pOnes', 'actualización' )
reg( 'pOnes', 'acumulación', 'acumulaciones' )
reg( 'pOnes', 'acusación', 'acusaciones' )
reg( 'pOnes', 'acuñación', 'acuñaciones' )
reg( 'pOnes', 'adaptación' )
reg( 'pOnes', 'adecuación' )
reg( 'pOnes', 'adhesión', 'adhesiones' )
reg( 'pOnes', 'adicción' )
reg( 'pOnes', 'adición' )
reg( 'pOnes', 'adjudicación' )
reg( 'pOnes', 'administración', 'administraciones' )
reg( 'pOnes', 'admiración' )
reg( 'pOnes', 'adopción' )
reg( 'pOnes', 'adoración' )
reg( 'pOnes', 'adquisición' )
reg( 'pOnes', 'adscripción' )
reg( 'pOnes', 'advocación', 'advocaciones' )
reg( 'pOnes', 'afección' )
reg( 'pOnes', 'afectación' )
reg( 'pOnes', 'afición' )
reg( 'pOnes', 'afiliación', 'afiliaciones' )
reg( 'pOnes', 'afinación', 'afinaciones' )
reg( 'pOnes', 'afirmación')
reg( 'pOnes', 'agitación', 'agitaciones' )
reg( 'pOnes', 'aglomeración', 'aglomeraciones' )
reg( 'pOnes', 'aglutinación' )
reg( 'pOnes', 'agregación' )
reg( 'pOnes', 'agresión', 'agresiones' )
reg( 'pOnes', 'agrupación', 'agrupaciones' )
reg( 'pOnes', 'aguijón', 'aguijones' )
reg( 'pOnes', 'aleación' )
reg( 'pOnes', 'alegación', 'alegaciones' )
reg( 'pOnes', 'alerón', 'alerones' )
reg( 'pOnes', 'alfabetización' )
reg( 'pOnes', 'algodón' )
reg( 'pOnes', 'alienación' )
reg( 'pOnes', 'alimentación' )
reg( 'pOnes', 'alineación' )
reg( 'pOnes', 'almidón', 'almidones' )
reg( 'pOnes', 'alocución' )
reg( 'pOnes', 'alteración' )
reg( 'pOnes', 'alucinación' )
reg( 'pOnes', 'alusión', 'alusiones' )
reg( 'pOnes', 'aluvión', 'aluviones' )
reg( 'pOnes', 'ambición' )
reg( 'pOnes', 'ambientación', 'ambientaciones' )
reg( 'pOnes', 'amonestación', 'amonestaciones' )
reg( 'pOnes', 'ampliación' )
reg( 'pOnes', 'amplificación' )
reg( 'pOnes', 'amputación', 'amputaciones' )
reg( 'pOnes', 'anfitrión', 'anfitriones' )
reg( 'pOnes', 'anglosajón', 'anglosajones' )
reg( 'pOnes', 'animación' )
reg( 'pOnes', 'aniquilación' )
reg( 'pOnes', 'anión', 'aniones' )
reg( 'pOnes', 'anotación' )
reg( 'pOnes', 'antelación' )
reg( 'pOnes', 'anticipación' )
reg( 'pOnes', 'anulación' )
reg( 'pOnes', 'apagón', 'apagones' )
reg( 'pOnes', 'aparición' )
reg( 'pOnes', 'apelación', 'apelaciones' )
reg( 'pOnes', 'aplicación' )
reg( 'pOnes', 'aportación', 'aportaciones' )
reg( 'pOnes', 'apreciación', 'apreciaciones' )
reg( 'pOnes', 'aprobación' )
reg( 'pOnes', 'apropiación' )
reg( 'pOnes', 'aproximación' )
reg( 'pOnes', 'argumentación', 'argumentaciones' )
reg( 'pOnes', 'arpón', 'arpones' )
reg( 'pOnes', 'articulación', 'articulaciones' )
reg( 'pOnes', 'ascensión', 'ascensiones' )
reg( 'pOnes', 'aserción' )
reg( 'pOnes', 'asignación' )
reg( 'pOnes', 'asimilación' )
reg( 'pOnes', 'asociación' )
reg( 'pOnes', 'aspiración', 'aspiraciones' )
reg( 'pOnes', 'asunción', 'asunciones' )
reg( 'pOnes', 'asuncuiones' )
reg( 'pOnes', 'atención' )
reg( 'pOnes', 'atolón', 'atolones' )
reg( 'pOnes', 'atracción' )
reg( 'pOnes', 'atribución' )
reg( 'pOnes', 'audición' )
reg( 'pOnes', 'autenticación' )
reg( 'pOnes', 'autodeterminación' )
reg( 'pOnes', 'autorización')
reg( 'pOnes', 'autrigón', 'autrigones' )
reg( 'pOnes', 'averiguación', 'averiguaciones' )
reg( 'pOnes', 'avión' )
reg( 'pOnes', 'axón', 'axones' )
reg( 'pOnes', 'balcón', 'balcones' )
reg( 'pOnes', 'balón' )
reg( 'pOnes', 'barión', 'bariones' )
reg( 'pOnes', 'barracón', 'barracones' )
reg( 'pOnes', 'barón', 'barones' )
reg( 'pOnes', 'bastión', 'bastiones' )
reg( 'pOnes', 'bastón', 'bastones' )
reg( 'pOnes', 'batallón', 'batallones' )
reg( 'pOnes', 'beatificación' )
reg( 'pOnes', 'bendición' )
reg( 'pOnes', 'bidón', 'bidones' )
reg( 'pOnes', 'bifurcación', 'bifurcaciones' )
reg( 'pOnes', 'billón', 'billones' )
reg( 'pOnes', 'blasón', 'blasones' )
reg( 'pOnes', 'bodegón', 'bodegones' )
reg( 'pOnes', 'bombón', 'bombones' )
reg( 'pOnes', 'bonificación', 'bonificaciones' )
reg( 'pOnes', 'borbón', 'borbones' )
reg( 'pOnes', 'bosón', 'bosones' )
reg( 'pOnes', 'botón' )
reg( 'pOnes', 'bretón', 'bretones' )
reg( 'pOnes', 'bufón', 'bufones' )
reg( 'pOnes', 'buzón', 'buzones' )
reg( 'pOnes', 'cajón', 'cajones' )
reg( 'pOnes', 'calefacción' )
reg( 'pOnes', 'calificación' )
reg( 'pOnes', 'callejón', 'callejones' )
reg( 'pOnes', 'calzón', 'calzones' )
reg( 'pOnes', 'camaleón', 'camaleones' )
reg( 'pOnes', 'camarón', 'camarones' )
reg( 'pOnes', 'camellón', 'camellones' )
reg( 'pOnes', 'camión', 'camiones' )
reg( 'pOnes', 'campeón' )
reg( 'pOnes', 'canalización', 'canalizaciones' )
reg( 'pOnes', 'cancelación', 'cancelaciones' )
reg( 'pOnes', 'canción' )
reg( 'pOnes', 'canelón', 'canelones' )
reg( 'pOnes', 'cantón', 'cantones' )
reg( 'pOnes', 'capacitación' )
reg( 'pOnes', 'caparazón' )
reg( 'pOnes', 'capitalización' )
reg( 'pOnes', 'capitulación', 'capitulaciones' )
reg( 'pOnes', 'captación' )
reg( 'pOnes', 'carbón', 'carbones' )
reg( 'pOnes', 'cardón', 'cardones' )
reg( 'pOnes', 'cartón', 'cartones' )
reg( 'pOnes', 'casetón', 'casetones' )
reg( 'pOnes', 'categorización' )
reg( 'pOnes', 'catión', 'cationes' )
reg( 'pOnes', 'cañón', 'cañones' )
reg( 'pOnes', 'celebración', 'celebraciones' )
reg( 'pOnes', 'centralización' )
reg( 'pOnes', 'centurión', 'centuriones' )
reg( 'pOnes', 'certificación', 'certificaciones' )
reg( 'pOnes', 'cesión', 'cesiones' )
reg( 'pOnes', 'champiñón', 'champiñones' )
reg( 'pOnes', 'chicharrón', 'chicharrones' )
reg( 'pOnes', 'ciclón', 'ciclones' )
reg( 'pOnes', 'cimarrón', 'cimarrones' )
reg( 'pOnes', 'cimentación', 'cimentaciones' )
reg( 'pOnes', 'cinturón', 'cinturones' )
reg( 'pOnes', 'circulación' )
reg( 'pOnes', 'circunnavegación' )
reg( 'pOnes', 'circunscripción', 'circunscripciones' )
reg( 'pOnes', 'circunvalación' )
reg( 'pOnes', 'citación' )
reg( 'pOnes', 'civilización', 'civilizaciones' )
reg( 'pOnes', 'clasificación')
reg( 'pOnes', 'clonación' )
reg( 'pOnes', 'coacción' )
reg( 'pOnes', 'coagulación' )
reg( 'pOnes', 'coalición' )
reg( 'pOnes', 'cocción' )
reg( 'pOnes', 'codificación', 'codificaciones' )
reg( 'pOnes', 'codón', 'codones' )
reg( 'pOnes', 'cojón', 'cojones' )
reg( 'pOnes', 'colaboración' )
reg( 'pOnes', 'colación' )
reg( 'pOnes', 'colchón', 'colchones' )
reg( 'pOnes', 'colección' )
reg( 'pOnes', 'colocación' )
reg( 'pOnes', 'colonización', 'colonizaciones' )
reg( 'pOnes', 'coloración', 'coloraciones' )
reg( 'pOnes', 'colón', 'colones' )
reg( 'pOnes', 'combinación' )
reg( 'pOnes', 'comercialización' )
reg( 'pOnes', 'comisión' )
reg( 'pOnes', 'comparación' )
reg( 'pOnes', 'compensación', 'compensaciones' )
reg( 'pOnes', 'competición' )
reg( 'pOnes', 'compilación' )
reg( 'pOnes', 'complicación', 'complicaciones' )
reg( 'pOnes', 'composición' )
reg( 'pOnes', 'compresión', 'compresiones' )
reg( 'pOnes', 'comprobación' )
reg( 'pOnes', 'comunicación' )
reg( 'pOnes', 'concatenación' )
reg( 'pOnes', 'concentración', 'concentraciones' )
reg( 'pOnes', 'concepción' )
reg( 'pOnes', 'concesión', 'concesiones' )
reg( 'pOnes', 'conciliación' )
reg( 'pOnes', 'conclusión' )
reg( 'pOnes', 'concreción' )
reg( 'pOnes', 'condecoración' )
reg( 'pOnes', 'condensación' )
reg( 'pOnes', 'condición' )
reg( 'pOnes', 'conducción', 'conducciones' )
reg( 'pOnes', 'condón', 'condones' )
reg( 'pOnes', 'conexión' )
reg( 'pOnes', 'confabulación' )
reg( 'pOnes', 'confección' )
reg( 'pOnes', 'confederación', 'confederaciones' )
reg( 'pOnes', 'confesión', 'confesiones' )
reg( 'pOnes', 'configuración' )
reg( 'pOnes', 'confirmación', 'confirmaciones' )
reg( 'pOnes', 'confiscación', 'confiscaciones' )
reg( 'pOnes', 'conformación', 'conformaciones' )
reg( 'pOnes', 'confrontación', 'confrontaciones' )
reg( 'pOnes', 'confusión', 'confusiones' )
reg( 'pOnes', 'congelación' )
reg( 'pOnes', 'congregación', 'congregaciones' )
reg( 'pOnes', 'conjugación', 'conjugaciones' )
reg( 'pOnes', 'conjunción' )
reg( 'pOnes', 'conmemoración', 'conmemoraciones' )
reg( 'pOnes', 'conmoción' )
reg( 'pOnes', 'conmutación' )
reg( 'pOnes', 'connotación', 'connotaciones' )
reg( 'pOnes', 'consagración' )
reg( 'pOnes', 'consecución' )
reg( 'pOnes', 'conservación' )
reg( 'pOnes', 'consideración', 'consideraciones' )
reg( 'pOnes', 'consolidación' )
reg( 'pOnes', 'conspiración', 'conspiraciones' )
reg( 'pOnes', 'constelación', 'constelaciones' )
reg( 'pOnes', 'constitución', 'constituciones' )
reg( 'pOnes', 'construcción' )
reg( 'pOnes', 'contaminación' )
reg( 'pOnes', 'contemplación', 'contemplaciones' )
reg( 'pOnes', 'contención' )
reg( 'pOnes', 'contestación', 'contestaciones' )
reg( 'pOnes', 'continuación' )
reg( 'pOnes', 'contracción', 'contracciones' )
reg( 'pOnes', 'contradicción', 'contradicciones' )
reg( 'pOnes', 'contraindicación', 'contraindicaciones' )
reg( 'pOnes', 'contraposición' )
reg( 'pOnes', 'contratación', 'contrataciones' )
reg( 'pOnes', 'contribución' )
reg( 'pOnes', 'contusión', 'contusiones' )
reg( 'pOnes', 'conurbación', 'conurbaciones' )
reg( 'pOnes', 'convección' )
reg( 'pOnes', 'convención' )
reg( 'pOnes', 'conversación' )
reg( 'pOnes', 'conversión' )
reg( 'pOnes', 'convicción' )
reg( 'pOnes', 'convulsión', 'convulsiones' )
reg( 'pOnes', 'cooperación' )
reg( 'pOnes', 'coordinación' )
reg( 'pOnes', 'coproducción' )
reg( 'pOnes', 'corazón' )
reg( 'pOnes', 'cordón', 'cordones' )
reg( 'pOnes', 'coronación', 'coronaciones' )
reg( 'pOnes', 'corporación' )
reg( 'pOnes', 'corrección' )
reg( 'pOnes', 'correlación', 'correlaciones' )
reg( 'pOnes', 'corrupción' )
reg( 'pOnes', 'cotiledón', 'cotiledones' )
reg( 'pOnes', 'cotización', 'cotizaciones' )
reg( 'pOnes', 'creación' )
reg( 'pOnes', 'cristalización' )
reg( 'pOnes', 'cristianización' )
reg( 'pOnes', 'cuaternión', 'cuaterniones' )
reg( 'pOnes', 'cuestión' )
reg( 'pOnes', 'culminación' )
reg( 'pOnes', 'curación' )
reg( 'pOnes', 'datación', 'dataciones' )
reg( 'pOnes', 'decapitación' )
reg( 'pOnes', 'decepción' )
reg( 'pOnes', 'decisión' )
reg( 'pOnes', 'declaración' )
reg( 'pOnes', 'declinación' )
reg( 'pOnes', 'decoración', 'decoraciones' )
reg( 'pOnes', 'dedicación' )
reg( 'pOnes', 'deducción', 'deducciones' )
reg( 'pOnes', 'definición' )
reg( 'pOnes', 'deforestación' )
reg( 'pOnes', 'deformación')
reg( 'pOnes', 'defunción', 'defunciones' )
reg( 'pOnes', 'degeneración' )
reg( 'pOnes', 'degradación' )
reg( 'pOnes', 'degustación', 'degustaciones' )
reg( 'pOnes', 'delegación', 'delegaciones' )
reg( 'pOnes', 'deliberación', 'deliberaciones' )
reg( 'pOnes', 'demarcación', 'demarcaciones' )
reg( 'pOnes', 'democratización' )
reg( 'pOnes', 'demolición' )
reg( 'pOnes', 'demostración', 'demostraciones' )
reg( 'pOnes', 'denegación')
reg( 'pOnes', 'denominación' )
reg( 'pOnes', 'deportación', 'deportaciones' )
reg( 'pOnes', 'deposición' )
reg( 'pOnes', 'depredación' )
reg( 'pOnes', 'depresión', 'depresiones' )
reg( 'pOnes', 'depuración' )
reg( 'pOnes', 'derivación', 'derivaciones' )
reg( 'pOnes', 'derogación' )
reg( 'pOnes', 'desambiguación', 'desambiguaciones' )
reg( 'pOnes', 'desamortización', 'desamortizaciones' )
reg( 'pOnes', 'desaparición', 'desapariciones' )
reg( 'pOnes', 'descalificación', 'descalificaciones' )
reg( 'pOnes', 'descentralización' )
reg( 'pOnes', 'descomposición' )
reg( 'pOnes', 'desconexión', 'desconexiones' )
reg( 'pOnes', 'descripción' )
reg( 'pOnes', 'deserción', 'deserciones' )
reg( 'pOnes', 'desesperación' )
reg( 'pOnes', 'deshidratación' )
reg( 'pOnes', 'designación', 'designaciones' )
reg( 'pOnes', 'desintegración' )
reg( 'pOnes', 'desnutrición' )
reg( 'pOnes', 'despoblación' )
reg( 'pOnes', 'destilación' )
reg( 'pOnes', 'destitución' )
reg( 'pOnes', 'destrucción' )
reg( 'pOnes', 'desviación', 'desviaciones' )
reg( 'pOnes', 'detección' )
reg( 'pOnes', 'detención', 'detenciones' )
reg( 'pOnes', 'determinación', 'determinaciones' )
reg( 'pOnes', 'detonación', 'detonaciones' )
reg( 'pOnes', 'devaluación' )
reg( 'pOnes', 'devastación' )
reg( 'pOnes', 'devoción', 'devociones' )
reg( 'pOnes', 'devolución' )
reg( 'pOnes', 'dicción' )
reg( 'pOnes', 'difamación' )
reg( 'pOnes', 'diferenciación' )
reg( 'pOnes', 'difracción' )
reg( 'pOnes', 'difusión' )
reg( 'pOnes', 'digresión', 'digresiones' )
reg( 'pOnes', 'dilación' )
reg( 'pOnes', 'dilatación' )
reg( 'pOnes', 'dimensión' )
reg( 'pOnes', 'diputación', 'diputaciones' )
reg( 'pOnes', 'dirección' )
reg( 'pOnes', 'discreción' )
reg( 'pOnes', 'discriminación', 'discriminaciones' )
reg( 'pOnes', 'discusión' )
reg( 'pOnes', 'diseminación' )
reg( 'pOnes', 'disensión', 'disensiones' )
reg( 'pOnes', 'disertación', 'disertaciones' )
reg( 'pOnes', 'disfunción', 'disfunciones' )
reg( 'pOnes', 'disjunción' )
reg( 'pOnes', 'dislocación', 'dislocaciones' )
reg( 'pOnes', 'disminución', 'disminuciones' )
reg( 'pOnes', 'disociación')
reg( 'pOnes', 'disolución' )
reg( 'pOnes', 'dispersiones' )
reg( 'pOnes', 'dispersión' )
reg( 'pOnes', 'disposición' )
reg( 'pOnes', 'distracción', 'distracciones' )
reg( 'pOnes', 'distribución' )
reg( 'pOnes', 'disyunción' )
reg( 'pOnes', 'diversificación' )
reg( 'pOnes', 'diversión', 'diversiones' )
reg( 'pOnes', 'división' )
reg( 'pOnes', 'divulgación' )
reg( 'pOnes', 'documentación' )
reg( 'pOnes', 'domesticación' )
reg( 'pOnes', 'dominación' )
reg( 'pOnes', 'donación' )
reg( 'pOnes', 'dotación' )
reg( 'pOnes', 'dragón', 'dragones' )
reg( 'pOnes', 'drón', 'drones' )
reg( 'pOnes', 'duplicación' )
reg( 'pOnes', 'duración', 'duraciones' )
reg( 'pOnes', 'ebullición' )
reg( 'pOnes', 'ecorregión', 'ecorregiones' )
reg( 'pOnes', 'ecuación' )
reg( 'pOnes', 'edición' )
reg( 'pOnes', 'edificación')
reg( 'pOnes', 'educación' )
reg( 'pOnes', 'ejecución' )
reg( 'pOnes', 'elaboración', 'elaboraciones' )
reg( 'pOnes', 'elección' )
reg( 'pOnes', 'electrificación' )
reg( 'pOnes', 'electrón' )
reg( 'pOnes', 'elevación', 'elevaciones' )
reg( 'pOnes', 'eliminación' )
reg( 'pOnes', 'emanación' )
reg( 'pOnes', 'emancipación' )
reg( 'pOnes', 'embarcación', 'embarcaciones' )
reg( 'pOnes', 'embrión' )
reg( 'pOnes', 'emigración', 'emigraciones' )
reg( 'pOnes', 'emisión' )
reg( 'pOnes', 'emoción' )
reg( 'pOnes', 'emulación' )
reg( 'pOnes', 'emulsión', 'emulsiones' )
reg( 'pOnes', 'encarnación', 'encarnaciones' )
reg( 'pOnes', 'entonación' )
reg( 'pOnes', 'enumeración' )
reg( 'pOnes', 'equipación', 'equipaciones' )
reg( 'pOnes', 'equitación' )
reg( 'pOnes', 'equivocación', 'equivocaciones' )
reg( 'pOnes', 'erección' )
reg( 'pOnes', 'erradicación' )
reg( 'pOnes', 'erudición' )
reg( 'pOnes', 'erupción' )
reg( 'pOnes', 'escalafón', 'escalafones' )
reg( 'pOnes', 'escalón', 'escalones' )
reg( 'pOnes', 'escisión', 'escisiones' )
reg( 'pOnes', 'escorpión', 'escorpiones' )
reg( 'pOnes', 'escuadrón', 'escuadrones' )
reg( 'pOnes', 'especialización', 'especializaciones' )
reg( 'pOnes', 'especificación' )
reg( 'pOnes', 'especulación', 'especulaciones' )
reg( 'pOnes', 'espolón', 'espolones' )
reg( 'pOnes', 'estabilización' )
reg( 'pOnes', 'estación' )
reg( 'pOnes', 'estandarización' )
reg( 'pOnes', 'esterilización' )
reg( 'pOnes', 'estimación' )
reg( 'pOnes', 'estimulación' )
reg( 'pOnes', 'estipulación', 'estipulaciones' )
reg( 'pOnes', 'estratificación' )
reg( 'pOnes', 'estribación', 'estribaciones' )
reg( 'pOnes', 'estructuración' )
reg( 'pOnes', 'esturión', 'esturiones' )
reg( 'pOnes', 'evacuación', 'evacuaciones' )
reg( 'pOnes', 'evaluación' )
reg( 'pOnes', 'evangelización' )
reg( 'pOnes', 'evaporación' )
reg( 'pOnes', 'evocación', 'evocaciones' )
reg( 'pOnes', 'exación' )
reg( 'pOnes', 'exageración', 'exageraciones' )
reg( 'pOnes', 'exaltación' )
reg( 'pOnes', 'exaptación' )
reg( 'pOnes', 'excavación', 'excavaciones' )
reg( 'pOnes', 'excepción' )
reg( 'pOnes', 'excitación', 'excitaciones' )
reg( 'pOnes', 'exclamación', 'exclamaciones' )
reg( 'pOnes', 'exclusión', 'exclusiones' )
reg( 'pOnes', 'excreción' )
reg( 'pOnes', 'excursión', 'excursiones' )
reg( 'pOnes', 'exención', 'exenciones' )
reg( 'pOnes', 'exhibición', 'exhibiciones' )
reg( 'pOnes', 'expansión', 'expansiones' )
reg( 'pOnes', 'expectación' )
reg( 'pOnes', 'expedición' )
reg( 'pOnes', 'experimentación', 'experimentaciones' )
reg( 'pOnes', 'explicación' )
reg( 'pOnes', 'exploración', 'exploraciones' )
reg( 'pOnes', 'explosión' )
reg( 'pOnes', 'explotación', 'explotaciones' )
reg( 'pOnes', 'exponenciación' )
reg( 'pOnes', 'exportación' )
reg( 'pOnes', 'exposición' )
reg( 'pOnes', 'expresión' )
reg( 'pOnes', 'expropiación', 'expropiaciones' )
reg( 'pOnes', 'expulsión', 'expulsiones' )
reg( 'pOnes', 'extensión' )
reg( 'pOnes', 'extinción' )
reg( 'pOnes', 'extinción', 'extinciones' )
reg( 'pOnes', 'extorsión', 'extorsiones' )
reg( 'pOnes', 'extracción', 'extracciones' )
reg( 'pOnes', 'extradición' )
reg( 'pOnes', 'extrusión' )
reg( 'pOnes', 'eón', 'eones' )
reg( 'pOnes', 'fabricación' )
reg( 'pOnes', 'facción' )
reg( 'pOnes', 'factorización' )
reg( 'pOnes', 'facturación' )
reg( 'pOnes', 'fajón', 'fajones' )
reg( 'pOnes', 'faldón', 'faldones' )
reg( 'pOnes', 'falsificación', 'falsificaciones' )
reg( 'pOnes', 'farallón', 'farallones' )
reg( 'pOnes', 'faraón', 'faraones' )
reg( 'pOnes', 'fascinación' )
reg( 'pOnes', 'fecundación' )
reg( 'pOnes', 'federación', 'federaciones' )
reg( 'pOnes', 'felicitación', 'felicitaciones' )
reg( 'pOnes', 'fermentación', 'fermentaciones' )
reg( 'pOnes', 'fermión', 'fermiones' )
reg( 'pOnes', 'fertilización' )
reg( 'pOnes', 'ficción', 'ficciones' )
reg( 'pOnes', 'figuración' )
reg( 'pOnes', 'fijación' )
reg( 'pOnes', 'filiación' )
reg( 'pOnes', 'filmación', 'filmaciones' )
reg( 'pOnes', 'filtración', 'filtraciones' )
reg( 'pOnes', 'filón', 'filones' )
reg( 'pOnes', 'finalización' )
reg( 'pOnes', 'financiación' )
reg( 'pOnes', 'fiscalización' )
reg( 'pOnes', 'floración', 'floraciones' )
reg( 'pOnes', 'florón', 'florones' )
reg( 'pOnes', 'flotación' )
reg( 'pOnes', 'fluctuación', 'fluctuaciones' )
reg( 'pOnes', 'fogón', 'fogones' )
reg( 'pOnes', 'formación', 'formaciones' )
reg( 'pOnes', 'formulación', 'formulaciones' )
reg( 'pOnes', 'fortificación', 'fortificaciones' )
reg( 'pOnes', 'fotón', 'fotones' )
reg( 'pOnes', 'fracción' )
reg( 'pOnes', 'fragmentación' )
reg( 'pOnes', 'francmasón', 'francmasones' )
reg( 'pOnes', 'fricción' )
reg( 'pOnes', 'frisón', 'frisones' )
reg( 'pOnes', 'frontón', 'frontones' )
reg( 'pOnes', 'frustración', 'frustraciones' )
reg( 'pOnes', 'función' )
reg( 'pOnes', 'fundación', 'fundaciones' )
reg( 'pOnes', 'fundición' )
reg( 'pOnes', 'fusión' )
reg( 'pOnes', 'galeón', 'galeones' )
reg( 'pOnes', 'galpón', 'galpones' )
reg( 'pOnes', 'galón', 'galones' )
reg( 'pOnes', 'gascón', 'gascones' )
reg( 'pOnes', 'generación' )
reg( 'pOnes', 'generalización', 'generalizaciones' )
reg( 'pOnes', 'geolocalización' )
reg( 'pOnes', 'germinación' )
reg( 'pOnes', 'gestación' )
reg( 'pOnes', 'gestión' )
reg( 'pOnes', 'glaciación', 'glaciaciones' )
reg( 'pOnes', 'globalización' )
reg( 'pOnes', 'gobernación', 'gobernaciones' )
reg( 'pOnes', 'gorrión', 'gorriones' )
reg( 'pOnes', 'grabación', 'grabaciones' )
reg( 'pOnes', 'gradación', 'gradaciones' )
reg( 'pOnes', 'graduación', 'graduaciones' )
reg( 'pOnes', 'gravitación' )
reg( 'pOnes', 'guarnición', 'guarniciones' )
reg( 'pOnes', 'guión', 'guiones' )
reg( 'pOnes', 'habilitación' )
reg( 'pOnes', 'habitación', 'habitaciones' )
reg( 'pOnes', 'hadrón', 'hadrones' )
reg( 'pOnes', 'halcón', 'halcones' )
reg( 'pOnes', 'hibernación' )
reg( 'pOnes', 'hibridación' )
reg( 'pOnes', 'hidroavión', 'hidroaviones' )
reg( 'pOnes', 'hormigón' )
reg( 'pOnes', 'humillación', 'humillaciones' )
reg( 'pOnes', 'hurón', 'hurones' )
reg( 'pOnes', 'identificación', 'identificaciones' )
reg( 'pOnes', 'ignición' )
reg( 'pOnes', 'iluminación' )
reg( 'pOnes', 'ilusión' )
reg( 'pOnes', 'ilustración' )
reg( 'pOnes', 'imaginación' )
reg( 'pOnes', 'imitación', 'imitaciones' )
reg( 'pOnes', 'imperfección', 'imperfecciones' )
reg( 'pOnes', 'implantación' )
reg( 'pOnes', 'implementación' )
reg( 'pOnes', 'implicación' )
reg( 'pOnes', 'importación', 'importaciones' )
reg( 'pOnes', 'imposición' )
reg( 'pOnes', 'imprecisión', 'imprecisiones' )
reg( 'pOnes', 'impregnación' )
reg( 'pOnes', 'impresión' )
reg( 'pOnes', 'improvisación', 'improvisaciones' )
reg( 'pOnes', 'imputación', 'imputaciones' )
reg( 'pOnes', 'inauguración', 'inauguraciones' )
reg( 'pOnes', 'incisión', 'incisiones' )
reg( 'pOnes', 'inclinación' )
reg( 'pOnes', 'inclusión', 'inclusiones' )
reg( 'pOnes', 'incorporación' )
reg( 'pOnes', 'incrustación', 'incrustaciones' )
reg( 'pOnes', 'incubación' )
reg( 'pOnes', 'indagación', 'indagaciones' )
reg( 'pOnes', 'indemnización', 'indemnizaciones' )
reg( 'pOnes', 'indicación' )
reg( 'pOnes', 'indignación' )
reg( 'pOnes', 'industrialización' )
reg( 'pOnes', 'infección' )
reg( 'pOnes', 'infiltración', 'infiltraciones' )
reg( 'pOnes', 'inflación' )
reg( 'pOnes', 'inflamación', 'inflamaciones' )
reg( 'pOnes', 'inflexión', 'inflexiones' )
reg( 'pOnes', 'información' )
reg( 'pOnes', 'infracción', 'infracciones' )
reg( 'pOnes', 'infusión', 'infusiones' )
reg( 'pOnes', 'inhalación' )
reg( 'pOnes', 'inhibición' )
reg( 'pOnes', 'inhumación', 'inhumaciones' )
reg( 'pOnes', 'iniciación' )
reg( 'pOnes', 'inicialización' )
reg( 'pOnes', 'inmediación', 'inmediaciones' )
reg( 'pOnes', 'inmersión', 'inmersiones' )
reg( 'pOnes', 'inmigración', 'inmigraciones' )
reg( 'pOnes', 'innovación')
reg( 'pOnes', 'inscripción', 'inscripciones' )
reg( 'pOnes', 'inseminación' )
reg( 'pOnes', 'inserción' )
reg( 'pOnes', 'insinuación', 'insinuaciones' )
reg( 'pOnes', 'insolación' )
reg( 'pOnes', 'inspección' )
reg( 'pOnes', 'inspiración' )
reg( 'pOnes', 'instalación' )
reg( 'pOnes', 'instauración' )
reg( 'pOnes', 'institución' )
reg( 'pOnes', 'instrucción' )
reg( 'pOnes', 'instrumentación' )
reg( 'pOnes', 'insurrección', 'insurrecciones' )
reg( 'pOnes', 'integración' )
reg( 'pOnes', 'intención' )
reg( 'pOnes', 'intensificación' )
reg( 'pOnes', 'interacción' )
reg( 'pOnes', 'intercepción', 'intercepciones' )
reg( 'pOnes', 'interconexión', 'interconexiones' )
reg( 'pOnes', 'interjección', 'interjecciones' )
reg( 'pOnes', 'intermediación' )
reg( 'pOnes', 'internacionalización' )
reg( 'pOnes', 'interpolación', 'interpolaciones' )
reg( 'pOnes', 'interpretación' )
reg( 'pOnes', 'interrelación', 'interrelaciones' )
reg( 'pOnes', 'interrogación' )
reg( 'pOnes', 'interrupción' )
reg( 'pOnes', 'intersección' )
reg( 'pOnes', 'intervención' )
reg( 'pOnes', 'intimidación' )
reg( 'pOnes', 'intoxicación', 'intoxicaciones' )
reg( 'pOnes', 'introducción' )
reg( 'pOnes', 'intrusión', 'intrusiones' )
reg( 'pOnes', 'intuición' )
reg( 'pOnes', 'inundación', 'inundaciones' )
reg( 'pOnes', 'invasión', 'invasiones' )
reg( 'pOnes', 'invención' )
reg( 'pOnes', 'inversión' )
reg( 'pOnes', 'investigación' )
reg( 'pOnes', 'invitación', 'invitaciones' )
reg( 'pOnes', 'invocación', 'invocaciones' )
reg( 'pOnes', 'inyección' )
reg( 'pOnes', 'ionización' )
reg( 'pOnes', 'irradiación' )
reg( 'pOnes', 'irrigación' )
reg( 'pOnes', 'irritación', 'irritaciones' )
reg( 'pOnes', 'irrupción' )
reg( 'pOnes', 'iteración', 'iteraciones' )
reg( 'pOnes', 'ión', 'iones' )
reg( 'pOnes', 'jabón', 'jabones' )
reg( 'pOnes', 'jamón', 'jamones' )
reg( 'pOnes', 'japón', 'japones' )
reg( 'pOnes', 'jarrón', 'jarrones' )
reg( 'pOnes', 'jonrón', 'jonrones' )
reg( 'pOnes', 'jubilación', 'jubilaciones' )
reg( 'pOnes', 'jurisdicción', 'jurisdicciones' )
reg( 'pOnes', 'justificación', 'justificaciones' )
reg( 'pOnes', 'kilotón', 'kilotones' )
reg( 'pOnes', 'ladrón', 'ladrones' )
reg( 'pOnes', 'lamentación', 'lamentaciones' )
reg( 'pOnes', 'lapón', 'lapones' )
reg( 'pOnes', 'lección' )
reg( 'pOnes', 'legalización' )
reg( 'pOnes', 'legislación')
reg( 'pOnes', 'legión', 'legiones' )
reg( 'pOnes', 'leptón', 'leptones' )
reg( 'pOnes', 'lesión' )
reg( 'pOnes', 'letón', 'letones' )
reg( 'pOnes', 'león', 'leones' )
reg( 'pOnes', 'libación', 'libaciones' )
reg( 'pOnes', 'liberación' )
reg( 'pOnes', 'liberalización' )
reg( 'pOnes', 'licitación', 'licitaciones' )
reg( 'pOnes', 'licuefacción' )
reg( 'pOnes', 'limitación' )
reg( 'pOnes', 'limón' )
reg( 'pOnes', 'liquidación' )
reg( 'pOnes', 'listón', 'listones' )
reg( 'pOnes', 'locación', 'locaciones' )
reg( 'pOnes', 'localización', 'localizaciones' )
reg( 'pOnes', 'loción' )
reg( 'pOnes', 'locomoción' )
reg( 'pOnes', 'locución' )
reg( 'pOnes', 'luxación', 'luxaciones' )
reg( 'pOnes', 'maduración' )
reg( 'pOnes', 'maldición' )
reg( 'pOnes', 'malformación', 'malformaciones' )
reg( 'pOnes', 'malversación' )
reg( 'pOnes', 'manifestación' )
reg( 'pOnes', 'manipulación' )
reg( 'pOnes', 'mansión', 'mansiones' )
reg( 'pOnes', 'maquetación' )
reg( 'pOnes', 'maquinación', 'maquinaciones' )
reg( 'pOnes', 'maratón', 'maratones' )
reg( 'pOnes', 'marginación' )
reg( 'pOnes', 'marrón', 'marrones' )
reg( 'pOnes', 'mascarón', 'mascarones' )
reg( 'pOnes', 'masterización' )
reg( 'pOnes', 'masón', 'masones' )
reg( 'pOnes', 'matón', 'matones' )
reg( 'pOnes', 'mechón', 'mechones' )
reg( 'pOnes', 'medallón', 'medallones' )
reg( 'pOnes', 'mediación' )
reg( 'pOnes', 'medicación' )
reg( 'pOnes', 'medición' )
reg( 'pOnes', 'meditación', 'meditaciones' )
reg( 'pOnes', 'megatón', 'megatones' )
reg( 'pOnes', 'mejillón', 'mejillones' )
reg( 'pOnes', 'melocotón', 'melocotones' )
reg( 'pOnes', 'melón', 'melones' )
reg( 'pOnes', 'mención' )
reg( 'pOnes', 'menstruación' )
reg( 'pOnes', 'mesorregión', 'mesorregiones' )
reg( 'pOnes', 'mesón', 'mesones' )
reg( 'pOnes', 'microacción' )
reg( 'pOnes', 'micromutación' )
reg( 'pOnes', 'microrregión', 'microrregiones' )
reg( 'pOnes', 'migración' )
reg( 'pOnes', 'millón' )
reg( 'pOnes', 'misión', 'misiones' )
reg( 'pOnes', 'moción' )
reg( 'pOnes', 'moderación' )
reg( 'pOnes', 'modernización', 'modernizaciones' )
reg( 'pOnes', 'modificación' )
reg( 'pOnes', 'modulación', 'modulaciones' )
reg( 'pOnes', 'mojón', 'mojones' )
reg( 'pOnes', 'montón' )
reg( 'pOnes', 'monzón', 'monzones' )
reg( 'pOnes', 'mormón', 'mormones' )
reg( 'pOnes', 'motivación' )
reg( 'pOnes', 'motorización', 'motorizaciones' )
reg( 'pOnes', 'movilización', 'movilizaciones' )
reg( 'pOnes', 'multiplicación' )
reg( 'pOnes', 'munición' )
reg( 'pOnes', 'musicalización' )
reg( 'pOnes', 'mutación' )
reg( 'pOnes', 'mutilación', 'mutilaciones' )
reg( 'pOnes', 'nacionalización' )
reg( 'pOnes', 'nación' )
reg( 'pOnes', 'narración', 'narraciones' )
reg( 'pOnes', 'natación' )
reg( 'pOnes', 'navegación' )
reg( 'pOnes', 'negación' )
reg( 'pOnes', 'negociación' )
reg( 'pOnes', 'nipón', 'nipones' )
reg( 'pOnes', 'noción' )
reg( 'pOnes', 'nominación', 'nominaciones' )
reg( 'pOnes', 'normalización' )
reg( 'pOnes', 'notación' )
reg( 'pOnes', 'notificación', 'notificaciones' )
reg( 'pOnes', 'nucleón', 'nucleones' )
reg( 'pOnes', 'numeración' )
reg( 'pOnes', 'nutrición' )
reg( 'pOnes', 'objeción' )
reg( 'pOnes', 'obligación', 'obligaciones' )
reg( 'pOnes', 'observación' )
reg( 'pOnes', 'obstrucción' )
reg( 'pOnes', 'ocasión' )
reg( 'pOnes', 'ocultación', 'ocultaciones' )
reg( 'pOnes', 'ocupación', 'ocupaciones' )
reg( 'pOnes', 'omisión', 'omisiones' )
reg( 'pOnes', 'ondulación', 'ondulaciones' )
reg( 'pOnes', 'opción' )
reg( 'pOnes', 'operación' )
reg( 'pOnes', 'opinión' )
reg( 'pOnes', 'oposición' )
reg( 'pOnes', 'oración', 'oraciones' )
reg( 'pOnes', 'ordenación', 'ordenaciones' )
reg( 'pOnes', 'orejón', 'orejones' )
reg( 'pOnes', 'organización' )
reg( 'pOnes', 'orientación' )
reg( 'pOnes', 'ornamentación' )
reg( 'pOnes', 'orquestación', 'orquestaciones' )
reg( 'pOnes', 'oscilación', 'oscilaciones' )
reg( 'pOnes', 'ovación' )
reg( 'pOnes', 'oxidación' )
reg( 'pOnes', 'pabellón', 'pabellones' )
reg( 'pOnes', 'pacificación' )
reg( 'pOnes', 'padrón', 'padrones' )
reg( 'pOnes', 'palpitación', 'palpitaciones' )
reg( 'pOnes', 'pantalón', 'pantalones' )
reg( 'pOnes', 'panteón', 'panteones' )
reg( 'pOnes', 'paralización' )
reg( 'pOnes', 'participación' )
reg( 'pOnes', 'partición' )
reg( 'pOnes', 'pasión', 'pasiones' )
reg( 'pOnes', 'patagón', 'patagones' )
reg( 'pOnes', 'patrón', 'patrona', 'patronas' )
reg( 'pOnes', 'pavimentación' )
reg( 'pOnes', 'peatón', 'peatones' )
reg( 'pOnes', 'pelotón', 'pelotones' )
reg( 'pOnes', 'penalización', 'penalizaciones' )
reg( 'pOnes', 'pendón', 'pendones' )
reg( 'pOnes', 'penetración', 'penetraciones' )
reg( 'pOnes', 'pensión', 'pensiones' )
reg( 'pOnes', 'percepción' )
reg( 'pOnes', 'percusión', 'percusiones' )
reg( 'pOnes', 'perdigón', 'perdigones' )
reg( 'pOnes', 'peregrinación', 'peregrinaciones' )
reg( 'pOnes', 'perfección' )
reg( 'pOnes', 'perforación', 'perforaciones' )
reg( 'pOnes', 'permutación', 'permutaciones' )
reg( 'pOnes', 'persecución' )
reg( 'pOnes', 'personalización' )
reg( 'pOnes', 'personificación', 'personificaciones' )
reg( 'pOnes', 'perturbación' )
reg( 'pOnes', 'perversión', 'perversiones' )
reg( 'pOnes', 'petición' )
reg( 'pOnes', 'pezón', 'pezones' )
reg( 'pOnes', 'peón', 'peones' )
reg( 'pOnes', 'pichón', 'pichones' )
reg( 'pOnes', 'pilón', 'pilones' )
reg( 'pOnes', 'pinzón', 'pinzones' )
reg( 'pOnes', 'pistón', 'pistones' )
reg( 'pOnes', 'piñón', 'piñones' )
reg( 'pOnes', 'planeación' )
reg( 'pOnes', 'plantación', 'plantaciones' )
reg( 'pOnes', 'población' )
reg( 'pOnes', 'poción', 'pociones' )
reg( 'pOnes', 'polarización' )
reg( 'pOnes', 'polimerización' )
reg( 'pOnes', 'polinización' )
reg( 'pOnes', 'pontón', 'pontones' )
reg( 'pOnes', 'popularización' )
reg( 'pOnes', 'porción' )
reg( 'pOnes', 'portón', 'portones' )
reg( 'pOnes', 'posesión' )
reg( 'pOnes', 'posición' )
reg( 'pOnes', 'positrón', 'positrones' )
reg( 'pOnes', 'postulación', 'postulaciones' )
reg( 'pOnes', 'precaución' )
reg( 'pOnes', 'precipitación' )
reg( 'pOnes', 'precisión' )
reg( 'pOnes', 'predicación', 'predicaciones' )
reg( 'pOnes', 'predicción' )
reg( 'pOnes', 'predilección' )
reg( 'pOnes', 'predisposición' )
reg( 'pOnes', 'preimpresión' )
reg( 'pOnes', 'premiación' )
reg( 'pOnes', 'preocupación' )
reg( 'pOnes', 'preparación' )
reg( 'pOnes', 'preposición', 'preposiciones' )
reg( 'pOnes', 'prescripción', 'prescripciones' )
reg( 'pOnes', 'preselección' )
reg( 'pOnes', 'presentación' )
reg( 'pOnes', 'preservación' )
reg( 'pOnes', 'presión' )
reg( 'pOnes', 'prestación', 'prestaciones' )
reg( 'pOnes', 'presunción', 'presunciones' )
reg( 'pOnes', 'pretensión', 'pretensiones' )
reg( 'pOnes', 'previsión', 'previsiones' )
reg( 'pOnes', 'previsualización' )
reg( 'pOnes', 'prisión', 'prisiones' )
reg( 'pOnes', 'privación', 'privaciones' )
reg( 'pOnes', 'privatización', 'privatizaciones' )
reg( 'pOnes', 'prión', 'priones' )
reg( 'pOnes', 'procesión' )
reg( 'pOnes', 'proclamación' )
reg( 'pOnes', 'producción' )
reg( 'pOnes', 'profesión', 'profesiones' )
reg( 'pOnes', 'programación' )
reg( 'pOnes', 'progresión', 'progresiones' )
reg( 'pOnes', 'prohibición', 'prohibiciones' )
reg( 'pOnes', 'proliferación' )
reg( 'pOnes', 'prolongación', 'prolongaciones' )
reg( 'pOnes', 'promoción' )
reg( 'pOnes', 'promulgación' )
reg( 'pOnes', 'pronunciación', 'pronunciaciones' )
reg( 'pOnes', 'propagación' )
reg( 'pOnes', 'proporción' )
reg( 'pOnes', 'proposición', 'proposiciones' )
reg( 'pOnes', 'propulsión' )
reg( 'pOnes', 'prospección', 'prospecciones' )
reg( 'pOnes', 'prostitución' )
reg( 'pOnes', 'protección', 'protecciones' )
reg( 'pOnes', 'protón' )
reg( 'pOnes', 'provisión', 'provisiones' )
reg( 'pOnes', 'provocación', 'provocaciones' )
reg( 'pOnes', 'proyección', 'proyecciones' )
reg( 'pOnes', 'publicación' )
reg( 'pOnes', 'pulgón', 'pulgones' )
reg( 'pOnes', 'pulmón' )
reg( 'pOnes', 'pulsación', 'pulsaciones' )
reg( 'pOnes', 'pulsión', 'pulsiones' )
reg( 'pOnes', 'punción' )
reg( 'pOnes', 'punición' )
reg( 'pOnes', 'puntuación', 'puntuaciones' )
reg( 'pOnes', 'punzón', 'punzones' )
reg( 'pOnes', 'purificación' )
reg( 'pOnes', 'ración' )
reg( 'pOnes', 'radiación' )
reg( 'pOnes', 'ramificación' )
reg( 'pOnes', 'ratificación' )
reg( 'pOnes', 'ratón' )
reg( 'pOnes', 'rayón', 'rayones' )
reg( 'pOnes', 'reacción' )
reg( 'pOnes', 'reactivación' )
reg( 'pOnes', 'realización', 'realizaciones' )
reg( 'pOnes', 'reanudación' )
reg( 'pOnes', 'reaparición' )
reg( 'pOnes', 'rebelión', 'rebeliones' )
reg( 'pOnes', 'recaptación' )
reg( 'pOnes', 'recaudación', 'recaudaciones' )
reg( 'pOnes', 'recepción', 'recepciones' )
reg( 'pOnes', 'reclamación', 'reclamaciones' )
reg( 'pOnes', 'recolección', 'recolecciones' )
reg( 'pOnes', 'recombinación' )
reg( 'pOnes', 'recomendación' )
reg( 'pOnes', 'reconciliación' )
reg( 'pOnes', 'reconstrucción', 'reconstrucciones' )
reg( 'pOnes', 'recopilación', 'recopilaciones' )
reg( 'pOnes', 'recreación')
reg( 'pOnes', 'rectificación' )
reg( 'pOnes', 'recuperación', 'recuperaciones' )
reg( 'pOnes', 'redacción' )
reg( 'pOnes', 'redención' )
reg( 'pOnes', 'redirección' )
reg( 'pOnes', 'redistribución' )
reg( 'pOnes', 'reducción' )
reg( 'pOnes', 'reedición', 'reediciones' )
reg( 'pOnes', 'reelección' )
reg( 'pOnes', 'reencarnación', 'reencarnaciones' )
reg( 'pOnes', 'refacción' )
reg( 'pOnes', 'refinación' )
reg( 'pOnes', 'reflexión' )
reg( 'pOnes', 'refracción' )
reg( 'pOnes', 'refrigeración' )
reg( 'pOnes', 'refundación' )
reg( 'pOnes', 'regeneración' )
reg( 'pOnes', 'región' )
reg( 'pOnes', 'reglamentación', 'reglamentaciones' )
reg( 'pOnes', 'regulación' )
reg( 'pOnes', 'rehabilitación' )
reg( 'pOnes', 'reimpresión', 'reimpresiones' )
reg( 'pOnes', 'reivindicación', 'reivindicaciones' )
reg( 'pOnes', 'relación' )
reg( 'pOnes', 'relajación' )
reg( 'pOnes', 'religión' )
reg( 'pOnes', 'remoción' )
reg( 'pOnes', 'remodelación', 'remodelaciones' )
reg( 'pOnes', 'remuneración', 'remuneraciones' )
reg( 'pOnes', 'rendición' )
reg( 'pOnes', 'renglón', 'renglones' )
reg( 'pOnes', 'renovación', 'renovaciones' )
reg( 'pOnes', 'reorganización' )
reg( 'pOnes', 'reparación', 'reparaciones' )
reg( 'pOnes', 'repartición', 'reparticiones' )
reg( 'pOnes', 'repercusión' )
reg( 'pOnes', 'repetición' )
reg( 'pOnes', 'replicación' )
reg( 'pOnes', 'repoblación', 'repoblaciones' )
reg( 'pOnes', 'reposición' )
reg( 'pOnes', 'representación' )
reg( 'pOnes', 'represión', 'represiones' )
reg( 'pOnes', 'reproducción', 'reproducciones' )
reg( 'pOnes', 'reputación' )
reg( 'pOnes', 'resolución' )
reg( 'pOnes', 'respiración' )
reg( 'pOnes', 'restauración', 'restauraciones' )
reg( 'pOnes', 'restitución' )
reg( 'pOnes', 'restricción' )
reg( 'pOnes', 'resurrección' )
reg( 'pOnes', 'retención', 'retenciones' )
reg( 'pOnes', 'retransmisión', 'retransmisiones' )
reg( 'pOnes', 'retribución', 'retribuciones' )
reg( 'pOnes', 'retrotransposón' )
reg( 'pOnes', 'reunificación' )
reg( 'pOnes', 'reunión' )
reg( 'pOnes', 'reutilización' )
reg( 'pOnes', 'revalidación', 'revalidaciones' )
reg( 'pOnes', 'revelación', 'revelaciones' )
reg( 'pOnes', 'reversión', 'reversiones' )
reg( 'pOnes', 'revisión' )
reg( 'pOnes', 'revolución' )
reg( 'pOnes', 'rincón', 'rincones' )
reg( 'pOnes', 'riñón', 'riñones' )
reg( 'pOnes', 'romanización' )
reg( 'pOnes', 'rosetón', 'rosetones' )
reg( 'pOnes', 'rotación' )
reg( 'pOnes', 'sajón', 'sajones' )
reg( 'pOnes', 'salazón', 'salazones' )
reg( 'pOnes', 'salmón', 'salmones' )
reg( 'pOnes', 'salvación' )
reg( 'pOnes', 'salón', 'salones' )
reg( 'pOnes', 'sanción' )
reg( 'pOnes', 'satisfacción' )
reg( 'pOnes', 'saturación' )
reg( 'pOnes', 'saxofón' )
reg( 'pOnes', 'sección' )
reg( 'pOnes', 'secreción', 'secreciones' )
reg( 'pOnes', 'secuenciación' )
reg( 'pOnes', 'secularización' )
reg( 'pOnes', 'sedimentación' )
reg( 'pOnes', 'seducción' )
reg( 'pOnes', 'segmentación' )
reg( 'pOnes', 'segregación' )
reg( 'pOnes', 'selección' )
reg( 'pOnes', 'semidesintegración' )
reg( 'pOnes', 'semiprotección' )
reg( 'pOnes', 'sensación' )
reg( 'pOnes', 'sensibilización' )
reg( 'pOnes', 'separación' )
reg( 'pOnes', 'sermón', 'sermones' )
reg( 'pOnes', 'sesión' )
reg( 'pOnes', 'señalización' )
reg( 'pOnes', 'sifón', 'sifones' )
reg( 'pOnes', 'significación', 'significaciones' )
reg( 'pOnes', 'sillón', 'sillones' )
reg( 'pOnes', 'simplificación', 'simplificaciones' )
reg( 'pOnes', 'simulación', 'simulaciones' )
reg( 'pOnes', 'sincronización' )
reg( 'pOnes', 'situación' )
reg( 'pOnes', 'socialización' )
reg( 'pOnes', 'solución' )
reg( 'pOnes', 'subcampeón', 'subcampeones' )
reg( 'pOnes', 'subdelegación', 'subdelegaciones' )
reg( 'pOnes', 'subdivisión', 'subdivisiones' )
reg( 'pOnes', 'subestación', 'subestaciones' )
reg( 'pOnes', 'sublevación', 'sublevaciones' )
reg( 'pOnes', 'subordinación' )
reg( 'pOnes', 'subregión', 'subregiones' )
reg( 'pOnes', 'subsección', 'subsecciones' )
reg( 'pOnes', 'subvención', 'subvenciones' )
reg( 'pOnes', 'sucesión', 'sucesiones' )
reg( 'pOnes', 'sujeción' )
reg( 'pOnes', 'superación' )
reg( 'pOnes', 'superposición' )
reg( 'pOnes', 'superstición', 'supersticiones' )
reg( 'pOnes', 'supervisión' )
reg( 'pOnes', 'suposición' )
reg( 'pOnes', 'suscripción', 'suscripciones' )
reg( 'pOnes', 'suspensión', 'suspensiones' )
reg( 'pOnes', 'sustentación' )
reg( 'pOnes', 'sustitución', 'sustituciones' )
reg( 'pOnes', 'tablón', 'tablones' )
reg( 'pOnes', 'tacón', 'tacones' )
reg( 'pOnes', 'talón', 'talones' )
reg( 'pOnes', 'tampón', 'tampones' )
reg( 'pOnes', 'tapón', 'tapones' )
reg( 'pOnes', 'taxón' )
reg( 'pOnes', 'tejón', 'tejones' )
reg( 'pOnes', 'telecomunicación', 'telecomunicaciones' )
reg( 'pOnes', 'televisión', 'televisiones' )
reg( 'pOnes', 'tendón', 'tendones' )
reg( 'pOnes', 'tensión', 'tensiones' )
reg( 'pOnes', 'tentación', 'tentaciones' )
reg( 'pOnes', 'terminación' )
reg( 'pOnes', 'teutón', 'teutones' )
reg( 'pOnes', 'tiburón', 'tiburones' )
reg( 'pOnes', 'tifón', 'tifones' )
reg( 'pOnes', 'timón', 'timones' )
reg( 'pOnes', 'tinción' )
reg( 'pOnes', 'titulación', 'titulaciones' )
reg( 'pOnes', 'torreón', 'torreones' )
reg( 'pOnes', 'tracción' )
reg( 'pOnes', 'tradición' )
reg( 'pOnes', 'traducción', 'traducciones' )
reg( 'pOnes', 'traición' )
reg( 'pOnes', 'tramitación' )
reg( 'pOnes', 'transacción' )
reg( 'pOnes', 'transcripción' )
reg( 'pOnes', 'transformación' )
reg( 'pOnes', 'transfusión', 'transfusiones' )
reg( 'pOnes', 'transgresión', 'transgresiones' )
reg( 'pOnes', 'transición' )
reg( 'pOnes', 'transliteración', 'transliteraciones' )
reg( 'pOnes', 'translocación' )
reg( 'pOnes', 'transmisión', 'transmisiones' )
reg( 'pOnes', 'transposición' )
reg( 'pOnes', 'traslación', 'traslaciones' )
reg( 'pOnes', 'tribulación', 'tribulaciones' )
reg( 'pOnes', 'trillón', 'trillones' )
reg( 'pOnes', 'tripulación', 'tripulaciones' )
reg( 'pOnes', 'trombón', 'trombones' )
reg( 'pOnes', 'turrón', 'turrones' )
reg( 'pOnes', 'táxón', 'táxones' )
reg( 'pOnes', 'ubicación' )
reg( 'pOnes', 'unificación' )
reg( 'pOnes', 'unión' )
reg( 'pOnes', 'urbanización', 'urbanizaciones' )
reg( 'pOnes', 'usurpación' )
reg( 'pOnes', 'utilización' )
reg( 'pOnes', 'vacación' )
reg( 'pOnes', 'vacilación', 'vacilaciones' )
reg( 'pOnes', 'vacunación' )
reg( 'pOnes', 'vagón', 'vagones' )
reg( 'pOnes', 'validación' )
reg( 'pOnes', 'valoración', 'valoraciones' )
reg( 'pOnes', 'valón', 'valones' )
reg( 'pOnes', 'variación' )
reg( 'pOnes', 'varón' )
reg( 'pOnes', 'vectorización' )
reg( 'pOnes', 'vegetación' )
reg( 'pOnes', 'vejación', 'vejaciones' )
reg( 'pOnes', 'veneración' )
reg( 'pOnes', 'ventilación' )
reg( 'pOnes', 'verificación' )
reg( 'pOnes', 'versión' )
reg( 'pOnes', 'vibración', 'vibraciones' )
reg( 'pOnes', 'vinculación', 'vinculaciones' )
reg( 'pOnes', 'violación', 'violaciones' )
reg( 'pOnes', 'visión' )
reg( 'pOnes', 'visualización' )
reg( 'pOnes', 'vocación' )
reg( 'pOnes', 'vocalización', 'vocalizaciones' )
reg( 'pOnes', 'votación', 'votaciones' )
reg( 'pS', 'mente' )
reg( 'pS', 'abadía' )
reg( 'pS', 'abeja' )
reg( 'pS', 'abnegado' )
reg( 'pS', 'abreviatura' )
reg( 'pS', 'abuela' )
reg( 'pS', 'abundante' )
reg( 'pS', 'abuso' )
reg( 'pS', 'academia' )
reg( 'pS', 'accesible' )
reg( 'pS', 'acceso' )
reg( 'pS', 'accesorio' )
reg( 'pS', 'accionista' )
reg( 'pS', 'aceite' )
reg( 'pS', 'acero' )
reg( 'pS', 'acogida' )
reg( 'pS', 'acompañante' )
reg( 'pS', 'acontecimiento' )
reg( 'pS', 'acoplable' )
reg( 'pS', 'acrónimo' )
reg( 'pS', 'acta' )
reg( 'pS', 'activista' )
reg( 'pS', 'activo')
reg( 'pS', 'acto' )
reg( 'pS', 'acuerdo' )
reg( 'pS', 'adolescente' )
reg( 'pS', 'adulto' )
reg( 'pS', 'adyacente' )
reg( 'pS', 'aerolínea' )
reg( 'pS', 'aeronave' )
reg( 'pS', 'aeropuerto' )
reg( 'pS', 'afluente' )
reg( 'pS', 'agencia' )
reg( 'pS', 'agente' )
reg( 'pS', 'agricultura' )
reg( 'pS', 'agrícola' )
reg( 'pS', 'agua' )
reg( 'pS', 'aguja' )
reg( 'pS', 'agujero')
reg( 'pS', 'aislante' )
reg( 'pS', 'ajuste' )
reg( 'pS', 'ala' )
reg( 'pS', 'alcalde', 'alcaldesa', 'alcaldesas' )
reg( 'pS', 'alcaldía' )
reg( 'pS', 'aldea' )
reg( 'pS', 'alegría' )
reg( 'pS', 'alelo' )
reg( 'pS', 'aleta' )
reg( 'pS', 'alfabeto' )
reg( 'pS', 'alga' )
reg( 'pS', 'algoritmo' )
reg( 'pS', 'alianza' )
reg( 'pS', 'alimento' )
reg( 'pS', 'alma' )
reg( 'pS', 'almirante' )
reg( 'pS', 'altruista' )
reg( 'pS', 'altura' )
reg( 'pS', 'aluminio' )
reg( 'pS', 'alumno' )
reg( 'pS', 'amante' )
reg( 'pS', 'amarillo' )
reg( 'pS', 'amazona' )
reg( 'pS', 'ambiental' )
reg( 'pS', 'ambiente' )
reg( 'pS', 'ambulante' )
reg( 'pS', 'ametralladora' )
reg( 'pS', 'amigo' )
reg( 'pS', 'aminoácido' )
reg( 'pS', 'amniota' )
reg( 'pS', 'analista' )
reg( 'pS', 'anarquista' )
reg( 'pS', 'anatomía' )
reg( 'pS', 'ancestro' )
reg( 'pS', 'anchura' )
reg( 'pS', 'anciano' )
reg( 'pS', 'angiosperma' )
reg( 'pS', 'anillo' )
reg( 'pS', 'aniversario' )
reg( 'pS', 'anomalía' )
reg( 'pS', 'antecedente' )
reg( 'pS', 'antena' )
reg( 'pS', 'antibiótico' )
reg( 'pS', 'anticuerpo' )
reg( 'pS', 'antiguo' )
reg( 'pS', 'antología' )
reg( 'pS', 'antropónimo' )
reg( 'pS', 'antónimo' )
reg( 'pS', 'anuncio' )
reg( 'pS', 'anécdota' )
reg( 'pS', 'aparato' )
reg( 'pS', 'aparente' )
reg( 'pS', 'apariencia' )
reg( 'pS', 'apartamento' )
reg( 'pS', 'apellido' )
reg( 'pS', 'apertura' )
reg( 'pS', 'apilable')
reg( 'pS', 'aplastante' )
reg( 'pS', 'arbusto' )
reg( 'pS', 'archipiélago' )
reg( 'pS', 'archivo' )
reg( 'pS', 'arco' )
reg( 'pS', 'area' )
reg( 'pS', 'arena' )
reg( 'pS', 'argumento' )
reg( 'pS', 'arista' )
reg( 'pS', 'arma' )
reg( 'pS', 'armada' )
reg( 'pS', 'armadura' )
reg( 'pS', 'armamento' )
reg( 'pS', 'armonía' )
reg( 'pS', 'arquitectura' )
reg( 'pS', 'arrecife' )
reg( 'pS', 'arrecifes' )
reg( 'pS', 'arreglo' )
reg( 'pS', 'arrogante' )
reg( 'pS', 'arroyo' )
reg( 'pS', 'arte' )
reg( 'pS', 'artefacto' )
reg( 'pS', 'arteria' )
reg( 'pS', 'artesanía' )
reg( 'pS', 'articulo' )
reg( 'pS', 'artillería' )
reg( 'pS', 'artista' )
reg( 'pS', 'artrópodo' )
reg( 'pS', 'artículo' )
reg( 'pS', 'artífice' )
reg( 'pS', 'arzobispo' )
reg( 'pS', 'asamblea' )
reg( 'pS', 'ascendencia' )
reg( 'pS', 'ascendente' )
reg( 'pS', 'ascenso' )
reg( 'pS', 'asedio' )
reg( 'pS', 'asentamiento' )
reg( 'pS', 'asentamientos' )
reg( 'pS', 'asesinato' )
reg( 'pS', 'asesoría' )
reg( 'pS', 'asiento' )
reg( 'pS', 'asistencia' )
reg( 'pS', 'asistente')
reg( 'pS', 'aspecto' )
reg( 'pS', 'aspirante' )
reg( 'pS', 'asteroide' )
reg( 'pS', 'astronomía' )
reg( 'pS', 'asunto' )
reg( 'pS', 'atacante' )
reg( 'pS', 'ateniense' )
reg( 'pS', 'atleta' )
reg( 'pS', 'atmósfera' )
reg( 'pS', 'atributo' )
reg( 'pS', 'audiencia' )
reg( 'pS', 'audio' )
reg( 'pS', 'aula' )
reg( 'pS', 'ausencia' )
reg( 'pS', 'ausente' )
reg( 'pS', 'auto' )
reg( 'pS', 'autopista' )
reg( 'pS', 'autorización')
reg( 'pS', 'autoría' )
reg( 'pS', 'avance' )
reg( 'pS', 'ave' )
reg( 'pS', 'avenida' )
reg( 'pS', 'aventura' )
reg( 'pS', 'aviso' )
reg( 'pS', 'avispa' )
reg( 'pS', 'ayudante' )
reg( 'pS', 'ayuntamiento' )
reg( 'pS', 'año' )
reg( 'pS', 'bachillerato' )
reg( 'pS', 'backup')
reg( 'pS', 'bacteria' )
reg( 'pS', 'bahía' )
reg( 'pS', 'bajista' )
reg( 'pS', 'bala' )
reg( 'pS', 'balada' )
reg( 'pS', 'balance' )
reg( 'pS', 'ballena' )
reg( 'pS', 'baloncestista' )
reg( 'pS', 'banco' )
reg( 'pS', 'banda' )
reg( 'pS', 'bandera' )
reg( 'pS', 'bando' )
reg( 'pS', 'barco' )
reg( 'pS', 'barra' )
reg( 'pS', 'barrera')
reg( 'pS', 'barrio' )
reg( 'pS', 'barítono' )
reg( 'pS', 'bastante' )
reg( 'pS', 'basura' )
reg( 'pS', 'batalla' )
reg( 'pS', 'baterista' )
reg( 'pS', 'batería' )
reg( 'pS', 'baño' )
reg( 'pS', 'bebé' )
reg( 'pS', 'beisbolista' )
reg( 'pS', 'belga' )
reg( 'pS', 'belleza' )
reg( 'pS', 'beneficio' )
reg( 'pS', 'bestia' )
reg( 'pS', 'biblioteca')
reg( 'pS', 'bicicleta' )
reg( 'pS', 'billete' )
reg( 'pS', 'blindaje' )
reg( 'pS', 'blog' )
reg( 'pS', 'bloque' )
reg( 'pS', 'bloqueo' )
reg( 'pS', 'boca' )
reg( 'pS', 'boda' )
reg( 'pS', 'bodega' )
reg( 'pS', 'bola' )
reg( 'pS', 'bolsa' )
reg( 'pS', 'bomba' )
reg( 'pS', 'bombardeo' )
reg( 'pS', 'borde', 'bordes' )
reg( 'pS', 'bosque' )
reg( 'pS', 'bosquejo' )
reg( 'pS', 'botella' )
reg( 'pS', 'brazo' )
reg( 'pS', 'breve' )
reg( 'pS', 'brigada' )
reg( 'pS', 'brillante' )
reg( 'pS', 'broma' )
reg( 'pS', 'bronce' )
reg( 'pS', 'budista' )
reg( 'pS', 'buque' )
reg( 'pS', 'burbuja' )
reg( 'pS', 'busto' )
reg( 'pS', 'byte' )
reg( 'pS', 'bóveda' )
reg( 'pS', 'caballero' )
reg( 'pS', 'caballería' )
reg( 'pS', 'caballo' )
reg( 'pS', 'cabecera' )
reg( 'pS', 'cabello')
reg( 'pS', 'cabeza' )
reg( 'pS', 'cabildo' )
reg( 'pS', 'cabina' )
reg( 'pS', 'cable' )
reg( 'pS', 'cadena')
reg( 'pS', 'café' )
reg( 'pS', 'caja' )
reg( 'pS', 'calcio' )
reg( 'pS', 'caldera' )
reg( 'pS', 'calendario' )
reg( 'pS', 'calibre' )
reg( 'pS', 'caligrafía' )
reg( 'pS', 'caliza' )
reg( 'pS', 'cama' )
reg( 'pS', 'cambiante' )
reg( 'pS', 'cambio' )
reg( 'pS', 'camino' )
reg( 'pS', 'camiseta' )
reg( 'pS', 'campamento' )
reg( 'pS', 'campana' )
reg( 'pS', 'campanario' )
reg( 'pS', 'campaña' )
reg( 'pS', 'campeonato' )
reg( 'pS', 'campo' )
reg( 'pS', 'canadiense' )
reg( 'pS', 'cancha' )
reg( 'pS', 'candidatura' )
reg( 'pS', 'cantante' )
reg( 'pS', 'cantera' )
reg( 'pS', 'canto' )
reg( 'pS', 'capa' )
reg( 'pS', 'capilla' )
reg( 'pS', 'capítulo' )
reg( 'pS', 'cara' )
reg( 'pS', 'característica' )
reg( 'pS', 'carbono' )
reg( 'pS', 'cargo' )
reg( 'pS', 'carlista' )
reg( 'pS', 'carne' )
reg( 'pS', 'carpeta' )
reg( 'pS', 'carrera' )
reg( 'pS', 'carretera' )
reg( 'pS', 'carro' )
reg( 'pS', 'carrocería' )
reg( 'pS', 'carta' )
reg( 'pS', 'carátula' )
reg( 'pS', 'casa')
reg( 'pS', 'casco' )
reg( 'pS', 'casilla' )
reg( 'pS', 'caso' )
reg( 'pS', 'casona' )
reg( 'pS', 'castigo' )
reg( 'pS', 'castillo' )
reg( 'pS', 'cataclismo' )
reg( 'pS', 'catedral' )
reg( 'pS', 'categoría' )
reg( 'pS', 'catálogo' )
reg( 'pS', 'cauce' )
reg( 'pS', 'caudillo' )
reg( 'pS', 'causa' )
reg( 'pS', 'causante' )
reg( 'pS', 'cavernícola' )
reg( 'pS', 'caña' )
reg( 'pS', 'celda' )
reg( 'pS', 'celeste' )
reg( 'pS', 'celta' )
reg( 'pS', 'cementerio' )
reg( 'pS', 'ceniza' )
reg( 'pS', 'censo' )
reg( 'pS', 'centenario' )
reg( 'pS', 'centro' )
reg( 'pS', 'centrocampista' )
reg( 'pS', 'centímetro' )
reg( 'pS', 'cercanía' )
reg( 'pS', 'ceremonia' )
reg( 'pS', 'cero' )
reg( 'pS', 'cerro' )
reg( 'pS', 'cerveza' )
reg( 'pS', 'chat' )
reg( 'pS', 'chimpancé' )
reg( 'pS', 'chocolate' )
reg( 'pS', 'chuleta' )
reg( 'pS', 'cianobacteria' )
reg( 'pS', 'ciclista' )
reg( 'pS', 'ciclo' )
reg( 'pS', 'cielo' )
reg( 'pS', 'ciencia' )
reg( 'pS', 'ciento' )
reg( 'pS', 'cierto' )
reg( 'pS', 'cilindro' )
reg( 'pS', 'cima' )
reg( 'pS', 'cimiento' )
reg( 'pS', 'cine' )
reg( 'pS', 'cineasta' )
reg( 'pS', 'cinta' )
reg( 'pS', 'circo' )
reg( 'pS', 'circuito' )
reg( 'pS', 'circundante' )
reg( 'pS', 'circunstancia' )
reg( 'pS', 'cirugía' )
reg( 'pS', 'ciudadania' )
reg( 'pS', 'clase' )
reg( 'pS', 'clasificado' )
reg( 'pS', 'claustro' )
reg( 'pS', 'clave')
reg( 'pS', 'clero' )
reg( 'pS', 'cliente' )
reg( 'pS', 'clima' )
reg( 'pS', 'cloroplasto' )
reg( 'pS', 'cobertura' )
reg( 'pS', 'coche' )
reg( 'pS', 'cocodrilo' )
reg( 'pS', 'cofradía' )
reg( 'pS', 'coherente')
reg( 'pS', 'cohete' )
reg( 'pS', 'cohorte' )
reg( 'pS', 'cola' )
reg( 'pS', 'coleccionista' )
reg( 'pS', 'colega' )
reg( 'pS', 'colegio' )
reg( 'pS', 'colgante' )
reg( 'pS', 'colina' )
reg( 'pS', 'colindante' )
reg( 'pS', 'colonia' )
reg( 'pS', 'colono' )
reg( 'pS', 'colorante' )
reg( 'pS', 'columna' )
reg( 'pS', 'comandante' )
reg( 'pS', 'comando' )
reg( 'pS', 'comarca' )
reg( 'pS', 'combate' )
reg( 'pS', 'combatiente' )
reg( 'pS', 'combustible' )
reg( 'pS', 'comedia' )
reg( 'pS', 'comediante' )
reg( 'pS', 'comentario' )
reg( 'pS', 'comerciante' )
reg( 'pS', 'comercio' )
reg( 'pS', 'comienzo' )
reg( 'pS', 'comité' )
reg( 'pS', 'compatible' )
reg( 'pS', 'compañía' )
reg( 'pS', 'competencia' )
reg( 'pS', 'competente' )
reg( 'pS', 'complementario' )
reg( 'pS', 'componente' )
reg( 'pS', 'comportamiento' )
reg( 'pS', 'compromiso' )
reg( 'pS', 'comuna' )
reg( 'pS', 'comunista' )
reg( 'pS', 'concejo' )
reg( 'pS', 'concepto' )
reg( 'pS', 'concha' )
reg( 'pS', 'concierto' )
reg( 'pS', 'concurrente' )
reg( 'pS', 'concursante' )
reg( 'pS', 'concurso' )
reg( 'pS', 'condado' )
reg( 'pS', 'conde' )
reg( 'pS', 'condesa' )
reg( 'pS', 'conducta' )
reg( 'pS', 'conexionista' )
reg( 'pS', 'conferencia' )
reg( 'pS', 'conflicto' )
reg( 'pS', 'congreso' )
reg( 'pS', 'conjunto' )
reg( 'pS', 'conncursante' )
reg( 'pS', 'cono' )
reg( 'pS', 'conocimiento' )
reg( 'pS', 'consciente' )
reg( 'pS', 'consecuencia' )
reg( 'pS', 'consejo' )
reg( 'pS', 'considerable' )
reg( 'pS', 'consiguiente' )
reg( 'pS', 'consistente' )
reg( 'pS', 'consola' )
reg( 'pS', 'consonante' )
reg( 'pS', 'consorte' )
reg( 'pS', 'constante' )
reg( 'pS', 'consulta' )
reg( 'pS', 'contacto' )
reg( 'pS', 'contaminante' )
reg( 'pS', 'contenido' )
reg( 'pS', 'continente' )
reg( 'pS', 'contorno' )
reg( 'pS', 'contraseña' )
reg( 'pS', 'contratista' )
reg( 'pS', 'contrato' )
reg( 'pS', 'contrincante' )
reg( 'pS', 'controversia' )
reg( 'pS', 'convento' )
reg( 'pS', 'convocatoria' )
reg( 'pS', 'coordenada' )
reg( 'pS', 'copia' )
reg( 'pS', 'copo', 'copos' )
reg( 'pS', 'corchete' )
reg( 'pS', 'cordillera' )
reg( 'pS', 'coro' )
reg( 'pS', 'correo' )
reg( 'pS', 'correspondiente' )
reg( 'pS', 'corriente' )
reg( 'pS', 'corteza' )
reg( 'pS', 'corto' )
reg( 'pS', 'cortometraje' )
reg( 'pS', 'cosa' )
reg( 'pS', 'costa' )
reg( 'pS', 'costarricense' )
reg( 'pS', 'coste' )
reg( 'pS', 'costilla' )
reg( 'pS', 'costo' )
reg( 'pS', 'costumbre' )
reg( 'pS', 'cota' )
reg( 'pS', 'creacionista' )
reg( 'pS', 'creciente' )
reg( 'pS', 'creencia' )
reg( 'pS', 'crema' )
reg( 'pS', 'creyente' )
reg( 'pS', 'criatura' )
reg( 'pS', 'criterio' )
reg( 'pS', 'croata' )
reg( 'pS', 'cromosoma' )
reg( 'pS', 'cromosómico' )
reg( 'pS', 'cronista' )
reg( 'pS', 'cronología' )
reg( 'pS', 'crucero' )
reg( 'pS', 'crustáceo' )
reg( 'pS', 'cruzamiento' )
reg( 'pS', 'cráneo' )
reg( 'pS', 'crédito' )
reg( 'pS', 'cuadra' )
reg( 'pS', 'cuadrante' )
reg( 'pS', 'cuadro' )
reg( 'pS', 'cubo' )
reg( 'pS', 'cucharada' )
reg( 'pS', 'cuello' )
reg( 'pS', 'cuenca' )
reg( 'pS', 'cuenta' )
reg( 'pS', 'cuento' )
reg( 'pS', 'cuerda' )
reg( 'pS', 'cuerno' )
reg( 'pS', 'cuero' )
reg( 'pS', 'cuerpo' )
reg( 'pS', 'cuestionario' )
reg( 'pS', 'cueva' )
reg( 'pS', 'culminante' )
reg( 'pS', 'culpable' )
reg( 'pS', 'cultivo' )
reg( 'pS', 'culto' )
reg( 'pS', 'cultura' )
reg( 'pS', 'cumbre' )
reg( 'pS', 'cuota' )
reg( 'pS', 'currículo' )
reg( 'pS', 'curso' )
reg( 'pS', 'curva' )
reg( 'pS', 'cálculo' )
reg( 'pS', 'cámara' )
reg( 'pS', 'cápsula' )
reg( 'pS', 'cátedra' )
reg( 'pS', 'célebre' )
reg( 'pS', 'célula' )
reg( 'pS', 'céntimo' )
reg( 'pS', 'círculo' )
reg( 'pS', 'códice' )
reg( 'pS', 'código' )
reg( 'pS', 'cómic' )
reg( 'pS', 'cónyuge' )
reg( 'pS', 'cúpula' )
reg( 'pS', 'dama' )
reg( 'pS', 'dato' )
reg( 'pS', 'daño' )
reg( 'pS', 'debate' )
reg( 'pS', 'decena' )
reg( 'pS', 'decepcionante')
reg( 'pS', 'decisivo' )
reg( 'pS', 'decreciente' )
reg( 'pS', 'dedo' )
reg( 'pS', 'defecto' )
reg( 'pS', 'defensa' )
reg( 'pS', 'deficiencia' )
reg( 'pS', 'delito' )
reg( 'pS', 'democracia' )
reg( 'pS', 'demografía' )
reg( 'pS', 'demócrata' )
reg( 'pS', 'denuncia' )
reg( 'pS', 'departamento' )
reg( 'pS', 'dependencia' )
reg( 'pS', 'dependiente' )
reg( 'pS', 'deporte' )
reg( 'pS', 'deportista' )
reg( 'pS', 'depósito' )
reg( 'pS', 'derecho')
reg( 'pS', 'desarrollo' )
reg( 'pS', 'desastre')
reg( 'pS', 'desbordamiento')
reg( 'pS', 'descendencia' )
reg( 'pS', 'descendiente' )
reg( 'pS', 'descenso' )
reg( 'pS', 'descubrimiento' )
reg( 'pS', 'desembarco' )
reg( 'pS', 'desembocadura' )
reg( 'pS', 'desencadenante' )
reg( 'pS', 'deseo' )
reg( 'pS', 'desfavorable' )
reg( 'pS', 'desierto' )
reg( 'pS', 'desplazamiento' )
reg( 'pS', 'desplegable' )
reg( 'pS', 'destino' )
reg( 'pS', 'desvío' )
reg( 'pS', 'detalle' )
reg( 'pS', 'detective' )
reg( 'pS', 'determinante' )
reg( 'pS', 'determinista' )
reg( 'pS', 'deuda' )
reg( 'pS', 'diablo' )
reg( 'pS', 'diagnóstico' )
reg( 'pS', 'diagrama' )
reg( 'pS', 'dialecto' )
reg( 'pS', 'diamante' )
reg( 'pS', 'dibujante' )
reg( 'pS', 'dibujo' )
reg( 'pS', 'diccionario' )
reg( 'pS', 'dictadura' )
reg( 'pS', 'dieta' )
reg( 'pS', 'diferencia' )
reg( 'pS', 'diferente' )
reg( 'pS', 'dilema' )
reg( 'pS', 'dinastía' )
reg( 'pS', 'dinero' )
reg( 'pS', 'dinosaurio' )
reg( 'pS', 'dirigente' )
reg( 'pS', 'disciplina' )
reg( 'pS', 'disco' )
reg( 'pS', 'discrepancia' )
reg( 'pS', 'discurso' )
reg( 'pS', 'discípulo' )
reg( 'pS', 'diseño' )
reg( 'pS', 'disparo' )
reg( 'pS', 'disponible' )
reg( 'pS', 'dispositivo' )
reg( 'pS', 'dispuesto' )
reg( 'pS', 'disputa' )
reg( 'pS', 'distancia' )
reg( 'pS', 'distante' )
reg( 'pS', 'distrito' )
reg( 'pS', 'disturbio' )
reg( 'pS', 'divergente' )
reg( 'pS', 'divorcio' )
reg( 'pS', 'diálogo' )
reg( 'pS', 'diámetro' )
reg( 'pS', 'docena' )
reg( 'pS', 'docente' )
reg( 'pS', 'doctrina' )
reg( 'pS', 'documento' )
reg( 'pS', 'dogma' )
reg( 'pS', 'domicilio' )
reg( 'pS', 'dominante' )
reg( 'pS', 'domingo' )
reg( 'pS', 'dominio' )
reg( 'pS', 'donante' )
reg( 'pS', 'drama' )
reg( 'pS', 'ducado' )
reg( 'pS', 'dulce' )
reg( 'pS', 'duna' )
reg( 'pS', 'duque' )
reg( 'pS', 'década' )
reg( 'pS', 'décimo' )
reg( 'pS', 'día' )
reg( 'pS', 'dígito' )
reg( 'pS', 'dúo' )
reg( 'pS', 'economista' )
reg( 'pS', 'economía' )
reg( 'pS', 'ecosistema' )
reg( 'pS', 'ecozona' )
reg( 'pS', 'edificio' )
reg( 'pS', 'efecto' )
reg( 'pS', 'eje' )
reg( 'pS', 'ejecutable' )
reg( 'pS', 'ejemplo' )
reg( 'pS', 'ejercicio' )
reg( 'pS', 'ejército' )
reg( 'pS', 'elefante' )
reg( 'pS', 'elegante' )
reg( 'pS', 'elemento' )
reg( 'pS', 'eliminatoria' )
reg( 'pS', 'elipse', 'elipses' )
reg( 'pS', 'embajada' )
reg( 'pS', 'embalse' )
reg( 'pS', 'embarazo' )
reg( 'pS', 'emblema' )
reg( 'pS', 'emergencia' )
reg( 'pS', 'emergente' )
reg( 'pS', 'emigrante' )
reg( 'pS', 'emisora' )
reg( 'pS', 'emocionante' )
reg( 'pS', 'emplazamiento' )
reg( 'pS', 'empleo' )
reg( 'pS', 'empresa')
reg( 'pS', 'encargo' )
reg( 'pS', 'enciclopedia' )
reg( 'pS', 'encuentro' )
reg( 'pS', 'encuesta' )
reg( 'pS', 'endógeno' )
reg( 'pS', 'enemigo' )
reg( 'pS', 'energía' )
reg( 'pS', 'enfermo' )
reg( 'pS', 'enfrentamiento' )
reg( 'pS', 'engranaje' )
reg( 'pS', 'enlace' )
reg( 'pS', 'enorme' )
reg( 'pS', 'ensamblaje' )
reg( 'pS', 'ensayo' )
reg( 'pS', 'enseñanza' )
reg( 'pS', 'entorno' )
reg( 'pS', 'entrada' )
reg( 'pS', 'entrante' )
reg( 'pS', 'entrenamiento' )
reg( 'pS', 'entretenimiento' )
reg( 'pS', 'envoltura' )
reg( 'pS', 'enzima' )
reg( 'pS', 'epidemia' )
reg( 'pS', 'episodio' )
reg( 'pS', 'epíteto' )
reg( 'pS', 'equilibrio' )
reg( 'pS', 'equipamiento' )
reg( 'pS', 'equipo' )
reg( 'pS', 'equivalente' )
reg( 'pS', 'ermita' )
reg( 'pS', 'errante' )
reg( 'pS', 'erudito' )
reg( 'pS', 'esbozo')
reg( 'pS', 'escala' )
reg( 'pS', 'escalera' )
reg( 'pS', 'escama' )
reg( 'pS', 'escaño' )
reg( 'pS', 'escena' )
reg( 'pS', 'escenario' )
reg( 'pS', 'escenografía' )
reg( 'pS', 'esclavo' )
reg( 'pS', 'escritura' )
reg( 'pS', 'escuadra' )
reg( 'pS', 'escudo' )
reg( 'pS', 'escuela' )
reg( 'pS', 'escultura' )
reg( 'pS', 'escándalo' )
reg( 'pS', 'esencia' )
reg( 'pS', 'esencial' )
reg( 'pS', 'esfera' )
reg( 'pS', 'esfuerzo' )
reg( 'pS', 'espacio' )
reg( 'pS', 'espada' )
reg( 'pS', 'espalda' )
reg( 'pS', 'especia' )
reg( 'pS', 'especialista' )
reg( 'pS', 'especie' )
reg( 'pS', 'espectaculo' )
reg( 'pS', 'espectro' )
reg( 'pS', 'espectáculo' )
reg( 'pS', 'espejo' )
reg( 'pS', 'espermatozoide' )
reg( 'pS', 'espina' )
reg( 'pS', 'esponja' )
reg( 'pS', 'espía')
reg( 'pS', 'espíritu' )
reg( 'pS', 'esqueleto' )
reg( 'pS', 'esquema' )
reg( 'pS', 'esquina' )
reg( 'pS', 'estable' )
reg( 'pS', 'establecimiento' )
reg( 'pS', 'estadio' )
reg( 'pS', 'estadistica' )
reg( 'pS', 'estado' )
reg( 'pS', 'estadounidense' )
reg( 'pS', 'estambre' )
reg( 'pS', 'estancia' )
reg( 'pS', 'estatua' )
reg( 'pS', 'estatura' )
reg( 'pS', 'estatuto' )
reg( 'pS', 'estereotipo' )
reg( 'pS', 'estilo' )
reg( 'pS', 'estimulante' )
reg( 'pS', 'estrategia')
reg( 'pS', 'estrato' )
reg( 'pS', 'estrella' )
reg( 'pS', 'estrofa' )
reg( 'pS', 'estructura' )
reg( 'pS', 'estudiante' )
reg( 'pS', 'estudio' )
reg( 'pS', 'estático' )
reg( 'pS', 'etapa' )
reg( 'pS', 'etiqueta' )
reg( 'pS', 'etnia' )
reg( 'pS', 'eucarionte' )
reg( 'pS', 'eucariota' )
reg( 'pS', 'euro')
reg( 'pS', 'evento' )
reg( 'pS', 'evidencia' )
reg( 'pS', 'evidente' )
reg( 'pS', 'evolucionista' )
reg( 'pS', 'examen', 'exámenes' )
reg( 'pS', 'excelente' )
reg( 'pS', 'exceso' )
reg( 'pS', 'excluyente' )
reg( 'pS', 'exigencia' )
reg( 'pS', 'exilio' )
reg( 'pS', 'existente' )
reg( 'pS', 'expectativa' )
reg( 'pS', 'experiencia' )
reg( 'pS', 'experimento')
reg( 'pS', 'extinción' )
reg( 'pS', 'extra' )
reg( 'pS', 'extravagante' )
reg( 'pS', 'exuberante' )
reg( 'pS', 'exónimo' )
reg( 'pS', 'fabricante' )
reg( 'pS', 'fachada' )
reg( 'pS', 'factible' )
reg( 'pS', 'factoría' )
reg( 'pS', 'falda' )
reg( 'pS', 'fallecimiento' )
reg( 'pS', 'falta' )
reg( 'pS', 'fama' )
reg( 'pS', 'familia' )
reg( 'pS', 'fantasma' )
reg( 'pS', 'fantasía' )
reg( 'pS', 'faro' )
reg( 'pS', 'fase' )
reg( 'pS', 'favorable' )
reg( 'pS', 'fecha' )
reg( 'pS', 'fenotipo' )
reg( 'pS', 'fenómeno')
reg( 'pS', 'feria' )
reg( 'pS', 'fiable' )
reg( 'pS', 'fibra' )
reg( 'pS', 'ficha' )
reg( 'pS', 'fichero')
reg( 'pS', 'fiebre' )
reg( 'pS', 'fiesta' )
reg( 'pS', 'figura' )
reg( 'pS', 'fila' )
reg( 'pS', 'filiforme' )
reg( 'pS', 'film' )
reg( 'pS', 'filo' )
reg( 'pS', 'filosofía' )
reg( 'pS', 'filtro' )
reg( 'pS', 'finalista' )
reg( 'pS', 'financiamiento' )
reg( 'pS', 'finanza' )
reg( 'pS', 'finca' )
reg( 'pS', 'fino' )
reg( 'pS', 'firewall')
reg( 'pS', 'firma')
reg( 'pS', 'firmante' )
reg( 'pS', 'flamante' )
reg( 'pS', 'flauta' )
reg( 'pS', 'flecha' )
reg( 'pS', 'flora' )
reg( 'pS', 'flotante' )
reg( 'pS', 'flujo' )
reg( 'pS', 'fondo')
reg( 'pS', 'forma' )
reg( 'pS', 'formato' )
reg( 'pS', 'formulario' )
reg( 'pS', 'foro' )
reg( 'pS', 'fortaleza' )
reg( 'pS', 'fortuna' )
reg( 'pS', 'fosa' )
reg( 'pS', 'foto' )
reg( 'pS', 'fotografía' )
reg( 'pS', 'fragata' )
reg( 'pS', 'fragmento' )
reg( 'pS', 'franja' )
reg( 'pS', 'franquicia' )
reg( 'pS', 'franquista' )
reg( 'pS', 'frase' )
reg( 'pS', 'frecuencia' )
reg( 'pS', 'frecuente' )
reg( 'pS', 'freguesia' )
reg( 'pS', 'frontera' )
reg( 'pS', 'fruta' )
reg( 'pS', 'fruto' )
reg( 'pS', 'fuego' )
reg( 'pS', 'fuente' )
reg( 'pS', 'fuerte', 'fortísimo', 'fortísima', 'fortísimos', 'fortísimas' )
reg( 'pS', 'fuerza' )
reg( 'pS', 'fundamentalista' )
reg( 'pS', 'futbolista' )
reg( 'pS', 'futuro' )
reg( 'pS', 'fábrica' )
reg( 'pS', 'fármaco' )
reg( 'pS', 'físico' )
reg( 'pS', 'fórmula' )
reg( 'pS', 'gabinete' )
reg( 'pS', 'gafa' )
reg( 'pS', 'gala' )
reg( 'pS', 'galaxia' )
reg( 'pS', 'galería' )
reg( 'pS', 'gameto' )
reg( 'pS', 'ganadería' )
reg( 'pS', 'ganancia' )
reg( 'pS', 'garabato' )
reg( 'pS', 'garantía')
reg( 'pS', 'garganta' )
reg( 'pS', 'garra' )
reg( 'pS', 'gasto' )
reg( 'pS', 'gastronomía' )
reg( 'pS', 'gato' )
reg( 'pS', 'genio' )
reg( 'pS', 'genoma' )
reg( 'pS', 'genotipo' )
reg( 'pS', 'gente' )
reg( 'pS', 'gentilicio' )
reg( 'pS', 'geometría' )
reg( 'pS', 'gerente' )
reg( 'pS', 'gesto')
reg( 'pS', 'gigante' )
reg( 'pS', 'globo' )
reg( 'pS', 'glándula' )
reg( 'pS', 'gobernante' )
reg( 'pS', 'gobierno' )
reg( 'pS', 'golpe' )
reg( 'pS', 'gota' )
reg( 'pS', 'gracia' )
reg( 'pS', 'grada' )
reg( 'pS', 'gradiente' )
reg( 'pS', 'grado' )
reg( 'pS', 'gradualista' )
reg( 'pS', 'grafo' )
reg( 'pS', 'granada' )
reg( 'pS', 'grande', 'grandísimo', 'grandísima', 'grandísimos', 'grandísimas' )
reg( 'pS', 'granito' )
reg( 'pS', 'granja' )
reg( 'pS', 'grano' )
reg( 'pS', 'grasa' )
reg( 'pS', 'grave', 'gravísimo', 'gravísima', 'gravísimos', 'gravísimas' )
reg( 'pS', 'grieta' )
reg( 'pS', 'gripe' )
reg( 'pS', 'grupo' )
reg( 'pS', 'guante' )
reg( 'pS', 'guantes' )
reg( 'pS', 'guardaespalda' )
reg( 'pS', 'guardia' )
reg( 'pS', 'guerra' )
reg( 'pS', 'guerrilla' )
reg( 'pS', 'guionista' )
reg( 'pS', 'guitarra' )
reg( 'pS', 'guitarrista' )
reg( 'pS', 'guía' )
reg( 'pS', 'género' )
reg( 'pS', 'habitante' )
reg( 'pS', 'hablante' )
reg( 'pS', 'hacienda' )
reg( 'pS', 'hacker')
reg( 'pS', 'hada' )
reg( 'pS', 'hallazgo' )
reg( 'pS', 'harina' )
reg( 'pS', 'hazaña' )
reg( 'pS', 'hectárea' )
reg( 'pS', 'helicóptero' )
reg( 'pS', 'hembra' )
reg( 'pS', 'hendidura' )
reg( 'pS', 'heredable' )
reg( 'pS', 'herencia' )
reg( 'pS', 'hermafrodita' )
reg( 'pS', 'herramienta' )
reg( 'pS', 'heterónimo' )
reg( 'pS', 'heurística' )
reg( 'pS', 'hidrógeno' )
reg( 'pS', 'hidrónimo' )
reg( 'pS', 'hierba' )
reg( 'pS', 'himno' )
reg( 'pS', 'hispanohablante' )
reg( 'pS', 'historia' )
reg( 'pS', 'historieta' )
reg( 'pS', 'historietista' )
reg( 'pS', 'hito' )
reg( 'pS', 'hoja' )
reg( 'pS', 'hombre' )
reg( 'pS', 'hombro' )
reg( 'pS', 'homenaje' )
reg( 'pS', 'homólogo' )
reg( 'pS', 'hongo' )
reg( 'pS', 'hora', 'horas' )
reg( 'pS', 'hormiga' )
reg( 'pS', 'hormona' )
reg( 'pS', 'horno' )
reg( 'pS', 'hortaliza' )
reg( 'pS', 'huelga' )
reg( 'pS', 'hueso' )
reg( 'pS', 'huevo' )
reg( 'pS', 'humano' )
reg( 'pS', 'humilde' )
reg( 'pS', 'humo' )
reg( 'pS', 'huso' )
reg( 'pS', 'hábitat' )
reg( 'pS', 'hábito' )
reg( 'pS', 'hélice' )
reg( 'pS', 'héroe' )
reg( 'pS', 'idea' )
reg( 'pS', 'ideología' )
reg( 'pS', 'idioma' )
reg( 'pS', 'iglesia' )
reg( 'pS', 'imperante' )
reg( 'pS', 'imperio' )
reg( 'pS', 'importable' )
reg( 'pS', 'importante', 'importantísimo', 'importantísima', 'importantísimos', 'importantísimas' )
reg( 'pS', 'imposible' )
reg( 'pS', 'imprenta' )
reg( 'pS', 'impresionante' )
reg( 'pS', 'imprevisible')
reg( 'pS', 'inca' )
reg( 'pS', 'incendio')
reg( 'pS', 'incentivo' )
reg( 'pS', 'incidencia')
reg( 'pS', 'incidente')
reg( 'pS', 'incompatible')
reg( 'pS', 'inconveniente' )
reg( 'pS', 'independencia' )
reg( 'pS', 'independentista' )
reg( 'pS', 'independiente')
reg( 'pS', 'indicio' )
reg( 'pS', 'indio' )
reg( 'pS', 'indispensable')
reg( 'pS', 'individuo' )
reg( 'pS', 'industria' )
reg( 'pS', 'indígena' )
reg( 'pS', 'inevitable')
reg( 'pS', 'infancia' )
reg( 'pS', 'infante' )
reg( 'pS', 'infierno' )
reg( 'pS', 'inflorescencia' )
reg( 'pS', 'influencia' )
reg( 'pS', 'influyente' )
reg( 'pS', 'infraestructura' )
reg( 'pS', 'ingrediente' )
reg( 'pS', 'ingreso' )
reg( 'pS', 'iniciativa' )
reg( 'pS', 'inicio' )
reg( 'pS', 'inmigrante' )
reg( 'pS', 'inmune' )
reg( 'pS', 'inmutable' )
reg( 'pS', 'innato' )
reg( 'pS', 'innecesario' )
reg( 'pS', 'innumerable' )
reg( 'pS', 'insecto' )
reg( 'pS', 'inservible')
reg( 'pS', 'insignia' )
reg( 'pS', 'insignificante' )
reg( 'pS', 'instancia' )
reg( 'pS', 'instante' )
reg( 'pS', 'instituto' )
reg( 'pS', 'instrumento' )
reg( 'pS', 'integrante' )
reg( 'pS', 'integrista' )
reg( 'pS', 'inteligencia' )
reg( 'pS', 'inteligente', 'inteligentísimo', 'inteligentísima', 'inteligentísimos', 'inteligentísimas' )
reg( 'pS', 'intendente' )
reg( 'pS', 'intento' )
reg( 'pS', 'intercambio' )
reg( 'pS', 'interesante' )
reg( 'pS', 'interferencia' )
reg( 'pS', 'intermitente' )
reg( 'pS', 'interrogante' )
reg( 'pS', 'intervalo' )
reg( 'pS', 'intratable' )
reg( 'pS', 'intruso')
reg( 'pS', 'intérprete' )
reg( 'pS', 'invertebrado' )
reg( 'pS', 'invierno' )
reg( 'pS', 'irrelevante' )
reg( 'pS', 'irreparable' )
reg( 'pS', 'isla' )
reg( 'pS', 'itinerante' )
reg( 'pS', 'izquierda' )
reg( 'pS', 'jefe' )
reg( 'pS', 'jerarquía' )
reg( 'pS', 'jesuita' )
reg( 'pS', 'jinete' )
reg( 'pS', 'jornada' )
reg( 'pS', 'joya' )
reg( 'pS', 'juego' )
reg( 'pS', 'jugo' )
reg( 'pS', 'juguete' )
reg( 'pS', 'juicio' )
reg( 'pS', 'jurista' )
reg( 'pS', 'justicia' )
reg( 'pS', 'kilómetro' )
reg( 'pS', 'labio' )
reg( 'pS', 'laboratorio' )
reg( 'pS', 'ladera' )
reg( 'pS', 'lado' )
reg( 'pS', 'ladrillo')
reg( 'pS', 'lago' )
reg( 'pS', 'laguna' )
reg( 'pS', 'lancha' )
reg( 'pS', 'lanzamiento' )
reg( 'pS', 'largometraje' )
reg( 'pS', 'larva' )
reg( 'pS', 'lazo' )
reg( 'pS', 'leche' )
reg( 'pS', 'lectura' )
reg( 'pS', 'legible' )
reg( 'pS', 'legislatura' )
reg( 'pS', 'legua' )
reg( 'pS', 'lema' )
reg( 'pS', 'lengua' )
reg( 'pS', 'lenguaje' )
reg( 'pS', 'letra' )
reg( 'pS', 'leyenda' )
reg( 'pS', 'liberal' )
reg( 'pS', 'libre' )
reg( 'pS', 'librería' )
reg( 'pS', 'libretista' )
reg( 'pS', 'libro' )
reg( 'pS', 'licencia' )
reg( 'pS', 'licenciatura' )
reg( 'pS', 'lienzo' )
reg( 'pS', 'limitante' )
reg( 'pS', 'limítrofe' )
reg( 'pS', 'linaje' )
reg( 'pS', 'lindante' )
reg( 'pS', 'linea' )
reg( 'pS', 'lineamiento' )
reg( 'pS', 'literatura' )
reg( 'pS', 'litro' )
reg( 'pS', 'llanura' )
reg( 'pS', 'llave')
reg( 'pS', 'lluvia' )
reg( 'pS', 'locomotora' )
reg( 'pS', 'locura' )
reg( 'pS', 'logo' )
reg( 'pS', 'logotipo' )
reg( 'pS', 'logro' )
reg( 'pS', 'lote' )
reg( 'pS', 'lucha' )
reg( 'pS', 'lucro' )
reg( 'pS', 'lujo' )
reg( 'pS', 'luna' )
reg( 'pS', 'lágrima' )
reg( 'pS', 'lámina' )
reg( 'pS', 'lámpara' )
reg( 'pS', 'límite' )
reg( 'pS', 'línea' )
reg( 'pS', 'líquido' )
reg( 'pS', 'macho' )
reg( 'pS', 'macro')
reg( 'pS', 'macromolécula' )
reg( 'pS', 'madera' )
reg( 'pS', 'madre' )
reg( 'pS', 'maestría' )
reg( 'pS', 'mafia' )
reg( 'pS', 'magia' )
reg( 'pS', 'malla')
reg( 'pS', 'mamífero' )
reg( 'pS', 'mancha' )
reg( 'pS', 'mandato' )
reg( 'pS', 'mando' )
reg( 'pS', 'manejable' )
reg( 'pS', 'manera' )
reg( 'pS', 'manifestante' )
reg( 'pS', 'mano')
reg( 'pS', 'manuscrito' )
reg( 'pS', 'manzana' )
reg( 'pS', 'mapa' )
reg( 'pS', 'maquillaje' )
reg( 'pS', 'maquinaria' )
reg( 'pS', 'marca' )
reg( 'pS', 'marco' )
reg( 'pS', 'marido' )
reg( 'pS', 'marinero' )
reg( 'pS', 'mariposa' )
reg( 'pS', 'masa' )
reg( 'pS', 'mascota' )
reg( 'pS', 'matemática' )
reg( 'pS', 'materia' )
reg( 'pS', 'matrimonio' )
reg( 'pS', 'maya' )
reg( 'pS', 'mañana' )
reg( 'pS', 'mecanismo' )
reg( 'pS', 'mecena' )
reg( 'pS', 'medalla' )
reg( 'pS', 'media' )
reg( 'pS', 'medicamento' )
reg( 'pS', 'medida' )
reg( 'pS', 'medio')
reg( 'pS', 'mediocampista' )
reg( 'pS', 'melodía' )
reg( 'pS', 'membrana' )
reg( 'pS', 'memoria' )
reg( 'pS', 'menaje' )
reg( 'pS', 'mensaje' )
reg( 'pS', 'mentira' )
reg( 'pS', 'menú' )
reg( 'pS', 'mercancía' )
reg( 'pS', 'mercante' )
reg( 'pS', 'mercurio' )
reg( 'pS', 'mesa' )
reg( 'pS', 'meseta' )
reg( 'pS', 'meta' )
reg( 'pS', 'metaheurística' )
reg( 'pS', 'metro' )
reg( 'pS', 'metáfora' )
reg( 'pS', 'microbio' )
reg( 'pS', 'microonda' )
reg( 'pS', 'microorganismo' )
reg( 'pS', 'miembro' )
reg( 'pS', 'miga' )
reg( 'pS', 'migrante' )
reg( 'pS', 'milenio' )
reg( 'pS', 'milicia' )
reg( 'pS', 'militante' )
reg( 'pS', 'milla' )
reg( 'pS', 'milímetro' )
reg( 'pS', 'mineral' )
reg( 'pS', 'miniatura' )
reg( 'pS', 'miniserie' )
reg( 'pS', 'ministerio' )
reg( 'pS', 'ministro' )
reg( 'pS', 'minoría' )
reg( 'pS', 'minuto' )
reg( 'pS', 'misa' )
reg( 'pS', 'misterio' )
reg( 'pS', 'mito' )
reg( 'pS', 'mitocondria' )
reg( 'pS', 'mitología' )
reg( 'pS', 'moda' )
reg( 'pS', 'modelo', 'modelos' )
reg( 'pS', 'modo' )
reg( 'pS', 'molino' )
reg( 'pS', 'molusco' )
reg( 'pS', 'molécula' )
reg( 'pS', 'momento' )
reg( 'pS', 'monarca' )
reg( 'pS', 'monarquía' )
reg( 'pS', 'monasterio' )
reg( 'pS', 'moneda' )
reg( 'pS', 'monja' )
reg( 'pS', 'monje' )
reg( 'pS', 'monstruo' )
reg( 'pS', 'montaje' )
reg( 'pS', 'montaña' )
reg( 'pS', 'monumento' )
reg( 'pS', 'motivo' )
reg( 'pS', 'motocicleta' )
reg( 'pS', 'movimiento' )
reg( 'pS', 'mueble' )
reg( 'pS', 'muelle' )
reg( 'pS', 'muerte' )
reg( 'pS', 'muerto' )
reg( 'pS', 'muesca' )
reg( 'pS', 'mundo' )
reg( 'pS', 'municipio' )
reg( 'pS', 'muralla' )
reg( 'pS', 'murciélago' )
reg( 'pS', 'muro' )
reg( 'pS', 'museo' )
reg( 'pS', 'mutante' )
reg( 'pS', 'máquina', 'máquinas' )
reg( 'pS', 'máscara' )
reg( 'pS', 'médico' )
reg( 'pS', 'mérito' )
reg( 'pS', 'método' )
reg( 'pS', 'módulo' )
reg( 'pS', 'múltiple' )
reg( 'pS', 'músculo' )
reg( 'pS', 'nacimiento' )
reg( 'pS', 'nacionalismo' )
reg( 'pS', 'nacionalista' )
reg( 'pS', 'naranja' )
reg( 'pS', 'narrativa' )
reg( 'pS', 'naturaleza' )
reg( 'pS', 'naturalista' )
reg( 'pS', 'nave' )
reg( 'pS', 'navegante' )
reg( 'pS', 'navío' )
reg( 'pS', 'nazi' )
reg( 'pS', 'negocio' )
reg( 'pS', 'nervio' )
reg( 'pS', 'neurona' )
reg( 'pS', 'nicho' )
reg( 'pS', 'nido' )
reg( 'pS', 'nitrógeno' )
reg( 'pS', 'nobiliario' )
reg( 'pS', 'noble' )
reg( 'pS', 'noche' )
reg( 'pS', 'nodo' )
reg( 'pS', 'nombramiento' )
reg( 'pS', 'nombre' )
reg( 'pS', 'norma' )
reg( 'pS', 'nota' )
reg( 'pS', 'notable' )
reg( 'pS', 'noticia' )
reg( 'pS', 'novela' )
reg( 'pS', 'novelista' )
reg( 'pS', 'noveno' )
reg( 'pS', 'nube' )
reg( 'pS', 'nudo' )
reg( 'pS', 'numero' )
reg( 'pS', 'nupcia' )
reg( 'pS', 'nómada' )
reg( 'pS', 'núcleo' )
reg( 'pS', 'número' )
reg( 'pS', 'obispo' )
reg( 'pS', 'objeto' )
reg( 'pS', 'obra' )
reg( 'pS', 'obstáculo' )
reg( 'pS', 'ocupante' )
reg( 'pS', 'océano' )
reg( 'pS', 'oficina' )
reg( 'pS', 'oficio' )
reg( 'pS', 'ofrenda' )
reg( 'pS', 'ojo' )
reg( 'pS', 'ola' )
reg( 'pS', 'onda' )
reg( 'pS', 'oponente' )
reg( 'pS', 'oreja' )
reg( 'pS', 'organismo')
reg( 'pS', 'origen', 'orígenes' )
reg( 'pS', 'orilla' )
reg( 'pS', 'orla' )
reg( 'pS', 'orquídea' )
reg( 'pS', 'oscuro' )
reg( 'pS', 'otoño' )
reg( 'pS', 'oveja' )
reg( 'pS', 'oxígeno' )
reg( 'pS', 'oído' )
reg( 'pS', 'paciente' )
reg( 'pS', 'padre' )
reg( 'pS', 'pago' )
reg( 'pS', 'paisaje' )
reg( 'pS', 'palabra' )
reg( 'pS', 'palacio' )
reg( 'pS', 'paleontólogo' )
reg( 'pS', 'palma' )
reg( 'pS', 'palmera' )
reg( 'pS', 'palo' )
reg( 'pS', 'panorama' )
reg( 'pS', 'pantalla' )
reg( 'pS', 'papa' )
reg( 'pS', 'paquete' )
reg( 'pS', 'paracaída' )
reg( 'pS', 'paraje' )
reg( 'pS', 'paraíso' )
reg( 'pS', 'parcela' )
reg( 'pS', 'pardo' )
reg( 'pS', 'pareja' )
reg( 'pS', 'pariente' )
reg( 'pS', 'parlamento' )
reg( 'pS', 'parque' )
reg( 'pS', 'parroquia' )
reg( 'pS', 'parte' )
reg( 'pS', 'participante' )
reg( 'pS', 'partitura' )
reg( 'pS', 'partícula')
reg( 'pS', 'parámetro' )
reg( 'pS', 'parásito' )
reg( 'pS', 'pasaje' )
reg( 'pS', 'pasajero' )
reg( 'pS', 'paso' )
reg( 'pS', 'pasta' )
reg( 'pS', 'pasto' )
reg( 'pS', 'pata' )
reg( 'pS', 'patata' )
reg( 'pS', 'patio' )
reg( 'pS', 'patria' )
reg( 'pS', 'patrimonio' )
reg( 'pS', 'patriota' )
reg( 'pS', 'pauta' )
reg( 'pS', 'pecho' )
reg( 'pS', 'pelaje')
reg( 'pS', 'peligro' )
reg( 'pS', 'pelo' )
reg( 'pS', 'pelota' )
reg( 'pS', 'peluquería' )
reg( 'pS', 'película' )
reg( 'pS', 'pena' )
reg( 'pS', 'pendiente' )
reg( 'pS', 'pensamiento' )
reg( 'pS', 'península' )
reg( 'pS', 'pequeño' )
reg( 'pS', 'perenne' )
reg( 'pS', 'perihelio' )
reg( 'pS', 'periodista' )
reg( 'pS', 'periodo' )
reg( 'pS', 'perla' )
reg( 'pS', 'permanente' )
reg( 'pS', 'permiso' )
reg( 'pS', 'perro' )
reg( 'pS', 'persa' )
reg( 'pS', 'persistente' )
reg( 'pS', 'persona' )
reg( 'pS', 'personaje' )
reg( 'pS', 'perspectiva' )
reg( 'pS', 'perteneciente' )
reg( 'pS', 'perímetro' )
reg( 'pS', 'período' )
reg( 'pS', 'peseta' )
reg( 'pS', 'peso' )
reg( 'pS', 'peña' )
reg( 'pS', 'pianista' )
reg( 'pS', 'piano' )
reg( 'pS', 'picante' )
reg( 'pS', 'pico' )
reg( 'pS', 'pie' )
reg( 'pS', 'piedra' )
reg( 'pS', 'pierna' )
reg( 'pS', 'pieza' )
reg( 'pS', 'pila' )
reg( 'pS', 'piloto' )
reg( 'pS', 'pincelada' )
reg( 'pS', 'pino' )
reg( 'pS', 'pintura' )
reg( 'pS', 'pirata' )
reg( 'pS', 'piscina' )
reg( 'pS', 'piso' )
reg( 'pS', 'pista' )
reg( 'pS', 'pistola' )
reg( 'pS', 'plana' )
reg( 'pS', 'planeta' )
reg( 'pS', 'plano' )
reg( 'pS', 'planta' )
reg( 'pS', 'plantilla' )
reg( 'pS', 'plata' )
reg( 'pS', 'plataforma' )
reg( 'pS', 'platillo' )
reg( 'pS', 'platino' )
reg( 'pS', 'plato' )
reg( 'pS', 'playa' )
reg( 'pS', 'plaza' )
reg( 'pS', 'plazo' )
reg( 'pS', 'plomo' )
reg( 'pS', 'plugin' )
reg( 'pS', 'pluma' )
reg( 'pS', 'plumaje' )
reg( 'pS', 'pobre' )
reg( 'pS', 'podio' )
reg( 'pS', 'poema' )
reg( 'pS', 'poesía' )
reg( 'pS', 'poeta' )
reg( 'pS', 'policía' )
reg( 'pS', 'polilla' )
reg( 'pS', 'polo' )
reg( 'pS', 'polvo' )
reg( 'pS', 'polígono' )
reg( 'pS', 'política' )
reg( 'pS', 'porcentaje' )
reg( 'pS', 'portero' )
reg( 'pS', 'pose' )
reg( 'pS', 'posgrado' )
reg( 'pS', 'posible' )
reg( 'pS', 'posicionamiento' )
reg( 'pS', 'poste' )
reg( 'pS', 'postulado' )
reg( 'pS', 'postura' )
reg( 'pS', 'potable' )
reg( 'pS', 'potencia' )
reg( 'pS', 'potente' )
reg( 'pS', 'pozo' )
reg( 'pS', 'poácea' )
reg( 'pS', 'practicante' )
reg( 'pS', 'pradera' )
reg( 'pS', 'precedente' )
reg( 'pS', 'precio' )
reg( 'pS', 'predominante' )
reg( 'pS', 'preexistente' )
reg( 'pS', 'prefectura' )
reg( 'pS', 'preferencia' )
reg( 'pS', 'pregunta' )
reg( 'pS', 'premio' )
reg( 'pS', 'premisa' )
reg( 'pS', 'prenda' )
reg( 'pS', 'prensa' )
reg( 'pS', 'presentamo' )
reg( 'pS', 'presidencia' )
reg( 'pS', 'presidente', 'presidenta', 'presidentes', 'presidentas' )
reg( 'pS', 'preso' )
reg( 'pS', 'prestigio' )
reg( 'pS', 'primate' )
reg( 'pS', 'primavera' )
reg( 'pS', 'princesa' )
reg( 'pS', 'principio' )
reg( 'pS', 'privilegio')
reg( 'pS', 'problema' )
reg( 'pS', 'procariota' )
reg( 'pS', 'procedencia' )
reg( 'pS', 'procedente')
reg( 'pS', 'procedimiento')
reg( 'pS', 'proceso' )
reg( 'pS', 'producto' )
reg( 'pS', 'programa' )
reg( 'pS', 'progresista' )
reg( 'pS', 'promedio' )
reg( 'pS', 'promesa' )
reg( 'pS', 'prominente' )
reg( 'pS', 'propaganda' )
reg( 'pS', 'proponente' )
reg( 'pS', 'propuesta' )
reg( 'pS', 'propósito' )
reg( 'pS', 'prosa' )
reg( 'pS', 'protagonista' )
reg( 'pS', 'protestante' )
reg( 'pS', 'proteína' )
reg( 'pS', 'protocolo' )
reg( 'pS', 'prototipo' )
reg( 'pS', 'proveniente' )
reg( 'pS', 'provincia' )
reg( 'pS', 'proyecto' )
reg( 'pS', 'práctica' )
reg( 'pS', 'préstamo' )
reg( 'pS', 'príncipe' )
reg( 'pS', 'prólogo' )
reg( 'pS', 'pseudónimo' )
reg( 'pS', 'pudieron' )
reg( 'pS', 'pueblo' )
reg( 'pS', 'puente' )
reg( 'pS', 'puerta' )
reg( 'pS', 'puerto' )
reg( 'pS', 'puesta' )
reg( 'pS', 'puesto' )
reg( 'pS', 'pulgada' )
reg( 'pS', 'pulso' )
reg( 'pS', 'punta' )
reg( 'pS', 'punto' )
reg( 'pS', 'página' )
reg( 'pS', 'pájaro' )
reg( 'pS', 'párrafo' )
reg( 'pS', 'pérdida' )
reg( 'pS', 'púrpura' )
reg( 'pS', 'queso' )
reg( 'pS', 'quinteto' )
reg( 'pS', 'racimo' )
reg( 'pS', 'radiante' )
reg( 'pS', 'radio' )
reg( 'pS', 'rama' )
reg( 'pS', 'rango' )
reg( 'pS', 'rasgo' )
reg( 'pS', 'rata' )
reg( 'pS', 'raya' )
reg( 'pS', 'rayo' )
reg( 'pS', 'raza' )
reg( 'pS', 'razonable' )
reg( 'pS', 'realista' )
reg( 'pS', 'rebelde' )
reg( 'pS', 'receta' )
reg( 'pS', 'rechazo' )
reg( 'pS', 'reciente' )
reg( 'pS', 'recinto' )
reg( 'pS', 'recomendable' )
reg( 'pS', 'reconocimiento' )
reg( 'pS', 'rectángulo' )
reg( 'pS', 'recuerdo' )
reg( 'pS', 'recurrente' )
reg( 'pS', 'recurso' )
reg( 'pS', 'redundante' )
reg( 'pS', 'reemplazo' )
reg( 'pS', 'referencia' )
reg( 'pS', 'referente' )
reg( 'pS', 'reflejo' )
reg( 'pS', 'reforma' )
reg( 'pS', 'refuerzo' )
reg( 'pS', 'refugio' )
reg( 'pS', 'regimiento' )
reg( 'pS', 'registro' )
reg( 'pS', 'regla' )
reg( 'pS', 'reinante' )
reg( 'pS', 'reino' )
reg( 'pS', 'relato' )
reg( 'pS', 'relevancia' )
reg( 'pS', 'relevante' )
reg( 'pS', 'relieve' )
reg( 'pS', 'reliquia' )
reg( 'pS', 'relleno' )
reg( 'pS', 'renacentista' )
reg( 'pS', 'renta' )
reg( 'pS', 'reparto' )
reg( 'pS', 'repelente')
reg( 'pS', 'repertorio' )
reg( 'pS', 'replicante' )
reg( 'pS', 'reporte' )
reg( 'pS', 'representante' )
reg( 'pS', 'repuesta' )
reg( 'pS', 'república' )
reg( 'pS', 'requerimiento' )
reg( 'pS', 'requisito' )
reg( 'pS', 'reserva' )
reg( 'pS', 'residencia' )
reg( 'pS', 'residente')
reg( 'pS', 'residuo' )
reg( 'pS', 'resistencia' )
reg( 'pS', 'resistente' )
reg( 'pS', 'respaldo' )
reg( 'pS', 'responsable' )
reg( 'pS', 'respuesta' )
reg( 'pS', 'restante' )
reg( 'pS', 'restaurante' )
reg( 'pS', 'resto' )
reg( 'pS', 'resultado' )
reg( 'pS', 'resultante' )
reg( 'pS', 'retablo' )
reg( 'pS', 'retrato' )
reg( 'pS', 'reutilizable' )
reg( 'pS', 'ribera' )
reg( 'pS', 'rienda' )
reg( 'pS', 'riesgo')
reg( 'pS', 'riqueza' )
reg( 'pS', 'ritmo' )
reg( 'pS', 'rito' )
reg( 'pS', 'robo')
reg( 'pS', 'robot' )
reg( 'pS', 'roca' )
reg( 'pS', 'rodaja' )
reg( 'pS', 'rodaje' )
reg( 'pS', 'rodante' )
reg( 'pS', 'rodilla' )
reg( 'pS', 'rogar' )
reg( 'pS', 'romance' )
reg( 'pS', 'rombo' )
reg( 'pS', 'ropa' )
reg( 'pS', 'rosa' )
reg( 'pS', 'rostro' )
reg( 'pS', 'rudimentarios' )
reg( 'pS', 'ruido' )
reg( 'pS', 'ruina' )
reg( 'pS', 'rumbo' )
reg( 'pS', 'ruptura' )
reg( 'pS', 'ruta' )
reg( 'pS', 'rótulo' )
reg( 'pS', 'sacerdote' )
reg( 'pS', 'sacrificio' )
reg( 'pS', 'saga' )
reg( 'pS', 'sala' )
reg( 'pS', 'salario' )
reg( 'pS', 'salida' )
reg( 'pS', 'saliente' )
reg( 'pS', 'salpicadura' )
reg( 'pS', 'salsa' )
reg( 'pS', 'salto' )
reg( 'pS', 'salvaje' )
reg( 'pS', 'santo' )
reg( 'pS', 'santuario' )
reg( 'pS', 'sargento' )
reg( 'pS', 'satélite' )
reg( 'pS', 'script' )
reg( 'pS', 'seco' )
reg( 'pS', 'secretaria' )
reg( 'pS', 'secretario' )
reg( 'pS', 'secreto' )
reg( 'pS', 'secuela' )
reg( 'pS', 'secuencia' )
reg( 'pS', 'seda' )
reg( 'pS', 'sede' )
reg( 'pS', 'sedimento' )
reg( 'pS', 'segmento' )
reg( 'pS', 'seguidore' )
reg( 'pS', 'seguimiento' )
reg( 'pS', 'seleccionable' )
reg( 'pS', 'sello' )
reg( 'pS', 'selva' )
reg( 'pS', 'semana' )
reg( 'pS', 'semejante' )
reg( 'pS', 'semejanza' )
reg( 'pS', 'semestre' )
reg( 'pS', 'semilla' )
reg( 'pS', 'seno' )
reg( 'pS', 'sensible' )
reg( 'pS', 'sentencia' )
reg( 'pS', 'sentido' )
reg( 'pS', 'sentimiento' )
reg( 'pS', 'serie' )
reg( 'pS', 'serpiente' )
reg( 'pS', 'servicio' )
reg( 'pS', 'seudónimo' )
reg( 'pS', 'sexo' )
reg( 'pS', 'seña' )
reg( 'pS', 'señorío' )
reg( 'pS', 'show' )
reg( 'pS', 'sigla' )
reg( 'pS', 'siglo' )
reg( 'pS', 'signo' )
reg( 'pS', 'siguiente' )
reg( 'pS', 'silencio' )
reg( 'pS', 'silla' )
reg( 'pS', 'silueta' )
reg( 'pS', 'silvestre' )
reg( 'pS', 'simio' )
reg( 'pS', 'simpatizants' )
reg( 'pS', 'simple' )
reg( 'pS', 'sindicato' )
reg( 'pS', 'sinónimo' )
reg( 'pS', 'sistema' )
reg( 'pS', 'sitio' )
reg( 'pS', 'soberanía' )
reg( 'pS', 'sobre' )
reg( 'pS', 'sobrenombre' )
reg( 'pS', 'sobreviviente' )
reg( 'pS', 'socialdemócrata' )
reg( 'pS', 'socialista' )
reg( 'pS', 'sodio' )
reg( 'pS', 'software')
reg( 'pS', 'solista' )
reg( 'pS', 'soluble' )
reg( 'pS', 'sombra' )
reg( 'pS', 'sombrero' )
reg( 'pS', 'sonido' )
reg( 'pS', 'sonriente' )
reg( 'pS', 'soprano' )
reg( 'pS', 'sorpresa' )
reg( 'pS', 'sostenible' )
reg( 'pS', 'specie' )
reg( 'pS', 'su' )
reg( 'pS', 'suave' )
reg( 'pS', 'subclase' )
reg( 'pS', 'subespecie' )
reg( 'pS', 'subfamilia' )
reg( 'pS', 'submarino' )
reg( 'pS', 'subproducto' )
reg( 'pS', 'subprograma' )
reg( 'pS', 'subsecuente' )
reg( 'pS', 'subsiguiente' )
reg( 'pS', 'subtribu' )
reg( 'pS', 'subtítulo' )
reg( 'pS', 'suceso' )
reg( 'pS', 'suelo' )
reg( 'pS', 'sueño' )
reg( 'pS', 'suficiente' )
reg( 'pS', 'suicidio' )
reg( 'pS', 'sulfato' )
reg( 'pS', 'suministro' )
reg( 'pS', 'superficie' )
reg( 'pS', 'superproducción')
reg( 'pS', 'superviviente' )
reg( 'pS', 'suplente' )
reg( 'pS', 'susceptible' )
reg( 'pS', 'sustancia' )
reg( 'pS', 'sábado' )
reg( 'pS', 'sílaba' )
reg( 'pS', 'símbolo' )
reg( 'pS', 'síndrome' )
reg( 'pS', 'síntoma' )
reg( 'pS', 'tabaco' )
reg( 'pS', 'tabla' )
reg( 'pS', 'tableta' )
reg( 'pS', 'talento' )
reg( 'pS', 'tallo' )
reg( 'pS', 'tamaño' )
reg( 'pS', 'tango' )
reg( 'pS', 'tanque' )
reg( 'pS', 'taoísta' )
reg( 'pS', 'tarea' )
reg( 'pS', 'tarifa' )
reg( 'pS', 'tarjeta' )
reg( 'pS', 'tasa' )
reg( 'pS', 'teatro' )
reg( 'pS', 'techo' )
reg( 'pS', 'tecla' )
reg( 'pS', 'teclado' )
reg( 'pS', 'tecnología' )
reg( 'pS', 'tela' )
reg( 'pS', 'telenovela' )
reg( 'pS', 'teléfono' )
reg( 'pS', 'tema' )
reg( 'pS', 'temperatura' )
reg( 'pS', 'templo' )
reg( 'pS', 'temporada' )
reg( 'pS', 'tendencia')
reg( 'pS', 'teniente' )
reg( 'pS', 'tenista' )
reg( 'pS', 'teología' )
reg( 'pS', 'teorema' )
reg( 'pS', 'teoría' )
reg( 'pS', 'terapia' )
reg( 'pS', 'tercio' )
reg( 'pS', 'terraza' )
reg( 'pS', 'terremoto' )
reg( 'pS', 'terreno' )
reg( 'pS', 'terrestre' )
reg( 'pS', 'terrible' )
reg( 'pS', 'territorio' )
reg( 'pS', 'terrorista' )
reg( 'pS', 'tesoro' )
reg( 'pS', 'testamento' )
reg( 'pS', 'testigo' )
reg( 'pS', 'testimonio' )
reg( 'pS', 'texto' )
reg( 'pS', 'textura' )
reg( 'pS', 'tiempo' )
reg( 'pS', 'tierra' )
reg( 'pS', 'timo' )
reg( 'pS', 'tipo' )
reg( 'pS', 'tira' )
reg( 'pS', 'tiro' )
reg( 'pS', 'tomo' )
reg( 'pS', 'tonelada' )
reg( 'pS', 'tono' )
reg( 'pS', 'topónimo' )
reg( 'pS', 'tormenta' )
reg( 'pS', 'torneo' )
reg( 'pS', 'toro' )
reg( 'pS', 'torpeza' )
reg( 'pS', 'torre' )
reg( 'pS', 'tortuga' )
reg( 'pS', 'trabajo' )
reg( 'pS', 'tragedia' )
reg( 'pS', 'traje' )
reg( 'pS', 'trama' )
reg( 'pS', 'tramo' )
reg( 'pS', 'trampa' )
reg( 'pS', 'transcurso' )
reg( 'pS', 'transferencia' )
reg( 'pS', 'transparencia' )
reg( 'pS', 'transparente' )
reg( 'pS', 'tranvía' )
reg( 'pS', 'traspaso' )
reg( 'pS', 'trasplante' )
reg( 'pS', 'trastorno' )
reg( 'pS', 'tratamiento')
reg( 'pS', 'trayecto' )
reg( 'pS', 'trayectoria' )
reg( 'pS', 'trazo' )
reg( 'pS', 'tribu' )
reg( 'pS', 'trigo' )
reg( 'pS', 'trilogía' )
reg( 'pS', 'trinchera' )
reg( 'pS', 'triple' )
reg( 'pS', 'tripulante' )
reg( 'pS', 'triste' )
reg( 'pS', 'triunfante' )
reg( 'pS', 'triunfo' )
reg( 'pS', 'triángulo' )
reg( 'pS', 'trofeo' )
reg( 'pS', 'trompeta' )
reg( 'pS', 'tronco' )
reg( 'pS', 'trono' )
reg( 'pS', 'tropa' )
reg( 'pS', 'tropico' )
reg( 'pS', 'trozo' )
reg( 'pS', 'tráfico' )
reg( 'pS', 'tránsito' )
reg( 'pS', 'trío' )
reg( 'pS', 'tubo' )
reg( 'pS', 'turbina' )
reg( 'pS', 'turismo' )
reg( 'pS', 'turista' )
reg( 'pS', 'turno' )
reg( 'pS', 'té' )
reg( 'pS', 'técnica' )
reg( 'pS', 'término' )
reg( 'pS', 'título' )
reg( 'pS', 'tópico' )
reg( 'pS', 'uniforme' )
reg( 'pS', 'universo' )
reg( 'pS', 'unánime' )
reg( 'pS', 'uso' )
reg( 'pS', 'usuario' )
reg( 'pS', 'uva' )
reg( 'pS', 'uña' )
reg( 'pS', 'vacante' )
reg( 'pS', 'valenciano' )
reg( 'pS', 'valla' )
reg( 'pS', 'valle' )
reg( 'pS', 'vanguardia' )
reg( 'pS', 'variable')
reg( 'pS', 'variante' )
reg( 'pS', 'vasija' )
reg( 'pS', 'vaso' )
reg( 'pS', 'vehículo' )
reg( 'pS', 'vejiga' )
reg( 'pS', 'vena' )
reg( 'pS', 'venganza' )
reg( 'pS', 'venta')
reg( 'pS', 'ventaja' )
reg( 'pS', 'ventana' )
reg( 'pS', 'verano' )
reg( 'pS', 'verde' )
reg( 'pS', 'verdura' )
reg( 'pS', 'vereda' )
reg( 'pS', 'verificable' )
reg( 'pS', 'verso' )
reg( 'pS', 'vertebrados' )
reg( 'pS', 'vertiente' )
reg( 'pS', 'vestigio' )
reg( 'pS', 'vestuario' )
reg( 'pS', 'viable' )
reg( 'pS', 'viaje' )
reg( 'pS', 'vibrante' )
reg( 'pS', 'vicepresidente' )
reg( 'pS', 'victoria' )
reg( 'pS', 'vida' )
reg( 'pS', 'videojuego' )
reg( 'pS', 'vidrio' )
reg( 'pS', 'viento' )
reg( 'pS', 'vientre' )
reg( 'pS', 'viga' )
reg( 'pS', 'vigente' )
reg( 'pS', 'vigilancia' )
reg( 'pS', 'vigilante' )
reg( 'pS', 'villa' )
reg( 'pS', 'vinilo' )
reg( 'pS', 'vino' )
reg( 'pS', 'virgen', 'vírgenes' )
reg( 'pS', 'visible' )
reg( 'pS', 'visitante' )
reg( 'pS', 'vivienda' )
reg( 'pS', 'vizconde' )
reg( 'pS', 'vocalista' )
reg( 'pS', 'volante' )
reg( 'pS', 'voluntario')
reg( 'pS', 'votante' )
reg( 'pS', 'voto' )
reg( 'pS', 'vuelo' )
reg( 'pS', 'vuelta' )
reg( 'pS', 'vuelto' )
reg( 'pS', 'vulnerable')
reg( 'pS', 'válvula' )
reg( 'pS', 'vértebra' )
reg( 'pS', 'vértice')
reg( 'pS', 'vía' )
reg( 'pS', 'víctima' )
reg( 'pS', 'vídeo' )
reg( 'pS', 'vínculo' )
reg( 'pS', 'víspera' )
reg( 'pS', 'wiki' )
reg( 'pS', 'yacimiento' )
reg( 'pS', 'yarda' )
reg( 'pS', 'zapato' )
reg( 'pS', 'zona' )
reg( 'pS', 'zoológico' )
reg( 'pS', 'águila' )
reg( 'pS', 'ámbito' )
reg( 'pS', 'ángulo' )
reg( 'pS', 'ánimo' )
reg( 'pS', 'árabe' )
reg( 'pS', 'árbitro' )
reg( 'pS', 'área' )
reg( 'pS', 'átomo' )
reg( 'pS', 'élite' )
reg( 'pS', 'época' )
reg( 'pS', 'éxito' )
reg( 'pS', 'ícono' )
reg( 'pS', 'índice' )
reg( 'pS', 'óleo' )
reg( 'pS', 'ópera' )
reg( 'pS', 'órbita' )
reg( 'pS', 'órgano' )
reg( 'pS', 'óvalo' )



respuestas = []

#palabras = set(reglas.keys())
def normalizar(t):
  if not(t in nombres):
    t = t.lower()
  if t in reglas:
    t = reglas[t][0]
  return t

def imprimirLemas(erroresEncontrados):
  print("==Lemas==")
  for e in erroresEncontrados:
    print (correcciones[e]+" +"),

def eliminaURL(linea):
  partes = regURL.split(linea)
  resp = ""
  for parte in partes:
    resp = resp + ' ' + parte
  return resp

def transformar(normalizedOnly=False, typos=False):
  #print (normalizedOnly),
  encontrados = {}
  titulos = {}
  errores = correcciones.keys()
  if normalizedOnly:
    valores.update(set(verificadas)) 
    for w in valores:
      encontrados[w] = 0
  elif typos:
    erroresEncontrados = set()
    titulosConErrores = set()
  else:
    valores.update(set(auxiliares+verificadas+ignorar))
    valores.update(nombres)
  while True:
    linea = sys.stdin.readline()
    if linea:
      match = regtitle.match(linea)
      if match:
        titulo = match.group(1) 
        #print(titulo)
      else:
        linea = eliminaURL(linea)
        for w in regexp.findall(linea):
          w1 = normalizar(w)
          if normalizedOnly:
            if w1 in encontrados :
              encontrados[w1] = encontrados[w1]+1
          elif typos:
            if w1==w and w in errores and titulo not in excluidos.excluidos and titulo not in excluidos.revisados:
              erroresEncontrados.add(w)
              if titulo not in titulosConErrores:
                 partes = linea.replace("[","<").replace("]",">").split(w,1)
                 print ("*[["+titulo+"]] - "+partes[0]+"'''"+w+"'''"+partes[1])
                 titulosConErrores.add(titulo)
                 if len(titulosConErrores)>=60:
                   #imprimirLemas(erroresEncontrados)
                   erroresEncontrados.clear()
                   titulosConErrores.clear()
          else:
            if w1 == w and w not in valores: # and not numbExp.match(w):
              if w1 in encontrados :
                encontrados[w1] = encontrados[w1]+1
              else:
                encontrados[w1] = 1
#        print('[[Expression:'+w1+'|'+w+']]')
    else:
      break
  last = ''
  count = 0
  if typos:
    imprimirLemas(erroresEncontrados)
  else:
    for w in encontrados.keys():
      n = encontrados[w]
      if n>0:
        if w in errores:
          print (('%d	' % (n))+w+' *'),
        else:  
          print (('%d	' % (n))+w),

def normalizados():
  for w in sorted(valores):
    #print ('[[Expression:'+w+'|'+w+']]')
    print (w)

def main (argv):
   try:
      opts, args = getopt.getopt(argv,"dhtnp",['dump', 'help', 'transform', 'normalized', 'typos'])
   except getopt.GetoptError:
      #print ("Error")
      print (sys.argv[0]+' [-t] < <inputfile> > <outputfile>')
      print (sys.argv[0]+' [-dh]')
      sys.exit(2)
   for opt, arg in opts:
      if opt in ('-h', '--help'):
        #print ("Help")
        print (sys.argv[0]+' [-t] < <inputfile> > <outputfile>')
        print (sys.argv[0]+' [-dh]')
        sys.exit()
      elif opt in ("-d", "--dump"):
       # print ("Dump")
        normalizados()
      elif opt in ("-t", "--transform"):
        #print ("Tramsform")
        transformar()
      elif opt in ("-n", "--normalyzed"):
        #print ("Only normalized words")
        transformar(True)
      elif opt in ("-p", "--typos"):
        #print ("Only typos")
        transformar(False, True)

if __name__ == "__main__":
   main(sys.argv[1:])

#!/usr/bin/env python
# -*- coding: utf-8  -*-

# conda execute
# env:
#  - python >=3

import sys, getopt, re
import excluidos



def filtrar(noElimDup, elimExcl, elimRev, excluidos, revisados):
  contador = 0;
  titulo=''
  prefijo=''
  pat = re.compile("^([^\[]*)\[\[(.*?)\]\](.*)$")
  noExcluir=False
  while True:
    linea = sys.stdin.readline()
    #print(linea)
    if linea:
      match = pat.match(linea)
      if match:
        #print('>>>'+match.group(1)+'<<<->>>'+match.group(2)+'<<<->>>'+match.group(3)+'<<<')
        nuevoPrefijo = match.group(1)
        nuevoTitulo = match.group(2)
        #print (nuevoTitulo)
        if titulo != nuevoTitulo:
          if len(titulo)>0 and noExcluir:
            contenido = match.group(3)
            contenido = re.sub("[\[\{]","<", contenido)
            contenido = re.sub("[\]\}]",">", contenido)
            print (prefijo+"[["+titulo+"]]"+contenido)
          titulo = nuevoTitulo
          prefijo = nuevoPrefijo
          contador = 1
         # print(titulo+str(contador))
          contenido = match.group(3)
          contenidoLow = contenido.lower()
          noExcluir = not((elimExcl and titulo in excluidos) or (elimRev and titulo in revisados) or ("#redirect" in contenido) or ("#redirección" in contenido))
          #print('>>>'+titulo+'<<<->>>'+contenido+'<<<Noexcluir>>>'+str(noExcluir))
        else:
          contador = contador + 1
          #print(titulo+str(contador))
    else:
      if len(titulo)>0 and noExcluir:
        print (prefijo+"[["+titulo+"]]"+contenido)
      break

def main (argv):
   elimDup = True
   elimExcl = True
   elimRev = True
   try:
      opts, args = getopt.getopt(argv,"der",['duplicados', 'excluidos', 'revisados'])
   except getopt.GetoptError:
     #print ("Error")
     print (sys.argv[0]+' [-t] < <inputfile> > <outputfile>')
     print (sys.argv[0]+' [-der]')
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

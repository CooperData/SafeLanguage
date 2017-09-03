#!/usr/bin/env python
# -*- coding: utf-8  -*-

# conda execute
# env:
#  - python >=3

#Preparar un respaldo para usar grep
import sys, getopt
import re

regTitle = re.compile('^.*<title>(.*)</title>.*$')
regSpace = re.compile('^.*<ns>(.*)</ns>.*$')

tabla = {
  '&lt;':'<',
  '&gt;':'>',
  '&quot;':'"',
  '&amp;':'&',
  '[[':'[{[',
  ']]':']}]',
}
pat = re.compile('(\[\[|\]\]|&(?:lt|gt|amp|quot);)')
splitpat = re.compile("^(.+?)([.:;]\s+)(.+)$")

def rep(m):
  global tabla
  return tabla[m.group(1)]

def filtrar():
  global pat
  modoHTML =True
  while True:
    linea = sys.stdin.readline()
    if linea:
      if modoHTML:
        for w in regTitle.findall(linea):        
            titulo = w
        for ns in regSpace.findall(linea):        
            modoNoIgnorar = (ns=="0" or ns=="104")
        partes = linea.split('<text xml:space="preserve">')
        if len(partes)>1:
          modoHTML = False
          #if modoNoIgnorar:
          #  print (titulo),
          #else:
          #  print (w+" Ignorado"),
          linea = partes[1]
      if not modoHTML:
        partes = linea.split('</text>')
        #print (partes[0])
        if modoNoIgnorar:
          conts = pat.sub(rep, partes[0])
          m=splitpat.match(conts)
          while m:
            cont,sep,conts = m.groups()
            sys.stdout.write ("[["+titulo+"]]→"+cont+sep+'\n')
            m=splitpat.match(conts)
          # conts = splitpat.split(pat.sub(rep, partes[0]))
          # for cont in conts[:-1]:
          #   sys.stdout.write ("[["+titulo+"]]→"+cont+',\n')
          conts = conts.strip()
          if conts:
            sys.stdout.write ("[["+titulo+"]]→"+conts+'\n')
        if '</text>' in linea:
          print()
          modoHTML = True 
    else:
      break


def main (argv):
  filtrar()

if __name__ == "__main__":
   main(sys.argv[1:])

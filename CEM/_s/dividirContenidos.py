#!/home/ascander/py3/Python-3.3.1/python
# -*- coding: utf-8  -*-
import sys, getopt
import re
import excluidos

regTitle = re.compile('^.*(<title>.*</title>).*$')
regSpace = re.compile('^.*<ns>(.*)</ns>.*$')

def filtrar():
  modoHTML =True
  while True:
    linea = sys.stdin.readline()
    if linea:
      if modoHTML:
        for w in regTitle.findall(linea):        
            titulo = w
        for ns in regSpace.findall(linea):        
            modoNoIgnorar = (ns=="0" or ns=="104") and titulo not in excluidos.excluidos
        partes = linea.split('<text xml:space="preserve">')
        if len(partes)>1:
          modoHTML = False
          if modoNoIgnorar:
            print (w),
          #else:
          #  print (w+" Ignorado"),
          linea = partes[1]
      if not modoHTML:
        partes = linea.split('</text>')
        #print (partes[0])
        if modoNoIgnorar:
          sys.stdout.write (partes[0])
        if '</text>' in linea:
          print()
          modoHTML = True 
    else:
      break


def main (argv):
  filtrar()

if __name__ == "__main__":
   main(sys.argv[1:])

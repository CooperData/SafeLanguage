#!/home/ascander/miniconda3/bin/python3
# -*- coding: utf-8  -*-
import sys, getopt, re
import excluidos

def filtrar(excluidos, revisados):
  listados = set()
  titulo=''
  pat = re.compile("^.*?\[\[(.*?)\]\].*$")
  linea = sys.stdin.readline()
  while linea:
    match = pat.match(linea)
    if match:
      titulo = match.group(1)
      if titulo not in excluidos and titulo not in revisados \
            and titulo not in listados:
        listados.add(titulo)
        print(linea, end='')
    linea = sys.stdin.readline()

def main (argv):
   filtrar(excluidos.excluidos, excluidos.revisados)



if __name__ == "__main__":
   main(sys.argv[1:])

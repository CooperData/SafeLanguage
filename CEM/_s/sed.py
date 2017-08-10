#!/usr/bin/python3
# -*- coding: utf-8  -*-
import sys, getopt, re

def sed(op, pat, val, glob):
  #print("op<"+op+">,pat=<"+pat+">,val=<"+val+">,glob=<"+glob+">")
  pat = re.compile(pat)
  while True:
    linea = sys.stdin.readline()
    if linea:
        linea1 = pat.sub(val, linea)
        if glob=='g':
           while linea1 != linea:
             linea = linea1
             linea1 = pat.sub(val, linea)
        print (linea1, end='')
        sys.stdout.flush()
    else:
      break

def main (argv):
   elimDup = True
   elimExcl = True
   elimRev = True
   try:
      opts, args = getopt.getopt(argv,"e",['ejecute'])
   except getopt.GetoptError:
     #print ("Error")
     print (sys.argv[0]+' -e "s/pat/val/g" < <inputfile> > <outputfile>')
     sys.exit(2)
   for opt, arg in opts:
     if opt in ('-e', '--ejecute'):
         partes = args[0].split(args[0][1])
         pat = partes[1]
         val = partes[2]
   sed(*partes)



if __name__ == "__main__":
   main(sys.argv[1:])

#!/home/ascander/py3/Python-3.3.1/python
# -*- coding: utf-8  -*-
import sys, getopt, re

f = open("/home/ascander/tmp/nueso.txt", "rb")
try:
    byte = f.read(1)
    while byte != "":
      n = int.from_bytes(byte, byteorder='big')
      if n==32:
        n= "_"
      else:
        n= str(n)
      # Do stuff with byte.
      print (n+" ", end='')
      byte = f.read(1)
finally:
    f.close()

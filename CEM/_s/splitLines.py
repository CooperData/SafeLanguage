#!/usr/bin/env python
# -*- coding: utf-8  -*-

# conda execute
# env:
#  - python >=3

import sys, re

def filter():
    line = sys.stdin.readline()[:-1]
    pat = re.compile("[.:;]\s+")
    spat = re.compile("→")
    while line:
        structure = spat.split(line)
        lines = pat.split(structure[1])
        for l in lines[:-1]:
            print (structure[0]+"→"+l+".")
        print(structure[0]+"→"+lines[-1])
        line = sys.stdin.readline()[:-1]

filter()

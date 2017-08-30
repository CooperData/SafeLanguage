#!/usr/bin/env python
# -*- coding: utf-8  -*-

# conda execute
# env:
#  - python >=3

#randomSplit.py percentage filePrefix
#split lines in the standard input into to gropus, selecting randomly which lines goes to the first or to the second group. The probability of going to the first group is percentage, and filePrefix is the prefix name of the output files.

import numbers, sys
from random import random

class Splitter:

    def __init__(self, filePrefix, *percentages):
        self.filePrefix = filePrefix
        total = 0.0
        perc = []
        try:
            for i in range(len(percentages)):
                perc.append(float(percentages[i]))
                total += perc[i]
        except ValueError:
            perc = [0.5, 0.5]
        if 0.0<=total and total <=1.0:
            perc.append(1.0-total)
            self.percentages = perc
        else:
            self.percentages = [0.5, 0.5]

    def split(self):
        files = [open(self.filePrefix+"_"+str(i+1), 'w')
                 for i in range(len(self.percentages))]
        line = sys.stdin.readline()
        while line:
            total = 0.0
            rand = random()
            for i in range(len(self.percentages)):
                total += self.percentages[i]
                if rand < total:
                    files[i].write(line)
                    break
            try:
                prev = line
                line = sys.stdin.readline()
            except:
                print(prev)
                print("Unexpected error:", sys.exc_info()[0])
                raise
        for file in files:
            file.close()
        
if len(sys.argv) < 3:
    print(sys.argv[0] + ' <filePrefix> <percentage1> ...')
Splitter(sys.argv[1], *sys.argv[2:]).split()

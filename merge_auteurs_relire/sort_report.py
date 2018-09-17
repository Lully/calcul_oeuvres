# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 14:55:05 2018

@author: BNF0017855
"""

import csv


entry_filename = "80000_pep_relire.csv"

completeliste = []
output_file = open("80000_pep_relire_sorted.csv","w",encoding="utf-8")

with open(entry_filename, newline='\n',encoding="utf-8") as csvfile:
    entry_file = csv.reader(csvfile, delimiter='\t')
    for row in entry_file:
        completeliste.append(row)
        

completeliste = sorted(completeliste)
for el in completeliste:
    output_file.write("\t".join(el) + "\n")
    
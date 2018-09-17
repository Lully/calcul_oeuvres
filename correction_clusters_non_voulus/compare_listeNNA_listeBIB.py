# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 11:50:15 2018

@author: BNF0017855
"""

import csv

def file2liste(filename,cols = False):
    liste = []
    with open(filename, newline='\n',encoding="utf-8") as csvfile:
        entry_file = csv.reader(csvfile, delimiter='\t')
        for row in entry_file:
            val = row[0]
            if (cols == True):
                val = row
            liste.append(val)
    return liste

def comparelistes(listeNNA,listeBIB,liste_bib_name):
    outputfile = open(liste_bib_name[:-4]+"-corr.txt","w",encoding="utf-8")
    outputfile_rej = open(liste_bib_name[:-4]+"-rej.txt","w",encoding="utf-8")
    i = 0
    num_col_nna = 0
    for el in listeBIB:
        if (i==0):
            i += 1
            num_col_nna = el.index("id de l'auteur (FRBNF)")
            outputfile.write("\t".join(el) + "\n")
        elif(el[num_col_nna] in listeNNA):
            outputfile.write("\t".join(el) + "\n")
            print("conservé", el[0])
        else:
            outputfile_rej.write("\t".join(el) + "\n")
            print("rejeté", el[0])

if __name__ == "__main__":
    listenna_name = input("fichier de NNA : ")
    liste_bib_name = input("fichier des résultats du minhashing : ")
    listeNNA = file2liste(listenna_name)
    listeBIB = file2liste(liste_bib_name,True)
    comparelistes(listeNNA,listeBIB,liste_bib_name)
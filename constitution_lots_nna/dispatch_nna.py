# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 16:13:00 2018

@author: BNF0017855
"""

import csv

def file2files(filename,trunc):
    liste = []
    with open(filename, newline='\n',encoding="utf-8") as csvfile:
        entry_file = csv.reader(csvfile, delimiter='\t')
        for row in entry_file:
            val = row[0]
            liste.append(val)
    liste2files(liste,0,trunc,filename)

def liste2files(liste,numero_debut,trunc,filename):

    outputfilename = filename[:-4]+"-"+str(numero_debut)+".txt"
    outputfile = open(outputfilename,"w",encoding="utf-8") 
    print(outputfilename)
    for el in liste[:trunc]:
        outputfile.write(el + "\n")
        numero_debut +=1
    outputfile.close()
    if (len(liste) > trunc):
        liste2files(liste[trunc:],numero_debut,trunc,filename)
    
    
if __name__ == "__main__":
    filename = input("fichier de NNA : ")
    trunc = int(input("Découpage par lot de ... NNA :  "))
    
    file2files(filename,trunc)
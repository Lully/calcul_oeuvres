# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 08:58:10 2018

@author: BNF0017855
Avec un fichier CSV de RobotDonnées en entrée, ne conserve que ceux associés à un NNA d'une liste de NNA

"""

import csv
from ListeNNAReLire import ListeNNAReLire

input_filename = input("Fichier à importer : ")
ouptut_filename = input_filename[:-4] + "-conserves.csv"
exclus_filename = input_filename[:-4] + "-exclus.csv"
output_file = open(ouptut_filename,"w",encoding="utf-8")
exclus_file = open(exclus_filename,"w",encoding="utf-8")

tous_nna = set()
nna_conserves = set()
tous_clusters = set()
tous_nnb = set()
clusters_conserves = set()
nnb_conserves = set()

def row2output(row):
    line = "\t".join(row[0:12]) + "\t" + row[13] + "\t" +  "20180419-182856" + "\n"
    return line

def func_filter(row,colonne_nna,colonne_zone,colonne_methode,colonne_clusterid,colonne_ark_manif):
    nna = row[colonne_nna]
    tous_nna.add(nna)
    tous_clusters.add(row[colonne_clusterid])
    tous_nnb.add(row[colonne_ark_manif])
    if (nna in ListeNNAReLire and "$r" not in row[colonne_zone] and "_unica" not in row[colonne_methode] and "id de l'auteur (FRBNF)" not in row):
        output_file.write(row2output(row))
        nna_conserves.add(nna)
        clusters_conserves.add(row[colonne_clusterid])
        nnb_conserves.add(row[colonne_ark_manif])
        print(nna, "OK")
    else:
        exclus_file.write(row2output(row))
        print(nna, "exclu")

with open(input_filename, encoding="utf-8") as csvfile:
    i = 0
    tableau = csv.reader(csvfile, delimiter='\t')
    for row in tableau:
        if (i == 0):
            i += 1
            colonne_nna = row.index("id de l'auteur (FRBNF)")
            colonne_zone = row.index("zones")
            colonne_methode = row.index("methode")
            colonne_clusterid = row.index("clusterid")
            colonne_ark_manif = row.index("id de la manifestation (ARK)")
            output_file.write("\t".join(row) + "\n")
            exclus_file.write("\t".join(row) + "\n")
        else:
            func_filter(row,colonne_nna,colonne_zone,colonne_methode,colonne_clusterid,colonne_ark_manif)

exclus_file.close()
output_file.close()

print("\nNb total de NNA : " + str(len(list(tous_nna))))
print("Nb de NNA conservés : " + str(len(list(nna_conserves))))

print("\nNb total de clusters : " + str(len(list(tous_clusters))))
print("\nNb de clusters conservés : " + str(len(list(clusters_conserves))))

print("Nb total de nnb : " + str(len(list(tous_nnb))))
print("Nb de nnb conservés : " + str(len(list(nnb_conserves))))
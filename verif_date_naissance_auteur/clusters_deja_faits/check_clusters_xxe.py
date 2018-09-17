# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 17:21:47 2018

@author: BNF0017855

Programme pour distinguer les auteurs ReLire non XXe siècle
et faire la liste de ceux déjà traités
"""

import csv

input_filename = input("Fichier en entrée : ")

output_file_clusters_ok = open("output_file_clusters_ok.txt","w",encoding="utf-8")
output_file_clusters_KO = open("output_file_clusters_KO.txt","w",encoding="utf-8")
headers = "pep_cluster_id	id de l'auteur (FRBNF)	id de l'auteur (ARK)	clusterid	clusternum	Titre de l'oeuvre	id de la manifestation (FRBNF)	id de la manifestation (ARK)	Titre Manifestation	Type de notice	Type de document	zones	methode	date	orig-clusters	\n"
output_file_clusters_ok.write(headers)
output_file_clusters_KO.write(headers)

ListeNNA_ReLire_XXe_siecle = "ListeNNA_ReLire_XXe_siecle.txt"
ListeNNA_ReLire_XXe_siecle_liste = []

NNA_XXe_deja_traites_file = open("Liste NNA XXe déjà traités.txt","w",encoding="utf-8")
NNA_XXe_deja_traites_liste = set()

with open(ListeNNA_ReLire_XXe_siecle, newline='\n',encoding="utf-8") as csvfile:
    entry_file = csv.reader(csvfile, delimiter='\t')
    for row in entry_file:
        nna = row[0]
        ListeNNA_ReLire_XXe_siecle_liste.append(nna)

print(ListeNNA_ReLire_XXe_siecle_liste)

with open(input_filename, newline='\n',encoding="utf-8") as csvfile:
    entry_file = csv.reader(csvfile, delimiter='\t')
    next(entry_file)
    i = 0
    for row in entry_file:
        i += 1
        nna = row[1]
        print(i, " - ", row[2])
        if (nna in ListeNNA_ReLire_XXe_siecle_liste):
            output_file_clusters_ok.write("\t".join(row) + "\n")
            NNA_XXe_deja_traites_liste.add(nna)
        else:
            output_file_clusters_KO.write("\t".join(row) + "\n")

for el in list(NNA_XXe_deja_traites_liste):
    NNA_XXe_deja_traites_file.write(el +  "\n")

output_file_clusters_KO.close()
output_file_clusters_ok.close()
NNA_XXe_deja_traites_file.close()

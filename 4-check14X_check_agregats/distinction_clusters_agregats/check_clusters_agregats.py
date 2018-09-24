# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 09:27:23 2018

@author: BNF0017855
"""
import csv
from collections import defaultdict

input_filename = input("Fichier CSV à traiter : ")
id_traitement = input("ID traitement : ")

output_sans_agregats = open(id_traitement + "-clusters_sans_agregats.csv","w")
output_avec_agregats = open(id_traitement + "-clusters_avec_agregats.csv","w")

clusters = defaultdict(dict)

with open(input_filename) as csvfile:
    tableau = csv.reader(csvfile, delimiter='\t')
    colonne_clusterID = 0
    colonne_anlnum = 0
    colonne_zones = 0
    i = 0
    for row in tableau:
        if (i == 0):
            i += 1
            colonne_clusterID = row.index("clusterid")
            colonne_anlnum  = row.index("anlnum")
            colonne_zones = row.index("zones")
            output_sans_agregats.write("\t".join(row) + "\n")
            output_avec_agregats.write("\t".join(row) + "\n")
        else:
            clusterID = row[colonne_clusterID]
            print(clusterID)
            if (clusterID not in clusters):
                clusters[clusterID]["manifs"] = []
                clusters[clusterID]["agregat"] = 0
                clusters[clusterID]["manifs"].append("\t".join(row))
            else:
                clusters[clusterID]["manifs"].append("\t".join(row))
            if ("748" in row[colonne_zones]):
                clusters[clusterID]["agregat"] += 1
            if ("245$b" in row[colonne_zones]):
                clusters[clusterID]["agregat"] += 1
            if (row[colonne_anlnum] != "0"):
                clusters[clusterID]["agregat"] += 1

i = 0
j = 0
for clusterID in clusters:
    if (clusters[clusterID]["agregat"] > 0):
        i += 1
        output_avec_agregats.write("\n".join(clusters[clusterID]["manifs"]) + "\n")
    else:
        j += 1
        output_sans_agregats.write("\n".join(clusters[clusterID]["manifs"]) + "\n")

print("nb de clusters avec agregats : ", i)
print("nb de clusters sans agregats : ", j)

output_sans_agregats.close()
output_avec_agregats.close()
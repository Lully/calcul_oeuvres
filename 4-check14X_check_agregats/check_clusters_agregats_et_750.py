# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 09:27:23 2018

@author: BNF0017855
"""
import csv
from collections import defaultdict

def filename2check_agregats(input_filename,liste_files,option_r="o"):
    clusters = defaultdict(dict)
    output_sans_agregats = liste_files[0] 
    output_avec_agregats = liste_files[1] 
    output_clusters_750 = liste_files[2]
    with open(input_filename, encoding="utf-8") as csvfile:
        tableau = csv.reader(csvfile, delimiter='\t')
        colonne_type_notice = 0
        colonne_clusterID = 0
        colonne_zones = 0
        i = 0
        for row in tableau:
            if (i == 0):
                i += 1
                colonne_clusterID = row.index("clusterid")
                colonne_type_notice = row.index("Type de notice")
                colonne_zones = row.index("zones")
                output_sans_agregats.write("\t".join(row) + "\n")
                output_avec_agregats.write("\t".join(row) + "\n")
                output_clusters_750.write("\t".join(row) + "\n")
            else:
                clusterID = row[colonne_clusterID]
                
                if (clusterID not in clusters):
                    clusters[clusterID]["manifs"] = []
                    clusters[clusterID]["agregat"] = False
                    clusters[clusterID]["test_autre_750"] = False
                    clusters[clusterID]["test_presence_750"] = False
                    clusters[clusterID]["manifs"].append("\t".join(row))
                else:
                    clusters[clusterID]["manifs"].append("\t".join(row))
                if ("750" in row[colonne_zones]):
                    clusters[clusterID]["test_presence_750"] = True
                if ("750" not in row[colonne_zones]):
                    clusters[clusterID]["test_autre_750"] = True

                if ("748" in row[colonne_zones]):
                    clusters[clusterID]["agregat"] = True
                if ("245$b" in row[colonne_zones]):
                    clusters[clusterID]["agregat"] = True
                if (row[colonne_type_notice] == "d"):
                    clusters[clusterID]["agregat"] = True
                print(clusterID, clusters[clusterID]["test_presence_750"], clusters[clusterID]["test_autre_750"], clusters[clusterID]["agregat"])
    return clusters


def analyse_clusters(liste_files,clusters):
    i = 0
    j = 0
    k = 0
    output_sans_agregats = liste_files[0] 
    output_avec_agregats = liste_files[1] 
    output_clusters_750 = liste_files[2]
    for clusterID in clusters:
        if (clusters[clusterID]["agregat"] == True):
            i += 1
            output_avec_agregats.write("\n".join(clusters[clusterID]["manifs"]) + "\n")
        elif(clusters[clusterID]["test_presence_750"] == True and clusters[clusterID]["test_autre_750"] == False):
            k += 1
            output_clusters_750.write("\n".join(clusters[clusterID]["manifs"]) + "\n")
        else:
            j += 1
            output_sans_agregats.write("\n".join(clusters[clusterID]["manifs"]) + "\n")
    return (i,j,k)


def filename2outputfiles(input_filename,id_traitement=""):
    if (id_traitement == ""):
        id_traitement = input_filename.split(".")[0]
    output_sans_agregats = open(id_traitement + "-clusters_sans_agregats.csv", "w", encoding="utf-8")
    output_avec_agregats = open(id_traitement + "-clusters_avec_agregats.csv", "w", encoding="utf-8")
    output_clusters_750 = open(id_traitement + "-clusters_uniquement_750.csv", "w", encoding="utf-8")
    output_stats = open("rapport-stats.csv", "a", encoding="utf-8")
    return [output_sans_agregats,output_avec_agregats,output_clusters_750,output_stats]

def EOT(nb_clusters_avec_agregats,nb_clusters_sans_agregats,nb_clusters_750,liste_files):
    print(liste_files[0].name)
    id_file = "-".join(liste_files[0].name.split("-")[:-1])
    stats = id_file + """
nb de clusters avec agregats : """ +  str(nb_clusters_avec_agregats) + """
nb de clusters sans agregats : """ +  str(nb_clusters_sans_agregats) + """
nb de clusters contenant uniquement des 750 :""" +  str(nb_clusters_750) + "\n\n"
    liste_files[-1].write(stats)
    for file in liste_files:
        file.close()

        
if __name__ == "__main__":
    input_filename = input("Fichier CSV à traiter : ")
    id_traitement = input("ID traitement : ")
    option_r = input("Supprimer les 245$r ? (O/N)")
    if (option_r == ""):
        option_r = "o"
    else:
        option_r = option_r.lower()
    liste_reports = filename2outputfiles(input_filename,id_traitement)
    clusters = filename2check_agregats(input_filename,liste_reports,option_r)
    (i,j,k) = analyse_clusters(liste_reports,clusters)
    EOT(i,j,k,liste_reports)
    
    
    

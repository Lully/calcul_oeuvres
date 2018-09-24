# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 14:16:08 2017

Objectif : Une même notice BIB ne peut être que dans un seul cluster

@author: BNF0017855
"""
import csv
from urllib import request
from lxml import etree
import urllib.error as error
from unidecode import unidecode
from collections import defaultdict
import http.client


ns = {"srw":"http://www.loc.gov/zing/srw/", "m":"http://catalogue.bnf.fr/namespaces/InterXMarc","mn":"http://catalogue.bnf.fr/namespaces/motsnotices"}


#En entrée, le fichier CSV issu de RobotDonnées (soit de dedupe, soit de minhashing)
#liste_oeuvres_file = open(filename_root + "-liste_oeuvres.csv","w")
url_access_pbs = []

#Variables globales pour la vérification des liens en 14X

def filename2outputfile(input_filename):
    outputfilename = f"{input_filename[:-4]}-dedupe.txt"
    outputfile = open(outputfile, "w", encoding="utf-8")
    return outputfile



def liste2clusters(liste, distance_max):
    libelle2clusters = defaultdict(list)  # libellé > liste des clusters temp
    clusters = defaultdict(set)
    i = 0
    cluster_no = 0
    for el in liste:
        libelle2libelles = defaultdict(list)
        j = liste.index(el)
        # Comparaison avec les éléments suivants dans la liste
        if (j > 0):
            if (el not in libelle2clusters):
                libelle2clusters[el].append(cluster_no)
            for el2 in liste[:j]:
                dist = levenshtein(el, el2)
                if (dist < distance_max):
                    cluster_num_el2 = libelle2clusters[el2][0]
                    libelle2clusters[el].append(cluster_num_el2)
        if (j+1 != len(liste)):
            for el2 in liste[j+1:]:
                dist = levenshtein(el, el2)
                if dist < distance_max:
                    libelle2libelles[el].append(el2)
                    libelle2clusters[el].append(cluster_no)
        if j == 0:
            libelle2clusters[el].append(i)
        i += 1
        cluster_no += 1

    clusters_temps2id = defaultdict(list)
    for libelle in libelle2clusters:
        libelle2clusters[libelle] = list(set(libelle2clusters[libelle]))
        for cluster in libelle2clusters[libelle]:
            clusters_temps2id[cluster].extend(libelle2clusters[libelle])
    for cluster in clusters_temps2id:
        clusters_temps2id[cluster] = "-".join([str(el)
                                               for el in sorted(list(set(clusters_temps2id[cluster])))])

    for libelle in libelle2clusters:
        for cluster_temp in libelle2clusters[libelle]:
            empreinte = clusters_temps2id[cluster_temp]
            clusters[empreinte].add(libelle)
    for cluster in clusters:
        clusters[cluster] = sorted(list(clusters[cluster]))

    return (clusters)


def group2cluster(group, distance_max):
    """Clusterisation des éléments
    pour un sous-ensemble (exemple : pour un éditeur)"""
    libelle2clusters = liste2clusters(group, distance_max)
    pprint(libelle2clusters)
    return libelle2clusters




def dedupe_clusters(input_filename, outputfile):
    while open(input_filename, "r", encoding="utf-8") as inputfile:
        table = csv.reader(inputfile, delimiter="\t")
        dic_nnb2cluster = defaultdict(str)
        dic_cluster2nnb = defaultdict(list)


if __name__ == "__main__":
    input_filename = input("Fichier CSV à traiter : ")
    outputfile = filename2outputfile(input_filename)
    dedupe_clusters(input_filename, outputfile)
    outputfile.close()
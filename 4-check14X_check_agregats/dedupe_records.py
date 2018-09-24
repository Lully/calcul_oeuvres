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
from pprint import pprint
from distance import levenshtein
from collections import defaultdict
import http.client
import networkx 
from networkx.algorithms.components.connected import connected_components

ns = {"srw":"http://www.loc.gov/zing/srw/", "m":"http://catalogue.bnf.fr/namespaces/InterXMarc","mn":"http://catalogue.bnf.fr/namespaces/motsnotices"}


#En entrée, le fichier CSV issu de RobotDonnées (soit de dedupe, soit de minhashing)
#liste_oeuvres_file = open(filename_root + "-liste_oeuvres.csv","w")
url_access_pbs = []

#Variables globales pour la vérification des liens en 14X

def filename2outputfile(input_filename):
    outputfilename = f"{input_filename[:-4]}-dedupe.txt"
    outputfile = open(outputfilename, "w", encoding="utf-8")
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


def group2cluster(group):
    """Pour chaque ARK, on identifie les clusters
    dont il fait partie"""
    ark2cluster_temp = defaultdict(list)
    for cluster in group:
        for ark in group[cluster]:
            ark2cluster_temp[ark].append(cluster)
    # print(ark2cluster_temp)

    network = []

    for ark in ark2cluster_temp:
        network.append(ark2cluster_temp[ark])

    grappes = to_graph(network)

    grappesid = defaultdict(list)
    cluster2grappeid = defaultdict(str)
    for grappe in grappes:
        grappesid[grappe[0]] = grappe[1:]
        for cluster in grappe:
            cluster2grappeid[cluster] = grappe[0]

    return ark2cluster_temp, grappesid, cluster2grappeid

def to_graph(l):
    out = []
    while len(l)>0:
        first, *rest = l
        first = set(first)

        lf = -1
        while len(first)>lf:
            lf = len(first)

            rest2 = []
            for r in rest:
                if len(first.intersection(set(r)))>0:
                    first |= set(r)
                else:
                    rest2.append(r)     
            rest = rest2

        out.append(first)
        l = rest
    listes = []
    for el in out:
        listes.append(list(el))
    return listes

def clusterisation(dico, distance_max):
    """
    Traitement du dictionnaire global comprenant plusieurs
    sous-ensembles de listes
    """
    general_dic = defaultdict(dict)
    for group in dico:
        print("clusterisation de ", group)
        general_dic[group] = group2cluster(dico[group], distance_max)
    return general_dic


def dedupe_clusters(input_filename, outputfile, distance_max):
    with open(input_filename, "r", encoding="utf-8") as inputfile:
        table = csv.reader(inputfile, delimiter="\t")
        dic_manifs2rows = defaultdict(list)
        dic_temp = defaultdict(dict)
        i = 0
        ark_manif_coll = 0
        clusterid_coll = 0
        for row in table:
            if (i == 0):
                outputfile.write("\t".join(row) + "\tcluster-orig\t" + "\n")
                ark_manif_coll = row.index("id de la manifestation (ARK)")
                clusterid_coll = row.index("clusterid")
                i += 1
            else:
                auteur = row[0]
                ark_manif = row[ark_manif_coll]
                clusterid = row[clusterid_coll]
                if (auteur not in dic_temp):
                    dic_temp[auteur] = defaultdict(list)
                dic_temp[auteur][clusterid].append(ark_manif)
                dic_manifs2rows[ark_manif].append(row) 

        for auteur in dic_temp:
            ark2clusters, grappesid, clusters2grappesid = group2cluster(dic_temp[auteur])
            #print(auteur, clusters)
            for ark in ark2clusters:
                rows_init = dic_manifs2rows[ark]
                old_clusterid = ark2clusters[ark][0]
                clusterark = clusters2grappesid[old_clusterid]
                for row in rows_init:
                    cluster_init = row[clusterid_coll]
                    # print(auteur, ark, old_clusterid, clusterark, cluster_init)                
                    if cluster_init != clusterark:
                        row[clusterid_coll] = clusterark
                    outputfile.write("\t".join(row))
                    if cluster_init != clusterark:
                        outputfile.write(f"\t{cluster_init}")
                    outputfile.write("\n")

def dedupe1file(input_filename, distance_max):
    outputfile = filename2outputfile(input_filename)
    dedupe_clusters(input_filename, outputfile, distance_max)
    outputfile.close()

if __name__ == "__main__":
    input_filename = input("Fichier CSV à traiter : ")
    distance_max = 0

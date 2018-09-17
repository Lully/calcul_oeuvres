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
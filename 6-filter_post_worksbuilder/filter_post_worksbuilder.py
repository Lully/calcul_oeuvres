# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 09:46:11 2018

@author: BNF0017855

Programme d'extraction et d'analyse des oeuvres générées par RobotDonnées pour identifier les auteurs homonymes co-auteurs d'une oeuvre
dont l'homonymie est approximative : même initiale, une lettre (distance de Levenshtein : 1) dans le nom de famille nettoyé

Processus : 
    - dézipper
    - ouvrir un ensemble de fichiers JSON
    - Appliquer chacun des filtres
"""
import zipfile
import json
import codecs
import shutil
from collections import defaultdict
import pprint
from unidecode import unidecode

import SRUextraction as sru


pp = pprint.PrettyPrinter()
reader = codecs.getreader("utf-8")


def zip_2_files(zipfilename):
    """A partir d'un nom de fichier ZIP, renvoie la liste des noms de fichiers contenus dans le zip"""
    file = zipfile.ZipFile(zipfilename)
    file.extractall()
    return file


def filename2json(filename):
    """A partir d'un nom de fichier JSON, récupération de son contenu dans une variable"""
    data = ""
    with open(zipfile.open(filename)) as f:
        data = json.load(f)
        print(data)
    return data


def filter(file, zipfile_ok, zipfile_ko):
    """"
    En entrée, un fichier JSON contenant une oeuvre
    on lui applique une succession de filtres
    Si tous les filtres sont OK
    --> le fichier est ajouté à l'archive zipfile_ok
    Sinon 
    --> le fichier est ajouté à l'archive zipfile_ko
    """
    with open(file.filename) as f:
        TIC = json.load(f)
        test = liste_tests(TIC)
        if test:
            zipfile_ok.write(file)
        else:
            zipfile_ko.write(file)


def liste_tests(TIC):
    """Applique une liste de tests
    puis renvoie True ou False """
    test = check_empty_titles(TIC)
    if test:
        test = check_elementary_pep(TIC)
    return test


def check_empty_titles(TIC):
    """Vérifie si le titre de l'oeuvre est
    une chaîne de caractères vide"""
    test = True
    title = TIC["preferred_title"]["title"].strip() 
    if not title:
        test = False
    return test


def check_elementary_pep(TIC):
    """Vérifie si toutes les PEP sont élémentaires"""
    test = False
    for author in TIC["authors"]:
        nna = author[3]
        sru_query = f'nna any "{nna}"'
        sru_nb_results = sru.SRU_result(parametres={"query": sru_query}).nb_results

        # Si la requête SRU a donné 0 résultat : c'est une PEP
        # élémentaire (ou la PEP a été fusionnée avec une autre
        # entre temps)
        if (sru_nb_results):
            test = True
    return test


def clean_key(string):
    string = unidecode(string.lower())
    signs = [" ","-","."]
    for sign in signs:
        string = string.replace(sign,"")
    return string

def multi_authors(TIC,outputfile):
    dic_authors = defaultdict(dict)
    line = [TIC["preferred_title"]["title"]," ".join(TIC["manifs"])]
    for author in TIC["authors"]:
        lastname_nett = clean_key(author[0].split(" ")[-1])
        initiale = unidecode(author[0][0].lower())
        nna = author[-1]
        key = initiale + " " + lastname_nett
        if ("nna" in dic_authors[key]):
            dic_authors[key]["nna"].append(str(nna))
        else:
            dic_authors[key]["nna"] = [str(nna)]
            dic_authors[key]["Nom complet"] = author[0]
            dic_authors[key]["initiale"] = initiale
        if ("count" in dic_authors[key]):
            dic_authors[key]["count"] += 1
        else:
            dic_authors[key]["count"] = 1
    for el in dic_authors:
        metas_aut = el + "\t" + dic_authors[el]["Nom complet"] + "\t" + " ".join(dic_authors[el]["nna"])
        if (dic_authors[el]["count"] > 1):
            print(line, metas_aut)
            outputfile.write("\t".join(line) + "\t" + metas_aut + "\n")
        for k in dic_authors:
            if (distance.levenshtein(el,k) == 1 and dic_authors[el]["initiale"]==dic_authors[k]["initiale"]):
                metas_autk = k + "\t" + dic_authors[k]["Nom complet"] + "\t" + " ".join(dic_authors[k]["nna"])
                outputfile.write("\t".join(line) + "\t" + metas_aut + "\t" + metas_autk + "\n")

def checkfiles(files, zipname):
    outputzipname = zipname[:-4] + "-filter_ok.zip"
    excluded_works_name = zipname[:-4] + "-filter_ko.zip"
    outputzip = zipfile.ZipFile(outputzipname, "w")
    excluded_works = zipfile.ZipFile(excluded_works_name, "w")
    for file in files:
        print(zipname, file.filename)
        filter(file, outputzip, excluded_works)

def EOT(content):
    foldername = content.filelist[0].filename.split("/")[0]
    shutil.rmtree(foldername )

def filter1zipfile(zipname):
    content = zip_2_files(zipname)
    checkfiles(content.filelist, zipname)
    EOT(content)


if __name__ == "__main__":
    zipfilename = input("Nom du ou des fichiers zip (sep \";\") : ")
    zipfilename = zipfilename.split(";")
    for zipname in zipfilename:
        filter1zipfile(zipname)
    
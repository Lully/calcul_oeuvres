# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 09:46:11 2018

@author: BNF0017855

Programme d'extraction et d'analyse des oeuvres générées par
RobotDonnées pour identifier les auteurs homonymes co-auteurs d'une oeuvre
dont l'homonymie est approximative : même initiale, une lettre
(distance de Levenshtein : 1) dans le nom de famille nettoyé

Processus :
    1. dezipper un lot d'oeuvre
    2. ne traiter que les oeuvres à plusieurs auteurs
    3. pour une oeuvres à plusieurs auteurs, comparer les noms
    et prénoms d'auteurs (uniquement PEP : ne pas conserver les ORG)

Fonctions nécessaires :
    - dézipper
    - ouvrir un ensemble de fichiers JSON
    - calculer la distance de Levenshtein
"""
import zipfile
import json
import codecs
import shutil
from collections import defaultdict
import pprint
from unidecode import unidecode
import distance

pp = pprint.PrettyPrinter()
reader = codecs.getreader("utf-8")

errors = []


def zip_2_files(zipfilename):
    """A partir d'un nom de fichier ZIP, renvoie la liste des noms de fichiers
    contenus dans le zip"""
    file = zipfile.ZipFile(zipfilename)
    file.extractall()   
    return file


def filename2json(filename):
    """A partir d'un nom de fichier JSON, récupération de
    son contenu dans une variable"""
    data = ""
    with open(zipfile.open(filename)) as f:
        data = json.load(f)
        print(data)
    return data


def analyse(zipname, file, outputfile):
    with open(file.filename) as f:
        try:
            TIC = json.load(f)
            liste_authors = TIC["authors"]
            if (len(liste_authors) > 1):
                multi_authors(TIC, outputfile)
        except json.decoder.JSONDecodeError as err:
            errors.append([zipname, file.filename, str(err)])


def clean_key(string):
    string = unidecode(string.lower())
    signs = [" ", "-", "."]
    for sign in signs:
        string = string.replace(sign, "")
    return string


def multi_authors(TIC, outputfile):
    dic_authors = defaultdict(dict)
    line = [TIC["preferred_title"]["title"], " ".join(TIC["manifs"])]
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
        metas_aut = "".join([el,
                            "\t",
                            dic_authors[el]["Nom complet"],
                            "\t",
                            " ".join(dic_authors[el]["nna"])
                            ]
                            )  
        if (dic_authors[el]["count"] > 1):
            print(line, metas_aut)
            outputfile.write("\t".join(line) + "\t" + metas_aut + "\n")
        for k in dic_authors:
            if (distance.levenshtein(el, k) == 1
                    and dic_authors[el]["initiale"] == dic_authors[k]["initiale"]):
                metas_autk = "".join([k,
                                     "\t",
                                     dic_authors[k]["Nom complet"],
                                     "\t",
                                     " ".join(dic_authors[k]["nna"])
                                     ])
                outputfile.write("".join(["\t".join(line),
                                         "\t",
                                         metas_aut,
                                         "\t",
                                         metas_autk,
                                         "\n"])
                                 ) 


def checkfiles(zipname, files, outputfile):
    for file in files:
        analyse(zipname, file, outputfile)


def EOT(content):
    foldername = content.filelist[0].filename.split("/")[0]
    shutil.rmtree(foldername)


if __name__ == "__main__":
    zipfilename = input("Nom du ou des fichiers zip (sep \";\") : ")
    zipfilename = zipfilename.split(";")
    for zipname in zipfilename:
        if (".json" in zipname):
            zip1 = zipname.split("\\")[-1]
            outputfilename = zip1[:-4] + "-rapport_auteurs_homonymes.txt"
            outputfile = open(outputfilename, "w", encoding="utf-8")
            outputfile.write("\t".join(["Titre", "Liste des ARK BIB",
                                        "Clé Nom", "Nom", "NNA"]) + "\n")
            content = zip_2_files(zipname)
            checkfiles(zipname, content.filelist, outputfile)
            EOT(content)
    if errors:
        errors_file = open("erreurs_JSON.txt", "a", encoding="utf-8")
        for error in errors:
            errors_file.write("\t".join(error) + "\n")

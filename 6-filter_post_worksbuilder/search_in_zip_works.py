# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 09:46:11 2018

@author: BNF0017855

Programme d'extraction et d'analyse des oeuvres
générées par RobotDonnées

Processus :
    - dézipper
    - ouvrir un ensemble de fichiers JSON
    - Appliquer chacun des filtres
"""
import zipfile
from collections import defaultdict
from unidecode import unidecode
import json
import codecs
import os

import SRUextraction as sru

reader = codecs.getreader("utf-8")

liste_pep_elementaires = []


def zip_2_files(zipfile_name):
    """A partir d'un nom de fichier ZIP, renvoie la liste
    des noms de fichiers contenus dans le zip"""
    file = zipfile.ZipFile(zipfile_name)
    file.extractall()
    return file


def filename2json(filename):
    """A partir d'un nom de fichier JSON, récupération
    de son contenu dans une variable"""
    data = ""
    with open(zipfile.open(filename)) as f:
        data = json.load(f)
        print(data)
    return data


def TIC2list(TIC):
    """
    En entrée, le JSON du fichier
    En sortie, la liste des valeurs mises bout à bout
    """
    liste_values = []
    for element in TIC:
        if type(TIC[element]) is str:
            liste_values.append(TIC[element])
        elif type(TIC[element]) is list:
            for el in TIC[element]:
                if type(el) is list:
                    for el2 in el:
                        liste_values.append(el2)
                elif type(el) is int or type(el) is str:
                    liste_values.append(el)
        elif type(TIC[element]) is int or type(TIC[element]) is str:
            liste_values.append(el)
        elif (type(TIC[element]) is dict):
            for key in TIC[element]:
                liste_values.append(TIC[element][key])
    liste_values = [unidecode(str(el).lower()) for el in liste_values if el]
    return liste_values
            

def search_in_file(file, zipname, report, keywords):
    """"
    En entrée, un fichier JSON contenant une oeuvre
    on extrait tous les mots qu'il contient, concaténés dans une liste
    et on cherche si tous les keywords sont présents dans cette liste
    """
    try:
        with open(file.filename) as f:
            print(file.filename)
            TIC = json.load(f)
            liste_value_tic = TIC2list(TIC)
            test = True
            for word in keywords:
                if word not in liste_value_tic:
                    test = False
            if test:
                line = [zipname, file.filename, TIC["preferred_title"]["title"],
                        " ".join(keywords), " ".join(TIC["manifs"])]
                print(line)
                report.write("\t".join(line) + "\n")
    except FileNotFoundError as err:
        pass

def check_empty_titles(TIC, report, filename, zipname):
    """Vérifie si le titre de l'oeuvre est
    une chaîne de caractères vide"""
    test = True
    title = TIC["preferred_title"]["title"].strip()
    if not title:
        test = False
        tic2report(TIC, "Titre vide", report, filename, zipname)
    return test


def RepresentsInt(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def tic2report(TIC, error, report, filename, zipname):
    workid = TIC["id"]
    work_arks = ", ".join(TIC["manifs"])
    work_title = TIC["preferred_title"]["title"]
    line = [error, zipname, filename, workid, work_arks, work_title]
    report.write("\t".join(line) + "\n")


def checkfiles(files, zipname, report, keywords):
    for file in files:
        search_in_file(file, zipname, report, keywords)
        os.remove(file.filename)


def report_name2reportfile(report_name):
    outputfile = open(report_name, "w", encoding="utf-8")
    headers = ["run (nom fichier ZIP)", "fichier JSON", "Titre de l'oeuvre",
               "Mot recherché", "ARKs Manifs"]
    outputfile.write("\t".join(headers) + "\n")
    return outputfile


def EOT(report):
    report.close()


def searchwords(zipname, report_name, keywords):
    content = zip_2_files(zipname)
    report = report_name2reportfile(report_name)
    checkfiles(content.filelist, zipname, report, keywords)
    EOT(report)


if __name__ == "__main__":
    zipfilename = input("Nom du ou des fichiers zip (sep \";\") : ")
    keywords = input("mot(s) à rechercher : ")
    report_name = input("Nom du rapport : ")
    if not report_name:
        report_name = "rapport.txt"
    elif (report_name[-4] != "."):
        report_name += ".txt"
    keywords = unidecode(keywords.lower()).split()
    zipfilename = zipfilename.split(";")
    for zipname in zipfilename:
        print("\n\n\n", zipname)
        searchwords(zipname, report_name, keywords)

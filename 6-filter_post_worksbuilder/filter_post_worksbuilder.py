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
import json
import codecs
import os

import SRUextraction as sru

reader = codecs.getreader("utf-8")

liste_pep_elementaires = []


def zip_2_files(zipfilename):
    """A partir d'un nom de fichier ZIP, renvoie la liste
    des noms de fichiers contenus dans le zip"""
    file = zipfile.ZipFile(zipfilename)
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


def filter(file, zipfile_ok, zipfile_ko, report, zipname):
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
        test = liste_tests(TIC, report, file.filename, zipname)
        if test:
            zipfile_ok.write(file.filename)
            print(zipname, file.filename)
        else:
            zipfile_ko.write(file.filename)
            print(zipname, file.filename, "rejected")


def liste_tests(TIC, report, f, zipname):
    """Applique une liste de tests
    puis renvoie True ou False """
    test = check_empty_titles(TIC, report, f, zipname)
    if test:
        test = check_long_titles(TIC, report, f, zipname)
    if test:
        test = check_elementary_pep(TIC, report, f, zipname)
    return test


def check_empty_titles(TIC, report, filename, zipname):
    """Vérifie si le titre de l'oeuvre est
    une chaîne de caractères vide"""
    test = True
    title = TIC["preferred_title"]["title"].strip()
    if not title:
        test = False
        tic2report(TIC, "Titre vide", report, filename, zipname)
    return test


def check_long_titles(TIC, report, filename, zipname):
    """Vérifie si le titre de l'oeuvre est
    une chaîne de caractères vide"""
    test = True
    title = TIC["preferred_title"]["title"]
    if len(title) > 510:
        test = False
        tic2report(TIC, "Titre trop long", report, filename, zipname)
    return test


def check_elementary_pep(TIC, report, filename, zipname):
    """Vérifie si toutes les PEP sont élémentaires"""
    test = False
    for author in TIC["authors"]:
        nna = author[3]
        if nna not in liste_pep_elementaires:
            sru_query = f'aut.recordid any "{nna}"'
            sru_results = sru.SRU_result(sru.srubnf_url, {"query": sru_query})
            sru_nb_results = sru_results.nb_results
            # Si la requête SRU a donné 0 résultat : c'est une PEP
            # élémentaire (ou la PEP a été fusionnée avec une autre
            # entre temps)
            if (sru_nb_results):
                test = True
            else:
                liste_pep_elementaires.append(nna)
    if not test:
        tic2report(TIC, "PEP élémentaires", report, filename, zipname)
    return test


def tic2report(TIC, error, report, filename, zipname):
    workid = TIC["id"]
    work_arks = ", ".join(TIC["manifs"])
    work_title = TIC["preferred_title"]["title"]
    line = [error, zipname, filename, workid, work_arks, work_title]
    report.write("\t".join(line) + "\n")


def checkfiles(files, zipname, report):
    outputzipname = zipname[:-4] + "-filter_ok.zip"
    excluded_works_name = zipname[:-4] + "-filter_ko.zip"
    outputzip = zipfile.ZipFile(outputzipname, "w")
    excluded_works = zipfile.ZipFile(excluded_works_name, "w")
    for file in files:
        filter(file, outputzip, excluded_works, report, zipname)
        os.remove(file.filename)


def zip2reportfile(zipname):
    outputfilename = zipname[:-4] + "-rejected.txt"
    outputfile = open(outputfilename, "w", encoding="utf-8")
    headers = ["Motif", "Fichier ZIP", "Fichier JSON",
               "ID Oeuvre", "ARK Manif", "Titre"]
    outputfile.write(header + "\n")
    return outputfile


def EOT(report):
    report.close()


def filter1zipfile(zipname):
    content = zip_2_files(zipname)
    report = zip2reportfile(zipname)
    checkfiles(content.filelist, zipname, report)
    EOT(report)


if __name__ == "__main__":
    zipfilename = input("Nom du ou des fichiers zip (sep \";\") : ")
    zipfilename = zipfilename.split(";")
    for zipname in zipfilename:
        filter1zipfile(zipname)

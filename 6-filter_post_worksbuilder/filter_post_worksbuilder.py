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
import re
import json
import codecs
import os

import SRUextraction as sru

reader = codecs.getreader("utf-8")

liste_pep_elementaires = []

liste_ark_manifs = []
liste_nna_aut = []

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


def filter(file, zipfile_ok, zipfile_ko, report, zipname,
           file_ark_manifs, file_ark_aut):
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
            TIC_2_lists(TIC, file_ark_manifs, file_ark_aut)
            print(zipname, file.filename)
        else:
            zipfile_ko.write(file.filename)
            print(zipname, file.filename, "rejected")


def TIC_2_lists(TIC, file_ark_manifs, file_ark_aut):
    """
    Génération de la liste des ARK concernés par les oeuvres créés
    """
    for ark_manif in TIC["manifs"]:
        if ark_manif not in liste_ark_manifs:
            liste_ark_manifs.append(ark_manif)
            file_ark_manifs.write(ark_manif + "\n")
    
    for author in TIC["authors"]:
        nna = author[3]
        if nna not in liste_nna_aut:
            liste_nna_aut.append(nna)
            file_ark_manifs.write(nna2ark(nna) + "\n")


def liste_tests(TIC, report, f, zipname):
    """Applique une liste de tests
    puis renvoie True ou False """
    test = check_empty_titles(TIC, report, f, zipname)
    if test:
        test = check_crochets_carres(TIC, report, f, zipname)
    if test:
        test = check_long_titles(TIC, report, f, zipname)
    if test:
        test = check_elementary_pep(TIC, report, f, zipname)
    if test:
        test = check_workdate(TIC, report, f, zipname)
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


def check_crochets_carres(TIC, report, filename, zipname):
    """Vérifie si le titre de l'oeuvre contient un crochet 
    ouvrant"""
    test = True
    title = TIC["preferred_title"]["title"].strip()
    if "[" in  title:
        test = False
        tic2report(TIC, "Titre avec crochet carré", report, filename, zipname)
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


def check_workdate(TIC, report, filename, zipname):
    test = True
    date = TIC["date"]
    if (date and RepresentsInt(date)):
        date = int(date)
        if (date > 2018):
            test = False
    if not test:
        tic2report(TIC, "Date > 2018", report, filename, zipname)
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


def checkfiles(files, zipname, report, file_ark_manifs, file_ark_aut):
    outputzipname = zipname[:-4] + "-filter_ok.zip"
    excluded_works_name = zipname[:-4] + "-filter_ko.zip"
    outputzip = zipfile.ZipFile(outputzipname, "w")
    excluded_works = zipfile.ZipFile(excluded_works_name, "w")
    for file in files:
        filter(file, outputzip, excluded_works, report, zipname,
               file_ark_manifs, file_ark_aut)
        os.remove(file.filename)


def zip2reportfile(zipname):
    outputfilename = zipname[:-4] + "-rejected.txt"
    outputfile = open(outputfilename, "w", encoding="utf-8")
    headers = ["Motif", "Fichier ZIP", "Fichier JSON",
               "ID Oeuvre", "ARK Manif", "Titre"]
    outputfile.write("\t".join(headers) + "\n")
    return outputfile


def dedupe(files, zip_file_name):
    liste_dedupes = []
    """
    Supprimer les clusters composés seulement d'une traduction
    alors qu'on a aussi un cluster avec toutes les éditions
    dans toutes les langues
    """
    dict_clusters2manifs = defaultdict(set)
    dict_clusters2filename = defaultdict(str)
    dict_manifs2clusters = defaultdict()
    dict_jsonfile2content = defaultdict() 

    for jsonfile in files:
        print("dedupe_analysis", jsonfile.filename)
        with open(jsonfile.filename) as f:
            dict_jsonfile2content[jsonfile.filename] = defaultdict(dict)
            work = json.load(f)
            dict_jsonfile2content[jsonfile.filename]["json"] = work
            dict_jsonfile2content[jsonfile.filename]["id"] = work["id"]
            id_work = work["id"]
            manifs = work["manifs"]
            nb_manifs = len(manifs)
            dict_clusters2filename[id_work] = jsonfile.filename
            for manif in manifs:
                if (manif in dict_manifs2clusters
                    and "list_works" in dict_manifs2clusters[manif]):
                    dict_manifs2clusters[manif]["list_works"][id_work] = nb_manifs
                else:
                    dict_manifs2clusters[manif] = {"list_works": {
                                                                id_work: nb_manifs
                                                                }
                                                  }
                dict_clusters2manifs[id_work].add(manif)

    # On réécrit ensuite un fichier ZIP avec uniquement les oeuvres
    # qui ne font pas doublon
    zip_file_filter_name = zip_file_name[:-4]+"-dedupe.zip"
    zip_file_filter = zipfile.ZipFile(zip_file_filter_name, "w")
    selected_works = set()
    for manif in dict_manifs2clusters:
        dict_manifs2clusters[manif]["selected_work"] = max(dict_manifs2clusters[manif]["list_works"], 
                                                    key=lambda key: dict_manifs2clusters[manif]["list_works"][key])
        selected_works.add(dict_manifs2clusters[manif]["selected_work"])
        for work in dict_manifs2clusters[manif]["list_works"]:
            if work != dict_manifs2clusters[manif]["selected_work"]:
                liste_dedupes.append(work + "\t" + dict_manifs2clusters[manif]["selected_work"])

    selected_works = list(selected_works)
    for id_work in selected_works:
        json_filename = dict_clusters2filename[id_work]
        work = dict_jsonfile2content[json_filename]["json"]
        # file = open(json_filename, "w", encoding="utf-8")
        zip_file_filter.write(json_filename)
        # os.remove(file)
    liste_dedupes = list(set(liste_dedupes))
    dedupe_files = open(f"{zip_file_name.replace('.zip', '')}-oeuvres_dedoublonnees.txt", "w", encoding="utf-8")
    for dedupe in liste_dedupes:
        dedupe_files.write(dedupe + "\n")

    return zip_file_filter_name


def EOT(list_files):
    for report in list_files:
        report.close()


def filter1zipfile(zipname, file_ark_manifs, file_ark_aut):

    content = zip_2_files(zipname)

    zip_file_dedupe_name = dedupe(content.filelist, zipname)
    dedupe_content = zip_2_files(zip_file_dedupe_name)
    report = zip2reportfile(zip_file_dedupe_name)
    checkfiles(dedupe_content.filelist, zipname,
               report, file_ark_manifs, file_ark_aut)
    EOT([report])


def lists_ark(id_treatment):
    if not id_treatment:
        import datetime
        now = datetime.datetime.now()
        id_treatment = str(now.year) + str(now.month) + str(now.day) + str(now.hour) + str(now.minute) + str(now.second)
    if (id_treatment[-1] != "-"
        and id_treatment[-1] != "_"):
        id_treatment += "-"
    file_ark_manifs = open(id_treatment + "ark_manifs.txt", "w", encoding="utf-8")
    file_ark_aut = open(id_treatment + "ark_aut.txt", "w", encoding="utf-8")
    return file_ark_manifs, file_ark_aut


def nna2ark(nna):
    """Conversion d'un NNA en ARK"""
    ark = sru.SRU_result("http://catalogue.bnf.fr/api/SRU?",
                         {"query": f"aut.recordid any {nna}"}).liste_identifiers
    if ark:
        ark = ark[0]
    else:
        ark = ""
    return ark

if __name__ == "__main__":
    zipfilename = input("Nom du ou des fichiers zip (sep \";\") : ")
    id_treatment = input("Identifiant du traitement : ")
    file_ark_manifs, file_ark_aut = lists_ark(id_treatment)
    zipfilename = zipfilename.split(";")
    for zipname in zipfilename:
        filter1zipfile(zipname, file_ark_manifs, file_ark_aut)
    EOT([file_ark_manifs, file_ark_aut])
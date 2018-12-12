# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 09:46:11 2018

@author: BNF0017855

Programme d'extraction et d'analyse des oeuvres générées par
RobotDonnées pour identifier les titres d'un même auteur qui seraient
quasiment identiques (hypothèse : suite à une faute de frappe dans le titre)

Processus :
    1. dezipper un lot d'oeuvre
    2. pour un auteur donné, extraire les formes de titre
    3. comparer à 2 caractères près

Fonctions nécessaires :
    - dézipper
    - ouvrir un ensemble de fichiers JSON
    - calculer la distance de Levenshtein
"""
import zipfile
import json
import string
import codecs
import shutil
from collections import defaultdict
import pprint
from unidecode import unidecode
import distance

from stdf import create_file, line2report

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


def analyse(dict_aut2titles, dict_titles2ark, zipname, file):
    """
    Il faut pour un zip donné, regrouper les oeuvres d'un même auteur
    --> dictionnaire au niveau du zip
    """
    with open(file.filename) as f:
        try:
            TIC = json.load(f)
            liste_authors = []
            for author in TIC["authors"]:
                liste_authors.append(author[-1])
            title = TIC["preferred_title"]["title"]
            for author in liste_authors:
                dict_aut2titles[author].add(title)
            for ark in TIC["manifs"]:
                dict_titles2ark[title].add(ark)            
        except json.decoder.JSONDecodeError as err:
            errors.append([zipname, file.filename, str(err)])


def analyse_titles(author, liste_titles,
                   dict_titles2ark, zipname, outputfile):
    """
    Si un auteur a plusieurs titres associés : 
    on compare chaque titre avec chacun des titres suivants dans la liste
    en ne tenant pas compte des variantes sur les chiffres
    """
    i = 0
    for title in liste_titles[i:]:
        title_chars = clean_titles_int(title)
        for foll_title in liste_titles[i + 1:]:
            foll_title_chars = clean_titles_int(foll_title)
            dist = distance.levenshtein(title, foll_title)
            if ((dist == 1 or dist == 2)
                and title_chars != foll_title_chars):
                nbark_title1 = len(dict_titles2ark[title])
                nbark_title2 = len(dict_titles2ark[foll_title])
                ark_title = " ".join(list(dict_titles2ark[title]))
                ark_foll_title = " ".join(list(dict_titles2ark[foll_title]))
                if nbark_title1 > nbark_title2:
                    line = [str(author),
                            ark_title, title,
                            ark_foll_title, foll_title,
                            str(dist), zipname]
                    line2report(line, outputfile)
                else:
                    line = [str(author),
                            ark_foll_title, foll_title,
                            ark_title, title,
                            str(dist), zipname]
                    line2report(line, outputfile)
        i += 1

def clean_titles_int(text):
    """
    Suppression des chiffres dans les chaînes de caractères, pour éviter
    que ce soit seulement une date ou un numéro qui indique un problème
    """
    for char in string.digits:
        text = text.replace(str(char), "")
    return text


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
            if ((distance.levenshtein(el, k) == 1
                 or distance.levenshtein(el, k) == 2)
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
    dict_aut2titles = defaultdict(set)
    dict_titles2ark = defaultdict(set)
    for file in files:
        analyse(dict_aut2titles, dict_titles2ark, zipname, file)

    for author in dict_aut2titles:
        if len(dict_aut2titles[author]) > 1:
            analyse_titles(author, list(dict_aut2titles[author]),
                           dict_titles2ark, zipname, outputfile)


def EOT(content):
    foldername = content.filelist[0].filename.split("/")[0]
    shutil.rmtree(foldername)


if __name__ == "__main__":
    zipfilename = input("Nom du ou des fichiers zip (sep \";\") : ")
    zipfilename = zipfilename.split(";")
    for zipname in zipfilename:
        if (".zip" in zipname):
            zip1 = zipname.split("\\")[-1]
            outputfilename = zip1[:-4] + "-rapport_titres_quasi_identiques.txt"
            outputfile = open(outputfilename, "w", encoding="utf-8")
            outputfile.write("\t".join(["NNA", "Titre 1",
                                        "ARKs Titre 1", "Titre 2", "ARKs Titre 2"]) + "\n")
            content = zip_2_files(zipname)
            checkfiles(zipname, content.filelist, outputfile)
            EOT(content)
    if errors:
        errors_file = open("erreurs_JSON.txt", "a", encoding="utf-8")
        for error in errors:
            errors_file.write("\t".join(error) + "\n")

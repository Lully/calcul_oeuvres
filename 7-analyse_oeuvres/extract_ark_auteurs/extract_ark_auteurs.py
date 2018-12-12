# coding: utf-8

"""
Récupération de la liste des NNA d'un lot d'oeuvres
"""

import zipfile
import json
import codecs
import shutil


from stdf import create_file, line2report, nn2ark

def zip_2_files(zipfilename):
    """A partir d'un nom de fichier ZIP, renvoie la liste des noms de fichiers
    contenus dans le zip"""
    file = zipfile.ZipFile(zipfilename)
    file.extractall()   
    return file


def extract(zipname, files, nna_extracted, outputfile):
    for file in files:
        analyse(zipname, file, nna_extracted, outputfile)


def analyse(zipname, file, nna_extracted, outputfile):
    with open(file.filename) as f:
        try:
            TIC = json.load(f)
            liste_authors = TIC["authors"]
            if (len(liste_authors) > 1):
                extract_authors(liste_authors, nna_extracted, outputfile)
        except json.decoder.JSONDecodeError as err:
            pass


def extract_authors(liste_authors, nna_extracted, outputfile):
    for aut in liste_authors:
        nna = str(aut[-1])
        if (nna not in nna_extracted):
            nna_extracted.append(nna)
            ark = nn2ark(nna)
            line2report(ark, outputfile)


def EOT(content):
    foldername = content.filelist[0].filename.split("/")[0]
    shutil.rmtree(foldername)



if __name__ == "__main__":
    zipfilename = input("Nom du ou des fichiers zip (sep \";\") : ")
    zipfilename = zipfilename.split(";")
    nna_extracted = []
    for zipname in zipfilename:
        if (".zip" in zipname):
            zip1 = zipname.split("\\")[-1]
            outputfilename = zip1[:-4] + "-liste_arks_auteurs.txt"
            outputfile = open(outputfilename, "w", encoding="utf-8")
            content = zip_2_files(zipname)
            extract(zipname, content.filelist, nna_extracted, outputfile)
            EOT(content)
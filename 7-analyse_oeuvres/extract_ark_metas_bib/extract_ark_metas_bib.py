# coding: utf-8

"""
Récupération des métadonnées des notices BIB dans les oeuvres RobotDonnées
En sortie : fichier tabulé avec ARK BIB, hash de l'oeuvre et zone(s) demandées
"""

import zipfile
import json
import codecs
import shutil


from stdf import create_file, line2report, nn2ark
import SRUextraction as sru

def zip_2_files(zipfilename):
    """A partir d'un nom de fichier ZIP, renvoie la liste des noms de fichiers
    contenus dans le zip"""
    file = zipfile.ZipFile(zipfilename)
    file.extractall()   
    return file


def extract(zipname, files, extract_zones, outputfile):
    for file in files:
        analyse(zipname, file, extract_zones, outputfile)


def analyse(zipname, file, extract_zones, outputfile):
    with open(file.filename) as f:
        try:
            TIC = json.load(f)
            liste_manifs = TIC["manifs"]
            id_RD = TIC["id"]
            extract_fields(liste_manifs, id_RD, extract_zones, outputfile)
        except json.decoder.JSONDecodeError as err:
            pass


def extract_fields(liste_manifs, id_RD, extract_zones, outputfile):
    for ark in liste_manifs:
        values = ark2values(ark, extract_zones)
        line = [ark, id_RD]
        line.extend(values)
        line2report(line, outputfile)


def ark2values(ark, extract_zones):
    default_param = {"recordSchema": "intermarcxchange"}
    result = sru.SRU_result(f"bib.persistentid any \"{ark}\"", parametres=default_param)
    #print(result.url)
    xml_record = None
    for ark in result.dict_records:
        xml_record = result.dict_records[ark]
    values = []
    if xml_record is not None:
        for zone in extract_zones.split(";"):
            values.append(sru.record2fieldvalue(xml_record, zone))
    return values

def EOT(content):
    foldername = content.filelist[0].filename.split("/")[0]
    shutil.rmtree(foldername)

def headers(outputfile, extract_zones):
    """
    Ajout d'en-têtes de colonnes
    """
    line = ["ARK BIB", "id hash RobotDonnées"]
    line.extend(extract_zones.split(";"))
    line2report(line, outputfile)

if __name__ == "__main__":
    zipfilename = input("Nom du ou des fichiers zip (sep \";\") : ")
    extract_zones = input("Zones à exporter (sep \";\") :")
    zipfilename = zipfilename.split(";")
    for zipname in zipfilename:
        if (".zip" in zipname):
            zip1 = zipname.split("\\")[-1]
            outputfilename = zip1[:-4] + "-liste_arks_auteurs.txt"
            outputfile = open(outputfilename, "w", encoding="utf-8")
            headers(outputfile, extract_zones)
            content = zip_2_files(zipname)
            extract(zipname, content.filelist, extract_zones, outputfile)
            EOT(content)
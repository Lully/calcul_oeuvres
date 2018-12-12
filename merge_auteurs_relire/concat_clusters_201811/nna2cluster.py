# coding: utf-8

"""
Récupération du 100$a$m pour constituer des fichiers concernant les auteurs homonymes...
"""
import urllib.parse
import string
from collections import defaultdict

from unidecode import unidecode

import SRUextraction as sru
from stdf import create_file

input_filename = "tous_clusters_dedupe-nett.txt"

def row2row17(row):
    # Ajustement des colonnes finales en rajoutant des tabulations si nécessaire
    row = row.replace("\r", "").replace("\n", "")
    row += "\t" * (17 - len(row.split("\t"))) + "\n"
    return row


def clean(key):
    key = unidecode(key.lower())
    for char in string.punctuation:
        key = key.replace(char, "")
    key = key.replace("-", "").replace(" ", "")
    return key

def ark2key(arkA):
    pep_record = sru.SRU_result(f'aut.persistentid any "{urllib.parse.quote(arkA)}" and aut.status any "sparse validated"',
                                parametres={"recordSchema": "intermarcxchange"}).dict_records
    xml_rec = None
    for rec in pep_record:
        xml_rec = pep_record[rec]
    key = ""
    if xml_rec is not None:
        key = sru.record2fieldvalue(xml_rec, "100$a") + sru.record2fieldvalue(xml_rec, "100$m")
    key = clean(key)
    print("key", arkA, key)
    return key

arkA_treated = []
dict_key2ark = defaultdict(list)
dict_arkA2row = defaultdict(list)

output_file = create_file("pep_homonymes.txt")

with open(input_filename, encoding="utf-8") as f:
    for row in f:
        arkA = row.split("\t")[2]
        if arkA not in arkA_treated:
            arkA_treated.append(arkA)
            key = ark2key(arkA)
            dict_key2ark[key].append(arkA)
        dict_arkA2row[arkA].append(row)

for key in dict_key2ark:
    if len(dict_key2ark[key]) > 1:
        print("homonymes", key, arkA)
        for arkA in dict_key2ark[key]:
            for row in dict_arkA2row[arkA]:
                row = row2row17(row)
                output_file.write(row)




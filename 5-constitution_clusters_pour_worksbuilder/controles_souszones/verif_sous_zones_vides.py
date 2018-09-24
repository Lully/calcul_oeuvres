# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 14:22:15 2018

@author: BNF0017855

Actuellement, RobotDonnées plante quand il veut récupérer dans une notice une sous-zone vide

"""
import csv 
from collections import defaultdict
from urllib import request
import urllib.parse
from unidecode import unidecode
import urllib.error as error
from lxml import etree
from lxml.html import parse
import http

ns = {"srw":"http://www.loc.gov/zing/srw/", "mxc":"info:lc/xmlns/marcxchange-v2", "m":"http://catalogue.bnf.fr/namespaces/InterXMarc","mn":"http://catalogue.bnf.fr/namespaces/motsnotices"}
urlSRUroot = "http://catalogueservice.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query="
urlNoticeService = "http://noticesservices.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query="

liste_nnb_traites = set()




def testURLetreeParse(url):
    test = True
    resultat = ""
    try:
        resultat = etree.parse(request.urlopen(url))
    except etree.XMLSyntaxError as err:
        print(url)
        print(err)
        test = False
    except etree.ParseError as err:
        print(url)
        print(err)
        test = False
    except error.URLError as err:
        print(url)
        print(err)
        test = False
    except ConnectionResetError as err:
        print(url)
        print(err)
        test = False
    except TimeoutError as err:
        print(url)
        print(err)
        test = False
    except http.client.RemoteDisconnected as err:
        print(url)
        print(err)
        test = False
    except http.client.BadStatusLine as err:
        print(url)
        print(err)
        test = False
    except ConnectionAbortedError as err:
        print(url)
        print(err)
        test = False
    return (test,resultat)

def url_requete_sru(query,recordSchema="InterXMarc_Complet",maximumRecords="1000",startRecord="1"):
    if ("idPerenne" in query):
        url = urlNoticeService + urllib.parse.quote(query) +"&recordSchema=" + recordSchema + "&maximumRecords=" + maximumRecords + "&startRecord=" + startRecord
    else:
        url = urlSRUroot + urllib.parse.quote(query) +"&recordSchema=" + recordSchema + "&maximumRecords=" + maximumRecords + "&startRecord=" + startRecord
    return url

def row2check_subfield(ark):
    url = url_requete_sru('idPerenne any "' + ark + '"')
    (test,record) = testURLetreeParse(url)
    if (test):
        j = 0
        for field in record.xpath("//m:record/m:datafield", namespaces=ns):
            j += 1
            tag = field.get("tag")
            if (tag[0] == "1" or tag[0] == "2" or tag[0] == "7") :
                i = 0
                if (tag == "100" or tag == "110" or tag == "700" or tag == "710"):
                    #print(tag)
                    try:
                        subf = field.find("m:subfield[@code='3']", namespaces=ns).text
                    except AttributeError as err:
                        
                        line = [ark[13:21], tag+ "$3 absent"]
                        print(line)
                        output_file.write("\t".join(line) + "\n")
                    try:
                        subf = field.find("m:subfield[@code='4']", namespaces=ns).text
                    except AttributeError as err:
                        
                        line = [ark[13:21], tag+ "$4 absent"]
                        print(line)
                        output_file.write("\t".join(line) + "\n")
                        
                for subfield in field.xpath("m:subfield", namespaces=ns):
                    i += 1
                    code = subfield.get("code")
                    if (subfield.text == "" or subfield.text is None or type(subfield.text) is None):
                        line = [ark[13:21], tag+ "$"+code]
                        output_file.write("\t".join(line) + "\n")
                if (i == 0):
                    line = [ark[13:21], tag]
                    output_file.write("\t".join(line) + "\n")

        for field in record.xpath("//m:controlfield", namespaces=ns):
            tag = field.get("tag")
            if (field.text == "" or field.text is None or type(field.text) is None):
                line = [ark[13:21], tag]
                print(line)
                output_file.write("\t".join(line) + "\n")
        if (j == 0):
            line = [ark[13:21]]
            print(line)
            output_file.write("\t".join(line) + "\n")

def controles_1_file(input_filename):
    with open(input_filename, newline="\n", encoding="utf-8") as csvfile:
        input_file = csv.reader(csvfile, delimiter='\t')
        col_ark = 0
        i = 1
        for row in input_file:
            if ("id de la manifestation (ARK)" in row):
                col_ark = row.index("id de la manifestation (ARK)")
            else:
                ark = row[col_ark]
                if (ark not in liste_nnb_traites):
                    print(i, ark)
                    liste_nnb_traites.add(ark)
                    row2check_subfield(ark)
            i += 1

if __name__ == '__main__':
    input_filename = input("Nom du fichier en entrée : ")
    input_filename_list = input_filename.split(",")
    for filename in input_filename_list:
        output_filename = filename[:-4] + "-NNB-souszones-vides.txt"
        output_file= open(output_filename, "w", encoding="utf-8")
        output_file.write("\t".join(["NNB","ark", "zone/sous-zone"]) + "\n")
        controles_1_file(filename)
        output_file.close()

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 12:13:25 2017

@author: BNF0017855
En entrée, une liste de PEP : chaque élément de la liste est une liste à 2 éléments [PEP source, PEP cible]
Le programme récupère toutes les dates de publication (008) de la PEP source pour vérifier qu'elles ne sont pas antérieures à la date de naissance de la PEP cible+10 ans
"""

from lxml import etree
from listePEP import listePEP
ns = {"srw":"http://www.loc.gov/zing/srw/", "mxc":"info:lc/xmlns/marcxchange-v2", "m":"http://catalogue.bnf.fr/namespaces/InterXMarc","mn":"http://catalogue.bnf.fr/namespaces/motsnotices"}

rapportPb = open("rapport_problemes.txt","w")
rapport_complet = open("rapport_complet.txt","w")
rapport_complet.write("NNA source\tNNAcible\tCible : Date naissance\tSource : Date publication la plus ancienne\n")
rapportPb.write("NNA source\tNNAcible\tCible : Date naissance\tSource : Date publication la plus ancienne\n")

def nna2datesPub(nna):
    url = "http://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.author2bib%20any%20%22" + nna + "%22&recordSchema=intermarcxchange&maximumRecords=1000&startRecord=1"
    page = etree.parse(url)
    listeDates = []
    for record in page.xpath("//srw:recordData/mxc:record",namespaces=ns):
        date = record.find("mxc:controlfield[@tag='008']",namespaces=ns).text[8:12]
        #print(date)
        if (date.find(".")<0 and date.find(" ")<0 and date.find("x")<0 and date.find("?")<0):
            listeDates.append(int(date))
    listeDates = sorted(listeDates)
    #print(listeDates)
    date_ancienne = False
    if (len(listeDates) > 0):
        date_ancienne = listeDates[0]
    return date_ancienne
         
def nna2birthdate10(nna):
    url = "http://catalogueservice.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=NN%20any%20" + nna + "&recordSchema=InterXMarc_Complet"
    page = etree.parse(url)
    birthdate = False
    f008_2831 = " "
    if (page.find("//m:controlfield[@tag='008']", namespaces=ns) is not None):
        f008_2831 = page.find("//m:controlfield[@tag='008']", namespaces=ns).text[28:32]
    if (f008_2831.find(".")<0 and f008_2831.find(" ")<0):
        birthdate = int(f008_2831)
        birthdate = birthdate+10
    return birthdate

for PEP in listePEP:
    pep_source = PEP[0]
    pep_cible = PEP[1]
    date_naissance_cible10 = nna2birthdate10(pep_cible)
    pep_source_datesPub = nna2datesPub(pep_source)
    rapport_complet.write(pep_source + " | " + pep_cible + " | " + str(date_naissance_cible10) + " | " + str(pep_source_datesPub) + "\n")
    if (pep_source_datesPub is not False and date_naissance_cible10 is not False):
        if (pep_source_datesPub < date_naissance_cible10):
            rapportPb.write("\t".join([pep_source,pep_cible,str(date_naissance_cible10),str(pep_source_datesPub)]) + "\n")
            
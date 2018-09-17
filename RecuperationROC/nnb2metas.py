# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 13:58:53 2016

@author: BNF0017855

A partir d'une liste de NNB, récupérer l'ark du NNB grâce à la fonction nn2ark. Puis récupérer le NNA et l'ark du NNA grâce à cette même fonction nn2ark.
"""

from lxml import etree

results = open("nnb_ark.txt","a")
results.write("id de l'auteur (FRBNF)    id de l'auteur (ARK)	clusterid	clusternum	Titre de l'oeuvre	id de la manifestation (FRBNF)	id de la manifestation (ARK)	Titre Manifestation	Type de notice	Type de document	zones	methode	date\n")
listeNNB = []
listeNNB_corr = []
with open("oeuvres_ROC.txt") as f:
    listeNNB = f.readlines()
for el in listeNNB[1:]:
    el = el.replace("\n","")
    el = el.split("\t")
    listeNNB_corr.append(el)


#for ark in fileARK:
#    listeARK.append(ark.replace("\n",""))


ns = {"srw":"http://www.loc.gov/zing/srw/","m":"http://catalogue.bnf.fr/namespaces/InterXMarc","mn":"http://catalogue.bnf.fr/namespaces/motsnotices"}

def nn2ark(nn):
    url = "http://catalogueservice.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=NN%20any%20" + nn + "&recordSchema=InterXMarc_Complet"
    record = etree.parse(url)
    ark = ""
    if (record.find("//srw:record/srw:recordIdentifier", namespaces=ns) is not None):
        ark = record.find("//srw:record/srw:recordIdentifier", namespaces=ns).text
    return ark

for el in listeNNB_corr[758725:]:
    idOeuvre = el[0]
    nnb = el[1]
    arkNNB = nn2ark(nnb)
    url = "http://catalogueservice.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=NN%20any%20" + nnb + "&recordSchema=InterXMarc_Complet"
    record = etree.parse(url)
    nna = ""
    if (record.find("//m:datafield[@tag='100']/m:subfield[@code='3']", namespaces=ns) is not None):
        nna = record.find("//m:datafield[@tag='100']/m:subfield[@code='3']", namespaces=ns).text
    arkNNA = nn2ark(nna)
    if (arkNNA != ""):
        results.write("\t".join([nna, arkNNA, idOeuvre, "", "", nnb, arkNNB]) + "\n")
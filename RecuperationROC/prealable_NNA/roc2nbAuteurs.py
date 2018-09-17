# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 13:58:53 2016

@author: BNF0017855

Compte le nombre de manifs dans chaque oeuvre du ROC
pour en extraire les oeuvres contenant plusieurs manifs
afin de travailler sur les PEP
"""

from lxml import etree

results = open("nnb_ark_count.txt","w")

listeROC = []
listeROC_corr = []
with open("oeuvresROC_multimanif.txt") as f:
    listeROC = f.readlines()
for el in listeROC:
    el = el.replace("\n","").split("\t")
    listeROC_corr.append(el)

results.write("id de l'auteur (FRBNF)    id de l'auteur (ARK)	clusterid	clusternum	Titre de l'oeuvre	id de la manifestation (FRBNF)	id de la manifestation (ARK)	Titre Manifestation	Type de notice	Type de document	zones	methode	date\n")


#listeNNA_corr = ['T3B--102-107;1;0901-0909','T3B--102-107;1;091-099','T3B--1-8;1;1-7','T3B--1-8;1;8','T3B--1-8;1;8001-8007','T3B--1-8;1;8008','T3B--1-8;1;8009','T3B--1-8;1;801-809','T3B--1-8;1;9','T3B--1-8;1;901-907','T3B--1-8;1;908','T3B--1-8;1;909','T3B--1-8;1;91-99','T3B--81-89;1;001-009','T3B--81-89;1;02','T3B--81-89;1;0201-0209','T3B--81-89;1;03','T3B--81-89;1;0301-0309','T3B--81-89;1;07','T3B--81-89;1;0701-0709','T3B--81-89;1;08','T3B--81-89;1;0801-0809','T4--8642-8649;1;024','T5--051-059;1;001-009','T5--051-059;1;09','T5--051-059;1;1-9','352-354;1;22','352-354;1;2293','352-354;1;27-28','380;1;09 vs. 380;1;065','616.1-.9;1;071 vs. 616.1-.9;1;01','617;1;06','784-788;1;092','913-919;1;04','930-990;1;01-09']

#for ark in fileARK:
#    listeARK.append(ark.replace("\n",""))


ns = {"srw":"http://www.loc.gov/zing/srw/","m":"http://catalogue.bnf.fr/namespaces/InterXMarc","mn":"http://catalogue.bnf.fr/namespaces/motsnotices"}

def ark2nbAuteurs(ark):
    url = "http://noticesservices.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=idPerenne%20any%20%22" + ark + "%22&recordSchema=InterXMarc_Complet"
    record = etree.parse(url)
    i = 0
    for auteur in record.xpath("//m:datafield[@tag='700']|//m:datafield[@tag='100']//m:datafield[@tag='710']//m:datafield[@tag='110']", namespaces=ns):
        i = i + 1
    return i

for el in listeROC_corr:
    ark = el[6]
    nbAuteurs = ark2nbAuteurs(ark)
    el.append(str(nbAuteurs))
    results.write("\t".join(el) + "\n")
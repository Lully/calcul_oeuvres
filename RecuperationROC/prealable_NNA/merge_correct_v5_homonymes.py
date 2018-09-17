# -*- coding: utf-8 -*-

# Correction des fichiers en sortie de merge pour préciser que 2 NNA sont co-auteurs

from lxml import etree
import csv
from unidecode import unidecode

ns = {"srw":"http://www.loc.gov/zing/srw/", "m":"http://catalogue.bnf.fr/namespaces/InterXMarc","mn":"http://catalogue.bnf.fr/namespaces/motsnotices"}

filename = input("nom et chemin du fichier CSV : ")
if (filename == ""):
    filename = "D:/BNF0017855/Documents/data/Robotdonnees/Creation_oeuvres_specifications/RecuperationROC/prealable_NNA/NNA_merge_actions_suite.csv"

#filename = filename.replace("\\","/")


file_corrige = filename.replace(".csv","") + "-corrige.csv"
resultats = open(file_corrige, "w")

couplesARKNoms = []
couplesNNANNB = []


output = []

def sru2coauteurs(nna):
    url = "http://catalogueservice.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=lienAuteur+all+%22" + nna + "%22&recordSchema=InterXMarc_Complet&recordSchema=InterXMarc_Complet&maximumRecords=10"
    firstPage = etree.parse(url)
    nbResultats = int(firstPage.find("//srw:numberOfRecords",namespaces=ns).text)
    listeCoauteurs = []
    i = 1
    while (i < nbResultats):
        urlPage = url + "&startRecord=" + str(i)
        page = etree.parse(urlPage)
        #listeCoauteurs.append(urlPage)
        for coauteur in page.xpath("//m:datafield[@tag='100']/m:subfield[@code='3']",namespaces=ns):
            if (coauteur.text not in listeCoauteurs and coauteur.text != nna):
                listeCoauteurs.append(coauteur.text)
        for coauteur in page.xpath("//m:datafield[@tag='110']/m:subfield[@code='3']",namespaces=ns):
            if (coauteur.text not in listeCoauteurs and coauteur.text != nna):
                listeCoauteurs.append(coauteur.text)
        for coauteur in page.xpath("//m:datafield[@tag='700']/m:subfield[@code='3']",namespaces=ns):
            if (coauteur.text not in listeCoauteurs and coauteur.text != nna):
                listeCoauteurs.append(coauteur.text)
        for coauteur in page.xpath("//m:datafield[@tag='710']/m:subfield[@code='3']",namespaces=ns):
            if (coauteur.text not in listeCoauteurs and coauteur.text != nna):
                listeCoauteurs.append(coauteur.text)
        i = i+10
    return listeCoauteurs

def nettoyage(nom):
    resultat = nom.replace(".","")
    resultat = resultat.replace(",","")
    resultat = resultat.replace("-","")
    resultat = resultat.replace(" ","")
    resultat = resultat.replace("'","")
    resultat = resultat.lower()
    return resultat
	
def nna2nomPrenom(nna):
        nnaRecordUrl = "http://catalogueservice.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=NN%20any%20%22" + nna + "%22&recordSchema=InterXMarc_Complet"
        nnaAuthorRecord = etree.parse(nnaRecordUrl)
        nnaAuthorRecordFirstName = ""
        nnaAuthorRecordLastName = ""
        NomPrenom = []
        for field100 in nnaAuthorRecord.xpath("//m:datafield[@tag='100']",namespaces = ns):
            if (field100.find("m:subfield[@code='m']",namespaces=ns) is not None):
                nnaAuthorRecordFirstName = unidecode(field100.find("m:subfield[@code='m']",namespaces=ns).text)
            if (field100.find("m:subfield[@code='a']",namespaces=ns) is not None):
                nnaAuthorRecordLastName = unidecode(field100.find("m:subfield[@code='a']",namespaces=ns).text)
        jointureNomPrenom = ""
        if (nnaAuthorRecordFirstName != ""):
            jointureNomPrenom = ", "
        NomPrenom.append(nnaAuthorRecordLastName + jointureNomPrenom + nnaAuthorRecordFirstName)
        NomPrenom.append(nettoyage(nnaAuthorRecordLastName + jointureNomPrenom + nnaAuthorRecordFirstName))
        return NomPrenom
        



with open(filename, newline="\n", encoding='utf-8') as csvfile:
    file = csv.reader(csvfile, delimiter="\t")
    for row in file:
        #pour chaque auteur (cible ou source) on crée deux dictionnaires 
            #NNA -> Nom, Prénom
            #NNA -> co-auteurs
        nna = row[0]
        ark = row[1]        
        authorname = nna2nomPrenom(nna)[0]
        authornamenettoye = nna2nomPrenom(nna)[1]
        nnasuggereNom = ""
        nnasuggereNomnettoye = ""
        if (nna == "id de l'auteur (FRBNF)"):
            authorname = "Auteur source"
            nnasuggereNom = "Auteur Cible"
        else:
            authornamenettoye = nna2nomPrenom(nna)[1]
            nnasuggere = row[15]
            if (nnasuggere != ""):
                nnasuggereNom = nna2nomPrenom(nnasuggere)[0]
                
                nnasuggereNomnettoye = nna2nomPrenom(nnasuggere)[1]
                #print(nnasuggereNomnettoye + "\t" + authornamenettoye)
                if (authornamenettoye != nnasuggereNomnettoye and nnasuggereNomnettoye != "" and authornamenettoye != ""):
                    row[14] = row[14] + " (co-auteur)"
        row.append(authorname)
        row.append(nnasuggereNom)
        resultats.write("\t".join(row) + "\n")



# -*- coding: utf-8 -*-

# Correction des fichiers en sortie de merge pour préciser que 2 NNA sont co-auteurs

from lxml import etree
import csv

ns = {"srw":"http://www.loc.gov/zing/srw/", "m":"http://catalogue.bnf.fr/namespaces/InterXMarc","mn":"http://catalogue.bnf.fr/namespaces/motsnotices"}

filename = input("nom et chemin du fichier CSV : ")
if (filename == ""):
    filename = "D:/BNF0017855/Documents/data/Robotdonnees/Creation_oeuvres_specifications/RecuperationROC/prealable_NNA/NNA_merge_actions.csv"

#filename = filename.replace("\\","/")


file_corrige = filename.replace(".csv","") + "-corrige.csv"

couplesARKNoms = []
couplesNNANNB = []

DicAuteur2coauteurs = {}
DicArk2Nom = {}
DicNna2Nom = {}

file_DicAuteur2coauteurs = open("DicAuteur2coauteurs.txt","w")
file_DicArk2Nom = open("DicArk2Nom.txt","w")
file_DicNna2Nom = open("DicNna2Nom.txt","w")

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

def nna2nomPrenom(nna):
        nnaRecordUrl = "http://catalogueservice.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=NN%20any%20%22" + nna + "%22&recordSchema=InterXMarc_Complet"
        nnaAuthorRecord = etree.parse(nnaRecordUrl)
        nnaAuthorRecordFirstName = ""
        nnaAuthorRecordLastName = ""
        for field100 in nnaAuthorRecord.xpath("//m:datafield[@tag='100']",namespaces = ns):
            if (field100.find("m:subfield[@code='m']",namespaces=ns) is not None):
                nnaAuthorRecordFirstName = field100.find("m:subfield[@code='m']",namespaces=ns).text
            if (field100.find("m:subfield[@code='a']",namespaces=ns) is not None):
                nnaAuthorRecordLastName = field100.find("m:subfield[@code='a']",namespaces=ns).text
        jointureNomPrenom = ""
        if (nnaAuthorRecordFirstName != ""):
            jointureNomPrenom = ", "
        NomPrenom = nnaAuthorRecordLastName + jointureNomPrenom + nnaAuthorRecordFirstName
        
        return NomPrenom
        

with open(filename, newline="\n", encoding='utf-8') as csvfile:
    file = csv.reader(csvfile, delimiter="\t")
    for row in file:
        nna = row[0]
        arkAuthor = row[1]
        arkAuthorRecordUrl = "http://noticesservices.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=idPerenne%20any%20%22" + arkAuthor + "%22&recordSchema=InterXMarc_Complet"
        arkAuthorRecord = etree.parse(arkAuthorRecordUrl)
        DicArk2Nom[arkAuthor] = nna2nomPrenom(nna)
        DicNna2Nom[nna] = nna2nomPrenom(nna)
        nnannb = row[0] + row[5]
        if (nnannb not in couplesNNANNB):
            couplesNNANNB.append(nnannb)
        #Pour chaque NNA : indiquer en valeur la liste de ses co-auteurs
        DicAuteur2coauteurs[nna] = sru2coauteurs(nna)
        if (row[15] != ""):
            DicAuteur2coauteurs[row[15]] = sru2coauteurs(row[15])
            DicNna2Nom[row[15]] = nna2nomPrenom(row[15])
        output.append(row)

"""A l'issue des opérations ci-dessus, on a donc 3 listes :
1. output = le fichier en entrée, à l'identique
2. couplesARKNoms = liste des auteurs. Chaque auteur est sous la forme [ARK, NNA, "Nom, Prénom"] (liste dédoublonnée)
3. paire NNA-NNB (association auteurs-BIB) (liste dédoublonnée)

Et 3 dictionnaires
DicArk2Nom : pour chaque ARK, la valeur est "Nom, Prénom"
DicNna2Nom : pour chaque NNA, la valeur est "Nom, Prénom"
DicAuteur2coauteurs = pour chaque NNA, la valeur est une liste : la liste des co-auteurs
"""

file_DicAuteur2coauteurs.write(DicAuteur2coauteurs)
file_DicArk2Nom.write(DicArk2Nom)
file_DicNna2Nom.write(DicNna2Nom)

"""with open(file_corrige, 'w', newline="\n", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")
    for row in output:
        nna = row[0]
        ark = row[1]
        authorname = ""
        nnasuggereNom = ""
        nnb = row[5]
        if (row[0] == "id de l'auteur (FRBNF)"):
            authorname = "Auteur source"
            nnasuggereNom = "Auteur Cible"
        else:
            authorname = DicNna2Nom[nna]
            nnasuggere = row[15]
            if (nnasuggere != ""):
                nnasuggereNom = DicNna2Nom[nnasuggere]
                if (nnasuggere in DicAuteur2coauteurs[nna]):
                    row[14] = row[14] + " (co-auteur)"
        
        row.append(authorname)
        row.append(nnasuggereNom)
        writer.writerow(row)"""
#print(couplesARKNoms)

# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 14:16:08 2017

Objectif : récupérer un rapport "regroupement de manifestations en oeuvres" de RobotDonnées et signaler les cluster dont 1 des manifs a déjà une zone 144/145 ou 744/745

@author: BNF0017855
"""
import csv
from lxml import etree
from unidecode import unidecode

ns = {"srw":"http://www.loc.gov/zing/srw/", "m":"http://catalogue.bnf.fr/namespaces/InterXMarc","mn":"http://catalogue.bnf.fr/namespaces/motsnotices"}


#En entrée, le fichier CSV issu de RobotDonnées (soit de dedupe, soit de minhashing)
input_filename = input("Fichier CSV à traiter : ")
if (input_filename == ""):
    input_filename = "coteYE_run73755.csv"
filename_root = input_filename.split(".")[0]

output_sans_alignements = open(filename_root + "-oeuvres_sans_alignements_existants.csv","w")
output_1_alignement = open(filename_root + "-oeuvres_1_alignement.csv","w")
output_x_alignements = open(filename_root + "-oeuvres_x_alignements.csv","w")
#liste_oeuvres_file = open(filename_root + "-liste_oeuvres.csv","w")

liste_oeuvres = {}

def check144_145(id_manif,anlnum):
    ark = id_manif.split("#")[0]
    url = "http://noticesservices.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=idPerenne%20any%20%22" + ark + "%22&recordSchema=InterXMarc_Complet"
    #print(url)
    record = etree.parse(url)
    liste141 = []
    liste144 = []
    liste145 = []
    if (anlnum == "0"):
        for f141 in record.xpath("//srw:recordData/m:record/m:datafield[@tag='141']", namespaces=ns):
            subf3 = ""
            subfa = ""
            if (f141.find("m:subfield[@code='3']",namespaces=ns) is not None):
                subf3 = f141.find("m:subfield[@code='3']",namespaces=ns).text
            if (f141.find("m:subfield[@code='a']",namespaces=ns) is not None):
                subfa = unidecode(f141.find("m:subfield[@code='a']",namespaces=ns).text)
            liste141.append([subf3,subfa])
        for f144 in record.xpath("//srw:recordData/m:record/m:datafield[@tag='144']", namespaces=ns):
            subf3 = ""
            subfa = ""
            if (f144.find("m:subfield[@code='3']",namespaces=ns) is not None):
                subf3 = f144.find("m:subfield[@code='3']",namespaces=ns).text
            if (f144.find("m:subfield[@code='a']",namespaces=ns) is not None):
                subfa = unidecode(f144.find("m:subfield[@code='a']",namespaces=ns).text)
            liste144.append([subf3,subfa])
        for f145 in record.xpath("//srw:recordData/m:record/m:datafield[@tag='145']", namespaces=ns):
            subf3 = ""
            subfa = ""
            if (f145.find("m:subfield[@code='3']",namespaces=ns) is not None):
                subf3 = f145.find("m:subfield[@code='3']",namespaces=ns).text
            if (f145.find("m:subfield[@code='a']",namespaces=ns) is not None):
                subfa = unidecode(f145.find("m:subfield[@code='a']",namespaces=ns).text)
            liste145.append([subf3,subfa])
    else:
        anl = anlnum
        if (len(anl) == 3):
            anl = anlnum
        if (len(anl) == 2):
            anl = "0" + anlnum
        elif (len(anl) == 1):
            anl = "00" + anlnum
        path_to_anl = "//srw:recordData/m:record/m:record[@Numero='"+ anl + "']"
        #print(path_to_anl)
        path_to_141 = path_to_anl + "/m:datafield[@tag='141']"
        path_to_144 = path_to_anl + "/m:datafield[@tag='144']"
        path_to_145 = path_to_anl + "/m:datafield[@tag='145']"

        for f141 in record.xpath(path_to_141, namespaces=ns):
            subf3 = ""
            subfa = ""
            if (f141.find("m:subfield[@code='3']",namespaces=ns) is not None):
                subf3 = f141.find("m:subfield[@code='3']",namespaces=ns).text
            if (f141.find("m:subfield[@code='a']",namespaces=ns) is not None):
                subfa = unidecode(f141.find("m:subfield[@code='a']",namespaces=ns).text)
            liste141.append([subf3,subfa])
        for f144 in record.xpath(path_to_144, namespaces=ns):
            subf3 = ""
            subfa = ""
            if (f144.find("m:subfield[@code='3']",namespaces=ns) is not None):
                subf3 = f144.find("m:subfield[@code='3']",namespaces=ns).text
            if (f144.find("m:subfield[@code='a']",namespaces=ns) is not None):
                subfa = unidecode(f144.find("m:subfield[@code='a']",namespaces=ns).text)
            liste144.append([subf3,subfa])
        for f145 in record.xpath(path_to_145, namespaces=ns):
            subf3 = ""
            subfa = ""
            if (f145.find("m:subfield[@code='3']",namespaces=ns) is not None):
                subf3 = f145.find("m:subfield[@code='3']",namespaces=ns).text
            if (f145.find("m:subfield[@code='a']",namespaces=ns) is not None):
                subfa = unidecode(f145.find("m:subfield[@code='a']",namespaces=ns).text)
            liste145.append([subf3,subfa])
    return (liste141,liste144,liste145)


with open(input_filename) as csvfile:
    tableau = csv.reader(csvfile, delimiter='\t')
    colonne_clusterID = 0
    colonne_manifARK = 0
    colonne_anlnum = 0
    for row in tableau:
        if (row[0]== "id de l'auteur (FRBNF)"):
            colonne_clusterID = row.index("clusterid")
            colonne_manifARK  = row.index("id de la manifestation (ARK)")
            colonne_anlnum  = row.index("anlnum")
            output_sans_alignements.write("\t".join(row) + "\n")
            output_1_alignement.write("\t".join(row) + "\t" + "\t".join(["Champ lien","ark Oeuvre","Titre Oeuvre"]) + "\n")
            output_x_alignements.write("\t".join(row) + "\t" + "\t".join(["ARK 141","Titres 141","ARK 144","Titres 144","ARK 145","Titres 145"]) + "\n")
        else:
            clusterID = row[colonne_clusterID]
            arkManif = row[colonne_manifARK]
            anlnum = row[colonne_anlnum]
            id_manif = "#".join([arkManif,anlnum])
            if (clusterID in liste_oeuvres):
                liste_oeuvres[clusterID].append(id_manif + "~" + "\t".join(row))
            else:
                liste_oeuvres[clusterID] = [id_manif + "~" + "\t".join(row)]



for oeuvre,val in liste_oeuvres.items():
    liste141 = []
    liste144 = []
    liste145 = []
    #print(val)
    for manif in val:
        manif = manif.split("~")
        #print(manif)
        id_manif = manif[0]
        resultRobotDonnees = manif[1]
        alignements_existants = check144_145(id_manif,anlnum)
        alignements_141 = alignements_existants[0]
        alignements_144 = alignements_existants[1]
        alignements_145 = alignements_existants[2]
        for el in alignements_141:
            if (el not in liste141):
                liste141.append(el)
        for el in alignements_144:
            if (el not in liste144):
                liste144.append(el)
        for el in alignements_145:
            if (el not in liste145):
                liste145.append(el)
    if (len(liste141) == 0 and len(liste144) == 0 and len(liste145) == 0):
        """print (oeuvre + " : 0 alignement")
        print ("liste144 : " + str(liste144))
        print ("liste145 : " + str(liste145))"""
        for manif in val:
            manif = manif.split("~")
            output_sans_alignements.write(manif[1] + "\n")
    elif (len(liste141) == 1 or len(liste144) == 1 or len(liste145) == 1):
        field = ""
        arkOeuvre = ""
        titreOeuvre = ""
        if (len(liste141) == 1):
            field = "144"
            arkOeuvre = liste141[0][0]
            titreOeuvre = liste141[0][1]
        if (len(liste144) == 1):
            field = "144"
            arkOeuvre = liste144[0][0]
            titreOeuvre = liste144[0][1]
        if (len(liste145) == 1):
            field = "145"
            arkOeuvre = liste145[0][0]
            titreOeuvre = liste145[0][1]
        #print (oeuvre + " : 1 alignement\n")
        for manif in val:
            manif = manif.split("~")
            output_1_alignement.write(manif[1] + "\t" + field + "\t" + arkOeuvre + "\t" + titreOeuvre + "\n")
    else:
        #print (oeuvre + " : plusieurs alignements\n")
        listeIDoeuvres141 = []
        listeTitresOeuvres141 = []
        listeIDoeuvres144 = []
        listeTitresOeuvres144 = []
        listeIDoeuvres145 = []
        listeTitresOeuvres145 = []
        for el in liste141:
            listeIDoeuvres141.append(el[0])
            listeTitresOeuvres141.append(el[1])
        for el in liste144:
            listeIDoeuvres144.append(el[0])
            listeTitresOeuvres144.append(el[1])
        for el in liste145:
            listeIDoeuvres145.append(el[0])
            listeTitresOeuvres145.append(el[1])
        for manif in val:
            manif = manif.split("~")
            output_x_alignements.write(manif[1] + "\t" + ",".join(listeIDoeuvres141) + "\t" + " | ".join(listeTitresOeuvres141) + "\t" + ",".join(listeIDoeuvres144) + "\t" + " | ".join(listeTitresOeuvres144) + "\t" + ",".join(listeIDoeuvres145) + "\t" + " | ".join(listeTitresOeuvres145) + "\n")
                        
            
#liste_oeuvres_file.write(str(liste_oeuvres))
        
output_sans_alignements.close()
output_1_alignement.close()
output_x_alignements.close()
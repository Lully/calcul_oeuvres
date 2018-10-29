# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 14:16:08 2017

Objectif : récupérer un rapport "regroupement de manifestations en oeuvres" de RobotDonnées et signaler les cluster dont 1 des manifs a déjà une zone 144/145 ou 744/745

@author: BNF0017855
"""
import csv
from urllib import request
from lxml import etree
import urllib.error as error
from unidecode import unidecode
from collections import defaultdict
import http.client

ns = {"srw":"http://www.loc.gov/zing/srw/", "m":"http://catalogue.bnf.fr/namespaces/InterXMarc","mn":"http://catalogue.bnf.fr/namespaces/motsnotices"}


#En entrée, le fichier CSV issu de RobotDonnées (soit de dedupe, soit de minhashing)
#liste_oeuvres_file = open(filename_root + "-liste_oeuvres.csv","w")
url_access_pbs = []

#Variables globales pour la vérification des liens en 14X



def testURLetreeParse(url):
    test = True
    resultat = ""
    try:
        resultat = etree.parse(request.urlopen(url))
    except OSError as err:
        print(url)
        print(err)
        test = False
    except etree.XMLSyntaxError as err:
        print(url)
        print(err)
        url_access_pbs.append([url,"etree.XMLSyntaxError"])
        test = False
    except etree.ParseError as err:
        print(url)
        print(err)
        test = False
        url_access_pbs.append([url,"etree.ParseError"])
    except error.URLError as err:
        print(url)
        print(err)
        test = False
        url_access_pbs.append([url,"urllib.error.URLError"])
    except ConnectionResetError as err:
        print(url)
        print(err)
        test = False
        url_access_pbs.append([url,"ConnectionResetError"])
    except TimeoutError as err:
        print(url)
        print(err)
        test = False
        url_access_pbs.append([url,"TimeoutError"])
    except http.client.RemoteDisconnected as err:
        print(url)
        print(err)
        test = False
        url_access_pbs.append([url,"http.client.RemoteDisconnected"])
    except http.client.BadStatusLine as err:
        print(url)
        print(err)
        test = False
        url_access_pbs.append([url,"http.client.BadStatusLine"])
    except ConnectionAbortedError as err:
        print(url)
        print(err)
        test = False
        url_access_pbs.append([url,"ConnectionAbortedError"])
    return (test,resultat)

def check144_145(id_manif):
    (ark,anlnum) = (id_manif.split("#")[0],id_manif.split("#")[1])
    url = "http://noticesservices.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=idPerenne%20any%20%22" + ark + "%22&recordSchema=InterXMarc_Complet"
    #print(url)
    (test,record) = testURLetreeParse(url)
    liste141 = []
    liste144 = []
    liste145 = []
    liste741 = []
    liste745 = []
    liste744 = []
    if (anlnum == "0" and test == True):
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
            liste145.append([subf3, subfa])
        for f741 in record.xpath("//srw:recordData/m:record/m:datafield[@tag='741']", namespaces=ns):
            subf3 = ""
            subfa = ""
            if (f741.find("m:subfield[@code='3']",namespaces=ns) is not None):
                subf3 = f741.find("m:subfield[@code='3']",namespaces=ns).text
            if (f741.find("m:subfield[@code='a']",namespaces=ns) is not None):
                subfa = unidecode(f741.find("m:subfield[@code='a']",namespaces=ns).text)
            liste741.append([subf3,subfa])
        for f744 in record.xpath("//srw:recordData/m:record/m:datafield[@tag='744']", namespaces=ns):
            subf3 = ""
            subfa = ""
            if (f744.find("m:subfield[@code='3']",namespaces=ns) is not None):
                subf3 = f744.find("m:subfield[@code='3']",namespaces=ns).text
            if (f744.find("m:subfield[@code='a']",namespaces=ns) is not None):
                subfa = unidecode(f744.find("m:subfield[@code='a']",namespaces=ns).text)
            liste744.append([subf3,subfa])
        for f745 in record.xpath("//srw:recordData/m:record/m:datafield[@tag='745']", namespaces=ns):
            subf3 = ""
            subfa = ""
            if (f745.find("m:subfield[@code='3']",namespaces=ns) is not None):
                subf3 = f745.find("m:subfield[@code='3']",namespaces=ns).text
            if (f745.find("m:subfield[@code='a']",namespaces=ns) is not None):
                subfa = unidecode(f745.find("m:subfield[@code='a']",namespaces=ns).text)
            liste745.append([subf3,subfa])
    elif (anlnum != "0" and test == True):
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
        path_to_741 = path_to_anl + "/m:datafield[@tag='741']"
        path_to_744 = path_to_anl + "/m:datafield[@tag='744']"
        path_to_745 = path_to_anl + "/m:datafield[@tag='745']"
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
            liste145.append([subf3, subfa])
        for f741 in record.xpath(path_to_741, namespaces=ns):
            subf3 = ""
            subfa = ""
            if (f741.find("m:subfield[@code='3']",namespaces=ns) is not None):
                subf3 = f741.find("m:subfield[@code='3']",namespaces=ns).text
            if (f741.find("m:subfield[@code='a']",namespaces=ns) is not None):
                subfa = unidecode(f741.find("m:subfield[@code='a']",namespaces=ns).text)
            liste741.append([subf3,subfa])
        for f744 in record.xpath(path_to_744, namespaces=ns):
            subf3 = ""
            subfa = ""
            if (f744.find("m:subfield[@code='3']",namespaces=ns) is not None):
                subf3 = f744.find("m:subfield[@code='3']",namespaces=ns).text
            if (f744.find("m:subfield[@code='a']",namespaces=ns) is not None):
                subfa = unidecode(f744.find("m:subfield[@code='a']",namespaces=ns).text)
            liste744.append([subf3,subfa])
        for f745 in record.xpath(path_to_745, namespaces=ns):
            subf3 = ""
            subfa = ""
            if (f745.find("m:subfield[@code='3']",namespaces=ns) is not None):
                subf3 = f745.find("m:subfield[@code='3']",namespaces=ns).text
            if (f745.find("m:subfield[@code='a']",namespaces=ns) is not None):
                subfa = unidecode(f745.find("m:subfield[@code='a']",namespaces=ns).text)
            liste745.append([subf3,subfa])
    print(id_manif,liste145)
    return (liste141,liste144,liste145,liste741,liste744,liste745)

def file2check14X(input_filename,output_reports):
    liste_oeuvres = {}
    with open(input_filename, encoding="utf-8") as csvfile:
        i = 0
        tableau = csv.reader(csvfile, delimiter='\t')
        colonne_clusterID = 0
        colonne_manifARK = 0
        colonne_anlnum = 0
        for row in tableau:
            for el in row:
                if (i == 0):
                    i += 1
                    colonne_clusterID = row.index("clusterid")
                    colonne_manifARK  = row.index("id de la manifestation (ARK)")
                    colonne_anlnum  = row.index("anlnum")
                    colonne_type_notice = row.index("Type de notice")
                    output_reports["liste_files"]["output_sans_alignement"].write("\t".join(row) + "\n")
                    output_reports["liste_files"]["output_1_alignement"].write("\t".join(row) + "\t" + "\t".join(["Champ lien","ark Oeuvre","Titre Oeuvre"]) + "\n")
                    output_reports["liste_files"]["output_x_alignements"].write("\t".join(row) + "\t" + "\t".join(["ARK 141","Titres 141","ARK 144","Titres 144","ARK 145","Titres 145","ARK 744","Titres 744","ARK 745","Titres 745"]) + "\n")
                else:
                    #print(colonne_clusterID, colonne_manifARK)
                    clusterID = row[colonne_clusterID]
                    arkManif = row[colonne_manifARK]
                    print(arkManif)
                    anlnum = row[colonne_anlnum]
                    if (row[colonne_type_notice] == "m"):
                        anlnum = "0"
                    id_manif = "#".join([arkManif,anlnum])
                    if (clusterID in liste_oeuvres):
                        liste_oeuvres[clusterID].append(id_manif + "¤" + "\t".join(row))
                    else:
                        liste_oeuvres[clusterID] = [id_manif + "¤" + "\t".join(row)]
    return liste_oeuvres



def liste_dedup(manifid, manif_liens):
    liens = []
    for el in manif_liens[manifid]:
        if (len(el) > 0):
            for lien in el:
                if (lien[0] not in liens):
                    liens.append(lien[0])
    liens = " ".join(liens)
    
    return liens

def check_oeuvres(output_reports,liste_oeuvres):
    manif_liens = defaultdict(list)
    for oeuvre,val in liste_oeuvres.items():
        print(oeuvre)
        liste141 = []
        liste144 = []
        liste145 = []
        liste744 = []
        liste745 = []
        #print(val)
        for manif in val:
            manif = manif.split("¤")
            #print(manif)
            id_manif = manif[0]
            resultRobotDonnees = manif[1]
            alignements_existants = check144_145(id_manif)
            alignements_141 = alignements_existants[0]
            alignements_144 = alignements_existants[1]
            alignements_145 = alignements_existants[2]
            alignements_744 = alignements_existants[3]
            alignements_745 = alignements_existants[4]
            manif_liens[id_manif] = [alignements_141,alignements_144,alignements_145,alignements_744,alignements_745]
            for el in alignements_141:
                if (el not in liste141):
                    liste141.append(el)
            for el in alignements_144:
                if (el not in liste144):
                    liste144.append(el)
            for el in alignements_145:
                if (el not in liste145):
                    liste145.append(el)
            for el in alignements_744:
                if (el not in liste744):
                    liste744.append(el)
            for el in alignements_745:
                if (el not in liste745):
                    liste745.append(el)
        
        if (len(liste141)+len(liste144)+len(liste145)+len(liste744)+len(liste745) == 0):
            #print("000",oeuvre,  liste141,liste144,liste145,liste744,liste745)
            """print (oeuvre + " : 0 alignement")
            print ("liste144 : " + str(liste144))
            print ("liste145 : " + str(liste145))"""
            for manif in val:
                manif = manif.split("¤")
                output_reports["liste_files"]["output_sans_alignement"].write(manif[1] + "\n")
        elif (len(liste141)+len(liste144)+len(liste145)+len(liste744)+len(liste745) == 1):
            #print("1",oeuvre,  liste141,liste144,liste145,liste744,liste745)
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
            if (len(liste744) == 1):
                field = "744"
                arkOeuvre = liste744[0][0]
                titreOeuvre = liste744[0][1]
            if (len(liste745) == 1):
                field = "745"
                arkOeuvre = liste745[0][0]
                titreOeuvre = liste745[0][1]
            #print (oeuvre + " : 1 alignement\n")
            for manif in val:
                [manifid,manifval] = manif.split("¤")
                liens_manif = liste_dedup(manifid,manif_liens)
                output_reports["liste_files"]["output_1_alignement"].write(manifval + "\t" + field + "\t" + liens_manif + "\t" + titreOeuvre + "\n")
        else:
            #print("x",oeuvre,  liste141,liste144,liste145,liste744,liste745)
            #print (oeuvre + " : plusieurs alignements\n")
            listeIDoeuvres141 = []
            listeTitresOeuvres141 = []
            listeIDoeuvres144 = []
            listeTitresOeuvres144 = []
            listeIDoeuvres145 = []
            listeTitresOeuvres145 = []
            listeIDoeuvres744 = []
            listeTitresOeuvres744 = []
            listeIDoeuvres745 = []
            listeTitresOeuvres745 = []
            for el in liste141:
                listeIDoeuvres141.append(el[0])
                listeTitresOeuvres141.append(el[1])
            for el in liste144:
                listeIDoeuvres144.append(el[0])
                listeTitresOeuvres144.append(el[1])
            for el in liste145:
                listeIDoeuvres145.append(el[0])
                listeTitresOeuvres145.append(el[1])
            for el in liste744:
                listeIDoeuvres744.append(el[0])
                listeTitresOeuvres744.append(el[1])
            for el in liste745:
                listeIDoeuvres745.append(el[0])
                listeTitresOeuvres745.append(el[1])
            for manif in val:
                manif = manif.split("¤")
                output_reports["liste_files"]["output_x_alignements"].write(manif[1] 
                + "\t" + ",".join(listeIDoeuvres141) 
                + "\t" + " | ".join(listeTitresOeuvres141) 
                + "\t" + ",".join(listeIDoeuvres144) 
                + "\t" + " | ".join(listeTitresOeuvres144) 
                + "\t" + ",".join(listeIDoeuvres145) 
                + "\t" + " | ".join(listeTitresOeuvres145) 
                + "\t" + ",".join(listeIDoeuvres744) 
                + "\t" + " | ".join(listeTitresOeuvres744) 
                + "\t" + ",".join(listeIDoeuvres745) 
                + "\t" + " | ".join(listeTitresOeuvres745) 
                + "\n")
    
                        

def filename2outputfiles_14X(input_filename):
    filename_root = input_filename.split(".")[0]
    output_sans_alignement_name = filename_root + "-oeuvres_sans_alignements_existants.csv"
    output_1_alignement_name = filename_root + "-oeuvres_1_alignement.csv"
    output_x_alignements_name = filename_root + "-oeuvres_x_alignements.csv"
    output_sans_alignement = open(output_sans_alignement_name, "w", encoding="utf-8")
    output_1_alignement = open(output_1_alignement_name, "w", encoding="utf-8")
    output_x_alignements = open(output_x_alignements_name, "w", encoding="utf-8")
    dic_files = {"output_sans_alignement_name":output_sans_alignement_name,
                 "liste_files":{
                 "output_sans_alignement":output_sans_alignement,
                 "output_1_alignement":output_1_alignement,
                 "output_x_alignements":output_x_alignements
                 }
            }
    return dic_files


if __name__ == "__main__":
    input_filename = input("Fichier CSV à traiter : ")
    if (input_filename == ""):
        input_filename = "coteYE_run73755.csv"
    output_reports = filename2outputfiles_14X(input_filename)
    liste_oeuvres = file2check14X(input_filename,output_reports)
    check_oeuvres(output_reports, liste_oeuvres)
    for output_file in output_reports["liste_files"]:
        output_reports["liste_files"][output_file].close()
    
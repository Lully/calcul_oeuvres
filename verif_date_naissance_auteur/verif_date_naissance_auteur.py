# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 14:53:08 2018

@author: BNF0017855
"""

import csv
from lxml import etree

ns = {"srw":"http://www.loc.gov/zing/srw/", "mxc":"info:lc/xmlns/marcxchange-v2", "m":"http://catalogue.bnf.fr/namespaces/InterXMarc","mn":"http://catalogue.bnf.fr/namespaces/motsnotices"}


output_OK = open("listeNNA_ROC_OK_2.txt","w",encoding="utf-8")
output_pb = open("listeNNA_ROC_pb_2.txt","w",encoding="utf-8")
output_incertains_18e = open("listeNNA_ROC_incertains_nes_18e_2.txt","w",encoding="utf-8")
output_incertains_dates_publis_XX = open("listeNNA_ROC_incertains_dates_publis_XXe_siecle_2.txt","w",encoding="utf-8")
output_incertains_dates_publis_not_XX = open("listeNNA_ROC_incertains_dates_publis_not_XXe_siecle_2.txt","w",encoding="utf-8")

output_OK.write("\t".join(["NNA", "Date de naissance"]) + "\n")
output_pb.write("\t".join(["NNA", "Date de naissance"]) + "\n")

#output_incertains_18e.write("\t".join(["NNA", "Date de naissance","Dates des publications"]) + "\n")
output_incertains_dates_publis_XX.write("\t".join(["NNA","Date de naissance","Dates des publications"]) + "\n")
output_incertains_dates_publis_not_XX.write("\t".join(["NNA","Date de naissance","Dates des publications"]) + "\n")

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def nna2dates(nna):
    dates = []
    url = "http://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.author2bib%20all%20%22" + nna + "%22&recordSchema=intermarcxchange&maximumRecords=1000&startRecord=1"
    resultats = etree.parse(url)
    XXe = True
    for record in resultats.xpath("//srw:recordData/mxc:record",namespaces=ns):
        date = record.find("mxc:controlfield[@tag='008']",namespaces=ns).text[8:12]
        print("     " + date)
        if (RepresentsInt(date)):
            dates.append(date)
            if (int(date) < 1900):
                XXe = False
        elif (RepresentsInt(date[0:3])):
            dates.append(date[0:3]+"0")
            if (int(date[0:3]) < 190):
                XXe = False
        elif (RepresentsInt(date[0:2])):
            dates.append(date[0:2]+"00")
            if (int(date[0:2]) < 19):
                XXe = False
    return (dates,XXe)

with open("listeNNA_ROC.txt", newline='\n',encoding="utf-8") as csvfile:
#with open("listeNNA_test.txt", newline='\n',encoding="utf-8") as csvfile:
        entry_file = csv.reader(csvfile, delimiter='\t')
        for row in entry_file:
            nna = row[0]
            
            url = "http://catalogueservice.bnf.fr/SRU?version=1.2&operation=searchRetrieve&query=NN%20any%20" + nna + "&recordSchema=InterXMarc_Complet"
            noticeAUT = etree.parse(url)
            for rec in noticeAUT.xpath("//m:controlfield[@tag='008']",namespaces=ns):
                datenaissance = rec.text[28:32]
                siecle = datenaissance[0:2]
                decennie = datenaissance[0:3]
                print(nna, datenaissance)
                if (datenaissance == "    "):
                    (liste_dates_publications,test_XXe) = nna2dates(nna)
                    if (test_XXe == True):
                        output_incertains_dates_publis_XX.write(nna + "\t" + datenaissance + "\t" +  " ".join(liste_dates_publications) + "\n")
                    else:
                        output_incertains_dates_publis_not_XX.write(nna + "\t" + datenaissance + "\t" + " ".join(liste_dates_publications) + "\n")
                if (RepresentsInt(decennie)):
                    if (int(decennie) > 187):
                        output_OK.write(nna + "\t" + datenaissance + "\n")
                    elif(int(decennie) < 188):
                        output_pb.write(nna + "\t" + datenaissance + "\n")
                elif(RepresentsInt(siecle)):
                    if (int(siecle) > 18):
                        output_OK.write(nna + "\t" + datenaissance + "\n")
                    elif(int(siecle) < 18):
                        output_pb.write(nna + "\t" + datenaissance + "\n")
                    elif(int(siecle) == 18):
                        (liste_dates_publications,test_XXe) = nna2dates(nna)
                        output_incertains_dates_publis_XX.write(nna + "\t" +  datenaissance + "\t" + " ".join(liste_dates_publications) + "\n")
                else:
                    (liste_dates_publications,test_XXe) = nna2dates(nna)
                    if (test_XXe == True):
                        output_incertains_dates_publis_XX.write(nna + "\t" + " ".join(liste_dates_publications) + "\n")
                    else:
                        output_incertains_dates_publis_not_XX.write(nna + "\t" + " ".join(liste_dates_publications) + "\n")
output_OK.close()
output_pb.close()
output_incertains_18e.close()
output_incertains_dates_publis_XX.close()
output_incertains_dates_publis_not_XX.close()
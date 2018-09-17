# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 16:38:41 2018

@author: BNF0017855

Programme qui inclut en 2 étapes :
    1. la vérification des liens 144, 145 dans les clusters
    2. pour les clusters sans lien, la distinction entre clusters contenant des agrégats et les autres
"""

import csv
import check144_145
import check_clusters_agregats_et_750
from collections import defaultdict


def one_file(input_filename):
    #Première étape : vérification des liens
    check14X_output_reports = check144_145.filename2outputfiles_14X(input_filename)
    liste_oeuvres = check144_145.file2check14X(input_filename, check14X_output_reports)
    check144_145.check_oeuvres(check14X_output_reports,liste_oeuvres)
    clusters_sans_14X_filename = check14X_output_reports["output_sans_alignement_name"]
    for output_file in check14X_output_reports["liste_files"]:
        check14X_output_reports["liste_files"][output_file].close()
    
    #2e étape : pour les clusters sans liens, distinction avec agrégats / sans agrégats        
    liste_reports = check_clusters_agregats_et_750.filename2outputfiles(clusters_sans_14X_filename)
    clusters = check_clusters_agregats_et_750.filename2check_agregats(clusters_sans_14X_filename,liste_reports)
    (i,j,k) = check_clusters_agregats_et_750.analyse_clusters(liste_reports,clusters)
    check_clusters_agregats_et_750.EOT(i,j,k,liste_reports)
    
if __name__ == "__main__":
    input_filename = input("Nom du fichier CSV à analyser (en sortie de minhashing + ajout des anlnum)\nou plusieurs fichies séparés par des \";\"\n")
    for filename in input_filename.split(";"):
        one_file(filename)
    
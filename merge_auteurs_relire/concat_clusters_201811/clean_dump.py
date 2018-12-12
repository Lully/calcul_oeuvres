# coding: utf-8

from itertools import zip_longest

from stdf import create_file

i = 0

errors_file = create_file("errors_file.txt")

liste_files = ['lot1_alb_clusters_dedupe.txt',
    'lot1_dnm_clusters_dedupe.txt',
    'lot1_gv_clusters_dedupe.txt',
    'lot1_jh_clusters_dedupe.txt',
    'lot2-oeuvres_sans_alignements_existants-clusters_sans_agregats.txt',
    'lot3_clusters_sans_alignement_sans_agregats_pour_dedupe.txt',
    'lot4_minhashing-oeuvres_sans_alignements_existants-clusters_sans_agregats-dedupe.txt',
    'lot5_minhashing-oeuvres_sans_alignements_existants-clusters_sans_agregats-dedupe.txt',
    'lot6-oeuvres_sans_alignements_existants-clusters_sans_agregats-dedupe.txt']

liste_files = ["tous_clusters_dedupe.txt"]
liste_files = ["tous_clusters_dedupe-nett-100000.txt",
    "tous_clusters_dedupe-nett-1000000.txt",
    "tous_clusters_dedupe-nett-1100000.txt",
    "tous_clusters_dedupe-nett-1200000.txt",
    "tous_clusters_dedupe-nett-1300000.txt",
    "tous_clusters_dedupe-nett-1400000.txt",
    "tous_clusters_dedupe-nett-1500000.txt",
    "tous_clusters_dedupe-nett-1600000.txt",
    "tous_clusters_dedupe-nett-1700000.txt",
    "tous_clusters_dedupe-nett-1800000.txt",
    "tous_clusters_dedupe-nett-1900000.txt",
    "tous_clusters_dedupe-nett-200000.txt",
    "tous_clusters_dedupe-nett-300000.txt",
    "tous_clusters_dedupe-nett-400000.txt",
    "tous_clusters_dedupe-nett-500000.txt",
    "tous_clusters_dedupe-nett-600000.txt",
    "tous_clusters_dedupe-nett-700000.txt",
    "tous_clusters_dedupe-nett-800000.txt",
    "tous_clusters_dedupe-nett-900000.txt"]

for filename in liste_files:
    with open(filename, encoding="utf-8") as file:
        i = 0
        output_file = create_file(f"{filename[:-4]}-corr_cols.txt")
        for row in file:
            row = row.replace("\r", "").replace("\n", "")
            nb_cols = len(row.split("\t"))
            row += "\t"*(17-nb_cols) + "\n"
            output_file.write(row)
            i += 1
            print(filename, i)


def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)


n = 100000
"""
for filename in liste_files:
    with open(filename, encoding="utf-8") as f:
        for i, g in enumerate(grouper(n, f, fillvalue=''), 1):
            with open(f"{filename[0:-4]}-{i*n}.txt", "w", encoding="utf-8") as fout:
                fout.write("\t".join(["pep_cluster_id", "id de l'auteur (FRBNF)",
                                      "id de l'auteur (ARK)", "clusterid", "clusternum",
                                      "Titre de l'oeuvre", "id de la manifestation (FRBNF)",
                                      "id de la manifestation (ARK)", "Titre original",
                                      "Titre Manifestation", "Type de notice",
                                      "Type de document", "zones", "methode",
                                      "date", "anlnum"]) + "\n")
                fout.writelines(g)"""
            

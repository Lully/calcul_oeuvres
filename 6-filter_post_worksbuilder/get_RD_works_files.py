# coding: utf-8
"""
Programme de récupération en masse des fichiers ZIP
produits par RobotDonnées / WorksBuilder
"""


import urllib.request


def get_zip_file(run_number, directory):
    url = "http://robotdonnees.bnf.fr/workszip/" + run_number
    filename = directory + run_number + ".zip"
    print(url, filename)
    try:
        urllib.request.urlretrieve(url, filename)
    except FileNotFoundError as err:
        print(run_number, " : ", str(err))


if __name__ == "__main__":
    runs_list = input("Liste des numéros de runs WorksBuilder à récupérer : ")
    directory = input("Dossier où les déposer : ")
    if ("/" in directory and directory[-1] != "/"):
        directory += "/"
    elif ("\\" in directory and directory[-1] != "\\"):
        directory += "\\"
    elif (directory[-1] != "/"):
        directory += "/"
    for run_number in runs_list.split(";"):
        get_zip_file(run_number, directory)
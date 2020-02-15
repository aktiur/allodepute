import csv
from collections import namedtuple
from pathlib import Path


Departement = namedtuple(
    "Departement", ["code", "nom", "avec_article", "avec_charniere"]
)

with open(Path(__file__).parent / "departements.csv") as file:
    _departements = [(d["id"], d["nom"], int(d["tncc"])) for d in csv.DictReader(file)]


# CF : https://www.insee.fr/fr/information/2114773
articles = [
    "",  # pas d'article et le nom commence par une consonne sauf H muet.
    "",  # pas d'article et le nom commence par une voyelle ou un H muet.
    "le ",
    "la ",
    "les ",
    "l'",
    "aux ",
    "las ",
    "los ",
]

charnieres = [
    "de ",
    "d'",
    "du ",
    "de la ",
    "des ",
    "de l'",
    "des ",
    "de las ",
    "de los ",
]

departements = {
    code: Departement(code, nom, f"{articles[tncc]}{nom}", f"{charnieres[tncc]}{nom}")
    for code, nom, tncc in _departements
}

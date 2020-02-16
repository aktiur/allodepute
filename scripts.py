import csv
import json
from pathlib import Path

import requests
from phonenumber_field.phonenumber import PhoneNumber

SEPARATOR = "|"

TYPE = "@xsi:type"

TYPE_ADDRESSES = {
    "email": "AdresseMail_Type",
    "telephone": "AdresseTelephonique_Type",
    "rs": "AdresseSiteWeb_Type",
}


def telecharger(url, path):
    res = requests.get(url)
    with path.open("wb") as fd:
        fd.write(res.content)


def extraire_organes(dir, type):
    files = dir.glob("PO*.json")

    for f in files:
        with f.open() as fd:
            content = json.load(fd)["organe"]

        if content["codeType"] == type:
            yield content


def correspondances_groupes(dir):
    return {
        "groupes": {
            groupe["uid"]: groupe["libelleAbrege"]
            for groupe in extraire_organes(dir, "GP")
        }
    }


def correspondances_partis(dir):
    return {
        "partis": {
            parti["uid"]: parti["libelleAbrev"]
            for parti in extraire_organes(dir, "PARPOL")
        }
    }


def masser_fichier_deputes(dir: Path, dest: Path, corr_groupes, corr_partis):
    files = list(dir.glob("PA*.json"))

    with dest.open("w") as fd_out:
        w = csv.DictWriter(
            fd_out,
            fieldnames=[
                "code",
                "nom",
                "prenom",
                "groupe",
                "parti",
                "emails",
                "telephones",
                "twitter",
                "facebook",
                "departement",
                "circo",
            ],
        )
        w.writeheader()

        for file in files:
            code = file.stem
            with file.open() as f:
                content = json.load(f)["acteur"]

            mandat = next(
                m
                for m in content["mandats"]["mandat"]
                if m[TYPE] == "MandatParlementaire_type"
                and m["infosQualite"]["codeQualite"] == "membre"
            )

            if mandat["dateFin"] is not None:
                pass

            ident = content["etatCivil"]["ident"]

            nom = ident["nom"]
            prenom = ident["prenom"]

            adresses = content["adresses"]["adresse"]

            if not isinstance(adresses, list):
                adresses = [adresses]

            emails = "|".join(
                a["valElec"] for a in adresses if a[TYPE] == TYPE_ADDRESSES["email"]
            )

            telephones = "|".join(
                PhoneNumber.from_string(a["valElec"], region="FR").as_e164
                for a in adresses
                if a[TYPE] == TYPE_ADDRESSES["telephone"]
            )

            twitter = "|".join(
                a["valElec"].strip("@")
                for a in adresses
                if a[TYPE] == TYPE_ADDRESSES["rs"] and a["typeLibelle"] == "Twitter"
            )

            facebook = "|".join(
                a["valElec"]
                for a in adresses
                if a[TYPE] == TYPE_ADDRESSES["rs"] and a["typeLibelle"] == "Facebook"
            )

            groupe = next(
                corr_groupes[m["organes"]["organeRef"]]
                for m in content["mandats"]["mandat"]
                if m["typeOrgane"] == "GP" and m["dateFin"] is None
            )

            try:
                parti = next(
                    corr_partis[m["organes"]["organeRef"]]
                    for m in content["mandats"]["mandat"]
                    if m["typeOrgane"] == "PARPOL" and m["dateFin"] is None
                )
            except StopIteration:
                parti = None

            info_circo = mandat["election"]["lieu"]

            w.writerow(
                {
                    "code": code,
                    "nom": nom,
                    "prenom": prenom,
                    "groupe": groupe,
                    "parti": parti,
                    "emails": emails,
                    "telephones": telephones,
                    "twitter": twitter,
                    "facebook": facebook,
                    "departement": info_circo["numDepartement"],
                    "circo": info_circo["numCirco"],
                }
            )

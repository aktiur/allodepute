import argparse
import json
from pathlib import Path

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand
from phonenumber_field.phonenumber import PhoneNumber

from ...models import Circonscription, Depute

TYPE = "@xsi:type"

TYPE_ADDRESSES = {
    "email": "AdresseMail_Type",
    "telephone": "AdresseTelephonique_Type",
    "rs": "AdresseSiteWeb_Type",
}

GROUPES = {
    "PO730970": "MODEM",
    "PO759900": "LT",
    "PO730958": "LFI",
    "PO758835": "SOC",
    "PO767217": "UAI",
    "PO730964": "LREM",
    "PO730934": "LR",
    "PO730940": "GDR",
    "PO723569": "NI",
}


def path(p):
    return Path(p)


class Command(BaseCommand):
    help = "Importe les députés"

    def add_arguments(self, parser):
        parser.add_argument(
            "-d",
            "--dir",
            type=path,
            default=Path(settings.BASE_DIR).parent / "data" / "deputes",
        )

    def handle(self, *args, dir, **options):
        files = list(dir.glob("*.json"))

        for file in files:
            try:
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

                emails = [
                    a["valElec"] for a in adresses if a[TYPE] == TYPE_ADDRESSES["email"]
                ]
                telephones = [
                    PhoneNumber.from_string(a["valElec"], region="FR")
                    for a in adresses
                    if a[TYPE] == TYPE_ADDRESSES["telephone"]
                ]

                twitter = [
                    a["valElec"]
                    for a in adresses
                    if a[TYPE] == TYPE_ADDRESSES["rs"] and a["typeLibelle"] == "Twitter"
                ]
                if len(twitter) > 1:
                    print("longer twitter !")
                twitter = twitter[0] if twitter else ""

                facebook = [
                    a["valElec"]
                    for a in adresses
                    if a[TYPE] == TYPE_ADDRESSES["rs"]
                    and a["typeLibelle"] == "Facebook"
                ]
                if len(facebook) > 1:
                    print("longer facebook !")
                facebook = facebook[0] if facebook else ""

                groupe = next(
                    m["organes"]["organeRef"]
                    for m in content["mandats"]["mandat"]
                    if m["typeOrgane"] == "GP"
                )

                info_circo = mandat["election"]["lieu"]

                circo = Circonscription.objects.get(
                    departement=info_circo["numDepartement"],
                    numero=int(info_circo["numCirco"]),
                )

                Depute.objects.update_or_create(
                    code=code,
                    defaults={
                        "nom": nom,
                        "prenom": prenom,
                        "emails": emails,
                        "telephones": telephones,
                        "twitter": twitter,
                        "facebook": facebook,
                        "groupe": GROUPES[groupe],
                        "circonscription": circo,
                    },
                )
            except Circonscription.DoesNotExist:
                print(f"Circo absente : {info_circo}")
            except Exception:
                print(json.dumps(content, indent=2))
                raise

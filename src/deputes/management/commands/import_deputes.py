import pandas as pd
import argparse

from django.core.management.base import BaseCommand

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


class Command(BaseCommand):
    help = "Importe les députés"

    def add_arguments(self, parser):
        parser.add_argument("-s", "--source", type=argparse.FileType("r"))

    def handle(self, *args, source, **options):
        df = pd.read_csv(source, dtype={"departement": str, "telephones": str})
        df = df.fillna("")

        for depute in df.itertuples():
            Depute.objects.update_or_create(
                code=depute.code,
                defaults={
                    "nom": depute.nom,
                    "prenom": depute.prenom,
                    "emails": depute.emails.split("|"),
                    "telephones": depute.telephones.split("|"),
                    "twitter": depute.twitter,
                    "facebook": depute.facebook,
                    "groupe": depute.groupe,
                    "circonscription": Circonscription.objects.get(
                        departement=depute.departement, numero=depute.circo
                    ),
                },
            )

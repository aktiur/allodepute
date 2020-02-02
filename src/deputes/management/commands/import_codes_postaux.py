import argparse

import pandas as pd
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand

from ...models import CodePostal


class Command(BaseCommand):
    help = "Importe les codes postaux"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s", "--source", type=argparse.FileType(mode="r"),
        )

    def handle(self, *args, source, **options):
        df = pd.read_csv(
            source, sep=";", dtype={"Code_commune_INSEE": str, "Code_postal": str}
        ).rename(
            columns={
                "Code_commune_INSEE": "insee",
                "Code_postal": "zip",
                "Nom_commune": "nom",
                "coordonnees_gps": "coords",
            }
        )
        coords = df.coords.str.split(",", expand=True)
        for c in coords:
            coords[c] = coords[c].map(float)
        df[["lat", "long"]] = coords

        df = df.reindex(
            columns=["insee", "zip", "nom", "lat", "long"]
        ).drop_duplicates()

        res = df.groupby(["zip"]).agg(
            {"lat": "mean", "long": "mean", "nom": lambda g: list(g.sort_values())}
        )

        for code_postal in res.itertuples():
            if pd.isna(code_postal.long):
                loc = None
            else:
                loc = Point(x=code_postal.long, y=code_postal.lat)

            CodePostal.objects.update_or_create(
                code=code_postal.Index,
                defaults={"centroid": loc, "communes": code_postal.nom},
            )

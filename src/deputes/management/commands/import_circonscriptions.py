import argparse
import json

from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from ...models import Circonscription


CORRESPONDANCES = {
    "ZA": "971",
    "ZB": "972",
    "ZC": "973",
    "ZD": "974",
    "ZM": "976",
    "ZN": "988",
    "ZP": "987",
    "ZS": "975",
    "ZW": "986",
    "ZX": "977",  # cas spécial Saint-Barthélemy + Saint-Martin, mais code de Saint-Barth
}


class Command(BaseCommand):
    help = "Importe les circonscriptions"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s", "--source", type=argparse.FileType(mode="r"),
        )

    def handle(self, *args, source, **options):
        circos = json.load(source)

        for circo in circos["features"]:
            contour = GEOSGeometry(json.dumps(circo["geometry"]))
            dep = circo["properties"]["code_dpt"]
            numero = int(circo["properties"]["num_circ"])

            if dep in CORRESPONDANCES:
                dep = CORRESPONDANCES[dep]

            centroid = contour.centroid

            Circonscription.objects.update_or_create(
                departement=dep,
                numero=numero,
                defaults={"contour": contour, "centroid": centroid},
            )

        for i in range(1, 12):
            Circonscription.objects.update_or_create(departement="099", numero=i)

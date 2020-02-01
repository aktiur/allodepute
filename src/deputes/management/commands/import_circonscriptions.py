import argparse
import json
from pathlib import Path

from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand

from ...models import Circonscription


class Command(BaseCommand):
    help = "Importe les circonscriptions"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--source",
            type=argparse.FileType(mode="r"),
            default=str(
                Path(settings.BASE_DIR).parent
                / "data"
                / "france-circonscriptions-legislatives-2012.json"
            ),
        )

    def handle(self, *args, source, **options):
        circos = json.load(source)

        for circo in circos["features"]:
            contour = GEOSGeometry(json.dumps(circo["geometry"]))
            dep = circo["properties"]["code_dpt"]
            numero = int(circo["properties"]["num_circ"])

            centroid = contour.centroid

            Circonscription.objects.update_or_create(
                departement=dep,
                numero=numero,
                defaults={"contour": contour, "centroid": centroid},
            )

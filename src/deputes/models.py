from django.contrib.gis.db.models import PointField, GeometryField
from django.contrib.postgres.fields import ArrayField
from django.db import models


class CodePostal(models.Model):
    code = models.CharField(verbose_name="Code postal", max_length=5, unique=True)

    centroid = PointField(
        verbose_name="Position approximative", geography=True, srid=4326, null=True
    )
    communes = ArrayField(
        verbose_name="Communes", base_field=models.CharField(max_length=100)
    )


class Circonscription(models.Model):
    departement = models.CharField(verbose_name="Code du département", max_length=3)

    numero = models.PositiveSmallIntegerField(
        verbose_name="Numéro de la circonscription"
    )

    contour = GeometryField(verbose_name="Contour", geography=True, null=True)
    centroid = PointField(verbose_name="Centre approximatif", geography=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["departement", "numero"], name="code_circonscription"
            )
        ]

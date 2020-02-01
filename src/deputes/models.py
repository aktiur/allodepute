from django.contrib.gis.db.models import PointField, GeometryField
from django.contrib.postgres.fields import ArrayField
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Depute(models.Model):
    code = models.CharField(verbose_name="Code député", max_length=20, unique=True)

    nom = models.CharField(verbose_name="Nom", max_length=100)
    prenom = models.CharField(verbose_name="Prénom", max_length=100)

    emails = ArrayField(verbose_name="Emails", base_field=models.EmailField())
    telephones = ArrayField(
        verbose_name="Numéros de téléphone",
        base_field=PhoneNumberField(verbose_name="Téléphone", region="FR"),
    )
    twitter = models.CharField(
        verbose_name="Compte Twitter", max_length=100, blank=True
    )
    facebook = models.CharField(
        verbose_name="Compte Facebook", max_length=100, blank=True
    )

    photo = models.ImageField(verbose_name="Photographie", null=True)

    GROUPE_LREM = "LREM"
    GROUPE_MODEM = "MODEM"
    GROUPE_SOC = " SOC"
    GROUPE_LR = "LR"
    GROUPE_GDR = "GDR"
    GROUPE_LT = "LT"
    GROUPE_UAI = "UAI"
    GROUPE_LFI = "LFI"
    GROUPE_NI = "NI"

    GROUPE_CHOIX = (
        (GROUPE_LREM, "Groupe La République en Marche"),
        (GROUPE_MODEM, "Mouvement démocrate et apparentés"),
        (GROUPE_SOC, "Socialiste et apparentés"),
        (GROUPE_LR, "Les Républicains",),
        (GROUPE_GDR, "Gauche démocrate et républicaine"),
        (GROUPE_LT, "Libertés et Territoires"),
        (GROUPE_UAI, "UDI, Agir et Indépendants"),
        (GROUPE_LFI, "La France insoumise"),
        (GROUPE_NI, "Non inscrits"),
    )

    groupe = models.CharField(
        verbose_name="Groupe parlementaire", choices=GROUPE_CHOIX, max_length=10
    )

    circonscription = models.ForeignKey(
        to="deputes.Circonscription", on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.groupe} - {self.circonscription})"

    class Meta:
        verbose_name = "Député"
        ordering = ("nom", "prenom")


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

    def __str__(self):
        return f"{self.departement}-{self.numero}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["departement", "numero"], name="code_circonscription"
            )
        ]
        verbose_name = "Circonscription"

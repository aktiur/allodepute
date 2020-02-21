from random import choice

from django.contrib.gis.db.models import PointField, GeometryField
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.templatetags.static import static
from django.utils.html import format_html
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber

from deputes.departements import departements


class Depute(models.Model):
    code = models.CharField(verbose_name="Code député", max_length=20, unique=True)

    nom = models.CharField(verbose_name="Nom", max_length=100)
    prenom = models.CharField(verbose_name="Prénom", max_length=100)

    GENRE_MASCULIN = "M"
    GENRE_FEMININ = "F"
    GENRE_CHOIX = ((GENRE_MASCULIN, "masculin"), (GENRE_FEMININ, "féminin"))
    genre = models.CharField(verbose_name="Genre", max_length=1, default="F")

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

    GROUPE_LREM = "LaREM"
    GROUPE_MODEM = "MODEM"
    GROUPE_SOC = "SOC"
    GROUPE_LR = "LR"
    GROUPE_GDR = "GDR"
    GROUPE_LT = "LT"
    GROUPE_UAI = "UDI-AGIR"
    GROUPE_LFI = "FI"
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

    def image_name(self):
        return f"deputes/{self.code[2:]}.jpg"

    def telephone(self):
        return (
            PhoneNumber.from_string(choice(self.telephones)) if self.telephones else ""
        )

    def telephone_link(self):
        phone_number = PhoneNumber.from_string(choice(self.telephones))

        return format_html(
            '<a href="tel:{international}">{national}</a>',
            international=phone_number.as_e164,
            national=phone_number.as_national,
        )

    def email(self):
        return choice(self.emails) if self.emails else ""

    def titre(self):
        return "députée" if self.genre == "F" else "député"

    def article_indefini(self):
        return "une" if self.genre == "F" else "un"

    def article_demonstratif(self):
        return "cette" if self.genre == "F" else "ce"

    def to_dict(self):
        tel = self.telephone()
        return {
            "code": self.code,
            "image": static(self.image_name()),
            "nom": f"{self.prenom} {self.nom}",
            "titre": self.titre(),
            "article_indefini": self.article_indefini(),
            "article_demonstratif": self.article_demonstratif(),
            "groupe": self.groupe,
            "circonscription": self.circonscription.nom,
            "telephone_as_e164": tel.as_e164,
            "telephone_as_national": tel.as_national,
            "twitter": self.twitter,
            "email": self.email(),
        }

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

    @property
    def nom(self):
        if self.numero == 1:
            ordinal_suffix = "ère"
        else:
            ordinal_suffix = "ème"

        return format_html(
            "{numero}<sup>{ordinal}</sup> circonscription {departement}",
            numero=self.numero,
            ordinal=ordinal_suffix,
            departement=departements[self.departement].avec_charniere,
        )

    def __str__(self):
        return f"{self.departement}-{self.numero}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["departement", "numero"], name="code_circonscription"
            )
        ]
        verbose_name = "Circonscription"

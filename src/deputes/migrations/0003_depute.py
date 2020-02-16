# Generated by Django 3.0.2 on 2020-02-01 18:15

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ("deputes", "0002_auto_20200201_1708"),
    ]

    operations = [
        migrations.CreateModel(
            name="Depute",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        max_length=20, unique=True, verbose_name="Code député"
                    ),
                ),
                ("nom", models.CharField(max_length=100, verbose_name="Nom")),
                ("prenom", models.CharField(max_length=100, verbose_name="Nom")),
                (
                    "emails",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.EmailField(max_length=254),
                        size=None,
                        verbose_name="Emails",
                    ),
                ),
                (
                    "telephones",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=phonenumber_field.modelfields.PhoneNumberField(
                            max_length=128, region="FR", verbose_name="Téléphone",
                        ),
                        size=None,
                        verbose_name="Numéros de téléphone",
                    ),
                ),
                (
                    "twitter",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Compte Twitter"
                    ),
                ),
                (
                    "facebook",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Compte Facebook"
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        null=True, upload_to="", verbose_name="Photographie"
                    ),
                ),
                (
                    "groupe",
                    models.CharField(
                        choices=[
                            ("LREM", "La République en Marche"),
                            ("MODEM", "Mouvement démocrate et apparentés"),
                            ("SOC", "Socialiste et apparentés"),
                            ("LR", "Les Républicains"),
                            ("GDR", "Gauche démocrate et républicaine"),
                            ("LT", "Libertés et Territoires"),
                            ("UAI", "UDI, Agir et Indépendants"),
                            ("LFI", "La France insoumise"),
                            ("NI", "Non inscrits"),
                        ],
                        max_length=10,
                        verbose_name="Groupe parlementaire",
                    ),
                ),
                (
                    "circonscription",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="deputes.Circonscription",
                    ),
                ),
            ],
        ),
    ]

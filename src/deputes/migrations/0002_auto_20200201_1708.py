# Generated by Django 3.0.2 on 2020-02-01 16:08

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("deputes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="circonscription",
            name="centroid",
            field=django.contrib.gis.db.models.fields.PointField(
                geography=True, null=True, srid=4326, verbose_name="Centre approximatif"
            ),
        ),
        migrations.AddField(
            model_name="circonscription",
            name="contour",
            field=django.contrib.gis.db.models.fields.GeometryField(
                geography=True, null=True, srid=4326, verbose_name="Contour"
            ),
        ),
    ]

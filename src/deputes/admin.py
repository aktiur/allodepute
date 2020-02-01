from django.contrib import admin

from deputes import models


@admin.register(models.Depute)
class DeputeAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "groupe", "circonscription", "telephones")
    list_filter = ("groupe",)

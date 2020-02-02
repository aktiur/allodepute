from django.contrib import admin

from deputes import models


class AvecTelephoneFilter(admin.SimpleListFilter):
    title = "Numéros de téléphone"
    parameter_name = "telephones"

    def lookups(self, request, model_admin):
        return (
            ("1", "Au moins un",),
            ("0", "Sans",),
        )

    def queryset(self, request, queryset):
        if self.value() == "0":
            return queryset.filter(telephones__len=0)
        if self.value() == "1":
            return queryset.exclude(telephones__len=0)
        return queryset


@admin.register(models.Depute)
class DeputeAdmin(admin.ModelAdmin):
    list_display = ("nom", "prenom", "groupe", "circonscription", "telephones")
    list_filter = ("groupe", AvecTelephoneFilter)


@admin.register(models.Circonscription)
class CirconscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "departement",
        "numero",
    )

    readonly_fields = ["departement", "numero", "contour", "centroid"]

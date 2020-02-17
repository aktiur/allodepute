from pathlib import Path

from django.conf import settings
from django.shortcuts import render
from django.views.generic import TemplateView

from deputes.models import Depute


def home(request):
    return render(request, "pages/index.html")


class HomeView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        depute = (
            Depute.objects.filter(groupe__in=settings.GROUPES_MAJORITE)
            .exclude(telephones=[])
            .order_by("?")
            .first()
        )

        argumentaires = [
            {
                "id": Path(template_name).stem,
                "titre": titre,
                "template_name": template_name,
            }
            for titre, template_name in settings.ARGUMENTAIRES
        ]

        return super().get_context_data(
            **kwargs, depute=depute, argumentaires=argumentaires
        )

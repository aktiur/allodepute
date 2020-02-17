from random import sample
from urllib.parse import quote

from django.conf import settings
from django.http import QueryDict
from django.shortcuts import render
from django.template import loader
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
            {"id": id, "titre": titre, "template_name": f"argumentaires/{id}.md",}
            for titre, id in settings.ARGUMENTAIRES
        ]

        if depute.twitter:
            kwargs["adresse_twitter"] = f".@{depute.twitter}"
            kwargs["tweets"] = [
                loader.render_to_string(f"tweets/{id}.txt")
                for _, id in sample(settings.ARGUMENTAIRES, 2)
            ]

        formule = "Madame la députée" if depute.genre == "F" else "Monsieur le député"
        subject = quote("Mon opposition à la réforme des retraites")
        body = quote(loader.render_to_string("email.txt", context={"formule": formule}))

        mailto_link = f"mailto:{depute.email()}?subject={subject}&body={body}"

        return super().get_context_data(
            **kwargs,
            depute=depute,
            argumentaires=argumentaires,
            mailto_link=mailto_link,
        )

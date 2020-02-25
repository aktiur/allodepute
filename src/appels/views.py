from random import shuffle
from urllib.parse import quote

from django.conf import settings
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

        kwargs["argumentaires"] = [
            {"id": id, "titre": titre, "template_name": f"argumentaires/{id}.md",}
            for titre, id in settings.ARGUMENTAIRES
        ]

        kwargs["adresse_twitter"] = f".@{depute.twitter}"

        tweets = [
            (id, loader.render_to_string(f"tweets/{id}.txt"))
            for _, id in settings.ARGUMENTAIRES
        ]
        shuffle(tweets)

        kwargs["tweets"] = tweets[:2]

        formule = "Madame la députée" if depute.genre == "F" else "Monsieur le député"
        subject = quote("Mon opposition à la réforme des retraites")
        body = loader.render_to_string("email.txt", context={"formule": formule})

        kwargs["link_data"] = {
            "depute": depute.to_dict(),
            "tweets": [
                {"id": id, "tweet": tweet, "quoted": quote(tweet)}
                for id, tweet in tweets
            ],
            "mailto_qs": f"?subject={subject}&body={quote(body)}",
        }

        kwargs["email_body"] = body

        return super().get_context_data(**kwargs, depute=depute,)

from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.http import HttpResponse, JsonResponse
from django.templatetags.static import static

from deputes.models import CodePostal, Depute


def rechercher_depute_view(request):
    if request.method != "POST":
        return HttpResponse(content=b"", status=405)

    if "code_postal" not in request.POST:
        return JsonResponse({"message": "Code postal manquant"}, status=400)

    code_postal = request.POST["code_postal"]

    try:
        code_postal = CodePostal.objects.get(code=code_postal)
    except CodePostal.DoesNotExist:
        return JsonResponse({"message": "Ce code postal est inconnu"}, status=400)

    deputes = (
        Depute.objects.filter(groupe__in=settings.GROUPES_MAJORITE)
        .exclude(telephones=[])
        .annotate(distance=Distance("circonscription__contour", code_postal.centroid))
        .order_by("distance")[:3]
    )

    return JsonResponse(
        {
            "deputes": [
                {
                    "image": static(d.image_name()),
                    "nom": f"{d.prenom} {d.nom}",
                    "titre": d.titre(),
                    "circonscription": f"{d.titre()} {d.groupe} de la {d.circonscription.nom}",
                    "telephone": d.telephone().as_national if d.telephones else "",
                    "twitter": d.twitter,
                    "email": d.email(),
                }
                for d in deputes
            ]
        }
    )

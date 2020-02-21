from django.conf import settings
from django.contrib.gis.db.models.functions import Distance
from django.http import HttpResponse, JsonResponse

from deputes.models import CodePostal, Depute


def depute_au_hasard(request):
    depute = (
        Depute.objects.filter(groupe__in=settings.GROUPES_MAJORITE)
        .exclude(telephones=[])
        .order_by("?")
        .first()
    )

    return JsonResponse({"depute": depute.to_dict()})


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

    return JsonResponse({"deputes": [d.to_dict() for d in deputes]})

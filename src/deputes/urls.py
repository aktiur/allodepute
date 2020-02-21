from django.urls import path

from . import views

urlpatterns = [
    path("chercher/", views.rechercher_depute_view, name="chercher_deputes"),
    path("hasard/", views.depute_au_hasard, name="chercher_deputes"),
]

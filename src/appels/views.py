from django.shortcuts import render
from django.views.generic import TemplateView

from deputes.models import Depute


def home(request):
    return render(request, "pages/index.html")


class HomeView(TemplateView):
    template_name = "pages/index.html"

    def get_context_data(self, **kwargs):
        depute = Depute.objects.order_by("?").first()

        return super().get_context_data(**kwargs, depute=depute)

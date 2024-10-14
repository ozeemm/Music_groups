from typing import Any
from django.http import HttpResponse
from django.views.generic import TemplateView

from music_groups.models import *

# Create your views here.
class ShowGroupsView(TemplateView):
    template_name = "music_groups/show_music_groups.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['music_groups'] = Group.objects.all()

        return context
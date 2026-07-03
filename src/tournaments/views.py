from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from unfold.views import UnfoldModelAdminViewMixin

from .models import Round


class RoundResultsView(UnfoldModelAdminViewMixin, TemplateView):
    template_name = "admin/tournaments/round_results.html"
    title = "Ввод результатов тура"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        round_obj = get_object_or_404(Round, pk=self.kwargs["round_id"])

        context.update(
            {
                "round": round_obj,
                "matches": round_obj.matches.select_related("round").all(),
            }
        )

        return context


from django.shortcuts import render

# Create your views here.

from django.contrib.postgres import expressions
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, UpdateView, View, TemplateView
from django.contrib import messages


from src.leagues.models import League, LeagueMember
from django.db.models import Window, F, QuerySet, Prefetch
from django.db.models.functions import Rank
from src.tournaments.models import Round, Match, Tournament
from src.results.models import Prediction


class ListLeagueStandingsView(LoginRequiredMixin, ListView):
    """Вивід списка ліг і перші 5 позицій турнірної таблиці для кожної ліги"""
    model = League
    template_name = "leaderboard/league_list.html"
    context_object_name = "leagues"

    def get_queryset(self):
        ranked_members = (
            LeagueMember.objects
            .select_related("user")
            .annotate(
                computed_rank=Window(
                    expression=Rank(),
                    order_by=F("total_points").desc(),
                )
            )
            .order_by("computed_rank", "user__username")
        )

        return (
            League.objects
            .filter(members__user=self.request.user)
            .distinct()
            .prefetch_related(
                Prefetch("members", queryset=ranked_members, to_attr="ranked_members")
            )
        )
class LeagueStandingsView(ListView):
    """ Вивід турнірної таблиці користувача """

    model = LeagueMember
    template_name = "leaderboard/league_standings.html"
    context_object_name = "standings"

    def get_queryset(self):
        self.league = get_object_or_404(League, slug=self.kwargs["slug"])
        return(
            LeagueMember.objects.filter(league=self.league)
            .select_related("user").annotate(
                computer_rank=Window(expression=Rank(), order_by=F("total_points").desc()
                )
            )
             .order_by("computer_rank","user__username"))

    def get_context_data(self, **kwargs):
        """Додаємо саму лігу в контекст шаблону, щоб використовувати її назву чи slug"""
        context = super().get_context_data(**kwargs)
        context["league"] = self.league
        return context
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Sum, F, Prefetch
from django.db.models.functions import Coalesce
from django.views.generic import ListView

from src.leagues.models import League, LeagueMember


def _annotate_points(queryset):
    """Додає суми балів за кожним типом угадування + загальний рахунок."""
    return (
        queryset
        .annotate(
            correct_winner_points=Coalesce(Sum("point_entries__point_correct_winner"), 0),
            correct_diff_points=Coalesce(Sum("point_entries__point_correct_diff"), 0),
            exact_score_points=Coalesce(Sum("point_entries__point_exact_score"), 0),
        )
        .annotate(
            computed_total=(
                F("correct_winner_points")
                + F("correct_diff_points")
                + F("exact_score_points")
            )
        )
    )


def _assign_ranks(members):
    """
    Емулює SQL RANK(): однакова сума балів -> однаковий ранг,
    наступний ранг враховує "пропущені" місця.
    Не використовуємо Window() тут, бо він погано поєднується
    з Sum()-аґрегацією в одному запиті.
    """
    members = list(members)
    rank = 0
    prev_total = None
    for i, member in enumerate(members, start=1):
        if member.computed_total != prev_total:
            rank = i
            prev_total = member.computed_total
        member.computed_rank = rank
    return members


class ListLeagueStandingsView(LoginRequiredMixin, ListView):
    """Вивід списку ліг і перших 5 позицій турнірної таблиці для кожної ліги"""
    model = League
    template_name = "leaderboard/league_list.html"
    context_object_name = "leagues"

    def get_queryset(self):
        ranked_members = _annotate_points(
            LeagueMember.objects.select_related("user")
        ).order_by("-computed_total", "user__username")

        leagues = (
            League.objects
            .filter(members__user=self.request.user)
            .distinct()
            .prefetch_related(
                Prefetch("members", queryset=ranked_members, to_attr="ranked_members")
            )
        )

        for league in leagues:
            league.ranked_members = _assign_ranks(league.ranked_members)[:5]

        return leagues


class LeagueStandingsView(ListView):
    """Вивід турнірної таблиці ліги"""
    model = LeagueMember
    template_name = "leaderboard/league_standings.html"
    context_object_name = "standings"

    def get_queryset(self):
        self.league = get_object_or_404(League, slug=self.kwargs["slug"])
        members = _annotate_points(
            LeagueMember.objects
            .filter(league=self.league)
            .select_related("user")
        ).order_by("-computed_total", "user__username")

        return _assign_ranks(members)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["league"] = self.league
        return context
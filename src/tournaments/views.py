from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from unfold.views import UnfoldModelAdminViewMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Round, Tournament
from src.results.models import MatchResult

from leagues.models import LeagueMember


class LeagueMemberRequiredMixin:
    """
    Проверяет, что пользователь — участник лиги, к которой относится турнир.
    Наследник обязан реализовать get_league().
    """
    def get_league(self):
        raise NotImplementedError("Реалізуйте get_league() у нащадку")

    def dispatch(self, request, *args, **kwargs):
        league = self.get_league()
        if not LeagueMember.objects.filter(league=league, user=request.user).exists():
            raise PermissionDenied("Ви не є учасником цієї ліги.")
        return super().dispatch(request, *args, **kwargs)


class RoundResultsView(UnfoldModelAdminViewMixin, TemplateView):
    template_name = "admin/tournaments/round_results.html"
    title = "Введення результатів туру"
    model_admin = None

    def dispatch(self, request, *args, **kwargs):
        # Наша жесткая и безопасная проверка прав
        if not request.user.has_perm("tournaments.change_match"):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_permission_required(self):
        # Заглушаем внутренние требования Unfold, возвращая пустой список прав
        return ()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        round_obj = get_object_or_404(Round, pk=self.kwargs["round_id"])
        matches = round_obj.matches.select_related("home_team", "away_team",
                                                   "match_result").all()
        context.update(
            {
                "round": round_obj,
                "matches": matches,
                "score_range": range(0, 11),  # 0..10, можешь поменять диапазон
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        round_obj = get_object_or_404(Round, pk=self.kwargs["round_id"])
        matches = round_obj.matches.all()
        for match in matches:
            home_ft_val = request.POST.get(f"home_{match.id}")
            away_ft_val = request.POST.get(f"away_{match.id}")

            if home_ft_val and away_ft_val:
                try:
                    home_ft = int(home_ft_val)
                    away_ft = int(away_ft_val)
                except ValueError:
                    continue

                has_pen = request.POST.get(f"has_pen_{match.id}") == "on"
                home_pen_val = request.POST.get(f"home_pen_{match.id}")
                away_pen_val = request.POST.get(f"away_pen_{match.id}")

                home_pen = None
                away_pen = None
                if has_pen and home_pen_val and away_pen_val:
                    try:
                        home_pen = int(home_pen_val)
                        away_pen = int(away_pen_val)
                    except ValueError:
                        home_pen = away_pen = None
                        has_pen = False

                match_result, created = MatchResult.objects.get_or_create(
                    match=match,
                    defaults={"home_ft": home_ft, "away_ft": away_ft}
                )
                match_result.home_ft = home_ft
                match_result.away_ft = away_ft
                match_result.has_penalty_shootout = has_pen
                match_result.home_pen = home_pen
                match_result.away_pen = away_pen
                match_result.home_scored = home_ft > 0
                match_result.away_scored = away_ft > 0
                match_result.home_clean_sheet = away_ft == 0
                match_result.away_clean_sheet = home_ft == 0
                match_result.entered_by = request.user
                match_result.save()

        messages.success(request, "Результати туру успішно збережено!")
        return redirect("admin:tournaments_round_changelist")


class TournamentsDetail(LoginRequiredMixin, LeagueMemberRequiredMixin, DetailView):
    model = Tournament
    template_name = "tournaments/tournament_detail.html"
    context_object_name = "tournament"

    def get_league(self):
        # тут self.get_object() безопасен, DetailView сам подставит self.object позже,
        # но на момент dispatch self.object ещё не установлен — берём напрямую
        tournament = get_object_or_404(Tournament, pk=self.kwargs["pk"])
        return tournament.league
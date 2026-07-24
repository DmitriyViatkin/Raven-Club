from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, UpdateView, View
from django.contrib import messages
from .models import League, LeagueMember

from src.tournaments.models import Round, Match, Tournament
from src.results.models import Prediction
from .forms import PredictionForm
from django.db import IntegrityError
from src.tournaments.views import LeagueMemberRequiredMixin


class LeagueJoinView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        league = get_object_or_404(League, pk=pk)

        if league.is_private:
            messages.error(request, "Ця ліга приватна, потрібне запрошення.")
            return redirect("predictions:league_detail", pk=league.pk)

        try:
            LeagueMember.objects.create(league=league, user=request.user)
            messages.success(request, f"Ви вступили в лігу «{league.name}».")
        except IntegrityError:
            messages.info(request, "Ви вже є учасником цієї ліги.")

        return redirect("predictions:league_detail", pk=league.pk)


class LeagueLeaveView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        league = get_object_or_404(League, pk=pk)

        deleted, _ = LeagueMember.objects.filter(
            league=league, user=request.user
        ).delete()

        if deleted:
            messages.success(request, f"Ви вийшли з ліги «{league.name}».")
        else:
            messages.info(request, "Ви не є учасником цієї ліги.")

        return redirect("predictions:league_detail", pk=league.pk)


class RoundMatchListView(LoginRequiredMixin, LeagueMemberRequiredMixin,
                          UserPassesTestMixin, ListView):
    """
    Список всех матчей раунда со статусом:
    сделал ли текущий пользователь прогноз на каждый матч.
    Доступ только для участников лиги, к которой относится турнир раунда.
    """
    model = Match
    template_name = "leagues/round_matches.html"
    context_object_name = "matches"

    def get_league(self):
        return self.get_round().tournament.league

    def get_round(self):
        if not hasattr(self, "_round_obj"):
            self._round_obj = get_object_or_404(
                Round.objects.select_related("tournament__league"),
                pk=self.kwargs["round_id"],
            )
        return self._round_obj

    def test_func(self):
        round_obj = self.get_round()
        league = round_obj.tournament.league
        return LeagueMember.objects.filter(
            league=league, user=self.request.user
        ).exists()

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Ви не є учасником цієї ліги.")
        return super().handle_no_permission()

    def get_queryset(self):
        round_obj = self.get_round()
        return (
            round_obj.matches
            .select_related("home_team", "away_team")
            .order_by("id")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        round_obj = self.get_round()
        context["round"] = round_obj

        user_predictions = Prediction.objects.filter(
            user=self.request.user,
            match__round=round_obj,
        ).values_list("match_id", flat=True)
        predicted_match_ids = set(user_predictions)

        for match in context["matches"]:
            match.has_prediction = match.id in predicted_match_ids
        return context


class PredictionEditView(LoginRequiredMixin, UpdateView):
    """
    Создание или редактирование прогноза на конкретный матч.
    Работает и когда прогноза ещё нет, и когда он уже существует —
    за счёт переопределённого get_object().
    Доступ только для участников лиги, к которой относится турнир матча.
    """
    model = Prediction
    form_class = PredictionForm
    template_name = "leagues/create_prediction.html"

    def get_match(self):
        if not hasattr(self, "_match_obj"):
            self._match_obj = get_object_or_404(
                Match.objects.select_related("round__tournament__league"),
                pk=self.kwargs["match_id"],
            )
        return self._match_obj

    def get_league(self):
        return self.get_match().round.tournament.league

    def dispatch(self, request, *args, **kwargs):
        match = self.get_match()

        # Проверка членства в лиге — раньше всех остальных проверок
        league = match.round.tournament.league
        if not LeagueMember.objects.filter(league=league, user=request.user).exists():
            raise PermissionDenied("Ви не є учасником цієї ліги.")

        # Проверка дедлайна — до того, как что-либо рендерить/сохранять
        if match.round.is_locked or (
                match.round.deadline and timezone.now() > match.round.deadline
        ):
            messages.error(request, "Приём прогнозів на цей тур закрито.")
            return redirect("tournaments:round_matches", round_id=match.round_id)

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        match = self.get_match()
        try:
            return Prediction.objects.get(user=self.request.user, match=match)
        except Prediction.DoesNotExist:
            return None

    def form_valid(self, form):
        match = self.get_match()
        prediction = form.save(commit=False)
        prediction.user = self.request.user
        prediction.match = match
        prediction.tournament = match.round.tournament
        prediction.save()
        messages.success(self.request, "Прогноз збережено.")
        self.object = prediction
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["match"] = self.get_match()
        context["score_range"] = range(0, 11)
        return context

    def get_success_url(self):
        match = self.get_match()
        return reverse("predictions:round_matches", kwargs={"round_id": match.round_id})


class CurrentRoundRedirectView(LoginRequiredMixin, View):
    """
    Точка входа без параметров: находит ближайший актуальный тур
    и редиректит на список его матчей.
    """
    def get(self, request, *args, **kwargs):
        round_obj = (
            Round.objects
            .filter(is_locked=False)
            .order_by("deadline")
            .first()
        )
        if round_obj is None:
            # На случай, если активных туров нет вообще
            messages.info(request, "Наразі немає активних турів.")
            return redirect("index")

        return redirect("predictions:round_matches", round_id=round_obj.id)


class LeaguesListAll(LoginRequiredMixin, ListView):
    """ Список усіх ліг. """

    model = League
    template_name = "leagues/leagues_list.html"
    context_object_name = "leagues"
    paginate_by = 10

    def get_queryset(self):
        """ Получаем список лиг """
        return League.objects.all().distinct()


class LeaguesList(LoginRequiredMixin, ListView):
    """ Список ліг, у яких бере участь користувач. """

    model = League
    template_name = "leagues/leagues_list.html"
    context_object_name = "leagues"
    paginate_by = 10

    def get_queryset(self):
        """ Получаем список лиг """
        return League.objects.filter(members__user=self.request.user).distinct()


class LeagueDetail(LoginRequiredMixin, ListView):
    """Конкретна ліга + список турнірів у ній."""

    model = Tournament
    template_name = "leagues/leagues_detail.html"
    context_object_name = "tournaments"
    paginate_by = 10

    def get_league(self):
        if not hasattr(self, "_league"):
            self._league = get_object_or_404(
                League.objects.prefetch_related("teams"),
                pk=self.kwargs["pk"]
            )
        return self._league

    def get_queryset(self):
        return (
            self.get_league().tournaments.order_by("-starts_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        league = self.get_league()
        context["league"] = league
        context["is_member"] = league.members.filter(
            user=self.request.user).exists()
        context["teams_count"] = league.teams.count()
        return context
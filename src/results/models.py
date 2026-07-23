

from django.db import models
from src.tournaments.models import Match, Tournament
from src.users.models import Player


class MatchResult(models.Model):
    """Еталонні результати матчів, які вносяться адміністратором."""
    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE,
        related_name="match_result"
    )
    home_ft = models.IntegerField()
    away_ft = models.IntegerField()

    # Нові поля для серії пенальті
    has_penalty_shootout = models.BooleanField(
        default=False,
        verbose_name="Була серія пенальті"
    )
    home_pen = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name="Пенальті (дом.)"
    )
    away_pen = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name="Пенальті (гості)"
    )

    home_scored = models.BooleanField(default=False)
    away_scored = models.BooleanField(default=False)
    home_clean_sheet = models.BooleanField(default=False)
    away_clean_sheet = models.BooleanField(default=False)
    entered_by = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entered_results"
    )
    entered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Match Result"
        verbose_name_plural = "Match Results"

    def __str__(self):
        base = f"Result for match {self.match_id}: {self.home_ft}-{self.away_ft}"
        if self.has_penalty_shootout:
            base += f" (пен. {self.home_pen}-{self.away_pen})"
        return base

    @property
    def winner(self):
        """'home', 'away' або None (нічия без пенальті)."""
        if self.home_ft > self.away_ft:
            return "home"
        if self.away_ft > self.home_ft:
            return "away"
        if self.has_penalty_shootout and self.home_pen is not None and self.away_pen is not None:
            if self.home_pen > self.away_pen:
                return "home"
            if self.away_pen > self.home_pen:
                return "away"
        return None


class Prediction(models.Model):
    """Прогнози користувачів на конкретні матчі."""

    user = models.ForeignKey(Player, on_delete=models.CASCADE,
                             related_name="predictions")
    match = models.ForeignKey(Match, on_delete=models.CASCADE,
                              related_name="predictions")

    # Денормалізоване поле за ТЗ для швидкої фільтрації прогнозів по всьому турніру
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE,
                                   related_name="predictions")

    home_ft = models.IntegerField()
    away_ft = models.IntegerField()

    home_scored = models.BooleanField(default=False)
    away_scored = models.BooleanField(default=False)
    home_clean_sheet = models.BooleanField(default=False)
    away_clean_sheet = models.BooleanField(default=False)

    # Виправлено: додано default=0, оскільки на старті балів ще немає
    points_earned = models.IntegerField(default=0)

    is_calculated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Гравець може зробити лише один прогноз на один конкретний матч
        unique_together = ('user', 'match')
        verbose_name = "Prediction"
        verbose_name_plural = "Predictions"

    def __str__(self):
        # Виправлено синтаксичну помилку розриву рядка
        return f"Prediction by {self.user.username} for match {self.match_id} ({self.home_ft}:{self.away_ft})"
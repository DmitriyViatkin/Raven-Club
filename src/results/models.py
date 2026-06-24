from django.db import models
from src.tournaments.models import Match
from src.users.models import Player


class MatchResult(models.Model):
    """Еталонні результати матчів, які вносяться адміністратором."""

    # Змінено на OneToOneField (у матчу може бути лише один результат)
    match = models.OneToOneField(
        Match,
        on_delete=models.CASCADE,
        related_name="match_result"  # в однині, бо зв'язок 1:1
    )

    home_ft = models.IntegerField()
    away_ft = models.IntegerField()

    # Денормалізовані поля (якщо ви вирішили їх залишити)
    home_scored = models.BooleanField(default=False)
    away_scored = models.BooleanField(default=False)
    home_clean_sheet = models.BooleanField(default=False)
    away_clean_sheet = models.BooleanField(default=False)

    # Змінено on_delete на SET_NULL, щоб не втратити результати матчу, якщо видалять адміна
    entered_by = models.ForeignKey(
        Player,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="entered_results"
    )

    entered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        auto_now=True)  # Виправлено на auto_now для автоматичного оновлення

    class Meta:
        verbose_name = "Match Result"
        verbose_name_plural = "Match Results"

    def __str__(self):
        return f"Result for match {self.match_id}: {self.home_ft}-{self.away_ft}"
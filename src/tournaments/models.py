from django.db import models

from enums.enums import StatusTournament
from src.leagues.models import League

class Tournament(models.Model):
    """ Конкретний сезон або змагання всередині ліги.

    Один турнір = один набір турів і матчів. """

    league = models.ForeignKey(League, on_delete=models.CASCADE,
                                 related_name= "tournaments")
    name = models.CharField(max_length=100)
    season= models.CharField(max_length=250)
    status = models.CharField(max_length=30, choices= StatusTournament.choices(),
                              default=StatusTournament.upcoming.value)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name= "Tournament"
        verbose_name_plural= "Tournaments"

    def __str__(self):
        return f"{self.name} ({self.season})"

class Round(models.Model):
    """ Один тур містить набір матчів. deadline визначає,
    до якого часу можна робити прогнози на тур. is_locked блокує прийом прогнозів. """
    tournament = models.ForeignKey(Tournament, on_delete= models.CASCADE,
                                      related_name="round")
    round_number = models.IntegerField()
    name= models.CharField(max_length=200)
    deadline= models.DateTimeField()
    is_locked= models.BooleanField(default=False)

    class Meta:
        unique_together = ('tournament_id', 'round_number')
        verbose_name = "Round"
        verbose_name_plural = "Rounds"

    def __str__(self):
        return f"{self.tournament.name} - {self.name}"

class Match(models.Model):
    """Окремий матч всередині туру. """

    round = models.ForeignKey(Round, on_delete= models.CASCADE,
                                 related_name="matches")
    home_team = models.CharField(max_length=250)
    away_team = models.CharField(max_length=250)
    home_logo = models.ImageField(upload_to='leagues/logos/', blank=True, null=True)
    away_logo = models.ImageField(upload_to='leagues/logos/', blank=True, null=True)

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"

    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
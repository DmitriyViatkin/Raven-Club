from django.db import models
from enums.enums import Status, Role
from src.users.models import Player
from typing import TYPE_CHECKING, List


class League (models.Model):

    name=models.CharField(max_length=100)
    teams = models.ManyToManyField(
        "tournaments.Team",

        blank=True,
        related_name="leagues",
        verbose_name="Команди ліги"
    )
    slug=models.CharField(max_length=100, unique=True)
    short_description=models.CharField(max_length=300)
    full_description=models.TextField()
    logo= models.ImageField(upload_to='leagues/', blank=True, null=True)
    is_private= models.BooleanField()
    status= models.CharField(max_length=20, choices =Status.choices(),
                             default=Status.draft.value)
    create_by= models.ForeignKey(Player, on_delete= models.PROTECT,
                                 related_name='created_leagues' )
    create_at= models.DateField()
    if TYPE_CHECKING:
        ranked_members: List["LeagueMember"]
    class Meta:
        verbose_name = "League"
        verbose_name_plural = "Leagues"

class LeagueMember (models.Model):

    league = models.ForeignKey(League, on_delete= models.CASCADE,
                                  related_name='members')
    user = models.ForeignKey(Player, on_delete= models.CASCADE,
                                related_name='league_memberships')
    role = models.CharField(max_length= 20 , choices=Role.choices(),
                            default=Role.USER.value)
    total_points = models.IntegerField(default=0)
    rank = models.IntegerField(null= True, blank= True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('league', 'user')
        verbose_name = "League Member"
        verbose_name_plural = "League Members"

class UserLeaguePoints(models.Model):
    league_member = models.ForeignKey(
        LeagueMember, on_delete=models.CASCADE, related_name='points'
    )
    match = models.ForeignKey(
        "tournaments.Match", on_delete=models.CASCADE, related_name='league_points'
    )
    point_correct_winner = models.IntegerField(default=0)
    point_correct_diff = models.IntegerField(default=0)
    point_exact_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('league_member', 'match')
        ordering = ['-created_at']
        verbose_name = "User League Points"
        verbose_name_plural = "User League Points"

    @property
    def points(self) -> int:
        return (
            self.point_correct_winner
            + self.point_correct_diff
            + self.point_exact_score
        )

class ScoringRules(models.Model):

    league= models.ForeignKey(League, on_delete= models.CASCADE)
    point_exact_score = models.IntegerField()
    point_correct_winner= models.IntegerField()
    point_correct_diff= models.IntegerField()
    points_home_scored = models.IntegerField()
    points_away_scored = models.IntegerField()
    points_home_clean_sheet = models.IntegerField()
    points_away_clean_sheet = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "scoring rules"
        verbose_name_plural = "scoring rules"



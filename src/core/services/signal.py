import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from src.tournaments.models import Match
from src.core.services.services import calculate_round_results
from src.results.models import MatchResult,Prediction
logger = logging.getLogger(__name__)
@receiver(post_save, sender=MatchResult)
def trigger_round_calculation(sender, instance, created, **kwargs):
    round_obj = instance.match.round

    # Считаем только если результаты внесены для ВСЕХ матчей тура
    total_matches = round_obj.matches.count()
    matches_with_result = round_obj.matches.filter(
        match_result__isnull=False
    ).count()

    if total_matches > 0 and total_matches == matches_with_result:
        calculate_round_results(round_obj)
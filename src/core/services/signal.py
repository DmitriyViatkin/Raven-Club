import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from src.tournaments.models import Match
from src.core.services.services import calculate_points_for_match
from src.results.models import MatchResult,Prediction
logger = logging.getLogger(__name__)
@receiver(post_save, sender=MatchResult)
def match_result_post_save(sender, instance, created, **kwargs):
    """
    Сигнал, который вызывается после сохранения MatchResult.
    Он инициирует расчет очков для всех прогнозов на этот матч.
    """
    match_id = instance.match.id
    result = calculate_points_for_match(match_id)
    if result["status"] == "error":
        # Логируем ошибку или уведомляем администратора
        logger.error(f"Ошибка при расчете очков для матча {match_id}: {result['message']}")

        #print(f"Ошибка при расчете очков для матча {match_id}: {result['message']}")
    elif result["status"] == "info":
        # Можно логировать информационные сообщения
        logger.info(
            "Информационное сообщение при расчете очков для матча %s: %s",
            match_id,
            result.get("message"),
        )
        #print(f"Информация: {result['message']}")
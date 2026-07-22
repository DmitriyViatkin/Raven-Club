from django.db import transaction
from src.results.models import MatchResult , Prediction
from src.tournaments.models import Match, Round,  Tournament
from src.leagues.models import ScoringRules
from django.utils import timezone



def calculate_points_for_match(match_id: int) -> dict:
    try:
        match = Match.objects.select_related(
            'round__tournament__league'
        ).get(id=match_id)
    except Match.DoesNotExist:
        raise ValueError(f"Match with id {match_id} does not exist.")

    result = getattr(match, "match_result", None)
    if result is None:
        return {"status": "error", "message": "У матча не указан финальный счет."}

    league = match.round.tournament.league
    try:
        rules = ScoringRules.objects.get(league=league)
    except ScoringRules.DoesNotExist:
        return {"status": "error",
                "message": f"Не найдены ScoringRules для лиги '{league.name}'."}

    predictions = Prediction.objects.filter(match=match, is_calculated=False)
    if not predictions.exists():
        return {"status": "info", "message": "Нет новых прогнозов для расчета."}

    now = timezone.now()
    predictions_to_update = []
    for pred in predictions:
        points = 0
        if pred.home_ft == result.home_ft and pred.away_ft == result.away_ft:
            points += rules.point_exact_score
        if (pred.home_ft - pred.away_ft) == (result.home_ft - result.away_ft):
            points += rules.point_correct_diff
        if (pred.home_ft > pred.away_ft and result.home_ft > result.away_ft) or \
           (pred.home_ft < pred.away_ft and result.home_ft < result.away_ft):
            points += rules.point_correct_winner
        if pred.home_ft > 0 and result.home_ft > 0:
            points += rules.points_home_scored
        if pred.away_ft > 0 and result.away_ft > 0:
            points += rules.points_away_scored
        if result.away_ft == 0 and pred.home_clean_sheet:
            points += rules.points_home_clean_sheet
        if result.home_ft == 0 and pred.away_clean_sheet:
            points += rules.points_away_clean_sheet

        pred.points_earned = points
        pred.is_calculated = True
        pred.updated_at = now
        predictions_to_update.append(pred)

    with transaction.atomic():
        Prediction.objects.bulk_update(
            predictions_to_update,
            fields=['points_earned', 'is_calculated', 'updated_at']
        )

    return {
        "status": "success",
        "message": f"Успешно рассчитано прогнозов: {len(predictions_to_update)}"
    }

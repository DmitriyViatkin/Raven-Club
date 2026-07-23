# predictions/services.py
from django.db.models import Sum

from src.results.models import  Prediction
from src.leagues.models import LeagueMember


def calculate_points(prediction, result):
    """Ваша логика начисления баллов по ScoringRules."""
    league = prediction.tournament.league
    rules = league.scoringrules_set.first()  # или как у вас связано

    points = 0

    # точный счёт
    if prediction.home_ft == result.home_ft and prediction.away_ft == result.away_ft:
        points += rules.point_exact_score
    else:
        # правильный победитель
        pred_winner = _winner(prediction.home_ft, prediction.away_ft)
        if pred_winner == result.winner:
            points += rules.point_correct_winner
        # правильная разница
        if (prediction.home_ft - prediction.away_ft) == (result.home_ft - result.away_ft):
            points += rules.point_correct_diff

    if prediction.home_scored and result.home_scored:
        points += rules.points_home_scored
    if prediction.away_scored and result.away_scored:
        points += rules.points_away_scored
    if prediction.home_clean_sheet and result.home_clean_sheet:
        points += rules.points_home_clean_sheet
    if prediction.away_clean_sheet and result.away_clean_sheet:
        points += rules.points_away_clean_sheet

    return points


def _winner(home, away):
    if home > away:
        return "home"
    if away > home:
        return "away"
    return None


def calculate_round_results(round_obj):
    """Считает очки для всех прогнозов тура и обновляет таблицы затронутых лиг."""
    touched_leagues = set()

    matches = round_obj.matches.select_related("match_result")

    for match in matches:
        result = getattr(match, "match_result", None)
        if not result:
            continue

        predictions = match.predictions.select_related("tournament__league")

        for prediction in predictions:
            prediction.points_earned = calculate_points(prediction, result)
            prediction.is_calculated = True
            prediction.save(update_fields=["points_earned", "is_calculated"])
            touched_leagues.add(prediction.tournament.league_id)

    from src.leagues.models import League
    for league in League.objects.filter(id__in=touched_leagues):
        recalc_league_points(league)


def recalc_league_points(league):
    members = list(league.members.all())
    for member in members:
        total = Prediction.objects.filter(
            user=member.user,
            tournament__league=league,
            is_calculated=True,
        ).aggregate(s=Sum("points_earned"))["s"] or 0
        member.total_points = total

    LeagueMember.objects.bulk_update(members, ["total_points"])
# predictions/services.py

from django.db import transaction

from src.leagues.models import UserLeaguePoints

from src.results.models import  Prediction
from src.leagues.models import LeagueMember


def calculate_points(prediction, result, rules) -> dict:
    """
    Обчислює бали за категоріями згідно з ScoringRules.
    Якщо вгадано точний рахунок — додаються бали за всіма трьома категоріями.
    Якщо ні — окремо перевіряються переможець та різниця.
    """
    pts_exact = 0
    pts_winner = 0
    pts_diff = 0

    # 1. Точний рахунок (включає в себе і переможця, і різницю)
    if prediction.home_ft == result.home_ft and prediction.away_ft == result.away_ft:

        pts_exact = rules.point_exact_score
        pts_winner = rules.point_correct_winner
        pts_diff = rules.point_correct_diff
    else:
        # 2. Вгаданий переможець або нічия
        pred_winner = _winner(prediction.home_ft, prediction.away_ft)
        if pred_winner == result.winner:

            pts_winner = rules.point_correct_winner

        # 3. Вгадана різниця м'ячів (працює і для нічиїх, наприклад: 1:1 та 2:2 має різницю 0)
        if abs(prediction.home_ft - prediction.away_ft) == abs(result.home_ft - result.away_ft):


            pts_diff = rules.point_correct_diff

    return {
        "point_exact_score": pts_exact,
        "point_correct_winner": pts_winner,
        "point_correct_diff": pts_diff,
    }


def _winner(home, away):
    if home > away:
        return "home"
    if away > home:
        return "away"
    return None

@transaction.atomic
def calculate_round_results(round_obj):
    """Рахує бали для всіх прогнозів туру і оновлює UserLeaguePoints
     + LeagueMember затронутих ліг."""
    touched_leagues = set()

    matches = round_obj.matches.select_related("match_result")

    for match in matches:
        result = getattr(match, "match_result", None)
        if not result:
            continue

        predictions = match.predictions.select_related("tournament__league").select_related("user")

        for prediction in predictions:
            league = prediction.tournament.league
            rules = getattr(league, "scoring_rules", None)
            if not rules:
                raise ValueError(f"Scoring rules not found for league {league.id}")
            league_member, _ = LeagueMember.objects.get_or_create(
                league=league, user=prediction.user)
            breakdown = calculate_points(prediction, result, rules)
            UserLeaguePoints.objects.update_or_create(
                league_member=league_member,
                prediction=prediction,
                defaults=breakdown,
            )

            prediction.is_calculated = True
            prediction.save(update_fields=["is_calculated"])
            touched_leagues.add(league.id)
    from src.leagues.models import League
    for league in League.objects.filter(id__in=touched_leagues):
        recalc_league_points(league)

@transaction.atomic
def recalc_league_points(league):
    """Перераховує total_points для всіх учасників ліги на основі UserLeaguePoints."""
    category_fields = ["point_exact_score",
                       "point_correct_winner", "point_correct_diff"]
    totals = {}
    for row in UserLeaguePoints.objects.filter(league_member__league=league).values(
        "league_member_id", *category_fields):
        member_id = row["league_member_id"]
        totals[member_id] = (totals.get(member_id, 0) +
                             sum(row[field] for field in category_fields))
    members = list(league.members.all())
    for member in members:
        member.total_points = totals.get(member.id, 0)
    LeagueMember.objects.bulk_update(members, ["total_points"])
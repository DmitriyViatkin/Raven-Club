from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import MatchResult, Prediction


class MatchResultInline(TabularInline):
    """Inline для використання всередині MatchAdmin у tournaments app."""
    model = MatchResult
    extra = 1
    max_num = 1
    can_delete = False
    fields = (
        ("home_ft", "away_ft"),
        ("home_scored", "away_scored"),
        ("home_clean_sheet", "away_clean_sheet"),
    )


@admin.register(MatchResult)
class MatchResultAdmin(ModelAdmin):
    # Усі поля беремо з MatchResult або через його FK на Match
    list_display = ("id", "display_teams", "display_round", "home_ft", "away_ft")
    search_fields = (
        "match__home_team",
        "match__away_team",
    )
    list_filter = ("match__round", "match__round__tournament")
    readonly_fields = ("entered_by", "entered_at", "updated_at")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.entered_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description="Матч")
    def display_teams(self, obj):
        return f"{obj.match.home_team} vs {obj.match.away_team}"

    @admin.display(description="Тур")
    def display_round(self, obj):
        return obj.match.round


@admin.register(Prediction)
class PredictionAdmin(ModelAdmin):
    list_display = (
        "user",
        "match",
        "tournament",
        "predicted_score",
        "points_earned",
        "is_calculated",
    )
    list_filter = ("is_calculated", "tournament", "user")
    search_fields = (
        "user__username",
        "user__email",
        "match__home_team",
        "match__away_team",
    )
    autocomplete_fields = ("user", "match", "tournament")
    fieldsets = (
        (None, {"fields": ("user", "match", "tournament")}),
        ("Прогноз рахунку", {"fields": (("home_ft", "away_ft"),)}),
        (
            "Додаткові маркери",
            {
                "fields": (
                    ("home_scored", "away_scored"),
                    ("home_clean_sheet", "away_clean_sheet"),
                )
            },
        ),
        ("Розрахунок балів", {"fields": ("points_earned", "is_calculated")}),
    )

    @admin.display(description="Прогноз")
    def predicted_score(self, obj):
        return f"{obj.home_ft} : {obj.away_ft}"
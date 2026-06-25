from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Tournament, Round, Match

@admin.register(Tournament)
class TournamentAdmin(ModelAdmin):
    list_display = ("league","name", "season","status", "starts_at", "ends_at",  )
    # По каким полям можно кликнуть, чтобы перейти к редактированию
    list_display_links = ("name",)
    # Фильтры в правой панели
    list_filter = ("status", "starts_at")
    # Поля для поиска
    search_fields = ("name",)

@admin.register(Round)
class RoundAdmin(ModelAdmin):

    list_display = ("tournament","round_number", "name", "deadline", "is_locked")
    list_display_links = ("name",)
    list_filter = ("is_locked",)
    search_fields = ("name",)
@admin.register(Match)
class MatchAdmin(ModelAdmin):
    list_display = ("round","home_team", "away_team")
    list_display_links = ("home_team",)
    list_filter = ("round",)
    search_fields = ("home_team", "away_team")



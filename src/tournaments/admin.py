from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html

from unfold.admin import ModelAdmin, TabularInline

from .models import Tournament, Round, Match, Team  # Добавили Team в импорт
from .views import RoundResultsView
from src.results.admin import MatchResultInline


# --- РЕГИСТРАЦИЯ КОМАНД ---
@admin.register(Team)
class TeamAdmin(ModelAdmin):
    list_display = ("display_logo", "name")
    list_display_links = ("name",)
    search_fields = ("name",)

    @admin.display(description="Логотип")
    def display_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" class="w-8 h-8 object-contain rounded" />', obj.logo.url)
        # Передаем пустую строку или текст аргументом, чтобы удовлетворить метод
        return format_html('<span class="text-gray-400 text-xs">{}</span>', "Нет лого")


class MatchInline(TabularInline):
    model = Match
    extra = 10


@admin.register(Tournament)
class TournamentAdmin(ModelAdmin):
    list_display = (
        "league",
        "name",
        "season",
        "status",
        "starts_at",
        "ends_at",
    )
    list_display_links = ("name",)
    list_filter = ("status", "starts_at")
    search_fields = ("name",)


@admin.register(Round)
class RoundAdmin(ModelAdmin):
    list_display = (
        "tournament",
        "round_number",
        "name",
        "deadline",
        "is_locked",
        "results_button",
    )
    list_display_links = ("name",)
    list_filter = ("tournament", "is_locked")
    search_fields = ("name",)
    inlines = [MatchInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "<int:round_id>/results/",
                self.admin_site.admin_view(
                    RoundResultsView.as_view(model_admin=self)
                ),
                name="round_results",
            ),
        ]
        return custom_urls + urls

    @admin.display(description="Результаты")
    def results_button(self, obj):
        url = reverse("admin:round_results", args=[obj.pk])
        return format_html(
            '<a class="button bg-primary-600 text-white px-3 py-1 rounded text-xs font-medium hover:bg-primary-700 transition-colors" href="{}">Ввести результаты</a>',
            url,
        )


@admin.register(Match)
class MatchAdmin(ModelAdmin):
    list_display = (
        "round",
        "home_team",
        "away_team",
    )
    list_display_links = ("home_team",)
    list_filter = ("round",)

    search_fields = (
        "home_team__name",
        "away_team__name",
    )
    inlines = [MatchResultInline]
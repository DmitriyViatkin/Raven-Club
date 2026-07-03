from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html

from unfold.admin import ModelAdmin, TabularInline

from .models import Tournament, Round, Match
from .views import RoundResultsView  # нужно создать
from src.results.admin import MatchResultInline  # лучше вынести Inline в отдельный файл


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
            '<a class="button" href="{}">Ввести результаты</a>',
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
        "home_team",
        "away_team",
    )

    inlines = [MatchResultInline]
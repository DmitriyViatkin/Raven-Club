from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline

from .models import League, LeagueMember, ScoringRules


# 1. Позволяет редактировать правила начисления очков прямо внутри Лиги
class ScoringRulesInline(TabularInline):
    model = ScoringRules
    extra = 1
    max_num = 1  # Обычно для лиги нужен только один набор правил
    tab = True  # Unfold визуально выделит это во вкладку


# 2. Позволяет видеть и добавлять участников прямо внутри Лиги
class LeagueMemberInline(TabularInline):
    model = LeagueMember
    extra = 3
    autocomplete_fields = ("user",)  # Быстрый поиск пользователя в inline-режиме
    tab = True


@admin.register(League)
class LeagueAdmin(ModelAdmin):
    list_display = (
        "name",
        "slug",
        "is_private",
        "status",
        "create_by",
        "create_at",
    )
    list_display_links = ("name",)
    list_filter = ("status", "is_private", "create_at")
    search_fields = ("name", "slug", "create_by__email", "create_by__username")
    filter_horizontal = ("teams",)
    autocomplete_fields = (
        "create_by",)  # Делает выпадающий список создателя удобным поисковым инпутом

    # Подключаем инлайны (вкладки для участников и правил)
    inlines = [ScoringRulesInline, LeagueMemberInline]

    # Красиво группируем поля лиги в интерфейсе Unfold
    fieldsets = (
        (None, {"fields": ("name", "slug", "logo")}),
        (_("Команди"), {"fields": ("teams",)}),
        # <-- ВОТ ЭТА СТРОКА ОЖИВИТ ВЫБОР КОМАНД
        (_("Descriptions"), {"fields": ("short_description", "full_description")}),
        (_("Settings"), {"fields": ("is_private", "status")}),
        (_("Meta"), {"fields": ("create_by", "create_at")}),
    )


@admin.register(LeagueMember)
class LeagueMemberAdmin(ModelAdmin):
    list_display = ("user", "league", "role", "total_points", "rank", "joined_at")
    list_filter = ("role", "league", "joined_at")
    search_fields = ("user__email", "user__username", "league__name")
    autocomplete_fields = ("user", "league")


@admin.register(ScoringRules)
class ScoringRulesAdmin(ModelAdmin):
    list_display = ("league", "point_exact_score", "point_correct_winner", "created_at")
    list_filter = ("created_at",)
    search_fields = ("league__name",)
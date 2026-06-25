from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from .models import MatchResult


@admin.register(MatchResult)
class MatchResultAdmin(ModelAdmin):
    # 1. Отображение списка
    list_display = (
        "match",
        "score_display",  # Красивое кастомное отображение счета
        "home_scored",
        "away_scored",
        "home_clean_sheet",
        "away_clean_sheet",
        "entered_by",
        "updated_at",
    )

    # 2. Позволяет переключать булевы свойства прямо в общей таблице
    list_editable = (
        "home_scored",
        "away_scored",
        "home_clean_sheet",
        "away_clean_sheet",
    )

    list_filter = (
        "home_scored",
        "away_scored",
        "home_clean_sheet",
        "away_clean_sheet",
        "entered_at"
    )

    # Поиск по названию матча (предполагаем, что у модели Match есть связанные команды или название)
    search_fields = (
        "match__id",
        "match__home_team__name",
        "match__away_team__name",
        "entered_by__email"
    )

    # Живой поиск для связанных объектов
    autocomplete_fields = ("match", "entered_by")

    # Автоматически сохраняем, кто внес или изменил результат
    readonly_fields = ("entered_by", "entered_at", "updated_at")

    # 3. Группировка полей на форме создания/редактирования
    fieldsets = (
        (None, {"fields": ("match",)}),
        (_("Final Score (Full Time)"), {
            "fields": (
                ("home_ft", "away_ft"),  # Две колонки в одну строку
            )
        }),
        (_("Additional Stats"), {
            "fields": (
                ("home_scored", "away_scored"),
                ("home_clean_sheet", "away_clean_sheet"),
            )
        }),
        (_("Audit Logs"), {
            "classes": ("collapse",),  # Сворачиваемый блок
            "fields": ("entered_by", "entered_at", "updated_at"),
        }),
    )

    # Кастомное поле для красивого вывода счета в списке
    @admin.display(description=_("Score (Home - Away)"))
    def score_display(self, obj):
        return f"{obj.home_ft} : {obj.away_ft}"

    # Автоматически подставляем текущего администратора в поле entered_by при сохранении
    def save_model(self, request, obj, form, change):
        if not change:  # Если объект только создается
            obj.entered_by = request.user
        super().save_model(request, obj, form, change)

# Register your models here.

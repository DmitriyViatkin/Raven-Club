from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.forms import UserChangeForm, UserCreationForm

from .models import Player


@admin.register(Player)
class PlayerAdmin(BaseUserAdmin, ModelAdmin):
    # Используем формы Unfold для корректной работы с паролями
    form = UserChangeForm
    add_form = UserCreationForm

    # 1. Настройка списка пользователей в админке
    list_display = ("email", "username", "role", "gender", "language", "is_staff",
                    "is_active")
    list_filter = ("role", "gender", "language", "is_staff", "is_active")
    search_fields = ("email", "username")
    ordering = ("email",)

    # 2. Группировка полей на странице редактирования (Fieldsets)
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email", "avatar", "gender", "language")}),
        (_("Permissions"), {
            "fields": (
                "role",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # Поля, которые запрашиваются при создании пользователя через админку
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password", "role"),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Исключаем всех, у кого флаг is_superuser равен True
        return qs.filter(is_superuser=False)


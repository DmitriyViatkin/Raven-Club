from django import forms
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from src.users.models import Player
from enums.enums import Gender, Language


class UserProfileForm(forms.ModelForm):
    old_password = forms.CharField(
        label="Поточний пароль (для підтвердження)",
        widget=forms.PasswordInput(
            attrs={
                "class": "border border-gray-300 rounded px-3 py-2 w-full",
                "placeholder": "Введіть поточний пароль",
            }
        ),
        required=False,
    )
    new_password = forms.CharField(
        label="Новий пароль (необов'язково)",
        widget=forms.PasswordInput(
            attrs={
                "class": "border border-gray-300 rounded px-3 py-2 w-full",
                "placeholder": "Залишіть порожнім, якщо не хочете змінювати",
            }
        ),
        required=False,
    )

    class Meta:
        model = Player
        fields = ["username", "email", "first_name", "last_name", "language", "gender",
                  "avatar"]

        widgets = {
            "username": forms.TextInput(
                attrs={"class": "border border-gray-300 rounded px-3 py-2 w-full"}),
            "email": forms.EmailInput(
                attrs={"class": "border border-gray-300 rounded px-3 py-2 w-full"}),
            "first_name": forms.TextInput(
                attrs={"class": "border border-gray-300 rounded px-3 py-2 w-full"}),
            "last_name": forms.TextInput(
                attrs={"class": "border border-gray-300 rounded px-3 py-2 w-full"}),
            "language": forms.Select(
                attrs={"class": "border border-gray-300 rounded px-3 py-2 w-full"}),
            "gender": forms.Select(
                attrs={"class": "border border-gray-300 rounded px-3 py-2 w-full"}),
            "avatar": forms.ClearableFileInput(
                attrs={"class": "border border-gray-300 rounded px-3 py-2 w-full"}),
        }

    def clean(self):
        """
        Переопределяем общий метод очистки для зависимой валидации полей.
        """
        cleaned_data = super().clean()
        old_password = cleaned_data.get("old_password")
        new_password = cleaned_data.get("new_password")

        # Если ввели НОВЫЙ пароль, проверяем СТАРЫЙ
        if new_password:
            if not old_password:
                self.add_error("old_password",
                               "Введіть поточний пароль, щоб змінити його.")
            elif not self.instance.check_password(old_password):
                self.add_error("old_password", "Неправильний поточний пароль.")
            else:
                # Проверяем надежность нового пароля стандартными средствами Django
                try:
                    validate_password(new_password, self.instance)
                except ValidationError as e:
                    self.add_error("new_password", e)

        # Если оба поля пустые (меняют только аватар или имя) — просто пропускаем валидацию
        return cleaned_data

    def save(self, commit=True):
        player = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")

        # Хешируем и сохраняем новый пароль только если он был передан
        if new_password:
            player.set_password(new_password)

        if commit:
            player.save()
        return player
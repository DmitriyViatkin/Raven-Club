from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm


class PlayerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("email", "username")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 1. Прибираємо довгу інструкцію до юзернейму
        self.fields['username'].help_text = "Обов'язкове поле. До 150 символів."

        # 2. Прибираємо купу тексту про вимоги до пароля (робимо порожнім)
        self.fields['password1'].help_text = ""
from typing import Any

from django.contrib.auth import login, get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .tasks import  send_password_reset_email_task
from django import forms

class AsyncPasswordResetForm(PasswordResetForm):
    def send_mail(
        self,
        subject_template_name: str,
        email_template_name: str,
        context: dict[str, Any],
        from_email: str | None,
        to_email: str,
        html_email_template_name: str | None = None,
        user_email: str | None = None
    ) -> None:

        context_dict = dict(context)

        if "user" in context_dict:
            del context_dict["user"]

        send_password_reset_email_task.delay(
                                         subject_template_name=subject_template_name,
                                         email_template_name=email_template_name,
                                         context=context_dict,
                                         from_email=from_email,
                                         to_email=to_email,
                                         html_email_template_name=html_email_template_name,
                                             )
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
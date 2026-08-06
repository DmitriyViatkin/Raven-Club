import time
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm


@shared_task
def send_email_task(subject, message, recipient_list):
    """
    Celery task to send an email.
    """


    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
        return f"Email sent to {', '.join(recipient_list)}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"

from django.contrib.auth import get_user_model

@shared_task
def send_password_reset_email_task(subject_template_name: str, email_template_name: str,
                                    context: dict, from_email: str | None, to_email: str,
                                    html_email_template_name: str | None = None,
                                    user_id: int | None = None,
                                    ):
    """
        Асинхронно рендерит и отправляет письмо со ссылкой для сброса пароля.
    """
    if user_id is not None:
        User = get_user_model()
        try:
            context = dict(context)
            context["user"] = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            pass

    PasswordResetForm().send_mail(
        subject_template_name=subject_template_name,
        email_template_name=email_template_name,
        context=context,
        from_email=from_email,
        to_email=to_email,
        html_email_template_name=html_email_template_name
    )
    return f"Password reset email sent to {to_email}"


from django.core.mail import send_mail

from config import settings


def send_auth_code(email: str, auth_code: str) -> None:
    subject = 'Ваш код для активации аккаунта'
    message = f'To activate your account, use this code: {auth_code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

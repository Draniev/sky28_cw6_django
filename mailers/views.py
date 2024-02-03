from django.core.mail import send_mail
from django.shortcuts import render


def test_mail_view(request):
    send_mail('Тестовое письмо',
              'Тело письма',
              'info@bid-trade.ru',
              ['sergan.mail@gmail.com'])

    return render(request, 'mailers/test_mail.html')

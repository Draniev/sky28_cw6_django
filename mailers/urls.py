from django.urls import path

from mailers.apps import MailersConfig
from mailers.views import test_mail_view

app_name = MailersConfig.name

urlpatterns = [
    path('test_mail/', test_mail_view, name='testmail'),
]

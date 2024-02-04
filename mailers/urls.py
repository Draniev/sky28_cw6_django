from django.urls import path

from mailers.apps import MailersConfig
from mailers.views import test_mail_view, new_app, SubscriberListView, SubscriberCreateView, SubscriberUpdateView, \
    SubscriberDeleteView, MailingListListView, MailingListCreateView, MailingListUpdateView, MailingListDeleteView, \
    MessageListView, MessageCreateView, MessageUpdateView, MessageDeleteView, DistributionListView, \
    DistributionCreateView, DistributionUpdateView, DistributionDeleteView, DistributionLogListView

app_name = MailersConfig.name

urlpatterns = [
    path('subscribers/', SubscriberListView.as_view(), name='subscribers'),
    path('subscribers/new/', SubscriberCreateView.as_view(), name='subscriber_create'),
    path('subscribers/<int:pk>/edit/', SubscriberUpdateView.as_view(), name='subscriber_edit'),
    path('subscribers/<int:pk>/delete/', SubscriberDeleteView.as_view(), name='subscriber_delete'),
    path('mailing-lists/', MailingListListView.as_view(), name='mailing_lists'),
    path('mailing-lists/new/', MailingListCreateView.as_view(), name='mailing_list_create'),
    path('mailing-lists/<int:pk>/edit/', MailingListUpdateView.as_view(), name='mailing_list_edit'),
    path('mailing-lists/<int:pk>/delete/', MailingListDeleteView.as_view(), name='mailing_list_delete'),
    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/new/', MessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/edit/', MessageUpdateView.as_view(), name='message_edit'),
    path('messages/<int:pk>/delete/', MessageDeleteView.as_view(), name='message_delete'),
    path('distributions/', DistributionListView.as_view(), name='distribution_list'),
    path('distributions/create/', DistributionCreateView.as_view(), name='distribution_create'),
    path('distributions/<int:pk>/edit/', DistributionUpdateView.as_view(), name='distribution_edit'),
    path('distributions/<int:pk>/delete/', DistributionDeleteView.as_view(), name='distribution_delete'),
    path('distributionslogs/', DistributionLogListView.as_view(), name='distributionlog_list'),
    path('test_mail/', test_mail_view, name='testmail'),
    path('app/', new_app, name='app'),
]

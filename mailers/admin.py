from django.contrib import admin

from mailers.models import Subscriber, MailingList, Message, Distribution


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('owner', 'email', 'first_name', 'last_name',)
    list_filter = ('owner', 'email',)
    search_fields = ('email',)


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name',)
    list_filter = ('owner',)


@admin.register(Message)
class MessageListAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title',)
    list_filter = ('owner',)


@admin.register(Distribution)
class DistributionAdmin(admin.ModelAdmin):
    list_display = ('owner',
                    'message',
                    'mailing_list',
                    'start_time',
                    'stop_time',
                    'periodicity',
                    'mailing_day',
                    'mailing_time',
                    'status',
                    )
    list_filter = ('owner', 'status')

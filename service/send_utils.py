import calendar

from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from mailers.models import Distribution, Message, DistributionLog, MailingList


def send_auth_code(email: str, auth_code: str) -> None:
    subject = 'Ваш код для активации аккаунта'
    body = f'To activate your account, use this code: {auth_code}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, body, from_email, recipient_list)


def send_message_for_list(mailinglist: MailingList, message: Message):
    for subscriber in mailinglist.subscribers.all():
        subject = message.title
        body = message.body
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [subscriber.email]

        send_mail(subject, body, from_email, recipient_list)
        subscriber.datetime_last_message = timezone.now()
        subscriber.save()


def is_last_day_of_month():
    today = timezone.now().date()
    _, last_day = calendar.monthrange(today.year, today.month)

    return today.day == last_day


def is_it_time_to_sent(distribution: Distribution) -> bool:
    last_task = DistributionLog.objects.filter(distribution=distribution).first()
    last_task_date = last_task.task_start_date.date() if last_task else None
    today_time = timezone.now().time()
    today_date = timezone.now().date()
    today_weekday = timezone.now().date().weekday() + 1  # В модели считаю от "1" а не от нуля
    mailing_time = distribution.get_mailing_time()

    if distribution.periodicity == Distribution.Periodicity.ONCE:
        if not last_task:
            if today_time > mailing_time:
                return True

    elif distribution.periodicity == Distribution.Periodicity.DAY:
        # Execute this branch if it hasn't run yet today,
        # and if the current time is greater than the
        # distribution time
        if ((not last_task or last_task_date < today_date)
                and today_time > mailing_time):
            return True

    elif distribution.periodicity == Distribution.Periodicity.WEEK:
        # Execute this branch if it has not already been executed
        # today and if today's weekday number matches mailing_day
        if not last_task or last_task_date < today_date:
            if today_weekday == distribution.mailing_day and today_time > mailing_time:
                return True

    elif distribution.periodicity == Distribution.Periodicity.MONTH:
        # Execute this branch if it has not already been executed today
        # and if today's day number changes to mailing_day
        if not last_task or last_task_date < today_date:
            if (distribution.mailing_day == today_date.day() or
                    (distribution.mailing_day > today_date.day() and is_last_day_of_month())):
                if today_time > mailing_time:
                    return True

    else:
        return False


def send_distribution(distribution: Distribution) -> bool:
    """
    Processes the Distribution model, and if it's the right time,
    sends emails to the distribution list.
    return:
        - TRUE if distribution was send
        - FALSE if the time hasn't come yet.
    """
    if is_it_time_to_sent(distribution):
        send_message_for_list(distribution.mailing_list, distribution.message)
        print(f'Отправили рассылку {distribution}')
        log = DistributionLog(owner=distribution.owner,
                              distribution=distribution,
                              task_start_date=timezone.now(),
                              emails_qty=distribution.mailing_list.subscribers.count(),
                              )
        log.save()
        return True

    else:
        return False

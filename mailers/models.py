import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()


class Subscriber(models.Model):
    """
    Модель ПОДПИСЧИКА. Подписчиков добавляют себе в базу пользователи
    системы. И рассылают подписчикам рассылки. Каждый подписчик
    принадлежит конкретному пользователю и только ему. Но другой
    пользователь может иметь в своей базе подписчика с такой-же
    электронной почтой.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    first_name = models.CharField(max_length=64, default='')
    last_name = models.CharField(max_length=64, default='')
    datetime_added = models.DateTimeField(auto_now_add=True)
    datetime_last_message = models.DateTimeField(default=None)

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'


class MailingList(models.Model):
    """
    Модель СПИСКА РАССЫЛКИ. Пользователь системы создаёт любое кол-во
    списков рассылки, куда включает своих подписчиков по необходимости.
    Рассылка отправляется, соответственно, по списку рассылки.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(Subscriber)

    class Meta:
        verbose_name = 'База для рассылок'
        verbose_name_plural = 'Базы для рассылок'


class Message(models.Model):
    """
    Модель СООБЩЕНИЯ для рассылки. Включает в себя:
    - тему письма
    - тело письма
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=1024, default='')
    body = models.TextField(default='')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Distribution(models.Model):
    """
    Модель РАССЫЛКИ. Включает в себя:
    - сообщение
    - список рассылки
    - параметры рассылки (дату начала и окончания?)
    - периодичность рассылки (один раз, раз в день, раз в неделю, рез в месяц)
    - состояние (новый, запущена, остановлена)
    """
    class Periodicity(models.TextChoices):
        DAY = 'da', 'every day'
        WEEK = 'we', 'every week'
        MONTH = 'mo', 'every month'
        ONCE = 'on', 'only once'

    class Status(models.TextChoices):
        NEW = 'new', 'new one'
        STARTED = 'on', 'Its up and running'
        STOPPED = 'off', 'Stopped'

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.PROTECT)
    start_time = models.DateTimeField(default=timezone.now)
    stop_time = models.DateTimeField(default=None)
    status = models.CharField(max_length=3, choices=Status, default=Status.NEW)
    periodicity = models.CharField(max_length=2, choices=Periodicity, default=Periodicity.ONCE)
    # День отправки сообщения.
    # Для ЕЖЕНЕДЕЛЬНОЙ отправки 1-Пн, 2-Вт, и т.д. 7-Вс
    # Для ЕЖЕМЕСЯЧНОЙ отправки, 1-31 число, либо последний день месяца
    # Для ежедневной и одноразовой рассылки не учитывается
    mailing_day = models.PositiveSmallIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1, 'Делать дела лучше с понедельника'),
                    MaxValueValidator(31, '32 мая оставим для Мюнхаузена!')],
    )
    # Время отправки письма для рассылки. Если время не указано, то
    # отправка сразу после start_time
    mailing_time = models.TimeField(default=None)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class DistributionLog(models.Model):
    """
    Модель для хранения ЛОГОВ рассылки с результатами.
    Пока не знаю, будет ли лог по каждому подписчику или по
    рассылке в целом.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

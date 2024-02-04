from django.core.management.base import BaseCommand
from mailers.models import Distribution
from django.utils import timezone

from service.send_utils import send_distribution


class Command(BaseCommand):
    help = 'Send distributions with STARTED status and start_time > current date'

    def handle(self, *args, **options):
        distributions = Distribution.objects.filter(
            status=Distribution.Status.STARTED,
            start_time__lt=timezone.now()
        )

        for distribution in distributions:
            if_sent = send_distribution(distribution)
            self.stdout.write(self.style.SUCCESS(f'{}Обработано {distribution.owner} - {distribution}'))

        self.stdout.write(self.style.SUCCESS(f'{timezone.now()} - Successfully ran the command'))

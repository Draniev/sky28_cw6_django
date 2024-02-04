# Generated by Django 5.0.1 on 2024-02-04 09:26

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailers', '0004_alter_subscriber_datetime_last_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='distributionlog',
            name='distribution',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mailers.distribution'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='distributionlog',
            name='emails_qty',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='distributionlog',
            name='task_start_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

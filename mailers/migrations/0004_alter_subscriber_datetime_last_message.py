# Generated by Django 5.0.1 on 2024-02-03 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailers', '0003_alter_subscriber_options_distribution_mailing_list_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='datetime_last_message',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]

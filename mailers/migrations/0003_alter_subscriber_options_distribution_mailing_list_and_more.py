# Generated by Django 5.0.1 on 2024-02-02 15:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailers', '0002_alter_distribution_options_alter_mailinglist_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriber',
            options={'ordering': ('datetime_added', 'email'), 'verbose_name': 'Подписчик', 'verbose_name_plural': 'Подписчики'},
        ),
        migrations.AddField(
            model_name='distribution',
            name='mailing_list',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='mailers.mailinglist'),
        ),
        migrations.AddField(
            model_name='mailinglist',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='Название списка'),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='Электронная почта'),
        ),
    ]

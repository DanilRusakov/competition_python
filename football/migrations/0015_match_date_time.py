# Generated by Django 3.0.5 on 2020-04-26 14:41

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0014_auto_20200426_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='date_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]

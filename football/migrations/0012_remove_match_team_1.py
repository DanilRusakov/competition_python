# Generated by Django 3.0.5 on 2020-04-26 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0011_match_team_1'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='team_1',
        ),
    ]

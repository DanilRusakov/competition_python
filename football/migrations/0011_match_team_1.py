# Generated by Django 3.0.5 on 2020-04-26 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0010_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='team_1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Team_1', to='football.Team'),
        ),
    ]

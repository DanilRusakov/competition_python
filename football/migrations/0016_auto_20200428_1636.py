# Generated by Django 3.0.5 on 2020-04-28 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0015_match_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Pending'), (1, 'Done')], default=0),
        ),
        migrations.AlterField(
            model_name='match',
            name='team_1_goals',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='match',
            name='team_2_goals',
            field=models.SmallIntegerField(default=0),
        ),
    ]

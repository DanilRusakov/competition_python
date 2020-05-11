# Generated by Django 3.0.5 on 2020-04-26 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0009_auto_20200411_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('team_1_goals', models.IntegerField(default=0)),
                ('team_2_goals', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Match',
                'verbose_name_plural': 'Matches',
            },
        ),
    ]
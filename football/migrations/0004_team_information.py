# Generated by Django 3.0.4 on 2020-04-08 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0003_auto_20200406_0703'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='information',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]

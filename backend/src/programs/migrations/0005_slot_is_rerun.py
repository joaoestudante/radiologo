# Generated by Django 3.0.8 on 2020-07-12 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0004_auto_20200708_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='is_rerun',
            field=models.BooleanField(default=False),
        ),
    ]

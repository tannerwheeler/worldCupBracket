# Generated by Django 2.0.2 on 2018-05-17 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bracket', '0011_auto_20180517_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='usergroup',
            name='editBracket',
            field=models.BooleanField(default=False),
        ),
    ]
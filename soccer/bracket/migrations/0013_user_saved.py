# Generated by Django 2.0.2 on 2018-05-18 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bracket', '0012_usergroup_editbracket'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='saved',
            field=models.BooleanField(default=False),
        ),
    ]

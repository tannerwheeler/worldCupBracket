# Generated by Django 2.0.2 on 2018-05-12 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bracket', '0004_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fourth',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='second',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
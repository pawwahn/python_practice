# Generated by Django 2.2.1 on 2019-05-07 12:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flight',
            name='distance',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]

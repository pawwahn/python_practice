# Generated by Django 2.2.1 on 2019-06-12 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flights', '0005_passenger'),
    ]

    operations = [
        migrations.CreateModel(
            name='Courier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=24)),
            ],
        ),
    ]